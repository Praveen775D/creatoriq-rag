from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ---------------- CORE ----------------
    OPENAI_API_KEY: str

    # ---------------- LLM ----------------
    llm_model: str = "gpt-4o-mini"

    # ---------------- EMBEDDINGS ----------------
    embedding_model: str = "text-embedding-3-small"

    # ---------------- CHROMA ----------------
    chroma_persist_directory: str = "./chroma_db"
    chroma_collection: str = "videos"

    # ---------------- API ----------------
    next_public_api_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()