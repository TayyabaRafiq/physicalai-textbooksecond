"""
Metadata store service for managing textbook hierarchy in Neon Postgres.
Handles creation of modules, chapters, sections, and chunks.
"""
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.database import Module, Chapter, Section, Chunk
from app.core.logging import get_logger

logger = get_logger(__name__)


class MetadataStoreService:
    """
    Service for storing and retrieving textbook metadata in Postgres.
    Manages hierarchical structure: Module → Chapter → Section → Chunk
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initialize metadata store service.

        Args:
            db_session: SQLAlchemy async session
        """
        self.db = db_session

    async def create_module(
        self,
        title: str,
        description: str | None,
        order: int
    ) -> Module:
        """
        Create a new module in the database.

        Args:
            title: Module title
            description: Optional module description
            order: Module order in textbook

        Returns:
            Created Module object
        """
        module = Module(
            title=title,
            description=description,
            order=order
        )
        self.db.add(module)
        await self.db.flush()  # Get the ID without committing
        await self.db.refresh(module)

        logger.info(
            f"Created module: {title}",
            extra={"module_id": module.id, "order": order}
        )

        return module

    async def create_chapter(
        self,
        module_id: int,
        title: str,
        order: int
    ) -> Chapter:
        """
        Create a new chapter in the database.

        Args:
            module_id: Parent module ID
            title: Chapter title
            order: Chapter order within module

        Returns:
            Created Chapter object
        """
        chapter = Chapter(
            module_id=module_id,
            title=title,
            order=order
        )
        self.db.add(chapter)
        await self.db.flush()
        await self.db.refresh(chapter)

        logger.info(
            f"Created chapter: {title}",
            extra={
                "chapter_id": chapter.id,
                "module_id": module_id,
                "order": order
            }
        )

        return chapter

    async def create_section(
        self,
        chapter_id: int,
        title: str,
        order: int
    ) -> Section:
        """
        Create a new section in the database.

        Args:
            chapter_id: Parent chapter ID
            title: Section title
            order: Section order within chapter

        Returns:
            Created Section object
        """
        section = Section(
            chapter_id=chapter_id,
            title=title,
            order=order
        )
        self.db.add(section)
        await self.db.flush()
        await self.db.refresh(section)

        logger.info(
            f"Created section: {title}",
            extra={
                "section_id": section.id,
                "chapter_id": chapter_id,
                "order": order
            }
        )

        return section

    async def create_chunk(
        self,
        section_id: int,
        content: str,
        token_count: int,
        file_path: str,
        line_start: int,
        line_end: int,
        qdrant_id: UUID
    ) -> Chunk:
        """
        Create a new chunk in the database.

        Args:
            section_id: Parent section ID
            content: Chunk text content
            token_count: Number of tokens in chunk
            file_path: Source file path
            line_start: Starting line number
            line_end: Ending line number
            qdrant_id: UUID linking to Qdrant vector

        Returns:
            Created Chunk object
        """
        chunk = Chunk(
            section_id=section_id,
            content=content,
            token_count=token_count,
            file_path=file_path,
            line_start=line_start,
            line_end=line_end,
            qdrant_id=qdrant_id
        )
        self.db.add(chunk)
        await self.db.flush()
        await self.db.refresh(chunk)

        logger.info(
            f"Created chunk",
            extra={
                "chunk_id": chunk.id,
                "section_id": section_id,
                "token_count": token_count,
                "qdrant_id": str(qdrant_id)
            }
        )

        return chunk

    async def get_module_by_id(self, module_id: int) -> Module | None:
        """Get module by ID"""
        result = await self.db.execute(
            select(Module).where(Module.id == module_id)
        )
        return result.scalar_one_or_none()

    async def get_chapter_by_id(self, chapter_id: int) -> Chapter | None:
        """Get chapter by ID"""
        result = await self.db.execute(
            select(Chapter).where(Chapter.id == chapter_id)
        )
        return result.scalar_one_or_none()

    async def get_section_by_id(self, section_id: int) -> Section | None:
        """Get section by ID"""
        result = await self.db.execute(
            select(Section).where(Section.id == section_id)
        )
        return result.scalar_one_or_none()

    async def get_chunk_by_id(self, chunk_id: int) -> Chunk | None:
        """Get chunk by ID"""
        result = await self.db.execute(
            select(Chunk).where(Chunk.id == chunk_id)
        )
        return result.scalar_one_or_none()

    async def commit(self):
        """Commit current transaction"""
        await self.db.commit()

    async def rollback(self):
        """Rollback current transaction"""
        await self.db.rollback()
