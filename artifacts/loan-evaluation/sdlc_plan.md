# SDLC Recommendation & Custom Workflow

**Recommended model:** Agile–DevSecOps Hybrid

Agile–DevSecOps Hybrid is selected because the project combines high regulatory and security criticality with legacy integration and a need for iterative delivery.

## Candidate ranking

| Model | Score |
|---|---:|
| Agile–DevSecOps Hybrid | 96.3% |
| Agile–V-Model Hybrid | 91.0% |
| V-Model | 83.0% |
| Spiral | 81.7% |
| Waterfall | 68.5% |
| Agile Scrum | 56.5% |

## Phases

### Discovery & Governance
- Activities: Baseline scope, identify stakeholders and regulatory obligations
- Roles: Product Owner, Compliance
- Security: Threat modeling, MFA/RBAC, SAST/DAST, encrypted audit logs
- Entry / exit: Approved prior-phase outputs and open risks reviewed / Evidence complete; no unresolved critical defects; human gate approved
- Human approval gate: Yes

### Architecture & Threat Modeling
- Activities: Define target architecture, threat model, privacy and security controls
- Roles: Architect, InfoSec
- Security: Threat modeling, MFA/RBAC, SAST/DAST, encrypted audit logs
- Entry / exit: Approved prior-phase outputs and open risks reviewed / Evidence complete; no unresolved critical defects; human gate approved
- Human approval gate: No

### Iterative Delivery
- Activities: Deliver prioritized onboarding increments with CI/CD and peer review
- Roles: Engineering, Product
- Security: Threat modeling, MFA/RBAC, SAST/DAST, encrypted audit logs
- Entry / exit: Approved prior-phase outputs and open risks reviewed / Evidence complete; no unresolved critical defects; human gate approved
- Human approval gate: No

### Verification & Compliance
- Activities: Run functional, integration, SAST/DAST, performance and audit evidence checks
- Roles: QA, InfoSec, Compliance
- Security: Threat modeling, MFA/RBAC, SAST/DAST, encrypted audit logs
- Entry / exit: Approved prior-phase outputs and open risks reviewed / Evidence complete; no unresolved critical defects; human gate approved
- Human approval gate: Yes

### Controlled Release
- Activities: Complete UAT, operational readiness, approval and staged rollout
- Roles: Operations, Business Owner
- Security: Threat modeling, MFA/RBAC, SAST/DAST, encrypted audit logs
- Entry / exit: Approved prior-phase outputs and open risks reviewed / Evidence complete; no unresolved critical defects; human gate approved
- Human approval gate: Yes

### Operate & Improve
- Activities: Monitor SIEM, SLAs, incidents, regulatory changes and backlog
- Roles: Operations, Compliance
- Security: Threat modeling, MFA/RBAC, SAST/DAST, encrypted audit logs
- Entry / exit: Approved prior-phase outputs and open risks reviewed / Evidence complete; no unresolved critical defects; human gate approved
- Human approval gate: No
