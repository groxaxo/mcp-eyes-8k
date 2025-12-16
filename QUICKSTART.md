# MCP Eyes 8K - Quick Start Guide

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/groxaxo/mcp-eyes-8k.git
cd mcp-eyes-8k

# 2. Install the package
pip install -e .

# 3. Set up environment variables
export OPENAI_API_KEY="your-api-key-here"
export VISION_BASE_DIR="/path/to/your/images"
export VISION_MODEL="gpt-4o"
```

## Quick Test

```bash
# Generate test images
python generate_test_images.py

# Run test suite
python test_suite.py

# Test server startup
python test_server.py

# Demo usage
python demo_usage.py
```

## Using as an MCP Server

### Start the server:
```bash
python active_vision.py
```

### Configure in Claude Desktop:

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or equivalent:

```json
{
  "mcpServers": {
    "active-vision": {
      "command": "python",
      "args": ["/absolute/path/to/mcp-eyes-8k/active_vision.py"],
      "env": {
        "VISION_MODEL": "gpt-4o",
        "VISION_BASE_DIR": "/path/to/your/images",
        "OPENAI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Use the tool in Claude:

```
"Can you examine this image: /path/to/image.png using UI mode?"
"What text is in this screenshot: /path/to/screenshot.png?"
"Describe this image: /path/to/photo.jpg"
"What color is the car in /path/to/photo.jpg?"
```

## Modes

### UI Mode
Detects interactive elements (buttons, inputs, dropdowns)
```python
examine_image(path="/path/to/ui.png", mode="ui")
```

### OCR Mode
Extracts text with bounding boxes
```python
examine_image(path="/path/to/text.png", mode="ocr")
```

### General Mode
Provides image description
```python
examine_image(path="/path/to/image.jpg", mode="general")
```

### Query Mode
Answers specific questions
```python
examine_image(path="/path/to/image.jpg", mode="query", question="What color is the car?")
```

### Region Analysis
Focus on specific area
```python
examine_image(path="/path/to/image.png", mode="ocr", region=[100, 100, 500, 500])
```

## Troubleshooting

### Error: "The api_key client option must be set"
**Solution**: Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Error: "Access denied: Path outside strict base directory"
**Solution**: Ensure the image path is within VISION_BASE_DIR:
```bash
export VISION_BASE_DIR="/path/to/your/images"
```

### Error: "File not found"
**Solution**: Check that:
1. The file path is correct
2. The file exists
3. You have read permissions

### Error: "Invalid mode"
**Solution**: Use one of: `ui`, `ocr`, `general`, `query`

### Error: "Parameter 'question' is required when mode='query'"
**Solution**: Provide a question parameter:
```python
examine_image(path="/path/to/image.jpg", mode="query", question="What is this?")
```

### Server won't start
**Check**:
1. Python version >= 3.10: `python --version`
2. Dependencies installed: `pip list | grep -E "mcp|litellm|pillow"`
3. No port conflicts (if using network mode)

### Poor accuracy
**Tips**:
1. Use higher resolution images
2. Ensure good lighting in photos
3. Use PNG for UI/text, JPEG for photos
4. Try different models (gpt-4-vision-preview, etc.)

### Slow performance
**Solutions**:
1. Caching is automatic (5-minute TTL)
2. Reduce image size before processing
3. Use region analysis for large images
4. Consider using a faster model

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VISION_MODEL` | `gpt-4o` | Vision model to use |
| `VISION_REPAIR_MODEL` | Same as VISION_MODEL | Model for JSON repair |
| `VISION_BASE_DIR` | Current directory | Base directory for image access |
| `OPENAI_API_KEY` | None | Your OpenAI API key |

## File Structure

```
mcp-eyes-8k/
├── active_vision.py        # Main server code
├── examples.py             # Usage examples
├── generate_test_images.py # Generate test images
├── test_suite.py           # Core functionality tests
├── test_server.py          # Server startup tests
├── demo_usage.py           # Usage demonstration
├── pyproject.toml          # Package configuration
├── README.md               # Full documentation
├── TESTING.md              # Testing documentation
└── test_images/            # Generated test images
    ├── ui_test.png
    ├── ocr_test.png
    ├── general_test.png
    └── query_test.png
```

## Performance Tips

1. **Caching**: Identical requests are cached for 5 minutes
2. **Image Format**: PNG for UI/text (preserves details), JPEG for photos (smaller)
3. **Image Size**: Automatically resized (max 2560px for UI/OCR, 1536px for general/query)
4. **Region Analysis**: Process only the area you need
5. **File Size Limit**: 20MB maximum

## Security Features

- ✅ Path validation prevents directory traversal
- ✅ File access restricted to VISION_BASE_DIR
- ✅ File size limits prevent DoS
- ✅ Input validation on all parameters

## Support

- Issues: https://github.com/groxaxo/mcp-eyes-8k/issues
- Documentation: README.md, TESTING.md
- Examples: examples.py, demo_usage.py

## License

Apache License 2.0 - See LICENSE file
