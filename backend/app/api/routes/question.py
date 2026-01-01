"""
Question answering API routes.
Handles full textbook and selected text question answering.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from qdrant_client import QdrantClient
from cohere import AsyncClient as CohereAsyncClient
import json

from app.models.requests import QuestionRequest, SelectedTextQuestionRequest
from app.models.responses import AnswerResponse
from app.services.question import QuestionService
from app.core.dependencies import get_db, get_qdrant_client, get_cohere_client
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter()

# ---------------------------
# Helper function
# ---------------------------
def normalize_answer(answer):
    """
    Normalize answer to always return a plain string.

    Args:
        answer: The answer to normalize (can be str, dict, list, or other)

    Returns:
        str: A readable string representation of the answer

    Examples:
        - String input: returns as-is
        - Dict input: extracts common text fields (text, content, message, answer)
        - List input: joins elements with newlines
        - None: returns empty string
        - Other: converts to string safely
    """
    # Already a string - return as-is
    if isinstance(answer, str):
        return answer

    # Dictionary - try common text field keys
    if isinstance(answer, dict):
        # Try common keys in order of preference
        for key in ["text", "content", "message", "answer"]:
            if key in answer and answer[key]:
                # Recursively normalize in case the value is also complex
                return normalize_answer(answer[key])
        # No common keys found - return formatted JSON
        return json.dumps(answer, indent=2)

    # List - join elements into readable string
    if isinstance(answer, list):
        if not answer:
            return ""
        return "\n".join(str(item) for item in answer)

    # None - return empty string
    if answer is None:
        return ""

    # Other types - safe string conversion
    return str(answer)

# ---------------------------
# Full textbook question endpoint
# ---------------------------
@router.post(
    "/question",
    response_model=AnswerResponse,
    summary="Ask a question about the textbook",
    description="""
    Ask a question and receive an answer based on the full textbook content.
    """
)
async def ask_question(
    request: QuestionRequest,
    http_request: Request,
    db: AsyncSession = Depends(get_db),
    qdrant_client: QdrantClient = Depends(get_qdrant_client),
    cohere_client: CohereAsyncClient = Depends(get_cohere_client)
) -> AnswerResponse:
    try:
        user_ip = http_request.client.host if http_request.client else None

        logger.info(
            "Received question",
            extra={
                "question": request.question[:100],
                "user_ip": user_ip
            }
        )

        question_service = QuestionService(
            db_session=db,
            qdrant_client=qdrant_client,
            cohere_client=cohere_client,
            user_ip=user_ip
        )

        response = await question_service.answer_question(request)

        logger.info(
            "Question answered successfully",
            extra={
                "question": request.question[:50],
                "confidence": response.confidence,
                "sources_count": len(response.sources)
            }
        )

        return AnswerResponse(
            answer=normalize_answer(response.answer),
            confidence=response.confidence,
            sources=response.sources,
            mode=getattr(response, "mode", None)
        )

    except Exception as e:
        error_msg = str(e)

        # Check for rate limiting errors
        if "429" in error_msg or "rate limit" in error_msg.lower() or "too many requests" in error_msg.lower():
            logger.warning(
                f"Rate limit hit for question: {request.question[:100]}",
                extra={"error": error_msg}
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Our AI service is experiencing high demand. Please wait a moment and try again."
            )

        logger.error(
            f"Failed to answer question: {error_msg}",
            extra={"error": error_msg, "question": request.question[:100]}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to answer question: {error_msg}"
        )

# ---------------------------
# Selected text question endpoint
# ---------------------------
@router.post(
    "/question/selected-text",
    response_model=AnswerResponse,
    summary="Ask a question about selected text",
    description="""
    Ask a question about user-selected text only.
    """
)
async def ask_about_selected_text(
    request: SelectedTextQuestionRequest,
    http_request: Request,
    db: AsyncSession = Depends(get_db),
    qdrant_client: QdrantClient = Depends(get_qdrant_client),
    cohere_client: CohereAsyncClient = Depends(get_cohere_client)
) -> AnswerResponse:
    try:
        user_ip = http_request.client.host if http_request.client else None

        logger.info(
            "Received selected text question",
            extra={
                "question": request.question[:100],
                "selected_text_length": len(request.selected_text),
                "user_ip": user_ip
            }
        )

        question_service = QuestionService(
            db_session=db,
            qdrant_client=qdrant_client,
            cohere_client=cohere_client,
            user_ip=user_ip
        )

        response = await question_service.answer_selected_text(request)

        logger.info(
            "Selected text question answered",
            extra={
                "question": request.question[:50],
                "mode": response.mode
            }
        )

        return AnswerResponse(
            answer=normalize_answer(response.answer),
            confidence=getattr(response, "confidence", None),
            sources=getattr(response, "sources", []),
            mode=getattr(response, "mode", None)
        )

    except Exception as e:
        error_msg = str(e)

        # Check for rate limiting errors
        if "429" in error_msg or "rate limit" in error_msg.lower() or "too many requests" in error_msg.lower():
            logger.warning(
                f"Rate limit hit for selected text question: {request.question[:100]}",
                extra={"error": error_msg}
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Our AI service is experiencing high demand. Please wait a moment and try again."
            )

        logger.error(
            f"Failed to answer selected text question: {error_msg}",
            extra={"error": error_msg, "question": request.question[:100]}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to answer question: {error_msg}"
        )
