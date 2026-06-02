
# backend/app/rag/nodes.py

from typing import Dict, Any

from langchain_groq import ChatGroq

from app.core.config import settings
from app.services.chroma_service import ChromaService


# =========================================================
# LLM
# =========================================================

llm = ChatGroq(
    groq_api_key=settings.GROQ_API_KEY,
    model_name=settings.llm_model,
    temperature=0
)


# =========================================================
# VECTOR STORE
# =========================================================

vector_store = ChromaService()


# =========================================================
# RETRIEVE
# =========================================================

def retrieve(state: Dict[str, Any]) -> Dict[str, Any]:

    question = state["question"]

    docs = vector_store.similarity_search(
        query=question,
        k=6
    )

    context = []
    sources = []

    for doc in docs:

        context.append(doc.page_content)

        sources.append({
            "video_id": doc.metadata.get("video_id"),
            "platform": doc.metadata.get("platform"),
            "creator": doc.metadata.get("creator"),
            "chunk_id": doc.metadata.get("chunk_id"),
            "source": doc.metadata.get("source")
        })

    return {
        "question": question,
        "context": context,
        "sources": sources
    }


# =========================================================
# ANALYZE
# =========================================================

def analyze(state: Dict[str, Any]) -> Dict[str, Any]:

    context = "\n\n".join(
        state["context"]
    )

    prompt = f"""
You are a CreatorIQ content analyst.

Analyze ONLY the information present below.

Do NOT invent:
- retention rates
- hook scores
- engagement percentages
- performance metrics

If information is missing,
say "Data not available".

Context:

{context}

Return:

1. Platform Differences
2. Engagement Signals
3. Content Themes
4. Creator Strategy
5. Key Observations
"""

    response = llm.invoke(prompt)

    return {
        **state,
        "analysis": response.content
    }


# =========================================================
# GENERATE
# =========================================================

def generate(state: Dict[str, Any]) -> Dict[str, Any]:

    question = state["question"]

    context = "\n\n".join(
        state["context"]
    )

    analysis = state.get(
        "analysis",
        ""
    )

    prompt = f"""
You are CreatorIQ AI.

Answer the user question using ONLY
the retrieved context.

Question:
{question}

Retrieved Context:
{context}

Analysis:
{analysis}

Rules:

- Never invent statistics
- Never invent retention rates
- Never invent hook scores
- Never invent engagement rates
- If data is missing, say so
- Compare videos using actual metadata
- Mention views, likes, comments, hashtags when available
- Be concise and professional

Answer:
"""

    response = llm.invoke(prompt)

    return {
        "question": question,
        "context": state["context"],
        "sources": state["sources"],
        "analysis": analysis,
        "answer": response.content
    }
