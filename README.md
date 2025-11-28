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

**Windows (MSYS2):**
```bash
pacman -S mingw-w64-x86_64-python mingw-w64-x86_64-gcc mingw-w64-x86_64-pkg-config mingw-w64-x86_64-cairo mingw-w64-x86_64-pango
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
- ⚠️ **Linux ARM64** - Build from source recommended

For unsupported platforms, you can build from source following the instructions above.

## 📖 Documentation

For comprehensive API documentation and examples, see [`docs/README.md`](docs/README.md).

## 📖 Usage

### Basic Example
```python
from pyemoji2 import Image

# Load an existing image
img = Image.load("input.png")

# Or create a blank canvas
img = Image.create_empty(500, 300)

# Add text with emojis
img.add_text("Hello World! 🌍", 50, 150, font_size=60, color="black")
img.add_text("Made with ❤️", 150, 250, font_size=30, color="red")

# Save
img.save("output.png")
```

### Advanced Example
```python
from pyemoji2 import Image, Text, TextBox

# Create image
img = Image.create_empty(800, 400)

# Title with styling
title = Text("🎉 pyemoji2", "DejaVu Sans", 72)
title = title.with_color("black").with_outline("white", 3)
img.add(title, (50, 80))

# Subtitle
img.add_text("Zero-dependency emoji rendering", 50, 150, font_size=36, color="black")

# Features in a box
box = TextBox("✅ Fast & Simple", "DejaVu Sans", 28)
box = box.with_background("lightblue", 10).with_border("blue", 2)
img.add(box, (50, 220))

img.save("demo.png")
```

### Loading from Other Libraries
```python
from pyemoji2 import Image
from PIL import Image as PILImage
import imgrs

# From PIL
pil_img = PILImage.open("photo.jpg")
img = Image.from_pil(pil_img)

# From imgrs
imgrs_img = imgrs.Image.open("photo.png")
img = Image.from_imgrs(imgrs_img)

# Add text and save
img.add_text("Converted!", 50, 50, font_size=40, color="red")
img.save("converted.png")
```

### API Reference

#### Image Class

**Class Methods:**
- `Image.load(path)` - Load image from file
- `Image.open(path)` - Alias for load()
- `Image.create_empty(width, height)` - Create blank image
- `Image.from_pil(pil_image)` - Convert from PIL Image
- `Image.from_imgrs(imgrs_image)` - Convert from imgrs Image

**Instance Methods:**
- `add(text_obj, position)` - Add Text/TextBox object
- `add_text(text, x, y, font_family="DejaVu Sans", font_size=20.0, color="black")` - Add simple text
- `save(output_path)` - Save as PNG

#### Text Class

```python
Text(text, font="DejaVu Sans", size=24)
```

**Methods:**
- `with_color(color)` - Set text color
- `with_outline(color, width=2)` - Add outline
- `with_gradient(color1, color2, vertical=False)` - Add gradient
- `with_shadow(offset_x=2, offset_y=2, color="gray", opacity=0.5)` - Add shadow

#### TextBox Class

```python
TextBox(text, font="DejaVu Sans", size=24)
```

**Additional Methods:**
- `with_background(color, padding=10)` - Set background
- `with_border(color, width=2)` - Set border

## 🏗️ Development

### Build Extension
```bash
python setup.py build_ext --inplace
```

### Run Examples
```bash
cd examples
python basic_usage.py
python advanced_styling.py
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