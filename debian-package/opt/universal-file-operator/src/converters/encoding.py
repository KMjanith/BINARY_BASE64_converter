"""
Common Encoding Converters
=========================

This module implements the most commonly used text and binary encoding conversions.
These are bidirectional converters that handle everyday encoding needs.

Learning Concepts:
- Built-in Python encoding libraries
- Binary vs text data handling
- Error handling for encoding issues
- Reversible conversion patterns
"""

import base64
import binascii
import urllib.parse
import html
from typing import Union, Any
import logging

from .base_converter import ReversibleConverter, converter_info
from .registry import register_converter
from ..utils.exceptions import ConversionError, ValidationError

logger = logging.getLogger(__name__)


@register_converter('binary', 'base64', 'Binary data to Base64 encoding', reversible=True)
class BinaryBase64Converter(ReversibleConverter):
    """
    Convert between binary data and Base64 encoding.
    
    Base64 is commonly used for:
    - Email attachments
    - Data URLs in web pages
    - API data transmission
    - Storing binary data in text formats
    
    Examples:
        >>> converter = BinaryBase64Converter('binary', 'base64')
        >>> result = converter.convert(b'Hello World')
        >>> print(result)  # 'SGVsbG8gV29ybGQ='
    """
    
    def __init__(self, from_format: str, to_format: str):
        super().__init__(from_format, to_format, 
                         'Convert binary data to/from Base64 encoding')
        # Set the actual format pairs for ReversibleConverter
        self.format_a = 'binary'
        self.format_b = 'base64'
    
    def validate_input(self, data: Any) -> None:
        """Validate input data for binary/base64 conversion."""
        super().validate_input(data)
        
        if self.from_format == 'binary':
            if not isinstance(data, bytes):
                raise ValidationError(
                    f"Binary format requires bytes input, got {type(data).__name__}",
                    data_type=type(data).__name__,
                    expected_format='bytes'
                )
        elif self.from_format == 'base64':
            if not isinstance(data, str):
                raise ValidationError(
                    f"Base64 format requires string input, got {type(data).__name__}",
                    data_type=type(data).__name__,
                    expected_format='str'
                )
    
    def _convert_a_to_b(self, data: bytes, **options) -> str:
        """Convert binary to base64."""
        try:
            return base64.b64encode(data).decode('ascii')
        except Exception as e:
            raise ConversionError(f"Failed to encode binary to base64: {e}", original_error=e)
    
    def _convert_b_to_a(self, data: str, **options) -> bytes:
        """Convert base64 to binary."""
        try:
            # Clean up the base64 string (remove whitespace, newlines)
            cleaned_data = ''.join(data.split())
            return base64.b64decode(cleaned_data)
        except Exception as e:
            raise ConversionError(f"Failed to decode base64 to binary: {e}", original_error=e)


@register_converter('binary', 'hex', 'Binary data to hexadecimal encoding', reversible=True)
class BinaryHexConverter(ReversibleConverter):
    """
    Convert between binary data and hexadecimal encoding.
    
    Hexadecimal is commonly used for:
    - Color codes (#FF0000)
    - Memory addresses
    - Hash values
    - Low-level debugging
    """
    
    def __init__(self, from_format: str, to_format: str):
        super().__init__('binary', 'hex', 
                         'Convert binary data to/from hexadecimal encoding')
    
    def validate_input(self, data: Any) -> None:
        """Validate input data."""
        super().validate_input(data)
        
        if self.from_format == 'binary' and not isinstance(data, bytes):
            raise ValidationError(f"Binary format requires bytes input, got {type(data).__name__}")
        elif self.from_format == 'hex' and not isinstance(data, str):
            raise ValidationError(f"Hex format requires string input, got {type(data).__name__}")
    
    def _convert_a_to_b(self, data: bytes, **options) -> str:
        """Convert binary to hex."""
        try:
            # Options for hex formatting
            uppercase = options.get('uppercase', False)
            separator = options.get('separator', '')  # e.g., ':' for MAC addresses
            
            hex_str = data.hex()
            if uppercase:
                hex_str = hex_str.upper()
            
            if separator:
                # Insert separator every 2 characters
                hex_str = separator.join(hex_str[i:i+2] for i in range(0, len(hex_str), 2))
            
            return hex_str
        except Exception as e:
            raise ConversionError(f"Failed to encode binary to hex: {e}", original_error=e)
    
    def _convert_b_to_a(self, data: str, **options) -> bytes:
        """Convert hex to binary."""
        try:
            # Clean the hex string (remove separators, whitespace, 0x prefix)
            cleaned_data = data.replace('0x', '').replace(':', '').replace('-', '').replace(' ', '')
            return bytes.fromhex(cleaned_data)
        except ValueError as e:
            raise ConversionError(f"Invalid hex string: {e}", original_error=e)
        except Exception as e:
            raise ConversionError(f"Failed to decode hex to binary: {e}", original_error=e)


@register_converter('text', 'url', 'Text to URL encoding', reversible=True)
class TextUrlConverter(ReversibleConverter):
    """
    Convert between text and URL encoding (percent encoding).
    
    URL encoding is used for:
    - Web form submissions
    - Query parameters
    - Safe transmission of special characters in URLs
    """
    
    def __init__(self, from_format: str, to_format: str):
        super().__init__('text', 'url', 
                         'Convert text to/from URL encoding (percent encoding)')
    
    def validate_input(self, data: Any) -> None:
        """Validate input data."""
        super().validate_input(data)
        
        if not isinstance(data, str):
            raise ValidationError(f"URL encoding requires string input, got {type(data).__name__}")
    
    def _convert_a_to_b(self, data: str, **options) -> str:
        """Convert text to URL encoding."""
        try:
            # Options for URL encoding
            safe = options.get('safe', '')  # Characters to not encode
            encoding = options.get('encoding', 'utf-8')
            
            return urllib.parse.quote(data, safe=safe, encoding=encoding)
        except Exception as e:
            raise ConversionError(f"Failed to URL encode text: {e}", original_error=e)
    
    def _convert_b_to_a(self, data: str, **options) -> str:
        """Convert URL encoding to text."""
        try:
            encoding = options.get('encoding', 'utf-8')
            return urllib.parse.unquote(data, encoding=encoding)
        except Exception as e:
            raise ConversionError(f"Failed to URL decode text: {e}", original_error=e)


@register_converter('text', 'html', 'Text to HTML entity encoding', reversible=True)
class TextHtmlConverter(ReversibleConverter):
    """
    Convert between text and HTML entity encoding.
    
    HTML encoding is used for:
    - Displaying special characters in web pages
    - Preventing XSS attacks
    - Email content encoding
    """
    
    def __init__(self, from_format: str, to_format: str):
        super().__init__('text', 'html', 
                         'Convert text to/from HTML entity encoding')
    
    def validate_input(self, data: Any) -> None:
        """Validate input data."""
        super().validate_input(data)
        
        if not isinstance(data, str):
            raise ValidationError(f"HTML encoding requires string input, got {type(data).__name__}")
    
    def _convert_a_to_b(self, data: str, **options) -> str:
        """Convert text to HTML entities."""
        try:
            # Options for HTML encoding
            quote = options.get('quote', True)  # Whether to encode quotes
            
            if quote:
                return html.escape(data, quote=True)
            else:
                return html.escape(data, quote=False)
        except Exception as e:
            raise ConversionError(f"Failed to HTML encode text: {e}", original_error=e)
    
    def _convert_b_to_a(self, data: str, **options) -> str:
        """Convert HTML entities to text."""
        try:
            return html.unescape(data)
        except Exception as e:
            raise ConversionError(f"Failed to HTML decode text: {e}", original_error=e)


@register_converter('text', 'ascii', 'Text to ASCII encoding', reversible=True)
class TextAsciiConverter(ReversibleConverter):
    """
    Convert between text and ASCII encoding.
    
    ASCII encoding is used for:
    - Legacy system compatibility
    - Simple text protocols
    - Basic character validation
    """
    
    def __init__(self, from_format: str, to_format: str):
        super().__init__('text', 'ascii', 
                         'Convert text to/from ASCII encoding')
    
    def _convert_a_to_b(self, data: str, **options) -> str:
        """Convert text to ASCII (with error handling)."""
        try:
            # Options for ASCII encoding
            errors = options.get('errors', 'replace')  # 'strict', 'ignore', 'replace'
            
            # First encode to bytes, then decode to see ASCII representation
            ascii_bytes = data.encode('ascii', errors=errors)
            return ascii_bytes.decode('ascii')
        except Exception as e:
            raise ConversionError(f"Failed to convert to ASCII: {e}", original_error=e)
    
    def _convert_b_to_a(self, data: str, **options) -> str:
        """Convert ASCII to text (basically a pass-through with validation)."""
        try:
            # Validate that it's actually ASCII
            data.encode('ascii')
            return data
        except UnicodeEncodeError as e:
            raise ConversionError(f"Input contains non-ASCII characters: {e}", original_error=e)
        except Exception as e:
            raise ConversionError(f"Failed to process ASCII text: {e}", original_error=e)


@register_converter('base64', 'hex', 'Base64 to Hexadecimal via binary', reversible=True)
class Base64HexConverter(ReversibleConverter):
    """
    Convert between Base64 and Hexadecimal encoding.
    
    This converter works by going through binary as an intermediate step:
    Base64 -> Binary -> Hex (and vice versa)
    
    This demonstrates how converters can be chained for complex conversions.
    """
    
    def __init__(self, from_format: str, to_format: str):
        super().__init__('base64', 'hex', 
                         'Convert Base64 to/from Hexadecimal via binary conversion')
    
    def _convert_a_to_b(self, data: str, **options) -> str:
        """Convert base64 to hex via binary."""
        try:
            # Step 1: Base64 to binary
            binary_data = base64.b64decode(data)
            # Step 2: Binary to hex
            return binary_data.hex()
        except Exception as e:
            raise ConversionError(f"Failed to convert base64 to hex: {e}", original_error=e)
    
    def _convert_b_to_a(self, data: str, **options) -> str:
        """Convert hex to base64 via binary."""
        try:
            # Step 1: Hex to binary
            cleaned_data = data.replace('0x', '').replace(':', '').replace('-', '').replace(' ', '')
            binary_data = bytes.fromhex(cleaned_data)
            # Step 2: Binary to base64
            return base64.b64encode(binary_data).decode('ascii')
        except Exception as e:
            raise ConversionError(f"Failed to convert hex to base64: {e}", original_error=e)