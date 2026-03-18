import sys
print("Testing patched ChromaDB...")

try:
    import chromadb
    print(f"✅ ChromaDB version: {chromadb.__version__}")
    
    # Try to create a client
    client = chromadb.Client()
    print("✅ ChromaDB client created")
    
    # Try to create a collection
    collection = client.create_collection("test_collection")
    print("✅ ChromaDB collection created")
    
    print("\n🎉 ChromaDB is working with the patch!")
    
except Exception as e:
    print(f"❌ Error: {e}")
