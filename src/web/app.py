"""
Web Interface for Universal File Operator
===========================================

A simple Flask web application with dropdown selection for formats.
No complex bidirectional logic - just simple, explicit conversions.

Learning Concepts:
- Flask web framework basics
- HTML forms and dropdowns
- Form validation and error handling
- AJAX for dynamic updates (future enhancement)
"""

from flask import Flask, render_template, request, jsonify, flash, send_file, Response
from flask_cors import CORS
import sys
import os
import base64
import io
import tempfile
from datetime import datetime

# Add the project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from src.converters.registry import ConversionRegistry
from src.utils.exceptions import ConversionError, ValidationError, UnsupportedFormatError
from src.cli.main import convert, list_conversions
from src.converters.text_compare import compare_texts

# Import PDF processing libraries
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Enable CORS for React integration
CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])

# Initialize the converter registry
registry = ConversionRegistry()


# Categorized formats for grouped dropdowns
AVAILABLE_FORMAT_CATEGORIES = [
    ("Text & Encoding", [
        ('text', '📝 Plain Text'),
        ('binary', '🔢 Binary Data (e.g., 0011001100)'),
        ('base64', '🔤 Base64 Encoded'),
        ('hex', '🔣 Hexadecimal'),
        ('url_encoded', '🌐 URL Encoded'),
        ('html_encoded', '📄 HTML Encoded'),
    ]),
    ("Data Formats", [
        ('json', '📋 JSON String'),
        ('dict', '🐍 Python Dictionary'),
        ('csv', '📊 CSV Data'),
        ('yaml', '📄 YAML Data'),
    ]),
    ("Number Conversions", [
        ('decimal', '🔢 Decimal Number'),
        ('binary_num', '🔢 Binary Number'),
        ('hex_num', '🔢 Hexadecimal Number'),
        ('octal', '🔢 Octal Number'),
    ]),
    ("Hash Functions", [
        ('md5', '🔐 MD5 Hash'),
        ('sha1', '🔐 SHA1 Hash'),
        ('sha256', '🔐 SHA256 Hash'),
        ('sha512', '🔐 SHA512 Hash'),
    ]),
    ("Image Conversions", [
        ('jpeg', '📸 JPEG Image'),
        ('png', '🖼️ PNG Image'),
        ('gif', '🎞️ GIF Image'),
        ('bmp', '🖼️ BMP Image'),
        ('tiff', '📷 TIFF Image'),
        ('webp', '🌐 WebP Image'),
        ('ico', '⚡ ICO Icon'),
        ('image', '🖼️ Generic Image'),
    ]),
]

@app.route('/')
def landing():
    """Landing page with operation selection."""
    return render_template('landing.html')

@app.route('/converter')
def converter():
    """File converter page."""
    return render_template('converter.html', format_categories=AVAILABLE_FORMAT_CATEGORIES)

@app.route('/pdf-merge')
def pdf_merge():
    """PDF merge page."""
    if not PDF_AVAILABLE:
        flash('PDF functionality is not available. Please install PyPDF2: pip install PyPDF2')
    return render_template('pdf_merge.html')

@app.route('/text-compare')
def text_compare():
    """Text comparison page."""
    return render_template('text_compare.html')

@app.route('/compare-texts', methods=['POST'])
def compare_texts_api():
    """Handle text comparison requests."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        text1 = data.get('text1', '').strip()
        text2 = data.get('text2', '').strip()
        
        if not text1 or not text2:
            return jsonify({
                'success': False,
                'error': 'Both text fields are required'
            }), 400
        
        # Compare the texts
        result = compare_texts(text1, text2)
        
        return jsonify({
            'success': True,
            **result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/convert', methods=['POST'])
def convert_data():
    """Handle conversion requests."""
    try:
        # Get form data
        from_format = request.form.get('from_format')
        to_format = request.form.get('to_format')
        
        # Validation
        if not from_format or not to_format:
            return jsonify({
                'success': False,
                'error': 'Please select both source and target formats'
            })
        
        if from_format == to_format:
            return jsonify({
                'success': False,
                'error': 'Source and target formats cannot be the same'
            })
        
        # Handle different input types
        image_formats = ['jpeg', 'jpg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'ico', 'image']
        
        if from_format in image_formats:
            # Handle file upload
            if 'file_input' not in request.files:
                return jsonify({
                    'success': False,
                    'error': 'No file uploaded'
                })
            
            file = request.files['file_input']
            if file.filename == '':
                return jsonify({
                    'success': False,
                    'error': 'No file selected'
                })
            
            # Read file content as bytes
            input_data = file.read()
            if not input_data:
                return jsonify({
                    'success': False,
                    'error': 'File is empty'
                })
        else:
            # Handle text input
            input_data = request.form.get('input_data', '').strip()
            if not input_data:
                return jsonify({
                    'success': False,
                    'error': 'Please enter some data to convert'
                })
        
        # Special case: hex to binary (01 string)
        if from_format == 'hex' and to_format == 'binary':
            # Use the new binary_01 converter
            result = convert(input_data, 'hex', 'binary_01')
            # Mark for string display
            result_type = 'binary (01 string)'
            result_display = result
            return jsonify({
                'success': True,
                'result': result_display,
                'result_type': result_type,
                'conversion': f"{from_format} → {to_format}"
            })
        # Perform conversion
        result = convert(input_data, from_format, to_format)
        
        # Debug logging
        print(f"DEBUG: Conversion {from_format} -> {to_format}")
        print(f"DEBUG: Result type: {type(result)}")
        print(f"DEBUG: Result is bytes: {isinstance(result, bytes)}")
        if isinstance(result, bytes):
            print(f"DEBUG: Result length: {len(result)} bytes")
        
        # Handle different result types
        image_formats = ['jpeg', 'jpg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'ico', 'image']
        
        print(f"DEBUG: to_format.lower(): '{to_format.lower()}'")
        print(f"DEBUG: Is image format: {to_format.lower() in image_formats}")
        
        # Check if result is base64 image string
        is_base64_image = False
        if isinstance(result, str) and to_format.lower() in image_formats:
            try:
                # Verify it's valid base64
                decoded = base64.b64decode(result)
                is_base64_image = True
                print(f"DEBUG: Found base64 image string, decoded size: {len(decoded)} bytes")
            except:
                print(f"DEBUG: Result is string but not valid base64")
        
        if isinstance(result, bytes):
            if to_format.lower() in image_formats:
                # For image results, provide base64 data URL for display
                result_base64 = base64.b64encode(result).decode('utf-8')
                
                # Determine MIME type
                mime_type_map = {
                    'jpeg': 'image/jpeg',
                    'jpg': 'image/jpeg',
                    'png': 'image/png',
                    'gif': 'image/gif',
                    'bmp': 'image/bmp',
                    'tiff': 'image/tiff',
                    'webp': 'image/webp',
                    'ico': 'image/x-icon',
                    'image': 'image/png'  # Default fallback
                }
                mime_type = mime_type_map.get(to_format.lower(), 'image/png')
                
                data_url = f"data:{mime_type};base64,{result_base64}"
                
                return jsonify({
                    'success': True,
                    'result': result_base64,
                    'result_type': 'image',
                    'data_url': data_url,
                    'mime_type': mime_type,
                    'size': len(result),
                    'conversion': f"{from_format} → {to_format}"
                })
            else:
                # For other binary results, show hex representation
                result_display = result.hex()
                result_type = 'binary (shown as hex)'
        elif is_base64_image:
            # Handle base64 encoded image strings (from image-to-image converters)
            mime_type_map = {
                'jpeg': 'image/jpeg',
                'jpg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
                'bmp': 'image/bmp',
                'tiff': 'image/tiff',
                'webp': 'image/webp',
                'ico': 'image/x-icon',
                'image': 'image/png'  # Default fallback
            }
            mime_type = mime_type_map.get(to_format.lower(), 'image/png')
            
            data_url = f"data:{mime_type};base64,{result}"
            
            return jsonify({
                'success': True,
                'result': result,
                'result_type': 'image',
                'data_url': data_url,
                'mime_type': mime_type,
                'size': len(base64.b64decode(result)),
                'conversion': f"{from_format} → {to_format}"
            })
        elif isinstance(result, dict):
            import json
            result_display = json.dumps(result, indent=2, ensure_ascii=False)
            result_type = 'dictionary'
        else:
            result_display = str(result)
            result_type = 'string'
        
        return jsonify({
            'success': True,
            'result': result_display,
            'result_type': result_type,
            'conversion': f"{from_format} → {to_format}"
        })
        
    except UnsupportedFormatError as e:
        return jsonify({
            'success': False,
            'error': f'Conversion not supported: {str(e)}'
        })
    
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': f'Validation error: {str(e)}'
        })
    
    except ConversionError as e:
        return jsonify({
            'success': False,
            'error': f'Conversion error: {str(e)}'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        })

@app.route('/download_image', methods=['POST'])
def download_image():
    """Handle image conversion and return the image file directly for download."""
    try:
        # Get form data
        from_format = request.form.get('from_format')
        to_format = request.form.get('to_format')
        
        # Validation
        if not from_format or not to_format:
            return "Missing format parameters", 400
        
        # Handle different input types
        image_formats = ['jpeg', 'jpg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'ico', 'image']
        
        if from_format in image_formats:
            # Handle file upload
            if 'file_input' not in request.files:
                return "No file uploaded", 400
            
            file = request.files['file_input']
            if file.filename == '':
                return "No file selected", 400
            
            # Read file content as bytes
            input_data = file.read()
            if not input_data:
                return "File is empty", 400
        else:
            # Handle text input
            input_data = request.form.get('input_data', '').strip()
            if not input_data:
                return "No input data", 400
        
        # Perform conversion
        result = convert(input_data, from_format, to_format)
        
        # Handle image results
        if to_format.lower() in image_formats:
            mime_type_map = {
                'jpeg': 'image/jpeg',
                'jpg': 'image/jpeg', 
                'png': 'image/png',
                'gif': 'image/gif',
                'bmp': 'image/bmp',
                'tiff': 'image/tiff',
                'webp': 'image/webp',
                'ico': 'image/x-icon',
                'image': 'image/png'
            }
            mime_type = mime_type_map.get(to_format.lower(), 'image/png')
            
            if isinstance(result, bytes):
                # Binary result - use directly
                image_data = result
            elif isinstance(result, str):
                # Base64 result - decode it
                try:
                    image_data = base64.b64decode(result)
                except:
                    return "Invalid base64 image data", 500
            else:
                return "Invalid conversion result type", 500
            
            response = send_file(
                io.BytesIO(image_data),
                mimetype=mime_type,
                as_attachment=True,
                download_name=f'converted_image.{to_format.lower()}'
            )
            return response
        else:
            return "Invalid conversion result", 500
            
    except Exception as e:
        return f"Conversion error: {str(e)}", 500

@app.route('/api/formats')
def get_formats():
    """API endpoint to get available formats."""
    return jsonify({
        'formats': AVAILABLE_FORMATS
    })

@app.route('/api/conversions')
def get_conversions():
    """API endpoint to get all available conversions."""
    try:
        conversions = list_conversions()
        return jsonify({
            'success': True,
            'conversions': conversions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/merge-pdf', methods=['POST'])
def merge_pdf():
    """Handle PDF merge requests."""
    if not PDF_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'PDF functionality is not available. Please install PyPDF2: pip install PyPDF2'
        }), 400

    try:
        # Get uploaded files
        uploaded_files = []
        output_filename = request.form.get('output_filename', 'merged-document.pdf')
        
        # Collect all PDF files from the request
        for key in sorted(request.files.keys()):  # Sort to maintain order
            if key.startswith('pdf_'):
                file = request.files[key]
                if file and file.filename and file.filename.endswith('.pdf'):
                    uploaded_files.append(file)
                elif file and file.filename:
                    return jsonify({
                        'success': False,
                        'error': f'File "{file.filename}" is not a PDF file'
                    }), 400
        
        if len(uploaded_files) < 2:
            return jsonify({
                'success': False,
                'error': 'At least 2 PDF files are required for merging'
            }), 400
        
        # Create a PDF merger
        pdf_merger = PyPDF2.PdfMerger()
        
        try:
            # Add each PDF file to the merger
            for i, uploaded_file in enumerate(uploaded_files):
                try:
                    # Reset file pointer
                    uploaded_file.seek(0)
                    # Validate that it's a proper PDF
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    if len(pdf_reader.pages) == 0:
                        return jsonify({
                            'success': False,
                            'error': f'File "{uploaded_file.filename}" appears to be an empty or corrupted PDF'
                        }), 400
                    
                    # Reset again and append to merger
                    uploaded_file.seek(0)
                    pdf_merger.append(uploaded_file)
                    
                except Exception as file_error:
                    pdf_merger.close()
                    return jsonify({
                        'success': False,
                        'error': f'Error processing file "{uploaded_file.filename}": {str(file_error)}'
                    }), 400
            
            # Create output buffer
            output_buffer = io.BytesIO()
            pdf_merger.write(output_buffer)
            pdf_merger.close()
            
            # Prepare the response
            output_buffer.seek(0)
            
            # Ensure the filename ends with .pdf
            if not output_filename.endswith('.pdf'):
                output_filename += '.pdf'
            
            return send_file(
                output_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=output_filename
            )
        
        except Exception as merge_error:
            try:
                pdf_merger.close()
            except:
                pass
            return jsonify({
                'success': False,
                'error': f'Failed to merge PDFs: {str(merge_error)}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Import converters to register them
    from src.converters import simple_converters
    
    print("🌐 Starting Universal File Operator Web Interface")
    print("📋 Available conversions:")
    
    try:
        conversions = list_conversions()
        for conv in conversions[:10]:  # Show first 10
            print(f"   {conv['from']} → {conv['to']}")
        if len(conversions) > 10:
            print(f"   ... and {len(conversions) - 10} more")
    except Exception as e:
        print(f"   Error loading conversions: {e}")
    
    print("\n🚀 Web interface available at: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)