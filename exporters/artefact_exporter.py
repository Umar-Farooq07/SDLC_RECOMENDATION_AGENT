"""Compile traceable requirements engineering artefacts in Markdown and DOCX."""
from __future__ import annotations

from io import BytesIO
import re
from pathlib import Path
from typing import Any

from config import ARTIFACT_PATH
from schemas.models import ProjectState, RequirementItem


def _requirements(state: ProjectState) -> list[RequirementItem]:
    return [RequirementItem.model_validate(item) for item in state.requirements]


def build_artifacts(state: ProjectState) -> dict[str, str]:
    requirements = _requirements(state)
    loan_scenario = state.scenario == "instant_digital_personal_loan"
    scope = ("Instant Digital Personal Loan Origination, including consent, KFS acknowledgment, "
             "underwriting, disbursal, and cooling-off controls." if loan_scenario else
             "Digital customer onboarding and Video KYC requirements and governance evidence.")
    srs = [
        f"# Software Requirements Specification: {state.project_name}", "",
        f"**Project:** `{state.project_id}`  |  **Domain:** {state.domain}  |  **Scenario:** {state.scenario}",
        "", "## 1. Purpose and Scope", scope,
        "", "## 2. Functional and Non-functional Requirements",
    ]
    for item in requirements:
        srs.extend([
            f"### {item.req_id} — {item.priority}", item.statement,
            f"- **Source:** {item.source_stakeholder}",
            f"- **Evidence:** “{item.source_quote}”",
            f"- **Acceptance criteria:** {'; '.join(item.acceptance_criteria) or 'TBD'}",
            f"- **Classification:** {', '.join(item.categories) or 'Unclassified'}",
        ])
    srs.extend(["", "## 3. Assumptions and Constraints",
                "- Regulatory mappings are evidence-based decision support and require qualified legal review.",
                "- Human approval is required for unresolved conflicts and the final baseline."])
    stories = ["# User Stories and Acceptance Criteria", ""]
    for item in requirements:
        stories.extend([
            f"## {item.req_id}", f"As a {item.source_stakeholder}, I need {item.statement.rstrip('.')} so that the onboarding control is satisfied.",
            "", "```gherkin", "Scenario: Verify requirement outcome",
            f"  Given the stakeholder evidence '{item.source_quote}'",
            "  When the onboarding requirement is evaluated",
            f"  Then {item.acceptance_criteria[0] if item.acceptance_criteria else 'the outcome is verified'}",
            "```", "",
        ])
    use_cases = [
        "# Use-Case Descriptions & Process Workflow", "",
        "## UC-LEND-01 — Originate and disburse a digital personal loan" if loan_scenario else
        "## UC-ONB-01 — Complete digital onboarding with Video KYC", "",
        "- **Primary actor:** Borrower" if loan_scenario else "- **Primary actor:** Retail customer",
        "- **Supporting actors:** Compliance reviewer, lender, Core Banking System" if loan_scenario else
        "- **Supporting actors:** V-CIP officer, Compliance reviewer, Core Banking System",
        "- **Preconditions:** Privacy notice is presented and the customer can authenticate.",
        "- **Trigger:** Customer starts a digital loan application." if loan_scenario else
        "- **Trigger:** Customer starts a new digital account application.",
        "- **Main flow:** Capture purpose-specific consent; collect minimum application data; present the KFS and "
        "record borrower acknowledgment before contract execution; originate and disburse directly through "
        "permitted bank accounts; disclose the cooling-off period." if loan_scenario else
        "- **Main flow:** Capture purpose-specific consent; collect minimum application data; verify PAN and OVD; "
        "perform live V-CIP with liveness and location evidence; complete concurrent audit; create the account "
        "using an idempotency key; notify the customer.",
        "- **Alternate flows:** Network interruption resumes the application; failed checks route to authorized "
        "review; dependency timeout leaves a recoverable pending state.",
        "- **Postconditions:** Consent, disclosures, decisions, transactions, and audit evidence are traceable.",
        "", "## Process sequence", "",
        ("Borrower → Notice & Consent → Underwriting → KFS Acknowledgment → Contract → Direct Disbursal "
         "→ Cooling-off / Servicing" if loan_scenario else
         "Customer → Consent & Notice → Identity / V-CIP Verification → Concurrent Audit → CBS Account Creation "
         "→ Customer Notification"),
    ]
    rtm = ["# Requirements Traceability Matrix", "",
           "| Stakeholder Quote | Req ID | Regulation Citation | Security Control | Test Case |",
           "|---|---|---|---|---|"]
    for item in requirements:
        citation = "; ".join(f"{c.document_title}, {c.section}" for c in item.applicable_regulations) or "Pending legal mapping"
        control = "; ".join(item.security_controls[:2]) or "Pending"
        tests = ", ".join(item.test_case_ids) or f"TC-{item.req_id}"
        rtm.append(f"| {item.source_quote.replace('|', '/')} | {item.req_id} | {citation} | {control} | {tests} |")
    compliance = ["# Compliance-Control Matrix", "",
                  "| Req ID | Source / Section | Evidence | Gaps / Sign-off |",
                  "|---|---|---|---|"]
    for item in requirements:
        if item.applicable_regulations:
            for citation in item.applicable_regulations:
                compliance.append(
                    f"| {item.req_id} | {citation.document_title} — {citation.section} | "
                    f"{citation.supporting_evidence.replace('|', '/')} | "
                    f"{'; '.join(item.compliance_gaps) or ('Legal sign-off required' if item.requires_legal_signoff else 'None identified')} |"
                )
        else:
            compliance.append(f"| {item.req_id} | No grounded citation | — | Legal sign-off required |")
    risks = ["# Threat & Risk Register", "",
             "| Req ID | Likelihood | Impact | Risk | Consequence | Mitigation |",
             "|---|---:|---:|---|---|---|"]
    for item in requirements:
        risks.append(f"| {item.req_id} | {item.likelihood} | {item.impact} | {item.risk_level} | "
                     f"{'; '.join(item.failure_consequences)} | {'; '.join(item.mitigations)} |")
    conflicts = ["## Open Conflicts", ""]
    for item in state.conflicts:
        conflicts.append(f"- **{item.conflict_id} ({item.severity}):** {item.description} "
                         f"Resolution: {item.suggested_resolution}")
    risk_register = "\n".join(risks + [""] + conflicts)
    rec = state.sdlc_recommendation
    plan = ["# SDLC Recommendation & Custom Workflow", "",
            f"**Recommended model:** {rec.selected_model}", "", rec.rationale, "",
            "## Candidate ranking", "", "| Model | Score |", "|---|---:|"]
    plan.extend(f"| {row['model']} | {row['score']}% |" for row in rec.rankings)
    plan.extend(["", "## Phases", ""])
    for phase in rec.workflow:
        plan.extend([
            f"### {phase['phase']}",
            f"- Activities: {phase['activities']}",
            f"- Roles: {phase['responsible_roles']}",
            f"- Security: {phase['security_controls']}",
            f"- Entry / exit: {phase['entry_criteria']} / {phase['exit_criteria']}",
            f"- Human approval gate: {'Yes' if phase['human_approval_gate'] else 'No'}", "",
        ])
    open_items = ["# Assumptions, Dependencies & Open Issues", "",
                  "## Open issues", *[f"- {question}" for question in state.follow_up_questions],
                  "", "## Dependencies", "- Core Banking System REST wrapper and identity verification services.",
                  "- Authorized compliance, InfoSec, legal, and operations reviewers.",
                  "", "## Assumptions", "- Seed knowledge documents are demonstrative source material; verify authoritative current requirements."]
    return {
        "srs.md": "\n".join(srs), "user_stories.md": "\n".join(stories),
        "use_cases.md": "\n".join(use_cases),
        "rtm.md": "\n".join(rtm), "compliance_matrix.md": "\n".join(compliance),
        "risk_register.md": "\n".join(risk_register), "sdlc_plan.md": "\n".join(plan),
        "open_issues.md": "\n".join(open_items),
    }


def docx_bytes(markdown: str, title: str = "Requirements Engineering Artefact") -> bytes:
    try:
        from docx import Document
    except ImportError as exc:
        raise RuntimeError("DOCX export requires python-docx. Install the project requirements.") from exc
    document = Document()
    document.add_heading(title, level=0)
    for line in markdown.splitlines():
        if line.startswith("# "):
            document.add_heading(line[2:], level=1)
        elif line.startswith("## "):
            document.add_heading(line[3:], level=2)
        elif line.startswith("### "):
            document.add_heading(line[4:], level=3)
        elif line.startswith("|"):
            document.add_paragraph(line, style="Caption")
        elif line.startswith("- "):
            document.add_paragraph(line[2:], style="List Bullet")
        elif line:
            document.add_paragraph(line.replace("**", ""))
    output = BytesIO()
    document.save(output)
    return output.getvalue()


def persist_artifacts(state: ProjectState, artifacts: dict[str, str],
                      output_dir: str | Path = ARTIFACT_PATH) -> list[str]:
    project_dir = Path(output_dir) / re.sub(r"[^A-Za-z0-9._-]+", "_", state.project_id).strip("._")
    project_dir.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    for name, markdown in artifacts.items():
        if Path(name).name != name or not name.endswith(".md"):
            raise ValueError(f"Invalid artefact filename: {name}")
        markdown_path = project_dir / name
        markdown_path.write_text(markdown, encoding="utf-8")
        word_path = markdown_path.with_suffix(".docx")
        word_path.write_bytes(docx_bytes(markdown, name.removesuffix(".md")))
        created.extend((str(markdown_path), str(word_path)))
    return created
