"""Test script to check if dependencies work"""
import asyncio
from app.core.dependencies import get_db, get_qdrant_client, get_cohere_client
from sqlalchemy import text

async def test_database():
    """Test database connection"""
    try:
        async for db in get_db():
            result = await db.execute(text("SELECT 1"))
            print("[OK] Database connection successful")
            return True
    except Exception as e:
        print(f"[FAIL] Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_qdrant():
    """Test Qdrant connection"""
    try:
        client = get_qdrant_client()
        collections = client.get_collections()
        print(f"[OK] Qdrant connection successful ({len(collections.collections)} collections)")
        return True
    except Exception as e:
        print(f"[FAIL] Qdrant connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_cohere():
    """Test Cohere connection"""
    try:
        client = get_cohere_client()
        response = await client.embed(
            texts=["test"],
            model="embed-english-v3.0",
            input_type="search_query",
            embedding_types=["float"]
        )
        print(f"[OK] Cohere connection successful")
        return True
    except Exception as e:
        print(f"[FAIL] Cohere connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("Testing dependencies...")
    print()

    db_ok = await test_database()
    print()

    qdrant_ok = test_qdrant()
    print()

    cohere_ok = await test_cohere()
    print()

    if db_ok and qdrant_ok and cohere_ok:
        print("All dependencies working!")
    else:
        print("Some dependencies failed!")

if __name__ == "__main__":
    asyncio.run(main())
