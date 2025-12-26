"""Physical AI RAG Backend"""

from fastapi import FastAPI

# --------------------------------------------------
# App initialization (ONLY safe things at import time)
# --------------------------------------------------

app = FastAPI(
    title="Physical AI RAG Backend",
    version="0.1.0",
)

# --------------------------------------------------
# Health & root routes (MUST always work)
# --------------------------------------------------

@app.get("/health")
def health():
    # HF Free tier SAFE endpoint
    return {"status": "ok"}

@app.get("/")
def root():
    return {
        "service": "Physical AI RAG Backend",
        "version": "0.1.0",
    }

# --------------------------------------------------
# Startup logic (ALL heavy things go here)
# --------------------------------------------------

@app.on_event("startup")
async def startup():
    try:
        # --- Core imports (safe after server is alive) ---
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.exceptions import RequestValidationError, HTTPException

        from app.core.config import get_settings
        from app.core.logging import setup_logging, get_logger

        # --- Logging & settings ---
        setup_logging()
        logger = get_logger(__name__)
        settings = get_settings()

        # --- Middleware ---
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        from app.api.middleware.timing import TimingMiddleware
        from app.api.middleware.error_handler import (
            validation_exception_handler,
            http_exception_handler,
            general_exception_handler,
            service_exception_handler,
            ServiceError,
        )

        app.add_middleware(TimingMiddleware)
        app.add_exception_handler(RequestValidationError, validation_exception_handler)
        app.add_exception_handler(ServiceError, service_exception_handler)
        app.add_exception_handler(HTTPException, http_exception_handler)
        app.add_exception_handler(Exception, general_exception_handler)

        # --- API routes ---
        from app.api.routes import ingestion, question

        app.include_router(
            ingestion.router,
            prefix="/api/v1",
            tags=["Ingestion"],
        )
        app.include_router(
            question.router,
            prefix="/api/v1",
            tags=["Questions"],
        )

        logger.info("Backend started successfully")

    except Exception as e:
        # IMPORTANT: never crash startup on HF
        print(f"Startup error (non-fatal): {e}")

# --------------------------------------------------
# Shutdown
# --------------------------------------------------

@app.on_event("shutdown")
async def shutdown():
    try:
        from app.core.logging import get_logger
        logger = get_logger(__name__)
        logger.info("Backend shutdown")
    except Exception:
        pass
