from src.agents.doctors_info_agent import DoctorsInfoAgent

if __name__ == "__main__":
    agent = DoctorsInfoAgent()
    query = "Book 3PM slot for Dr. Lee for tomorrow"
    response = agent.run(query)
    print("=== Agent Response ===")
    print(response)