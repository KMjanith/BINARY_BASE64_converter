"""
Conversion Registry System
=========================

This module implements the registry pattern for managing format converters.
It provides automatic discovery, registration, and lookup of converters.

Learning Concepts:
- Registry Pattern: Central management of objects
- Singleton Pattern: Single global registry instance  
- Decorators: Automatic registration
- Graph Theory: Format conversion as a directed graph
- Reflection: Dynamic class discovery and instantiation
"""

from typing import Dict, List, Tuple, Set, Optional, Type, Any
import logging
from collections import defaultdict, deque
import importlib
import inspect

from .base_converter import BaseConverter, ReversibleConverter
from ..utils.exceptions import UnsupportedFormatError, ConversionError

logger = logging.getLogger(__name__)


class ConversionRegistry:
    """
    Central registry for all format converters.
    
    This class manages the registration and discovery of converters, handles
    bidirectional registration, and provides path finding for multi-step conversions.
    
    Key Features:
    - Automatic bidirectional registration for reversible converters
    - Multi-step conversion path finding (e.g., binary -> hex -> base64)
    - Converter discovery and validation
    - Thread-safe registration (future enhancement)
    
    The registry maintains converters as a directed graph where:
    - Nodes = format names (e.g., 'binary', 'base64')
    - Edges = converters (e.g., BinaryToBase64Converter)
    """
    
    def __init__(self):
        """Initialize an empty registry."""
        # Main converter storage: {(from_format, to_format): converter_class}
        self._converters: Dict[Tuple[str, str], Type[BaseConverter]] = {}
        
        # Format graph for path finding: {from_format: {to_format, ...}}
        self._format_graph: Dict[str, Set[str]] = defaultdict(set)
        
        # Reverse lookup: {format: [converters_involving_format]}
        self._format_converters: Dict[str, List[Type[BaseConverter]]] = defaultdict(list)
        
        # Registry metadata
        self._registered_count = 0
        
        logger.info("Initialized conversion registry")
    
    def register_converter(self, converter_class: Type[BaseConverter], 
                          from_format: str = None, to_format: str = None,
                          auto_reverse: bool = True) -> None:
        """
        Register a converter class in the registry.
        
        Args:
            converter_class: The converter class to register
            from_format: Source format (if not specified, tries to get from class metadata)
            to_format: Target format (if not specified, tries to get from class metadata)  
            auto_reverse: Whether to automatically register the reverse for ReversibleConverters
            
        Raises:
            ConversionError: If converter registration fails
            
        Example:
            >>> registry = ConversionRegistry()
            >>> registry.register_converter(BinaryToBase64Converter, 'binary', 'base64')
        """
        # Extract format information from class metadata if not provided
        if from_format is None:
            from_format = getattr(converter_class, '_converter_from_format', None)
        if to_format is None:
            to_format = getattr(converter_class, '_converter_to_format', None)
            
        if not from_format or not to_format:
            raise ConversionError(
                f"Cannot register {converter_class.__name__}: missing format information. "
                f"Provide from_format and to_format parameters or use @converter_info decorator."
            )
        
        # Normalize format names
        from_format = from_format.lower().strip()
        to_format = to_format.lower().strip()
        
        # Check if this conversion is already registered
        conversion_pair = (from_format, to_format)
        if conversion_pair in self._converters:
            existing_class = self._converters[conversion_pair]
            logger.warning(
                f"Overriding existing converter for {from_format} -> {to_format}: "
                f"{existing_class.__name__} -> {converter_class.__name__}"
            )
        
        # Validate converter class
        if not issubclass(converter_class, BaseConverter):
            raise ConversionError(
                f"Converter {converter_class.__name__} must inherit from BaseConverter"
            )
        
        # Register the converter
        self._converters[conversion_pair] = converter_class
        self._format_graph[from_format].add(to_format)
        self._format_converters[from_format].append(converter_class)
        self._format_converters[to_format].append(converter_class)
        
        self._registered_count += 1
        
        logger.info(f"Registered converter: {from_format} -> {to_format} ({converter_class.__name__})")
        
        # Auto-register reverse for reversible converters
        if (auto_reverse and 
            issubclass(converter_class, ReversibleConverter) and
            (to_format, from_format) not in self._converters):
            
            self._converters[(to_format, from_format)] = converter_class
            self._format_graph[to_format].add(from_format)
            self._registered_count += 1
            
            logger.info(f"Auto-registered reverse: {to_format} -> {from_format} ({converter_class.__name__})")
    
    def get_converter(self, from_format: str, to_format: str) -> BaseConverter:
        """
        Get a converter instance for the specified format pair.
        
        Args:
            from_format: Source format name
            to_format: Target format name
            
        Returns:
            Converter instance ready for use
            
        Raises:
            UnsupportedFormatError: If no converter is available for this format pair
            
        Example:
            >>> registry = ConversionRegistry()
            >>> converter = registry.get_converter('binary', 'base64')
            >>> result = converter.convert(b'Hello')
        """
        from_format = from_format.lower().strip()
        to_format = to_format.lower().strip()
        
        # Check for direct converter
        conversion_pair = (from_format, to_format)
        if conversion_pair in self._converters:
            converter_class = self._converters[conversion_pair]
            return converter_class(from_format, to_format)
        
        # TODO: In future versions, implement multi-step conversion path finding
        # For now, only support direct conversions
        available_formats = self.get_supported_formats()
        raise UnsupportedFormatError(from_format, to_format, available_formats)
    
    def convert(self, data: Any, from_format: str, to_format: str, **options) -> Any:
        """
        Convert data directly using the registry.
        
        This is a convenience method that gets the appropriate converter and
        performs the conversion in one step.
        
        Args:
            data: Data to convert
            from_format: Source format name
            to_format: Target format name
            **options: Additional conversion options
            
        Returns:
            Converted data
            
        Example:
            >>> registry = ConversionRegistry()  
            >>> result = registry.convert(b'Hello', 'binary', 'base64')
        """
        converter = self.get_converter(from_format, to_format)
        return converter.convert(data, **options)
    
    def is_supported(self, from_format: str, to_format: str) -> bool:
        """
        Check if a conversion is supported.
        
        Args:
            from_format: Source format name
            to_format: Target format name
            
        Returns:
            True if conversion is supported, False otherwise
        """
        from_format = from_format.lower().strip()
        to_format = to_format.lower().strip()
        return (from_format, to_format) in self._converters
    
    def get_supported_formats(self) -> List[str]:
        """
        Get a list of all supported format names.
        
        Returns:
            Sorted list of format names
        """
        formats = set()
        for from_fmt, to_fmt in self._converters.keys():
            formats.add(from_fmt)
            formats.add(to_fmt)
        return sorted(formats)
    
    def list_conversions(self) -> List[Dict[str, str]]:
        """
        List all available conversions.
        
        Returns:
            List of dictionaries with conversion information
            
        Example:
            >>> registry.list_conversions()
            [
                {
                    'from': 'binary', 
                    'to': 'base64', 
                    'description': 'Binary to Base64 encoding',
                    'converter': 'BinaryToBase64Converter'
                },
                ...
            ]
        """
        conversions = []
        for (from_fmt, to_fmt), converter_class in self._converters.items():
            # Create a temporary instance to get description
            temp_instance = converter_class(from_fmt, to_fmt)
            conversions.append({
                'from': from_fmt,
                'to': to_fmt,
                'description': temp_instance.description,
                'converter': converter_class.__name__,
                'reversible': issubclass(converter_class, ReversibleConverter)
            })
        
        # Sort by from_format, then to_format
        conversions.sort(key=lambda x: (x['from'], x['to']))
        return conversions
    
    def get_conversions_for_format(self, format_name: str) -> Dict[str, List[str]]:
        """
        Get all possible conversions involving a specific format.
        
        Args:
            format_name: Format to search for
            
        Returns:
            Dictionary with 'from' and 'to' lists showing possible conversions
            
        Example:
            >>> registry.get_conversions_for_format('binary')
            {'from': ['base64', 'hex'], 'to': ['base64', 'hex']}
        """
        format_name = format_name.lower().strip()
        from_conversions = []  # Formats that can convert TO this format
        to_conversions = []    # Formats that this format can convert TO
        
        for (from_fmt, to_fmt) in self._converters.keys():
            if from_fmt == format_name:
                to_conversions.append(to_fmt)
            if to_fmt == format_name:
                from_conversions.append(from_fmt)
        
        return {
            'from': sorted(set(from_conversions)),
            'to': sorted(set(to_conversions))
        }
    
    def clear(self) -> None:
        """Clear all registered converters."""
        self._converters.clear()
        self._format_graph.clear()
        self._format_converters.clear()
        self._registered_count = 0
        logger.info("Cleared all converters from registry")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get registry statistics.
        
        Returns:
            Dictionary with registry statistics
        """
        return {
            'total_converters': len(self._converters),
            'total_formats': len(self.get_supported_formats()),
            'registered_count': self._registered_count,
            'converter_pairs': len(self._converters)
        }
    
    def __len__(self) -> int:
        """Return the number of registered converter pairs."""
        return len(self._converters)
    
    def __contains__(self, conversion_pair: Tuple[str, str]) -> bool:
        """Check if a conversion pair is registered."""
        from_fmt, to_fmt = conversion_pair
        return self.is_supported(from_fmt, to_fmt)
    
    def __str__(self) -> str:
        """String representation of the registry."""
        stats = self.get_stats()
        return (f"ConversionRegistry("
                f"converters={stats['total_converters']}, "
                f"formats={stats['total_formats']})")


# Global registry instance
_global_registry = ConversionRegistry()


def get_global_registry() -> ConversionRegistry:
    """
    Get the global registry instance.
    
    Returns:
        The global ConversionRegistry instance
    """
    return _global_registry


def register_converter(from_format: str = None, to_format: str = None, 
                      description: str = "", reversible: bool = False):
    """
    Decorator for automatic converter registration.
    
    This decorator automatically registers converter classes with the global registry
    when they are defined.
    
    Args:
        from_format: Source format name
        to_format: Target format name
        description: Converter description
        reversible: Whether the converter is bidirectional
        
    Example:
        @register_converter('binary', 'base64', 'Binary to Base64 encoding', reversible=True)
        class BinaryBase64Converter(ReversibleConverter):
            # implementation here
    """
    def decorator(converter_class: Type[BaseConverter]):
        # Add metadata to the class
        converter_class._converter_from_format = from_format
        converter_class._converter_to_format = to_format
        converter_class._converter_description = description
        converter_class._converter_reversible = reversible
        
        # Register with global registry
        try:
            _global_registry.register_converter(
                converter_class, 
                from_format, 
                to_format, 
                auto_reverse=reversible
            )
        except Exception as e:
            logger.error(f"Failed to register converter {converter_class.__name__}: {e}")
        
        return converter_class
    
    return decorator


# Convenience functions using the global registry
def convert(data: Any, from_format: str, to_format: str, **options) -> Any:
    """Convert data using the global registry."""
    return _global_registry.convert(data, from_format, to_format, **options)


def is_supported(from_format: str, to_format: str) -> bool:
    """Check if conversion is supported in the global registry."""
    return _global_registry.is_supported(from_format, to_format)


def list_conversions() -> List[Dict[str, str]]:
    """List all conversions in the global registry."""
    return _global_registry.list_conversions()