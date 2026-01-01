"""
Text Comparison Utilities
========================

This module provides text comparison functionality with highlighting of differences
and similarity percentage calculation.

Learning Concepts:
- Difflib for text comparison
- Sequence matching algorithms
- HTML generation for highlighting
- Similarity percentage calculation
"""

import difflib
from typing import Tuple, List, Dict, Any
import html


class TextComparator:
    """Text comparison utility with highlighting and similarity calculation."""
    
    def __init__(self):
        """Initialize the text comparator."""
        pass
    
    def compare_texts(self, text1: str, text2: str) -> Dict[str, Any]:
        """
        Compare two texts and return detailed comparison results.
        
        Args:
            text1: First text to compare
            text2: Second text to compare
            
        Returns:
            Dictionary containing:
            - highlighted_text1: HTML with highlighted differences in text1
            - highlighted_text2: HTML with highlighted differences in text2
            - similarity_percentage: Similarity as percentage (0-100)
            - word_count_text1: Word count of text1
            - word_count_text2: Word count of text2
            - char_count_text1: Character count of text1
            - char_count_text2: Character count of text2
        """
        
        # Calculate similarity percentage
        similarity = self._calculate_similarity(text1, text2)
        
        # Generate highlighted HTML
        highlighted_text1, highlighted_text2 = self._generate_highlighted_html(text1, text2)
        
        # Calculate statistics
        stats = self._calculate_statistics(text1, text2)
        
        return {
            'highlighted_text1': highlighted_text1,
            'highlighted_text2': highlighted_text2,
            'similarity_percentage': round(similarity * 100, 2),
            **stats
        }
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity ratio between two texts using SequenceMatcher.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity ratio (0.0 to 1.0)
        """
        matcher = difflib.SequenceMatcher(None, text1, text2)
        return matcher.ratio()
    
    def _generate_highlighted_html(self, text1: str, text2: str) -> Tuple[str, str]:
        """
        Generate HTML with highlighted differences for both texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Tuple of (highlighted_text1, highlighted_text2)
        """
        
        # Split texts into lines for better comparison
        lines1 = text1.splitlines(keepends=True)
        lines2 = text2.splitlines(keepends=True)
        
        # Create diff
        differ = difflib.unified_diff(lines1, lines2, n=0)
        diff_list = list(differ)
        
        # If no differences, return escaped original texts
        if len(diff_list) <= 2:  # Only headers
            return html.escape(text1), html.escape(text2)
        
        # Use HtmlDiff for better formatting
        html_differ = difflib.HtmlDiff(wrapcolumn=80)
        diff_table = html_differ.make_table(lines1, lines2, 
                                          context=True, 
                                          numlines=3)
        
        # Extract the two columns from the diff table
        highlighted1, highlighted2 = self._extract_highlighted_texts(text1, text2)
        
        return highlighted1, highlighted2
    
    def _extract_highlighted_texts(self, text1: str, text2: str) -> Tuple[str, str]:
        """
        Extract highlighted texts by comparing character by character.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Tuple of highlighted HTML strings
        """
        
        # Use SequenceMatcher for detailed comparison
        matcher = difflib.SequenceMatcher(None, text1, text2)
        
        highlighted1 = []
        highlighted2 = []
        
        # Process each matching block
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            text1_segment = text1[i1:i2]
            text2_segment = text2[j1:j2]
            
            if tag == 'equal':
                # Identical segments
                highlighted1.append(html.escape(text1_segment))
                highlighted2.append(html.escape(text2_segment))
            elif tag == 'delete':
                # Deleted from text1
                highlighted1.append(f'<span class="text-deleted">{html.escape(text1_segment)}</span>')
            elif tag == 'insert':
                # Inserted in text2
                highlighted2.append(f'<span class="text-inserted">{html.escape(text2_segment)}</span>')
            elif tag == 'replace':
                # Modified segments
                highlighted1.append(f'<span class="text-modified">{html.escape(text1_segment)}</span>')
                highlighted2.append(f'<span class="text-modified">{html.escape(text2_segment)}</span>')
        
        return ''.join(highlighted1), ''.join(highlighted2)
    
    def _calculate_statistics(self, text1: str, text2: str) -> Dict[str, int]:
        """
        Calculate various statistics for both texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Dictionary with statistics
        """
        
        return {
            'word_count_text1': len(text1.split()) if text1.strip() else 0,
            'word_count_text2': len(text2.split()) if text2.strip() else 0,
            'char_count_text1': len(text1),
            'char_count_text2': len(text2),
            'line_count_text1': len(text1.splitlines()) if text1 else 0,
            'line_count_text2': len(text2.splitlines()) if text2 else 0,
        }
    
    def get_detailed_diff(self, text1: str, text2: str) -> List[str]:
        """
        Get a detailed line-by-line diff.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            List of diff lines
        """
        
        lines1 = text1.splitlines(keepends=True)
        lines2 = text2.splitlines(keepends=True)
        
        diff = list(difflib.unified_diff(
            lines1, lines2,
            fromfile='Text 1',
            tofile='Text 2',
            lineterm=''
        ))
        
        return diff


# Create global instance
text_comparator = TextComparator()


def compare_texts(text1: str, text2: str) -> Dict[str, Any]:
    """
    Convenience function to compare two texts.
    
    Args:
        text1: First text to compare
        text2: Second text to compare
        
    Returns:
        Comparison results dictionary
    """
    return text_comparator.compare_texts(text1, text2)