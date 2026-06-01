# app/services/instagram_service.py

import re
from typing import Dict, Any, List

import yt_dlp
from loguru import logger

from app.models.video import VideoMetadata


class InstagramService:
    """
    Instagram Reel ingestion service.

    Responsibilities:
    - Extract reel shortcode
    - Fetch reel metadata
    - Calculate engagement
    - Normalize output to VideoMetadata schema
    """

    SHORTCODE_PATTERN = r"instagram\.com\/(?:reel|p)\/([^\/\?]+)"

    @classmethod
    def extract_shortcode(cls, url: str) -> str:
        """
        Extract Instagram Reel shortcode.
        """

        match = re.search(
            cls.SHORTCODE_PATTERN,
            url
        )

        if not match:
            raise ValueError(
                f"Invalid Instagram Reel URL: {url}"
            )

        return match.group(1)

    @staticmethod
    def get_metadata(url: str) -> Dict[str, Any]:
        """
        Fetch reel metadata using yt-dlp.
        """

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "extract_flat": False
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
                f"Instagram metadata extraction failed: {str(e)}"
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

        if not description:
            return []

        return [
            word.strip()
            for word in description.split()
            if word.startswith("#")
        ]

    def process_reel(
        self,
        url: str,
        video_label: str = "B"
    ) -> VideoMetadata:
        """
        Complete Instagram ingestion workflow.
        """

        logger.info(
            f"Processing Instagram Reel: {url}"
        )

        shortcode = self.extract_shortcode(url)

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
                views=views
            )
        )

        description = metadata.get(
            "description",
            ""
        )

        hashtags = self.extract_hashtags(
            description
        )

        creator = (
            metadata.get("uploader")
            or metadata.get("channel")
            or metadata.get("creator")
            or ""
        )

        return VideoMetadata(
            video_id=video_label,
            platform="instagram",
            title=metadata.get(
                "title",
                f"Instagram Reel {shortcode}"
            ),
            creator=creator,
            views=views,
            likes=likes,
            comments=comments,
            followers=None,
            hashtags=hashtags,
            upload_date=metadata.get(
                "upload_date"
            ),
            duration=metadata.get(
                "duration"
            ),
            engagement_rate=engagement_rate,
            transcript=""
        )