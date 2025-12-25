"""
Ingestion orchestration service.
Coordinates markdown parsing, chunking, embedding, and storage.
"""
from uuid import uuid4
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from qdrant_client import QdrantClient
from cohere import AsyncClient as CohereAsyncClient

from app.models.requests import IngestionRequest
from app.utils.markdown_parser import parse_textbook_markdown
from app.services.chunker import ChunkerService
from app.services.metadata_store import MetadataStoreService
from app.services.embedder import EmbedderService
from app.services.vector_store import VectorStoreService
from app.core.logging import get_logger

logger = get_logger(__name__)


# In-memory job status store (for MVP)
# In production, this should be Redis or a database table
JOB_STATUS_STORE: Dict[str, Dict[str, Any]] = {}


class IngestionService:
    """
    Orchestrates the full ingestion pipeline:
    1. Parse markdown file
    2. Chunk sections
    3. Generate embeddings
    4. Store in Qdrant and Neon
    """

    def __init__(
        self,
        db_session: AsyncSession,
        qdrant_client: QdrantClient,
        cohere_client: CohereAsyncClient
    ):
        """
        Initialize ingestion service with dependencies.

        Args:
            db_session: Database session
            qdrant_client: Qdrant client
            cohere_client: Cohere client
        """
        self.db = db_session
        self.metadata_store = MetadataStoreService(db_session)
        self.chunker = ChunkerService()
        self.embedder = EmbedderService(cohere_client)
        self.vector_store = VectorStoreService(qdrant_client)

    async def ingest_file(self, request: IngestionRequest) -> str:
        """
        Ingest a markdown file into the RAG system.

        Args:
            request: Ingestion request with file path and module metadata

        Returns:
            Job ID for tracking ingestion progress

        Process:
            1. Parse markdown into hierarchical structure
            2. Create module, chapters, sections in database
            3. Chunk section content
            4. Generate embeddings for chunks
            5. Store chunks in Qdrant and Neon
        """
        # Generate job ID
        job_id = f"ing-{uuid4()}"
        chunks_processed = 0

        try:
            # Update job status
            JOB_STATUS_STORE[job_id] = {
                "status": "processing",
                "message": "Parsing markdown file",
                "chunks_processed": 0
            }

            logger.info(
                f"Starting ingestion job {job_id}",
                extra={
                    "job_id": job_id,
                    "file_path": request.file_path,
                    "module_title": request.module_title
                }
            )

            # Step 1: Parse markdown file
            parsed_module = parse_textbook_markdown(
                file_path=request.file_path,
                module_title=request.module_title,
                module_description=request.module_description,
                module_order=request.module_order
            )

            logger.info(
                f"Parsed markdown: {len(parsed_module.chapters)} chapters",
                extra={"job_id": job_id, "chapters": len(parsed_module.chapters)}
            )

            # Step 2: Initialize Qdrant collection
            await self.vector_store.initialize_collection()

            # Step 3: Create module in database
            module = await self.metadata_store.create_module(
                title=parsed_module.title,
                description=parsed_module.description,
                order=parsed_module.order
            )

            chunks_processed = 0

            # Step 4: Process each chapter
            for parsed_chapter in parsed_module.chapters:
                chapter = await self.metadata_store.create_chapter(
                    module_id=module.id,
                    title=parsed_chapter.title,
                    order=parsed_chapter.order
                )

                # Step 5: Process each section
                for parsed_section in parsed_chapter.sections:
                    section = await self.metadata_store.create_section(
                        chapter_id=chapter.id,
                        title=parsed_section.title,
                        order=parsed_section.order
                    )

                    # Step 6: Chunk section content
                    chunks = self.chunker.chunk_section(parsed_section.content)

                    logger.info(
                        f"Chunked section into {len(chunks)} chunks",
                        extra={
                            "job_id": job_id,
                            "section_title": parsed_section.title,
                            "chunk_count": len(chunks)
                        }
                    )

                    # Step 7: Process each chunk
                    for chunk in chunks:
                        # Generate embedding
                        embedding = await self.embedder.generate_embedding(
                            chunk.content
                        )

                        # Store in Qdrant first
                        qdrant_id = await self.vector_store.store_chunk(
                            chunk_id=0,  # Temporary, will update with actual ID
                            embedding=embedding,
                            metadata={
                                "module_id": module.id,
                                "chapter_id": chapter.id,
                                "section_id": section.id,
                                "module_title": module.title,
                                "chapter_title": chapter.title,
                                "section_title": section.title,
                                "file_path": request.file_path,
                                "line_start": parsed_section.line_start,
                                "line_end": parsed_section.line_end,
                                "content": chunk.content,
                                "token_count": chunk.token_count
                            }
                        )

                        # Store chunk metadata in Neon
                        db_chunk = await self.metadata_store.create_chunk(
                            section_id=section.id,
                            content=chunk.content,
                            token_count=chunk.token_count,
                            file_path=request.file_path,
                            line_start=parsed_section.line_start,
                            line_end=parsed_section.line_end,
                            qdrant_id=qdrant_id
                        )

                        # Update Qdrant point with actual chunk_id
                        await self.vector_store.update_chunk_id(
                            qdrant_id=qdrant_id,
                            chunk_id=db_chunk.id
                        )

                        chunks_processed += 1

                        # Update job status
                        JOB_STATUS_STORE[job_id]["chunks_processed"] = chunks_processed

            # Commit database transaction
            await self.metadata_store.commit()

            # Update final job status
            JOB_STATUS_STORE[job_id] = {
                "status": "completed",
                "message": f"Successfully ingested {chunks_processed} chunks",
                "chunks_processed": chunks_processed
            }

            logger.info(
                f"Ingestion job {job_id} completed",
                extra={
                    "job_id": job_id,
                    "chunks_processed": chunks_processed
                }
            )

            return job_id

        except Exception as e:
            # Rollback database on error
            await self.metadata_store.rollback()

            # Update job status
            JOB_STATUS_STORE[job_id] = {
                "status": "failed",
                "message": f"Ingestion failed: {str(e)}",
                "chunks_processed": chunks_processed,
                "error": str(e)
            }

            logger.error(
                f"Ingestion job {job_id} failed",
                extra={"job_id": job_id, "error": str(e)}
            )

            raise

    @staticmethod
    def get_job_status(job_id: str) -> Dict[str, Any] | None:
        """
        Get status of an ingestion job.

        Args:
            job_id: Job ID to check

        Returns:
            Job status dict or None if not found
        """
        return JOB_STATUS_STORE.get(job_id)
