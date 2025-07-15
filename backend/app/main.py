from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os
if "PYTEST_CURRENT_TEST" not in os.environ:
    from .api import chat, ingest
from .core.config import settings

app = FastAPI(
    title="RAG Chatbot API",
    description="Backend API for Retrieval-Augmented Generation Chatbot",
    version="0.1.0",
)

# Configure CORS to allow communication from your frontend (OpenWebUI or Streamlit)
# Adjust allow_origins as needed for your frontend's URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust this to your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(ingest.router, prefix="/api/ingest", tags=["Ingest"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the RAG Chatbot API!"}

# Example of how to use settings
