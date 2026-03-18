import sys
sys.path.append('.')
from app.core.rag_pipeline_direct import rag_pipeline

print('🔍 Searching for BBB bundles...')
docs = rag_pipeline.vector_store.similarity_search('Big Beautiful Bundles BBB 100 150 200', k=10)
print(f'Found {len(docs)} relevant chunks')

for i, doc in enumerate(docs):
    print(f'\n--- CHUNK {i+1} ---')
    print(doc.page_content[:300] + '...')
    print(f'Source: {doc.metadata.get("title", "Unknown")}')
