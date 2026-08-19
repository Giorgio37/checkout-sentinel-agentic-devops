from __future__ import annotations

import argparse
import json
import shutil

from .approval import approve, create_request
from .ci_agent import run_ci_agent
from .common import ARTIFACTS, read_json, record_audit
from .deployment import deploy
from .provenance import generate_provenance
from .risk_agent import assess_risk
from .telemetry import configure_telemetry, flush


def prepare() -> dict:
    if ARTIFACTS.exists():
        shutil.rmtree(ARTIFACTS)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    configure_telemetry(reset=True)
    ci_result = run_ci_agent()
    risk = assess_risk(ci_result)
    generate_provenance()
    request = create_request(risk)
    summary = {"ci": ci_result, "risk": risk, "approval": request}
    record_audit("pipeline-orchestrator", "pipeline.prepare", "AWAITING_APPROVAL", {"release": "2.3.1"}, summary)
    flush()
    return summary


def status() -> dict:
    return {
        "pipeline": read_json(ARTIFACTS / "pipeline_state.json", {"stage": "NOT_STARTED"}),
        "ci": read_json(ARTIFACTS / "build" / "ci_result.json"),
        "risk": read_json(ARTIFACTS / "release" / "risk_assessment.json"),
        "approval_request": read_json(ARTIFACTS / "approval" / "request.json"),
        "approval_decision": read_json(ARTIFACTS / "approval" / "decision.json"),
        "deployment": read_json(ARTIFACTS / "release" / "deployment_result.json"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Checkout Sentinel capstone pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("prepare", help="Run CI, security, risk, provenance, and create approval request")
    approval_parser = subparsers.add_parser("approve", help="Record a timestamped human approval")
    approval_parser.add_argument("--actor", required=True)
    subparsers.add_parser("deploy", help="Verify approval, run canary, detect anomaly, and remediate")
    subparsers.add_parser("status", help="Print current pipeline state")
    args = parser.parse_args()

    if args.command == "prepare":
        result = prepare()
    elif args.command == "approve":
        result = approve(args.actor)
    elif args.command == "deploy":
        result = deploy()
    else:
        result = status()
    flush()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

