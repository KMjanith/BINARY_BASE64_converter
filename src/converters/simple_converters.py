"""
Simple Converter Classes
=======================

This module implements simple, single-direction converters.
Each converter handles one specific conversion type without automatic reversal.

Learning Concepts:
- Single Responsibility Principle
- Explicit converter registration
- Simple inheritance hierarchy
"""

import base64
import binascii
import urllib.parse
import html
import hashlib
import zlib
import json
import csv
import io
from typing import Union, Any
import logging

from .base_converter import BaseConverter
from .registry import register_converter
from ..utils.exceptions import ConversionError, ValidationError

logger = logging.getLogger(__name__)

# Optional YAML support
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# ============================================================================
# TEXT AND BINARY ENCODING CONVERTERS
# ============================================================================

@register_converter('binary', 'base64', 'Convert binary data to Base64 string')
class BinaryToBase64Converter(BaseConverter):
    """Convert binary data to Base64 string."""
    
    def __init__(self, from_format='binary', to_format='base64'):
        super().__init__('binary', 'base64', 'Convert binary data to Base64 string')
    
    def validate_input(self, data: Any) -> None:
        super().validate_input(data)
        if isinstance(data, str):
            # Validate binary string format (only 0s and 1s)
            if not all(c in '01' for c in data.replace(' ', '')):
                raise ValidationError(f"Binary string must contain only 0s and 1s")
        elif not isinstance(data, bytes):
            raise ValidationError(f"Binary input requires bytes or binary string, got {type(data).__name__}")
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        try:
            if isinstance(data, str):
                # Convert binary string to bytes
                binary_str = data.replace(' ', '')  # Remove spaces
                if len(binary_str) % 8 != 0:
                    # Pad with zeros to make it a multiple of 8
                    binary_str = binary_str.zfill((len(binary_str) + 7) // 8 * 8)
                
                # Convert binary string to bytes
                byte_data = bytes(int(binary_str[i:i+8], 2) for i in range(0, len(binary_str), 8))
                return base64.b64encode(byte_data).decode('ascii')
            else:
                # Already bytes
                return base64.b64encode(data).decode('ascii')
        except Exception as e:
            raise ConversionError(f"Failed to encode to base64: {e}", original_error=e)


@register_converter('base64', 'binary', 'Convert Base64 string to binary data')
class Base64ToBinaryConverter(BaseConverter):
    """Convert Base64 string to binary data."""
    
    def __init__(self, from_format='base64', to_format='binary'):
        super().__init__('base64', 'binary', 'Convert Base64 string to binary data')
    
    def validate_input(self, data: Any) -> None:
        super().validate_input(data)
        if not isinstance(data, str):
            raise ValidationError(f"Base64 input requires string, got {type(data).__name__}")
    
    def _convert(self, data: str, **options) -> bytes:
        try:
            cleaned_data = ''.join(data.split())
            return base64.b64decode(cleaned_data)
        except Exception as e:
            raise ConversionError(f"Failed to decode base64: {e}", original_error=e)


@register_converter('binary', 'hex', 'Convert binary data to hexadecimal string')
class BinaryToHexConverter(BaseConverter):
    """Convert binary data to hexadecimal."""
    
    def __init__(self, from_format='binary', to_format='hex'):
        super().__init__('binary', 'hex', 'Convert binary data to hexadecimal string')
    
    def validate_input(self, data: Any) -> None:
        super().validate_input(data)
        if isinstance(data, str):
            # Validate binary string format (only 0s and 1s)
            if not all(c in '01' for c in data.replace(' ', '')):
                raise ValidationError(f"Binary string must contain only 0s and 1s")
        elif not isinstance(data, bytes):
            raise ValidationError(f"Binary input requires bytes or binary string, got {type(data).__name__}")
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        try:
            uppercase = options.get('uppercase', False)
            separator = options.get('separator', '')
            
            if isinstance(data, str):
                # Convert binary string to bytes first
                binary_str = data.replace(' ', '')  # Remove spaces
                if len(binary_str) % 8 != 0:
                    # Pad with zeros to make it a multiple of 8
                    binary_str = binary_str.zfill((len(binary_str) + 7) // 8 * 8)
                
                # Convert binary string to bytes
                byte_data = bytes(int(binary_str[i:i+8], 2) for i in range(0, len(binary_str), 8))
                hex_str = byte_data.hex()
            else:
                hex_str = data.hex()
            
            if uppercase:
                hex_str = hex_str.upper()
            
            if separator:
                hex_str = separator.join(hex_str[i:i+2] for i in range(0, len(hex_str), 2))
            
            return hex_str
        except Exception as e:
            raise ConversionError(f"Failed to encode to hex: {e}", original_error=e)


@register_converter('hex', 'binary', 'Convert hexadecimal string to binary data')
class HexToBinaryConverter(BaseConverter):
    """Convert hexadecimal string to binary data."""
    
    def __init__(self, from_format='hex', to_format='binary'):
        super().__init__('hex', 'binary', 'Convert hexadecimal string to binary data')
    
    def validate_input(self, data: Any) -> None:
        super().validate_input(data)
        if not isinstance(data, str):
            raise ValidationError(f"Hex input requires string, got {type(data).__name__}")
    
    def _convert(self, data: str, **options) -> bytes:
        try:
            cleaned_data = data.replace('0x', '').replace(':', '').replace('-', '').replace(' ', '')
            return bytes.fromhex(cleaned_data)
        except Exception as e:
            raise ConversionError(f"Failed to decode hex: {e}", original_error=e)


@register_converter('text', 'url_encoded', 'Convert text to URL encoded string')
class TextToUrlConverter(BaseConverter):
    """Convert text to URL encoding."""
    
    def __init__(self, from_format='text', to_format='url_encoded'):
        super().__init__('text', 'url_encoded', 'Convert text to URL encoded string')
    
    def validate_input(self, data: Any) -> None:
        super().validate_input(data)
        if not isinstance(data, str):
            raise ValidationError(f"Text input requires string, got {type(data).__name__}")
    
    def _convert(self, data: str, **options) -> str:
        try:
            safe = options.get('safe', '')
            encoding = options.get('encoding', 'utf-8')
            return urllib.parse.quote(data, safe=safe, encoding=encoding)
        except Exception as e:
            raise ConversionError(f"Failed to URL encode: {e}", original_error=e)


@register_converter('url_encoded', 'text', 'Convert URL encoded string to text')
class UrlToTextConverter(BaseConverter):
    """Convert URL encoding to text."""
    
    def __init__(self, from_format='url_encoded', to_format='text'):
        super().__init__('url_encoded', 'text', 'Convert URL encoded string to text')
    
    def validate_input(self, data: Any) -> None:
        super().validate_input(data)
        if not isinstance(data, str):
            raise ValidationError(f"URL encoded input requires string, got {type(data).__name__}")
    
    def _convert(self, data: str, **options) -> str:
        try:
            encoding = options.get('encoding', 'utf-8')
            return urllib.parse.unquote(data, encoding=encoding)
        except Exception as e:
            raise ConversionError(f"Failed to URL decode: {e}", original_error=e)


@register_converter('text', 'html_encoded', 'Convert text to HTML encoded string')
class TextToHtmlConverter(BaseConverter):
    """Convert text to HTML encoding."""
    
    def __init__(self, from_format='text', to_format='html_encoded'):
        super().__init__('text', 'html_encoded', 'Convert text to HTML encoded string')
    
    def validate_input(self, data: Any) -> None:
        super().validate_input(data)
        if not isinstance(data, str):
            raise ValidationError(f"Text input requires string, got {type(data).__name__}")
    
    def _convert(self, data: str, **options) -> str:
        try:
            quote = options.get('quote', True)
            return html.escape(data, quote=quote)
        except Exception as e:
            raise ConversionError(f"Failed to HTML encode: {e}", original_error=e)


@register_converter('html_encoded', 'text', 'Convert HTML encoded string to text')
class HtmlToTextConverter(BaseConverter):
    """Convert HTML encoding to text."""
    
    def __init__(self, from_format='html_encoded', to_format='text'):
        super().__init__('html_encoded', 'text', 'Convert HTML encoded string to text')
    
    def validate_input(self, data: Any) -> None:
        super().validate_input(data)
        if not isinstance(data, str):
            raise ValidationError(f"HTML encoded input requires string, got {type(data).__name__}")
    
    def _convert(self, data: str, **options) -> str:
        try:
            return html.unescape(data)
        except Exception as e:
            raise ConversionError(f"Failed to HTML decode: {e}", original_error=e)


# ============================================================================
# HASH CONVERTERS
# ============================================================================

@register_converter('text', 'md5', 'Generate MD5 hash from text')
class TextToMD5Converter(BaseConverter):
    """Generate MD5 hash from text."""
    
    def __init__(self, from_format='text', to_format='md5'):
        super().__init__('text', 'md5', 'Generate MD5 hash from text')
    
    def validate_input(self, data: Any) -> None:
        super().validate_input(data)
        if not isinstance(data, str):
            raise ValidationError(f"Text input required, got {type(data).__name__}")
    
    def _convert(self, data: str, **options) -> str:
        try:
            encoding = options.get('encoding', 'utf-8')
            data_bytes = data.encode(encoding)
            return hashlib.md5(data_bytes).hexdigest()
        except Exception as e:
            raise ConversionError(f"Failed to generate MD5: {e}", original_error=e)


@register_converter('text', 'sha256', 'Generate SHA256 hash from text')
class TextToSHA256Converter(BaseConverter):
    """Generate SHA256 hash from text."""
    
    def __init__(self, from_format='text', to_format='sha256'):
        super().__init__('text', 'sha256', 'Generate SHA256 hash from text')
    
    def validate_input(self, data: Any) -> None:
        super().validate_input(data)
        if not isinstance(data, str):
            raise ValidationError(f"Text input required, got {type(data).__name__}")
    
    def _convert(self, data: str, **options) -> str:
        try:
            encoding = options.get('encoding', 'utf-8')
            data_bytes = data.encode(encoding)
            return hashlib.sha256(data_bytes).hexdigest()
        except Exception as e:
            raise ConversionError(f"Failed to generate SHA256: {e}", original_error=e)


# ============================================================================
# DATA FORMAT CONVERTERS
# ============================================================================

@register_converter('json', 'dict', 'Parse JSON string to Python dictionary')
class JsonToDictConverter(BaseConverter):
    """Parse JSON string to Python dictionary."""
    
    def __init__(self, from_format='json', to_format='dict'):
        super().__init__('json', 'dict', 'Parse JSON string to Python dictionary')
    
    def validate_input(self, data: Any) -> None:
        super().validate_input(data)
        if not isinstance(data, str):
            raise ValidationError(f"JSON input requires string, got {type(data).__name__}")
    
    def _convert(self, data: str, **options) -> dict:
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            raise ConversionError(f"Invalid JSON: {e}", original_error=e)
        except Exception as e:
            raise ConversionError(f"Failed to parse JSON: {e}", original_error=e)


@register_converter('dict', 'json', 'Convert Python dictionary to JSON string')
class DictToJsonConverter(BaseConverter):
    """Convert Python dictionary to JSON string."""
    
    def __init__(self, from_format='dict', to_format='json'):
        super().__init__('dict', 'json', 'Convert Python dictionary to JSON string')
    
    def validate_input(self, data: Any) -> None:
        super().validate_input(data)
        if not isinstance(data, (dict, list)):
            raise ValidationError(f"Dict input requires dict or list, got {type(data).__name__}")
    
    def _convert(self, data: dict, **options) -> str:
        try:
            indent = options.get('indent', 2)
            sort_keys = options.get('sort_keys', False)
            return json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)
        except Exception as e:
            raise ConversionError(f"Failed to serialize to JSON: {e}", original_error=e)


# ============================================================================
# NUMBER BASE CONVERTERS
# ============================================================================

@register_converter('decimal', 'binary', 'Convert decimal number to binary')
class DecimalToBinaryConverter(BaseConverter):
    """Convert decimal number to binary representation."""
    
    def __init__(self, from_format='decimal', to_format='binary'):
        super().__init__('decimal', 'binary', 'Convert decimal number to binary')
    
    def validate_input(self, data: Any) -> None:
        super().validate_input(data)
        try:
            int(data)
        except ValueError:
            raise ValidationError(f"Invalid decimal number: {data}")
    
    def _convert(self, data: Union[int, str], **options) -> str:
        try:
            num = int(data)
            include_prefix = options.get('include_prefix', False)
            
            binary_str = bin(num)
            if include_prefix:
                return binary_str
            else:
                return binary_str[2:] if num >= 0 else binary_str[3:]
        except Exception as e:
            raise ConversionError(f"Failed to convert to binary: {e}", original_error=e)


@register_converter('binary', 'decimal', 'Convert binary to decimal number')
class BinaryToDecimalConverter(BaseConverter):
    """Convert binary representation to decimal number."""
    
    def __init__(self, from_format='binary', to_format='decimal'):
        super().__init__('binary', 'decimal', 'Convert binary to decimal number')
    
    def validate_input(self, data: Any) -> None:
        super().validate_input(data)
        if not isinstance(data, str):
            raise ValidationError(f"Binary input requires string, got {type(data).__name__}")
    
    def _convert(self, data: str, **options) -> int:
        try:
            cleaned = data.strip()
            if cleaned.startswith('0b'):
                cleaned = cleaned[2:]
            
            if not all(c in '01' for c in cleaned):
                raise ValidationError(f"Invalid binary string: {data}")
            
            return int(cleaned, 2)
        except Exception as e:
            raise ConversionError(f"Failed to convert binary: {e}", original_error=e)


@register_converter('decimal', 'hex', 'Convert decimal number to hexadecimal')
class DecimalToHexConverter(BaseConverter):
    """Convert decimal number to hexadecimal representation."""
    
    def __init__(self, from_format='decimal', to_format='hex'):
        super().__init__('decimal', 'hex', 'Convert decimal number to hexadecimal')
    
    def validate_input(self, data: Any) -> None:
        super().validate_input(data)
        try:
            int(data)
        except ValueError:
            raise ValidationError(f"Invalid decimal number: {data}")
    
    def _convert(self, data: Union[int, str], **options) -> str:
        try:
            num = int(data)
            include_prefix = options.get('include_prefix', False)
            uppercase = options.get('uppercase', False)
            
            hex_str = hex(num)
            if num >= 0:
                hex_digits = hex_str[2:]
            else:
                hex_digits = hex_str[3:]
            
            if uppercase:
                hex_digits = hex_digits.upper()
            
            if include_prefix:
                return ('0x' if num >= 0 else '-0x') + hex_digits
            else:
                return ('-' if num < 0 else '') + hex_digits
        except Exception as e:
            raise ConversionError(f"Failed to convert to hex: {e}", original_error=e)