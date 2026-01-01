# Universal File Operator - Changelog

## Version 1.0.3 (January 1, 2026)

### 🆕 New Features
- **Text Comparison Tool**: Complete side-by-side text comparison functionality
  - Visual difference highlighting with color-coded changes
  - Real-time similarity percentage calculation
  - Comprehensive statistics (word count, character count, line count)
  - Support for multiple file formats (.txt, .md, .csv, .json, .xml, .html, .py, .js, etc.)
  - Drag & drop file support for automatic content loading
  - Dual input methods: Type/paste text or drag files
  - Responsive split-screen interface
  - File size validation (up to 5MB)
  - Error handling and user feedback

### 🔧 Technical Improvements
- Added `text_compare.py` module with advanced difflib-based comparison algorithms
- Enhanced Flask application with new `/text-compare` and `/compare-texts` API endpoints
- Updated landing page with new text comparison card
- Comprehensive test suite with edge case coverage
- HTML highlighting system for visual difference representation

### 📦 Package Updates
- Updated debian package to version 1.0.3
- Enhanced package description to include text comparison features
- Package size optimized for new functionality
- Updated documentation and README

### 🧪 Testing
- Created comprehensive test suite (`test_text_compare_comprehensive.py`)
- Added sample text files for testing drag & drop functionality
- All 5/5 core functionality tests passing
- Package verification script included

### 📚 Documentation
- Updated README.md with text comparison feature documentation
- Added installation and usage instructions
- Created changelog for version tracking

---

## Version 1.0.2 (Previous)
- PDF merging capabilities
- Enhanced web interface
- Image conversion improvements

## Version 1.0.0 (Initial Release)
- Core conversion functionality
- CLI and web interfaces
- Basic file operations