import httpx
import litellm
from langchain.prompts import PromptTemplate
from langchain.agents import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI
from crewai import Agent
from crewai.tools import BaseTool
from pydantic import Field
from typing import Any
from src.data.db_loader import get_mysql_uri

litellm.client_session = httpx.Client(verify=False)

class EmergencySQLAgent:
    def __init__(self, llm=None, db_path=get_mysql_uri(), verbose=True):
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

Use like operator with lowercase when matching a name. When user is asking to book slots, delete the corresponding row from the table.
Begin!

Question: {input}
Thought:{agent_scratchpad}'''
        )

        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)

        self.agent = create_sql_agent(
            llm=self.llm,
            toolkit=self.toolkit,
            prompt=self.prompt_template,
            verbose=self.verbose,
            handle_parsing_errors=True,
        )

    def run_query(self, query: str) -> str:
        return self.agent.invoke(query)


class EmergencyQueryTool(BaseTool):
    name: str = "sql_query_tool"
    description: str = "Run SQL queries and analyze emergency database"
    agent: Any = Field(...)

    def _run(self, query: str) -> str:
        return self.agent.run_query(query)

    def _arun(self, query: str) -> str:
        raise NotImplementedError("Async not supported")


def build_emergency_agent(llm=None) -> Agent:
    agent_instance = EmergencySQLAgent(llm=llm)
    tool = EmergencyQueryTool(agent=agent_instance)

    return Agent(
        role="Emergency Information Finder",
        goal="Analyze emergency services availability data",
        backstory="Expert at analyzing emergency SQL databases for time-sensitive decisions",
        tools=[tool],
        verbose=True
    )