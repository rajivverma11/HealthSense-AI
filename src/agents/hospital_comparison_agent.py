import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate
from src.data.constants import LOCAL_DB_CONFIG
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from typing import Any
from pydantic import Field



class HospitalComparisonAgent:
    def __init__(self, df: pd.DataFrame):
        # System-level prompt
        system_message = SystemMessagePromptTemplate.from_template(
            """
            You are a highly skilled healthcare assistant with expertise in comparing hospitals.
            Your task is to assess various hospitals based on a user's specific conditions, preferences, and needs.
            You will evaluate hospitals considering factors such as medical specialties, patient reviews, location, cost, accessibility, facilities,
            and the availability of treatment for specific conditions.

            When comparing hospitals, follow these guidelines:

            - Condition-Specific Comparison: Focus on the hospitals' expertise in treating the user's specific health condition
            (e.g., heart disease, cancer, etc.).
            - Hospital Features: Include details about the hospital's reputation, technology, facilities, specialized care, and any awards or
            recognitions.
            - Location and Accessibility: Consider the proximity to the user’s location and the convenience of travel.
            - Cost and Insurance: Compare the cost of treatment and insurance coverage options offered by the hospitals.
            - Patient Feedback: Analyze reviews and ratings to gauge patient satisfaction and outcomes.
            - Personalized Recommendation: Provide a clear, personalized suggestion based on the user’s priorities, whether they are medical
            expertise, convenience, or cost.

            Use "HospitalType" column to look for good facilities of each hospital.
            CAREFULLY look at each column name to understand what to output.
            """
        )

        prompt = ChatPromptTemplate.from_messages([system_message])

        # Load OpenAI LLM
        openai_api_key = LOCAL_DB_CONFIG["OPENAI_API_KEY"]
        llm = ChatOpenAI(model=LOCAL_DB_CONFIG['LLM_MODEL_NAME'], api_key=openai_api_key)

        # Create the agent
        self.agent = create_pandas_dataframe_agent(
            llm=llm,
            df=df,
            prompt=prompt,
            verbose=True,
            allow_dangerous_code=True,
            agent_type=AgentType.OPENAI_FUNCTIONS
        )

    def compare(self, query: str) -> str:
        """Run the user query through the agent."""
        return self.agent.run(query)

class PandasTool(BaseTool):
    name: str = "pandas_tool"
    description: str = "Query pandas dataframe and analyze data"
    
    agent_instance: Any = Field(...)

    def __init__(self, agent_instance: Any):
        super().__init__(agent_instance=agent_instance)

    def _run(self, query: str) -> str:
        return self.agent_instance.compare(query)

    def _arun(self, query: str) -> str:
        raise NotImplementedError("Async not supported")


# hospital_info_agent = Agent(
#     role='Hospital Information Analyst',
#     goal='Analyze hospital data using pandas dataframe and provide relevant output',
#     backstory='Expert at analyzing complex datasets using pandas dataframe',
#     tools=[PandasTool()],
#     verbose=True
# )