# PyEmoji2 Cross-Build Guide

This guide explains how to build and test pyemoji2 wheels locally and in CI.

## Local Cross-Build Testing

### Prerequisites

```bash
pip install cibuildwheel
```

### Build for Current Platform

```bash
python build_local.py
```

### Build for Specific Platform

```bash
# Linux only
python build_local.py --platform linux

# macOS only
python build_local.py --platform macos

# Windows only
python build_local.py --platform windows
```

### Build and Test Installation

```bash
python build_local.py --test
```

This will:
1. Build wheels for your platform
2. Create a temporary virtual environment
3. Install the wheel
4. Test basic functionality

## CI/CD Workflows

### Supported Platforms

- ✅ **Linux**: x86_64, i686
- ✅ **macOS**: x86_64, arm64
- ✅ **Windows**: x86_64

### Workflow Triggers

- **Build**: Manual trigger (`workflow_dispatch`)
- **Publish**: Manual trigger (`workflow_dispatch`) with PyPI token

### Build Process

1. **Dependencies**: Cairo and Pango built from source (headless)
2. **Compilation**: C extension compiled for each platform
3. **Bundling**: Libraries statically linked into wheels
4. **Testing**: Wheels uploaded as artifacts

## Manual Build (Alternative)

If you prefer not to use cibuildwheel:

### Linux
```bash
sudo apt install libcairo2-dev libpango1.0-dev pkg-config
python setup.py build_ext --inplace
pip install -e .
```

### macOS
```bash
brew install cairo pango pkg-config
python setup.py build_ext --inplace
pip install -e .
```

### Windows (MSYS2)
```bash
pacman -S mingw-w64-x86_64-cairo mingw-w64-x86_64-pango mingw-w64-x86_64-gcc
python setup.py build_ext --inplace
pip install -e .
```

## Troubleshooting

### Common Issues

1. **Missing system libraries**: Use the CI build process which builds everything from source
2. **Font rendering issues**: Ensure DejaVu Sans or compatible fonts are available
3. **Import errors**: Make sure the C extension was built correctly

### Debug Build

```bash
# Enable verbose output
export CIBW_BUILD_VERBOSITY=2

# Build with debug symbols
python build_local.py
```

## Distribution

Built wheels are zero-dependency and include all necessary libraries. Users can install with:

```bash
pip install pyemoji2
```

No system libraries required! 🎉