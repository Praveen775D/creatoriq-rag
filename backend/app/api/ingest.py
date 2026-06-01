from fastapi import APIRouter
from app.models.request_models import VideoIngestRequest

from app.services.youtube_service import YouTubeService
from app.services.instagram_service import InstagramService

router = APIRouter()


@router.post("/")
async def ingest_videos(
    payload: VideoIngestRequest
):

    youtube_service = YouTubeService()
    instagram_service = InstagramService()

    youtube_video = youtube_service.process_video(
        payload.youtube_url,
        "A"
    )

    instagram_video = instagram_service.process_reel(
        payload.instagram_url,
        "B"
    )

    return {
        "video_a": youtube_video.model_dump(),
        "video_b": instagram_video.model_dump()
    }