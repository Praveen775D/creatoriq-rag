from langchain_openai import OpenAIEmbeddings

from app.core.config import settings


class EmbeddingService:

    def __init__(self):

        self.embeddings = OpenAIEmbeddings(
            api_key=settings.OPENAI_API_KEY,
            model=settings.embedding_model
        )

    def embed_documents(
        self,
        texts: list[str]
    ):
        return self.embeddings.embed_documents(
            texts
        )

    def embed_query(
        self,
        query: str
    ):
        return self.embeddings.embed_query(
            query
        )