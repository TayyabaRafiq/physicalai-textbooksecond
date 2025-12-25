"""
Question answering API routes.
Handles full textbook and selected text question answering.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from qdrant_client import QdrantClient
from cohere import AsyncClient as CohereAsyncClient

from app.models.requests import QuestionRequest, SelectedTextQuestionRequest
from app.models.responses import AnswerResponse
from app.services.question import QuestionService
from app.core.dependencies import get_db, get_qdrant_client, get_cohere_client
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post(
    "/question",
    response_model=AnswerResponse,
    summary="Ask a question about the textbook",
    description="""
    Ask a question and receive an answer based on the full textbook content.

    The question answering process:
    1. Generates embedding for your question
    2. Retrieves top-k most relevant chunks using semantic search
    3. Generates a grounded answer using retrieved context
    4. Returns answer with source citations (module, chapter, section)

    The answer will:
    - Be grounded strictly in textbook content (no external knowledge)
    - Include source citations for verification
    - Indicate confidence level (high, medium, low)
    - Respond with "I cannot answer based on the textbook content" if no relevant info found
    """
)
async def ask_question(
    request: QuestionRequest,
    http_request: Request,
    db: AsyncSession = Depends(get_db),
    qdrant_client: QdrantClient = Depends(get_qdrant_client),
    cohere_client: CohereAsyncClient = Depends(get_cohere_client)
) -> AnswerResponse:
    """
    Answer a question using full textbook retrieval.

    Args:
        request: Question request
        http_request: HTTP request for IP extraction
        db: Database session
        qdrant_client: Qdrant client
        cohere_client: Cohere client

    Returns:
        AnswerResponse with answer and source citations
    """
    try:
        # Get user IP for logging
        user_ip = http_request.client.host if http_request.client else None

        logger.info(
            "Received question",
            extra={
                "question": request.question[:100],
                "user_ip": user_ip
            }
        )

        # Create question service
        question_service = QuestionService(
            db_session=db,
            qdrant_client=qdrant_client,
            cohere_client=cohere_client,
            user_ip=user_ip
        )

        # Answer question
        response = await question_service.answer_question(request)

        logger.info(
            f"Question answered successfully",
            extra={
                "question": request.question[:50],
                "confidence": response.confidence,
                "sources_count": len(response.sources)
            }
        )

        return response

    except Exception as e:
        logger.error(
            f"Failed to answer question: {str(e)}",
            extra={"error": str(e), "question": request.question[:100]}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to answer question: {str(e)}"
        )


@router.post(
    "/question/selected-text",
    response_model=AnswerResponse,
    summary="Ask a question about selected text",
    description="""
    Ask a question about user-selected text only (context-restricted mode).

    The question answering process:
    1. Uses ONLY the provided selected text as context
    2. Generates answer without any vector search or retrieval
    3. Returns answer marked as "selected_text" mode
    4. No source citations (since context is the selected text itself)

    The answer will:
    - Be strictly limited to the selected text provided
    - Not use any other textbook content
    - Respond with "I cannot answer based on the selected text alone" if insufficient info
    """
)
async def ask_about_selected_text(
    request: SelectedTextQuestionRequest,
    http_request: Request,
    db: AsyncSession = Depends(get_db),
    qdrant_client: QdrantClient = Depends(get_qdrant_client),
    cohere_client: CohereAsyncClient = Depends(get_cohere_client)
) -> AnswerResponse:
    """
    Answer a question about selected text only.

    Args:
        request: Selected text question request
        http_request: HTTP request for IP extraction
        db: Database session
        qdrant_client: Qdrant client (not used, but needed for service init)
        cohere_client: Cohere client

    Returns:
        AnswerResponse with answer (no source citations)
    """
    try:
        # Get user IP for logging
        user_ip = http_request.client.host if http_request.client else None

        logger.info(
            "Received selected text question",
            extra={
                "question": request.question[:100],
                "selected_text_length": len(request.selected_text),
                "user_ip": user_ip
            }
        )

        # Create question service
        question_service = QuestionService(
            db_session=db,
            qdrant_client=qdrant_client,
            cohere_client=cohere_client,
            user_ip=user_ip
        )

        # Answer question with selected text
        response = await question_service.answer_selected_text(request)

        logger.info(
            f"Selected text question answered",
            extra={
                "question": request.question[:50],
                "mode": response.mode
            }
        )

        return response

    except Exception as e:
        logger.error(
            f"Failed to answer selected text question: {str(e)}",
            extra={"error": str(e), "question": request.question[:100]}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to answer question: {str(e)}"
        )
