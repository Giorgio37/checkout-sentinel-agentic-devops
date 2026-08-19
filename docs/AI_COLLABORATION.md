# AI Collaboration Record

## Human responsibilities

- Defined the assignment objective and required complete rubric coverage.
- Retains approval over release, real cloud resource creation, remote repository publication, and final submission.
- Will perform the recorded approval action in the dashboard.

## Codex responsibilities

- Inspected the literal Classroom requirements and separated the Week 7 lab from the full Capstone.
- Designed and implemented the service, agents, controls, telemetry, IaC/OPA integration, dashboard, tests, report, presentation, and recording runbook.
- Executed reproducible verification and labeled simulated evidence, real cloud-plan evidence, and actions that were not performed.

## Decision trail

The design favors a deterministic local agent runtime for a reliable classroom demonstration. This avoids putting credentials or sensitive prompts into an external model and makes each action independently testable. A production version would add a hosted, signed build provenance service, identity-based short-lived cloud credentials, real traffic telemetry, and an ITSM connector.

