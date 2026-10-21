"""Review-lane exact checker for issue #678 (c-review-678-fable), standard library only.

Reads the 83 retained certificates and the issue body as data and decides, over Q:
  * each certificate's rows parse under the format `n S` then n rows `x y t`;
  * (c, s) = ((1-t^2)/(1+t^2), 2t/(1+t^2)) satisfies c^2 + s^2 = 1;
  * containment in the closed box [0, S]^2 by half-extents h = (|c|+|s|)/2 (no corner formed);
  * every pair (all pairs, no filter) by the separating-axis gap with unit normals
    (max over the four edge normals of |n.d| - h_i(n) - h_j(n)); gap < 0 is overlap;
  * every near pair (dx^2 + dy^2 < 2) again by the exact area of one square clipped by
    the other's four closed half-planes (Sutherland-Hodgman + shoelace), overlap iff area > 0;
  * the issue's printed side is the header side rounded upward at 12 places;
  * the margins at 204 and 260 against main's verified ceilings and T-196.

Usage: python -I review_678_check.py PACKET_SOURCE_DIR ISSUE_JSON RECEIPT_JSON OUT_JSON [--all-pairs 204 260 ...] [--workers 3]
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from pathlib import Path

RATIONAL = re.compile(r"-?\d+(/\d+)?|-?\d+\.\d+")
ROW = re.compile(
    r"\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*\[certificate( \(delete (\d+)\))?\]"
    r"\(https://github\.com/franciscouzo/square-packing/blob/([0-9a-f]{40})/certificates/best/n(\d+)\.cert\)"
)
DELETE = {545: 546, 641: 642}

# main at d588ad987 (verified_upper_bound exact_form of n-204.md and n-260.md), and T-196's claim
T186_204 = Fraction(
    "740433161719347828316145172430104761481126338872178671530915993369069066972891707484286255665843382616078162213/50000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
)
T155_260 = Fraction("416421356237309504880168872421/25000000000000000000000000000")
T196_260 = Fraction("16645778804181379786535601/1000000000000000000000000")
SEED_260 = Fraction("4161444696515435316429350771309/250000000000000000000000000000")


def lit(text: str, where: str) -> Fraction:
    if RATIONAL.fullmatch(text) is None:
        raise ValueError(f"{where}: {text!r} is not a rational literal")
    return Fraction(text)


def parse(text: str) -> tuple[int, Fraction, list[tuple[Fraction, Fraction, Fraction]]]:
    rows = [ln.split() for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
    if not rows or len(rows[0]) != 2 or not rows[0][0].isdigit():
        raise ValueError("bad header")
    n = int(rows[0][0])
    side = lit(rows[0][1], "side")
    if side <= 0 or len(rows) != n + 1:
        raise ValueError("count/side mismatch")
    poses = []
    for k, row in enumerate(rows[1:], 1):
        if len(row) != 3:
            raise ValueError(f"row {k}: not x y t")
        poses.append(tuple(lit(v, f"row {k}") for v in row))
    return n, side, poses


def basis(t: Fraction) -> tuple[Fraction, Fraction]:
    d = 1 + t * t
    c, s = (1 - t * t) / d, 2 * t / d
    if c * c + s * s != 1:
        raise AssertionError("rotation not on the unit circle")
    return c, s


def half_extent(c: Fraction, s: Fraction, nx: Fraction, ny: Fraction) -> Fraction:
    # projection half-width of a unit square with axes (c,s),(-s,c) onto unit normal n
    return (abs(nx * c + ny * s) + abs(-nx * s + ny * c)) / 2


def sat_gap(a, b) -> Fraction:
    xa, ya, ca, sa = a
    xb, yb, cb, sb = b
    dx, dy = xb - xa, yb - ya
    best = None
    for nx, ny in ((ca, sa), (-sa, ca), (cb, sb), (-sb, cb)):
        m = abs(nx * dx + ny * dy) - half_extent(ca, sa, nx, ny) - half_extent(cb, sb, nx, ny)
        if best is None or m > best:
            best = m
    return best


def corners(sq):
    x, y, c, s = sq
    h = Fraction(1, 2)
    ux, uy, vx, vy = c * h, s * h, -s * h, c * h
    return [(x + ux + vx, y + uy + vy), (x - ux + vx, y - uy + vy), (x - ux - vx, y - uy - vy), (x + ux - vx, y + uy - vy)]


def clip(poly, p, q):
    """Keep the part of poly on the left of (or on) directed line p->q (closed half-plane)."""
    out = []
    px, py = p
    ex, ey = q[0] - px, q[1] - py

    def side(pt):
        return ex * (pt[1] - py) - ey * (pt[0] - px)

    for i in range(len(poly)):
        cur, prev = poly[i], poly[i - 1]
        sc, sp = side(cur), side(prev)
        if sc >= 0:
            if sp < 0:
                t = sp / (sp - sc)
                out.append((prev[0] + t * (cur[0] - prev[0]), prev[1] + t * (cur[1] - prev[1])))
            out.append(cur)
        elif sp >= 0:
            t = sp / (sp - sc)
            out.append((prev[0] + t * (cur[0] - prev[0]), prev[1] + t * (cur[1] - prev[1])))
    return out


def area(poly) -> Fraction:
    a = Fraction(0)
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i - 1], poly[i]
        a += x1 * y2 - x2 * y1
    return abs(a) / 2


def overlap_area(a, b) -> Fraction:
    poly = corners(a)
    cb = corners(b)
    # corners() is counter-clockwise, so the interior is left of each directed edge
    for i in range(4):
        poly = clip(poly, cb[i], cb[(i + 1) % 4])
        if len(poly) < 3:
            return Fraction(0)
    return area(poly)


def ceil_places(v: Fraction, places: int) -> str:
    scale = 10**places
    k = -((-v * scale) // 1)  # ceiling of v*scale
    k = int(k)
    return f"{k // scale}.{k % scale:0{places}d}"


def decide(job):
    n, side, poses, all_pairs = job
    t0 = time.process_time()
    sqs = []
    for x, y, t in poses:
        c, s = basis(t)
        sqs.append((x, y, c, s))
    # containment by half-extents, closed box
    wall = min(min(x - (abs(c) + abs(s)) / 2, y - (abs(c) + abs(s)) / 2, side - x - (abs(c) + abs(s)) / 2, side - y - (abs(c) + abs(s)) / 2) for x, y, c, s in sqs)
    near = []
    for i, j in itertools.combinations(range(n), 2):
        dx, dy = sqs[j][0] - sqs[i][0], sqs[j][1] - sqs[i][1]
        if dx * dx + dy * dy < 2:
            near.append((i, j))
    least_gap, least_pair, overlaps, touching = None, None, 0, 0
    pairs_sat = 0
    for i, j in (itertools.combinations(range(n), 2) if all_pairs else near):
        g = sat_gap(sqs[i], sqs[j])
        pairs_sat += 1
        if g < 0:
            overlaps += 1
        elif g == 0:
            touching += 1
        if least_gap is None or g < least_gap:
            least_gap, least_pair = g, (i + 1, j + 1)
    area_overlaps = 0
    max_area = Fraction(0)
    for i, j in near:
        ar = overlap_area(sqs[i], sqs[j])
        if ar > 0:
            area_overlaps += 1
            max_area = max(max_area, ar)
    return {
        "n": n,
        "side": f"{side.numerator}/{side.denominator}",
        "wall_least": str(wall),
        "near_pairs": len(near),
        "pairs_sat": pairs_sat,
        "all_pairs": bool(all_pairs),
        "sat_overlaps": overlaps,
        "touching": touching,
        "least_gap": str(least_gap),
        "least_pair": least_pair,
        "area_overlaps": area_overlaps,
        "max_area": str(max_area),
        "passed": wall >= 0 and overlaps == 0 and area_overlaps == 0,
        "cpu": round(time.process_time() - t0, 2),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("issue", type=Path)
    ap.add_argument("receipt", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--all-pairs", type=int, nargs="*", default=[])
    ap.add_argument("--only", type=int, nargs="*", default=None)
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    body = json.loads(a.issue.read_text())["body"]
    claims = []
    for ln in body.splitlines():
        m = ROW.match(ln)
        if m:
            claims.append((int(m[1]), m[2], m[3], int(m[7]), int(m[5] or 0), m[6]))
    assert len(claims) == 85, len(claims)
    receipt = {r["n"]: r for r in json.loads(a.receipt.read_text())["rows"]}
    jobs, meta = [], []
    for n, prior, printed, cn, deleted, pin in claims:
        if a.only is not None and n not in a.only:
            continue
        assert pin == "7b6c87e129cf80b5ff9847b90b47fd30b4563c54"
        assert cn == DELETE.get(n, n) and deleted == cn - n
        hn, side, poses = parse((a.source / f"certificates/best/n{cn}.cert").read_text())
        assert hn == cn
        poses = poses[:n]
        up = ceil_places(side, 12)
        meta.append({"n": n, "printed": printed, "ceil12": up, "printed_ok": up == printed and Fraction(printed) - Fraction(1, 10**12) < side <= Fraction(printed), "prior": prior, "side": side})
        jobs.append((n, side, tuple(poses), n in a.all_pairs))
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        results = list(pool.map(decide, jobs))
    out = {"rows": [], "disagreements": [], "margins": {}}
    for m, r in zip(meta, results, strict=True):
        rec = receipt[m["n"]]
        ind = rec["decision"]["independent"]
        agree = {
            "side": rec["exact_side"] == r["side"],
            "near_pairs": rec["decision"]["candidate_pairs"] == r["near_pairs"],
            "least_wall": Fraction(ind["least_wall_clearance"]) == Fraction(r["wall_least"]),
            "least_gap": Fraction(ind["least_pair_gap"]) == Fraction(r["least_gap"]) if not r["all_pairs"] else Fraction(r["least_gap"]) <= Fraction(ind["least_pair_gap"]),
            "ceiling16": rec["side_ceiling_16"] == ceil_places(m["side"], 16),
        }
        row = {**r, **{k: v for k, v in m.items() if k != "side"}, "agrees_with_receipt": agree}
        out["rows"].append(row)
        if not (r["passed"] and m["printed_ok"] and all(agree.values())):
            out["disagreements"].append(row)
    sides = {m["n"]: m["side"] for m in meta}
    if 204 in sides:
        s = sides[204]
        out["margins"]["204"] = {
            "side": str(s), "ceil16": ceil_places(s, 16), "T-186_main": str(T186_204),
            "below_T186_by": str(T186_204 - s), "below_T186_float": float(T186_204 - s),
            "issue_prior_675_printed": next(m["prior"] for m in meta if m["n"] == 204),
            "below_675_at_least": float(Fraction(next(m["prior"] for m in meta if m["n"] == 204)) - Fraction(1, 10**12) - s),
        }
    if 260 in sides:
        s = sides[260]
        out["margins"]["260"] = {
            "side": str(s), "ceil16": ceil_places(s, 16), "T-155_main": str(T155_260), "below_T155_by": str(T155_260 - s), "below_T155_float": float(T155_260 - s),
            "T-196": str(T196_260), "below_T196_by": str(T196_260 - s), "below_T196_float": float(T196_260 - s),
            "seed_14a9af8": str(SEED_260), "below_seed_by_float": float(SEED_260 - s), "seed_ceil12": ceil_places(SEED_260, 12),
            "issue_prior_printed": next(m["prior"] for m in meta if m["n"] == 260),
        }
    out["summary"] = {"rows": len(out["rows"]), "passed": sum(1 for r in out["rows"] if r["passed"] and r["printed_ok"]), "disagreements": len(out["disagreements"]), "near_pairs_total": sum(r["near_pairs"] for r in out["rows"]), "sat_pairs_total": sum(r["pairs_sat"] for r in out["rows"]), "touching_total": sum(r["touching"] for r in out["rows"]), "cpu_total": round(sum(r["cpu"] for r in out["rows"]), 1)}
    a.out.write_text(json.dumps(out, indent=1))
    print(json.dumps(out["summary"]))
    print(json.dumps(out["margins"], indent=1))
    for d in out["disagreements"]:
        print("DISAGREE", d["n"], d["agrees_with_receipt"], d["passed"], d["printed_ok"])
    return 0 if not out["disagreements"] else 1


if __name__ == "__main__":
    sys.exit(main())
