
from crewai import Task
from src.agents.hospital_comparison_agent import HospitalComparisonAgent


hospital_info_task = Task(
    description="I have an emergency, please provide phone number of the hospital nearby San Mateo.",
    expected_output="Phone number of the nearest hospital to San Mateo.",
    agent=HospitalComparisonAgent
)
