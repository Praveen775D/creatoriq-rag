# backend/app/api/ingest.py
from fastapi import APIRouter, HTTPException

from app.models.request_models import VideoIngestRequest

from app.services.youtube_service import YouTubeService
from app.services.instagram_service import InstagramService
from app.services.chunking_service import ChunkingService
from app.services.chroma_service import ChromaService

router = APIRouter()


@router.post("/")
async def ingest_videos(
    payload: VideoIngestRequest
):
    try:
        youtube_service = YouTubeService()
        instagram_service = InstagramService()

        chunker = ChunkingService()
        chroma = ChromaService()

        # Video A
        youtube_video = youtube_service.process_video(
            payload.youtube_url,
            "A"
        )

        # Video B
        instagram_video = instagram_service.process_reel(
            payload.instagram_url,
            "B"
        )

        # Chunk YouTube Transcript
        youtube_chunks = chunker.process_video(
            transcript=youtube_video.transcript,
            video_id="A",
            platform="youtube",
            creator=youtube_video.creator
        )

        # Chunk Instagram Transcript
        instagram_chunks = chunker.process_video(
            transcript=instagram_video.transcript,
            video_id="B",
            platform="instagram",
            creator=instagram_video.creator
        )

        # Store in ChromaDB
        chroma.add_documents(youtube_chunks)
        chroma.add_documents(instagram_chunks)

        return {
            "success": True,
            "message": "Videos processed and stored successfully",
            "video_a": youtube_video.model_dump(),
            "video_b": instagram_video.model_dump(),
            "youtube_chunks": len(youtube_chunks),
            "instagram_chunks": len(instagram_chunks)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )