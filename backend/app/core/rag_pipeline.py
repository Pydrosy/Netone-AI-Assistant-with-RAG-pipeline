"""
RAG Pipeline for NetOne AI Assistant
Handles document ingestion, retrieval, and response generation
"""

import os
from typing import List, Dict, Any, Optional, Tuple
import logging
from datetime import datetime

# LangChain imports
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, CSVLoader
from langchain.schema import Document as LangchainDocument
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory

# Local imports
from ..config import settings
from ..models.database import SessionLocal, Document, Message

# Set up logging
logger = logging.getLogger(__name__)

class NetOneRAGPipeline:
    """
    RAG Pipeline for NetOne customer service
    Handles document ingestion, retrieval, and response generation
    """
    
    def __init__(self):
        """Initialize the RAG pipeline with embeddings, vector store, and LLM"""
        logger.info("Initializing NetOne RAG Pipeline...")
        
        # Initialize embeddings
        self.embeddings = self._init_embeddings()
        logger.info(f"✅ Embeddings initialized: {type(self.embeddings).__name__}")
        
        # Initialize vector store
        self.vector_store = self._init_vector_store()
        logger.info(f"✅ Vector store initialized: {type(self.vector_store).__name__}")
        
        # Initialize LLM
        self.llm = self._init_llm()
        logger.info(f"✅ LLM initialized: {type(self.llm).__name__ if self.llm else 'None'}")
        
        # Initialize text splitter for document chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Custom prompt template for NetOne
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question", "chat_history"],
            template="""You are NetOne's AI customer service assistant. You help customers with inquiries about 
telecommunications services, billing, technical support, and general information.

**Important Guidelines:**
1. Answer ONLY based on the provided context from NetOne's official documents
2. If you don't know the answer, say "I don't have that information. Please contact our support team at support@netone.co.zm or call 1234."
3. Be helpful, professional, and concise
4. If asked about pricing or plans, provide accurate details from the context
5. For technical issues, suggest troubleshooting steps from the documentation

**Previous conversation:**
{chat_history}

**Context from NetOne documents:**
{context}

**Customer question:** {question}

**Your response:**"""
        )
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        logger.info("✅ RAG Pipeline initialization complete!")
    
    def _init_embeddings(self):
        """Initialize embeddings based on configuration"""
        if settings.USE_LOCAL_LLM:
            logger.info("Using local HuggingFace embeddings")
            return HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
        else:
            logger.info("Using OpenAI embeddings")
            return OpenAIEmbeddings(
                openai_api_key=settings.OPENAI_API_KEY,
                model="text-embedding-3-small"
            )
    
    def _init_vector_store(self):
        """Initialize ChromaDB vector store"""
        persist_directory = settings.VECTOR_DB_PATH
        
        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize Chroma
        return Chroma(
            collection_name=settings.COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )
    
def _init_llm(self):
    """Initialize LLM based on configuration"""
    try:
        if settings.USE_LOCAL_LLM:
            logger.info("Using local mode (no LLM)")
            return None
        
        # Try Groq first
        if hasattr(settings, 'GROQ_API_KEY') and settings.GROQ_API_KEY:
            try:
                from langchain_groq import ChatGroq
                model_name = getattr(settings, 'GROQ_MODEL', 'llama-3.3-70b-versatile')
                logger.info(f"✅ Using Groq LLM with model: {model_name}")
                return ChatGroq(
                    groq_api_key=settings.GROQ_API_KEY,
                    model_name=model_name,
                    temperature=0.1,
                    streaming=True
                )
            except ImportError:
                logger.warning("langchain-groq not installed, trying legacy Groq")
                try:
                    from langchain.llms import Groq
                    model_name = getattr(settings, 'GROQ_MODEL', 'llama-3.3-70b-versatile')
                    logger.info(f"✅ Using legacy Groq with model: {model_name}")
                    return Groq(
                        groq_api_key=settings.GROQ_API_KEY,
                        model_name=model_name,
                        temperature=0.1
                    )
                except ImportError:
                    logger.warning("Groq not available")
                    return None
        
        # Fallback to OpenAI
        if settings.OPENAI_API_KEY:
            from langchain.chat_models import ChatOpenAI
            logger.info("Using OpenAI LLM")
            return ChatOpenAI(
                openai_api_key=settings.OPENAI_API_KEY,
                model="gpt-3.5-turbo",
                temperature=0.1
            )
        
        logger.warning("No LLM configured")
        return None
        
    except Exception as e:
        logger.error(f"Error initializing LLM: {e}")
        return None
# Create singleton instance
rag_pipeline = NetOneRAGPipeline()