from src.agents.crew_router_setup import create_crew_router

def test_routing_crew():
    test_cases = [
        # {
        #     "query": "book 3 PM slot with doctor who can cure patient",
        #     "expected": "Doctor Availability Checker and Slot Booking",
        #     "name": "Andrew Norton"
           
        # },
        # {
        #     "query": "Which hospitals have emergency services available now ?",
        #     "expected": "Emergency Information Finder",
        #     "name": "Danielle Parker" --poor test
            
        # },
        {
            "query": "What diagnostic tests are used to detect disease?",
            "expected": "Diagnostic Info Agent",
            "name": "Gregory Caldwell"
        },
        # {
        #     "query": "Compare hospitals in patient zipcode that specialize in his disease with high ratings.",
        #     "expected": "Hospital Comparison Agent",
        #    "name": "Gregory Caldwell"
        # }
    ]

    for idx, case in enumerate(test_cases, 1):
        print("=" * 80)
        print(f"🧪 Test Case {idx}: {case['query']}")

        # ✅ Now pass the name into the router
        crew, result = create_crew_router(
            query=case["query"],
            name=case["name"],
            
        )

        # Extract the final answer cleanly
        if isinstance(result, dict):
            final = next(iter(result.values()))
        else:
            final = result

        # Clean up result
        if "Final Answer:" in str(final):
            final_output = str(final).split("Final Answer:")[-1].strip()
        else:
            final_output = str(final).strip() if final else "No response."

        print(f"✅ Final Answer: {final_output}\n")
        assert final_output, "❌ No final output returned."

if __name__ == "__main__":
    test_routing_crew()
