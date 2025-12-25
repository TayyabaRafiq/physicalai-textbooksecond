"""Final demo test with 5 high-quality questions"""
import requests
import json

BASE_URL = "http://localhost:8000"

demo_questions = [
    "What is Physical AI and how does it differ from traditional AI?",
    "Explain the four key ROS 2 concepts: nodes, topics, services, and actions.",
    "Why is simulation important for Physical AI development?",
    "What are the main safety considerations for deploying Physical AI systems?",
    "How does ROS 2 use DDS for real-time communication?"
]

print("=" * 80)
print("FINAL DEMO TEST - 5 High-Quality Questions")
print("=" * 80)

all_passed = True

for i, question in enumerate(demo_questions, 1):
    print(f"\n{'=' * 80}")
    print(f"TEST {i}/5: {question}")
    print("=" * 80)

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/question",
            headers={"Content-Type": "application/json"},
            json={"question": question},
            timeout=60
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            # Check answer
            if data['answer']:
                print(f"[OK] Answer generated ({len(data['answer'])} chars)")
            else:
                print("[FAIL] No answer generated")
                all_passed = False

            # Check sources
            if len(data['sources']) > 0:
                print(f"[OK] Sources cited ({len(data['sources'])} chunks)")
                for j, source in enumerate(data['sources'][:2], 1):  # Show first 2
                    print(f"  {j}. {source['section']}")
            else:
                print("[FAIL] No sources cited")
                all_passed = False

            # Check confidence
            print(f"[OK] Confidence: {data['confidence']}")

            # Show answer preview
            print(f"\nAnswer Preview:")
            print(data['answer'][:200] + "...")

        else:
            print(f"[FAIL] HTTP Error: {response.status_code}")
            print(response.text[:200])
            all_passed = False

    except Exception as e:
        print(f"[FAIL] Exception: {str(e)}")
        all_passed = False

print(f"\n{'=' * 80}")
if all_passed:
    print("[SUCCESS] ALL TESTS PASSED - Ready for demo")
else:
    print("[WARNING] SOME TESTS FAILED - Check errors above")
print("=" * 80)
