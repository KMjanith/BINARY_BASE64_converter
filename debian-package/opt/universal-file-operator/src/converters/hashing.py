"""
Hash and Checksum Converters
============================

This module implements hash functions and checksum calculations.
These are one-way converters (data -> hash) that are commonly used for:
- Data integrity verification
- Password hashing (educational purposes only)
- File checksums
- Digital fingerprints

Learning Concepts:
- Python's hashlib library
- One-way vs reversible conversions
- Different hash algorithms and their uses
- Hexadecimal representation of hashes
"""

import hashlib
import zlib
from typing import Union, Any
import logging

from .base_converter import BaseConverter
from .registry import register_converter
from ..utils.exceptions import ConversionError, ValidationError

logger = logging.getLogger(__name__)


class HashConverter(BaseConverter):
    """
    Base class for hash converters.
    
    Hash functions are one-way conversions that produce a fixed-size output
    regardless of input size. They are NOT reversible.
    """
    
    def __init__(self, from_format: str, hash_algorithm: str):
        to_format = f"{hash_algorithm.lower()}_hash"
        description = f"Generate {hash_algorithm.upper()} hash from {from_format}"
        super().__init__(from_format, to_format, description)
        self.hash_algorithm = hash_algorithm.lower()
        self.supports_options = True
    
    def validate_input(self, data: Any) -> None:
        """Validate input data for hashing."""
        super().validate_input(data)
        
        if self.from_format == 'text' and not isinstance(data, str):
            raise ValidationError(f"Text input required, got {type(data).__name__}")
        elif self.from_format == 'binary' and not isinstance(data, bytes):
            raise ValidationError(f"Binary input required, got {type(data).__name__}")


@register_converter('text', 'md5_hash', 'Generate MD5 hash from text')
class TextMD5Converter(HashConverter):
    """
    Generate MD5 hash from text input.
    
    MD5 is commonly used for:
    - File integrity checks
    - Simple checksums
    - Legacy systems (NOT secure for passwords!)
    """
    
    def __init__(self, from_format='text', to_format='md5_hash'):
        super().__init__('text', 'md5')
    
    def _convert(self, data: str, **options) -> str:
        """Convert text to MD5 hash."""
        try:
            encoding = options.get('encoding', 'utf-8')
            output_format = options.get('format', 'hex')  # 'hex' or 'base64'
            
            # Convert text to bytes
            data_bytes = data.encode(encoding)
            
            # Generate hash
            hash_obj = hashlib.md5(data_bytes)
            
            if output_format == 'base64':
                import base64
                return base64.b64encode(hash_obj.digest()).decode('ascii')
            else:
                return hash_obj.hexdigest()
                
        except Exception as e:
            raise ConversionError(f"Failed to generate MD5 hash: {e}", original_error=e)


@register_converter('text', 'sha1_hash', 'Generate SHA1 hash from text')
class TextSHA1Converter(HashConverter):
    """
    Generate SHA1 hash from text input.
    
    SHA1 is commonly used for:
    - Git commit hashes
    - File integrity
    - Digital signatures (legacy)
    """
    
    def __init__(self, from_format='text', to_format='sha1_hash'):
        super().__init__('text', 'sha1')
    
    def _convert(self, data: str, **options) -> str:
        """Convert text to SHA1 hash."""
        try:
            encoding = options.get('encoding', 'utf-8')
            output_format = options.get('format', 'hex')
            
            data_bytes = data.encode(encoding)
            hash_obj = hashlib.sha1(data_bytes)
            
            if output_format == 'base64':
                import base64
                return base64.b64encode(hash_obj.digest()).decode('ascii')
            else:
                return hash_obj.hexdigest()
                
        except Exception as e:
            raise ConversionError(f"Failed to generate SHA1 hash: {e}", original_error=e)


@register_converter('text', 'sha256_hash', 'Generate SHA256 hash from text')
class TextSHA256Converter(HashConverter):
    """
    Generate SHA256 hash from text input.
    
    SHA256 is commonly used for:
    - Bitcoin and cryptocurrency
    - Modern security applications
    - File integrity verification
    - Digital certificates
    """
    
    def __init__(self, from_format='text', to_format='sha256_hash'):
        super().__init__('text', 'sha256')
    
    def _convert(self, data: str, **options) -> str:
        """Convert text to SHA256 hash."""
        try:
            encoding = options.get('encoding', 'utf-8')
            output_format = options.get('format', 'hex')
            
            data_bytes = data.encode(encoding)
            hash_obj = hashlib.sha256(data_bytes)
            
            if output_format == 'base64':
                import base64
                return base64.b64encode(hash_obj.digest()).decode('ascii')
            else:
                return hash_obj.hexdigest()
                
        except Exception as e:
            raise ConversionError(f"Failed to generate SHA256 hash: {e}", original_error=e)


@register_converter('text', 'sha512_hash', 'Generate SHA512 hash from text')
class TextSHA512Converter(HashConverter):
    """Generate SHA512 hash from text input."""
    
    def __init__(self, from_format='text', to_format='sha512_hash'):
        super().__init__('text', 'sha512')
    
    def _convert(self, data: str, **options) -> str:
        """Convert text to SHA512 hash."""
        try:
            encoding = options.get('encoding', 'utf-8')
            output_format = options.get('format', 'hex')
            
            data_bytes = data.encode(encoding)
            hash_obj = hashlib.sha512(data_bytes)
            
            if output_format == 'base64':
                import base64
                return base64.b64encode(hash_obj.digest()).decode('ascii')
            else:
                return hash_obj.hexdigest()
                
        except Exception as e:
            raise ConversionError(f"Failed to generate SHA512 hash: {e}", original_error=e)


@register_converter('text', 'crc32', 'Generate CRC32 checksum from text')
class TextCRC32Converter(BaseConverter):
    """
    Generate CRC32 checksum from text input.
    
    CRC32 is commonly used for:
    - ZIP file integrity
    - Network error detection
    - Simple file checksums
    """
    
    def __init__(self, from_format='text', to_format='crc32'):
        super().__init__('text', 'crc32', 'Generate CRC32 checksum from text')
    
    def validate_input(self, data: Any) -> None:
        """Validate input data."""
        super().validate_input(data)
        if not isinstance(data, str):
            raise ValidationError(f"Text input required, got {type(data).__name__}")
    
    def _convert(self, data: str, **options) -> str:
        """Convert text to CRC32 checksum."""
        try:
            encoding = options.get('encoding', 'utf-8')
            output_format = options.get('format', 'hex')  # 'hex', 'int', 'unsigned'
            
            data_bytes = data.encode(encoding)
            crc = zlib.crc32(data_bytes)
            
            if output_format == 'int':
                return str(crc)
            elif output_format == 'unsigned':
                # Convert to unsigned 32-bit integer
                return str(crc & 0xffffffff)
            else:  # hex format
                return format(crc & 0xffffffff, '08x')
                
        except Exception as e:
            raise ConversionError(f"Failed to generate CRC32: {e}", original_error=e)


# Binary hash converters (same algorithms, different input type)
@register_converter('binary', 'md5_hash', 'Generate MD5 hash from binary data')
class BinaryMD5Converter(HashConverter):
    """Generate MD5 hash from binary data."""
    
    def __init__(self, from_format='binary', to_format='md5_hash'):
        super().__init__('binary', 'md5')
    
    def _convert(self, data: bytes, **options) -> str:
        """Convert binary to MD5 hash."""
        try:
            output_format = options.get('format', 'hex')
            hash_obj = hashlib.md5(data)
            
            if output_format == 'base64':
                import base64
                return base64.b64encode(hash_obj.digest()).decode('ascii')
            else:
                return hash_obj.hexdigest()
                
        except Exception as e:
            raise ConversionError(f"Failed to generate MD5 hash: {e}", original_error=e)


@register_converter('binary', 'sha256_hash', 'Generate SHA256 hash from binary data')
class BinarySHA256Converter(HashConverter):
    """Generate SHA256 hash from binary data."""
    
    def __init__(self, from_format='binary', to_format='sha256_hash'):
        super().__init__('binary', 'sha256')
    
    def _convert(self, data: bytes, **options) -> str:
        """Convert binary to SHA256 hash."""
        try:
            output_format = options.get('format', 'hex')
            hash_obj = hashlib.sha256(data)
            
            if output_format == 'base64':
                import base64
                return base64.b64encode(hash_obj.digest()).decode('ascii')
            else:
                return hash_obj.hexdigest()
                
        except Exception as e:
            raise ConversionError(f"Failed to generate SHA256 hash: {e}", original_error=e)