/**
 * Sherlock Frontend - Case File Assistant
 */

// API endpoint - works both locally and in Docker
const API_BASE = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000/api'
    : '/api';

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
    
    const uploadStatus = document.getElementById('uploadStatus');
    uploadStatus.textContent = 'Uploading...';
    
    try {
        const response = await fetch(`${API_BASE}/documents`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            uploadStatus.textContent = `✓ ${file.name} uploaded successfully (${result.chunks} chunks)`;
            fileInput.value = '';
            loadDocuments();
        } else {
            uploadStatus.textContent = `✗ Upload failed: ${result.error || 'Unknown error'}`;
        }
    } catch (error) {
        uploadStatus.textContent = `✗ Error: ${error.message}`;
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
    answerDiv.style.color = '#666';
    
    try {
        const response = await fetch(`${API_BASE}/query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: question })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // Parse answer and sources
            let answerText = result.answer || 'No answer found';
            let sources = result.sources || [];
            
            // Clean up the answer - remove "Based on available evidence:" prefix and source info
            answerText = answerText.replace(/Based on available evidence:\s*/i, '')
                                  .replace(/📚 Sources:.*$/i, '')
                                  .trim();
            
            // Extract sources from answer if needed
            const sourceMatch = answerText.match(/Evidence \d+.*?from\s+([^:]+):/g);
            if (sourceMatch) {
                sourceMatch.forEach(match => {
                    const file = match.match(/from\s+([^:]+):/)[1];
                    if (!sources.includes(file)) {
                        sources.push(file);
                    }
                });
                // Clean evidence markers from answer
                answerText = answerText.replace(/Evidence \d+.*?from [^:]+:\s*/g, '');
            }
            
            // Build formatted response
            let html = `<div class="answer-content">${answerText}</div>`;
            
            if (sources && sources.length > 0) {
                html += `<div class="sources-box">
                    <strong>📚 Sources:</strong>
                    <ul>
                        ${sources.map(s => `<li>${s}</li>`).join('')}
                    </ul>
                </div>`;
            }
            
            answerDiv.innerHTML = html;
            answerDiv.style.color = '#333';
        } else {
            answerDiv.textContent = `Error: ${result.error || 'Unknown error'}`;
            answerDiv.style.color = '#d32f2f';
        }
    } catch (error) {
        answerDiv.textContent = `Error: ${error.message}`;
        answerDiv.style.color = '#d32f2f';
    }
}

async function loadDocuments() {
    try {
        const response = await fetch(`${API_BASE}/documents`);
        const result = await response.json();
        
        const list = document.getElementById('documentsList');
        
        if (result.documents && result.documents.length > 0) {
            list.innerHTML = result.documents
                .map(doc => `<li>📄 ${doc}</li>`)
                .join('');
        } else {
            list.innerHTML = '<li>No documents uploaded yet</li>';
        }
    } catch (error) {
        console.error('Error loading documents:', error);
        document.getElementById('documentsList').innerHTML = '<li>Error loading documents</li>';
    }
}

// Load documents on page load
document.addEventListener('DOMContentLoaded', loadDocuments);
