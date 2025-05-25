# src/test/test_doctor_slot_agent.py

from src.agents.doctors_info_agent import build_crewai_agent
from langchain_openai import ChatOpenAI


def main():
    llm = ChatOpenAI(model="gpt-4", temperature=0.1)
    agent = build_crewai_agent(llm)

    query = "Book a 3PM slot for Dr. Lee"
    print(f"🤖 Running agent with query: {query}")
    result = agent.kickoff(query)
    print("✅ Result:\n", result)


if __name__ == "__main__":
    main()
