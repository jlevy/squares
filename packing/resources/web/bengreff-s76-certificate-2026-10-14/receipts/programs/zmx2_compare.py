"""Triage diagnostic for #594: compare two zmx2 cert root logs root for root (census fields,
timing left out), list the roots with uncertified or capped boxes, and check them against a
list of failing roots.

usage: python -I zmx2_compare.py SHIPPED_LOG[.gz] REPLAY_LOG FAILING_ROOTS
"""

import gzip
import re
import sys

PAT = re.compile(
    r"^ROOT (\d+) pass (\d+) root (\S+) boxes (\d+) cert (\d+) empty (\d+) uncert (\d+) maxdepth (\d+) capped (\d+) ms \d+$"
)


def read(path):
    op = gzip.open if path.endswith(".gz") else open
    headers, roots, uncert = [], {}, []
    with op(path, "rt") as fh:
        for ln in fh:
            ln = ln.rstrip("\n")
            if ln.startswith("UNCERT "):
                uncert.append(ln.split(" | ")[0])
                continue
            if ln.startswith("#"):
                headers.append(ln)
                continue
            m = PAT.match(ln)
            if not m:
                raise SystemExit(f"{path}: unparsed line {ln!r}")
            key = (m.group(1), m.group(2), m.group(3))
            if key in roots:
                raise SystemExit(f"{path}: duplicate root {key}")
            roots[key] = tuple(int(v) for v in m.groups()[3:])
    return headers, roots, sorted(uncert)


h1, r1, u1 = read(sys.argv[1])
h2, r2, u2 = read(sys.argv[2])
failing = sorted(ln.strip() for ln in open(sys.argv[3]) if ln.strip())
same = sum(1 for k in r1 if r2.get(k) == r1[k])
bad1 = sorted(k[2] for k, v in r1.items() if v[3] > 0 or v[5] > 0)
bad2 = sorted(k[2] for k, v in r2.items() if v[3] > 0 or v[5] > 0)
tot = lambda r, i: sum(v[i] for v in r.values())
print("headers equal:", h1 == h2, h1[:1])
print(f"roots shipped {len(r1)}, replay {len(r2)}, identical census {same}")
print("shipped boxes/cert/empty/uncert:", [tot(r1, i) for i in range(4)], "max depth", max(v[4] for v in r1.values()))
print("replay  boxes/cert/empty/uncert:", [tot(r2, i) for i in range(4)], "max depth", max(v[4] for v in r2.values()))
print("roots with uncertified or capped boxes, shipped:", bad1)
print("same in replay:", bad1 == bad2, "; equal to failing_roots.txt:", bad2 == failing)
for k, v in sorted(r2.items()):
    if v[3] > 0:
        print("  ", k[2], "uncert", v[3], "boxes", v[0], "maxdepth", v[4])
print("UNCERT boxes shipped", len(u1), "replay", len(u2), "identical sets:", u1 == u2)
