# PyEmoji2 Documentation

PyEmoji2 is a Python library for adding text and emoji to images with advanced styling capabilities.

## Installation

```bash
pip install pyemoji2
```

## Quick Start

```python
from pyemoji2 import Image, Text

# Load an image
img = Image.load("input.png")

# Add simple text
img.add_text("Hello World!", 50, 100, font_size=30, color="black")

# Add styled text
text = Text("Beautiful Text ✨", "DejaVu Sans", 40)
text = text.with_color("blue").with_outline("white", 2)
img.add(text, (50, 150))

# Save the result
img.save("output.png")
```

## API Reference

### Image Class

The main class for image manipulation.

#### Class Methods

- `Image.load(path)` - Load image from file path
- `Image.open(path)` - Alias for load()
- `Image.create_empty(width, height)` - Create blank image
- `Image.from_pil(pil_image)` - Create from PIL Image
- `Image.from_imgrs(imgrs_image)` - Create from imgrs Image

#### Instance Methods

- `add(text_obj, position)` - Add Text or TextBox object
- `add_text(text, x, y, font_family="DejaVu Sans", font_size=20.0, color="black")` - Add simple text
- `save(output_path)` - Save image to file

### Text Class

For creating styled text objects.

#### Constructor

```python
Text(text, font="DejaVu Sans", size=24)
```

#### Methods

- `with_color(color)` - Set text color
- `with_outline(color, width=2)` - Add text outline
- `with_gradient(color1, color2, vertical=False)` - Add gradient
- `with_shadow(offset_x=2, offset_y=2, color="gray", opacity=0.5)` - Add shadow

### TextBox Class

Text with background and border.

#### Constructor

```python
TextBox(text, font="DejaVu Sans", size=24)
```

#### Additional Methods

- `with_background(color, padding=10)` - Set background
- `with_border(color, width=2)` - Set border

## Examples

See the `examples/` directory for comprehensive examples:

- `examples/basic_usage.py` - Basic text addition
- `examples/advanced_styling.py` - Advanced text styling
- `examples/emoji_support.py` - Emoji rendering
- `examples/image_conversion.py` - Converting from PIL/imgrs

## Supported Formats

- Input: PNG, JPEG, and other formats supported by Cairo
- Output: PNG
- Fonts: System fonts + DejaVu Sans (default for Unicode support)

## Dependencies

- Cairo
- Pango
- PIL/Pillow (optional, for from_pil)
- imgrs (optional, for from_imgrs)

## Color Support

Colors can be specified as:
- Named colors: "red", "blue", "black", etc.
- Hex colors: "#FF0000", "#00FF00", etc.
- RGB tuples: (255, 0, 0)

## Font Support

- Default font: "DejaVu Sans" for excellent Unicode/emoji support
- Any system font can be specified by name
- Font sizes in points

## Advanced Features

- Text outlining with customizable width and color
- Gradient text effects
- Drop shadows with opacity control
- Background boxes with borders
- Emoji rendering with proper color preservation
- Method chaining for fluent API