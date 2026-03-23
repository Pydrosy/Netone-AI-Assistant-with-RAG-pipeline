import uuid
import hashlib
from fastapi import Request

def generate_session_id() -> str:
    """Generate a unique session ID for anonymous users"""
    return str(uuid.uuid4())

def get_or_create_session(request: Request, db) -> str:
    """Get existing session or create new one"""
    session_id = request.cookies.get("session_id")
    
    if not session_id:
        session_id = generate_session_id()
        
    return session_id

def hash_session_id(session_id: str) -> str:
    """Hash session ID for storage (security)"""
    return hashlib.sha256(session_id.encode()).hexdigest()[:32]