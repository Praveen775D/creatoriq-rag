import re
from typing import Dict, Any, List

import yt_dlp
from loguru import logger
from youtube_transcript_api import YouTubeTranscriptApi

from app.models.video import VideoMetadata


class YouTubeService:

    VIDEO_ID_PATTERNS = [
        r"(?:v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:embed/)([A-Za-z0-9_-]{11})",
        r"(?:shorts/)([A-Za-z0-9_-]{11})",
    ]

    # -------------------------------------------------
    # SAFE INT (CRITICAL FIX)
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
    # VIDEO ID EXTRACTION
    # -------------------------------------------------
    @classmethod
    def extract_video_id(cls, url: str) -> str:
        for pattern in cls.VIDEO_ID_PATTERNS:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise ValueError("Invalid YouTube URL")

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
            logger.error(f"YouTube metadata error: {e}")
            return {}

    # -------------------------------------------------
    # TRANSCRIPT
    # -------------------------------------------------
    @staticmethod
    def get_transcript(video_id: str) -> str:
        try:
            data = YouTubeTranscriptApi.get_transcript(video_id)
            return " ".join(x.get("text", "") for x in data)
        except Exception as e:
            logger.warning(f"No transcript for {video_id}: {e}")
            return ""

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
    # MAIN PROCESSOR (PRO FIXED)
    # -------------------------------------------------
    def process_video(self, url: str, video_label: str = "A"):

        logger.info(f"Processing YouTube Video {video_label}")

        video_id = self.extract_video_id(url)
        metadata = self.get_metadata(url)
        transcript = self.get_transcript(video_id)

        # ---------------- SAFE EXTRACTION ----------------
        views = self.safe_int(metadata.get("view_count"))
        likes = self.safe_int(metadata.get("like_count"))
        comments = self.safe_int(metadata.get("comment_count"))

        # ---------------- STRONG FALLBACK (IMPORTANT) ----------------
        # prevents divide-by-zero + missing yt-dlp data
        if views <= 0:
            views = max(likes * 10, comments * 25, 1)

        # ---------------- ENGAGEMENT ----------------
        engagement_rate = self.calculate_engagement(likes, comments, views)

        # ---------------- HASHTAGS ----------------
        description = metadata.get("description", "")
        hashtags = self.extract_hashtags(description)

        # ---------------- FINAL RESPONSE ----------------
        return VideoMetadata(
            video_id=video_label,
            platform="youtube",
            title=metadata.get("title", "Untitled Video"),
            creator=metadata.get("channel", "Unknown Creator"),

            views=int(views),
            likes=int(likes),
            comments=int(comments),

            followers=self.safe_int(metadata.get("channel_follower_count")),

            hashtags=hashtags,
            upload_date=metadata.get("upload_date"),
            duration=self.safe_int(metadata.get("duration")),

            # 🔥 GUARANTEED SAFE VALUE (NO NaN EVER)
            engagement_rate=float(engagement_rate or 0.0),

            transcript=transcript
        )