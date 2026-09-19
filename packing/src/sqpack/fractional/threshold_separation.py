"""2-of-3 threshold-atom separation against an exact placement family.

Agenda-034's separation core lived as a ``.py.txt`` scratch driver. This module is the
in-tree lift: overlap geometry in ``Fraction`` arithmetic, a float screen only where it
cannot decide, and atom-orbit columns whose cost is ``|orbit| * floor(|S|/k)``.

It does not run a covering LP, does not freeze a certificate, and does not import the
scratch files.
"""

from __future__ import annotations

import logging
import math
import time
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction

import numpy as np
from scipy import sparse

from sqpack.fractional.ceiling import (
    CeilingCertificate,
    Placement,
    arrangement_lines,
    exact_intersection,
    float_family,
    loose_membership,
)
from sqpack.fractional.cutting import (
    COVER_SLACK,
    ExactRow,
    float_vertices,
    support_entries,
    symmetric_placements,
    tidy_family,
)
from sqpack.fractional.generate import direction_net
from sqpack.fractional.threshold import ThresholdAtom

logger = logging.getLogger(__name__)

type Point = tuple[Fraction, Fraction]
type HalfPlane = tuple[Fraction, Fraction, Fraction]

#: Float membership margin used only to screen; ambiguous pairs are decided by
#: ``Placement.contains``.
CONTAINMENT_MARGIN = 1e-9
_WEIGHT_DENOMINATOR = 10**9
_VERTEX_CHUNK = 2_000_000
_CHARGE_STEP = 20_000
_FOLD_AXIS_DEG = 2.5
_FOLD_29_LOW = 25.0
_FOLD_29_HIGH = 35.0


@dataclass(frozen=True, slots=True)
class TwoOfThreeViolation:
    """One D4-orbit representative of a 2-of-3 atom whose exact charge exceeds 1."""

    points: tuple[Point, Point, Point]
    charge: Fraction
    triangle: tuple[int, int, int]
    classes: tuple[str, str, str]
    angles: tuple[float, float, float]
    threshold: int = 2
    budget: Fraction = Fraction(1)

    def atom(self) -> ThresholdAtom:
        return ThresholdAtom(self.points, self.threshold, Fraction(1))


def clip_polygon(polygon: list[Point], a: Fraction, b: Fraction, c: Fraction) -> list[Point]:
    """Keep the part of the convex polygon with ``a x + b y <= c``."""

    if not polygon:
        return []
    clipped: list[Point] = []
    count = len(polygon)
    for index in range(count):
        start = polygon[index]
        end = polygon[(index + 1) % count]
        start_value = a * start[0] + b * start[1] - c
        end_value = a * end[0] + b * end[1] - c
        if start_value <= 0:
            clipped.append(start)
        if (start_value < 0 < end_value) or (end_value < 0 < start_value):
            parameter = start_value / (start_value - end_value)
            clipped.append(
                (
                    start[0] + parameter * (end[0] - start[0]),
                    start[1] + parameter * (end[1] - start[1]),
                )
            )
    return clipped


def half_planes(placement: Placement) -> tuple[HalfPlane, HalfPlane, HalfPlane, HalfPlane]:
    ax, ay, u, bx, by, v = placement.slabs()
    half = placement.side / 2
    return (
        (ax, ay, u + half),
        (-ax, -ay, half - u),
        (bx, by, v + half),
        (-bx, -by, half - v),
    )


def intersect_placement(polygon: list[Point], placement: Placement) -> list[Point]:
    clipped = polygon
    for a, b, c in half_planes(placement):
        clipped = clip_polygon(clipped, a, b, c)
        if not clipped:
            return []
    return clipped


def overlap_exact(
    first: Placement,
    second: Placement,
    first_corners: Sequence[Point],
    second_corners: Sequence[Point],
) -> bool:
    """Closed squares meet iff no edge normal of either separates the other corner set."""

    for square, other in ((first, second_corners), (second, first_corners)):
        ax, ay, u, bx, by, v = square.slabs()
        half = square.side / 2
        for nx, ny, offset in ((ax, ay, u), (bx, by, v)):
            values = [nx * x + ny * y for x, y in other]
            if max(values) < offset - half or min(values) > offset + half:
                return False
    return True


def fold_deg(half_tangent: Fraction) -> float:
    angle = math.degrees(2 * math.atan(float(half_tangent)))
    return angle if angle <= 45 else 90 - angle


def angle_class(angle: float) -> str:
    if angle <= _FOLD_AXIS_DEG:
        return "axis"
    if _FOLD_29_LOW <= angle <= _FOLD_29_HIGH:
        return "29"
    return "other"


def merge_identical_placements(placements: tuple[Placement, ...]) -> tuple[Placement, ...]:
    """Sum weights of geometrically identical squares.

    D4 expansion keeps repeated images of a placement on a mirror; two identical squares
    would otherwise give two edges the same representative point.
    """

    merged: dict[tuple[Fraction, Fraction, Fraction, Fraction], Placement] = {}
    for placement in placements:
        key = (
            placement.half_tangent,
            placement.centre_x,
            placement.centre_y,
            placement.side,
        )
        existing = merged.get(key)
        if existing is None:
            merged[key] = placement
            continue
        merged[key] = Placement(
            placement.half_tangent,
            placement.centre_x,
            placement.centre_y,
            existing.weight + placement.weight,
            placement.side,
        )
    return tuple(merged.values())


def family_from_dual(
    exact_rows: list[ExactRow],
    duals: np.ndarray,
    *,
    half_tangents: tuple[Fraction, ...],
    outer_side: Fraction,
    square_side: Fraction,
    n: int,
    weight_denominator: int = _WEIGHT_DENOMINATOR,
) -> CeilingCertificate | None:
    """The LP dual as an exact D4-symmetric family, or ``None`` when the dual is empty."""

    entries = support_entries(
        exact_rows,
        duals,
        half_tangents,
        support_cap=len(exact_rows),
        weight_denominator=weight_denominator,
    )
    if not entries:
        return None
    return CeilingCertificate(
        n,
        outer_side,
        square_side,
        half_tangents,
        symmetric_placements(entries, outer_side, square_side),
    )


def containment(
    points: Sequence[Point],
    placements: Sequence[Placement],
    normals: np.ndarray,
    offsets: np.ndarray,
    halves: np.ndarray,
) -> tuple[np.ndarray, int]:
    """Exact containment matrix ``[points x placements]``: floats screen, Fractions decide."""

    if not points:
        return np.zeros((0, len(placements)), dtype=bool), 0
    coords = np.array([[float(x), float(y)] for x, y in points])
    first = np.abs(coords @ normals[:, 0, :].T - offsets[None, :, 0])
    second = np.abs(coords @ normals[:, 1, :].T - offsets[None, :, 1])
    loose = (first <= halves[None, :] + CONTAINMENT_MARGIN) & (
        second <= halves[None, :] + CONTAINMENT_MARGIN
    )
    strict = (first <= halves[None, :] - CONTAINMENT_MARGIN) & (
        second <= halves[None, :] - CONTAINMENT_MARGIN
    )
    result = strict.copy()
    ambiguous = np.argwhere(loose & ~strict)
    for point_index, placement_index in ambiguous:
        point = points[int(point_index)]
        member = placements[int(placement_index)]
        result[int(point_index), int(placement_index)] = member.contains(point[0], point[1])
    return result, len(ambiguous)


def _centroid(polygon: Sequence[Point]) -> Point | None:
    if not polygon:
        return None
    count = len(polygon)
    return (
        sum((point[0] for point in polygon), start=Fraction(0)) / count,
        sum((point[1] for point in polygon), start=Fraction(0)) / count,
    )


def _overlap_edges(
    placements: Sequence[Placement], corners: Sequence[tuple[Point, ...]]
) -> list[tuple[int, int]]:
    count = len(placements)
    if count < 2:
        return []
    centres_x = np.array([float(placement.centre_x) for placement in placements])
    centres_y = np.array([float(placement.centre_y) for placement in placements])
    side = max(float(placement.side) for placement in placements)
    distance_sq = (centres_x[:, None] - centres_x[None, :]) ** 2 + (
        centres_y[:, None] - centres_y[None, :]
    ) ** 2
    reach = (side * math.sqrt(2) + 1e-6) ** 2
    candidates = np.argwhere(np.triu(distance_sq <= reach, 1))
    return [
        (int(i), int(j))
        for i, j in candidates
        if overlap_exact(
            placements[int(i)],
            placements[int(j)],
            corners[int(i)],
            corners[int(j)],
        )
    ]


class FamilyGeometry:
    """Overlap graph, pairwise representatives, and 2-of-3 charges for one family."""

    def __init__(self, family: CeilingCertificate) -> None:
        started = time.perf_counter()
        merged = CeilingCertificate(
            family.n,
            family.outer_side,
            family.square_side,
            family.half_tangents,
            merge_identical_placements(family.placements),
        )
        self.family = tidy_family(merged, _WEIGHT_DENOMINATOR)
        self.placements = self.family.placements
        self.placement_count = len(self.placements)
        self.weights_float = np.array(
            [float(placement.weight) for placement in self.placements], dtype=float
        )
        self.weights = [placement.weight for placement in self.placements]
        self.corners = [placement.corners() for placement in self.placements]
        self.angles = [fold_deg(placement.half_tangent) for placement in self.placements]
        self.classes = [angle_class(angle) for angle in self.angles]
        self.edges = _overlap_edges(self.placements, self.corners)
        self.adjacent = [set() for _ in range(self.placement_count)]
        for i, j in self.edges:
            self.adjacent[i].add(j)
            self.adjacent[j].add(i)
        self.edge_index = {edge: index for index, edge in enumerate(self.edges)}
        self.representatives: list[Point] = []
        for i, j in self.edges:
            polygon = intersect_placement(list(self.corners[i]), self.placements[j])
            centroid = _centroid(polygon)
            if centroid is None:
                raise RuntimeError(
                    f"placements {i} and {j} overlap exactly but the "
                    "intersection polygon is empty"
                )
            self.representatives.append(centroid)
        self.normals, self.offsets, self.halves, _ = float_family(self.family)
        self.edge_containment, ambiguous = containment(
            self.representatives,
            self.placements,
            self.normals,
            self.offsets,
            self.halves,
        )
        self.edge_containment_int = self.edge_containment.astype(np.int8)
        self.vertex_points: list[Point] = []
        self.vertex_containment: np.ndarray | None = None
        self.vertex_containment_int: np.ndarray | None = None
        self.vertex_depth: np.ndarray | None = None
        self._interior_cache: dict[
            tuple[int, int, Fraction], tuple[list[Point], np.ndarray]
        ] = {}
        logger.info(
            "geometry: %s placements, %s edges, mean degree %.1f, "
            "%s containments decided exactly, %.2fs",
            self.placement_count,
            len(self.edges),
            2 * len(self.edges) / max(self.placement_count, 1),
            ambiguous,
            time.perf_counter() - started,
        )

    def triangles(self) -> np.ndarray:
        found = [
            (i, j, k)
            for i, j in self.edges
            for k in self.adjacent[i] & self.adjacent[j]
            if k > j
        ]
        return np.array(found, dtype=np.int64).reshape(-1, 3)

    def charges_2of3(
        self, triangles: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        if triangles.size == 0:
            empty = np.zeros(0, dtype=np.int64)
            return np.zeros(0, dtype=float), empty, empty, empty
        edge_ij = np.array(
            [self.edge_index[(int(i), int(j))] for i, j, _k in triangles], dtype=np.int64
        )
        edge_jk = np.array(
            [self.edge_index[(int(j), int(k))] for _i, j, k in triangles], dtype=np.int64
        )
        edge_ik = np.array(
            [self.edge_index[(int(i), int(k))] for i, _j, k in triangles], dtype=np.int64
        )
        charges = np.zeros(len(triangles), dtype=float)
        for start in range(0, len(triangles), _CHARGE_STEP):
            stop = start + _CHARGE_STEP
            counts = (
                self.edge_containment_int[edge_ij[start:stop]]
                + self.edge_containment_int[edge_jk[start:stop]]
                + self.edge_containment_int[edge_ik[start:stop]]
            )
            charges[start:stop] = (counts >= 2) @ self.weights_float
        return charges, edge_ij, edge_jk, edge_ik

    def exact_charge(self, point_ids: Sequence[int], threshold: int) -> Fraction:
        counts = np.zeros(self.placement_count, dtype=np.int16)
        for edge in point_ids:
            counts = counts + self.edge_containment_int[edge]
        members = np.flatnonzero(counts >= threshold)
        return sum((self.weights[int(index)] for index in members), start=Fraction(0))

    def vertex_candidates(self, *, total_cap: int = 60000) -> None:
        """Arrangement vertices as extra candidate points, deepest first, exact points."""

        started = time.perf_counter()
        lines = arrangement_lines(self.family)
        points, pairs, cache = float_vertices(self.family, lines)
        normals, offsets, halves, weights = float_family(self.family)
        depth = np.zeros(points.shape[0], dtype=float)
        chunk = max(1, _VERTEX_CHUNK // max(1, self.placement_count))
        for start in range(0, points.shape[0], chunk):
            block = points[start : start + chunk]
            depth[start : start + chunk] = (
                loose_membership(block, normals, offsets, halves, margin=2e-6).astype(float)
                @ weights
            )
        order = np.argsort(-depth, kind="stable")[:total_cap]
        side = self.family.outer_side
        exact_points: list[Point] = []
        for index in order:
            exact = cache.get(int(index))
            if exact is None:
                first_line = lines[int(pairs[index, 0])]
                second_line = lines[int(pairs[index, 1])]
                exact = exact_intersection(first_line, second_line)
            if exact is None or not (0 <= exact[0] <= side and 0 <= exact[1] <= side):
                continue
            exact_points.append(exact)
        unique: list[Point] = []
        seen: set[Point] = set()
        for point in exact_points:
            if point in seen:
                continue
            seen.add(point)
            unique.append(point)
        self.vertex_points = unique
        contained, ambiguous = containment(
            unique, self.placements, self.normals, self.offsets, self.halves
        )
        self.vertex_containment = contained
        self.vertex_containment_int = contained.astype(np.int8)
        self.vertex_depth = contained @ self.weights_float
        deepest = float(self.vertex_depth.max()) if unique else 0.0
        logger.info(
            "vertex candidates: %s vertices, kept %s deepest (max depth %.4f), "
            "%s decided exactly, %.2fs",
            points.shape[0],
            len(unique),
            deepest,
            ambiguous,
            time.perf_counter() - started,
        )

    def interior_candidates(
        self, edge: int, *, cap: int, pull: Fraction = Fraction(1, 1000)
    ) -> tuple[list[Point], np.ndarray]:
        """Interior points for one pairwise intersection, plus the pair centroid."""

        key = (edge, cap, pull)
        cached = self._interior_cache.get(key)
        if cached is not None:
            return cached
        if self.vertex_containment is None or self.vertex_depth is None:
            raise RuntimeError("interior_candidates needs vertex_candidates first")
        i, j = self.edges[edge]
        inside = np.flatnonzero(self.vertex_containment[:, i] & self.vertex_containment[:, j])
        if inside.size > cap:
            inside = inside[np.argsort(-self.vertex_depth[inside], kind="stable")[:cap]]
        cx, cy = self.representatives[edge]
        points = [
            (x + pull * (cx - x), y + pull * (cy - y))
            for x, y in (self.vertex_points[int(index)] for index in inside)
        ]
        points.append((cx, cy))
        contained, _ = containment(
            points, self.placements, self.normals, self.offsets, self.halves
        )
        packed = (points, contained.astype(np.int8))
        self._interior_cache[key] = packed
        return packed

    def refine_triangle(
        self, i: int, j: int, k: int, *, cap: int = 24
    ) -> tuple[Fraction, tuple[Point, Point, Point]] | None:
        """Best 2-of-3 atom on triangle ``(i, j, k)`` among interior vertex candidates."""

        edge_ij = self.edge_index[(i, j)]
        edge_jk = self.edge_index[(j, k)]
        edge_ik = self.edge_index[(i, k)]
        points_a, mask_a = self.interior_candidates(edge_ij, cap=cap)
        points_b, mask_b = self.interior_candidates(edge_jk, cap=cap)
        points_c, mask_c = self.interior_candidates(edge_ik, cap=cap)
        counts = mask_a[:, None, None, :] + mask_b[None, :, None, :] + mask_c[None, None, :, :]
        charged = (counts >= 2) @ self.weights_float
        a, b, c = np.unravel_index(int(charged.argmax()), charged.shape)
        points = (points_a[int(a)], points_b[int(b)], points_c[int(c)])
        if len(set(points)) < 3:
            return None
        members = np.flatnonzero(counts[int(a), int(b), int(c)] >= 2)
        exact = sum((self.weights[int(index)] for index in members), start=Fraction(0))
        return exact, points

    def violated_2of3(
        self,
        *,
        outer_side: Fraction,
        min_violation: float = 0.0,
        vertex_cap: int = 0,
        refine_above: float = 0.85,
    ) -> list[TwoOfThreeViolation]:
        """2-of-3 atoms on triangle representatives whose exact charge exceeds 1.

        One representative per D4 orbit, the heaviest. ``vertex_cap > 0`` re-chooses
        points among arrangement vertices inside each pairwise intersection for triangles
        whose centroid charge reaches ``refine_above``.
        """

        started = time.perf_counter()
        triangles = self.triangles()
        charges, edge_ij, edge_jk, edge_ik = self.charges_2of3(triangles)
        if triangles.size == 0:
            logger.info("separation: 0 triangles")
            return []
        order = np.argsort(-charges, kind="stable")
        found: dict[tuple[object, ...], TwoOfThreeViolation] = {}
        checked = 0
        refined = 0
        if vertex_cap > 0 and self.vertex_containment is None:
            self.vertex_candidates()
        exact_floor = 1 + Fraction(min_violation).limit_denominator(_WEIGHT_DENOMINATOR)
        for index in order:
            float_floor = (
                (1 + min_violation - 1e-7)
                if vertex_cap == 0
                else min(refine_above, 1 + min_violation - 1e-7)
            )
            if charges[index] < float_floor:
                break
            checked += 1
            points = (
                self.representatives[int(edge_ij[index])],
                self.representatives[int(edge_jk[index])],
                self.representatives[int(edge_ik[index])],
            )
            if len(set(points)) < 3:
                continue
            exact = self.exact_charge(
                [int(edge_ij[index]), int(edge_jk[index]), int(edge_ik[index])], 2
            )
            i, j, k = (int(value) for value in triangles[index])
            if vertex_cap > 0:
                better = self.refine_triangle(i, j, k, cap=vertex_cap)
                refined += 1
                if better is not None and better[0] > exact:
                    exact, points = better
            if exact <= exact_floor:
                continue
            atom = ThresholdAtom(points, 2, Fraction(1))
            key = min(image.key for image in atom.images(outer_side))
            existing = found.get(key)
            if existing is not None and existing.charge >= exact:
                continue
            found[key] = TwoOfThreeViolation(
                points=points,
                charge=exact,
                triangle=(i, j, k),
                classes=(self.classes[i], self.classes[j], self.classes[k]),
                angles=(self.angles[i], self.angles[j], self.angles[k]),
            )
        atoms = sorted(found.values(), key=lambda item: item.charge, reverse=True)
        heaviest = float(atoms[0].charge) if atoms else 0.0
        logger.info(
            "separation: %s triangles, max centroid charge %.6f, %s violated (float), "
            "%s rechecked exactly, %s vertex-refined, %s violated orbits "
            "(max charge %.6f), %.2fs",
            len(triangles),
            float(charges.max()),
            int((charges > 1).sum()),
            checked,
            refined,
            len(atoms),
            heaviest,
            time.perf_counter() - started,
        )
        return atoms


def atom_columns(
    orbits: Sequence[tuple[ThresholdAtom, ...]],
    exact_rows: Sequence[ExactRow],
    half_tangents: tuple[Fraction, ...],
    square_side: Fraction,
    *,
    slack: float = COVER_SLACK,
) -> tuple[sparse.csr_matrix, np.ndarray]:
    """Coefficient matrix ``[rows x orbits]`` and cost vector for threshold-atom orbits.

    Coefficient: how many images in the orbit the row's placement charges (contains at
    least ``k`` of the image's points), with the LP's loosening. Cost: orbit size times
    ``floor(|S|/k)``.
    """

    costs = np.array(
        [len(orbit) * (orbit[0].size // orbit[0].threshold) for orbit in orbits],
        dtype=float,
    )
    n_rows = len(exact_rows)
    if not orbits or n_rows == 0:
        return sparse.csr_matrix((n_rows, len(orbits))), costs
    directions = direction_net(half_tangents)
    images: list[ThresholdAtom] = []
    orbit_of: list[int] = []
    for orbit_index, orbit in enumerate(orbits):
        for image in orbit:
            images.append(image)
            orbit_of.append(orbit_index)
    max_size = max(image.size for image in images)
    pts = np.full((len(images), max_size, 2), np.nan)
    thresholds = np.array([image.threshold for image in images])
    for image_index, image in enumerate(images):
        for point_index, (x, y) in enumerate(image.points):
            pts[image_index, point_index] = (float(x), float(y))
    orbit_of_arr = np.array(orbit_of)
    row_dirs = np.array([row[0] for row in exact_rows])
    xs = np.array([float(row[1]) for row in exact_rows])
    ys = np.array([float(row[2]) for row in exact_rows])
    half = float(square_side) / 2 + slack
    rows_out: list[np.ndarray] = []
    cols_out: list[np.ndarray] = []
    vals_out: list[np.ndarray] = []
    for direction_index, direction in enumerate(directions):
        which = np.flatnonzero(row_dirs == direction_index)
        if which.size == 0:
            continue
        cosine, sine = float(direction.ux), float(direction.uy)
        pu = pts[..., 0] * cosine + pts[..., 1] * sine
        pv = -pts[..., 0] * sine + pts[..., 1] * cosine
        cu = xs[which] * cosine + ys[which] * sine
        cv = -xs[which] * sine + ys[which] * cosine
        inside = (np.abs(pu[None, :, :] - cu[:, None, None]) <= half) & (
            np.abs(pv[None, :, :] - cv[:, None, None]) <= half
        )
        count = inside.sum(axis=2)
        charged = count >= thresholds[None, :]
        row_hits, image_hits = np.nonzero(charged)
        if row_hits.size == 0:
            continue
        rows_out.append(which[row_hits])
        cols_out.append(orbit_of_arr[image_hits])
        vals_out.append(np.ones(row_hits.size))
    if not rows_out:
        return sparse.csr_matrix((n_rows, len(orbits))), costs
    matrix = sparse.csr_matrix(
        sparse.coo_matrix(
            (np.concatenate(vals_out), (np.concatenate(rows_out), np.concatenate(cols_out))),
            shape=(n_rows, len(orbits)),
        )
    )
    matrix.sum_duplicates()
    return matrix, costs


def class_summary(atoms: Sequence[TwoOfThreeViolation]) -> dict[str, int]:
    return dict(Counter("-".join(sorted(atom.classes)) for atom in atoms))
