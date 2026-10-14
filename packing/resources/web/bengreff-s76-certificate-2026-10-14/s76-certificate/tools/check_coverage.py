#!/usr/bin/env python3
"""Check that the zmx2 sweep and the zm_mixed records together certify the whole D4 fundamental
region [0, 9/2]^2 x {u in [0, 1/2]} for the given cover. Standard library only.

* every zmx2 root (cells 1/10 x 1/10 x 1/8 in u) appears exactly once in the zmx2 log, and the
  roots tile the region;
* every zmx2 root with uncertified boxes is tiled exactly by zm_mixed roots (1/20 x 1/20 x 1/32)
  whose records report 0 uncertified boxes, and whose headers name the same cover (sha256).

usage: python3 check_coverage.py ZMX2_LOG ZM_MIXED_JSONL_DIR COVER_SHA256
"""
import sys, re, json, glob, gzip
from fractions import Fraction as F

zlog, zdir, cover_sha = sys.argv[1], sys.argv[2], sys.argv[3]
op = gzip.open if zlog.endswith(".gz") else open
roots, failing = [], []
for ln in op(zlog, "rt"):
    if not ln.startswith("ROOT"):
        continue
    m = re.search(r"root (\S+) .*uncert (\d+) maxdepth (\d+) capped (\d+)", ln)
    b = tuple(F(v) for v in m.group(1).split(","))
    roots.append(b)
    if int(m.group(2)) > 0 or int(m.group(4)) > 0:
        failing.append(b)
vol = lambda b: (b[1] - b[0]) * (b[3] - b[2]) * (b[5] - b[4])
assert len(roots) == len(set(roots)), "duplicate zmx2 roots"
cells = {(b[0], b[2], b[4]) for b in roots}
expect = {(F(i, 10), F(j, 10), F(k, 8)) for i in range(45) for j in range(45) for k in range(4)}
assert cells == expect, "zmx2 roots do not tile the D4 region"
assert all(b[1] - b[0] == F(1, 10) and b[3] - b[2] == F(1, 10) and b[5] - b[4] == F(1, 8) for b in roots)
print("zmx2: %d roots tile [0,9/2]^2 x [0,1/2]; %d have uncertified boxes" % (len(roots), len(failing)))

subs = {}
for f in sorted(glob.glob(zdir + "/*.jsonl")):
    for ln in open(f):
        d = json.loads(ln)
        if d.get("kind") == "zm_mixed cert header":
            assert d["sha256"]["input"] == cover_sha, "%s: record for a different cover" % f
            continue
        if "st" in d:
            b = tuple(F(v) for v in d["root"])
            assert d["st"]["UNCERT"] == 0 and not d["unc"], "%s: root %s not certified" % (f, d["root"])
            assert b not in subs, "duplicate zm_mixed root"
            subs[b] = f
for r in failing:
    inside = [b for b in subs if r[0] <= b[0] and b[1] <= r[1] and r[2] <= b[2] and b[3] <= r[3] and r[4] <= b[4] and b[5] <= r[5]]
    assert sum(vol(b) for b in inside) == vol(r), "zmx2 root %s not tiled by certified zm_mixed roots" % (r,)
    assert all(b[1] - b[0] == F(1, 20) and b[3] - b[2] == F(1, 20) and b[5] - b[4] == F(1, 32) for b in inside)
print("zm_mixed: %d certified roots tile the %d remaining zmx2 roots exactly" % (len(subs), len(failing)))
print("OK: the D4 fundamental region is certified (zmx2 or zm_mixed on every cell)")
