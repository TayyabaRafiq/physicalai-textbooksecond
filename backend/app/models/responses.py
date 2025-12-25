"""
Pydantic response models for API endpoints.
Defines response schemas for ingestion, question answering, and errors.
"""
from pydantic import BaseModel, Field
from typing import List


class IngestionResponse(BaseModel):
    """Response model for ingestion endpoint"""

    job_id: str = Field(
        ...,
        description="ID to track ingestion job status"
    )
    status: str = Field(
        ...,
        description="Job status: accepted, processing, completed, failed"
    )
    message: str = Field(
        ...,
        description="Human-readable status message"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "job_id": "ing-123e4567-e89b-12d3-a456-426614174000",
                    "status": "accepted",
                    "message": "Ingestion job accepted. Check /api/v1/ingestion/status/{job_id} for progress."
                }
            ]
        }
    }


class IngestionStatusResponse(BaseModel):
    """Response model for ingestion status endpoint"""

    job_id: str = Field(..., description="Ingestion job ID")
    status: str = Field(
        ...,
        description="Job status: accepted, processing, completed, failed"
    )
    message: str = Field(..., description="Status message")
    chunks_processed: int | None = Field(
        None,
        description="Number of chunks processed (if available)"
    )
    error: str | None = Field(
        None,
        description="Error message if status is failed"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "job_id": "ing-123e4567-e89b-12d3-a456-426614174000",
                    "status": "completed",
                    "message": "Ingestion completed successfully",
                    "chunks_processed": 42,
                    "error": None
                }
            ]
        }
    }


class SourceCitation(BaseModel):
    """Source citation for answers"""

    module: str
    chapter: str
    section: str
    chunk_id: int


class AnswerResponse(BaseModel):
    """Response model for question answering endpoints"""

    answer: str = Field(
        ...,
        description="Generated answer to the question"
    )
    sources: List[SourceCitation] = Field(
        ...,
        description="Source citations for the answer"
    )
    mode: str = Field(
        ...,
        description="Question mode: full_textbook or selected_text"
    )
    confidence: str = Field(
        ...,
        description="Confidence level: high, medium, low"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "answer": "Physical AI refers to artificial intelligence systems that interact with the physical world through embodied agents, such as robots. These systems combine perception, reasoning, and action to operate in real-world environments.",
                    "sources": [
                        {
                            "module": "Module 1: Introduction to Physical AI",
                            "chapter": "Chapter 1: What is Physical AI?",
                            "section": "Section 1.1: Defining Physical AI",
                            "chunk_id": 42
                        }
                    ],
                    "mode": "full_textbook",
                    "confidence": "high"
                }
            ]
        }
    }


class ErrorDetail(BaseModel):
    """Error detail information"""

    code: str = Field(
        ...,
        description="Error code (e.g., INVALID_INPUT, NOT_FOUND)"
    )
    message: str = Field(
        ...,
        description="Human-readable error message"
    )
    details: dict | None = Field(
        None,
        description="Additional error context"
    )


class ErrorResponse(BaseModel):
    """Standard error response model"""

    error: ErrorDetail

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": {
                        "code": "NO_RELEVANT_CONTENT",
                        "message": "I cannot answer based on the textbook content",
                        "details": {"question": "What is the meaning of life?"}
                    }
                }
            ]
        }
    }
