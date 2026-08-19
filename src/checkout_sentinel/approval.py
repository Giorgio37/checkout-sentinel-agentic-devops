from __future__ import annotations

from .common import ARTIFACTS, digest, read_json, record_audit, utc_now, write_json


REQUEST_PATH = ARTIFACTS / "approval" / "request.json"
DECISION_PATH = ARTIFACTS / "approval" / "decision.json"


def create_request(risk: dict) -> dict:
    request = {
        "release": "2.3.1",
        "environment": "capstone-demo",
        "risk_sha256": digest(risk),
        "risk_score": risk["score"],
        "strategy": risk["strategy"],
        "requested_at": utc_now(),
        "status": "PENDING",
    }
    write_json(REQUEST_PATH, request)
    write_json(ARTIFACTS / "pipeline_state.json", {"stage": "AWAITING_APPROVAL", "release": "2.3.1"})
    record_audit("pipeline-orchestrator", "approval.request", "PENDING", risk, request)
    return request


def approve(actor: str) -> dict:
    if len(actor.strip()) < 3:
        raise ValueError("Approver name must contain at least three characters")
    request = read_json(REQUEST_PATH)
    if not request:
        raise FileNotFoundError("No pending approval request; run prepare first")
    decision = {
        "request_sha256": digest(request),
        "risk_sha256": request["risk_sha256"],
        "decision": "APPROVED",
        "approver": actor.strip(),
        "approved_at": utc_now(),
        "scope": {"release": request["release"], "environment": request["environment"]},
    }
    write_json(DECISION_PATH, decision)
    write_json(ARTIFACTS / "pipeline_state.json", {"stage": "APPROVED", "release": request["release"]})
    record_audit(actor.strip(), "approval.decide", "APPROVED", request, decision)
    return decision


def verify() -> tuple[dict, dict]:
    request = read_json(REQUEST_PATH)
    decision = read_json(DECISION_PATH)
    if not request or not decision or decision.get("decision") != "APPROVED":
        raise PermissionError("Deployment blocked: timestamped human approval is missing")
    if decision.get("request_sha256") != digest(request):
        raise PermissionError("Deployment blocked: approval request integrity check failed")
    risk = read_json(ARTIFACTS / "release" / "risk_assessment.json")
    if not risk or request.get("risk_sha256") != digest(risk):
        raise PermissionError("Deployment blocked: risk assessment integrity check failed")
    if decision.get("risk_sha256") != request.get("risk_sha256"):
        raise PermissionError("Deployment blocked: approved risk hash does not match the request")
    return request, decision
