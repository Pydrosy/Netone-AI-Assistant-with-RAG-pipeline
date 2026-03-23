from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
import logging

from ..models.database import SessionLocal, Conversation, Message, TrainingData, Feedback
from ..models.schemas import TrainingDataResponse, TrainingDataApprove

router = APIRouter(prefix="/admin", tags=["Admin"])
logger = logging.getLogger(__name__)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/health")
async def admin_health():
    """Health check for admin endpoint"""
    return {"status": "admin endpoint healthy"}

@router.get("/analytics")
async def get_analytics(
    db: Session = Depends(get_db),
    days: int = Query(30, description="Number of days to analyze")
):
    """Get analytics for admin dashboard"""
    try:
        # Date range
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Total conversations
        total_conversations = db.query(func.count(Conversation.id)).scalar() or 0
        
        # Total messages
        total_messages = db.query(func.count(Message.id)).scalar() or 0
        
        # Average response time
        avg_latency = db.query(func.avg(Message.latency_ms)).filter(
            Message.latency_ms.isnot(None)
        ).scalar() or 0
        
        # Feedback distribution
        feedback_stats = db.query(
            Message.feedback_rating,
            func.count(Message.id)
        ).filter(
            Message.feedback_rating.isnot(None)
        ).group_by(Message.feedback_rating).all()
        
        # Most common questions (from training data)
        common_questions = db.query(
            TrainingData.user_question,
            func.count(TrainingData.id)
        ).group_by(
            TrainingData.user_question
        ).order_by(
            func.count(TrainingData.id).desc()
        ).limit(10).all()
        
        # Conversations by day (last N days)
        daily_conversations = db.query(
            func.date(Conversation.created_at),
            func.count(Conversation.id)
        ).filter(
            Conversation.created_at >= start_date
        ).group_by(
            func.date(Conversation.created_at)
        ).order_by(
            func.date(Conversation.created_at)
        ).all()
        
        # Helpful rate (messages with positive feedback)
        helpful_messages = db.query(func.count(Message.id)).filter(
            Message.feedback_rating >= 4
        ).scalar() or 0
        
        helpful_rate = (helpful_messages / total_messages * 100) if total_messages > 0 else 0
        
        # Documents count
        from ..models.database import Document
        total_documents = db.query(func.count(Document.id)).filter(
            Document.is_active == True
        ).scalar() or 0
        
        return {
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "total_documents": total_documents,
            "average_response_time_ms": round(avg_latency, 2),
            "helpful_rate": round(helpful_rate, 2),
            "feedback_distribution": {
                str(rating): count for rating, count in feedback_stats
            },
            "most_common_questions": [
                {"question": q[:100], "count": c} for q, c in common_questions[:5]
            ],
            "daily_conversations": [
                {"date": str(d), "count": c} for d, c in daily_conversations
            ]
        }
        
    except Exception as e:
        logger.error(f"Error in analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/training-data")
async def get_training_data(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    helpful_only: bool = False,
    unlabeled_only: bool = False,
    approved_only: bool = False
):
    """Get training data for review"""
    try:
        query = db.query(TrainingData)
        
        if helpful_only:
            query = query.filter(TrainingData.was_helpful == True)
        elif unlabeled_only:
            query = query.filter(TrainingData.was_helpful.is_(None))
        
        if approved_only:
            query = query.filter(TrainingData.is_approved == True)
        
        total = query.count()
        data = query.order_by(desc(TrainingData.created_at)).offset(offset).limit(limit).all()
        
        return {
            "total": total,
            "offset": offset,
            "limit": limit,
            "data": [
                {
                    "id": td.id,
                    "user_question": td.user_question,
                    "assistant_response": td.assistant_response,
                    "sources": td.sources_used,
                    "was_helpful": td.was_helpful,
                    "user_rating": td.user_rating,
                    "is_approved": td.is_approved,
                    "created_at": td.created_at.isoformat()
                }
                for td in data
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting training data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/training-data/{id}/approve")
async def approve_training_data(
    id: int,
    data: TrainingDataApprove,
    db: Session = Depends(get_db)
):
    """Approve and optionally improve training data"""
    try:
        training_record = db.query(TrainingData).filter(TrainingData.id == id).first()
        if not training_record:
            raise HTTPException(status_code=404, detail="Training record not found")
        
        training_record.is_approved = True
        if data.improved_response:
            training_record.improved_response = data.improved_response
        
        if data.tags:
            training_record.tags = data.tags
        
        db.commit()
        
        return {"message": "Training data approved", "id": id}
        
    except Exception as e:
        logger.error(f"Error approving training data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/training-data/{id}/reject")
async def reject_training_data(
    id: int,
    db: Session = Depends(get_db)
):
    """Reject training data (mark as not helpful)"""
    try:
        training_record = db.query(TrainingData).filter(TrainingData.id == id).first()
        if not training_record:
            raise HTTPException(status_code=404, detail="Training record not found")
        
        training_record.was_helpful = False
        db.commit()
        
        return {"message": "Training data rejected", "id": id}
        
    except Exception as e:
        logger.error(f"Error rejecting training data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations")
async def get_conversations(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session_id: Optional[str] = None
):
    """Get all conversations (admin view)"""
    try:
        query = db.query(Conversation)
        
        if session_id:
            query = query.filter(Conversation.session_id == session_id)
        
        total = query.count()
        conversations = query.order_by(desc(Conversation.created_at)).offset(offset).limit(limit).all()
        
        return {
            "total": total,
            "offset": offset,
            "limit": limit,
            "conversations": [
                {
                    "id": conv.id,
                    "session_id": conv.session_id,
                    "title": conv.title,
                    "user_id": conv.user_id,
                    "message_count": len(conv.messages),
                    "status": conv.status,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat()
                }
                for conv in conversations
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{conversation_id}")
async def get_conversation_detail(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """Get full conversation details with messages"""
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
            "session_id": conversation.session_id,
            "user_id": conversation.user_id,
            "title": conversation.title,
            "status": conversation.status,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "messages": [
                {
                    "id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "sources": msg.sources,
                    "feedback_rating": msg.feedback_rating,
                    "latency_ms": msg.latency_ms,
                    "created_at": msg.created_at.isoformat()
                }
                for msg in messages
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting conversation detail: {e}")
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

@router.get("/export/training")
async def export_training_data(
    db: Session = Depends(get_db),
    format: str = Query("json", regex="^(json|csv)$"),
    approved_only: bool = True
):
    """Export training data for model fine-tuning"""
    try:
        query = db.query(TrainingData)
        
        if approved_only:
            query = query.filter(TrainingData.is_approved == True)
        
        data = query.order_by(desc(TrainingData.created_at)).all()
        
        if format == "json":
            export_data = [
                {
                    "messages": [
                        {"role": "user", "content": td.user_question},
                        {"role": "assistant", "content": td.improved_response or td.assistant_response}
                    ],
                    "metadata": {
                        "sources": td.sources_used,
                        "rating": td.user_rating
                    }
                }
                for td in data
            ]
            
            return export_data
            
        else:  # CSV format
            import csv
            from fastapi.responses import StreamingResponse
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['user_question', 'assistant_response', 'sources', 'rating', 'approved'])
            
            for td in data:
                writer.writerow([
                    td.user_question,
                    td.improved_response or td.assistant_response,
                    json.dumps(td.sources_used),
                    td.user_rating or '',
                    td.is_approved
                ])
            
            output.seek(0)
            return StreamingResponse(
                iter([output.getvalue()]),
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=training_data.csv"}
            )
            
    except Exception as e:
        logger.error(f"Error exporting training data: {e}")
        raise HTTPException(status_code=500, detail=str(e))