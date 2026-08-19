from __future__ import annotations

import json
from pathlib import Path

from checkout_sentinel.approval import verify
from checkout_sentinel.common import ARTIFACTS, read_json


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    request, decision = verify()
    state = read_json(ARTIFACTS / "pipeline_state.json")
    deployment = read_json(ARTIFACTS / "release" / "deployment_result.json")
    rollback = read_json(ARTIFACTS / "release" / "rollback.json")
    incident = read_json(ARTIFACTS / "itsm" / "INC-CAPSTONE-001.json")
    provenance = read_json(ARTIFACTS / "governance" / "slsa-provenance.intoto.json")
    iac = read_json(ARTIFACTS / "iac" / "verification-summary.json")
    gcp_apply = read_json(ARTIFACTS / "iac" / "gcp-apply-attempt.json")
    sandbox_apply = read_json(ARTIFACTS / "iac" / "sandbox-apply-summary.json")
    spans = jsonl(ARTIFACTS / "telemetry" / "spans.jsonl")
    metrics = jsonl(ARTIFACTS / "telemetry" / "metrics.jsonl")
    audit = jsonl(ARTIFACTS / "audit" / "events.jsonl")

    assert decision["decision"] == "APPROVED"
    assert state["stage"] == "ROLLED_BACK"
    assert [phase["traffic_percent"] for phase in deployment["phases"]] == [10, 50]
    assert deployment["final_status"] == "ROLLED_BACK"
    assert rollback["traffic_affected_percent"] <= 50
    assert rollback["status"] == "SUCCEEDED"
    assert incident["status"] == "RESOLVED"
    assert provenance["predicateType"] == "https://slsa.dev/provenance/v1"
    assert iac["real_authenticated_plan"]["result"] == "PASS"
    assert iac["negative_policy_fixture"]["result"] == "BLOCKED_AS_EXPECTED"
    assert iac["real_cloud_apply"]["result"] == "FAILED_BEFORE_CREATION"
    assert gcp_apply["cloud_resource_created"] is False
    assert gcp_apply["terraform_state_resources_after_attempt"] == 0
    assert sandbox_apply["approved_policy"]["result"] == "PASS"
    assert sandbox_apply["denied_policy"]["result"] == "BLOCKED_AS_EXPECTED"
    assert sandbox_apply["terraform_apply"]["executed"] is True
    assert sandbox_apply["terraform_apply"]["result"] == "SUCCESS"
    assert sandbox_apply["terraform_apply"]["approved"] is True
    assert any(span["attributes"].get("gen_ai.operation.name") == "invoke_agent" for span in spans)
    assert any(span["attributes"].get("gen_ai.operation.name") == "execute_tool" for span in spans)
    assert any(span["attributes"].get("service.name") == "checkout-api" for span in spans)
    assert any(metric.get("http.server.error_rate") == 0.20 for metric in metrics)
    required_actions = {
        "prompt_injection.blocked",
        "config.remediate",
        "approval.decide",
        "release.deploy",
        "incident.respond",
    }
    assert required_actions.issubset({event["action"] for event in audit})

    print(
        json.dumps(
            {
                "status": "PASS",
                "release": request["release"],
                "approver": decision["approver"],
                "pipeline": state["stage"],
                "spans": len(spans),
                "metrics": len(metrics),
                "audit_events": len(audit),
                "gcp_apply": iac["real_cloud_apply"]["result"],
                "gcp_resource_created": iac["real_cloud_apply"]["cloud_resource_created"],
                "sandbox_apply": iac["approved_sandbox_apply"]["result"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
