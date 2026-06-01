from pydantic import BaseModel


class VideoIngestRequest(BaseModel):
    youtube_url: str
    instagram_url: str