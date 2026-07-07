"""
Sherlock API - Main entry point
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200

@app.route('/api/documents', methods=['POST'])
def upload_document():
    """Upload a case file to the knowledge base"""
    # TODO: Implement document upload
    return jsonify({"message": "TODO"}), 501

@app.route('/api/query', methods=['POST'])
def query():
    """Ask a question about case files"""
    # TODO: Implement query endpoint
    return jsonify({"message": "TODO"}), 501

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
