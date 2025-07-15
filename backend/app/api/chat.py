from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
if "PYTEST_CURRENT_TEST" not in os.environ:
    from..services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService() # Only Ollama (Llama 3.2) is used

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

@router.post("/", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    import traceback
    try:
        response = await rag_service.answer_query(request.query)
        return ChatResponse(answer=response)
    except Exception as e:
        print("Exception in chat_with_bot:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{e}\n{traceback.format_exc()}")