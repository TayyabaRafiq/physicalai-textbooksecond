"""Physical AI RAG Backend"""
from fastapi import FastAPI

app = FastAPI(title="Physical AI RAG Backend", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"service": "Physical AI RAG Backend", "version": "0.1.0"}

# Initialize other components
try:
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.exceptions import RequestValidationError, HTTPException
    from app.core.config import get_settings
    from app.core.logging import setup_logging, get_logger

    setup_logging()
    logger = get_logger(__name__)
    settings = get_settings()

    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

    from app.api.middleware.timing import TimingMiddleware
    from app.api.middleware.error_handler import (validation_exception_handler, http_exception_handler, general_exception_handler, service_exception_handler, ServiceError)

    app.add_middleware(TimingMiddleware)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ServiceError, service_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    try:
        from app.api.routes import ingestion, question
        app.include_router(ingestion.router, prefix="/api/v1", tags=["Ingestion"])
        app.include_router(question.router, prefix="/api/v1", tags=["Questions"])
    except Exception as e:
        print(f"API routers unavailable: {e}")

    @app.on_event("startup")
    async def startup():
        try:
            logger.info("Backend started")
        except:
            pass

    @app.on_event("shutdown")
    async def shutdown():
        try:
            logger.info("Backend shutdown")
        except:
            pass

except Exception as e:
    print(f"Initialization error: {e}")
