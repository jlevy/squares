"""A third exact route for the rational upper-bound certificates of the 2026-10-10 reviews.

It was written for T-128, T-130 and T-131, and extended for the four imports of the same
intake pass, #476, #481, #483 and #484 (``decide-imports``), in the review
``review-2026-10-10-upper-bound-imports-476-481-483-484.md``. For those it reads each
certificate the register would cite with readers of its own: Evan Daniel's text format,
SQUISH's JSON (#484 holds each count in both, which must agree), and the derived facts of
#481 and #483, rational centre-basis witnesses whose bases it reads as stated, holding
each to the unit circle. Where no upstream byte is retained, ``--upstream PACKET DIR``
holds each fact to the file it was derived from, fetched at the pin into ``DIR``: the
packet's pinned SHA-256, this route's own SQUISH or centred-JSON reader (centres moved by
``S/2``), and the printed side in its row of the file it is printed in.

It was extended again for the last two packets of that pass, in
``review-2026-10-10-upper-bound-imports-470-and-trio126.md`` (``decide-imports --imports
'#470' trio126``): Evan Daniel's ``n126_xu.cert``, read by the same text reader, and the
exact witnesses #470's importer derived from Mishapolk's decimal centre-and-angle poses,
read as derived facts over the whole replayed roster of 30. For #470, ``--upstream``
derives each witness again from the pinned decimal pose with this route's own reader and
arithmetic: the file's printed side ``s`` and the issue's ceiling ``S``, which must be
``s`` rounded up at its places; every centre dilated by ``S/s`` about the box centre; and
each ``tan(theta/2)`` rounded down at the declared places, computed in `decimal`
arithmetic by Machin's formula and Taylor series rather than by the importer's mpmath
intervals. For a packet that retains its certificates, ``--upstream`` holds each
retained file to its fetched upstream bytes. Where credit turns on whose arrangement a
certificate is (`CREDITED`), it is measured pose by pose against that certificate:
``n126_xu`` against Ryan Xu's at 126, and #470 at 103 and 258, the two counts where its
side is the smallest known, against Ryan Xu's and SQUISH's.

It reads the two issues filed after that sweep too, #488 and #489 (``decide-imports
--imports '#488' '#489'``): Francisco Couzo's and Evan Daniel's retained certificates in
Evan Daniel's text format, read by the same text reader at the counts each entry cites.
And it reads the fifteen certificates of Evan Daniel's display-regularized record lists,
which no issue reports (``decide-imports --imports regularized``): the same text format,
each retained as its upstream gzip and decompressed here. ``--upstream`` holds each
retained gzip to its fetched bytes as stored, and each offered side to the ``S_cert``
that the certificate's own JSON prints (`printed_json_side`). Each is measured pose by
pose against the packing the register credits it to, which T-146's `regularizations`
name count by count (`regularized_credit`): Ryan Xu's, Mishapolk's refinements at 103
and 258, and SQUISH's third request.

It reads PingYou Ltd's two certificates of 11 October too, #503 at 207 and #504 at 153
(``decide-imports --imports '#503' '#504'``), in the review
``review-2026-10-11-upper-bound-imports-503-504.md``: derived facts, since the source
states no licence, read as their bases state. ``--upstream`` holds each fact to the
source's ``nNNN.cert.json`` at the pin, read by this route's own reader of that JSON
(`read_pingyou_json`: SQUISH's rows, with the source's note, guard, undilated side and
construction record named and not read), and to the source's own corners Witness/v2
beside it, which the row names as stating the same packing, read by
`read_witness_corners`: each square's centre as the mean of its corners and its rotation
as its first edge, held to the unit circle, the other three edges held to be that edge's
quarter turns. Where the source says a certificate was assembled from placed patches of
another packing (`LINEAGE`), `patch_lineage` measures how many of the parent's squares
reappear in it, centre and orientation, under a symmetry of the parent's box and a
translation, after the child's declared guard dilation is undone; that is a measurement
for credit and decides nothing.

It reads the two other certificate releases of 11 October too, Robert Barnett's #505 at
146 and 261 and Daniil Ostashev's #501 at 155, 156 and 211 (``decide-imports --imports
'#505' '#501'``), in the review ``review-2026-10-11-upper-bound-imports-505-501.md``.
#505's are derived facts, the source stating no licence; ``--upstream`` holds each to the
source's ``nNNN.cert`` at the pin, Evan Daniel's format read by this route's own text
reader (`read_evand_cert`). #501's are retained byte for byte under the source's MIT
licence in its own ``.sqcert`` format, Evan Daniel's with the header split over ``n N``
and ``s S`` lines, read by `parse_sqcert`; ``--upstream`` holds each retained file to its
fetched bytes and its offered side to the README table at the pin (`printed_table_side`).
Where the source says a certificate refines a credited packing, or says it was built from
scratch, `CREDITED` measures it pose by pose against the case's house and the pending entry
nearest it: #505 against Ryan Xu's certificates (T-125) and, at 146, Evan Daniel's
regularized view (T-146); #501 against SQUISH's update and Francisco Couzo's refinement at
155 (T-115, T-128) and Evan Daniel's exact optima at 156 and 211 (T-098).

It reads SQUISH's fourth request of 11 October too, #500's nine certificates at 176,
181, 238, 239, 270, 271, 272, 304 and 305 (``decide-imports --imports '#500'``), in the
review ``review-2026-10-11-upper-bound-imports-500.md``: derived facts, as for #481, read
as their bases state, and ``--upstream`` holds each to the source's ``nNNN.cert.json``
at the pin by `read_squish_json` and its offered side to a row of the source's
``summary.csv``. Where the source names a packing the record retains as a whole or
nearly whole piece (`LINEAGE`: Francisco Couzo's 127 of T-128 in the 176, SQUISH's #481
209 in the 270 and the 304), `patch_lineage` measures it, at `NEAR` and, in its tests,
at a tenth of a unit.

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
every exact checker here; it reads a derived fact with ``sqpack.yamlio``, as every YAML
read in this repository must, and a JSON certificate with the standard library. For each
positive it also measures the least Euclidean distance between squares whose centres lie
within 2 of each other, a different quantity from the separating-axis gap the maintained
routes report and never smaller than it; every other pair is at least ``2 - sqrt(2)``
apart.

Every certificate gets six controls with required outcomes, each a full decision:
a duplicated square and a square moved outside the box (refused); the side shrunk by the
least far-wall clearance (accepted, the box being closed) and by ``10^-40`` more
(refused); and the closest pair, translated into contact (that pair accepted) and then
``10^-30`` of the centre distance further (the certificate refused).

From ``packing/``, with the project interpreter::

    python -m devtools.check_half_angle_area decide [--workers 2] [--json PATH]
    python -m devtools.check_half_angle_area decide-imports [--workers 2] [--json PATH]
        [--imports KEY ...] [--upstream PACKET DIRECTORY ...]
    python -m devtools.check_half_angle_area replay-t128 [--workers 2]

``decide-imports`` holds each import's certificates to the maintained routes' retained
positive inputs and margins, to the side its packet's frozen claim record and register
plan state, and to its printed side: equal to it, or rounding up to it at its places. A
decided count the entry does not cite (#470's 132 and 267) must be absent from the plan's
claim. ``--imports`` selects by key (``#476``, ``#481``, ``#483``, ``#484``, ``#470``,
``trio126``, ``#488``, ``#489``, ``regularized``, ``#503``, ``#504``, ``#505``, ``#501``);
it defaults to the first four, the roster of the first imports review.

``replay-t128`` is the maintained two-route replay of T-128's retained receipt, which
``devtools.couzo_refinement_reports`` has no command for: every job decided again by the
kernel and held to its retained row, as ``check --replay`` does for T-130 and T-131.
"""

from __future__ import annotations

import argparse
import csv
import functools
import gzip
import hashlib
import io
import json
import math
import re
import time
from collections.abc import Callable, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import couzo_followup_reports as t130
from devtools import couzo_refinement_reports as t128
from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import evand_hunt_reports as t131
from devtools import ryxu_arrangement_reports as ryxu
from devtools import squish_followup_packets as squish_update
from devtools import upper_bound_reports as upper
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "frontier/results.yaml"
FRONTIER = ROOT / "frontier"

Point = tuple[Fraction, Fraction]
Square = tuple[Point, Point, Point, Point]
Pose = tuple[Fraction, Fraction, Fraction]
#: A square as every decision reads it: centre ``(x, y)`` and rotation ``(cos, sin)``.
Placed = tuple[Fraction, Fraction, Fraction, Fraction]

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
    #: How many square-to-wall clearances are exactly zero: squares touching the closed box.
    wall_contacts: int = 0


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


def _data_rows(text: str) -> list[list[str]]:
    """The whitespace-split data lines of a text certificate: blank and ``#`` lines skipped."""
    return [
        line.split()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def _square_rows(rows: Sequence[Sequence[str]], n: int) -> tuple[Pose, ...]:
    """Exactly ``n`` rows ``x y t`` after a certificate's header, each read as a pose."""
    if len(rows) != n:
        raise AreaRouteError(f"{len(rows)} square rows for n = {n}")
    poses: list[Pose] = []
    for index, row in enumerate(rows, start=1):
        if len(row) != 3:
            raise AreaRouteError(f"square {index}: {len(row)} fields, not `x y t`")
        x, y, t = (literal(value) for value in row)
        poses.append((x, y, t))
    return tuple(poses)


def parse_certificate(text: str, n: int) -> tuple[Fraction, tuple[Pose, ...]]:
    """The header ``n S`` and exactly ``n`` rows ``x y t``, skipping blank and ``#`` lines."""
    rows = _data_rows(text)
    if not rows or len(rows[0]) != 2 or rows[0][0] != str(n):
        raise AreaRouteError(f"the header is not `{n} S`")
    side = literal(rows[0][1])
    if side <= 0:
        raise AreaRouteError("the side must be positive")
    return side, _square_rows(rows[1:], n)


def parse_sqcert(text: str, n: int) -> tuple[Fraction, tuple[Pose, ...]]:
    """Daniil Ostashev's ``.sqcert`` (#501): ``n N``, ``s S``, then ``n`` rows ``x y t``.

    Evan Daniel's format with its header split over two labelled lines, the labels in that
    order; blank and ``#`` lines are skipped, so the source's ``claimed_s`` and ``delta``
    header comments are not read, and nothing else is allowed.
    """
    rows = _data_rows(text)
    if len(rows) < 2 or rows[0] != ["n", str(n)] or len(rows[1]) != 2 or rows[1][0] != "s":
        raise AreaRouteError(f"the header is not `n {n}` then `s S`")
    side = literal(rows[1][1])
    if side <= 0:
        raise AreaRouteError("the side must be positive")
    return side, _square_rows(rows[2:], n)


def read_evand_cert(raw: bytes, n: int) -> tuple[Fraction, tuple[Pose, ...]]:
    """A pinned upstream ``.cert`` in Evan Daniel's format, as `parse_certificate` reads it."""
    return parse_certificate(raw.decode("utf-8"), n)


def rotation(t: Fraction) -> tuple[Fraction, Fraction]:
    """``(cos theta, sin theta)`` from ``t = tan(theta/2)``, held to the unit circle."""
    q = 1 + t * t
    c, s = (1 - t * t) / q, 2 * t / q
    if c * c + s * s != 1:
        raise AreaRouteError("the half-angle map left the unit circle")
    return c, s


def placed(poses: Sequence[Pose]) -> list[Placed]:
    """Each centre with its exact rotation: the form every decision below reads."""
    return [(x, y, *rotation(t)) for x, y, t in poses]


def unit_basis(c: Fraction, s: Fraction) -> tuple[Fraction, Fraction]:
    """A basis read as stated, refused unless it is a rotation, so the square is a unit one."""
    if c * c + s * s != 1:
        raise AreaRouteError("a stated basis is not a rotation")
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
    return decide_placed(side, placed(poses), measure=measure)


def decide_placed(
    side: Fraction, placements: Sequence[Placed], *, measure: bool = False
) -> Decision:
    """`decide` on squares whose rotation is already exact, as a derived fact states it."""
    squares: list[Square] = []
    clearances: list[Fraction] = []
    far: list[Fraction] = []
    outside = 0
    for x, y, c, s in placements:
        unit_basis(c, s)
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
    for i, (lx, ly, _lc, _ls) in enumerate(placements):
        for j in range(i + 1, len(placements)):
            rx, ry, _rc, _rs = placements[j]
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
        wall_contacts=sum(1 for clearance in clearances if clearance == 0),
    )


def controls(side: Fraction, poses: Sequence[Pose], decision: Decision) -> dict[str, bool]:
    """Each control's outcome; every one must match its required outcome."""
    return controls_placed(side, placed(poses), decision)


def controls_placed(
    side: Fraction, placements: Sequence[Placed], decision: Decision
) -> dict[str, bool]:
    """`controls` on squares whose rotation is already exact."""
    duplicate = list(placements)
    duplicate[1] = duplicate[0]
    outside = list(placements)
    x, y, c0, s0 = outside[0]
    outside[0] = (x + side + 2, y, c0, s0)
    touching = side - decision.far_wall_clearance
    result = {
        "duplicate-square-refused": not decide_placed(side, duplicate).passed,
        "square-outside-refused": not decide_placed(side, outside).passed,
        "side-at-far-wall-contact-accepted": decide_placed(touching, placements).passed,
        "side-past-far-wall-contact-refused": not decide_placed(
            touching - WALL_STEP, placements
        ).passed,
    }
    if decision.closest is None:
        raise AreaRouteError("the pair controls need two squares within 2 of each other")
    _distance, i, j, p, q = decision.closest
    (xi, yi, ci, si), (xj, yj, cj, sj) = placements[i], placements[j]
    shift = (p[0] - q[0], p[1] - q[1])
    contact = corners(xj + shift[0], yj + shift[1], cj, sj)
    left = corners(xi, yi, ci, si)
    result["closest-pair-in-contact-accepted"] = not overlaps(left, contact)
    pushed = list(placements)
    pushed[j] = (
        xj + shift[0] + PAIR_PUSH * (xi - xj),
        yj + shift[1] + PAIR_PUSH * (yi - yj),
        cj,
        sj,
    )
    result["closest-pair-pushed-past-contact-refused"] = not decide_placed(side, pushed).passed
    return result


def _root(value: Fraction) -> str:
    """The square root of a non-negative rational, to seven significant digits."""
    with localcontext() as context:
        context.prec = 40
        return f"{(Decimal(value.numerator) / Decimal(value.denominator)).sqrt():.6e}"


def _text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def verdict(side: Fraction, placements: Sequence[Placed]) -> dict[str, Any]:
    """This route's full verdict on one packing, its margins and its six controls."""
    started = time.monotonic()
    decision = decide_placed(side, placements, measure=True)
    outcomes = controls_placed(side, placements, decision)
    if decision.closest is None:
        raise AreaRouteError("no pair within 2 to measure")
    distance, i, j, _p, _q = decision.closest
    return {
        "side": _text(side),
        "passed": decision.passed,
        "pairs": decision.pairs,
        "clipped_pairs": decision.clipped,
        "overlapping_pairs": decision.overlapping,
        "outside_squares": decision.outside,
        "wall_clearance": _text(decision.wall_clearance),
        "far_wall_clearance": _text(decision.far_wall_clearance),
        "wall_contacts": decision.wall_contacts,
        "least_distance_squared": _text(distance),
        "least_distance": _root(distance),
        "closest_pair": [i, j],
        "controls": outcomes,
        "wall_seconds": round(time.monotonic() - started, 2),
    }


def decide_case(case: Case) -> dict[str, Any]:
    """This route's full verdict on one certificate, its margins and its controls."""
    side, poses = parse_certificate(case.text, case.n)
    return {
        "entry": case.entry,
        "packet": case.packet,
        "n": case.n,
        "poses": [[_text(value) for value in pose] for pose in poses],
        **verdict(side, placed(poses)),
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
    return {
        module.PACKET.name: _totals(kernel.read_xz(module.receipt_path())["cases"])
        for module in (t128, t130, t131)
    }


def _totals(jobs: Sequence[dict[str, Any]]) -> dict[str, Any]:
    return {
        "jobs": len(jobs),
        "pair_decisions": sum(
            job[route]["pairs_tested"] for job in jobs for route in kernel.ROUTES
        ),
        "route_cpu_seconds": round(sum(sum(job["cpu_seconds"].values()) for job in jobs), 2),
        "job_wall_seconds": round(sum(job["wall_seconds"] for job in jobs), 2),
        "longest_job_seconds": round(max(job["wall_seconds"] for job in jobs), 2),
    }


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


# --------------------------------------------------------------------------- 2026-10-10 imports

#: The four upper-bound imports of the 2026-10-10 intake pass, by issue, with their packets.
IMPORTS = {
    "#476": "couzo-exact-certificates-2026-10-09",
    "#481": "squish-481-third-request-2026-10-09",
    "#483": "ebdeleeuw-n70-refinement-2026-10-10",
    "#484": "fang-two-wedge-certificates-2026-10-10",
}
#: The two imports reviewed after them: the exact witnesses derived from Mishapolk's
#: decimal poses (#470), and Evan Daniel's ``n126_xu.cert``, which no issue reports.
LATER_IMPORTS = {
    "#470": "mishapolk-decimal-poses-2026-10-09",
    "trio126": "evand-trio126-2026-10-09",
}
#: The two imports filed after the sweep: Francisco Couzo's certificates of #488 and
#: Evan Daniel's Hunt 3 certificates of #489, both retained in Evan Daniel's text format.
IMPORTS_488_489 = {
    "#488": "couzo-certificates-2026-10-10",
    "#489": "evand-record-hunt3-2026-10-10",
}
#: Evan Daniel's display-regularized record lists, which no issue reports: fifteen
#: certificates in his text format, each retained as its original gzip.
IMPORTS_REGULARIZED = {"regularized": "evand-regularized-2026-10-10"}
#: PingYou Ltd's two certificates of 11 October, #503 at 207 and #504 at 153, each kept
#: as a derived fact beside the source's own corners witness, which the packet pins.
IMPORTS_503_504 = {
    "#503": "pingyou-n207-certificate-2026-10-11",
    "#504": "pingyou-n153-certificate-2026-10-11",
}
#: The two other releases of 11 October: Robert Barnett's refinements of Ryan Xu's
#: packings at 146 and 261 (#505), kept as derived facts since the source states no
#: licence, with five superseded certificates the issue excludes beside them; and Daniil
#: Ostashev's three record packings at 155, 156 and 211 (#501), retained byte for byte
#: under the source's MIT licence in its own sqcert format.
IMPORTS_505_501 = {
    "#505": "barnett-refinements-2026-10-11",
    "#501": "dostashev-records-2026-10-11",
}
#: SQUISH's fourth request of 11 October (#500): nine certificates from Mondrian
#: composition, at 176, 181, 238, 239, 270, 271, 272, 304 and 305, each kept as a
#: derived fact beside the digest of its pinned ``nNNN.cert.json``; no upstream byte is
#: retained, as for #481, and the same SQUISH JSON reader holds each fact to its pin.
IMPORTS_500 = {"#500": "squish-500-fourth-request-2026-10-11"}
#: Francisco Couzo's #506 of 11 October: eleven certificates in Evan Daniel's text format
#: retained as factual data at 337078c, 304 and 305 in the case corpus and 338, 339, 344,
#: 375, 376, 378, 379, 380 and 381 beyond it, each read by this route's own parser.
IMPORTS_506 = {"#506": "couzo-certificates-2026-10-11"}
ALL_IMPORTS = {
    **IMPORTS,
    **LATER_IMPORTS,
    **IMPORTS_488_489,
    **IMPORTS_REGULARIZED,
    **IMPORTS_503_504,
    **IMPORTS_505_501,
    **IMPORTS_500,
    **IMPORTS_506,
}
#: Imports decided over their whole replayed roster rather than the counts the entry
#: cites: #470's README-printed 132 and 267 are certified beside the issue's 28.
WHOLE_ROSTER = frozenset({"#470"})
#: The imported certificates measured against the certificates whose arrangements they
#: would be credited to: n126_xu against Ryan Xu's (T-125), and #470 at the two counts
#: where it is the smallest side, 103 against Ryan Xu's and 258 against SQUISH's (T-115).
#: A certificate the register types as a regularization is measured against the packing
#: its entry's `regularizations` name instead (`regularized_credit`).
#: #505's two, which the source calls refinements of Ryan Xu's packings, against his
#: certificates, and at 146 against Evan Daniel's regularized view of the same packing,
#: which the source compares with; #501's three, which the source says were built from
#: scratch, against each case's house and the pending entry nearest it.
CREDITED: dict[tuple[str, int], tuple[str, ...]] = {
    ("trio126", 126): ("T-125",),
    ("#470", 103): ("T-125",),
    ("#470", 258): ("T-115",),
    ("#505", 146): ("T-125", "T-146"),
    ("#505", 261): ("T-125",),
    ("#501", 155): ("T-115", "T-128"),
    ("#501", 156): ("T-098",),
    ("#501", 211): ("T-098",),
    # Couzo's #506 says its 304 and 305 start from SQUISH's #500 Mondrian packings and
    # its 344 from Kevin Fang's #484, whose arrangement Evan Daniel's Hunt 3 (#489) also
    # moved; a key that is no register entry names the import whose certificate it is.
    ("#506", 304): ("#500",),
    ("#506", 305): ("#500",),
    ("#506", 344): ("#484", "#489"),
}
WEB = ROOT / "resources/web"
REPO = ROOT.parent


@functools.cache
def regularized_credit() -> dict[tuple[str, int], tuple[str, ...]]:
    """The packing each regularized import certificate is credited to, read from the register.

    A register entry whose `artifacts` cite an import's packet and that carries
    `regularizations` says, count by count, which result's packing (`of`) its certificate
    regularizes; that result is what the certificate is measured against, so the third
    route measures each view against the packing the record credits. For Evan Daniel's
    display-regularized lists that is T-146: Ryan Xu's packings (T-125), Mishapolk's
    refinements at 103 and 258 (T-138) and SQUISH's third request (T-136).
    """
    document = load_yaml(RESULTS.read_text(encoding="utf-8"))
    credit: dict[tuple[str, int], tuple[str, ...]] = {}
    for key, packet in ALL_IMPORTS.items():
        prefix = f"{(WEB / packet).relative_to(REPO).as_posix()}/"
        for result in document["results"]:
            if not any(str(path).startswith(prefix) for path in result["artifacts"]):
                continue
            for item in result.get("regularizations") or ():
                credit[key, int(item["n"])] = (str(item["of"]),)
    return credit


def credited(issue: str, n: int) -> tuple[str, ...]:
    """The register entries an import's certificate at ``n`` is measured against: the
    fixed pairs of `CREDITED`, or the packing the register's `regularizations` name."""
    return CREDITED.get((issue, n)) or regularized_credit().get((issue, n), ())


PLAN_CLAIM = re.compile(r"s\((\d+)\)\s*<=\s*(\d+(?:\.\d+|/\d+))")
_DECIMALS = re.compile(r"[0-9]+\.([0-9]+)")
_BLOB = re.compile(r"https://github\.com/[^/]+/[^/]+/blob/([0-9a-f]{40})/([^?#]+)")


@dataclass(frozen=True, slots=True)
class Imported:
    """One certificate an import's register entry would cite, as this route read it."""

    issue: str
    packet: str
    n: int
    read: str
    side: Fraction
    placements: tuple[Placed, ...]


def _unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    keys = [key for key, _value in pairs]
    if len(keys) != len(set(keys)):
        raise AreaRouteError("a JSON object names a key twice")
    return dict(pairs)


def _json_object(raw: bytes, n: int) -> dict[str, Any]:
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique)
    if type(value) is not dict or type(value.get("n")) is not int or value["n"] != n:
        raise AreaRouteError(f"n={n}: not a JSON certificate of {n} squares")
    if type(value.get("squares")) is not list or len(value["squares"]) != n:
        raise AreaRouteError(f"n={n}: the squares are not a list of {n}")
    return value


def _scalar(value: object, where: str) -> Fraction:
    """A rational as a JSON or YAML document states it: a literal string, or an integer."""
    if type(value) is int:
        return Fraction(value)
    if type(value) is not str:
        raise AreaRouteError(f"{where}: not a rational")
    return literal(value)


def _side_and_rows(value: dict[str, Any], n: int) -> tuple[Fraction, tuple[Pose, ...]]:
    """``s_exact`` and the ``[x, y, t]`` rows of a SQUISH-shaped JSON certificate."""
    side = _scalar(value.get("s_exact"), f"n={n} side")
    poses: list[Pose] = []
    for index, square in enumerate(value["squares"], start=1):
        if type(square) is not list or len(square) != 3:
            raise AreaRouteError(f"n={n} square {index}: not [x, y, t]")
        x, y, t = (_scalar(item, f"n={n} square {index}") for item in square)
        poses.append((x, y, t))
    if side <= 0:
        raise AreaRouteError("the side must be positive")
    return side, tuple(poses)


def read_squish_json(raw: bytes, n: int) -> tuple[Fraction, tuple[Pose, ...]]:
    """SQUISH's JSON: ``s_exact`` and ``[x, y, t]`` strings, centres in ``[0, S]^2``.

    Its display fields, ``s_decimal`` and ``note``, are not read.
    """
    return _side_and_rows(_json_object(raw, n), n)


#: What PingYou Ltd's JSON adds to SQUISH's rows: the source's prose, its guard
#: dilation, its undilated floating-point side and its construction record. None is
#: read; the side is ``s_exact`` and the poses are the rows.
PINGYOU_UNREAD = frozenset({"note", "dilation_exact", "raw_side", "provenance"})


def read_pingyou_json(raw: bytes, n: int) -> tuple[Fraction, tuple[Pose, ...]]:
    """PingYou Ltd's JSON (#503, #504): SQUISH's ``s_exact`` and ``[x, y, t]`` rows.

    The fields of `PINGYOU_UNREAD` are left unread; any field beyond those, ``n``,
    ``s_exact`` and ``squares`` is refused, since this reader does not know what it
    would mean.
    """
    value = _json_object(raw, n)
    unknown = set(value) - {"n", "s_exact", "squares"} - PINGYOU_UNREAD
    if unknown:
        raise AreaRouteError(f"n={n}: fields this reader does not know: {sorted(unknown)}")
    return _side_and_rows(value, n)


#: The frame a corners witness must state; an angle unit does not apply to corners.
CORNER_FRAME = {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "not-applicable"}


def read_witness_corners(raw: bytes, n: int) -> tuple[Fraction, tuple[Placed, ...]]:
    """A rational ``corners`` Witness/v2, each square read from its four corners.

    The centre is the corners' mean and the rotation the first edge, corner 1 less
    corner 0, held to the unit circle; the other three edges must be that edge's
    successive quarter turns, so the four corners are one unit square's, counter-
    clockwise from the corner the maintained adapter writes first. The envelope's
    ``softschema`` block and any ``claim``, ``source`` or ``certificate`` block are not
    read. A square whose corners start from another vertex is the same square at a
    rotation a quarter turn away, and is read as that rotation: a comparison with a
    certificate's poses holds the witness to the convention the certificate's bases use.
    """
    document = load_yaml(raw.decode("utf-8"))
    witness = document.get("witness") if type(document) is dict else None
    if type(witness) is not dict:
        raise AreaRouteError(f"n={n}: no witness")
    if (
        witness.get("n") != n
        or witness.get("representation") != "corners"
        or witness.get("scalar") != {"kind": "rational"}
        or _scalar(witness.get("square_size"), "square size") != 1
        or witness.get("coordinates") != CORNER_FRAME
    ):
        raise AreaRouteError(f"n={n}: not a rational unit corners witness in [0, S]^2")
    side = _scalar(witness.get("side"), f"n={n} side")
    squares = witness.get("squares")
    if side <= 0 or type(squares) is not list or len(squares) != n:
        raise AreaRouteError(f"n={n}: a positive side and {n} squares")
    placements: list[Placed] = []
    for index, square in enumerate(squares, start=1):
        where = f"n={n} square {index}"
        corners_stated = square.get("corners") if type(square) is dict else None
        if (
            type(square) is not dict
            or set(square) != {"id", "corners"}
            or square["id"] != index
            or type(corners_stated) is not list
            or len(corners_stated) != 4
            or any(type(point) is not list or len(point) != 2 for point in corners_stated)
        ):
            raise AreaRouteError(f"{where}: not four corners")
        points = [(_scalar(u, where), _scalar(v, where)) for u, v in corners_stated]
        c, s = unit_basis(points[1][0] - points[0][0], points[1][1] - points[0][1])
        edges = [
            (points[(k + 1) % 4][0] - points[k][0], points[(k + 1) % 4][1] - points[k][1])
            for k in range(4)
        ]
        if edges != [(c, s), (-s, c), (-c, -s), (s, -c)]:
            raise AreaRouteError(f"{where}: the corners are not one unit square's, in order")
        x = sum((u for u, _v in points), Fraction(0)) / 4
        y = sum((v for _u, v in points), Fraction(0)) / 4
        placements.append((x, y, c, s))
    return side, tuple(placements)


def read_centred_json(raw: bytes, n: int) -> tuple[Fraction, tuple[Pose, ...]]:
    """#483's JSON: ``side`` and ``{x, y, t}`` squares, centres in ``[-S/2, S/2]^2``.

    Each centre is moved by ``S/2`` into ``[0, S]^2``. The ``schema`` label is not read.
    """
    value = _json_object(raw, n)
    if value.get("coordinate_system") != "centered":
        raise AreaRouteError(f"n={n}: not a centred certificate")
    side = _scalar(value.get("side"), f"n={n} side")
    if side <= 0:
        raise AreaRouteError("the side must be positive")
    poses: list[Pose] = []
    for index, square in enumerate(value["squares"], start=1):
        if type(square) is not dict or set(square) != {"x", "y", "t"}:
            raise AreaRouteError(f"n={n} square {index}: not exactly x, y and t")
        x, y, t = (_scalar(square[key], f"n={n} square {index}") for key in ("x", "y", "t"))
        poses.append((x + side / 2, y + side / 2, t))
    return side, tuple(poses)


def read_fact(text: str, n: int) -> tuple[Fraction, tuple[Placed, ...]]:
    """A derived fact, a rational centre-basis Witness/v2, read as its bases state them."""
    document = load_yaml(text)
    witness = document.get("witness") if type(document) is dict else None
    if type(witness) is not dict:
        raise AreaRouteError(f"n={n}: no witness")
    coordinates = witness.get("coordinates")
    if (
        witness.get("n") != n
        or witness.get("representation") != "center-basis"
        or witness.get("scalar") != {"kind": "rational"}
        or _scalar(witness.get("square_size"), "square size") != 1
        or type(coordinates) is not dict
        or coordinates.get("origin") != "lower-left"
        or coordinates.get("axes") != "x-right-y-up"
    ):
        raise AreaRouteError(f"n={n}: not a rational unit centre-basis witness in [0, S]^2")
    side = _scalar(witness.get("side"), f"n={n} side")
    squares = witness.get("squares")
    if side <= 0 or type(squares) is not list or len(squares) != n:
        raise AreaRouteError(f"n={n}: a positive side and {n} squares")
    placements: list[Placed] = []
    for index, square in enumerate(squares, start=1):
        where = f"n={n} square {index}"
        if (
            type(square) is not dict
            or set(square) != {"id", "center", "basis"}
            or square["id"] != index
            or type(square["center"]) is not list
            or type(square["basis"]) is not list
            or len(square["center"]) != 2
            or len(square["basis"]) != 2
        ):
            raise AreaRouteError(f"{where}: not one exact pose")
        x, y = (_scalar(value, where) for value in square["center"])
        c, s = (_scalar(value, where) for value in square["basis"])
        placements.append((x, y, *unit_basis(c, s)))
    return side, tuple(placements)


_POSE_SIDE = re.compile(r"s: ([0-9]+\.[0-9]+)")
_POSE_SQUARE = re.compile(
    r"Square ([1-9][0-9]*): x=(-?[0-9]+\.[0-9]+), y=(-?[0-9]+\.[0-9]+), deg=(-?[0-9]+\.[0-9]+)"
)
#: The angles in [-180, 180) degrees whose half-angle tangent is rational: tan 0 and tan 45.
RATIONAL_HALF_ANGLES = {
    Fraction(0): Fraction(0),
    Fraction(90): Fraction(1),
    Fraction(-90): Fraction(-1),
}
#: Working digits beyond the rounding place, tried in turn until the floor is decided.
TANGENT_GUARDS = (40, 120, 400)


def read_decimal_pose(raw: bytes, n: int) -> tuple[str, tuple[Pose, ...]]:
    """Ellsworth's decimal text (#470): ``s: SIDE``, then ``Square K: x=X, y=Y, deg=D``.

    The squares are ``K = 1..n`` in order, centres in ``[-s/2, s/2]^2`` and angles in
    degrees, each a plain decimal read exactly; blank lines are skipped and nothing else
    is allowed. Returns the side as printed and each ``(x, y, degrees)``.
    """
    lines = [line.strip() for line in raw.decode("utf-8").splitlines() if line.strip()]
    side = _POSE_SIDE.fullmatch(lines[0]) if lines else None
    if side is None:
        raise AreaRouteError(f"n={n}: the first line is not `s: SIDE`")
    if len(lines) - 1 != n:
        raise AreaRouteError(f"n={n}: {len(lines) - 1} square lines")
    squares: list[Pose] = []
    for index, line in enumerate(lines[1:], start=1):
        match = _POSE_SQUARE.fullmatch(line)
        if match is None or int(match.group(1)) != index:
            raise AreaRouteError(f"n={n}: line {index + 1} is not square {index}")
        x, y, degrees = (literal(match.group(group)) for group in (2, 3, 4))
        squares.append((x, y, degrees))
    return side.group(1), tuple(squares)


@functools.cache
def _pi(digits: int) -> Decimal:
    """Pi at ``digits`` significant digits, by Machin's formula."""
    with localcontext() as context:
        context.prec = digits + 5
        tiny = Decimal(10) ** -(digits + 5)

        def arctan_inverse(k: int) -> Decimal:
            power = total = Decimal(1) / k
            index, sign = 1, 1
            while True:
                power /= k * k
                index += 2
                sign = -sign
                term = power / index
                if term < tiny:
                    return total
                total += sign * term

        return +(16 * arctan_inverse(5) - 4 * arctan_inverse(239))


def _tan_half(turn: Fraction, digits: int) -> Fraction:
    """``tan(turn/2 degrees)`` at about ``digits`` significant digits, by Taylor series."""
    with localcontext() as context:
        context.prec = digits
        tiny = Decimal(10) ** -(digits + 5)
        half = Decimal(turn.numerator) * _pi(digits) / (360 * Decimal(turn.denominator))
        square = half * half
        sine = sine_term = half
        cosine = cosine_term = Decimal(1)
        k = 1
        while abs(sine_term) > tiny or abs(cosine_term) > tiny:
            cosine_term = -cosine_term * square / ((2 * k - 1) * (2 * k))
            sine_term = -sine_term * square / ((2 * k) * (2 * k + 1))
            cosine += cosine_term
            sine += sine_term
            k += 1
        return Fraction(sine / cosine)


def half_angle_floor(degrees: Fraction, places: int) -> Fraction:
    """``tan(theta/2)`` for ``theta`` in degrees, rounded down at ``places`` decimals.

    The angle is reduced exactly to [-180, 180). The tangent is rational there only at 0
    and +-90 degrees; elsewhere it is irrational, so no rounding point is ever hit and a
    narrow enough bound decides the floor. The bound allows ``10^(10 - digits)`` times
    ``(1 + |t|)(1 + t^2)`` either side of the computed tangent, orders of magnitude more
    than the error of ``digits``-digit arithmetic, and the working digits rise until both
    ends floor alike.
    """
    turn = (degrees + 180) % 360 - 180
    if turn == -180:
        raise AreaRouteError(f"{degrees} degrees has no finite half-angle tangent")
    if turn in RATIONAL_HALF_ANGLES:
        return RATIONAL_HALF_ANGLES[turn]
    scale = 10**places
    for guard in TANGENT_GUARDS:
        digits = places + guard
        value = _tan_half(turn, digits)
        error = Fraction(1, 10 ** (digits - 10)) * (1 + abs(value)) * (1 + value * value)
        low, high = math.floor((value - error) * scale), math.floor((value + error) * scale)
        if low == high:
            return Fraction(low, scale)
    raise AreaRouteError(f"no precision decides tan({degrees}/2 degrees) at {places} places")


def derive_decimal_pose(raw: bytes, row: dict[str, Any]) -> tuple[Fraction, tuple[Placed, ...]]:
    """#470's exact witness, derived again from its decimal pose by this route's arithmetic.

    The side is the printed ceiling ``S`` the row offers, which must be the file's printed
    side ``s`` rounded up at its places, and the declared dilation must be ``S/s``. Each
    centre is dilated by ``S/s`` about the box centre and moved by ``S/2`` into
    ``[0, S]^2``; each ``t`` is `half_angle_floor` at the declared places.
    """
    n = row["n"]
    printed_text, squares = read_decimal_pose(raw, n)
    printed, side = literal(printed_text), literal(row["offered"])
    if not admitted(printed, row["offered"]):
        raise AreaRouteError(f"n={n}: {row['offered']} is not {printed_text} rounded up")
    options = {option["name"]: option["value"] for option in row.get("options", [])}
    if set(options) != {"dilation", "half_angle_places"}:
        raise AreaRouteError(f"n={n}: not exactly a dilation and half-angle places")
    dilation = side / printed
    if literal(options["dilation"]) != dilation:
        raise AreaRouteError(f"n={n}: the declared dilation is not the ceiling over the side")
    places = int(options["half_angle_places"])
    half = side / 2
    placements = tuple(
        (
            dilation * x + half,
            dilation * y + half,
            *rotation(half_angle_floor(degrees, places)),
        )
        for x, y, degrees in squares
    )
    return side, placements


def stored_bytes(path: Path) -> bytes:
    """A packet file's bytes as stored, gzip or not: what an upstream copy must equal."""
    if path.is_symlink() or not path.resolve().is_relative_to(REPO.resolve()):
        raise AreaRouteError(f"{path}: not a private repository file")
    return path.read_bytes()


def packet_bytes(path: Path) -> bytes:
    """A packet file's content, decompressed here where it is stored as gzip.

    That is the deterministic copy ``X.gz`` a packet keeps of ``X``, or an upstream file
    whose own name ends in ``.gz``, retained as its original gzip.
    """
    stored = path if path.is_file() else path.with_name(path.name + ".gz")
    raw = stored_bytes(stored)
    return gzip.decompress(raw) if stored.name.endswith(".gz") else raw


def _declaration(packet: Path) -> dict[str, Any]:
    return json.loads((packet / "acquisition/report.json").read_text(encoding="utf-8"))


def roster(issue: str, declaration: dict[str, Any]) -> list[int]:
    """The counts this route decides: those the entry cites, or the whole replayed roster."""
    return declaration["replayed" if issue in WHOLE_ROSTER else "requested"]


def import_cases(keys: Sequence[str] = tuple(IMPORTS)) -> list[Imported]:
    """Every certificate the selected imports' entries would cite, after each packet's custody.

    ``upper_bound_reports.read_facts`` admits each packet's bytes, as the packet modules
    do for the first roster; this route then reads the files itself. A count of #484 is
    read from its ``.cert`` and held to its ``.cert.json`` by this route's own readers.
    #470 is read over its whole replayed roster (`WHOLE_ROSTER`).
    """
    found: list[Imported] = []
    for issue in keys:
        declaration = _admitted(issue)
        counts = roster(issue, declaration)
        found.extend(
            read_import(issue, row) for row in declaration["certificates"] if row["n"] in counts
        )
    return found


@functools.cache
def _admitted(issue: str) -> dict[str, Any]:
    """The import's declaration, once ``upper_bound_reports.read_facts`` admits its packet."""
    packet = WEB / ALL_IMPORTS[issue]
    upper.read_facts(packet)
    return _declaration(packet)


def read_import(issue: str, row: dict[str, Any]) -> Imported:
    """One declared certificate of an admitted import, read by this route's own readers."""
    name = ALL_IMPORTS[issue]
    packet = WEB / name
    n = row["n"]
    if "fact" in row:
        read = row["fact"]
        side, placements = read_fact(packet_bytes(packet / read).decode("utf-8"), n)
        return Imported(issue, name, n, read, side, placements)
    reader = RETAINED_READERS.get(row["format"])
    if reader is None:
        raise AreaRouteError(f"{issue} n={n}: no reader for {row['format']}")
    record = json.loads((packet / "acquisition/sources.json").read_text(encoding="utf-8"))
    source = REPO / record["sources"][0]["archived_path"]
    read = (source / row["path"]).relative_to(packet).as_posix()
    side, poses = reader(packet_bytes(source / row["path"]).decode("utf-8"), n)
    for other in row.get("same_packing", []):
        if other["format"] != "squish-json":
            raise AreaRouteError(f"{issue} n={n}: no reader for {other['format']}")
        copy = read_squish_json(packet_bytes(source / other["path"]), n)
        if copy != (side, poses):
            raise AreaRouteError(f"{issue} n={n}: {other['path']} differs")
    return Imported(issue, name, n, read, side, tuple(placed(poses)))


#: Readers of a certificate a packet retains, by the declared format: Evan Daniel's text
#: and Daniil Ostashev's sqcert, each the header then ``x y t`` rows.
RETAINED_READERS: dict[str, Callable[[str, int], tuple[Fraction, tuple[Pose, ...]]]] = {
    "evand-cert": parse_certificate,
    "sqcert": parse_sqcert,
}


def import_packing(issue: str) -> Callable[[int], tuple[Fraction, tuple[Placed, ...]]]:
    """The reader of an import's certificate at ``n``, any count it declares, for credit."""

    def read(n: int) -> tuple[Fraction, tuple[Placed, ...]]:
        rows = [row for row in _admitted(issue)["certificates"] if row["n"] == n]
        if not rows:
            raise AreaRouteError(f"{issue} declares no certificate at n={n}")
        case = read_import(issue, rows[0])
        return case.side, case.placements

    return read


def decide_import(case: Imported) -> dict[str, Any]:
    """This route's verdict on one imported certificate."""
    return {
        "issue": case.issue,
        "packet": case.packet,
        "n": case.n,
        "read": case.read,
        "placements": [[_text(value) for value in square] for square in case.placements],
        **verdict(case.side, case.placements),
    }


def admitted(side: Fraction, offered: str) -> bool:
    """Whether ``side`` is the printed side, or a decimal print is ``side`` rounded up there."""
    printed = literal(offered)
    if printed == side:
        return True
    match = _DECIMALS.fullmatch(offered)
    if match is None:
        return False
    scale = 10 ** len(match.group(1))
    return printed == Fraction(-(-side.numerator * scale // side.denominator), scale)


def import_positives(
    keys: Sequence[str] = tuple(IMPORTS),
) -> dict[tuple[str, int], dict[str, Any]]:
    """Each retained positive job of the selected imports, as `upper_bound_reports` admits."""
    rows: dict[tuple[str, int], dict[str, Any]] = {}
    for name in (ALL_IMPORTS[key] for key in keys):
        for n, row in upper.check_certification(WEB / name).items():
            rows[name, n] = row
    return rows


def import_receipt_totals(keys: Sequence[str] = tuple(IMPORTS)) -> dict[str, dict[str, Any]]:
    """What each selected import's retained receipt, whole or by count, records in total."""
    totals: dict[str, dict[str, Any]] = {}
    for name in (ALL_IMPORTS[key] for key in keys):
        paths = sorted((WEB / name / "receipts").glob("exact-certification*.json.xz"))
        totals[name] = _totals([job for path in paths for job in kernel.read_xz(path)["cases"]])
    return totals


def plan_claims(keys: Sequence[str] = tuple(IMPORTS)) -> dict[str, dict[int, Fraction]]:
    """Every ``s(n) <= v`` each selected import's register plan would write, exactly."""
    claims: dict[str, dict[int, Fraction]] = {}
    for name in (ALL_IMPORTS[key] for key in keys):
        claim = upper.register_plan(WEB / name)["results.yaml"]["claim"]
        printed = PLAN_CLAIM.findall(" ".join(str(claim).split()))
        claims[name] = {int(n): literal(value) for n, value in printed}
    return claims


def compare_import(
    row: dict[str, Any],
    maintained: dict[str, Any],
    claimed: Fraction | None,
    frozen: dict[str, Any],
    offered: str,
    *,
    cited: bool = True,
) -> list[str]:
    """Every way this route's reading and margins disagree with the import's record.

    A count the entry does not cite (``cited`` false) must be absent from the plan's claim.
    """
    problems: list[str] = []
    where = f"{row['issue']} n={row['n']} ({row['packet']})"
    side = literal(row["side"])
    inputs = maintained["checker_input"]
    if literal(inputs["side"]) != side:
        problems.append(f"{where}: side differs from the maintained routes' input")
    mine = [tuple(literal(value) for value in square) for square in row["placements"]]
    theirs = [(literal(x), literal(y), *rotation(literal(t))) for x, y, t in inputs["poses"]]
    if mine != theirs:
        problems.append(f"{where}: a pose differs from the maintained routes' input")
    if cited and claimed != side:
        problems.append(f"{where}: the register plan's claim is not the exact side")
    if not cited and claimed is not None:
        problems.append(f"{where}: the register plan claims a count its entry does not cite")
    if literal(frozen["exact_side"]) != side or frozen["offered_side"] != offered:
        problems.append(f"{where}: the frozen claim record states another side")
    if not admitted(side, offered):
        problems.append(
            f"{where}: the side is neither the printed {offered} nor rounds up to it"
        )
    distance = literal(row["least_distance_squared"])
    for route in kernel.ROUTES:
        found = maintained[route]
        if found["verification_passed"] is not row["passed"]:
            problems.append(f"{where}: {route} verdict differs")
        if literal(found["minimum_containment_clearance"]) != literal(row["wall_clearance"]):
            problems.append(f"{where}: {route} wall clearance differs from h-extent clearance")
        gap = literal(found["minimum_best_pair_gap"])
        if gap > 0 and gap * gap > distance:
            problems.append(f"{where}: {route} separating gap exceeds the Euclidean distance")
    if not row["passed"] or not all(row["controls"].values()):
        problems.append(f"{where}: a positive or control missed its required outcome")
    return problems


UPSTREAM_READERS = {
    "squish-json": read_squish_json,
    "centred-json": read_centred_json,
    "pingyou-json": read_pingyou_json,
    "evand-cert": read_evand_cert,
}
#: Readers of a pinned file a derived fact's row names as stating the same packing,
#: each returning the packing in placed form.
SAME_PACKING_READERS: dict[str, Callable[[bytes, int], tuple[Fraction, tuple[Placed, ...]]]] = {
    "witness-corners": read_witness_corners,
}


def printed_rows(table: bytes, path: str) -> list[list[str]]:
    """The rows of a file a side is printed in: CSV, or a Markdown table's cells."""
    text = table.decode("utf-8")
    if path.endswith(".md"):
        return [
            [cell.strip() for cell in line.strip().strip("|").split("|")]
            for line in text.splitlines()
            if line.strip().startswith("|")
        ]
    return [line for line in csv.reader(io.StringIO(text)) if line]


def printed_json_side(
    packet: Path, row: dict[str, Any], directory: Path
) -> tuple[int, list[str]]:
    """Hold a retained certificate's offered side to the JSON its row says prints it.

    Evan Daniel's regularized lists print each certificate's exact side as ``S_cert`` in
    a gzipped JSON beside it, which the row names as ``printed_in``. Where that is a JSON
    at the pin, the copy fetched into ``directory`` must be the packet's retained file,
    byte for byte, and its ``S_cert`` must be the side the row offers, for the row's
    count. Any other ``printed_in`` is not a JSON print and is left alone. Returns the
    number of printed sides checked, 0 or 1, and every disagreement.
    """
    blob = _BLOB.fullmatch(row.get("printed_in", ""))
    if blob is None or not blob.group(2).endswith((".json", ".json.gz")):
        return 0, []
    record = json.loads((packet / "acquisition/sources.json").read_text(encoding="utf-8"))
    source = record["sources"][0]
    path = blob.group(2)
    problem = _printed_json_problem(
        row,
        path,
        directory / path,
        REPO / source["archived_path"] / path,
        at_pin=blob.group(1) == source["source_commit"],
    )
    return (0, [f"{packet.name} n={row['n']}: {problem}"]) if problem else (1, [])


def _printed_json_problem(
    row: dict[str, Any], path: str, fetched: Path, retained: Path, *, at_pin: bool
) -> str | None:
    """What is wrong with the JSON print of one row's side, or None."""
    if not at_pin:
        return "the side is printed at another commit"
    if not fetched.is_file() or not retained.is_file():
        return f"{path} is not both retained and fetched"
    raw = fetched.read_bytes()
    if raw != stored_bytes(retained):
        return f"the retained {path} differs"
    text = gzip.decompress(raw) if path.endswith(".gz") else raw
    value = json.loads(text.decode("utf-8"), object_pairs_hook=_unique)
    n = row["n"]
    if type(value) is not dict or value.get("n") != n or type(value.get("S_cert")) is not str:
        return f"{path} prints no S_cert for {n} squares"
    if literal(value["S_cert"]) != literal(row["offered"]):
        return f"{path} prints another side than the row offers"
    return None


def printed_table_side(
    packet: Path, row: dict[str, Any], directory: Path, pinned: dict[str, str]
) -> tuple[int, list[str]]:
    """Hold a retained certificate's offered side to the table its row says prints it.

    Where ``printed_in`` names a Markdown or CSV file at the pin, such as Daniil
    Ostashev's README (#501), the copy fetched into ``directory`` must be the packet's
    own: its retained copy, byte for byte, or else the digest the packet pins; and the
    offered side must be a cell of a row of that table for the row's count, as
    `upstream_problems` holds a derived fact's print. A JSON print is `printed_json_side`'s
    and is left alone here. Returns the number of printed sides checked, 0 or 1, and every
    disagreement.
    """
    blob = _BLOB.fullmatch(row.get("printed_in", ""))
    if blob is None or blob.group(2).endswith((".json", ".json.gz")):
        return 0, []
    record = json.loads((packet / "acquisition/sources.json").read_text(encoding="utf-8"))
    source = record["sources"][0]
    path = blob.group(2)
    problem = _printed_table_problem(
        row,
        path,
        directory / path,
        REPO / source["archived_path"] / path,
        pinned.get(path),
        at_pin=blob.group(1) == source["source_commit"],
    )
    return (0, [f"{packet.name} n={row['n']}: {problem}"]) if problem else (1, [])


def _printed_table_problem(
    row: dict[str, Any],
    path: str,
    fetched: Path,
    retained: Path,
    digest: str | None,
    *,
    at_pin: bool,
) -> str | None:
    """What is wrong with the table print of one row's side, or None."""
    if not at_pin:
        return "the side is printed at another commit"
    if not fetched.is_file():
        return f"no upstream {path} in {fetched.parent}"
    raw = fetched.read_bytes()
    if retained.is_file():
        if raw != stored_bytes(retained):
            return f"the retained {path} differs"
    elif digest != hashlib.sha256(raw).hexdigest():
        return f"{path} is neither retained nor the file the packet pins"
    count, offered = str(row["n"]), row["offered"]
    if not any(line[0] == count and offered in line for line in printed_rows(raw, path)):
        return f"{path} does not print the side"
    return None


def upstream_problems(
    packet: Path, directory: Path, counts: Sequence[int] | None = None
) -> tuple[int, list[str]]:
    """Hold each certificate to the upstream file it was derived or retained from.

    ``directory`` holds the source's files fetched at the pinned commit. Where a count
    has a derived fact, its upstream file must have the SHA-256 the packet pins and must
    state the packing the fact states, read by this route's own reader (`UPSTREAM_READERS`)
    or, for #470's decimal poses, derived again by `derive_decimal_pose`; where the row
    names the file its side is printed in, that file must be there too, at its pinned
    digest, and the printed side must be a cell of its row for the count, as a retained
    certificate's JSON print must be. Where the packet retains the certificate, the
    retained bytes must be the upstream file's, as stored for an upstream gzip, and a
    side printed in a JSON at the pin must be the one the row offers
    (`printed_json_side`), or printed in a Markdown or CSV table at the pin must be a cell
    of its row for the count (`printed_table_side`). ``counts`` defaults to the requested
    ones.
    Returns the number of checks made, certificates and printed sides, and every
    disagreement.
    """
    declaration = _declaration(packet)
    record = json.loads((packet / "acquisition/sources.json").read_text(encoding="utf-8"))
    source = record["sources"][0]
    pinned = {item["path"]: item["sha256"] for item in source["pinned_only"]}
    held = 0
    problems: list[str] = []

    def upstream_bytes(path: str) -> bytes | None:
        target = directory / path
        if not target.is_file():
            problems.append(f"{packet.name}: no upstream {path} in {directory}")
            return None
        return target.read_bytes()

    def pinned_bytes(path: str) -> bytes | None:
        raw = upstream_bytes(path)
        if raw is not None and pinned.get(path) != hashlib.sha256(raw).hexdigest():
            problems.append(f"{packet.name}: {path} is not the file the packet pins")
            return None
        return raw

    for row in declaration["certificates"]:
        n = row["n"]
        if n not in (declaration["requested"] if counts is None else counts):
            continue
        if "fact" not in row:
            raw = upstream_bytes(row["path"])
            if raw is None:
                continue
            retained = REPO / source["archived_path"] / row["path"]
            # An upstream gzip is retained as its original bytes, so those are compared.
            kept = (
                stored_bytes(retained)
                if row["path"].endswith(".gz")
                else packet_bytes(retained)
            )
            if raw != kept:
                problems.append(f"{packet.name} n={n}: the retained {row['path']} differs")
            held += 1
            for printed, printed_problems in (
                printed_json_side(packet, row, directory),
                printed_table_side(packet, row, directory, pinned),
            ):
                held += printed
                problems += printed_problems
            continue
        raw = pinned_bytes(row["path"])
        if raw is None:
            continue
        fact = read_fact(packet_bytes(packet / row["fact"]).decode("utf-8"), n)
        try:
            if row["format"] == "decimal-dilation":
                stated = derive_decimal_pose(raw, row)
            else:
                side, poses = UPSTREAM_READERS[row["format"]](raw, n)
                stated = side, tuple(placed(poses))
        except AreaRouteError as error:
            problems.append(f"{packet.name} n={n}: {error}")
            continue
        if stated != fact:
            problems.append(
                f"{packet.name} n={n}: the fact is not the packing {row['path']} states"
            )
        held += 1
        # A pinned file the row names as the same packing, such as the source's own
        # witness, must be at its pin too and state the packing the fact states.
        for other in row.get("same_packing", []):
            reader = SAME_PACKING_READERS.get(other["format"])
            if reader is None:
                problems.append(f"{packet.name} n={n}: no reader for {other['format']}")
                continue
            raw = pinned_bytes(other["path"])
            if raw is None:
                continue
            try:
                same = reader(raw, n)
            except AreaRouteError as error:
                problems.append(f"{packet.name} n={n}: {other['path']}: {error}")
                continue
            if same != fact:
                problems.append(
                    f"{packet.name} n={n}: {other['path']} is not the packing the fact states"
                )
            held += 1
        blob = _BLOB.fullmatch(row.get("printed_in", ""))
        if blob is None:
            continue
        if blob.group(1) != source["source_commit"]:
            problems.append(f"{packet.name} n={n}: the side is printed at another commit")
            continue
        table = pinned_bytes(blob.group(2))
        if table is None:
            continue
        rows = printed_rows(table, blob.group(2))
        if not any(line[0] == str(n) and row["offered"] in line for line in rows):
            problems.append(f"{packet.name} n={n}: {blob.group(2)} does not print the side")
        held += 1
    return held, problems


def ryxu_packing(n: int) -> tuple[Fraction, tuple[Placed, ...]]:
    """Ryan Xu's certificate at ``n`` (T-125), after its packet's custody, read here.

    `devtools.ryxu_arrangement_reports` admits the retained source text; this route reads
    its JSON, ``s_exact`` and ``{x, y, t}`` rational strings in ``[0, S]^2``, itself.
    """
    ryxu.read_facts()
    record = kernel.read_xz(ryxu.fact_path())
    text = next(row["source_certificate"] for row in record["cases"] if row["n"] == n)
    value = _json_object(text.encode("utf-8"), n)
    side = _scalar(value.get("s_exact"), f"n={n} side")
    poses: list[Pose] = []
    for index, square in enumerate(value["squares"], start=1):
        if type(square) is not dict or set(square) != {"x", "y", "t"}:
            raise AreaRouteError(f"n={n} square {index}: not exactly x, y and t")
        x, y, t = (_scalar(square[key], f"n={n} square {index}") for key in ("x", "y", "t"))
        poses.append((x, y, t))
    return side, tuple(placed(poses))


def squish_update_packing(n: int) -> tuple[Fraction, tuple[Placed, ...]]:
    """SQUISH's update certificate at ``n`` (T-115), a rational corner witness, read here.

    `devtools.squish_followup_packets` admits and loads the retained witness; this route
    takes each square's centre as the midpoint of its first and third corners and its
    rotation as its first edge, held to the unit circle.
    """
    witness = squish_update.read_certificate(n)
    side = _scalar(witness["side"], f"n={n} side")
    placements: list[Placed] = []
    for index, square in enumerate(witness["squares"], start=1):
        where = f"n={n} square {index}"
        p0, p1, p2, _p3 = ((_scalar(x, where), _scalar(y, where)) for x, y in square["corners"])
        centre_x, centre_y = (p0[0] + p2[0]) / 2, (p0[1] + p2[1]) / 2
        placements.append((centre_x, centre_y, *unit_basis(p1[0] - p0[0], p1[1] - p0[1])))
    return side, tuple(placements)


def couzo_refinement_packing(n: int) -> tuple[Fraction, tuple[Placed, ...]]:
    """Francisco Couzo's refinement at ``n`` (T-128), after its packet's custody, read here.

    `devtools.couzo_refinement_reports.read_facts` admits the retained source text, Evan
    Daniel's format with centres in ``[0, S]^2``; this route parses that text itself.
    """
    t128.read_facts()
    record = kernel.read_xz(t128.fact_path())
    text = next(row["source_certificate"] for row in record["cases"] if row["n"] == n)
    side, poses = parse_certificate(text, n)
    return side, tuple(placed(poses))


def evand_optimum_packing(n: int) -> tuple[Fraction, tuple[Placed, ...]]:
    """Evan Daniel's exact optimum at ``n`` (T-098), the retained ``n-N.cert``, read here.

    `devtools.evand_exact_certificates.is_decided` admits the file as, byte for byte, the
    one that packet's first-party receipt decided at ``n``; this route parses it itself.
    """
    path = legacy.certificate_path(legacy.CERTS, n)
    if not legacy.is_decided(path, n):
        raise AreaRouteError(f"n={n}: not the certificate the T-098 packet decided")
    side, poses = parse_certificate(path.read_text(encoding="utf-8"), n)
    return side, tuple(placed(poses))


#: How each credited certificate is read, by its register entry.
CREDITED_READERS: dict[str, Callable[[int], tuple[Fraction, tuple[Placed, ...]]]] = {
    "T-125": ryxu_packing,
    "T-115": squish_update_packing,
    "T-136": import_packing("#481"),
    "T-138": import_packing("#470"),
    "T-146": import_packing("regularized"),
    "T-128": couzo_refinement_packing,
    "T-098": evand_optimum_packing,
}


#: The displacements `arrangement_gap` counts squares beyond.
MOVED = {f"1e-{k}": Fraction(1, 10**k) for k in (9, 6, 3, 2, 1)}


def symmetric(side: Fraction, square: Placed, k: int) -> Placed:
    """``square`` under the ``k``-th of the eight symmetries of ``[0, side]^2``.

    ``k`` counts quarter turns about the box centre, after a reflection in ``x = side/2``
    when ``k >= 4``; the orientation is read modulo a quarter turn, as a square's is.
    """
    x, y, c, s = square
    if k >= 4:
        x, s = side - x, -s
    for _turn in range(k % 4):
        x, y = side - y, x
    return x, y, c, s


def nearest_reach(points: Sequence[tuple[float, float]]) -> float:
    """How far above the least binary64 squared distance between two of these centres an
    exact nearest one can read, with a wide margin.

    Each coordinate is its exact value correctly rounded, within ``M * 2^-53`` of it for
    ``M`` the largest magnitude, and the difference, the squares and the sum each round
    once more, so a squared distance read in binary64 is within ``48 * M^2 * 2^-53`` of
    the exact one, and certainly within ``64 * M^2 * 2^-53``. The exact nearest reads at
    most twice that above the least read value, and so does every exact tie with it. This
    allows ``(1 + M)^2 * 2^-40``, at least 64 times twice that bound, so the search never
    drops a centre it would have needed; a coordinate past binary64's range is refused.
    """
    largest = max((max(abs(x), abs(y)) for x, y in points), default=0.0)
    if not math.isfinite(largest):
        raise AreaRouteError("a centre's coordinate is past binary64's range")
    return (1.0 + largest) ** 2 * 2.0**-40


def arrangement_gap(
    first: tuple[Fraction, Sequence[Placed]], second: tuple[Fraction, Sequence[Placed]]
) -> dict[str, Any]:
    """How far apart two packings of one count are, pose by pose, under the best symmetry.

    For each of the box's eight symmetries applied to ``second``, every square of
    ``first`` is matched to the nearest centre of ``second``; a symmetry counts only
    where that matching is one to one. Reported for the best: the largest centre
    displacement, the largest orientation difference (the sine of the least angle between
    the two squares' edges), how many squares moved by more than each of ``10^-9`` to
    ``10^-1`` (`MOVED`), and how many turned by a sine above ``10^-6``. A measurement for
    credit; it decides nothing.

    The nearest centre is the exact one, the least exact squared distance and then the
    least index, as an exact search over every pair finds it; only the search is cheaper
    (think-uomm). Each squared distance is first taken in binary64 and only the centres
    within `nearest_reach` of the least of those are compared exactly, which always
    holds the exact nearest and every exact tie with it.
    """
    side, left = first
    other_side, right = second
    best: dict[str, Any] | None = None
    near = [(float(x), float(y)) for x, y, _c, _s in left]
    for k in range(8):
        mapped = [symmetric(other_side, square, k) for square in right]
        far = [(float(u), float(v)) for u, v, _a, _b in mapped]
        reach = nearest_reach([*near, *far])
        nearest: list[tuple[Fraction, int]] = []
        for (x, y, _c, _s), (fx, fy) in zip(left, near, strict=True):
            rough = [(fx - fu) ** 2 + (fy - fv) ** 2 for fu, fv in far]
            within = min(rough) + reach
            nearest.append(
                min(
                    ((x - u) ** 2 + (y - v) ** 2, j)
                    for j, (u, v, _a, _b) in enumerate(mapped)
                    if rough[j] <= within
                )
            )
        if len({j for _d, j in nearest}) != len(left):
            continue
        largest = max(distance for distance, _j in nearest)
        if best is not None and largest >= best["largest_squared"]:
            continue
        turns = [
            min(abs(c * b - s * a), abs(c * a + s * b))
            for (_x, _y, c, s), (_d, j) in zip(left, nearest, strict=True)
            for _u, _v, a, b in (mapped[j],)
        ]
        best = {
            "symmetry": k,
            "largest_squared": largest,
            "largest_displacement": _root(largest),
            "largest_orientation_sine": f"{float(max(turns)):.6e}",
            "moved_beyond": {
                label: sum(1 for d, _j in nearest if d > bound * bound)
                for label, bound in MOVED.items()
            },
            "turned_beyond_1e-6": sum(1 for turn in turns if turn > Fraction(1, 10**6)),
            "side_difference": _text(side - other_side),
        }
    if best is None:
        raise AreaRouteError("no symmetry matches the two packings square for square")
    best["largest_squared"] = _text(best["largest_squared"])
    return best


def credited_gaps(found: Sequence[Imported]) -> dict[str, dict[str, Any]]:
    """`arrangement_gap` of each credited certificate against each entry it is credited to.

    A display-regularized certificate may slide squares far enough that no symmetry
    matches the two packings one to one; that is recorded as ``unmatched`` with the side
    difference, and is a measurement, as every gap is, not a refusal.
    """
    credit: dict[str, dict[str, Any]] = {}
    for case in found:
        for house in credited(case.issue, case.n):
            other = parent_packing(house, case.n)
            try:
                gap = arrangement_gap((case.side, case.placements), other)
            except AreaRouteError as error:
                gap = {"unmatched": str(error), "side_difference": _text(case.side - other[0])}
            credit[f"{case.issue} n={case.n} against {house}"] = gap
    return credit


#: A certificate its source says it assembled from placed patches of another packing:
#: the parent's import key and count, and the guard dilation the source says it applied
#: to every centre afterwards, which the measurement undoes. PingYou Ltd's n207 (#503)
#: and n153 (#504) are both cut from Evan Daniel's exact n70 certificate of Ryan Xu's
#: packing, the regularized ``n-070`` that T-146 retains, with guards 1 + 1e-10 and
#: 1 + 2e-13 as their certificates' metadata states them.
LINEAGE: dict[tuple[str, int], tuple[str, int, Fraction]] = {
    ("#503", 207): ("regularized", 70, Fraction(10000000001, 10000000000)),
    ("#504", 153): ("regularized", 70, Fraction(5000000000001, 5000000000000)),
    # SQUISH's #500 names whole or nearly whole pieces at three counts, with no dilation:
    # Francisco Couzo's s(127) (T-128) less a 2 x 3 corner of cells in the 176, and
    # SQUISH's own #481 s(209) whole in the 270 and the 304. Its other pieces are
    # narrowed before composition or come from certificates no packet retains.
    ("#500", 176): ("T-128", 127, Fraction(1)),
    ("#500", 270): ("#481", 209, Fraction(1)),
    ("#500", 304): ("#481", 209, Fraction(1)),
    # Couzo's #506 starts from #500's packings of the same count at 304 and 305 and from
    # Kevin Fang's #484 at 344; its exact optima carry the 1 + 10^-20 guard of Evan
    # Daniel's solver, far below `NEAR`, so no dilation is undone.
    ("#506", 304): ("#500", 304, Fraction(1)),
    ("#506", 305): ("#500", 305, Fraction(1)),
    ("#506", 344): ("#484", 344, Fraction(1)),
}
#: How near a parent square must land on a child square to be counted as reappearing:
#: its centre within 10^-9, and its edge direction within a sine of 10^-6 modulo a
#: quarter turn to count as unturned.
NEAR = Fraction(1, 10**9)
NEAR_SINE = Fraction(1, 10**6)
#: The fewest reappearing squares for a placement to be reported.
PATCH_FLOOR = 4


def _turn_sine(c: Fraction, s: Fraction, a: Fraction, b: Fraction) -> Fraction:
    """The sine of the least angle between two squares' edges, modulo a quarter turn."""
    return min(abs(c * b - s * a), abs(c * a + s * b))


def patch_lineage(
    child: tuple[Fraction, Sequence[Placed]],
    parent: tuple[Fraction, Sequence[Placed]],
    dilation: Fraction,
    *,
    limit: int = 3,
    near: Fraction = NEAR,
) -> list[dict[str, Any]]:
    """The placements of ``parent`` under which most of its squares reappear in ``child``.

    Each child centre is divided by ``dilation`` first. For each of the eight symmetries
    of the parent's box, every parent square paired with every child square names the
    translation carrying the one onto the other; the translations named most often, read
    to ``near`` (`NEAR`, ``10^-9``, unless a coarser scale is asked for), are the
    candidate placements. For each, the parent's squares are counted that land within
    ``near`` of a child centre (``squares``), those of them that land at another
    orientation (``turned_beyond_1e-6``), and those that land on a child square to the
    digit, the centre equal and the edge direction exactly a multiple of a quarter turn
    away, however the child writes its basis (``exact``). Returns at most ``limit``
    placements with at least `PATCH_FLOOR` squares, the fullest first. A measurement for
    credit: it decides nothing. At a coarse ``near`` the count says whether a piece
    reappears to the eye; only `NEAR` says it reappears by pose.
    """
    parent_side, parent_squares = parent
    _child_side, child_squares = child
    undone = [(x / dilation, y / dilation, c, s) for x, y, c, s in child_squares]
    if near <= 0:
        raise AreaRouteError("the nearness must be positive")
    scale = 1 / near
    votes: dict[tuple[int, int, int], dict[tuple[Fraction, Fraction], int]] = {}
    mapped_by_symmetry: dict[int, list[Placed]] = {}
    for k in range(8):
        mapped = [symmetric(parent_side, square, k) for square in parent_squares]
        mapped_by_symmetry[k] = mapped
        for px, py, _pc, _ps in mapped:
            for cx, cy, _cc, _cs in undone:
                shift = (cx - px, cy - py)
                cell = (k, round(shift[0] * scale), round(shift[1] * scale))
                exact = votes.setdefault(cell, {})
                exact[shift] = exact.get(shift, 0) + 1
    ranked = sorted(votes.items(), key=lambda item: (-sum(item[1].values()), item[0]))
    placements: list[dict[str, Any]] = []
    for (k, _tx, _ty), exact_shifts in ranked[:limit]:
        shift = max(exact_shifts.items(), key=lambda item: (item[1], item[0]))[0]
        squares = turned = exact = 0
        for px, py, pc, ps in mapped_by_symmetry[k]:
            x, y = px + shift[0], py + shift[1]
            for cx, cy, cc, cs in undone:
                if (cx - x) ** 2 + (cy - y) ** 2 > near * near:
                    continue
                squares += 1
                turn = _turn_sine(pc, ps, cc, cs)
                if turn > NEAR_SINE:
                    turned += 1
                elif turn == 0 and (cx, cy) == (x, y):
                    exact += 1
                break
        if squares >= PATCH_FLOOR:
            placements.append(
                {
                    "symmetry": k,
                    "translation": [_text(shift[0]), _text(shift[1])],
                    "squares": squares,
                    "turned_beyond_1e-6": turned,
                    "exact": exact,
                }
            )
    return placements


def parent_packing(key: str, m: int) -> tuple[Fraction, tuple[Placed, ...]]:
    """A lineage parent at ``m``: a register entry's packing by its `CREDITED_READERS`
    reader, or an import's certificate by the import's key."""
    reader = CREDITED_READERS.get(key)
    return reader(m) if reader is not None else import_packing(key)(m)


def lineage_gaps(found: Sequence[Imported]) -> dict[str, list[dict[str, Any]]]:
    """`patch_lineage` of each certificate `LINEAGE` names against its stated parent."""
    lineage: dict[str, list[dict[str, Any]]] = {}
    for case in found:
        named = LINEAGE.get((case.issue, case.n))
        if named is None:
            continue
        key, m, dilation = named
        parent = parent_packing(key, m)
        lineage[f"{case.issue} n={case.n} from {key} n={m}"] = patch_lineage(
            (case.side, case.placements), parent, dilation
        )
    return lineage


def run_decide_imports(
    workers: int,
    output: Path | None,
    upstream: list[list[str]],
    keys: Sequence[str] = tuple(IMPORTS),
) -> int:
    started = time.monotonic()
    found = import_cases(keys)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(decide_import, found))
    maintained = import_positives(keys)
    claims = plan_claims(keys)
    problems: list[str] = []
    for row in rows:
        packet = WEB / row["packet"]
        frozen = json.loads((packet / "acquisition/claims.json").read_text(encoding="utf-8"))
        declaration = _declaration(packet)
        offered = {r["n"]: r["offered"] for r in declaration["certificates"]}
        problems += compare_import(
            row,
            maintained[row["packet"], row["n"]],
            claims[row["packet"]].get(row["n"]),
            next(r for r in frozen["results"] if r["n"] == row["n"]),
            offered[row["n"]],
            cited=row["n"] in declaration["requested"],
        )
    credit = credited_gaps(found)
    lineage = lineage_gaps(found)
    for row in rows:
        print(
            f"{row['issue']} n={row['n']:3d} passed={row['passed']} pairs={row['pairs']} "
            f"clipped={row['clipped_pairs']} wall={row['wall_clearance']} "
            f"wall_contacts={row['wall_contacts']} least_distance={row['least_distance']} "
            f"controls={sum(row['controls'].values())}/{len(row['controls'])} "
            f"{row['wall_seconds']}s"
        )
    totals = import_receipt_totals(keys)
    for packet_name, total in totals.items():
        print(f"retained receipt {packet_name}: {json.dumps(total)}")
    for name, gap in credit.items():
        print(f"arrangement {name}: {json.dumps(gap)}")
    for name, patches in lineage.items():
        print(f"lineage {name}: {json.dumps(patches)}")
    selected = {ALL_IMPORTS[key]: key for key in keys}
    held: dict[str, int] = {}
    for name, directory in upstream:
        if name not in selected:
            problems.append(f"{name}: not one of the selected imports")
            continue
        packet = WEB / name
        held[name], found_problems = upstream_problems(
            packet, Path(directory), roster(selected[name], _declaration(packet))
        )
        problems += found_problems
        print(f"upstream {name}: {held[name]} certificates and printed sides checked")
    wall = round(time.monotonic() - started, 2)
    print(f"{len(rows)} certificates, {sum(r['pairs'] for r in rows)} pairs, {wall}s wall")
    if output is not None:
        report = {
            "rows": rows,
            "receipts": totals,
            "arrangements": credit,
            "lineage": lineage,
            "upstream": held,
            "problems": problems,
            "wall_seconds": wall,
        }
        output.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    for problem in problems:
        print(f"DISAGREEMENT: {problem}")
    return 1 if problems else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    deciding = sub.add_parser("decide")
    deciding.add_argument("--workers", type=int, choices=(1, 2), default=2)
    deciding.add_argument("--json", type=Path)
    imports = sub.add_parser("decide-imports")
    imports.add_argument("--workers", type=int, choices=(1, 2), default=2)
    imports.add_argument("--json", type=Path)
    imports.add_argument(
        "--upstream", nargs=2, action="append", default=[], metavar=("PACKET", "DIRECTORY")
    )
    imports.add_argument(
        "--imports", nargs="+", choices=tuple(ALL_IMPORTS), default=list(IMPORTS)
    )
    replay = sub.add_parser("replay-t128")
    replay.add_argument("--workers", type=int, choices=(1, 2), default=2)
    args = parser.parse_args(argv)
    if args.action == "decide":
        return run_decide(args.workers, args.json)
    if args.action == "decide-imports":
        return run_decide_imports(args.workers, args.json, args.upstream, args.imports)
    return run_replay_t128(args.workers)


if __name__ == "__main__":
    raise SystemExit(main())
