from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter()


@router.post("/upload")
async def upload_source(file: UploadFile = File(...)):
    """Upload a source document (PDF, DOCX, TXT)"""
    return {
        "message": "Source uploaded successfully",
        "filename": file.filename,
        "content_type": file.content_type,
    }


@router.get("/")
async def list_sources():
    """List all uploaded sources"""
    return {"sources": []}


@router.get("/{source_id}")
async def get_source(source_id: int):
    """Get a specific source"""
    return {"source_id": source_id}


@router.delete("/{source_id}")
async def delete_source(source_id: int):
    """Delete a source"""
    return {"message": "Source deleted"}
