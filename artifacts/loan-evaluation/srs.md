# Software Requirements Specification: Digital Customer Onboarding & Video KYC

**Project:** `loan-evaluation`  |  **Domain:** Financial Services  |  **Scenario:** instant_digital_personal_loan

## 1. Purpose and Scope
Instant Digital Personal Loan Origination, including consent, KFS acknowledgment, underwriting, disbursal, and cooling-off controls.

## 2. Functional and Non-functional Requirements
### FR-KYC-001 — Medium
The system shall provide an instant loan decision and disburse funds within 60 seconds for an eligible returning customer.
- **Source:** Product Owner
- **Evidence:** “The system shall provide an instant loan decision and disburse funds within 60 seconds for an eligible returning customer.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall provide an instant loan decision and disburse funds within 60 seconds for an eligible returning customer.
- **Classification:** Stakeholder, Functional
### FR-KYC-002 — Medium
The system shall disburse loan funds immediately before the borrower acknowledges the Key Fact Statement (KFS).
- **Source:** Product Owner
- **Evidence:** “The system shall disburse loan funds immediately before the borrower acknowledges the Key Fact Statement (KFS).”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall disburse loan funds immediately before the borrower acknowledges the Key Fact Statement (KFS).
- **Classification:** Business, Functional
### FR-KYC-003 — Medium
The system shall collect mobile-device contact data for fast underwriting and retain it for future cross-sell.
- **Source:** Product Owner
- **Evidence:** “The system shall collect mobile-device contact data for fast underwriting and retain it for future cross-sell.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall collect mobile-device contact data for fast underwriting and retain it for future cross-sell.
- **Classification:** Functional, Performance, Data Management
### FR-REG-001 — Medium
The system shall present the Key Fact Statement and capture durable borrower acknowledgment before loan contract execution and disbursal.
- **Source:** Compliance Officer
- **Evidence:** “The system shall present the Key Fact Statement and capture durable borrower acknowledgment before loan contract execution and disbursal.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall present the Key Fact Statement and capture durable borrower acknowledgment before loan contract execution and disbursal.
- **Classification:** Business, Functional, Integration
### FR-REG-002 — High
The system shall obtain explicit purpose-specific borrower consent before collecting or sharing personal data for underwriting.
- **Source:** Compliance Officer
- **Evidence:** “The system shall obtain explicit purpose-specific borrower consent before collecting or sharing personal data for underwriting.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall obtain explicit purpose-specific borrower consent before collecting or sharing personal data for underwriting.
- **Classification:** Business, Functional, Privacy, Data Management
### FR-REG-003 — Medium
The system shall disburse directly between the borrower and the regulated entity's bank account and disclose the applicable cooling-off period.
- **Source:** Compliance Officer
- **Evidence:** “The system shall disburse directly between the borrower and the regulated entity's bank account and disclose the applicable cooling-off period.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall disburse directly between the borrower and the regulated entity's bank account and disclose the applicable cooling-off period.
- **Classification:** Business, Functional
### NFR-SEC-001 — High
The system shall use TLS 1.3 in transit, AES-256 at rest, MFA for sensitive actions, least-privilege RBAC, and immutable audit logging.
- **Source:** InfoSec Architect
- **Evidence:** “The system shall use TLS 1.3 in transit, AES-256 at rest, MFA for sensitive actions, least-privilege RBAC, and immutable audit logging.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall use TLS 1.3 in transit, AES-256 at rest, MFA for sensitive actions, least-privilege RBAC, and immutable audit logging.
- **Classification:** Functional, Security, Audit & Reporting
### FR-KYC-004 — Medium
The system shall use idempotency keys for disbursal requests and safely handle duplicate callbacks and interrupted network connections.
- **Source:** Software Architect
- **Evidence:** “The system shall use idempotency keys for disbursal requests and safely handle duplicate callbacks and interrupted network connections.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall use idempotency keys for disbursal requests and safely handle duplicate callbacks and interrupted network connections.
- **Classification:** Functional

## 3. Assumptions and Constraints
- Regulatory mappings are evidence-based decision support and require qualified legal review.
- Human approval is required for unresolved conflicts and the final baseline.