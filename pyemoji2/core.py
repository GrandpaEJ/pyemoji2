import ctypes
import os
import glob
import pathlib

# Load the shared library
# We look for the extension built by setuptools in the same directory
# It will be named something like _emoji_img.cpython-*.so
_lib_files = glob.glob(str(pathlib.Path(__file__).parent / "_emoji_img*.so"))
if not _lib_files:
    # Fallback for local dev if not built yet (or if using makefile)
    # Try finding it in ../c/libemoji_img.so
    fallback = pathlib.Path(__file__).parent.parent / "c" / "libemoji_img.so"
    if fallback.exists():
        LIB_PATH = fallback
    else:
        raise FileNotFoundError("Could not find _emoji_img extension or libemoji_img.so")
else:
    LIB_PATH = pathlib.Path(_lib_files[0])

class EmojiImageManipulator(ctypes.Structure):
    pass

class EmojiEditor:
    def __init__(self, image_path=None, image_data=None, empty_size=None):
        self._lib = ctypes.CDLL(str(LIB_PATH))
        self._setup_signatures()
        
        self._manip = None
        self._data_ref = None # Keep reference to data to prevent GC
        
        if image_path:
            self._manip = self._lib.emoji_img_create(image_path.encode('utf-8'))
        elif image_data:
            # Expecting (data, width, height, stride)
            data, width, height, stride = image_data
            self._data_ref = data # Keep it alive!
            self._manip = self._lib.emoji_img_create_from_data(data, width, height, stride)
        elif empty_size:
            width, height = empty_size
            self._manip = self._lib.emoji_img_create_empty(width, height)
        else:
            raise ValueError("Must provide image_path, image_data, or empty_size")

    def _setup_signatures(self):
        self._lib.emoji_img_create.argtypes = [ctypes.c_char_p]
        self._lib.emoji_img_create.restype = ctypes.POINTER(EmojiImageManipulator)
        
        self._lib.emoji_img_create_from_data.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self._lib.emoji_img_create_from_data.restype = ctypes.POINTER(EmojiImageManipulator)

        self._lib.emoji_img_create_empty.argtypes = [ctypes.c_int, ctypes.c_int]
        self._lib.emoji_img_create_empty.restype = ctypes.POINTER(EmojiImageManipulator)

        self._lib.emoji_img_add_text.argtypes = [
            ctypes.POINTER(EmojiImageManipulator),
            ctypes.c_char_p,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_char_p,
            ctypes.c_double,
            ctypes.c_char_p
        ]
        
        self._lib.emoji_img_save.argtypes = [ctypes.POINTER(EmojiImageManipulator), ctypes.c_char_p]
        self._lib.emoji_img_destroy.argtypes = [ctypes.POINTER(EmojiImageManipulator)]

    def add_text(self, text, x, y, font_family="Sans", font_size=20.0, color="black"):
        self._lib.emoji_img_add_text(
            self._manip,
            text.encode('utf-8'),
            x, y,
            font_family.encode('utf-8'),
            font_size,
            color.encode('utf-8')
        )

    def save(self, output_path):
        self._lib.emoji_img_save(self._manip, output_path.encode('utf-8'))

    def __del__(self):
        if self._manip:
            self._lib.emoji_img_destroy(self._manip)

    @classmethod
    def create_empty(cls, width, height):
        return cls(empty_size=(width, height))


