"""Check what's in Qdrant collection"""
from app.core.dependencies import get_qdrant_client
from app.core.config import get_settings

settings = get_settings()
client = get_qdrant_client()

try:
    # Get collection info
    info = client.get_collection(settings.QDRANT_COLLECTION_NAME)
    print(f"Collection: {settings.QDRANT_COLLECTION_NAME}")
    print(f"Points count: {info.points_count}")
    print(f"Status: {info.status}")

    # Try to scroll through some points
    if info.points_count > 0:
        points, _ = client.scroll(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            limit=10
        )
        print(f"\nFirst {len(points)} points:")
        for i, point in enumerate(points):
            print(f"\n{i+1}. ID: {point.id}")
            if point.payload:
                print(f"   Payload keys: {list(point.payload.keys())}")
                if 'content' in point.payload:
                    content_preview = point.payload['content'][:100]
                    print(f"   Content: {content_preview}...")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
