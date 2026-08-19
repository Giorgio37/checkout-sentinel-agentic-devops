from __future__ import annotations

import re
from dataclasses import dataclass

from .common import record_audit
from .telemetry import span


INJECTION_PATTERNS = (
    r"ignore\s+(all|any|the)\s+(previous|prior|system)\s+instructions?",
    r"reveal\s+(the\s+)?(secret|credential|system prompt)",
    r"disable\s+(the\s+)?(policy|guardrail|approval)",
    r"run\s+.*(powershell|cmd\.exe|curl|wget)",
)

ALLOWED_TOOLS = {
    "patch_checkout_config": {"max_fields": 1},
    "rollback_canary": {"max_traffic_percent": 50},
    "create_incident": {"max_records": 1},
}


@dataclass(frozen=True)
class SecurityDecision:
    allowed: bool
    reason: str
    matched_pattern: str | None = None


def inspect_untrusted_text(text: str, source: str) -> SecurityDecision:
    with span(
        "execute_tool inspect_untrusted_text",
        {"gen_ai.operation.name": "execute_tool", "gen_ai.tool.name": "inspect_untrusted_text", "input.source": source},
    ):
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
                decision = SecurityDecision(False, "Prompt-injection pattern blocked", pattern)
                record_audit(
                    "security-guard",
                    "prompt_injection.blocked",
                    "DENY",
                    {"source": source, "content_length": len(text)},
                    {"reason": decision.reason, "matched_pattern": pattern},
                    {"content_logged": False},
                )
                return decision
    return SecurityDecision(True, "No injection pattern detected")


def authorize_tool(tool: str, parameters: dict[str, int]) -> SecurityDecision:
    policy = ALLOWED_TOOLS.get(tool)
    if policy is None:
        return SecurityDecision(False, f"Tool '{tool}' is not allowlisted")
    for field, maximum in policy.items():
        actual_key = field.replace("max_", "")
        if parameters.get(actual_key, 0) > maximum:
            return SecurityDecision(False, f"{actual_key} exceeds limit {maximum}")
    return SecurityDecision(True, "Tool and blast radius are allowed")

