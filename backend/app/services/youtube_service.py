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
    - Calculate engagement metrics
    - Normalize output
    """

    VIDEO_ID_PATTERNS = [
        r"(?:v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:embed/)([A-Za-z0-9_-]{11})",
    ]

    @classmethod
    def extract_video_id(cls, url: str) -> str:
        """
        Extract YouTube video ID from multiple URL formats.
        """

        for pattern in cls.VIDEO_ID_PATTERNS:
            match = re.search(pattern, url)

            if match:
                return match.group(1)

        raise ValueError(f"Invalid YouTube URL: {url}")

    @staticmethod
    def get_transcript(video_id: str) -> str:
        """
        Retrieve transcript from YouTube.
        """

        try:
            transcript_data = YouTubeTranscriptApi().fetch(video_id)

            transcript_text = " ".join(
                chunk.text
                for chunk in transcript_data
            )

            return transcript_text

        except Exception as e:
            logger.warning(
                f"Transcript unavailable for {video_id}: {str(e)}"
            )
            return ""

    @staticmethod
    def get_metadata(url: str) -> Dict[str, Any]:
        """
        Retrieve metadata using yt-dlp.
        """

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "extract_flat": False,
            "noplaylist": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                metadata = ydl.extract_info(
                    url,
                    download=False
                )

            return metadata

        except Exception as e:
            logger.error(
                f"Metadata extraction failed: {str(e)}"
            )
            raise

    @staticmethod
    def calculate_engagement(
        likes: int,
        comments: int,
        views: int
    ) -> float:
        """
        Engagement Rate =
        (likes + comments) / views * 100
        """

        if not views:
            return 0.0

        return round(
            ((likes + comments) / views) * 100,
            2
        )

    @staticmethod
    def extract_hashtags(
        description: str
    ) -> List[str]:
        """
        Extract hashtags from description.
        """

        if not description:
            return []

        return [
            word.strip()
            for word in description.split()
            if word.startswith("#")
        ]

    def process_video(
        self,
        url: str,
        video_label: str = "A"
    ) -> VideoMetadata:
        """
        Complete ingestion workflow.
        """

        logger.info(
            f"Processing YouTube video: {url}"
        )

        video_id = self.extract_video_id(url)

        transcript = self.get_transcript(video_id)

        metadata = self.get_metadata(url)

        views = metadata.get(
            "view_count",
            0
        )

        likes = metadata.get(
            "like_count",
            0
        )

        comments = metadata.get(
            "comment_count",
            0
        )

        engagement_rate = (
            self.calculate_engagement(
                likes=likes,
                comments=comments,
                views=views,
            )
        )

        hashtags = self.extract_hashtags(
            metadata.get(
                "description",
                ""
            )
        )

        return VideoMetadata(
            video_id=video_label,
            platform="youtube",
            title=metadata.get(
                "title",
                ""
            ),
            creator=metadata.get(
                "channel",
                ""
            ),
            views=views,
            likes=likes,
            comments=comments,
            followers=metadata.get(
                "channel_follower_count"
            ),
            hashtags=hashtags,
            upload_date=metadata.get(
                "upload_date"
            ),
            duration=metadata.get(
                "duration"
            ),
            engagement_rate=engagement_rate,
            transcript=transcript,
        )