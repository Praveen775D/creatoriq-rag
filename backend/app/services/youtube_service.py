# app/services/youtube_service.py

import re
from typing import Dict, Any, List

import yt_dlp
from loguru import logger
from youtube_transcript_api import YouTubeTranscriptApi

from app.models.video import VideoMetadata


class YouTubeService:
    """
    YouTube ingestion service.

    Responsibilities:
    - Extract video ID
    - Fetch transcript
    - Fetch metadata
    - Compute engagement rate
    - Normalize output into VideoMetadata
    """

    VIDEO_ID_PATTERNS = [
        r"(?:v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:embed/)([A-Za-z0-9_-]{11})",
    ]

    # -----------------------------
    # Extract Video ID
    # -----------------------------
    @classmethod
    def extract_video_id(cls, url: str) -> str:
        for pattern in cls.VIDEO_ID_PATTERNS:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        raise ValueError(f"Invalid YouTube URL: {url}")

    # -----------------------------
    # Fetch Transcript
    # -----------------------------
    @staticmethod
    def get_transcript(video_id: str) -> str:
        try:
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id)

            return " ".join(
                chunk["text"] for chunk in transcript_data
            )

        except Exception as e:
            logger.warning(f"No transcript for {video_id}: {str(e)}")
            return ""

    # -----------------------------
    # Fetch Metadata
    # -----------------------------
    @staticmethod
    def get_metadata(url: str) -> Dict[str, Any]:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "noplaylist": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)

        except Exception as e:
            logger.error(f"Metadata extraction failed: {str(e)}")
            raise

    # -----------------------------
    # Engagement Calculator
    # -----------------------------
    @staticmethod
    def calculate_engagement(likes: int, comments: int, views: int) -> float:
        if not views:
            return 0.0

        return round(((likes + comments) / views) * 100, 2)

    # -----------------------------
    # Hashtag Extractor
    # -----------------------------
    @staticmethod
    def extract_hashtags(description: str) -> List[str]:
        if not description:
            return []

        return [
            word.strip()
            for word in description.split()
            if word.startswith("#")
        ]

    # -----------------------------
    # Main Pipeline
    # -----------------------------
    def process_video(self, url: str, video_label: str = "A") -> VideoMetadata:

        logger.info(f"Processing YouTube video: {url}")

        video_id = self.extract_video_id(url)

        metadata = self.get_metadata(url)
        transcript = self.get_transcript(video_id)

        views = metadata.get("view_count", 0)
        likes = metadata.get("like_count", 0)
        comments = metadata.get("comment_count", 0)

        engagement_rate = self.calculate_engagement(
            likes=likes,
            comments=comments,
            views=views
        )

        hashtags = self.extract_hashtags(
            metadata.get("description", "")
        )

        return VideoMetadata(
            video_id=video_label,
            platform="youtube",
            title=metadata.get("title", ""),
            creator=metadata.get("channel", ""),
            views=views,
            likes=likes,
            comments=comments,
            followers=metadata.get("channel_follower_count"),
            hashtags=hashtags,
            upload_date=metadata.get("upload_date"),
            duration=metadata.get("duration"),
            engagement_rate=engagement_rate,
            transcript=transcript,
        )