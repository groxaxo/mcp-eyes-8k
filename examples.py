#!/usr/bin/env python3
"""
Example script demonstrating how to use the MCP Eyes 8K server.

This shows various ways to analyze images using different modes.
"""

import json
from active_vision import examine_image

def print_result(title: str, result: dict):
    """Pretty print results."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(json.dumps(result, indent=2))


def main():
    """Run example analyses."""
    
    # Example 1: General image description
    print("\n🌅 Example 1: General Image Description")
    print("   Analyzes an image and provides a general description")
    # Uncomment and modify path when you have an image to test:
    # result = examine_image(
    #     path="/path/to/your/image.jpg",
    #     mode="general"
    # )
    # print_result("General Description", result)
    
    # Example 2: OCR - Extract text
    print("\n📝 Example 2: OCR Text Extraction")
    print("   Extracts all text from an image with bounding boxes")
    # result = examine_image(
    #     path="/path/to/screenshot.png",
    #     mode="ocr"
    # )
    # print_result("OCR Results", result)
    
    # Example 3: UI element detection
    print("\n🎯 Example 3: UI Element Detection")
    print("   Detects interactive UI elements (buttons, inputs, etc.)")
    # result = examine_image(
    #     path="/path/to/ui-screenshot.png",
    #     mode="ui"
    # )
    # print_result("UI Elements", result)
    
    # Example 4: Visual Q&A
    print("\n🔍 Example 4: Visual Question Answering")
    print("   Ask specific questions about image content")
    # result = examine_image(
    #     path="/path/to/photo.jpg",
    #     mode="query",
    #     question="What is the main subject of this image?"
    # )
    # print_result("Q&A Result", result)
    
    # Example 5: Region-specific analysis
    print("\n✂️  Example 5: Region-Specific Analysis")
    print("   Analyze only a specific region of a larger image")
    # result = examine_image(
    #     path="/path/to/large-image.png",
    #     mode="general",
    #     region=[100, 100, 500, 500]  # [x1, y1, x2, y2]
    # )
    # print_result("Region Analysis", result)
    
    print("\n" + "="*60)
    print("  To run these examples:")
    print("  1. Uncomment the example you want to try")
    print("  2. Update the image paths")
    print("  3. Make sure your API keys are set")
    print("  4. Run: python examples.py")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
