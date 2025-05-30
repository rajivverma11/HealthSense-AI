# src/agents/hospital_comparison_agent.py

import pandas as pd
from crewai import Agent
from langchain.agents.agent_types import AgentType
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from src.data.db_loader import load_hospital_dataframe
from langchain.agents.agent import AgentExecutor 


from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from typing import Any, Type

class PandasQueryInput(BaseModel):
    query: str = Field(..., description="Hospital search query using pandas")

class PandasTool(BaseTool):
    name: str = "pandas_tool"
    description: str = "Query pandas dataframe for hospital info"
    args_schema: Type[BaseModel] = PandasQueryInput

    def __init__(self, pandas_agent):
        super().__init__()
        self._pandas_agent = pandas_agent

    def _run(self, query: str) -> str:
        return self._pandas_agent.invoke(query)

    def _arun(self, query: str) -> str:
        raise NotImplementedError("Async not supported")
    

class HospitalComparisonAgent:
    def __init__(self, llm):
        self.df = load_hospital_dataframe()

        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template("""
            You are a highly skilled healthcare assistant with expertise in comparing hospitals.
            Your task is to assess various hospitals based on a user's specific conditions, preferences, and needs.
            You will evaluate hospitals considering:
              - Medical specialties
              - Patient reviews and ratings
              - Location and accessibility
              - Cost and insurance
              - Hospital reputation, facilities, and awards

            Use the "Hospital Type" column to identify well-equipped facilities.
            Use ALL COLUMNS wisely. Provide well-rounded, personalized suggestions.
            """)
        ])

        self.pandas_agent = create_pandas_dataframe_agent(
            llm=llm,
            df=self.df,
            verbose=False,
            allow_dangerous_code=True,
            agent_type=AgentType.OPENAI_FUNCTIONS
        )

        self.agent = Agent(
        role='Hospital Information Analyst',
        goal='Compare and recommend hospitals',
        backstory='Expert in analyzing hospital data using pandas dataframe',
        tools=[PandasTool(self.pandas_agent)],  # ✅ Not BaseTool()
        verbose=False
    )



    def get_agent(self) -> Agent:
        return self.agent
