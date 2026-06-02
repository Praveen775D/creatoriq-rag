# backend/app/api/ingest.py
from fastapi import APIRouter, HTTPException

from app.models.request_models import VideoIngestRequest
from app.services.youtube_service import YouTubeService
from app.services.instagram_service import InstagramService
from app.services.chunking_service import ChunkingService
from app.services.chroma_service import ChromaService

router = APIRouter()


@router.post("/")
async def ingest_videos(payload: VideoIngestRequest):
    try:
        # Initialize services
        youtube_service = YouTubeService()
        instagram_service = InstagramService()
        chunking_service = ChunkingService()
        chroma_service = ChromaService()

        # ==============================
        # Process YouTube Video (A)
        # ==============================
        youtube_video = youtube_service.process_video(
            url=payload.youtube_url,
            video_label="A"
        )

        # ==============================
        # Process Instagram Reel (B)
        # ==============================
        instagram_video = instagram_service.process_reel(
            url=payload.instagram_url,
            video_label="B"
        )

        # ==============================
        # Create Chunks
        # ==============================
        youtube_chunks = chunking_service.process_video(
            transcript=youtube_video.transcript,
            video_id="A",
            platform="youtube",
            creator=youtube_video.creator,
        )

        instagram_chunks = chunking_service.process_video(
            transcript=instagram_video.transcript,
            video_id="B",
            platform="instagram",
            creator=instagram_video.creator,
        )

        # ==============================
        # Store Chunks in ChromaDB
        # ==============================
        chroma_service.add_documents(youtube_chunks)
        chroma_service.add_documents(instagram_chunks)

        # ==============================
        # Response
        # ==============================
        return {
            "status": "success",
            "message": "Videos ingested successfully",
            "video_a": youtube_video.model_dump(),
            "video_b": instagram_video.model_dump(),
            "chunks_a": len(youtube_chunks),
            "chunks_b": len(instagram_chunks),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )