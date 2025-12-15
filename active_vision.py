import os
import json
import base64
import hashlib
import re
import time
import threading
from io import BytesIO
from typing import Optional, List, Dict, Any, Tuple, Union
from collections import OrderedDict

from PIL import Image, ImageOps
from mcp.server.fastmcp import FastMCP
from litellm import completion
import litellm.exceptions

# --- CONFIGURATION ---
MODEL_NAME = os.getenv("VISION_MODEL", "gpt-4o")
REPAIR_MODEL = os.getenv("VISION_REPAIR_MODEL", MODEL_NAME)

BASE_DIR = os.getenv("VISION_BASE_DIR", os.getcwd()) 
MAX_FILE_SIZE_MB = 20
CACHE_TTL = 300  # 5 minutes
CACHE_MAX_SIZE = 100
PROMPT_VERSION = "v1.5" 

ALLOWED_MODES = {"ui", "ocr", "general", "query"}

mcp = FastMCP("Active Vision Adamant")

# --- THREAD-SAFE LRU CACHE ---
class TTLCache:
    def __init__(self, max_size: int, ttl: int):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl
        self.lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                return None
            data, timestamp = self.cache[key]
            if time.time() - timestamp > self.ttl:
                del self.cache[key]
                return None
            self.cache.move_to_end(key)
            return data

    def set(self, key: str, value: Any):
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = (value, time.time())
            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False)

_CACHE = TTLCache(CACHE_MAX_SIZE, CACHE_TTL)

# --- HELPERS ---

def _validate_path(path: str) -> str:
    """Securely validates path is within BASE_DIR using strict resolution."""
    abs_path = os.path.realpath(os.path.abspath(path))
    base_abs = os.path.realpath(os.path.abspath(BASE_DIR))

    try:
        if os.path.commonpath([base_abs, abs_path]) != base_abs:
            raise PermissionError("Access denied: Path outside strict base directory.")
    except ValueError:
         raise PermissionError("Access denied: Path on different drive.")

    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"File not found: {path}")
        
    if os.path.getsize(abs_path) > (MAX_FILE_SIZE_MB * 1024 * 1024):
        raise ValueError(f"File too large (> {MAX_FILE_SIZE_MB}MB)")
        
    return abs_path

def _process_image(path: str, region: Optional[List[int]], mode: str):
    """
    Loads, crops, resizes, and encodes.
    Returns: (b64, mime, orig_size, crop_bbox, sent_size)
    """
    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img)
        orig_w, orig_h = img.size

        # 1. Crop Logic
        if region:
            x1, y1, x2, y2 = region
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(orig_w, x2), min(orig_h, y2)
            if x2 <= x1 or y2 <= y1:
                raise ValueError(f"Invalid region {region} for image size {orig_w}x{orig_h}")
            crop_bbox = (x1, y1, x2, y2)
            img = img.crop(crop_bbox)
        else:
            crop_bbox = (0, 0, orig_w, orig_h)

        # 2. Resize Logic
        max_dim = 2560 if mode in ["ocr", "ui"] else 1536
        if max(img.size) > max_dim:
            img.thumbnail((max_dim, max_dim))
        
        sent_w, sent_h = img.size 

        # 3. Encoding Logic
        buffer = BytesIO()
        if mode in ["ocr", "ui"]:
            mime = "image/png"
            img.save(buffer, format="PNG", optimize=True)
        else:
            mime = "image/jpeg"
            if img.mode in ("RGBA", "LA"):
                bg = Image.new("RGB", img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[-1])
                img = bg
            elif img.mode != "RGB":
                img = img.convert("RGB")
            img.save(buffer, format="JPEG", quality=85, optimize=True)

        return (
            base64.b64encode(buffer.getvalue()).decode("utf-8"),
            mime,
            (orig_w, orig_h),
            crop_bbox,
            (sent_w, sent_h)
        )

def _normalize_content(content: Any) -> str:
    """Safely converts diverse provider outputs (lists, dicts, None) to string."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                parts.append(str(item.get("text", item)))
            else:
                parts.append(str(item))
        return "\n".join(parts)
    return str(content)

def _adjust_coordinates(result: Dict, crop_bbox: Tuple[int,int,int,int], sent_size: Tuple[int,int], orig_size: Tuple[int,int]):
    """
    Maps relative VLM coordinates -> Absolute Original coordinates.
    Handles normalization detection, sorting, rounding, and safe-clamping.
    """
    crop_x1, crop_y1, crop_x2, crop_y2 = crop_bbox
    crop_w = crop_x2 - crop_x1
    crop_h = crop_y2 - crop_y1
    sent_w, sent_h = sent_size
    orig_w, orig_h = orig_size
    
    # 0-indexed max boundaries for click safety
    max_x_safe = max(0, orig_w - 1)
    max_y_safe = max(0, orig_h - 1)

    sx = crop_w / max(sent_w, 1)
    sy = crop_h / max(sent_h, 1)

    def sanitize_and_map(bbox):
        if not isinstance(bbox, list) or len(bbox) != 4:
            return bbox
        
        try:
            raw_coords = [float(x) for x in bbox]
            
            # Heuristic: If largest value <= 1.5, treat as normalized (0.0-1.0)
            if max(raw_coords) <= 1.5:
                raw_coords[0] *= sent_w
                raw_coords[1] *= sent_h
                raw_coords[2] *= sent_w
                raw_coords[3] *= sent_h

            # Map Sent-Coords -> Crop-Coords -> Original-Coords
            x1 = crop_x1 + (raw_coords[0] * sx)
            y1 = crop_y1 + (raw_coords[1] * sy)
            x2 = crop_x1 + (raw_coords[2] * sx)
            y2 = crop_y1 + (raw_coords[3] * sy)

            # Sort coordinates
            final_x1, final_x2 = sorted((x1, x2))
            final_y1, final_y2 = sorted((y1, y2))

            # Round and Clamp
            return [
                int(round(max(0, min(final_x1, max_x_safe)))),
                int(round(max(0, min(final_y1, max_y_safe)))),
                int(round(max(0, min(final_x2, max_x_safe)))),
                int(round(max(0, min(final_y2, max_y_safe))))
            ]
        except (ValueError, TypeError):
            return bbox 

    if "elements" in result:
        for el in result["elements"]:
            if "bbox" in el: el["bbox"] = sanitize_and_map(el["bbox"])
            
    if "text_blocks" in result:
        for blk in result["text_blocks"]:
            if "bbox" in blk: blk["bbox"] = sanitize_and_map(blk["bbox"])

def _repair_json(raw_input: Union[str, Dict, List, None], model: str) -> Dict:
    """Robust JSON extraction/repair with internal content normalization."""
    
    # 1. Handle pre-parsed Dict
    if isinstance(raw_input, dict):
        return raw_input
    
    # 2. Normalize input to String (handles List/None)
    raw_text = _normalize_content(raw_input)

    # 3. Slice method
    try:
        start = raw_text.find('{')
        end = raw_text.rfind('}')
        if start != -1 and end != -1:
            return json.loads(raw_text[start:end+1])
    except:
        pass

    # 4. LLM Repair (Truncated)
    try:
        truncated_text = raw_text[:8000]
        response = completion(
            model=model,
            temperature=0,
            top_p=1,
            messages=[{
                "role": "system", 
                "content": "You are a JSON fixer. Return ONLY valid JSON. No markdown."
            }, {
                "role": "user", 
                "content": truncated_text
            }]
        )
        
        # Normalize response content (handle lists/None from repair model)
        repaired_content = _normalize_content(response.choices[0].message.content)
        
        cleaned = re.sub(r"```json|```", "", repaired_content).strip()
        start = cleaned.find('{')
        end = cleaned.rfind('}')
        if start != -1 and end != -1:
             return json.loads(cleaned[start:end+1])
        return json.loads(cleaned)
    except Exception:
        return {"error": "JSON Parse Failed", "raw_output": raw_text[:500] + "..."}

# --- TOOL ---

@mcp.tool()
def examine_image(
    path: str, 
    mode: str = "general", 
    question: Optional[str] = None, 
    region: Optional[List[int]] = None
) -> Dict[str, Any]:
    """
    Analyzes an image.
    
    Args:
        path: Absolute local path.
        mode: 'ui' (elements), 'ocr' (text), 'general' (describe), 'query' (QA).
        question: Required if mode='query'.
        region: [x1, y1, x2, y2] pixel crop.
    """
    try:
        # 1. Strict Validation
        if mode not in ALLOWED_MODES:
             return {"error": f"Invalid mode '{mode}'. Allowed: {sorted(list(ALLOWED_MODES))}", "path": path}

        if mode == "query" and not question:
             return {"error": "Parameter 'question' is required when mode='query'", "path": path}

        safe_path = _validate_path(path)
        region_norm = [int(c) for c in region] if region else None

        # 2. Cache Lookup
        mtime = os.path.getmtime(safe_path)
        cache_key_str = f"{safe_path}|{mtime}|{mode}|{question}|{json.dumps(region_norm)}|{PROMPT_VERSION}"
        cache_key = hashlib.md5(cache_key_str.encode()).hexdigest()
        
        cached = _CACHE.get(cache_key)
        if cached: return cached

        # 3. Processing
        b64_img, mime, orig_size, crop_bbox, sent_size = _process_image(safe_path, region_norm, mode)

        # 4. Prompting
        schemas = {
            "ui": "JSON: { \"elements\": [ { \"type\": \"button|input\", \"label\": string, \"bbox\": [x1,y1,x2,y2] } ], \"uncertainties\": [string] }",
            "ocr": "JSON: { \"text_blocks\": [ { \"text\": string, \"bbox\": [x1,y1,x2,y2] } ], \"uncertainties\": [string] }",
            "query": f"Question: {question}. JSON: {{ \"answer\": string, \"evidence\": [string], \"uncertainties\": [string] }}",
            "general": "JSON: { \"description\": string, \"main_objects\": [string], \"uncertainties\": [string] }"
        }
        
        system_prompt = (
            "You are a machine vision engine. Output strict JSON only. "
            f"Mode: {mode.upper()}. {schemas.get(mode, schemas['general'])} "
            f"Image is {sent_size[0]}x{sent_size[1]}. Coordinates must be relative to this size."
        )

        user_content_text = "Analyze."
        if mode == "query" and question:
             user_content_text = f"Answer this question strictly based on the image: {question}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": user_content_text},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64_img}"}}
            ]}
        ]

        # 5. Inference
        try:
            response = completion(
                model=MODEL_NAME,
                messages=messages,
                temperature=0, 
                top_p=1,
                response_format={"type": "json_object"}
            )
        except litellm.exceptions.UnsupportedParamsError:
            response = completion(model=MODEL_NAME, messages=messages, temperature=0, top_p=1)
        except Exception as e:
            # Broad fallback for any provider rejection of structured outputs
            msg = str(e).lower()
            if any(k in msg for k in ("response_format", "unsupported", "bad request", "invalid_request")):
                response = completion(model=MODEL_NAME, messages=messages, temperature=0, top_p=1)
            else:
                raise e
        
        # 6. Repair & Normalize
        # Pass raw content (string/list/none) directly to repair, which now handles normalization
        result_json = _repair_json(response.choices[0].message.content, REPAIR_MODEL)

        _adjust_coordinates(result_json, crop_bbox, sent_size, orig_size)

        envelope = {
            "mode": mode,
            "metadata": {
                "original_path": path,
                "original_size": {"width": orig_size[0], "height": orig_size[1]},
                "crop_bbox": list(crop_bbox) if region else None,
                "sent_size": {"width": sent_size[0], "height": sent_size[1]},
                "prompt_version": PROMPT_VERSION
            },
            "content": result_json
        }
        
        _CACHE.set(cache_key, envelope)
        return envelope

    except Exception as e:
        return {"error": str(e), "path": path}

if __name__ == "__main__":
    mcp.run()
