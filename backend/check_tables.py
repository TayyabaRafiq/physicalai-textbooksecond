"""Check what tables exist in the database"""
import asyncio
from sqlalchemy import text
from app.models.database import get_engine

async def check():
    engine = get_engine()
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = [row[0] for row in result]
        print('Tables in database:', tables)

asyncio.run(check())
