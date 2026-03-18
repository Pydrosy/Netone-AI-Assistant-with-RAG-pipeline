import sys
sys.path.append('.')
from app.core.rag_pipeline_direct import rag_pipeline
import os

print('Loading vector store...')
if os.path.exists('./faiss_index'):
    from langchain.vectorstores import FAISS
    # Remove the allow_dangerous_deserialization parameter
    rag_pipeline.vector_store = FAISS.load_local(
        './faiss_index', 
        rag_pipeline.embeddings
    )
    print(f'✅ Vector store loaded with {rag_pipeline.vector_store.index.ntotal} vectors')
    
    query = 'reverse calling 164 pay for me'
    print(f'Searching for: {query}')
    print('-' * 50)
    
    results = rag_pipeline.vector_store.similarity_search_with_score(query, k=5)
    
    for i, (doc, score) in enumerate(results):
        print(f'RESULT {i+1} (Score: {score:.4f})')
        print(f'Source: {doc.metadata.get("source", "Unknown")}')
        print('Content preview:')
        print(doc.page_content[:300] + '...')
        print('-' * 30)
else:
    print('FAISS index not found')
