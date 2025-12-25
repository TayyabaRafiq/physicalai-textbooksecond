"""
Chunking service for splitting text into semantically meaningful chunks.
Respects paragraph boundaries and preserves code blocks.
"""
import re
from typing import List
from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class TextChunk:
    """Represents a chunk of text with metadata"""

    def __init__(self, content: str, token_count: int):
        self.content = content
        self.token_count = token_count


class ChunkerService:
    """
    Service for chunking text content into semantically meaningful pieces.
    Splits at paragraph boundaries while preserving code blocks.
    """

    def __init__(self, max_tokens: int | None = None):
        """
        Initialize chunker service.

        Args:
            max_tokens: Maximum tokens per chunk (default from config)
        """
        settings = get_settings()
        self.max_tokens = max_tokens or settings.MAX_CHUNK_TOKENS

    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text.
        Uses simple heuristic: ~4 characters per token (conservative estimate).

        Args:
            text: Text to count tokens for

        Returns:
            Estimated token count
        """
        # Simple heuristic: roughly 4 characters per token
        # This is conservative for English text
        return len(text) // 4

    def split_into_paragraphs(self, text: str) -> List[str]:
        """
        Split text into paragraphs, preserving code blocks.

        Args:
            text: Text to split

        Returns:
            List of paragraphs
        """
        # Handle code blocks specially
        code_block_pattern = r'```[\s\S]*?```'
        code_blocks = re.findall(code_block_pattern, text)

        # Replace code blocks with placeholders
        placeholder_text = text
        for i, block in enumerate(code_blocks):
            placeholder_text = placeholder_text.replace(
                block,
                f'__CODE_BLOCK_{i}__',
                1
            )

        # Split by double newlines (paragraphs)
        paragraphs = re.split(r'\n\s*\n', placeholder_text)

        # Restore code blocks
        result = []
        for para in paragraphs:
            restored = para
            for i, block in enumerate(code_blocks):
                restored = restored.replace(f'__CODE_BLOCK_{i}__', block)
            if restored.strip():
                result.append(restored.strip())

        return result

    def chunk_section(
        self,
        text: str,
        max_tokens: int | None = None
    ) -> List[TextChunk]:
        """
        Chunk section text into smaller pieces, respecting paragraph boundaries.

        Args:
            text: Section text to chunk
            max_tokens: Override max tokens (default from init)

        Returns:
            List of TextChunk objects

        Algorithm:
            1. Split text into paragraphs
            2. Accumulate paragraphs into chunks until max_tokens reached
            3. If single paragraph exceeds max_tokens, split by sentences
            4. Preserve code blocks as atomic units

        Edge Cases Handled:
            - Empty or whitespace-only text
            - Malformed markdown (unclosed code blocks)
            - Missing headings
            - Very long code blocks (>max_tokens)
            - Special characters and unicode
        """
        max_tok = max_tokens or self.max_tokens
        chunks = []

        # Edge case: Empty or whitespace-only text
        if not text or not text.strip():
            logger.warning("Empty text provided for chunking")
            return chunks

        # Edge case: Fix malformed code blocks (unclosed ```)
        text = self._fix_malformed_code_blocks(text)

        # Edge case: Handle very long text without paragraphs
        if '\n\n' not in text and len(text) > max_tok * 4:
            logger.warning("Text has no paragraph breaks, forcing splits")
            text = self._add_paragraph_breaks(text)

        # Split into paragraphs
        paragraphs = self.split_into_paragraphs(text)

        current_chunk = []
        current_tokens = 0

        for para in paragraphs:
            para_tokens = self.count_tokens(para)

            # If adding this paragraph exceeds limit
            if current_tokens + para_tokens > max_tok and current_chunk:
                # Save current chunk
                chunk_content = '\n\n'.join(current_chunk)
                chunks.append(TextChunk(
                    content=chunk_content,
                    token_count=self.count_tokens(chunk_content)
                ))
                current_chunk = []
                current_tokens = 0

            # If single paragraph is too large, split by sentences
            if para_tokens > max_tok:
                # Check if it's a code block
                if para.strip().startswith('```'):
                    # Keep code block as single chunk
                    chunks.append(TextChunk(
                        content=para,
                        token_count=para_tokens
                    ))
                else:
                    # Split by sentences
                    sentences = re.split(r'(?<=[.!?])\s+', para)
                    sentence_chunk = []
                    sentence_tokens = 0

                    for sentence in sentences:
                        sent_tokens = self.count_tokens(sentence)
                        if sentence_tokens + sent_tokens > max_tok and sentence_chunk:
                            # Save sentence chunk
                            chunk_content = ' '.join(sentence_chunk)
                            chunks.append(TextChunk(
                                content=chunk_content,
                                token_count=self.count_tokens(chunk_content)
                            ))
                            sentence_chunk = []
                            sentence_tokens = 0

                        sentence_chunk.append(sentence)
                        sentence_tokens += sent_tokens

                    # Save remaining sentences
                    if sentence_chunk:
                        chunk_content = ' '.join(sentence_chunk)
                        chunks.append(TextChunk(
                            content=chunk_content,
                            token_count=self.count_tokens(chunk_content)
                        ))
            else:
                # Add paragraph to current chunk
                current_chunk.append(para)
                current_tokens += para_tokens

        # Save final chunk
        if current_chunk:
            chunk_content = '\n\n'.join(current_chunk)
            chunks.append(TextChunk(
                content=chunk_content,
                token_count=self.count_tokens(chunk_content)
            ))

        logger.info(
            f"Chunked text into {len(chunks)} chunks",
            extra={
                "chunk_count": len(chunks),
                "max_tokens": max_tok,
                "original_length": len(text)
            }
        )

        return chunks

    def _fix_malformed_code_blocks(self, text: str) -> str:
        """
        Fix malformed code blocks (unclosed backticks).

        Args:
            text: Text to fix

        Returns:
            Fixed text
        """
        # Count backtick triplets
        backtick_count = text.count('```')

        # If odd number, add closing backticks at the end
        if backtick_count % 2 != 0:
            logger.warning("Malformed markdown detected: unclosed code block")
            text += '\n```\n'

        return text

    def _add_paragraph_breaks(self, text: str) -> str:
        """
        Add paragraph breaks to text that has none.
        Useful for handling very long unformatted text.

        Args:
            text: Text without paragraph breaks

        Returns:
            Text with added paragraph breaks
        """
        # Split by single newlines
        lines = text.split('\n')

        # Add double newline every N lines (heuristic)
        lines_per_para = 5
        result_lines = []

        for i, line in enumerate(lines):
            result_lines.append(line)
            if (i + 1) % lines_per_para == 0 and i < len(lines) - 1:
                result_lines.append('')  # Add blank line

        return '\n'.join(result_lines)
