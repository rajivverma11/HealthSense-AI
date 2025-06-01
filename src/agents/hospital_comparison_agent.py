from textwrap import dedent
from crewai import Agent
from crewai.tools import BaseTool
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from src.data.db_loader import load_hospital_dataframe
from typing import Type
from pydantic import BaseModel


# ✅ Tool input schema
class HospitalQueryInput(BaseModel):
    query: str


# ✅ Subclass BaseTool for compatibility with CrewAI
class HospitalComparisonTool(BaseTool):
    name: str = "hospital_comparison_tool"
    description: str = "Compare hospitals based on condition, location, and patient ratings."
    args_schema: Type[BaseModel] = HospitalQueryInput

    def __init__(self, pandas_agent, **kwargs):
        super().__init__(**kwargs)
        self._pandas_agent = pandas_agent

    def _run(self, query: str) -> str:
        try:
            result = self._pandas_agent.run(query)

            # ✅ Ensure final answer is clearly returned
            return f"Final Answer:\n{result}"

        except Exception as e:
            return f"❌ Error while running hospital comparison: {str(e)}"


    def _arun(self, query: str):
        raise NotImplementedError("Async not supported")


# ✅ CrewAI-compatible Agent wrapper
class HospitalComparisonAgent:
    def __init__(self, llm):
        self.llm = llm
        self._agent = self._build_agent()

    def _build_agent(self):
        df = load_hospital_dataframe()
        print(f"✅ Loaded hospital data with shape: {df.shape}")

        pandas_agent = create_pandas_dataframe_agent(
            llm=self.llm,
            df=df,
            verbose=False,
            allow_dangerous_code=True
        )

        comparison_tool = HospitalComparisonTool(pandas_agent=pandas_agent)

        return Agent(
            role="Hospital Comparison Agent",
            goal="Compare hospitals based on user needs like specialty, rating, and location.",
            backstory="You help users choose the right hospital by analyzing structured hospital data.",
            tools=[comparison_tool],
            llm=self.llm,
            verbose=False
        )

    def get_agent(self):
        return self._agent
