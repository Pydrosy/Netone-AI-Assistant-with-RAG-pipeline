# test_rag_imports.py
print("Testing RAG pipeline imports...")
print("-" * 40)

try:
    from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
    print("✅ langchain.embeddings imported")
except Exception as e:
    print(f"❌ langchain.embeddings failed: {e}")

try:
    from langchain.vectorstores import Chroma
    print("✅ Chroma imported")
except Exception as e:
    print(f"❌ Chroma failed: {e}")

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    print("✅ text_splitter imported")
except Exception as e:
    print(f"❌ text_splitter failed: {e}")

try:
    from langchain.document_loaders import TextLoader
    print("✅ document_loaders imported")
except Exception as e:
    print(f"❌ document_loaders failed: {e}")

try:
    from langchain.chat_models import ChatOpenAI
    print("✅ chat_models imported")
except Exception as e:
    print(f"❌ chat_models failed: {e}")

print("\n" + "-" * 40)
print("Import test complete!")