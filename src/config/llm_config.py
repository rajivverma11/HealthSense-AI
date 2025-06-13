# src/config/llm_config.py

from langchain_openai import ChatOpenAI
import os
import httpx
import litellm
from src.data.constants import DB_CONFIG,LOCAL_DB_CONFIG

# Optional: Turn off SSL verification for development (not recommended for production)
litellm.client_session = httpx.Client(verify=False)

# Load your OpenAI API key from environment or hardcode for testing (prefer env)
openai_api_key = os.environ.get('OPENAI_API_KEY')
#openai_api_key = LOCAL_DB_CONFIG['OPENAI_API_KEY']  # fallback for dev
print(f"Open API Key is : {openai_api_key}")
       


# Define your LLM
llm = ChatOpenAI(
    temperature=0.0,
    max_tokens=500,
    model_name="gpt-3.5-turbo",
    #model="gpt-4o",  # You can switch to "gpt-3.5-turbo" if cost is a concern 
    openai_api_key=openai_api_key
)

llm_4o = ChatOpenAI(
    temperature=0.0,
    max_tokens=500,
    model_name="gpt-4o",
    #model="gpt-4o",  # You can switch to "gpt-3.5-turbo" if cost is a concern
    openai_api_key=openai_api_key
)
