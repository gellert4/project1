"""
Sherlock API - Main entry point
"""
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import os
from rag.document_handler import DocumentHandler
from config import Config

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload

# Initialize document handler
doc_handler = DocumentHandler()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200

@app.route('/api/documents', methods=['POST'])
def upload_document():
    """Upload a case file to the knowledge base"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Validate file type
    if not (file.filename.endswith('.pdf') or file.filename.endswith('.txt')):
        return jsonify({"error": "Only PDF and TXT files allowed"}), 400
    
    try:
        filename = secure_filename(file.filename)
        file_content = file.read()
        result = doc_handler.add_document(filename, file_content)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/documents', methods=['GET'])
def list_documents():
    """Get list of uploaded documents"""
    docs = doc_handler.list_documents()
    return jsonify({"documents": docs}), 200

@app.route('/api/query', methods=['POST'])
def query():
    """Ask a question about case files"""
    # TODO: Implement query endpoint
    return jsonify({"message": "TODO"}), 501

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File too large"}), 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
