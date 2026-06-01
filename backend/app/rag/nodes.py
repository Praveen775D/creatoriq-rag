# backend/app/rag/nodes.py

from typing import Dict, Any

from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.services.chroma_service import ChromaService


# LLM
llm = ChatOpenAI(
    model=settings.LLM_MODEL,
    api_key=settings.OPENAI_API_KEY,
    temperature=0
)

# Vector Store
vector_store = ChromaService()


def retrieve(
    state: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Retrieve relevant chunks from ChromaDB.
    """

    question = state["question"]

    documents = vector_store.similarity_search(
        query=question,
        k=5
    )

    context = []
    sources = []

    for document in documents:

        context.append(
            document.page_content
        )

        sources.append(
            {
                "video_id": document.metadata.get(
                    "video_id"
                ),
                "platform": document.metadata.get(
                    "platform"
                ),
                "creator": document.metadata.get(
                    "creator"
                ),
                "chunk_id": document.metadata.get(
                    "chunk_id"
                ),
                "source": document.metadata.get(
                    "source"
                )
            }
        )

    return {
        "question": question,
        "context": context,
        "sources": sources
    }


def generate(
    state: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate answer using retrieved context.
    """

    question = state["question"]

    context = "\n\n".join(
        state["context"]
    )

    prompt = f"""
You are an expert Creator Analytics Assistant.

You are comparing two social media videos:

Video A = YouTube
Video B = Instagram Reel

Use ONLY the supplied context.

=========================
CONTEXT
=========================

{context}

=========================
QUESTION
=========================

{question}

=========================
RULES
=========================

1. Use only the provided context.
2. Never hallucinate information.
3. Compare Video A and Video B when relevant.
4. Mention engagement insights if available.
5. Mention creator insights if available.
6. Suggest actionable improvements when asked.
7. If information is unavailable, clearly state it.

Provide a clear and structured answer.
"""

    response = llm.invoke(prompt)

    return {
        "question": question,
        "context": state["context"],
        "sources": state["sources"],
        "answer": response.content
    }