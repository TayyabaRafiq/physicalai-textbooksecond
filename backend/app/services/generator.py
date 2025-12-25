"""
Answer generation service using Cohere Command model.
Generates grounded answers with source citations.
"""
from typing import List
from cohere import AsyncClient as CohereAsyncClient
from app.services.retriever import RetrievedChunk
from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class GeneratedAnswer:
    """Represents a generated answer with metadata"""

    def __init__(
        self,
        answer: str,
        confidence: str,
        model_used: str
    ):
        self.answer = answer
        self.confidence = confidence
        self.model_used = model_used


class GeneratorService:
    """
    Service for generating answers using Cohere Command model.
    Ensures answers are grounded in retrieved context.
    """

    def __init__(self, cohere_client: CohereAsyncClient):
        """
        Initialize generator service.

        Args:
            cohere_client: Cohere async client instance
        """
        self.client = cohere_client
        self.settings = get_settings()

    async def generate_answer(
        self,
        question: str,
        context_chunks: List[RetrievedChunk],
        mode: str = "full_textbook"
    ) -> GeneratedAnswer:
        """
        Generate answer from question and retrieved chunks.

        Args:
            question: User's question
            context_chunks: Retrieved chunks with content and metadata
            mode: Answer mode ("full_textbook" or "selected_text")

        Returns:
            GeneratedAnswer with answer text and metadata

        Answer Generation Strategy:
            1. Build context from retrieved chunks
            2. Create strict prompt enforcing grounding
            3. Generate answer using Cohere Command
            4. Assess confidence based on chunk scores

        Edge Cases Handled:
            - Very long questions (truncated)
            - Special characters and unicode
            - Empty/whitespace questions
            - Non-English text (best-effort)
            - No context chunks available
        """
        try:
            # Edge case: Empty or whitespace-only question
            if not question or not question.strip():
                logger.warning("Empty question provided")
                return GeneratedAnswer(
                    answer="Please provide a valid question.",
                    confidence="low",
                    model_used=self.settings.COHERE_MODEL_GENERATE
                )

            # Edge case: Very long question (truncate to 500 chars)
            if len(question) > 500:
                logger.warning(f"Question too long ({len(question)} chars), truncating")
                question = question[:500] + "..."

            # Edge case: Sanitize question (remove null bytes, control characters)
            question = self._sanitize_text(question)

            if not context_chunks:
                logger.warning("No context chunks provided for answer generation")
                return GeneratedAnswer(
                    answer="I cannot answer based on the textbook content. No relevant information was found.",
                    confidence="low",
                    model_used=self.settings.COHERE_MODEL_GENERATE
                )

            # Step 1: Build context from chunks
            context = self._build_context(context_chunks)

            # Step 2: Create grounded prompt
            prompt = self._create_grounded_prompt(question, context, mode)

            logger.info(
                "Generating answer",
                extra={
                    "question": question[:100],
                    "context_length": len(context),
                    "num_chunks": len(context_chunks)
                }
            )

            # Step 3: Generate answer using Cohere
            logger.info(f"Using model for generation: {self.settings.COHERE_MODEL_GENERATE}")
            response = await self.client.chat(
                message=prompt,
                model=self.settings.COHERE_MODEL_GENERATE,
                temperature=0.3,  # Lower temperature for more factual responses
                max_tokens=500,
                preamble="You are a helpful AI tutor specializing in Physical AI. You provide clear, accurate explanations based strictly on the provided textbook content."
            )

            answer_text = response.text.strip()

            # Step 4: Assess confidence based on chunk scores
            confidence = self._assess_confidence(context_chunks)

            logger.info(
                "Generated answer",
                extra={
                    "question": question[:50],
                    "answer_length": len(answer_text),
                    "confidence": confidence,
                    "model": self.settings.COHERE_MODEL_GENERATE
                }
            )

            return GeneratedAnswer(
                answer=answer_text,
                confidence=confidence,
                model_used=self.settings.COHERE_MODEL_GENERATE
            )

        except Exception as e:
            logger.error(
                f"Failed to generate answer: {str(e)}",
                extra={"error": str(e), "question": question[:100]}
            )
            raise

    def _build_context(self, chunks: List[RetrievedChunk]) -> str:
        """
        Build context string from retrieved chunks.

        Args:
            chunks: List of retrieved chunks

        Returns:
            Formatted context string with source citations
        """
        context_parts = []

        for i, chunk in enumerate(chunks, 1):
            # Format: [Source 1] Module > Chapter > Section
            # Content...
            source_label = f"[Source {i}] {chunk.module_title} > {chunk.chapter_title} > {chunk.section_title}"
            context_parts.append(f"{source_label}\n{chunk.content}\n")

        return "\n".join(context_parts)

    def _create_grounded_prompt(
        self,
        question: str,
        context: str,
        mode: str
    ) -> str:
        """
        Create a prompt that enforces grounded answers.

        Args:
            question: User's question
            context: Built context from chunks
            mode: Answer mode

        Returns:
            Formatted prompt
        """
        if mode == "selected_text":
            instruction = "Answer the question using ONLY the selected text provided below. Do not use any external knowledge."
        else:
            instruction = "Answer the question using ONLY the textbook content provided below. Do not use any external knowledge."

        prompt = f"""{instruction}

If the provided content does not contain enough information to answer the question, respond with: "I cannot answer based on the textbook content."

Textbook Content:
{context}

Question: {question}

Answer (be clear and beginner-friendly):"""

        return prompt

    def _assess_confidence(self, chunks: List[RetrievedChunk]) -> str:
        """
        Assess confidence level based on chunk similarity scores.

        Args:
            chunks: Retrieved chunks with scores

        Returns:
            Confidence level: "high", "medium", or "low"

        Heuristics:
            - high: Top chunk score >= 0.8
            - medium: Top chunk score >= 0.6
            - low: Top chunk score < 0.6
        """
        if not chunks:
            return "low"

        top_score = chunks[0].score

        if top_score >= 0.8:
            return "high"
        elif top_score >= 0.6:
            return "medium"
        else:
            return "low"

    def _sanitize_text(self, text: str) -> str:
        """
        Sanitize text to remove problematic characters.

        Args:
            text: Text to sanitize

        Returns:
            Sanitized text
        """
        # Remove null bytes
        text = text.replace('\x00', '')

        # Remove other control characters except newlines and tabs
        text = ''.join(char for char in text if char.isprintable() or char in '\n\t')

        # Normalize whitespace
        text = ' '.join(text.split())

        return text.strip()

    async def generate_answer_from_text(
        self,
        question: str,
        selected_text: str
    ) -> GeneratedAnswer:
        """
        Generate answer from selected text (context-restricted mode).

        Args:
            question: User's question
            selected_text: Selected text to use as context

        Returns:
            GeneratedAnswer with answer text and metadata

        Edge Cases Handled:
            - Empty question or selected text
            - Very long selected text (truncated)
            - Special characters
        """
        try:
            # Edge case: Empty question
            if not question or not question.strip():
                logger.warning("Empty question provided for selected text")
                return GeneratedAnswer(
                    answer="Please provide a valid question.",
                    confidence="low",
                    model_used=self.settings.COHERE_MODEL_GENERATE
                )

            # Edge case: Empty selected text
            if not selected_text or not selected_text.strip():
                logger.warning("Empty selected text provided")
                return GeneratedAnswer(
                    answer="Please provide selected text to analyze.",
                    confidence="low",
                    model_used=self.settings.COHERE_MODEL_GENERATE
                )

            # Sanitize inputs
            question = self._sanitize_text(question)
            selected_text = self._sanitize_text(selected_text)

            # Edge case: Very long selected text (truncate to 5000 chars)
            if len(selected_text) > 5000:
                logger.warning(f"Selected text too long ({len(selected_text)} chars), truncating")
                selected_text = selected_text[:5000] + "..."

            logger.info(
                "Generating answer from selected text",
                extra={
                    "question": question[:100],
                    "text_length": len(selected_text)
                }
            )

            # Create prompt for selected text
            prompt = f"""Answer the question using ONLY the selected text provided below. Do not use any external knowledge.

If the selected text does not contain enough information to answer the question, respond with: "I cannot answer based on the selected text alone."

Selected Text:
{selected_text}

Question: {question}

Answer (be clear and beginner-friendly):"""

            # Generate answer
            response = await self.client.chat(
                message=prompt,
                model=self.settings.COHERE_MODEL_GENERATE,
                temperature=0.3,
                max_tokens=500,
                preamble="You are a helpful AI tutor specializing in Physical AI. You provide clear, accurate explanations based strictly on the provided text."
            )

            answer_text = response.text.strip()

            logger.info(
                "Generated answer from selected text",
                extra={
                    "question": question[:50],
                    "answer_length": len(answer_text)
                }
            )

            return GeneratedAnswer(
                answer=answer_text,
                confidence="medium",  # Fixed confidence for selected text mode
                model_used=self.settings.COHERE_MODEL_GENERATE
            )

        except Exception as e:
            logger.error(
                f"Failed to generate answer from selected text: {str(e)}",
                extra={"error": str(e), "question": question[:100]}
            )
            raise
