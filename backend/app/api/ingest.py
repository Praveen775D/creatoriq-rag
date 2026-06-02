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

        
        # SERVICES
        

        youtube_service = YouTubeService()
        instagram_service = InstagramService()

        chunking_service = ChunkingService()
        chroma_service = ChromaService()

        
        # PROCESS VIDEOS
        

        youtube_video = youtube_service.process_video(
            url=payload.youtube_url,
            video_label="A"
        )

        instagram_video = instagram_service.process_reel(
            url=payload.instagram_url,
            video_label="B"
        )

        
        # BUILD RAG KNOWLEDGE DOCUMENTS
        

        youtube_doc = f"""
VIDEO A

Platform: YouTube

Title: {youtube_video.title}

Creator: {youtube_video.creator}

Views: {youtube_video.views}

Likes: {youtube_video.likes}

Comments: {youtube_video.comments}

Followers: {youtube_video.followers}

Engagement Rate: {youtube_video.engagement_rate}%

Upload Date: {youtube_video.upload_date}

Duration: {youtube_video.duration} seconds

Hashtags:
{", ".join(youtube_video.hashtags) if youtube_video.hashtags else "None"}

Transcript:
{youtube_video.transcript if youtube_video.transcript else "Transcript unavailable"}

Analysis Notes:
Video A is a YouTube Short.
Current engagement rate is {youtube_video.engagement_rate}%.
Views = {youtube_video.views}
Likes = {youtube_video.likes}
Comments = {youtube_video.comments}
"""

        instagram_doc = f"""
VIDEO B

Platform: Instagram

Title: {instagram_video.title}

Creator: {instagram_video.creator}

Views: {instagram_video.views}

Likes: {instagram_video.likes}

Comments: {instagram_video.comments}

Followers: {instagram_video.followers}

Engagement Rate: {instagram_video.engagement_rate}%

Upload Date: {instagram_video.upload_date}

Duration: {instagram_video.duration} seconds

Hashtags:
{", ".join(instagram_video.hashtags) if instagram_video.hashtags else "None"}

Transcript:
{instagram_video.transcript if instagram_video.transcript else "Transcript unavailable"}

Analysis Notes:
Video B is an Instagram Reel.
Current engagement rate is {instagram_video.engagement_rate}%.
Views = {instagram_video.views}
Likes = {instagram_video.likes}
Comments = {instagram_video.comments}
"""

        
        # CHUNK DOCUMENTS
        

        youtube_chunks = chunking_service.process_video(
            transcript=youtube_doc,
            video_id="A",
            platform="youtube",
            creator=youtube_video.creator,
        )

        instagram_chunks = chunking_service.process_video(
            transcript=instagram_doc,
            video_id="B",
            platform="instagram",
            creator=instagram_video.creator,
        )

        
        # COMBINE DOCUMENTS
        

        all_chunks = []

        if youtube_chunks:
            all_chunks.extend(youtube_chunks)

        if instagram_chunks:
            all_chunks.extend(instagram_chunks)

        
        # STORE TO CHROMA
        

        if all_chunks:
            chroma_service.add_documents(all_chunks)

        
        # RESPONSE
        

        return {
            "status": "success",
            "message": "Videos ingested successfully",

            "video_a": youtube_video.model_dump(),
            "video_b": instagram_video.model_dump(),

            "chunks_a": len(youtube_chunks),
            "chunks_b": len(instagram_chunks),
            "total_chunks": len(all_chunks)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )