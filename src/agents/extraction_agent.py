from src.llm_service import get_llm_response
from src.models import RequirementList

class ExtractionAgent:
    def extract_requirements(self, raw_text: str) -> dict:
        print("-> ExtractionAgent: Analyzing text and extracting structured requirements...")
        prompt = f"""
        Extract the software requirements from the following stakeholder notes.
        Format the output according to the provided schema.
        
        Stakeholder Notes: {raw_text}
        """
        response = get_llm_response(prompt, response_schema=RequirementList)
        return response
