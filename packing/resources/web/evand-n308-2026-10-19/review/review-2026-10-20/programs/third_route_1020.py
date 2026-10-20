"""An exact route of its own for Evan Daniel's #689 (308) and #694 (154) certificates.

Written for the stage 4 review of 20 October 2026. Standard library only; it imports
nothing from this repository and reads the certificate's literals with a reader of its
own. It decides, for each certificate, that the file gives exactly n unit squares with
pairwise disjoint interiors inside the closed box [0, S]^2, and measures the least wall
clearance and the least Euclidean distance between two squares, both exactly.

The method, applied to closed convex quadrilaterals given exactly over Q:

- Row k gives centre (x, y) and t; (c, s) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2)) lies on
  the unit circle identically, and the four corners centre +- u +- v with u = (c, s)/2
  and v = (-s, c)/2 bound a square of edge 1, held here by its edge lengths, right
  angles and area, counter-clockwise.
- Containment: every corner in the closed box, equivalently each coordinate in [0, S].
- Pairs whose centres are more than 2 apart are decided by circumscribed discs of
  radius sqrt(2)/2 (disjoint once the centres are sqrt(2) apart). Every closer pair is
  decided on the closed squares: a corner of one inside the other, or two edges meeting,
  by exact orientation tests. Where the closed squares are disjoint, the route records
  their exact squared distance, the least corner-to-edge one. Where they meet, the
  interiors are decided by the Minkowski difference: the exact convex hull of the sixteen
  corner differences, whose interior holds the origin exactly when the interiors meet.

Six controls per certificate, each at its required outcome: square 1 replaced by a copy
of square 0 (refused); square 0 moved by S + 2 (refused); the side lowered to the
largest corner coordinate, a far-wall contact (accepted, the box being closed), and to
10^-40 below that (refused); the closest pair's second square translated by the exact
difference of the closest points into contact (that pair alone: a contact, accepted) and
then 10^-30 of the centre difference further (the certificate refused, that pair
overlapping).

Usage::

    python -I third_route_1020.py --json OUT.json CERT [CERT ...] [--no-controls]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

Point = tuple[Fraction, Fraction]
Square = tuple[Point, Point, Point, Point]

ONE = Fraction(1)
TWO = Fraction(2)
FOUR = Fraction(4)


class Refused(Exception):
    """The certificate is not a packing, with the reason."""


# ---------------------------------------------------------------- reading


def read_certificate(text: str) -> tuple[int, Fraction, list[tuple[Fraction, Fraction, Fraction]]]:
    rows = [line.strip() for line in text.splitlines()]
    data = [line for line in rows if line and not line.startswith("#")]
    if not data:
        raise Refused("no header")
    head = data[0].split()
    if len(head) != 2:
        raise Refused("the header is not `n S`")
    n = int(head[0])
    side = Fraction(head[1])
    if n <= 0 or side <= 0:
        raise Refused("n and S must be positive")
    if len(data) != n + 1:
        raise Refused(f"{len(data) - 1} rows for n = {n}")
    poses = []
    for line in data[1:]:
        parts = line.split()
        if len(parts) != 3:
            raise Refused("a row is not `x y t`")
        poses.append((Fraction(parts[0]), Fraction(parts[1]), Fraction(parts[2])))
    return n, side, poses


# ---------------------------------------------------------------- geometry


def place(x: Fraction, y: Fraction, t: Fraction) -> Square:
    d = 1 + t * t
    c = (1 - t * t) / d
    s = 2 * t / d
    if c * c + s * s != 1:
        raise Refused("rotation off the unit circle")
    ux, uy = c / 2, s / 2
    vx, vy = -s / 2, c / 2
    square = (
        (x - ux - vx, y - uy - vy),
        (x + ux - vx, y + uy - vy),
        (x + ux + vx, y + uy + vy),
        (x - ux + vx, y - uy + vy),
    )
    # Unit edges, right angles, area 1, counter-clockwise.
    for i in range(4):
        a, b, c2 = square[i], square[(i + 1) % 4], square[(i + 2) % 4]
        ex, ey = b[0] - a[0], b[1] - a[1]
        fx, fy = c2[0] - b[0], c2[1] - b[1]
        if ex * ex + ey * ey != 1 or ex * fx + ey * fy != 0:
            raise Refused("not a unit square")
    if twice_area(square) != 2:
        raise Refused("area is not 1 or orientation is not counter-clockwise")
    return square


def twice_area(polygon: tuple[Point, ...]) -> Fraction:
    total = Fraction(0)
    for i in range(len(polygon)):
        (ax, ay), (bx, by) = polygon[i], polygon[(i + 1) % len(polygon)]
        total += ax * by - bx * ay
    return total


def cross(o: Point, a: Point, b: Point) -> Fraction:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def inside_closed(p: Point, square: Square) -> bool:
    """p in the closed square, which is counter-clockwise."""
    for i in range(4):
        if cross(square[i], square[(i + 1) % 4], p) < 0:
            return False
    return True


def on_segment(p: Point, a: Point, b: Point) -> bool:
    """p collinear with a, b and within the segment's bounding box."""
    return (
        min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
        and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
    )


def segments_meet(a: Point, b: Point, c: Point, d: Point) -> bool:
    """Closed segments ab and cd share a point."""
    d1 = cross(c, d, a)
    d2 = cross(c, d, b)
    d3 = cross(a, b, c)
    d4 = cross(a, b, d)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and (
        (d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)
    ):
        return True
    if d1 == 0 and on_segment(a, c, d):
        return True
    if d2 == 0 and on_segment(b, c, d):
        return True
    if d3 == 0 and on_segment(c, a, b):
        return True
    return d4 == 0 and on_segment(d, a, b)


def closed_meet(p: Square, q: Square) -> bool:
    if any(inside_closed(v, q) for v in p) or any(inside_closed(v, p) for v in q):
        return True
    for i in range(4):
        for j in range(4):
            if segments_meet(p[i], p[(i + 1) % 4], q[j], q[(j + 1) % 4]):
                return True
    return False


def point_segment_sq(p: Point, a: Point, b: Point) -> tuple[Fraction, Point]:
    """Exact squared distance from p to the closed segment ab, and the closest point."""
    abx, aby = b[0] - a[0], b[1] - a[1]
    apx, apy = p[0] - a[0], p[1] - a[1]
    length2 = abx * abx + aby * aby
    lam = (apx * abx + apy * aby) / length2
    if lam <= 0:
        foot = a
    elif lam >= 1:
        foot = b
    else:
        foot = (a[0] + lam * abx, a[1] + lam * aby)
    dx, dy = p[0] - foot[0], p[1] - foot[1]
    return dx * dx + dy * dy, foot


def squared_distance(p: Square, q: Square) -> tuple[Fraction, Point, Point]:
    """Least squared distance between two disjoint closed squares, with the closest points
    (on p, on q)."""
    best: tuple[Fraction, Point, Point] | None = None
    for v in p:
        for j in range(4):
            d2, foot = point_segment_sq(v, q[j], q[(j + 1) % 4])
            if best is None or d2 < best[0]:
                best = (d2, v, foot)
    for v in q:
        for i in range(4):
            d2, foot = point_segment_sq(v, p[i], p[(i + 1) % 4])
            if best is None or d2 < best[0]:
                best = (d2, foot, v)
    assert best is not None
    return best


def convex_hull(points: list[Point]) -> list[Point]:
    """Andrew's monotone chain, exact, counter-clockwise, no collinear points kept."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def half(seq: list[Point]) -> list[Point]:
        chain: list[Point] = []
        for pt in seq:
            while len(chain) >= 2 and cross(chain[-2], chain[-1], pt) <= 0:
                chain.pop()
            chain.append(pt)
        return chain

    lower = half(pts)
    upper = half(pts[::-1])
    return lower[:-1] + upper[:-1]


def interiors_meet(p: Square, q: Square) -> bool:
    """The origin is interior to the Minkowski difference p - q."""
    hull = convex_hull([(a[0] - b[0], a[1] - b[1]) for a in p for b in q])
    if len(hull) < 3:
        raise Refused("degenerate Minkowski difference")
    origin = (Fraction(0), Fraction(0))
    for i in range(len(hull)):
        if cross(hull[i], hull[(i + 1) % len(hull)], origin) <= 0:
            return False
    return True


def decide_pair(p: Square, q: Square, cp: Point, cq: Point) -> tuple[str, Fraction | None, tuple[Point, Point] | None]:
    """'far', 'apart' with the squared distance, 'contact' or 'overlap'."""
    dx, dy = cp[0] - cq[0], cp[1] - cq[1]
    centre2 = dx * dx + dy * dy
    if centre2 > FOUR:
        return "far", None, None
    if not closed_meet(p, q):
        d2, a, b = squared_distance(p, q)
        if d2 <= 0:
            raise Refused("disjoint closed squares at distance zero")
        return "apart", d2, (a, b)
    if interiors_meet(p, q):
        return "overlap", None, None
    return "contact", Fraction(0), None


# ---------------------------------------------------------------- the decision


def decide(
    n: int, side: Fraction, poses: list[tuple[Fraction, Fraction, Fraction]], *, pairs_only: set[tuple[int, int]] | None = None
) -> dict[str, object]:
    if len(poses) != n:
        raise Refused("row count")
    squares = [place(x, y, t) for x, y, t in poses]
    wall = None
    for k, square in enumerate(squares):
        for px, py in square:
            if px < 0 or py < 0 or px > side or py > side:
                raise Refused(f"square {k} leaves the closed box")
            for clearance in (px, side - px, py, side - py):
                if wall is None or clearance < wall[0]:
                    wall = (clearance, k)
    assert wall is not None
    exact = 0
    far = 0
    contacts = 0
    least: tuple[Fraction, int, int, tuple[Point, Point]] | None = None
    pairs = (
        sorted(pairs_only)
        if pairs_only is not None
        else [(i, j) for i in range(n) for j in range(i + 1, n)]
    )
    for i, j in pairs:
        verdict, d2, pts = decide_pair(
            squares[i], squares[j], (poses[i][0], poses[i][1]), (poses[j][0], poses[j][1])
        )
        if verdict == "far":
            far += 1
            continue
        exact += 1
        if verdict == "overlap":
            raise Refused(f"squares {i} and {j} overlap")
        if verdict == "contact":
            contacts += 1
            if least is None or Fraction(0) < least[0]:
                least = (Fraction(0), i, j, ((Fraction(0), Fraction(0)),) * 2)
            continue
        assert d2 is not None and pts is not None
        if least is None or d2 < least[0]:
            least = (d2, i, j, pts)
    assert least is not None
    return {
        "n": n,
        "side": str(side),
        "wall_clearance": str(wall[0]),
        "wall_clearance_float": f"{float(wall[0]):.4e}",
        "wall_square": wall[1],
        "least_squared_distance": str(least[0]),
        "least_distance_float": f"{math.sqrt(float(least[0])):.4e}",
        "closest_pair": [least[1], least[2]],
        "pairs_total": len(pairs),
        "pairs_decided_exactly": exact,
        "pairs_by_discs": far,
        "contacts": contacts,
        "_closest_points": least[3],
    }


# ---------------------------------------------------------------- controls


def outcome(fn) -> dict[str, object]:
    try:
        result = fn()
    except Refused as error:
        return {"accepted": False, "reason": str(error)}
    return {"accepted": True, "wall_clearance": result["wall_clearance"], "least_squared_distance": result["least_squared_distance"], "contacts": result["contacts"]}


def controls(n: int, side: Fraction, poses: list[tuple[Fraction, Fraction, Fraction]], positive: dict[str, object]) -> dict[str, dict[str, object]]:
    results: dict[str, dict[str, object]] = {}
    # 1. duplicate square: square 1 replaced by square 0.
    dup = list(poses)
    dup[1] = poses[0]
    results["duplicate_square_refused"] = {**outcome(lambda: decide(n, side, dup)), "required": "refused"}
    # 2. square 0 moved by S + 2.
    out = list(poses)
    out[0] = (poses[0][0] + side + 2, poses[0][1], poses[0][2])
    results["square_outside_refused"] = {**outcome(lambda: decide(n, side, out)), "required": "refused"}
    # 3/4. far-wall contact, and past it.
    squares = [place(x, y, t) for x, y, t in poses]
    largest = max(max(px, py) for sq in squares for px, py in sq)
    results["far_wall_contact_accepted"] = {**outcome(lambda: decide(n, largest, poses)), "required": "accepted", "side": str(largest)}
    past = largest - Fraction(1, 10**40)
    results["past_far_wall_refused"] = {**outcome(lambda: decide(n, past, poses)), "required": "refused"}
    # 5/6. closest pair into contact, then past it.
    i, j = positive["closest_pair"]  # type: ignore[misc]
    (ax, ay), (bx, by) = positive["_closest_points"]  # type: ignore[misc]
    shift = (ax - bx, ay - by)  # move square j so its closest point lands on square i's
    touching = list(poses)
    touching[j] = (poses[j][0] + shift[0], poses[j][1] + shift[1], poses[j][2])
    pair_only = outcome(lambda: decide(n, side, touching, pairs_only={(i, j)}))
    results["closest_pair_contact_accepted"] = {**pair_only, "required": "accepted with one contact", "pair": [i, j]}
    cx, cy = poses[i][0] - poses[j][0], poses[i][1] - poses[j][1]
    eps = Fraction(1, 10**30)
    over = list(poses)
    over[j] = (touching[j][0] + eps * cx, touching[j][1] + eps * cy, poses[j][2])
    results["closest_pair_overlap_refused"] = {**outcome(lambda: decide(n, side, over)), "required": "refused", "pair": [i, j]}
    return results


def satisfied(name: str, row: dict[str, object]) -> bool:
    required = str(row["required"])
    if required == "refused":
        return row["accepted"] is False
    if required == "accepted":
        return row["accepted"] is True
    return row["accepted"] is True and row.get("contacts") == 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("certificates", nargs="+", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--no-controls", action="store_true")
    args = parser.parse_args(argv)
    report: dict[str, object] = {}
    failures = 0
    for path in args.certificates:
        started = time.time()
        n, side, poses = read_certificate(path.read_text("utf-8"))
        try:
            positive = decide(n, side, poses)
        except Refused as error:
            report[str(path)] = {"accepted": False, "reason": str(error)}
            failures += 1
            print(f"{path}: REFUSED {error}", flush=True)
            continue
        row: dict[str, object] = {"accepted": True, **{k: v for k, v in positive.items() if not k.startswith("_")}}
        if not args.no_controls:
            ctl = controls(n, side, poses, positive)
            row["controls"] = ctl
            bad = [name for name, r in ctl.items() if not satisfied(name, r)]
            row["controls_at_required_outcome"] = len(ctl) - len(bad)
            if bad:
                failures += 1
                row["controls_failed"] = bad
        row["seconds"] = round(time.time() - started, 1)
        report[str(path)] = row
        print(
            f"{path}: n={n} side={float(side):.15f} wall={row['wall_clearance_float']} "
            f"least={row['least_distance_float']} pair={row['closest_pair']} exact={row['pairs_decided_exactly']} "
            f"discs={row['pairs_by_discs']} controls_ok={row.get('controls_at_required_outcome', 'n/a')} "
            f"{row['seconds']}s",
            flush=True,
        )
    args.json.write_text(json.dumps(report, indent=1, default=str) + "\n", "utf-8")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
