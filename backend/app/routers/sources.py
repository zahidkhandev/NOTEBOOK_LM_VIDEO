"""
Source document management endpoints - Tortoise ORM
Handles file uploads, extraction, storage, and management.
"""

import logging
import os
from typing import List, Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, status
import pdfplumber

from app.config import settings
from app.models.models import Source
from app.utils.validators import validate_file_upload, sanitize_filename
from app.services.embedding_service import get_embedding_service

logger = logging.getLogger(__name__)
router = APIRouter()


ERROR_MESSAGES = {
    "invalid_file_type": "Invalid file type. Supported: PDF, DOCX, TXT",
    "no_content": "No content could be extracted from file",
}


async def extract_content(file_path: str, file_type: str) -> tuple:
    """Extract content from various file types."""
    try:
        content = ""
        word_count = 0

        if file_type == "txt":
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="latin-1") as f:
                    content = f.read()

        elif file_type == "pdf":
            try:
                import PyPDF2
                with open(file_path, "rb") as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    for page in pdf_reader.pages:
                        text = page.extract_text()
                        if text:
                            text = text.replace('\x00', '').strip()
                            content += text + "\n"

                if not content or content.strip() == "":
                    logger.warning("⚠️ PyPDF2: No text, trying pdfplumber...")
                    try:
                        with pdfplumber.open(file_path) as pdf:
                            for page in pdf.pages:
                                text = page.extract_text()
                                if text:
                                    text = text.replace('\x00', '').strip()
                                    content += text + "\n"
                    except Exception as e:
                        logger.warning(f"pdfplumber failed: {e}")
                        content = "[PDF content extraction not available]"

            except Exception as pdf_error:
                logger.warning(f"PyPDF2 failed: {pdf_error}, trying pdfplumber...")
                try:
                    with pdfplumber.open(file_path) as pdf:
                        for page in pdf.pages:
                            text = page.extract_text()
                            if text:
                                text = text.replace('\x00', '').strip()
                                content += text + "\n"
                except Exception as e:
                    logger.error(f"❌ All PDF extraction failed: {e}")
                    content = "[PDF content extraction not available]"

        elif file_type == "docx":
            try:
                from docx import Document
                doc = Document(file_path)
                for para in doc.paragraphs:
                    content += para.text + "\n"
            except ImportError:
                logger.warning("python-docx not installed")
                content = "[DOCX content extraction not available]"
            except Exception as e:
                logger.error(f"DOCX extraction failed: {e}")
                content = "[DOCX content extraction not available]"

        word_count = len(content.split())
        return content, word_count

    except Exception as e:
        logger.error(f"❌ Content extraction failed: {e}")
        raise


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_source(file: UploadFile = File(...)):
    """Upload a source document. Accepts PDF, DOCX, TXT files."""
    try:
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES["invalid_file_type"],
            )

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

        safe_filename = sanitize_filename(file.filename)
        file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)

        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(file_content)

        # Extract content
        content, word_count = await extract_content(file_path, file_ext)

        # ✅ SANITIZE CONTENT
        if content:
            content = ''.join(
                char for char in content 
                if ord(char) > 31 or char in '\n\r\t'
            )
            content = content.replace('\x00', '').replace('\ufffd', '').strip()
            word_count = len(content.split())

        if not content or len(content.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES["no_content"],
            )

        # ✅ Create with Tortoise ORM
        source = await Source.create(
            filename=file.filename,
            file_type=file_ext,
            file_path=file_path,
            file_size=file_size,
            content=content,
            word_count=word_count,
            status="ready",
        )

        logger.info(f"✅ Source created: {source.id} - {word_count} words")

        return {
            "id": source.id,
            "filename": source.filename,
            "file_type": source.file_type,
            "status": source.status,
            "word_count": source.word_count,
            "file_size": source.file_size,
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
async def list_sources(skip: int = 0, limit: int = 100):
    """List all uploaded sources."""
    try:
        logger.debug("Fetching sources list")

        # ✅ Tortoise ORM
        sources = await Source.all().offset(skip).limit(limit)
        total = await Source.all().count()

        sources_list = [
            {
                "id": s.id,
                "filename": s.filename,
                "file_type": s.file_type,
                "status": s.status,
                "word_count": s.word_count,
                "file_size": s.file_size,
                "language": s.language,
                "page_count": s.page_count,
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
async def get_source(source_id: int):
    """Get source document details."""
    try:
        logger.debug(f"Fetching source: {source_id}")

        # ✅ Tortoise ORM
        source = await Source.get_or_none(id=source_id)

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
            "language": source.language,
            "summary": source.summary,
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
async def delete_source(source_id: int):
    """Delete a source document."""
    try:
        logger.info(f"🗑️ Deleting source: {source_id}")

        # ✅ Tortoise ORM
        source = await Source.get_or_none(id=source_id)

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
        await source.delete()

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
async def generate_embeddings(source_id: int):
    """Generate embeddings for source document."""
    try:
        logger.info(f"📊 Generating embeddings for source: {source_id}")

        # ✅ Tortoise ORM
        source = await Source.get_or_none(id=source_id)

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

        # ✅ USE EMBEDDING SERVICE
        embedding_service = get_embedding_service()
        embedding = await embedding_service.embed_text(source.content)

        return {
            "source_id": source_id,
            "status": "processing",
            "message": "Embeddings generation started",
            "embedding_dimension": len(embedding),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Embedding generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate embeddings",
        )
