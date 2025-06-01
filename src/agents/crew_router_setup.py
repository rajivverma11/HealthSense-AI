from crewai import Agent, Task, Crew, Process
from textwrap import dedent

# ✅ Import your agents
from src.agents.doctors_info_agent import build_crewai_agent
from src.agents.emergency_service_agent import build_emergency_agent
from src.agents.diagnostic_tests_agent import DiagnosticInfoAgent
from src.agents.hospital_comparison_agent import HospitalComparisonAgent
from src.config.llm_config import llm

# ✅ Instantiate all agents
doctor_slots_agent = build_crewai_agent(llm)
emergency_agent = build_emergency_agent(llm)
diagnostic_info_agent = DiagnosticInfoAgent(llm).get_agent()
hospital_info_agent = HospitalComparisonAgent(llm).get_agent()

# ✅ Router agent
router_agent = Agent(
    role='Router Agent',
    goal='Route medical queries to the correct domain expert agent',
    backstory='Expert at understanding healthcare queries and delegating to the appropriate specialist',
    allow_delegation=True,
    verbose=False
)

# ✅ Dynamic function to build the crew with a routed task
def create_crew_router(query: str):
    routing_task = Task(
        description=dedent(f"""
            You are a smart healthcare router agent. Your job is to understand the user's query and delegate it 
            to the correct expert agent who can best answer it.

            The user's query is:
            "{query}"

            You can delegate the query to one of these agents:
            - Doctors Info Agent: Handles doctor availability and appointment booking
            - Emergency Service Agent: Handles emergency services and hospital readiness
            - Diagnostic Info Agent: Provides information about lab tests and diagnostics
            - Hospital Comparison Agent: Compares hospitals based on specialties, ratings, cost, and location

            Avoid routing vague or underspecified queries like:
            - "Which hospitals are good?"
            - "I want to see a doctor"
            - "Tell me about tests"

            If the query is too vague or lacks location/specialty/condition details, respond:
            "Please provide more specific details such as the condition, location, or hospital features you care about."

            Otherwise, delegate the query to the appropriate agent and return their final answer.
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
        memory=False
    )

    result = crew.kickoff()
    return crew, result
