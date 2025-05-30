from crewai import Agent, Task, Crew, Process
from textwrap import dedent
from src.agents.hospital_comparison_agent import HospitalComparisonAgent
from src.agents.doctors_info_agent import build_crewai_agent
from src.agents.emergency_service_agent import build_emergency_agent
from src.agents.diagnostic_tests_agent import DiagnosticInfoAgent

# Define a query to be routed
query = "book 1 PM slot for dr lee"

# Router agent that analyzes and delegates
router_agent = Agent(
    role='Router Agent',
    goal='Route medical queries to the correct domain expert agent',
    backstory='Expert at understanding healthcare queries and delegating to the appropriate specialist',
    allow_delegation=True,
    verbose=True
)

# Routing task description
routing_task = Task(
    description=dedent(f"""
        Your task is to analyze the following query and delegate it to the correct expert agent:
        
        Query: "{query}"

        You have the following experts available:
        - Hospital Comparison Agent
        - Doctors Info Agent
        - Emergency Service Agent
        - Diagnostic Info Agent

        Route the query based on its meaning and return the appropriate response.
    """),
    expected_output="The final answer to the routed query.",
    agent=router_agent
)

# Define the crew with all agents
multi_agent_crew = Crew(
    agents=[
        router_agent,
        HospitalComparisonAgent,
        build_crewai_agent,
        build_emergency_agent,
        DiagnosticInfoAgent
    ],
    tasks=[routing_task],
    process=Process.sequential,  # can be parallel if needed
    verbose=True
)

# Execute the crew
result = multi_agent_crew.kickoff()
print("🚀 Final Answer:", result)
