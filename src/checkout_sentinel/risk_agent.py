from __future__ import annotations

from typing import Any

from .common import ARTIFACTS, record_audit, write_json
from .telemetry import span


def assess_risk(ci_result: dict[str, Any]) -> dict[str, Any]:
    inputs = {
        "files_changed": 4,
        "infrastructure_change": True,
        "database_migration": False,
        "security_signal": ci_result.get("prompt_injection") == "BLOCKED",
        "final_tests_pass": ci_result["final"]["status"] == "PASS",
    }
    score = 20 + inputs["files_changed"] * 3
    score += 20 if inputs["infrastructure_change"] else 0
    score += 30 if inputs["database_migration"] else 0
    score += 10 if inputs["security_signal"] else 0
    score -= 10 if inputs["final_tests_pass"] else 0
    score = max(0, min(100, score))
    strategy = "canary-10-50-100" if score >= 40 else "rolling"
    decision = {
        "score": score,
        "band": "MEDIUM" if score < 70 else "HIGH",
        "strategy": strategy,
        "human_approval_required": True,
        "inputs": inputs,
        "finops_estimate": {
            "currency": "USD",
            "monthly_estimate": 0.22,
            "basis": "Illustrative 10 GB storage plus low request volume; verify live cloud pricing before production.",
        },
    }
    with span(
        "invoke_agent release-risk-agent",
        {"gen_ai.operation.name": "invoke_agent", "gen_ai.agent.name": "release-risk-agent", "risk.score": score},
    ):
        write_json(ARTIFACTS / "release" / "risk_assessment.json", decision)
        record_audit("release-risk-agent", "release.assess_risk", "REVIEW", inputs, decision)
    return decision

