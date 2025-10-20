#!/usr/bin/env python3

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/simple_test', methods=['POST'])
def simple_test():
    try:
        data = request.form.to_dict()
        return jsonify({
            'success': True,
            'received': data,
            'message': 'Simple test works!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("Starting simple Flask server on port 5002...")
    app.run(host='127.0.0.1', port=5002, debug=False)