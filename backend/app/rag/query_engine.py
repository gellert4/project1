"""
Query engine for RAG - retrieves relevant documents and generates answers
"""
import os
from config import Config

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class QueryEngine:
    """RAG query engine using LLM and vector search"""
    
    def __init__(self, vector_store):
        """
        Initialize query engine
        
        Args:
            vector_store: FAISS vector store with document embeddings
        """
        self.vector_store = vector_store
        self.llm_available = False
        
        # Try to initialize Google AI
        if Config.GOOGLE_API_KEY and genai:
            genai.configure(api_key=Config.GOOGLE_API_KEY)
            self.llm_available = True
            self.model = genai.GenerativeModel('gemini-pro')
    
    def query(self, question, top_k=3):
        """
        Ask a question and get an answer based on stored documents
        
        Args:
            question: The question to ask
            top_k: Number of top relevant chunks to retrieve
            
        Returns:
            dict with 'answer', 'sources', 'confidence' keys
        """
        if not self.vector_store:
            return {
                "answer": "I don't have any case files loaded yet.",
                "sources": [],
                "confidence": 0.0
            }
        
        try:
            # Search for relevant documents
            results = self.vector_store.similarity_search(question, k=top_k)
            
            if not results:
                return {
                    "answer": "I don't have enough evidence to answer that question.",
                    "sources": [],
                    "confidence": 0.0
                }
            
            # Prepare context from retrieved documents
            context = self._prepare_context(results, question)
            
            # Generate answer using LLM
            answer = self._generate_answer(question, context)
            
            # Extract sources
            sources = list(set([doc.metadata.get('source', 'Unknown') for doc in results]))
            
            return {
                "answer": answer,
                "sources": sources,
                "confidence": 0.85
            }
        
        except Exception as e:
            return {
                "answer": f"Error processing query: {str(e)}",
                "sources": [],
                "confidence": 0.0
            }
    
    def _prepare_context(self, documents, question):
        """Prepare context from retrieved documents"""
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"Evidence {i} (from {doc.metadata.get('source', 'Unknown')}):\n{doc.page_content}")
        
        return "\n\n".join(context_parts)
    
    def _generate_answer(self, question, context):
        """Generate answer using LLM with retrieved context"""
        
        # Fallback to simple extraction if LLM unavailable
        if not self.llm_available or not genai:
            return self._extract_simple_answer(question, context)
        
        try:
            prompt = f"""You are a detective's assistant. Answer questions ONLY based on the provided evidence.

Evidence from case files:
{context}

Question: {question}

Instructions:
1. Answer ONLY using information from the evidence above
2. If the answer is not in the evidence, respond with "I don't have enough evidence to answer that."
3. Be concise and direct
4. Never make up or guess information
5. If multiple pieces of evidence are relevant, mention them

Answer:"""
            
            response = self.model.generate_content(prompt)
            answer = response.text.strip()
            
            # Validate answer doesn't hallucinate
            if not self._contains_hallucination_indicators(answer):
                return answer
            else:
                return "I don't have enough evidence to answer that question accurately."
        
        except Exception:
            return self._extract_simple_answer(question, context)
    
    def _extract_simple_answer(self, question, context):
        """Simple extraction if LLM is unavailable"""
        # Just return relevant context if no LLM available
        if context:
            return f"Based on available evidence:\n\n{context[:500]}..."
        return "I don't have enough evidence to answer that."
    
    def _contains_hallucination_indicators(self, answer):
        """Check if answer seems to be hallucinated"""
        # Check for common hallucination patterns
        indicators = [
            "presumably",
            "it's possible that",
            "could have",
            "might have",
            "unclear from the evidence"
        ]
        
        lower_answer = answer.lower()
        return any(indicator in lower_answer for indicator in indicators)
