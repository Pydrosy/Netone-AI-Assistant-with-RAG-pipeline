from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/health")
async def admin_health():
    return {"status": "admin endpoint healthy"}