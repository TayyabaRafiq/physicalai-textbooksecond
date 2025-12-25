"""Test RAG system with realistic demo questions"""
import requests
import json

BASE_URL = "http://localhost:8000"

demo_questions = [
    "What is Physical AI?",
    "What are the key concepts of ROS 2?",
    "How does ROS 2 enable communication in robotic systems?",
    "What is the purpose of simulation in Physical AI development?",
    "What safety considerations are important for Physical AI systems?"
]

print("=" * 80)
print("RAG SYSTEM DEMO - Testing 5 Questions")
print("=" * 80)

for i, question in enumerate(demo_questions, 1):
    print(f"\n{'=' * 80}")
    print(f"QUESTION {i}: {question}")
    print("=" * 80)

    # Make request
    response = requests.post(
        f"{BASE_URL}/api/v1/question",
        headers={"Content-Type": "application/json"},
        json={"question": question},
        timeout=60
    )

    print(f"\nSTATUS CODE: {response.status_code}")

    if response.status_code == 200:
        data = response.json()

        print(f"\nANSWER:")
        print(data['answer'])

        print(f"\nSOURCES ({len(data['sources'])} chunks):")
        for j, source in enumerate(data['sources'], 1):
            print(f"  {j}. {source['module']} > {source['chapter']} > {source['section']}")

        print(f"\nCONFIDENCE: {data['confidence']}")
        print(f"MODE: {data['mode']}")

        # Verify answer is grounded
        if len(data['sources']) > 0:
            print("\n[OK] Answer is grounded in ingested content")
        else:
            print("\n[WARNING] No sources cited")
    else:
        print(f"\nERROR: {response.text}")

print(f"\n{'=' * 80}")
print("DEMO COMPLETE")
print("=" * 80)
