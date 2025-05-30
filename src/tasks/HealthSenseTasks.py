from crewai import Task
from src.agents.hospital_comparison_agent import HospitalComparisonAgent
from src.agents.doctors_info_agent import DoctorsInfoAgent
from src.agents.emergency_service_agent import EmergencyServiceAgent
from src.agents.diagnostic_tests_agent import DiagnosticInfoAgent


hospital_info_task = Task(
    description="I have an emergency, please provide phone number of the hospital nearby San Mateo.",
    expected_output="Phone number of the nearest hospital to San Mateo.",
    agent=HospitalComparisonAgent
)

doctor_slots_task = Task(description="show slots for lee",
                         expected_output='',
                         agent=DoctorsInfoAgent)


emergency_task = Task(description="any ambulance available at 94404",
                      expected_output='',
                      agent=EmergencyServiceAgent)

diagnostic_info_task = Task(description="what would be preparation instructions for cancer screening",
                        expected_output='',
                        agent=DiagnosticInfoAgent)

