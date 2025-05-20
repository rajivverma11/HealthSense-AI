# test_emergency_info_agent.py

from langchain_openai import ChatOpenAI
from src.agents.emergency_service_agent import EmergencyInfoAgent

llm = ChatOpenAI(model="gpt-4", temperature=0)

agent = EmergencyInfoAgent(llm=llm)

response = agent.run_query("Find the nearest hospital with emergency services in Atlanta")
print("Response:", response)
