from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .approval import approve
from .common import ARTIFACTS, PROJECT_ROOT, read_json
from .deployment import deploy
from .orchestrator import status


def count_lines(path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def dashboard_state() -> dict:
    current = status()
    current["counts"] = {
        "audit_events": count_lines(ARTIFACTS / "audit" / "events.jsonl"),
        "otel_spans": count_lines(ARTIFACTS / "telemetry" / "spans.jsonl"),
        "otel_metrics": count_lines(ARTIFACTS / "telemetry" / "metrics.jsonl"),
    }
    return current


class Handler(BaseHTTPRequestHandler):
    def send_json(self, value: dict, code: int = HTTPStatus.OK) -> None:
        body = json.dumps(value).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/":
            body = (PROJECT_ROOT / "dashboard" / "index.html").read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/api/state":
            self.send_json(dashboard_state())
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        size = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(size) or b"{}")
        try:
            if self.path == "/api/approve":
                self.send_json({"ok": True, "decision": approve(str(payload.get("actor", "")))})
                return
            if self.path == "/api/deploy":
                self.send_json({"ok": True, "deployment": deploy()})
                return
            self.send_error(HTTPStatus.NOT_FOUND)
        except (ValueError, PermissionError, FileNotFoundError) as error:
            self.send_json({"ok": False, "error": str(error)}, HTTPStatus.CONFLICT)

    def log_message(self, format: str, *args) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the Checkout Sentinel dashboard")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8765, type=int)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Checkout Sentinel dashboard: http://{args.host}:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()

