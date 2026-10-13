from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from knowledge_loader import load_knowledge_base


def add_subject_metadata(documents):
    """
    Add subject information to each document based on its folder.
    """

    for document in documents:
        source_path = Path(document.metadata.get("source", ""))

        # Folder name is the subject
        subject = source_path.parent.name

        document.metadata["subject"] = subject

    return documents


def chunk_knowledge_base(documents):
    """
    Split knowledge documents into smaller meaningful chunks.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        length_function=len,
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


if __name__ == "__main__":

    print("\n===== EDUASSIST AI KNOWLEDGE CHUNKING =====")

    documents = load_knowledge_base()

    print(f"Documents loaded: {len(documents)}")

    documents = add_subject_metadata(documents)

    chunks = chunk_knowledge_base(documents)

    print(f"Total chunks created: {len(chunks)}")

    print("\n===== SAMPLE CHUNKS =====")

    for i, chunk in enumerate(chunks[:5], start=1):

        print(f"\n--- Chunk {i} ---")
        print(f"Subject: {chunk.metadata.get('subject')}")
        print(f"Source: {Path(chunk.metadata.get('source', '')).name}")
        print(f"Characters: {len(chunk.page_content)}")
        print(f"Content preview:\n{chunk.page_content[:300]}...")

    print("\nKnowledge base chunking completed successfully.")