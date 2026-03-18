#!/usr/bin/env python3
"""
Script to ingest sample documents into the RAG pipeline
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from app.core.rag_pipeline import rag_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_samples():
    """Ingest sample documents"""
    
    sample_files = [
        {
            "path": "data/documents/sample_faq.txt",
            "metadata": {
                "title": "NetOne FAQ",
                "category": "faq",
                "description": "Frequently asked questions about NetOne services"
            }
        }
    ]
    
    for sample in sample_files:
        if os.path.exists(sample["path"]):
            logger.info(f"Ingesting {sample['path']}...")
            success, chunks = rag_pipeline.ingest_document(
                sample["path"],
                sample["metadata"]
            )
            if success:
                logger.info(f"✅ Ingested {chunks} chunks")
            else:
                logger.error(f"❌ Failed to ingest {sample['path']}")
        else:
            logger.warning(f"File not found: {sample['path']}")
    
    # Show stats
    logger.info("\n📊 Final collection stats:")
    stats = rag_pipeline.get_collection_stats()
    for key, value in stats.items():
        logger.info(f"  {key}: {value}")

if __name__ == "__main__":
    ingest_samples()