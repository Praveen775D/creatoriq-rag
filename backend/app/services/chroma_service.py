from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from app.core.config import settings


class ChromaService:

    def __init__(self):

        self.vectorstore = Chroma(
            collection_name=settings.CHROMA_COLLECTION,
            embedding_function=OpenAIEmbeddings(
                api_key=settings.OPENAI_API_KEY,
                model=settings.EMBEDDING_MODEL
            ),
            persist_directory="./chroma_db"
        )

    def add_documents(
        self,
        documents
    ):
        self.vectorstore.add_documents(
            documents
        )

    def similarity_search(
        self,
        query: str,
        k: int = 5
    ):
        return self.vectorstore.similarity_search(
            query,
            k=k
        )

    def retriever(self):
        return self.vectorstore.as_retriever(
            search_kwargs={
                "k": 5
            }
        )