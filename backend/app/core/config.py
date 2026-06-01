from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str

    CHROMA_COLLECTION: str = "creatoriq_videos"

    EMBEDDING_MODEL: str = "text-embedding-3-small"

    LLM_MODEL: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"


settings = Settings()