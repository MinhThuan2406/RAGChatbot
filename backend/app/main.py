from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from contextlib import asynccontextmanager
from .core.config import settings
from starlette.middleware.cors import ALL_METHODS

if "PYTEST_CURRENT_TEST" not in os.environ:
    from .api import chat, ingest
    from .services.file_cleanup import delete_old_files_task

@asynccontextmanager
async def lifespan(app):
    if "PYTEST_CURRENT_TEST" not in os.environ:
        from threading import Thread
        import time
        def run_cleanup():
            while True:
                delete_old_files_task("/app/data/raw_docs", max_age_hours=24)
                time.sleep(3600)  
        Thread(target=run_cleanup, daemon=True).start()
    yield

app = FastAPI(
    title="RAG Chatbot API",
    description="Backend API for Retrieval-Augmented Generation Chatbot",
    version="0.1.0",
    lifespan=lifespan
)

def get_cors_origins():
    env_origins = os.getenv("CORS_ALLOW_ORIGIN", "http://localhost:3000")
    return [o.strip() for o in env_origins.split(",") if o.strip()]

cors_origins = get_cors_origins()

class DynamicCORSMiddleware(CORSMiddleware):
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            headers = dict(scope.get("headers", []))
            origin = headers.get(b"origin", b"").decode()
            if origin and origin.endswith(".ngrok-free.app") and origin not in cors_origins:
                cors_origins.append(origin)
        await super().__call__(scope, receive, send)

app.add_middleware(
    DynamicCORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if "PYTEST_CURRENT_TEST" not in os.environ:
    app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
    app.include_router(ingest.router, prefix="/api/ingest", tags=["Ingest"])


@app.get("/")
async def read_root():
    return {"message": "Welcome to the RAG Chatbot API!"}
