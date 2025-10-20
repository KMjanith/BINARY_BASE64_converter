#!/usr/bin/env python3
"""
Image Conversion Demo
====================

Practical demonstration of image format conversions with real examples.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.cli.main import convert


def demo_image_conversions():
    """Demonstrate image conversions with sample data."""
    print("🖼️  Image Conversion Demonstration")
    print("=" * 50)
    
    # Create a simple test image in base64 format (1x1 PNG pixel)
    # This is a minimal valid PNG image in base64
    sample_png_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    
    print("🎨 Testing with sample PNG image (1x1 transparent pixel)")
    print(f"📋 Sample PNG (base64): {sample_png_base64[:50]}...")
    
    # Demonstrate various image format conversions
    conversions_to_test = [
        ('png', 'jpeg', '📸 PNG to JPEG (removes transparency)'),
        ('png', 'bmp', '🖼️ PNG to BMP (uncompressed)'),
        ('png', 'gif', '🎞️ PNG to GIF (palette mode)'),
        ('png', 'webp', '🌐 PNG to WebP (modern format)'),
        ('png', 'tiff', '📷 PNG to TIFF (high quality)'),
        ('png', 'ico', '⚡ PNG to ICO (icon format)'),
    ]
    
    print(f"\n🔄 Testing {len(conversions_to_test)} image format conversions:")
    
    results = {}
    for from_fmt, to_fmt, description in conversions_to_test:
        try:
            print(f"\n   {description}")
            result = convert(sample_png_base64, from_fmt, to_fmt)
            
            # Store result and show preview
            results[f"{from_fmt}_to_{to_fmt}"] = result
            result_preview = result[:60] + "..." if len(result) > 60 else result
            print(f"   ✅ Success: {result_preview}")
            print(f"   📏 Output size: {len(result)} characters")
            
        except Exception as e:
            print(f"   ❌ Failed: {str(e)}")
    
    # Test reverse conversions
    print(f"\n🔄 Testing reverse conversions:")
    if 'png_to_jpeg' in results:
        try:
            jpeg_data = results['png_to_jpeg']
            print(f"\n   📸 Converting JPEG back to PNG")
            png_result = convert(jpeg_data, 'jpeg', 'png')
            print(f"   ✅ Success: Round-trip conversion completed")
            print(f"   📏 Final size: {len(png_result)} characters")
        except Exception as e:
            print(f"   ❌ Reverse conversion failed: {str(e)}")
    
    print(f"\n✨ Image Conversion Features:")
    print(f"   🎯 Quality Control: JPEG quality settings")
    print(f"   🌐 Transparency: PNG/ICO transparency support")
    print(f"   🎞️ Animation: GIF animation handling (first frame)")
    print(f"   📱 Optimization: WebP compression for smaller files")
    print(f"   ⚡ Icons: ICO format for favicons and app icons")
    print(f"   📷 Professional: TIFF with LZW compression")
    
    print(f"\n🚀 Web Interface Available:")
    print(f"   Open the Flask web app to try image conversions")
    print(f"   Upload image data as base64 or use the examples")
    print(f"   All {len(conversions_to_test)} conversion types supported in GUI!")


if __name__ == "__main__":
    demo_image_conversions()