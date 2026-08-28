#!/usr/bin/env python3
"""Screen every known-best square for translational play, with replayable certificates.

WHAT IS DECIDED HERE

Translate one square by `t*d` and hold every other square and the container fixed.
Each separating-axis projection interval of that square then shifts by exactly
`t*(d.n)` along axis `n`, so every constraint the validity oracle tests is an *affine*
function of `t`.  There is no linearization and no first-order error: a feasible
direction plus the first blocking `t` is an exact statement about the witness geometry
at the precision it is materialized in.

Only the axes whose gap is already zero can decide the question.  A blocker's strictly
negative axes stay negative for small `t`, and a pair with a strictly positive gap stays
separated.  So the square can move iff some direction `d` keeps, for every active
blocker, at least one zero-gap axis non-decreasing: `d.n >= 0`.

The sign pattern of `d.n` is constant on each open arc between the critical directions
where `d.n = 0`.  Testing one interior direction per arc *and* every critical direction
is therefore a complete search over all translation directions, not a sample: if any
direction works, one of the tested directions works.

TWO CLASSES OF MOTION, COUNTED SEPARATELY

- `strict-separating`: some direction makes a zero-gap axis of every active blocker
  *strictly* increase, so the square leaves everything it touches at once.  This is the
  robust witness -- strict inequalities survive a perturbation of the direction and of
  the tolerance -- and it is the headline count.
- `contact-preserving`: no direction separates, but some direction keeps at least one
  contact exactly closed while the square moves along it.  A square in a partly empty
  grid row slides the length of the row this way without ever leaving its neighbours.

Both are translations.  Reporting only the first would make a miss mean "cannot be
pushed clear", which is much weaker than what a reader hears; reporting both is what
lets a miss mean the square cannot be translated at all.

WHAT A RESULT MEANS, AND WHAT IT DOES NOT

- A HIT is a sound certificate of play, modulo the contact tolerance.  The direction and
  the slide distance are recorded, and this module replays each one: it translates the
  square by that distance in that direction and re-runs `sqpack.verify.verify_packing`
  on the moved configuration.  A certificate that does not replay is not reported.
- A MISS proves only that THAT ONE SQUARE cannot be TRANSLATED, at that tolerance.  It
  is not rigidity and must never be read as rigidity.  Rotating the square, and moving
  two or more squares together, are both outside this test -- a packing in which every
  square fails this screen can still be a mechanism.  "Rigid" is a claim about all
  motions of all pieces; this file only ever rules out one motion of one piece.
- Movability is a property of the retained witness, not of `s(n)`.  `n = 10` is proved
  optimal and still has two rattlers: optimality and rigidity are independent.
- The tolerance is load bearing in both directions.  Too tight and a real contact reads
  as free space, so a witness's rounding shows up as play; too loose and real play is
  hidden by a contact that is not there.  Every case is therefore screened across four
  tolerances and the file records whether the answer moved.
- Clearance and contact counts do not substitute for this.  Every square in every
  retained record touches something, and the loose ones slide tangentially rather than
  float, so no gap or degree heuristic finds them.

EXCLUSIONS

`n = 68` and `n = 69` are excluded, and the exclusion is measured rather than asserted:
their witnesses are UnitSquare renderings whose corners are not exact unit squares
(edge lengths differ at ~1e-8), which is 22 orders of magnitude worse than every other
record in the corpus.  Below that residual contacts stop registering, so nearly every
square reports movable -- a witness-fidelity artifact, not a finding.  Tracked as
think-ecqk.

Usage:
    uv run --frozen python -m devtools.screen_translation_escape --update
    uv run --frozen python -m devtools.screen_translation_escape --check
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import mpmath as mp
from jsonschema import Draft202012Validator
from strif import atomic_output_file

from sqpack.verify import Square, edge_axes, float_sign, project, verify_packing
from sqpack.witness import load_witness, materialize_witness
from sqpack.yamlio import load_yaml

type Scalar = Any
type Vector = tuple[Scalar, Scalar]

ROOT = Path(__file__).resolve().parent.parent
ATLAS_ROOT = ROOT / "atlas/known-best"
MANIFEST = ATLAS_ROOT / "manifest.json"
OUTPUT = ATLAS_ROOT / "translation-escape-screen.json"
SCHEMA = ATLAS_ROOT / "translation-escape-screen.schema.yaml"
WITNESS_SCHEMA = ROOT / "witnesses/witness.schema.yaml"
GENERATOR = "python -m devtools.screen_translation_escape"
CONTRACT = "packing.squares:TranslationEscapeScreen/v1"

# The witnesses carry 28 or more significant digits; 50 keeps every gap, dot product,
# and slide distance far below the loosest tolerance screened.
DIGITS = 50
# Screened tightest to loosest.  A contact is "active" when its gap is within the
# tolerance of zero, so a tighter tolerance sees fewer contacts and more play.
TOLERANCES = ("1e-12", "1e-10", "1e-8", "1e-6")
# Certificates are recorded at the tolerance the derived witnesses were numerically
# checked at in the manifest.
PRIMARY_TOLERANCE = "1e-8"
# Two unit squares can touch only if their centers are within sqrt(2); the screen adds
# slack so a float center comparison cannot drop a real contact.
CONTACT_RADIUS = mp.mpf("1.4143")
BLOCKER_RADIUS = 1.5
# A witness whose own squares are not unit squares to this residual cannot support a
# contact claim at any tolerance screened here.  The corpus splits at 5e-50 vs 1e-8,
# so no record sits near this line.
SHAPE_RESIDUAL_LIMIT = mp.mpf("1e-30")
# Every normal here is a unit vector, so `d.n` is a rate of change per unit slide and
# this is an absolute floor on it.  A rate below it moves a gap by less than 1e-29 over
# the longest slide in the corpus, which is seventeen orders inside the tightest
# tolerance screened, so the direction is treated as parallel to the contact.  Without
# a floor, an exact perpendicular would be rejected by its own rounding.
RATE_ZERO = mp.mpf("1e-30")
EXCLUSION_BEAD = "think-ecqk"
REPORTED_DIGITS = 21
# The two ways a square can be free to translate.  The first is the stronger witness and
# is the one the headline counts; the second still moves the square, and recording it is
# what lets a miss mean "cannot be translated" rather than "cannot be pushed clear".
SEPARATING = "strict-separating"
SLIDING = "contact-preserving"

CLAIM_BOUNDARIES = (
    (
        "A hit is a sound certificate that one square can be translated, modulo the "
        "contact tolerance; the direction and distance are recorded and replayed."
    ),
    "A miss proves only that that one square cannot be translated at that tolerance.",
    (
        "This screen cannot establish rigidity: rotation and coordinated multi-square "
        "motion are outside it, so a record with no hit is not a rigid record."
    ),
    (
        "Movability is a property of the retained witness geometry, not of s(n): a "
        "proved optimal packing can still contain a rattler, so optimality and "
        "rigidity are independent questions."
    ),
    (
        "Every constraint is exactly affine in the slide parameter, so the arithmetic "
        "is exact to the materialized precision and carries no linearization error."
    ),
    (
        "The direction search is complete rather than sampled: one interior direction "
        "per arc plus every critical direction covers all translation directions."
    ),
    (
        "A strict-separating count is not a clearance count: every square in every "
        "retained record touches something, and the loose ones slide tangentially "
        "rather than float."
    ),
)


def _json_text(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _decimal(value: Scalar) -> str:
    """A stable decimal rendering of an mpmath scalar."""
    return str(mp.nstr(value, REPORTED_DIGITS, strip_zeros=True))


def _sign(value: Scalar) -> int:
    """Exact sign of an mpmath scalar, for the projection primitive."""
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def shape_residual(squares: Sequence[Square]) -> Scalar:
    """How far the witness's own pieces are from being unit squares.

    The largest violation of `edge^2 = 1` and of the right-angle condition over every
    piece.  A packing whose pieces are not the shape it claims cannot support a contact
    claim, because the gaps a contact screen reads are smaller than the shape error.
    """
    worst = mp.mpf(0)
    for square in squares:
        for k in range(4):
            (px, py), (qx, qy) = square[k], square[(k + 1) % 4]
            length = (qx - px) * (qx - px) + (qy - py) * (qy - py)
            worst = max(worst, abs(length - 1))
        for k in range(4):
            (ax, ay), (bx, by), (cx, cy) = square[k - 1], square[k], square[(k + 1) % 4]
            worst = max(worst, abs((ax - bx) * (cx - bx) + (ay - by) * (cy - by)))
    return worst


def pair_separations(moving: Square, fixed: Square) -> list[tuple[Scalar, Vector]]:
    """The eight signed separations of one pair, with the normal each one follows.

    Entry `(gap, n)` means the pair is separated on that axis when `gap >= 0`, and that
    translating `moving` by `t*d` changes the gap by exactly `t*(d.n)`.  The pair is
    disjoint iff at least one of the eight is non-negative -- the separating-axis test,
    written so its dependence on the translation is explicit.
    """
    separations: list[tuple[Scalar, Vector]] = []
    for axis in edge_axes(moving) + edge_axes(fixed):
        moving_low, moving_high = project(moving, axis, _sign)
        fixed_low, fixed_high = project(fixed, axis, _sign)
        separations.append((fixed_low - moving_high, (-axis[0], -axis[1])))
        separations.append((moving_low - fixed_high, (axis[0], axis[1])))
    return separations


def reversed_separations(
    separations: Sequence[tuple[Scalar, Vector]],
) -> list[tuple[Scalar, Vector]]:
    """The same pair with the roles swapped: same gaps, opposite normals."""
    return [(gap, (-normal[0], -normal[1])) for gap, normal in separations]


def container_slacks(square: Square, side: Scalar) -> list[tuple[Scalar, Vector]]:
    """Signed container slacks with the inward normal each one follows."""
    slacks: list[tuple[Scalar, Vector]] = []
    one, zero = mp.mpf(1), mp.mpf(0)
    for px, py in square:
        slacks.append((px, (one, zero)))
        slacks.append((py, (zero, one)))
        slacks.append((side - px, (-one, zero)))
        slacks.append((side - py, (zero, -one)))
    return slacks


def _unit(x: Scalar, y: Scalar) -> Vector:
    norm = mp.sqrt(x * x + y * y)
    return (x / norm, y / norm)


def _pseudo_angle(direction: Vector) -> Scalar:
    """A monotone circular key, computed without transcendentals.

    Sorting by this is sorting by angle up to where the circle is cut, which is all the
    arc walk needs and is exactly reproducible on any platform.
    """
    x, y = direction
    scale = abs(x) + abs(y)
    ratio = y / scale
    return 2 - ratio if x < 0 else ratio


def candidate_directions(normals: Sequence[Vector]) -> list[tuple[Vector, str]]:
    """Every direction the search must try, and which kind each one is.

    The critical directions are the ones perpendicular to a blocker normal, where that
    blocker's gap neither opens nor closes; they are built as exact perpendiculars, so
    `d.n` is identically zero rather than a rounded near-zero.  Between consecutive
    critical directions the sign of every `d.n` is constant, so the bisector of each arc
    decides that whole arc.  Interior and critical together cover the circle.
    """
    if not normals:
        # Nothing is touching the square: no direction is constrained, so a small
        # canonical set is enough to find the longest free slide.
        canonical = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        return [(_unit(mp.mpf(x), mp.mpf(y)), "interior") for x, y in canonical]
    critical = [
        perpendicular for x, y in normals for perpendicular in (_unit(-y, x), _unit(y, -x))
    ]
    critical.sort(key=_pseudo_angle)
    directions: list[tuple[Vector, str]] = [(item, "critical") for item in critical]
    for index, start in enumerate(critical):
        end = critical[(index + 1) % len(critical)]
        bisector = (start[0] + end[0], start[1] + end[1])
        if abs(bisector[0]) + abs(bisector[1]) < mp.mpf("1e-20"):
            # The arc is a half turn: its midpoint is the start turned a quarter turn.
            bisector = (-start[1], start[0])
        directions.append((_unit(bisector[0], bisector[1]), "interior"))
    return directions


def _rate_sign(direction: Vector, normal: Vector) -> int:
    """Which way a contact's gap moves per unit slide, with a floor at `RATE_ZERO`."""
    rate = direction[0] * normal[0] + direction[1] * normal[1]
    if rate > RATE_ZERO:
        return 1
    if rate < -RATE_ZERO:
        return -1
    return 0


def _feasible(direction: Vector, blockers: Sequence[Sequence[Vector]], *, strict: bool) -> bool:
    """Does `direction` keep every active blocker satisfied?

    One zero-gap axis per blocker has to stay non-decreasing.  On an arc interior every
    `d.n` is bounded away from zero, so that test is the strict one and a hit there
    separates the square from everything it touches.  A critical direction slides along
    at least one contact, keeping its gap at zero, which is still a valid motion.
    """
    floor = 1 if strict else 0
    return all(
        any(_rate_sign(direction, normal) >= floor for normal in group) for group in blockers
    )


class RecordGeometry:
    """One materialized packing, with the pair separations computed at most once."""

    def __init__(self, squares: Sequence[Square], side: Scalar) -> None:
        self.squares = squares
        self.side = side
        self.centers = [
            (
                float(sum(point[0] for point in square) / 4),
                float(sum(point[1] for point in square) / 4),
            )
            for square in squares
        ]
        self._cache: dict[tuple[int, int], list[tuple[Scalar, Vector]]] = {}

    def neighbours(self, index: int, radius: float) -> list[int]:
        cx, cy = self.centers[index]
        return [
            other
            for other, (ox, oy) in enumerate(self.centers)
            if other != index and (ox - cx) ** 2 + (oy - cy) ** 2 <= radius * radius
        ]

    def separations(self, moving: int, fixed: int) -> list[tuple[Scalar, Vector]]:
        key = (min(moving, fixed), max(moving, fixed))
        cached = self._cache.get(key)
        if cached is None:
            cached = pair_separations(self.squares[key[0]], self.squares[key[1]])
            self._cache[key] = cached
        return cached if moving == key[0] else reversed_separations(cached)


def first_block(
    geometry: RecordGeometry, index: int, direction: Vector, radius: float
) -> Scalar:
    """The largest `t` for which sliding square `index` by `t*direction` stays valid.

    Every constraint is affine in `t`, so this is exact rather than a line search.  For
    a pair, the overlapping set of `t` is the intersection of the eight half lines where
    all eight signed separations are negative -- an interval, because the translations
    that make two convex bodies overlap are a convex set.  `t = 0` is outside it, so the
    pair blocks the slide at that interval's lower end when that end is positive.
    """
    limit = mp.inf
    for slack, normal in container_slacks(geometry.squares[index], geometry.side):
        rate = direction[0] * normal[0] + direction[1] * normal[1]
        if _rate_sign(direction, normal) < 0:
            limit = min(limit, slack / (-rate))
    for other in geometry.neighbours(index, radius):
        low, high = -mp.inf, mp.inf
        clear = False
        for gap, normal in geometry.separations(index, other):
            sign = _rate_sign(direction, normal)
            if sign == 0:
                if gap >= 0:
                    clear = True  # This axis separates the pair for every t.
                    break
                continue
            rate = direction[0] * normal[0] + direction[1] * normal[1]
            if sign > 0:
                high = min(high, -gap / rate)
            else:
                low = max(low, -gap / rate)
        if not clear and low > 0 and low < high:
            limit = min(limit, low)
    return limit


def slide_distance(geometry: RecordGeometry, index: int, direction: Vector) -> Scalar:
    """`first_block` over a neighbourhood wide enough to contain the whole slide.

    A pair can only interact once the moving square comes within sqrt(2) of it, so a
    slide of length `t` can only be blocked by a square within `sqrt(2) + t`.  The first
    pass bounds `t`; the second pass, when the first slide was long enough to leave the
    neighbourhood, redoes it against every square that bound can reach.
    """
    limit = first_block(geometry, index, direction, BLOCKER_RADIUS)
    reach = CONTACT_RADIUS + limit
    if reach > BLOCKER_RADIUS:
        limit = first_block(geometry, index, direction, float(reach) + 1e-9)
    return limit


def translated(
    squares: Sequence[Square], index: int, direction: Vector, distance: Scalar
) -> list[Square]:
    """The packing with one square translated -- the geometry a certificate claims."""
    moved = list(squares)
    moved[index] = [
        (px + distance * direction[0], py + distance * direction[1])
        for px, py in squares[index]
    ]
    return moved


class ActiveContacts:
    """What square `index` is touching at one tolerance, as constraints on a direction.

    `groups` holds one list of zero-gap normals per active blocker.  A direction is
    admissible when, for every group, at least one normal has `d.n >= 0`: that blocker
    keeps a separating axis.  The OR inside a group and the AND across groups are the
    whole geometry of the question.
    """

    def __init__(self, geometry: RecordGeometry, index: int, tolerance: Scalar) -> None:
        self.container_normals: list[Vector] = []
        self.square_indices: list[int] = []
        self.groups: list[list[Vector]] = []
        for slack, normal in container_slacks(geometry.squares[index], geometry.side):
            if slack < -tolerance:
                raise ValueError(
                    f"square {index} leaves the container by more than {tolerance}"
                )
            if slack <= tolerance and normal not in self.container_normals:
                self.container_normals.append(normal)
                self.groups.append([normal])
        for other in geometry.neighbours(index, BLOCKER_RADIUS):
            separations = geometry.separations(index, other)
            if max(gap for gap, _ in separations) > tolerance:
                continue  # Strictly separated: it cannot block a small enough slide.
            group = [normal for gap, normal in separations if gap >= -tolerance]
            if not group:
                raise ValueError(
                    f"squares {index} and {other} overlap by more than {tolerance}"
                )
            self.groups.append(group)
            self.square_indices.append(other)

    def admissible(self) -> list[tuple[Vector, str]]:
        """Every admissible direction, labelled by how it treats the contacts.

        `SEPARATING` breaks away from every active blocker at once; `SLIDING` keeps at
        least one contact exactly closed while it moves.  Both are real translations of
        the square; the first is the more robust witness, because strict inequalities
        survive a perturbation of the direction and of the tolerance.
        """
        normals = [normal for group in self.groups for normal in group]
        found: list[tuple[Vector, str]] = []
        for direction, _ in candidate_directions(normals):
            if _feasible(direction, self.groups, strict=True):
                found.append((direction, SEPARATING))
            elif _feasible(direction, self.groups, strict=False):
                found.append((direction, SLIDING))
        return found


def classify_square(geometry: RecordGeometry, index: int, tolerance: Scalar) -> str | None:
    """How square `index` can translate, without pricing the motion.

    A direction that is admissible at `t = 0` stays admissible for some `t > 0`: the
    active constraints do not decrease along it, and the inactive ones have room.  So
    admissibility alone settles whether the square moves, and the distance only has to
    be computed for the certificate that gets published.
    """
    kinds = {kind for _, kind in ActiveContacts(geometry, index, tolerance).admissible()}
    if SEPARATING in kinds:
        return SEPARATING
    return SLIDING if kinds else None


def certify_square(
    geometry: RecordGeometry, index: int, tolerance: Scalar
) -> dict[str, Any] | None:
    """The replayable certificate for square `index`, or None if it cannot translate."""
    contacts = ActiveContacts(geometry, index, tolerance)
    admissible = contacts.admissible()
    kind = SEPARATING if any(k == SEPARATING for _, k in admissible) else SLIDING
    best: tuple[Scalar, Vector] | None = None
    for direction, found in admissible:
        if found != kind:
            continue
        distance = slide_distance(geometry, index, direction)
        if distance <= 0:
            continue
        if best is None or distance > best[0]:
            best = (distance, direction)
    if best is None:
        if admissible:
            raise ValueError(f"square {index}: an admissible direction gave no room to move")
        return None

    distance, direction = best
    angle = mp.atan2(direction[1], direction[0]) * 180 / mp.pi
    return {
        "active_blockers": {
            "container_normals": len(contacts.container_normals),
            "square_indices": contacts.square_indices,
        },
        "direction": {
            "angle_degrees": mp.nstr(angle + 360 if angle < 0 else angle, 15, strip_zeros=True),
            "x": _decimal(direction[0]),
            "y": _decimal(direction[1]),
        },
        "slide_distance": _decimal(distance),
        "square_index": index,
        "witness_kind": kind,
    }


def _replay(geometry: RecordGeometry, certificate: dict[str, Any], tolerance: Scalar) -> bool:
    """Re-verify the packing with the square actually moved where the certificate says.

    The certificate is a claim about geometry, so it is checked by the same validity
    oracle the rest of the project uses rather than by the code that produced it.
    """
    direction = (mp.mpf(certificate["direction"]["x"]), mp.mpf(certificate["direction"]["y"]))
    distance = mp.mpf(certificate["slide_distance"])
    moved = translated(geometry.squares, certificate["square_index"], direction, distance)
    report = verify_packing(
        moved,
        geometry.side,
        sign=float_sign(tolerance),
        check_shapes=False,
        bucket=True,
    )
    return report.valid


def margins(geometry: RecordGeometry) -> tuple[Scalar | None, Scalar]:
    """The witness's own validity margins: worst pair separation and container slack.

    A screen that reads contacts is only as meaningful as the geometry it reads, so the
    file records how close the retained packing itself is to invalid.  No retained record
    is worse than -1e-29 on either margin -- seventeen orders inside the tightest
    tolerance screened -- which is why the sweep can start at 1e-12 and mean something.
    """
    worst_pair: Scalar | None = None
    worst_slack = mp.inf
    for index, square in enumerate(geometry.squares):
        for slack, _ in container_slacks(square, geometry.side):
            worst_slack = min(worst_slack, slack)
        for other in geometry.neighbours(index, BLOCKER_RADIUS):
            if other <= index:
                continue
            separation = max(gap for gap, _ in geometry.separations(index, other))
            worst_pair = separation if worst_pair is None else min(worst_pair, separation)
    return worst_pair, worst_slack


def screen_record(
    n: int, squares: Sequence[Square], side: Scalar, square_ids: Sequence[int]
) -> dict[str, Any]:
    """Screen one packing at every tolerance and certify the primary-tolerance hits."""
    geometry = RecordGeometry(squares, side)
    worst_pair, worst_slack = margins(geometry)
    movable: dict[str, list[int]] = {}
    separating: dict[str, list[int]] = {}
    for text in TOLERANCES:
        tolerance = mp.mpf(text)
        kinds = {
            index: kind
            for index in range(len(squares))
            if (kind := classify_square(geometry, index, tolerance)) is not None
        }
        movable[text] = sorted(kinds)
        separating[text] = sorted(index for index, kind in kinds.items() if kind == SEPARATING)

    primary = mp.mpf(PRIMARY_TOLERANCE)
    certificates: list[dict[str, Any]] = []
    for index in movable[PRIMARY_TOLERANCE]:
        certificate = certify_square(geometry, index, primary)
        if certificate is None:
            raise ValueError(f"n={n}: square {index} classified movable but not certifiable")
        certificate["witness_square_id"] = square_ids[index]
        certificate["replay_verified"] = _replay(geometry, certificate, primary)
        certificates.append(certificate)
    stable = all(indices == movable[PRIMARY_TOLERANCE] for indices in movable.values()) and all(
        indices == separating[PRIMARY_TOLERANCE] for indices in separating.values()
    )
    return {
        "min_container_slack": _decimal(worst_slack),
        "min_pair_separation": None if worst_pair is None else _decimal(worst_pair),
        "movable_square_count": len(certificates),
        "movable_squares": certificates,
        "movable_squares_by_tolerance": movable,
        "n": n,
        "separating_square_count": len(separating[PRIMARY_TOLERANCE]),
        "separating_squares_by_tolerance": separating,
        "square_count": len(squares),
        "stable_across_tolerances": stable,
    }


def manifest_entries() -> list[dict[str, Any]]:
    """The retained known-best corpus, in the manifest's order."""
    return json.loads(MANIFEST.read_text(encoding="utf-8"))["atlas"]["entries"]


def materialize_record(
    entry: dict[str, Any],
) -> tuple[Sequence[Square], Scalar, list[int]]:
    """One record's geometry and square ids at the screen's working precision."""
    mp.mp.dps = DIGITS
    witness = load_witness(ROOT / entry["witness"]["path"], fallback_schema=WITNESS_SCHEMA)
    squares, side = materialize_witness(witness, digits=DIGITS)
    return squares, side, [square["id"] for square in witness["squares"]]


def load_record(n: int) -> tuple[Sequence[Square], Scalar, list[int]]:
    """Materialize one retained record by `n`."""
    entry = next(item for item in manifest_entries() if item["n"] == n)
    return materialize_record(entry)


def screen_corpus() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Screen the whole known-best corpus; returns (cases, exclusions)."""
    mp.mp.dps = DIGITS
    cases: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    for entry in manifest_entries():
        squares, side, square_ids = materialize_record(entry)
        residual = shape_residual(squares)
        if residual > SHAPE_RESIDUAL_LIMIT:
            excluded.append(
                {
                    "bead": EXCLUSION_BEAD,
                    "n": entry["n"],
                    "note": (
                        "The witness pieces are not unit squares to a residual far "
                        "larger than any contact tolerance screened here, so contacts "
                        "stop registering and nearly every square reports movable. "
                        "That is a witness-fidelity artifact, not a finding about the "
                        "packing."
                    ),
                    "reason": "witness-shape-residual-above-limit",
                    "shape_residual": _decimal(residual),
                    "source_kind": entry["source"]["kind"],
                }
            )
            continue
        cases.append(screen_record(entry["n"], squares, side, square_ids))
    return cases, excluded


def schema_errors(screen: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(load_yaml(SCHEMA.read_text(encoding="utf-8")))
    return [
        f"{'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(screen), key=lambda error: list(error.path))
    ]


def screen_errors(screen: dict[str, Any]) -> list[str]:
    """Invariants that make the file readable as evidence rather than as output."""
    errors: list[str] = []
    aggregate = screen["aggregate"]
    cases = screen["cases"]
    if [case["n"] for case in cases] != sorted(case["n"] for case in cases):
        errors.append("cases are not in ascending n order")
    if aggregate["records_screened"] != len(cases):
        errors.append("records_screened disagrees with the case list")
    for case in cases:
        certificates = case["movable_squares"]
        if case["movable_square_count"] != len(certificates):
            errors.append(f"n={case['n']}: movable_square_count disagrees with the list")
        if [item["square_index"] for item in certificates] != sorted(
            item["square_index"] for item in certificates
        ):
            errors.append(f"n={case['n']}: certificates are not in square order")
        for certificate in certificates:
            if not certificate["replay_verified"]:
                errors.append(
                    f"n={case['n']}: certificate for square "
                    f"{certificate['square_index']} did not replay"
                )
            if mp.mpf(certificate["slide_distance"]) <= 0:
                errors.append(
                    f"n={case['n']}: certificate for square "
                    f"{certificate['square_index']} claims no motion"
                )
        if case["separating_square_count"] != sum(
            item["witness_kind"] == SEPARATING for item in certificates
        ):
            errors.append(f"n={case['n']}: separating_square_count disagrees with the list")
        if case["movable_squares_by_tolerance"][PRIMARY_TOLERANCE] != [
            item["square_index"] for item in certificates
        ]:
            errors.append(f"n={case['n']}: the primary tolerance sweep lost a certificate")
    if aggregate["movable_squares"] != sum(case["movable_square_count"] for case in cases):
        errors.append("movable_squares disagrees with the case list")
    if aggregate["separating_squares"] != sum(
        case["separating_square_count"] for case in cases
    ):
        errors.append("separating_squares disagrees with the case list")
    for key, counted in (
        ("records_with_movable_square", "movable_square_count"),
        ("records_with_separating_square", "separating_square_count"),
    ):
        if aggregate[key] != sum(case[counted] > 0 for case in cases):
            errors.append(f"{key} disagrees with the case list")
    if aggregate["tolerance_disagreement_ns"] != [
        case["n"] for case in cases if not case["stable_across_tolerances"]
    ]:
        errors.append("tolerance_disagreement_ns disagrees with the case list")
    return errors


def expected_document() -> dict[str, Any]:
    cases, excluded = screen_corpus()
    aggregate = {
        "movable_squares": sum(case["movable_square_count"] for case in cases),
        "records_excluded": len(excluded),
        "records_screened": len(cases),
        "records_with_movable_square": sum(case["movable_square_count"] > 0 for case in cases),
        "records_with_separating_square": sum(
            case["separating_square_count"] > 0 for case in cases
        ),
        "separating_squares": sum(case["separating_square_count"] for case in cases),
        "squares_screened": sum(case["square_count"] for case in cases),
        "tolerance_disagreement_ns": [
            case["n"] for case in cases if not case["stable_across_tolerances"]
        ],
    }
    screen = {
        "aggregate": aggregate,
        "cases": cases,
        "claim_boundaries": list(CLAIM_BOUNDARIES),
        "excluded": excluded,
        "generated_by": GENERATOR,
        "inputs": {"corpus": "manifest.json", "witnesses": "witnesses/known-best"},
        "method": {
            "certificate_classes": (
                f"{SEPARATING}: the square leaves every active contact at once; "
                f"{SLIDING}: it can only move while keeping a contact closed"
            ),
            "certificate_replay": (
                "each hit is re-verified by translating the square by the recorded "
                "distance and re-running sqpack.verify.verify_packing"
            ),
            "direction_search": (
                "one interior direction per arc between critical directions, plus "
                "every critical direction: complete over directions, not sampled"
            ),
            "exactness": (
                "each projection interval shifts by exactly t*(d.n) under translation, "
                "so every constraint is affine in t and no linearization enters"
            ),
            "materialization_digits": DIGITS,
            "primary_tolerance": PRIMARY_TOLERANCE,
            "shape_residual_limit": _decimal(SHAPE_RESIDUAL_LIMIT),
            "tolerances": list(TOLERANCES),
        },
        "one_sidedness": (
            "A hit certifies that one square can be translated. A miss proves only that "
            "that one square cannot be translated at that tolerance; rotation and "
            "coordinated multi-square motion are outside this test, so no result here "
            "may be read as rigidity."
        ),
    }
    errors = [*schema_errors(screen), *screen_errors(screen)]
    if errors:
        raise ValueError("invalid translation escape screen: " + "; ".join(errors))
    return {
        "softschema": {
            "contract": CONTRACT,
            "envelope": "screen",
            "schema": SCHEMA.name,
            "status": "enforced",
        },
        "screen": screen,
    }


def _summary(document: dict[str, Any]) -> str:
    aggregate = document["screen"]["aggregate"]
    excluded = ", ".join(f"n={item['n']}" for item in document["screen"]["excluded"])
    return (
        f"{aggregate['records_screened']} records screened, "
        f"{aggregate['records_with_separating_square']} with a square that separates "
        f"({aggregate['separating_squares']} squares), "
        f"{aggregate['records_with_movable_square']} with a square that translates at all "
        f"({aggregate['movable_squares']} squares), "
        f"excluded: {excluded or 'none'}"
    )


def update() -> None:
    document = expected_document()
    with atomic_output_file(OUTPUT) as temporary:
        temporary.write_text(_json_text(document), encoding="utf-8")
    print(f"translation escape screen updated: {_summary(document)}")


def check() -> None:
    document = expected_document()
    if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != _json_text(document):
        raise ValueError("translation escape screen is missing or stale")
    print(f"translation escape screen check passed: {_summary(document)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    update() if args.update else check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
