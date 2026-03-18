from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import json
import asyncio
import logging

# Use the working direct pipeline
from ..core.rag_pipeline_direct import rag_pipeline
from ..models.database import SessionLocal, Conversation, Message, User
from ..models.schemas import ChatRequest, MessageResponse, ConversationResponse, FeedbackCreate  # Added FeedbackCreate here
from ..utils.rate_limiter import rate_limit

router = APIRouter(prefix="/chat", tags=["Chat"])
logger = logging.getLogger(__name__)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/health")
async def chat_health():
    """Health check for chat endpoint"""
    return {
        "status": "healthy",
        "rag_initialized": rag_pipeline is not None,
        "stats": rag_pipeline.get_collection_stats()
    }

@router.post("/query")
async def query(request: ChatRequest):
    """Simple query endpoint (non-streaming)"""
    try:
        result = rag_pipeline.generate_response(request.message)
        return {
            "answer": result["answer"],
            "sources": result["sources"]
        }
    except Exception as e:
        logger.error(f"Error in query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream")
async def stream_chat(request: ChatRequest):
    """Stream chat responses using Server-Sent Events"""
    try:
        async def event_generator():
            # For now, just yield the full response (you can implement streaming later)
            result = rag_pipeline.generate_response(request.message)
            yield {
                "event": "message",
                "data": json.dumps({"chunk": result["answer"]})
            }
            yield {
                "event": "complete",
                "data": json.dumps({"sources": result["sources"]})
            }
        
        return EventSourceResponse(event_generator())
        
    except Exception as e:
        logger.error(f"Error in stream chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback")
async def submit_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db)
):
    """Submit feedback for a response"""
    # This would store feedback in database
    return {"message": "Feedback received"}