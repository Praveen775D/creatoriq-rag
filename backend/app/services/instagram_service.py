import re
from typing import Dict, Any, List

import yt_dlp
from loguru import logger

from app.models.video import VideoMetadata


class InstagramService:

    SHORTCODE_PATTERN = r"instagram\.com/(?:reel|p)/([^/?]+)"

    # -------------------------------------------------
    # SAFE INT (ROBUST FOR ALL EDGE CASES)
    # -------------------------------------------------
    @staticmethod
    def safe_int(value: Any) -> int:
        try:
            if value is None:
                return 0

            if isinstance(value, str):
                value = value.replace(",", "").strip()

            return int(float(value))
        except:
            return 0

    # -------------------------------------------------
    # SHORTCODE
    # -------------------------------------------------
    @classmethod
    def extract_shortcode(cls, url: str) -> str:
        match = re.search(cls.SHORTCODE_PATTERN, url)
        if not match:
            raise ValueError("Invalid Instagram URL")
        return match.group(1)

    # -------------------------------------------------
    # METADATA FETCH
    # -------------------------------------------------
    @staticmethod
    def get_metadata(url: str) -> Dict[str, Any]:
        try:
            with yt_dlp.YoutubeDL({
                "quiet": True,
                "skip_download": True,
                "noplaylist": True,
            }) as ydl:
                return ydl.extract_info(url, download=False)
        except Exception as e:
            logger.error(f"Instagram metadata error: {e}")
            return {}

    # -------------------------------------------------
    # ENGAGEMENT FORMULA
    # -------------------------------------------------
    @staticmethod
    def calculate_engagement(likes: int, comments: int, views: int) -> float:
        if not views or views <= 0:
            return 0.0

        return round(((likes + comments) / views) * 100, 2)

    # -------------------------------------------------
    # HASHTAGS
    # -------------------------------------------------
    @staticmethod
    def extract_hashtags(text: str) -> List[str]:
        if not text:
            return []
        return [w for w in text.split() if w.startswith("#")]

    # -------------------------------------------------
    # MAIN PROCESSOR
    # -------------------------------------------------
    def process_reel(self, url: str, video_label: str = "B"):

        logger.info(f"Processing Instagram Reel {video_label}")

        shortcode = self.extract_shortcode(url)
        metadata = self.get_metadata(url)

        # -----------------------------
        # MULTI-SOURCE EXTRACTION
        # -----------------------------
        likes = self.safe_int(
            metadata.get("like_count")
            or metadata.get("likes")
            or metadata.get("edge_media_preview_like")
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

        # -----------------------------
        # STRONG FALLBACK (IMPORTANT FIX)
        # -----------------------------
        if views <= 0:
            # safer estimation (prevents fake spikes)
            views = max(likes * 12, comments * 30, 1)

        # -----------------------------
        # ENGAGEMENT (ALWAYS SAFE)
        # -----------------------------
        engagement = self.calculate_engagement(likes, comments, views)

        # -----------------------------
        # CREATOR
        # -----------------------------
        creator = (
            metadata.get("uploader")
            or metadata.get("creator")
            or metadata.get("channel")
            or "Unknown Creator"
        )

        # -----------------------------
        # HASHTAGS
        # -----------------------------
        description = metadata.get("description", "")
        hashtags = self.extract_hashtags(description)

        # -----------------------------
        # FINAL SAFE OUTPUT
        # -----------------------------
        return VideoMetadata(
            video_id=video_label,
            platform="instagram",
            title=metadata.get("title", f"Instagram Reel {shortcode}"),
            creator=creator,

            views=int(views),
            likes=int(likes),
            comments=int(comments),

            followers=0,
            hashtags=hashtags,

            upload_date=metadata.get("upload_date"),
            duration=self.safe_int(metadata.get("duration")),

            # 🔥 GUARANTEED NEVER NaN
            engagement_rate=float(engagement or 0.0),

            transcript=""
        )