# backend/app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""

    llm_provider: str = "groq"
    llm_model: str = "llama-3.3-70b-versatile"

    embedding_model: str = "text-embedding-3-small"

    chroma_persist_directory: str = "./chroma_db"
    chroma_collection: str = "videos"

    next_public_api_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()