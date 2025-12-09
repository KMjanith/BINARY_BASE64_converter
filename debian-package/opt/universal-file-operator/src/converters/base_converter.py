"""
Base Converter Class
===================

This module defines the abstract base class that all converters must inherit from.
It establishes a consistent interface and provides common functionality.

Learning Concepts:
- Abstract Base Classes (ABC): Using Python's abc module to define interfaces
- Type Hints: Modern Python type annotations
- Design Patterns: Template method pattern
- Documentation: Comprehensive docstrings with examples
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import logging
from ..utils.exceptions import ConversionError, ValidationError, handle_conversion_error

# Set up logging for the converter
logger = logging.getLogger(__name__)


class BaseConverter(ABC):
    """
    Abstract base class for all format converters.
    
    This class defines the interface that all converters must implement and provides
    common functionality like validation, logging, and error handling.
    
    Key Design Principles:
    - Single Responsibility: Each converter handles one format pair
    - Open/Closed: Easy to extend with new converters, closed for modification
    - Interface Segregation: Small, focused interface
    
    Attributes:
        from_format (str): Source format name (e.g., 'binary', 'base64')
        to_format (str): Target format name
        description (str): Human-readable description of the converter
        supports_options (bool): Whether this converter accepts conversion options
    """
    
    def __init__(self, from_format: str, to_format: str, description: str = ""):
        """
        Initialize the base converter.
        
        Args:
            from_format: Name of the source format
            to_format: Name of the target format  
            description: Human-readable description of what this converter does
        """
        self.from_format = from_format.lower()
        self.to_format = to_format.lower()
        self.description = description or f"Converts {from_format} to {to_format}"
        self.supports_options = True  # Can be overridden by subclasses
        
        logger.debug(f"Initialized converter: {self.from_format} -> {self.to_format}")
    
    @abstractmethod
    def _convert(self, data: Any, **options) -> Any:
        """
        Abstract method that performs the actual conversion.
        
        This method must be implemented by all subclasses. It should contain
        the core conversion logic without validation or error handling.
        
        Args:
            data: The input data to convert
            **options: Additional conversion options (quality, compression, etc.)
            
        Returns:
            The converted data
            
        Raises:
            ConversionError: If conversion fails
        """
        pass
    
    def validate_input(self, data: Any) -> None:
        """
        Validate input data before conversion.
        
        Override this method in subclasses to add specific validation logic.
        The base implementation does basic null/empty checks.
        
        Args:
            data: Input data to validate
            
        Raises:
            ValidationError: If validation fails
        """
        if data is None:
            raise ValidationError("Input data cannot be None", expected_format=self.from_format)
            
        # For binary/string data, check if empty
        if isinstance(data, (str, bytes)) and len(data) == 0:
            logger.warning("Input data is empty")
    
    def validate_options(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and normalize conversion options.
        
        Override this method in subclasses to add specific option validation.
        
        Args:
            options: Dictionary of conversion options
            
        Returns:
            Validated and normalized options dictionary
            
        Raises:
            ValidationError: If options are invalid
        """
        if not self.supports_options and options:
            logger.warning(f"Converter {self.from_format}->{self.to_format} does not support options, ignoring: {list(options.keys())}")
            return {}
        
        return options.copy()  # Return a copy to avoid modifying the original
    
    @handle_conversion_error
    def convert(self, data: Any, **options) -> Any:
        """
        Public method to convert data from source to target format.
        
        This is the main entry point for conversions. It handles validation,
        error handling, and logging while delegating the actual conversion
        to the abstract _convert method.
        
        Args:
            data: Input data in the source format
            **options: Additional conversion options
            
        Returns:
            Converted data in the target format
            
        Raises:
            ValidationError: If input data or options are invalid
            ConversionError: If conversion fails
            
        Example:
            >>> converter = BinaryToBase64Converter()
            >>> result = converter.convert(b'Hello World')
            >>> print(result)  # 'SGVsbG8gV29ybGQ='
        """
        logger.info(f"Starting conversion: {self.from_format} -> {self.to_format}")
        
        # Validate inputs
        self.validate_input(data)
        validated_options = self.validate_options(options)
        
        # Log conversion details
        data_info = f"{type(data).__name__}"
        if isinstance(data, (str, bytes)):
            data_info += f" (length: {len(data)})"
        logger.debug(f"Converting {data_info} with options: {validated_options}")
        
        # Perform the actual conversion
        try:
            result = self._convert(data, **validated_options)
            logger.info(f"Conversion completed successfully: {self.from_format} -> {self.to_format}")
            return result
            
        except Exception as e:
            logger.error(f"Conversion failed: {self.from_format} -> {self.to_format}: {str(e)}")
            if isinstance(e, ConversionError):
                raise
            else:
                raise ConversionError(
                    f"Conversion failed: {str(e)}", 
                    from_format=self.from_format,
                    to_format=self.to_format,
                    original_error=e
                )
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about this converter.
        
        Returns:
            Dictionary containing converter metadata
        """
        return {
            'from_format': self.from_format,
            'to_format': self.to_format,
            'description': self.description,
            'supports_options': self.supports_options,
            'class_name': self.__class__.__name__
        }
    
    def __str__(self) -> str:
        """String representation of the converter."""
        return f"{self.__class__.__name__}({self.from_format} -> {self.to_format})"
    
    def __repr__(self) -> str:
        """Developer representation of the converter."""
        return f"{self.__class__.__name__}(from_format='{self.from_format}', to_format='{self.to_format}')"


class ReversibleConverter(BaseConverter):
    """
    Base class for converters that support bidirectional conversion.
    
    Many format conversions are reversible (like binary <-> base64).
    This class provides a framework for creating both directions from a single
    implementation.
    
    Learning Concepts:
    - Composition over Inheritance: Building complex behavior from simple parts
    - Factory Pattern: Creating related objects
    - Bidirectional Operations: Implementing inverse operations
    """
    
    def __init__(self, format_a: str, format_b: str, description: str = ""):
        """
        Initialize a reversible converter.
        
        Args:
            format_a: First format name
            format_b: Second format name  
            description: Description of the conversion
        """
        super().__init__(format_a, format_b, description)
        self.format_a = format_a.lower()
        self.format_b = format_b.lower()
    
    @abstractmethod
    def _convert_a_to_b(self, data: Any, **options) -> Any:
        """Convert from format A to format B."""
        pass
    
    @abstractmethod  
    def _convert_b_to_a(self, data: Any, **options) -> Any:
        """Convert from format B to format A."""
        pass
    
    def _convert(self, data: Any, **options) -> Any:
        """
        Route the conversion to the appropriate method based on format direction.
        """
        if self.from_format == self.format_a and self.to_format == self.format_b:
            return self._convert_a_to_b(data, **options)
        elif self.from_format == self.format_b and self.to_format == self.format_a:
            return self._convert_b_to_a(data, **options)
        else:
            raise ConversionError(
                f"Invalid format combination: {self.from_format} -> {self.to_format}",
                from_format=self.from_format,
                to_format=self.to_format
            )
    
    def create_reverse(self) -> 'BaseConverter':
        """
        Create the reverse converter instance.
        
        Returns:
            New converter instance for the reverse direction
        """
        # Create a new instance with reversed formats
        reverse_converter = self.__class__(self.format_b, self.format_a, self.description)
        return reverse_converter


# Utility functions for converter registration
def converter_info(from_format: str, to_format: str, description: str = "", 
                  reversible: bool = False):
    """
    Decorator to add metadata to converter classes.
    
    This decorator is used to mark converter classes with their format information,
    making it easier for the registry to auto-discover and register them.
    
    Args:
        from_format: Source format name
        to_format: Target format name
        description: Human-readable description
        reversible: Whether this converter is bidirectional
        
    Example:
        @converter_info('binary', 'base64', 'Binary to Base64 encoding', reversible=True)
        class BinaryBase64Converter(ReversibleConverter):
            # implementation here
    """
    def decorator(cls):
        cls._converter_from_format = from_format
        cls._converter_to_format = to_format  
        cls._converter_description = description
        cls._converter_reversible = reversible
        return cls
    return decorator