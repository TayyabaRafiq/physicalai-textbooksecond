"""Fix chunk_ids in Qdrant points"""
import asyncio
from app.core.dependencies import get_qdrant_client
from app.core.config import get_settings
from app.services.vector_store import VectorStoreService

async def fix_chunk_ids():
    settings = get_settings()
    client = get_qdrant_client()
    vector_store = VectorStoreService(client)

    # Get all points
    points, _ = client.scroll(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        limit=100
    )

    print(f"Found {len(points)} points to update")

    # Update each point with correct chunk_id
    for i, point in enumerate(points, 1):
        await vector_store.update_chunk_id(point.id, i)
        print(f"Updated point {point.id} with chunk_id={i}")

    print("All chunk_ids updated!")

asyncio.run(fix_chunk_ids())
