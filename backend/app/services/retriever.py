"""
Retriever service for semantic search using Qdrant.
Retrieves relevant chunks based on query embedding similarity.
"""
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.database import Chunk, Section, Chapter, Module
from app.services.vector_store import VectorStoreService
from app.services.embedder import EmbedderService
from app.core.logging import get_logger

logger = get_logger(__name__)


class RetrievedChunk:
    """Represents a retrieved chunk with metadata and similarity score"""

    def __init__(
        self,
        chunk_id: int,
        content: str,
        score: float,
        module_title: str,
        chapter_title: str,
        section_title: str,
        file_path: str,
        line_start: int,
        line_end: int
    ):
        self.chunk_id = chunk_id
        self.content = content
        self.score = score
        self.module_title = module_title
        self.chapter_title = chapter_title
        self.section_title = section_title
        self.file_path = file_path
        self.line_start = line_start
        self.line_end = line_end


class RetrieverService:
    """
    Service for retrieving relevant chunks based on semantic similarity.
    Uses Qdrant for vector search and enriches with metadata from Postgres.
    """

    def __init__(
        self,
        vector_store: VectorStoreService,
        embedder: EmbedderService,
        db_session: AsyncSession
    ):
        """
        Initialize retriever service.

        Args:
            vector_store: Vector store service for similarity search
            embedder: Embedder service for query embedding
            db_session: Database session for metadata lookup
        """
        self.vector_store = vector_store
        self.embedder = embedder
        self.db = db_session

    async def search_similar(
        self,
        query: str,
        top_k: int = 5,
        module_filter: int | None = None
    ) -> List[RetrievedChunk]:
        """
        Search for chunks similar to the query.

        Args:
            query: User's question
            top_k: Number of chunks to retrieve
            module_filter: Optional module ID to filter results

        Returns:
            List of RetrievedChunk objects with metadata and scores

        Process:
            1. Generate query embedding
            2. Search Qdrant for similar vectors
            3. Enrich with metadata from Postgres
            4. Return ranked results
        """
        try:
            logger.info(
                f"Searching for similar chunks",
                extra={"query": query[:100], "top_k": top_k}
            )

            # Step 1: Generate query embedding
            query_embedding = await self.embedder.generate_query_embedding(query)

            # Step 2: Search Qdrant
            search_results = await self.vector_store.search_similar(
                query_embedding=query_embedding,
                top_k=top_k,
                module_filter=module_filter
            )

            if not search_results:
                logger.warning("No similar chunks found")
                return []

            # Step 3: Enrich with metadata from Postgres
            retrieved_chunks = []
            for result in search_results:
                chunk_id = result["payload"].get("chunk_id")

                # Get full chunk metadata from database
                chunk = await self._get_chunk_with_hierarchy(chunk_id)

                if chunk:
                    retrieved_chunk = RetrievedChunk(
                        chunk_id=chunk_id,
                        content=result["payload"].get("content", ""),
                        score=result["score"],
                        module_title=chunk["module_title"],
                        chapter_title=chunk["chapter_title"],
                        section_title=chunk["section_title"],
                        file_path=result["payload"].get("file_path", ""),
                        line_start=result["payload"].get("line_start", 0),
                        line_end=result["payload"].get("line_end", 0)
                    )
                    retrieved_chunks.append(retrieved_chunk)

            logger.info(
                f"Retrieved {len(retrieved_chunks)} chunks",
                extra={
                    "query": query[:50],
                    "chunks_found": len(retrieved_chunks),
                    "top_score": retrieved_chunks[0].score if retrieved_chunks else 0
                }
            )

            return retrieved_chunks

        except Exception as e:
            logger.error(
                f"Failed to retrieve similar chunks: {str(e)}",
                extra={"error": str(e), "query": query[:100]}
            )
            raise

    async def _get_chunk_with_hierarchy(
        self,
        chunk_id: int
    ) -> Dict[str, Any] | None:
        """
        Get chunk with full hierarchical metadata (module, chapter, section).

        Args:
            chunk_id: Chunk ID to retrieve

        Returns:
            Dict with chunk and hierarchy metadata, or None if not found
        """
        try:
            # Query with joins to get full hierarchy
            query = (
                select(Chunk, Section, Chapter, Module)
                .join(Section, Chunk.section_id == Section.id)
                .join(Chapter, Section.chapter_id == Chapter.id)
                .join(Module, Chapter.module_id == Module.id)
                .where(Chunk.id == chunk_id)
            )

            result = await self.db.execute(query)
            row = result.first()

            if not row:
                logger.warning(f"Chunk not found: {chunk_id}")
                return None

            chunk, section, chapter, module = row

            return {
                "chunk_id": chunk.id,
                "content": chunk.content,
                "module_title": module.title,
                "chapter_title": chapter.title,
                "section_title": section.title,
                "file_path": chunk.file_path,
                "line_start": chunk.line_start,
                "line_end": chunk.line_end
            }

        except Exception as e:
            logger.error(
                f"Failed to get chunk hierarchy: {str(e)}",
                extra={"error": str(e), "chunk_id": chunk_id}
            )
            return None
