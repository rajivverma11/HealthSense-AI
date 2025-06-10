from textwrap import dedent
from crewai import Agent
from crewai.tools import BaseTool
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from src.data.db_loader import load_hospital_dataframe
from pydantic import BaseModel
from typing import Type
import re


# Tool input schema
class HospitalQueryInput(BaseModel):
    query: str


# ✅ Correct BaseTool subclass for CrewAI compatibility
class HospitalComparisonTool(BaseTool):
    name: str = "hospital_comparison_tool"
    description: str = "Compare hospitals based on condition, location, and patient ratings."
    args_schema: Type[BaseModel] = HospitalQueryInput

    def __init__(self, pandas_agent, df, **kwargs):
        super().__init__(**kwargs)
        self._pandas_agent = pandas_agent
        self._df = df

    def _run(self, query: str) -> str:
        try:
            result = self._pandas_agent.invoke(query)
            if not result or "no hospitals" in str(result).lower():
                return self._fallback(query)
            return f"Final Answer: {result.strip()}"
        except Exception as e:
            return f"Tool execution failed: {str(e)}"

    def _arun(self, query: str):
        raise NotImplementedError("Async not supported")

    def _fallback(self, query: str) -> str:
        zip_match = re.search(r"\b\d{5}\b", query)
        if not zip_match:
            return "I couldn’t find any results for your query. Please include a zip code or state in your query."

        zip_code = zip_match.group()
        zip_prefix = zip_code[:3]
        nearby_zips = self._df[self._df["ZIP Code"].astype(str).str.startswith(zip_prefix)]["ZIP Code"].unique()

        for zip_alt in nearby_zips:
            if str(zip_alt) == zip_code:
                continue
            modified_query = query.replace(zip_code, str(zip_alt))
            try:
                result = self._pandas_agent.invoke(modified_query)
                if result and "no hospitals" not in str(result).lower():
                    return f"No hospitals found in {zip_code}, but nearby zip {zip_alt} has:\n{result.strip()}"
            except:
                continue
        return f"No results found in zip code {zip_code} or surrounding areas."


# ✅ CrewAI Agent wrapper
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
            allow_dangerous_code=True,
            max_iterations=2
        )

        comparison_tool = HospitalComparisonTool(pandas_agent=pandas_agent, df=df)

        return Agent(
            role="Hospital Finder and Comparator",
            goal=(
                "Analyze hospital data to help users compare and find the best hospitals based on their medical condition, "
                "location, patient reviews, costs, and specialties."
            ),
            backstory=dedent("""\
                You are a trusted hospital recommendation specialist with access to structured hospital datasets. 
                Your job is to recommend hospitals based on user needs such as:
                - The medical condition or specialty needed (e.g., cardiology, orthopedics)
                - Location or city preference (e.g., New York, Atlanta)
                - Patient ratings, reputation, or hospital type
                - Cost sensitivity, if mentioned

                You also have access to the user’s demographic and medical profile (age, gender, condition, city) if provided in memory.
                Use this to personalize your recommendations when relevant.

                Guidelines:
                - If the query lacks specific details (no location or condition), respond:
                  "Please include the medical condition and city you're looking for hospitals in."
                - Always use the full hospital dataset and try to balance condition, rating, and location when comparing.
                - If no matching hospitals are found, expand the search to neighboring cities or ZIP codes.
                - Ensure tool input follows this format:
                  {"query": "cardiology, high rating, 30301"}
                - Do NOT use nested structures like {"query": {"description": ...}}.
            """),
            tools=[comparison_tool],
            llm=self.llm,
            verbose=True
        )

    def get_agent(self):
        return self._agent
