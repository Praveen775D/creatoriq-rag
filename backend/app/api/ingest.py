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
        youtube_service = YouTubeService()
        instagram_service = InstagramService()
        chunker = ChunkingService()
        chroma = ChromaService()

        # ---------------- FETCH DATA ----------------
        yt_video = youtube_service.process_video(payload.youtube_url, video_id="A")
        ig_video = instagram_service.process_reel(payload.instagram_url, video_id="B")

        # ---------------- CHUNKING ----------------
        yt_chunks = chunker.process_video(
            transcript=yt_video.transcript,
            video_id="A",
            platform="youtube",
            creator=yt_video.creator
        )

        ig_chunks = chunker.process_video(
            transcript=ig_video.transcript,
            video_id="B",
            platform="instagram",
            creator=ig_video.creator
        )

        # ---------------- STORE ----------------
        chroma.add_documents(yt_chunks)
        chroma.add_documents(ig_chunks)

        return {
            "status": "success",
            "message": "Videos ingested successfully",
            "data": {
                "video_a": yt_video.model_dump(),
                "video_b": ig_video.model_dump(),
                "chunks_a": len(yt_chunks),
                "chunks_b": len(ig_chunks)
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )