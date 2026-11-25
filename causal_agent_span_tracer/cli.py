"""CLI for Causal Agent Span Tracer."""
import argparse
import json
from .core import CausalSpanTracer


def main():
    parser = argparse.ArgumentParser(description="Causal Agent Span Tracer CLI")
    parser.add_argument("--trace-id", default="trace-demo", help="Trace ID")
    args = parser.parse_args()

    tr = CausalSpanTracer(args.trace_id)
    r = tr.start_span("orchestrate", kind="reasoning")
    t1 = tr.start_span("read_ast", kind="tool", parent_id=r)
    tr.end_span(t1, duration_ms=15.0, tokens=90)
    t2 = tr.start_span("run_tests", kind="tool", parent_id=r)
    tr.end_span(t2, duration_ms=340.0, tokens=40)
    tr.end_span(r, duration_ms=120.0, tokens=450)
    print(json.dumps(tr.summary(), indent=2))


if __name__ == "__main__":
    main()
