# backend/app/api/chat.py

from typing import AsyncGenerator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.rag.graph import graph

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    thread_id: str = "default-thread"


@router.post("/")
async def chat(payload: ChatRequest):
    try:
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

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat failed: {str(e)}"
        )


async def stream_generator(
    question: str,
    thread_id: str
) -> AsyncGenerator[str, None]:

    try:
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

        for word in answer.split():
            yield word + " "

    except Exception as e:
        yield f"ERROR: {str(e)}"


@router.post("/stream")
async def stream_chat(payload: ChatRequest):

    return StreamingResponse(
        stream_generator(
            payload.question,
            payload.thread_id
        ),
        media_type="text/plain"
    )