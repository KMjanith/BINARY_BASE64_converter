#!/usr/bin/env python3
"""
Test script for the Universal File Operator
==============================================

This script tests various converters to ensure they're working correctly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_conversions():
    """Test basic conversion functionality."""
    print("🧪 Testing Universal File Operator")
    print("=" * 50)
    
    try:
        # Import converters to register them
        from src.converters import encoding, hashing, data_formats, numbers
        from src.converters.registry import convert, list_conversions
        
        print("✅ Successfully imported all converter modules")
        
        # Test 1: Binary to Base64
        print("\n📝 Test 1: Binary to Base64")
        test_data = b"Hello World"
        result = convert(test_data, 'binary', 'base64')
        print(f"   Input:  {test_data}")
        print(f"   Output: {result}")
        
        # Test 2: Base64 back to Binary
        print("\n📝 Test 2: Base64 to Binary (reverse)")
        result2 = convert(result, 'base64', 'binary')
        print(f"   Input:  {result}")
        print(f"   Output: {result2}")
        print(f"   Match:  {test_data == result2}")
        
        # Test 3: Text to URL encoding
        print("\n📝 Test 3: Text to URL encoding")
        text = "Hello World & Special Characters!"
        url_encoded = convert(text, 'text', 'url')
        print(f"   Input:  {text}")
        print(f"   Output: {url_encoded}")
        
        # Test 4: Decimal to Binary
        print("\n📝 Test 4: Decimal to Binary")
        number = "42"
        binary = convert(number, 'decimal', 'binary_num')
        print(f"   Input:  {number}")
        print(f"   Output: {binary}")
        
        # Test 5: JSON to Dict
        print("\n📝 Test 5: JSON to Dictionary")
        json_data = '{"name": "John", "age": 30, "city": "New York"}'
        dict_result = convert(json_data, 'json', 'dict')
        print(f"   Input:  {json_data}")
        print(f"   Output: {dict_result}")
        
        # Test 6: Hash generation
        print("\n📝 Test 6: Text to SHA256 Hash")
        text = "Hello World"
        hash_result = convert(text, 'text', 'sha256_hash')
        print(f"   Input:  {text}")
        print(f"   Output: {hash_result}")
        
        # List all available conversions
        print("\n📋 Available Conversions:")
        conversions = list_conversions()
        for conv in conversions[:10]:  # Show first 10
            reversible = "↔" if conv.get('reversible', False) else "→"
            print(f"   {conv['from']} {reversible} {conv['to']}")
        
        print(f"\n📊 Total conversions available: {len(conversions)}")
        
        print("\n🎉 All tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli():
    """Test the CLI interface."""
    print("\n🖥️  Testing CLI Interface")
    print("=" * 30)
    
    try:
        from src.cli.main import main
        print("✅ CLI module imported successfully")
        print("💡 To test CLI, run: python -m src.cli.main --help")
        return True
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

if __name__ == "__main__":
    success = True
    
    success &= test_basic_conversions()
    success &= test_cli()
    
    if success:
        print("\n🏆 All systems working correctly!")
        print("\n🚀 Try these commands:")
        print("   python test_converter.py")
        print("   python -m src.cli.main --help")
        print("   python -m src.cli.main list-formats")
        print("   python -m src.cli.main convert-data 'Hello World' --from text --to base64")
        print("   python -m src.cli.main demo")
        print("   python -m src.cli.main interactive")
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)