import sys
sys.path.append('.')
from app.core.rag_pipeline_direct import rag_pipeline
import os

print('Loading vector store...')
if os.path.exists('./faiss_index'):
    from langchain.vectorstores import FAISS
    rag_pipeline.vector_store = FAISS.load_local(
        './faiss_index', 
        rag_pipeline.embeddings
    )
    print(f'✅ Vector store loaded with {rag_pipeline.vector_store.index.ntotal} vectors')
    
    # Search for the query
    query = '164 wena?'
    print(f'\nSearching for: "{query}"')
    print('-' * 50)
    
    results = rag_pipeline.vector_store.similarity_search_with_score(query, k=5)
    
    found_local_language = False
    for i, (doc, score) in enumerate(results):
        print(f'\nRESULT {i+1} (Score: {score:.4f})')
        source = doc.metadata.get('source', 'Unknown')
        print(f'Source: {source}')
        print('Content preview:')
        print(doc.page_content[:200] + '...')
        print('-' * 30)
        
        if 'netone_local_languages.txt' in source:
            found_local_language = True
            print('✓ This is the local language guide!')
    
    if not found_local_language:
        print('\n⚠️  Local language guide not found in top 5 results')
        
        # Try searching specifically for local language content
        print('\nTrying broader search for local language content...')
        results2 = rag_pipeline.vector_store.similarity_search_with_score('shona ndebele wena', k=5)
        
        for i, (doc, score) in enumerate(results2):
            if 'netone_local_languages.txt' in doc.metadata.get('source', ''):
                print(f'Found local language guide with broader query (score: {score:.4f})')
                print('Preview:')
                print(doc.page_content[:200] + '...')
                break
else:
    print('❌ FAISS index not found')
