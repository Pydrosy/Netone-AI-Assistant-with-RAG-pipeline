import sys
import os
print("Testing FAISS RAG Pipeline...")

# Import the FAISS pipeline
from app.core.rag_pipeline_faiss import rag_pipeline

# Get stats
stats = rag_pipeline.get_collection_stats()
print(f"Collection stats: {stats}")

# Test document ingestion
sample_path = "data/documents/sample_faq.txt"
if os.path.exists(sample_path):
    print(f"Ingesting sample document...")
    success, chunks = rag_pipeline.ingest_document(sample_path, {
        "title": "NetOne FAQ",
        "category": "faq"
    })
    print(f"Ingestion {'successful' if success else 'failed'} - {chunks} chunks")
else:
    print("Sample document not found, creating one...")
    os.makedirs("data/documents", exist_ok=True)
    with open(sample_path, "w") as f:
        f.write("""
NetOne Services:
- Mobile voice and data plans
- Internet bundles (daily, weekly, monthly)
- Enterprise solutions
- Customer support available 24/7
- Check balance by dialing *123#
        """)
    print("Sample document created")

# Test query
print("\nTesting query...")
result = rag_pipeline.generate_response("What services does NetOne offer?")
print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")

print("\n🎉 FAISS RAG Pipeline test complete!")
