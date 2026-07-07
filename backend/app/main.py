"""
Sherlock API - Main entry point
"""
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import os
from rag.document_handler import DocumentHandler
from rag.query_engine import QueryEngine
from config import Config

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload

# Initialize handlers
doc_handler = DocumentHandler()
query_engine = QueryEngine(doc_handler.get_vector_store())

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
            # Update query engine with new vector store
            query_engine.vector_store = doc_handler.get_vector_store()
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
        return jsonify({"error": str(e)}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File too large"}), 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
