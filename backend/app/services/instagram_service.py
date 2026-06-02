# backend/app/services/instagram_service.py
import re
from typing import Dict, Any, List

import yt_dlp
from loguru import logger

from app.models.video import VideoMetadata


class InstagramService:

    SHORTCODE_PATTERN = r"instagram\.com/(?:reel|p)/([^/?]+)"

    @classmethod
    def extract_shortcode(cls, url: str) -> str:

        match = re.search(
            cls.SHORTCODE_PATTERN,
            url
        )

        if not match:
            raise ValueError(
                f"Invalid Instagram URL: {url}"
            )

        return match.group(1)

    @staticmethod
    def get_metadata(url: str) -> Dict[str, Any]:

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(
                url,
                download=False
            )

    @staticmethod
    def calculate_engagement(
        likes: int,
        comments: int,
        views: int
    ) -> float:

        if views <= 0:
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

        logger.info(
            f"Processing Instagram Reel {video_label}"
        )

        shortcode = self.extract_shortcode(url)

        metadata = self.get_metadata(url)

        logger.info(metadata)

        views = int(
            metadata.get("view_count")
            or metadata.get("play_count")
            or metadata.get("viewer_count")
            or 0
        )

        likes = int(
            metadata.get("like_count")
            or 0
        )

        comments = int(
            metadata.get("comment_count")
            or 0
        )

        engagement_rate = self.calculate_engagement(
            likes,
            comments,
            views
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
            or metadata.get("uploader_id")
            or "Unknown Creator"
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
            followers=0,
            hashtags=hashtags,
            upload_date=metadata.get("upload_date"),
            duration=int(
                metadata.get("duration")
                or 0
            ),
            engagement_rate=engagement_rate,
            transcript=""
        )