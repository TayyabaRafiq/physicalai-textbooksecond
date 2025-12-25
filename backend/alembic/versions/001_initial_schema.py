"""initial_schema

Revision ID: 001
Revises:
Create Date: 2025-12-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum type for question_mode
    question_mode_enum = postgresql.ENUM('full_textbook', 'selected_text', name='question_mode', create_type=True)
    question_mode_enum.create(op.get_bind(), checkfirst=True)

    # Create modules table
    op.create_table(
        'modules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('title'),
        sa.UniqueConstraint('order')
    )
    op.create_index('idx_modules_order', 'modules', ['order'])

    # Create chapters table
    op.create_table(
        'chapters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('module_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['module_id'], ['modules.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_chapters_module_id', 'chapters', ['module_id'])
    op.create_index('idx_chapters_order', 'chapters', ['order'])

    # Create sections table
    op.create_table(
        'sections',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('chapter_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_sections_chapter_id', 'sections', ['chapter_id'])
    op.create_index('idx_sections_order', 'sections', ['order'])

    # Create chunks table
    op.create_table(
        'chunks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('section_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('token_count', sa.Integer(), nullable=False),
        sa.Column('file_path', sa.String(length=512), nullable=False),
        sa.Column('line_start', sa.Integer(), nullable=False),
        sa.Column('line_end', sa.Integer(), nullable=False),
        sa.Column('qdrant_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['section_id'], ['sections.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('qdrant_id')
    )
    op.create_index('idx_chunks_section_id', 'chunks', ['section_id'])
    op.create_index('idx_chunks_qdrant_id', 'chunks', ['qdrant_id'])
    op.create_index('idx_chunks_file_path', 'chunks', ['file_path'])

    # Create question_log table
    op.create_table(
        'question_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=False),
        sa.Column('mode', question_mode_enum, nullable=False),
        sa.Column('selected_text', sa.Text(), nullable=True),
        sa.Column('user_ip', sa.String(length=45), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_question_log_created_at', 'question_log', ['created_at'])
    op.create_index('idx_question_log_user_ip', 'question_log', ['user_ip'])

    # Create answer_log table
    op.create_table(
        'answer_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('answer_text', sa.Text(), nullable=False),
        sa.Column('sources', postgresql.JSONB(), nullable=False),
        sa.Column('retrieved_chunk_ids', postgresql.ARRAY(sa.Integer()), nullable=False),
        sa.Column('model_used', sa.String(length=50), nullable=False),
        sa.Column('response_time_ms', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['question_log.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_answer_log_question_id', 'answer_log', ['question_id'])
    op.create_index('idx_answer_log_created_at', 'answer_log', ['created_at'])


def downgrade() -> None:
    op.drop_index('idx_answer_log_created_at', table_name='answer_log')
    op.drop_index('idx_answer_log_question_id', table_name='answer_log')
    op.drop_table('answer_log')

    op.drop_index('idx_question_log_user_ip', table_name='question_log')
    op.drop_index('idx_question_log_created_at', table_name='question_log')
    op.drop_table('question_log')

    op.drop_index('idx_chunks_file_path', table_name='chunks')
    op.drop_index('idx_chunks_qdrant_id', table_name='chunks')
    op.drop_index('idx_chunks_section_id', table_name='chunks')
    op.drop_table('chunks')

    op.drop_index('idx_sections_order', table_name='sections')
    op.drop_index('idx_sections_chapter_id', table_name='sections')
    op.drop_table('sections')

    op.drop_index('idx_chapters_order', table_name='chapters')
    op.drop_index('idx_chapters_module_id', table_name='chapters')
    op.drop_table('chapters')

    op.drop_index('idx_modules_order', table_name='modules')
    op.drop_table('modules')

    # Drop enum type
    sa.Enum(name='question_mode').drop(op.get_bind(), checkfirst=True)
