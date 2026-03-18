import sys
sys.path.append('.')
from app.core.rag_pipeline_direct import rag_pipeline
import os

print('Checking RAG Pipeline Configuration...')
print('=' * 50)

# First, load the vector store
print('Loading vector store...')
if os.path.exists('./faiss_index'):
    from langchain.vectorstores import FAISS
    rag_pipeline.vector_store = FAISS.load_local(
        './faiss_index', 
        rag_pipeline.embeddings
    )
    print(f'✅ Vector store loaded with {rag_pipeline.vector_store.index.ntotal} vectors')
else:
    print('❌ FAISS index not found')
    exit()

# Check pipeline attributes - using correct attribute names
print(f'\nPipeline attributes:')
print(f'Vector store type: {type(rag_pipeline.vector_store)}')
print(f'Embeddings model: {rag_pipeline.embeddings.model_name if hasattr(rag_pipeline.embeddings, "model_name") else "Unknown"}')
print(f'Has embeddings: {rag_pipeline.embeddings is not None}')
print(f'Has vector store: {rag_pipeline.vector_store is not None}')

# Check what methods are available
print(f'\nAvailable methods:')
methods = [method for method in dir(rag_pipeline) if not method.startswith('_')]
print(f'Methods: {methods[:10]}...')  # Show first 10 methods

# Test document retrieval directly from vector store
print('\n' + '=' * 50)
print('Testing document retrieval directly from vector store:')
query = "How can I make a call when I have no airtime?"
print(f'Query: {query}')

# Direct similarity search
docs_with_scores = rag_pipeline.vector_store.similarity_search_with_score(query, k=5)
print(f'Direct similarity search found {len(docs_with_scores)} documents')

for i, (doc, score) in enumerate(docs_with_scores[:3]):
    print(f'\n{i+1}. Score: {score:.4f} - Source: {doc.metadata.get("source", "Unknown")}')
    print(f'   Preview: {doc.page_content[:150]}...')

# Try to use the pipeline's retrieve method if it exists
print('\n' + '=' * 50)
print('Testing pipeline retrieval:')
if hasattr(rag_pipeline, 'retrieve'):
    retrieved_docs = rag_pipeline.retrieve(query)
    print(f'Pipeline.retrieve returned {len(retrieved_docs)} documents')
elif hasattr(rag_pipeline, 'get_relevant_documents'):
    retrieved_docs = rag_pipeline.get_relevant_documents(query)
    print(f'Pipeline.get_relevant_documents returned {len(retrieved_docs)} documents')
else:
    print('No retrieval method found in pipeline')

# Try to use the pipeline's generate method
print('\n' + '=' * 50)
print('Testing API endpoint:')
try:
    import requests
    response = requests.post(
        'http://localhost:8000/api/chat/query',
        json={'message': query}
    )
    if response.status_code == 200:
        data = response.json()
        print(f'API Response:')
        print(f'Answer preview: {data.get("answer", "")[:150]}...')
        sources = data.get('sources', [])
        print(f'Sources found: {len(sources)}')
        for i, source in enumerate(sources[:3]):
            print(f'  {i+1}. {source.get("title", "Unknown")} (relevance: {source.get("relevance", "N/A")})')
    else:
        print(f'API Error: {response.status_code}')
except Exception as e:
    print(f'Error calling API: {e}')
