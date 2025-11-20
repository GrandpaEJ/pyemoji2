# emoji-img

**Add text to images using emojis.** 🌍✨

A high-performance Python library for rendering text and emojis onto images. Built with **Cairo** and **Pango** for absolute speed and professional typography.

## Features

- 🚀 **Native Speed**: Written in C, wrapped in Python. Zero overhead.
- 🎨 **Rich Text**: Supports all system fonts and emojis.
- 🖼️ **Direct Access**: Creates images directly in memory (no Pillow required).
- 📦 **Easy Integration**: Works with `imgrs` and other image libraries.

## Installation

### Prerequisites
You need `cairo` and `pango` installed on your system.

**Ubuntu/Debian:**
```bash
sudo apt install libcairo2-dev libpango1.0-dev
```

**macOS:**
```bash
brew install cairo pango
```

**Termux (Android):**
```bash
pkg install python clang make pkg-config libcairo pango
```

### Install Package
```bash
pip install .
```

## Usage

```python
import pyemoji2

# 1. Create a blank image (Width, Height)
editor = pyemoji2.EmojiEditor.create_empty(500, 300)

# 2. Add text with emojis
#    Arguments: text, x, y, font_family, font_size, color
editor.add_text("Hello World! 🚀", 50, 150, "Sans", 60, "black")
editor.add_text("Made with ❤️", 150, 250, "Sans", 30, "red")

# 3. Save the result
editor.save("cool_image.png")
```

## Development

To build locally:
```bash
# Install dependencies
pip install -r requirements.txt

# Build extension
python3 setup.py build_ext --inplace
```

## License
MIT