# 🚀 Quick Start Guide

## One-Click Startup

### Linux/Mac:
```bash
./start_converter.sh
```

### Windows:
```cmd
start_converter.bat
```

## What it does:
1. ✅ Checks Python installation
2. 📦 Creates virtual environment (if needed)
3. 📥 Installs dependencies automatically
4. 🎨 Creates favicon
5. 🌐 Starts web server at http://127.0.0.1:5000

## Manual Startup (Alternative):
```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate.bat  # Windows

# 2. Install dependencies
pip install flask pillow click rich pyyaml

# 3. Start web interface
cd src/web && python app.py

# 4. Open browser: http://127.0.0.1:5000
```

## CLI Usage:
```bash
# After activation
python src/cli/main.py "Hello World" text base64
python src/cli/main.py --list-conversions
```

## Features:
- 🌐 **Web Interface**: User-friendly browser interface
- 💻 **CLI Interface**: Command-line tool for automation
- 📷 **Image Support**: Upload/convert PNG, JPEG, GIF, etc.
- 🔄 **70+ Conversions**: Text, binary, images, hashes, data formats
- 🎨 **Professional UI**: Green theme with drag-drop support