"""Exact, target-blind primitives for threshold-certificate compression.

The compression route starts from a fully expanded :class:`ThresholdCertificate`, but
its independent choices are complete D4 orbits.  This module turns the expanded source
into a canonical orbit inventory, compares inventories without losing exact weight
ratios, and expands an explicitly selected synthetic family back into an ordinary
certificate.  It does not optimize weights or decide coverage.

An inventory is deliberately strict.  Every geometric image must occur exactly once and
all images in an orbit must carry one weight.  A nearly symmetric source is not silently
completed, since doing so would change the certificate whose support is being measured.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from sqpack.fractional.certificate import d4_images
from sqpack.fractional.model import Atom
from sqpack.fractional.threshold import ThresholdAtom, ThresholdCertificate

type Point = tuple[Fraction, Fraction]
type ThresholdKey = tuple[tuple[tuple[Fraction, Fraction, int], ...], int]
type SupportKey = tuple[str, Point | ThresholdKey]


@dataclass(frozen=True, slots=True)
class PointOrbit:
    """One complete point-atom orbit in canonical D4 order."""

    representative: Point
    members: tuple[Point, ...]
    weight: Fraction

    @property
    def orbit_size(self) -> int:
        return len(self.members)

    @property
    def budget_coefficient(self) -> int:
        """The number multiplying this orbit's weight in the point budget."""

        return self.orbit_size


@dataclass(frozen=True, slots=True)
class ThresholdOrbit:
    """One complete threshold-atom orbit, including token multiplicities."""

    representative: ThresholdKey
    members: tuple[ThresholdKey, ...]
    weight: Fraction

    @property
    def orbit_size(self) -> int:
        return len(self.members)

    @property
    def threshold(self) -> int:
        return self.representative[1]

    @property
    def token_count(self) -> int:
        return sum(count for _, _, count in self.representative[0])

    @property
    def site_count(self) -> int:
        return len(self.representative[0])

    @property
    def budget_coefficient(self) -> int:
        """The exact coefficient of this orbit's weight in Condition 2'."""

        return self.orbit_size * (self.token_count // self.threshold)


@dataclass(frozen=True, slots=True)
class OrbitInventory:
    """A canonical, fully checked orbit view of one threshold certificate."""

    n: int
    outer_side: Fraction
    square_side: Fraction
    half_tangents: tuple[Fraction, ...]
    symmetry: str
    point_orbits: tuple[PointOrbit, ...]
    threshold_orbits: tuple[ThresholdOrbit, ...]

    @property
    def point_orbit_count(self) -> int:
        return len(self.point_orbits)

    @property
    def threshold_orbit_count(self) -> int:
        return len(self.threshold_orbits)

    @property
    def orbit_count(self) -> int:
        return self.point_orbit_count + self.threshold_orbit_count

    @property
    def point_atom_count(self) -> int:
        return sum(orbit.orbit_size for orbit in self.point_orbits)

    @property
    def threshold_atom_count(self) -> int:
        return sum(orbit.orbit_size for orbit in self.threshold_orbits)

    @property
    def atom_count(self) -> int:
        return self.point_atom_count + self.threshold_atom_count

    @property
    def total_budget(self) -> Fraction:
        return sum(
            (orbit.weight * orbit.budget_coefficient for orbit in self.point_orbits),
            start=Fraction(0),
        ) + sum(
            (orbit.weight * orbit.budget_coefficient for orbit in self.threshold_orbits),
            start=Fraction(0),
        )


@dataclass(frozen=True, slots=True)
class SupportRelation:
    """Exact support and weight-scaling relation from a reference to a candidate."""

    point_support_equal: bool
    threshold_support_equal: bool
    common_weight_scale: Fraction | None

    @property
    def support_equal(self) -> bool:
        return self.point_support_equal and self.threshold_support_equal

    @property
    def weights_have_common_scale(self) -> bool:
        return self.support_equal and self.common_weight_scale is not None

    @property
    def matches(self) -> bool:
        return self.weights_have_common_scale


@dataclass(frozen=True, slots=True)
class CompressionPolicy:
    """Predeclared support-compression rule; coverage remains a separate gate."""

    max_orbits: int = 23
    minimum_compression_factor: Fraction = Fraction(5)

    def __post_init__(self) -> None:
        if (
            not isinstance(self.max_orbits, int)
            or isinstance(self.max_orbits, bool)
            or self.max_orbits < 1
        ):
            raise ValueError("max_orbits must be a positive integer")
        if not isinstance(self.minimum_compression_factor, Fraction):
            raise TypeError("minimum_compression_factor must be an exact Fraction")
        if self.minimum_compression_factor <= 0:
            raise ValueError("minimum_compression_factor must be positive")


@dataclass(frozen=True, slots=True)
class ThresholdNetSpec:
    """The exact uniform half-tangent net accepted by the existing certificate loader."""

    direction_steps: int = 180
    angle_limit: Fraction = Fraction(207107, 500000)

    def __post_init__(self) -> None:
        if (
            not isinstance(self.direction_steps, int)
            or isinstance(self.direction_steps, bool)
            or self.direction_steps < 1
        ):
            raise ValueError("direction_steps must be a positive integer")
        if not isinstance(self.angle_limit, Fraction):
            raise TypeError("angle_limit must be an exact Fraction")
        if self.angle_limit <= 0:
            raise ValueError("angle_limit must be positive")

    @property
    def half_tangents(self) -> tuple[Fraction, ...]:
        return tuple(
            self.angle_limit * index / self.direction_steps
            for index in range(self.direction_steps + 1)
        )


_DEFAULT_POLICY = CompressionPolicy()
_T025_NET = ThresholdNetSpec()


@dataclass(frozen=True, slots=True)
class PointOrbitSelection:
    """A source point-orbit key and its proposed positive weight."""

    representative: Point
    weight: Fraction

    def __post_init__(self) -> None:
        _require_point(self.representative, "selected point representative")
        if not isinstance(self.weight, Fraction):
            raise TypeError("a selected point-orbit weight must be an exact Fraction")
        if self.weight <= 0:
            raise ValueError("a selected point orbit must have positive weight")


@dataclass(frozen=True, slots=True)
class ThresholdOrbitSelection:
    """A source threshold-orbit key and its proposed positive weight."""

    representative: ThresholdKey
    weight: Fraction

    def __post_init__(self) -> None:
        _require_threshold_key(self.representative, "selected threshold representative")
        if not isinstance(self.weight, Fraction):
            raise TypeError("a selected threshold-orbit weight must be an exact Fraction")
        if self.weight <= 0:
            raise ValueError("a selected threshold orbit must have positive weight")


@dataclass(frozen=True, slots=True)
class CompressionMetrics:
    """Exact structural metrics for one source-bound proposed selection."""

    baseline_orbits: int
    point_orbits: int
    threshold_orbits: int
    selected_orbits: int
    expanded_atoms: int
    coordinate_parameters: int
    distinct_weights: int
    threshold_templates: int
    total_budget: Fraction
    budget_below_n: bool
    compression_factor: Fraction
    within_orbit_ceiling: bool
    meets_compression_factor: bool

    @property
    def satisfies_policy(self) -> bool:
        return self.within_orbit_ceiling and self.meets_compression_factor


def _require_fraction(value: object, label: str) -> None:
    if not isinstance(value, Fraction):
        raise TypeError(f"{label} must be an exact Fraction")


def _require_point(value: object, label: str) -> None:
    if not isinstance(value, tuple) or len(value) != 2:
        raise TypeError(f"{label} must be an exact coordinate pair")
    _require_fraction(value[0], f"{label} x")
    _require_fraction(value[1], f"{label} y")


def _require_threshold_key(value: object, label: str) -> None:
    if not isinstance(value, tuple) or len(value) != 2:
        raise TypeError(f"{label} must be an exact threshold key")
    sites, threshold = value
    if not isinstance(sites, tuple) or not sites:
        raise TypeError(f"{label} sites must be a nonempty tuple")
    if not isinstance(threshold, int) or isinstance(threshold, bool):
        raise TypeError(f"{label} threshold must be an integer")
    for index, site in enumerate(sites):
        if not isinstance(site, tuple) or len(site) != 3:
            raise TypeError(f"{label} site {index} must be an (x, y, count) tuple")
        _require_fraction(site[0], f"{label} site {index} x")
        _require_fraction(site[1], f"{label} site {index} y")
        if not isinstance(site[2], int) or isinstance(site[2], bool):
            raise TypeError(f"{label} site {index} count must be an integer")


def _point_images(point: Point, outer_side: Fraction) -> tuple[Point, ...]:
    return tuple(sorted(set(d4_images(point[0], point[1], outer_side))))


def _threshold_from_key(key: ThresholdKey, weight: Fraction) -> ThresholdAtom:
    sites, threshold = key
    return ThresholdAtom(
        tuple((x, y) for x, y, _ in sites),
        threshold,
        weight,
        tuple(count for _, _, count in sites),
    )


def _threshold_images(key: ThresholdKey, outer_side: Fraction) -> tuple[ThresholdKey, ...]:
    atom = _threshold_from_key(key, Fraction(1))
    return tuple(sorted({image.key for image in atom.images(outer_side)}))


def _point_orbits(certificate: ThresholdCertificate) -> tuple[PointOrbit, ...]:
    grouped: dict[Point, list[Atom]] = {}
    for atom in certificate.atoms:
        point = (atom.x, atom.y)
        representative = _point_images(point, certificate.outer_side)[0]
        grouped.setdefault(representative, []).append(atom)

    result: list[PointOrbit] = []
    for representative, atoms in sorted(grouped.items()):
        expected = _point_images(representative, certificate.outer_side)
        actual = tuple(sorted((atom.x, atom.y) for atom in atoms))
        if len(actual) != len(set(actual)):
            raise ValueError(f"point orbit {representative} contains a duplicate image")
        if actual != expected:
            missing = tuple(sorted(set(expected) - set(actual)))
            extra = tuple(sorted(set(actual) - set(expected)))
            raise ValueError(
                f"point orbit {representative} is not D4-complete; "
                f"missing {missing}, extra {extra}"
            )
        weights = {atom.weight for atom in atoms}
        if len(weights) != 1:
            raise ValueError(f"point orbit {representative} does not have one weight")
        result.append(PointOrbit(representative, expected, weights.pop()))
    return tuple(result)


def _threshold_orbits(certificate: ThresholdCertificate) -> tuple[ThresholdOrbit, ...]:
    grouped: dict[ThresholdKey, list[ThresholdAtom]] = {}
    for atom in certificate.threshold_atoms:
        representative = _threshold_images(atom.key, certificate.outer_side)[0]
        grouped.setdefault(representative, []).append(atom)

    result: list[ThresholdOrbit] = []
    for representative, atoms in sorted(grouped.items()):
        expected = _threshold_images(representative, certificate.outer_side)
        actual = tuple(sorted(atom.key for atom in atoms))
        if actual != expected:
            missing = tuple(sorted(set(expected) - set(actual)))
            extra = tuple(sorted(set(actual) - set(expected)))
            raise ValueError(
                f"threshold orbit {representative} is not D4-complete; "
                f"missing {missing}, extra {extra}"
            )
        weights = {atom.weight for atom in atoms}
        if len(weights) != 1:
            raise ValueError(f"threshold orbit {representative} does not have one weight")
        result.append(ThresholdOrbit(representative, expected, weights.pop()))
    return tuple(result)


def inventory_certificate(certificate: ThresholdCertificate) -> OrbitInventory:
    """Build the canonical exact D4 inventory, refusing incomplete source orbits."""

    if certificate.symmetry != "D4":
        raise ValueError(f"compression inventory requires D4, not {certificate.symmetry!r}")
    _require_fraction(certificate.outer_side, "outer_side")
    _require_fraction(certificate.square_side, "square_side")
    for index, tangent in enumerate(certificate.half_tangents):
        _require_fraction(tangent, f"half_tangents[{index}]")
    for index, atom in enumerate(certificate.atoms):
        _require_point((atom.x, atom.y), f"point atom {index}")
        _require_fraction(atom.weight, f"point atom {index} weight")
    for index, atom in enumerate(certificate.threshold_atoms):
        _require_threshold_key(atom.key, f"threshold atom {index}")
        _require_fraction(atom.weight, f"threshold atom {index} weight")
    inventory = OrbitInventory(
        n=certificate.n,
        outer_side=certificate.outer_side,
        square_side=certificate.square_side,
        half_tangents=certificate.half_tangents,
        symmetry=certificate.symmetry,
        point_orbits=_point_orbits(certificate),
        threshold_orbits=_threshold_orbits(certificate),
    )
    if inventory.total_budget != certificate.total_budget:
        raise ValueError(
            "orbit inventory changed the certificate budget: "
            f"{inventory.total_budget} != {certificate.total_budget}"
        )
    return inventory


def ordered_support(inventory: OrbitInventory) -> tuple[SupportKey, ...]:
    """The canonical mixed point/threshold orbit support, with type tags."""

    return (
        *(("point", orbit.representative) for orbit in inventory.point_orbits),
        *(("threshold", orbit.representative) for orbit in inventory.threshold_orbits),
    )


def _common_scale(
    reference: tuple[Fraction, ...], candidate: tuple[Fraction, ...]
) -> Fraction | None:
    scale: Fraction | None = None
    for source_weight, candidate_weight in zip(reference, candidate, strict=True):
        if source_weight == 0:
            if candidate_weight != 0:
                return None
            continue
        ratio = candidate_weight / source_weight
        if ratio <= 0:
            return None
        if scale is None:
            scale = ratio
        elif scale != ratio:
            return None
    return Fraction(1) if scale is None else scale


def compare_scaled_support(
    reference: OrbitInventory, candidate: OrbitInventory
) -> SupportRelation:
    """Compare exact orbit support and a candidate/reference common weight scale.

    Metadata such as shrink and direction-net density is intentionally outside this
    relation.  T-026 is a provenance sentinel precisely because it retains T-025's
    support and rescales every weight while changing those verification parameters.
    """

    reference_points = tuple(orbit.representative for orbit in reference.point_orbits)
    candidate_points = tuple(orbit.representative for orbit in candidate.point_orbits)
    reference_thresholds = tuple(orbit.representative for orbit in reference.threshold_orbits)
    candidate_thresholds = tuple(orbit.representative for orbit in candidate.threshold_orbits)
    points_equal = reference_points == candidate_points
    thresholds_equal = reference_thresholds == candidate_thresholds
    if not (points_equal and thresholds_equal):
        return SupportRelation(points_equal, thresholds_equal, None)
    reference_weights = tuple(
        orbit.weight for orbit in (*reference.point_orbits, *reference.threshold_orbits)
    )
    candidate_weights = tuple(
        orbit.weight for orbit in (*candidate.point_orbits, *candidate.threshold_orbits)
    )
    return SupportRelation(
        points_equal,
        thresholds_equal,
        _common_scale(reference_weights, candidate_weights),
    )


def quantize_upward(weight: Fraction, denominator: int) -> Fraction:
    """Round a nonnegative exact weight up to the nearest multiple of ``1/denominator``."""

    if not isinstance(denominator, int) or isinstance(denominator, bool) or denominator < 1:
        raise ValueError("the quantization denominator must be a positive integer")
    if not isinstance(weight, Fraction):
        raise TypeError("upward certificate quantization requires an exact Fraction")
    if weight < 0:
        raise ValueError("upward certificate quantization requires a nonnegative weight")
    scaled = weight * denominator
    numerator = (scaled.numerator + scaled.denominator - 1) // scaled.denominator
    return Fraction(numerator, denominator)


def quantized_inventory_budget(inventory: OrbitInventory, denominator: int) -> Fraction:
    """The exact Condition 2' budget after orbitwise upward weight quantization."""

    return sum(
        (
            quantize_upward(orbit.weight, denominator) * orbit.budget_coefficient
            for orbit in inventory.point_orbits
        ),
        start=Fraction(0),
    ) + sum(
        (
            quantize_upward(orbit.weight, denominator) * orbit.budget_coefficient
            for orbit in inventory.threshold_orbits
        ),
        start=Fraction(0),
    )


def _point_record(point: Point) -> list[str]:
    return [str(point[0]), str(point[1])]


def _threshold_key_record(key: ThresholdKey) -> dict[str, Any]:
    sites, threshold = key
    return {
        "weighted_points": [[str(x), str(y), count] for x, y, count in sites],
        "threshold": threshold,
    }


def canonical_catalog_record(inventory: OrbitInventory) -> dict[str, Any]:
    """A JSON-ready canonical record of exact source support, weights, and metadata."""

    return {
        "schema": "packing.squares:ThresholdOrbitCatalog/v1",
        "certificate": {
            "n": inventory.n,
            "outer_side": str(inventory.outer_side),
            "square_side": str(inventory.square_side),
            "half_tangents": [str(value) for value in inventory.half_tangents],
            "symmetry": inventory.symmetry,
            "total_budget": str(inventory.total_budget),
        },
        "counts": {
            "point_orbits": inventory.point_orbit_count,
            "threshold_orbits": inventory.threshold_orbit_count,
            "orbits": inventory.orbit_count,
            "point_atoms": inventory.point_atom_count,
            "threshold_atoms": inventory.threshold_atom_count,
            "atoms": inventory.atom_count,
        },
        "point_orbits": [
            {
                "representative": _point_record(orbit.representative),
                "members": [_point_record(point) for point in orbit.members],
                "weight": str(orbit.weight),
                "budget_coefficient": orbit.budget_coefficient,
            }
            for orbit in inventory.point_orbits
        ],
        "threshold_orbits": [
            {
                "representative": _threshold_key_record(orbit.representative),
                "members": [_threshold_key_record(key) for key in orbit.members],
                "weight": str(orbit.weight),
                "budget_coefficient": orbit.budget_coefficient,
            }
            for orbit in inventory.threshold_orbits
        ],
    }


def catalog_sha256(inventory: OrbitInventory) -> str:
    """SHA-256 of the canonical compact UTF-8 catalog serialization."""

    encoded = json.dumps(
        canonical_catalog_record(inventory),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def _selected_orbits(
    inventory: OrbitInventory,
    point_selections: tuple[PointOrbitSelection, ...],
    threshold_selections: tuple[ThresholdOrbitSelection, ...],
) -> tuple[
    tuple[tuple[PointOrbit, PointOrbitSelection], ...],
    tuple[tuple[ThresholdOrbit, ThresholdOrbitSelection], ...],
]:
    point_by_key = {orbit.representative: orbit for orbit in inventory.point_orbits}
    threshold_by_key = {orbit.representative: orbit for orbit in inventory.threshold_orbits}
    if len({selection.representative for selection in point_selections}) != len(
        point_selections
    ):
        raise ValueError("a point orbit is selected more than once")
    if len({selection.representative for selection in threshold_selections}) != len(
        threshold_selections
    ):
        raise ValueError("a threshold orbit is selected more than once")
    try:
        points = tuple(
            (point_by_key[selection.representative], selection)
            for selection in point_selections
        )
    except KeyError as error:
        raise ValueError(
            f"selected point orbit is outside the source catalog: {error.args[0]}"
        ) from None
    try:
        thresholds = tuple(
            (threshold_by_key[selection.representative], selection)
            for selection in threshold_selections
        )
    except KeyError as error:
        raise ValueError(
            f"selected threshold orbit is outside the source catalog: {error.args[0]}"
        ) from None
    return (
        tuple(sorted(points, key=lambda pair: pair[0].representative)),
        tuple(sorted(thresholds, key=lambda pair: pair[0].representative)),
    )


def measure_selection(
    inventory: OrbitInventory,
    point_selections: tuple[PointOrbitSelection, ...],
    threshold_selections: tuple[ThresholdOrbitSelection, ...],
    policy: CompressionPolicy = _DEFAULT_POLICY,
) -> CompressionMetrics:
    """Measure one source-bound selection; this neither optimizes nor checks coverage."""

    points, thresholds = _selected_orbits(inventory, point_selections, threshold_selections)
    selected_count = len(points) + len(thresholds)
    if selected_count == 0:
        raise ValueError("a compression selection must contain at least one orbit")
    coordinate_parameters = 2 * len(points) + 2 * sum(
        orbit.site_count for orbit, _ in thresholds
    )
    weights = {selection.weight for _, selection in (*points, *thresholds)}
    templates = {
        (
            orbit.site_count,
            orbit.token_count,
            orbit.threshold,
            tuple(sorted(count for _, _, count in orbit.representative[0])),
        )
        for orbit, _ in thresholds
    }
    total_budget = sum(
        (
            selection.weight * orbit.budget_coefficient
            for orbit, selection in (*points, *thresholds)
        ),
        start=Fraction(0),
    )
    compression_factor = Fraction(inventory.orbit_count, selected_count)
    return CompressionMetrics(
        baseline_orbits=inventory.orbit_count,
        point_orbits=len(points),
        threshold_orbits=len(thresholds),
        selected_orbits=selected_count,
        expanded_atoms=sum(orbit.orbit_size for orbit, _ in (*points, *thresholds)),
        coordinate_parameters=coordinate_parameters,
        distinct_weights=len(weights),
        threshold_templates=len(templates),
        total_budget=total_budget,
        budget_below_n=total_budget < inventory.n,
        compression_factor=compression_factor,
        within_orbit_ceiling=selected_count <= policy.max_orbits,
        meets_compression_factor=compression_factor >= policy.minimum_compression_factor,
    )


def decompress_selection(
    inventory: OrbitInventory,
    point_selections: tuple[PointOrbitSelection, ...],
    threshold_selections: tuple[ThresholdOrbitSelection, ...],
    policy: CompressionPolicy = _DEFAULT_POLICY,
) -> ThresholdCertificate:
    """Expand an admitted synthetic selection to a conventional certificate object.

    The output is synthetic: point labels are generated from canonical orbit order, and
    no source label or unselected weight is copied.  The function only reconstructs the
    declared D4 family; the ordinary exact verifier remains responsible for coverage.
    """

    metrics = measure_selection(inventory, point_selections, threshold_selections, policy)
    if not metrics.satisfies_policy:
        raise ValueError(
            f"selection has {metrics.selected_orbits} orbits at compression factor "
            f"{metrics.compression_factor}; policy requires at most {policy.max_orbits} "
            f"and factor at least {policy.minimum_compression_factor}"
        )
    points, thresholds = _selected_orbits(inventory, point_selections, threshold_selections)
    atoms = tuple(
        Atom(f"compression:p{orbit_index}:g{image_index}", x, y, selection.weight)
        for orbit_index, (orbit, selection) in enumerate(points)
        for image_index, (x, y) in enumerate(orbit.members)
    )
    threshold_atoms = tuple(
        _threshold_from_key(key, selection.weight)
        for orbit, selection in thresholds
        for key in orbit.members
    )
    return ThresholdCertificate(
        n=inventory.n,
        outer_side=inventory.outer_side,
        square_side=inventory.square_side,
        atoms=atoms,
        threshold_atoms=threshold_atoms,
        half_tangents=inventory.half_tangents,
        symmetry=inventory.symmetry,
    )


def threshold_certificate_record(
    certificate: ThresholdCertificate,
    net: ThresholdNetSpec = _T025_NET,
) -> dict[str, Any]:
    """Return the deterministic ordinary record consumed by the existing exact loader.

    The loader's certificate variant represents only all-ones threshold atoms.  Weighted
    site multiplicities are therefore refused rather than flattened into a different
    threshold.  Inventory construction also proves that the emitted ordering consists of
    complete, equal-weight D4 orbits.
    """

    if certificate.half_tangents != net.half_tangents:
        raise ValueError(
            "certificate direction net does not equal the declared uniform net "
            f"({net.direction_steps} steps, angle limit {net.angle_limit})"
        )
    inventory = inventory_certificate(certificate)
    for orbit in inventory.threshold_orbits:
        if any(count != 1 for _, _, count in orbit.representative[0]):
            raise ValueError(
                "the existing threshold-certificate loader accepts only ordinary "
                "all-ones threshold atoms"
            )
    return {
        "variant": "threshold",
        "n": inventory.n,
        "outer_side": str(inventory.outer_side),
        "square_side": str(inventory.square_side),
        "direction_steps": net.direction_steps,
        "angle_limit": str(net.angle_limit),
        "symmetry": inventory.symmetry,
        "total_budget": str(inventory.total_budget),
        "atoms": [
            [str(x), str(y), str(orbit.weight)]
            for orbit in inventory.point_orbits
            for x, y in orbit.members
        ],
        "threshold_atoms": [
            {
                "points": [[str(x), str(y)] for x, y, _ in key[0]],
                "threshold": key[1],
                "weight": str(orbit.weight),
            }
            for orbit in inventory.threshold_orbits
            for key in orbit.members
        ],
    }


def serialize_threshold_certificate(
    certificate: ThresholdCertificate,
    net: ThresholdNetSpec = _T025_NET,
) -> bytes:
    """Serialize a synthetic certificate deterministically for the existing loader."""

    record = threshold_certificate_record(certificate, net)
    return (json.dumps(record, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
