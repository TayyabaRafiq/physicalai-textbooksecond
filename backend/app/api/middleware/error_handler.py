"""
Error handling middleware and exception handlers.
Provides consistent error responses and validation error handling.
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from app.core.logging import get_logger

logger = get_logger(__name__)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle Pydantic validation errors with clear, user-friendly messages.

    Args:
        request: FastAPI request
        exc: Validation exception

    Returns:
        JSON response with validation error details
    """
    # Extract validation errors
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        errors.append({
            "field": field,
            "message": message,
            "type": error["type"]
        })

    logger.warning(
        f"Validation error on {request.url.path}",
        extra={
            "path": request.url.path,
            "errors": errors
        }
    )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": {
                    "errors": errors
                }
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle general uncaught exceptions.

    Args:
        request: FastAPI request
        exc: Exception

    Returns:
        JSON response with generic error message
    """
    logger.error(
        f"Unhandled exception on {request.url.path}: {str(exc)}",
        extra={
            "path": request.url.path,
            "error": str(exc),
            "error_type": type(exc).__name__
        },
        exc_info=True
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred. Please try again later.",
                "details": None
            }
        }
    )


class ServiceError(Exception):
    """Base exception for service-level errors"""
    def __init__(self, message: str, code: str = "SERVICE_ERROR", details: dict = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


class DatabaseError(ServiceError):
    """Database operation error"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="DATABASE_ERROR", details=details)


class EmbeddingError(ServiceError):
    """Embedding generation error"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="EMBEDDING_ERROR", details=details)


class VectorStoreError(ServiceError):
    """Vector store operation error"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="VECTOR_STORE_ERROR", details=details)


class GenerationError(ServiceError):
    """Answer generation error"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="GENERATION_ERROR", details=details)


class IngestionError(ServiceError):
    """Content ingestion error"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="INGESTION_ERROR", details=details)


async def service_exception_handler(request: Request, exc: ServiceError) -> JSONResponse:
    """
    Handle service-level exceptions.

    Args:
        request: FastAPI request
        exc: Service exception

    Returns:
        JSON response with service error details
    """
    logger.error(
        f"Service error on {request.url.path}: {exc.message}",
        extra={
            "path": request.url.path,
            "error_code": exc.code,
            "details": exc.details
        }
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )
