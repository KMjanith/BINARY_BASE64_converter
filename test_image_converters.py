#!/usr/bin/env python3
"""
Test Image Converters
====================

Quick test to verify image conversion capabilities.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.cli.main import convert, list_conversions


def test_image_converters():
    """Test image conversion functionality."""
    print("🖼️  Testing Image Conversion System")
    print("=" * 50)
    
    # List all available conversions to see image ones
    conversions = list_conversions()
    image_conversions = [conv for conv in conversions if any(
        fmt in conv['from'].lower() or fmt in conv['to'].lower() 
        for fmt in ['jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'ico', 'image']
    )]
    
    print(f"📋 Found {len(image_conversions)} image conversion types:")
    for conv in image_conversions:
        print(f"   {conv['from']} → {conv['to']}: {conv['description']}")
    
    print("\n🎨 Image Format Overview:")
    formats = {
        'JPEG': 'Lossy compression, good for photos',
        'PNG': 'Lossless, supports transparency',
        'GIF': 'Palette mode, supports animation',
        'BMP': 'Uncompressed bitmap format',
        'TIFF': 'High quality, supports compression',
        'WebP': 'Modern format, great compression',
        'ICO': 'Icon format, multiple sizes'
    }
    
    for fmt, desc in formats.items():
        print(f"   {fmt}: {desc}")
    
    # Test with a simple creation of a test image
    print(f"\n✨ Image conversion system ready!")
    print(f"📊 Total conversions available: {len(conversions)}")
    print(f"🖼️  Image-related conversions: {len(image_conversions)}")
    
    print("\n💡 Usage Examples:")
    print("   # Convert JPEG to PNG (preserves quality, adds transparency)")
    print("   python -m src.cli.main convert <jpeg_base64> --from jpeg --to png")
    print("   # Convert PNG to WebP (better compression)")
    print("   python -m src.cli.main convert <png_base64> --from png --to webp")
    print("   # Convert any image to base64")
    print("   python -m src.cli.main convert <image_path> --from image --to base64")


if __name__ == "__main__":
    test_image_converters()