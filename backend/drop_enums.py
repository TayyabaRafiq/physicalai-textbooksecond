"""Drop existing enum types that are blocking migration"""
import asyncio
from sqlalchemy import text
from app.models.database import get_engine

async def drop_enums():
    engine = get_engine()
    async with engine.connect() as conn:
        # Drop the question_mode enum if it exists
        await conn.execute(text("DROP TYPE IF EXISTS question_mode CASCADE"))
        await conn.commit()
        print("Dropped question_mode enum type")

asyncio.run(drop_enums())
