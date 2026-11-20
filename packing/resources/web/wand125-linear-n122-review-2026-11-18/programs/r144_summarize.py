"""Gather the complete decision: node 0 from r144_axis.py, nodes 1 to 200 from r144_bnb.py.

Usage: r144_summarize.py --axis AXIS.json --ranges DIR --bundle BUNDLE_DIR --out OUT.json

Reads this review's receipts (the axis decision and the range files written by
r144_run_all.sh) and, for comparison only, the source's 201 result.json records (nodes and
seconds). Writes one receipt: every node's verdict, boxes, CPU and least discharged
margin; the nodes decided, refuted or undecided; the totals; and the ratio of this
review's boxes to the source's nodes. Decides nothing beyond what the receipts say.
Written after the controls plan (a disclosed addition); imports nothing from
jlevy/squares or the source.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import statistics
import sys
from fractions import Fraction as F


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--axis", required=True)
    ap.add_argument("--ranges", required=True)
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    ax = json.load(open(a.axis))
    nodes = {}
    for p in sorted(glob.glob(os.path.join(a.ranges, "range-*.json"))):
        for r in json.load(open(p))["nodes"]:
            if r["j"] in nodes:
                raise SystemExit(f"node {r['j']} twice")
            nodes[r["j"]] = {"j": r["j"], "verdict": r["verdict"], "boxes": r["stats"]["nodes"], "discharged": r["stats"]["discharged"], "cpu_seconds": r["cpu_seconds"], "least_margin": r["stats"]["least_margin"], "max_terms": r["stats"]["max_terms"], "rect_exact": r["stats"]["rect_exact"], "max_depth": r["stats"]["max_depth"], "file": os.path.basename(p)}
    src = {}
    for j in range(201):
        rr = json.loads(open(os.path.join(a.bundle, f"net{j:03d}", "result.json")).read(), parse_float=lambda s: F(s))
        src[j] = {"nodes": rr["nodes"], "leaves": rr["leaves"], "seconds": float(rr["seconds"])}
    rows = [{"j": 0, "verdict": ax["verdict"], "method": "r144_axis.py", "least_exact": ax["least_exact"]["exact_float"], "cpu_seconds": ax["cpu_seconds"]}]
    for j in range(1, 201):
        if j in nodes:
            r = dict(nodes[j])
            r["method"] = "r144_bnb.py"
            r["source_nodes"] = src[j]["nodes"]
            r["boxes_over_source_nodes"] = r["boxes"] / src[j]["nodes"]
            rows.append(r)
        else:
            rows.append({"j": j, "verdict": "NOT_RUN"})
    decided = [r["j"] for r in rows if r["verdict"] in ("NODE_DECIDED", "AXIS_DECIDED")]
    other = [{"j": r["j"], "verdict": r["verdict"]} for r in rows if r["verdict"] not in ("NODE_DECIDED", "AXIS_DECIDED")]
    bnb = [r for r in rows if r.get("method") == "r144_bnb.py"]
    ratios = [r["boxes_over_source_nodes"] for r in bnb]
    res = {
        "program": "r144_summarize.py",
        "verdict": "ALL_201_NODES_DECIDED" if len(decided) == 201 else "INCOMPLETE",
        "nodes_decided": len(decided),
        "not_decided": other,
        "boxes_total_nodes_1_200": sum(r["boxes"] for r in bnb),
        "source_nodes_total_1_200": sum(src[j]["nodes"] for j in range(1, 201)),
        "source_nodes_total": sum(src[j]["nodes"] for j in range(201)),
        "source_seconds_total": sum(src[j]["seconds"] for j in range(201)),
        "cpu_seconds_nodes_1_200_in_run": round(sum(r["cpu_seconds"] for r in bnb), 1),
        "boxes_over_source_nodes": {"min": min(ratios), "median": statistics.median(ratios), "max": max(ratios)} if ratios else None,
        "least_discharged_margin": min((r for r in bnb), key=lambda r: r["least_margin"]) if bnb else None,
        "max_terms": max(r["max_terms"] for r in bnb) if bnb else None,
        "rect_exact_total": sum(r["rect_exact"] for r in bnb),
        "max_depth": max(r["max_depth"] for r in bnb) if bnb else None,
        "rows": rows,
    }
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1)
        f.write("\n")
    print(res["verdict"], f"{len(decided)}/201 decided", f"boxes {res['boxes_total_nodes_1_200']}", f"run cpu {res['cpu_seconds_nodes_1_200_in_run']} s", f"ratio {res['boxes_over_source_nodes']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
