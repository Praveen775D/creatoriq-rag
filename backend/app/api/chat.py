from fastapi import APIRouter

from pydantic import BaseModel

from app.rag.graph import graph

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/")
async def chat(
    payload: ChatRequest
):

    result = graph.invoke(
        {
            "question": payload.question
        }
    )

    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }