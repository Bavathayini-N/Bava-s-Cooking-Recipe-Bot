"""
ask_ai/chain.py
───────────────
Creates the RAG (Retrieval-Augmented Generation) chain that:
  1. Retrieves relevant recipes from ChromaDB
  2. Passes them as context to a Groq LLM
  3. Returns a helpful cooking answer
"""

import os
from dotenv import load_dotenv
load_dotenv() # This loads the GROQ_API_KEY from your .env file
import sys

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

#  allow imports from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from vector_db.build_vectordb import load_vectordb

#  load env 
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# prompt 
SYSTEM_PROMPT = """\
You are ChefBot 🍳 — a friendly, knowledgeable cooking assistant.

Your job is to suggest recipes based on the ingredients the user provides.
Use ONLY the recipe context supplied below when recommending recipes.
If the context does not contain a good match, say so honestly and suggest
the user try different ingredients.

For every recipe you suggest, provide:
1. 🍽️ Recipe name
2. 📝 Full ingredient list
3. 👨‍🍳 Step-by-step cooking directions
4. 💡 A short pro tip (optional but appreciated)

Keep your tone warm, fun, and encouraging — like a helpful friend in the kitchen!
"""

RAG_TEMPLATE = """\
{system}

──── Retrieved Recipe Context ────
{context}
──────────────────────────────────

User's ingredients / question:
{question}

Please suggest the best matching recipe(s) from the context above.
"""

prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)


def format_docs(docs):
    """Join retrieved documents into a single context string."""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def get_rag_chain():
    """Build and return the full RAG chain."""
    # 1. Vector store retriever
    vectordb  = load_vectordb()
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    # 2. Groq LLM
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.4,
        max_tokens=2048,
    )

    # 3. RAG chain
    chain = (
        {
            "system":   lambda _: SYSTEM_PROMPT,
            "context":  retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


# standalone test 
if __name__ == "__main__":
    chain = get_rag_chain()

    question = "I have chicken, garlic, and butter. What can I make?"
    print(f"❓ {question}\n")
    print("━" * 60)
    answer = chain.invoke(question)
    print(answer)
