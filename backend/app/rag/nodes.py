# backend/app/rag/nodes.py

from typing import Dict, Any

from groq import Groq

from app.core.config import settings
from app.services.chroma_service import ChromaService



# LLM


llm = ChatGroq(
    groq_api_key=settings.GROQ_API_KEY,
    model_name=settings.llm_model,
    temperature=0
)



# VECTOR STORE


vector_store = ChromaService()



# RETRIEVE


def retrieve(state: Dict[str, Any]) -> Dict[str, Any]:

    question = state["question"]

    docs = vector_store.similarity_search(
        query=question,
        k=8
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



# ANALYZE


def analyze(state: Dict[str, Any]) -> Dict[str, Any]:

    context = "\n\n".join(
        state.get("context", [])
    )

    analysis_prompt = f"""
You are a professional social media analyst.

Use ONLY the information provided below.

CONTEXT:

{context}

RULES:

1. Never invent metrics.
2. Never estimate views, likes or engagement.
3. If a value is missing say:
   Data not available.
4. Use exact numbers from context.
5. Compare Video A and Video B only.

Analyze:

- Views
- Likes
- Comments
- Engagement Rate
- Creator
- Hashtags

Provide:

1. Reach Comparison
2. Engagement Comparison
3. Strongest Video
4. Weakest Video
5. Creator Insights
6. Improvement Suggestions

Keep answers factual.
"""

    response = llm.invoke(analysis_prompt)

    return {
        **state,
        "analysis": response.content
    }



# GENERATE


def generate(state: Dict[str, Any]) -> Dict[str, Any]:

    question = state["question"]

    context = "\n\n".join(
        state.get("context", [])
    )

    analysis = state.get(
        "analysis",
        ""
    )

    prompt = f"""
You are CreatorIQ AI.

QUESTION:

{question}

RETRIEVED DATA:

{context}

PREVIOUS ANALYSIS:

{analysis}

STRICT RULES:

1. Use ONLY retrieved data.

2. Never generate numbers that are not present.

3. Never estimate engagement rates.

4. Never claim a video performed better unless the metrics prove it.

5. If information is unavailable say:
   Data not available.

6. Compare:
   - Views
   - Likes
   - Comments
   - Engagement Rate
   - Creator
   - Hashtags

7. Give actionable creator advice.

8. Mention exact metrics whenever available.

9. Keep responses concise and professional.

10. If user asks:
    "Which video is better?"

    Decide using:
    - Views
    - Engagement Rate
    - Likes
    - Comments

    Explain using actual values only.

FINAL ANSWER:
"""

    response = llm.invoke(prompt)

    return {
        "question": question,
        "context": state.get("context", []),
        "sources": state.get("sources", []),
        "analysis": analysis,
        "answer": response.content
    }