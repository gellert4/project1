"""
Document handling for case files - extract text and create embeddings
"""
import os
from pathlib import Path
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config import Config


class DocumentHandler:
    """Handle document uploads and processing"""
    
    def __init__(self):
        """Initialize vector store and embeddings"""
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_db_path = Config.VECTOR_DB_PATH
        self.vector_store = self._load_or_create_vector_store()
        self.documents_meta = {}
        
        # Create upload directory if it doesn't exist
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(self.vector_db_path, exist_ok=True)
    
    def _load_or_create_vector_store(self):
        """Load existing vector store or create new one"""
        try:
            if os.path.exists(self.vector_db_path):
                return FAISS.load_local(self.vector_db_path, self.embeddings)
        except Exception:
            pass
        
        # Create empty vector store with a dummy document
        dummy_docs = [{"page_content": "empty", "metadata": {"source": "empty"}}]
        return None
    
    def add_document(self, filename, file_content):
        """
        Add a document to the knowledge base
        
        Args:
            filename: Name of the file (e.g., "case1.pdf")
            file_content: File content (bytes)
        """
        try:
            # Save file temporarily
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            with open(filepath, 'wb') as f:
                f.write(file_content)
            
            # Extract text based on file type
            text = self._extract_text(filepath)
            
            # Split text into chunks
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50,
                separators=["\n\n", "\n", " ", ""]
            )
            chunks = splitter.split_text(text)
            
            # Create documents with metadata
            docs = [
                {"page_content": chunk, "metadata": {"source": filename}}
                for chunk in chunks
            ]
            
            # Add to vector store
            if self.vector_store is None:
                # Create first vector store
                from langchain_community.vectorstores import FAISS
                from langchain.schema import Document
                doc_objects = [Document(page_content=d["page_content"], metadata=d["metadata"]) for d in docs]
                self.vector_store = FAISS.from_documents(doc_objects, self.embeddings)
                self.vector_store.save_local(self.vector_db_path)
            else:
                # Add to existing
                from langchain.schema import Document
                doc_objects = [Document(page_content=d["page_content"], metadata=d["metadata"]) for d in docs]
                self.vector_store.add_documents(doc_objects)
                self.vector_store.save_local(self.vector_db_path)
            
            # Track document
            self.documents_meta[filename] = {
                "chunks": len(chunks),
                "source": filepath
            }
            
            return {"success": True, "filename": filename, "chunks": len(chunks)}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _extract_text(self, filepath):
        """Extract text from PDF or TXT file"""
        if filepath.endswith('.pdf'):
            loader = PyPDFLoader(filepath)
            pages = loader.load()
            return "\n".join([page.page_content for page in pages])
        
        elif filepath.endswith('.txt'):
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        
        else:
            raise ValueError(f"Unsupported file type: {filepath}")
    
    def list_documents(self):
        """List all stored documents"""
        return list(self.documents_meta.keys())
    
    def get_vector_store(self):
        """Get the vector store for querying"""
        return self.vector_store
