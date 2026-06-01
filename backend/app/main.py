# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.ingest import router as ingest_router
from app.api.chat import router as chat_router

app = FastAPI(
    title="CreatorIQ RAG API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
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

app.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"]
)


@app.get("/")
async def root():
    return {
        "service": "CreatorIQ RAG",
        "status": "running"
    }