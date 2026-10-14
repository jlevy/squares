"""Triage diagnostic for #594: compare zm_mixed per-root records, source against replay,
census for census with CPU left out, and the headers apart from the input path.

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
        h = {k: v for k, v in h.items() if k != "input"}
        st = {k: v for k, v in r["st"].items() if k != "cpu"}
        out[p.name] = (h, tuple(r["root"]), st, r["unc"])
    return out


a, b = read(sys.argv[1]), read(sys.argv[2])
same_h = sum(1 for k in a if k in b and a[k][0] == b[k][0])
same_r = sum(1 for k in a if k in b and a[k][1:] == b[k][1:])
print(f"files source {len(a)} replay {len(b)}; headers equal (input path aside) {same_h}; roots and census equal {same_r}")
for k in sorted(a):
    if k not in b or a[k][1:] != b[k][1:]:
        print("differs:", k, a[k][2], b.get(k, (None, None, None))[2])
