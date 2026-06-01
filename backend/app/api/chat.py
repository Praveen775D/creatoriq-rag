from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.rag.graph import graph

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    thread_id: str = "default"


def generate_response(question, thread_id):

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

    yield result["answer"]


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