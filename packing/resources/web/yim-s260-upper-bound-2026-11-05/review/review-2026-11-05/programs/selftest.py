#!/usr/bin/env python3
"""Self-test of certcheck.py's two methods on configurations whose answers are known by hand.

Each case is decided by method A (separating axes) and method B (exact clipped areas);
the test fails unless both give the expected verdict. A randomized part then builds
pairs at exact contact (by the separating-axis gap, moved along the axis that attains
it until the largest gap is exactly 0) and 1e-30 to either side of it, and requires the
two methods to agree on every one; it also checks that every square's shoelace area is
exactly 1 and that the reversed sense reflects each square about its centre's
horizontal line.

Usage: python -I selftest.py --out RECEIPT.json [--random 400] [--seed 895]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import random
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import certcheck as cc  # noqa: E402

EPS = F(1, 10**30)


def square(x, y, t, sense="ccw"):
    u, v = cc.frame(F(t), sense)
    return {"x": F(x), "y": F(y), "u": u, "v": v, "P": cc.corners(F(x), F(y), u, v)}


def pair_verdicts(a, b):
    gap = cc.sat_gap(a["P"], (a["u"], a["v"]), b["P"], (b["u"], b["v"]))
    ar = cc.clipped_area(b["P"], a["P"])
    ar2 = cc.clipped_area(a["P"], b["P"])
    if ar != ar2:
        raise AssertionError("clipped area not symmetric")
    return gap >= 0, ar == 0, gap, ar


def wall_verdicts(sq, side):
    side = F(side)
    cl = cc.wall_clearances(sq["P"], side)
    container = [(F(0), F(0)), (side, F(0)), (side, side), (F(0), side)]
    inside = cc.clipped_area(sq["P"], container)
    return min(cl) >= 0, inside == 1, min(cl), inside


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--random", type=int, default=400)
    ap.add_argument("--seed", type=int, default=895)
    args = ap.parse_args(argv)
    t0 = time.time()
    cases = []

    def expect_pair(name, a, b, accept):
        va, vb, gap, ar = pair_verdicts(a, b)
        ok = va == accept and vb == accept
        cases.append({"case": name, "expected": "accept" if accept else "refuse", "A": va, "B": vb,
                      "gap": str(gap), "area": str(ar), "ok": ok})

    def expect_wall(name, sq, side, accept):
        va, vb, least, inside = wall_verdicts(sq, side)
        ok = va == accept and vb == accept
        cases.append({"case": name, "expected": "accept" if accept else "refuse", "A": va, "B": vb,
                      "least_clearance": str(least), "inside_area": str(inside), "ok": ok})

    # upright pairs
    o = square(0, 0, 0)
    expect_pair("upright side by side at exact contact", o, square(1, 0, 0), True)
    expect_pair("upright side by side 1e-30 past contact", o, square(1 - EPS, 0, 0), False)
    expect_pair("upright side by side 1e-30 short of contact", o, square(1 + EPS, 0, 0), True)
    expect_pair("upright corner to corner at contact", o, square(1, 1, 0), True)
    expect_pair("upright corner to corner 1e-30 past", o, square(1 - EPS, 1 - EPS, 0), False)
    expect_pair("t=1 is upright: side by side at contact", o, square(1, 0, 1), True)
    expect_pair("t=1 is upright: 1e-30 past", o, square(1 - EPS, 0, 1), False)
    expect_pair("duplicate square", o, square(0, 0, 0), False)
    expect_pair("duplicate square, t=1 against t=0", o, square(0, 0, 1), False)
    # t = 1/2: c = 3/5, s = 4/5, half extent 7/10
    expect_pair("corner of tilted square on upright edge", o, square(0, F(6, 5), F(1, 2)), True)
    expect_pair("corner of tilted square 1e-30 into upright edge", o, square(0, F(6, 5) - EPS, F(1, 2)), False)
    # only the tilted square's own normal separates: upright corner (1/2,1/2) on its edge
    expect_pair("upright corner on tilted edge (axis of the second square)", o, square(F(4, 5), F(9, 10), F(1, 2)), True)
    expect_pair("upright corner 1e-30 into tilted edge", o,
                square(F(4, 5) - F(3, 5) * EPS, F(9, 10) - F(4, 5) * EPS, F(1, 2)), False)
    # equal tilt, face to face along u = (3/5, 4/5)
    expect_pair("equal tilt face to face at contact", square(0, 0, F(1, 2)), square(F(3, 5), F(4, 5), F(1, 2)), True)
    expect_pair("equal tilt face to face 1e-30 past", square(0, 0, F(1, 2)),
                square(F(3, 5) - F(3, 5) * EPS, F(4, 5) - F(4, 5) * EPS, F(1, 2)), False)
    # a tiny negative turn like the certificate's near-upright squares
    tiny = F(-1, 850217033674)
    a = square(0, 0, tiny)
    # place a second square of the same tiny turn face to face along its own u
    b_u = a["u"]
    expect_pair("tiny equal turn face to face at contact", a, square(b_u[0], b_u[1], tiny), True)
    expect_pair("tiny equal turn face to face 1e-30 past", a,
                square(b_u[0] * (1 - EPS), b_u[1] * (1 - EPS), tiny), False)
    # walls
    expect_wall("upright square touching all walls of side 1", square(F(1, 2), F(1, 2), 0), 1, True)
    expect_wall("upright square in side 1 - 1e-30", square(F(1, 2), F(1, 2), 0), 1 - EPS, False)
    expect_wall("tilted square touching all walls of side 7/5", square(F(7, 10), F(7, 10), F(1, 2)), F(7, 5), True)
    expect_wall("tilted square in side 7/5 - 1e-30", square(F(7, 10), F(7, 10), F(1, 2)), F(7, 5) - EPS, False)
    expect_wall("tilted square 1e-30 past the left wall", square(F(7, 10) - EPS, F(7, 10), F(1, 2)), F(7, 5) + 1, False)
    expect_wall("square far outside", square(-5, F(1, 2), 0), 10, False)

    # reversed sense is the reflection about the centre's horizontal line
    reflect_ok = True
    for t in (F(1, 2), F(-1, 3), F(2, 7), F(-1, 850217033674), F(5, 11)):
        ccw = square(F(3, 2), F(5, 2), t, "ccw")["P"]
        cw = square(F(3, 2), F(5, 2), t, "cw")["P"]
        mirrored = {(p[0], 2 * F(5, 2) - p[1]) for p in ccw}
        reflect_ok &= mirrored == set(cw)

    # randomized agreement at exact contact and 1e-30 either side
    rng = random.Random(args.seed)
    tangents = [F(0), F(1), F(-1), F(1, 2), F(-1, 3), F(2, 7), F(-5, 11), F(-1, 850217033674),
                F(89582500535, 412421283321), F(216934655428, 998727077879), F(3729384701, 997374846231)]
    disagreements = 0
    unexpected = 0
    trials = 0
    areas_bad = 0
    contact_built = 0
    for _ in range(args.random):
        ti, tj = rng.choice(tangents), rng.choice(tangents)
        a = square(0, 0, ti)
        # random direction with a small rational slope, start far apart, then slide in
        dx = F(rng.randint(-40, 40), rng.randint(1, 40))
        dy = F(rng.randint(-40, 40), rng.randint(1, 40))
        if dx == 0 and dy == 0:
            dx = F(1)
        scale = F(3) / (abs(dx) + abs(dy))
        bx, by = dx * scale, dy * scale
        b = square(bx, by, tj)
        for sq in (a, b):
            areas_bad += cc.area(sq["P"]) != 1
        # move b toward a along the axis that attains the largest gap, by the gap, until the gap is 0
        for _step in range(12):
            axes = (a["u"], a["v"], b["u"], b["v"])
            best, axis = None, None
            for ax in axes:
                pa = [ax[0] * p[0] + ax[1] * p[1] for p in a["P"]]
                pb = [ax[0] * p[0] + ax[1] * p[1] for p in b["P"]]
                g1, g2 = min(pb) - max(pa), min(pa) - max(pb)
                g, sign = (g1, 1) if g1 >= g2 else (g2, -1)
                if best is None or g > best:
                    best, axis, direction = g, ax, sign
            if best <= 0:
                break
            bx -= direction * axis[0] * best
            by -= direction * axis[1] * best
            b = square(bx, by, tj)
        gap = cc.sat_gap(a["P"], (a["u"], a["v"]), b["P"], (b["u"], b["v"]))
        if gap != 0:
            continue
        contact_built += 1
        # probe along the centre line: exact contact, then 1e-30 nearer and farther
        norm = abs(bx) + abs(by)
        for shift, expected in ((F(0), True), (EPS, False), (-EPS, True)):
            sx = bx - bx / norm * shift
            sy = by - by / norm * shift
            va, vb, _g, _ar = pair_verdicts(a, square(sx, sy, tj))
            trials += 1
            disagreements += va != vb
            unexpected += (va != expected) or (vb != expected)
    ok_cases = all(c["ok"] for c in cases)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    receipt = {
        "program": "selftest.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "certcheck_sha256": cc.program_digest(),
        "python": platform.python_version(),
        "hand_cases": cases,
        "hand_cases_all_as_expected": ok_cases,
        "reversed_sense_is_reflection": reflect_ok,
        "random": {"seed": args.seed, "draws": args.random, "contacts_built": contact_built,
                   "probes": trials, "disagreements": disagreements,
                   "unexpected_verdicts": unexpected, "square_area_not_one": areas_bad},
        "passed": ok_cases and reflect_ok and disagreements == 0 and unexpected == 0 and areas_bad == 0
        and contact_built > 0,
        "cpu_seconds_total": round(usage.ru_utime + usage.ru_stime, 3),
        "wall_seconds": round(time.time() - t0, 3),
    }
    Path(args.out).write_text(json.dumps(receipt, indent=1) + "\n")
    for c in cases:
        print(("ok  " if c["ok"] else "FAIL"), c["case"], c["A"], c["B"])
    print("reflection", reflect_ok, "random", receipt["random"], "passed", receipt["passed"],
          "cpu", receipt["cpu_seconds_total"])
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
