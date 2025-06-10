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

litellm.client_session = httpx.Client(verify=False)

class EmergencySQLAgent:
    def __init__(self, llm=None, db_path=get_mysql_uri(), verbose=False):
        self.llm = llm
        self.verbose = verbose
        self.db = SQLDatabase.from_uri(db_path)

        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        self.tools = self.toolkit.get_tools()
        self.tool_names = [tool.name for tool in self.tools]

        self.prompt_template = PromptTemplate(
            input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
            template='''
    You are a hospital emergency services specialist with access to SQL tools.

    Available tools:
    {tools}

    You may ONLY use these tools: [{tool_names}]

    Respond to questions using this format:


    RULES:
    - Query only from table: `hospital_general_information`
    - Use column: `emergencyservices` (with `= 1` for hospitals that offer emergency services)
    - Use 2-letter state codes as-is (e.g., `FL`, `NY`) — do NOT expand to full names
    - Zip code must be used exactly as stored
    - If you find matches, name the hospitals and cities
    - If no match, clearly say that no emergency hospital was found

Question: {input}
{agent_scratchpad}
'''
        )

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
    description: str = "Query hospital_general_information data like EmergencyServices"
    agent: Any = Field(...)

    def _run(self, query: str) -> str:
        return self.agent.run_query(query)

    def _arun(self, query: str) -> str:
        raise NotImplementedError("Async not supported")


def build_emergency_agent(llm=None) -> Agent:
    agent_instance = EmergencySQLAgent(llm=llm)
    tool = EmergencyQueryTool(agent=agent_instance)

    return Agent(
       role='Emergency Information Finder',
        goal='Analyze emergency services availability data',
        backstory='Expert at analyzing complex datasets using SQL',
        tools=[tool],
        verbose=True,
        max_iter=3
    )
