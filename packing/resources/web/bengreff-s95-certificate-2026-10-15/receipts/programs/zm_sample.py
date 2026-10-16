"""Triage diagnostic for #610: choose a deterministic sample of the source's zm_mixed jobs
for a replay that prices the whole set, and print the cost distribution the source's
records state.

The sample is the TOP jobs by the source's recorded CPU (the hardest sub-roots), every
STRIDE-th job of jobs.txt in order, and the jobs named in ALSO (comma-separated ids, such
as the cells at the centre in the u bin [3/32, 1/8] that holds theta = arctan(1/5), where
the issue says an earlier cover was left uncertified), without repeats. It is written to
OUT in jobs.txt's format, so the run script reads it as it would the whole list.

usage: python -I zm_sample.py RECORDS_DIR JOBS OUT [TOP] [STRIDE] [ALSO]
"""

import json
import sys
from pathlib import Path

rec_dir, jobs_path, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
top = int(sys.argv[4]) if len(sys.argv) > 4 else 4
stride = int(sys.argv[5]) if len(sys.argv) > 5 else 38
also = [j for j in sys.argv[6].split(",") if j] if len(sys.argv) > 6 else []
jobs = [ln for ln in jobs_path.read_text().splitlines() if ln.strip()]
cost = {}
for path in sorted(rec_dir.glob("j*.jsonl")):
    for line in path.read_text().splitlines():
        d = json.loads(line)
        if "st" in d:
            cost[path.stem[1:]] = (d["st"]["cpu"], d["st"]["boxes"], d["st"]["maxdepth"], d["root"])
ranked = sorted(cost, key=lambda j: -cost[j][0])
total = sum(c[0] for c in cost.values())
print(f"jobs {len(jobs)}, recorded CPU {total:.1f} s, mean {total / len(cost):.2f} s")
for j in ranked[:8]:
    c = cost[j]
    print(f"  j{j}: cpu {c[0]:.1f} s, boxes {c[1]}, depth {c[2]}, root {' '.join(c[3])}")
pick = list(dict.fromkeys(ranked[:top] + [ln.split()[0] for ln in jobs[::stride]] + also))
chosen = [ln for ln in jobs if ln.split()[0] in set(pick)]
out.write_text("\n".join(chosen) + "\n")
share = sum(cost[ln.split()[0]][0] for ln in chosen)
print(f"sample {len(chosen)} jobs, recorded CPU {share:.1f} s ({100 * share / total:.1f}% of the whole)")
