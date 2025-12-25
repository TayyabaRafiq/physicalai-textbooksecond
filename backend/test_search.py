"""Test vector search"""
import asyncio
from app.core.dependencies import get_qdrant_client, get_cohere_client
from app.services.embedder import EmbedderService
from app.core.config import get_settings

async def test_search():
    settings = get_settings()
    qdrant = get_qdrant_client()
    cohere = get_cohere_client()
    embedder = EmbedderService(cohere)

    # Generate query embedding
    query = "What is ROS 2?"
    print(f"Query: {query}")
    query_embedding = await embedder.generate_embedding(query)
    print(f"Embedding size: {len(query_embedding)}")

    # Try query_points
    print("\nTrying query_points...")
    try:
        result = qdrant.query_points(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query=query_embedding,
            limit=3
        )
        print(f"Result type: {type(result)}")
        print(f"Result: {result}")
        if hasattr(result, 'points'):
            print(f"Points count: {len(result.points)}")
            for i, point in enumerate(result.points):
                print(f"\n{i+1}. Score: {point.score}")
                if point.payload:
                    content = point.payload.get('content', '')[:100]
                    print(f"   Content: {content}...")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test_search())
