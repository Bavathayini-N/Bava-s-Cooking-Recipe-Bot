"""
data_prep/prepare_data.py
─────────────────────────
Loads the raw RecipeNLG CSV, cleans stringified lists into readable text,
and produces a list of LangChain Document objects ready for embedding.
"""

import pandas as pd
import ast
from langchain_core.documents import Document


def clean_text(text, separator=", "):
    """Converts a stringified list into a clean joined string."""
    try:
        actual_list = ast.literal_eval(text)
        return separator.join(actual_list)
    except Exception:
        return text


def load_and_clean_data(csv_path: str, sample_size: int = 5000) -> pd.DataFrame:
    """Load *sample_size* rows from the CSV and clean them."""
    print(f"📂 Loading {sample_size} rows from dataset …")
    df = pd.read_csv(csv_path, nrows=sample_size)

    df = df[["title", "ingredients", "directions"]]
    df = df.dropna()

    print("🧹 Cleaning stringified lists …")
    df["ingredients"] = df["ingredients"].apply(lambda x: clean_text(x, separator=", "))
    df["directions"] = df["directions"].apply(lambda x: clean_text(x, separator=" "))

    print(f"✅ {len(df)} recipes cleaned and ready.\n")
    return df


def dataframe_to_documents(df: pd.DataFrame) -> list[Document]:
    """
    Convert each recipe row into a LangChain Document.

    page_content → a rich text block the retriever will search against.
    metadata     → stores the title for display purposes.
    """
    docs = []
    for _, row in df.iterrows():
        content = (
            f"Recipe: {row['title']}\n"
            f"Ingredients: {row['ingredients']}\n"
            f"Directions: {row['directions']}"
        )
        docs.append(
            Document(page_content=content, metadata={"title": row["title"]})
        )
    print(f"📄 Created {len(docs)} LangChain documents.\n")
    return docs


# ── quick standalone test ────────────────────────────────────────────
if __name__ == "__main__":
    recipe_df = load_and_clean_data("./raw_dataset/RecipeNLG_dataset.csv", sample_size=5000)
    print("Data Preview:")
    print(recipe_df.head(5))
    print()

    documents = dataframe_to_documents(recipe_df)
    print("Sample document:\n")
    print(documents[0].page_content[:500])