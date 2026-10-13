"""Independent cross-check of sqverify's numbers with mpmath (brute-force SAT on 8 vertices).

    uv run python -I tools/crosscheck_mpmath.py --json runs/verify/records.json [--dps 80] files...

For each .sqpk it recomputes, at `dps` decimal digits, the containment slack (min over vertices
of min(x, y, s-x, s-y)), the bounding side, and the minimum SAT separation over every pair
whose centres are closer than sqrt(2) (projection of all 8 vertices on the 4 edge normals; this
is deliberately a different formulation from the closed form used in verify/). Each file gets its
own verdict, at the tolerance of sqverify's precise check (TOL = 1e-14): "separated" if every vertex
is inside the box and every pair is strictly apart (slack >= 0, min sep > 0), "contacts" if nothing
overlaps or leaves the box by more than TOL (exact contacts written as decimals evaluate to about
-1e-30, rounded published coordinates to about -1e-15; the exact certificate settles them), and
"INVALID" otherwise. Files are listed when invalid, or all with --list; the exit status is 1 if any
file is invalid. With --json it also
compares min sep and containment slack with sqverify's JSON and reports the largest disagreement.
"""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import mpmath

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sqpk import read_sqpk

DPS = 80
TOL = mpmath.mpf("1e-14")  # sqverify --precise tolerance


def check(path: str) -> dict:
    mpmath.mp.dps = DPS
    p = read_sqpk(Path(path))
    s = mpmath.mpf(p.s)
    sq = []
    for cx, cy, th in p.squares:
        x, y = mpmath.mpf(cx), mpmath.mpf(cy)
        t = mpmath.mpf(th) * mpmath.pi / 180
        c, si = mpmath.cos(t), mpmath.sin(t)
        h = mpmath.mpf(1) / 2
        verts = [(x + a * c - b * si, y + a * si + b * c) for a in (-h, h) for b in (-h, h)]
        sq.append((x, y, (c, si), (-si, c), verts))
    slack = min(min(vx, vy, s - vx, s - vy) for q in sq for vx, vy in q[4])
    xs = [v[0] for q in sq for v in q[4]]
    ys = [v[1] for q in sq for v in q[4]]
    bound = max(max(xs) - min(xs), max(ys) - min(ys))
    # broad phase by float centres (margin generous); exact decision below in mpmath
    fl = [(float(q[0]), float(q[1])) for q in sq]
    cell = {}
    for i, (x, y) in enumerate(fl):
        cell.setdefault((int(x // 1.5), int(y // 1.5)), []).append(i)
    min_sep = None
    pair = None
    for i, (x, y) in enumerate(fl):
        gx, gy = int(x // 1.5), int(y // 1.5)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in cell.get((gx + dx, gy + dy), []):
                    if j <= i:
                        continue
                    a, b = sq[i], sq[j]
                    if (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 >= 2:
                        continue
                    best = None
                    for ax in (a[2], a[3], b[2], b[3]):
                        pa = [vx * ax[0] + vy * ax[1] for vx, vy in a[4]]
                        pb = [vx * ax[0] + vy * ax[1] for vx, vy in b[4]]
                        gap = max(min(pb) - max(pa), min(pa) - max(pb))
                        best = gap if best is None or gap > best else best
                    if min_sep is None or best < min_sep:
                        min_sep, pair = best, (i, j)
    return {
        "path": str(Path(path).resolve()),
        "n": p.n,
        "slack": mpmath.nstr(slack, 25),
        "bounding_s": mpmath.nstr(bound, 40),
        "min_sep": mpmath.nstr(min_sep, 25) if min_sep is not None else None,
        "pair": pair,
    }


def main() -> None:
    global DPS
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="sqverify JSON to compare against")
    ap.add_argument("--dps", type=int, default=DPS)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--out", help="write per-file results as JSON")
    ap.add_argument("--list", action="store_true", help="print every file's verdict, not only invalid ones")
    ap.add_argument("files", nargs="+")
    a = ap.parse_args()
    DPS = a.dps
    with ProcessPoolExecutor(max_workers=a.jobs) as ex:
        res = list(ex.map(check, a.files, chunksize=2))
    ref = {}
    if a.json:
        ref = {str(Path(f["path"]).resolve()): f for f in json.loads(Path(a.json).read_text())["files"]}
    worst = (0.0, None)
    worst_slack = (0.0, None)
    for r in res:
        f = ref.get(r["path"])
        if not f or r["min_sep"] is None or f.get("min_sep") in (None, ""):
            continue
        d = abs(mpmath.mpf(r["min_sep"]) - mpmath.mpf(f["min_sep"]))
        if d > worst[0]:
            worst = (float(d), r["path"])
        ds = abs(mpmath.mpf(r["slack"]) - mpmath.mpf(f["containment_slack"]))
        if ds > worst_slack[0]:
            worst_slack = (float(ds), r["path"])
    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=1))
    print(f"crosscheck: {len(res)} files at {DPS} digits")
    counts = {"separated": 0, "contacts": 0, "INVALID": 0}
    for r in res:
        sl = mpmath.mpf(r["slack"])
        ms = mpmath.mpf(r["min_sep"]) if r["min_sep"] is not None else mpmath.inf
        v = "separated" if sl >= 0 and ms > 0 else "contacts" if sl >= -TOL and ms >= -TOL else "INVALID"
        counts[v] += 1
        if a.list or v == "INVALID":
            print(f"  {r['path']}  n={r['n']} slack={r['slack']} min_sep={r['min_sep']} pair={r['pair']} {v}")
    if ref:
        print(f"max |min_sep(mpmath) - min_sep(sqverify)| = {worst[0]:.3e}  ({worst[1]})")
        print(f"max |slack(mpmath) - slack(sqverify)|     = {worst_slack[0]:.3e}  ({worst_slack[1]})")
    print(f"summary: valid={counts['separated'] + counts['contacts']} (separated {counts['separated']}, "
          f"contacts within {mpmath.nstr(TOL, 1)} {counts['contacts']}) invalid={counts['INVALID']}")
    if counts["INVALID"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
