"""Price the full recomputations check.py does not run, from the author's own records.

    python -I price_recomputation.py EDITION_ROOT OUT.json

Reads, as data only:
- the 1,152 selected capture slices (98 statements): each slice's Python and Node outputs
  give `cpu_seconds_rows` and `seconds` (wall, 4 workers), and its provenance record gives
  started_utc/finished_utc and the runtime;
- the 13 trees' second execution (local-research/.../rerun_trees_20261011): each checker
  output ends with the BSD `time -l` line "<real> real <user> user <sys> sys".
Standard library only; nothing in the edition is executed.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

CAP = "research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/"
RERUN = "local-research/claude-20261002/results/rerun_trees_20261011/"
TREES = ["JQ", "JPG15p_v5", "JPG17m_v5", "JPG3m_v5", "JPG3p_v5", "JPG17p_v5", "JPG15m_v5",
         "G20S", "HW", "JG", "JPWS_v4", "JPW13", "JPA_v5"]
TIME_LINE = re.compile(r"^\s*([0-9.]+) real\s+([0-9.]+) user\s+([0-9.]+) sys\s*$", re.M)


def utc(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    plan = json.loads((root / CAP / "checker_sources/PLAN_MANIFEST.json").read_text())
    tot = Counter()
    runtimes = Counter()
    per_row_py: list[float] = []
    first_start, last_end = None, None
    n_slices = n_rows = 0
    for st in plan["statements"]:
        sid = st["statement_id"]
        folder = root / CAP / "statements" / sid / "slices"
        dirs = {p.name.split("-")[0]: p for p in folder.iterdir() if p.is_dir()}
        for sl in st["slices"]:
            d = dirs[sl["slice_id"]]
            py = json.loads((d / "py.json").read_text())
            node = json.loads((d / "node.json").read_text())
            prov = json.loads((d / "provenance.json").read_text())
            rows = sl["end_exclusive"] - sl["start"]
            n_slices += 1
            n_rows += rows
            tot["py_cpu_s"] += float(py["cpu_seconds_rows"])
            tot["node_cpu_s"] += float(node["cpu_seconds_rows"])
            tot["py_wall_s"] += float(py["seconds"])
            tot["node_wall_s"] += float(node["seconds"])
            s, e = utc(prov["started_utc"]), utc(prov["finished_utc"])
            tot["slice_record_wall_s"] += (e - s).total_seconds()
            first_start = s if first_start is None or s < first_start else first_start
            last_end = e if last_end is None or e > last_end else last_end
            per_row_py.append(float(py["cpu_seconds_rows"]) / rows)
            rt = prov["runtime"]
            runtimes[(rt["platform_system"], rt["platform_architecture"], rt["python_version"],
                      rt["node_version"], py["workers"], node["workers"])] += 1
    trees = {}
    for t in TREES:
        rec = {}
        for c in ("C1", "C2"):
            text = (root / RERUN / f"{t}_{c}.out").read_text(errors="replace")
            m = TIME_LINE.findall(text)
            real, user, sys_ = (float(x) for x in m[-1])
            rec[c] = {"real_s": real, "cpu_s": round(user + sys_, 2)}
        trees[t] = rec
    tree_c1 = sum(v["C1"]["cpu_s"] for v in trees.values())
    tree_c2 = sum(v["C2"]["cpu_s"] for v in trees.values())
    per_row_py.sort()
    h = 3600.0
    receipt = {
        "schema": "k17-recomputation-price/v1",
        "capture": {
            "statements": len(plan["statements"]),
            "slices_per_checker": n_slices,
            "rows_per_checker": n_rows,
            "python_cpu_hours": round(tot["py_cpu_s"] / h, 1),
            "node_cpu_hours": round(tot["node_cpu_s"] / h, 1),
            "both_checkers_cpu_hours": round((tot["py_cpu_s"] + tot["node_cpu_s"]) / h, 1),
            "python_wall_hours_4_workers": round(tot["py_wall_s"] / h, 1),
            "node_wall_hours_4_workers": round(tot["node_wall_s"] / h, 1),
            "slice_record_wall_hours_sum": round(tot["slice_record_wall_s"] / h, 1),
            "python_cpu_s_per_row_median": round(per_row_py[len(per_row_py) // 2], 3),
            "python_cpu_s_per_row_max_slice": round(per_row_py[-1], 3),
            "first_slice_started_utc": first_start.isoformat() + "Z",
            "last_slice_finished_utc": last_end.isoformat() + "Z",
            "runtimes": [
                {"system": k[0], "arch": k[1], "python": k[2], "node": k[3],
                 "py_workers": k[4], "node_workers": k[5], "slices": v}
                for k, v in runtimes.items()
            ],
            "basis": "sum over the 1,152 selected slices of each output's cpu_seconds_rows (CPU) and seconds (wall); the author's Linux x86_64 runners",
        },
        "trees": {
            "per_tree": trees,
            "python_checker_cpu_hours": round(tree_c1 / h, 2),
            "node_checker_cpu_hours": round(tree_c2 / h, 2),
            "both_checkers_cpu_hours": round((tree_c1 + tree_c2) / h, 2),
            "basis": "user+sys of the time line each stored second-execution output ends with; the author's macOS arm64 build machine, one process per checker; JPA_v5's Node checker peaked at 7.0 GB RSS",
        },
    }
    out.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({k: v for k, v in receipt["capture"].items() if k != "runtimes"}, indent=1))
    print(json.dumps({k: v for k, v in receipt["trees"].items() if k != "per_tree"}, indent=1))
    print(json.dumps(receipt["capture"]["runtimes"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
