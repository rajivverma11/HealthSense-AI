# diagnostic_info_agent.py

import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents import AgentType  # keep this import for the agent type
from crewai import Agent
#from langchain.agents import create_pandas_dataframe_agent, AgentType
from langchain.prompts.chat import SystemMessagePromptTemplate, ChatPromptTemplate
from langchain.tools import BaseTool
from src.data.db_loader import load_hospital_info_test_dataframe


class DiagnosticInfoAgent:
    def __init__(self, llm):
        self.llm = llm
        self._agent = self._build_agent()
    
    def _build_agent(self):
        return Agent(
            role="Diagnostic Info Agent",
            goal="Provide accurate diagnostic test info",
            backstory="Expert in lab tests and diagnosis",
            verbose=False,
            llm=self.llm,
        )
    
    def get_agent(self):
        return self._agent


# class DiagnosticInfoAgent:
#     def __init__(self, llm, verbose=False):
#         self.llm = llm
#         self.verbose = verbose
        

#         self.system_message = SystemMessagePromptTemplate.from_template(
#             """
#             You are a highly skilled healthcare assistant with expertise in suggesting health screening tests and packages.
#             Your task is to assess various hospitals based on a user's specific conditions, preferences, and needs.
#             You will evaluate hospitals considering factors such as medical specialties, patient reviews, location, cost, accessibility, facilities,
#             and the availability of treatment for specific conditions.

#             When comparing hospitals, follow these guidelines:

#             - Condition-Specific Comparison: Focus on the hospitals' expertise in treating the user's specific health condition
#             (e.g., heart disease, cancer, etc.).
#             - Hospital Features: Include details about the hospital's reputation, technology, facilities, specialized care, and any awards or
#             recognitions.
#             - Location and Accessibility: Consider the proximity to the user’s location and the convenience of travel.
#             - Cost and Insurance: Compare the cost of treatment and insurance coverage options offered by the hospitals.
#             - Patient Feedback: Analyze reviews and ratings to gauge patient satisfaction and outcomes.
#             - Personalized Recommendation: Provide a clear, personalized suggestion based on the user’s priorities, whether they are medical
#             expertise, convenience, or cost.

#             CAREFULLY look at each column name to understand what to output.
#             """
#         )

#         df = load_hospital_info_test_dataframe()
#         print(f"number of rows: {df.shape[0]}")
#         #print(df.count())
#         prompt = ChatPromptTemplate.from_messages([self.system_message])

#         self.agent = create_pandas_dataframe_agent(
#             llm=self.llm,
#             df=df,
#             prompt=prompt,
#             verbose=self.verbose,
#             allow_dangerous_code=True,
#             agent_type=AgentType.OPENAI_FUNCTIONS,
#         )

#     def run_query(self, query: str) -> str:
#         return self.agent.invoke(query)


# class DiagnosticTool(BaseTool):
#     name: str = "pandas_tool"
#     description: str = "Query pandas dataframe and analyze diagnostic test/package data"

#     def __init__(self, agent_instance: DiagnosticInfoAgent):
#         super().__init__()
#         self.agent = agent_instance

#     def _run(self, query: str) -> str:
#         return self.agent.run_query(query)

#     def _arun(self, query: str) -> str:
#         raise NotImplementedError("Async not supported")
