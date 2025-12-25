from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses Pydantic BaseSettings for validation and type checking.
    """

    # Cohere API Configuration
    COHERE_API_KEY: str
    COHERE_MODEL_EMBED: str = "embed-english-v3.0"
    COHERE_MODEL_GENERATE: str = "command-a-03-2025"

    # Qdrant Cloud Configuration
    QDRANT_API_KEY: str
    QDRANT_URL: str
    QDRANT_CLUSTER_ID: str | None = None
    QDRANT_COLLECTION_NAME: str = "textbook_chunks"

    # Neon Serverless Postgres Configuration
    NEON_DATABASE_URL: str

    # Application Configuration
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    API_RATE_LIMIT: int = 100
    INGESTION_RATE_LIMIT: int = 10

    # Chunking Configuration
    MAX_CHUNK_TOKENS: int = 1024

    # Performance Configuration
    EMBEDDING_TIMEOUT_SECONDS: int = 30
    GENERATION_TIMEOUT_SECONDS: int = 60
    QDRANT_TIMEOUT_SECONDS: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance to avoid re-reading environment variables.
    Use this function to get settings throughout the application.
    """
    return Settings()


# Global settings instance for backward compatibility
settings = get_settings()
