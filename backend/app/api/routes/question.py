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
def safe_answer_str(answer):
    """
    Ensure answer is always a readable string
    """
    if isinstance(answer, dict):
        return answer.get("text") or answer.get("content") or answer.get("message") or json.dumps(answer, indent=2)
    elif isinstance(answer, list):
        return "\n".join(map(str, answer))
    elif answer is None:
        return ""
    else:
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
            answer=safe_answer_str(response.answer),
            confidence=response.confidence,
            sources=response.sources,
            mode=getattr(response, "mode", None)
        )

    except Exception as e:
        logger.error(
            f"Failed to answer question: {str(e)}",
            extra={"error": str(e), "question": request.question[:100]}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to answer question: {str(e)}"
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
            answer=safe_answer_str(response.answer),
            confidence=getattr(response, "confidence", None),
            sources=getattr(response, "sources", []),
            mode=getattr(response, "mode", None)
        )

    except Exception as e:
        logger.error(
            f"Failed to answer selected text question: {str(e)}",
            extra={"error": str(e), "question": request.question[:100]}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to answer question: {str(e)}"
        )
