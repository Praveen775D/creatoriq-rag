# backend/app/services/instagram_service.py
import re
from typing import Dict, Any, List, Optional

import yt_dlp
from loguru import logger

from app.models.video import VideoMetadata


class InstagramService:

   
    # SAFE INTEGER CONVERSION
   
    @staticmethod
    def safe_int(value: Any) -> int:
        try:
            if value is None:
                return 0

            if isinstance(value, str):
                value = value.replace(",", "").strip()

            return int(float(value))
        except Exception:
            return 0

   
    # FETCH INSTAGRAM METADATA
   
    @staticmethod
    def get_metadata(url: str) -> Dict[str, Any]:
        try:
            ydl_opts = {
                "quiet": True,
                "skip_download": True,
                "noplaylist": True,
                "extract_flat": False,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            return info if isinstance(info, dict) else {}

        except Exception as e:
            logger.error(f"Instagram metadata error: {e}")
            return {}

   
    # ENGAGEMENT RATE
   
    @staticmethod
    def calculate_engagement(
        likes: int,
        comments: int,
        views: int,
    ) -> float:

        if views <= 0:
            return 0.0

        return round(
            ((likes + comments) / views) * 100,
            2
        )

   
    # HASHTAGS
   
    @staticmethod
    def extract_hashtags(
        text: Optional[str]
    ) -> List[str]:

        if not text:
            return []

        hashtags = re.findall(
            r"#(\w+)",
            text
        )

        return hashtags

   
    # CREATOR NAME
   
    @staticmethod
    def extract_creator(
        metadata: Dict[str, Any]
    ) -> str:

        return (
            metadata.get("uploader")
            or metadata.get("creator")
            or metadata.get("channel")
            or metadata.get("uploader_id")
            or "Unknown Creator"
        )

   
    # PROCESS REEL
   
    def process_reel(
        self,
        url: str,
        video_label: str = "B",
    ):

        logger.info(
            f"Processing Instagram Reel {video_label}"
        )

        metadata = self.get_metadata(url)

        # FALLBACK IF yt-dlp RETURNS NOTHING
        
        if not metadata:

            return VideoMetadata(
                video_id=video_label,
                platform="instagram",
                title="Instagram Reel",
                creator="Unknown Creator",
                views=0,
                likes=0,
                comments=0,
                followers=0,
                hashtags=[],
                upload_date=None,
                duration=0,
                engagement_rate=0.0,
                transcript="",
            )

        # METRICS
        likes = self.safe_int(
            metadata.get("like_count")
            or metadata.get("likes")
        )

        comments = self.safe_int(
            metadata.get("comment_count")
            or metadata.get("comments")
        )

        views = self.safe_int(
            metadata.get("view_count")
            or metadata.get("play_count")
            or metadata.get("viewer_count")
            or metadata.get("video_view_count")
        )

        # FALLBACK VIEWS
        if views <= 0:
            views = (
                likes * 12
            ) + (
                comments * 25
            )

        engagement_rate = (
            self.calculate_engagement(
                likes,
                comments,
                views,
            )
        )

        creator = self.extract_creator(
            metadata
        )

        hashtags = self.extract_hashtags(
            metadata.get(
                "description",
                ""
            )
        )

        return VideoMetadata(
            video_id=video_label,
            platform="instagram",
            title=metadata.get(
                "title",
                "Instagram Reel",
            ),
            creator=creator,

            views=views,
            likes=likes,
            comments=comments,

            followers=0,

            hashtags=hashtags,

            upload_date=metadata.get(
                "upload_date"
            ),

            duration=self.safe_int(
                metadata.get(
                    "duration"
                )
            ),

            engagement_rate=engagement_rate,

            transcript="",
        )

