from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.ingest import router as ingest_router

app = FastAPI(
    title="CreatorIQ RAG API",
    version="1.0.0"
)

app.include_router(
    health_router,
    prefix="/health",
    tags=["Health"]
)

app.include_router(
    ingest_router,
    prefix="/ingest",
    tags=["Ingest"]
)

@app.get("/")
async def root():
    return {
        "status": "running"
    }