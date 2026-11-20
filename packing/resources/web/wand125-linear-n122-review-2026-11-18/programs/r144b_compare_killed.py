"""Compare the killed run of range 176 to 200 with its rerun, node by node.

Usage: r144b_compare_killed.py --killed KILLED.stdout.txt --rerun RERUN.stdout.txt
                               --out OUT.json

A container restart killed the first run of r144_bnb.py over nodes 176 to 200 after it
had printed nodes 176 to 193; r144_run_all.sh then ran the range again from scratch. This
program reads the lines both runs printed and reports, for every node the killed run
finished, whether the verdict, the box count, the least discharged margin and the witness
agree (they should: the program is deterministic), with each run's CPU over those nodes.
It decides nothing about the certificate. Written by lane r144b-1118 after the controls
plan (a disclosed addition); imports nothing from jlevy/squares or the source.
"""

from __future__ import annotations

import argparse
import json
import re
import sys

LINE = re.compile(r"^(\S+) node (\d+) boxes (\d+) least margin (\S+) witness (.+) cpu (\S+) s$")


def read(path: str) -> dict[int, dict]:
    rows = {}
    with open(path) as f:
        for line in f:
            m = LINE.match(line.strip())
            if m:
                rows[int(m.group(2))] = {"verdict": m.group(1), "boxes": int(m.group(3)), "least_margin": m.group(4), "witness": m.group(5), "cpu_seconds": float(m.group(6))}
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--killed", required=True)
    ap.add_argument("--rerun", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    killed, rerun = read(a.killed), read(a.rerun)
    fields = ("verdict", "boxes", "least_margin", "witness")
    agree = [j for j in sorted(killed) if j in rerun and all(killed[j][k] == rerun[j][k] for k in fields)]
    differ = [j for j in sorted(killed) if j not in agree]
    res = {
        "program": "r144b_compare_killed.py",
        "killed_nodes": sorted(killed),
        "rerun_nodes": sorted(rerun),
        "compared_fields": list(fields),
        "agree": agree,
        "differ_or_missing": differ,
        "killed_cpu_seconds_over_its_nodes": round(sum(r["cpu_seconds"] for r in killed.values()), 2),
        "rerun_cpu_seconds_over_the_same_nodes": round(sum(rerun[j]["cpu_seconds"] for j in killed if j in rerun), 2),
        "verdict": "KILLED_RUN_REPRODUCED" if killed and not differ else "KILLED_RUN_DIFFERS",
    }
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1)
        f.write("\n")
    print(res["verdict"], f"{len(agree)} of {len(killed)} nodes agree", f"differ {differ}")
    return 0 if res["verdict"] == "KILLED_RUN_REPRODUCED" else 1


if __name__ == "__main__":
    sys.exit(main())
