"""
Converters Package
=================

This package contains all format converters and the conversion registry.

The converters package follows a plugin architecture where each converter
is a separate module that registers itself with the global registry.

Key Components:
- registry.py: Central registry for all converters
- base_converter.py: Abstract base class for all converters
- encoding/: Text and binary encoding converters
- image/: Image format converters
- document/: Document format converters

Learning Concepts:
- Plugin Architecture: Dynamic loading of converter modules
- Registry Pattern: Central registration and discovery system
- Abstract Base Classes: Enforcing consistent interfaces
- Decorators: Automatic registration of converters
"""

# Import the registry and make it available at package level
from .registry import ConversionRegistry, register_converter
from .base_converter import BaseConverter, ConversionError

# Create default registry instance
_default_registry = ConversionRegistry()

def get_converter(from_format: str, to_format: str):
    """
    Get a converter for the specified format pair.
    
    Args:
        from_format: Source format name
        to_format: Target format name
        
    Returns:
        Converter instance
        
    Example:
        >>> converter = get_converter('binary', 'base64')
        >>> result = converter.convert(b'Hello World')
    """
    return _default_registry.get_converter(from_format, to_format)

def convert(data, from_format: str, to_format: str, **options):
    """
    Direct conversion using the default registry.
    
    Args:
        data: Data to convert
        from_format: Source format
        to_format: Target format
        **options: Conversion options
        
    Returns:
        Converted data
    """
    return _default_registry.convert(data, from_format, to_format, **options)

# Auto-import all converter modules to register them
# This happens when the converters package is imported
def _load_converters():
    """Load all converter modules to trigger registration."""
    import importlib
    import pkgutil
    
    # Get the current package path
    import os
    package_path = os.path.dirname(__file__)
    
    # Find and import all submodules
    for finder, name, ispkg in pkgutil.iter_modules([package_path]):
        if name not in ['__init__', 'registry', 'base_converter']:
            try:
                importlib.import_module(f'.{name}', package=__name__)
            except ImportError as e:
                print(f"Warning: Could not load converter module {name}: {e}")

# Load converters when the package is imported
_load_converters()