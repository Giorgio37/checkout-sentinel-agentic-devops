from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = PROJECT_ROOT / "artifacts"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value: Any) -> str:
    payload = value if isinstance(value, bytes) else canonical_json(value).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def append_jsonl(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(canonical_json(value) + "\n")


def record_audit(
    actor: str,
    action: str,
    outcome: str,
    request: Any,
    response: Any,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    event = {
        "schema": "checkout-sentinel.audit/v1",
        "event_id": digest({"actor": actor, "action": action, "timestamp": utc_now(), "request": request})[:20],
        "timestamp": utc_now(),
        "actor": actor,
        "action": action,
        "outcome": outcome,
        "request_sha256": digest(request),
        "response_sha256": digest(response),
        "details": details or {},
    }
    append_jsonl(ARTIFACTS / "audit" / "events.jsonl", event)
    return event

