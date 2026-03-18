"""
NetOne AI Customer Assistant API
Main application entry point
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from typing import Dict

from .config import settings
from .api import chat, feedback, documents, admin
from .models.database import engine, Base
from .utils.logger import setup_logging

# Setup logging
setup_logging(settings.LOG_LEVEL, settings.LOG_FILE)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="RAG-powered AI Customer Assistant for NetOne Telecommunications",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and their processing time"""
    start_time = time.time()
    
    # Get request ID or generate one
    request_id = request.headers.get("X-Request-ID", str(time.time_ns()))
    
    # Log request
    logger.info(f"Request {request_id}: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Add custom headers
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request_id
        
        # Log response
        logger.info(
            f"Response {request_id}: {response.status_code} - {process_time:.3f}s"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error {request_id}: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "request_id": request_id
            }
        )

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check() -> Dict:
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.APP_VERSION,
        "service": settings.APP_NAME
    }

# Root endpoint
@app.get("/", tags=["Root"])
async def root() -> Dict:
    """Root endpoint with API information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "AI-powered customer service assistant",
        "documentation": "/api/docs",
        "health": "/health"
    }

# Include routers
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(feedback.router, prefix="/api", tags=["Feedback"])
app.include_router(documents.router, prefix="/api", tags=["Documents"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

# Startup event
@app.on_event("startup")
async def startup_event():
    """Actions to run on application startup"""
    logger.info("=" * 50)
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting...")
    logger.info(f"📡 Database: {settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}")
    logger.info(f"🔧 Debug mode: {settings.DEBUG}")
    logger.info("=" * 50)

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Actions to run on application shutdown"""
    logger.info("👋 Shutting down application...")