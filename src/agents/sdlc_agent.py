from src.llm_service import get_llm_response
from src.models import SDLCRecommendation

class SDLCAgent:
    def recommend_sdlc(self, requirements: dict) -> dict:
        print("-> SDLCAgent: Recommending Software Development Life Cycle (SDLC) model...")
        prompt = f"""
        Based on the following extracted requirements, recommend an appropriate SDLC model 
        (e.g., Agile, DevSecOps, V-Model, Waterfall, Spiral). Consider factors like regulation, security, and uptime.
        
        CRITICAL INSTRUCTION: You must provide a HIGHLY DETAILED development plan. Do not just list 5 bullet points. Break the plan down into extensive phases (Initiation, Design, Development, Security Testing, Deployment), detailing specific roles, deliverables, and compliance checkpoints in each phase.
        
        Requirements: {requirements}
        """
        response = get_llm_response(prompt, response_schema=SDLCRecommendation)
        return response
