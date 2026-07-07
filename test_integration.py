"""
Integration tests for Sherlock API
"""
import pytest
import json
import os
import sys
from io import BytesIO

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.main import app


@pytest.fixture
def client():
    """Create Flask test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_case_file():
    """Create a sample case file for testing"""
    content = b"""
    CASE #001
    
    Witness Interview - Mrs. Hudson:
    Q: Where were you at midnight?
    A: I was in my room reading.
    
    Interview - The Butler:
    Q: Did you see anything?
    A: Nothing unusual. I was asleep.
    """
    return ('test_case.txt', BytesIO(content))


class TestDocumentUpload:
    """Test document upload functionality"""
    
    def test_upload_text_file(self, client, sample_case_file):
        """Test uploading a TXT file"""
        filename, content = sample_case_file
        
        response = client.post(
            '/api/documents',
            data={'file': (content, filename)},
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        assert 'success' in response.json
        assert response.json['success'] is True
        assert response.json['filename'] == filename
        assert 'chunks' in response.json
        assert response.json['chunks'] > 0
    
    def test_list_after_upload(self, client, sample_case_file):
        """Test listing documents after upload"""
        filename, content = sample_case_file
        
        # Upload
        client.post(
            '/api/documents',
            data={'file': (content, filename)},
            content_type='multipart/form-data'
        )
        
        # List
        response = client.get('/api/documents')
        assert response.status_code == 200
        assert 'documents' in response.json
        assert len(response.json['documents']) > 0


class TestQuery:
    """Test query functionality"""
    
    def test_query_with_context(self, client, sample_case_file):
        """Test querying with uploaded document"""
        filename, content = sample_case_file
        
        # Upload file
        client.post(
            '/api/documents',
            data={'file': (content, filename)},
            content_type='multipart/form-data'
        )
        
        # Query
        response = client.post(
            '/api/query',
            data=json.dumps({'question': 'What was Mrs. Hudson doing at midnight?'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert 'answer' in response.json
        assert 'sources' in response.json
        assert 'confidence' in response.json
        
        # Answer should reference the context
        assert len(response.json['answer']) > 0
        assert len(response.json['sources']) > 0


class TestCORSHeaders:
    """Test CORS functionality"""
    
    def test_cors_headers_on_query(self, client):
        """Test CORS headers are present"""
        response = client.post(
            '/api/query',
            data=json.dumps({'question': 'test'}),
            content_type='application/json'
        )
        
        assert 'Access-Control-Allow-Origin' in response.headers
        assert 'Access-Control-Allow-Methods' in response.headers
    
    def test_options_request(self, client):
        """Test OPTIONS preflight request"""
        response = client.options('/api/query')
        assert response.status_code == 204


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
