#!/bin/bash
# Universal Format Converter - Quick Start Script
# This script sets up and starts the web interface

echo "🔄 Universal Format Converter - Quick Start"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "💡 Please run: python -m venv venv && source venv/bin/activate && pip install flask click rich pyyaml pillow python-magic"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if required packages are installed
echo "🔍 Checking dependencies..."
python -c "import flask, click, rich, yaml, PIL; print('✅ All dependencies found')" 2>/dev/null || {
    echo "❌ Missing dependencies! Installing..."
    pip install flask click rich pyyaml pillow python-magic
}

# Start the web application
echo "🌐 Starting web interface..."
echo "📋 Available at: http://127.0.0.1:5000"
echo "🎯 Press Ctrl+C to stop"
echo ""

# Set PYTHONPATH and start the Flask app
export PYTHONPATH=.
python src/web/app.py