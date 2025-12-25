from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from app.api.routes import ingestion, question, health
from app.api.middleware.timing import TimingMiddleware
from app.api.middleware.error_handler import (
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler,
    service_exception_handler,
    ServiceError
)

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Physical AI RAG Backend",
    description="RAG chatbot backend for Physical AI textbook question answering",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add timing middleware
app.add_middleware(TimingMiddleware)

# Add exception handlers (order matters - most specific first)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ServiceError, service_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Simple root and health endpoints (no dependencies)
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Physical AI RAG Backend",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    """Simple health check without dependencies"""
    return {"status": "ok", "version": "0.1.0"}

# Include routers
# Note: Simple /health endpoint defined above, not using health.router to avoid dependencies
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


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("Starting Physical AI RAG Backend")
    logger.info(f"Environment: {settings.ENVIRONMENT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Shutting down Physical AI RAG Backend")

