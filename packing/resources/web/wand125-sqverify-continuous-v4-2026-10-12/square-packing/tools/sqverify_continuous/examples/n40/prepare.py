#!/usr/bin/env python3
"""Fetch the two n = 40 densities and write sqverify-fast candidates (format T), with controls.

    python3 prepare.py OUT_DIR

Downloads, at fixed commits of Guzhou0806/n40-square-packing, the files below, checks
their SHA-256, and writes OUT_DIR/{c6715,c6718}.json and the controls
OUT_DIR/{c6715,c6718}_mass0985.json (every weight times 985/1000).

  c6715: certificate/certified_candidate.json at 71c97d0 (the rect_n40_L67 density,
         480 positive orbits); claim s(40) > 1340000/199529 with B = 199529/200000.
  c6718: certificate/certified_candidate.json at 6a65957e (685 orbits: 522 from the
         original pool, 163 new); claim s(40) > 3359/500 with B = 3350/3359.

All arithmetic is exact (fractions). Standard library only.
"""
import hashlib
import json
import sys
import urllib.request
from fractions import Fraction as F
from pathlib import Path

RAW = "https://raw.githubusercontent.com/Guzhou0806/n40-square-packing/{commit}/{path}"
SOURCES = {
    "c6715": ("71c97d0", "71011d0356dd179c6e7e6e02c9a064ff30f6f13844016ce3b97463bf7ef53dc0"),
    "c6718": ("6a65957e6c5c51cdf267917d882dab7f5b4928dd",
              "984fcd3acc605fe3c50a84912eed77e0192ca5b7253b19b6aa31a4e28e1bf5c2"),
}
ORIGINAL_SHA = "71011d0356dd179c6e7e6e02c9a064ff30f6f13844016ce3b97463bf7ef53dc0"
L = F(67, 10)
M = F(3999, 100)


def fetch(commit, path, sha):
    data = urllib.request.urlopen(RAW.format(commit=commit, path=path), timeout=60).read()
    got = hashlib.sha256(data).hexdigest()
    if got != sha:
        raise SystemExit(f"{path}@{commit}: sha256 {got}, expected {sha}")
    return data


def orbit(a, b, c, e):
    out = set()
    for x0, y0, x1, y1 in ((a, b, c, e), (b, a, e, c)):
        for fx in (0, 1):
            for fy in (0, 1):
                xa, xb = (L - x1, L - x0) if fx else (x0, x1)
                ya, yb = (L - y1, L - y0) if fy else (y0, y1)
                out.add((xa, ya, xb, yb))
    return frozenset(out)


def write(out, name, core, rects, weights):
    total = sum(weights, F(0))
    assert total == M, (name, total)
    for a, b, c, e in rects:
        assert 0 <= a < c <= L and 0 <= b < e <= L
    assert all(w > 0 for w in weights)
    for label, f in ((name, F(1)), (name + "_mass0985", F(985, 1000))):
        doc = {"n": 40, "L": str(L), "B": str(core), "mass": str(total * f),
               "rectangles": [[str(v) for v in r] for r in rects],
               "weights": [str(w * f) for w in weights]}
        (out / f"{label}.json").write_text(json.dumps(doc))
    print(f"{name}: {len(rects)} orbits, mass {total}, B = {core}, X = L/B = {L / core}, "
          f"40 tau - M = {40 * F(4999, 5000) - total}")


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    path = "certificate/certified_candidate.json"
    commit, sha = SOURCES["c6715"]
    d = json.loads(fetch(commit, path, sha), parse_float=F)
    rects = [tuple(F(v) for v in r) for r, w in zip(d["rectangles"], d["weights"]) if F(w) > 0]
    weights = [F(w) for w in d["weights"] if F(w) > 0]
    write(out, "c6715", F(199529, 200000), rects, weights)

    commit, sha = SOURCES["c6718"]
    d = json.loads(fetch(commit, path, sha), parse_float=F)
    original = json.loads(fetch(commit, "certificate/original_density.json", ORIGINAL_SHA), parse_float=F)
    pool = [tuple(F(v) for v in r) for r in original["rectangles"]]
    pool_orbits = {orbit(*r) for r in pool}
    seen, used = set(), set()
    rects, weights, kinds = [], [], {"inherited": 0, "generated": 0}
    for s in d["sites"]:
        box = tuple(F(v) for v in s["box"])
        o = orbit(*box)
        assert o not in seen, "duplicate orbit"
        seen.add(o)
        kinds[s["kind"]] += 1
        if s["kind"] == "inherited":
            assert s["source_index"] not in used and pool[s["source_index"]] == box
            used.add(s["source_index"])
        else:
            assert o not in pool_orbits
        rects.append(box)
        weights.append(F(s["weight"]))
    print(f"c6718 sites: {kinds}")
    write(out, "c6718", F(3350, 3359), rects, weights)


if __name__ == "__main__":
    main()
