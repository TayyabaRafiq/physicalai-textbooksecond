"""
FastAPI dependency injection functions for database sessions and external service clients.
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from qdrant_client import QdrantClient
from cohere import AsyncClient as CohereAsyncClient

from app.core.config import get_settings
from app.models.database import get_db_session


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
    async for session in get_db_session():
        yield session


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

    return QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        timeout=settings.QDRANT_TIMEOUT_SECONDS,
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

    return CohereAsyncClient(
        api_key=settings.COHERE_API_KEY,
    )
