# 👁️ MCP Eyes 8K - Active Vision Server

```
 ███╗   ███╗ ██████╗██████╗     ███████╗██╗   ██╗███████╗███████╗
 ████╗ ████║██╔════╝██╔══██╗    ██╔════╝╚██╗ ██╔╝██╔════╝██╔════╝
 ██╔████╔██║██║     ██████╔╝    █████╗   ╚████╔╝ █████╗  ███████╗
 ██║╚██╔╝██║██║     ██╔═══╝     ██╔══╝    ╚██╔╝  ██╔══╝  ╚════██║
 ██║ ╚═╝ ██║╚██████╗██║         ███████╗   ██║   ███████╗███████║
 ╚═╝     ╚═╝ ╚═════╝╚═╝         ╚══════╝   ╚═╝   ╚══════╝╚══════╝
                    
                    🌟 Adamant Edition v2.0 🌟
           Give your AI agent the gift of sight, mate!
```

## G'day! 👋

Welcome to **MCP Eyes 8K**, the absolute legend of an MCP (Model Context Protocol) server that gives your AI agents proper vision superpowers. This thing's been built to handle all your image analysis needs – from reading tiny text to spotting UI elements and answering complex visual questions. No worries, no fuss, just solid functionality.

Think of it as giving your AI mate a pair of seriously good eyes. Whether you're after OCR, UI automation, or just want to ask questions about images, we've got you sorted.

## What Can This Beauty Do? 🚀

MCP Eyes 8K comes loaded with four ripper modes:

### 🎯 **UI Mode** - Element Detection
Perfect for automation and UI testing. This mode spots all the clickable bits – buttons, inputs, dropdowns, you name it. Returns precise coordinates so your agent knows exactly where to click.

**Use it for:**
- Automating web testing
- Building browser automation tools
- Creating accessibility helpers
- Mapping UI layouts

### 📝 **OCR Mode** - Text Extraction
Reads text from images like a champion. Whether it's a screenshot, a photo of a document, or a meme with text, OCR mode extracts it all with bounding boxes so you know where each bit of text lives.

**Use it for:**
- Document digitization
- Receipt scanning
- Screenshot text extraction
- Reading text from photos

### 🔍 **Query Mode** - Visual Q&A
Ask specific questions about images and get accurate answers. It's like having a conversation about what's in the picture.

**Use it for:**
- Visual question answering
- Image content verification
- Detailed image analysis
- Context-aware image understanding

### 🌅 **General Mode** - Image Description
Get a comprehensive description of what's happening in an image. Main objects, scene details, the whole shebang.

**Use it for:**
- Alt text generation
- Image cataloguing
- Content moderation
- General image understanding

## Features That'll Make You Stoked 🎨

- **⚡ Blazing Fast**: Thread-safe LRU caching with 5-minute TTL means repeated requests are instant
- **🔒 Secure**: Strict path validation – no sneaky file access outside your base directory
- **🎯 Precise**: Smart coordinate mapping handles crops, resizing, and normalization automatically
- **🛡️ Robust**: Fallback handling for different vision model providers (works with OpenAI, Azure, local models, etc.)
- **📦 Efficient**: Automatic image optimization (JPEG for photos, PNG for UI/text)
- **🔧 Flexible**: Configure via environment variables
- **💪 Resilient**: Automatic JSON repair when models get creative with their output

## Getting Started 🏃‍♂️

### Prerequisites

You'll need Python 3.10 or newer. Sweet as.

### Installation with uv (Recommended) 📦

If you haven't got `uv` yet, it's the fastest Python package installer around. Get it first:

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Now install MCP Eyes 8K:

```bash
# Clone the repo
git clone https://github.com/groxaxo/mcp-eyes-8k.git
cd mcp-eyes-8k

# Create a virtual environment and install dependencies with uv (super quick!)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .
```

### Alternative Installation (pip)

Not keen on uv? No worries, classic pip works too:

```bash
# Clone the repo
git clone https://github.com/groxaxo/mcp-eyes-8k.git
cd mcp-eyes-8k

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Configuration ⚙️

Set these environment variables to customize the behaviour:

```bash
# Vision model to use (default: gpt-4o)
export VISION_MODEL="gpt-4o"

# Model for JSON repair fallback (default: same as VISION_MODEL)
export VISION_REPAIR_MODEL="gpt-4o"

# Base directory for file access (default: current working directory)
export VISION_BASE_DIR="/path/to/your/images"

# For local or Azure models, set your API keys
export OPENAI_API_KEY="your-key-here"
# or for Azure
export AZURE_API_KEY="your-key-here"
export AZURE_API_BASE="your-endpoint"
```

## Running the Server 🏃

Fire it up:

```bash
python active_vision.py
```

The server will start and expose the `examine_image` tool via MCP. Connect your MCP client (like Claude Desktop, Cline, or your custom implementation) and you're good to go!

## Usage Examples 📸

### Example 1: OCR a Screenshot

```json
{
  "path": "/path/to/screenshot.png",
  "mode": "ocr"
}
```

**Response:**
```json
{
  "mode": "ocr",
  "metadata": {
    "original_path": "/path/to/screenshot.png",
    "original_size": {"width": 1920, "height": 1080},
    "crop_bbox": null,
    "sent_size": {"width": 1920, "height": 1080},
    "prompt_version": "v1.5"
  },
  "content": {
    "text_blocks": [
      {
        "text": "Welcome to MCP Eyes",
        "bbox": [120, 45, 450, 78]
      },
      {
        "text": "The future of vision",
        "bbox": [125, 85, 420, 112]
      }
    ],
    "uncertainties": []
  }
}
```

### Example 2: Detect UI Elements

```json
{
  "path": "/path/to/ui-screenshot.png",
  "mode": "ui"
}
```

**Response:**
```json
{
  "mode": "ui",
  "content": {
    "elements": [
      {
        "type": "button",
        "label": "Submit",
        "bbox": [820, 450, 920, 490]
      },
      {
        "type": "input",
        "label": "Email address",
        "bbox": [300, 350, 650, 385]
      }
    ],
    "uncertainties": []
  }
}
```

### Example 3: Ask Questions About an Image

```json
{
  "path": "/path/to/photo.jpg",
  "mode": "query",
  "question": "What color is the car in this image?"
}
```

**Response:**
```json
{
  "mode": "query",
  "content": {
    "answer": "The car is red",
    "evidence": ["Red sedan visible in the center of the image", "Paint appears to be metallic red finish"],
    "uncertainties": []
  }
}
```

### Example 4: Analyze a Specific Region

```json
{
  "path": "/path/to/large-image.png",
  "mode": "general",
  "region": [500, 300, 1200, 800]
}
```

This crops the image to the specified region `[x1, y1, x2, y2]` before analysis – super handy for focusing on specific areas!

### Example 5: General Description

```json
{
  "path": "/path/to/photo.jpg",
  "mode": "general"
}
```

**Response:**
```json
{
  "mode": "general",
  "content": {
    "description": "A sunny beach scene with clear blue water and white sand. Several people are visible in the background, and palm trees line the shore.",
    "main_objects": ["beach", "ocean", "palm trees", "people", "sand"],
    "uncertainties": []
  }
}
```

## How It Works 🔧

1. **Security First**: Validates file paths to ensure they're within your specified base directory
2. **Smart Processing**: Automatically crops, resizes, and optimizes images based on the mode
3. **Caching**: Keeps results cached for 5 minutes to speed up repeated requests
4. **Vision Magic**: Sends the image to your configured vision model with mode-specific prompts
5. **Coordinate Mapping**: Translates model coordinates back to original image coordinates
6. **Resilient Parsing**: If the model returns wonky JSON, automatically repairs it

## Advanced Features 🎓

### Region-Based Analysis
Crop images on the fly by specifying a region – great for analyzing specific parts of large images without processing the whole thing.

### Coordinate Accuracy
All bounding boxes are mapped back to original image coordinates, even if the image was cropped or resized for analysis. Click-safe coordinates guaranteed!

### Provider Compatibility
Works with OpenAI, Azure OpenAI, Anthropic, local LLMs via Ollama, and any provider supported by LiteLLM. Just set your model name and API keys.

### JSON Repair
Sometimes vision models get a bit creative with their JSON formatting. MCP Eyes has a fallback repair mechanism using another LLM to fix malformed responses.

## Troubleshooting 🔍

**Server won't start?**
- Check Python version: `python --version` (needs 3.10+)
- Verify all dependencies installed: `uv pip list` or `pip list`
- Make sure you've set your API keys

**Getting access denied errors?**
- Check your `VISION_BASE_DIR` is set correctly
- Ensure the image path is within the base directory

**Model errors?**
- Verify your API key is valid
- Check you have credits/quota available
- Try a different model if yours doesn't support vision

## Contributing 🤝

Keen to make this even better? Choice! Feel free to open issues or submit PRs. All contributions welcome, no matter how small.

## License 📄

Apache License 2.0 - See [LICENSE](LICENSE) file for details.

## Acknowledgements 🙏

Built with:
- [FastMCP](https://github.com/jlowin/fastmcp) - For the MCP server framework
- [LiteLLM](https://github.com/BerriAI/litellm) - For unified LLM API access
- [Pillow](https://python-pillow.org/) - For image processing

## Questions? 💬

Something not working right? Open an issue on GitHub and we'll sort you out!

---

Made with ❤️ in Aotearoa 🇳🇿

*Kia kaha, code on!*
