"""
Ingestion API routes.
Handles content ingestion requests and status checking.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from qdrant_client import QdrantClient
from cohere import AsyncClient as CohereAsyncClient

from app.models.requests import IngestionRequest
from app.models.responses import IngestionResponse, IngestionStatusResponse
from app.services.ingestion import IngestionService
from app.core.dependencies import get_db, get_qdrant_client, get_cohere_client
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post(
    "/ingestion",
    response_model=IngestionResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Ingest textbook content",
    description="""
    Ingest a textbook markdown file into the RAG system.

    The ingestion process:
    1. Parses markdown file into hierarchical structure (modules, chapters, sections)
    2. Chunks section content into semantically meaningful pieces (max 1024 tokens)
    3. Generates vector embeddings using Cohere
    4. Stores embeddings in Qdrant Cloud
    5. Stores metadata in Neon Postgres

    Returns a job ID that can be used to track ingestion progress.
    """
)
async def ingest_content(
    request: IngestionRequest,
    db: AsyncSession = Depends(get_db),
    qdrant_client: QdrantClient = Depends(get_qdrant_client),
    cohere_client: CohereAsyncClient = Depends(get_cohere_client)
) -> IngestionResponse:
    """
    Start content ingestion job.

    Args:
        request: Ingestion request with file path and module metadata
        db: Database session
        qdrant_client: Qdrant client
        cohere_client: Cohere client

    Returns:
        Ingestion response with job ID and status
    """
    try:
        logger.info(
            "Received ingestion request",
            extra={
                "file_path": request.file_path,
                "module_title": request.module_title
            }
        )

        # Create ingestion service
        ingestion_service = IngestionService(
            db_session=db,
            qdrant_client=qdrant_client,
            cohere_client=cohere_client
        )

        # Start ingestion (async processing would be better, but for MVP we'll do sync)
        job_id = await ingestion_service.ingest_file(request)

        logger.info(
            f"Ingestion job started: {job_id}",
            extra={"job_id": job_id}
        )

        return IngestionResponse(
            job_id=job_id,
            status="accepted",
            message=f"Ingestion job accepted. Check /api/v1/ingestion/status/{job_id} for progress."
        )

    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File not found: {request.file_path}"
        )

    except Exception as e:
        logger.error(
            f"Ingestion failed: {str(e)}",
            extra={"error": str(e)}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ingestion failed: {str(e)}"
        )


@router.get(
    "/ingestion/status/{job_id}",
    response_model=IngestionStatusResponse,
    summary="Get ingestion job status",
    description="""
    Check the status of an ingestion job.

    Status values:
    - `accepted`: Job has been accepted but not started
    - `processing`: Job is currently being processed
    - `completed`: Job completed successfully
    - `failed`: Job failed with an error
    """
)
async def get_ingestion_status(job_id: str) -> IngestionStatusResponse:
    """
    Get status of an ingestion job.

    Args:
        job_id: Job ID from ingestion request

    Returns:
        Ingestion status response
    """
    try:
        logger.info(f"Checking status for job: {job_id}")

        # Get job status from service
        job_status = IngestionService.get_job_status(job_id)

        if job_status is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job not found: {job_id}"
            )

        return IngestionStatusResponse(
            job_id=job_id,
            status=job_status["status"],
            message=job_status["message"],
            chunks_processed=job_status.get("chunks_processed"),
            error=job_status.get("error")
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(
            f"Failed to get job status: {str(e)}",
            extra={"error": str(e), "job_id": job_id}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get job status: {str(e)}"
        )
