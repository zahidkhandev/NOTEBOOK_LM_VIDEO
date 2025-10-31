"""
Validation utilities for input validation and sanitization.

Provides validators for files, text, and configuration values.
"""

import logging
import mimetypes
from typing import Tuple, Optional

from app.config import settings
from app.core.constants import SUPPORTED_EXTENSIONS, FileType

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom validation error."""

    pass


def validate_file_upload(
    filename: str,
    file_size: int,
    content_type: str,
) -> Tuple[bool, Optional[str]]:
    """
    Validate uploaded file.

    Args:
        filename: File name
        file_size: File size in bytes
        content_type: MIME type

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        ```
        is_valid, error = validate_file_upload(
            "document.pdf",
            1024000,
            "application/pdf"
        )
        ```
    """
    try:
        # Check file size
        if file_size > settings.MAX_UPLOAD_SIZE:
            return False, "File exceeds maximum size limit"

        # Check file extension
        ext = filename.split(".")[-1].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            return False, f"Unsupported file type: {ext}"

        # Check MIME type
        supported_mimes = SUPPORTED_EXTENSIONS.get(ext, [])
        if content_type not in supported_mimes:
            logger.warning(f"⚠️  Unexpected MIME type: {content_type}")

        logger.info(f"✅ File validation passed: {filename}")
        return True, None

    except Exception as e:
        logger.error(f"❌ Validation error: {e}")
        return False, str(e)


def validate_duration(duration: int) -> Tuple[bool, Optional[str]]:
    """
    Validate video duration.

    Args:
        duration: Duration in seconds

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        ```
        is_valid, error = validate_duration(300)
        ```
    """
    try:
        if duration < 60:
            return False, "Duration must be at least 60 seconds"

        if duration > 600:
            return False, "Duration cannot exceed 600 seconds"

        return True, None

    except Exception as e:
        logger.error(f"❌ Duration validation error: {e}")
        return False, str(e)


def validate_text_length(
    text: str,
    min_length: int = 1,
    max_length: int = 10000,
) -> Tuple[bool, Optional[str]]:
    """
    Validate text length.

    Args:
        text: Text to validate
        min_length: Minimum length
        max_length: Maximum length

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        ```
        is_valid, error = validate_text_length(
            "Hello world",
            min_length=1,
            max_length=1000
        )
        ```
    """
    try:
        text_length = len(text.strip())

        if text_length < min_length:
            return False, f"Text must be at least {min_length} characters"

        if text_length > max_length:
            return False, f"Text cannot exceed {max_length} characters"

        return True, None

    except Exception as e:
        logger.error(f"❌ Text validation error: {e}")
        return False, str(e)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename

    Example:
        ```
        safe_name = sanitize_filename("My Document.pdf")
        ```
    """
    import re
    from datetime import datetime

    try:
        # Remove special characters
        safe_name = re.sub(r"[^\w\s.-]", "", filename)

        # Limit length
        if len(safe_name) > 200:
            name, ext = safe_name.rsplit(".", 1)
            safe_name = name[:195] + "." + ext

        # Add timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = safe_name.rsplit(".", 1)
        safe_name = f"{name}_{timestamp}.{ext}"

        logger.debug(f"✅ Sanitized filename: {safe_name}")
        return safe_name

    except Exception as e:
        logger.error(f"❌ Filename sanitization error: {e}")
        return filename
