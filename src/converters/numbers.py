"""
Number Base Converters
=====================

This module implements conversions between different number bases and formats.
These converters handle common number system conversions used in:
- Programming (hex, octal, binary)
- Mathematics education
- Computer science applications
- Data representation

Learning Concepts:
- Number base conversion algorithms
- Python's built-in number format functions
- Integer validation and parsing
- Roman numeral algorithms
"""

from typing import Union, Any
import logging

from .base_converter import ReversibleConverter, BaseConverter
from .registry import register_converter
from ..utils.exceptions import ConversionError, ValidationError

logger = logging.getLogger(__name__)


@register_converter('decimal', 'binary_num', 'Convert decimal number to binary representation', reversible=True)
class DecimalBinaryConverter(ReversibleConverter):
    """
    Convert between decimal numbers and binary representation.
    
    Examples:
    - 42 -> "101010"
    - "1111" -> 15
    """
    
    def __init__(self, from_format: str, to_format: str):
        super().__init__('decimal', 'binary_num', 'Convert decimal to/from binary representation')
    
    def validate_input(self, data: Any) -> None:
        """Validate input data."""
        super().validate_input(data)
        
        if self.from_format == 'decimal':
            if not isinstance(data, (int, str)):
                raise ValidationError(f"Decimal input requires int or string, got {type(data).__name__}")
            try:
                int(data)
            except ValueError:
                raise ValidationError(f"Invalid decimal number: {data}")
        elif self.from_format == 'binary_num':
            if not isinstance(data, str):
                raise ValidationError(f"Binary input requires string, got {type(data).__name__}")
    
    def _convert_a_to_b(self, data: Union[int, str], **options) -> str:
        """Convert decimal to binary."""
        try:
            # Options
            include_prefix = options.get('include_prefix', False)  # Whether to include '0b'
            min_width = options.get('min_width', 0)  # Minimum width with zero padding
            
            num = int(data)
            if num < 0:
                # Handle negative numbers
                binary_str = bin(num)  # This gives '-0b...'
                if include_prefix:
                    return binary_str
                else:
                    return binary_str.replace('-0b', '-')
            else:
                binary_str = bin(num)[2:]  # Remove '0b' prefix
                
                # Apply zero padding if requested
                if min_width > 0:
                    binary_str = binary_str.zfill(min_width)
                
                if include_prefix:
                    return '0b' + binary_str
                else:
                    return binary_str
                    
        except ValueError as e:
            raise ConversionError(f"Invalid decimal number: {e}", original_error=e)
        except Exception as e:
            raise ConversionError(f"Failed to convert decimal to binary: {e}", original_error=e)
    
    def _convert_b_to_a(self, data: str, **options) -> int:
        """Convert binary to decimal."""
        try:
            # Clean the binary string
            cleaned = data.strip()
            
            # Handle negative numbers
            negative = False
            if cleaned.startswith('-'):
                negative = True
                cleaned = cleaned[1:]
            
            # Remove common prefixes
            if cleaned.startswith('0b'):
                cleaned = cleaned[2:]
            
            # Validate binary string
            if not all(c in '01' for c in cleaned):
                raise ValidationError(f"Invalid binary string: {data}")
            
            result = int(cleaned, 2)
            return -result if negative else result
            
        except ValueError as e:
            raise ConversionError(f"Invalid binary string: {e}", original_error=e)
        except Exception as e:
            raise ConversionError(f"Failed to convert binary to decimal: {e}", original_error=e)


@register_converter('decimal', 'hex_num', 'Convert decimal number to hexadecimal', reversible=True)
class DecimalHexConverter(ReversibleConverter):
    """Convert between decimal numbers and hexadecimal representation."""
    
    def __init__(self, from_format: str, to_format: str):
        super().__init__('decimal', 'hex_num', 'Convert decimal to/from hexadecimal')
    
    def _convert_a_to_b(self, data: Union[int, str], **options) -> str:
        """Convert decimal to hexadecimal."""
        try:
            # Options
            include_prefix = options.get('include_prefix', False)  # '0x'
            uppercase = options.get('uppercase', False)
            min_width = options.get('min_width', 0)
            
            num = int(data)
            hex_str = hex(num)
            
            if num >= 0:
                hex_digits = hex_str[2:]  # Remove '0x'
            else:
                hex_digits = hex_str[3:]  # Remove '-0x', we'll handle sign separately
            
            if uppercase:
                hex_digits = hex_digits.upper()
            
            if min_width > 0:
                hex_digits = hex_digits.zfill(min_width)
            
            # Reconstruct with options
            result = hex_digits
            if include_prefix:
                result = '0x' + result
            if num < 0:
                result = '-' + result
                
            return result
            
        except ValueError as e:
            raise ConversionError(f"Invalid decimal number: {e}", original_error=e)
        except Exception as e:
            raise ConversionError(f"Failed to convert decimal to hex: {e}", original_error=e)
    
    def _convert_b_to_a(self, data: str, **options) -> int:
        """Convert hexadecimal to decimal."""
        try:
            # Clean the hex string
            cleaned = data.strip()
            
            # Handle negative numbers
            negative = False
            if cleaned.startswith('-'):
                negative = True
                cleaned = cleaned[1:]
            
            # Remove common prefixes
            if cleaned.lower().startswith('0x'):
                cleaned = cleaned[2:]
            
            result = int(cleaned, 16)
            return -result if negative else result
            
        except ValueError as e:
            raise ConversionError(f"Invalid hexadecimal string: {e}", original_error=e)
        except Exception as e:
            raise ConversionError(f"Failed to convert hex to decimal: {e}", original_error=e)


@register_converter('decimal', 'octal', 'Convert decimal number to octal', reversible=True)
class DecimalOctalConverter(ReversibleConverter):
    """Convert between decimal numbers and octal representation."""
    
    def __init__(self, from_format: str, to_format: str):
        super().__init__('decimal', 'octal', 'Convert decimal to/from octal')
    
    def _convert_a_to_b(self, data: Union[int, str], **options) -> str:
        """Convert decimal to octal."""
        try:
            include_prefix = options.get('include_prefix', False)  # '0o'
            min_width = options.get('min_width', 0)
            
            num = int(data)
            octal_str = oct(num)
            
            if num >= 0:
                octal_digits = octal_str[2:]  # Remove '0o'
            else:
                octal_digits = octal_str[3:]  # Remove '-0o'
            
            if min_width > 0:
                octal_digits = octal_digits.zfill(min_width)
            
            result = octal_digits
            if include_prefix:
                result = '0o' + result
            if num < 0:
                result = '-' + result
                
            return result
            
        except ValueError as e:
            raise ConversionError(f"Invalid decimal number: {e}", original_error=e)
        except Exception as e:
            raise ConversionError(f"Failed to convert decimal to octal: {e}", original_error=e)
    
    def _convert_b_to_a(self, data: str, **options) -> int:
        """Convert octal to decimal."""
        try:
            cleaned = data.strip()
            
            negative = False
            if cleaned.startswith('-'):
                negative = True
                cleaned = cleaned[1:]
            
            if cleaned.lower().startswith('0o'):
                cleaned = cleaned[2:]
            
            result = int(cleaned, 8)
            return -result if negative else result
            
        except ValueError as e:
            raise ConversionError(f"Invalid octal string: {e}", original_error=e)
        except Exception as e:
            raise ConversionError(f"Failed to convert octal to decimal: {e}", original_error=e)


@register_converter('decimal', 'roman', 'Convert decimal to Roman numerals', reversible=True)
class DecimalRomanConverter(ReversibleConverter):
    """
    Convert between decimal numbers and Roman numerals.
    
    Supports numbers from 1 to 3999 (standard Roman numeral range).
    """
    
    def __init__(self, from_format: str, to_format: str):
        super().__init__('decimal', 'roman', 'Convert decimal to/from Roman numerals')
    
    def _convert_a_to_b(self, data: Union[int, str], **options) -> str:
        """Convert decimal to Roman numerals."""
        try:
            num = int(data)
            
            if num <= 0 or num > 3999:
                raise ValidationError(f"Roman numerals only support numbers 1-3999, got {num}")
            
            # Roman numeral conversion table
            values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
            symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
            
            result = ""
            for i, value in enumerate(values):
                count = num // value
                if count:
                    result += symbols[i] * count
                    num -= value * count
            
            return result
            
        except ValueError as e:
            raise ConversionError(f"Invalid decimal number: {e}", original_error=e)
        except Exception as e:
            raise ConversionError(f"Failed to convert decimal to Roman: {e}", original_error=e)
    
    def _convert_b_to_a(self, data: str, **options) -> int:
        """Convert Roman numerals to decimal."""
        try:
            roman = data.upper().strip()
            
            # Roman numeral values
            roman_values = {
                'I': 1, 'V': 5, 'X': 10, 'L': 50,
                'C': 100, 'D': 500, 'M': 1000
            }
            
            # Validate Roman numeral string
            valid_chars = set(roman_values.keys())
            if not all(c in valid_chars for c in roman):
                raise ValidationError(f"Invalid Roman numeral characters in: {data}")
            
            total = 0
            prev_value = 0
            
            # Process from right to left
            for char in reversed(roman):
                value = roman_values[char]
                
                if value < prev_value:
                    # Subtractive notation (like IV, IX, XL, etc.)
                    total -= value
                else:
                    total += value
                
                prev_value = value
            
            return total
            
        except KeyError as e:
            raise ConversionError(f"Invalid Roman numeral character: {e}", original_error=e)
        except Exception as e:
            raise ConversionError(f"Failed to convert Roman to decimal: {e}", original_error=e)


# Cross-base converters (binary to hex, etc.)
@register_converter('binary_num', 'hex_num', 'Convert binary to hexadecimal via decimal', reversible=True)
class BinaryHexConverter(ReversibleConverter):
    """Convert between binary and hexadecimal number representations."""
    
    def __init__(self, from_format: str, to_format: str):
        super().__init__('binary_num', 'hex_num', 'Convert binary to/from hexadecimal')
    
    def _convert_a_to_b(self, data: str, **options) -> str:
        """Convert binary to hex via decimal."""
        try:
            # First convert binary to decimal
            decimal_converter = DecimalBinaryConverter('binary_num', 'decimal')
            decimal_value = decimal_converter._convert_b_to_a(data)
            
            # Then convert decimal to hex
            hex_converter = DecimalHexConverter('decimal', 'hex_num')
            return hex_converter._convert_a_to_b(decimal_value, **options)
            
        except Exception as e:
            raise ConversionError(f"Failed to convert binary to hex: {e}", original_error=e)
    
    def _convert_b_to_a(self, data: str, **options) -> str:
        """Convert hex to binary via decimal."""
        try:
            # First convert hex to decimal
            hex_converter = DecimalHexConverter('hex_num', 'decimal')
            decimal_value = hex_converter._convert_b_to_a(data)
            
            # Then convert decimal to binary
            binary_converter = DecimalBinaryConverter('decimal', 'binary_num')
            return binary_converter._convert_a_to_b(decimal_value, **options)
            
        except Exception as e:
            raise ConversionError(f"Failed to convert hex to binary: {e}", original_error=e)