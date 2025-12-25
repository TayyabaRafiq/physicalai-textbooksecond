"""
Vector store service for Qdrant Cloud.
Manages vector embeddings storage and retrieval.
"""
from typing import List, Dict, Any
from uuid import UUID, uuid4
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    SearchRequest,
    Filter,
    FieldCondition,
    MatchValue
)
from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class VectorStoreService:
    """
    Service for managing vector embeddings in Qdrant Cloud.
    Handles collection initialization and point storage/retrieval.
    """

    def __init__(self, qdrant_client: QdrantClient):
        """
        Initialize vector store service.

        Args:
            qdrant_client: Qdrant client instance
        """
        self.client = qdrant_client
        self.settings = get_settings()
        self.collection_name = self.settings.QDRANT_COLLECTION_NAME

    async def initialize_collection(self) -> None:
        """
        Initialize Qdrant collection for textbook chunks.
        Creates collection if it doesn't exist.

        Collection config:
        - Vector size: 1024 (Cohere embed-english-v3.0)
        - Distance: Cosine similarity
        - HNSW indexing for fast approximate search
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections().collections
            collection_exists = any(
                col.name == self.collection_name for col in collections
            )

            if not collection_exists:
                # Create collection
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=1024,  # Cohere embed-english-v3.0 dimension
                        distance=Distance.COSINE
                    ),
                    # HNSW config for efficient similarity search
                    hnsw_config={
                        "m": 16,  # Number of edges per node
                        "ef_construct": 100  # Size of candidate list
                    }
                )
                logger.info(
                    f"Created Qdrant collection: {self.collection_name}",
                    extra={"collection_name": self.collection_name}
                )
            else:
                logger.info(
                    f"Qdrant collection already exists: {self.collection_name}",
                    extra={"collection_name": self.collection_name}
                )

        except Exception as e:
            logger.error(
                f"Failed to initialize Qdrant collection: {str(e)}",
                extra={"error": str(e)}
            )
            raise

    async def store_chunk(
        self,
        chunk_id: int,
        embedding: List[float],
        metadata: Dict[str, Any]
    ) -> UUID:
        """
        Store a chunk embedding in Qdrant with metadata.

        Args:
            chunk_id: Postgres chunk ID
            embedding: Vector embedding (1024 dimensions)
            metadata: Chunk metadata (module, chapter, section, content, etc.)

        Returns:
            UUID of the stored point in Qdrant

        Metadata should include:
            - chunk_id: Postgres chunk ID
            - section_id: Parent section ID
            - chapter_id: Parent chapter ID
            - module_id: Parent module ID
            - module_title: Module title
            - chapter_title: Chapter title
            - section_title: Section title
            - file_path: Source file path
            - line_start: Starting line number
            - line_end: Ending line number
            - content: Full chunk text
            - token_count: Number of tokens
        """
        try:
            # Generate UUID for this point
            point_id = uuid4()

            # Create point
            point = PointStruct(
                id=str(point_id),
                vector=embedding,
                payload={
                    **metadata,
                    "chunk_id": chunk_id  # Ensure chunk_id is in payload
                }
            )

            # Upload to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )

            logger.info(
                f"Stored chunk in Qdrant",
                extra={
                    "chunk_id": chunk_id,
                    "qdrant_id": str(point_id),
                    "section_id": metadata.get("section_id")
                }
            )

            return point_id

        except Exception as e:
            logger.error(
                f"Failed to store chunk in Qdrant: {str(e)}",
                extra={"error": str(e), "chunk_id": chunk_id}
            )
            raise

    async def search_similar(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        module_filter: int | None = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar chunks using vector similarity.

        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            module_filter: Optional module ID to filter results

        Returns:
            List of search results with scores and metadata

        Each result contains:
            - id: Qdrant point ID
            - score: Similarity score
            - payload: Chunk metadata
        """
        try:
            # Build filter if module specified
            search_filter = None
            if module_filter is not None:
                search_filter = Filter(
                    must=[
                        FieldCondition(
                            key="module_id",
                            match=MatchValue(value=module_filter)
                        )
                    ]
                )

            # Search using query_points
            search_result = self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=top_k,
                query_filter=search_filter
            )

            results = [
                {
                    "id": hit.id,
                    "score": hit.score,
                    "payload": hit.payload
                }
                for hit in search_result.points
            ]

            logger.info(
                f"Found {len(results)} similar chunks",
                extra={
                    "top_k": top_k,
                    "module_filter": module_filter,
                    "results_count": len(results)
                }
            )

            return results

        except Exception as e:
            logger.error(
                f"Failed to search Qdrant: {str(e)}",
                extra={"error": str(e), "top_k": top_k}
            )
            raise

    async def delete_chunk(self, qdrant_id: str) -> None:
        """
        Delete a chunk from Qdrant by its ID.

        Args:
            qdrant_id: UUID of the point to delete
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[qdrant_id]
            )
            logger.info(
                f"Deleted chunk from Qdrant",
                extra={"qdrant_id": qdrant_id}
            )
        except Exception as e:
            logger.error(
                f"Failed to delete chunk from Qdrant: {str(e)}",
                extra={"error": str(e), "qdrant_id": qdrant_id}
            )
            raise

    async def update_chunk_id(self, qdrant_id: UUID, chunk_id: int) -> None:
        """
        Update the chunk_id in a Qdrant point's payload.

        Args:
            qdrant_id: UUID of the Qdrant point
            chunk_id: Actual chunk ID from database
        """
        try:
            self.client.set_payload(
                collection_name=self.collection_name,
                payload={"chunk_id": chunk_id},
                points=[str(qdrant_id)]
            )
            logger.info(
                f"Updated chunk_id in Qdrant",
                extra={"qdrant_id": str(qdrant_id), "chunk_id": chunk_id}
            )
        except Exception as e:
            logger.error(
                f"Failed to update chunk_id in Qdrant: {str(e)}",
                extra={"error": str(e), "qdrant_id": str(qdrant_id)}
            )
            raise

    async def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": info.config.params.vectors.size,
                "points_count": info.points_count,
                "status": info.status
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {str(e)}")
            return {"error": str(e)}
