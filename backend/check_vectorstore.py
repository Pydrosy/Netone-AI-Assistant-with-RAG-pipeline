import sys
sys.path.append('.')
from app.core.rag_pipeline_direct import rag_pipeline

print('🔍 Checking vector store contents...')

if rag_pipeline.vector_store:
    # Try to search for CEO information
    docs = rag_pipeline.vector_store.similarity_search('CEO Netone executive', k=5)
    print(f'Found {len(docs)} relevant chunks for CEO query:')
    
    for i, doc in enumerate(docs):
        print(f'\n--- CHUNK {i+1} ---')
        print(doc.page_content[:300] + '...')
        print(f'Source: {doc.metadata.get("title", "Unknown")}')
        print(f'Category: {doc.metadata.get("category", "Unknown")}')
    
    # Get total count from FAISS directly
    try:
        count = rag_pipeline.vector_store.index.ntotal
        print(f'\n📊 FAISS index total vectors: {count}')
        
        # Also try a broader search
        print('\n🔍 Searching for "leadership" information:')
        leadership_docs = rag_pipeline.vector_store.similarity_search('leadership board members', k=3)
        for i, doc in enumerate(leadership_docs):
            print(f'\nLEADERSHIP {i+1}: {doc.metadata.get("title", "Unknown")}')
            print(doc.page_content[:150] + '...')
            
    except Exception as e:
        print(f'Could not get FAISS count: {e}')
else:
    print('Vector store not initialized')
