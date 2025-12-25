"""Create tables directly using SQLAlchemy metadata"""
import asyncio
from app.models.database import Base, get_engine

async def create_tables():
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully")

asyncio.run(create_tables())
