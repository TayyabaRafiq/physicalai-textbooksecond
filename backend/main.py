from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Physical AI RAG Backend",
    version="0.1.0",
)

# ✅ Middleware goes HERE (NOT in startup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Routes that MUST always work
# --------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {
        "service": "Physical AI RAG Backend",
        "version": "0.1.0",
    }

# --------------------------------------------------
# Startup (ONLY heavy logic, NO middleware)
# --------------------------------------------------

@app.on_event("startup")
async def startup():
    try:
        from app.core.config import get_settings
        from app.core.logging import setup_logging, get_logger

        setup_logging()
        logger = get_logger(__name__)
        settings = get_settings()

        # Routers
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
        print(f"Startup error: {e}")

@app.on_event("shutdown")
async def shutdown():
    pass
