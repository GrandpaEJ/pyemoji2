#!/usr/bin/env python3
"""
Comprehensive test for pyemoji2 advanced features.
"""

import sys
sys.path.insert(0, '.')

from pyemoji2 import EmojiEditor, Text, TextBox

# Create canvas
img = EmojiEditor.create_empty(800, 600)

# Test 1: Simple text (backward compatible)
img.add_text("Simple Text", 50, 50, "Sans", 24, "black")

# Test 2: Text with outline (method chaining)
text = Text("Outlined! 🎨", "Sans Bold", 48).with_outline("black", 3).with_color("white")
img.add(text, (50, 100))

# Test 3: Gradient text
text = Text("Gradient 🌈", "Sans Bold", 60).with_gradient("red", "blue", vertical=False)
img.add(text, (50, 180))

# Test 4: Text with shadow
text = Text("Shadow ✨", "Sans", 40).with_shadow(3, 3, "gray", 0.7)
img.add(text, (50, 270))

# Test 5: TextBox with background
box = TextBox("Boxed Text 📦", "Sans", 32).with_background("blue", 15).with_border("white", 3)
img.add(box, (50, 350))

# Test 6: Complex chaining
text = (Text("Chained! ⛓️", "Sans Bold", 36)
        .with_color("yellow")
        .with_outline("black", 2))
img.add(text, (50, 450))

# Test 7: Emoji support
img.add_text("Emojis: 😀 🚀 ❤️ 🌟 🎉", 50, 520, "Sans", 32, "purple")

# Save
img.save("test_advanced.png")

print("✅ Advanced features test complete! Check test_advanced.png")
