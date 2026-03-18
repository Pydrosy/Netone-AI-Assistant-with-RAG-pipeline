import os
import pickle
from typing import List, Dict, Any, Tuple
import numpy as np
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
import logging

logger = logging.getLogger(__name__)

class FAISSVectorStore:
    """FAISS-based vector store as ChromaDB replacement"""
    
    def __init__(self, embedding_function, persist_directory="./faiss_index"):
        self.embedding_function = embedding_function
        self.persist_directory = persist_directory
        self.documents = []
        self.embeddings = []
        self.index = None
        os.makedirs(persist_directory, exist_ok=True)
        
    def add_documents(self, documents: List[Document]):
        """Add documents to the store"""
        from langchain_community.vectorstores import FAISS
        
        # Create FAISS store
        self.store = FAISS.from_documents(documents, self.embedding_function)
        self.documents.extend(documents)
        
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Search for similar documents"""
        if hasattr(self, 'store'):
            return self.store.similarity_search(query, k=k)
        return []
    
    def similarity_search_with_score(self, query: str, k: int = 4) -> List[Tuple[Document, float]]:
        """Search with relevance scores"""
        if hasattr(self, 'store'):
            return self.store.similarity_search_with_score(query, k=k)
        return []
    
    def persist(self):
        """Save the index"""
        if hasattr(self, 'store'):
            self.store.save_local(self.persist_directory)
    
    def count(self) -> int:
        """Get document count"""
        if hasattr(self, 'store'):
            return self.store.index.ntotal
        return 0
