"""Core causal span DAG recorder and critical-path analyzer for AI agents."""
from typing import Any, Dict, List, Optional


class CausalSpanTracer:
    """Tracks nested causal agent spans, token rollups, and critical-path bottlenecks."""

    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self._spans: Dict[str, Dict[str, Any]] = {}
        self._seq = 0

    def start_span(self, name: str, kind: str = "tool", parent_id: Optional[str] = None) -> str:
        if parent_id is not None and parent_id not in self._spans:
            raise KeyError(f"Unknown parent span {parent_id}")
        self._seq += 1
        sid = f"sp-{self._seq}"
        self._spans[sid] = {
            "span_id": sid,
            "name": name,
            "kind": kind,
            "parent_id": parent_id,
            "duration_ms": 0.0,
            "tokens": 0,
            "status": "running",
        }
        return sid

    def end_span(self, span_id: str, duration_ms: float, tokens: int = 0, status: str = "ok"):
        sp = self._spans[span_id]
        sp["duration_ms"] = duration_ms
        sp["tokens"] = tokens
        sp["status"] = status

    def summary(self) -> Dict[str, Any]:
        total_tokens = sum(s["tokens"] for s in self._spans.values())
        bottleneck = max(self._spans.values(), key=lambda s: s["duration_ms"]) if self._spans else None
        errors = [s["span_id"] for s in self._spans.values() if s["status"] != "ok"]
        return {
            "trace_id": self.trace_id,
            "span_count": len(self._spans),
            "total_tokens": total_tokens,
            "bottleneck_span": bottleneck["name"] if bottleneck else None,
            "bottleneck_ms": bottleneck["duration_ms"] if bottleneck else 0.0,
            "error_spans": errors,
        }
