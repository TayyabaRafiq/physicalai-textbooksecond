"""
Request timing middleware.
Tracks and logs request processing time.
"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import get_logger

logger = get_logger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to track request processing time.
    Adds X-Process-Time header to responses.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Process request and track timing.

        Args:
            request: FastAPI request
            call_next: Next middleware/route handler

        Returns:
            Response with timing header
        """
        start_time = time.time()

        # Process request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time
        process_time_ms = int(process_time * 1000)

        # Add header to response
        response.headers["X-Process-Time"] = str(process_time_ms)

        # Log for monitoring (only log slow requests to reduce noise)
        if process_time_ms > 1000:  # Log if > 1 second
            logger.warning(
                f"Slow request: {request.method} {request.url.path}",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "process_time_ms": process_time_ms,
                    "status_code": response.status_code
                }
            )
        elif process_time_ms > 500:  # Log if > 500ms
            logger.info(
                f"Request: {request.method} {request.url.path}",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "process_time_ms": process_time_ms,
                    "status_code": response.status_code
                }
            )

        return response
