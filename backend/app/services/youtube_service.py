# backend/app/services/youtube_service.py
import re
from typing import Any, Dict, List

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

    
    # SAFE INTEGER
    
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

    
    # VIDEO ID
    
    @classmethod
    def extract_video_id(cls, url: str) -> str:

        for pattern in cls.VIDEO_ID_PATTERNS:
            match = re.search(pattern, url)

            if match:
                return match.group(1)

        raise ValueError("Invalid YouTube URL")

    
    # METADATA
    
    @staticmethod
    def get_metadata(url: str) -> Dict[str, Any]:

        options = {
            "quiet": True,
            "skip_download": True,
            "noplaylist": True,
            "extract_flat": False,

            "extractor_args": {
                "youtube": {
                    "player_client": [
                        "android",
                        "web"
                    ]
                }
            }
        }

        try:
            with yt_dlp.YoutubeDL(options) as ydl:

                info = ydl.extract_info(
                    url,
                    download=False
                )

                if isinstance(info, dict):
                    return info

                return {}

        except Exception as e:

            logger.error(
                f"YouTube metadata error: {e}"
            )

            return {}

    
    # TRANSCRIPT
    
    @staticmethod
    def get_transcript(video_id: str) -> str:

        try:
            api = YouTubeTranscriptApi()

            transcript = api.fetch(video_id)

            text = " ".join(
                item.text
                for item in transcript
            )

            return text[:5000]

        except Exception as e:

            logger.warning(
                f"Transcript unavailable "
                f"for {video_id}: {e}"
            )

            return ""

    
    # ENGAGEMENT
    
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

    
    # HASHTAGS
    
    @staticmethod
    def extract_hashtags(
        description: str
    ) -> List[str]:

        if not description:
            return []

        return re.findall(
            r"#(\w+)",
            description
        )

    
    # PERFORMANCE SCORE
    
    @staticmethod
    def calculate_score(
        engagement_rate: float,
        views: int,
        likes: int,
        comments: int
    ) -> float:

        ratio = (
            likes + comments
        ) / max(views, 1)

        score = (
            engagement_rate * 0.5
            + ratio * 100 * 0.3
            + min(views / 50000, 20)
        )

        return round(score, 2)

    
    # MAIN PROCESSOR
    
    def process_video(
        self,
        url: str,
        video_label: str = "A"
    ):

        logger.info(
            f"Processing YouTube Video {video_label}"
        )

        video_id = self.extract_video_id(url)

        metadata = self.get_metadata(url)

        transcript = self.get_transcript(
            video_id
        )

        
        # METRICS
        

        views = self.safe_int(
            metadata.get("view_count")
        )

        likes = self.safe_int(
            metadata.get("like_count")
        )

        comments = self.safe_int(
            metadata.get("comment_count")
        )

        followers = self.safe_int(
            metadata.get(
                "channel_follower_count"
            )
        )

        
        # FALLBACK VIEWS
        

        if views <= 0:

            estimated_views = max(
                likes * 15,
                comments * 40,
                100
            )

            views = estimated_views

        
        # ENGAGEMENT
        

        engagement_rate = (
            self.calculate_engagement(
                likes,
                comments,
                views
            )
        )

        
        # CONTENT
        

        hashtags = self.extract_hashtags(
            metadata.get(
                "description",
                ""
            )
        )

        
        # SCORE
        

        performance_score = (
            self.calculate_score(
                engagement_rate,
                views,
                likes,
                comments
            )
        )

        
        # BADGE
        

        if engagement_rate >= 10:
            badge = "🔥 Viral"

        elif engagement_rate >= 5:
            badge = "⚡ High"

        elif engagement_rate >= 2:
            badge = "📊 Medium"

        else:
            badge = "📉 Low"

        
        # INSIGHT
        

        if engagement_rate >= 10:

            insight = (
                "Excellent engagement. "
                "Strong viral potential."
            )

        elif engagement_rate >= 5:

            insight = (
                "Good audience interaction."
            )

        else:

            insight = (
                "Needs stronger hook and "
                "better audience retention."
            )

        
        # BASIC INFO
        

        title = (
            metadata.get("title")
            or "Untitled Video"
        )

        creator = (
            metadata.get("channel")
            or metadata.get("uploader")
            or "Unknown Creator"
        )

        duration = self.safe_int(
            metadata.get("duration")
        )

        
        # RETURN MODEL
        

        return VideoMetadata(

            video_id=video_label,
            platform="youtube",

            title=title,
            creator=creator,

            views=views,
            likes=likes,
            comments=comments,

            followers=followers,

            hashtags=hashtags,

            upload_date=metadata.get(
                "upload_date"
            ),

            duration=duration,

            transcript=transcript,

            engagement_rate=engagement_rate,

            formatted_views=f"{views:,}",
            formatted_likes=f"{likes:,}",
            formatted_comments=f"{comments:,}",
            formatted_engagement=f"{engagement_rate:.2f}%",

            performance_score=performance_score,
            performance_badge=badge,
            quick_insight=insight,
        )