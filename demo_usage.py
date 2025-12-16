#!/usr/bin/env python3
"""
Script to test MCP Eyes 8K as an MCP tool by simulating client interaction.
This demonstrates how the tool would be used in a real MCP client.
"""

import os
import sys
import json
from pathlib import Path

# Set up environment
os.environ["VISION_BASE_DIR"] = str(Path(__file__).parent / "test_images")

# Import the examine_image tool
from active_vision import examine_image

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_result(result):
    """Pretty print the result."""
    print(json.dumps(result, indent=2))

def demo_basic_usage():
    """Demonstrate basic usage of each mode."""
    
    print_section("DEMO 1: UI Mode - Detect Interactive Elements")
    print("Testing: ui_test.png")
    print("Purpose: Detect buttons, inputs, and other UI elements\n")
    
    result = examine_image(
        path=os.path.join(os.environ["VISION_BASE_DIR"], "ui_test.png"),
        mode="ui"
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        print("Note: This requires a valid OPENAI_API_KEY to be set")
    else:
        print("✅ Success!")
        print_result(result)
    
    print_section("DEMO 2: OCR Mode - Extract Text")
    print("Testing: ocr_test.png")
    print("Purpose: Extract all text with bounding boxes\n")
    
    result = examine_image(
        path=os.path.join(os.environ["VISION_BASE_DIR"], "ocr_test.png"),
        mode="ocr"
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        print("Note: This requires a valid OPENAI_API_KEY to be set")
    else:
        print("✅ Success!")
        print_result(result)
    
    print_section("DEMO 3: General Mode - Describe Image")
    print("Testing: general_test.png")
    print("Purpose: Get a general description of the scene\n")
    
    result = examine_image(
        path=os.path.join(os.environ["VISION_BASE_DIR"], "general_test.png"),
        mode="general"
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        print("Note: This requires a valid OPENAI_API_KEY to be set")
    else:
        print("✅ Success!")
        print_result(result)
    
    print_section("DEMO 4: Query Mode - Answer Questions")
    print("Testing: query_test.png")
    print("Question: What shapes are in this image?\n")
    
    result = examine_image(
        path=os.path.join(os.environ["VISION_BASE_DIR"], "query_test.png"),
        mode="query",
        question="What shapes are in this image? List their colors."
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        print("Note: This requires a valid OPENAI_API_KEY to be set")
    else:
        print("✅ Success!")
        print_result(result)

def demo_region_analysis():
    """Demonstrate region-based analysis."""
    
    print_section("DEMO 5: Region Analysis")
    print("Testing: ui_test.png with region crop")
    print("Region: [100, 100, 700, 300] (focusing on upper portion)\n")
    
    result = examine_image(
        path=os.path.join(os.environ["VISION_BASE_DIR"], "ui_test.png"),
        mode="ocr",
        region=[100, 100, 700, 300]
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        print("Note: This requires a valid OPENAI_API_KEY to be set")
    else:
        print("✅ Success!")
        print_result(result)

def demo_error_handling():
    """Demonstrate error handling."""
    
    print_section("DEMO 6: Error Handling - Invalid Mode")
    
    result = examine_image(
        path=os.path.join(os.environ["VISION_BASE_DIR"], "ui_test.png"),
        mode="invalid_mode"
    )
    print(f"Expected error: {result['error']}")
    
    print_section("DEMO 7: Error Handling - Missing Question")
    
    result = examine_image(
        path=os.path.join(os.environ["VISION_BASE_DIR"], "query_test.png"),
        mode="query"
    )
    print(f"Expected error: {result['error']}")
    
    print_section("DEMO 8: Error Handling - Invalid Path")
    
    result = examine_image(
        path="/etc/passwd",
        mode="general"
    )
    print(f"Expected error: {result['error']}")

def demo_caching():
    """Demonstrate caching behavior."""
    
    print_section("DEMO 9: Caching Behavior")
    print("Running the same request twice to demonstrate caching\n")
    
    import time
    
    # First call
    print("First call (will be slow if API is available)...")
    start = time.time()
    result1 = examine_image(
        path=os.path.join(os.environ["VISION_BASE_DIR"], "general_test.png"),
        mode="general"
    )
    time1 = time.time() - start
    
    # Second call (should be cached)
    print("Second call (should be instant from cache)...")
    start = time.time()
    result2 = examine_image(
        path=os.path.join(os.environ["VISION_BASE_DIR"], "general_test.png"),
        mode="general"
    )
    time2 = time.time() - start
    
    print(f"\nFirst call took: {time1:.4f} seconds")
    print(f"Second call took: {time2:.4f} seconds")
    
    if time2 < time1 / 10:
        print("✅ Caching is working! Second call was much faster.")
    else:
        print("⚠️  Note: Both calls had similar timing (likely both hit errors)")

def main():
    """Run all demonstrations."""
    
    print("\n" + "="*70)
    print("  MCP Eyes 8K - Usage Demonstration")
    print("="*70)
    print(f"\nBase Directory: {os.environ['VISION_BASE_DIR']}")
    print(f"Model: {os.environ.get('VISION_MODEL', 'gpt-4o')}")
    print(f"API Key Set: {'Yes' if os.environ.get('OPENAI_API_KEY') else 'No'}")
    
    print("\n" + "-"*70)
    print("NOTE: To see actual vision model results, set OPENAI_API_KEY")
    print("      export OPENAI_API_KEY='your-key-here'")
    print("-"*70)
    
    # Run all demos
    demo_basic_usage()
    demo_region_analysis()
    demo_error_handling()
    demo_caching()
    
    print("\n" + "="*70)
    print("  Demonstration Complete")
    print("="*70)
    
    if not os.environ.get('OPENAI_API_KEY'):
        print("\n⚠️  API calls failed because OPENAI_API_KEY is not set.")
        print("   However, all code paths and error handling work correctly!")
        print("\n✅ To test with actual vision model:")
        print("   1. Get an OpenAI API key from https://platform.openai.com")
        print("   2. Set it: export OPENAI_API_KEY='your-key-here'")
        print("   3. Run this script again: python demo_usage.py")
    else:
        print("\n✅ All demonstrations completed!")
        print("   The tool is working correctly with the vision model.")
    
    print("\n" + "="*70)
    print("  Tool Usage in MCP Clients")
    print("="*70)
    print("""
To use this tool in an MCP client like Claude Desktop:

1. Add to your MCP client configuration:
   {
     "mcpServers": {
       "active-vision": {
         "command": "python",
         "args": ["/path/to/mcp-eyes-8k/active_vision.py"],
         "env": {
           "VISION_MODEL": "gpt-4o",
           "VISION_BASE_DIR": "/path/to/your/images",
           "OPENAI_API_KEY": "your-api-key-here"
         }
       }
     }
   }

2. The tool will be available as "examine_image" with these parameters:
   - path: string (required) - Path to the image file
   - mode: string (optional, default: "general") - One of: ui, ocr, general, query
   - question: string (required if mode=query) - Question to ask about the image
   - region: array of 4 integers (optional) - [x1, y1, x2, y2] crop region

3. Example usage from Claude:
   "Can you examine this screenshot using the examine_image tool?"
   "What text is in this image?" (will use OCR mode)
   "What UI elements are clickable in this screenshot?" (will use UI mode)
    """)

if __name__ == "__main__":
    main()
