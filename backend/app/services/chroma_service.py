# backend/app/services/chroma_service.py
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings


class ChromaService:

    def __init__(self):

        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )

        self.vectorstore = Chroma(
            collection_name=settings.chroma_collection,
            embedding_function=self.embeddings,
            persist_directory=settings.chroma_persist_directory
        )

    def add_documents(self, documents):

        if not documents:
            return

        self.vectorstore.add_documents(documents)

    def similarity_search(
        self,
        query: str,
        k: int = 5
    ):
        return self.vectorstore.similarity_search(
            query=query,
            k=k
        )

    def retriever(self):

        return self.vectorstore.as_retriever(
            search_kwargs={"k": 5}
        )