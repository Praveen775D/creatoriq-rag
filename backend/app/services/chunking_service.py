from langchain.text_splitter import RecursiveCharacterTextSplitter


class ChunkingService:

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        self.splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=[
                    "\n\n",
                    "\n",
                    ". ",
                    " ",
                    ""
                ]
            )
        )

    def chunk_transcript(
        self,
        transcript: str,
        metadata: dict
    ):
        """
        Split transcript into chunks.
        """

        chunks = self.splitter.create_documents(
            [transcript],
            metadatas=[metadata]
        )

        return chunks

    def process_video(
        self,
        transcript: str,
        video_id: str,
        platform: str,
        creator: str
    ):

        metadata = {
            "video_id": video_id,
            "platform": platform,
            "creator": creator
        }

        chunks = self.chunk_transcript(
            transcript,
            metadata
        )

        return chunks