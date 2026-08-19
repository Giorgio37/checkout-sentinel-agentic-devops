from __future__ import annotations

from typing import Any

from .common import ARTIFACTS, append_jsonl, record_audit, utc_now, write_json
from .security import authorize_tool
from .telemetry import span


def respond_to_anomaly(anomaly: dict[str, Any]) -> dict[str, Any]:
    traffic = int(anomaly["observed"]["traffic_percent"])
    reasoning_record = {
        "observation": anomaly["reasons"],
        "policy": "Rollback only an allowlisted canary at or below 50% traffic.",
        "selected_action": "rollback_canary",
        "excluded_action": "modify_production_infrastructure",
    }
    with span(
        "invoke_agent sre-response-agent",
        {
            "gen_ai.operation.name": "invoke_agent",
            "gen_ai.agent.name": "sre-response-agent",
            "incident.traffic_percent": traffic,
        },
    ):
        decision = authorize_tool("rollback_canary", {"traffic_percent": traffic})
        if not decision.allowed:
            result = {"status": "ESCALATED", "reason": decision.reason, "reasoning_record": reasoning_record}
            record_audit("sre-response-agent", "incident.respond", "DENY", anomaly, result)
            return result

        with span(
            "execute_tool rollback_canary",
            {
                "gen_ai.operation.name": "execute_tool",
                "gen_ai.tool.name": "rollback_canary",
                "blast_radius.traffic_percent": traffic,
            },
        ):
            rollback = {
                "action": "rollback_canary",
                "from_version": "2.3.1",
                "to_version": "2.3.0",
                "traffic_affected_percent": traffic,
                "status": "SUCCEEDED",
                "executed_at": utc_now(),
            }
            write_json(ARTIFACTS / "release" / "rollback.json", rollback)

        incident = {
            "schema": "checkout-sentinel.itsm/v1",
            "incident_id": "INC-CAPSTONE-001",
            "severity": "SEV-2",
            "service": "checkout-api",
            "summary": "Canary error rate exceeded 5% at 50% traffic",
            "status": "RESOLVED",
            "opened_at": utc_now(),
            "resolution": "Policy-constrained rollback to 2.3.0",
            "evidence": ["telemetry/metrics.jsonl", "release/rollback.json", "audit/events.jsonl"],
        }
        write_json(ARTIFACTS / "itsm" / "INC-CAPSTONE-001.json", incident)
        postmortem = (
            "# INC-CAPSTONE-001 Postmortem\n\n"
            "## Impact\n\nThe 2.3.1 canary reached 50% simulated traffic before rollback. Stable 2.3.0 remained available.\n\n"
            "## Detection\n\nError rate reached 20%, above the 5% SLO guardrail; p95 latency reached 480 ms.\n\n"
            "## Response\n\nThe SRE agent selected the allowlisted rollback tool. The runtime enforced a 50% blast-radius ceiling and recorded the action.\n\n"
            "## Follow-up\n\nAdd production traffic replay and signed hosted provenance before a real deployment.\n"
        )
        postmortem_path = ARTIFACTS / "itsm" / "INC-CAPSTONE-001-postmortem.md"
        postmortem_path.parent.mkdir(parents=True, exist_ok=True)
        postmortem_path.write_text(postmortem, encoding="utf-8")
        append_jsonl(
            ARTIFACTS / "telemetry" / "metrics.jsonl",
            {
                "schema": "opentelemetry.metric/v1",
                "timestamp": utc_now(),
                "gen_ai.agent.name": "sre-response-agent",
                "gen_ai.invoke_agent.tool_calls": 2,
                "gen_ai.invoke_agent.inference_calls": 1,
            },
        )
        result = {"status": "ROLLED_BACK", "rollback": rollback, "incident": incident, "reasoning_record": reasoning_record}
        record_audit("sre-response-agent", "incident.respond", "ALLOW", anomaly, result, {"blast_radius_limit": 50})
        return result

