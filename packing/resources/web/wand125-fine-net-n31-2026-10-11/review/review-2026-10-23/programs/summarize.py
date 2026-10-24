"""Gather capture.py's receipts for the sample and the controls, beside the source's log.

Usage: python3 -I summarize.py OUTDIR RUN_LOG PLAN.json SUMMARY.json

Decides nothing: it reads the receipts capture.py wrote (capture-<tag>-<j>.json), the
plan, and the source's run log, and tabulates for every planned direction this
checker's verdict, nodes, leaves, least exact bound and CPU beside the source's method,
nodes and least certified bound; then the controls' verdicts and their exact witnesses.
Prints the totals.
"""

from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path


def main() -> int:
    outdir, log, plan_path, summary_path = (Path(a) for a in sys.argv[1:5])
    plan = json.loads(plan_path.read_text())
    src = {r["r"]: r for r in (json.loads(x) for x in gzip.open(log, "rt")) if "r" in r}
    rows = []
    missing = []
    for j in plan["directions"]:
        f = outdir / f"capture-original-{j:04d}.json"
        if not f.exists():
            missing.append(j)
            continue
        d = json.loads(f.read_text())
        s = src[j]
        rows.append({
            "j": j, "verdict": d["verdict"], "float_nodes": d["float_nodes"],
            "leaves": d.get("exact_leaves"), "retried": d.get("exact_retried_leaves"),
            "least_exact_bound": d.get("exact_least_bound_float"),
            "least_leaf_centre_capture": d.get("least_leaf_centre_capture_float"),
            "cpu": d["cpu_total"], "partition": d.get("partition_holds"),
            "source_method": s["method"], "source_nodes": s.get("nodes"),
            "source_least_bound": s["min_certified_lower_bound"],
            "source_cpu": s["cpu_seconds"],
        })
    controls = []
    for f in sorted(outdir.glob("capture-*.json")):
        if f.name.startswith("capture-original-"):
            continue
        d = json.loads(f.read_text())
        controls.append({k: d.get(k) for k in (
            "j", "verdict", "mass_scale", "dropped_row", "float_status", "float_nodes",
            "worst_centre", "worst_centre_capture_float", "worst_centre_in_exact_domain",
            "exact_least_bound_float", "cpu_total")} | {"file": f.name})
    verified = [r for r in rows if r["verdict"] == "VERIFIED"]
    summary = {
        "kind": "review-2026-10-23-n31-summary/v1",
        "planned": len(plan["directions"]), "decided": len(rows), "missing": missing,
        "verified": len(verified),
        "not_verified": [r["j"] for r in rows if r["verdict"] != "VERIFIED"],
        "cpu_sample": round(sum(r["cpu"] for r in rows), 1),
        "cpu_controls": round(sum(c["cpu_total"] or 0 for c in controls), 1),
        "float_nodes_sample": sum(r["float_nodes"] for r in rows),
        "source_nodes_same_directions": sum(r["source_nodes"] or 0 for r in rows),
        "least_exact_bound": min((r["least_exact_bound"] for r in verified), default=None),
        "rows": rows, "controls": controls,
    }
    summary_path.write_text(json.dumps(summary, indent=1) + "\n")
    print(f"planned {summary['planned']} decided {summary['decided']} verified "
          f"{summary['verified']} not verified {summary['not_verified']} missing {missing}")
    print(f"cpu sample {summary['cpu_sample']} s, controls {summary['cpu_controls']} s; "
          f"nodes {summary['float_nodes_sample']} here against "
          f"{summary['source_nodes_same_directions']} at the source")
    for c in controls:
        print("control", c["file"], c["verdict"], c["worst_centre_capture_float"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
