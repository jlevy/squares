"""Adaptive, strictly interior cores for a parent-square obstruction.

Rows retain four independent rationals ``(a, b, t, B)``: a closed interval of
parent half-tangents, one core half-tangent, and its side. The parent side ``A``
determines the centre domain; ``B`` determines site membership. Replacing either
by the other changes the theorem.

At parent half-tangent ``u``, legal centres are ``[h(u), L-h(u)]**2`` with
``h(u)=A*(1+2*u-u*u)/(2*(1+u*u))``. On ``0<=u<1``, its derivative has the sign
of ``1-2*u-u*u``: its only stationary point is a maximum. These domains are
nested, so their union on ``[a,b]`` is exactly the square with margin
``min(h(a),h(b))``. This remains true when the last rational endpoint slightly
exceeds ``tan(pi/8)``. The interval decision covers that entire union.

The exact premise checks below establish a contiguous folded angle cover, D4
invariance, and strict core containment throughout each row by minimizing
vertex-projection quadratics, including their interior minima. If every row's
domain has charge at least ``Gamma`` and the budget is less than ``n*Gamma``,
there is no packing of n parents. The strict bound is ``s(n)>L/A``: closed cores
lie in disjoint parent interiors, and the minimum packing side is attained.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Any

from sqpack.fractional.certificate import d4_images
from sqpack.fractional.model import Atom, require_nonnegative_atom_weights
from sqpack.fractional.threshold import ThresholdAtom


def _rational(value: object, field: str) -> Fraction:
    if type(value) is int or type(value) is Fraction:
        return Fraction(value)
    raise ValueError(f"{field} must be an exact rational (Fraction or int)")


@dataclass(frozen=True, slots=True)
class ParentCoreRow:
    left: Fraction
    right: Fraction
    half_tangent: Fraction
    core_side: Fraction

    def __post_init__(self) -> None:
        for field in ("left", "right", "half_tangent", "core_side"):
            object.__setattr__(self, field, _rational(getattr(self, field), field))

    @property
    def rotation(self) -> tuple[Fraction, Fraction]:
        tangent = self.half_tangent
        denominator = 1 + tangent * tangent
        return (1 - tangent * tangent) / denominator, 2 * tangent / denominator

    def centre_margin(self, parent_side: Fraction) -> Fraction:
        """The exact margin of the union of the row's parent-centre domains."""
        return (
            parent_side
            * min((1 + 2 * u - u * u) / (1 + u * u) for u in (self.left, self.right))
            / 2
        )


@dataclass(frozen=True, slots=True)
class ParentCoreCertificate:
    n: int
    outer_side: Fraction
    parent_side: Fraction
    minimum_charge: Fraction
    atoms: tuple[Atom, ...]
    threshold_atoms: tuple[ThresholdAtom, ...]
    rows: tuple[ParentCoreRow, ...]

    def __post_init__(self) -> None:
        for field in ("outer_side", "parent_side", "minimum_charge"):
            object.__setattr__(self, field, _rational(getattr(self, field), field))

    @property
    def budget(self) -> Fraction:
        return sum((atom.weight for atom in self.atoms), Fraction(0)) + sum(
            (atom.budget for atom in self.threshold_atoms), Fraction(0)
        )


@dataclass(frozen=True, slots=True)
class ParentCorePremises:
    budget: Fraction
    minimum_containment_numerator: Fraction
    final_half_tangent: Fraction
    rows: int


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _quadratic_minimum(
    constant: Fraction,
    linear: Fraction,
    square: Fraction,
    left: Fraction,
    right: Fraction,
) -> Fraction:
    candidates = [left, right]
    if square > 0:
        vertex = -linear / (2 * square)
        if left < vertex < right:
            candidates.append(vertex)
    return min(constant + linear * u + square * u * u for u in candidates)


def _validate_symmetry(certificate: ParentCoreCertificate) -> None:
    side = certificate.outer_side
    point_weights: defaultdict[tuple[Fraction, Fraction], Fraction] = defaultdict(Fraction)
    for atom in certificate.atoms:
        _require(0 <= atom.x <= side and 0 <= atom.y <= side, "site outside container")
        point_weights[atom.x, atom.y] += atom.weight
    for point, weight in tuple(point_weights.items()):
        _require(
            all(
                point_weights.get(image, Fraction(0)) == weight
                for image in d4_images(*point, side)
            ),
            "point charges are not D4 invariant",
        )
    feature_weights: defaultdict[
        tuple[tuple[tuple[Fraction, Fraction, int], ...], int], Fraction
    ] = defaultdict(Fraction)
    for atom in certificate.threshold_atoms:
        _require(
            all(0 <= x <= side and 0 <= y <= side for x, y in atom.points),
            "threshold site outside container",
        )
        feature_weights[atom.key] += atom.weight
    for atom in certificate.threshold_atoms:
        weight = feature_weights[atom.key]
        _require(
            all(
                feature_weights.get(image.key, Fraction(0)) == weight
                for image in atom.images(side)
            ),
            "threshold charges are not D4 invariant",
        )


def validate_parent_core(certificate: ParentCoreCertificate) -> ParentCorePremises:
    """Discharge every premise except the universal centre-coverage decision."""
    _require(type(certificate.n) is int and certificate.n > 0, "n must be positive")
    side, parent = certificate.outer_side, certificate.parent_side
    _require(0 < parent < side, "invalid container or parent side")
    _require(certificate.minimum_charge > 0, "minimum charge must be positive")
    for atom in certificate.atoms:
        for field in ("x", "y", "weight"):
            _rational(getattr(atom, field), f"point {field}")
    for atom in certificate.threshold_atoms:
        _rational(atom.weight, "threshold weight")
        for x, y in atom.points:
            _rational(x, "threshold x")
            _rational(y, "threshold y")
    require_nonnegative_atom_weights(certificate.atoms)
    _validate_symmetry(certificate)
    budget = certificate.budget
    _require(budget < certificate.n * certificate.minimum_charge, "no strict counting gap")
    _require(bool(certificate.rows), "empty parent-angle catalogue")
    cursor = Fraction(0)
    margins: list[Fraction] = []
    for index, row in enumerate(certificate.rows):
        _require(
            row.left == cursor and 0 <= row.left < row.right < 1,
            f"row {index}: noncontiguous parent-angle partition",
        )
        _require(
            0 <= row.half_tangent < 1, f"row {index}: core direction outside first quadrant"
        )
        _require(0 < row.core_side < parent, f"row {index}: invalid core side")
        cosine, sine = row.rotation
        for horizontal, vertical in product((-1, 1), repeat=2):
            # The maximum absolute projection onto either parent axis ranges over
            # these same four vertices by the core's quarter-turn symmetry.
            dot = horizontal * cosine - vertical * sine
            cross = horizontal * sine + vertical * cosine
            margin = _quadratic_minimum(
                parent - row.core_side * dot,
                -2 * row.core_side * cross,
                parent + row.core_side * dot,
                row.left,
                row.right,
            )
            _require(margin > 0, f"row {index}: core reaches a parent boundary")
            margins.append(margin)
        radius = row.centre_margin(parent)
        _require(0 < radius < side / 2, f"row {index}: empty centre domain")
        cursor = row.right
    _require(cursor * cursor + 2 * cursor >= 1, "parent-angle cover does not reach pi/4")
    return ParentCorePremises(budget, min(margins), cursor, len(certificate.rows))


def _exact(value: object, field: str) -> Fraction:
    if (
        type(value) is not str
        or len(value) > 256
        or re.fullmatch(r"-?[0-9]+(?:/[1-9][0-9]*)?", value) is None
    ):
        raise ValueError(f"{field} must be an exact rational string")
    return Fraction(value)


def _integer(value: object, field: str, *, positive: bool = False) -> int:
    if type(value) is not int or value < int(positive):
        raise ValueError(
            f"{field} must be a {'positive' if positive else 'nonnegative'} integer"
        )
    return value


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        _require(key not in result, f"duplicate JSON key {key}")
        result[key] = value
    return result


def _source_sites(
    raw: dict[str, Any], side: Fraction, denominator: int, weight_denominator: int
) -> tuple[list[tuple[Fraction, Fraction]], tuple[Atom, ...]]:
    sites: list[tuple[Fraction, Fraction]] = []
    atoms: list[Atom] = []
    scaled_side = side * denominator
    _require(scaled_side.denominator == 1, "container is not integral on the coordinate scale")
    _require(isinstance(raw["point_orbits"], list), "point_orbits must be an array")
    for index, row in enumerate(raw["point_orbits"]):
        _require(isinstance(row, list) and len(row) == 3, "point orbit must be [x,y,w]")
        x, y, weight = (_integer(value, f"point orbit {index}") for value in row)
        _require(x <= scaled_side and y <= scaled_side, "source site outside container")
        orbit = sorted(set(d4_images(Fraction(x, denominator), Fraction(y, denominator), side)))
        sites.extend(orbit)
        if weight:
            atoms.extend(
                Atom(f"{index}:{member}", px, py, Fraction(weight, weight_denominator))
                for member, (px, py) in enumerate(orbit)
            )
    _require(len(sites) == len(set(sites)), "duplicate physical source sites")
    return sites, tuple(atoms)


def _source_features(
    raw: dict[str, Any], sites: list[tuple[Fraction, Fraction]], denominator: int
) -> tuple[ThresholdAtom, ...]:
    _require("threshold_orbits" not in raw, "ambiguous charge schema")
    _require(isinstance(raw["charge_orbits"], list), "charge_orbits must be an array")
    result: list[ThresholdAtom] = []
    for feature in raw["charge_orbits"]:
        _require(isinstance(feature, dict), "charge orbit must be an object")
        threshold = _integer(feature["threshold"], "threshold", positive=True)
        weight = _integer(feature["weight"], "feature weight")
        members = feature["sets"]
        _require(isinstance(members, list) and bool(members), "empty charge orbit")
        seen: set[tuple[int, ...]] = set()
        for member in members:
            _require(isinstance(member, list) and bool(member), "empty feature")
            _require(
                all(type(i) is int and 0 <= i < len(sites) for i in member),
                "invalid site index",
            )
            key = tuple(sorted(member))
            _require(len(key) == len(set(key)) and key not in seen, "repeated feature or site")
            seen.add(key)
            atom = ThresholdAtom(
                tuple(sites[i] for i in member), threshold, Fraction(weight, denominator)
            )
            if weight:
                result.append(atom)
    return tuple(result)


def load_kleddamag_parent_core(
    path: Path, *, expected_sha256: str | None = None
) -> ParentCoreCertificate:
    """Read exact n11 source data into native charges without importing source code.

    Zero-weight point records remain available to index every feature. D4 expansion
    is sorted in physical coordinates, preserving the source's member indices.
    The native premise validator separately proves symmetry of the weighted result.
    """
    with path.open("rb") as stream:
        data = stream.read(16 * 1024 * 1024 + 1)
    _require(len(data) <= 16 * 1024 * 1024, "source certificate exceeds 16 MiB")
    if expected_sha256 is not None:
        _require(
            hashlib.sha256(data).hexdigest() == expected_sha256,
            "certificate bytes differ from the reviewed n11 release",
        )
    raw = json.loads(data, object_pairs_hook=_unique_object)
    _require(isinstance(raw, dict), "certificate must be a JSON object")
    side = _exact(raw["L"], "L")
    _require(side == Fraction(191, 50), "not the n11 source container")
    parent = _exact(raw["A"], "A")
    coordinates = _integer(
        raw["coordinate_denominator"], "coordinate denominator", positive=True
    )
    weights = _integer(raw["weight_denominator"], "weight denominator", positive=True)
    sites, atoms = _source_sites(raw, side, coordinates, weights)
    features = _source_features(raw, sites, weights)
    _require(isinstance(raw["entries"], list), "entries must be an array")
    rows: list[ParentCoreRow] = []
    for index, row in enumerate(raw["entries"]):
        _require(isinstance(row, list) and len(row) == 4, "parent row must have four values")
        rows.append(ParentCoreRow(*(_exact(value, f"row {index}") for value in row)))
    certificate = ParentCoreCertificate(
        11,
        side,
        parent,
        Fraction(_integer(raw["minimum_units"], "minimum units", positive=True), weights),
        atoms,
        features,
        tuple(rows),
    )
    declared = Fraction(_integer(raw["budget_units"], "budget units"), weights)
    _require(certificate.budget == declared, "incorrect declared counting budget")
    return certificate
