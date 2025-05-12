from src.agents.hospital_comparison_agent import HospitalComparisonAgent
from src.data.db_loader import load_hospital_dataframe
import pandas as pd

def main():
    # Load data
    
    df = load_hospital_dataframe()
    # Initialize agent
    agent = HospitalComparisonAgent(df)

    # Test a query
    query = "I have an emergency, please provide phone number of the hospital nearby cumming GA."
    result = agent.compare(query)

    print("Response:")
    print(result)

if __name__ == "__main__":
    main()
