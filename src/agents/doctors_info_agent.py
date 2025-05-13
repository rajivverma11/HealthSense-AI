import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
import mysql.connector
from langchain_core.messages import AIMessage
from langchain_community.agent_toolkits.sql.prompt import SQL_FUNCTIONS_SUFFIX
from src.data.constants import LOCAL_DB_CONFIG

class DoctorsInfoAgent:
    def __init__(self, llm_model: str = LOCAL_DB_CONFIG['LLM_MODEL_NAME']):
        

        # ✅ Load OpenAI API Key
        api_key = LOCAL_DB_CONFIG['OPENAI_API_KEY']
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY not found in environment!")

        # ✅ Load MySQL connection details
        mysql_uri = self._get_mysql_uri()

        # ✅ Connect to MySQL database
        self.db = SQLDatabase.from_uri(mysql_uri)

        # ✅ Initialize LLM
        self.llm = ChatOpenAI(model=llm_model, api_key=api_key)

        # ✅ Build SQL Agent Toolkit
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        self.context = self.toolkit.get_context()
        self.tools = self.toolkit.get_tools()

        # ✅ Define Prompt
        messages = [
            HumanMessagePromptTemplate.from_template("{input}"),
            AIMessage(content=SQL_FUNCTIONS_SUFFIX + """
                Use the LIKE operator with lowercase when matching doctor names.
                When a user books a slot, set is_slot_available = 0 (do not delete the row).
                If the user cancels the slot, set is_slot_available = 1 to restore availability.
            """),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]

        prompt = ChatPromptTemplate.from_messages(messages).partial(**self.context)

        # ✅ Create AI Agent
        agent = create_openai_tools_agent(llm=self.llm, tools=self.tools, prompt=prompt)

        # ✅ Finalize Executor
        self.executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def _get_mysql_uri(self) -> str:
        """Builds SQLAlchemy-style MySQL URI from .env"""
        user = LOCAL_DB_CONFIG['user']
        password = LOCAL_DB_CONFIG['password']
        host = LOCAL_DB_CONFIG['host']
        port = LOCAL_DB_CONFIG['port']
        db = LOCAL_DB_CONFIG['database']

        if not all([user, password, host, port, db]):
            raise ValueError("❌ Missing one or more MySQL DB environment variables.")

        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"

    def run(self, user_input: str) -> str:
        """Runs the AI agent against a user query."""
        result = self.executor.invoke({"input": user_input})
        return result["output"]
