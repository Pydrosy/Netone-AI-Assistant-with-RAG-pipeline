from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# ============ CHAT SCHEMAS ============

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    stream: bool = False

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]] = []
    conversation_id: Optional[int] = None
    message_id: Optional[int] = None
    latency_ms: Optional[int] = None

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    sources: Optional[List[Dict[str, Any]]] = None
    feedback_rating: Optional[int] = None
    latency_ms: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    title: Optional[str] = None
    session_id: Optional[str] = None
    user_id: Optional[int] = None
    message_count: Optional[int] = None
    status: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True

class ConversationListItem(BaseModel):
    id: int
    title: Optional[str] = None
    message_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============ FEEDBACK SCHEMAS ============

class FeedbackCreate(BaseModel):
    message_id: int
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    feedback_text: Optional[str] = Field(None, max_length=500)

class FeedbackResponse(BaseModel):
    id: int
    user_id: Optional[int]
    message_id: int
    rating: int
    feedback_text: Optional[str]
    category: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ============ TRAINING DATA SCHEMAS ============

class TrainingDataResponse(BaseModel):
    id: int
    message_id: Optional[int]
    user_question: str
    assistant_response: str
    sources_used: Optional[List[Dict[str, Any]]] = None
    was_helpful: Optional[bool] = None
    user_rating: Optional[int] = None
    improved_response: Optional[str] = None
    is_approved: bool = False
    tags: Optional[List[str]] = None
    created_at: datetime

    class Config:
        from_attributes = True

class TrainingDataApprove(BaseModel):
    improved_response: Optional[str] = Field(None, description="Admin-corrected response")
    tags: Optional[List[str]] = Field(None, description="Tags for categorization")

class TrainingDataExport(BaseModel):
    messages: List[Dict[str, str]]
    metadata: Dict[str, Any]


# ============ DOCUMENT SCHEMAS ============

class DocumentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., description="faq, product, technical, billing, policy, general")
    description: Optional[str] = Field(None, max_length=500)

class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = None
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None

class DocumentResponse(BaseModel):
    id: int
    title: str
    filename: str
    content_type: str
    category: str
    description: Optional[str]
    file_path: str
    chunk_count: int
    doc_metadata: Optional[Dict[str, Any]] = None
    created_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


# ============ ANALYTICS SCHEMAS ============

class AnalyticsResponse(BaseModel):
    total_conversations: int
    total_messages: int
    total_documents: int
    average_response_time_ms: float
    helpful_rate: float
    feedback_distribution: Dict[str, int]
    most_common_questions: List[Dict[str, Any]]
    daily_conversations: List[Dict[str, Any]]

class DailyConversation(BaseModel):
    date: str
    count: int

class CommonQuestion(BaseModel):
    question: str
    count: int


# ============ USER SCHEMAS ============

class UserCreate(BaseModel):
    email: str = Field(..., email=True)
    full_name: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=6)
    phone: Optional[str] = Field(None, max_length=20)
    account_number: Optional[str] = Field(None, max_length=50)

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    phone: Optional[str]
    account_number: Optional[str]
    service_plan: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    service_plan: Optional[str] = Field(None, max_length=100)


# ============ AUTH SCHEMAS ============

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None


# ============ RATE LIMIT SCHEMAS ============

class RateLimitStatus(BaseModel):
    allowed: bool
    remaining: int
    reset_seconds: int


# ============ HEALTH SCHEMAS ============

class HealthResponse(BaseModel):
    status: str
    rag_initialized: bool
    stats: Dict[str, Any]

class AdminHealthResponse(BaseModel):
    status: str
    timestamp: datetime


# ============ ERROR SCHEMAS ============

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    request_id: Optional[str] = None


# ============ PAGINATION SCHEMAS ============

class PaginatedResponse(BaseModel):
    total: int
    offset: int
    limit: int
    data: List[Any]


# ============ SESSION SCHEMAS ============

class SessionInfo(BaseModel):
    session_id: str
    created_at: datetime
    expires_at: datetime