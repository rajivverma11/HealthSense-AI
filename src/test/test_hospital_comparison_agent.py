from langchain_openai import ChatOpenAI
from src.agents.hospital_comparison_agent import HospitalComparisonAgent

def main():
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    agent_instance = HospitalComparisonAgent(llm)
    agent = agent_instance.get_agent()

    task = "Compare hospitals in San Mateo for cancer treatment with good patient reviews"
    print("Running task:", task)
    result = agent.tools[0].run(task)
    print("Result:\n", result)

if __name__ == "__main__":
    main()
