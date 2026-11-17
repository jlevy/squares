"""Tabulate this review's sampled decisions beside the lab's lines (decides nothing).

Reads out/axis-r0.json, out/sample/bnb-r*.json, out/bnb-r3663.json and the merged
receipts with selection.csv, and writes a Markdown table and a JSON summary: for each
sampled direction, the lab's stream and certified bound, this review's verdict, nodes,
least certified bound, lowest centre value, and CPU seconds.

Usage: tabulate.py PACKET OUT_DIR
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from xzcommon import read_bytes


def main() -> int:
    packet = Path(sys.argv[1])
    out = Path(sys.argv[2])
    rec = packet / "source" / "receipts"
    with (rec / "selection.csv").open() as fh:
        sel = {int(row["r"]): row["source"] for row in csv.DictReader(fh)}
    lab = {}
    for line in read_bytes(rec / "directions.jsonl.gz").decode().splitlines():
        row = json.loads(line)
        lab[row["r"]] = row
    shared = {round(j * 83 * 12000 / 40000) for j in range(0, 200, 10)}
    rows = []
    files = sorted(out.glob("sample/bnb-r*.json"))
    for f in files:
        rep = json.loads(f.read_text())
        r = rep["r"]
        rows.append({
            "r": r,
            "stream": sel[r],
            "node": "shared" if r in shared else "new",
            "lab_bound": lab[r]["min_certified_lower_bound"],
            "lab_nodes": lab[r].get("nodes"),
            "status": rep["status"],
            "nodes": rep["nodes"],
            "least_bound": rep["least_certified_bound"],
            "lowest_centre": rep["lowest_centre_estimate"],
            "lowest_at": rep["lowest_centre_estimate_at"],
            "U_r": rep["U_r"],
            "cpu": rep["cpu_seconds"],
            "largest_error_budget": rep["largest_error_budget"],
        })
    ax = json.loads((out / "axis-r0.json").read_text())
    rows.append({
        "r": 0, "stream": sel[0], "node": "shared", "lab_bound": lab[0]["min_certified_lower_bound"],
        "lab_nodes": None, "status": ax["verdict"], "nodes": ax["vertices"],
        "least_bound": ax["min_capture_float"], "lowest_centre": ax["min_capture_float"],
        "lowest_at": ax["argmin_float"], "U_r": "1184/125", "cpu": ax["cpu_seconds"],
        "largest_error_budget": 0.0,
    })
    rows.sort(key=lambda d: d["r"])
    lines = [
        "| r | lab stream | node | lab’s bound | verdict here | nodes here | least bound here | lowest centre here | CPU s |",
        "| ---: | --- | --- | ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for d in rows:
        lines.append(
            f"| {d['r']} | {d['stream']} | {d['node']} | {d['lab_bound']:.16f} | {d['status']} | {d['nodes']:,} | "
            f"{d['least_bound']:.12f} | {d['lowest_centre']:.9f} | {d['cpu']:.1f} |"
        )
    by_stream: dict[str, list[int]] = {}
    for d in rows:
        by_stream.setdefault(d["stream"], []).append(d["r"])
    summary = {
        "directions": len(rows),
        "all_verified": all(d["status"] == "verified" for d in rows),
        "by_stream": by_stream,
        "least_lowest_centre": min((d["lowest_centre"], d["r"]) for d in rows),
        "largest_error_budget": max(d["largest_error_budget"] for d in rows),
        "oblique_cpu_seconds": sum(d["cpu"] for d in rows if d["r"] != 0),
        "rows": rows,
    }
    (out / "sample-table.md").write_text("\n".join(lines) + "\n")
    (out / "sample-summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    print("\n".join(lines))
    print(json.dumps({k: v for k, v in summary.items() if k != "rows"}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
