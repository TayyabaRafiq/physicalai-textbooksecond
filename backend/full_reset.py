"""Full database schema reset"""
import asyncio
from sqlalchemy import text
from app.models.database import get_engine

async def full_reset():
    engine = get_engine()
    async with engine.connect() as conn:
        # Drop all tables
        await conn.execute(text("DROP SCHEMA public CASCADE"))
        await conn.execute(text("CREATE SCHEMA public"))
        await conn.commit()
        print("Database schema reset complete")

asyncio.run(full_reset())
