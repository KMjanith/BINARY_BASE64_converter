@echo off
REM Universal Format Converter - Windows Startup Script
REM ===================================================

echo 🚀 Starting Universal Format Converter...
echo =========================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if virtual environment exists, create if it doesn't
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📋 Installing dependencies...
pip install --upgrade pip
pip install flask pillow click rich pyyaml

REM Create favicon if it doesn't exist
if not exist "src\web\static\favicon.ico" (
    echo 🎨 Creating favicon...
    mkdir src\web\static 2>nul
    python -c "from PIL import Image, ImageDraw; img = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); draw = ImageDraw.Draw(img); draw.ellipse([2, 2, 29, 29], fill=(39, 174, 96, 255), outline=(30, 132, 73, 255), width=2); draw.polygon([(8, 12), (14, 16), (8, 20), (10, 22), (18, 16), (10, 10)], fill=(255, 255, 255, 255)); draw.polygon([(14, 10), (22, 16), (14, 22), (16, 20), (20, 16), (16, 12)], fill=(255, 255, 255, 255)); img.save('src/web/static/favicon.ico', format='ICO', sizes=[(16, 16), (32, 32)]); print('✅ Favicon created')"
)

echo.
echo 🌟 Universal Format Converter is ready!
echo =======================================
echo.
echo Available interfaces:
echo   🌐 Web Interface: Starting web server...
echo   💻 CLI Interface: Available in terminal
echo.
echo 🚀 Launching web interface at http://127.0.0.1:5000
echo.
echo 💡 Usage Options:
echo    • Open http://127.0.0.1:5000 in your browser for web interface
echo    • Use 'python src/cli/main.py --help' for CLI commands
echo.
echo 📝 Supported conversions: 70+ format combinations
echo.
echo Press Ctrl+C to stop the server
echo =================================
echo.

REM Start the Flask web server
cd src\web
python app.py