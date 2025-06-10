from crewai import Agent, Task, Crew, Process
from textwrap import dedent
import os
from datetime import datetime

# ✅ Import your agents
from src.agents.doctors_info_agent import build_crewai_agent
from src.agents.emergency_service_agent import build_emergency_agent
from src.agents.diagnostic_tests_agent import DiagnosticInfoAgent
from src.agents.hospital_comparison_agent import HospitalComparisonAgent
from src.config.llm_config import llm
from src.data.db_loader import get_patient_profile

# ✅ LangChain components for memory
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

# ✅ Instantiate all agents
doctor_slots_agent = build_crewai_agent(llm)
emergency_agent = build_emergency_agent(llm)
diagnostic_info_agent = DiagnosticInfoAgent(llm).get_agent()
hospital_info_agent = HospitalComparisonAgent(llm).get_agent()

# ✅ Utilities for per-user memory summary I/O
def get_memory_path(username: str) -> str:
    safe_name = username.lower().replace(" ", "_")
    return f"memory/{safe_name}_summary.txt"

def load_summary(username: str) -> str:
    path = get_memory_path(username)
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""

def save_summary(user_name: str, summary_str: str):
    os.makedirs("memory", exist_ok=True)
    file_path = get_memory_path(user_name)
    with open(file_path, "w") as f:
        f.write(summary_str)

def GetAge(dob_str):
    dob = datetime.strptime(str(dob_str), '%Y-%m-%d %H:%M:%S')
    today = datetime.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def format_patient_context(name: str) -> str:
    patient = get_patient_profile(name)
    if not patient:
        return "User information is not available."
    else:
        patient['Age'] = GetAge(patient['Dateofbirth'])
        return (
            f"The current user is {patient['Name']} , "
            f"a {patient['Age']}-year-old {patient['Gender']},"
            f" whose ethnicity is {patient['Ethnicity']}"
            f" living in {patient['Address']} from state {patient['State']} with zipcode {patient['Zipcode']} "
            f"who is dealing with {patient['Firstdisease']} diseases. "
            f"Use this context to personalize recommendations and responses."
        )

# ✅ Main entry point to build router with persistent summary memory
def create_crew_router(query: str, name: str):
    # ⏪ Load prior summary memory for this user
    initial_summary = load_summary(name)

    summary_memory = ConversationSummaryMemory(
        llm=ChatOpenAI(temperature=0, model="gpt-4"),
        memory_key="chat_history",
        return_messages=True,
        input_key="input"
    )

    # ✅ Router agent now uses per-user summary memory
    router_agent = Agent(
        role='Router Agent',
        goal='Route medical queries to the correct domain expert agent',
        backstory='Expert at understanding healthcare queries and delegating to the appropriate specialist',
        allow_delegation=True,
        verbose=False,
        memory=summary_memory
    )

    memory_context = format_patient_context(name)
    print(f"memory_context: {memory_context}")

    routing_task = Task(
        description=dedent(f"""
        {memory_context}

        You are an intelligent and empathetic healthcare routing agent. Your task is to understand the user's query
        and route it to the most suitable domain expert who can provide an accurate and helpful response.

        🔍 User Query:
        "{query}"

        Based on the user's needs, delegate the query to one of the following expert agents:

        - 🩺 **Doctors Info Agent**: Handles doctor availability and appointment slot booking.
        - 🚨 **Emergency Service Agent**: Provides emergency service availability and hospital readiness info.
        - 🦢 **Diagnostic Info Agent**: Explains lab tests, diagnostics, and testing procedures.
        - 🏥 **Hospital Comparison Agent**: Compares hospitals based on specialties, quality ratings, location, cost, and other attributes.

        ⚠️ Avoid routing vague or underspecified queries such as:
        - "Which hospitals are good?"
        - "I want to see a doctor."
        - "Tell me about tests."

        🧠 In such cases, respond:
        "Please provide more specific details such as the medical condition, location, or hospital features you're interested in."

        Otherwise, determine the correct agent to handle the request, and extract the final result from them. Never say you delegated the task. Always respond with a direct and helpful answer as if it came from you.
        """),
        expected_output="The most appropriate response to the user's query, based on expert input.",
        agent=router_agent,
        max_reruns=3
    )

    crew = Crew(
        agents=[
            router_agent,
            doctor_slots_agent,
            emergency_agent,
            diagnostic_info_agent,
            hospital_info_agent
        ],
        tasks=[routing_task],
        process=Process.sequential,
        verbose=False,
        memory=True
    )

    result = crew.kickoff()

    # ✅ Explicitly save interaction to memory
    summary_memory.save_context(
        inputs={"input": query},
        outputs={"output": str(result)}
    )

    # ✅ Save to file
    chat_history = summary_memory.load_memory_variables({})["chat_history"]
    if chat_history:
        summary_text = "\n".join(
            [f"{msg.type.upper()}: {msg.content}" for msg in chat_history if msg.content.strip()]
        )
        save_summary(name, summary_text)

    return crew, result
