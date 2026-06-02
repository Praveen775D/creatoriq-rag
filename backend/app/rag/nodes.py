# backend/app/rag/nodes.py

from typing import Dict, Any

from langchain_groq import ChatGroq

from app.core.config import settings
from app.services.chroma_service import ChromaService


# =========================================================
# LLM (GROQ)
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

    context = state["context"]

    analysis_prompt = f"""
You are a senior creator analytics expert.

Analyze Video A and Video B.

Focus on:

1. Hook quality
2. Engagement signals
3. Content structure
4. Creator strategy
5. Audience retention clues

Context:

{chr(10).join(context)}

Provide:

- Key Differences
- Strongest Video
- Weakest Video
- Engagement Insights
- Improvement Suggestions
"""

    response = llm.invoke(analysis_prompt)

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

Question:

{question}

Context:

{context}

Analysis:

{analysis}

Rules:

- Use only retrieved data
- Compare Video A and Video B
- Give actionable creator advice
- Cite source videos when possible
- Be concise but insightful
"""

    response = llm.invoke(prompt)

    return {
        "question": question,
        "context": state["context"],
        "sources": state["sources"],
        "analysis": analysis,
        "answer": response.content
    }