# Use-Case Descriptions & Process Workflow

## UC-ONB-01 — Complete digital onboarding with Video KYC

- **Primary actor:** Retail customer
- **Supporting actors:** V-CIP officer, Compliance reviewer, Core Banking System
- **Preconditions:** Privacy notice is presented and the customer can authenticate.
- **Trigger:** Customer starts a new digital account application.
- **Main flow:** Capture purpose-specific consent; collect minimum application data; verify PAN and OVD; perform live V-CIP with liveness and location evidence; complete concurrent audit; create the account using an idempotency key; notify the customer.
- **Alternate flows:** Network interruption resumes the application; failed checks route to authorized review; dependency timeout leaves a recoverable pending state.
- **Postconditions:** Consent, disclosures, decisions, transactions, and audit evidence are traceable.

## Process sequence

Customer → Consent & Notice → Identity / V-CIP Verification → Concurrent Audit → CBS Account Creation → Customer Notification