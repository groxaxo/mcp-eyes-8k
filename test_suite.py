#!/usr/bin/env python3
"""
Test script to validate MCP Eyes 8K functionality.
This script tests the code without requiring actual API calls.
"""

import os
import sys
from pathlib import Path

# Set up environment
os.environ["VISION_BASE_DIR"] = str(Path(__file__).parent / "test_images")
os.environ["VISION_MODEL"] = "gpt-4o"

# Import the module
from active_vision import (
    _validate_path,
    _process_image,
    _normalize_content,
    _adjust_coordinates,
    _repair_json,
    examine_image,
    BASE_DIR
)

def test_path_validation():
    """Test the path validation function."""
    print("\n" + "="*60)
    print("TEST 1: Path Validation")
    print("="*60)
    
    # Test valid path
    test_img = os.path.join(BASE_DIR, "ui_test.png")
    try:
        result = _validate_path(test_img)
        print(f"✓ Valid path test passed: {result}")
    except Exception as e:
        print(f"✗ Valid path test failed: {e}")
    
    # Test invalid path (outside base dir)
    try:
        _validate_path("/etc/passwd")
        print("✗ Invalid path test failed: Should have raised PermissionError")
    except PermissionError as e:
        print(f"✓ Invalid path test passed: {e}")
    
    # Test non-existent file
    try:
        _validate_path(os.path.join(BASE_DIR, "nonexistent.png"))
        print("✗ Non-existent file test failed: Should have raised FileNotFoundError")
    except FileNotFoundError as e:
        print(f"✓ Non-existent file test passed: {e}")

def test_image_processing():
    """Test image processing functionality."""
    print("\n" + "="*60)
    print("TEST 2: Image Processing")
    print("="*60)
    
    test_img = os.path.join(BASE_DIR, "ui_test.png")
    
    # Test without region
    try:
        b64, mime, orig_size, crop_bbox, sent_size = _process_image(test_img, None, "ui")
        print(f"✓ Image processing (no region) passed:")
        print(f"  - MIME type: {mime}")
        print(f"  - Original size: {orig_size}")
        print(f"  - Crop bbox: {crop_bbox}")
        print(f"  - Sent size: {sent_size}")
        print(f"  - Base64 length: {len(b64)}")
    except Exception as e:
        print(f"✗ Image processing (no region) failed: {e}")
    
    # Test with region
    try:
        region = [100, 100, 400, 300]
        b64, mime, orig_size, crop_bbox, sent_size = _process_image(test_img, region, "ocr")
        print(f"✓ Image processing (with region) passed:")
        print(f"  - MIME type: {mime}")
        print(f"  - Original size: {orig_size}")
        print(f"  - Crop bbox: {crop_bbox}")
        print(f"  - Sent size: {sent_size}")
    except Exception as e:
        print(f"✗ Image processing (with region) failed: {e}")

def test_normalize_content():
    """Test content normalization."""
    print("\n" + "="*60)
    print("TEST 3: Content Normalization")
    print("="*60)
    
    # Test string input
    result = _normalize_content("Hello World")
    print(f"✓ String input: '{result}'")
    
    # Test list input
    result = _normalize_content(["Line 1", "Line 2", {"text": "Line 3"}])
    print(f"✓ List input: '{result}'")
    
    # Test None input
    result = _normalize_content(None)
    print(f"✓ None input: '{result}'")
    
    # Test dict input
    result = _normalize_content({"text": "Test", "other": "data"})
    print(f"✓ Dict input: '{result}'")

def test_coordinate_adjustment():
    """Test coordinate adjustment logic."""
    print("\n" + "="*60)
    print("TEST 4: Coordinate Adjustment")
    print("="*60)
    
    # Test data
    result = {
        "elements": [
            {"type": "button", "label": "Test", "bbox": [0.1, 0.2, 0.3, 0.4]},
            {"type": "input", "label": "Input", "bbox": [100, 150, 200, 180]}
        ],
        "text_blocks": [
            {"text": "Hello", "bbox": [50, 60, 150, 80]}
        ]
    }
    
    crop_bbox = (0, 0, 800, 600)
    sent_size = (800, 600)
    orig_size = (800, 600)
    
    _adjust_coordinates(result, crop_bbox, sent_size, orig_size)
    
    print(f"✓ Coordinate adjustment completed:")
    print(f"  - Element 1 bbox: {result['elements'][0]['bbox']}")
    print(f"  - Element 2 bbox: {result['elements'][1]['bbox']}")
    print(f"  - Text block bbox: {result['text_blocks'][0]['bbox']}")

def test_json_repair():
    """Test JSON repair functionality."""
    print("\n" + "="*60)
    print("TEST 5: JSON Repair")
    print("="*60)
    
    # Test valid JSON string
    valid_json = '{"status": "ok", "data": [1, 2, 3]}'
    result = _repair_json(valid_json, "gpt-4o")
    print(f"✓ Valid JSON: {result}")
    
    # Test JSON with markdown
    markdown_json = '```json\n{"status": "ok"}\n```'
    result = _repair_json(markdown_json, "gpt-4o")
    print(f"✓ Markdown JSON: {result}")
    
    # Test dict input
    dict_input = {"already": "parsed"}
    result = _repair_json(dict_input, "gpt-4o")
    print(f"✓ Dict input: {result}")
    
    # Test list input (should be normalized)
    list_input = [{"text": "item1"}, "item2"]
    result = _repair_json(list_input, "gpt-4o")
    print(f"✓ List input: {result}")

def test_examine_image_validation():
    """Test examine_image input validation."""
    print("\n" + "="*60)
    print("TEST 6: examine_image Input Validation")
    print("="*60)
    
    # Test invalid mode
    result = examine_image("/tmp/test.png", mode="invalid")
    if "error" in result and "Invalid mode" in result["error"]:
        print(f"✓ Invalid mode test passed: {result['error']}")
    else:
        print(f"✗ Invalid mode test failed: {result}")
    
    # Test query mode without question
    result = examine_image("/tmp/test.png", mode="query")
    if "error" in result and "question" in result["error"]:
        print(f"✓ Query without question test passed: {result['error']}")
    else:
        print(f"✗ Query without question test failed: {result}")
    
    # Test with invalid path
    result = examine_image("/etc/passwd", mode="general")
    if "error" in result:
        print(f"✓ Invalid path test passed: {result['error']}")
    else:
        print(f"✗ Invalid path test failed: {result}")

def test_all_modes():
    """Test all modes with actual test images (will fail without API key)."""
    print("\n" + "="*60)
    print("TEST 7: All Modes (Note: Will fail without API key)")
    print("="*60)
    
    modes = [
        ("ui", "ui_test.png", None),
        ("ocr", "ocr_test.png", None),
        ("general", "general_test.png", None),
        ("query", "query_test.png", "What shapes are in this image?")
    ]
    
    for mode, image, question in modes:
        test_path = os.path.join(BASE_DIR, image)
        print(f"\nTesting {mode} mode with {image}...")
        
        if mode == "query":
            result = examine_image(test_path, mode=mode, question=question)
        else:
            result = examine_image(test_path, mode=mode)
        
        if "error" in result:
            print(f"  ⚠ {mode} mode returned error: {result['error']}")
        else:
            print(f"  ✓ {mode} mode completed successfully")
            print(f"    Metadata: {result.get('metadata', {})}")
            print(f"    Content keys: {list(result.get('content', {}).keys())}")

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("MCP Eyes 8K - Test Suite")
    print("="*60)
    print(f"Base directory: {BASE_DIR}")
    print(f"Python version: {sys.version}")
    
    try:
        test_path_validation()
        test_image_processing()
        test_normalize_content()
        test_coordinate_adjustment()
        test_json_repair()
        test_examine_image_validation()
        test_all_modes()
        
        print("\n" + "="*60)
        print("Test Suite Completed!")
        print("="*60)
        print("\nNote: Tests requiring API calls will fail without valid API keys.")
        print("To run full tests, set OPENAI_API_KEY environment variable.")
        
    except Exception as e:
        print(f"\n✗ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
