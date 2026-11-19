import os
import json
import re
from pydantic import BaseModel
from huggingface_hub import InferenceClient

def get_llm_response(prompt: str, response_schema=None):
    """
    Calls the Hugging Face Inference API using an open-source model if HF_TOKEN is set.
    Otherwise, returns a simulated response so the project can still run.
    """
    hf_token = os.environ.get("HF_TOKEN")
    
    # We use Mistral-Nemo-Instruct, a powerful open-source model available for free on HF
    repo_id = "mistralai/Mistral-Nemo-Instruct-2407"
    
    if hf_token:
        client = InferenceClient(api_key=hf_token)
        
        # Adjust prompt for JSON if a schema is expected
        if response_schema:
            prompt += f"\n\nRespond ONLY with valid JSON matching this schema. Do not add any conversational text or markdown blocks:\n{response_schema.model_json_schema()}"
            
        print(f"    [LLM Service] Querying open-source model: {repo_id}...")
        
        messages = [{"role": "user", "content": prompt}]
        response = client.chat_completion(
            model=repo_id,
            messages=messages,
            max_tokens=2500,
            temperature=0.1
        )
        
        response_text = response.choices[0].message.content.strip()
        
        if response_schema:
            try:
                # Attempt to extract JSON from the response
                json_str = extract_json(response_text)
                return json.loads(json_str)
            except json.JSONDecodeError:
                print("    [LLM Service] Failed to parse JSON from open-source model. Returning mock data as fallback.")
                return _mock_response(prompt, response_schema)
        return response_text
    else:
        # Fallback for course project if no API key is provided
        return _mock_response(prompt, response_schema)

def extract_json(text: str) -> str:
    """Helper to extract JSON block from markdown if the model wraps it."""
    match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def _mock_response(prompt: str, schema):
    if schema and schema.__name__ == 'RequirementList':
        return {
            "requirements": [
                {"req_id": "FR-001", "statement": "The system must process payments in under 1 second.", "category": "Functional", "risk_level": "Medium", "priority": "High", "confidence_score": "95%", "acceptance_criteria": ["Response < 1s", "Success code 200"]},
                {"req_id": "SEC-001", "statement": "All users must use 2FA via authenticator app.", "category": "Security", "risk_level": "High", "priority": "High", "confidence_score": "99%", "acceptance_criteria": ["Prompt for 2FA", "SMS blocked"]},
                {"req_id": "COMP-001", "statement": "Extensive audit trail of every financial transaction is required.", "category": "Compliance", "risk_level": "High", "priority": "High", "confidence_score": "90%", "acceptance_criteria": ["Log saved to DB", "Log is immutable"]}
            ]
        }
    elif schema and schema.__name__ == 'QualityReport':
        return {
            "ambiguity_detected": True,
            "missing_information": [
                "No fallback behavior specified if a third-party API (e.g., Equifax) is unreachable",
                "No maximum transaction value limit mentioned",
                "Missing data retention period for audit logs",
                "No details on supported browsers or mobile OS versions"
            ],
            "clarification_questions": [
                "What should the system do if the credit scoring API is temporarily unavailable — reject the application, queue it, or allow manual override?",
                "Is there a maximum transaction amount above which additional approval is required?",
                "How long must audit logs be stored before they can be deleted (e.g., 5 years, 7 years)?",
                "Which mobile platforms must be supported — iOS only, Android only, or both?"
            ]
        }
    elif schema and schema.__name__ == 'DocumentationArtifacts':
        return {
            "user_stories": [
                {"story_id": "US-001", "as_a": "Loan Officer", "i_want_to": "securely log in using 2FA", "so_that": "I can access sensitive customer data safely"},
                {"story_id": "US-002", "as_a": "Customer", "i_want_to": "submit my application online", "so_that": "I don't have to visit a physical branch"}
            ]
        }
    elif schema and schema.__name__ == 'SDLCRecommendation':
        return {
            "model_name": "Agile-DevSecOps Hybrid",
            "confidence": "92%",
            "justification": "High security and compliance requirements along with the need for a highly available system strongly suggest DevSecOps.",
            "development_plan": "### Phase 1: Initiation & Requirements\n- **Activities:** Define business goals, extract exact regulatory needs (e.g., Banking Authority rules), and perform initial threat modeling.\n- **Roles:** Product Manager, Compliance Officer, Lead Architect.\n- **Deliverables:** Approved Requirements Specification, Risk Register.\n- **Gates:** Compliance Sign-off.\n\n### Phase 2: System & Security Design\n- **Activities:** Architect highly available (99.99%) cloud infrastructure. Design the 2FA authentication flow and encrypted audit log architecture.\n- **Roles:** Cloud Architect, Security Engineer.\n- **Deliverables:** Architecture Diagrams, Threat Model Document.\n- **Gates:** Security Architecture Review Board Approval.\n\n### Phase 3: Implementation (Sprints)\n- **Activities:** Develop microservices for payments and user management. Implement real-time transaction processing. Integrate Static Application Security Testing (SAST) into the IDEs.\n- **Roles:** Backend/Frontend Developers, QA.\n- **Deliverables:** Feature branches, Unit tests.\n- **Gates:** Peer Code Review, automated SAST pass.\n\n### Phase 4: Automated Testing & Security Validation\n- **Activities:** Execute Dynamic Application Security Testing (DAST). Perform load testing to guarantee under 1-second response time. Validate CSV export formatting.\n- **Roles:** QA Automation Engineer, Penetration Tester.\n- **Deliverables:** Test Execution Report, Pen-Test Summary.\n- **Gates:** Zero Critical/High vulnerabilities remaining.\n\n### Phase 5: Deployment & Continuous Monitoring\n- **Activities:** Deploy via CI/CD pipelines using blue/green deployment to ensure zero downtime. Activate transaction audit logging. Set up alerts for uptime monitoring.\n- **Roles:** DevOps Engineer, Site Reliability Engineer (SRE).\n- **Deliverables:** Production Environment, Monitoring Dashboards.\n- **Gates:** Final Go/No-Go Business Approval."
        }
    else:
        if "compliance" in prompt.lower():
            return "COMPLIANCE REPORT:\n- SEC-001 (2FA) aligns perfectly with banking authentication standards.\n- COMP-001 (Audit trail) satisfies the Banking Authority regulations.\n- No compliance gaps identified in the provided requirements."
        return "Mock response generated successfully."
