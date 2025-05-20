# test_diagnostic_info_agent.py

from langchain_openai import ChatOpenAI
from src.agents.diagnostic_tests_agent import DiagnosticInfoAgent

llm = ChatOpenAI(model="gpt-4", temperature=0.0)

agent = DiagnosticInfoAgent(llm=llm)
query = "Suggest the most affordable hospital offering full body checkup in New York"

response = agent.run_query(query)
print("Diagnostic Info:", response)
