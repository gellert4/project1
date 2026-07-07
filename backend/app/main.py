"""
Sherlock API - Main entry point
"""
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import os
import sys
from rag.document_handler import DocumentHandler
from rag.query_engine import QueryEngine
from config import Config

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload

# Initialize handlers
doc_handler = DocumentHandler()
query_engine = QueryEngine(doc_handler.get_vector_store())

def add_cors_headers(response):
    """Add CORS headers to all responses"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.after_request
def after_request(response):
    return add_cors_headers(response)

@app.route('/health', methods=['GET', 'OPTIONS'])
def health():
    """Health check endpoint"""
    if request.method == 'OPTIONS':
        return '', 204
    return jsonify({"status": "ok", "version": "1.0.0"}), 200

@app.route('/api/documents', methods=['POST', 'OPTIONS'])
def upload_document():
    """Upload a case file to the knowledge base"""
    if request.method == 'OPTIONS':
        return '', 204
    
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
            # Update query engine with new vector store
            query_engine.vector_store = doc_handler.get_vector_store()
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    
    except Exception as e:
        app.logger.error(f"Upload error: {str(e)}")
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@app.route('/api/documents', methods=['GET', 'OPTIONS'])
def list_documents():
    """Get list of uploaded documents"""
    if request.method == 'OPTIONS':
        return '', 204
    
    docs = doc_handler.list_documents()
    return jsonify({"documents": docs, "count": len(docs)}), 200

@app.route('/api/query', methods=['POST', 'OPTIONS'])
def query():
    """Ask a question about case files"""
    if request.method == 'OPTIONS':
        return '', 204
    
    data = request.get_json()
    
    if not data or 'question' not in data:
        return jsonify({"error": "No question provided"}), 400
    
    question = data['question'].strip()
    
    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400
    
    try:
        result = query_engine.query(question)
        return jsonify(result), 200
    except Exception as e:
        app.logger.error(f"Query error: {str(e)}")
        return jsonify({"error": f"Query failed: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File too large (max 50MB)"}), 413

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Check for API key in development
    if Config.FLASK_ENV == 'development' and not Config.GOOGLE_API_KEY:
        print("⚠️  Warning: GOOGLE_API_KEY not set. LLM queries will use fallback mode.")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
