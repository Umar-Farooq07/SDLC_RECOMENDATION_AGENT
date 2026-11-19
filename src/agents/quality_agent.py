from src.llm_service import get_llm_response
from src.models import QualityReport

class QualityAgent:
    def analyze_quality(self, requirements: dict) -> dict:
        prompt = f"""
        Analyze these software requirements for ambiguity, incompleteness, or conflicts.
        Requirements: {requirements}
        """
        return get_llm_response(prompt, response_schema=QualityReport)
