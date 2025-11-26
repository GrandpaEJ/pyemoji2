# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Fixed
- CentOS 7 EOL mirror issues by switching to vault.centos.org
- Package installation commands in CI workflows
- Windows build configuration with delvewheel
- Segmentation fault in PyPI wheels by building Cairo/Pango without OpenGL/X11 dependencies

### Changed
- Improved README with comprehensive examples and API reference
- Enhanced CI/CD workflows for better reliability

## [0.1.0] - 2025-11-20

### Added
- Initial release of `pyemoji2`
- High-performance C extension using Cairo and Pango for text/emoji rendering
- Python wrapper with ctypes for easy integration
- `EmojiEditor.create_empty()` for creating blank images
- `EmojiEditor.add_text()` for adding text and emojis
- Support for custom fonts, sizes, and colors
- Cross-platform support (Linux x86_64/aarch64, macOS x86_64/arm64, Windows x64)
- Termux (Android) support via source build
- GitHub Actions workflows for automated wheel building
- Manual PyPI publish workflow
- **Zero system dependencies** - all libraries bundled in wheels
- Comprehensive README with installation instructions

### Technical Details
- Removed Pillow dependency for zero Python overhead
- Native Cairo surface creation for maximum speed
- Extracted Cairo and Pango headers to `c/include/` for build portability
- Build system using `setuptools` with `pkg-config` integration
- ARM64 wheel support via QEMU in CI
- Library bundling using `auditwheel` (Linux), `delocate` (macOS), `delvewheel` (Windows)

### Dependencies
- Runtime: None (all bundled)
- Build-time: `libcairo2`, `libpango1.0`, `pkg-config`

