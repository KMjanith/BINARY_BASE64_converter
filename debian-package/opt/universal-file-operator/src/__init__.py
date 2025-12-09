"""
Universal File Operator
=========================

An educational Python project for learning format conversions with bidirectional support.

This package provides:
- Bidirectional format conversion (if A->B is supported, B->A is automatically available)
- Plugin architecture for easy extension
- Web and CLI interfaces
- Batch processing capabilities
- Smart format detection

Examples:
    Basic usage:
        >>> from src.converters import get_converter
        >>> converter = get_converter('binary', 'base64')
        >>> result = converter.convert(b'Hello World')
        
    Using the registry:
        >>> from src.converters.registry import ConversionRegistry
        >>> registry = ConversionRegistry()
        >>> result = registry.convert(data, 'binary', 'base64')

Author: Kavindu Janith
Date: October 2025
"""

__version__ = "1.0.0"
__author__ = "Kavindu Janith"
__email__ = ""
__description__ = "Educational Universal File Operator with Web GUI"

# Version info as a tuple for programmatic access
VERSION_INFO = tuple(map(int, __version__.split('.')))

# Package-level imports for convenience
from .converters.registry import ConversionRegistry
from .utils.exceptions import ConversionError, UnsupportedFormatError

# Create a default global registry instance
default_registry = ConversionRegistry()

def convert(data, from_format: str, to_format: str, **options):
    """
    Convenience function for quick conversions using the default registry.
    
    Args:
        data: The data to convert
        from_format: Source format name
        to_format: Target format name
        **options: Additional conversion options
        
    Returns:
        Converted data
        
    Example:
        >>> import src
        >>> result = src.convert(b'Hello', 'binary', 'base64')
    """
    return default_registry.convert(data, from_format, to_format, **options)

def list_supported_conversions():
    """List all supported conversion pairs."""
    return default_registry.list_conversions()