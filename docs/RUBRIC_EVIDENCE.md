# Capstone Rubric Evidence Map

This map ties each grading item to inspectable repository evidence. It intentionally separates real execution, local controlled simulation, and work that still requires an external account action.

## 1. End-to-end intelligent DevOps workflow — 20 points

- One release (`2.3.1`) moves through failing CI, generated regression test, bounded repair, risk scoring, timestamped approval, 10/50 canary, anomaly detection, rollback, incident, postmortem, audit, and provenance.
- Evidence: `artifacts/pipeline_state.json`, `artifacts/build/`, `artifacts/release/`, `artifacts/approval/`, `artifacts/itsm/`, `artifacts/governance/`.
- Automated verification: `scripts/verify_evidence.py`.

## 2. Agentic IaC, OPA violation, approval, and apply — 15 points

- Authenticated GCP plan: 1 add / 0 change / 0 destroy; cloud OPA: 5/5 pass.
- Negative cloud fixture: environment-label violation blocked with 4 pass / 1 fail.
- Human approval: `artifacts/iac/apply-approval.json` binds actor, UTC time, project, plan summary, and plan SHA-256.
- Real GCP apply: authorized and attempted; GCP returned 403 `accountDisabled` before creation; Terraform state remained empty and no cloud resource exists.
- No-cost apply proof: approved local `terraform_data` plan passed 3/3 and applied 1/0/0; `approved=false` was blocked with one expected OPA failure.
- Evidence: `artifacts/iac/verification-summary.json`, `gcp-apply-attempt.json`, `sandbox-apply-summary.json`, `tfplan-real.json`, and `artifacts/iac/sandbox/`.

## 3. Guardrails and prompt-injection defense — 15 points

- Prompt injection is treated as untrusted data and blocked without logging raw prompt contents.
- Tool allowlist denies unknown tools; CI may edit one allowlisted field; SRE rollback is capped at 50% traffic.
- Approval integrity re-hashes the current risk evidence before deployment.
- Evidence: `src/checkout_sentinel/security.py`, `approval.py`, `ci_agent.py`, `sre_agent.py`, `tests/`, and `artifacts/audit/events.jsonl`.

## 4. Service and agent telemetry — 10 points

- Checkout service and agents emit OpenTelemetry spans in one traceable workflow.
- Agent/tool spans use `gen_ai.operation.name=invoke_agent` and `execute_tool`.
- Metrics include error rate, p95 latency, traffic, tool calls, and invocations.
- Evidence: `src/checkout_sentinel/telemetry.py`, `observability.py`, `artifacts/telemetry/spans.jsonl`, and `metrics.jsonl`.

## 5. Automated remediation, blast radius, and ITSM — 10 points

- CI performs a one-field repair and re-test; SRE reacts to the 50% anomaly with an allowlisted rollback.
- Maximum affected traffic is 50%; stable `2.3.0` remains available.
- Incident `INC-CAPSTONE-001` and postmortem link operational evidence.
- Evidence: `artifacts/build/ci_result.json`, `artifacts/release/deployment_result.json`, `rollback.json`, and `artifacts/itsm/`.

## 6. Audit, governance, timestamped approvals, and SLSA — 10 points

- JSONL audit events record UTC time, actor, action, outcome, and input/output digests.
- Approval records identity, timestamp, request hash, and risk hash.
- In-toto provenance uses the SLSA provenance v1 predicate and artifact/source digests.
- Boundary: this is local Build L1-style provenance existence, not signed hosted Build L2/L3.
- Evidence: `artifacts/audit/`, `artifacts/approval/`, and `artifacts/governance/slsa-provenance.intoto.json`.

## 7. Fifteen-minute presentation — 10 points

- Twelve-slide deck follows the required 3-minute problem / 8-minute demo / 3-minute lessons / 1-minute questions allocation.
- The recording guide gives exact clicks and an English talk track.
- Evidence: `Checkout_Sentinel_Capstone_Presentation.pptx` and `docs/PRESENTATION_SCRIPT_CN.md` in the final submission package.

## 8. Four-to-six-page technical report — 10 points

- Five-page report covers architecture, autonomy decisions, guardrails, OTel, SRE behavior, IaC evidence, governance, lessons, limitations, and improvements.
- Evidence: `Agentic_DevOps_Capstone_Technical_Report.docx` in the final submission package.

## External completion boundary

- Not yet performed: remote repository publication, video recording/upload, and final Classroom submission.
- Cloud limitation: the course GCP project's disabled billing prevented resource creation. The attempt and zero-resource result are preserved instead of being represented as success.
