from src.agents.crew_router_setup import create_crew_router

def test_routing_crew():
    test_cases = [
        {
            "query": "book 1 PM slot for dr lee",
            "expected": "Doctor Availability Checker and Slot Booking"
        },
        {
            "query": "Which hospitals have emergency services available now in New York?",
            "expected": "Emergency Information Finder"
        },
        {
            "query": "What diagnostic tests are used to detect diabetes?",
            "expected": "Diagnostic Info Agent"
        }
    ]

    for idx, case in enumerate(test_cases, 1):
        print("=" * 80)
        print(f"🧪 Test Case {idx}: {case['query']}")
        crew, result = create_crew_router(case["query"])

        # Extract the final answer cleanly
        if isinstance(result, dict):
            final = next(iter(result.values()))
        else:
            final = result

        # Try to extract just the final output text
        if "Final Answer:" in str(final):
            final_output = str(final).split("Final Answer:")[-1].strip()
        else:
            final_output = str(final).strip() if final else "No response."


        print(f"✅ Final Answer: {final_output}\n")
        assert final_output, "❌ No final output returned."

if __name__ == "__main__":
    test_routing_crew()
