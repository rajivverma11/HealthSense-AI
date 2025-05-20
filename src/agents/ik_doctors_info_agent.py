from src.data.db_loader import get_mysql_uri
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.prompts import PromptTemplate
from langchain.tools import BaseTool
from langchain_community.utilities import SQLDatabase
from langchain.agents.agent_types import AgentType

class DoctorSlotAgent:
    def __init__(self, llm, db_uri=get_mysql_uri(), verbose=True):
        self.db = SQLDatabase.from_uri(db_uri)
        self.llm = llm
        self.verbose = verbose

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

Use like operator with lowercase when matching a name.
When a user is asking to book slots for any dr, STRICTLY Delete the corresponding row from the table.
Begin!

Question: {input}
Thought:{agent_scratchpad}'''

        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)

        self.agent = create_sql_agent(
            llm=self.llm,
            toolkit=self.toolkit,
            prompt=PromptTemplate.from_template(self.prompt_template),
            verbose=self.verbose,
            handle_parsing_errors=True
        )

    def run_query(self, user_query: str):
        """Invoke the LangChain SQL agent with a user query."""
        return self.agent.invoke(user_query)


class SlotsQueryTool(BaseTool):
    name: str = "sql_query_tool"
    description: str = "Run SQL queries and analyze database data"

    def __init__(self, agent_instance: DoctorSlotAgent):
        super().__init__()
        self.agent = agent_instance

    def _run(self, query: str) -> str:
        return self.agent.run_query(query)

    def _arun(self, query: str) -> str:
        raise NotImplementedError("Async not supported")
