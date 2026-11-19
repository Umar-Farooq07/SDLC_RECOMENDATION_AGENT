from src.llm_service import get_llm_response

class ComplianceAgent:
    def check_compliance(self, requirements: dict) -> str:
        print("-> ComplianceAgent: Verifying requirements against financial regulations...")
        req_str = str(requirements)
        prompt = f"""
        Review these requirements for any compliance gaps in a financial application context.
        Identify if any crucial security, privacy, or audit controls are missing according to general banking regulations.
        
        Requirements: {req_str}
        """
        return get_llm_response(prompt)
