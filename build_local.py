#!/usr/bin/env python3
"""
Local cross-build testing script for pyemoji2.

This script helps test wheel building locally without pushing to CI.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, cwd=None, env=None):
    """Run a command and return success status."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, env=env, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}")
        print(f"Error: {e.stderr}")
        return False, e.stderr

def check_dependencies():
    """Check if required build tools are available."""
    tools = ['cibuildwheel', 'pip', 'python']
    missing = []

    for tool in tools:
        success, _ = run_command(f"which {tool}")
        if not success:
            missing.append(tool)

    if missing:
        print(f"Missing required tools: {', '.join(missing)}")
        print("Install with: pip install cibuildwheel")
        return False

    return True

def build_wheels(platform=None):
    """Build wheels for specified platform or all platforms."""
    if not check_dependencies():
        return False

    # Create dist directory
    os.makedirs('dist', exist_ok=True)

    # Set environment variables for cibuildwheel
    env = os.environ.copy()
    env.update({
        'CIBW_SKIP': 'pp* *-musllinux*',
        'CIBW_ARCHS_LINUX': 'x86_64 i686',
        'CIBW_BEFORE_ALL_LINUX': '''
            apt-get update && apt-get install -y build-essential wget pkg-config libpng-dev libfreetype6-dev libfontconfig1-dev libglib2.0-dev libffi-dev libpcre2-dev zlib1g-dev &&
            wget https://cairographics.org/releases/cairo-1.18.0.tar.xz &&
            tar xf cairo-1.18.0.tar.xz &&
            cd cairo-1.18.0 &&
            ./configure --prefix=/usr/local --disable-xlib --disable-gl --disable-xcb --enable-png=yes --enable-ft=yes &&
            make -j$(nproc) && make install &&
            cd .. &&
            wget https://download.gnome.org/sources/pango/1.50/pango-1.50.14.tar.xz &&
            tar xf pango-1.50.14.tar.xz &&
            cd pango-1.50.14 &&
            ./configure --prefix=/usr/local --without-x &&
            make -j$(nproc) && make install &&
            cd ..
        ''',
        'CIBW_BEFORE_ALL_MACOS': '''
            brew install cairo pango pkg-config || (
                curl -L https://cairographics.org/releases/cairo-1.18.0.tar.xz | tar xJ &&
                cd cairo-1.18.0 &&
                ./configure --prefix=/usr/local --disable-xlib --disable-gl --disable-xcb --enable-png=yes --enable-ft=yes &&
                make -j$(sysctl -n hw.ncpu) && sudo make install &&
                cd .. &&
                curl -L https://download.gnome.org/sources/pango/1.50/pango-1.50.14.tar.xz | tar xJ &&
                cd pango-1.50.14 &&
                ./configure --prefix=/usr/local --without-x &&
                make -j$(sysctl -n hw.ncpu) && sudo make install &&
                cd ..
            )
        ''',
        'CIBW_BEFORE_ALL_WINDOWS': '''
            pacman -S --noconfirm --needed mingw-w64-x86_64-gcc mingw-w64-x86_64-pkg-config curl tar make
            curl -L https://cairographics.org/releases/cairo-1.18.0.tar.xz -o cairo.tar.xz
            tar xf cairo.tar.xz
            cd cairo-1.18.0
            ./configure --prefix=/usr/local --disable-xlib --disable-gl --disable-xcb --enable-png=yes --enable-ft=yes
            make -j2
            make install
            cd ..
            curl -L https://download.gnome.org/sources/pango/1.50/pango-1.50.14.tar.xz -o pango.tar.xz
            tar xf pango.tar.xz
            cd pango-1.50.14
            ./configure --prefix=/usr/local --without-x
            make -j2
            make install
            cd ..
        ''',
        'CIBW_REPAIR_WHEEL_COMMAND_LINUX': 'auditwheel repair -w {dest_dir} {wheel}',
        'CIBW_REPAIR_WHEEL_COMMAND_MACOS': 'delocate-wheel --require-archs {delocate_archs} -w {dest_dir} -v {wheel}',
        'CIBW_REPAIR_WHEEL_COMMAND_WINDOWS': '',
    })

    # Build command
    cmd = 'cibuildwheel --output-dir dist'

    if platform:
        if platform == 'linux':
            cmd += ' --platform linux'
        elif platform == 'macos':
            cmd += ' --platform macos'
        elif platform == 'windows':
            cmd += ' --platform windows'
        else:
            print(f"Unknown platform: {platform}")
            return False

    print(f"Building wheels with command: {cmd}")
    success, output = run_command(cmd, env=env)

    if success:
        print("✅ Build successful!")
        print("Wheels created in dist/ directory:")
        wheels = list(Path('dist').glob('*.whl'))
        for wheel in wheels:
            print(f"  - {wheel.name}")
    else:
        print("❌ Build failed!")

    return success

def test_installation():
    """Test installing and importing the built wheel."""
    wheels = list(Path('dist').glob('*.whl'))
    if not wheels:
        print("No wheels found in dist/ directory")
        return False

    # Find the wheel for current platform
    current_platform = sys.platform
    platform_wheel = None

    for wheel in wheels:
        wheel_name = str(wheel)
        if 'linux' in wheel_name and current_platform.startswith('linux'):
            platform_wheel = wheel
            break
        elif 'macos' in wheel_name and current_platform == 'darwin':
            platform_wheel = wheel
            break
        elif 'win' in wheel_name and current_platform == 'win32':
            platform_wheel = wheel
            break

    if not platform_wheel:
        print(f"No compatible wheel found for platform: {current_platform}")
        return False

    print(f"Testing installation of: {platform_wheel.name}")

    # Create a temporary virtual environment for testing
    import tempfile
    import venv

    with tempfile.TemporaryDirectory() as temp_dir:
        venv_path = Path(temp_dir) / 'test_env'
        venv.create(venv_path, with_pip=True)

        # Install the wheel
        pip_path = venv_path / 'bin' / 'pip' if current_platform != 'win32' else venv_path / 'Scripts' / 'pip.exe'
        python_path = venv_path / 'bin' / 'python' if current_platform != 'win32' else venv_path / 'Scripts' / 'python.exe'

        success, _ = run_command(f'"{pip_path}" install "{platform_wheel}"')
        if not success:
            print("❌ Wheel installation failed!")
            return False

        # Test import
        test_script = '''
import sys
sys.path.insert(0, ".")
try:
    import pyemoji2
    print("✅ Import successful!")
    # Test basic functionality
    img = pyemoji2.Image.create_empty(100, 100)
    img.add_text("Test", 10, 10)
    img.save("test_output.png")
    print("✅ Basic functionality works!")
except Exception as e:
    print(f"❌ Import/functionality test failed: {e}")
    sys.exit(1)
'''

        with open(venv_path / 'test_script.py', 'w') as f:
            f.write(test_script)

        success, output = run_command(f'"{python_path}" test_script.py', cwd=str(venv_path))
        if success:
            print("✅ Wheel test successful!")
            return True
        else:
            print("❌ Wheel test failed!")
            print(output)
            return False

def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description='Local cross-build testing for pyemoji2')
    parser.add_argument('--platform', choices=['linux', 'macos', 'windows'],
                       help='Build for specific platform only')
    parser.add_argument('--test', action='store_true',
                       help='Test installation after building')

    args = parser.parse_args()

    print("🚀 PyEmoji2 Local Cross-Build Tester")
    print("=" * 40)

    # Build wheels
    if build_wheels(args.platform):
        if args.test:
            print("\n🧪 Testing installation...")
            test_installation()
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()