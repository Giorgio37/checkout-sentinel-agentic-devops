# Checkout Sentinel

Checkout Sentinel is a reproducible capstone demonstrating an end-to-end, policy-constrained agentic DevOps workflow for a checkout API. It begins with an intentionally failing release candidate, performs a bounded repair, scores deployment risk, requires human approval, runs a 10/50/100 canary, detects an injected anomaly, rolls back within a 50% blast-radius limit, creates an ITSM incident, and records OpenTelemetry and governance evidence.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e . pytest
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m checkout_sentinel.orchestrator prepare
.\.venv\Scripts\python.exe -m checkout_sentinel.dashboard_server --port 8765
```

Open `http://127.0.0.1:8765`, enter the human approver name, select **Approve release**, and then select **Continue deployment**. The dashboard updates to show the anomaly and rollback. CLI equivalents are:

```powershell
.\.venv\Scripts\python.exe -m checkout_sentinel.orchestrator approve --actor "Your Name"
.\.venv\Scripts\python.exe -m checkout_sentinel.orchestrator deploy
```

## Evidence map

| Requirement | Implementation | Evidence |
|---|---|---|
| CI agent review, generated test, remediation | `ci_agent.py` | `artifacts/build/ci_result.json`, `generated_test.json` |
| Risk score, canary, cost estimate | `risk_agent.py` | `artifacts/release/risk_assessment.json` |
| Human approval | `approval.py` | `artifacts/approval/request.json`, `decision.json` |
| Service and agent OTel | `telemetry.py`, `observability.py` | `artifacts/telemetry/spans.jsonl`, `metrics.jsonl` |
| Anomaly and SRE response | `deployment.py`, `sre_agent.py` | `deployment_result.json`, `rollback.json` |
| ITSM and postmortem | `sre_agent.py` | `artifacts/itsm/INC-CAPSTONE-001*` |
| Structured audit | `common.py` | `artifacts/audit/events.jsonl` |
| SLSA provenance | `provenance.py` | `artifacts/governance/slsa-provenance.intoto.json` |
| Terraform and OPA | `iac/` | authenticated GCP plan, cloud apply attempt, and approved sandbox apply evidence |
| Prompt-injection defense | `security.py` | blocked audit event; raw content is not logged |

## Safety boundaries

- The CI agent may change one field in a generated runtime copy only.
- The release never starts without a timestamped approval whose request hash still matches.
- The SRE agent may only roll back an allowlisted canary at or below 50% traffic.
- Untrusted ticket text cannot alter tool policy and is not copied into telemetry.
- Credentials, state, live `terraform.tfvars`, and binary plans are excluded from version control.
- Local provenance demonstrates SLSA Build L1-style provenance existence; it is not signed hosted provenance and does not claim Build L2 or L3.

## Real cloud boundary

After explicit human approval, Terraform attempted to apply the policy-compliant plan to the course GCP project. GCP returned `403 accountDisabled` because the project's billing account was unavailable, and Terraform state remained empty, so no cloud resource was created. The repository also contains a no-cost local `terraform_data` sandbox: its approved plan passed 3/3 OPA tests and applied successfully, while the unapproved plan was blocked with one expected policy failure. These are reported as separate outcomes and the sandbox is not presented as a cloud deployment.

See `docs/ARCHITECTURE.md`, `docs/SECURITY.md`, `docs/DEMO_RUNBOOK.md`, and `docs/AI_COLLABORATION.md` for the design and presentation procedure.
