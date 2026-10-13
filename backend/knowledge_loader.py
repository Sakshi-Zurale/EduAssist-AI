from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Knowledge base directory
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"


def load_knowledge_base():
    """
    Load all Markdown documents from the knowledge base.
    """

    loader = DirectoryLoader(
        str(KNOWLEDGE_BASE_DIR),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True
    )

    documents = loader.load()

    return documents


if __name__ == "__main__":
    documents = load_knowledge_base()

    print("\n===== EDUASSIST AI KNOWLEDGE BASE =====")
    print(f"Knowledge base path: {KNOWLEDGE_BASE_DIR}")
    print(f"Documents loaded: {len(documents)}")

    for i, document in enumerate(documents, start=1):
        print(f"\nDocument {i}")
        print(f"Source: {document.metadata.get('source')}")
        print(f"Characters: {len(document.page_content)}")

    print("\nKnowledge base loading completed successfully.")