"""Reset alembic version to force re-migration"""
import asyncio
from sqlalchemy import text
from app.models.database import get_engine

async def reset():
    engine = get_engine()
    async with engine.connect() as conn:
        # Delete all rows from alembic_version
        await conn.execute(text("DELETE FROM alembic_version"))
        await conn.commit()
        print("Reset alembic version")

asyncio.run(reset())
