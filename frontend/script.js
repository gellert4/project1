/**
 * Sherlock Frontend - Case File Assistant
 */

const API_BASE = 'http://localhost:5000/api';

// Upload functionality
document.getElementById('uploadBtn').addEventListener('click', uploadFile);
document.getElementById('queryBtn').addEventListener('click', askQuestion);

async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(`${API_BASE}/documents`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        document.getElementById('uploadStatus').textContent = 
            response.ok ? `✓ ${file.name} uploaded!` : `✗ Upload failed`;
        
        if (response.ok) {
            loadDocuments();
        }
    } catch (error) {
        document.getElementById('uploadStatus').textContent = `✗ Error: ${error.message}`;
    }
}

async function askQuestion() {
    const question = document.getElementById('questionInput').value;
    
    if (!question.trim()) {
        alert('Please enter a question');
        return;
    }
    
    const answerDiv = document.getElementById('answer');
    answerDiv.textContent = 'Searching evidence... 🔍';
    
    try {
        const response = await fetch(`${API_BASE}/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: question })
        });
        
        const result = await response.json();
        answerDiv.textContent = result.answer || 'No answer found';
    } catch (error) {
        answerDiv.textContent = `Error: ${error.message}`;
    }
}

async function loadDocuments() {
    try {
        const response = await fetch(`${API_BASE}/documents`);
        const result = await response.json();
        
        const list = document.getElementById('documentsList');
        list.innerHTML = result.documents ? 
            result.documents.map(doc => `<li>${doc}</li>`).join('') :
            '<li>No documents yet</li>';
    } catch (error) {
        console.error('Error loading documents:', error);
    }
}

// Load documents on page load
document.addEventListener('DOMContentLoaded', loadDocuments);
