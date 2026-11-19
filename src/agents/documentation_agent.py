from src.llm_service import get_llm_response
from src.models import DocumentationArtifacts

class DocumentationAgent:
    def generate_artifacts(self, requirements: dict) -> dict:
        prompt = f"""
        Generate Agile User Stories (As a... I want to... So that...) based on these requirements:
        Requirements: {requirements}
        """
        return get_llm_response(prompt, response_schema=DocumentationArtifacts)
