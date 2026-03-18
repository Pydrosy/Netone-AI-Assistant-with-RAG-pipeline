#!/usr/bin/env python3
"""
Test the full RAG pipeline functionality
"""

import os
import sys
import logging
from app.core.rag_pipeline import rag_pipeline

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_rag_full():
    """Test the complete RAG pipeline"""
    
    print("\n" + "="*60)
    print("TESTING NETONE RAG PIPELINE - FULL FUNCTIONALITY")
    print("="*60 + "\n")
    
    # Step 1: Check collection stats
    print("📊 Initial Collection Stats:")
    stats = rag_pipeline.get_collection_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "-"*60)
    
    # Step 2: Test document ingestion if we have a sample
    sample_path = "data/documents/sample_faq.txt"
    if os.path.exists(sample_path):
        print(f"\n📄 Testing document ingestion: {sample_path}")
        metadata = {
            "title": "Test FAQ",
            "category": "test",
            "description": "Test document for RAG pipeline"
        }
        
        success, chunks = rag_pipeline.ingest_document(sample_path, metadata)
        if success:
            print(f"  ✅ Successfully ingested {chunks} chunks")
        else:
            print("  ❌ Failed to ingest document")
    else:
        print(f"\n⚠️  Sample document not found at {sample_path}")
        print("   Creating a sample document...")
        
        # Create a sample document
        os.makedirs("data/documents", exist_ok=True)
        sample_content = """# NetOne Frequently Asked Questions

## Account & Billing
Q: How do I check my account balance?
A: You can check your balance by dialing *123# on your NetOne line, or by logging into the MyNetOne app.

Q: How can I pay my bill?
A: NetOne accepts payments through:
- Mobile money (Airtel Money, MTN Money)
- Bank transfers
- Credit/debit cards via our website
- At any NetOne service center

## Network & Technical Support
Q: What should I do if I have no network signal?
A: Try these steps:
1. Restart your phone
2. Check if you're in a coverage area
3. Remove and reinsert your SIM card
4. Contact support if issues persist

Q: How do I set up my internet APN?
A: For NetOne internet, use these settings:
- APN: netone.internet
- Username: (leave blank)
- Password: (leave blank)

## Services & Plans
Q: What internet packages do you offer?
A: NetOne offers:
- Daily bundles (from 100MB to 2GB)
- Weekly bundles (from 1GB to 10GB)
- Monthly bundles (from 5GB to 50GB)
"""
        
        with open(sample_path, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        print(f"  ✅ Created sample document at {sample_path}")
        
        # Now ingest it
        metadata = {
            "title": "NetOne FAQ",
            "category": "faq",
            "description": "Frequently asked questions about NetOne services"
        }
        success, chunks = rag_pipeline.ingest_document(sample_path, metadata)
        if success:
            print(f"  ✅ Successfully ingested {chunks} chunks")
        else:
            print("  ❌ Failed to ingest document")
    
    print("\n" + "-"*60)
    
    # Step 3: Test queries
    print("\n🔍 Testing Queries:")
    print("-"*40)
    
    test_queries = [
        "How do I check my balance?",
        "What internet packages do you offer?",
        "How can I pay my bill?",
        "I have no network signal, what should I do?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Query {i}: {query}")
        print("-"*30)
        
        # Generate response
        result = rag_pipeline.generate_response(query)
        
        print(f"🤖 Answer: {result['answer']}")
        
        if result['sources']:
            print(f"\n📚 Sources ({len(result['sources'])}):")
            for source in result['sources']:
                print(f"  • {source.get('title', 'Unknown')} - {source.get('category', 'general')}")
        else:
            print("\n📚 No sources found (document may not have relevant info)")
        
        print("-"*30)
    
    # Step 4: Show final stats
    print("\n" + "="*60)
    print("📊 Final Collection Stats:")
    stats = rag_pipeline.get_collection_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print("="*60)

if __name__ == "__main__":
    test_rag_full()