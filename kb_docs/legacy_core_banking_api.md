# Legacy Core Banking Integration Interface
Jurisdiction: India | Version: CBS Wrapper 3.8 | Effective date: 2025-02-01

## Interface and protocol
The legacy Core Banking System (CBS) exposes an ISO-8583 transaction interface and a REST wrapper for customer and account operations. Integrations shall validate schemas, map error codes, and preserve the CBS transaction reference.

## Latency and availability
The CBS API dependency has a 2,000 ms response-time limit for synchronous calls. Applications shall use bounded timeouts, retries with backoff where safe, circuit breaking, and a recoverable pending state for unavailable dependencies.

## Idempotency
Account creation and financial operations shall carry a unique idempotency key. Retried requests with the same key shall not create duplicate customers, accounts, or financial transactions.

## End-of-day reconciliation
Batch end-of-day reconciliation runs between 00:00 and 01:30 IST. Onboarding or account updates during this window shall respect the documented availability and reconciliation rules and must not corrupt pending settlement or account state.

## Operational monitoring
Requests, latency, failures, retries, reconciliation exceptions, and CBS correlation identifiers shall be monitored and retained for operational investigation.
