#!/bin/bash
# Universal Format Converter - CLI Demo Script
# This script demonstrates the CLI interface capabilities

echo "💻 Universal Format Converter - CLI Interface"
echo "============================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "💡 Please run setup first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo "🔄 Available CLI Commands:"
echo ""

echo "📋 1. List all available conversions:"
echo "   python -m src.cli.main list-conversions | head -10"
python -m src.cli.main list-conversions | head -10
echo "   ... and many more!"

echo ""
echo "💬 2. Text conversions:"
echo '   python -m src.cli.main convert "Hello World" --from text --to base64'
python -m src.cli.main convert "Hello World" --from text --to base64

echo ""
echo "🔢 3. Number conversions:"
echo '   python -m src.cli.main convert "42" --from decimal --to binary'
python -m src.cli.main convert "42" --from decimal --to binary

echo ""
echo "🔐 4. Hash generation:"
echo '   python -m src.cli.main convert "password123" --from text --to sha256'
python -m src.cli.main convert "password123" --from text --to sha256

echo ""
echo "✨ CLI interface ready! Try your own conversions with:"
echo "   python -m src.cli.main convert <data> --from <format> --to <format>"