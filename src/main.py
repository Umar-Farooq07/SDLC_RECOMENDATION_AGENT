import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from src.agents.orchestrator import Orchestrator

def main():
    # Load environment variables from .env if present
    load_dotenv()
    
    # Read sample input
    sample_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sample_input.txt")
    try:
        with open(sample_path, "r") as f:
            stakeholder_input = f.read()
    except FileNotFoundError:
        stakeholder_input = (
            "We need a new mobile banking app. It must have secure login with two-factor authentication. "
            "Users should be able to transfer money internationally. The system must process transactions within 2 seconds. "
            "We are heavily regulated so audit logs for every transaction are mandatory. System uptime must be 99.99%."
        )

    print("Stakeholder Input Loaded:\n")
    print(stakeholder_input)
    
    orchestrator = Orchestrator()
    orchestrator.run_pipeline(stakeholder_input)

if __name__ == "__main__":
    main()
