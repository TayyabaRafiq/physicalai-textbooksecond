"""
Physical AI RAG Backend - FastAPI Application

CRITICAL: /health endpoint is defined first to ensure it's always available
even if downstream imports or initialization fail.
"""
from fastapi import FastAPI

# Create FastAPI app FIRST (before any imports that could fail)
app = FastAPI(
    title="Physical AI RAG Backend",
    description="RAG chatbot backend for Physical AI textbook question answering",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# CRITICAL: Define /health endpoint FIRST - must be 100% bulletproof
@app.get("/health")
async def health_check():
    """
    Bulletproof health check endpoint.
    Returns 200 OK even if all services are down.
    No dependencies, no imports, no settings required.
    """
    return {"status": "ok"}


# Root endpoint (also simple, no dependencies)
@app.get("/")
async def root():
    """Root endpoint - basic service info"""
    return {
        "service": "Physical AI RAG Backend",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs"
    }


# NOW safe to import and initialize everything else
# If any of these fail, /health and / will still work
initialization_successful = False
try:
    from fastapi import HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.exceptions import RequestValidationError
    from app.core.config import get_settings
    from app.core.logging import setup_logging, get_logger

    # Setup logging
    setup_logging()
    logger = get_logger(__name__)

    # Get settings
    settings = get_settings()

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify actual frontend domain
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Import middleware and error handlers
    from app.api.middleware.timing import TimingMiddleware
    from app.api.middleware.error_handler import (
        validation_exception_handler,
        http_exception_handler,
        general_exception_handler,
        service_exception_handler,
        ServiceError
    )

    # Add timing middleware
    app.add_middleware(TimingMiddleware)

    # Add exception handlers (order matters - most specific first)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ServiceError, service_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    # Import and include routers (these imports might fail if dependencies aren't configured)
    try:
        from app.api.routes import ingestion, question

        app.include_router(
            ingestion.router,
            prefix="/api/v1",
            tags=["Ingestion"]
        )
        app.include_router(
            question.router,
            prefix="/api/v1",
            tags=["Questions"]
        )
        print("✓ API routers loaded successfully")
    except Exception as router_error:
        print(f"⚠ Warning: Could not load API routers: {router_error}")
        print("  /health and / endpoints available, but /api/v1/* endpoints unavailable")

    @app.on_event("startup")
    async def startup_event():
        """Run on application startup"""
        try:
            logger.info("Starting Physical AI RAG Backend")
            logger.info(f"Environment: {settings.ENVIRONMENT}")
        except Exception as e:
            print(f"Warning: Startup event error: {e}")

    @app.on_event("shutdown")
    async def shutdown_event():
        """Run on application shutdown"""
        try:
            logger.info("Shutting down Physical AI RAG Backend")
        except Exception as e:
            print(f"Warning: Shutdown event error: {e}")

    initialization_successful = True
    logger.info("✓ Backend initialization successful")

except Exception as e:
    initialization_successful = False
    # If initialization fails, print to stdout (HF Spaces logs)
    # but /health and / endpoints will still work
    print(f"ERROR: Backend initialization failed: {e}")
    print("Service running in degraded mode - only /health and / endpoints available")
    import traceback
    traceback.print_exc()
