# Universal File Operator

A comprehensive Python-based conversion system that supports converting between various data formats with both CLI and web interfaces. Currently supports **77+ conversion combinations** with modern web GUI, PDF merging capabilities, text comparison tools, and extensible plugin architecture.

## 🚀 Quick Installation & Usage Guide

### Installing the Desktop Application (.deb Package)

**Step 1: Download & Install**
```bash
# Install the .deb package
sudo dpkg -i universal-file-operator_1.0.1_all.deb

# Fix any dependency issues (if needed)
sudo apt-get install -f
```

**Step 2: Launch the Application**
```bash
# Method 1: Use Applications menu
# Go to Applications → Office → Universal File Operator

# Method 2: Command line launch
/opt/universal-file-operator/launch.sh

# Method 3: Service management (Recommended)
/opt/universal-file-operator/service.sh start
```

**Step 3: Stop the Application**
```bash
# Simple stop
/opt/universal-file-operator/stop.sh

# Or using service management
/opt/universal-file-operator/service.sh stop

# Check status
/opt/universal-file-operator/service.sh status

# Restart if needed
/opt/universal-file-operator/service.sh restart
```

**Step 4: Uninstall (if needed)**
```bash
# Stop the application first
/opt/universal-file-operator/service.sh stop

# Remove the package
sudo dpkg -r universal-file-operator

# Remove remaining files
sudo rm -rf /opt/universal-file-operator
```

### 🎯 Essential Commands Summary

| Action | Command |
|--------|---------|
| **Install** | `sudo dpkg -i universal-file-operator_1.0.1_all.deb` |
| **Start** | `/opt/universal-file-operator/service.sh start` |
| **Stop** | `/opt/universal-file-operator/service.sh stop` |
| **Status** | `/opt/universal-file-operator/service.sh status` |
| **Restart** | `/opt/universal-file-operator/service.sh restart` |
| **Uninstall** | `sudo dpkg -r universal-file-operator` |

## Installation Options

### Option 1: Ubuntu 24 Desktop Package (Recommended for Teams)

**For easy distribution to team members on Ubuntu 24:**

```bash
# Download the .deb package and install script
# Then run the team installer:
./install-for-team.sh
```

**Manual installation:**
```bash
sudo dpkg -i universal-file-operator_1.0.1_all.deb
sudo apt-get install -f  # Fix any dependency issues
```

**Usage after installation:**
- Open **Applications** → **Office** → **Universal File Operator**
- Or run: `/opt/universal-file-operator/launch.sh`
- The app will automatically open in your web browser

### Option 2: Development Setup

**For developers and custom installations:**

```bash
git clone https://github.com/KMjanith/BINARY_BASE64_converter.git
cd BINARY_BASE64_converter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Features

### Core Capabilities

#### **📄 PDF Operations**
- **PDF Merging**: Combine multiple PDFs with drag-and-drop reordering
- **Preview Mode**: See complete merged document before finalizing
- **Zoom Controls**: Adjust preview size (20%-200%)
- **Auto-Reordering**: Alphabetical, size-based, or custom ordering

#### **📊 Text Comparison**
- **Side-by-side comparison**: Compare two texts with visual highlighting
- **Similarity percentage**: Calculate and display accuracy percentage
- **Difference highlighting**: Visual indicators for added, deleted, and modified content
- **Statistics**: Word count, character count, and line count for both texts
- **File support**: Drag and drop text files (.txt, .md, .csv, .json, .xml, .html, .py, .js, etc.)
- **Multiple input methods**: Type/paste text or drag files for automatic content loading

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
- **Desktop Integration**: Ubuntu .deb package with applications menu entry

## Quick Start

### Using the Ubuntu Package (Recommended)

1. **Install the package:**
   ```bash
   sudo dpkg -i universal-file-operator_1.0.0_all.deb
   ```

2. **Launch the application:**
   - Open **Applications** → **Office** → **Universal File Operator**
   - Or run: `/opt/universal-file-operator/launch.sh`

3. **Use the features:**
   - **File Converter**: Convert between 70+ formats
   - **PDF Merger**: Combine and reorder PDFs with live preview

### Development Setup

### Development Setup

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

## Team Distribution

### For Ubuntu 24 Teams

1. **Build the package** (if needed):
   ```bash
   dpkg-deb --build debian-package universal-file-operator_1.0.0_all.deb
   ```

2. **Share with team**:
   - Send them `universal-file-operator_1.0.0_all.deb` and `install-for-team.sh`
   - Team runs: `./install-for-team.sh`

3. **Features for teams**:
   - Professional desktop integration
   - Automatic dependency management
   - Easy uninstallation: `sudo dpkg -r universal-file-operator`
   - Logs available at: `~/.universal-file-operator.log`

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

## Uninstallation

### Uninstalling the Ubuntu Package

If you installed using the .deb package and want to remove it:

**Step 1: Stop the Application First**
```bash
# Stop the running application
/opt/universal-file-operator/service.sh stop

# Or use the simple stop script
/opt/universal-file-operator/stop.sh
```

**Step 2: Standard Uninstall**
```bash
# Remove the package
sudo dpkg -r universal-file-operator

# Remove remaining installation files
sudo rm -rf /opt/universal-file-operator
```

**Complete Purge (Alternative):**
```bash
# Stop application first
/opt/universal-file-operator/service.sh stop

# Completely remove package and all config files
sudo dpkg -P universal-file-operator
```

**Using apt (Alternative):**
```bash
# If installed via apt
sudo apt remove universal-file-operator
```

**Verify Removal:**
```bash
# Check if package is removed
dpkg -l | grep universal-file-operator

# Check if directories are gone
ls /opt/ | grep universal-file-operator
```

### Uninstalling Development Setup

For development installations:

```bash
# Deactivate virtual environment
deactivate

# Remove the project directory
cd ..
rm -rf BINARY_BASE64_converter
```

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