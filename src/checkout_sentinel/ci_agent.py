from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import ARTIFACTS, PROJECT_ROOT, read_json, record_audit, write_json
from .security import authorize_tool, inspect_untrusted_text
from .service import checkout
from .telemetry import span


EXPECTED_THRESHOLD = 50.0


def evaluate_build(config: dict[str, Any]) -> dict[str, Any]:
    threshold = float(config["free_shipping_threshold"])
    sample = checkout(20.0, threshold)
    failures = []
    if threshold != EXPECTED_THRESHOLD:
        failures.append(f"free_shipping_threshold must equal {EXPECTED_THRESHOLD:.1f}")
    if sample.shipping != 7.99:
        failures.append("$20 checkout must retain standard shipping")
    return {"status": "PASS" if not failures else "FAIL", "failures": failures, "tests": 2}


def run_ci_agent() -> dict[str, Any]:
    candidate = read_json(PROJECT_ROOT / "fixtures" / "candidate_config.json")
    untrusted = (PROJECT_ROOT / "fixtures" / "untrusted_ticket.txt").read_text(encoding="utf-8")
    runtime_config = ARTIFACTS / "build" / "candidate_config.runtime.json"
    write_json(runtime_config, candidate)

    with span(
        "invoke_agent ci-review-agent",
        {"gen_ai.operation.name": "invoke_agent", "gen_ai.agent.name": "ci-review-agent", "agent.autonomy": "on-loop"},
    ):
        injection = inspect_untrusted_text(untrusted, "fixtures/untrusted_ticket.txt")
        generated_test = {
            "id": "generated-shipping-threshold-regression",
            "arrange": {"subtotal": 20.0},
            "assert": {"shipping": 7.99, "free_shipping_threshold": EXPECTED_THRESHOLD},
            "generated_by": "ci-review-agent",
        }
        write_json(ARTIFACTS / "build" / "generated_test.json", generated_test)

        first = evaluate_build(candidate)
        record_audit("ci-review-agent", "build.test", first["status"], candidate, first, {"attempt": 1})
        if first["status"] == "PASS":
            result = {"initial": first, "remediation": "NOT_NEEDED", "final": first}
            write_json(ARTIFACTS / "build" / "ci_result.json", result)
            return result

        decision = authorize_tool("patch_checkout_config", {"fields": 1})
        if not decision.allowed:
            raise PermissionError(decision.reason)

        with span(
            "execute_tool patch_checkout_config",
            {"gen_ai.operation.name": "execute_tool", "gen_ai.tool.name": "patch_checkout_config", "change.fields": 1},
        ):
            repaired = dict(candidate)
            before = repaired["free_shipping_threshold"]
            repaired["free_shipping_threshold"] = EXPECTED_THRESHOLD
            write_json(runtime_config, repaired)
            record_audit(
                "ci-review-agent",
                "config.remediate",
                "ALLOW",
                {"field": "free_shipping_threshold", "before": before},
                {"field": "free_shipping_threshold", "after": EXPECTED_THRESHOLD},
                {"bounded_fields": 1, "rollback": "restore runtime copy"},
            )

        final = evaluate_build(repaired)
        record_audit("ci-review-agent", "build.test", final["status"], repaired, final, {"attempt": 2})
        result = {
            "initial": first,
            "remediation": "APPLIED",
            "changed_field": "free_shipping_threshold",
            "final": final,
            "prompt_injection": "BLOCKED" if not injection.allowed else "NOT_DETECTED",
        }
        write_json(ARTIFACTS / "build" / "ci_result.json", result)
        return result

