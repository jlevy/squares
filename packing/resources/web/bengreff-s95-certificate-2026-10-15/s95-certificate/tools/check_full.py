#!/usr/bin/env python3
"""Check that zm_mixed alone certifies the whole D4 fundamental region [0, K/2]^2 x {u in [0, 1/2]} (side K from the K argument, default 9).
Standard library only.

* FULL_JSONL is the record file of one zm_mixed run over the whole region (no --cx-lo etc.);
* each RERUN_JSONL is the record file of a run on single roots, at a greater depth;
* every header names the cover (sha256), the pinned checker files, cert mode and the D4 mode;
* the 10K x 10K x 16 roots of 1/20 x 1/20 x 1/32 each have a record, and each root is certified
  (UNCERT 0 and an empty `unc` list) in FULL_JSONL or in a rerun.

usage: [K=10] python3 check_full.py COVER_SHA256 FULL_JSONL [RERUN_JSONL ...]
"""
import sys, os, json, gzip
from fractions import Fraction as F

PINNED = {
    "zm_mixed.py": "ee3e2915349b8795128417bca6414b205d526db9f01f88cd4cd32c32e8d760ac",
    "mixed_cover.py": "bb89de15ecf5821dd7e1a36ebab8a50d792a406b7fb0f5cb38059f99ef74aae5",
    "zeromargin.py": "640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab",
}
cover_sha, full, reruns = sys.argv[1], sys.argv[2], sys.argv[3:]
K = int(os.environ.get("K", "9")); nr = 10 * K
expect = {(F(i, 20), F(i + 1, 20), F(j, 20), F(j + 1, 20), F(k, 32), F(k + 1, 32))
          for i in range(nr) for j in range(nr) for k in range(16)}


def read(path, whole):
    seen, ok, heads = set(), set(), 0
    for ln in (gzip.open if path.endswith(".gz") else open)(path, "rt"):
        d = json.loads(ln)
        if d.get("kind") == "zm_mixed cert header":
            heads += 1
            sh, st = d["sha256"], d["settings"]
            assert sh["input"] == cover_sha, "%s: record for a different cover" % path
            assert all(sh[k] == v for k, v in PINNED.items()), "%s: checker files differ from the pins" % path
            assert st["cert_mode"] and st["mode"] == "D4" and st["pitch"] == "1/20" and st["ubins"] == 16, path
            if whole:
                assert all(v is None for v in st["region"].values()), "%s: not a run over the whole region" % path
            print("%s: header depth %d, region %s" % (path, st["depth"], "whole" if whole else st["region"]))
            continue
        if "st" in d:
            b = tuple(F(v) for v in d["root"])
            assert b in expect, "%s: root %s is not a 1/20 x 1/20 x 1/32 cell of the region" % (path, d["root"])
            seen.add(b)
            if d["st"]["UNCERT"] == 0 and not d["unc"]:
                ok.add(b)
    assert heads >= 1, "%s: no header" % path
    return seen, ok


seen, ok = read(full, True)
assert seen == expect, "full run is missing %d roots" % len(expect - seen)
left = expect - ok
print("full run: %d roots, %d certified, %d with uncertified boxes" % (len(seen), len(ok), len(left)))
for r in reruns:
    s2, ok2 = read(r, False)
    print("%s: %d roots, %d certified" % (r, len(s2), len(ok2)))
    left -= ok2
assert not left, "roots not certified by any run: %s" % sorted(left)
print("OK: zm_mixed certifies every root of the D4 fundamental region")
