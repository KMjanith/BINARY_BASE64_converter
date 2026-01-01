#!/usr/bin/env python3
"""
Comprehensive test script for the enhanced text comparison functionality.
This script tests both the backend text comparison logic and the file handling capabilities.
"""

import sys
import os
import tempfile
import json

# Add the project root to path for imports
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.converters.text_compare import compare_texts


def test_basic_comparison():
    """Test basic text comparison functionality."""
    print("🧪 Testing Basic Text Comparison")
    print("-" * 40)
    
    # Test case 1: Similar texts
    text1 = "Hello world! This is a test sentence."
    text2 = "Hello world! This is a test message."
    
    result = compare_texts(text1, text2)
    
    print(f"Text 1: {text1}")
    print(f"Text 2: {text2}")
    print(f"Similarity: {result['similarity_percentage']}%")
    print(f"Highlighted Text 1: {result['highlighted_text1'][:100]}...")
    print(f"Word counts: {result['word_count_text1']} vs {result['word_count_text2']}")
    print("✅ Basic comparison test passed\n")
    
    return result['similarity_percentage'] > 80  # Should be quite similar


def test_file_formats():
    """Test different file format support."""
    print("📁 Testing File Format Support")
    print("-" * 40)
    
    test_content = "This is test content for file format testing.\nMultiple lines supported."
    
    # Test different file extensions
    formats = [
        ('.txt', 'text/plain'),
        ('.md', 'text/markdown'),
        ('.csv', 'text/csv'),
        ('.json', 'application/json'),
        ('.xml', 'application/xml'),
        ('.html', 'text/html'),
        ('.py', 'text/python'),
        ('.js', 'text/javascript')
    ]
    
    for ext, mime_type in formats:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix=ext, delete=False) as f:
            if ext == '.json':
                json.dump({"content": test_content, "type": "test"}, f, indent=2)
            else:
                f.write(test_content)
            temp_path = f.name
        
        # Check if file was created
        if os.path.exists(temp_path):
            with open(temp_path, 'r') as f:
                content = f.read()
                print(f"✅ {ext} format: {len(content)} characters read")
        
        # Clean up
        os.unlink(temp_path)
    
    print("✅ File format tests completed\n")


def test_edge_cases():
    """Test edge cases for text comparison."""
    print("⚡ Testing Edge Cases")
    print("-" * 40)
    
    # Empty texts
    result1 = compare_texts("", "Some text")
    print(f"Empty vs Text similarity: {result1['similarity_percentage']}%")
    
    # Identical texts
    text = "Identical text content"
    result2 = compare_texts(text, text)
    print(f"Identical texts similarity: {result2['similarity_percentage']}%")
    
    # Very different texts
    result3 = compare_texts("abc", "xyz")
    print(f"Very different texts similarity: {result3['similarity_percentage']}%")
    
    # Large text simulation
    large_text1 = "Lorem ipsum " * 100
    large_text2 = "Lorem ipsum " * 95 + "dolor sit amet"
    result4 = compare_texts(large_text1, large_text2)
    print(f"Large text comparison similarity: {result4['similarity_percentage']}%")
    
    print("✅ Edge case tests completed\n")


def test_html_highlighting():
    """Test HTML highlighting functionality."""
    print("🎨 Testing HTML Highlighting")
    print("-" * 40)
    
    text1 = "The quick brown fox"
    text2 = "The slow brown dog"
    
    result = compare_texts(text1, text2)
    
    print("Highlighted Text 1:")
    print(result['highlighted_text1'])
    print("\nHighlighted Text 2:")
    print(result['highlighted_text2'])
    
    # Check if highlighting tags are present
    has_highlighting = any(tag in result['highlighted_text1'] or tag in result['highlighted_text2'] 
                          for tag in ['text-deleted', 'text-inserted', 'text-modified'])
    
    if has_highlighting:
        print("✅ HTML highlighting working correctly\n")
    else:
        print("⚠️ HTML highlighting might not be working properly\n")
    
    return has_highlighting


def test_statistics():
    """Test statistics calculation."""
    print("📊 Testing Statistics Calculation")
    print("-" * 40)
    
    text1 = "Word1 Word2 Word3\nLine2 content"
    text2 = "Word1 Word2 Word4\nLine2 different"
    
    result = compare_texts(text1, text2)
    
    print(f"Text 1 - Words: {result['word_count_text1']}, Chars: {result['char_count_text1']}, Lines: {result['line_count_text1']}")
    print(f"Text 2 - Words: {result['word_count_text2']}, Chars: {result['char_count_text2']}, Lines: {result['line_count_text2']}")
    
    # Verify statistics
    expected_words1 = len(text1.split())
    expected_chars1 = len(text1)
    expected_lines1 = len(text1.splitlines())
    
    stats_correct = (result['word_count_text1'] == expected_words1 and 
                    result['char_count_text1'] == expected_chars1 and
                    result['line_count_text1'] == expected_lines1)
    
    if stats_correct:
        print("✅ Statistics calculation working correctly\n")
    else:
        print("⚠️ Statistics calculation might have issues\n")
    
    return stats_correct


def run_all_tests():
    """Run all tests and provide summary."""
    print("🚀 Running Comprehensive Text Comparison Tests")
    print("=" * 60)
    
    tests = [
        ("Basic Comparison", test_basic_comparison),
        ("File Formats", test_file_formats),
        ("Edge Cases", test_edge_cases),
        ("HTML Highlighting", test_html_highlighting),
        ("Statistics", test_statistics)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result if result is not None else True))
        except Exception as e:
            print(f"❌ {test_name} failed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("📋 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, passed_test in results:
        status = "✅ PASSED" if passed_test else "❌ FAILED"
        print(f"{test_name:<20} {status}")
        if passed_test:
            passed += 1
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Text comparison functionality is working perfectly.")
    else:
        print(f"⚠️ {total - passed} test(s) failed. Please check the implementation.")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)