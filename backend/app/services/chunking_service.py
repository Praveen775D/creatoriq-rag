# backend/app/services/chunking_service.py
from typing import List, Dict
import hashlib

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkingService:
    """
    PRODUCTION RAG chunking service
    - Stable chunking
    - Dedup-safe hashes
    - Rich metadata for vector DB
    - Embedding-ready documents
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )


    # CLEAN TEXT (RAG OPTIMIZED)

    def _clean_transcript(self, transcript: str) -> str:
        if not transcript:
            return ""

        # remove extra spaces + normalize text
        return " ".join(transcript.split()).strip()


    # HASH (DEDUP + TRACEABILITY)

    def _make_hash(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()


    # CHUNK TRANSCRIPT

    def chunk_transcript(
        self,
        transcript: str,
        metadata: Dict
    ) -> List[Document]:

        transcript = self._clean_transcript(transcript)

        if not transcript:
            return []

        docs = self.splitter.create_documents(
            texts=[transcript],
            metadatas=[metadata]
        )

        return docs


    # PROCESS VIDEO (MAIN ENTRY)

    def process_video(
        self,
        transcript: str,
        video_id: str,
        platform: str,
        creator: str
    ) -> List[Document]:

        if not transcript:
            return []

        base_metadata = {
            "video_id": video_id,
            "platform": platform,
            "creator": creator
        }

        chunks = self.chunk_transcript(
            transcript=transcript,
            metadata=base_metadata
        )

        enriched: List[Document] = []

        for idx, chunk in enumerate(chunks):

            content = chunk.page_content

            # stable fingerprint for dedup + vector DB safety
            chunk_hash = self._make_hash(
                f"{video_id}|{platform}|{idx}|{content[:300]}"
            )

            chunk.metadata.update({
                "chunk_id": idx,
                "video_id": video_id,
                "platform": platform,
                "creator": creator,

                # useful for UI + tracing
                "source": f"{platform.upper()} Video {video_id}",
                "chunk_index": idx,
                "total_chunks_estimate": len(chunks),

                # vector DB optimization
                "char_count": len(content),
                "token_estimate": len(content.split()),

                # dedup key
                "chunk_hash": chunk_hash,

                # ranking boost fields (future RAG upgrade)
                "importance_score": 1.0
            })

            enriched.append(chunk)

        return enriched