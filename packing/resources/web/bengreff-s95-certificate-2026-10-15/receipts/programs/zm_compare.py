"""Triage diagnostic for #610: compare zm_mixed per-root records, source against replay,
census for census with CPU left out, and the headers apart from the input path. The #594
triage's zm_compare.py, changed to read a replay of a sample: source records the replay
did not run are counted as not replayed, not failed, and a replay record with no source
record fails. It also prints each replayed job's CPU beside the source's, for the price.

usage: python -I zm_compare.py SOURCE_DIR REPLAY_DIR
"""

import json
import sys
from pathlib import Path


def read(d):
    out = {}
    for p in sorted(Path(d).glob("j*.jsonl")):
        lines = [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
        h = next(x for x in lines if x.get("kind") == "zm_mixed cert header")
        r = next(x for x in lines if "st" in x)
        cpu = r["st"]["cpu"]
        h = {k: v for k, v in h.items() if k != "input"}
        st = {k: v for k, v in r["st"].items() if k != "cpu"}
        out[p.name] = (h, tuple(r["root"]), st, r["unc"], cpu)
    return out


a, b = read(sys.argv[1]), read(sys.argv[2])
both = sorted(k for k in b if k in a)
same_h = sum(1 for k in both if a[k][0] == b[k][0])
same_r = sum(1 for k in both if a[k][1:4] == b[k][1:4])
print(
    f"files source {len(a)} replay {len(b)}; compared {len(both)}; not replayed {len(a) - len(both)}; "
    f"headers equal (input path aside) {same_h}; roots and census equal {same_r}"
)
bad = [k for k in b if k not in a] + [k for k in both if a[k][:4] != b[k][:4]]
for k in sorted(bad):
    print("differs:", k, a.get(k, (None, None, None))[2], b[k][2])
src_cpu = sum(a[k][4] for k in both)
rep_cpu = sum(b[k][4] for k in both)
for k in both:
    print(f"  {k}: boxes {b[k][2]['boxes']}, depth {b[k][2]['maxdepth']}, UNCERT {b[k][2]['UNCERT']}, "
          f"cpu source {a[k][4]:.1f} s, replay {b[k][4]:.1f} s")
if both:
    total = sum(v[4] for v in a.values())
    print(
        f"compared jobs: CPU source {src_cpu:.1f} s, replay {rep_cpu:.1f} s, ratio {rep_cpu / src_cpu:.3f}; "
        f"whole set at that ratio: {total * rep_cpu / src_cpu:.0f} CPU-s"
    )
sys.exit(1 if bad else 0)
