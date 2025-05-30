# src/test/test_crew_router.py
from src.agents.crew_router_setup import create_crew_router

def test_routing_crew():
    crew, result = create_crew_router("book 1 PM slot for dr lee")
    print("Result:", result)
    assert result is not None
