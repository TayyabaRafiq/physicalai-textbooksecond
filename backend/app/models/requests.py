"""
Pydantic request models for API endpoints.
Handles validation for ingestion and question answering requests.
"""
from pydantic import BaseModel, Field


class IngestionRequest(BaseModel):
    """Request model for content ingestion endpoint"""

    file_path: str = Field(
        ...,
        description="Path to markdown file to ingest",
        min_length=1,
        max_length=512
    )
    module_title: str = Field(
        ...,
        description="Title of the module",
        min_length=1,
        max_length=255
    )
    module_description: str | None = Field(
        None,
        description="Optional module description"
    )
    module_order: int = Field(
        ...,
        description="Order of the module in the textbook",
        ge=1
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "file_path": "content/module1.md",
                    "module_title": "Module 1: Introduction to Physical AI",
                    "module_description": "Foundational concepts in Physical AI",
                    "module_order": 1
                }
            ]
        }
    }


class QuestionRequest(BaseModel):
    """Request model for full textbook question answering"""

    question: str = Field(
        ...,
        description="User's question",
        min_length=5,
        max_length=500
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"question": "What is physical AI?"}
            ]
        }
    }


class SelectedTextQuestionRequest(BaseModel):
    """Request model for selected text question answering"""

    question: str = Field(
        ...,
        description="User's question about selected text",
        min_length=5,
        max_length=500
    )
    selected_text: str = Field(
        ...,
        description="Text selected by user",
        min_length=10,
        max_length=5000
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "Can you explain this concept?",
                    "selected_text": "Physical AI refers to artificial intelligence systems that interact with the physical world through embodied agents like robots..."
                }
            ]
        }
    }
