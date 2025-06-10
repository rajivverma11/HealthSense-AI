# src/agents/doctor_slot_agent.py

import httpx
import litellm
from langchain.prompts import PromptTemplate
from langchain_community.agent_toolkits.sql.base import create_sql_agent  
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from crewai import Agent
from crewai.tools import BaseTool
from pydantic import Field
from typing import Any
from src.data.db_loader import get_mysql_uri


# Disable SSL warning for LiteLLM (optional, not recommended in production)
litellm.client_session = httpx.Client(verify=False)

class DoctorSlotAgent:
    def __init__(self, llm=None, db_path=get_mysql_uri(), verbose=False):
        self.llm = llm or ChatOpenAI(model="gpt-4", temperature=0)
        self.verbose = verbose
        self.db = SQLDatabase.from_uri(db_path)

        self.prompt_template = PromptTemplate.from_template(
            '''Answer the following questions as best you can. You have access to the following tools:

        {tools}

        Use the following format:

        Question: the input question you must answer  
        Thought: you should always think about what to do  
        Action: the action to take, should be one of [{tool_names}]  
        Action Input: the input to the action  
        Observation: the result of the action  
        ... (this Thought/Action/Action Input/Observation can repeat N times)  
        Thought: I now know the final answer  
        Final Answer: the final answer to the original input question  

        Match doctor names and specialties using LIKE and lowercase logic. Do not try complex reasoning. Just retrieve and book slots as clearly instructed.  
        If a user provides a specific time (e.g., '3 PM'), try to match it.  
        Update `is_available` to 0 when booking a slot.  
        If no available doctor is found or the request is unclear, reply immediately without retrying endlessly.  
        Begin!

        Question: {input}
        Thought:{agent_scratchpad}'''
        )

        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)

        self.langchain_agent = create_sql_agent(
            llm=self.llm,
            toolkit=self.toolkit,
            prompt=self.prompt_template,
            verbose=self.verbose,
            handle_parsing_errors=True,
            max_iterations=2
        )

    def run_query(self, query: str) -> str:
        try:
            return self.langchain_agent.invoke(query)
        except Exception as e:
            return f"⚠️ Unable to process your request with gpt-3.5-turbo: {str(e)}"

class SlotsQueryTool(BaseTool):
    name: str = "sql_query_tool"
    description: str = "Run SQL queries and analyze database data"
    agent: Any = Field(...)

    def _run(self, query: str) -> str:
        return self.agent.run_query(query)

    def _arun(self, query: str) -> str:
        raise NotImplementedError("Async not supported")

def build_crewai_agent(llm=None) -> Agent:
    agent_impl = DoctorSlotAgent(llm=llm)
    tool = SlotsQueryTool(agent=agent_impl)

    return Agent(
        role="Doctor Slot Manager",
        goal=(
            "Quickly find and book a slot with a doctor who specializes in the patient's condition. "
            "If no match is found, respond clearly and exit without retrying."
        ),
        backstory=(
            "You are a scheduling expert with access to a SQL database of doctors and their availability. "
            "You are trained to interpret vague queries, match them to known medical specialties, and handle slot booking efficiently. "
            "You prioritize speed and clarity. You avoid infinite retries. You can handle both named doctors and generic requests using specialties."
        ),
        tools=[tool],
        verbose=False
    )
