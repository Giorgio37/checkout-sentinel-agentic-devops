# 15-Minute Demonstration Runbook

## Before recording

1. Run `python -m checkout_sentinel.orchestrator prepare`.
2. Start `python -m checkout_sentinel.dashboard_server --port 8765`.
3. Open the dashboard and terminal side by side. Keep credentials and `terraform.tfvars` closed.
4. Open the report architecture page and the Terraform/OPA source in the editor.

## Timing

- 0:00-3:00: problem, autonomy model, architecture, and safety boundary.
- 3:00-11:00: end-to-end demo.
- 11:00-14:00: guardrails, lessons, and improvements.
- 14:00-15:00: closing and questions.

## Click-by-click demo

1. Dashboard: point to `Build PASS`, then explain attempt 1 failed and one-field remediation passed attempt 2.
2. Point to risk score and `canary-10-50-100` strategy.
3. Show the flow is stopped at `Human approval`.
4. Enter your name in **Approver name**, select **Approve release**, and point out `APPROVED`.
5. Select **Continue deployment**. Point to the 10% healthy row and 50% anomaly row.
6. Point to `ROLLED BACK`, OTel counts, and audit count.
7. Open `artifacts/itsm/INC-CAPSTONE-001.json`, `artifacts/audit/events.jsonl`, and `artifacts/governance/slsa-provenance.intoto.json`.
8. In the editor, show `iac/gcs.tf` and `iac/policy/gcs.rego`; explain that OPA permits the secure plan and blocks the staging-label plan.
9. State clearly that the real GCP plan was performed, but apply was intentionally held for human authorization.

