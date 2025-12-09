# Universal File Operator

A comprehensive Python-based conversion system that supports converting between various data formats with both CLI and web interfaces. Currently supports **77+ conversion combinations** with modern web GUI and extensible plugin architecture.

## Features

### Supported Conversions

#### **Encoding & Binary**
- Binary ↔ Base64
- Binary ↔ Hexadecimal  
- Base64 ↔ Hexadecimal
- ASCII ↔ Text
- URL encoding/decoding

#### **Image Formats**
- JPEG ↔ PNG ↔ GIF ↔ BMP ↔ TIFF ↔ WebP ↔ ICO
- Image → Base64
- Base64 → Image (any format)
- Image → Hexadecimal
- Quality control for JPEG/WebP
- Transparency support for PNG

#### **Data Formats**
- JSON ↔ XML
- JSON ↔ CSV
- JSON ↔ YAML
- Dictionary ↔ JSON

#### **Number Systems**
- Binary ↔ Decimal ↔ Hexadecimal ↔ Octal
- Unit conversions

#### **Cryptographic**
- MD5, SHA1, SHA256 hashing
- CRC32 checksums

## Architecture

### Modular Plugin System
- **Base Converter Architecture**: Abstract base classes with plugin registration
- **Decorator-based Registry**: Automatic converter discovery and registration
- **Bidirectional Support**: Automatic reverse operation registration
- **Format Detection**: Smart input format detection

### Dual Interface Support
- **CLI Interface**: Command-line tool using Click framework
- **Web Interface**: Flask-based web application with file upload and real-time conversion
   pip install flask click rich pyyaml pillow python-magic
   ```

### Start the Web Interface

**Option 1: Direct Flask App (Recommended)**
```bash
# From project root directory
source venv/bin/activate
PYTHONPATH=. python src/web/app.py
```

**Option 2: Using Python Module**
```bash
source venv/bin/activate
python -m src.web.app
```

The web interface will be available at: **http://127.0.0.1:5000**

### Use the CLI Interface

```bash
# From project root with virtual environment activated
source venv/bin/activate

# Convert data directly
python -m src.cli.main convert "Hello World" --from text --to base64

# Interactive mode with format selection
python -m src.cli.main convert "SGVsbG8gV29ybGQ=" --from base64 --to text

# List all available conversions
python -m src.cli.main list-conversions
```

## Supported Conversions (73+ Types)

### Text & Encoding (12 conversions)
- **Binary** ↔ **Base64** ↔ **Hexadecimal**
- **Text** ↔ **URL Encoded** ↔ **HTML Encoded** 
- **ASCII** ↔ **Unicode** ↔ **Binary**

### Number Systems (18 conversions)
- **Decimal** ↔ **Binary** ↔ **Hexadecimal** ↔ **Octal**
- **Binary Numbers** ↔ **Decimal Numbers**
- Full cross-format number base conversions

### Cryptographic Hashes (15 conversions)
- **Text/Binary** → **MD5**, **SHA1**, **SHA256**, **SHA512**
- **Secure hashing** for data integrity and validation

### Data Formats (12 conversions)
- **JSON** ↔ **Python Dictionary** ↔ **YAML**
- **CSV** ↔ **JSON** ↔ **Lists**
- Structured data interchange formats

### Image Formats (26 conversions)
- **JPEG** ↔ **PNG** ↔ **GIF** ↔ **BMP**
- **TIFF** ↔ **WebP** ↔ **ICO**
- **Image** ↔ **Base64** (universal format)
- Quality control, transparency handling, compression options

## Usage Examples

### Web Interface (Recommended for Beginners)

1. **Start the web server:**
   ```bash
   cd /home/kavindu-janith/FUN/BINARY_BASE64_converter
   source venv/bin/activate
   PYTHONPATH=. python src/web/app.py
   ```

2. **Open in browser:** `http://127.0.0.1:5000`

3. **Features:**
   - Dropdown menus for easy format selection
   - Interactive examples with one-click loading
   - Real-time conversion with loading animations
   - Error handling with helpful messages
   - Responsive design for mobile and desktop

### Command Line Interface (Advanced Users)

```bash
# Text conversions
python -m src.cli.main convert "Hello World" --from text --to base64
python -m src.cli.main convert "SGVsbG8gV29ybGQ=" --from base64 --to text

# Number conversions  
python -m src.cli.main convert "42" --from decimal --to binary
python -m src.cli.main convert "101010" --from binary --to hex

# Image conversions (using base64 data)
python -m src.cli.main convert "<image_base64>" --from png --to jpeg
python -m src.cli.main convert "<image_base64>" --from jpeg --to webp

# Hash generation
python -m src.cli.main convert "password123" --from text --to md5
python -m src.cli.main convert "sensitive data" --from text --to sha256

# List all available conversions
python -m src.cli.main list-conversions
```

### Python API Integration

```python
# Add the project root to Python path
import sys
import os
sys.path.insert(0, '/path/to/BINARY_BASE64_converter')

from src.cli.main import convert, list_conversions

# Simple conversions
text_to_b64 = convert("Hello World", "text", "base64")
b64_to_text = convert(text_to_b64, "base64", "text")
number_to_bin = convert("42", "decimal", "binary")
hash_result = convert("password", "text", "sha256")

# List all available conversions
conversions = list_conversions()
print(f"Total conversions available: {len(conversions)}")

# Using the registry directly (advanced)
from src.converters.registry import ConversionRegistry
registry = ConversionRegistry()

# Direct conversion
result = registry.convert("Hello", "text", "base64")

# Get converter instance
converter = registry.get_converter("png", "jpeg")
jpeg_data = converter.convert(png_base64_data, quality=95)
```

## Project Architecture

```
/home/kavindu-janith/FUN/BINARY_BASE64_converter/
├── src/                           # Main source code
│   ├── converters/                # All format converters
│   │   ├── registry.py           # Central conversion registry
│   │   ├── base_converter.py     # Abstract base class  
│   │   ├── simple_converters.py  # Individual converter classes
│   │   ├── image_converters.py   # Image format converters (PIL/Pillow)
│   │   ├── hashing.py           # Cryptographic hash converters
│   │   └── __init__.py          # Auto-loading converter modules
│   ├── cli/                      # Command-line interface
│   │   └── main.py              # Click-based CLI with Rich output
│   ├── web/                      # Flask web interface
│   │   ├── app.py               # Main Flask application
│   │   └── templates/           # HTML templates
│   │       └── index.html       # Main web interface
│   └── utils/                    # Utility functions
│       └── exceptions.py         # Custom exception classes
├── tests/                        # Test demonstrations
├── venv/                         # Virtual environment
├── requirements.txt              # Project dependencies
└── README.md                     # This file
```

### Key Design Patterns

- **Registry Pattern**: Automatic converter discovery and registration
- **Decorator Pattern**: `@register_converter` for clean registration
- **Abstract Base Class**: Consistent converter interface via `BaseConverter`
- **Factory Pattern**: Dynamic converter instantiation via registry

## Testing & Demonstrations

### Built-in Test Scripts

```bash
# Test all image conversions with real examples
python test_image_converters.py

# Demonstrate image conversion capabilities  
python demo_image_conversions.py

# Test basic converter functionality
python test_converter.py
```

### Manual Testing

```bash
# Test web interface
# 1. Start the web app: PYTHONPATH=. python src/web/app.py
# 2. Open browser to http://127.0.0.1:5000
# 3. Try the example conversions and dropdown selections

# Test CLI interface
python -m src.cli.main convert "test data" --from text --to base64
python -m src.cli.main list-conversions | head -20
```

## Learning Outcomes & Next Steps

### What You've Built
- Complete Format Converter with 73+ conversion types
- Modern Web Application using Flask, HTML, CSS, JavaScript
- Command Line Tool with Click and Rich libraries
- Image Processing System using PIL/Pillow
- Object-Oriented Design with abstract base classes
- Registry Pattern Implementation for plugin architecture

### Concepts Mastered
- **Python OOP**: Inheritance, abstract classes, decorators
- **Web Development**: Flask framework, templates, AJAX
- **CLI Development**: Argument parsing, user interaction  
- **Image Processing**: Format conversion, quality control
- **Error Handling**: Custom exceptions, validation
- **Code Organization**: Modular design, separation of concerns

### Possible Enhancements (Learning Opportunities)
1. **Add Compression**: ZIP, GZIP, TAR format support
2. **Batch Processing**: Multi-file conversion with progress bars
3. **Format Detection**: Auto-detect file types by content
4. **API Endpoint**: RESTful API for external integrations
5. **File Upload**: Direct file upload in web interface
6. **Performance**: Async processing for large files
7. **Database**: Save conversion history and user preferences

## Troubleshooting

### Common Issues & Solutions

**Import Errors:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Set PYTHONPATH when running modules
PYTHONPATH=. python src/web/app.py
```

**Web Server Issues:**
```bash
# Check if port 5000 is available
lsof -i :5000

# Try different port
export FLASK_RUN_PORT=8080
```

**Missing Dependencies:**
```bash
# Install all required packages
pip install flask click rich pyyaml pillow python-magic
```

## Project Statistics

- **Source Files**: 15+ Python modules
- **Conversions**: 73+ different format combinations
- **Image Formats**: 7 formats (JPEG, PNG, GIF, BMP, TIFF, WebP, ICO)
- **CLI Commands**: Interactive and direct conversion modes
- **Web Features**: Responsive UI with real-time conversion
- **Learning Concepts**: 10+ advanced Python programming patterns

## Success! You've Built

A **production-ready format converter** that demonstrates:
- Modern Python development practices
- Web application development
- Command-line tool creation  
- Image processing capabilities
- Clean code architecture
- User-friendly interfaces

**Perfect for portfolios, interviews, and continued learning!**

---

### Quick Start Summary

```bash
cd /home/kavindu-janith/FUN/BINARY_BASE64_converter
source venv/bin/activate
PYTHONPATH=. python src/web/app.py
# Open http://127.0.0.1:5000 in browser
```

**Happy Converting!**