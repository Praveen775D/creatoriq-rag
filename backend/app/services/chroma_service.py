# backend/app/services/chroma_service.py
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from app.core.config import settings


class ChromaService:

    def __init__(self):

        # EMBEDDINGS (REUSABLE)
        self.embeddings = OpenAIEmbeddings(
            api_key=settings.OPENAI_API_KEY,
            model=settings.embedding_model
        )

        # VECTOR DB
        self.vectorstore = Chroma(
            collection_name=settings.chroma_collection,
            embedding_function=self.embeddings,
            persist_directory=settings.chroma_persist_directory
        )

    
    # ADD DOCUMENTS
    
    def add_documents(self, documents):

        if not documents:
            return

        self.vectorstore.add_documents(documents)

        # optional persist (safe for interview demo)
        self.vectorstore.persist()

    
    # SIMILARITY SEARCH
    
    def similarity_search(self, query: str, k: int = 5):

        return self.vectorstore.similarity_search(
            query=query,
            k=k
        )

    
    # RETRIEVER (FOR LANGCHAIN/LANGGRAPH EXTENSION)
    
    def retriever(self):

        return self.vectorstore.as_retriever(
            search_kwargs={"k": 5}
        )