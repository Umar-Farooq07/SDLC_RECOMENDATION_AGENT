from __future__ import annotations

from typing import Any

from agents.common import as_state, audit
from exporters.artefact_exporter import build_artifacts, persist_artifacts
from schemas.models import ProjectState


def documentation(state: ProjectState | dict[str, Any]) -> dict[str, Any]:
    current = as_state(state)
    artifacts = build_artifacts(current)
    paths = persist_artifacts(current, artifacts)
    audit(current, "documentation", f"Generated {len(artifacts)} engineering artefacts")
    return {"artifacts": artifacts, "artifact_files": paths}
