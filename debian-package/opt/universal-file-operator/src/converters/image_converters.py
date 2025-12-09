"""
Image Format Converters
======================

Comprehensive image format conversion system supporting all major image types.
Uses PIL/Pillow for robust image processing and format conversion.

Supported Formats:
- JPEG/JPG (with quality control)
- PNG (with transparency support)
- GIF (with animation support)
- BMP (bitmap format)
- TIFF (with compression)
- WebP (modern web format)
- ICO (icon format)

Learning Concepts:
- PIL/Pillow library usage
- Image format characteristics
- Quality and compression settings
- Binary data handling
- File I/O operations
- Error handling for image processing
"""

from PIL import Image, ImageSequence
import io
import base64
from typing import Dict, Any, Optional, Union
import os

from .base_converter import BaseConverter
from .registry import register_converter
from ..utils.exceptions import ConversionError, ValidationError


class ImageConverter(BaseConverter):
    """Base class for all image converters with common functionality."""

# JPEG to binary (01 string) converter
@register_converter("jpeg", "binary")
class JpegToBinaryConverter(ImageConverter):
    """Convert JPEG image to binary (01 string) representation."""
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert JPEG to binary string (01 representation)."""
        if isinstance(data, str):
            # If it's a file path
            if os.path.exists(data):
                with open(data, 'rb') as f:
                    image_bytes = f.read()
            else:
                # Try as base64
                try:
                    image_bytes = base64.b64decode(data)
                except:
                    raise ValidationError("Invalid JPEG data provided")
        else:
            image_bytes = data
        # Convert bytes to 01 string
        return ''.join(f'{byte:08b}' for byte in image_bytes)
    
    SUPPORTED_FORMATS = {
        'jpeg': {'extensions': ['.jpg', '.jpeg'], 'mime': 'image/jpeg', 'mode': 'RGB'},
        'png': {'extensions': ['.png'], 'mime': 'image/png', 'mode': 'RGBA'},
        'gif': {'extensions': ['.gif'], 'mime': 'image/gif', 'mode': 'P'},
        'bmp': {'extensions': ['.bmp'], 'mime': 'image/bmp', 'mode': 'RGB'},
        'tiff': {'extensions': ['.tiff', '.tif'], 'mime': 'image/tiff', 'mode': 'RGB'},
        'webp': {'extensions': ['.webp'], 'mime': 'image/webp', 'mode': 'RGB'},
        'ico': {'extensions': ['.ico'], 'mime': 'image/x-icon', 'mode': 'RGBA'},
    }
    
    def __init__(self, from_format: str, to_format: str):
        super().__init__(from_format, to_format)
        self.default_quality = 85
        self.default_optimize = True
    
    def _load_image_from_data(self, data: Union[str, bytes]) -> Image.Image:
        """Load PIL Image from various data formats."""
        try:
            if isinstance(data, str):
                # Try to decode as base64 first
                try:
                    image_bytes = base64.b64decode(data)
                except Exception:
                    # If not base64, treat as file path
                    if os.path.exists(data):
                        return Image.open(data)
                    else:
                        raise ValidationError(f"Invalid image data or file path: {data}")
            else:
                image_bytes = data
            
            # Load from bytes
            image_buffer = io.BytesIO(image_bytes)
            image = Image.open(image_buffer)
            return image
            
        except Exception as e:
            raise ConversionError(f"Failed to load image: {str(e)}")
    
    def _image_to_bytes(self, image: Image.Image, format_name: str, **kwargs) -> bytes:
        """Convert PIL Image to bytes in specified format."""
        try:
            output_buffer = io.BytesIO()
            
            # Get format info
            format_info = self.SUPPORTED_FORMATS.get(format_name.lower())
            if not format_info:
                raise ValidationError(f"Unsupported image format: {format_name}")
            
            # Convert image mode if needed
            target_mode = format_info['mode']
            if image.mode != target_mode:
                if target_mode == 'RGB' and image.mode == 'RGBA':
                    # Handle transparency for RGB formats
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                    image = background
                elif target_mode == 'P' and format_name.lower() == 'gif':
                    # Convert to palette mode for GIF
                    image = image.convert('P', palette=Image.ADAPTIVE)
                else:
                    image = image.convert(target_mode)
            
            # Set format-specific parameters
            save_kwargs = {}
            if format_name.lower() == 'jpeg':
                save_kwargs.update({
                    'quality': kwargs.get('quality', self.default_quality),
                    'optimize': kwargs.get('optimize', self.default_optimize)
                })
            elif format_name.lower() == 'png':
                save_kwargs.update({
                    'optimize': kwargs.get('optimize', self.default_optimize)
                })
            elif format_name.lower() == 'webp':
                save_kwargs.update({
                    'quality': kwargs.get('quality', self.default_quality),
                    'method': kwargs.get('method', 6)
                })
            elif format_name.lower() == 'tiff':
                save_kwargs.update({
                    'compression': kwargs.get('compression', 'lzw')
                })
            
            # Save image to buffer
            image.save(output_buffer, format=format_name.upper(), **save_kwargs)
            return output_buffer.getvalue()
            
        except Exception as e:
            raise ConversionError(f"Failed to convert image to {format_name}: {str(e)}")


# JPEG Converters
@register_converter("jpeg", "png")
class JpegToPngConverter(ImageConverter):
    """Convert JPEG images to PNG format (adds transparency support)."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert JPEG to PNG and return as base64."""
        image = self._load_image_from_data(data)
        
        # Convert to RGBA for PNG transparency support
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        png_bytes = self._image_to_bytes(image, 'png')
        return base64.b64encode(png_bytes).decode('utf-8')


@register_converter("png", "jpeg")
class PngToJpegConverter(ImageConverter):
    """Convert PNG images to JPEG format (removes transparency)."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert PNG to JPEG and return as base64."""
        image = self._load_image_from_data(data)
        
        jpeg_bytes = self._image_to_bytes(image, 'jpeg', quality=90)
        return base64.b64encode(jpeg_bytes).decode('utf-8')


@register_converter("jpeg", "webp")
class JpegToWebpConverter(ImageConverter):
    """Convert JPEG to WebP format (better compression)."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert JPEG to WebP and return as base64."""
        image = self._load_image_from_data(data)
        
        webp_bytes = self._image_to_bytes(image, 'webp', quality=80, method=6)
        return base64.b64encode(webp_bytes).decode('utf-8')


@register_converter("webp", "jpeg")
class WebpToJpegConverter(ImageConverter):
    """Convert WebP to JPEG format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert WebP to JPEG and return as base64."""
        image = self._load_image_from_data(data)
        
        jpeg_bytes = self._image_to_bytes(image, 'jpeg', quality=90)
        return base64.b64encode(jpeg_bytes).decode('utf-8')


# PNG Converters
@register_converter("png", "gif")
class PngToGifConverter(ImageConverter):
    """Convert PNG to GIF format (adds palette mode)."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert PNG to GIF and return as base64."""
        image = self._load_image_from_data(data)
        
        gif_bytes = self._image_to_bytes(image, 'gif')
        return base64.b64encode(gif_bytes).decode('utf-8')


@register_converter("gif", "png")
class GifToPngConverter(ImageConverter):
    """Convert GIF to PNG format (preserves transparency)."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert GIF to PNG and return as base64."""
        image = self._load_image_from_data(data)
        
        # Convert palette mode to RGBA for PNG
        if image.mode == 'P':
            image = image.convert('RGBA')
        
        png_bytes = self._image_to_bytes(image, 'png')
        return base64.b64encode(png_bytes).decode('utf-8')


# BMP Converters
@register_converter("bmp", "png")
class BmpToPngConverter(ImageConverter):
    """Convert BMP to PNG format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert BMP to PNG and return as base64."""
        image = self._load_image_from_data(data)
        
        png_bytes = self._image_to_bytes(image, 'png')
        return base64.b64encode(png_bytes).decode('utf-8')


@register_converter("png", "bmp")
class PngToBmpConverter(ImageConverter):
    """Convert PNG to BMP format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert PNG to BMP and return as base64."""
        image = self._load_image_from_data(data)
        
        bmp_bytes = self._image_to_bytes(image, 'bmp')
        return base64.b64encode(bmp_bytes).decode('utf-8')


@register_converter("bmp", "jpeg")
class BmpToJpegConverter(ImageConverter):
    """Convert BMP to JPEG format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert BMP to JPEG and return as base64."""
        image = self._load_image_from_data(data)
        
        jpeg_bytes = self._image_to_bytes(image, 'jpeg', quality=90)
        return base64.b64encode(jpeg_bytes).decode('utf-8')


@register_converter("jpeg", "bmp")
class JpegToBmpConverter(ImageConverter):
    """Convert JPEG to BMP format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert JPEG to BMP and return as base64."""
        image = self._load_image_from_data(data)
        
        bmp_bytes = self._image_to_bytes(image, 'bmp')
        return base64.b64encode(bmp_bytes).decode('utf-8')


# TIFF Converters
@register_converter("tiff", "png")
class TiffToPngConverter(ImageConverter):
    """Convert TIFF to PNG format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert TIFF to PNG and return as base64."""
        image = self._load_image_from_data(data)
        
        png_bytes = self._image_to_bytes(image, 'png')
        return base64.b64encode(png_bytes).decode('utf-8')


@register_converter("png", "tiff")
class PngToTiffConverter(ImageConverter):
    """Convert PNG to TIFF format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert PNG to TIFF and return as base64."""
        image = self._load_image_from_data(data)
        
        tiff_bytes = self._image_to_bytes(image, 'tiff', compression='lzw')
        return base64.b64encode(tiff_bytes).decode('utf-8')


@register_converter("tiff", "jpeg")
class TiffToJpegConverter(ImageConverter):
    """Convert TIFF to JPEG format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert TIFF to JPEG and return as base64."""
        image = self._load_image_from_data(data)
        
        jpeg_bytes = self._image_to_bytes(image, 'jpeg', quality=90)
        return base64.b64encode(jpeg_bytes).decode('utf-8')


@register_converter("jpeg", "tiff")
class JpegToTiffConverter(ImageConverter):
    """Convert JPEG to TIFF format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert JPEG to TIFF and return as base64."""
        image = self._load_image_from_data(data)
        
        tiff_bytes = self._image_to_bytes(image, 'tiff', compression='lzw')
        return base64.b64encode(tiff_bytes).decode('utf-8')


# WebP Converters
@register_converter("webp", "png")
class WebpToPngConverter(ImageConverter):
    """Convert WebP to PNG format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert WebP to PNG and return as base64."""
        image = self._load_image_from_data(data)
        
        png_bytes = self._image_to_bytes(image, 'png')
        return base64.b64encode(png_bytes).decode('utf-8')


@register_converter("png", "webp")
class PngToWebpConverter(ImageConverter):
    """Convert PNG to WebP format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert PNG to WebP and return as base64."""
        image = self._load_image_from_data(data)
        
        webp_bytes = self._image_to_bytes(image, 'webp', quality=80, method=6)
        return base64.b64encode(webp_bytes).decode('utf-8')


# ICO Converters
@register_converter("ico", "png")
class IcoToPngConverter(ImageConverter):
    """Convert ICO (icon) to PNG format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert ICO to PNG and return as base64."""
        image = self._load_image_from_data(data)
        
        # ICO files can contain multiple sizes, use the largest
        if hasattr(image, 'size'):
            png_bytes = self._image_to_bytes(image, 'png')
        else:
            # Handle multi-frame ICO
            largest_frame = max(ImageSequence.Iterator(image), key=lambda x: x.size[0] * x.size[1])
            png_bytes = self._image_to_bytes(largest_frame, 'png')
        
        return base64.b64encode(png_bytes).decode('utf-8')


@register_converter("png", "ico")
class PngToIcoConverter(ImageConverter):
    """Convert PNG to ICO format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert PNG to ICO and return as base64."""
        image = self._load_image_from_data(data)
        
        # Resize to common ICO sizes if too large
        max_size = 256
        if image.width > max_size or image.height > max_size:
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        ico_bytes = self._image_to_bytes(image, 'ico')
        return base64.b64encode(ico_bytes).decode('utf-8')


# Additional format converters
@register_converter("gif", "jpeg")
class GifToJpegConverter(ImageConverter):
    """Convert GIF to JPEG format (first frame only)."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert GIF to JPEG and return as base64."""
        image = self._load_image_from_data(data)
        
        # For animated GIFs, take the first frame
        if getattr(image, 'is_animated', False):
            image.seek(0)
        
        jpeg_bytes = self._image_to_bytes(image, 'jpeg', quality=90)
        return base64.b64encode(jpeg_bytes).decode('utf-8')


@register_converter("jpeg", "gif")
class JpegToGifConverter(ImageConverter):
    """Convert JPEG to GIF format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert JPEG to GIF and return as base64."""
        image = self._load_image_from_data(data)
        
        gif_bytes = self._image_to_bytes(image, 'gif')
        return base64.b64encode(gif_bytes).decode('utf-8')


# Cross-format converters
@register_converter("bmp", "gif")
class BmpToGifConverter(ImageConverter):
    """Convert BMP to GIF format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert BMP to GIF and return as base64."""
        image = self._load_image_from_data(data)
        
        gif_bytes = self._image_to_bytes(image, 'gif')
        return base64.b64encode(gif_bytes).decode('utf-8')


@register_converter("gif", "bmp")
class GifToBmpConverter(ImageConverter):
    """Convert GIF to BMP format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert GIF to BMP and return as base64."""
        image = self._load_image_from_data(data)
        
        bmp_bytes = self._image_to_bytes(image, 'bmp')
        return base64.b64encode(bmp_bytes).decode('utf-8')


@register_converter("webp", "gif")
class WebpToGifConverter(ImageConverter):
    """Convert WebP to GIF format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert WebP to GIF and return as base64."""
        image = self._load_image_from_data(data)
        
        gif_bytes = self._image_to_bytes(image, 'gif')
        return base64.b64encode(gif_bytes).decode('utf-8')


@register_converter("gif", "webp")
class GifToWebpConverter(ImageConverter):
    """Convert GIF to WebP format."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert GIF to WebP and return as base64."""
        image = self._load_image_from_data(data)
        
        webp_bytes = self._image_to_bytes(image, 'webp', quality=80, method=6)
        return base64.b64encode(webp_bytes).decode('utf-8')


# Utility converters
@register_converter("image", "base64")
class ImageToBase64Converter(ImageConverter):
    """Convert any supported image format to base64 string."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert image to base64 string."""
        if isinstance(data, str) and os.path.exists(data):
            with open(data, 'rb') as f:
                image_bytes = f.read()
            return base64.b64encode(image_bytes).decode('utf-8')
        elif isinstance(data, bytes):
            return base64.b64encode(data).decode('utf-8')
        else:
            raise ValidationError("Invalid image data provided")


@register_converter("base64", "image")
class Base64ToImageConverter(ImageConverter):
    """Convert base64 string to image (auto-detect format)."""
    
    def _convert(self, data: str, **options) -> bytes:
        """Convert base64 to image bytes."""
        try:
            image_bytes = base64.b64decode(data)
            
            # Validate that it's actually an image
            image_buffer = io.BytesIO(image_bytes)
            image = Image.open(image_buffer)
            image.verify()  # Verify it's a valid image
            
            return image_bytes
        except Exception as e:
            raise ConversionError(f"Invalid base64 image data: {str(e)}")


@register_converter("base64", "jpeg")
class Base64ToJpegConverter(ImageConverter):
    """Convert base64 string to JPEG image."""
    
    def _convert(self, data: str, **options) -> bytes:
        """Convert base64 to JPEG bytes."""
        try:
            # Decode base64 to bytes
            image_bytes = base64.b64decode(data)
            
            # Open the image
            image_buffer = io.BytesIO(image_bytes)
            image = Image.open(image_buffer)
            
            # Convert to RGB if necessary (JPEG doesn't support transparency)
            if image.mode in ('RGBA', 'LA', 'P'):
                # Create white background for transparency
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                if image.mode == 'RGBA':
                    background.paste(image, mask=image.split()[-1])
                else:
                    background.paste(image)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Save as JPEG
            output_buffer = io.BytesIO()
            quality = options.get('quality', 95)
            image.save(output_buffer, format='JPEG', quality=quality, optimize=True)
            
            return output_buffer.getvalue()
        except Exception as e:
            raise ConversionError(f"Failed to convert base64 to JPEG: {str(e)}")


@register_converter("base64", "png")
class Base64ToPngConverter(ImageConverter):
    """Convert base64 string to PNG image."""
    
    def _convert(self, data: str, **options) -> bytes:
        """Convert base64 to PNG bytes."""
        try:
            # Decode base64 to bytes
            image_bytes = base64.b64decode(data)
            
            # Open the image
            image_buffer = io.BytesIO(image_bytes)
            image = Image.open(image_buffer)
            
            # Save as PNG (supports all modes including transparency)
            output_buffer = io.BytesIO()
            image.save(output_buffer, format='PNG', optimize=True)
            
            return output_buffer.getvalue()
        except Exception as e:
            raise ConversionError(f"Failed to convert base64 to PNG: {str(e)}")


@register_converter("base64", "gif")
class Base64ToGifConverter(ImageConverter):
    """Convert base64 string to GIF image."""
    
    def _convert(self, data: str, **options) -> bytes:
        """Convert base64 to GIF bytes."""
        try:
            # Decode base64 to bytes
            image_bytes = base64.b64decode(data)
            
            # Open the image
            image_buffer = io.BytesIO(image_bytes)
            image = Image.open(image_buffer)
            
            # Convert to appropriate mode for GIF
            if image.mode not in ('P', 'L'):
                image = image.convert('P', palette=Image.ADAPTIVE)
            
            # Save as GIF
            output_buffer = io.BytesIO()
            image.save(output_buffer, format='GIF', optimize=True)
            
            return output_buffer.getvalue()
        except Exception as e:
            raise ConversionError(f"Failed to convert base64 to GIF: {str(e)}")


@register_converter("base64", "bmp")
class Base64ToBmpConverter(ImageConverter):
    """Convert base64 string to BMP image."""
    
    def _convert(self, data: str, **options) -> bytes:
        """Convert base64 to BMP bytes."""
        try:
            # Decode base64 to bytes
            image_bytes = base64.b64decode(data)
            
            # Open the image
            image_buffer = io.BytesIO(image_bytes)
            image = Image.open(image_buffer)
            
            # Convert to RGB (BMP doesn't support transparency well)
            if image.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'RGBA':
                    background.paste(image, mask=image.split()[-1])
                else:
                    background.paste(image)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Save as BMP
            output_buffer = io.BytesIO()
            image.save(output_buffer, format='BMP')
            
            return output_buffer.getvalue()
        except Exception as e:
            raise ConversionError(f"Failed to convert base64 to BMP: {str(e)}")


@register_converter("base64", "webp")
class Base64ToWebpConverter(ImageConverter):
    """Convert base64 string to WebP image."""
    
    def _convert(self, data: str, **options) -> bytes:
        """Convert base64 to WebP bytes."""
        try:
            # Decode base64 to bytes
            image_bytes = base64.b64decode(data)
            
            # Open the image
            image_buffer = io.BytesIO(image_bytes)
            image = Image.open(image_buffer)
            
            # Save as WebP
            output_buffer = io.BytesIO()
            quality = options.get('quality', 95)
            image.save(output_buffer, format='WebP', quality=quality, method=6)
            
            return output_buffer.getvalue()
        except Exception as e:
            raise ConversionError(f"Failed to convert base64 to WebP: {str(e)}")


@register_converter("base64", "tiff")
class Base64ToTiffConverter(ImageConverter):
    """Convert base64 string to TIFF image."""
    
    def _convert(self, data: str, **options) -> bytes:
        """Convert base64 to TIFF bytes."""
        try:
            # Decode base64 to bytes
            image_bytes = base64.b64decode(data)
            
            # Open the image
            image_buffer = io.BytesIO(image_bytes)
            image = Image.open(image_buffer)
            
            # Save as TIFF
            output_buffer = io.BytesIO()
            compression = options.get('compression', 'lzw')
            image.save(output_buffer, format='TIFF', compression=compression)
            
            return output_buffer.getvalue()
        except Exception as e:
            raise ConversionError(f"Failed to convert base64 to TIFF: {str(e)}")


@register_converter("base64", "ico")
class Base64ToIcoConverter(ImageConverter):
    """Convert base64 string to ICO image."""
    
    def _convert(self, data: str, **options) -> bytes:
        """Convert base64 to ICO bytes."""
        try:
            # Decode base64 to bytes
            image_bytes = base64.b64decode(data)
            
            # Open the image
            image_buffer = io.BytesIO(image_bytes)
            image = Image.open(image_buffer)
            
            # Resize to common ICO sizes if needed
            size = options.get('size', 32)
            if image.size != (size, size):
                image = image.resize((size, size), Image.Resampling.LANCZOS)
            
            # Convert to RGBA for ICO
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            # Save as ICO
            output_buffer = io.BytesIO()
            image.save(output_buffer, format='ICO', sizes=[(size, size)])
            
            return output_buffer.getvalue()
        except Exception as e:
            raise ConversionError(f"Failed to convert base64 to ICO: {str(e)}")


# Image to Hex Converters
@register_converter("png", "hex")
class PngToHexConverter(ImageConverter):
    """Convert PNG image to hexadecimal representation."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert PNG to hex string."""
        if isinstance(data, str):
            # If it's a file path
            if os.path.exists(data):
                with open(data, 'rb') as f:
                    image_bytes = f.read()
            else:
                # Try as base64
                try:
                    image_bytes = base64.b64decode(data)
                except:
                    raise ValidationError("Invalid PNG data provided")
        else:
            image_bytes = data
        
        return image_bytes.hex()


@register_converter("jpeg", "hex")
class JpegToHexConverter(ImageConverter):
    """Convert JPEG image to hexadecimal representation."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert JPEG to hex string."""
        if isinstance(data, str):
            # If it's a file path
            if os.path.exists(data):
                with open(data, 'rb') as f:
                    image_bytes = f.read()
            else:
                # Try as base64
                try:
                    image_bytes = base64.b64decode(data)
                except:
                    raise ValidationError("Invalid JPEG data provided")
        else:
            image_bytes = data
        
        return image_bytes.hex()


@register_converter("gif", "hex")
class GifToHexConverter(ImageConverter):
    """Convert GIF image to hexadecimal representation."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert GIF to hex string."""
        if isinstance(data, str):
            # If it's a file path
            if os.path.exists(data):
                with open(data, 'rb') as f:
                    image_bytes = f.read()
            else:
                # Try as base64
                try:
                    image_bytes = base64.b64decode(data)
                except:
                    raise ValidationError("Invalid GIF data provided")
        else:
            image_bytes = data
        
        return image_bytes.hex()


@register_converter("bmp", "hex")
class BmpToHexConverter(ImageConverter):
    """Convert BMP image to hexadecimal representation."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert BMP to hex string."""
        if isinstance(data, str):
            # If it's a file path
            if os.path.exists(data):
                with open(data, 'rb') as f:
                    image_bytes = f.read()
            else:
                # Try as base64
                try:
                    image_bytes = base64.b64decode(data)
                except:
                    raise ValidationError("Invalid BMP data provided")
        else:
            image_bytes = data
        
        return image_bytes.hex()


@register_converter("webp", "hex")
class WebpToHexConverter(ImageConverter):
    """Convert WebP image to hexadecimal representation."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert WebP to hex string."""
        if isinstance(data, str):
            # If it's a file path
            if os.path.exists(data):
                with open(data, 'rb') as f:
                    image_bytes = f.read()
            else:
                # Try as base64
                try:
                    image_bytes = base64.b64decode(data)
                except:
                    raise ValidationError("Invalid WebP data provided")
        else:
            image_bytes = data
        
        return image_bytes.hex()


@register_converter("tiff", "hex")
class TiffToHexConverter(ImageConverter):
    """Convert TIFF image to hexadecimal representation."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert TIFF to hex string."""
        if isinstance(data, str):
            # If it's a file path
            if os.path.exists(data):
                with open(data, 'rb') as f:
                    image_bytes = f.read()
            else:
                # Try as base64
                try:
                    image_bytes = base64.b64decode(data)
                except:
                    raise ValidationError("Invalid TIFF data provided")
        else:
            image_bytes = data
        
        return image_bytes.hex()


@register_converter("ico", "hex")
class IcoToHexConverter(ImageConverter):
    """Convert ICO image to hexadecimal representation."""
    
    def _convert(self, data: Union[str, bytes], **options) -> str:
        """Convert ICO to hex string."""
        if isinstance(data, str):
            # If it's a file path
            if os.path.exists(data):
                with open(data, 'rb') as f:
                    image_bytes = f.read()
            else:
                # Try as base64
                try:
                    image_bytes = base64.b64decode(data)
                except:
                    raise ValidationError("Invalid ICO data provided")
        else:
            image_bytes = data
        
        return image_bytes.hex()


# --- DYNAMIC CONVERTER REGISTRATION (must be after all imports/classes) ---
# Helper functions for dynamic converters
def _binary_to_image(data, fmt):
    """Convert binary string (01) to image format."""
    if not isinstance(data, str):
        data = str(data)
    # Remove any whitespace and common separators
    data = data.replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
    # Validate binary string
    invalid_chars = [c for c in data if c not in '01']
    if invalid_chars:
        # Get first few invalid characters for error message
        invalid_sample = ''.join(set(invalid_chars))[:10]
        raise ValidationError(f"Input contains invalid characters: '{invalid_sample}'. Only 0 and 1 are allowed.")
    # Convert binary string to bytes
    if len(data) % 8 != 0:
        # Pad with zeros if needed
        padding = 8 - (len(data) % 8)
        data = '0' * padding + data
    image_bytes = bytes(int(data[i:i+8], 2) for i in range(0, len(data), 8))
    
    # Load and convert image
    try:
        image = Image.open(io.BytesIO(image_bytes))
        output = io.BytesIO()
        
        # Handle JPEG format specifically (requires RGB mode)
        if fmt.lower() == 'jpeg':
            if image.mode in ('RGBA', 'LA', 'P'):
                # Convert to RGB for JPEG
                if image.mode == 'P':
                    image = image.convert('RGBA')
                # Create white background
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'RGBA' or image.mode == 'LA':
                    background.paste(image, mask=image.split()[-1])  # Use alpha channel as mask
                else:
                    background.paste(image)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
        
        image.save(output, format=fmt.upper())
        return output.getvalue()
    except Exception as e:
        raise ConversionError(f"Failed to convert binary to {fmt.upper()} image: {str(e)}")

def _hex_to_image(data, fmt):
    """Convert hex string to image format."""
    if not isinstance(data, str):
        data = str(data)
    # Remove common hex prefixes and separators
    cleaned = data.replace('0x', '').replace(':', '').replace('-', '').replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
    
    # Validate hex string
    try:
        image_bytes = bytes.fromhex(cleaned)
    except ValueError as e:
        raise ValidationError(f"Invalid hexadecimal string: {str(e)}")
    
    # Convert to image
    try:
        image = Image.open(io.BytesIO(image_bytes))
        output = io.BytesIO()
        
        # Handle JPEG format specifically (requires RGB mode)
        if fmt.lower() == 'jpeg':
            if image.mode in ('RGBA', 'LA', 'P'):
                # Convert to RGB for JPEG
                if image.mode == 'P':
                    image = image.convert('RGBA')
                # Create white background
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'RGBA' or image.mode == 'LA':
                    background.paste(image, mask=image.split()[-1])  # Use alpha channel as mask
                else:
                    background.paste(image)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
        
        image.save(output, format=fmt.upper())
        return output.getvalue()
    except Exception as e:
        raise ConversionError(f"Failed to convert hex to {fmt.upper()} image: {str(e)}")

def _image_to_base64(data, fmt):
    """Convert image data to base64 string in specified format."""
    # Load image from data
    if isinstance(data, str):
        if os.path.exists(data):
            with open(data, 'rb') as f:
                data = f.read()
        else:
            try:
                data = base64.b64decode(data)
            except:
                raise ValidationError("Invalid image data")
    
    image = Image.open(io.BytesIO(data))
    output = io.BytesIO()
    image.save(output, format=fmt.upper())
    return base64.b64encode(output.getvalue()).decode('utf-8')

def _image_to_binary_bytes(data, fmt):
    """Convert image data to binary bytes in specified format."""
    # Load image from data
    if isinstance(data, str):
        if os.path.exists(data):
            with open(data, 'rb') as f:
                data = f.read()
        else:
            try:
                data = base64.b64decode(data)
            except:
                raise ValidationError("Invalid image data")
    
    image = Image.open(io.BytesIO(data))
    output = io.BytesIO()
    image.save(output, format=fmt.upper())
    return output.getvalue()

# Register dynamic converters for all image formats
for fmt in ["jpeg", "png", "gif", "bmp", "tiff", "webp", "ico"]:
    # Binary (01 string) to Image
    exec(f"""
@register_converter('binary', '{fmt}')
class BinaryTo{fmt.capitalize()}Converter(ImageConverter):
    '''Convert binary (01 string) to {fmt.upper()} image.'''
    def _convert(self, data, **options):
        return _binary_to_image(data, '{fmt}')
""", globals())

for fmt in ["jpeg", "png", "gif", "bmp", "tiff", "webp", "ico"]:
    # Hex to Image - now including JPEG
    exec(f"""
@register_converter('hex', '{fmt}')
class HexTo{fmt.capitalize()}Converter(ImageConverter):
    '''Convert hex string to {fmt.upper()} image.'''
    def _convert(self, data, **options):
        return _hex_to_image(data, '{fmt}')
""", globals())

# Add image formats to base64 converters (reverse direction)
for fmt in ["jpeg", "png", "gif", "bmp", "tiff", "webp", "ico"]:
    exec(f"""
@register_converter('{fmt}', 'base64')
class {fmt.capitalize()}ToBase64Converter(ImageConverter):
    '''Convert {fmt.upper()} image to base64 string.'''
    def _convert(self, data, **options):
        return _image_to_base64(data, '{fmt}')
""", globals())

# Add image formats to binary (01 string) converters  
for fmt in ["png", "gif", "bmp", "tiff", "webp", "ico"]:
    exec(f"""
@register_converter('{fmt}', 'binary')
class {fmt.capitalize()}ToBinaryConverter(ImageConverter):
    '''Convert {fmt.upper()} image to binary (01 string).'''
    def _convert(self, data, **options):
        # Load image and convert to bytes
        if isinstance(data, str):
            if os.path.exists(data):
                with open(data, 'rb') as f:
                    image_bytes = f.read()
            else:
                try:
                    image_bytes = base64.b64decode(data)
                except:
                    raise ValidationError("Invalid image data")
        else:
            image_bytes = data
        # Convert bytes to binary string (01)
        return ''.join(f'{{byte:08b}}' for byte in image_bytes)
""", globals())

# Add hex ↔ base64 conversions
@register_converter('hex', 'base64')
class HexToBase64Converter(BaseConverter):
    """Convert hexadecimal to base64."""
    def _convert(self, data, **options):
        if not isinstance(data, str):
            data = str(data)
        # Clean hex string
        cleaned = data.replace('0x', '').replace(':', '').replace('-', '').replace(' ', '').replace('\\n', '').replace('\\r', '').replace('\\t', '')
        try:
            binary_data = bytes.fromhex(cleaned)
            return base64.b64encode(binary_data).decode('utf-8')
        except ValueError as e:
            raise ValidationError(f"Invalid hexadecimal string: {{str(e)}}")

@register_converter('base64', 'hex')
class Base64ToHexConverter(BaseConverter):
    """Convert base64 to hexadecimal."""
    def _convert(self, data, **options):
        if not isinstance(data, str):
            data = str(data)
        try:
            binary_data = base64.b64decode(data)
            return binary_data.hex()
        except Exception as e:
            raise ValidationError(f"Invalid base64 string: {{str(e)}}")

# Add binary (01 string) ↔ hex converters
@register_converter('binary', 'hex')  
class BinaryStringToHexConverter(BaseConverter):
    """Convert binary (01 string) to hexadecimal."""
    def _convert(self, data, **options):
        if not isinstance(data, str):
            data = str(data)
        # Remove whitespace
        data = data.replace(' ', '').replace('\\n', '').replace('\\r', '').replace('\\t', '')
        # Validate binary string
        if not all(c in '01' for c in data):
            raise ValidationError("Input must be a binary string (only 0 and 1)")
        # Pad if needed
        if len(data) % 8 != 0:
            padding = 8 - (len(data) % 8)
            data = '0' * padding + data
        # Convert to hex
        hex_str = ''
        for i in range(0, len(data), 8):
            byte_val = int(data[i:i+8], 2)
            hex_str += f'{{byte_val:02x}}'
        return hex_str

@register_converter('hex', 'binary')
class HexToBinaryStringConverter(BaseConverter):
    """Convert hexadecimal to binary (01 string)."""
    def _convert(self, data, **options):
        if not isinstance(data, str):
            data = str(data)
        # Clean hex string
        cleaned = data.replace('0x', '').replace(':', '').replace('-', '').replace(' ', '').replace('\\n', '').replace('\\r', '').replace('\\t', '')
        try:
            binary_str = ''
            for i in range(0, len(cleaned), 2):
                hex_byte = cleaned[i:i+2]
                byte_val = int(hex_byte, 16)
                binary_str += f'{{byte_val:08b}}'
            return binary_str
        except ValueError as e:
            raise ValidationError(f"Invalid hexadecimal string: {{str(e)}}")

# Helper function for generic image format conversion
def _convert_image_format(data, from_fmt, to_fmt):
    """Convert between any two image formats."""
    # Load image from data
    if isinstance(data, str):
        if os.path.exists(data):
            with open(data, 'rb') as f:
                data = f.read()
        else:
            try:
                data = base64.b64decode(data)
            except:
                raise ValidationError("Invalid image data")
    
    try:
        image = Image.open(io.BytesIO(data))
        output = io.BytesIO()
        
        # Handle JPEG format specifically (requires RGB mode)
        if to_fmt.lower() == 'jpeg':
            if image.mode in ('RGBA', 'LA', 'P'):
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'RGBA' or image.mode == 'LA':
                    background.paste(image, mask=image.split()[-1])
                else:
                    background.paste(image)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
        
        image.save(output, format=to_fmt.upper())
        return output.getvalue()
    except Exception as e:
        raise ConversionError(f"Failed to convert {{from_fmt.upper()}} to {{to_fmt.upper()}}: {{str(e)}}")

# Add all image format to image format conversions dynamically
image_formats = ["jpeg", "png", "gif", "bmp", "tiff", "webp", "ico"]
for from_fmt in image_formats:
    for to_fmt in image_formats:
        if from_fmt != to_fmt:  # Skip same format conversions
            exec(f"""
@register_converter('{from_fmt}', '{to_fmt}')
class {from_fmt.capitalize()}To{to_fmt.capitalize()}DynamicConverter(ImageConverter):
    '''Convert {from_fmt.upper()} to {to_fmt.upper()} image format.'''
    def _convert(self, data, **options):
        return _convert_image_format(data, '{from_fmt}', '{to_fmt}')
""", globals())