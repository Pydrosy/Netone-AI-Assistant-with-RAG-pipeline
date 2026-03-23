from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import json
import asyncio
import time
import logging
from datetime import datetime

# Use the working direct pipeline
from ..core.rag_pipeline_direct import rag_pipeline
from ..models.database import SessionLocal, Conversation, Message, TrainingData
from ..models.schemas import ChatRequest, MessageResponse, ConversationResponse, FeedbackCreate
from ..utils.rate_limiter import rate_limit
from ..utils.session import get_or_create_session, hash_session_id

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
async def query(
    request: ChatRequest,
    http_request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """Query endpoint with conversation storage"""
    try:
        start_time = time.time()
        
        # Get or create session
        session_id = get_or_create_session(http_request, db)
        hashed_session = hash_session_id(session_id)
        
        # Get or create conversation
        conversation = None
        if request.conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == request.conversation_id
            ).first()
        
        if not conversation:
            # Create new conversation
            conversation = Conversation(
                session_id=hashed_session,
                title=request.message[:50] + ("..." if len(request.message) > 50 else ""),
                created_at=datetime.utcnow()
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        # Store user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=request.message,
            created_at=datetime.utcnow()
        )
        db.add(user_message)
        db.commit()
        db.refresh(user_message)
        
        # Generate response from RAG pipeline
        result = rag_pipeline.generate_response(request.message)
        
        # Calculate latency
        latency_ms = int((time.time() - start_time) * 1000)
        
        # Store assistant message
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=result["answer"],
            sources=result.get("sources", []),
            latency_ms=latency_ms,
            created_at=datetime.utcnow()
        )
        db.add(assistant_message)
        db.commit()
        db.refresh(assistant_message)
        
        # Store in training data table for future model improvement
        training_record = TrainingData(
            message_id=assistant_message.id,
            user_question=request.message,
            assistant_response=result["answer"],
            sources_used=result.get("sources", []),
            was_helpful=False,  # Will be updated with feedback
            created_at=datetime.utcnow()
        )
        db.add(training_record)
        db.commit()
        
        # Set session cookie
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            max_age=30*24*60*60,  # 30 days
            samesite="lax"
        )
        
        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "conversation_id": conversation.id,
            "message_id": assistant_message.id,
            "latency_ms": latency_ms
        }
        
    except Exception as e:
        logger.error(f"Error in query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream")
async def stream_chat(
    request: ChatRequest,
    http_request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """Stream chat responses using Server-Sent Events with storage"""
    try:
        start_time = time.time()
        
        # Get or create session
        session_id = get_or_create_session(http_request, db)
        hashed_session = hash_session_id(session_id)
        
        # Get or create conversation
        conversation = None
        if request.conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == request.conversation_id
            ).first()
        
        if not conversation:
            conversation = Conversation(
                session_id=hashed_session,
                title=request.message[:50] + ("..." if len(request.message) > 50 else ""),
                created_at=datetime.utcnow()
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        # Store user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=request.message,
            created_at=datetime.utcnow()
        )
        db.add(user_message)
        db.commit()
        
        # Set session cookie
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            max_age=30*24*60*60,
            samesite="lax"
        )
        
        async def event_generator():
            full_response = ""
            
            # Generate response (streaming)
            async for chunk in rag_pipeline.stream_response(request.message):
                full_response += chunk
                yield {
                    "event": "message",
                    "data": json.dumps({"chunk": chunk})
                }
            
            # Calculate latency
            latency_ms = int((time.time() - start_time) * 1000)
            
            # Store assistant message
            assistant_message = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=full_response,
                sources=[],  # Would need to capture sources separately
                latency_ms=latency_ms,
                created_at=datetime.utcnow()
            )
            db.add(assistant_message)
            db.commit()
            
            # Store in training data
            training_record = TrainingData(
                message_id=assistant_message.id,
                user_question=request.message,
                assistant_response=full_response,
                sources_used=[],
                was_helpful=False,
                created_at=datetime.utcnow()
            )
            db.add(training_record)
            db.commit()
            
            yield {
                "event": "complete",
                "data": json.dumps({
                    "conversation_id": conversation.id,
                    "message_id": assistant_message.id,
                    "latency_ms": latency_ms
                })
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
    """Submit feedback for a response and update training data"""
    try:
        # Get the message
        message = db.query(Message).filter(Message.id == feedback.message_id).first()
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        # Update message with feedback
        message.feedback_rating = feedback.rating
        if feedback.feedback_text:
            message.feedback_text = feedback.feedback_text
        
        # Update training data
        training_record = db.query(TrainingData).filter(
            TrainingData.message_id == feedback.message_id
        ).first()
        
        if training_record:
            training_record.was_helpful = feedback.rating >= 4  # 4-5 stars = helpful
            if feedback.feedback_text:
                training_record.user_rating = feedback.rating
        
        db.commit()
        
        return {
            "message": "Feedback submitted successfully",
            "rating": feedback.rating,
            "was_helpful": feedback.rating >= 4
        }
        
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations")
async def get_conversations(
    http_request: Request,
    db: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0
):
    """Get conversation history for current user/session"""
    try:
        session_id = get_or_create_session(http_request, db)
        hashed_session = hash_session_id(session_id)
        
        conversations = db.query(Conversation).filter(
            Conversation.session_id == hashed_session
        ).order_by(Conversation.updated_at.desc()).offset(offset).limit(limit).all()
        
        return [
            {
                "id": conv.id,
                "title": conv.title,
                "message_count": len(conv.messages),
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat()
            }
            for conv in conversations
        ]
        
    except Exception as e:
        logger.error(f"Error getting conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """Get full conversation with all messages"""
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()
        
        return {
            "id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at.isoformat(),
            "messages": [
                {
                    "id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "sources": msg.sources,
                    "feedback_rating": msg.feedback_rating,
                    "timestamp": msg.created_at.isoformat()
                }
                for msg in messages
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """Delete a conversation"""
    try:
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        db.delete(conversation)
        db.commit()
        
        return {"message": "Conversation deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))