"""Tests for Causal Agent Span Tracer."""
import unittest
from causal_agent_span_tracer.core import CausalSpanTracer


class TestCausalSpanTracer(unittest.TestCase):
    def test_records_hierarchy_and_bottleneck(self):
        tr = CausalSpanTracer("tr-1")
        p = tr.start_span("plan", kind="reasoning")
        c = tr.start_span("compile", kind="tool", parent_id=p)
        tr.end_span(c, duration_ms=520.0, tokens=50)
        tr.end_span(p, duration_ms=180.0, tokens=400)
        s = tr.summary()
        self.assertEqual(s["span_count"], 2)
        self.assertEqual(s["total_tokens"], 450)
        self.assertEqual(s["bottleneck_span"], "compile")

    def test_unknown_parent_raises(self):
        tr = CausalSpanTracer("tr-2")
        with self.assertRaises(KeyError):
            tr.start_span("child", parent_id="missing")
