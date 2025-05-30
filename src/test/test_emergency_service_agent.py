# src/test/test_emergency_agent.py

from src.agents.emergency_service_agent import build_emergency_agent
from langchain_openai import ChatOpenAI


def main():
    llm = ChatOpenAI(model="gpt-4", temperature=0.1)
    agent = build_emergency_agent(llm=llm)

    query = "Is any ambulance available near 94404?"
    print(f"🧪 Running emergency agent with query: {query}")

    # Access the tool from the agent
    emergency_tool = agent.tools[0]  # Assuming one tool
    result = emergency_tool.run(query)  # Use `.invoke()` instead of `.run()`

    print("✅ Result:\n", result)


if __name__ == "__main__":
    main()
