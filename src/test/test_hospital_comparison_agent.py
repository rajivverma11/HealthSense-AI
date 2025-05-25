import pandas as pd
from crewai import Agent, Task, Crew, Process
from src.agents.hospital_comparison_agent import HospitalComparisonAgent, PandasTool
from src.data.db_loader import load_hospital_dataframe  # Assuming you load from MySQL

# hospital_agent_instance = HospitalComparisonAgent(df)
# pandas_tool = PandasTool(agent_instance=hospital_agent_instance)  # ✅ Correct usage


# ✅ Step 1: Load hospital data from your database or CSV
df = load_hospital_dataframe()  # returns pd.DataFrame

# ✅ Step 2: Wrap it in your custom LangChain + Pandas agent
hospital_agent_instance = HospitalComparisonAgent(df)

# ✅ Step 3: Wrap that agent in a CrewAI-compatible tool
pandas_tool = PandasTool(agent_instance=hospital_agent_instance)

# ✅ Step 4: Define the CrewAI agent with the correct tool
hospital_info_agent = Agent(
    role='Hospital Information Analyst',
    goal='Analyze hospital data using pandas dataframe and provide relevant output',
    backstory='Expert at analyzing complex datasets using pandas dataframe',
    tools=[pandas_tool],  # ✅ Tools must be attached here
    verbose=True
)

# ✅ Step 5: Create the task
comparison_task = Task(
    description="Which hospital has the best emergency services near San Mateo?",
    agent=hospital_info_agent,
    expected_output="List of top-rated hospitals with emergency services in San Mateo"
)

# ✅ Step 6: Create and run the crew
crew = Crew(
    agents=[hospital_info_agent],
    tasks=[comparison_task],
    process=Process.sequential,
    verbose=True
)

# ✅ Step 7: Kick it off
result = crew.kickoff()
print("\nFinal Output:\n", result)
