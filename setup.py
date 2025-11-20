from setuptools import setup, Extension
import subprocess
import os

def pkg_config(package, kw):
    flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}
    try:
        output = subprocess.check_output(
            ['pkg-config', '--cflags', '--libs', package],
            text=True
        )
    except subprocess.CalledProcessError:
        print(f"Warning: pkg-config failed for {package}")
        return

    for token in output.split():
        if token[:2] in flag_map:
            kw.setdefault(flag_map[token[:2]], []).append(token[2:])
        else:
            kw.setdefault('extra_compile_args', []).append(token)

ext_modules = []

# Define the extension
# We build it as a Python extension so setuptools handles the filename/location
# But we don't use Python.h, so we can't import it. We load it via ctypes.
emoji_img_ext = Extension(
    'pyemoji2._emoji_img',
    sources=['c/emoji_img.c'],
    include_dirs=['c/include'],
)

# Add pkg-config flags
pkg_config('cairo', emoji_img_ext.__dict__)
pkg_config('pangocairo', emoji_img_ext.__dict__)

setup(
    ext_modules=[emoji_img_ext],
)
