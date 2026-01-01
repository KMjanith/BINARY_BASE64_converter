#!/usr/bin/env python3
"""
Test script for text comparison functionality.
"""

import sys
import os

# Add the project root to path for imports
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.converters.text_compare import compare_texts


def test_text_comparison():
    """Test the text comparison functionality."""
    
    print("Testing Text Comparison Functionality")
    print("=" * 50)
    
    # Test case 1: Similar texts
    text1 = "Hello world! This is a test sentence. How are you today?"
    text2 = "Hello world! This is a test message. How are you today?"
    
    print("\nTest 1: Similar texts")
    print(f"Text 1: {text1}")
    print(f"Text 2: {text2}")
    
    result1 = compare_texts(text1, text2)
    print(f"Similarity: {result1['similarity_percentage']}%")
    print(f"Words (Text 1): {result1['word_count_text1']}")
    print(f"Words (Text 2): {result1['word_count_text2']}")
    print(f"Chars (Text 1): {result1['char_count_text1']}")
    print(f"Chars (Text 2): {result1['char_count_text2']}")
    
    # Test case 2: Completely different texts
    text3 = "The quick brown fox jumps over the lazy dog."
    text4 = "Python is a powerful programming language for data science."
    
    print("\n" + "-" * 50)
    print("Test 2: Different texts")
    print(f"Text 1: {text3}")
    print(f"Text 2: {text4}")
    
    result2 = compare_texts(text3, text4)
    print(f"Similarity: {result2['similarity_percentage']}%")
    print(f"Words (Text 1): {result2['word_count_text1']}")
    print(f"Words (Text 2): {result2['word_count_text2']}")
    
    # Test case 3: Identical texts
    text5 = "This is exactly the same text."
    text6 = "This is exactly the same text."
    
    print("\n" + "-" * 50)
    print("Test 3: Identical texts")
    print(f"Text 1: {text5}")
    print(f"Text 2: {text6}")
    
    result3 = compare_texts(text5, text6)
    print(f"Similarity: {result3['similarity_percentage']}%")
    
    # Test case 4: Empty texts
    print("\n" + "-" * 50)
    print("Test 4: Empty and non-empty")
    result4 = compare_texts("", "Some text here")
    print(f"Similarity (empty vs text): {result4['similarity_percentage']}%")
    
    print("\n" + "=" * 50)
    print("All tests completed!")


if __name__ == "__main__":
    test_text_comparison()