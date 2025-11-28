import ctypes
import os
import pathlib
import platform

# Cross-platform font fallbacks
FONT_FALLBACKS = {
    "linux": ["DejaVu Sans", "Liberation Sans", "Ubuntu", "Sans"],
    "darwin": [
        "Helvetica Neue",
        "Helvetica",
        "System Font",
        "San Francisco",
        "DejaVu Sans",
    ],
    "windows": ["Segoe UI", "Arial", "DejaVu Sans", "Sans"],
    "android": ["Roboto", "DejaVu Sans", "Sans"],
    "ios": ["San Francisco", "Helvetica Neue", "DejaVu Sans"],
}


def get_system_fonts():
    """Get appropriate fonts for current platform."""
    system = platform.system().lower()
    if system == "linux":
        return FONT_FALLBACKS["linux"]
    elif system == "darwin":
        return FONT_FALLBACKS["darwin"]
    elif system == "windows":
        return FONT_FALLBACKS["windows"]
    else:
        # Fallback for unknown systems
        return FONT_FALLBACKS["linux"]


# Load the shared library with cross-platform support
def find_library():
    """Find the appropriate shared library for current platform."""
    lib_dir = pathlib.Path(__file__).parent

    # Try platform-specific extensions
    system = platform.system().lower()
    if system == "linux":
        patterns = ["_emoji_img*.so", "libemoji_img.so"]
    elif system == "darwin":
        patterns = ["_emoji_img*.so", "libemoji_img.dylib"]
    elif system == "windows":
        patterns = ["_emoji_img*.pyd", "_emoji_img*.dll"]
    else:
        patterns = ["_emoji_img*.so"]

    for pattern in patterns:
        lib_files = list(lib_dir.glob(pattern))
        if lib_files:
            return lib_files[0]

    # Fallback for local dev
    fallback = pathlib.Path(__file__).parent.parent / "c" / "libemoji_img.so"
    if fallback.exists():
        return fallback

    raise FileNotFoundError(
        f"Could not find _emoji_img extension for {system} platform"
    )


LIB_PATH = find_library()


class EmojiImageManipulator(ctypes.Structure):
    pass


class Image:
    def __init__(self, image_path=None, image_data=None, empty_size=None):
        self._lib = None
        self._manip = None
        self._data_ref = None  # Keep reference to data to prevent GC
        self._is_closed = False

        try:
            self._lib = ctypes.CDLL(str(LIB_PATH))
            self._setup_signatures()

            if image_path:
                # Normalize path for cross-platform compatibility
                normalized_path = os.path.abspath(image_path)
                if not os.path.exists(normalized_path):
                    raise FileNotFoundError(f"Image file not found: {image_path}")
                self._manip = self._lib.emoji_img_create(
                    normalized_path.encode("utf-8")
                )
            elif image_data:
                # Expecting (data, width, height, stride)
                data, width, height, stride = image_data
                self._data_ref = data  # Keep it alive!
                self._manip = self._lib.emoji_img_create_from_data(
                    data, width, height, stride
                )
            elif empty_size:
                width, height = empty_size
                # Validate dimensions for memory safety
                if width <= 0 or height <= 0 or width > 65535 or height > 65535:
                    raise ValueError(f"Invalid image dimensions: {width}x{height}")
                self._manip = self._lib.emoji_img_create_empty(width, height)
            else:
                raise ValueError("Must provide image_path, image_data, or empty_size")

            if self._manip is None:
                raise RuntimeError("Failed to create image manipulator")

        except Exception as e:
            self._cleanup()
            raise RuntimeError(f"Failed to initialize image: {e}") from e

    def _setup_signatures(self):
        self._lib.emoji_img_create.argtypes = [ctypes.c_char_p]
        self._lib.emoji_img_create.restype = ctypes.POINTER(EmojiImageManipulator)

        self._lib.emoji_img_create_from_data.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
        ]
        self._lib.emoji_img_create_from_data.restype = ctypes.POINTER(
            EmojiImageManipulator
        )

        self._lib.emoji_img_create_empty.argtypes = [ctypes.c_int, ctypes.c_int]
        self._lib.emoji_img_create_empty.restype = ctypes.POINTER(EmojiImageManipulator)

        self._lib.emoji_img_add_text.argtypes = [
            ctypes.POINTER(EmojiImageManipulator),
            ctypes.c_char_p,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_char_p,
            ctypes.c_double,
            ctypes.c_char_p,
        ]

        # Advanced text functions
        self._lib.emoji_img_add_text_outlined.argtypes = [
            ctypes.POINTER(EmojiImageManipulator),
            ctypes.c_char_p,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_char_p,
            ctypes.c_double,
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_double,
        ]

        self._lib.emoji_img_add_text_gradient.argtypes = [
            ctypes.POINTER(EmojiImageManipulator),
            ctypes.c_char_p,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_char_p,
            ctypes.c_double,
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_int,
        ]

        self._lib.emoji_img_add_text_shadow.argtypes = [
            ctypes.POINTER(EmojiImageManipulator),
            ctypes.c_char_p,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_char_p,
            ctypes.c_double,
            ctypes.c_char_p,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_char_p,
            ctypes.c_double,
        ]

        self._lib.emoji_img_add_textbox.argtypes = [
            ctypes.POINTER(EmojiImageManipulator),
            ctypes.c_char_p,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_char_p,
            ctypes.c_double,
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_double,
            ctypes.c_char_p,
            ctypes.c_double,
        ]

        self._lib.emoji_img_save.argtypes = [
            ctypes.POINTER(EmojiImageManipulator),
            ctypes.c_char_p,
        ]
        self._lib.emoji_img_destroy.argtypes = [ctypes.POINTER(EmojiImageManipulator)]

    def add_text(self, text, x, y, font_family=None, font_size=20.0, color="black"):
        """Add simple text (backward compatible)."""
        if self._is_closed or self._lib is None or self._manip is None:
            raise RuntimeError("Image has been closed or not properly initialized")

        if font_family is None:
            font_family = get_system_fonts()[0]  # Use best system font

        # Try font fallbacks if the primary font fails
        fonts_to_try = [font_family] + get_system_fonts()
        last_error = None

        for font in fonts_to_try:
            try:
                self._lib.emoji_img_add_text(
                    self._manip,
                    text.encode("utf-8"),
                    x,
                    y,
                    font.encode("utf-8"),
                    font_size,
                    color.encode("utf-8"),
                )
                return self  # Success, return
            except (OSError, UnicodeEncodeError) as e:
                last_error = e
                continue

        # If all fonts failed, raise the last error
        raise RuntimeError(
            f"Failed to render text with any font: {last_error}"
        ) from last_error

    def add(self, text_obj, position):
        """Add Text or TextBox object (new API)."""
        if self._is_closed or self._lib is None or self._manip is None:
            raise RuntimeError("Image has been closed or not properly initialized")

        from .text import TextBox

        x, y = position

        if isinstance(text_obj, TextBox):
            # Render as textbox
            self._lib.emoji_img_add_textbox(
                self._manip,
                text_obj.text.encode("utf-8"),
                x,
                y,
                text_obj.font.encode("utf-8"),
                text_obj.size,
                text_obj.color.encode("utf-8"),
                (text_obj.background or "white").encode("utf-8"),
                text_obj.padding,
                (text_obj.border_color or "black").encode("utf-8"),
                text_obj.border_width,
            )
        elif text_obj.gradient_colors:
            # Render with gradient
            c1, c2 = text_obj.gradient_colors
            self._lib.emoji_img_add_text_gradient(
                self._manip,
                text_obj.text.encode("utf-8"),
                x,
                y,
                text_obj.font.encode("utf-8"),
                text_obj.size,
                c1.encode("utf-8"),
                c2.encode("utf-8"),
                1 if text_obj.gradient_vertical else 0,
            )
        elif text_obj.shadow_offset:
            # Render with shadow
            sx, sy = text_obj.shadow_offset
            self._lib.emoji_img_add_text_shadow(
                self._manip,
                text_obj.text.encode("utf-8"),
                x,
                y,
                text_obj.font.encode("utf-8"),
                text_obj.size,
                text_obj.color.encode("utf-8"),
                sx,
                sy,
                text_obj.shadow_color.encode("utf-8"),
                text_obj.shadow_opacity,
            )
        elif text_obj.outline_color:
            # Render with outline
            self._lib.emoji_img_add_text_outlined(
                self._manip,
                text_obj.text.encode("utf-8"),
                x,
                y,
                text_obj.font.encode("utf-8"),
                text_obj.size,
                text_obj.color.encode("utf-8"),
                text_obj.outline_color.encode("utf-8"),
                text_obj.outline_width,
            )
        else:
            # Simple text
            self.add_text(
                text_obj.text, x, y, text_obj.font, text_obj.size, text_obj.color
            )

        return self  # Chainable

    def save(self, output_path):
        """Save image to file."""
        if self._is_closed or self._lib is None or self._manip is None:
            raise RuntimeError("Image has been closed or not properly initialized")

        # Ensure output directory exists
        output_path = os.path.abspath(output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        self._lib.emoji_img_save(self._manip, output_path.encode("utf-8"))
        return self  # Chainable

    def _cleanup(self):
        """Clean up resources."""
        if self._manip and self._lib:
            try:
                self._lib.emoji_img_destroy(self._manip)
            except Exception:
                pass  # Ignore errors during cleanup
        self._manip = None
        self._data_ref = None
        self._is_closed = True

    def close(self):
        """Explicitly close and clean up resources."""
        self._cleanup()

    def __del__(self):
        if not self._is_closed:
            self._cleanup()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @classmethod
    def load(cls, path):
        """Load image from file path."""
        return cls(image_path=path)

    @classmethod
    def open(cls, path):
        """Open image from file path (alias for load)."""
        return cls.load(path)

    @classmethod
    def create_empty(cls, width, height):
        """Create empty image."""
        return cls(empty_size=(width, height))

    @classmethod
    def from_pil(cls, pil_image):
        """Create Image from PIL Image."""
        # Convert PIL image to raw data
        if pil_image.mode not in ("RGB", "RGBA"):
            pil_image = pil_image.convert("RGBA")
        data_bytes = pil_image.tobytes()
        width = pil_image.width
        height = pil_image.height

        if pil_image.mode == "RGBA":
            # Cairo expects BGRA (little-endian ARGB), PIL gives RGBA. Need to swizzle.
            bgra_data = bytearray(len(data_bytes))
            for i in range(0, len(data_bytes), 4):
                r, g, b, a = data_bytes[i : i + 4]
                bgra_data[i : i + 4] = [b, g, r, a]
            data_bytes = bytes(bgra_data)
            stride = width * 4
        else:
            # For RGB, convert to RGBA first
            pil_image = pil_image.convert("RGBA")
            data_bytes = pil_image.tobytes()
            # Swizzle to BGRA
            bgra_data = bytearray(len(data_bytes))
            for i in range(0, len(data_bytes), 4):
                r, g, b, a = data_bytes[i : i + 4]
                bgra_data[i : i + 4] = [b, g, r, a]
            data_bytes = bytes(bgra_data)
            stride = width * 4

        # Convert to ctypes array
        data_array = (ctypes.c_ubyte * len(data_bytes)).from_buffer_copy(data_bytes)
        return cls(image_data=(data_array, width, height, stride))

    @classmethod
    def from_imgrs(cls, imgrs_image):
        """Create Image from imgrs Image."""
        # Assuming imgrs has similar interface
        data_bytes = imgrs_image.to_bytes()
        width = imgrs_image.width
        height = imgrs_image.height

        # Assume RGBA format, need to swizzle to BGRA for Cairo
        if len(data_bytes) == width * height * 4:  # RGBA
            bgra_data = bytearray(len(data_bytes))
            for i in range(0, len(data_bytes), 4):
                r, g, b, a = data_bytes[i : i + 4]
                bgra_data[i : i + 4] = [b, g, r, a]
            data_bytes = bytes(bgra_data)
            stride = width * 4
        else:
            # If not RGBA, try to get stride
            if hasattr(imgrs_image, "stride"):
                stride = imgrs_image.stride()
            else:
                stride = width * 4  # Assume 4 bytes per pixel

        # Convert to ctypes array
        data_array = (ctypes.c_ubyte * len(data_bytes)).from_buffer_copy(data_bytes)
        return cls(image_data=(data_array, width, height, stride))
