
# backend/app/services/chunking_service.py
from typing import List

from langchain.schema import Document
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)


class ChunkingService:
    """
    Handles transcript chunking
    before embedding and vector storage.
    """

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
    ) -> List[Document]:
        """
        Split transcript into chunks.
        """

        documents = (
            self.splitter.create_documents(
                texts=[transcript],
                metadatas=[metadata]
            )
        )

        return documents

    def process_video(
        self,
        transcript: str,
        video_id: str,
        platform: str,
        creator: str
    ) -> List[Document]:
        """
        Create chunked documents
        with source metadata.
        """

        metadata = {
            "video_id": video_id,
            "platform": platform,
            "creator": creator
        }

        chunks = self.chunk_transcript(
            transcript=transcript,
            metadata=metadata
        )

        # Add chunk ids for source citations
        for idx, chunk in enumerate(chunks):

            chunk.metadata["chunk_id"] = idx

            chunk.metadata["source"] = (
                f"Video {video_id} - Chunk {idx}"
            )

        return chunks