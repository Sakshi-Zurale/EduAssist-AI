from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Vector store location
VECTOR_STORE_DIR = BASE_DIR / "vector_store"


def load_vector_store():
    """
    Load the saved FAISS vector store.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.load_local(
        str(VECTOR_STORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store


def test_retrieval(question, k=3):

    vector_store = load_vector_store()

    results = vector_store.similarity_search(
        question,
        k=k
    )

    print("\n========================================")
    print(f"QUESTION: {question}")
    print("========================================")

    for i, document in enumerate(results, start=1):

        print(f"\n--- Result {i} ---")

        print(
            f"Subject: "
            f"{document.metadata.get('subject', 'Unknown')}"
        )

        print(
            f"Source: "
            f"{Path(document.metadata.get('source', '')).name}"
        )

        print("\nContent:")
        print(document.page_content[:1000])


if __name__ == "__main__":

    print("\n===== EDUASSIST AI SEMANTIC RETRIEVAL =====")

    test_retrieval(
        "What is a Type 1 hypervisor?"
    )

    test_retrieval(
        "What is normalization in DBMS?"
    )

    test_retrieval(
        "What is supervised learning?"
    )

    print("\n===== RETRIEVAL TEST COMPLETED =====")
    