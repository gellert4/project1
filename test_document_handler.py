"""
Test document handler functionality
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.rag.document_handler import DocumentHandler

def test_document_handler():
    """Test basic document handler functionality"""
    print("Testing Document Handler...")
    
    try:
        # Initialize
        handler = DocumentHandler()
        print("✓ Document handler initialized")
        
        # Create a test document
        test_content = b"""
        CASE FILE #001
        
        Interview with Mrs. Hudson:
        Q: Where were you on the night of the murder?
        A: I was at home reading a book.
        
        Interview with the Butler:
        Q: Did you see anything suspicious?
        A: Nothing, sir. I was asleep in my quarters.
        """
        
        # Test adding document
        result = handler.add_document("test_case.txt", test_content)
        print(f"✓ Document added: {result}")
        
        # Test listing documents
        docs = handler.list_documents()
        print(f"✓ Documents list: {docs}")
        
        # Check vector store
        vs = handler.get_vector_store()
        if vs is not None:
            print(f"✓ Vector store created with embeddings")
        
        print("\n✅ All tests passed!")
        return True
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_document_handler()
    sys.exit(0 if success else 1)
