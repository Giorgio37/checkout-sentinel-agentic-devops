from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter, SpanExportResult

from .common import ARTIFACTS, append_jsonl


class JsonlSpanExporter(SpanExporter):
    def __init__(self, path: Path) -> None:
        self.path = path

    def export(self, spans: list[ReadableSpan]) -> SpanExportResult:
        for item in spans:
            context = item.get_span_context()
            parent_id = f"{item.parent.span_id:016x}" if item.parent else None
            append_jsonl(
                self.path,
                {
                    "schema": "opentelemetry.span/v1",
                    "trace_id": f"{context.trace_id:032x}",
                    "span_id": f"{context.span_id:016x}",
                    "parent_span_id": parent_id,
                    "name": item.name,
                    "start_time_unix_nano": item.start_time,
                    "end_time_unix_nano": item.end_time,
                    "duration_ms": round((item.end_time - item.start_time) / 1_000_000, 3),
                    "status": item.status.status_code.name,
                    "attributes": dict(item.attributes or {}),
                    "resource": dict(item.resource.attributes),
                },
            )
        return SpanExportResult.SUCCESS


_provider: TracerProvider | None = None


def configure_telemetry(reset: bool = False) -> None:
    global _provider
    path = ARTIFACTS / "telemetry" / "spans.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    if reset and path.exists():
        path.unlink()
    if _provider is None:
        _provider = TracerProvider(resource=Resource.create({"service.name": "checkout-sentinel"}))
        _provider.add_span_processor(SimpleSpanProcessor(JsonlSpanExporter(path)))
        trace.set_tracer_provider(_provider)


@contextmanager
def span(name: str, attributes: dict[str, Any]) -> Iterator[Any]:
    configure_telemetry()
    tracer = trace.get_tracer("checkout-sentinel", "1.0.0")
    safe_attributes = {
        key: value if isinstance(value, (str, bool, int, float)) else json.dumps(value, sort_keys=True)
        for key, value in attributes.items()
    }
    with tracer.start_as_current_span(name, attributes=safe_attributes) as current:
        yield current


def flush() -> None:
    if _provider is not None:
        _provider.force_flush()

