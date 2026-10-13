
from pathlib import Path
from functools import lru_cache
import time

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_STORE_DIR = BASE_DIR / "vector_store"


# ============================================================
# SETTINGS
# ============================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

DEFAULT_TOP_K = 3
MAX_DISTANCE = 1.20


# ============================================================
# LOAD EMBEDDING MODEL ONLY ONCE
# ============================================================

@lru_cache(maxsize=1)
def load_embeddings():
    """Load and cache the embedding model."""

    print("[RAG] Loading embedding model...")
    start_time = time.perf_counter()

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": False},
    )

    elapsed = time.perf_counter() - start_time
    print(f"[RAG] Embedding model loaded in {elapsed:.2f}s")

    return embeddings


# ============================================================
# LOAD FAISS VECTOR STORE ONLY ONCE
# ============================================================

@lru_cache(maxsize=1)
def load_vector_store():
    """Load and cache the FAISS vector store."""

    if not VECTOR_STORE_DIR.exists():
        raise FileNotFoundError(
            f"FAISS vector store not found: {VECTOR_STORE_DIR}"
        )

    index_file = VECTOR_STORE_DIR / "index.faiss"
    metadata_file = VECTOR_STORE_DIR / "index.pkl"

    if not index_file.exists() or not metadata_file.exists():
        raise FileNotFoundError(
            f"FAISS index files are missing in: {VECTOR_STORE_DIR}"
        )

    print("[RAG] Loading FAISS vector store...")
    start_time = time.perf_counter()

    vector_store = FAISS.load_local(
        str(VECTOR_STORE_DIR),
        load_embeddings(),
        allow_dangerous_deserialization=True,
    )

    elapsed = time.perf_counter() - start_time
    print(f"[RAG] FAISS vector store loaded in {elapsed:.2f}s")

    return vector_store


# ============================================================
# RETRIEVE RELEVANT KNOWLEDGE
# ============================================================

def retrieve_knowledge(
    question: str,
    k: int = DEFAULT_TOP_K,
    max_distance: float = MAX_DISTANCE,
):
    """Retrieve the most relevant documents from FAISS."""

    if not question or not question.strip():
        return []

    start_time = time.perf_counter()

    # Limit retrieval to avoid unnecessarily large results.
    k = max(1, min(k, DEFAULT_TOP_K))

    vector_store = load_vector_store()
    store_ready_time = time.perf_counter()

    results = vector_store.similarity_search_with_score(
        question.strip(),
        k=k,
    )

    search_complete_time = time.perf_counter()

    retrieved_documents = []

    for document, distance in results:
        distance = float(distance)

        # FAISS returns L2 distance for the usual
        # IndexFlatL2 configuration.
        if distance > max_distance:
            continue

        source_path = Path(
            document.metadata.get("source", "")
        )

        retrieved_documents.append(
            {
                "content": document.page_content,
                "subject": document.metadata.get(
                    "subject", "unknown"
                ),
                "source": source_path.name,
                "distance": round(distance, 4),
            }
        )

    end_time = time.perf_counter()

    print(
        f"[RAG] Store access: "
        f"{store_ready_time - start_time:.3f}s"
    )
    print(
        f"[RAG] Search + query embedding: "
        f"{search_complete_time - store_ready_time:.3f}s"
    )
    print(
        f"[RAG] Filtering + total retrieval: "
        f"{end_time - start_time:.3f}s"
    )
    print(
        f"[RAG] Documents retrieved: "
        f"{len(retrieved_documents)}"
    )

    return retrieved_documents


# ============================================================
# BUILD RAG CONTEXT
# ============================================================

def build_rag_context(
    question: str,
    k: int = DEFAULT_TOP_K,
    max_distance: float = MAX_DISTANCE,
):
    """Build the context and source metadata for the chatbot."""

    results = retrieve_knowledge(
        question=question,
        k=k,
        max_distance=max_distance,
    )

    if not results:
        return {
            "question": question,
            "context": "",
            "sources": [],
            "results": [],
            "retrieval_status": "no_relevant_knowledge",
        }

    context_parts = []
    sources = []

    for index, result in enumerate(results, start=1):
        context_parts.append(
            f"""--- Knowledge Source {index} ---
Subject: {result['subject']}
Source: {result['source']}
Similarity Distance: {result['distance']}

{result['content']}"""
        )

        sources.append(
            {
                "subject": result["subject"],
                "source": result["source"],
                "distance": result["distance"],
            }
        )

    return {
        "question": question,
        "context": "\n\n".join(context_parts),
        "sources": sources,
        "results": results,
        "retrieval_status": "knowledge_found",
    }
