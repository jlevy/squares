"""Compare K3 independent row results (JSON lines from k3_capture_row.py) with the stored rows.

Usage: python compare_independent.py STATEMENT_DIR K3_OUTPUT.jsonl OUT.json
Compared per row: the pass decision and, per level (each class and the default), the least charge.
Cell counts are reported but not compared (the two arrangements differ in granularity).
"""

import glob
import json
import os
import sys


def main():
    sdir, k3out, out = sys.argv[1], sys.argv[2], sys.argv[3]
    mine = {}
    for line in open(k3out, encoding="utf-8"):
        line = line.strip()
        if line.startswith('{"row"'):
            r = json.loads(line)
            mine[r["row"]] = r
    stored_py, stored_node = {}, {}
    for kind, store in (("py", stored_py), ("node", stored_node)):
        for f in sorted(glob.glob(os.path.join(sdir, "slices", "*", kind + ".json"))):
            s = json.load(open(f, encoding="utf-8"))
            if s["end_exclusive"] <= min(mine) or s["start"] > max(mine):
                continue
            for r in s["rows"]:
                if r["interval"] in mine:
                    store[r["interval"]] = r
    results = []
    for i in sorted(mine):
        m = mine[i]
        for kind, store in (("python", stored_py), ("node", stored_node)):
            s = store[i]
            stored_levels = {c["name"]: c["minimum_units"] for c in s["classes"]}
            stored_levels["default"] = s["default"]["minimum_units"]
            mine_levels = {k: v["minimum_units"] for k, v in m["levels"].items()}
            same = stored_levels == mine_levels and s["passed"] == m["passed"]
            results.append({"row": i, "against": kind, "equal": same, "passed_k3": m["passed"],
                            "k3_minima": mine_levels, "stored_minima": stored_levels,
                            "k3_cells": sum(v["cells"] for v in m["levels"].values()), "stored_cells": s["cells"],
                            "k3_cpu_seconds": m["cpu_seconds"]})
    summary = {
        "statement": os.path.basename(os.path.normpath(sdir)),
        "rows": sorted(mine),
        "rows_checked": len(mine),
        "all_pass_k3": all(m["passed"] for m in mine.values()),
        "all_minima_equal_python": all(r["equal"] for r in results if r["against"] == "python"),
        "all_minima_equal_node": all(r["equal"] for r in results if r["against"] == "node"),
        "k3_cpu_seconds": round(sum(m["cpu_seconds"] for m in mine.values()), 1),
        "differences": [r for r in results if not r["equal"]],
    }
    json.dump({"summary": summary, "rows": results}, open(out, "w", encoding="utf-8"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
