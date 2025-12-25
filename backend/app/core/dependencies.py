"""
FastAPI dependency injection functions for database sessions and external service clients.
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from qdrant_client import QdrantClient
from cohere import AsyncClient as CohereAsyncClient
from fastapi import HTTPException, status

from app.core.config import get_settings
from app.models.database import get_db_session
from app.core.logging import get_logger

logger = get_logger(__name__)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting database session.

    Yields:
        AsyncSession: SQLAlchemy async database session

    Example:
        ```python
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()
        ```
    """
    settings = get_settings()

    if not settings.NEON_DATABASE_URL:
        logger.error("Database not configured: NEON_DATABASE_URL missing")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": {
                    "code": "SERVICE_UNAVAILABLE",
                    "message": "Database service not configured. Please set NEON_DATABASE_URL environment variable.",
                    "details": None
                }
            }
        )

    try:
        async for session in get_db_session():
            yield session
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": f"Database connection failed: {str(e)}",
                    "details": None
                }
            }
        )


def get_qdrant_client() -> QdrantClient:
    """
    Dependency for getting Qdrant client.

    Returns:
        QdrantClient: Configured Qdrant client instance

    Example:
        ```python
        @app.get("/search")
        async def search(qdrant: QdrantClient = Depends(get_qdrant_client)):
            results = qdrant.search(...)
            return results
        ```
    """
    settings = get_settings()

    if not settings.QDRANT_URL or not settings.QDRANT_API_KEY:
        logger.error("Qdrant not configured: QDRANT_URL or QDRANT_API_KEY missing")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": {
                    "code": "SERVICE_UNAVAILABLE",
                    "message": "Vector store service not configured. Please set QDRANT_URL and QDRANT_API_KEY environment variables.",
                    "details": None
                }
            }
        )

    try:
        return QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            timeout=settings.QDRANT_TIMEOUT_SECONDS,
        )
    except Exception as e:
        logger.error(f"Qdrant client initialization failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": {
                    "code": "VECTOR_STORE_ERROR",
                    "message": f"Vector store connection failed: {str(e)}",
                    "details": None
                }
            }
        )


def get_cohere_client() -> CohereAsyncClient:
    """
    Dependency for getting Cohere async client.

    Returns:
        CohereAsyncClient: Configured Cohere async client instance

    Example:
        ```python
        @app.post("/embed")
        async def embed_text(
            text: str,
            cohere: CohereAsyncClient = Depends(get_cohere_client)
        ):
            response = await cohere.embed(texts=[text])
            return response.embeddings[0]
        ```
    """
    settings = get_settings()

    if not settings.COHERE_API_KEY:
        logger.error("Cohere not configured: COHERE_API_KEY missing")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": {
                    "code": "SERVICE_UNAVAILABLE",
                    "message": "AI service not configured. Please set COHERE_API_KEY environment variable.",
                    "details": None
                }
            }
        )

    try:
        return CohereAsyncClient(
            api_key=settings.COHERE_API_KEY,
        )
    except Exception as e:
        logger.error(f"Cohere client initialization failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": {
                    "code": "AI_SERVICE_ERROR",
                    "message": f"AI service connection failed: {str(e)}",
                    "details": None
                }
            }
        )
