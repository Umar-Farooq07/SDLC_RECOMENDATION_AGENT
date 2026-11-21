# Use-Case Descriptions & Process Workflow

## UC-LEND-01 — Originate and disburse a digital personal loan

- **Primary actor:** Borrower
- **Supporting actors:** Compliance reviewer, lender, Core Banking System
- **Preconditions:** Privacy notice is presented and the customer can authenticate.
- **Trigger:** Customer starts a digital loan application.
- **Main flow:** Capture purpose-specific consent; collect minimum application data; present the KFS and record borrower acknowledgment before contract execution; originate and disburse directly through permitted bank accounts; disclose the cooling-off period.
- **Alternate flows:** Network interruption resumes the application; failed checks route to authorized review; dependency timeout leaves a recoverable pending state.
- **Postconditions:** Consent, disclosures, decisions, transactions, and audit evidence are traceable.

## Process sequence

Borrower → Notice & Consent → Underwriting → KFS Acknowledgment → Contract → Direct Disbursal → Cooling-off / Servicing