#!/usr/bin/env python3
"""
Generate test images for testing the MCP Eyes 8K server.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create test_images directory if it doesn't exist
os.makedirs("test_images", exist_ok=True)

# 1. Create a simple UI mockup
def create_ui_test_image():
    """Create a mock UI screenshot with buttons and text inputs."""
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    draw.text((250, 50), "Login Form", fill='black', font=font_large)
    
    # Username input box
    draw.rectangle([100, 150, 700, 200], outline='gray', width=2)
    draw.text((110, 120), "Username:", fill='black', font=font_small)
    
    # Password input box
    draw.rectangle([100, 250, 700, 300], outline='gray', width=2)
    draw.text((110, 220), "Password:", fill='black', font=font_small)
    
    # Submit button
    draw.rectangle([300, 350, 500, 400], fill='blue', outline='darkblue', width=2)
    draw.text((360, 365), "Submit", fill='white', font=font_large)
    
    # Cancel button
    draw.rectangle([300, 420, 500, 470], fill='lightgray', outline='gray', width=2)
    draw.text((360, 435), "Cancel", fill='black', font=font_large)
    
    img.save("test_images/ui_test.png")
    print("Created test_images/ui_test.png")

# 2. Create an OCR test image with text
def create_ocr_test_image():
    """Create an image with various text blocks."""
    img = Image.new('RGB', (800, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
    
    # Title
    draw.text((50, 50), "Welcome to MCP Eyes 8K", fill='black', font=font_title)
    
    # Body text
    draw.text((50, 120), "This is a test document for OCR.", fill='black', font=font_body)
    draw.text((50, 160), "It contains multiple lines of text.", fill='black', font=font_body)
    draw.text((50, 200), "The vision model should extract all text.", fill='black', font=font_body)
    draw.text((50, 240), "Each line should have bounding boxes.", fill='black', font=font_body)
    
    # Footer
    draw.text((50, 320), "Thank you for testing!", fill='gray', font=font_body)
    
    img.save("test_images/ocr_test.png")
    print("Created test_images/ocr_test.png")

# 3. Create a general description test image
def create_general_test_image():
    """Create a simple scene for general description."""
    img = Image.new('RGB', (600, 400), color='skyblue')
    draw = ImageDraw.Draw(img)
    
    # Sun
    draw.ellipse([450, 50, 550, 150], fill='yellow', outline='orange')
    
    # Ground
    draw.rectangle([0, 300, 600, 400], fill='green')
    
    # House
    draw.rectangle([100, 200, 300, 300], fill='lightgray', outline='black', width=2)
    
    # Roof
    draw.polygon([100, 200, 200, 150, 300, 200], fill='red', outline='darkred')
    
    # Door
    draw.rectangle([170, 230, 230, 300], fill='brown', outline='black', width=1)
    
    # Window
    draw.rectangle([120, 220, 160, 260], fill='lightblue', outline='black', width=1)
    draw.line([140, 220, 140, 260], fill='black', width=1)
    draw.line([120, 240, 160, 240], fill='black', width=1)
    
    # Tree
    draw.rectangle([400, 250, 420, 300], fill='brown')
    draw.ellipse([370, 200, 450, 270], fill='darkgreen', outline='green')
    
    img.save("test_images/general_test.png")
    print("Created test_images/general_test.png")

# 4. Create a simple image for query mode
def create_query_test_image():
    """Create an image with specific objects to query about."""
    img = Image.new('RGB', (500, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    # Red circle
    draw.ellipse([50, 50, 150, 150], fill='red', outline='darkred', width=2)
    
    # Blue square
    draw.rectangle([200, 50, 300, 150], fill='blue', outline='darkblue', width=2)
    
    # Green triangle
    draw.polygon([350, 150, 400, 50, 450, 150], fill='green', outline='darkgreen', width=2)
    
    # Text label
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    draw.text((150, 200), "Three Shapes", fill='black', font=font)
    
    img.save("test_images/query_test.png")
    print("Created test_images/query_test.png")

if __name__ == "__main__":
    print("Generating test images...")
    create_ui_test_image()
    create_ocr_test_image()
    create_general_test_image()
    create_query_test_image()
    print("\nAll test images created successfully!")
    print("Test images are in the test_images/ directory")
