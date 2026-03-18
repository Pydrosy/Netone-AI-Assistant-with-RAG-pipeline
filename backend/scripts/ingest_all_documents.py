#!/usr/bin/env python3
"""
Script to ingest all Netone documents into the RAG pipeline
"""

import os
import sys
import glob
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from app.core.rag_pipeline_direct import rag_pipeline

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def ingest_all_documents():
    """Ingest all documents from the data/documents directory"""
    
    documents_dir = "data/documents"
    if not os.path.exists(documents_dir):
        logger.error(f"Documents directory not found: {documents_dir}")
        return
    
    # Get all text files
    text_files = glob.glob(os.path.join(documents_dir, "*.txt"))
    
    if not text_files:
        logger.warning("No text files found in documents directory")
        return
    
    logger.info(f"Found {len(text_files)} documents to ingest")
    
    total_chunks = 0
    for file_path in text_files:
        filename = os.path.basename(file_path)
        logger.info(f"\n📄 Ingesting: {filename}")
        
        # Determine category based on filename
        if "faq" in filename.lower():
            category = "faq"
        elif "complete" in filename.lower() or "guide" in filename.lower():
            category = "company_guide"
        elif "services" in filename.lower():
            category = "services"
        elif "bundles" in filename.lower():
            category = "bundles"
        elif "zimbabwe" in filename.lower():
            category = "zimbabwe"
        else:
            category = "general"
        
        metadata = {
            "title": filename.replace(".txt", "").replace("_", " ").title(),
            "category": category,
            "source": filename,
            "company": "Netone Zimbabwe"
        }
        
        try:
            success, chunks = rag_pipeline.ingest_document(file_path, metadata)
            if success:
                total_chunks += chunks
                logger.info(f"  ✅ Ingested {chunks} chunks")
            else:
                logger.error(f"  ❌ Failed to ingest {filename}")
        except Exception as e:
            logger.error(f"  ❌ Error ingesting {filename}: {e}")
    
    logger.info(f"\n📊 Total chunks ingested: {total_chunks}")
    
    # Get final stats
    stats = rag_pipeline.get_collection_stats()
    logger.info(f"Collection stats: {stats}")
    
    return stats

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Starting Netone Document Ingestion")
    logger.info("=" * 60)
    
    stats = ingest_all_documents()
    
    logger.info("\n" + "=" * 60)
    logger.info("Ingestion Complete!")
    logger.info("=" * 60)
