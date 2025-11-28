#!/usr/bin/env python3
"""
Test color preservation from PIL and imgrs.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.getcwd()))

from pyemoji2 import Image, Text

# Create a test image with colored emoji
img = Image.create_empty(200, 100)
img.add_text("🌈🎨", 50, 30, font_size=40, color="black")
img.save("original_emoji.png")
print("Created original_emoji.png")

# Test loading it back with Image.load
img_loaded = Image.load("original_emoji.png")
img_loaded.add_text("Loaded", 10, 80, font_size=20, color="red")
img_loaded.save("loaded_emoji.png")
print("Created loaded_emoji.png")

# Test with PIL
try:
    from PIL import Image as PILImage
    pil_img = PILImage.open("original_emoji.png")
    img_from_pil = Image.from_pil(pil_img)
    img_from_pil.add_text("From PIL", 10, 80, font_size=20, color="blue")
    img_from_pil.save("pil_emoji.png")
    print("Created pil_emoji.png")
except Exception as e:
    print(f"PIL test failed: {e}")

# Test with imgrs
try:
    import imgrs
    imgrs_img = imgrs.Image.open("original_emoji.png")
    img_from_imgrs = Image.from_imgrs(imgrs_img)
    img_from_imgrs.add_text("From imgrs", 10, 80, font_size=20, color="green")
    img_from_imgrs.save("imgrs_emoji.png")
    print("Created imgrs_emoji.png")
except Exception as e:
    print(f"imgrs test failed: {e}")

print("Color preservation test complete!")