from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.get("/health")
async def documents_health():
    return {"status": "documents endpoint healthy"}