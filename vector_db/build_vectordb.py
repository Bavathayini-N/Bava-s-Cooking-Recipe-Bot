"""
vector_db/build_vectordb.py
───────────────────────────
Builds (or loads) a ChromaDB vector store from recipe documents.

Uses HuggingFace `all-MiniLM-L6-v2` for embeddings — fast, free,
and runs entirely on CPU.
"""

import os
import sys

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# ── allow imports from project root ──────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data_prep.prepare_data import load_and_clean_data, dataframe_to_documents

# ── paths ────────────────────────────────────────────────────────────
PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_store")
CSV_PATH    = os.path.join(os.path.dirname(__file__), "..", "raw_dataset", "RecipeNLG_dataset.csv")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "recipes"


def get_embeddings():
    """Return the HuggingFace embedding function."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def build_vectordb(force_rebuild: bool = False):
    """
    Build the Chroma vector store from scratch.
    If the store already exists on disk and *force_rebuild* is False,
    it is loaded instead.
    """
    embeddings = get_embeddings()

    if os.path.exists(PERSIST_DIR) and not force_rebuild:
        print(" Loading existing ChromaDB from disk …")
        vectordb = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embeddings,
            collection_name=COLLECTION_NAME,
        )
        print(f" Loaded ChromaDB with {vectordb._collection.count()} documents.\n")
        return vectordb

    # ── fresh build ──────────────────────────────────────────────────
    print("  Building a fresh ChromaDB vector store …\n")

    df   = load_and_clean_data(CSV_PATH, sample_size=5000)
    docs = dataframe_to_documents(df)

    # ChromaDB has a batch-add limit; chunk the documents to be safe
    BATCH = 500
    vectordb = None

    for i in range(0, len(docs), BATCH):
        batch = docs[i : i + BATCH]
        print(f"   ↳ Embedding batch {i // BATCH + 1} ({len(batch)} docs) …")

        if vectordb is None:
            vectordb = Chroma.from_documents(
                documents=batch,
                embedding=embeddings,
                persist_directory=PERSIST_DIR,
                collection_name=COLLECTION_NAME,
            )
        else:
            vectordb.add_documents(batch)

    print(f"\n ChromaDB built and persisted → {PERSIST_DIR}")
    print(f"   Total documents: {vectordb._collection.count()}\n")
    return vectordb


def load_vectordb():
    """Convenience function: load an existing store (build if missing)."""
    return build_vectordb(force_rebuild=False)


# ── standalone runner ────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build / load the recipe vector DB")
    parser.add_argument("--rebuild", action="store_true", help="Force a full rebuild")
    args = parser.parse_args()

    db = build_vectordb(force_rebuild=args.rebuild)

    # quick sanity search
    query = "chicken garlic butter"
    results = db.similarity_search(query, k=3)
    print(f" Top 3 results for '{query}':\n")
    for r in results:
        print(f"{r.metadata['title']}")
    print()
