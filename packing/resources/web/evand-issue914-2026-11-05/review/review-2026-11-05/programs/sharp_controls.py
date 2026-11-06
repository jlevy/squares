"""Sharp and gross controls for one certificate, each decided by method A and method B.

Usage (from packing/, Python 3.14):
  python -I sharp_controls.py CERT OUT.json [--label NAME]

Every control states its expected verdict from its construction before either method
decides it; a control passes when both methods return the expected verdict.

Full-packing controls (pairs are unchanged by construction; every wall is decided):
  C1  the box at its extent (side = the largest corner coordinate): accept;
      and 1e-30 below it: refuse.
  C2  the packing translated so the least corner coordinates are exactly 0: accept;
      then 1e-30 further left, and separately 1e-30 further down: refuse.
Constraint-level controls at the tightest pair and the tightest wall:
  C3  the least-gap pair (i, j), gap g along unit axis a: j moved by g toward i along a,
      exact contact: accept; moved by g + 1e-30: refuse (expected because every axis of
      the pair not parallel to a keeps a gap below -2(g + 1e-30), checked from the
      construction and recorded; parallel axes carry the same gap as a). A second
      version left this expectation unstated where two axes were parallel; that run is
      kept in out/controls-v2-parallel-axes/. The moved square's other walls and pairs are then
      decided too and reported, as information.
  C4  the least-clearance square k, clearance w to wall W: k moved by w toward W:
      accept; by w + 1e-30: refuse (its four walls decided).
  C5  square i of the least-gap pair enlarged about its centre by delta*, the least
      enlargement that closes the pair (max over the pair's axes of gap_b / width_b):
      accept; by delta* + 1e-30: refuse.
Gross controls:
  G1  the last square replaced by a copy of the first (duplicate): refuse.
  G2  the first square centred at x = -1 (outside the box): refuse. (A first version
      moved square 1 left by 1, which leaves it inside wherever it sits more than about
      1.71 from the left wall; both methods accepted it there, correctly, and the control
      was redefined; that run is kept in out/controls-v1-g2-misconstructed/.)
  G3  every square turned to t = 0 (axis-aligned) in place: decided, verdict recorded
      (no expectation).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import exact_geometry as eg  # noqa: E402
from cert_reader import read_cert  # noqa: E402

E30 = F(1, 10**30)
H = F(1, 2)


def walls_both(squares, side, hs=None):
    """Decide every wall by A and B; return (verdict_a, verdict_b, outside_a, outside_b)."""
    hs = hs or [H] * len(squares)
    out_a = [k + 1 for k, (q, h) in enumerate(zip(squares, hs)) if eg.wall_clearance_a(eg.square_a(*q, h=h), side) < 0]
    out_b = [k + 1 for k, (q, h) in enumerate(zip(squares, hs)) if eg.wall_deficit_b(eg.square_b(*q, h=h), side) != 0]
    return ("accept" if not out_a else "refuse"), ("accept" if not out_b else "refuse"), out_a, out_b


def pair_both(qi, qj, hi=H, hj=H):
    g, k = eg.pair_gap_a(eg.square_a(*qi, h=hi), eg.square_a(*qj, h=hj))
    a = eg.pair_area_b(eg.square_b(*qi, h=hi), eg.square_b(*qj, h=hj))
    return ("accept" if g >= 0 else "refuse"), ("accept" if a == 0 else "refuse"), g, a


def one_square_all(squares, k, side, hk=H):
    """Decide square k's walls and all its pairs by both methods (information)."""
    qk = squares[k]
    wa = eg.wall_clearance_a(eg.square_a(*qk, h=hk), side) >= 0
    wb = eg.wall_deficit_b(eg.square_b(*qk, h=hk), side) == 0
    bad_a, bad_b = [], []
    sa = eg.square_a(*qk, h=hk)
    sb = eg.square_b(*qk, h=hk)
    for m, q in enumerate(squares):
        if m == k:
            continue
        g, _ = eg.pair_gap_a(sa, eg.square_a(*q))
        if g < 0:
            bad_a.append(m + 1)
        if eg.pair_area_b(sb, eg.square_b(*q)) != 0:
            bad_b.append(m + 1)
    return {
        "walls_a": "inside" if wa else "outside",
        "walls_b": "inside" if wb else "outside",
        "overlapping_partners_a": bad_a,
        "overlapping_partners_b": bad_b,
        "verdict_a": "accept" if wa and not bad_a else "refuse",
        "verdict_b": "accept" if wb and not bad_b else "refuse",
    }


def rec(controls, name, expected, va, vb, **extra):
    ok = (va == expected and vb == expected) if expected else (va == vb)
    controls.append({"control": name, "expected": expected, "method_a": va, "method_b": vb, "pass": ok, **extra})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("out")
    ap.add_argument("--label", default="")
    args = ap.parse_args()
    t0 = time.process_time()
    c = read_cert(args.cert)
    n, side, sq = c["n"], c["S"], list(c["squares"])
    controls: list[dict] = []

    corners = [eg.square_a(*q)[0] for q in sq]
    xs = [p[0] for cs in corners for p in cs]
    ys = [p[1] for cs in corners for p in cs]
    top = max(max(xs), max(ys))
    xmin, ymin = min(xs), min(ys)

    # C1
    va, vb, _, _ = walls_both(sq, top)
    rec(controls, "C1 box at its extent", "accept", va, vb, side=f"{top.numerator}/{top.denominator}", side_minus_header=str(float(top - side)))
    va, vb, oa, ob = walls_both(sq, top - E30)
    rec(controls, "C1 box 1e-30 below its extent", "refuse", va, vb, outside_a=oa, outside_b=ob)
    # C2
    moved = [(x - xmin, y - ymin, t) for (x, y, t) in sq]
    va, vb, _, _ = walls_both(moved, side)
    rec(controls, "C2 packing at the near walls (translated by the least corner coordinates)", "accept", va, vb,
        translation=[str(float(-xmin)), str(float(-ymin))])
    va, vb, oa, ob = walls_both([(x - E30, y, t) for (x, y, t) in moved], side)
    rec(controls, "C2 then 1e-30 past the left wall", "refuse", va, vb, outside_a=oa, outside_b=ob)
    va, vb, oa, ob = walls_both([(x, y - E30, t) for (x, y, t) in moved], side)
    rec(controls, "C2 then 1e-30 past the bottom wall", "refuse", va, vb, outside_a=oa, outside_b=ob)

    # the least-gap pair, by method A over all pairs
    sa = [eg.square_a(*q) for q in sq]
    best = None
    for i in range(n):
        for j in range(i + 1, n):
            g, k = eg.pair_gap_a(sa[i], sa[j])
            if best is None or g < best[0]:
                best = (g, i, j, k)
    g, i, j, k = best
    ax, ay = (sa[i][1] + sa[j][1])[k]
    pi = [px * ax + py * ay for (px, py) in sa[i][0]]
    pj = [px * ax + py * ay for (px, py) in sa[j][0]]
    sign = 1 if (min(pj) - max(pi)) == g else -1  # j lies on the +sign side of i along a
    # the other axes' gaps before the move (construction check for the 'past' expectation)
    others = []
    for kk, (bx, by) in enumerate(sa[i][1] + sa[j][1]):
        if kk == k or ax * by - ay * bx == 0:
            continue  # the axis itself, or an axis parallel to it (same direction, same gap)
        qi_ = [px * bx + py * by for (px, py) in sa[i][0]]
        qj_ = [px * bx + py * by for (px, py) in sa[j][0]]
        others.append(max(min(qj_) - max(qi_), min(qi_) - max(qj_)))
    second = max(others) if others else None
    past_expected = "refuse" if second is not None and second < -2 * (g + E30) else None
    for extra, label, exp in ((F(0), "exact contact", "accept"), (E30, "1e-30 past", past_expected)):
        m = g + extra
        qj = (sq[j][0] - sign * m * ax, sq[j][1] - sign * m * ay, sq[j][2])
        va, vb, g2, a2 = pair_both(sq[i], qj)
        moved_sq = list(sq)
        moved_sq[j] = qj
        info = one_square_all(moved_sq, j, side)
        rec(controls, f"C3 least-gap pair ({i + 1}, {j + 1}) closed along its axis, {label}", exp, va, vb,
            gap_before=str(float(g)), gap_after=str(float(g2)), area_after=str(float(a2)),
            second_axis_gap_before=(str(float(second)) if second is not None else "all axes parallel"), moved_square_full_decision=info)

    # the least-clearance wall
    best_w = None
    for kq, s in enumerate(sa):
        for (px, py) in s[0]:
            for wall, v in (("left", px), ("right", side - px), ("bottom", py), ("top", side - py)):
                if best_w is None or v < best_w[0]:
                    best_w = (v, kq, wall)
    w, kq, wall = best_w
    direction = {"left": (-1, 0), "right": (1, 0), "bottom": (0, -1), "top": (0, 1)}[wall]
    for extra, label, exp in ((F(0), "exact contact", "accept"), (E30, "1e-30 past", "refuse")):
        m = w + extra
        q = (sq[kq][0] + direction[0] * m, sq[kq][1] + direction[1] * m, sq[kq][2])
        va, vb, oa, ob = walls_both([q], side)
        moved_sq = list(sq)
        moved_sq[kq] = q
        info = one_square_all(moved_sq, kq, side)
        rec(controls, f"C4 least-clearance square {kq + 1} moved to the {wall} wall, {label}", exp, va, vb,
            clearance_before=str(float(w)), moved_square_full_decision=info)

    # C5: enlarge square i of the least-gap pair to contact
    ci = sa[i]
    cands = []
    for kk, (bx, by) in enumerate(ci[1] + sa[j][1]):
        qi_ = [px * bx + py * by for (px, py) in ci[0]]
        qj_ = [px * bx + py * by for (px, py) in sa[j][0]]
        gb = max(min(qj_) - max(qi_), min(qi_) - max(qj_))
        (ux, uy), (vx, vy) = ci[1]
        width = abs(ux * bx + uy * by) + abs(vx * bx + vy * by)  # d(half-extent)/d(h) along b
        if gb > 0:
            cands.append(gb / width)
    delta = max(cands)
    for extra, label, exp in ((F(0), "exact contact", "accept"), (E30, "1e-30 past", "refuse")):
        va, vb, g2, a2 = pair_both(sq[i], sq[j], hi=H + delta + extra)
        rec(controls, f"C5 square {i + 1} enlarged by delta* against {j + 1}, {label}", exp, va, vb,
            delta=str(float(delta)), gap_after=str(float(g2)))

    # gross
    dup = list(sq)
    dup[-1] = sq[0]
    va, vb, g2, a2 = pair_both(dup[0], dup[-1])
    rec(controls, f"G1 duplicate: square {n} replaced by square 1", "refuse", va, vb, area=str(a2))
    va, vb, oa, ob = walls_both([(F(-1), sq[0][1], sq[0][2])], side)
    rec(controls, "G2 square 1 centred at x = -1 (outside the box)", "refuse", va, vb)
    flat = [(x, y, F(0)) for (x, y, _) in sq]
    fa = [eg.square_a(*q) for q in flat]
    fb = [eg.square_b(*q) for q in flat]
    bad_a = sum(1 for p in range(n) for r in range(p + 1, n) if eg.pair_gap_a(fa[p], fa[r])[0] < 0)
    bad_b = sum(1 for p in range(n) for r in range(p + 1, n) if eg.pair_area_b(fb[p], fb[r]) != 0)
    rec(controls, "G3 every square turned to t = 0 in place", None,
        "accept" if bad_a == 0 else "refuse", "accept" if bad_b == 0 else "refuse",
        overlapping_pairs_a=bad_a, overlapping_pairs_b=bad_b)

    out = {
        "label": args.label,
        "path": args.cert,
        "sha256": c["sha256"],
        "n": n,
        "controls": controls,
        "all_pass": all(x["pass"] for x in controls),
        "cpu_seconds": round(time.process_time() - t0, 3),
    }
    Path(args.out).write_text(json.dumps(out, indent=1) + "\n")
    print(args.label, "ALL PASS" if out["all_pass"] else "FAILURES", len(controls), "controls", "cpu", out["cpu_seconds"])
    for x in controls:
        extra = ""
        if "moved_square_full_decision" in x:
            d = x["moved_square_full_decision"]
            extra = f" [moved square, whole: A {d['verdict_a']} B {d['verdict_b']} partners {d['overlapping_partners_a']}]"
        print("   ", "ok " if x["pass"] else "BAD", x["control"], "| expected", x["expected"], "| A", x["method_a"], "| B", x["method_b"], extra)


if __name__ == "__main__":
    main()
