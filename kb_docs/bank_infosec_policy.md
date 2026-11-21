# Bank Information Security and Privacy Policy
Jurisdiction: India | Version: 4.2 (2025) | Effective date: 2025-04-01

## Encryption
All customer and authentication data shall use TLS 1.3 or stronger in transit and AES-256 encryption at rest using centrally managed keys. Secrets shall not be embedded in application source.

## Authentication and authorization
MFA or step-up authentication is mandatory for account activation and transactions above INR 50,000. Access shall use least-privilege role-based access control (RBAC), with privileged access reviewed and periodically recertified.

## Session management
Interactive sessions shall expire after 15 minutes of inactivity. Sensitive operations shall re-authenticate users and invalidate stale sessions.

## Audit logging and monitoring
Security-relevant events, consent changes, identity checks, approvals, and administrative actions shall be sent to immutable SIEM-backed audit storage. Logs shall be time-synchronized, access-controlled, and monitored for suspicious activity.

## Secure delivery and operations
Threat modeling, code review, SAST, dependency scanning, DAST, penetration testing, vulnerability remediation, backup validation, and incident-response readiness are required before production release according to risk.

## Privacy controls
Systems shall minimize personal data collection, enforce purpose-based access, support retention schedules, and record legal or regulatory exceptions to deletion.
