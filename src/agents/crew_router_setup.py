
from crewai import Agent, Task, Crew, Process
from textwrap import dedent
#from src.agents.hospital_comparison_agent import HospitalComparisonAgent
from src.agents.doctors_info_agent import build_crewai_agent
from src.agents.emergency_service_agent import build_emergency_agent
from src.agents.diagnostic_tests_agent import DiagnosticInfoAgent
#from src.data.db_loader import get_mysql_uri
from src.config.llm_config import llm 

# ✅ Initialize your three working agents
doctor_slots_agent = build_crewai_agent(llm)
emergency_agent = build_emergency_agent(llm)
diagnostic_info_agent = DiagnosticInfoAgent(llm).get_agent()

# ✅ Define router agent
router_agent = Agent(
    role='Router Agent',
    goal='Route medical queries to the correct domain expert agent',
    backstory='Expert at understanding healthcare queries and delegating to the appropriate specialist',
    allow_delegation=True,
    verbose=False  # Turn on for debugging
)

# ✅ Function to create and run the crew
def create_crew_router(query: str):
    routing_task = Task(
        description=dedent(f"""
            Your task is to analyze the following user query and delegate it to the most appropriate expert agent.

            Query: "{query}"

            You can delegate to one of these agents:
            - Doctors Info Agent
            - Emergency Service Agent
            - Diagnostic Info Agent

            Think carefully about the query's intent and route it accordingly. Respond with a final answer from the selected expert.
        """),
        expected_output="The expert agent's final response to the user's query.",
        agent=router_agent,
        max_reruns=2
    )

    # ✅ Define crew with all agents and just the routing task
    crew = Crew(
        agents=[
            router_agent,
            doctor_slots_agent,
            emergency_agent,
            diagnostic_info_agent
        ],
        tasks=[routing_task],
        process=Process.sequential,
        verbose=False,  # See full agent logs
        memory=False   # Optional: can enable later
    )

    # ✅ Execute and return both the crew object and the result
    result = crew.kickoff()
    return crew, result




