from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from knowledge_loader import load_knowledge_base
from knowledge_chunker import add_subject_metadata, chunk_knowledge_base


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Where the vector database will be stored
VECTOR_STORE_DIR = BASE_DIR / "vector_store"


def build_vector_store():
    print("\n===== EDUASSIST AI VECTOR STORE =====")

    # 1. Load documents
    documents = load_knowledge_base()
    print(f"Documents loaded: {len(documents)}")

    # 2. Add metadata
    documents = add_subject_metadata(documents)

    # 3. Create chunks
    chunks = chunk_knowledge_base(documents)
    print(f"Chunks created: {len(chunks)}")

    # 4. Create embedding model
    print("\nLoading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Embedding model loaded.")

    # 5. Convert chunks into vectors
    print("\nCreating embeddings and FAISS index...")

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    # 6. Create directory
    VECTOR_STORE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # 7. Save FAISS vector store
    vector_store.save_local(
        str(VECTOR_STORE_DIR)
    )

    print("\n===== VECTOR STORE CREATED =====")
    print(f"Vector store location: {VECTOR_STORE_DIR}")
    print(f"Vectors created: {len(chunks)}")

    return vector_store


if __name__ == "__main__":
    build_vector_store()