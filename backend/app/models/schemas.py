from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Chat Schemas
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    stream: bool = False

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    sources: Optional[List[Dict[str, Any]]] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True

# Feedback Schemas
class FeedbackCreate(BaseModel):
    message_id: int
    rating: int  # 1-5
    feedback_text: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    user_id: Optional[int]
    message_id: int
    rating: int
    feedback_text: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Document Schemas
class DocumentCreate(BaseModel):
    title: str
    category: str
    description: Optional[str] = None

class DocumentResponse(BaseModel):
    id: int
    title: str
    filename: str
    content_type: str
    category: str
    description: Optional[str]
    file_path: str
    chunk_count: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# User Schemas (for reference)
class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    phone: Optional[str]
    account_number: Optional[str]
    service_plan: Optional[str]

    class Config:
        from_attributes = True
