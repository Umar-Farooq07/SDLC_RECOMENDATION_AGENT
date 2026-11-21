"""Application configuration loaded from environment variables."""
from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

_env_file = BASE_DIR / ".env"
if _env_file.is_file():
    for _line in _env_file.read_text(encoding="utf-8").splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _key, _value = _line.split("=", 1)
            os.environ.setdefault(_key.strip(), _value.strip().strip("\"'"))

DATABASE_PATH = Path(os.getenv("DATABASE_PATH", BASE_DIR / "data" / "requirements.db"))
CHROMA_PATH = Path(os.getenv("CHROMA_PATH", BASE_DIR / "data" / "chroma"))
KB_PATH = Path(os.getenv("KB_PATH", BASE_DIR / "kb_docs"))
ARTIFACT_PATH = Path(os.getenv("ARTIFACT_PATH", BASE_DIR / "artifacts"))
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock").lower()
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
MAX_CLARIFICATION_ROUNDS = 2
MCDA_WEIGHTS = {
    "regulatory_criticality": 0.14,
    "security_risk": 0.12,
    "testing_rigor": 0.12,
    "formal_verification_need": 0.10,
    "requirement_stability": 0.08,
    "project_complexity": 0.08,
    "legacy_dependence": 0.08,
    "failure_consequence": 0.08,
    "continuous_delivery_need": 0.06,
    "change_frequency": 0.05,
    "stakeholder_availability": 0.04,
    "system_size": 0.03,
    "budget_schedule_constraint": 0.02,
}


def create_chat_model(provider: str | None = None, model: str | None = None):
    """Create the configured LangChain chat model, or return None for offline mock mode."""
    selected = (provider or LLM_PROVIDER).lower()
    model_name = model or LLM_MODEL
    credentials = {
        "openai": os.getenv("OPENAI_API_KEY"),
        "google": os.getenv("GOOGLE_API_KEY"),
        "anthropic": os.getenv("ANTHROPIC_API_KEY"),
    }
    if selected == "mock" or not credentials.get(selected):
        if selected not in {"mock", "openai", "google", "anthropic"}:
            raise ValueError(f"Unsupported LLM_PROVIDER: {selected}")
        return None
    if selected == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=model_name, api_key=credentials[selected], temperature=0)
    if selected == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=model_name or "gemini-2.5-pro", google_api_key=credentials[selected],
                                      temperature=0)
    from langchain_anthropic import ChatAnthropic
    return ChatAnthropic(model=model_name, api_key=credentials[selected], temperature=0)
