from app.services.youtube_service import YouTubeService


def test_video():

    service = YouTubeService()

    result = service.process_video(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "A"
    )

    print(result)