"""
SQLAlchemy models for Neon Postgres database.
Defines the hierarchical textbook structure: Module → Chapter → Section → Chunk
and logging tables for questions and answers.
"""
from datetime import datetime
from typing import AsyncGenerator
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    TIMESTAMP,
    Enum as SQLEnum,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
import enum

from app.core.config import get_settings

# Base class for all models
Base = declarative_base()


# Enums
class QuestionMode(str, enum.Enum):
    """Question answering mode"""
    FULL_TEXTBOOK = "full_textbook"
    SELECTED_TEXT = "selected_text"


# Models
class Module(Base):
    """
    Top-level module in the textbook (e.g., "Module 1: Introduction to Physical AI")
    """
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    order = Column(Integer, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    chapters = relationship("Chapter", back_populates="module", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_modules_order", "order"),
    )


class Chapter(Base):
    """
    Chapter within a module (e.g., "Chapter 1: What is Physical AI?")
    """
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    order = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    module = relationship("Module", back_populates="chapters")
    sections = relationship("Section", back_populates="chapter", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_chapters_module_id", "module_id"),
        Index("idx_chapters_order", "order"),
    )


class Section(Base):
    """
    Section within a chapter (e.g., "Section 1.1: Defining Physical AI")
    """
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    order = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    chapter = relationship("Chapter", back_populates="sections")
    chunks = relationship("Chunk", back_populates="section", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_sections_chapter_id", "chapter_id"),
        Index("idx_sections_order", "order"),
    )


class Chunk(Base):
    """
    Semantically meaningful piece of content for RAG retrieval (max 1024 tokens)
    """
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("sections.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    token_count = Column(Integer, nullable=False)
    file_path = Column(String(512), nullable=False)
    line_start = Column(Integer, nullable=False)
    line_end = Column(Integer, nullable=False)
    qdrant_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    section = relationship("Section", back_populates="chunks")

    __table_args__ = (
        Index("idx_chunks_section_id", "section_id"),
        Index("idx_chunks_qdrant_id", "qdrant_id"),
        Index("idx_chunks_file_path", "file_path"),
    )


class QuestionLog(Base):
    """
    Records all user questions for monitoring and analytics
    """
    __tablename__ = "question_log"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    mode = Column(SQLEnum(QuestionMode), nullable=False)
    selected_text = Column(Text)  # Only populated for selected_text mode
    user_ip = Column(String(45))  # IPv4 or IPv6
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)

    # Relationships
    answer = relationship("AnswerLog", back_populates="question", uselist=False, cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_question_log_created_at", "created_at"),
        Index("idx_question_log_user_ip", "user_ip"),
    )


class AnswerLog(Base):
    """
    Records generated answers with source citations and performance metrics
    """
    __tablename__ = "answer_log"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("question_log.id", ondelete="CASCADE"), nullable=False)
    answer_text = Column(Text, nullable=False)
    sources = Column(JSONB, nullable=False)  # Array of {module, chapter, section, chunk_id}
    retrieved_chunk_ids = Column(ARRAY(Integer), nullable=False)  # Array of chunk IDs
    model_used = Column(String(50), nullable=False)  # e.g., "command-r-plus"
    response_time_ms = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)

    # Relationships
    question = relationship("QuestionLog", back_populates="answer")

    __table_args__ = (
        Index("idx_answer_log_question_id", "question_id"),
        Index("idx_answer_log_created_at", "created_at"),
    )


# Database engine and session factory
def get_engine():
    """Create async database engine"""
    settings = get_settings()
    return create_async_engine(
        settings.NEON_DATABASE_URL,
        echo=False,  # Set to True for SQL query logging
        future=True,
        pool_pre_ping=True,  # Verify connections before using them
        pool_size=5,
        max_overflow=10,
    )


def get_session_factory():
    """Create async session factory"""
    engine = get_engine()
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session.

    Yields:
        AsyncSession: SQLAlchemy async session
    """
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
