#!/bin/bash

# Universal Format Converter - One-Click Startup Script
# =====================================================

set -e  # Exit on any error

echo "🚀 Starting Universal Format Converter..."
echo "========================================="

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if virtual environment exists, create if it doesn't
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
echo "📋 Checking dependencies..."
if ! python -c "import flask, PIL, click, rich" 2>/dev/null; then
    echo "📥 Installing required packages..."
    pip install --upgrade pip
    pip install flask pillow click rich pyyaml
    echo "✅ Dependencies installed"
else
    echo "✅ All dependencies are already installed"
fi

# Check if favicon exists, create if it doesn't
if [ ! -f "src/web/static/favicon.ico" ]; then
    echo "🎨 Creating favicon..."
    mkdir -p src/web/static
    python3 -c "
from PIL import Image, ImageDraw
img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
draw.ellipse([2, 2, 29, 29], fill=(39, 174, 96, 255), outline=(30, 132, 73, 255), width=2)
draw.polygon([(8, 12), (14, 16), (8, 20), (10, 22), (18, 16), (10, 10)], fill=(255, 255, 255, 255))
draw.polygon([(14, 10), (22, 16), (14, 22), (16, 20), (20, 16), (16, 12)], fill=(255, 255, 255, 255))
img.save('src/web/static/favicon.ico', format='ICO', sizes=[(16, 16), (32, 32)])
print('✅ Favicon created')
"
fi

echo ""
echo "🌟 Universal Format Converter is ready!"
echo "======================================="
echo ""
echo "Available interfaces:"
echo "  🌐 Web Interface: Starting web server..."
echo "  💻 CLI Interface: Available in terminal"
echo ""

# Start the web server
echo "🚀 Launching web interface at http://127.0.0.1:5000"
echo ""
echo "💡 Usage Options:"
echo "   • Open http://127.0.0.1:5000 in your browser for web interface"
echo "   • Use 'python src/cli/main.py --help' for CLI commands"
echo ""
echo "📝 Supported conversions: 70+ format combinations including:"
echo "   • Text ↔ Binary ↔ Base64 ↔ Hex"
echo "   • Image formats (PNG, JPEG, GIF, BMP, TIFF, WebP, ICO)"  
echo "   • Data formats (JSON, CSV, YAML, XML)"
echo "   • Hash functions (MD5, SHA1, SHA256, SHA512)"
echo "   • Number bases (Decimal, Binary, Hex, Octal)"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"
echo ""

# Start the Flask web server
cd src/web && python app.py