# backend/app/rag/state.py
from typing import TypedDict, List, Optional, Dict, Any


class GraphState(TypedDict):
    question: str

    # retrieved context chunks
    context: List[str]

    # structured reasoning layer (NEW)
    analysis: Optional[str]

    # final output
    answer: Optional[str]

    # source tracking for citations
    sources: List[Dict[str, Any]]