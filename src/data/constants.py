import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_CONFIG ={
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    'LLM_MODEL_NAME': os.getenv('LLM_MODEL_NAME')
   
}


LOCAL_DB_CONFIG = {
    'host': os.getenv('LOCAL_DB_HOST'),
    'user': os.getenv('LOCAL_DB_USER'),
    'password': os.getenv('LOCAL_DB_PASSWORD'),
    'database': os.getenv('LOCAL_DB_NAME'),
    'port': int(os.getenv('LOCAL_DB_PORT', 3306)),
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    'LLM_MODEL_NAME': os.getenv('LLM_MODEL_NAME')

}