# Architecture

```text
Candidate change
      |
      v
CI Review Agent -- generated regression test --> bounded config repair
      |
      v
Release Risk Agent --> score + strategy + illustrative FinOps estimate
      |
      v
Human approval gate (timestamp + request/risk hashes)
      |
      v
Canary 10% --> healthy --> 50% --> injected error/latency anomaly
                                      |
                                      v
                              SRE Response Agent
                                      |
                       allowlist + <=50% blast radius
                                      |
                       rollback + ITSM + postmortem

Cross-cutting: OpenTelemetry spans/metrics, JSONL audit, SLSA provenance
IaC track: Terraform plan --> OPA/Conftest --> human approval --> optional apply
```

The agents are deterministic policy-constrained software agents so the demonstration is repeatable without transferring secrets to an external model. Their contracts, tools, write scopes, and autonomy levels are declared in `config/agents.json` and `prompts/`. Codex is the AI collaborator used to design, implement, test, document, and prepare this project; the human retains the approval and cloud-apply decisions.

