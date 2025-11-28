# PyEmoji2 Examples

This directory contains examples demonstrating various features of PyEmoji2.

## Running Examples

```bash
cd examples
python basic_usage.py
python advanced_styling.py
python api_demo.py
python color_test.py
```

## Examples Overview

### basic_usage.py
Demonstrates basic image loading and text addition:
- Loading images with `Image.load()`
- Creating empty images with `Image.create_empty()`
- Adding simple text with `add_text()`

### advanced_styling.py
Shows advanced text styling features:
- Outlined text
- Gradient text
- Text with shadows
- TextBox with background and borders
- Emoji support

### api_demo.py
Comprehensive API demonstration:
- All loading methods (`load`, `open`, `from_pil`, `from_imgrs`)
- Method chaining
- Different text styles

### color_test.py
Tests color preservation when loading from different sources:
- Direct image loading
- PIL image conversion
- imgrs image conversion

## Output

All generated images are saved to the `output/` subdirectory.

## Requirements

Make sure PyEmoji2 is installed and the C extension is built:

```bash
pip install -e .
python setup.py build_ext --inplace
```

Optional dependencies for full functionality:
```bash
pip install pillow
pip install imgrs