# User Stories and Acceptance Criteria

## FR-KYC-001
As a Product Owner, I need The system shall provide an instant loan decision and disburse funds within 60 seconds for an eligible returning customer so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall provide an instant loan decision and disburse funds within 60 seconds for an eligible returning customer.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall provide an instant loan decision and disburse funds within 60 seconds for an eligible returning customer.
```

## FR-KYC-002
As a Product Owner, I need The system shall disburse loan funds immediately before the borrower acknowledges the Key Fact Statement (KFS) so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall disburse loan funds immediately before the borrower acknowledges the Key Fact Statement (KFS).'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall disburse loan funds immediately before the borrower acknowledges the Key Fact Statement (KFS).
```

## FR-KYC-003
As a Product Owner, I need The system shall collect mobile-device contact data for fast underwriting and retain it for future cross-sell so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall collect mobile-device contact data for fast underwriting and retain it for future cross-sell.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall collect mobile-device contact data for fast underwriting and retain it for future cross-sell.
```

## FR-REG-001
As a Compliance Officer, I need The system shall present the Key Fact Statement and capture durable borrower acknowledgment before loan contract execution and disbursal so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall present the Key Fact Statement and capture durable borrower acknowledgment before loan contract execution and disbursal.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall present the Key Fact Statement and capture durable borrower acknowledgment before loan contract execution and disbursal.
```

## FR-REG-002
As a Compliance Officer, I need The system shall obtain explicit purpose-specific borrower consent before collecting or sharing personal data for underwriting so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall obtain explicit purpose-specific borrower consent before collecting or sharing personal data for underwriting.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall obtain explicit purpose-specific borrower consent before collecting or sharing personal data for underwriting.
```

## FR-REG-003
As a Compliance Officer, I need The system shall disburse directly between the borrower and the regulated entity's bank account and disclose the applicable cooling-off period so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall disburse directly between the borrower and the regulated entity's bank account and disclose the applicable cooling-off period.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall disburse directly between the borrower and the regulated entity's bank account and disclose the applicable cooling-off period.
```

## NFR-SEC-001
As a InfoSec Architect, I need The system shall use TLS 1.3 in transit, AES-256 at rest, MFA for sensitive actions, least-privilege RBAC, and immutable audit logging so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall use TLS 1.3 in transit, AES-256 at rest, MFA for sensitive actions, least-privilege RBAC, and immutable audit logging.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall use TLS 1.3 in transit, AES-256 at rest, MFA for sensitive actions, least-privilege RBAC, and immutable audit logging.
```

## FR-KYC-004
As a Software Architect, I need The system shall use idempotency keys for disbursal requests and safely handle duplicate callbacks and interrupted network connections so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall use idempotency keys for disbursal requests and safely handle duplicate callbacks and interrupted network connections.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall use idempotency keys for disbursal requests and safely handle duplicate callbacks and interrupted network connections.
```
