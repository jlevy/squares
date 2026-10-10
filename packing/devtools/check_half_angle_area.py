"""A third exact route for the rational half-angle certificates of T-128, T-130 and T-131.

The register's two maintained routes (``devtools.evand_arrangement_reports``) share one
parse and one half-angle conversion (``devtools.evand_exact_certificates``) and both decide
pairs by the separating-axis theorem; at T-128 and T-130 one of them, ``sqpack.verify``, is
also the copy the source author ran. This route was written for the 2026-10-10 review of
the three entries, ``review-2026-10-10-couzo-daniel-refinement-replays.md`` under
``docs/project/reviews/``, from the certificate format and plane geometry. Its author had
read both maintained routes
and their parser; it imports none of their deciding or parsing code. The packet modules
are called only to admit the custody of the bytes it reads and to hand over the retained
receipts it compares with.

For ``n`` unit squares, each a centre ``(x, y)`` and ``t = tan(theta/2)``, in the closed
box ``[0, S]^2``:

- **rotation**: ``(c, s) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))``, checked to satisfy
  ``c^2 + s^2 = 1``, so every square is a unit square;
- **containment**: a unit square at angle ``theta`` reaches ``h = (|c| + |s|)/2`` either
  side of its centre along each axis, so it lies in the box iff ``h <= x <= S - h`` and
  ``h <= y <= S - h``; no corner is formed for this test;
- **disjoint interiors**: centres at least ``sqrt(2)`` apart hold the two squares in
  circumscribed discs whose interiors are disjoint; any closer pair is intersected
  exactly, one square clipped by the other's four closed half-planes, and the interiors
  are disjoint iff the intersection has area zero.

Arithmetic is ``fractions.Fraction`` throughout, the one component this route shares with
every exact checker here. For each positive it also measures the least Euclidean distance
between squares whose centres lie within 2 of each other, a different quantity from the
separating-axis gap the maintained routes report and never smaller than it; every other
pair is at least ``2 - sqrt(2)`` apart.

Every certificate gets five controls with required outcomes, each a full decision:
a duplicated square and a square moved outside the box (refused); the side shrunk by the
least far-wall clearance (accepted, the box being closed) and by ``10^-40`` more
(refused); and the closest pair, translated into contact (that pair accepted) and then
``10^-30`` of the centre distance further (the certificate refused).

From ``packing/``, with the project interpreter::

    python -m devtools.check_half_angle_area decide [--workers 2] [--json PATH]
    python -m devtools.check_half_angle_area replay-t128 [--workers 2]

``replay-t128`` is the maintained two-route replay of T-128's retained receipt, which
``devtools.couzo_refinement_reports`` has no command for: every job decided again by the
kernel and held to its retained row, as ``check --replay`` does for T-130 and T-131.
"""

from __future__ import annotations

import argparse
import json
import re
import time
from collections.abc import Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import couzo_followup_reports as t130
from devtools import couzo_refinement_reports as t128
from devtools import evand_arrangement_reports as kernel
from devtools import evand_hunt_reports as t131
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "frontier/results.yaml"
FRONTIER = ROOT / "frontier"

Point = tuple[Fraction, Fraction]
Square = tuple[Point, Point, Point, Point]
Pose = tuple[Fraction, Fraction, Fraction]

#: The side-shrink control's step past contact, and the pair control's push past contact
#: as a fraction of the centre distance: both far below binary64 resolution at these sides.
WALL_STEP = Fraction(1, 10**40)
PAIR_PUSH = Fraction(1, 10**30)
HALF = Fraction(1, 2)
OFFSETS = ((HALF, HALF), (-HALF, HALF), (-HALF, -HALF), (HALF, -HALF))
_LITERAL = re.compile(r"(-?)([0-9]+)(?:/([1-9][0-9]*)|\.([0-9]+))?")
_CLAIM = re.compile(r"s\((\d+)\)\s*<=\s*(\d+\.\d+)")


class AreaRouteError(ValueError):
    """A certificate this route refuses to read, or a disagreement it found."""


@dataclass(frozen=True, slots=True)
class Case:
    """One certificate: the register entry it supports, where it came from, and its text."""

    entry: str
    packet: str
    n: int
    text: str


@dataclass(frozen=True, slots=True)
class Decision:
    """One full decision of ``n`` squares in ``[0, side]^2``, with its least margins."""

    passed: bool
    pairs: int
    clipped: int
    overlapping: int
    outside: int
    wall_clearance: Fraction
    far_wall_clearance: Fraction
    closest: tuple[Fraction, int, int, Point, Point] | None


def literal(text: str) -> Fraction:
    """An integer, ``p/q`` or plain decimal literal, converted without `Fraction`'s parser."""
    match = _LITERAL.fullmatch(text)
    if match is None:
        raise AreaRouteError(f"{text[:40]!r} is not a rational literal")
    sign, whole, denominator, decimals = match.groups()
    if denominator is not None:
        value = Fraction(int(whole), int(denominator))
    elif decimals is not None:
        value = Fraction(int(whole + decimals), 10 ** len(decimals))
    else:
        value = Fraction(int(whole))
    return -value if sign else value


def parse_certificate(text: str, n: int) -> tuple[Fraction, tuple[Pose, ...]]:
    """The header ``n S`` and exactly ``n`` rows ``x y t``, skipping blank and ``#`` lines."""
    rows = [
        line.split()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not rows or len(rows[0]) != 2 or rows[0][0] != str(n):
        raise AreaRouteError(f"the header is not `{n} S`")
    side = literal(rows[0][1])
    if side <= 0:
        raise AreaRouteError("the side must be positive")
    if len(rows) - 1 != n:
        raise AreaRouteError(f"{len(rows) - 1} square rows for n = {n}")
    poses: list[Pose] = []
    for index, row in enumerate(rows[1:], start=1):
        if len(row) != 3:
            raise AreaRouteError(f"square {index}: {len(row)} fields, not `x y t`")
        x, y, t = (literal(value) for value in row)
        poses.append((x, y, t))
    return side, tuple(poses)


def rotation(t: Fraction) -> tuple[Fraction, Fraction]:
    """``(cos theta, sin theta)`` from ``t = tan(theta/2)``, held to the unit circle."""
    q = 1 + t * t
    c, s = (1 - t * t) / q, 2 * t / q
    if c * c + s * s != 1:
        raise AreaRouteError("the half-angle map left the unit circle")
    return c, s


def corners(x: Fraction, y: Fraction, c: Fraction, s: Fraction) -> Square:
    """The square's corners, counter-clockwise: its centre plus the rotated half-diagonals."""
    a, b, d, e = ((x + c * u - s * v, y + s * u + c * v) for u, v in OFFSETS)
    return a, b, d, e


def _cross(origin: Point, a: Point, b: Point) -> Fraction:
    return (a[0] - origin[0]) * (b[1] - origin[1]) - (a[1] - origin[1]) * (b[0] - origin[0])


def _cut(p: Point, q: Point, dp: Fraction, dq: Fraction) -> Point:
    r = dp / (dp - dq)
    return p[0] + (q[0] - p[0]) * r, p[1] + (q[1] - p[1]) * r


def intersection(subject: Sequence[Point], clip: Square) -> list[Point]:
    """``subject`` clipped by the four closed half-planes left of ``clip``'s edges."""
    polygon = list(subject)
    for k in range(4):
        if not polygon:
            break
        a, b = clip[k], clip[(k + 1) % 4]
        kept: list[Point] = []
        previous = polygon[-1]
        dp = _cross(a, b, previous)
        for current in polygon:
            dq = _cross(a, b, current)
            if dq >= 0:
                if dp < 0:
                    kept.append(_cut(previous, current, dp, dq))
                kept.append(current)
            elif dp > 0:
                kept.append(_cut(previous, current, dp, dq))
            previous, dp = current, dq
        polygon = kept
    return polygon


def twice_area(polygon: Sequence[Point]) -> Fraction:
    """Twice the signed area, by the shoelace formula; zero for a point or a segment."""
    total = Fraction(0)
    for index, p in enumerate(polygon):
        q = polygon[(index + 1) % len(polygon)]
        total += p[0] * q[1] - q[0] * p[1]
    return total


def centre(square: Square) -> Point:
    return (square[0][0] + square[2][0]) / 2, (square[0][1] + square[2][1]) / 2


def overlaps(left: Square, right: Square) -> bool:
    """Whether two unit squares' interiors meet: the disc test, then the exact area."""
    (lx, ly), (rx, ry) = centre(left), centre(right)
    if (lx - rx) ** 2 + (ly - ry) ** 2 >= 2:
        return False
    area = twice_area(intersection(left, right))
    if area < 0:
        raise AreaRouteError("a clipped intersection lost its orientation")
    return area > 0


def _foot(v: Point, a: Point, b: Point) -> Point:
    """The point of the unit segment ``ab`` nearest ``v``."""
    ux, uy = b[0] - a[0], b[1] - a[1]
    along = (v[0] - a[0]) * ux + (v[1] - a[1]) * uy
    if along <= 0:
        return a
    if along >= 1:
        return b
    return a[0] + along * ux, a[1] + along * uy


def closest_points(left: Square, right: Square) -> tuple[Fraction, Point, Point]:
    """Squared distance between two squares with disjoint interiors, and a nearest pair.

    The nearest points of two such convex polygons include a vertex of one, so the least
    vertex-to-edge distance in either direction is the distance between them.
    """
    best: tuple[Fraction, Point, Point] | None = None
    for first, second, flipped in ((left, right, False), (right, left, True)):
        for v in first:
            for k in range(4):
                foot = _foot(v, second[k], second[(k + 1) % 4])
                distance = (v[0] - foot[0]) ** 2 + (v[1] - foot[1]) ** 2
                if best is None or distance < best[0]:
                    best = (distance, foot, v) if flipped else (distance, v, foot)
    if best is None:
        raise AreaRouteError("a square has no vertices")
    return best


def decide(side: Fraction, poses: Sequence[Pose], *, measure: bool = False) -> Decision:
    """Decide every square against the box and every pair against each other."""
    squares: list[Square] = []
    clearances: list[Fraction] = []
    far: list[Fraction] = []
    outside = 0
    for x, y, t in poses:
        c, s = rotation(t)
        h = (abs(c) + abs(s)) / 2
        near_walls = (x - h, y - h)
        far_walls = (side - h - x, side - h - y)
        clearances.extend((*near_walls, *far_walls))
        far.extend(far_walls)
        if min(*near_walls, *far_walls) < 0:
            outside += 1
        squares.append(corners(x, y, c, s))
    pairs = clipped = overlapping = 0
    closest: tuple[Fraction, int, int, Point, Point] | None = None
    for i, (lx, ly, _lt) in enumerate(poses):
        for j in range(i + 1, len(poses)):
            rx, ry, _rt = poses[j]
            pairs += 1
            spread = (lx - rx) ** 2 + (ly - ry) ** 2
            if spread < 2:
                clipped += 1
                if overlaps(squares[i], squares[j]):
                    overlapping += 1
            if measure and spread < 4:
                distance, p, q = closest_points(squares[i], squares[j])
                if closest is None or distance < closest[0]:
                    closest = (distance, i, j, p, q)
    return Decision(
        passed=not outside and not overlapping,
        pairs=pairs,
        clipped=clipped,
        overlapping=overlapping,
        outside=outside,
        wall_clearance=min(clearances),
        far_wall_clearance=min(far),
        closest=closest,
    )


def controls(side: Fraction, poses: Sequence[Pose], decision: Decision) -> dict[str, bool]:
    """Each control's outcome; every one must match its required outcome."""
    duplicate = list(poses)
    duplicate[1] = duplicate[0]
    outside = list(poses)
    x, y, t = outside[0]
    outside[0] = (x + side + 2, y, t)
    touching = side - decision.far_wall_clearance
    result = {
        "duplicate-square-refused": not decide(side, duplicate).passed,
        "square-outside-refused": not decide(side, outside).passed,
        "side-at-far-wall-contact-accepted": decide(touching, poses).passed,
        "side-past-far-wall-contact-refused": not decide(touching - WALL_STEP, poses).passed,
    }
    if decision.closest is None:
        raise AreaRouteError("the pair controls need two squares within 2 of each other")
    _distance, i, j, p, q = decision.closest
    (xi, yi, _ti), (xj, yj, tj) = poses[i], poses[j]
    c, s = rotation(tj)
    shift = (p[0] - q[0], p[1] - q[1])
    contact = corners(xj + shift[0], yj + shift[1], c, s)
    left = corners(xi, yi, *rotation(poses[i][2]))
    result["closest-pair-in-contact-accepted"] = not overlaps(left, contact)
    pushed = list(poses)
    pushed[j] = (
        xj + shift[0] + PAIR_PUSH * (xi - xj),
        yj + shift[1] + PAIR_PUSH * (yi - yj),
        tj,
    )
    result["closest-pair-pushed-past-contact-refused"] = not decide(side, pushed).passed
    return result


def _root(value: Fraction) -> str:
    """The square root of a non-negative rational, to seven significant digits."""
    with localcontext() as context:
        context.prec = 40
        return f"{(Decimal(value.numerator) / Decimal(value.denominator)).sqrt():.6e}"


def _text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def decide_case(case: Case) -> dict[str, Any]:
    """This route's full verdict on one certificate, its margins and its controls."""
    started = time.monotonic()
    side, poses = parse_certificate(case.text, case.n)
    decision = decide(side, poses, measure=True)
    outcomes = controls(side, poses, decision)
    if decision.closest is None:
        raise AreaRouteError("no pair within 2 to measure")
    distance, i, j, _p, _q = decision.closest
    return {
        "entry": case.entry,
        "packet": case.packet,
        "n": case.n,
        "side": _text(side),
        "poses": [[_text(value) for value in pose] for pose in poses],
        "passed": decision.passed,
        "pairs": decision.pairs,
        "clipped_pairs": decision.clipped,
        "overlapping_pairs": decision.overlapping,
        "outside_squares": decision.outside,
        "wall_clearance": _text(decision.wall_clearance),
        "far_wall_clearance": _text(decision.far_wall_clearance),
        "least_distance_squared": _text(distance),
        "least_distance": _root(distance),
        "closest_pair": [i, j],
        "controls": outcomes,
        "wall_seconds": round(time.monotonic() - started, 2),
    }


def cases() -> list[Case]:
    """All fifteen certificates, after each packet's own custody admission of its bytes.

    T-128's eight texts are the complete originals its facts carry; T-130's five are the
    texts its facts rebuild, which its admission holds to the pinned blobs; T-131's two,
    n132 and the n155 evidence update to T-128, are the retained source files.
    """
    t128.read_facts()
    found = [
        Case("T-128", t128.PACKET.name, row["n"], row["source_certificate"])
        for row in kernel.read_xz(t128.fact_path())["cases"]
    ]
    found += [
        Case("T-130", t130.PACKET.name, n, t130.render(certificate))
        for n, certificate in t130.read_facts().items()
    ]
    t131.read_facts()
    found += [
        Case(
            "T-131" if n == 132 else "T-128",
            t131.PACKET.name,
            n,
            (t131.PACKET / "source" / t131.certificate_path(n)).read_text(encoding="utf-8"),
        )
        for n in t131.NUMBERS
    ]
    return found


def maintained_positives() -> dict[tuple[str, int], dict[str, Any]]:
    """Each retained positive job, as its packet module admits it."""
    rows: dict[tuple[str, int], dict[str, Any]] = {}
    for module in (t128, t130, t131):
        for n, row in module.check_certification().items():
            rows[module.PACKET.name, n] = row
    return rows


def register_claims() -> dict[str, dict[int, Fraction]]:
    """Every ``s(n) <= D`` the three register claims print, as exact rationals."""
    document = load_yaml(RESULTS.read_text(encoding="utf-8"))
    claims: dict[str, dict[int, Fraction]] = {}
    for result in document["results"]:
        if result["id"] in {"T-128", "T-130", "T-131"}:
            printed = _CLAIM.findall(" ".join(str(result["claim"]).split()))
            claims[result["id"]] = {int(n): Fraction(Decimal(value)) for n, value in printed}
    return claims


def receipt_totals() -> dict[str, dict[str, Any]]:
    """What each retained receipt records in total, for the register's prose to be held to."""
    totals: dict[str, dict[str, Any]] = {}
    for module in (t128, t130, t131):
        jobs = kernel.read_xz(module.receipt_path())["cases"]
        totals[module.PACKET.name] = {
            "jobs": len(jobs),
            "pair_decisions": sum(
                job[route]["pairs_tested"] for job in jobs for route in kernel.ROUTES
            ),
            "route_cpu_seconds": round(
                sum(sum(job["cpu_seconds"].values()) for job in jobs), 2
            ),
            "job_wall_seconds": round(sum(job["wall_seconds"] for job in jobs), 2),
            "longest_job_seconds": round(max(job["wall_seconds"] for job in jobs), 2),
        }
    return totals


def case_ceiling(n: int) -> dict[str, str]:
    """The case record's verified upper lane and reported source, read and not changed."""
    text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    front = load_yaml(text.split("---\n", 2)[1])["packing"]
    lane = front["verified_upper_bound"]
    return {
        "exact_form": str(lane["exact_form"]),
        "value": str(lane["value"]),
        "evidence": ", ".join(str(item) for item in lane["evidence"]),
        "reported_source_key": str(front["reported_upper_bound"]["source_key"]),
    }


def compare(row: dict[str, Any], maintained: dict[str, Any], claimed: Fraction) -> list[str]:
    """Every way this route's reading and margins disagree with the record."""
    problems: list[str] = []
    where = f"{row['entry']} n={row['n']} ({row['packet']})"
    inputs = maintained["checker_input"]
    if Fraction(inputs["side"]) != Fraction(row["side"]):
        problems.append(f"{where}: side differs from the maintained routes' input")
    if [[Fraction(value) for value in pose] for pose in inputs["poses"]] != [
        [Fraction(value) for value in pose] for pose in row["poses"]
    ]:
        problems.append(f"{where}: a pose differs from the maintained routes' input")
    if claimed != Fraction(row["side"]):
        problems.append(f"{where}: the register claim's decimal is not the exact side")
    distance = Fraction(row["least_distance_squared"])
    for route in kernel.ROUTES:
        verdict = maintained[route]
        if verdict["verification_passed"] is not row["passed"]:
            problems.append(f"{where}: {route} verdict differs")
        if Fraction(verdict["minimum_containment_clearance"]) != Fraction(
            row["wall_clearance"]
        ):
            problems.append(f"{where}: {route} wall clearance differs from h-extent clearance")
        gap = Fraction(verdict["minimum_best_pair_gap"])
        if gap > 0 and gap * gap > distance:
            problems.append(f"{where}: {route} separating gap exceeds the Euclidean distance")
    if not row["passed"] or not all(row["controls"].values()):
        problems.append(f"{where}: a positive or control missed its required outcome")
    return problems


def run_decide(workers: int, output: Path | None) -> int:
    started = time.monotonic()
    found = cases()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(decide_case, found))
    maintained = maintained_positives()
    claims = register_claims()
    problems: list[str] = []
    for row in rows:
        problems += compare(
            row, maintained[row["packet"], row["n"]], claims[row["entry"]][row["n"]]
        )
        row["case_verified_upper_bound"] = case_ceiling(row["n"])
    for row in rows:
        print(
            f"{row['entry']} n={row['n']:3d} {row['packet'][:24]:24s} "
            f"passed={row['passed']} pairs={row['pairs']} clipped={row['clipped_pairs']} "
            f"wall={row['wall_clearance']} least_distance={row['least_distance']} "
            f"controls={sum(row['controls'].values())}/{len(row['controls'])} "
            f"{row['wall_seconds']}s"
        )
    totals = receipt_totals()
    for packet, total in totals.items():
        print(f"retained receipt {packet}: {json.dumps(total)}")
    wall = round(time.monotonic() - started, 2)
    print(f"{len(rows)} certificates, {sum(r['pairs'] for r in rows)} pairs, {wall}s wall")
    if output is not None:
        report = {"rows": rows, "receipts": totals, "problems": problems, "wall_seconds": wall}
        output.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    for problem in problems:
        print(f"DISAGREEMENT: {problem}")
    return 1 if problems else 0


def _replay_t128_count(n: int) -> tuple[int, float]:
    started = time.monotonic()
    facts = t128.read_facts()
    record = kernel.read_xz(t128.receipt_path())
    t128.validate_certification(record, facts)
    kernel.replay_receipt(
        record,
        facts,
        [n],
        witness_prefix=t128.WITNESS_PREFIX,
        claim_limitations=t128.CLAIM_LIMITATIONS,
    )
    return n, round(time.monotonic() - started, 2)


def run_replay_t128(workers: int) -> int:
    started = time.monotonic()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        walls = list(pool.map(_replay_t128_count, t128.NUMBERS))
    for n, seconds in walls:
        print(
            f"T-128 n={n}: all three jobs, both routes, equal to the retained rows ({seconds}s)"
        )
    print(f"T-128: 24 jobs replayed and equal, {round(time.monotonic() - started, 2)}s wall")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    deciding = sub.add_parser("decide")
    deciding.add_argument("--workers", type=int, choices=(1, 2), default=2)
    deciding.add_argument("--json", type=Path)
    replay = sub.add_parser("replay-t128")
    replay.add_argument("--workers", type=int, choices=(1, 2), default=2)
    args = parser.parse_args(argv)
    if args.action == "decide":
        return run_decide(args.workers, args.json)
    return run_replay_t128(args.workers)


if __name__ == "__main__":
    raise SystemExit(main())
