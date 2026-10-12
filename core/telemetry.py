"""OpenTelemetry GenAI Observability Engine for CampusGemma AI.

Provides semantic span instrumentation for Google Gemma 2 model inference,
tracking latency, prompt tokens, completion tokens, and execution traces.
Supports native OpenTelemetry SDK with a seamless fallback logger for zero-dependency environments.
"""

from __future__ import annotations

import time
import uuid
from typing import Any, Dict, List, Optional

_SPANS: List[Dict[str, Any]] = []

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
    HAS_OTEL_SDK = True
except ImportError:
    HAS_OTEL_SDK = False


class FallbackSpan:
    """A resilient, zero-dependency OpenTelemetry span representation."""

    def __init__(self, name: str):
        self.name = name
        self.trace_id = uuid.uuid4().hex
        self.span_id = uuid.uuid4().hex[:16]
        self.attributes: Dict[str, Any] = {}
        self.start_time = time.perf_counter()
        self.end_time: Optional[float] = None
        self.status = "OK"

    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = value

    def __enter__(self) -> FallbackSpan:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.end_time = time.perf_counter()
        duration_ms = round((self.end_time - self.start_time) * 1000, 2)
        if exc_type:
            self.status = "ERROR"
        _SPANS.append({
            "name": self.name,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "duration_ms": duration_ms,
            "attributes": dict(self.attributes),
            "status": self.status,
        })


class FallbackTracer:
    """Fallback tracer providing start_as_current_span interface."""

    def start_as_current_span(self, name: str) -> FallbackSpan:
        return FallbackSpan(name)


_EXPORTER: Any = None
_TRACER: Any = None


def init_telemetry() -> Any:
    """Initialize OpenTelemetry tracer provider with an in-memory exporter, or fallback."""
    global _EXPORTER, _TRACER

    if _TRACER is not None:
        return _TRACER

    if HAS_OTEL_SDK:
        try:
            _EXPORTER = InMemorySpanExporter()
            provider = TracerProvider()
            provider.add_span_processor(SimpleSpanProcessor(_EXPORTER))
            trace.set_tracer_provider(provider)
            _TRACER = trace.get_tracer("campus.gemma.agent", "0.1.0")
            return _TRACER
        except Exception:
            pass

    _TRACER = FallbackTracer()
    return _TRACER


def get_tracer() -> Any:
    """Get or initialize the global GenAI tracer."""
    global _TRACER
    if _TRACER is None:
        return init_telemetry()
    return _TRACER


def get_recent_spans() -> List[Dict[str, Any]]:
    """Retrieve formatted list of recent trace spans for UI visualization."""
    global _EXPORTER, _SPANS

    if HAS_OTEL_SDK and _EXPORTER is not None:
        spans_data = []
        for span in _EXPORTER.get_finished_spans()[-15:]:
            duration_ms = (span.end_time - span.start_time) / 1_000_000.0 if (span.end_time and span.start_time) else 0.0
            spans_data.append({
                "name": span.name,
                "trace_id": format(span.context.trace_id, "032x"),
                "span_id": format(span.context.span_id, "016x"),
                "duration_ms": round(duration_ms, 2),
                "attributes": dict(span.attributes or {}),
                "status": span.status.status_code.name,
            })
        return spans_data

    return _SPANS[-15:]
