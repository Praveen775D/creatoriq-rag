from typing import Generator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.rag.graph import graph


router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    thread_id: str = "default"


def generate_response(
    question: str,
    thread_id: str
) -> Generator[str, None, None]:
    """
    Execute LangGraph workflow
    and stream response.
    """

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = graph.invoke(
        {
            "question": question
        },
        config=config
    )

    answer = result["answer"]

    yield answer


@router.post("/")
async def chat(
    payload: ChatRequest
):

    config = {
        "configurable": {
            "thread_id": payload.thread_id
        }
    }

    result = graph.invoke(
        {
            "question": payload.question
        },
        config=config
    )

    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }


@router.post("/stream")
async def stream_chat(
    payload: ChatRequest
):

    return StreamingResponse(
        generate_response(
            payload.question,
            payload.thread_id
        ),
        media_type="text/plain"
    )