"""Summarize run_bins.py receipts: decided count, refinements, smallest margins.

Usage: python -I summarize.py W FILE.jsonl [FILE.jsonl ...]
"""

import json
import sys
from collections import Counter


def main():
    w = int(sys.argv[1])
    recs = {}
    for path in sys.argv[2:]:
        for line in open(path):
            if line.strip():
                r = json.loads(line)
                recs[r["bin"]] = r
    bins = sorted(recs)
    out = {
        "bins": len(bins),
        "first_last": [bins[0], bins[-1]] if bins else None,
        "decided": sum(1 for k in bins if recs[k]["decided"]),
        "undecided": [k for k in bins if not recs[k]["decided"]],
        "refined_bins": {k: recs[k]["nodes"] for k in bins if recs[k]["nodes"] > 1},
        "min_root_core": min(recs[k]["root_core_min"] for k in bins),
        "min_over_leaves": min(recs[k]["min_over_leaves"] for k in bins),
        "cpu_s_total": round(sum(recs[k]["cpu_s"] for k in bins), 1),
    }
    margins = Counter(recs[k]["root_core_min"] - w for k in bins)
    out["root_core_margin_histogram_smallest"] = dict(sorted(margins.items())[:12])
    tight = sorted(bins, key=lambda k: (recs[k]["root_core_min"], k))[:15]
    out["tightest_bins_root_core"] = [(k, recs[k]["root_core_min"] - w, recs[k]["root_witness_centre"]) for k in tight]
    ex = [k for k in bins if "exact_angle_min" in recs[k]]
    if ex:
        allmins = [(min(recs[k]["exact_angle_min"].values()), k) for k in ex]
        out["exact_angle_bins"] = len(ex)
        out["exact_angle_min_overall"] = min(allmins)
        out["exact_angle_below_W"] = [k for v, k in allmins if v < w]
        out["exact_angle_equal_W"] = [k for v, k in allmins if v == w]
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
