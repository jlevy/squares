"""Extract the contact structure of a pose, and refuse where it cannot decide.

This is the first step of the promotion route: before a system of equations can be
assembled, something has to say *which* squares touch which, and which corners sit on
the container wall.  Getting that wrong is not a small error -- a wrong incidence
produces a system whose root is a different packing, and the failure surfaces much later
as a reconstructed side that quietly disagrees with the input.

Two properties of this module matter more than its speed.

**It decides through the injected `sign`, not through a comparison written here.**  That
is the same seam :mod:`sqpack.verify` uses, so the extractor runs unchanged over exact
algebraic scalars, where a contact is *certified*, and over high-precision floats, where
it is measured against a declared floor.  At `n = 11` the coordinates are exact and the
question of ambiguity does not arise; at `n = 29` they are a hundred-digit reconstruction
and it does.

**It reports what it could not decide instead of choosing.**  An incidence whose margin
sits just above the floor is neither a contact nor a strict separation as far as this
code is concerned, and :func:`require_decided` turns any such incidence into a typed
refusal.  D-021 is the reason the distinction is not academic: the float LP solver has a
noise floor around `1e-11`, and a pose quenched through it carries margins that no
tolerance can honestly classify.  A source carrying ninety-nine orders of magnitude
between its worst contact and its smallest strict separation is a different situation,
and the point of `separation_decades` is to make which situation you are in a reported
number rather than an assumption.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass
from typing import Any

import mpmath as mp

from sqpack.verify import Square, edge_axes, project

WALLS = ("left", "bottom", "right", "top")

# Margins are whatever scalar the caller's pose is built from -- an mpmath float or an
# exact field element -- because the arithmetic is the caller's choice and not this
# module's. Pinning the annotation to one of them would contradict the seam.
Scalar = Any


class ContactExtractionError(ValueError):
    """A typed extraction failure suitable for both human and machine callers."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


@dataclass(frozen=True)
class Incidence:
    """One decided contact: a touching pair, or a corner resting on a wall."""

    kind: str
    left: int
    right: str
    margin: str


@dataclass(frozen=True)
class AngleClass:
    """One orientation class, as a set of square indices sharing an orientation."""

    label: str
    members: tuple[int, ...]
    degrees: str | None


@dataclass(frozen=True)
class ContactStructure:
    """Everything the assembly step needs, plus everything it must not assume."""

    n: int
    side: str
    floor: str
    ambiguity_ceiling: str
    pair_contacts: tuple[Incidence, ...]
    wall_contacts: tuple[Incidence, ...]
    ambiguous: tuple[Incidence, ...]
    angle_classes: tuple[AngleClass, ...]
    pairs_tested: int
    wall_relations_tested: int
    worst_contact_margin: str
    smallest_strict_separation: str
    separation_decades: str | None

    @property
    def incidence_count(self) -> int:
        return len(self.pair_contacts) + len(self.wall_contacts)

    def as_record(self) -> dict:
        record = asdict(self)
        record["incidence_count"] = self.incidence_count
        return record


def _decimal(value, digits: int = 30) -> str:
    try:
        return str(mp.nstr(mp.mpf(value), n=digits, strip_zeros=False))
    except TypeError, ValueError:
        return str(value)


def _larger(left, right, sign: Callable):
    """The larger of two scalars, decided by the injected sign.

    `max` would use `>`, which exact field elements deliberately do not provide: an
    ordering on algebraic numbers is itself a sign decision, and this module is not
    allowed to make sign decisions of its own.
    """
    return left if sign(left - right) >= 0 else right


def _pair_margin(first: Square, second: Square, sign: Callable):
    """The widest separating-axis gap, negative when the squares overlap."""
    best = None
    for axis in edge_axes(first) + edge_axes(second):
        first_low, first_high = project(first, axis, sign)
        second_low, second_high = project(second, axis, sign)
        gap = _larger(second_low - first_high, first_low - second_high, sign)
        best = gap if best is None else _larger(best, gap, sign)
    return best


def _same_orientation(first: Square, second: Square, sign: Callable) -> bool:
    """Whether two squares share an orientation modulo ninety degrees.

    Decided by exact predicates -- a vanishing cross product or a vanishing dot
    product -- rather than by comparing angles, so this is a certified answer over
    exact scalars and stays free of `atan2` over any scalar type.
    """
    first_dx = first[1][0] - first[0][0]
    first_dy = first[1][1] - first[0][1]
    second_dx = second[1][0] - second[0][0]
    second_dy = second[1][1] - second[0][1]
    cross = first_dx * second_dy - first_dy * second_dx
    dot = first_dx * second_dx + first_dy * second_dy
    return sign(cross) == 0 or sign(dot) == 0


def _orientation_degrees(square: Square) -> str | None:
    """A descriptive angle in `[-45, 45)`, or None when the scalars resist floats."""
    try:
        dx = mp.mpf(square[1][0] - square[0][0])
        dy = mp.mpf(square[1][1] - square[0][1])
    except TypeError, ValueError:
        return None
    angle = mp.degrees(mp.atan2(dy, dx))
    canonical = mp.fmod(angle + 45, 90)
    if canonical < 0:
        canonical += 90
    return _decimal(canonical - 45)


def extract_contacts(
    squares: Sequence[Square],
    side,
    *,
    sign: Callable,
    floor: str = "0",
    ambiguity_ratio: str = "1e10",
) -> ContactStructure:
    """Classify every pair and every corner-to-wall relation of a pose.

    `sign` decides zero and is the only thing that does; `floor` names the magnitude at
    which that decision stops being trustworthy, and `ambiguity_ratio` widens it into the
    band this extractor refuses to classify.  With an exact `sign` the default `floor` of
    zero leaves that band empty, which is the correct behaviour: exact arithmetic has no
    ambiguity to report.
    """
    count = len(squares)
    if count < 2:
        raise ContactExtractionError("bad-request", f"need at least two squares, got {count}")
    floor_value = mp.mpf(floor)
    ceiling = floor_value * mp.mpf(ambiguity_ratio)

    pair_contacts: list[Incidence] = []
    ambiguous: list[Incidence] = []
    contact_magnitudes: list[Scalar] = []
    strict_magnitudes: list[Scalar] = []

    def classify(kind: str, left: int, right: str, margin, sink: list[Incidence]) -> None:
        """Sort one relation into contact, strict separation, or the refused band."""
        incidence = Incidence(kind=kind, left=left, right=right, margin=_decimal(margin))
        try:
            magnitude = abs(mp.mpf(margin))
        except TypeError, ValueError:
            magnitude = None
        if sign(margin) == 0:
            sink.append(incidence)
            if magnitude is not None:
                contact_magnitudes.append(magnitude)
            return
        if magnitude is None:
            return
        strict_magnitudes.append(magnitude)
        if floor_value > 0 and magnitude <= ceiling:
            ambiguous.append(incidence)

    for left in range(count):
        for right in range(left + 1, count):
            classify(
                "pair",
                left,
                str(right),
                _pair_margin(squares[left], squares[right], sign),
                pair_contacts,
            )

    wall_contacts: list[Incidence] = []
    for index, square in enumerate(squares):
        for corner, (x, y) in enumerate(square):
            for wall, margin in zip(WALLS, (x, y, side - x, side - y), strict=True):
                classify("wall", index, f"{wall}:{corner}", margin, wall_contacts)

    classes: list[list[int]] = []
    for index, square in enumerate(squares):
        for members in classes:
            if _same_orientation(squares[members[0]], square, sign):
                members.append(index)
                break
        else:
            classes.append([index])
    angle_classes = tuple(
        AngleClass(
            label=f"class-{position}",
            members=tuple(members),
            degrees=_orientation_degrees(squares[members[0]]),
        )
        for position, members in enumerate(classes)
    )

    worst_contact = max(contact_magnitudes) if contact_magnitudes else mp.mpf(0)
    smallest_strict = min(strict_magnitudes) if strict_magnitudes else None
    decades = None
    if smallest_strict is not None and worst_contact > 0:
        decades = _decimal(mp.log10(smallest_strict / worst_contact), 6)

    return ContactStructure(
        n=count,
        side=_decimal(side),
        floor=floor,
        ambiguity_ceiling=_decimal(ceiling, 6),
        pair_contacts=tuple(pair_contacts),
        wall_contacts=tuple(wall_contacts),
        ambiguous=tuple(ambiguous),
        angle_classes=angle_classes,
        pairs_tested=count * (count - 1) // 2,
        wall_relations_tested=count * 4 * len(WALLS),
        worst_contact_margin=_decimal(worst_contact, 6),
        smallest_strict_separation=(
            _decimal(smallest_strict, 6) if smallest_strict is not None else "none"
        ),
        separation_decades=decades,
    )


def require_decided(structure: ContactStructure) -> ContactStructure:
    """Return the structure, or refuse if any incidence sat in the ambiguous band."""
    if structure.ambiguous:
        listed = ", ".join(
            f"{incidence.kind} {incidence.left}-{incidence.right} at {incidence.margin}"
            for incidence in structure.ambiguous[:5]
        )
        raise ContactExtractionError(
            "undecidable-incidence",
            f"{len(structure.ambiguous)} incidence(s) fall between the floor "
            f"{structure.floor} and the ambiguity ceiling {structure.ambiguity_ceiling}: "
            f"{listed}",
        )
    return structure
