from fastapi import APIRouter
from app.models.request_models import VideoIngestRequest

router = APIRouter()


@router.post("/")
async def ingest_videos(data: VideoIngestRequest):

    return {
        "message": "Ingestion endpoint ready",
        "youtube_url": data.youtube_url,
        "instagram_url": data.instagram_url
    }