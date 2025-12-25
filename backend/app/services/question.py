"""
Question answering orchestration service.
Coordinates retrieval, generation, and logging.
"""
import time
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from qdrant_client import QdrantClient
from cohere import AsyncClient as CohereAsyncClient

from app.models.requests import QuestionRequest, SelectedTextQuestionRequest
from app.models.responses import AnswerResponse, SourceCitation
from app.models.database import QuestionLog, AnswerLog, QuestionMode
from app.services.retriever import RetrieverService, RetrievedChunk
from app.services.generator import GeneratorService
from app.services.embedder import EmbedderService
from app.services.vector_store import VectorStoreService
from app.core.logging import get_logger

logger = get_logger(__name__)


class QuestionService:
    """
    Orchestrates the question answering pipeline:
    1. Embed question
    2. Retrieve relevant chunks
    3. Generate answer
    4. Log question and answer
    5. Return response with sources
    """

    def __init__(
        self,
        db_session: AsyncSession,
        qdrant_client: QdrantClient,
        cohere_client: CohereAsyncClient,
        user_ip: str | None = None
    ):
        """
        Initialize question service.

        Args:
            db_session: Database session
            qdrant_client: Qdrant client
            cohere_client: Cohere client
            user_ip: Optional user IP for logging
        """
        self.db = db_session
        self.user_ip = user_ip

        # Initialize services
        self.embedder = EmbedderService(cohere_client)
        self.vector_store = VectorStoreService(qdrant_client)
        self.retriever = RetrieverService(
            vector_store=self.vector_store,
            embedder=self.embedder,
            db_session=db_session
        )
        self.generator = GeneratorService(cohere_client)

    async def answer_question(
        self,
        request: QuestionRequest,
        top_k: int = 5
    ) -> AnswerResponse:
        """
        Answer a question using full textbook retrieval.

        Args:
            request: Question request
            top_k: Number of chunks to retrieve

        Returns:
            AnswerResponse with answer and source citations

        Process:
            1. Retrieve similar chunks using semantic search
            2. Generate answer from retrieved context
            3. Log question and answer to database
            4. Return response with sources
        """
        start_time = time.time()

        try:
            logger.info(
                f"Answering question: {request.question}",
                extra={"question": request.question[:100]}
            )

            # Step 1: Retrieve relevant chunks
            retrieved_chunks = await self.retriever.search_similar(
                query=request.question,
                top_k=top_k
            )

            # Step 2: Generate answer
            generated_answer = await self.generator.generate_answer(
                question=request.question,
                context_chunks=retrieved_chunks,
                mode="full_textbook"
            )

            # Step 3: Build source citations
            sources = self._build_sources(retrieved_chunks)

            # Step 4: Log to database
            response_time_ms = int((time.time() - start_time) * 1000)
            await self._log_question_and_answer(
                question_text=request.question,
                mode=QuestionMode.FULL_TEXTBOOK,
                answer_text=generated_answer.answer,
                sources=sources,
                retrieved_chunk_ids=[chunk.chunk_id for chunk in retrieved_chunks],
                model_used=generated_answer.model_used,
                response_time_ms=response_time_ms
            )

            # Step 5: Commit transaction
            await self.db.commit()

            logger.info(
                f"Question answered successfully",
                extra={
                    "question": request.question[:50],
                    "response_time_ms": response_time_ms,
                    "chunks_used": len(retrieved_chunks),
                    "confidence": generated_answer.confidence
                }
            )

            # Step 6: Return response
            return AnswerResponse(
                answer=generated_answer.answer,
                sources=sources,
                mode="full_textbook",
                confidence=generated_answer.confidence
            )

        except Exception as e:
            await self.db.rollback()
            logger.error(
                f"Failed to answer question: {str(e)}",
                extra={"error": str(e), "question": request.question[:100]}
            )
            raise

    async def answer_selected_text(
        self,
        request: SelectedTextQuestionRequest
    ) -> AnswerResponse:
        """
        Answer a question about selected text only (context-restricted mode).

        Args:
            request: Selected text question request

        Returns:
            AnswerResponse with answer (no Qdrant sources)

        Process:
            1. Generate answer from selected text only
            2. Log question and answer to database
            3. Return response (no source citations from Qdrant)
        """
        start_time = time.time()

        try:
            logger.info(
                f"Answering question about selected text",
                extra={
                    "question": request.question[:100],
                    "text_length": len(request.selected_text)
                }
            )

            # Step 1: Generate answer from selected text
            generated_answer = await self.generator.generate_answer_from_text(
                question=request.question,
                selected_text=request.selected_text
            )

            # Step 2: Log to database
            response_time_ms = int((time.time() - start_time) * 1000)
            await self._log_question_and_answer(
                question_text=request.question,
                mode=QuestionMode.SELECTED_TEXT,
                answer_text=generated_answer.answer,
                sources=[],  # No Qdrant sources for selected text
                retrieved_chunk_ids=[],
                model_used=generated_answer.model_used,
                response_time_ms=response_time_ms,
                selected_text=request.selected_text
            )

            # Step 3: Commit transaction
            await self.db.commit()

            logger.info(
                f"Selected text question answered",
                extra={
                    "question": request.question[:50],
                    "response_time_ms": response_time_ms
                }
            )

            # Step 4: Return response
            return AnswerResponse(
                answer=generated_answer.answer,
                sources=[],  # No sources for selected text mode
                mode="selected_text",
                confidence=generated_answer.confidence
            )

        except Exception as e:
            await self.db.rollback()
            logger.error(
                f"Failed to answer selected text question: {str(e)}",
                extra={"error": str(e), "question": request.question[:100]}
            )
            raise

    def _build_sources(
        self,
        chunks: List[RetrievedChunk]
    ) -> List[SourceCitation]:
        """
        Build source citations from retrieved chunks.

        Args:
            chunks: Retrieved chunks

        Returns:
            List of SourceCitation objects
        """
        sources = []
        for chunk in chunks:
            citation = SourceCitation(
                module=chunk.module_title,
                chapter=chunk.chapter_title,
                section=chunk.section_title,
                chunk_id=chunk.chunk_id
            )
            sources.append(citation)

        return sources

    async def _log_question_and_answer(
        self,
        question_text: str,
        mode: QuestionMode,
        answer_text: str,
        sources: List[SourceCitation],
        retrieved_chunk_ids: List[int],
        model_used: str,
        response_time_ms: int,
        selected_text: str | None = None
    ) -> None:
        """
        Log question and answer to database.

        Args:
            question_text: The question
            mode: Question mode
            answer_text: Generated answer
            sources: Source citations
            retrieved_chunk_ids: List of chunk IDs used
            model_used: Model used for generation
            response_time_ms: Response time in milliseconds
            selected_text: Optional selected text
        """
        try:
            # Create question log
            question_log = QuestionLog(
                question_text=question_text,
                mode=mode,
                selected_text=selected_text,
                user_ip=self.user_ip
            )
            self.db.add(question_log)
            await self.db.flush()  # Get the question_id

            # Convert sources to JSONB format
            sources_json = [
                {
                    "module": s.module,
                    "chapter": s.chapter,
                    "section": s.section,
                    "chunk_id": s.chunk_id
                }
                for s in sources
            ]

            # Create answer log
            answer_log = AnswerLog(
                question_id=question_log.id,
                answer_text=answer_text,
                sources=sources_json,
                retrieved_chunk_ids=retrieved_chunk_ids,
                model_used=model_used,
                response_time_ms=response_time_ms
            )
            self.db.add(answer_log)

            logger.info(
                "Logged question and answer",
                extra={
                    "question_id": question_log.id,
                    "mode": mode.value,
                    "response_time_ms": response_time_ms
                }
            )

        except Exception as e:
            logger.error(
                f"Failed to log question and answer: {str(e)}",
                extra={"error": str(e)}
            )
            raise
