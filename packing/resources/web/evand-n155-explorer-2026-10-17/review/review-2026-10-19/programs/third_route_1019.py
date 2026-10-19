"""A third exact route for Evan Daniel's five certificates of 16 to 18 October 2026.

Written for the stage 4 review of 19 October 2026 (bead think-s5u5): #669's s(155), #674's
two s(229) dilation certificates (opening and update), #659's s(236) and #664's s(271).
It imports nothing from this repository and nothing outside Python's standard library.
It reads each certificate's retained bytes as data with its own parser and decides
feasibility in exact rational arithmetic by a method neither maintained route uses:
closed squares are shown disjoint with an exact positive Euclidean distance, and only a
pair whose closed squares meet is decided by its Minkowski difference.

For ``n`` unit squares, each a centre ``(x, y)`` and ``t = tan(theta/2)``, in the closed
box ``[0, S]^2``:

- **unit squares**: ``(c, s) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))`` is held to
  ``c^2 + s^2 = 1``; the corners are ``(x, y) + u (c, s) + v (-s, c)`` for
  ``u, v = +-1/2``, and each placed polygon is held to four edges of squared length 1,
  each at a right angle to the next, turning counter-clockwise, with shoelace area 1;
- **containment**: every corner lies in ``[0, S]^2``; the box being convex, so does the
  square. The least clearance is the least of ``x, S - x, y, S - y`` over every corner;
- **disjoint interiors**: centres 2 or more apart (``d^2 >= 4``) hold the two squares in
  circumscribed discs of radius ``sqrt(2)/2`` that cannot meet. For every closer pair
  the closed squares are disjoint iff no edge of one meets an edge of the other (exact
  orientation tests, touching included) and no corner of one lies in the other (closed).
  Then their exact squared Euclidean distance is the least corner-to-edge squared distance, a rational
  number because every edge has length 1. A pair whose closed squares meet has disjoint
  interiors iff the origin is not interior to the Minkowski difference ``A - B``, the
  convex hull of the sixteen corner differences, built exactly; that pair is a contact
  when the origin is on its boundary and an overlap when inside.

Every certificate also takes six controls, each a full decision with a required outcome:
square 1 replaced by square 0 (refused); square 0 moved by ``S + 2`` (refused); the side
shrunk by the least far-wall clearance (accepted, the box being closed) and by ``10^-40``
more (refused); the closest pair, square ``j`` translated by the exact closest-point
difference into contact (that pair accepted, decided alone), then a further ``10^-30`` of
the centre difference (the certificate refused).

It also holds each certificate to what other records state about it, as data: the side
and every pose to the positive job of the packet's retained receipt, the least wall
clearance to both maintained routes' ``minimum_containment_clearance`` exactly, the
least distance to at least their ``minimum_best_pair_gap``; the side to the register's
claim (``CLAIMED``, copied by hand from ``packing/frontier/results.yaml`` at
``d7413ccdb``) and to the issue's print (``PRINTED``), rounded up at its places; with
``--upstream DIR``, the retained bytes to the pinned file ``custody.py`` fetched.

Usage, from ``packing/`` with the project interpreter::

    python -I third_route_1019.py --json OUT.json [--upstream CUSTODY_OUT]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import re
import sys
import time
from fractions import Fraction
from pathlib import Path

Point = tuple[Fraction, Fraction]
Poly = tuple[Point, Point, Point, Point]
Pose = tuple[Fraction, Fraction, Fraction]

WEB = Path.cwd() / "resources/web"

#: The five certificates: key, packet, n, the certificate's upstream path.
CERTIFICATES = (
    ("#669 n155", "evand-n155-explorer-2026-10-17", 155, "search/packer/candidates/s155_ex2.cert"),
    ("#674 n229 opening", "evand-n229-dilation-2026-10-17", 229, "search/packer/candidates/s229.cert"),
    ("#674 n229 update", "evand-n229-dilation-update-2026-10-18", 229, "search/packer/candidates/s229_v2.cert"),
    ("#659 n236", "evand-n236-2026-10-16", 236, "search/packer/candidates/s236_bm3c.cert"),
    ("#664 n271", "evand-n271-2026-10-17", 271, "search/packer/candidates/s271_ex1.cert"),
)

#: The side each register entry's claim states, as printed in results.yaml at d7413ccdb.
CLAIMED = {
    "#669 n155": ("T-197", "2590452188930112807053435932173/200000000000000000000000000000"),
    "#674 n229 opening": ("T-198", "7825081627429265081627421439843/500000000000000000000000000000"),
    "#674 n229 update": ("T-199", "7825080756947776580756939951343/500000000000000000000000000000"),
    "#659 n236": ("T-218", "15.861934390607358617243798571394"),
    "#664 n271": ("T-219", "16.948947733713657510723401112423"),
}

#: The side each issue prints, which it says is the exact side rounded up at 12 places.
PRINTED = {
    "#669 n155": "12.952260944651",
    "#674 n229 opening": "15.650163254859",
    "#674 n229 update": "15.650161513896",
    "#659 n236": "15.861934390608",
    "#664 n271": "16.948947733714",
}

WALL_STEP = Fraction(1, 10**40)
PAIR_PUSH = Fraction(1, 10**30)
HALF = Fraction(1, 2)
ZERO = Fraction(0)
_INTEGER = re.compile(r"(-?)([0-9]+)")
_RATIO = re.compile(r"(-?)([0-9]+)/([0-9]+)")
_DECIMAL = re.compile(r"(-?)([0-9]+)\.([0-9]+)")


class RouteError(ValueError):
    """A certificate this route refuses to read, or a disagreement it found."""


# ---------------------------------------------------------------- reading


def literal(text: str) -> Fraction:
    """An integer, ``p/q`` with ``q > 0``, or plain decimal, read without Fraction's parser."""
    if match := _INTEGER.fullmatch(text):
        value = Fraction(int(match[2]))
    elif match := _RATIO.fullmatch(text):
        if int(match[3]) == 0:
            raise RouteError(f"{text[:40]!r}: zero denominator")
        value = Fraction(int(match[2]), int(match[3]))
    elif match := _DECIMAL.fullmatch(text):
        value = Fraction(int(match[2] + match[3]), 10 ** len(match[3]))
    else:
        raise RouteError(f"{text[:40]!r} is not a rational literal")
    return -value if match[1] else value


def parse(text: str, n: int) -> tuple[Fraction, list[Pose], list[str]]:
    """Comment lines (``#``) and blank lines skipped; then ``n S``; then exactly n rows ``x y t``."""
    comments = [line for line in text.splitlines() if line.strip().startswith("#")]
    rows = [
        line.split()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not rows or len(rows[0]) != 2 or rows[0][0] != str(n):
        raise RouteError(f"the header is not `{n} S`")
    side = literal(rows[0][1])
    if side <= 0:
        raise RouteError("the side must be positive")
    if len(rows) != n + 1:
        raise RouteError(f"{len(rows) - 1} square rows for n = {n}")
    poses: list[Pose] = []
    for index, row in enumerate(rows[1:]):
        if len(row) != 3:
            raise RouteError(f"square {index}: {len(row)} fields")
        x, y, t = (literal(field) for field in row)
        poses.append((x, y, t))
    return side, poses, comments


# ---------------------------------------------------------------- geometry


def rotation(t: Fraction) -> tuple[Fraction, Fraction]:
    denominator = 1 + t * t
    c, s = (1 - t * t) / denominator, 2 * t / denominator
    if c * c + s * s != 1:
        raise RouteError("rotation off the unit circle")
    return c, s


def corners(x: Fraction, y: Fraction, c: Fraction, s: Fraction) -> Poly:
    """The four corners, counter-clockwise, of the unit square at ``(x, y)`` turned by (c, s)."""
    out = []
    for u, v in ((-HALF, -HALF), (HALF, -HALF), (HALF, HALF), (-HALF, HALF)):
        out.append((x + u * c - v * s, y + u * s + v * c))
    return (out[0], out[1], out[2], out[3])


def cross(o: Point, a: Point, b: Point) -> Fraction:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def is_unit_square(poly: Poly) -> bool:
    edges = [(poly[(k + 1) % 4][0] - poly[k][0], poly[(k + 1) % 4][1] - poly[k][1]) for k in range(4)]
    for k in range(4):
        ex, ey = edges[k]
        fx, fy = edges[(k + 1) % 4]
        if ex * ex + ey * ey != 1 or ex * fx + ey * fy != 0 or ex * fy - ey * fx != 1:
            return False
    twice_area = sum(
        poly[k][0] * poly[(k + 1) % 4][1] - poly[(k + 1) % 4][0] * poly[k][1] for k in range(4)
    )
    return twice_area == 2


def _between(a: Point, b: Point, p: Point) -> bool:
    """For ``p`` on the line ``ab``: whether it lies on the closed segment."""
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def segments_meet(p1: Point, p2: Point, q1: Point, q2: Point) -> bool:
    """Whether two closed segments share a point, by exact orientation tests."""
    d1, d2 = cross(q1, q2, p1), cross(q1, q2, p2)
    d3, d4 = cross(p1, p2, q1), cross(p1, p2, q2)
    if ((d1 > 0 > d2) or (d1 < 0 < d2)) and ((d3 > 0 > d4) or (d3 < 0 < d4)):
        return True
    return (
        (d1 == 0 and _between(q1, q2, p1))
        or (d2 == 0 and _between(q1, q2, p2))
        or (d3 == 0 and _between(p1, p2, q1))
        or (d4 == 0 and _between(p1, p2, q2))
    )


def in_closed(poly: Poly, p: Point) -> bool:
    return all(cross(poly[k], poly[(k + 1) % 4], p) >= 0 for k in range(4))


def corner_to_edge(p: Point, a: Point, b: Point) -> tuple[Fraction, Point]:
    """Squared distance from ``p`` to the closed unit segment ``ab``, and the nearest point."""
    ex, ey = b[0] - a[0], b[1] - a[1]
    length2 = ex * ex + ey * ey
    wx, wy = p[0] - a[0], p[1] - a[1]
    along = wx * ex + wy * ey
    if along <= 0:
        return wx * wx + wy * wy, a
    if along >= length2:
        vx, vy = p[0] - b[0], p[1] - b[1]
        return vx * vx + vy * vy, b
    normal = ex * wy - ey * wx
    ratio = along / length2
    return normal * normal / length2, (a[0] + ratio * ex, a[1] + ratio * ey)


def hull(points: list[Point]) -> list[Point]:
    """The convex hull, counter-clockwise, collinear points dropped (monotone chain, exact)."""
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts
    lower: list[Point] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list[Point] = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def interiors_meet(a: Poly, b: Poly) -> bool:
    """Whether the open squares meet: the origin strictly inside the hull of ``A - B``."""
    difference = hull([(p[0] - q[0], p[1] - q[1]) for p in a for q in b])
    origin = (ZERO, ZERO)
    count = len(difference)
    return count >= 3 and all(
        cross(difference[k], difference[(k + 1) % count], origin) > 0 for k in range(count)
    )


def pair(a: Poly, b: Poly) -> tuple[str, Fraction, Point | None, Point | None]:
    """``apart`` with the exact squared distance and closest points, or ``contact``/``overlap``."""
    meet = any(
        segments_meet(a[i], a[(i + 1) % 4], b[j], b[(j + 1) % 4]) for i in range(4) for j in range(4)
    ) or any(in_closed(b, p) for p in a) or any(in_closed(a, q) for q in b)
    if meet:
        return ("overlap" if interiors_meet(a, b) else "contact"), ZERO, None, None
    best: tuple[Fraction, Point, Point] | None = None
    for p in a:
        for j in range(4):
            d2, foot = corner_to_edge(p, b[j], b[(j + 1) % 4])
            if best is None or d2 < best[0]:
                best = (d2, p, foot)
    for q in b:
        for i in range(4):
            d2, foot = corner_to_edge(q, a[i], a[(i + 1) % 4])
            if best is None or d2 < best[0]:
                best = (d2, foot, q)
    assert best is not None
    if best[0] <= 0:
        raise RouteError("disjoint closed squares at distance zero")
    return "apart", best[0], best[1], best[2]


# ---------------------------------------------------------------- deciding


def place(poses: list[Pose]) -> list[Poly]:
    polys = []
    for index, (x, y, t) in enumerate(poses):
        c, s = rotation(t)
        poly = corners(x, y, c, s)
        if not is_unit_square(poly):
            raise RouteError(f"square {index} is not a unit square")
        polys.append(poly)
    return polys


def decide(side: Fraction, poses: list[Pose]) -> dict[str, object]:
    """One full decision: containment of every corner, then every pair.

    Pairs whose centres are 2 or more apart are decided by the disc rule alone; every
    other pair is decided, and measured, by `pair`.
    """
    polys = place(poses)
    centres = [(x, y) for x, y, _t in poses]
    outside = []
    wall: Fraction | None = None
    far: Fraction | None = None
    for index, poly in enumerate(polys):
        for vx, vy in poly:
            if not (0 <= vx <= side and 0 <= vy <= side):
                outside.append(index)
            gaps = (vx, vy, side - vx, side - vy)
            far_gap = min(gaps[2], gaps[3])
            wall = min(gaps) if wall is None else min(wall, *gaps)
            far = far_gap if far is None else min(far, far_gap)
    pairs = disc = measured = contacts = 0
    overlaps: list[tuple[int, int]] = []
    closest: tuple[Fraction, int, int, Point, Point] | None = None
    for i in range(len(polys)):
        xi, yi = centres[i]
        for j in range(i + 1, len(polys)):
            pairs += 1
            dx, dy = xi - centres[j][0], yi - centres[j][1]
            if dx * dx + dy * dy >= 4:
                disc += 1
                continue
            measured += 1
            verdict, dist2, p, q = pair(polys[i], polys[j])
            if verdict == "overlap":
                overlaps.append((i, j))
            elif verdict == "contact":
                contacts += 1
            elif closest is None or dist2 < closest[0]:
                assert p is not None and q is not None
                closest = (dist2, i, j, p, q)
    return {
        "passed": not outside and not overlaps,
        "outside": sorted(set(outside)),
        "overlaps": overlaps,
        "pairs": pairs,
        "disc_rule": disc,
        "measured": measured,
        "contacts": contacts,
        "wall": wall,
        "far_wall": far,
        "closest": closest,
    }


def controls(
    side: Fraction, poses: list[Pose], positive: dict[str, object]
) -> dict[str, dict[str, object]]:
    """The six controls, each with its required outcome and what this route found."""
    out: dict[str, dict[str, object]] = {}
    duplicate = list(poses)
    duplicate[1] = duplicate[0]
    result = decide(side, duplicate)
    out["duplicate square"] = {"required": "refused", "passed": result["passed"], "overlaps": result["overlaps"]}
    moved = list(poses)
    x, y, t = moved[0]
    moved[0] = (x + side + 2, y, t)
    result = decide(side, moved)
    out["square moved by S + 2"] = {"required": "refused", "passed": result["passed"], "outside": result["outside"]}
    far = positive["far_wall"]
    assert isinstance(far, Fraction)
    result = decide(side - far, poses)
    out["side at far-wall contact"] = {"required": "accepted", "passed": result["passed"], "wall": str(result["wall"])}
    result = decide(side - far - WALL_STEP, poses)
    out["side 1e-40 past contact"] = {"required": "refused", "passed": result["passed"], "outside": result["outside"]}
    closest = positive["closest"]
    assert isinstance(closest, tuple)
    _d2, i, j, p, q = closest
    xi, yi, _ti = poses[i]
    xj, yj, tj = poses[j]
    touching = (xj + p[0] - q[0], yj + p[1] - q[1], tj)
    polys = place([poses[i], touching])
    verdict = pair(polys[0], polys[1])[0]
    out["closest pair into contact"] = {"required": "accepted", "pair": [i, j], "verdict": verdict, "passed": verdict == "contact"}
    pushed = list(poses)
    pushed[j] = (touching[0] + PAIR_PUSH * (xi - xj), touching[1] + PAIR_PUSH * (yi - yj), tj)
    result = decide(side, pushed)
    out["closest pair 1e-30 past contact"] = {"required": "refused", "passed": result["passed"], "overlaps": result["overlaps"]}
    for row in out.values():
        row["at_required_outcome"] = row["passed"] is (row["required"] == "accepted")
    return out


# ---------------------------------------------------------------- records read as data


def decimal(value: Fraction, places: int = 4) -> str:
    """``value`` in scientific notation at ``places`` significant digits, for display only."""
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    value = abs(value)
    exponent = len(str(value.numerator)) - len(str(value.denominator))
    while Fraction(10) ** exponent > value:
        exponent -= 1
    while Fraction(10) ** (exponent + 1) <= value:
        exponent += 1
    digits = round(value / Fraction(10) ** exponent * 10 ** (places - 1))
    if digits >= 10**places:
        digits //= 10
        exponent += 1
    text = str(digits)
    return f"{sign}{text[0]}.{text[1:]}e{exponent}"


def fixed(value: Fraction, places: int) -> str:
    """A fraction whose denominator divides ``10^places``, written out in full."""
    scaled = value * 10**places
    if scaled.denominator != 1:
        raise RouteError("not a terminating decimal at these places")
    whole, rest = divmod(scaled.numerator, 10**places)
    return f"{whole}.{rest:0{places}d}"


def sqrt_decimal(value: Fraction, places: int = 4) -> str:
    """``sqrt(value)`` for display, from an integer square root at ample precision."""
    from math import isqrt

    scale = 10**80
    root = Fraction(isqrt(value.numerator * scale * scale // value.denominator), scale)
    return decimal(root, places)


def rounded_up(value: Fraction, places: int) -> Fraction:
    scale = 10**places
    return Fraction(-((-value.numerator * scale) // value.denominator), scale)


def receipt_positive(packet: str) -> dict[str, object]:
    record = json.loads(lzma.decompress((WEB / packet / "receipts/exact-certification.json.xz").read_bytes()))
    (row,) = [case for case in record["cases"] if case["control"] == "positive"]
    return row


def run(upstream: Path | None) -> dict[str, object]:
    report: dict[str, object] = {"certificates": {}}
    problems: list[str] = []
    for key, packet, n, path in CERTIFICATES:
        started = time.monotonic()
        cpu = time.process_time()
        raw = (WEB / packet / "source" / path).read_bytes()
        row: dict[str, object] = {"packet": packet, "n": n, "path": path, "sha256": hashlib.sha256(raw).hexdigest()}
        if upstream is not None:
            fetched = (upstream / packet / "tree" / path).read_bytes()
            row["equals_fetched_upstream"] = fetched == raw
            if fetched != raw:
                problems.append(f"{key}: retained bytes differ from the fetched pin")
        side, poses, comments = parse(raw.decode("ascii"), n)
        row["header_comments"] = comments
        row["side"] = str(side)
        decision = decide(side, poses)
        positive_seconds = time.process_time() - cpu
        row["passed"] = decision["passed"]
        if not decision["passed"]:
            problems.append(f"{key}: refused")
        wall = decision["wall"]
        closest = decision["closest"]
        assert isinstance(wall, Fraction) and isinstance(closest, tuple)
        row["pairs"] = decision["pairs"]
        row["disc_rule_pairs"] = decision["disc_rule"]
        row["measured_pairs"] = decision["measured"]
        row["contacts"] = decision["contacts"]
        row["least_wall_clearance"] = str(wall)
        row["least_wall_clearance_decimal"] = decimal(wall)
        row["least_far_wall_clearance"] = str(decision["far_wall"])
        row["least_distance_squared"] = str(closest[0])
        row["least_distance_decimal"] = sqrt_decimal(closest[0])
        row["closest_pair"] = [closest[1], closest[2]]
        row["positive_cpu_seconds"] = round(positive_seconds, 2)
        # Records read as data.
        retained = receipt_positive(packet)
        given = retained["checker_input"]
        same_input = Fraction(given["side"]) == side and len(given["poses"]) == n and all(
            tuple(Fraction(v) for v in pose) == mine for pose, mine in zip(given["poses"], poses, strict=True)
        )
        row["equals_receipt_input"] = same_input
        if not same_input:
            problems.append(f"{key}: side or poses differ from the receipt's positive input")
        for route in ("exact_verify", "independent"):
            theirs = retained[route]
            wall_equal = Fraction(theirs["minimum_containment_clearance"]) == wall
            gap = Fraction(theirs["minimum_best_pair_gap"])
            distance_covers = closest[0] >= gap * gap and gap > 0
            row[f"{route}_wall_equal"] = wall_equal
            row[f"{route}_best_pair_gap"] = decimal(gap)
            row[f"{route}_distance_at_least_gap"] = distance_covers
            if not (wall_equal and distance_covers and theirs["verification_passed"]):
                problems.append(f"{key}: disagrees with {route}")
        entry, claimed = CLAIMED[key]
        row["claim"] = {"entry": entry, "equal": literal(claimed) == side}
        if literal(claimed) != side:
            problems.append(f"{key}: side is not {entry}'s claim")
        printed = PRINTED[key]
        places = len(printed.split(".")[1])
        row["printed"] = {"value": printed, "rounded_up_equal": rounded_up(side, places) == literal(printed)}
        if rounded_up(side, places) != literal(printed):
            problems.append(f"{key}: the print is not the side rounded up")
        row["rounded_up_16"] = fixed(rounded_up(side, 16), 16)
        row["controls"] = controls(side, poses, decision)
        held = row["controls"]
        assert isinstance(held, dict)
        for name, outcome in held.items():
            if not outcome["at_required_outcome"]:
                problems.append(f"{key}: control {name} not at its required outcome")
        row["wall_seconds"] = round(time.monotonic() - started, 2)
        certificates = report["certificates"]
        assert isinstance(certificates, dict)
        certificates[key] = row
        at_outcome = sum(1 for outcome in held.values() if outcome["at_required_outcome"])
        print(
            f"{key}: passed={row['passed']} pairs={row['pairs']} measured={row['measured_pairs']} "
            f"wall={row['least_wall_clearance_decimal']} distance={row['least_distance_decimal']} "
            f"controls={at_outcome}/6 receipt_input={same_input} "
            f"claim={literal(claimed) == side} print={rounded_up(side, places) == literal(printed)} "
            f"{row['wall_seconds']} s",
            flush=True,
        )
    report["problems"] = problems
    return report


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--upstream", type=Path)
    args = parser.parse_args(argv)
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    report = run(args.upstream)
    report["started_utc"] = started
    report["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    report["python"] = sys.version.split()[0]
    args.json.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    problems = report["problems"]
    assert isinstance(problems, list)
    print(f"{len(CERTIFICATES)} certificates, problems: {problems or 'none'}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
