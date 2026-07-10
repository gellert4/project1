/**
 * Sherlock Frontend - Case File Assistant
 */

// Works locally and through the Docker Nginx proxy.
const isLocal =
    window.location.hostname === 'localhost' ||
    window.location.hostname === '127.0.0.1';

const API_BASE = isLocal
    ? 'http://localhost:5000/api'
    : '/api';

const uploadButton = document.getElementById('uploadBtn');
const queryButton = document.getElementById('queryBtn');
const questionInput = document.getElementById('questionInput');

uploadButton.addEventListener('click', uploadFile);
queryButton.addEventListener('click', askQuestion);

// Submit the question with Enter.
// Shift + Enter still creates a new line.
questionInput.addEventListener('keydown', event => {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        askQuestion();
    }
});

async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const uploadStatus = document.getElementById('uploadStatus');
    const file = fileInput.files[0];

    if (!file) {
        uploadStatus.textContent = 'Please select a PDF or TXT file.';
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setButtonLoading(uploadButton, true, 'Uploading...');
    uploadStatus.textContent = `Uploading ${file.name}...`;

    try {
        const response = await fetch(`${API_BASE}/documents`, {
            method: 'POST',
            body: formData,
        });

        const result = await parseResponse(response);

        if (!response.ok) {
            throw new Error(result.error || 'Upload failed.');
        }

        uploadStatus.textContent =
            `${file.name} uploaded successfully ` +
            `(${result.chunks ?? 0} searchable sections).`;

        fileInput.value = '';

        await loadDocuments();
    } catch (error) {
        uploadStatus.textContent = `Upload failed: ${error.message}`;
    } finally {
        setButtonLoading(uploadButton, false, 'Upload');
    }
}

async function askQuestion() {
    const question = questionInput.value.trim();
    const answerDiv = document.getElementById('answer');

    if (!question) {
        answerDiv.textContent = 'Please enter a question.';
        return;
    }

    answerDiv.replaceChildren();
    answerDiv.textContent = 'Searching the evidence...';

    setButtonLoading(queryButton, true, 'Searching...');

    try {
        const response = await fetch(`${API_BASE}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question,
            }),
        });

        const result = await parseResponse(response);

        if (!response.ok) {
            throw new Error(result.error || 'The query failed.');
        }

        renderAnswer(
            result.answer || "I don't have enough evidence to answer that.",
            result.sources || [],
            result.confidence
        );
    } catch (error) {
        answerDiv.replaceChildren();

        const errorText = document.createElement('div');
        errorText.className = 'answer-content';
        errorText.textContent = `Error: ${error.message}`;
        errorText.style.color = '#a8473d';

        answerDiv.appendChild(errorText);
    } finally {
        setButtonLoading(queryButton, false, 'Search Evidence');
    }
}

function renderAnswer(answer, sources, confidence) {
    const answerDiv = document.getElementById('answer');
    answerDiv.replaceChildren();

    const answerContent = document.createElement('div');
    answerContent.className = 'answer-content';
    answerContent.textContent = cleanAnswer(answer);

    answerDiv.appendChild(answerContent);

    const uniqueSources = cleanSources(sources);

    if (uniqueSources.length > 0) {
        const sourcesBox = document.createElement('div');
        sourcesBox.className = 'sources-box';

        const sourceTitle = document.createElement('strong');
        sourceTitle.textContent = 'Sources';

        const sourceList = document.createElement('ul');

        uniqueSources.forEach(source => {
            const listItem = document.createElement('li');
            listItem.textContent = source;
            sourceList.appendChild(listItem);
        });

        sourcesBox.appendChild(sourceTitle);
        sourcesBox.appendChild(sourceList);
        answerDiv.appendChild(sourcesBox);
    }

    if (typeof confidence === 'number') {
        const confidenceText = document.createElement('small');
        confidenceText.textContent =
            `Retrieval confidence: ${Math.round(confidence * 100)}%`;

        confidenceText.style.display = 'block';
        confidenceText.style.marginTop = '12px';
        confidenceText.style.color = '#6d746f';

        answerDiv.appendChild(confidenceText);
    }
}

function cleanAnswer(answer) {
    return String(answer)
        .replace(/^Based on available evidence:\s*/i, '')
        .replace(/Sources?:.*$/is, '')
        .replace(
            /Evidence\s+\d+\s+\(from\s+[^)]+\):\s*/gi,
            ''
        )
        .trim();
}

function cleanSources(sources) {
    const cleanedSources = sources.map(source => {
        const normalized = String(source).replaceAll('\\', '/');
        return normalized.split('/').pop();
    });

    return [...new Set(cleanedSources)].filter(Boolean);
}

async function loadDocuments() {
    const list = document.getElementById('documentsList');

    try {
        const response = await fetch(`${API_BASE}/documents`);
        const result = await parseResponse(response);

        if (!response.ok) {
            throw new Error(result.error || 'Could not load documents.');
        }

        list.replaceChildren();

        const documents = cleanSources(result.documents || []);

        if (documents.length === 0) {
            const item = document.createElement('li');
            item.textContent = 'No documents uploaded yet';
            list.appendChild(item);
            return;
        }

        documents.forEach(documentName => {
            const item = document.createElement('li');
            item.textContent = documentName;
            list.appendChild(item);
        });
    } catch (error) {
        console.error('Error loading documents:', error);

        list.replaceChildren();

        const item = document.createElement('li');
        item.textContent = 'Documents could not be loaded';
        list.appendChild(item);
    }
}

async function parseResponse(response) {
    const contentType = response.headers.get('content-type') || '';

    if (contentType.includes('application/json')) {
        return response.json();
    }

    const text = await response.text();

    throw new Error(
        text || `The server returned HTTP ${response.status}.`
    );
}

function setButtonLoading(button, loading, label) {
    button.disabled = loading;
    button.textContent = label;
}

document.addEventListener('DOMContentLoaded', loadDocuments);