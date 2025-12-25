"""Test what Cohere models are available"""
import asyncio
from cohere import AsyncClient
from app.core.config import get_settings

async def test_models():
    settings = get_settings()
    client = AsyncClient(api_key=settings.COHERE_API_KEY)

    models_to_try = [
        "command-r7b-12-2024",
        "command-a-03-2025",
        "command-light-nightly",
        "command-nightly"
    ]

    for model in models_to_try:
        try:
            print(f"\nTrying model: {model}")
            response = await client.chat(
                message="What is 2+2?",
                model=model,
                max_tokens=50
            )
            print(f"  SUCCESS: {model}")
            print(f"  Response: {response.text[:100]}")
            print(f"\n** Use this model: {model} **")
            break  # Stop on first success
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg.lower():
                print(f"  Model not available: {model}")
            else:
                print(f"  Error: {error_msg[:200]}")

asyncio.run(test_models())
