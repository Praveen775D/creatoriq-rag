from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.services.chroma_service import ChromaService


llm = ChatOpenAI(
    model=settings.LLM_MODEL,
    api_key=settings.OPENAI_API_KEY,
    temperature=0
)

vector_db = ChromaService()


def retrieve(state):

    question = state["question"]

    docs = vector_db.similarity_search(
        question,
        k=5
    )

    context = []

    sources = []

    for doc in docs:

        context.append(
            doc.page_content
        )

        sources.append(
            {
                "video_id": doc.metadata.get(
                    "video_id"
                ),
                "platform": doc.metadata.get(
                    "platform"
                ),
                "creator": doc.metadata.get(
                    "creator"
                )
            }
        )

    return {
        "question": question,
        "context": context,
        "sources": sources
    }


def generate(state):

    question = state["question"]

    context = "\n\n".join(
        state["context"]
    )

    prompt = f"""
You are a creator analytics assistant.

Answer ONLY using the provided context.

Context:
{context}

Question:
{question}

Provide:
1. Direct answer
2. Comparison insights
3. Source references
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }