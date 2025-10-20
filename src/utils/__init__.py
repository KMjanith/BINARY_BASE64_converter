"""
Utilities Package
================

Common utility functions and classes used throughout the project.

Modules:
- exceptions.py: Custom exception classes
- file_handler.py: File I/O utilities
- format_detection.py: Automatic format detection
- validation.py: Data validation helpers
- progress.py: Progress tracking utilities
"""

# Common utilities that might be used across the project
from .exceptions import ConversionError, UnsupportedFormatError, ValidationError

__all__ = [
    'ConversionError',
    'UnsupportedFormatError', 
    'ValidationError'
]