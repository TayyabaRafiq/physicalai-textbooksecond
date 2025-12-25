"""
Embedding service using Cohere API.
Generates vector embeddings for text chunks.
"""
from typing import List
from cohere import AsyncClient as CohereAsyncClient
from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class EmbedderService:
    """
    Service for generating text embeddings using Cohere.
    Uses embed-english-v3.0 model with 1024 dimensions.
    """

    def __init__(self, cohere_client: CohereAsyncClient):
        """
        Initialize embedder service.

        Args:
            cohere_client: Cohere async client instance
        """
        self.client = cohere_client
        self.settings = get_settings()

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed (will be truncated to 512 tokens if needed)

        Returns:
            List of floats representing the embedding vector (1024 dimensions)

        Raises:
            Exception: If embedding generation fails
        """
        try:
            # Truncate text if too long (Cohere has limits)
            # Roughly 4 chars per token, so 512 tokens ≈ 2048 chars
            max_chars = 2048
            truncated_text = text[:max_chars] if len(text) > max_chars else text

            # Generate embedding
            response = await self.client.embed(
                texts=[truncated_text],
                model=self.settings.COHERE_MODEL_EMBED,
                input_type="search_document",  # For indexing documents
                embedding_types=["float"]
            )

            embedding = response.embeddings.float[0]

            logger.info(
                "Generated embedding",
                extra={
                    "text_length": len(text),
                    "truncated": len(text) > max_chars,
                    "embedding_dim": len(embedding)
                }
            )

            return embedding

        except Exception as e:
            logger.error(
                f"Failed to generate embedding: {str(e)}",
                extra={"error": str(e), "text_preview": text[:100]}
            )
            raise

    async def generate_embeddings_batch(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors

        Note:
            Batch processing is more efficient than individual calls.
            Cohere API has batch size limits (~96 texts per request).
        """
        if not texts:
            return []

        try:
            # Truncate texts if needed
            max_chars = 2048
            truncated_texts = [
                text[:max_chars] if len(text) > max_chars else text
                for text in texts
            ]

            # Generate embeddings in batch
            response = await self.client.embed(
                texts=truncated_texts,
                model=self.settings.COHERE_MODEL_EMBED,
                input_type="search_document",
                embedding_types=["float"]
            )

            embeddings = response.embeddings.float

            logger.info(
                f"Generated {len(embeddings)} embeddings in batch",
                extra={
                    "batch_size": len(texts),
                    "embedding_dim": len(embeddings[0]) if embeddings else 0
                }
            )

            return embeddings

        except Exception as e:
            logger.error(
                f"Failed to generate batch embeddings: {str(e)}",
                extra={"error": str(e), "batch_size": len(texts)}
            )
            raise

    async def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a search query.

        Args:
            query: Search query text

        Returns:
            Query embedding vector

        Note:
            Uses input_type="search_query" for better retrieval performance
        """
        try:
            # Truncate if needed
            max_chars = 2048
            truncated_query = query[:max_chars] if len(query) > max_chars else query

            # Generate query embedding
            response = await self.client.embed(
                texts=[truncated_query],
                model=self.settings.COHERE_MODEL_EMBED,
                input_type="search_query",  # Optimized for queries
                embedding_types=["float"]
            )

            embedding = response.embeddings.float[0]

            logger.info(
                "Generated query embedding",
                extra={
                    "query_length": len(query),
                    "embedding_dim": len(embedding)
                }
            )

            return embedding

        except Exception as e:
            logger.error(
                f"Failed to generate query embedding: {str(e)}",
                extra={"error": str(e), "query": query[:100]}
            )
            raise
