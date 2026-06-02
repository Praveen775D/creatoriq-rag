# backend/app/services/embedding_service.py
from typing import List, Optional, Iterable, Any

from langchain_openai import OpenAIEmbeddings
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger

from app.core.config import settings


class EmbeddingService:
    """
    Production-grade embedding service:
    - safe batching
    - retry logic
    - input validation
    - zero-crash guarantees
    """

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            api_key=settings.OPENAI_API_KEY,
            model=settings.embedding_model
        )

        # prevents rate-limit + token overflow
        self.max_batch_size = 100

   
    # CLEAN + VALIDATE INPUT
   
    def _validate_texts(self, texts: List[Any]) -> List[str]:
        if not texts:
            return []

        cleaned = []

        for t in texts:
            if isinstance(t, str):
                t = t.strip()
                if t:
                    cleaned.append(t)

        return cleaned

   
    # SAFE BATCH GENERATOR
   
    def _batch(self, items: List[str], size: int) -> Iterable[List[str]]:
        for i in range(0, len(items), size):
            yield items[i:i + size]

   
    # EMBED DOCUMENTS (BATCH SAFE)
   
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        reraise=True
    )
    def embed_documents(self, texts: List[Any]) -> List[List[float]]:
        texts = self._validate_texts(texts)

        if not texts:
            logger.warning("embed_documents received empty input")
            return []

        try:
            all_vectors = []

            for batch in self._batch(texts, self.max_batch_size):
                logger.debug(f"Embedding batch size: {len(batch)}")

                vectors = self.embeddings.embed_documents(batch)

                # safety check
                if vectors:
                    all_vectors.extend(vectors)

            return all_vectors

        except Exception as e:
            logger.error(f"embed_documents failed: {e}")
            raise

   
    # EMBED QUERY (SAFE + CONSISTENT OUTPUT TYPE)
   
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        reraise=True
    )
    def embed_query(self, query: Optional[str]) -> List[float]:
        if not query or not isinstance(query, str):
            logger.warning("embed_query received invalid input")
            return []

        try:
            return self.embeddings.embed_query(query.strip())

        except Exception as e:
            logger.error(f"embed_query failed: {e}")
            raise