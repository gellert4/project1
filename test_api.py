"""
Unit tests for Sherlock API
"""
import pytest
import json
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.main import app


@pytest.fixture
def client():
    """Create Flask test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'


def test_get_documents_empty(client):
    """Test getting documents when none uploaded"""
    response = client.get('/api/documents')
    assert response.status_code == 200
    assert 'documents' in response.json
    assert isinstance(response.json['documents'], list)


def test_upload_no_file(client):
    """Test upload without file"""
    response = client.post('/api/documents')
    assert response.status_code == 400
    assert 'error' in response.json


def test_upload_wrong_format(client):
    """Test upload with unsupported file format"""
    data = {
        'file': (b'test data', 'test.docx')
    }
    response = client.post('/api/documents', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'Only PDF and TXT files allowed' in response.json['error']


def test_query_no_question(client):
    """Test query without question"""
    response = client.post(
        '/api/query',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert 'error' in response.json


def test_query_empty_question(client):
    """Test query with empty question"""
    response = client.post(
        '/api/query',
        data=json.dumps({'question': '   '}),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert 'error' in response.json


def test_query_no_documents(client):
    """Test query when no documents uploaded"""
    response = client.post(
        '/api/query',
        data=json.dumps({'question': 'Who did it?'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert 'answer' in response.json
    assert 'case files loaded' in response.json['answer'].lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
