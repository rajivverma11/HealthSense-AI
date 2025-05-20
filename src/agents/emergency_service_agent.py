from src.data.db_loader import get_mysql_uri
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.prompts import PromptTemplate
from langchain.tools import BaseTool

class EmergencyInfoAgent:
    def __init__(self, llm, db_uri=get_mysql_uri(), verbose=True):
        self.llm = llm
        self.verbose = verbose
        self.db_uri = db_uri

        self.db = SQLDatabase.from_uri(self.db_uri)
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)

        self.prompt_template = '''Answer the following questions as best you can. You have access to the following tools:

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

        self.agent = create_sql_agent(
            llm=self.llm,
            toolkit=self.toolkit,
            prompt=PromptTemplate.from_template(self.prompt_template),
            verbose=self.verbose,
            handle_parsing_errors=True
        )

    def run_query(self, query: str) -> str:
        return self.agent.invoke(query)


class EmergencyQueryTool(BaseTool):
    name: str = "sql_query_tool"
    description: str = "Run SQL queries and analyze emergency services data"

    def __init__(self, agent_instance: EmergencyInfoAgent):
        super().__init__()
        self.agent = agent_instance

    def _run(self, query: str) -> str:
        return self.agent.run_query(query)

    def _arun(self, query: str) -> str:
        raise NotImplementedError("Async not supported")
