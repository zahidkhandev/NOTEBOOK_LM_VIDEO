"""
Source document management endpoints.

Handles file uploads, extraction, storage, and management of source documents.
"""

import logging
import os
from typing import List, Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.core.constants import SourceStatus, ERROR_MESSAGES
from app.db.database import get_db
from app.models.source import Source
from app.utils.validators import validate_file_upload, sanitize_filename
from app.services.embedding_service import get_embedding_service

logger = logging.getLogger(__name__)

router = APIRouter()


class SourceSchema:
    """Source response schema."""

    def __init__(self, source: Source):
        self.id = source.id
        self.filename = source.filename
        self.file_type = source.file_type
        self.status = source.status
        self.word_count = source.word_count
        self.page_count = source.page_count
        self.created_at = source.created_at.isoformat()
        self.updated_at = source.updated_at.isoformat()

    def dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "file_type": self.file_type,
            "status": self.status,
            "word_count": self.word_count,
            "page_count": self.page_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


async def extract_content(file_path: str, file_type: str) -> tuple[str, int]:
    """
    Extract content from various file types.

    Args:
        file_path: Path to file
        file_type: File type (pdf, docx, txt)

    Returns:
        Tuple of (content, word_count)
    """
    try:
        content = ""
        word_count = 0

        if file_type == "txt":
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

        elif file_type == "pdf":
            try:
                import PyPDF2

                with open(file_path, "rb") as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    for page in pdf_reader.pages:
                        content += page.extract_text()
            except ImportError:
                logger.warning("PyPDF2 not installed, skipping PDF extraction")
                content = "[PDF content extraction not available]"

        elif file_type == "docx":
            try:
                from docx import Document

                doc = Document(file_path)
                for para in doc.paragraphs:
                    content += para.text + "\n"
            except ImportError:
                logger.warning("python-docx not installed, skipping DOCX extraction")
                content = "[DOCX content extraction not available]"

        word_count = len(content.split())
        return content, word_count

    except Exception as e:
        logger.error(f"❌ Content extraction failed: {e}")
        raise


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_source(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload a source document.

    Accepts PDF, DOCX, TXT files for processing.

    Args:
        file: Source document file
        db: Database session

    Returns:
        dict: Upload confirmation with source metadata

    Raises:
        HTTPException: If file validation fails

    Example:
        ```
        POST /api/sources/upload
        Content-Type: multipart/form-data

        {
            "file": <binary file data>
        }

        Response (201):
        {
            "id": 1,
            "filename": "document.pdf",
            "file_type": "pdf",
            "status": "processing",
            "message": "File uploaded successfully"
        }
        ```
    """
    try:
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES["invalid_file_type"],
            )

        # Validate file
        file_content = await file.read()
        file_size = len(file_content)
        file_ext = file.filename.split(".")[-1].lower()

        is_valid, error_msg = validate_file_upload(
            file.filename,
            file_size,
            file.content_type or "",
        )

        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg or ERROR_MESSAGES["invalid_file_type"],
            )

        logger.info(f"📁 Processing upload: {file.filename}")

        # Save file
        safe_filename = sanitize_filename(file.filename)
        file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)

        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(file_content)

        # Extract content
        content, word_count = await extract_content(file_path, file_ext)

        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES["no_content"],
            )

        # Create database record
        source = Source(
            filename=file.filename,
            file_type=file_ext,
            file_path=file_path,
            file_size=file_size,
            content=content,
            word_count=word_count,
            status=SourceStatus.READY.value,
        )

        db.add(source)
        db.commit()
        db.refresh(source)

        logger.info(f"✅ Source created: {source.id}")

        return {
            "id": source.id,
            "filename": source.filename,
            "file_type": source.file_type,
            "status": source.status,
            "word_count": source.word_count,
            "message": "File uploaded successfully",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Upload failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process upload",
        )


@router.get("/")
async def list_sources(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    List all uploaded sources.

    Args:
        skip: Number of records to skip
        limit: Number of records to return
        db: Database session

    Returns:
        dict: List of source documents

    Example:
        ```
        GET /api/sources/?skip=0&limit=10

        Response:
        {
            "sources": [
                {
                    "id": 1,
                    "filename": "document.pdf",
                    "status": "ready",
                    "word_count": 5000,
                    "created_at": "2025-10-31T23:00:00Z"
                }
            ],
            "total": 1,
            "skip": 0,
            "limit": 10
        }
        ```
    """
    try:
        logger.debug("Fetching sources list")

        query = db.query(Source).offset(skip).limit(limit)
        sources = query.all()
        total = db.query(Source).count()

        sources_list = [
            {
                "id": s.id,
                "filename": s.filename,
                "file_type": s.file_type,
                "status": s.status,
                "word_count": s.word_count,
                "created_at": s.created_at.isoformat(),
            }
            for s in sources
        ]

        return {
            "sources": sources_list,
            "total": total,
            "skip": skip,
            "limit": limit,
        }

    except Exception as e:
        logger.error(f"❌ Failed to list sources: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve sources",
        )


@router.get("/{source_id}")
async def get_source(
    source_id: int,
    db: Session = Depends(get_db),
):
    """
    Get source document details.

    Args:
        source_id: Source ID
        db: Database session

    Returns:
        dict: Source document metadata and content

    Raises:
        HTTPException: If source not found

    Example:
        ```
        GET /api/sources/1

        Response:
        {
            "id": 1,
            "filename": "document.pdf",
            "file_type": "pdf",
            "status": "ready",
            "file_size": 1024000,
            "word_count": 5000,
            "content_preview": "First 500 characters...",
            "created_at": "2025-10-31T23:00:00Z"
        }
        ```
    """
    try:
        logger.debug(f"Fetching source: {source_id}")

        source = db.query(Source).filter(Source.id == source_id).first()

        if not source:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Source not found",
            )

        return {
            "id": source.id,
            "filename": source.filename,
            "file_type": source.file_type,
            "status": source.status,
            "file_size": source.file_size,
            "word_count": source.word_count,
            "page_count": source.page_count,
            "content_preview": (source.content[:500] + "...") if source.content else None,
            "created_at": source.created_at.isoformat(),
            "updated_at": source.updated_at.isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get source: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve source",
        )


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(
    source_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a source document.

    Args:
        source_id: Source ID
        db: Database session

    Returns:
        None

    Raises:
        HTTPException: If deletion fails

    Example:
        ```
        DELETE /api/sources/1

        Response: 204 No Content
        ```
    """
    try:
        logger.info(f"🗑️  Deleting source: {source_id}")

        source = db.query(Source).filter(Source.id == source_id).first()

        if not source:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Source not found",
            )

        # Delete file
        if source.file_path and os.path.exists(source.file_path):
            os.remove(source.file_path)
            logger.debug(f"Deleted file: {source.file_path}")

        # Delete database record
        db.delete(source)
        db.commit()

        logger.info(f"✅ Source deleted: {source_id}")
        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to delete source: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete source",
        )


@router.post("/{source_id}/generate-embeddings", status_code=status.HTTP_202_ACCEPTED)
async def generate_embeddings(
    source_id: int,
    db: Session = Depends(get_db),
):
    """
    Generate embeddings for source document.

    Args:
        source_id: Source ID
        db: Database session

    Returns:
        dict: Job status

    Example:
        ```
        POST /api/sources/1/generate-embeddings

        Response (202):
        {
            "source_id": 1,
            "status": "processing",
            "message": "Embeddings generation started"
        }
        ```
    """
    try:
        logger.info(f"📊 Generating embeddings for source: {source_id}")

        source = db.query(Source).filter(Source.id == source_id).first()

        if not source:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Source not found",
            )

        if not source.content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Source has no content",
            )

        # Start embedding generation (would be in background in production)
        embedding_service = get_embedding_service()
        embedding = await embedding_service.embed_text(source.content)

        return {
            "source_id": source_id,
            "status": "processing",
            "message": "Embeddings generation started",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Embedding generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate embeddings",
        )
