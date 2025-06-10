from fastapi import FastAPI
from pydantic import BaseModel
from src.agents.crew_router_setup import create_crew_router
#from src.data.db_loader import format_patient_context
from src.agents.crew_router_setup import format_patient_context


app = FastAPI()

class UserQuery(BaseModel):
    name: str
    query: str

@app.post("/ask")
def ask(user_query: UserQuery):
    try:
        context = format_patient_context(user_query.name)
        crew, result = create_crew_router(user_query.query, context)
        if isinstance(result, dict):
            final = next(iter(result.values()))
        else:
            final = result
        return {"answer": str(final)}
    except Exception as e:
        return {"error": str(e)}
