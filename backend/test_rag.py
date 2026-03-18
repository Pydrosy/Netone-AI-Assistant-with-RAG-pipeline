#!/usr/bin/env python3
"""
Test script for RAG pipeline
"""

import logging
from app.core.rag_pipeline import rag_pipeline

logging.basicConfig(level=logging.INFO)

def test_rag():
    """Test the RAG pipeline"""
    
    print("\n" + "="*60)
    print("TESTING NETONE RAG PIPELINE")
    print("="*60 + "\n")
    
    # Test 1: Check collection stats
    print("📊 Collection Stats:")
    stats = rag_pipeline.get_collection_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "-"*60)
    
    # Test 2: Try a query
    test_queries = [
        "What services do you offer?",
        "How do I check my balance?",
        "I'm having network issues in Lusaka"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        print("-"*40)
        
        # Generate response
        result = rag_pipeline.generate_response(query)
        
        print(f"📝 Answer: {result['answer']}\n")
        
        if result['sources']:
            print("📚 Sources:")
            for source in result['sources']:
                print(f"  • {source['title']} ({source['category']})")
                print(f"    {source['excerpt']}")
        
        print("\n" + "-"*60)

if __name__ == "__main__":
    test_rag()