#!/usr/bin/env python3

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
import base64
from src.cli.main import convert

app = Flask(__name__)

@app.route('/test_convert', methods=['POST'])
def test_convert():
    """Simplified test endpoint"""
    start_time = time.time()
    
    try:
        data = request.get_json() or request.form
        from_format = data.get('from_format')
        to_format = data.get('to_format')
        input_data = data.get('input_data')
        
        print(f"Converting {from_format} -> {to_format}, input length: {len(input_data) if input_data else 0}")
        
        # Perform conversion
        result = convert(input_data, from_format, to_format)
        
        conversion_time = time.time() - start_time
        print(f"Conversion completed in {conversion_time:.3f}s, result size: {len(result) if isinstance(result, bytes) else len(str(result))}")
        
        # Simple response for images
        if to_format.lower() in ['jpeg', 'png', 'gif', 'bmp'] and isinstance(result, bytes):
            result_base64 = base64.b64encode(result).decode('utf-8')
            mime_type = f'image/{to_format.lower()}'
            
            return jsonify({
                'success': True,
                'result_type': 'image',
                'data_url': f'data:{mime_type};base64,{result_base64}',
                'size': len(result),
                'conversion_time': conversion_time
            })
        else:
            return jsonify({
                'success': True,
                'result': str(result),
                'result_type': 'text',
                'conversion_time': conversion_time
            })
            
    except Exception as e:
        error_time = time.time() - start_time
        print(f"Error after {error_time:.3f}s: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'error_time': error_time
        })

if __name__ == '__main__':
    print("Starting test Flask server...")
    app.run(host='127.0.0.1', port=5001, debug=True)