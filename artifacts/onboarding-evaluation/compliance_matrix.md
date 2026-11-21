# Compliance-Control Matrix

| Req ID | Source / Section | Evidence | Gaps / Sign-off |
|---|---|---|---|
| FR-REG-001 | RBI KYC Direction: Video-based Customer Identification Process (V-CIP) — V-CIP process controls | ## V-CIP process controls
The regulated entity shall conduct V-CIP using a secure, live, informed-consent interaction with a trained official. The official shall confirm the customer's identity and record the process in an auditable manner. | Legal sign-off required |
| FR-REG-001 | RBI KYC Direction: Video-based Customer Identification Process (V-CIP) — Live location and liveness | ## Live location and liveness
The process shall capture live location and timestamp evidence and use liveness controls to reduce spoofing, replay, and impersonation risk. Failed liveness or interrupted connectivity shall route the case to a controlled exception and review process. | Legal sign-off required |
| FR-REG-001 | Digital Personal Data Protection Act, 2023: Financial Services Control Notes — Accountability | ## Accountability
The organization shall maintain evidence of notices, consent, processing purposes, access, security controls, retention decisions, and rights requests. | Legal sign-off required |
| FR-REG-002 | RBI KYC Direction: Video-based Customer Identification Process (V-CIP) — PAN and Officially Valid Document | ## PAN and Officially Valid Document
PAN shall be verified through an authorized issuer or verification service such as NSDL or UTIITSL. An Officially Valid Document (OVD) or permitted equivalent shall be verified and associated with the customer record before account activation. | Legal sign-off required |
| FR-REG-002 | RBI Digital Lending Directions — Disbursal and repayment | ## Disbursal and repayment
Loan disbursal and repayment shall flow directly between the borrower and the regulated entity's bank account, subject to applicable permitted arrangements. The system shall retain an auditable transaction trail. | Legal sign-off required |
| FR-REG-002 | Legacy Core Banking Integration Interface — Interface and protocol | ## Interface and protocol
The legacy Core Banking System (CBS) exposes an ISO-8583 transaction interface and a REST wrapper for customer and account operations. Integrations shall validate schemas, map error codes, and preserve the CBS transaction reference. | Legal sign-off required |
| NFR-SEC-001 | RBI KYC Direction: Video-based Customer Identification Process (V-CIP) — Video and audit retention | ## Video and audit retention
V-CIP video and associated audit logs shall be encrypted and retained for at least five years, or longer where another applicable statutory obligation requires it. Access shall be restricted, logged, and available for authorized audit. | Legal sign-off required |
| NFR-SEC-001 | Legacy Core Banking Integration Interface — Latency and availability | ## Latency and availability
The CBS API dependency has a 2,000 ms response-time limit for synchronous calls. Applications shall use bounded timeouts, retries with backoff where safe, circuit breaking, and a recoverable pending state for unavailable dependencies. | Legal sign-off required |
| NFR-SEC-001 | RBI Digital Lending Directions — Disbursal and repayment | ## Disbursal and repayment
Loan disbursal and repayment shall flow directly between the borrower and the regulated entity's bank account, subject to applicable permitted arrangements. The system shall retain an auditable transaction trail. | Legal sign-off required |
| NFR-SEC-002 | RBI KYC Direction: Video-based Customer Identification Process (V-CIP) — Concurrent audit before activation | ## Concurrent audit before activation
The V-CIP record shall be subjected to concurrent audit. Account activation shall not occur until the required verification and audit controls have been completed, with exceptions routed for authorized resolution. | Legal sign-off required |
| NFR-SEC-002 | RBI KYC Direction: Video-based Customer Identification Process (V-CIP) — PAN and Officially Valid Document | ## PAN and Officially Valid Document
PAN shall be verified through an authorized issuer or verification service such as NSDL or UTIITSL. An Officially Valid Document (OVD) or permitted equivalent shall be verified and associated with the customer record before account activation. | Legal sign-off required |
| NFR-SEC-002 | RBI KYC Direction: Video-based Customer Identification Process (V-CIP) — Video and audit retention | ## Video and audit retention
V-CIP video and associated audit logs shall be encrypted and retained for at least five years, or longer where another applicable statutory obligation requires it. Access shall be restricted, logged, and available for authorized audit. | Legal sign-off required |
| FR-REG-003 | RBI Digital Lending Directions — Explicit borrower consent | ## Explicit borrower consent
A borrower shall receive clear information and provide explicit, purpose-specific consent before personal data is collected or shared for a digital lending journey. Consent and its scope shall be recorded and revocable where applicable. | Legal sign-off required |
| FR-REG-003 | Digital Personal Data Protection Act, 2023: Financial Services Control Notes — Purpose-limited consent | ## Purpose-limited consent
Consent shall be free, specific, informed, unconditional, and unambiguous, expressed through clear affirmative action. Personal data shall be processed for the specified purpose and limited to what is necessary for that purpose. | Legal sign-off required |
| FR-REG-003 | Bank Information Security and Privacy Policy — Privacy controls | ## Privacy controls
Systems shall minimize personal data collection, enforce purpose-based access, support retention schedules, and record legal or regulatory exceptions to deletion. | Legal sign-off required |
| FR-REG-004 | Digital Personal Data Protection Act, 2023: Financial Services Control Notes — Erasure and statutory retention | ## Erasure and statutory retention
When consent is withdrawn or the purpose is no longer served, personal data shall be erased unless retention is required to comply with law. Financial institutions shall document the applicable statutory retention basis and restrict retained data to that basis. | Legal sign-off required |
| FR-REG-004 | Digital Personal Data Protection Act, 2023: Financial Services Control Notes — Itemized notice | ## Itemized notice
Before or at the time of consent, the data fiduciary shall provide a notice describing the personal data and the purpose for which it is processed, together with a clear way to exercise applicable rights and contact the organization. | Legal sign-off required |
| FR-REG-004 | RBI Digital Lending Directions — Data storage and access | ## Data storage and access
Personal data shall be collected only as required for the stated lending purpose. Storage, access, and processing shall follow applicable regulatory and bank data-localization requirements, with controlled access and auditable deletion or retention handling. | Legal sign-off required |
| NFR-SEC-003 | Digital Personal Data Protection Act, 2023: Financial Services Control Notes — Accountability | ## Accountability
The organization shall maintain evidence of notices, consent, processing purposes, access, security controls, retention decisions, and rights requests. | Legal sign-off required |
| NFR-SEC-003 | RBI Digital Lending Directions — Disbursal and repayment | ## Disbursal and repayment
Loan disbursal and repayment shall flow directly between the borrower and the regulated entity's bank account, subject to applicable permitted arrangements. The system shall retain an auditable transaction trail. | Legal sign-off required |
| NFR-SEC-003 | RBI KYC Direction: Video-based Customer Identification Process (V-CIP) — V-CIP process controls | ## V-CIP process controls
The regulated entity shall conduct V-CIP using a secure, live, informed-consent interaction with a trained official. The official shall confirm the customer's identity and record the process in an auditable manner. | Legal sign-off required |
| NFR-SEC-004 | Bank Information Security and Privacy Policy — Encryption | ## Encryption
All customer and authentication data shall use TLS 1.3 or stronger in transit and AES-256 encryption at rest using centrally managed keys. Secrets shall not be embedded in application source. | None identified |
| NFR-SEC-004 | Legacy Core Banking Integration Interface — Interface and protocol | ## Interface and protocol
The legacy Core Banking System (CBS) exposes an ISO-8583 transaction interface and a REST wrapper for customer and account operations. Integrations shall validate schemas, map error codes, and preserve the CBS transaction reference. | None identified |
| NFR-SEC-004 | Legacy Core Banking Integration Interface — Latency and availability | ## Latency and availability
The CBS API dependency has a 2,000 ms response-time limit for synchronous calls. Applications shall use bounded timeouts, retries with backoff where safe, circuit breaking, and a recoverable pending state for unavailable dependencies. | None identified |
| NFR-SEC-005 | Bank Information Security and Privacy Policy — Authentication and authorization | ## Authentication and authorization
MFA or step-up authentication is mandatory for account activation and transactions above INR 50,000. Access shall use least-privilege role-based access control (RBAC), with privileged access reviewed and periodically recertified. | Legal sign-off required |
| NFR-SEC-005 | RBI KYC Direction: Video-based Customer Identification Process (V-CIP) — PAN and Officially Valid Document | ## PAN and Officially Valid Document
PAN shall be verified through an authorized issuer or verification service such as NSDL or UTIITSL. An Officially Valid Document (OVD) or permitted equivalent shall be verified and associated with the customer record before account activation. | Legal sign-off required |
| NFR-SEC-005 | RBI KYC Direction: Video-based Customer Identification Process (V-CIP) — Concurrent audit before activation | ## Concurrent audit before activation
The V-CIP record shall be subjected to concurrent audit. Account activation shall not occur until the required verification and audit controls have been completed, with exceptions routed for authorized resolution. | Legal sign-off required |
| NFR-SEC-006 | Bank Information Security and Privacy Policy — Session management | ## Session management
Interactive sessions shall expire after 15 minutes of inactivity. Sensitive operations shall re-authenticate users and invalidate stale sessions. | None identified |
| NFR-SEC-006 | RBI Digital Lending Directions — Disbursal and repayment | ## Disbursal and repayment
Loan disbursal and repayment shall flow directly between the borrower and the regulated entity's bank account, subject to applicable permitted arrangements. The system shall retain an auditable transaction trail. | None identified |
| NFR-SEC-006 | Legacy Core Banking Integration Interface — Interface and protocol | ## Interface and protocol
The legacy Core Banking System (CBS) exposes an ISO-8583 transaction interface and a REST wrapper for customer and account operations. Integrations shall validate schemas, map error codes, and preserve the CBS transaction reference. | None identified |
| NFR-SEC-007 | Bank Information Security and Privacy Policy — Audit logging and monitoring | ## Audit logging and monitoring
Security-relevant events, consent changes, identity checks, approvals, and administrative actions shall be sent to immutable SIEM-backed audit storage. Logs shall be time-synchronized, access-controlled, and monitored for suspicious activity. | Legal sign-off required |
| NFR-SEC-007 | Digital Personal Data Protection Act, 2023: Financial Services Control Notes — Accountability | ## Accountability
The organization shall maintain evidence of notices, consent, processing purposes, access, security controls, retention decisions, and rights requests. | Legal sign-off required |
| NFR-SEC-007 | RBI KYC Direction: Video-based Customer Identification Process (V-CIP) — V-CIP process controls | ## V-CIP process controls
The regulated entity shall conduct V-CIP using a secure, live, informed-consent interaction with a trained official. The official shall confirm the customer's identity and record the process in an auditable manner. | Legal sign-off required |
| FR-KYC-001 | Legacy Core Banking Integration Interface — Latency and availability | ## Latency and availability
The CBS API dependency has a 2,000 ms response-time limit for synchronous calls. Applications shall use bounded timeouts, retries with backoff where safe, circuit breaking, and a recoverable pending state for unavailable dependencies. | None identified |
| FR-KYC-001 | Legacy Core Banking Integration Interface — Interface and protocol | ## Interface and protocol
The legacy Core Banking System (CBS) exposes an ISO-8583 transaction interface and a REST wrapper for customer and account operations. Integrations shall validate schemas, map error codes, and preserve the CBS transaction reference. | None identified |
| FR-KYC-001 | Digital Personal Data Protection Act, 2023: Financial Services Control Notes — Itemized notice | ## Itemized notice
Before or at the time of consent, the data fiduciary shall provide a notice describing the personal data and the purpose for which it is processed, together with a clear way to exercise applicable rights and contact the organization. | None identified |
| FR-KYC-002 | Legacy Core Banking Integration Interface — Latency and availability | ## Latency and availability
The CBS API dependency has a 2,000 ms response-time limit for synchronous calls. Applications shall use bounded timeouts, retries with backoff where safe, circuit breaking, and a recoverable pending state for unavailable dependencies. | None identified |
| FR-KYC-002 | RBI Digital Lending Directions — Disbursal and repayment | ## Disbursal and repayment
Loan disbursal and repayment shall flow directly between the borrower and the regulated entity's bank account, subject to applicable permitted arrangements. The system shall retain an auditable transaction trail. | None identified |
| FR-KYC-002 | Legacy Core Banking Integration Interface — Interface and protocol | ## Interface and protocol
The legacy Core Banking System (CBS) exposes an ISO-8583 transaction interface and a REST wrapper for customer and account operations. Integrations shall validate schemas, map error codes, and preserve the CBS transaction reference. | None identified |
| FR-KYC-003 | Legacy Core Banking Integration Interface — End-of-day reconciliation | ## End-of-day reconciliation
Batch end-of-day reconciliation runs between 00:00 and 01:30 IST. Onboarding or account updates during this window shall respect the documented availability and reconciliation rules and must not corrupt pending settlement or account state. | None identified |
| FR-KYC-003 | Digital Personal Data Protection Act, 2023: Financial Services Control Notes — Accountability | ## Accountability
The organization shall maintain evidence of notices, consent, processing purposes, access, security controls, retention decisions, and rights requests. | None identified |
| FR-KYC-003 | Legacy Core Banking Integration Interface — Operational monitoring | ## Operational monitoring
Requests, latency, failures, retries, reconciliation exceptions, and CBS correlation identifiers shall be monitored and retained for operational investigation. | None identified |
| NFR-SEC-008 | Legacy Core Banking Integration Interface — Interface and protocol | ## Interface and protocol
The legacy Core Banking System (CBS) exposes an ISO-8583 transaction interface and a REST wrapper for customer and account operations. Integrations shall validate schemas, map error codes, and preserve the CBS transaction reference. | None identified |
| NFR-SEC-008 | RBI Digital Lending Directions — Disbursal and repayment | ## Disbursal and repayment
Loan disbursal and repayment shall flow directly between the borrower and the regulated entity's bank account, subject to applicable permitted arrangements. The system shall retain an auditable transaction trail. | None identified |
| NFR-SEC-008 | RBI KYC Direction: Video-based Customer Identification Process (V-CIP) — V-CIP process controls | ## V-CIP process controls
The regulated entity shall conduct V-CIP using a secure, live, informed-consent interaction with a trained official. The official shall confirm the customer's identity and record the process in an auditable manner. | None identified |
| FR-KYC-004 | RBI Digital Lending Directions — Disbursal and repayment | ## Disbursal and repayment
Loan disbursal and repayment shall flow directly between the borrower and the regulated entity's bank account, subject to applicable permitted arrangements. The system shall retain an auditable transaction trail. | None identified |
| FR-KYC-004 | Legacy Core Banking Integration Interface — Latency and availability | ## Latency and availability
The CBS API dependency has a 2,000 ms response-time limit for synchronous calls. Applications shall use bounded timeouts, retries with backoff where safe, circuit breaking, and a recoverable pending state for unavailable dependencies. | None identified |
| FR-KYC-004 | Legacy Core Banking Integration Interface — End-of-day reconciliation | ## End-of-day reconciliation
Batch end-of-day reconciliation runs between 00:00 and 01:30 IST. Onboarding or account updates during this window shall respect the documented availability and reconciliation rules and must not corrupt pending settlement or account state. | None identified |
| FR-KYC-005 | Legacy Core Banking Integration Interface — Latency and availability | ## Latency and availability
The CBS API dependency has a 2,000 ms response-time limit for synchronous calls. Applications shall use bounded timeouts, retries with backoff where safe, circuit breaking, and a recoverable pending state for unavailable dependencies. | None identified |
| FR-KYC-005 | Legacy Core Banking Integration Interface — End-of-day reconciliation | ## End-of-day reconciliation
Batch end-of-day reconciliation runs between 00:00 and 01:30 IST. Onboarding or account updates during this window shall respect the documented availability and reconciliation rules and must not corrupt pending settlement or account state. | None identified |
| FR-KYC-005 | RBI Digital Lending Directions — Disbursal and repayment | ## Disbursal and repayment
Loan disbursal and repayment shall flow directly between the borrower and the regulated entity's bank account, subject to applicable permitted arrangements. The system shall retain an auditable transaction trail. | None identified |
| FR-KYC-006 | Legacy Core Banking Integration Interface — Latency and availability | ## Latency and availability
The CBS API dependency has a 2,000 ms response-time limit for synchronous calls. Applications shall use bounded timeouts, retries with backoff where safe, circuit breaking, and a recoverable pending state for unavailable dependencies. | None identified |
| FR-KYC-006 | Legacy Core Banking Integration Interface — Interface and protocol | ## Interface and protocol
The legacy Core Banking System (CBS) exposes an ISO-8583 transaction interface and a REST wrapper for customer and account operations. Integrations shall validate schemas, map error codes, and preserve the CBS transaction reference. | None identified |
| FR-KYC-006 | RBI Digital Lending Directions — Disbursal and repayment | ## Disbursal and repayment
Loan disbursal and repayment shall flow directly between the borrower and the regulated entity's bank account, subject to applicable permitted arrangements. The system shall retain an auditable transaction trail. | None identified |
| NFR-SEC-009 | Bank Information Security and Privacy Policy — Encryption | ## Encryption
All customer and authentication data shall use TLS 1.3 or stronger in transit and AES-256 encryption at rest using centrally managed keys. Secrets shall not be embedded in application source. | None identified |
| NFR-SEC-009 | Legacy Core Banking Integration Interface — Interface and protocol | ## Interface and protocol
The legacy Core Banking System (CBS) exposes an ISO-8583 transaction interface and a REST wrapper for customer and account operations. Integrations shall validate schemas, map error codes, and preserve the CBS transaction reference. | None identified |
| NFR-SEC-009 | Legacy Core Banking Integration Interface — Latency and availability | ## Latency and availability
The CBS API dependency has a 2,000 ms response-time limit for synchronous calls. Applications shall use bounded timeouts, retries with backoff where safe, circuit breaking, and a recoverable pending state for unavailable dependencies. | None identified |
| FR-KYC-007 | Legacy Core Banking Integration Interface — Interface and protocol | ## Interface and protocol
The legacy Core Banking System (CBS) exposes an ISO-8583 transaction interface and a REST wrapper for customer and account operations. Integrations shall validate schemas, map error codes, and preserve the CBS transaction reference. | None identified |
| FR-KYC-007 | RBI Digital Lending Directions — Disbursal and repayment | ## Disbursal and repayment
Loan disbursal and repayment shall flow directly between the borrower and the regulated entity's bank account, subject to applicable permitted arrangements. The system shall retain an auditable transaction trail. | None identified |
| FR-KYC-007 | RBI Digital Lending Directions — Cooling-off period | ## Cooling-off period
The digital lending journey shall disclose an applicable cooling-off or look-up period and support the corresponding borrower exit and repayment workflow. | None identified |
| FR-KYC-008 | Digital Personal Data Protection Act, 2023: Financial Services Control Notes — Itemized notice | ## Itemized notice
Before or at the time of consent, the data fiduciary shall provide a notice describing the personal data and the purpose for which it is processed, together with a clear way to exercise applicable rights and contact the organization. | None identified |
| FR-KYC-008 | Digital Personal Data Protection Act, 2023: Financial Services Control Notes — Purpose-limited consent | ## Purpose-limited consent
Consent shall be free, specific, informed, unconditional, and unambiguous, expressed through clear affirmative action. Personal data shall be processed for the specified purpose and limited to what is necessary for that purpose. | None identified |
| FR-KYC-008 | RBI Digital Lending Directions — Disbursal and repayment | ## Disbursal and repayment
Loan disbursal and repayment shall flow directly between the borrower and the regulated entity's bank account, subject to applicable permitted arrangements. The system shall retain an auditable transaction trail. | None identified |