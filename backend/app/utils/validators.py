"""
Input validation utilities.
Provides validation functions for sanitizing and validating user inputs.
"""
import re
from pathlib import Path
from typing import Tuple


def validate_question_length(question: str, min_length: int = 5, max_length: int = 500) -> Tuple[bool, str]:
    """
    Validate question length.

    Args:
        question: Question text
        min_length: Minimum allowed length
        max_length: Maximum allowed length

    Returns:
        Tuple of (is_valid, error_message)
    """
    length = len(question.strip())

    if length < min_length:
        return False, f"Question must be at least {min_length} characters long"

    if length > max_length:
        return False, f"Question must not exceed {max_length} characters"

    return True, ""


def validate_selected_text_length(text: str, min_length: int = 10, max_length: int = 5000) -> Tuple[bool, str]:
    """
    Validate selected text length.

    Args:
        text: Selected text
        min_length: Minimum allowed length
        max_length: Maximum allowed length

    Returns:
        Tuple of (is_valid, error_message)
    """
    length = len(text.strip())

    if length < min_length:
        return False, f"Selected text must be at least {min_length} characters long"

    if length > max_length:
        return False, f"Selected text must not exceed {max_length} characters"

    return True, ""


def sanitize_markdown(content: str) -> str:
    """
    Sanitize markdown content to prevent injection attacks.

    Args:
        content: Raw markdown content

    Returns:
        Sanitized markdown content

    Note:
        This is a basic sanitization. For production, consider using
        a library like bleach or markdown-it with proper configuration.
    """
    # Remove null bytes
    content = content.replace('\x00', '')

    # Normalize line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')

    # Remove excessive whitespace
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    return content


def validate_file_path(file_path: str, allowed_extensions: list[str] = None) -> Tuple[bool, str]:
    """
    Validate file path for security and correctness.

    Args:
        file_path: File path to validate
        allowed_extensions: List of allowed file extensions (e.g., ['.md', '.txt'])

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file_path or not file_path.strip():
        return False, "File path cannot be empty"

    # Check for path traversal attempts
    if '..' in file_path or file_path.startswith('/'):
        return False, "Invalid file path: path traversal not allowed"

    # Check for null bytes
    if '\x00' in file_path:
        return False, "Invalid file path: null bytes not allowed"

    # Validate file extension if specified
    if allowed_extensions:
        path = Path(file_path)
        if path.suffix.lower() not in allowed_extensions:
            return False, f"Invalid file extension. Allowed: {', '.join(allowed_extensions)}"

    return True, ""


def validate_module_title(title: str) -> Tuple[bool, str]:
    """
    Validate module title.

    Args:
        title: Module title

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not title or not title.strip():
        return False, "Module title cannot be empty"

    if len(title) > 255:
        return False, "Module title must not exceed 255 characters"

    # Check for valid characters (alphanumeric, spaces, basic punctuation)
    if not re.match(r'^[\w\s\-:,.\'"()]+$', title):
        return False, "Module title contains invalid characters"

    return True, ""


def validate_module_order(order: int) -> Tuple[bool, str]:
    """
    Validate module order.

    Args:
        order: Module order number

    Returns:
        Tuple of (is_valid, error_message)
    """
    if order < 1:
        return False, "Module order must be a positive integer"

    if order > 1000:
        return False, "Module order must not exceed 1000"

    return True, ""


def sanitize_user_input(text: str, max_length: int = 10000) -> str:
    """
    Sanitize general user input.

    Args:
        text: User input text
        max_length: Maximum allowed length

    Returns:
        Sanitized text
    """
    # Truncate to max length
    text = text[:max_length]

    # Remove null bytes
    text = text.replace('\x00', '')

    # Normalize whitespace
    text = ' '.join(text.split())

    return text.strip()


def validate_chunk_size(token_count: int, max_tokens: int = 1024) -> Tuple[bool, str]:
    """
    Validate chunk token count.

    Args:
        token_count: Number of tokens in chunk
        max_tokens: Maximum allowed tokens

    Returns:
        Tuple of (is_valid, error_message)
    """
    if token_count < 1:
        return False, "Chunk must contain at least 1 token"

    if token_count > max_tokens:
        return False, f"Chunk size ({token_count} tokens) exceeds maximum ({max_tokens} tokens)"

    return True, ""


def detect_code_injection(text: str) -> Tuple[bool, str]:
    """
    Detect potential code injection attempts.

    Args:
        text: Text to check

    Returns:
        Tuple of (is_safe, warning_message)
    """
    # Check for common injection patterns
    dangerous_patterns = [
        r'<script[^>]*>',
        r'javascript:',
        r'onerror\s*=',
        r'onload\s*=',
        r'eval\s*\(',
        r'exec\s*\(',
        r'__import__',
        r'subprocess',
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False, f"Potential code injection detected: {pattern}"

    return True, ""


def validate_embedding_dimension(dimension: int, expected: int = 1024) -> Tuple[bool, str]:
    """
    Validate embedding vector dimension.

    Args:
        dimension: Actual dimension
        expected: Expected dimension

    Returns:
        Tuple of (is_valid, error_message)
    """
    if dimension != expected:
        return False, f"Invalid embedding dimension: expected {expected}, got {dimension}"

    return True, ""
