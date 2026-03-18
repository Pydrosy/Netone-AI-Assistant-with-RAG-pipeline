"""
FAISS-based RAG Pipeline for NetOne AI Assistant
Using stable LangChain 0.0.340
"""

import os
from typing import List, Dict, Any, Optional, Tuple
import logging
from datetime import datetime
import pickle

# Stable LangChain imports
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.schema import Document as LangchainDocument
from langchain.vectorstores import FAISS
from langchain.llms import Groq  # Use older Groq import
from langchain.prompts import PromptTemplate

from ..config import settings

logger = logging.getLogger(__name__)

class NetOneRAGPipelineFAISS:
    """RAG Pipeline using FAISS with stable LangChain"""
    
    def __init__(self):
        logger.info("Initializing FAISS-based RAG Pipeline...")
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        logger.info("✅ Embeddings initialized")
        
        # Initialize vector store
        self.vector_store = None
        self.persist_directory = "./faiss_index"
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Initialize LLM (Groq)
        self.llm = self._init_llm()
        logger.info(f"✅ LLM initialized: {type(self.llm).__name__ if self.llm else 'None'}")
        
        # Custom prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are NetOne's AI customer service assistant. Answer the question based on the context provided.

Context: {context}

Question: {question}

Answer:"""
        )
        
        logger.info("✅ FAISS RAG Pipeline initialization complete!")
    
    def _init_llm(self):
        """Initialize Groq LLM with stable API"""
        try:
            if hasattr(settings, 'GROQ_API_KEY') and settings.GROQ_API_KEY:
                model_name = getattr(settings, 'GROQ_MODEL', 'llama-3.3-70b-versatile')
                logger.info(f"Using Groq with model: {model_name}")
                # Use the older Groq implementation
                return Groq(
                    groq_api_key=settings.GROQ_API_KEY,
                    model_name=model_name,
                    temperature=0.1
                )
            return None
        except Exception as e:
            logger.error(f"Error initializing LLM: {e}")
            return None
    
    def ingest_document(self, file_path: str, metadata: Dict[str, Any]) -> Tuple[bool, int]:
        """Ingest document into FAISS"""
        try:
            logger.info(f"📄 Ingesting document: {file_path}")
            
            # Load document
            loader = TextLoader(file_path, encoding='utf-8')
            documents = loader.load()
            
            # Split into chunks
            chunks = self.text_splitter.split_documents(documents)
            
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
            else:
                self.vector_store.add_documents(chunks)
            
            # Save to disk
            self.vector_store.save_local(self.persist_directory)
            
            logger.info(f"✅ Ingested {len(chunks)} chunks")
            return True, len(chunks)
            
        except Exception as e:
            logger.error(f"❌ Error ingesting document: {e}")
            return False, 0
    
    def generate_response(self, query: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Generate response using RAG"""
        try:
            logger.info(f"💬 Generating response for: {query[:50]}...")
            
            # Search for relevant documents
            if self.vector_store is None:
                # Try to load existing index
                index_path = os.path.join(self.persist_directory, "index.faiss")
                if os.path.exists(index_path):
                    self.vector_store = FAISS.load_local(
                        self.persist_directory,
                        self.embeddings
                    )
                else:
                    return {
                        "answer": "No documents have been ingested yet. Please add documents first.",
                        "sources": []
                    }
            
            # Search
            docs = self.vector_store.similarity_search_with_score(query, k=3)
            
            if not docs:
                return {
                    "answer": "I couldn't find relevant information in my knowledge base.",
                    "sources": []
                }
            
            # Format context
            context = "\n\n".join([doc.page_content for doc, _ in docs])
            
            # Format prompt
            formatted_prompt = self.prompt_template.format(
                context=context,
                question=query
            )
            
            # Generate response using LLM
            if self.llm:
                response = self.llm(formatted_prompt)  # Note: llm() not invoke() for older version
                answer = response
            else:
                answer = f"Found relevant information: {context[:200]}..."
            
            # Extract sources
            sources = []
            seen = set()
            for doc, score in docs:
                title = doc.metadata.get('title', 'Unknown')
                if title not in seen:
                    sources.append({
                        "title": title,
                        "category": doc.metadata.get('category', 'general'),
                        "relevance": f"{score:.2f}",
                        "excerpt": doc.page_content[:150] + "..."
                    })
                    seen.add(title)
            
            return {
                "answer": answer,
                "sources": sources
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            return {
                "answer": f"Error: {str(e)}",
                "sources": []
            }
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get stats about the FAISS index"""
        try:
            if self.vector_store is not None:
                count = self.vector_store.index.ntotal
            else:
                count = 0
            
            return {
                "total_documents": count,
                "vector_store": "FAISS",
                "llm": type(self.llm).__name__ if self.llm else "None"
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"total_documents": 0, "error": str(e)}

# Create singleton instance
rag_pipeline = NetOneRAGPipelineFAISS()
