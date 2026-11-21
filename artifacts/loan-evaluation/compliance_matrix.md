# Compliance-Control Matrix

| Req ID | Source / Section | Evidence | Gaps / Sign-off |
|---|---|---|---|
| FR-KYC-001 | Legacy Core Banking Integration Interface — Interface and protocol | ## Interface and protocol
The legacy Core Banking System (CBS) exposes an ISO-8583 transaction interface and a REST wrapper for customer and account operations. Integrations shall validate schemas, map error codes, and preserve the CBS transaction reference. | None identified |
| FR-KYC-001 | RBI Digital Lending Directions — Disbursal and repayment | ## Disbursal and repayment
Loan disbursal and repayment shall flow directly between the borrower and the regulated entity's bank account, subject to applicable permitted arrangements. The system shall retain an auditable transaction trail. | None identified |
| FR-KYC-001 | RBI KYC Direction: Video-based Customer Identification Process (V-CIP) — V-CIP process controls | ## V-CIP process controls
The regulated entity shall conduct V-CIP using a secure, live, informed-consent interaction with a trained official. The official shall confirm the customer's identity and record the process in an auditable manner. | None identified |
| FR-KYC-002 | RBI Digital Lending Directions — Key Fact Statement | ## Key Fact Statement
A Key Fact Statement (KFS) shall be presented and acknowledged before execution of the loan contract. Charges, repayment terms, and material loan conditions shall be disclosed in a clear, durable form. | None identified |
| FR-KYC-002 | RBI Digital Lending Directions — Disbursal and repayment | ## Disbursal and repayment
Loan disbursal and repayment shall flow directly between the borrower and the regulated entity's bank account, subject to applicable permitted arrangements. The system shall retain an auditable transaction trail. | None identified |
| FR-KYC-002 | RBI KYC Direction: Video-based Customer Identification Process (V-CIP) — V-CIP process controls | ## V-CIP process controls
The regulated entity shall conduct V-CIP using a secure, live, informed-consent interaction with a trained official. The official shall confirm the customer's identity and record the process in an auditable manner. | None identified |
| FR-KYC-003 | Digital Personal Data Protection Act, 2023: Financial Services Control Notes — Itemized notice | ## Itemized notice
Before or at the time of consent, the data fiduciary shall provide a notice describing the personal data and the purpose for which it is processed, together with a clear way to exercise applicable rights and contact the organization. | None identified |
| FR-KYC-003 | Legacy Core Banking Integration Interface — Latency and availability | ## Latency and availability
The CBS API dependency has a 2,000 ms response-time limit for synchronous calls. Applications shall use bounded timeouts, retries with backoff where safe, circuit breaking, and a recoverable pending state for unavailable dependencies. | None identified |
| FR-KYC-003 | Legacy Core Banking Integration Interface — Interface and protocol | ## Interface and protocol
The legacy Core Banking System (CBS) exposes an ISO-8583 transaction interface and a REST wrapper for customer and account operations. Integrations shall validate schemas, map error codes, and preserve the CBS transaction reference. | None identified |
| FR-REG-001 | RBI Digital Lending Directions — Key Fact Statement | ## Key Fact Statement
A Key Fact Statement (KFS) shall be presented and acknowledged before execution of the loan contract. Charges, repayment terms, and material loan conditions shall be disclosed in a clear, durable form. | Legal sign-off required |
| FR-REG-001 | RBI Digital Lending Directions — Disbursal and repayment | ## Disbursal and repayment
Loan disbursal and repayment shall flow directly between the borrower and the regulated entity's bank account, subject to applicable permitted arrangements. The system shall retain an auditable transaction trail. | Legal sign-off required |
| FR-REG-001 | Legacy Core Banking Integration Interface — Interface and protocol | ## Interface and protocol
The legacy Core Banking System (CBS) exposes an ISO-8583 transaction interface and a REST wrapper for customer and account operations. Integrations shall validate schemas, map error codes, and preserve the CBS transaction reference. | Legal sign-off required |
| FR-REG-002 | RBI Digital Lending Directions — Explicit borrower consent | ## Explicit borrower consent
A borrower shall receive clear information and provide explicit, purpose-specific consent before personal data is collected or shared for a digital lending journey. Consent and its scope shall be recorded and revocable where applicable. | Legal sign-off required |
| FR-REG-002 | Digital Personal Data Protection Act, 2023: Financial Services Control Notes — Itemized notice | ## Itemized notice
Before or at the time of consent, the data fiduciary shall provide a notice describing the personal data and the purpose for which it is processed, together with a clear way to exercise applicable rights and contact the organization. | Legal sign-off required |
| FR-REG-002 | Digital Personal Data Protection Act, 2023: Financial Services Control Notes — Purpose-limited consent | ## Purpose-limited consent
Consent shall be free, specific, informed, unconditional, and unambiguous, expressed through clear affirmative action. Personal data shall be processed for the specified purpose and limited to what is necessary for that purpose. | Legal sign-off required |
| FR-REG-003 | RBI Digital Lending Directions — Disbursal and repayment | ## Disbursal and repayment
Loan disbursal and repayment shall flow directly between the borrower and the regulated entity's bank account, subject to applicable permitted arrangements. The system shall retain an auditable transaction trail. | None identified |
| FR-REG-003 | RBI Digital Lending Directions — Cooling-off period | ## Cooling-off period
The digital lending journey shall disclose an applicable cooling-off or look-up period and support the corresponding borrower exit and repayment workflow. | None identified |
| FR-REG-003 | RBI KYC Direction: Video-based Customer Identification Process (V-CIP) — V-CIP process controls | ## V-CIP process controls
The regulated entity shall conduct V-CIP using a secure, live, informed-consent interaction with a trained official. The official shall confirm the customer's identity and record the process in an auditable manner. | None identified |
| NFR-SEC-001 | Bank Information Security and Privacy Policy — Encryption | ## Encryption
All customer and authentication data shall use TLS 1.3 or stronger in transit and AES-256 encryption at rest using centrally managed keys. Secrets shall not be embedded in application source. | None identified |
| NFR-SEC-001 | Bank Information Security and Privacy Policy — Audit logging and monitoring | ## Audit logging and monitoring
Security-relevant events, consent changes, identity checks, approvals, and administrative actions shall be sent to immutable SIEM-backed audit storage. Logs shall be time-synchronized, access-controlled, and monitored for suspicious activity. | None identified |
| NFR-SEC-001 | RBI KYC Direction: Video-based Customer Identification Process (V-CIP) — Video and audit retention | ## Video and audit retention
V-CIP video and associated audit logs shall be encrypted and retained for at least five years, or longer where another applicable statutory obligation requires it. Access shall be restricted, logged, and available for authorized audit. | None identified |
| FR-KYC-004 | Legacy Core Banking Integration Interface — Idempotency | ## Idempotency
Account creation and financial operations shall carry a unique idempotency key. Retried requests with the same key shall not create duplicate customers, accounts, or financial transactions. | Legal sign-off required |
| FR-KYC-004 | RBI Digital Lending Directions — Disbursal and repayment | ## Disbursal and repayment
Loan disbursal and repayment shall flow directly between the borrower and the regulated entity's bank account, subject to applicable permitted arrangements. The system shall retain an auditable transaction trail. | Legal sign-off required |
| FR-KYC-004 | Legacy Core Banking Integration Interface — Latency and availability | ## Latency and availability
The CBS API dependency has a 2,000 ms response-time limit for synchronous calls. Applications shall use bounded timeouts, retries with backoff where safe, circuit breaking, and a recoverable pending state for unavailable dependencies. | Legal sign-off required |