#!/usr/bin/env python3
"""Sharp and gross controls on #895's certificate, every one decided in full by both methods.

Sharp controls take the certificate to exact contact and 1e-30 past it at its tightest
walls and pairs; each mutated certificate is decided over every wall and all 33,670
pairs by certcheck.py's method A (separating axes) and method B (exact clipped areas).

- far walls: the side lowered by the least far-wall clearance (0, the right wall), then
  by 1e-30 more;
- left and bottom walls: every square moved toward that wall by the least clearance
  there, then by 1e-30 more;
- the top wall: the square nearest it raised by its clearance, then by 1e-30 more;
- the tightest pair, the tightest pair with a tilted square, and the tightest pair of
  two tilted squares: the second square of the pair translated along the edge normal
  that attains the pair's gap, by the exact distance at which the largest gap over the
  pair's four normals reaches 0 (computed per normal as an interval of the motion), then
  1e-30 further.

Gross controls: a duplicated square, a square outside the box, and the side lowered by
1e-10. (The reversed rotation sense is certcheck.py --sense cw.)

Usage: python -I controls.py CERT --out RECEIPT.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import certcheck as cc  # noqa: E402

EPS = F(1, 10**30)
TAN_HALF_DEGREE = F(87266, 10**7)


def clone(cert, side=None, changes=None, shift=None):
    squares = []
    for i, s in enumerate(cert["squares"]):
        x, y, t = s["x"], s["y"], s["t"]
        if shift is not None:
            x, y = x + shift[0], y + shift[1]
        if changes and i in changes:
            x, y, t = changes[i]
        squares.append({"row": i + 1, "line": i + 3, "x": x, "y": y, "t": t, "tokens": []})
    return {"n": cert["n"], "side": cert["side"] if side is None else side, "squares": squares}


def contact_motion(cert, i, j):
    """Exact distance to move square j along the gap-attaining normal of pair (i, j) to contact."""
    P = cc.poses(cert, "ccw")
    pi, pj = P[i], P[j]
    axes = (pi["u"], pi["v"], pj["u"], pj["v"])
    best, axis, sign = None, None, None
    stats = []
    for a in axes:
        proj_i = [a[0] * p[0] + a[1] * p[1] for p in pi["P"]]
        proj_j = [a[0] * p[0] + a[1] * p[1] for p in pj["P"]]
        half = (max(proj_i) - min(proj_i)) / 2 + (max(proj_j) - min(proj_j)) / 2
        centre_gap = a[0] * (pj["x"] - pi["x"]) + a[1] * (pj["y"] - pi["y"])
        stats.append((a, half, centre_gap))
        g1, g2 = min(proj_j) - max(proj_i), min(proj_i) - max(proj_j)
        g, s = (g1, 1) if g1 >= g2 else (g2, -1)
        if best is None or g > best:
            best, axis, sign = g, a, s
    # move j by -lam * sign * axis; on each normal a the centre gap becomes c - lam*sign*(a.axis)
    lo, hi = F(0), None
    for a, half, c in stats:
        k = sign * (a[0] * axis[0] + a[1] * axis[1])
        if k == 0:
            if abs(c) >= half:
                return None  # this normal separates for every lam: no contact along this motion
            continue
        # g_a(lam) <= 0  <=>  -half <= c - lam*k <= half  <=>  lam in [(c-half)/k, (c+half)/k] (k>0)
        ends = sorted(((c - half) / k, (c + half) / k))
        lo = max(lo, ends[0])
        hi = ends[1] if hi is None else min(hi, ends[1])
    if hi is not None and lo >= hi:
        return None
    return {"gap": best, "axis": axis, "sign": sign, "lam": lo, "hi": hi}


def moved(cert, j, motion, extra):
    lam = motion["lam"] + extra
    s = cert["squares"][j]
    ax, sg = motion["axis"], motion["sign"]
    return clone(cert, changes={j: (s["x"] - lam * sg * ax[0], s["y"] - lam * sg * ax[1], s["t"])})


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    t0 = time.time()
    C = cc.parse_cert(args.cert)
    base = cc.decide(C, "ccw", "A")
    gaps, walls = base["_gaps"], base["_walls"]
    n = C["n"]
    tilted = {i for i, s in enumerate(C["squares"])
              if abs(s["t"]) > TAN_HALF_DEGREE and abs(s["t"] - 1) > TAN_HALF_DEGREE and abs(s["t"] + 1) > TAN_HALF_DEGREE}
    controls = []

    def run(name, cert, expect, detail):
        res = cc.decide(cert, "ccw", "AB")
        ok = (res["accepted_by_A"] == expect) and (res["accepted_by_B"] == expect)
        rec = {"control": name, "expected": "accept" if expect else "refuse",
               "A": res["accepted_by_A"], "B": res["accepted_by_B"],
               "methods_agree_on_pairs": res["methods_agree_on_pairs"],
               "methods_agree_on_walls": res["methods_agree_on_walls"],
               "A_overlapping_pairs": res["A"]["overlapping_pair_count"],
               "A_wall_failures": res["A"]["wall_failure_count"],
               "B_overlapping_pairs": res["B"]["overlapping_pair_count"],
               "B_wall_failures": res["B"]["wall_failure_count"],
               "least_pair_gap": res["A"]["least_pairs"][0]["gap_float"],
               "least_walls": {k: v["least_float"] for k, v in res["A"]["walls"].items()},
               "as_expected": ok, "detail": detail,
               "cpu_seconds": round(res["A"]["cpu_seconds"] + res["B"]["cpu_seconds"], 3)}
        controls.append(rec)
        print(("ok  " if ok else "FAIL"), name, "A", rec["A"], "B", rec["B"], "pairs A/B",
              rec["A_overlapping_pairs"], rec["B_overlapping_pairs"], "walls A/B", rec["A_wall_failures"],
              rec["B_wall_failures"], "cpu", rec["cpu_seconds"])

    # far walls: least far-wall clearance
    far = min(min(w[1] for w in walls), min(w[3] for w in walls))
    run("side lowered by the least far-wall clearance", clone(C, side=C["side"] - far), True,
        {"least_far_clearance": str(far)})
    run("side lowered 1e-30 past it", clone(C, side=C["side"] - far - EPS), False, {})
    # near walls
    for name, w, vec in (("left", 0, (-1, 0)), ("bottom", 2, (0, -1))):
        m = min(ws[w] for ws in walls)
        at = [i + 1 for i in range(n) if walls[i][w] == m]
        run(f"every square moved to the {name} wall by its least clearance",
            clone(C, shift=(vec[0] * m, vec[1] * m)), True, {"clearance": str(m), "float": float(m), "rows": at})
        run(f"every square moved to the {name} wall, 1e-30 past", clone(C, shift=(vec[0] * (m + EPS), vec[1] * (m + EPS))),
            False, {})
    # the top wall's nearest square raised to it
    top = min(range(n), key=lambda i: walls[i][3])
    m = walls[top][3]
    s = C["squares"][top]
    run("the square nearest the top wall raised by its clearance", clone(C, changes={top: (s["x"], s["y"] + m, s["t"])}),
        True, {"row": top + 1, "clearance": float(m)})
    run("the square nearest the top wall raised 1e-30 past", clone(C, changes={top: (s["x"], s["y"] + m + EPS, s["t"])}),
        False, {"row": top + 1})
    # tightest pairs
    order = sorted(gaps, key=lambda k: gaps[k])
    picks = [("tightest pair", order[0])]
    picks.append(("tightest pair of two tilted squares", next(k for k in order if k[0] in tilted and k[1] in tilted)))
    picks.append(("tightest pair of a tilted and a near-upright square",
                  next(k for k in order if (k[0] in tilted) != (k[1] in tilted))))
    for label, (i, j) in picks:
        mo = contact_motion(C, i, j)
        if mo is None:
            controls.append({"control": label, "rows": [i + 1, j + 1], "skipped": "no contact along the motion"})
            continue
        detail = {"rows": [i + 1, j + 1], "gap": str(mo["gap"]), "gap_float": float(mo["gap"]),
                  "motion": str(mo["lam"]), "motion_float": float(mo["lam"]),
                  "i_tilted": i in tilted, "j_tilted": j in tilted}
        run(f"{label} closed to contact", moved(C, j, mo, F(0)), True, detail)
        run(f"{label} 1e-30 past contact", moved(C, j, mo, EPS), False, {"rows": [i + 1, j + 1]})
    # gross controls
    s0 = C["squares"][0]
    run("duplicated square (row 2 := row 1)", clone(C, changes={1: (s0["x"], s0["y"], s0["t"])}), False, {})
    run("square outside the box (row 1 at x = -1)", clone(C, changes={0: (F(-1), s0["y"], s0["t"])}), False, {})
    run("side lowered by 1e-10", clone(C, side=C["side"] - F(1, 10**10)), False, {})
    usage = resource.getrusage(resource.RUSAGE_SELF)
    out = {"program": "controls.py", "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           "certcheck_sha256": cc.program_digest(), "python": platform.python_version(),
           "input": {"path": args.cert, "sha256": C["sha256"]},
           "tilted_definition": "|t|, |t - 1|, |t + 1| all above 0.0087266 (about 1 degree from upright)",
           "controls": controls,
           "all_as_expected": all(c.get("as_expected", False) for c in controls),
           "cpu_seconds_total": round(usage.ru_utime + usage.ru_stime, 3),
           "wall_seconds": round(time.time() - t0, 3)}
    Path(args.out).write_text(json.dumps(out, indent=1, default=str) + "\n")
    print("all as expected:", out["all_as_expected"], "cpu", out["cpu_seconds_total"])
    return 0 if out["all_as_expected"] else 1


if __name__ == "__main__":
    sys.exit(main())
