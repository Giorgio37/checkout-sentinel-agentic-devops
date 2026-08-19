from __future__ import annotations

from .approval import verify
from .common import ARTIFACTS, record_audit, utc_now, write_json
from .observability import detect_anomaly, record_release_metrics
from .service import checkout
from .sre_agent import respond_to_anomaly
from .telemetry import span


def deploy() -> dict:
    request, approval = verify()
    phases = []
    with span(
        "release canary-10-50-100",
        {"deployment.strategy": request["strategy"], "deployment.version": request["release"]},
    ):
        for traffic in (10, 50, 100):
            # Version 2.3.1 has a controlled fault only at the 50% demo phase.
            error_rate = 0.01 if traffic == 10 else (0.20 if traffic == 50 else 0.01)
            latency = 140 if traffic == 10 else (480 if traffic == 50 else 160)
            checkout(75.0, 50.0, request["release"])
            metric = record_release_metrics(traffic, error_rate, latency)
            anomaly = detect_anomaly(metric)
            phase = {"traffic_percent": traffic, "metric": metric, "anomaly": anomaly, "timestamp": utc_now()}
            phases.append(phase)
            if anomaly["anomaly"]:
                response = respond_to_anomaly(anomaly)
                result = {
                    "release": request["release"],
                    "approval": approval,
                    "strategy": request["strategy"],
                    "phases": phases,
                    "final_status": response["status"],
                    "sre_response": response,
                }
                write_json(ARTIFACTS / "release" / "deployment_result.json", result)
                write_json(ARTIFACTS / "pipeline_state.json", {"stage": response["status"], "release": request["release"]})
                record_audit("release-orchestrator", "release.deploy", response["status"], request, result)
                return result
    raise RuntimeError("Fault injection did not trigger the expected anomaly")

