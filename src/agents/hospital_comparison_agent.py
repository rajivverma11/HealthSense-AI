
import pandas as pd
from crewai import Agent
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain.tools.base import BaseTool
from typing import Optional, Type
from pydantic import BaseModel

from src.data.db_loader import load_hospital_dataframe


# ✅ Custom tool for CrewAI that is a proper subclass of BaseTool
class HospitalComparisonInput(BaseModel):
    query: str


class HospitalComparisonTool(BaseTool):
    name = "hospital_comparison_tool"
    description = "Compares hospitals based on condition, location, reviews, etc."
    args_schema: Type[BaseModel] = HospitalComparisonInput

    def __init__(self, pandas_agent, **kwargs):
        super().__init__(**kwargs)
        self.pandas_agent = pandas_agent

    def _run(self, query: str) -> str:
        return self.pandas_agent.run(query)

    def _arun(self, query: str) -> str:
        raise NotImplementedError("Async not supported")


class HospitalComparisonAgent:
    def __init__(self, llm):
        # Load hospital data
        df = load_hospital_dataframe()
        print(f"Loaded hospital data with shape: {df.shape}")

        # Create the pandas agent
        pandas_agent = create_pandas_dataframe_agent(
            llm=llm,
            df=df,
            verbose=True,
            allow_dangerous_code=True
        )

        # Create a valid CrewAI-compatible tool
        hospital_comparison_tool = HospitalComparisonTool(pandas_agent=pandas_agent)

        # Register CrewAI agent
        self.agent = Agent(
            role="Hospital Info Agent",
            goal="Help users compare hospitals for their health conditions.",
            backstory="You are a data-driven healthcare assistant with access to hospital data.",
            tools=[hospital_comparison_tool],
            llm=llm,
            verbose=True
        )

    def get_agent(self):
        return self.agent






#######

# import pandas as pd
# from pydantic import BaseModel
# from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
# from langchain_core.tools import BaseTool
# from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
# from langchain_openai import ChatOpenAI
# from textwrap import dedent
# from src.data.db_loader import load_hospital_dataframe
# from crewai import Agent
# from typing import Type
# from langchain_core.tools import BaseTool
# from pydantic import BaseModel
# from langchain.tools import Tool



# from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
# from crewai import Agent
#from src.data.db_loader import load_hospital_data

#     def __init__(self, llm):
#         # Load hospital data
#         df = load_hospital_dataframe()
#         print(f"Loaded hospital data with shape: {df.shape}")

#         # Create LangChain pandas dataframe agent
#         self.pandas_agent = create_pandas_dataframe_agent(
#             llm=llm,
#             df=df,
#             verbose=True,
#             allow_dangerous_code=True  # required!
#         )

#         # ✅ Define a LangChain Tool compatible with CrewAI
#         def _run_hospital_comparison(query: str) -> str:
#             return self.pandas_agent.run(query)

#         self.compare_tool = Tool(
#         name="HospitalComparisonTool",
#         description="Compare hospitals based on user query, considering condition, reviews, location, etc.",
#         func=_run_hospital_comparison
# )

#         # ✅ Define the CrewAI Agent
#         self.agent = Agent(
#         role="Hospital Info Agent",
#         goal="Help users compare hospitals for their health conditions.",
#         backstory="You are a data-driven healthcare assistant with access to hospital data.",
#         tools=[self.compare_tool],  # ✅ This must be a valid BaseTool
#         llm=llm,
#         verbose=False
# )


#     def get_agent(self):
#         return self.agent



# class HospitalQueryInput(BaseModel):
#     query: str

# class HospitalComparisonTool(BaseTool):
#     name: str = "hospital_comparison_tool"
#     description: str = "Compare hospitals based on user preferences like condition, location, and reviews."
#     args_schema: Type[BaseModel] = HospitalQueryInput

#     def __init__(self, pandas_agent, **kwargs):
#         super().__init__(**kwargs)
#         self._pandas_agent = pandas_agent

#     def _run(self, query: str) -> str:
#         return self._pandas_agent.invoke(query)

#     def _arun(self, query: str):
#         raise NotImplementedError("Async not supported")

#     name = "hospital_comparison_tool"
#     description = "Compare hospitals based on user preferences like condition, location, and reviews."
#     args_schema = HospitalQueryInput

#     def __init__(self, pandas_agent, **kwargs):
#         super().__init__(**kwargs)
#         self._pandas_agent = pandas_agent

#     def _run(self, query: str) -> str:
#         return self._pandas_agent.invoke(query)

#     def _arun(self, query: str):
#         raise NotImplementedError("Async not supported")

# class HospitalComparisonAgent:
#     def __init__(self, llm):
#         df = load_hospital_dataframe()
#         print("Loaded hospital data with shape:", df.shape)

#         system_prompt = SystemMessagePromptTemplate.from_template(
#             dedent("""
#             You are a highly skilled healthcare assistant with expertise in comparing hospitals.
#             Your task is to assess various hospitals based on a user's specific conditions, preferences, and needs.
#             You will evaluate hospitals considering:
#               - Medical specialties
#               - Patient reviews and ratings
#               - Location and accessibility
#               - Cost and insurance
#               - Hospital reputation, facilities, and awards
#             Use the "Hospital Type" column to identify well-equipped facilities.
#             Use ALL COLUMNS wisely. Provide well-rounded, personalized suggestions.
#             """)
#         )
#         prompt = ChatPromptTemplate.from_messages([system_prompt])

#         pandas_agent = create_pandas_dataframe_agent(
#             llm=llm,
#             df=df,
#             agent_type="openai-functions",
#             verbose=False,
#             allow_dangerous_code=True,
#             handle_parsing_errors=True
#         )

#         self.agent_tool = HospitalComparisonTool(pandas_agent=pandas_agent)
    
#     def get_agent(self):
#         return self

#     @property
#     def tools(self):
#         return [self.agent_tool]
