from app.services.chunking_service import (
    ChunkingService
)

sample_text = """
This is a long transcript.
Imagine this transcript contains
a complete youtube video.
""" * 500

service = ChunkingService()

chunks = service.process_video(
    transcript=sample_text,
    video_id="A",
    platform="youtube",
    creator="Mr Beast"
)

print(
    f"Total chunks: {len(chunks)}"
)

print(chunks[0].page_content[:300])