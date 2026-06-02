# backend/app/services/chroma_service.py
from typing import List, Optional, Dict, Any

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from loguru import logger

from app.core.config import settings


class ChromaService:

    def __init__(self):

        try:
            
            # EMBEDDINGS
            
            self.embeddings = HuggingFaceEmbeddings(
                model_name=getattr(
                    settings,
                    "embedding_model_hf",
                    "BAAI/bge-small-en-v1.5"
                )
            )

            
            # VECTOR STORE
            
            self.vectorstore = Chroma(
                collection_name=settings.chroma_collection,
                embedding_function=self.embeddings,
                persist_directory=settings.chroma_persist_directory
            )

            logger.info(" Chroma initialized successfully")

        except Exception as e:
            logger.error(f" Chroma init failed: {e}")
            raise

    
    # ADD DOCUMENTS
    
    def add_documents(self, documents: List[Any]):

        if not documents:
            logger.warning("No documents to add to Chroma")
            return

        try:
            logger.info(f"Adding {len(documents)} documents to Chroma")

            self.vectorstore.add_documents(documents)

            # safer persistence handling
            if hasattr(self.vectorstore, "persist"):
                self.vectorstore.persist()

        except Exception as e:
            logger.error(f"Chroma add_documents failed: {e}")
            raise

    
    # SAFE SIMILARITY SEARCH
    
    def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter: Optional[Dict[str, Any]] = None
    ):

        if not query or not query.strip():
            return []

        try:
            return self.vectorstore.similarity_search(
                query=query,
                k=k,
                filter=filter
            )

        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
            return []

    
    # MMR SEARCH
    
    def similarity_search_mmr(
        self,
        query: str,
        k: int = 5,
        fetch_k: int = 20,
        lambda_mult: float = 0.5,
        filter: Optional[Dict[str, Any]] = None
    ):

        if not query or not query.strip():
            return []

        try:
            return self.vectorstore.max_marginal_relevance_search(
                query=query,
                k=k,
                fetch_k=fetch_k,
                lambda_mult=lambda_mult,
                filter=filter
            )

        except Exception as e:
            logger.error(f"MMR search failed: {e}")
            return []

    
    # RETRIEVER
    
    def retriever(
        self,
        k: int = 5,
        search_type: str = "similarity"
    ):

        try:
            if search_type == "mmr":
                return self.vectorstore.as_retriever(
                    search_type="mmr",
                    search_kwargs={
                        "k": k,
                        "fetch_k": 20,
                        "lambda_mult": 0.5
                    }
                )

            return self.vectorstore.as_retriever(
                search_kwargs={"k": k}
            )

        except Exception as e:
            logger.error(f"Retriever creation failed: {e}")
            return None

    
    # FILTERED RETRIEVAL
    
    def retrieve_by_metadata(
        self,
        query: str,
        metadata_filter: Dict[str, Any],
        k: int = 5
    ):

        if not query or not query.strip():
            return []

        try:
            return self.vectorstore.similarity_search(
                query=query,
                k=k,
                filter=metadata_filter
            )

        except Exception as e:
            logger.error(f"Filtered retrieval failed: {e}")
            return []