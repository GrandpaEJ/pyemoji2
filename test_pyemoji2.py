import sys
import os
# from PIL import Image, ImageDraw # Removed Pillow


# Add current directory to path so we can import pyemoji2
sys.path.append(os.getcwd())

try:
    import pyemoji2
    import imgrs
    print("Imports successful")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

def test_pyemoji2():
    print("Testing pyemoji2...")
    
    # Create a blank image with pyemoji2 (Native Cairo)
    width, height = 400, 200
    editor = pyemoji2.EmojiEditor.create_empty(width, height)
    editor.add_text("Hello 🌍", 50, 100, font_size=40, color="black")
    
    # Save using C save (for verification)
    editor.save("output_pyemoji2.png")
    print("Saved output_pyemoji2.png")
    
    # Verify with imgrs
    # imgrs usage: imgrs.load(path) -> Image
    # This part depends on what imgrs actually exposes.
    # Based on search, it's a high perf image lib.
    # Let's just try to load it.
    try:
        rs_img = imgrs.Image.open("output_pyemoji2.png")
        print(f"Loaded with imgrs: {rs_img}")
    except Exception as e:
        print(f"imgrs load failed: {e}")

if __name__ == "__main__":
    test_pyemoji2()
