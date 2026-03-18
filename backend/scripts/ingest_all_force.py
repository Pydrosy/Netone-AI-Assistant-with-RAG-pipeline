#!/usr/bin/env python3
"""
Complete ingestion of ALL Netone documents
"""

import os
import sys
import glob
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("=" * 60)
logger.info("LOADING RAG PIPELINE...")
logger.info("=" * 60)

from app.core.rag_pipeline_direct import rag_pipeline

# Get all document files
docs_dir = "data/documents"
all_files = glob.glob(os.path.join(docs_dir, "*.txt"))
all_files.sort()

logger.info(f"📚 Found {len(all_files)} documents to ingest:")
for i, f in enumerate(all_files, 1):
    size = os.path.getsize(f)
    logger.info(f"  {i}. {os.path.basename(f)} ({size} bytes)")

logger.info("-" * 60)

total_chunks = 0
successful_files = 0

for file_path in all_files:
    filename = os.path.basename(file_path)
    logger.info(f"\n📄 Ingesting: {filename}")
    
    # Determine category based on filename
    category = "general"
    if "history" in filename.lower():
        category = "company_history"
    elif "technical" in filename.lower():
        category = "technical_support"
    elif "faq" in filename.lower():
        category = "faq"
    elif "scratch" in filename.lower():
        category = "airtime"
    elif "complete" in filename.lower() or "guide" in filename.lower():
        category = "company_guide"
    elif "sample" in filename.lower():
        category = "sample"
    
    metadata = {
        "title": filename.replace(".txt", "").replace("_", " ").title(),
        "category": category,
        "source": filename,
        "file_size": os.path.getsize(file_path)
    }
    
    try:
        logger.info(f"  Processing...")
        success, chunks = rag_pipeline.ingest_document(file_path, metadata)
        if success:
            total_chunks += chunks
            successful_files += 1
            logger.info(f"  ✅ Added {chunks} chunks")
        else:
            logger.error(f"  ❌ Failed to ingest")
    except Exception as e:
        logger.error(f"  ❌ Error: {e}")
    
    # Small pause between files
    time.sleep(1)

logger.info("\n" + "=" * 60)
logger.info("📊 INGESTION SUMMARY")
logger.info("=" * 60)
logger.info(f"📚 Files processed: {len(all_files)}")
logger.info(f"✅ Successful: {successful_files}")
logger.info(f"📦 Total chunks: {total_chunks}")
logger.info("-" * 60)

# Final stats
stats = rag_pipeline.get_collection_stats()
logger.info(f"📊 Collection stats: {stats}")
logger.info("=" * 60)
