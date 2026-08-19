# Security and Governance

## Guardrails

1. Tool allowlist and blast-radius enforcement: unknown tools are denied; canary rollback is capped at 50% traffic; CI writes one runtime field only.
2. Integrity-bound human approval: approval includes actor, UTC timestamp, request hash, risk hash, release, and environment. Deployment recalculates the request hash before continuing.
3. Prompt-injection boundary: untrusted text is pattern-inspected as data. A malicious support ticket attempts to disable approval and reveal credentials; it is blocked and its raw content is not logged.
4. Secret boundary: no credential is supplied to an agent, dashboard, artifact, Git ignore exception, or provenance material.

## Governance records

Audit events contain timestamp, actor, action, outcome, request/response SHA-256 digests, and bounded operational details. Agent records expose concise observation/policy/action/outcome summaries, not private chain-of-thought. The in-toto statement uses the official `https://slsa.dev/provenance/v1` predicate and honestly claims only local Build L1-style provenance existence.

