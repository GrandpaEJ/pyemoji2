# pyemoji2

**Add text and emojis to images with zero dependencies.** 🚀✨

A high-performance Python library for rendering text and emojis onto images. Built with **Cairo** and **Pango**, bundled for absolute simplicity.

## ✨ Features

- 🎯 **Zero System Dependencies** - Everything bundled in the wheel
- 🚀 **Native Speed** - Written in C, wrapped in Python
- 🎨 **Rich Text** - Supports all system fonts and emojis
- 🖼️ **Direct Memory Access** - No Pillow required
- 📦 **Cross-Platform** - Linux (x86_64, i686), macOS (x86_64, arm64)
- 📱 **Android/Termux** - Build from source support
- 🔥 **Lightweight** - ~5-8MB wheels with all dependencies included

## 🚀 Installation

### From PyPI (Recommended)
```bash
pip install pyemoji2
```

**That's it!** No system libraries, no build tools, no hassle.

### From Source (For Development)
If building from source, you need:

**Ubuntu/Debian:**
```bash
sudo apt install libcairo2-dev libpango1.0-dev pkg-config
```

**macOS:**
```bash
brew install cairo pango pkg-config
```

**Termux (Android):**
```bash
pkg install python clang make pkg-config libcairo pango
```

Then install:
```bash
pip install .
```

## 🖥️ Platform Support

### Supported Platforms (Pre-built Wheels)
- ✅ **Linux** - x86_64, i686 (manylinux2014)
- ✅ **macOS** - x86_64 (Intel), arm64 (Apple Silicon)

### Build from Source
- ✅ **Android/Termux** - Full support with source build
- ⚠️ **Windows** - Not currently supported (Cairo/Pango dependency issues)
- ⚠️ **Linux ARM64** - Build from source recommended

For unsupported platforms, you can build from source following the instructions above.

## 📖 Usage

### Basic Example
```python
import pyemoji2

# Create a blank canvas
editor = pyemoji2.EmojiEditor.create_empty(500, 300)

# Add text with emojis
editor.add_text("Hello World! 🌍", 50, 150, "Sans", 60, "black")
editor.add_text("Made with ❤️", 150, 250, "Sans", 30, "red")

# Save
editor.save("output.png")
```

### Advanced Example
```python
import pyemoji2

# Create image
editor = pyemoji2.EmojiEditor.create_empty(800, 400)

# Title
editor.add_text("🎉 pyemoji2", 50, 80, "Sans Bold", 72, "black")

# Subtitle
editor.add_text("Zero-dependency emoji rendering", 50, 150, "Sans", 36, "black")

# Features
editor.add_text("✅ Fast", 50, 220, "Sans", 28, "black")
editor.add_text("✅ Simple", 50, 270, "Sans", 28, "black")
editor.add_text("✅ Cross-platform", 50, 320, "Sans", 28, "black")

editor.save("demo.png")
```

### API Reference

#### `EmojiEditor.create_empty(width, height)`
Create a blank ARGB32 image.

**Parameters:**
- `width` (int): Image width in pixels
- `height` (int): Image height in pixels

**Returns:** `EmojiEditor` instance

#### `editor.add_text(text, x, y, font_family, font_size, color)`
Add text to the image.

**Parameters:**
- `text` (str): Text to render (supports emojis)
- `x` (float): X coordinate (top-left)
- `y` (float): Y coordinate (top-left)
- `font_family` (str): Font name (e.g., "Sans", "Serif", "Monospace")
- `font_size` (float): Font size in points
- `color` (str): Color name ("black", "red", etc.)

#### `editor.save(output_path)`
Save the image as PNG.

**Parameters:**
- `output_path` (str): Output file path

## 🏗️ Development

### Build Extension
```bash
python setup.py build_ext --inplace
```

### Run Tests
```bash
python test_pyemoji2.py
```

## 📊 Performance

- **Rendering Speed**: ~1ms for typical text
- **Memory**: Minimal overhead, direct Cairo surfaces
- **Wheel Size**: 5-10MB (all dependencies included)

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📄 License

MIT

## 🙏 Acknowledgments

Built with:
- [Cairo](https://www.cairographics.org/) - 2D graphics library
- [Pango](https://pango.gnome.org/) - Text layout engine
- [cibuildwheel](https://cibuildwheel.readthedocs.io/) - Cross-platform wheel building