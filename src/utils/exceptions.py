"""
Custom Exceptions for Universal File Operator
===============================================

This module defines custom exception classes that provide specific error handling
for different types of conversion failures.

Learning Concepts:
- Exception Hierarchy: Creating custom exceptions that inherit from built-in exceptions
- Error Context: Providing detailed error information for debugging
- Exception Chaining: Preserving original error information
"""

class ConversionError(Exception):
    """
    Base exception for all conversion-related errors.
    
    This is the parent class for all conversion exceptions, following Python's
    exception hierarchy best practices.
    
    Attributes:
        message (str): Human-readable error message
        from_format (str): Source format that caused the error
        to_format (str): Target format that caused the error
        original_error (Exception): Original exception that caused this error
    """
    
    def __init__(self, message: str, from_format: str = None, to_format: str = None, original_error: Exception = None):
        """
        Initialize a ConversionError.
        
        Args:
            message: Human-readable error description
            from_format: Source format name (optional)
            to_format: Target format name (optional)  
            original_error: The original exception that caused this error (optional)
        """
        self.message = message
        self.from_format = from_format
        self.to_format = to_format
        self.original_error = original_error
        
        # Create a detailed error message
        full_message = message
        if from_format and to_format:
            full_message = f"Conversion from '{from_format}' to '{to_format}': {message}"
        elif from_format:
            full_message = f"Format '{from_format}': {message}"
        elif to_format:
            full_message = f"Format '{to_format}': {message}"
            
        super().__init__(full_message)
    
    def __str__(self):
        """Return a string representation of the error."""
        return self.args[0] if self.args else self.message


class UnsupportedFormatError(ConversionError):
    """
    Raised when trying to convert between unsupported format pairs.
    
    This exception is raised when:
    - A requested format is not registered in the system
    - A conversion pair is not available (e.g., trying to convert PDF to MP3)
    """
    
    def __init__(self, from_format: str, to_format: str, available_formats: list = None):
        """
        Initialize an UnsupportedFormatError.
        
        Args:
            from_format: The unsupported source format
            to_format: The unsupported target format
            available_formats: List of supported formats (optional)
        """
        message = f"Conversion from '{from_format}' to '{to_format}' is not supported"
        if available_formats:
            message += f". Available formats: {', '.join(available_formats)}"
        
        super().__init__(message, from_format, to_format)
        self.available_formats = available_formats or []


class ValidationError(ConversionError):
    """
    Raised when input data fails validation checks.
    
    This exception is raised when:
    - Input data is in the wrong format
    - Data is corrupted or incomplete
    - Required parameters are missing
    """
    
    def __init__(self, message: str, data_type: str = None, expected_format: str = None):
        """
        Initialize a ValidationError.
        
        Args:
            message: Description of the validation failure
            data_type: Type of data that failed validation (optional)
            expected_format: Expected format of the data (optional)
        """
        full_message = message
        if data_type and expected_format:
            full_message = f"Validation failed for {data_type} (expected {expected_format}): {message}"
        elif data_type:
            full_message = f"Validation failed for {data_type}: {message}"
        elif expected_format:
            full_message = f"Validation failed (expected {expected_format}): {message}"
            
        super().__init__(full_message)
        self.data_type = data_type
        self.expected_format = expected_format


class ConfigurationError(ConversionError):
    """
    Raised when there are configuration-related errors.
    
    This exception is raised when:
    - Configuration files are missing or invalid
    - Required settings are not provided
    - Configuration values are out of range
    """
    
    def __init__(self, message: str, config_key: str = None, config_file: str = None):
        """
        Initialize a ConfigurationError.
        
        Args:
            message: Description of the configuration error
            config_key: The configuration key that caused the error (optional)
            config_file: The configuration file with the error (optional)
        """
        full_message = message
        if config_key and config_file:
            full_message = f"Configuration error in '{config_file}' at key '{config_key}': {message}"
        elif config_key:
            full_message = f"Configuration error at key '{config_key}': {message}"
        elif config_file:
            full_message = f"Configuration error in '{config_file}': {message}"
            
        super().__init__(full_message)
        self.config_key = config_key
        self.config_file = config_file


class ProcessingError(ConversionError):
    """
    Raised when errors occur during the actual conversion process.
    
    This exception is raised when:
    - File I/O operations fail
    - External tools or libraries fail
    - Memory or resource constraints are hit
    """
    
    def __init__(self, message: str, stage: str = None, file_path: str = None):
        """
        Initialize a ProcessingError.
        
        Args:
            message: Description of the processing error
            stage: The processing stage where the error occurred (optional)
            file_path: The file being processed when the error occurred (optional)
        """
        full_message = message
        if stage and file_path:
            full_message = f"Processing error in stage '{stage}' for file '{file_path}': {message}"
        elif stage:
            full_message = f"Processing error in stage '{stage}': {message}"
        elif file_path:
            full_message = f"Processing error for file '{file_path}': {message}"
            
        super().__init__(full_message)
        self.stage = stage
        self.file_path = file_path


# Convenience function for error handling
def handle_conversion_error(func):
    """
    Decorator to handle and re-raise conversion errors with context.
    
    This decorator catches common exceptions and converts them to our custom
    ConversionError types with additional context information.
    
    Usage:
        @handle_conversion_error
        def my_conversion_function():
            # conversion logic here
            pass
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConversionError:
            # Re-raise our custom errors as-is
            raise
        except ValueError as e:
            raise ValidationError(f"Invalid data: {str(e)}", original_error=e)
        except FileNotFoundError as e:
            raise ProcessingError(f"File not found: {str(e)}", original_error=e)
        except MemoryError as e:
            raise ProcessingError(f"Insufficient memory: {str(e)}", original_error=e)
        except Exception as e:
            raise ConversionError(f"Unexpected error: {str(e)}", original_error=e)
    
    return wrapper