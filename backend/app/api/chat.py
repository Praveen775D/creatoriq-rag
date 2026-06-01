# backend/app/api/chat.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import AsyncGenerator

from app.rag.graph import graph

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    thread_id: str = "default"


# ---------------- NORMAL CHAT ----------------
@router.post("/")
async def chat(payload: ChatRequest):

    result = graph.invoke(
        {
            "question": payload.question
        },
        config={
            "configurable": {
                "thread_id": payload.thread_id
            }
        }
    )

    return {
        "answer": result.get("answer", ""),
        "sources": result.get("sources", []),
        "video_references": result.get("video_refs", [])
    }


# ---------------- STREAMING CHAT ----------------
async def stream_generator(question: str, thread_id: str) -> AsyncGenerator[str, None]:

    result = graph.invoke(
        {
            "question": question
        },
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    answer = result.get("answer", "")

    # streaming word-by-word (simple but interview-safe)
    for word in answer.split():
        yield word + " "


@router.post("/stream")
async def stream_chat(payload: ChatRequest):

    return StreamingResponse(
        stream_generator(payload.question, payload.thread_id),
        media_type="text/plain"
    )