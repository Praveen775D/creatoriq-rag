# backend/app/rag/nodes.py

from typing import Dict, Any, List

from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.services.chroma_service import ChromaService


# ---------------- LLM ----------------
llm = ChatOpenAI(
    model=settings.llm_model,
    api_key=settings.OPENAI_API_KEY,
    temperature=0
)

# ---------------- VECTOR DB ----------------
vector_store = ChromaService()


# =========================================================
# 1. RETRIEVAL NODE
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
# 2. ANALYSIS NODE (NEW - INTERVIEW CRITICAL)
# =========================================================
def analyze(state: Dict[str, Any]) -> Dict[str, Any]:

    context = state["context"]

    analysis_prompt = f"""
You are a senior AI analyst.

You are given chunks from TWO videos:
- Video A (YouTube)
- Video B (Instagram Reel)

TASK:
Analyze differences between Video A and Video B.

Focus on:
1. Hook quality (first 5 seconds)
2. Engagement signals
3. Content structure
4. Creator strategy differences

CONTEXT:
{chr(10).join(context)}

Return structured insights:
- Key Differences
- Why one performed better
- Engagement insights
"""

    response = llm.invoke(analysis_prompt)

    return {
        **state,
        "analysis": response.content
    }


# =========================================================
# 3. GENERATION NODE
# =========================================================
def generate(state: Dict[str, Any]) -> Dict[str, Any]:

    question = state["question"]
    context = "\n\n".join(state["context"])
    analysis = state.get("analysis", "")

    prompt = f"""
You are an expert CreatorIQ Analytics Assistant.

You compare video performance using real data.

========================
QUESTION
========================
{question}

========================
RAW CONTEXT
========================
{context}

========================
PRE-ANALYSIS
========================
{analysis}

========================
RULES
========================
- Always compare Video A vs Video B when relevant
- Use ONLY provided data
- No hallucination
- Give actionable insights
- Be structured and clear

FINAL ANSWER:
"""

    response = llm.invoke(prompt)

    return {
        "question": question,
        "context": state["context"],
        "sources": state["sources"],
        "analysis": analysis,
        "answer": response.content
    }