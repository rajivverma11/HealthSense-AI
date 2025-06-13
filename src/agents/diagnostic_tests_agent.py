# diagnostic_info_agent.py

import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents import AgentType  # keep this import for the agent type
from crewai import Agent
#from langchain.agents import create_pandas_dataframe_agent, AgentType



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


