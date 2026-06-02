from pydantic import BaseModel
from typing import List


class VideoMetadata(BaseModel):
    video_id: str
    platform: str
    title: str
    creator: str
    views: int
    likes: int
    comments: int
    followers: int | None = None
    hashtags: List[str] = []
    upload_date: str | None = None
    duration: float | None = None
    engagement_rate: float
    transcript: str