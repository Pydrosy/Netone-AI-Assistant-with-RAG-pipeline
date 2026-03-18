from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.get("/health")
async def feedback_health():
    return {"status": "feedback endpoint healthy"}