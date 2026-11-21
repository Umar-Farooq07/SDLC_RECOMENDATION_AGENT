# Software Requirements Specification: Digital Customer Onboarding & Video KYC

**Project:** `onboarding-evaluation`  |  **Domain:** Financial Services  |  **Scenario:** onboarding

## 1. Purpose and Scope
Digital customer onboarding and Video KYC requirements and governance evidence.

## 2. Functional and Non-functional Requirements
### FR-REG-001 — High
The system shall complete live V-CIP with customer consent, liveness detection, live location and timestamp capture, and trained-official verification.
- **Source:** Compliance Officer
- **Evidence:** “The system shall complete live V-CIP with customer consent, liveness detection, live location and timestamp capture, and trained-official verification.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall complete live V-CIP with customer consent, liveness detection, live location and timestamp capture, and trained-official verification.
- **Classification:** Stakeholder, Functional, Privacy, Regulatory
### FR-REG-002 — High
The system shall verify PAN using an authorized service and verify an OVD or permitted equivalent before account activation.
- **Source:** Compliance Officer
- **Evidence:** “The system shall verify PAN using an authorized service and verify an OVD or permitted equivalent before account activation.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall verify PAN using an authorized service and verify an OVD or permitted equivalent before account activation.
- **Classification:** Business, Functional, Regulatory
### NFR-SEC-001 — High
The system shall retain encrypted V-CIP video and associated audit evidence for at least five years, subject to a longer statutory retention obligation.
- **Source:** Compliance Officer
- **Evidence:** “The system shall retain encrypted V-CIP video and associated audit evidence for at least five years, subject to a longer statutory retention obligation.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall retain encrypted V-CIP video and associated audit evidence for at least five years, subject to a longer statutory retention obligation.
- **Classification:** Functional, Security, Regulatory, Data Management, Audit & Reporting
### NFR-SEC-002 — High
The system shall complete concurrent audit of the V-CIP record before account activation; exceptions require authorized review.
- **Source:** Compliance Officer
- **Evidence:** “The system shall complete concurrent audit of the V-CIP record before account activation; exceptions require authorized review.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall complete concurrent audit of the V-CIP record before account activation; exceptions require authorized review.
- **Classification:** Business, Functional, Regulatory, Data Management, Audit & Reporting
### FR-REG-003 — High
The system shall present an itemized privacy notice and record explicit purpose-specific consent before collecting personal data.
- **Source:** Compliance Officer
- **Evidence:** “The system shall present an itemized privacy notice and record explicit purpose-specific consent before collecting personal data.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall present an itemized privacy notice and record explicit purpose-specific consent before collecting personal data.
- **Classification:** Functional, Privacy, Data Management
### FR-REG-004 — High
The system shall limit collection to the stated purpose and erase data when the purpose ends unless statutory banking retention applies.
- **Source:** Compliance Officer
- **Evidence:** “The system shall limit collection to the stated purpose and erase data when the purpose ends unless statutory banking retention applies.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall limit collection to the stated purpose and erase data when the purpose ends unless statutory banking retention applies.
- **Classification:** Functional, Privacy, Regulatory, Data Management
### NFR-SEC-003 — High
The system shall retain evidence of consent, verification, audit decisions, retention basis, and customer rights requests.
- **Source:** Compliance Officer
- **Evidence:** “The system shall retain evidence of consent, verification, audit decisions, retention basis, and customer rights requests.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall retain evidence of consent, verification, audit decisions, retention basis, and customer rights requests.
- **Classification:** Stakeholder, Functional, Privacy, Regulatory, Data Management, Audit & Reporting
### NFR-SEC-004 — Medium
The system shall use TLS 1.3 in transit and AES-256 encryption at rest for customer, identity, and video data.
- **Source:** InfoSec Architect
- **Evidence:** “The system shall use TLS 1.3 in transit and AES-256 encryption at rest for customer, identity, and video data.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall use TLS 1.3 in transit and AES-256 encryption at rest for customer, identity, and video data.
- **Classification:** Stakeholder, Functional, Security, Data Management
### NFR-SEC-005 — High
The system shall require MFA or step-up authentication for account activation and transactions above INR 50,000, with least-privilege RBAC.
- **Source:** InfoSec Architect
- **Evidence:** “The system shall require MFA or step-up authentication for account activation and transactions above INR 50,000, with least-privilege RBAC.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall require MFA or step-up authentication for account activation and transactions above INR 50,000, with least-privilege RBAC.
- **Classification:** Business, Functional, Security
### NFR-SEC-006 — Medium
The system shall expire interactive sessions after 15 minutes of inactivity and re-authenticate sensitive actions.
- **Source:** InfoSec Architect
- **Evidence:** “The system shall expire interactive sessions after 15 minutes of inactivity and re-authenticate sensitive actions.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall expire interactive sessions after 15 minutes of inactivity and re-authenticate sensitive actions.
- **Classification:** Functional, Security
### NFR-SEC-007 — High
The system shall send immutable security, consent, identity, and approval events to SIEM-backed audit storage.
- **Source:** InfoSec Architect
- **Evidence:** “The system shall send immutable security, consent, identity, and approval events to SIEM-backed audit storage.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall send immutable security, consent, identity, and approval events to SIEM-backed audit storage.
- **Classification:** Functional, Security, Privacy, Data Management, Audit & Reporting
### FR-KYC-001 — Medium
The system shall integrate with the legacy Core Banking System REST wrapper, whose API dependency is limited to 2,000 ms response time.
- **Source:** Software Architect
- **Evidence:** “The system shall integrate with the legacy Core Banking System REST wrapper, whose API dependency is limited to 2,000 ms response time.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall integrate with the legacy Core Banking System REST wrapper, whose API dependency is limited to 2,000 ms response time.
- **Classification:** Functional, Performance, Integration
### FR-KYC-002 — Medium
The system shall use an idempotency key for account creation and recover safely from retries and duplicate delivery.
- **Source:** Software Architect
- **Evidence:** “The system shall use an idempotency key for account creation and recover safely from retries and duplicate delivery.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall use an idempotency key for account creation and recover safely from retries and duplicate delivery.
- **Classification:** Functional
### FR-KYC-003 — Medium
The system shall schedule end-of-day reconciliation from 00:00 to 01:30 IST and monitor pending onboarding exceptions.
- **Source:** Operations Lead
- **Evidence:** “The system shall schedule end-of-day reconciliation from 00:00 to 01:30 IST and monitor pending onboarding exceptions.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall schedule end-of-day reconciliation from 00:00 to 01:30 IST and monitor pending onboarding exceptions.
- **Classification:** Business, Functional, Availability & Reliability, Operational & Maintenance
### NFR-SEC-008 — High
The system shall activate an account instantly after the customer submits the onboarding form, without waiting for a concurrent audit.
- **Source:** Product Owner
- **Evidence:** “The system shall activate an account instantly after the customer submits the onboarding form, without waiting for a concurrent audit.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall activate an account instantly after the customer submits the onboarding form, without waiting for a concurrent audit.
- **Classification:** Business, Stakeholder, Functional, Audit & Reporting
### FR-KYC-004 — Medium
The system shall retain behavioral analytics and onboarding video indefinitely so marketing can improve conversion.
- **Source:** Product Owner
- **Evidence:** “The system shall retain behavioral analytics and onboarding video indefinitely so marketing can improve conversion.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall retain behavioral analytics and onboarding video indefinitely so marketing can improve conversion.
- **Classification:** Business, Functional, Data Management
### FR-KYC-005 — Medium
The system shall complete onboarding and all connected API calls within 500 ms end-to-end.
- **Source:** Product Owner
- **Evidence:** “The system shall complete onboarding and all connected API calls within 500 ms end-to-end.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall complete onboarding and all connected API calls within 500 ms end-to-end.
- **Classification:** Business, Functional, Performance, Integration
### FR-KYC-006 — Medium
The system shall run a fast liveness check and raise an alert for high-value applications.
- **Source:** Product Owner
- **Evidence:** “The system shall run a fast liveness check and raise an alert for high-value applications.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall run a fast liveness check and raise an alert for high-value applications.
- **Classification:** Functional, Performance
### NFR-SEC-009 — Medium
The system shall use standard encryption for all customer data.
- **Source:** Product Owner
- **Evidence:** “The system shall use standard encryption for all customer data.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall use standard encryption for all customer data.
- **Classification:** Stakeholder, Functional, Security, Data Management
### FR-KYC-007 — Medium
The system shall support retry after network interruption and let customers resume an incomplete application.
- **Source:** Product Owner
- **Evidence:** “The system shall support retry after network interruption and let customers resume an incomplete application.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall support retry after network interruption and let customers resume an incomplete application.
- **Classification:** Stakeholder, Functional, Operational & Maintenance
### FR-KYC-008 — Medium
The system shall priority is a low-friction flow; exceptions should be reviewed by an operations user.
- **Source:** Product Owner
- **Evidence:** “Priority is a low-friction flow; exceptions should be reviewed by an operations user.”
- **Acceptance criteria:** Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: Priority is a low-friction flow; exceptions should be reviewed by an operations user.
- **Classification:** Functional, Usability, Operational & Maintenance

## 3. Assumptions and Constraints
- Regulatory mappings are evidence-based decision support and require qualified legal review.
- Human approval is required for unresolved conflicts and the final baseline.