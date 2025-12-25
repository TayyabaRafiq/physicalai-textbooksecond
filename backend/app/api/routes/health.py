"""
Health check endpoint with graceful degradation.
Checks connectivity to all external services.
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from qdrant_client import QdrantClient
from cohere import AsyncClient as CohereAsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.dependencies import get_db, get_qdrant_client, get_cohere_client
from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


class ServiceStatus(BaseModel):
    """Individual service status"""
    available: bool
    message: str
    latency_ms: int | None = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str  # "healthy", "degraded", "unhealthy"
    version: str
    services: dict[str, ServiceStatus]


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="""
    Check the health status of the backend and all external services.

    Status levels:
    - `healthy`: All services are operational
    - `degraded`: Some services are unavailable but core functionality works
    - `unhealthy`: Critical services are down

    Returns 200 OK even in degraded state to allow partial functionality.
    """
)
async def health_check(
    db: AsyncSession = Depends(get_db),
    qdrant_client: QdrantClient = Depends(get_qdrant_client),
    cohere_client: CohereAsyncClient = Depends(get_cohere_client)
) -> HealthResponse:
    """
    Perform health check on all services.

    Args:
        db: Database session
        qdrant_client: Qdrant client
        cohere_client: Cohere client

    Returns:
        HealthResponse with status and service details
    """
    import time
    settings = get_settings()
    services = {}

    # Check Database (Neon Postgres)
    db_status = await _check_database(db)
    services["database"] = db_status

    # Check Qdrant
    qdrant_status = await _check_qdrant(qdrant_client)
    services["qdrant"] = qdrant_status

    # Check Cohere
    cohere_status = await _check_cohere(cohere_client)
    services["cohere"] = cohere_status

    # Determine overall status
    all_available = all(s.available for s in services.values())
    critical_available = services["cohere"].available  # Cohere is critical

    if all_available:
        overall_status = "healthy"
    elif critical_available:
        overall_status = "degraded"
    else:
        overall_status = "unhealthy"

    logger.info(
        f"Health check: {overall_status}",
        extra={
            "status": overall_status,
            "services": {k: v.available for k, v in services.items()}
        }
    )

    return HealthResponse(
        status=overall_status,
        version="0.1.0",
        services=services
    )


async def _check_database(db: AsyncSession) -> ServiceStatus:
    """Check database connectivity"""
    import time
    try:
        start = time.time()
        await db.execute(text("SELECT 1"))
        latency = int((time.time() - start) * 1000)

        return ServiceStatus(
            available=True,
            message="Database connection successful",
            latency_ms=latency
        )
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return ServiceStatus(
            available=False,
            message=f"Database connection failed: {str(e)}"
        )


async def _check_qdrant(client: QdrantClient) -> ServiceStatus:
    """Check Qdrant connectivity"""
    import time
    try:
        start = time.time()
        collections = client.get_collections()
        latency = int((time.time() - start) * 1000)

        return ServiceStatus(
            available=True,
            message=f"Qdrant available ({len(collections.collections)} collections)",
            latency_ms=latency
        )
    except Exception as e:
        logger.error(f"Qdrant health check failed: {str(e)}")
        return ServiceStatus(
            available=False,
            message=f"Qdrant connection failed: {str(e)}"
        )


async def _check_cohere(client: CohereAsyncClient) -> ServiceStatus:
    """Check Cohere API connectivity"""
    import time
    try:
        start = time.time()
        # Simple API call to check connectivity
        # Use a minimal embed request
        await client.embed(
            texts=["health check"],
            model="embed-english-v3.0",
            input_type="search_query",
            embedding_types=["float"]
        )
        latency = int((time.time() - start) * 1000)

        return ServiceStatus(
            available=True,
            message="Cohere API available",
            latency_ms=latency
        )
    except Exception as e:
        logger.error(f"Cohere health check failed: {str(e)}")
        return ServiceStatus(
            available=False,
            message=f"Cohere API connection failed: {str(e)}"
        )
