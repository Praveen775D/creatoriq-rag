from pydantic import BaseModel


class VideoIngestRequest(BaseModel):
    youtube_url: str
    instagram_url: str


class ChatRequest(BaseModel):
    question: str
    thread_id: str = "default"