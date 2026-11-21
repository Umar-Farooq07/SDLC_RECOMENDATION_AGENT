# User Stories and Acceptance Criteria

## FR-REG-001
As a Compliance Officer, I need The system shall complete live V-CIP with customer consent, liveness detection, live location and timestamp capture, and trained-official verification so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall complete live V-CIP with customer consent, liveness detection, live location and timestamp capture, and trained-official verification.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall complete live V-CIP with customer consent, liveness detection, live location and timestamp capture, and trained-official verification.
```

## FR-REG-002
As a Compliance Officer, I need The system shall verify PAN using an authorized service and verify an OVD or permitted equivalent before account activation so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall verify PAN using an authorized service and verify an OVD or permitted equivalent before account activation.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall verify PAN using an authorized service and verify an OVD or permitted equivalent before account activation.
```

## NFR-SEC-001
As a Compliance Officer, I need The system shall retain encrypted V-CIP video and associated audit evidence for at least five years, subject to a longer statutory retention obligation so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall retain encrypted V-CIP video and associated audit evidence for at least five years, subject to a longer statutory retention obligation.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall retain encrypted V-CIP video and associated audit evidence for at least five years, subject to a longer statutory retention obligation.
```

## NFR-SEC-002
As a Compliance Officer, I need The system shall complete concurrent audit of the V-CIP record before account activation; exceptions require authorized review so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall complete concurrent audit of the V-CIP record before account activation; exceptions require authorized review.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall complete concurrent audit of the V-CIP record before account activation; exceptions require authorized review.
```

## FR-REG-003
As a Compliance Officer, I need The system shall present an itemized privacy notice and record explicit purpose-specific consent before collecting personal data so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall present an itemized privacy notice and record explicit purpose-specific consent before collecting personal data.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall present an itemized privacy notice and record explicit purpose-specific consent before collecting personal data.
```

## FR-REG-004
As a Compliance Officer, I need The system shall limit collection to the stated purpose and erase data when the purpose ends unless statutory banking retention applies so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall limit collection to the stated purpose and erase data when the purpose ends unless statutory banking retention applies.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall limit collection to the stated purpose and erase data when the purpose ends unless statutory banking retention applies.
```

## NFR-SEC-003
As a Compliance Officer, I need The system shall retain evidence of consent, verification, audit decisions, retention basis, and customer rights requests so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall retain evidence of consent, verification, audit decisions, retention basis, and customer rights requests.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall retain evidence of consent, verification, audit decisions, retention basis, and customer rights requests.
```

## NFR-SEC-004
As a InfoSec Architect, I need The system shall use TLS 1.3 in transit and AES-256 encryption at rest for customer, identity, and video data so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall use TLS 1.3 in transit and AES-256 encryption at rest for customer, identity, and video data.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall use TLS 1.3 in transit and AES-256 encryption at rest for customer, identity, and video data.
```

## NFR-SEC-005
As a InfoSec Architect, I need The system shall require MFA or step-up authentication for account activation and transactions above INR 50,000, with least-privilege RBAC so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall require MFA or step-up authentication for account activation and transactions above INR 50,000, with least-privilege RBAC.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall require MFA or step-up authentication for account activation and transactions above INR 50,000, with least-privilege RBAC.
```

## NFR-SEC-006
As a InfoSec Architect, I need The system shall expire interactive sessions after 15 minutes of inactivity and re-authenticate sensitive actions so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall expire interactive sessions after 15 minutes of inactivity and re-authenticate sensitive actions.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall expire interactive sessions after 15 minutes of inactivity and re-authenticate sensitive actions.
```

## NFR-SEC-007
As a InfoSec Architect, I need The system shall send immutable security, consent, identity, and approval events to SIEM-backed audit storage so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall send immutable security, consent, identity, and approval events to SIEM-backed audit storage.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall send immutable security, consent, identity, and approval events to SIEM-backed audit storage.
```

## FR-KYC-001
As a Software Architect, I need The system shall integrate with the legacy Core Banking System REST wrapper, whose API dependency is limited to 2,000 ms response time so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall integrate with the legacy Core Banking System REST wrapper, whose API dependency is limited to 2,000 ms response time.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall integrate with the legacy Core Banking System REST wrapper, whose API dependency is limited to 2,000 ms response time.
```

## FR-KYC-002
As a Software Architect, I need The system shall use an idempotency key for account creation and recover safely from retries and duplicate delivery so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall use an idempotency key for account creation and recover safely from retries and duplicate delivery.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall use an idempotency key for account creation and recover safely from retries and duplicate delivery.
```

## FR-KYC-003
As a Operations Lead, I need The system shall schedule end-of-day reconciliation from 00:00 to 01:30 IST and monitor pending onboarding exceptions so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall schedule end-of-day reconciliation from 00:00 to 01:30 IST and monitor pending onboarding exceptions.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall schedule end-of-day reconciliation from 00:00 to 01:30 IST and monitor pending onboarding exceptions.
```

## NFR-SEC-008
As a Product Owner, I need The system shall activate an account instantly after the customer submits the onboarding form, without waiting for a concurrent audit so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall activate an account instantly after the customer submits the onboarding form, without waiting for a concurrent audit.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall activate an account instantly after the customer submits the onboarding form, without waiting for a concurrent audit.
```

## FR-KYC-004
As a Product Owner, I need The system shall retain behavioral analytics and onboarding video indefinitely so marketing can improve conversion so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall retain behavioral analytics and onboarding video indefinitely so marketing can improve conversion.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall retain behavioral analytics and onboarding video indefinitely so marketing can improve conversion.
```

## FR-KYC-005
As a Product Owner, I need The system shall complete onboarding and all connected API calls within 500 ms end-to-end so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall complete onboarding and all connected API calls within 500 ms end-to-end.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall complete onboarding and all connected API calls within 500 ms end-to-end.
```

## FR-KYC-006
As a Product Owner, I need The system shall run a fast liveness check and raise an alert for high-value applications so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall run a fast liveness check and raise an alert for high-value applications.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall run a fast liveness check and raise an alert for high-value applications.
```

## NFR-SEC-009
As a Product Owner, I need The system shall use standard encryption for all customer data so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall use standard encryption for all customer data.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall use standard encryption for all customer data.
```

## FR-KYC-007
As a Product Owner, I need The system shall support retry after network interruption and let customers resume an incomplete application so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'The system shall support retry after network interruption and let customers resume an incomplete application.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: The system shall support retry after network interruption and let customers resume an incomplete application.
```

## FR-KYC-008
As a Product Owner, I need The system shall priority is a low-friction flow; exceptions should be reviewed by an operations user so that the onboarding control is satisfied.

```gherkin
Scenario: Verify requirement outcome
  Given the stakeholder evidence 'Priority is a low-friction flow; exceptions should be reviewed by an operations user.'
  When the onboarding requirement is evaluated
  Then Given the onboarding workflow, when the requirement is exercised, then the outcome is verified: Priority is a low-friction flow; exceptions should be reviewed by an operations user.
```
