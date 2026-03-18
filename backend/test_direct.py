import sys
import os
print("=" * 60)
print("Testing Direct Groq RAG Pipeline")
print("=" * 60)

# Import the pipeline
from app.core.rag_pipeline_direct import rag_pipeline

# Get stats
print("\n📊 Initial Stats:")
stats = rag_pipeline.get_collection_stats()
for key, value in stats.items():
    print(f"  {key}: {value}")

# Create sample document if needed
sample_path = "data/documents/sample_faq.txt"
if not os.path.exists(sample_path):
    os.makedirs("data/documents", exist_ok=True)
    with open(sample_path, "w", encoding="utf-8") as f:
        f.write("""
NetOne Services and Information:
- NetOne is a leading telecommunications company in Zambia
- Services include mobile voice calls, SMS, and data packages
- Internet bundles: Daily (100MB-2GB), Weekly (1GB-10GB), Monthly (5GB-50GB)
- Check balance: Dial *123#
- Customer support: Call 1234 or email support@netone.co.zm
- Enterprise solutions: Dedicated business internet, VPN services, cloud solutions
- Network coverage: Available in all provincial capitals and major towns
        """)
    print("\n📄 Created sample document")

# Ingest the document
print("\n📄 Ingesting sample document...")
success, chunks = rag_pipeline.ingest_document(sample_path, {
    "title": "NetOne FAQ",
    "category": "general"
})
print(f"  Ingestion {'✅ successful' if success else '❌ failed'} - {chunks} chunks")

# Test queries
test_queries = [
    "What services does NetOne offer?",
    "How do I check my balance?",
    "What internet packages are available?"
]

print("\n" + "=" * 60)
print("🔍 Testing Queries")
print("=" * 60)

for i, query in enumerate(test_queries, 1):
    print(f"\n📝 Query {i}: {query}")
    print("-" * 40)
    
    result = rag_pipeline.generate_response(query)
    
    print(f"🤖 Answer: {result['answer']}")
    
    if result['sources']:
        print(f"\n📚 Sources:")
        for source in result['sources']:
            print(f"  • {source['title']} (relevance: {source['relevance']})")

print("\n" + "=" * 60)
print("✅ Test Complete!")
print("=" * 60)
