"""Relational certificate atoms: weighted majority, k-of-S, and floor charges.

T-025 already prices a relation as a threshold atom ``(S, a, k, w)``: weight ``w`` when
a core holds at least ``k`` tokens of ``S``. That class is `ThresholdAtom` and this
module reuses it. Floor atoms are a different tagged class. A floor atom
``(S, a, t, w)`` with nonnegative integer multiplicities ``a``, divisor ``t >= 2`` and
weight ``w >= 0`` charges ``w floor(a(P) / t)`` to a core ``P`` and budgets
``w floor(a(S) / t)``. The two are not equivalent when ``a = 1`` and ``|S| >= 2k``: a
2-of-5 threshold atom charges ``1`` to a four-site core, while the floor atom with the
same sites, unit multiplicities and divisor 2 charges ``2``.

Counting for floor atoms: disjoint closed cores consume disjoint site traces, so
``sum_i floor(a(P_i) / t) <= floor(sum_i a(P_i) / t) <= floor(a(S) / t)``. Superadditivity
of ``floor`` is the first step; disjointness of traces is the second.

`FloorCertificate` is the relational record: point atoms, threshold atoms (legacy
all-ones or weighted-majority), and floor atoms, with the net stored as
``direction_steps`` and ``angle_limit``. The serializer emits that pair and never
``half_tangents``, so it round-trips with the loader (think-h1ju). Ordinary T-025 bytes
are not this class; the CLI delegates those to `devtools.decide_threshold_certificate`.

Coverage. Condition 5' is decided twice, by methods that share the event geometry and
not the charge arithmetic:

* event-cell: integer difference arrays of token counts, then threshold or floor, in
  Python integers so a zero-charge atom with weight or divisor ``2**63`` cannot overflow
  a NumPy ``int64`` conversion (think-k1pe);
* interval boxes: inner and outer Fraction containment of each reachable event cell
  against each site rectangle, independently of the prefix sums.

Those two exact routes are an admission gate. They are not the floating-point interval
branch-and-bound of `sqpack.fractional.threshold_interval`. A T-id in this class still
waits on two-route C4 against that independent verifier.
"""

# The cell witness is the sweep's; one construction, the same admissible centre.
# pyright: reportPrivateUsage=false

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from fractions import Fraction
from math import lcm
from typing import Any, Literal

from sqpack.fractional.certificate import (
    Certificate,
    ConditionReport,
    Verdict,
    closed_form_conditions,
    d4_images,
)
from sqpack.fractional.generate import net_half_tangents
from sqpack.fractional.model import Atom, Direction, require_nonnegative_atom_weights
from sqpack.fractional.sweep import (
    SpanReduction,
    _cell_witness,
    centre_domain,
    reduce_to_cells,
    reduce_to_spans,
)
from sqpack.fractional.threshold import (
    ThresholdAtom,
    ThresholdCertificate,
    closed_form_threshold_conditions,
    exact_charge,
)

Point = tuple[Fraction, Fraction]
Contains = Callable[[Fraction, Fraction], bool]
RouteName = Literal["event-cell", "interval"]

RELATIONAL_VARIANT = "relational/v1"
FLOOR_VARIANT = "floor/v1"
_EVENT_ONLY = Fraction(0)
_RATIONAL = re.compile(r"-?[0-9]+(?:/[1-9][0-9]*)?")


def _record_rational(value: object, field: str) -> Fraction:
    if not isinstance(value, str) or _RATIONAL.fullmatch(value) is None:
        raise TypeError(f"field {field!r} must be an exact rational string, got {value!r}")
    return Fraction(value)


def _json_int(value: object, field: str) -> int:
    if type(value) is not int:
        raise TypeError(f"field {field!r} must be a JSON integer, got {value!r}")
    return value


@dataclass(frozen=True, slots=True)
class FloorAtom:
    """``(S, a, t, w)``: weight ``w * floor(a(P) / t)`` on a core, budget ``w floor(A / t)``.

    ``sites`` are distinct. Each carries a positive integer multiplicity; a site with no
    tokens is omitted rather than declared empty (zero is refused). ``divisor`` is ``t``
    and must be at least 2: ``t = 1`` is a sum of point atoms. Weight may be zero.

    An atom with ``A < t`` or weight zero is inert: charge and budget are exact zero for
    every core. Coverage routes skip it before converting a weight or divisor onto a
    packed integer grid, so ``weight = 2**63`` and ``t = 2**63`` do not overflow.
    """

    sites: tuple[Point, ...]
    multiplicities: tuple[int, ...]
    divisor: int
    weight: Fraction

    def __post_init__(self) -> None:
        if not isinstance(self.divisor, int) or isinstance(self.divisor, bool):
            raise TypeError("the divisor must be an integer")
        if self.divisor < 2:
            raise ValueError(
                f"divisor {self.divisor} is below 2; a floor-1 atom is a sum of point atoms"
            )
        if not self.sites:
            raise ValueError("a floor atom needs at least one site")
        if len(set(self.sites)) != len(self.sites):
            raise ValueError("a floor atom's sites must be distinct")
        if len(self.multiplicities) != len(self.sites):
            raise ValueError(
                f"{len(self.sites)} sites carry {len(self.multiplicities)} multiplicities; "
                "every site needs exactly one token count"
            )
        for multiplicity in self.multiplicities:
            if not isinstance(multiplicity, int) or isinstance(multiplicity, bool):
                raise TypeError(
                    f"multiplicity {multiplicity!r} is not an integer; a token count may "
                    "not be a bool, a float or a string"
                )
            if multiplicity < 1:
                raise ValueError(
                    f"multiplicity {multiplicity} is not positive; a site carrying no "
                    "tokens is left out rather than declared empty"
                )
        if isinstance(self.weight, bool) or not isinstance(self.weight, int | Fraction):
            raise TypeError(f"weight {self.weight!r} is not a nonnegative rational")
        weight = Fraction(self.weight)
        if weight < 0:
            raise ValueError(
                f"floor atom has weight {weight} < 0; the counting argument needs every "
                "weight nonnegative"
            )
        object.__setattr__(self, "weight", weight)

    @property
    def token_count(self) -> int:
        return sum(self.multiplicities)

    @property
    def inert(self) -> bool:
        """True when every core is charged zero, including weight zero and ``A < t``."""

        return self.weight == 0 or self.token_count < self.divisor

    @property
    def budget(self) -> Fraction:
        return self.weight * (self.token_count // self.divisor)

    @property
    def key(self) -> tuple[tuple[tuple[Fraction, Fraction, int], ...], int]:
        return (
            tuple(
                sorted(
                    (x, y, a) for (x, y), a in zip(self.sites, self.multiplicities, strict=True)
                )
            ),
            self.divisor,
        )

    def trace_count(self, contains: Contains) -> int:
        return sum(
            a
            for (x, y), a in zip(self.sites, self.multiplicities, strict=True)
            if contains(x, y)
        )

    def charge(self, contains: Contains) -> Fraction:
        return self.weight * (self.trace_count(contains) // self.divisor)

    def images(self, outer_side: Fraction) -> tuple[FloorAtom, ...]:
        per_site = [d4_images(x, y, outer_side) for x, y in self.sites]
        return tuple(
            FloorAtom(
                tuple(images[g] for images in per_site),
                self.multiplicities,
                self.divisor,
                self.weight,
            )
            for g in range(8)
        )

    def orbit(self, outer_side: Fraction) -> tuple[FloorAtom, ...]:
        seen: dict[tuple[tuple[tuple[Fraction, Fraction, int], ...], int], FloorAtom] = {}
        for image in self.images(outer_side):
            seen.setdefault(image.key, image)
        return tuple(seen.values())

    def to_record(self) -> dict[str, Any]:
        return {
            "variant": FLOOR_VARIANT,
            "sites": [[str(x), str(y)] for x, y in self.sites],
            "multiplicities": list(self.multiplicities),
            "divisor": self.divisor,
            "weight": str(self.weight),
        }

    @classmethod
    def from_record(cls, record: object) -> FloorAtom:
        if not isinstance(record, dict):
            raise TypeError("a floor atom record must be a JSON object")
        variant = record.get("variant")
        if variant != FLOOR_VARIANT:
            raise ValueError(
                f"floor atom declares variant {variant!r}, which this reader does not "
                f"support; expected {FLOOR_VARIANT!r}"
            )
        for banned in ("points", "threshold", "weighted_points", "half_tangents"):
            if banned in record:
                raise ValueError(
                    f"floor atom carries {banned!r}; floor records use tagged 'sites' "
                    "and 'divisor', not threshold fields"
                )
        rows = record.get("sites")
        if not isinstance(rows, list) or not rows:
            raise ValueError("field 'sites' must be a nonempty JSON array")
        sites: list[Point] = []
        for index, row in enumerate(rows):
            if not isinstance(row, list) or len(row) != 2:
                raise ValueError(f"sites[{index}] must be [x, y]")
            sites.append(
                (
                    _record_rational(row[0], f"sites[{index}][0]"),
                    _record_rational(row[1], f"sites[{index}][1]"),
                )
            )
        counts = record.get("multiplicities")
        if not isinstance(counts, list):
            raise TypeError("field 'multiplicities' must be a JSON array")
        multiplicities = tuple(
            _json_int(count, f"multiplicities[{index}]") for index, count in enumerate(counts)
        )
        return cls(
            tuple(sites),
            multiplicities,
            _json_int(record.get("divisor"), "divisor"),
            _record_rational(record.get("weight"), "weight"),
        )


def disjoint_floor_charge_sum(atom: FloorAtom, traces: tuple[int, ...]) -> Fraction:
    """``w * sum floor(a_i / t)`` for traces of pairwise disjoint cores.

    Raises if the traces cannot be disjoint: their tokens would exceed ``A``.
    """

    if any(trace < 0 for trace in traces):
        raise ValueError("a core trace cannot be negative")
    if sum(traces) > atom.token_count:
        raise ValueError("traces exceed the atom's tokens; they are not disjoint")
    return atom.weight * sum(trace // atom.divisor for trace in traces)


@dataclass(frozen=True, slots=True)
class FloorCertificate:
    """A relational certificate: points, threshold atoms, and floor atoms on one net.

    The net is ``direction_steps`` equal steps up to ``angle_limit``. `to_record` emits
    that pair and not ``half_tangents``, matching the loader.
    """

    n: int
    outer_side: Fraction
    square_side: Fraction
    atoms: tuple[Atom, ...]
    threshold_atoms: tuple[ThresholdAtom, ...]
    floor_atoms: tuple[FloorAtom, ...]
    direction_steps: int
    angle_limit: Fraction
    symmetry: str = "D4"

    def __post_init__(self) -> None:
        if not isinstance(self.direction_steps, int) or isinstance(self.direction_steps, bool):
            raise TypeError("direction_steps must be an integer")
        if self.direction_steps < 1:
            raise ValueError("the direction net needs at least one step")
        self.point_certificate  # noqa: B018 - constructing it is the check
        keys = [atom.key for atom in self.threshold_atoms]
        if len(set(keys)) != len(keys):
            raise ValueError("two threshold atoms share the same (sites, threshold)")
        floor_keys = [atom.key for atom in self.floor_atoms]
        if len(set(floor_keys)) != len(floor_keys):
            raise ValueError("two floor atoms share the same (sites, divisor)")
        require_nonnegative_atom_weights(self.atoms)
        for atom in self.floor_atoms:
            for x, y in atom.sites:
                if not (0 <= x <= self.outer_side and 0 <= y <= self.outer_side):
                    raise ValueError(f"floor site ({x}, {y}) lies outside the container")

    @property
    def half_tangents(self) -> tuple[Fraction, ...]:
        return net_half_tangents(self.angle_limit, self.direction_steps)

    @property
    def point_certificate(self) -> Certificate:
        return Certificate(
            n=self.n,
            outer_side=self.outer_side,
            square_side=self.square_side,
            atoms=self.atoms,
            half_tangents=self.half_tangents,
            symmetry=self.symmetry,
        )

    @property
    def threshold_certificate(self) -> ThresholdCertificate:
        return ThresholdCertificate(
            n=self.n,
            outer_side=self.outer_side,
            square_side=self.square_side,
            atoms=self.atoms,
            threshold_atoms=self.threshold_atoms,
            half_tangents=self.half_tangents,
            symmetry=self.symmetry,
        )

    @property
    def directions(self) -> tuple[Direction, ...]:
        return self.point_certificate.directions

    @property
    def point_mass(self) -> Fraction:
        return sum((atom.weight for atom in self.atoms), start=Fraction(0))

    @property
    def threshold_budget(self) -> Fraction:
        return sum((atom.budget for atom in self.threshold_atoms), start=Fraction(0))

    @property
    def floor_budget(self) -> Fraction:
        return sum((atom.budget for atom in self.floor_atoms), start=Fraction(0))

    @property
    def total_budget(self) -> Fraction:
        return self.point_mass + self.threshold_budget + self.floor_budget

    def to_record(self) -> dict[str, Any]:
        return {
            "variant": RELATIONAL_VARIANT,
            "n": self.n,
            "outer_side": str(self.outer_side),
            "square_side": str(self.square_side),
            "angle_limit": str(self.angle_limit),
            "direction_steps": self.direction_steps,
            "symmetry": self.symmetry,
            "atoms": [[str(a.x), str(a.y), str(a.weight)] for a in self.atoms],
            "threshold_atoms": [atom.to_record() for atom in self.threshold_atoms],
            "floor_atoms": [atom.to_record() for atom in self.floor_atoms],
            "total_budget": str(self.total_budget),
        }

    @classmethod
    def from_record(cls, record: object) -> FloorCertificate:
        if not isinstance(record, dict):
            raise TypeError("a relational certificate record must be a JSON object")
        if "half_tangents" in record:
            raise ValueError(
                "field 'half_tangents' is not a relational-certificate field; the net is "
                "'direction_steps' and 'angle_limit'"
            )
        variant = record.get("variant", RELATIONAL_VARIANT)
        if variant != RELATIONAL_VARIANT:
            raise ValueError(
                f"variant {variant!r} is not {RELATIONAL_VARIANT!r}; ordinary threshold "
                "records go through the preserved threshold loader"
            )
        atoms_record = record.get("atoms", [])
        if not isinstance(atoms_record, list):
            raise TypeError("field 'atoms' must be a JSON array")
        atoms: list[Atom] = []
        for index, entry in enumerate(atoms_record):
            if not isinstance(entry, list) or len(entry) != 3:
                raise ValueError(f"atoms[{index}] must be a three-element JSON array")
            x, y, weight = (
                _record_rational(value, f"atoms[{index}][{column}]")
                for column, value in enumerate(entry)
            )
            atoms.append(Atom(f"{index:04d}", x, y, weight))
        thresholds_record = record.get("threshold_atoms", [])
        if not isinstance(thresholds_record, list):
            raise TypeError("field 'threshold_atoms' must be a JSON array")
        threshold_atoms = tuple(ThresholdAtom.from_record(entry) for entry in thresholds_record)
        floors_record = record.get("floor_atoms", [])
        if not isinstance(floors_record, list):
            raise TypeError("field 'floor_atoms' must be a JSON array")
        floor_atoms = tuple(FloorAtom.from_record(entry) for entry in floors_record)
        return cls(
            n=_json_int(record.get("n"), "n"),
            outer_side=_record_rational(record.get("outer_side"), "outer_side"),
            square_side=_record_rational(record.get("square_side"), "square_side"),
            atoms=tuple(atoms),
            threshold_atoms=threshold_atoms,
            floor_atoms=floor_atoms,
            direction_steps=_json_int(record.get("direction_steps"), "direction_steps"),
            angle_limit=_record_rational(record.get("angle_limit"), "angle_limit"),
            symmetry=str(record.get("symmetry", "D4")),
        )


RelationalCertificate = FloorCertificate


def relational_weight_scale(
    atoms: Iterable[Atom],
    threshold_atoms: Iterable[ThresholdAtom],
    floor_atoms: Iterable[FloorAtom],
) -> int:
    scale = 1
    for atom in atoms:
        scale = lcm(scale, atom.weight.denominator)
    for atom in threshold_atoms:
        scale = lcm(scale, atom.weight.denominator)
    for atom in floor_atoms:
        scale = lcm(scale, atom.weight.denominator)
    return scale


def _scaled(weight: Fraction, scale: int) -> int:
    scaled = weight * scale
    if scaled.denominator != 1:
        raise ValueError("weights are not integers on the declared common scale")
    return int(scaled)


def exact_relational_charge(
    atoms: Iterable[Atom],
    threshold_atoms: Iterable[ThresholdAtom],
    floor_atoms: Iterable[FloorAtom],
    contains: Contains,
) -> Fraction:
    """Charge of one core by membership counting, atom by atom."""

    return exact_charge(atoms, threshold_atoms, contains) + sum(
        (atom.charge(contains) for atom in floor_atoms), start=Fraction(0)
    )


def _event_atoms(
    atoms: tuple[Atom, ...],
    threshold_atoms: tuple[ThresholdAtom, ...],
    floor_atoms: tuple[FloorAtom, ...],
) -> tuple[Atom, ...]:
    extra = [
        Atom(f"t{index}:{offset}", x, y, _EVENT_ONLY)
        for index, atom in enumerate(threshold_atoms)
        for offset, (x, y) in enumerate(atom.points)
    ]
    extra.extend(
        Atom(f"f{index}:{offset}", x, y, _EVENT_ONLY)
        for index, atom in enumerate(floor_atoms)
        for offset, (x, y) in enumerate(atom.sites)
    )
    return (*atoms, *extra)


def _empty_grid(width: int, height: int) -> list[list[int]]:
    return [[0] * height for _ in range(width)]


def _add_rectangle(
    grid: list[list[int]],
    u_index: dict[Fraction, int],
    v_index: dict[Fraction, int],
    rectangle: tuple[Fraction, ...],
    value: int,
) -> None:
    if value == 0:
        return
    left, right = u_index[rectangle[0]], u_index[rectangle[1]]
    bottom, top = v_index[rectangle[2]], v_index[rectangle[3]]
    grid[left][bottom] += value
    grid[right][bottom] -= value
    grid[left][top] -= value
    grid[right][top] += value


def _prefix_sum(grid: list[list[int]]) -> None:
    if not grid:
        return
    height = len(grid[0])
    for row in grid:
        running = 0
        for j in range(height):
            running += row[j]
            row[j] = running
    for i in range(1, len(grid)):
        previous, current = grid[i - 1], grid[i]
        for j in range(height):
            current[j] += previous[j]


def _paint_counts(
    reduction_rectangles: tuple[tuple[Fraction, ...], ...],
    start: int,
    multiplicities: tuple[int, ...],
    u_index: dict[Fraction, int],
    v_index: dict[Fraction, int],
    *,
    width: int,
    height: int,
) -> list[list[int]]:
    counts = _empty_grid(width, height)
    for offset, multiplicity in enumerate(multiplicities):
        _add_rectangle(
            counts, u_index, v_index, reduction_rectangles[start + offset], multiplicity
        )
    _prefix_sum(counts)
    return counts


def event_cell_charge_grid(
    atoms: tuple[Atom, ...],
    threshold_atoms: tuple[ThresholdAtom, ...],
    floor_atoms: tuple[FloorAtom, ...],
    direction: Direction,
    *,
    outer_side: Fraction,
    square_side: Fraction,
    scale: int,
) -> tuple[SpanReduction, list[list[int]], int]:
    """Integer charge on the event grid by count-then-threshold and count-then-floor.

    Prefix sums use Python integers. Inert floor atoms still contribute event sites and
    never have a weight or divisor packed into a fixed-width integer.
    """

    everything = _event_atoms(atoms, threshold_atoms, floor_atoms)
    reduction = reduce_to_spans(everything, direction, outer_side, square_side)
    u_index = {value: index for index, value in enumerate(reduction.u_events)}
    v_index = {value: index for index, value in enumerate(reduction.v_events)}
    width, height = len(reduction.u_events), len(reduction.v_events)
    charge = _empty_grid(width, height)
    cursor = 0
    for atom in atoms:
        _add_rectangle(
            charge, u_index, v_index, reduction.rectangles[cursor], _scaled(atom.weight, scale)
        )
        cursor += 1
    _prefix_sum(charge)
    for atom in threshold_atoms:
        counts = _paint_counts(
            reduction.rectangles,
            cursor,
            atom.multiplicities,
            u_index,
            v_index,
            width=width,
            height=height,
        )
        cursor += atom.size
        scaled = _scaled(atom.weight, scale)
        if scaled == 0:
            continue
        for i in range(width):
            charge_row, count_row = charge[i], counts[i]
            for j in range(height):
                if count_row[j] >= atom.threshold:
                    charge_row[j] += scaled
    for atom in floor_atoms:
        size = len(atom.sites)
        if atom.inert:
            cursor += size
            continue
        counts = _paint_counts(
            reduction.rectangles,
            cursor,
            atom.multiplicities,
            u_index,
            v_index,
            width=width,
            height=height,
        )
        cursor += size
        scaled = _scaled(atom.weight, scale)
        divisor = atom.divisor
        for i in range(width):
            charge_row, count_row = charge[i], counts[i]
            for j in range(height):
                charge_row[j] += (count_row[j] // divisor) * scaled
    return reduction, charge, scale


def _span_minimum(
    reduction: SpanReduction, charge: list[list[int]]
) -> tuple[int, tuple[int, int]]:
    best: int | None = None
    cell: tuple[int, int] | None = None
    for i, j0, j1 in reduction.spans:
        row = charge[i]
        for j in range(j0, j1 + 1):
            score = row[j]
            if best is None or score < best:
                best, cell = score, (i, j)
    if best is None or cell is None:
        raise ValueError("the sweep produced no reachable cell")
    return best, cell


def _witness_at(
    u_events: tuple[Fraction, ...],
    v_events: tuple[Fraction, ...],
    cell: tuple[int, int],
    *,
    outer_side: Fraction,
    square_side: Fraction,
    direction: Direction,
) -> Point:
    i, j = cell
    return _cell_witness(
        centre_domain(outer_side, square_side, direction),
        u_events[i],
        u_events[i + 1],
        v_events[j],
        v_events[j + 1],
    )


def minimum_charge_event_cell(
    atoms: tuple[Atom, ...],
    threshold_atoms: tuple[ThresholdAtom, ...],
    floor_atoms: tuple[FloorAtom, ...],
    direction: Direction,
    *,
    outer_side: Fraction,
    square_side: Fraction,
) -> tuple[Fraction, Point]:
    """Least reachable charge at one direction by the event-cell count grids."""

    scale = relational_weight_scale(atoms, threshold_atoms, floor_atoms)
    reduction, charge, _ = event_cell_charge_grid(
        atoms,
        threshold_atoms,
        floor_atoms,
        direction,
        outer_side=outer_side,
        square_side=square_side,
        scale=scale,
    )
    best, cell = _span_minimum(reduction, charge)
    return Fraction(best, scale), _witness_at(
        reduction.u_events,
        reduction.v_events,
        cell,
        outer_side=outer_side,
        square_side=square_side,
        direction=direction,
    )


def _site_rectangle(
    direction: Direction, x: Fraction, y: Fraction, half: Fraction
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    u = direction.ux * x + direction.uy * y
    v = direction.vx * x + direction.vy * y
    return (u - half, u + half, v - half, v + half)


def _box_certain(
    box: tuple[Fraction, Fraction, Fraction, Fraction],
    rectangle: tuple[Fraction, Fraction, Fraction, Fraction],
) -> bool:
    u0, u1, v0, v1 = box
    ulo, uhi, vlo, vhi = rectangle
    return ulo <= u0 and u1 <= uhi and vlo <= v0 and v1 <= vhi


def _box_possible(
    box: tuple[Fraction, Fraction, Fraction, Fraction],
    rectangle: tuple[Fraction, Fraction, Fraction, Fraction],
) -> bool:
    u0, u1, v0, v1 = box
    ulo, uhi, vlo, vhi = rectangle
    return u0 < uhi and u1 > ulo and v0 < vhi and v1 > vlo


def _certain_on(
    box: tuple[Fraction, Fraction, Fraction, Fraction],
) -> Callable[[tuple[Fraction, Fraction, Fraction, Fraction]], bool]:
    def holds(rectangle: tuple[Fraction, Fraction, Fraction, Fraction]) -> bool:
        return _box_certain(box, rectangle)

    return holds


def _possible_on(
    box: tuple[Fraction, Fraction, Fraction, Fraction],
) -> Callable[[tuple[Fraction, Fraction, Fraction, Fraction]], bool]:
    def holds(rectangle: tuple[Fraction, Fraction, Fraction, Fraction]) -> bool:
        return _box_possible(box, rectangle)

    return holds


def _scaled_charge_from_holds(
    atoms: tuple[Atom, ...],
    threshold_atoms: tuple[ThresholdAtom, ...],
    floor_atoms: tuple[FloorAtom, ...],
    rectangles: dict[Point, tuple[Fraction, Fraction, Fraction, Fraction]],
    holds: Callable[[tuple[Fraction, Fraction, Fraction, Fraction]], bool],
    *,
    scale: int,
) -> int:
    total = 0
    for atom in atoms:
        if holds(rectangles[(atom.x, atom.y)]):
            total += _scaled(atom.weight, scale)
    for atom in threshold_atoms:
        tokens = sum(
            multiplicity
            for site, multiplicity in zip(atom.points, atom.multiplicities, strict=True)
            if holds(rectangles[site])
        )
        if tokens >= atom.threshold:
            total += _scaled(atom.weight, scale)
    for atom in floor_atoms:
        tokens = sum(
            multiplicity
            for site, multiplicity in zip(atom.sites, atom.multiplicities, strict=True)
            if holds(rectangles[site])
        )
        total += (tokens // atom.divisor) * _scaled(atom.weight, scale)
    return total


def minimum_charge_interval_boxes(
    atoms: tuple[Atom, ...],
    threshold_atoms: tuple[ThresholdAtom, ...],
    floor_atoms: tuple[FloorAtom, ...],
    direction: Direction,
    *,
    outer_side: Fraction,
    square_side: Fraction,
) -> tuple[Fraction, Point]:
    """Least reachable charge by inner/outer Fraction bounds on each event cell.

    The lower bound uses sites whose closed rectangle contains the whole cell; the upper
    bound uses sites whose rectangle meets the open cell. On the event arrangement those
    bounds agree, which is the width-zero enclosure. No float enters the decision.
    """

    scale = relational_weight_scale(atoms, threshold_atoms, floor_atoms)
    everything = _event_atoms(atoms, threshold_atoms, floor_atoms)
    reduction = reduce_to_cells(everything, direction, outer_side, square_side)
    half = square_side / 2
    rectangles = {
        (x, y): _site_rectangle(direction, x, y, half)
        for x, y in (
            [(atom.x, atom.y) for atom in atoms]
            + [point for atom in threshold_atoms for point in atom.points]
            + [site for atom in floor_atoms for site in atom.sites]
        )
    }
    best: int | None = None
    cell: tuple[int, int] | None = None
    for i, j in reduction.cells:
        box = (
            reduction.u_events[i],
            reduction.u_events[i + 1],
            reduction.v_events[j],
            reduction.v_events[j + 1],
        )
        lower = _scaled_charge_from_holds(
            atoms,
            threshold_atoms,
            floor_atoms,
            rectangles,
            _certain_on(box),
            scale=scale,
        )
        upper = _scaled_charge_from_holds(
            atoms,
            threshold_atoms,
            floor_atoms,
            rectangles,
            _possible_on(box),
            scale=scale,
        )
        if lower != upper:
            raise ValueError(
                f"interval enclosure has width on event cell {(i, j)}: [{lower}, {upper}]"
            )
        if best is None or lower < best:
            best, cell = lower, (i, j)
    if best is None or cell is None:
        raise ValueError("the interval route decided no reachable cell")
    return Fraction(best, scale), _witness_at(
        reduction.u_events,
        reduction.v_events,
        cell,
        outer_side=outer_side,
        square_side=square_side,
        direction=direction,
    )


def _condition_symmetric_floor_atoms(certificate: FloorCertificate) -> ConditionReport:
    name = "Condition 1' floor atoms carry the declared symmetry"
    if certificate.symmetry != "D4":
        return ConditionReport(
            name, f"only D4 is supported, not {certificate.symmetry!r}", holds=False
        )
    weights = {atom.key: atom.weight for atom in certificate.floor_atoms}
    for atom in certificate.floor_atoms:
        for image in atom.images(certificate.outer_side):
            if weights.get(image.key) != atom.weight:
                return ConditionReport(
                    name,
                    f"floor atom on {atom.sites} has no matching image on {image.sites}",
                    holds=False,
                )
    return ConditionReport(
        name,
        f"{len(certificate.floor_atoms)} floor atoms closed under D4 about the centre",
        holds=True,
    )


def _condition_budget_below_n(certificate: FloorCertificate) -> ConditionReport:
    total = certificate.total_budget
    return ConditionReport(
        "Condition 2' total budget below n",
        f"point mass {certificate.point_mass} + threshold budget "
        f"{certificate.threshold_budget} + floor budget {certificate.floor_budget} = "
        f"{total} against n = {certificate.n}",
        holds=total < certificate.n,
    )


def closed_form_relational_conditions(
    certificate: FloorCertificate,
) -> tuple[ConditionReport, ...]:
    """Conditions 1', 2', 3 and 4: everything but the two coverage routes."""

    point = [
        report
        for report in closed_form_conditions(certificate.point_certificate)
        if not report.name.startswith("Condition 2")
    ]
    threshold_symmetry = [
        report
        for report in closed_form_threshold_conditions(certificate.threshold_certificate)
        if report.name.startswith("Condition 1'")
    ]
    return (
        point[0],
        *threshold_symmetry,
        _condition_symmetric_floor_atoms(certificate),
        _condition_budget_below_n(certificate),
        *point[1:],
    )


def minimum_on_certificate(
    certificate: FloorCertificate, direction: Direction, *, route: RouteName
) -> tuple[Fraction, Point]:
    if route == "event-cell":
        return minimum_charge_event_cell(
            certificate.atoms,
            certificate.threshold_atoms,
            certificate.floor_atoms,
            direction,
            outer_side=certificate.outer_side,
            square_side=certificate.square_side,
        )
    return minimum_charge_interval_boxes(
        certificate.atoms,
        certificate.threshold_atoms,
        certificate.floor_atoms,
        direction,
        outer_side=certificate.outer_side,
        square_side=certificate.square_side,
    )


def sweep_relational_directions(
    certificate: FloorCertificate, *, route: RouteName
) -> tuple[tuple[Fraction, str], ...]:
    return tuple(
        (minimum_on_certificate(certificate, direction, route=route)[0], direction.label)
        for direction in certificate.directions
    )


def verify_relational(certificate: FloorCertificate) -> Verdict:
    """Closed-form conditions plus both exact coverage routes. Never short-circuits."""

    conditions = list(closed_form_relational_conditions(certificate))
    event = sweep_relational_directions(certificate, route="event-cell")
    interval = sweep_relational_directions(certificate, route="interval")
    event_worst = min(event, key=lambda item: item[0])
    interval_worst = min(interval, key=lambda item: item[0])
    agree = event_worst[0] == interval_worst[0]
    conditions.append(
        ConditionReport(
            "Condition 5' event-cell every reachable cell is charged at least 1",
            f"least cell charge {event_worst[0]} at direction {event_worst[1]}",
            holds=event_worst[0] >= 1,
        )
    )
    conditions.append(
        ConditionReport(
            "Condition 5' interval every reachable cell is charged at least 1",
            f"least cell charge {interval_worst[0]} at direction {interval_worst[1]}",
            holds=interval_worst[0] >= 1,
        )
    )
    conditions.append(
        ConditionReport(
            "the two exact routes agree on the least charge",
            f"event-cell {event_worst[0]} against interval {interval_worst[0]}",
            holds=agree,
        )
    )
    worst = event_worst[0] if agree else min(event_worst[0], interval_worst[0])
    return Verdict(tuple(conditions), certificate.total_budget, worst, event_worst[1])


__all__ = [
    "FLOOR_VARIANT",
    "RELATIONAL_VARIANT",
    "FloorAtom",
    "FloorCertificate",
    "Point",
    "RelationalCertificate",
    "RouteName",
    "closed_form_relational_conditions",
    "disjoint_floor_charge_sum",
    "event_cell_charge_grid",
    "exact_relational_charge",
    "minimum_charge_event_cell",
    "minimum_charge_interval_boxes",
    "minimum_on_certificate",
    "relational_weight_scale",
    "sweep_relational_directions",
    "verify_relational",
]
