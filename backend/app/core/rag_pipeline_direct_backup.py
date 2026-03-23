"""
Simplified RAG Pipeline with Direct Groq API Calls
No LangChain Groq dependency issues
"""

import os
import requests
import logging
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
import json

# Stable LangChain imports (these work)
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.schema import Document

from ..config import settings

logger = logging.getLogger(__name__)

class DirectGroqRAGPipeline:
    """RAG Pipeline using direct Groq API calls (no LangChain Groq dependency)"""
    
    def __init__(self):
        logger.info("Initializing Direct Groq RAG Pipeline...")
        
        # Initialize embeddings (works locally)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        logger.info("✅ Embeddings initialized")
        
        # Initialize FAISS vector store
        self.vector_store = None
        self.persist_directory = "./faiss_index"
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Groq API settings
        self.groq_api_key = settings.GROQ_API_KEY
        self.groq_model = getattr(settings, 'GROQ_MODEL', 'llama-3.3-70b-versatile')
        
        if self.groq_api_key:
            logger.info(f"✅ Groq API configured with model: {self.groq_model}")
        else:
            logger.warning("⚠️ No Groq API key found")
        
        logger.info("✅ Direct Groq RAG Pipeline initialized")
    
    def _call_groq_api(self, prompt: str) -> str:
        """Direct call to Groq API"""
        if not self.groq_api_key:
            return "Groq API not configured. Please add GROQ_API_KEY to .env"
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.groq_model,
            "messages": [
                {"role": "system", "content": "You are NetOne's AI customer service assistant. Be helpful, concise, and professional."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "max_tokens": 500
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            logger.error(f"Groq API error: {e}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            return f"I'm having trouble connecting to my AI service. Please try again later. (Error: {str(e)})"
    
    def ingest_document(self, file_path: str, metadata: Dict[str, Any]) -> Tuple[bool, int]:
        """Ingest document into FAISS"""
        try:
            logger.info(f"📄 Ingesting document: {file_path}")
            
            # Load document
            loader = TextLoader(file_path, encoding='utf-8')
            documents = loader.load()
            
            # Split into chunks
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Split into {len(chunks)} chunks")
            
            # Add metadata
            for i, chunk in enumerate(chunks):
                chunk.metadata.update({
                    **metadata,
                    "chunk_id": i,
                    "ingested_at": datetime.now().isoformat()
                })
            
            # Create or update FAISS index
            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(chunks, self.embeddings)
                logger.info("Created new FAISS index")
            else:
                self.vector_store.add_documents(chunks)
                logger.info("Added to existing FAISS index")
            
            # Save to disk
            self.vector_store.save_local(self.persist_directory)
            logger.info(f"✅ Saved to {self.persist_directory}")
            
            return True, len(chunks)
            
        except Exception as e:
            logger.error(f"❌ Error ingesting document: {e}")
            return False, 0
    
    def generate_response(self, query: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """Generate response using RAG with direct Groq API"""
        try:
            logger.info(f"💬 Generating response for: {query[:50]}...")
            
            # Load or use vector store
            if self.vector_store is None:
                # Try to load existing index
                index_path = os.path.join(self.persist_directory, "index.faiss")
                if os.path.exists(index_path):
                    self.vector_store = FAISS.load_local(
                        self.persist_directory,
                        self.embeddings
                    )
                    logger.info("Loaded existing FAISS index")
                else:
                    return {
                        "answer": "No documents have been ingested yet. Please add documents first using the admin interface.",
                        "sources": []
                    }
            
            # Search for relevant documents
            docs_with_scores = self.vector_store.similarity_search_with_score(query, k=5)
            
            if not docs_with_scores:
                # No relevant documents found, still try to answer with general knowledge
                prompt = f"""The user asked: "{query}"

As NetOne's AI assistant, please provide a helpful response. If this is about specific services or plans, note that you don't have specific documentation loaded yet, but provide general guidance."""
                
                answer = self._call_groq_api(prompt)
                return {
                    "answer": answer,
                    "sources": []
                }
            
            # Format context from documents
            context_parts = []
            sources = []
            seen_titles = set()
            
            for doc, score in docs_with_scores:
                # Add to context
                context_parts.append(f"[Source: {doc.metadata.get('title', 'Unknown')}]\n{doc.page_content}")
                
                # Add to sources list
                title = doc.metadata.get('title', 'Unknown')
                if title not in seen_titles:
                    sources.append({
                        "title": title,
                        "category": doc.metadata.get('category', 'general'),
                        "relevance": f"{score:.2f}",
                        "excerpt": doc.page_content[:150] + "..."
                    })
                    seen_titles.add(title)
            
            context = "\n\n".join(context_parts)
            
            # Prepare prompt for Groq
            prompt = f"""Based on the following information from NetOne's knowledge base, please answer the customer's question.

Context information:
{context}

Customer question: {query}

Please provide a helpful, accurate answer based ONLY on the context provided. If the answer isn't in the context, say so politely."""

            # Get answer from Groq
            answer = self._call_groq_api(prompt)
            
            return {
                "answer": answer,
                "sources": sources
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            return {
                "answer": f"I apologize, but I encountered an error. Please try again later. (Error: {str(e)})",
                "sources": []
            }
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        try:
            if self.vector_store is not None:
                count = self.vector_store.index.ntotal
            else:
                # Try to get count from saved index
                index_path = os.path.join(self.persist_directory, "index.faiss")
                if os.path.exists(index_path):
                    import faiss
                    index = faiss.read_index(index_path)
                    count = index.ntotal
                else:
                    count = 0
            
            return {
                "total_documents": count,
                "vector_store": "FAISS",
                "groq_model": self.groq_model,
                "groq_configured": self.groq_api_key is not None
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"total_documents": 0, "error": str(e)}

# Create singleton instance
rag_pipeline = DirectGroqRAGPipeline()
