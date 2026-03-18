"""
Rate limiting middleware for FastAPI
"""

from fastapi import HTTPException, Request
from typing import Dict, Tuple
import time
from collections import defaultdict
import logging
from ..config import settings

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Simple in-memory rate limiter
    For production, use Redis-based implementation
    """
    
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> Tuple[bool, int]:
        """
        Check if request is allowed
        
        Args:
            key: Unique identifier (IP or user ID)
            max_requests: Maximum requests allowed in window
            window_seconds: Time window in seconds
            
        Returns:
            Tuple[bool, int]: (allowed, remaining_requests)
        """
        now = time.time()
        window_start = now - window_seconds
        
        # Clean old requests
        self.requests[key] = [req_time for req_time in self.requests[key] if req_time > window_start]
        
        # Check if under limit
        if len(self.requests[key]) < max_requests:
            self.requests[key].append(now)
            remaining = max_requests - len(self.requests[key])
            return True, remaining
        
        return False, 0
    
    def get_remaining(self, key: str, max_requests: int, window_seconds: int) -> int:
        """Get remaining requests for key"""
        now = time.time()
        window_start = now - window_seconds
        recent = [req_time for req_time in self.requests[key] if req_time > window_start]
        return max_requests - len(recent)

# Global rate limiter instance
rate_limiter = RateLimiter()

def rate_limit(max_requests: int = None, window_seconds: int = None):
    """
    Rate limiting decorator for FastAPI endpoints
    
    Args:
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds
    """
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            # Use settings if not provided
            limit = max_requests or settings.RATE_LIMIT_REQUESTS
            window = window_seconds or settings.RATE_LIMIT_PERIOD
            
            # Get client identifier (IP or user ID)
            client_id = request.client.host
            
            # Check if user is authenticated
            if hasattr(request, "user") and request.user:
                client_id = f"user_{request.user.id}"
            
            # Check rate limit
            allowed, remaining = rate_limiter.is_allowed(client_id, limit, window)
            
            if not allowed:
                logger.warning(f"Rate limit exceeded for {client_id}")
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests. Please try again later."
                )
            
            # Add rate limit headers to response
            response = await func(request, *args, **kwargs)
            
            if hasattr(response, "headers"):
                response.headers["X-RateLimit-Limit"] = str(limit)
                response.headers["X-RateLimit-Remaining"] = str(remaining)
                response.headers["X-RateLimit-Reset"] = str(int(time.time() + window))
            
            return response
        
        return wrapper
    
    return decorator