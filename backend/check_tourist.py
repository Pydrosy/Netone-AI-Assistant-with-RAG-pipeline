import sys
sys.path.append('.')
from app.core.rag_pipeline_direct import rag_pipeline

print('🔍 CHECKING VECTOR STORE CONTENTS')
print('=' * 50)

if rag_pipeline.vector_store:
    # Search for tourist SIM information
    docs = rag_pipeline.vector_store.similarity_search('tourist SIM card visitors', k=10)
    print(f'Found {len(docs)} documents about tourist SIM:')
    
    for i, doc in enumerate(docs):
        print(f'\n--- DOCUMENT {i+1} ---')
        print(f'Title: {doc.metadata.get("title", "Unknown")}')
        print(f'Category: {doc.metadata.get("category", "Unknown")}')
        print(f'Content preview: {doc.page_content[:200]}...')
    
    # Get total count
    try:
        count = rag_pipeline.vector_store.index.ntotal
        print(f'\n📊 Total vectors in store: {count}')
    except:
        print('Could not get vector count')
else:
    print('Vector store not initialized!')
