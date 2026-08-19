from __future__ import annotations

from .common import ARTIFACTS, append_jsonl, record_audit, utc_now
from .telemetry import span


ERROR_RATE_THRESHOLD = 0.05
LATENCY_P95_THRESHOLD_MS = 350


def record_release_metrics(traffic_percent: int, error_rate: float, latency_p95_ms: int) -> dict:
    metric = {
        "schema": "opentelemetry.metric/v1",
        "timestamp": utc_now(),
        "service.name": "checkout-api",
        "deployment.environment": "capstone-demo",
        "canary.traffic_percent": traffic_percent,
        "http.server.error_rate": error_rate,
        "http.server.duration.p95_ms": latency_p95_ms,
    }
    append_jsonl(ARTIFACTS / "telemetry" / "metrics.jsonl", metric)
    return metric


def detect_anomaly(metric: dict) -> dict:
    with span(
        "anomaly_detector evaluate",
        {
            "service.name": "checkout-api",
            "error_rate": metric["http.server.error_rate"],
            "latency_p95_ms": metric["http.server.duration.p95_ms"],
        },
    ):
        reasons = []
        if metric["http.server.error_rate"] > ERROR_RATE_THRESHOLD:
            reasons.append("error_rate_above_5_percent")
        if metric["http.server.duration.p95_ms"] > LATENCY_P95_THRESHOLD_MS:
            reasons.append("latency_p95_above_350_ms")
        result = {
            "anomaly": bool(reasons),
            "reasons": reasons,
            "thresholds": {"error_rate": ERROR_RATE_THRESHOLD, "latency_p95_ms": LATENCY_P95_THRESHOLD_MS},
            "observed": {
                "error_rate": metric["http.server.error_rate"],
                "latency_p95_ms": metric["http.server.duration.p95_ms"],
                "traffic_percent": metric["canary.traffic_percent"],
            },
        }
        record_audit("anomaly-detector", "telemetry.evaluate", "ALERT" if reasons else "HEALTHY", metric, result)
        return result

