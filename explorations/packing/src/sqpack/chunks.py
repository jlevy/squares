"""Conservative lattice-component census for known-best square packings."""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from functools import cache
from itertools import combinations
from typing import Any

import mpmath as mp

from sqpack.witness import materialize_witness

ANGLE_TOLERANCE_RADIANS = 1e-6
ANGLE_TOLERANCE_DEGREES = math.degrees(ANGLE_TOLERANCE_RADIANS)
EXACT_ADJACENCY_TOLERANCE = 1e-9
NEAR_ADJACENCY_TOLERANCE = 1e-3
ALLOWED_SHAPES = frozenset({"bar", "L", "rectangle"})
REGISTERED_MAXIMUM_CHUNKS = 6
PORTABLE_TRIG_DIGITS = 50
PORTABLE_ZERO_FLOOR = 1e-14


@dataclass(frozen=True)
class Pose:
    square_id: str
    center_x: float
    center_y: float
    angle_degrees: float


@dataclass(frozen=True)
class _PartitionCandidate:
    key: str
    mask: int
    members: tuple[str, ...]
    shape: str
    angle_class: int
    angle_degrees: float
    off_frame: bool
    maximum_contact_residual: float
    contacts: tuple[tuple[str, str, float], ...]


@dataclass(frozen=True)
class _PartitionSolution:
    candidates: tuple[int, ...]
    free_squares: tuple[int, ...]
    maximum_contact_residual: float


class _PartitionSearchLimitError(RuntimeError):
    pass


class _UnionFind:
    def __init__(self, size: int) -> None:
        self.parents = list(range(size))

    def find(self, item: int) -> int:
        while self.parents[item] != item:
            self.parents[item] = self.parents[self.parents[item]]
            item = self.parents[item]
        return item

    def union(self, left: int, right: int) -> None:
        left_root, right_root = self.find(left), self.find(right)
        if left_root != right_root:
            self.parents[max(left_root, right_root)] = min(left_root, right_root)

    def groups(self) -> list[tuple[int, ...]]:
        grouped: dict[int, list[int]] = {}
        for item in range(len(self.parents)):
            grouped.setdefault(self.find(item), []).append(item)
        return [tuple(values) for _root, values in sorted(grouped.items())]


def _orientation(angle_degrees: float) -> float:
    result = angle_degrees % 90.0
    return 0.0 if min(result, 90.0 - result) < 1e-10 else result


def _orientation_distance(left: float, right: float) -> float:
    difference = abs(_orientation(left) - _orientation(right))
    return min(difference, 90.0 - difference)


def _clean_residual(value: float) -> float:
    """Erase arithmetic dust far below the strictest registered tolerance."""
    return 0.0 if abs(value) < PORTABLE_ZERO_FLOOR else value


def _representative_orientation(poses: list[Pose], members: tuple[int, ...]) -> float:
    # Orientations live modulo 90 degrees. Multiplying by four maps them to an ordinary
    # circle, where a circular mean handles the 0/90 seam without a special case. Use
    # mpmath instead of the platform libm because the result enters a retained,
    # byte-stable census.
    with mp.workdps(PORTABLE_TRIG_DIGITS):
        radians = [
            mp.mpf(repr(4 * poses[index].angle_degrees)) * mp.pi / 180 for index in members
        ]
        cosine = mp.fsum(mp.cos(angle) for angle in radians)
        sine = mp.fsum(mp.sin(angle) for angle in radians)
        return _orientation(float(mp.degrees(mp.atan2(sine, cosine)) / 4))


def _poses(witness: dict[str, Any]) -> list[Pose]:
    squares, _side = materialize_witness(witness, digits=80)
    result = []
    for source, corners in zip(witness["squares"], squares, strict=True):
        center_x = float(mp.fsum(x for x, _y in corners) / 4)
        center_y = float(mp.fsum(y for _x, y in corners) / 4)
        edge_x = corners[1][0] - corners[0][0]
        edge_y = corners[1][1] - corners[0][1]
        with mp.workdps(PORTABLE_TRIG_DIGITS):
            angle_degrees = float(mp.degrees(mp.atan2(edge_y, edge_x)))
        result.append(
            Pose(
                str(source["id"]),
                center_x,
                center_y,
                _orientation(angle_degrees),
            )
        )
    return result


def _angle_classes(
    poses: list[Pose], *, angle_tolerance_degrees: float
) -> list[tuple[int, ...]]:
    classes = _UnionFind(len(poses))
    for left in range(len(poses)):
        for right in range(left + 1, len(poses)):
            if (
                _orientation_distance(poses[left].angle_degrees, poses[right].angle_degrees)
                <= angle_tolerance_degrees
            ):
                classes.union(left, right)
    return classes.groups()


def _fitted_angle_classes(
    poses: list[Pose], *, angle_tolerance_degrees: float
) -> list[tuple[int, ...]]:
    """Split tolerance chains until every class fits one circular-mean angle.

    Pairwise tolerance is not transitive. The broad contact view still needs a useful
    partition, so an invalid connected class is cut at its largest circular gap and
    extended greedily only while every member stays within the declared fit radius.
    """
    fitted: list[tuple[int, ...]] = []
    for members in _angle_classes(poses, angle_tolerance_degrees=angle_tolerance_degrees):
        representative = _representative_orientation(poses, members)
        if all(
            _orientation_distance(poses[index].angle_degrees, representative)
            <= angle_tolerance_degrees
            for index in members
        ):
            fitted.append(members)
            continue

        ordered = sorted(
            ((_orientation(poses[index].angle_degrees), index) for index in members),
            key=lambda item: (item[0], item[1]),
        )
        gaps = [
            (
                (ordered[(position + 1) % len(ordered)][0] - angle) % 90.0,
                position,
            )
            for position, (angle, _index) in enumerate(ordered)
        ]
        _gap, seam = max(gaps, key=lambda item: (item[0], -item[1]))
        circular_order = ordered[seam + 1 :] + ordered[: seam + 1]
        group: list[int] = []
        for _angle, index in circular_order:
            proposal = (*group, index)
            proposal_angle = _representative_orientation(poses, proposal)
            if group and any(
                _orientation_distance(poses[item].angle_degrees, proposal_angle)
                > angle_tolerance_degrees
                for item in proposal
            ):
                fitted.append(tuple(sorted(group)))
                group = [index]
            else:
                group.append(index)
        if group:
            fitted.append(tuple(sorted(group)))
    return sorted(fitted, key=lambda members: (min(members), members))


def _lattice_delta(left: Pose, right: Pose, angle_degrees: float) -> tuple[float, float]:
    with mp.workdps(PORTABLE_TRIG_DIGITS):
        radians = mp.mpf(repr(angle_degrees)) * mp.pi / 180
        cosine, sine = mp.cos(radians), mp.sin(radians)
        delta_x = mp.mpf(repr(right.center_x)) - mp.mpf(repr(left.center_x))
        delta_y = mp.mpf(repr(right.center_y)) - mp.mpf(repr(left.center_y))
        return (
            float(delta_x * cosine + delta_y * sine),
            float(-delta_x * sine + delta_y * cosine),
        )


def _adjacency_residual(delta_u: float, delta_v: float) -> tuple[float, int, int]:
    lattice_u, lattice_v = round(delta_u), round(delta_v)
    residual = _clean_residual(math.hypot(delta_u - lattice_u, delta_v - lattice_v))
    return residual, lattice_u, lattice_v


def _shape(points: set[tuple[int, int]]) -> str:
    if len(points) < 2:
        return "singleton"
    width = max(x for x, _y in points) - min(x for x, _y in points) + 1
    height = max(y for _x, y in points) - min(y for _x, y in points) + 1
    if (width == 1 or height == 1) and len(points) == max(width, height):
        return "bar"
    if len(points) == width * height:
        return "rectangle"
    if width > 1 and height > 1 and len(points) == width + height - 1:
        minimum_x, maximum_x = min(x for x, _y in points), max(x for x, _y in points)
        minimum_y, maximum_y = min(y for _x, y in points), max(y for _x, y in points)
        for corner_x, corner_y in (
            (minimum_x, minimum_y),
            (minimum_x, maximum_y),
            (maximum_x, minimum_y),
            (maximum_x, maximum_y),
        ):
            expected = {(x, corner_y) for x in range(minimum_x, maximum_x + 1)} | {
                (corner_x, y) for y in range(minimum_y, maximum_y + 1)
            }
            if points == expected:
                return "L"
    return "other-polyomino"


def _class_components(
    poses: list[Pose], members: tuple[int, ...], tolerance: float, class_id: int
) -> list[dict[str, Any]]:
    representative = _representative_orientation(poses, members)
    adjacency = _UnionFind(len(members))
    member_position = {
        source_index: local_index for local_index, source_index in enumerate(members)
    }
    edges: list[tuple[int, int, float]] = []
    for left_position, left in enumerate(members):
        for right in members[left_position + 1 :]:
            delta_u, delta_v = _lattice_delta(poses[left], poses[right], representative)
            residual, lattice_u, lattice_v = _adjacency_residual(delta_u, delta_v)
            if abs(lattice_u) + abs(lattice_v) == 1 and residual <= tolerance:
                adjacency.union(member_position[left], member_position[right])
                edges.append((left, right, residual))

    components = []
    for component_id, local_members in enumerate(adjacency.groups(), start=1):
        source_members = tuple(members[index] for index in local_members)
        anchor = source_members[0]
        points: set[tuple[int, int]] = set()
        lattice_coordinates = []
        maximum_residual = 0.0
        for member in source_members:
            delta_u, delta_v = _lattice_delta(poses[anchor], poses[member], representative)
            residual, lattice_u, lattice_v = _adjacency_residual(delta_u, delta_v)
            maximum_residual = max(maximum_residual, residual)
            points.add((lattice_u, lattice_v))
            lattice_coordinates.append(
                {
                    "square": poses[member].square_id,
                    "u": lattice_u,
                    "v": lattice_v,
                }
            )
        shape = _shape(points) if len(points) == len(source_members) else "ambiguous-lattice"
        component_edges = [
            {
                "squares": [poses[left].square_id, poses[right].square_id],
                "residual": f"{residual:.12g}",
                "band": "exact" if residual <= EXACT_ADJACENCY_TOLERANCE else "near",
            }
            for left, right, residual in edges
            if left in source_members and right in source_members
        ]
        components.append(
            {
                "id": f"a{class_id:02d}-c{component_id:02d}",
                "angle_class": class_id,
                "angle_degrees": f"{representative:.12g}",
                "members": [poses[index].square_id for index in source_members],
                "size": len(source_members),
                "shape": shape,
                "allowed_shape": shape in ALLOWED_SHAPES,
                "maximum_lattice_residual": f"{maximum_residual:.12g}",
                "lattice_coordinates": lattice_coordinates,
                "internal_edges": component_edges,
            }
        )
    return components


def component_census(witness: dict[str, Any], *, tolerance: float) -> dict[str, Any]:
    """Describe maximal same-angle adjacent components under one residual band.

    A passing certificate is sound for this maximal-component decomposition. A failure
    is only ``not-established``: splitting a maximal component can still yield a valid
    lower-``K`` bar/L/rectangle partition, and that exact partition solver is separate.
    """
    if tolerance not in {EXACT_ADJACENCY_TOLERANCE, NEAR_ADJACENCY_TOLERANCE}:
        raise ValueError("component census accepts only the registered exact or near band")
    poses = _poses(witness)
    classes = _angle_classes(poses, angle_tolerance_degrees=ANGLE_TOLERANCE_DEGREES)
    class_fit_residuals = [
        _clean_residual(
            max(
                _orientation_distance(
                    poses[index].angle_degrees,
                    _representative_orientation(poses, members),
                )
                for index in members
            )
        )
        for members in classes
    ]
    angle_fit_valid = all(
        residual <= ANGLE_TOLERANCE_DEGREES for residual in class_fit_residuals
    )
    components = [
        component
        for class_id, members in enumerate(classes, start=1)
        for component in _class_components(poses, members, tolerance, class_id)
    ]
    chunks = [component for component in components if component["size"] >= 2]
    singletons = [component for component in components if component["size"] == 1]
    allowed_chunks = [component for component in chunks if component["allowed_shape"]]
    unsupported = [component for component in chunks if not component["allowed_shape"]]
    off_frame = [
        component
        for component in allowed_chunks
        if _orientation_distance(float(component["angle_degrees"]), 0) > ANGLE_TOLERANCE_DEGREES
    ]
    established = (
        angle_fit_valid
        and len(allowed_chunks) <= 6
        and len(singletons) <= 2
        and len(off_frame) <= 2
        and not unsupported
    )
    return {
        "n": witness["n"],
        "witness_id": witness["id"],
        "adjacency_tolerance": f"{tolerance:.12g}",
        "angle_tolerance_radians": f"{ANGLE_TOLERANCE_RADIANS:.12g}",
        "angle_class_count": len(classes),
        "angle_fit_valid": angle_fit_valid,
        "maximum_angle_fit_residual_radians": f"{math.radians(max(class_fit_residuals)):.12g}",
        "component_count": len(components),
        "chunk_count": len(allowed_chunks),
        "free_square_count": len(singletons),
        "off_frame_chunk_count": len(off_frame),
        "unsupported_component_count": len(unsupported),
        "structured_square_count": sum(component["size"] for component in allowed_chunks),
        "status": "established" if established else "not-established",
        "limitation": (
            "A pass certifies this maximal-component decomposition. A non-pass does not "
            "refute chunk expressibility until the minimal partition solver is built. "
            "Connected angle classes are rejected if no circular-mean fitted angle lies "
            "within the registered tolerance of every member."
        ),
        "components": components,
    }


def _consecutive_runs(values: list[int]) -> list[tuple[int, ...]]:
    runs: list[list[int]] = []
    for value in sorted(values):
        if not runs or value != runs[-1][-1] + 1:
            runs.append([value])
        else:
            runs[-1].append(value)
    return [tuple(run) for run in runs]


def _component_partition_candidates(
    component: dict[str, Any],
    *,
    square_positions: dict[str, int],
) -> list[_PartitionCandidate]:
    coordinate_to_square = {
        (int(item["u"]), int(item["v"])): str(item["square"])
        for item in component["lattice_coordinates"]
    }
    if len(coordinate_to_square) != len(component["members"]):
        return []
    edge_residual = {
        frozenset(str(square) for square in edge["squares"]): float(edge["residual"])
        for edge in component["internal_edges"]
    }
    angle = float(component["angle_degrees"])
    off_frame = _orientation_distance(angle, 0) > ANGLE_TOLERANCE_DEGREES
    candidates: dict[tuple[str, ...], _PartitionCandidate] = {}

    def add(shape: str, coordinates: set[tuple[int, int]]) -> None:
        if len(coordinates) < 2:
            return
        members = tuple(
            sorted(
                (coordinate_to_square[coordinate] for coordinate in coordinates),
                key=square_positions.__getitem__,
            )
        )
        contacts: list[tuple[str, str, float]] = []
        for u, v in sorted(coordinates):
            for neighbor in ((u + 1, v), (u, v + 1)):
                if neighbor not in coordinates:
                    continue
                left, right = coordinate_to_square[(u, v)], coordinate_to_square[neighbor]
                residual = edge_residual.get(frozenset((left, right)))
                if residual is None:
                    return
                contacts.append((left, right, residual))
        if len(contacts) < len(coordinates) - 1:
            return
        mask = sum(1 << square_positions[member] for member in members)
        maximum_residual = max(residual for _left, _right, residual in contacts)
        key = f"a{int(component['angle_class']):02d}:{shape}:{','.join(members)}"
        candidate = _PartitionCandidate(
            key=key,
            mask=mask,
            members=members,
            shape=shape,
            angle_class=int(component["angle_class"]),
            angle_degrees=angle,
            off_frame=off_frame,
            maximum_contact_residual=maximum_residual,
            contacts=tuple(contacts),
        )
        previous = candidates.get(members)
        if previous is None or (
            candidate.maximum_contact_residual,
            candidate.key,
        ) < (previous.maximum_contact_residual, previous.key):
            candidates[members] = candidate

    by_v: dict[int, list[int]] = {}
    by_u: dict[int, list[int]] = {}
    for u, v in coordinate_to_square:
        by_v.setdefault(v, []).append(u)
        by_u.setdefault(u, []).append(v)
    for v, values in sorted(by_v.items()):
        for run in _consecutive_runs(values):
            for start in range(len(run)):
                for end in range(start + 2, len(run) + 1):
                    add("bar", {(u, v) for u in run[start:end]})
    for u, values in sorted(by_u.items()):
        for run in _consecutive_runs(values):
            for start in range(len(run)):
                for end in range(start + 2, len(run) + 1):
                    add("bar", {(u, v) for v in run[start:end]})

    u_values = sorted({u for u, _v in coordinate_to_square})
    v_values = sorted({v for _u, v in coordinate_to_square})
    for left, right in combinations(u_values, 2):
        for bottom, top in combinations(v_values, 2):
            coordinates = {
                (u, v) for u in range(left, right + 1) for v in range(bottom, top + 1)
            }
            if coordinates <= coordinate_to_square.keys():
                add("rectangle", coordinates)

    for corner_u, corner_v in sorted(coordinate_to_square):
        for direction_u in (-1, 1):
            horizontal = [(corner_u, corner_v)]
            step = 1
            while (corner_u + direction_u * step, corner_v) in coordinate_to_square:
                horizontal.append((corner_u + direction_u * step, corner_v))
                step += 1
            for direction_v in (-1, 1):
                vertical = [(corner_u, corner_v)]
                step = 1
                while (corner_u, corner_v + direction_v * step) in coordinate_to_square:
                    vertical.append((corner_u, corner_v + direction_v * step))
                    step += 1
                for horizontal_size in range(2, len(horizontal) + 1):
                    for vertical_size in range(2, len(vertical) + 1):
                        add(
                            "L",
                            set(horizontal[:horizontal_size]) | set(vertical[:vertical_size]),
                        )

    return sorted(
        candidates.values(),
        key=lambda candidate: (
            -len(candidate.members),
            candidate.maximum_contact_residual,
            candidate.key,
        ),
    )


def _solution_key(
    solution: _PartitionSolution,
    candidates: list[_PartitionCandidate],
) -> tuple[Any, ...]:
    keys = tuple(sorted(candidates[index].key for index in solution.candidates))
    return (
        len(solution.candidates),
        solution.maximum_contact_residual,
        keys,
        solution.free_squares,
    )


def _solve_partition(
    candidates: list[_PartitionCandidate],
    *,
    square_count: int,
    exact_free_squares: int,
    maximum_off_frame_chunks: int,
    maximum_states: int,
) -> tuple[_PartitionSolution | None, int, bool]:
    by_square: list[list[int]] = [[] for _ in range(square_count)]
    for candidate_index, candidate in enumerate(candidates):
        for square_index in range(square_count):
            if candidate.mask & (1 << square_index):
                by_square[square_index].append(candidate_index)
    maximum_candidate_size = max(
        (candidate.mask.bit_count() for candidate in candidates), default=1
    )
    states = 0

    @cache
    def solve(
        remaining: int,
        free_remaining: int,
        off_frame_remaining: int,
    ) -> _PartitionSolution | None:
        nonlocal states
        states += 1
        if states > maximum_states:
            raise _PartitionSearchLimitError
        remaining_count = remaining.bit_count()
        minimum_chunk_count = math.ceil(
            max(0, remaining_count - free_remaining) / maximum_candidate_size
        )
        if free_remaining < 0 or remaining_count < free_remaining:
            return None
        if remaining == 0:
            return _PartitionSolution((), (), 0.0) if free_remaining == 0 else None

        remaining_indices = [index for index in range(square_count) if remaining & (1 << index)]

        def available(index: int) -> list[int]:
            return [
                candidate_index
                for candidate_index in by_square[index]
                if candidates[candidate_index].mask & remaining
                == candidates[candidate_index].mask
                and (not candidates[candidate_index].off_frame or off_frame_remaining > 0)
            ]

        pivot = min(
            remaining_indices,
            key=lambda index: (len(available(index)), index),
        )
        options = available(pivot)
        best: _PartitionSolution | None = None
        for candidate_index in options:
            candidate = candidates[candidate_index]
            child = solve(
                remaining ^ candidate.mask,
                free_remaining,
                off_frame_remaining - int(candidate.off_frame),
            )
            if child is None:
                continue
            proposal = _PartitionSolution(
                tuple(sorted((candidate_index, *child.candidates))),
                child.free_squares,
                max(candidate.maximum_contact_residual, child.maximum_contact_residual),
            )
            if best is None or _solution_key(proposal, candidates) < _solution_key(
                best, candidates
            ):
                best = proposal
                # Count and nonnegative residual cannot improve past this bound. The
                # fixed MRV pivot and candidate ordering define the remaining tie,
                # avoiding an exponential all-ties traversal on dense grids.
                if (
                    len(proposal.candidates) == minimum_chunk_count
                    and proposal.maximum_contact_residual == 0
                ):
                    return proposal
        if free_remaining > 0:
            child = solve(remaining ^ (1 << pivot), free_remaining - 1, off_frame_remaining)
            if child is not None:
                proposal = _PartitionSolution(
                    child.candidates,
                    tuple(sorted((pivot, *child.free_squares))),
                    child.maximum_contact_residual,
                )
                if best is None or _solution_key(proposal, candidates) < _solution_key(
                    best, candidates
                ):
                    best = proposal
                    if (
                        len(proposal.candidates) == minimum_chunk_count
                        and proposal.maximum_contact_residual == 0
                    ):
                        return proposal
        return best

    try:
        result = solve(
            (1 << square_count) - 1,
            exact_free_squares,
            maximum_off_frame_chunks,
        )
    except _PartitionSearchLimitError:
        return None, states, True
    return result, states, False


def minimal_lattice_partition(
    witness: dict[str, Any],
    *,
    tolerance: float,
    maximum_free_squares: int = 2,
    maximum_off_frame_chunks: int = 2,
    maximum_states: int = 250_000,
) -> dict[str, Any]:
    """Find a deterministic bar/L/rectangle partition in the registered free-square slice.

    Candidate chunks are exhaustive for contiguous axis-aligned bars, filled rectangles,
    and corner Ls inside the maximal lattice components emitted by ``component_census``.
    They are deliberately not exhaustive over sliding contact assemblies or angle-class
    splits, which remain typed limitations rather than silent refutations.
    """
    if tolerance not in {EXACT_ADJACENCY_TOLERANCE, NEAR_ADJACENCY_TOLERANCE}:
        raise ValueError("partition search accepts only the registered exact or near band")
    if maximum_free_squares < 0 or maximum_off_frame_chunks < 0 or maximum_states < 1:
        raise ValueError("partition search limits must be nonnegative and states positive")
    component_document = component_census(witness, tolerance=tolerance)
    poses = _poses(witness)
    square_positions = {pose.square_id: index for index, pose in enumerate(poses)}
    candidates = [
        candidate
        for component in component_document["components"]
        for candidate in _component_partition_candidates(
            component,
            square_positions=square_positions,
        )
    ]
    candidates.sort(
        key=lambda candidate: (
            -len(candidate.members),
            candidate.maximum_contact_residual,
            candidate.key,
        )
    )
    options = []
    exhausted = False
    for free_count in range(maximum_free_squares + 1):
        if not component_document["angle_fit_valid"]:
            solution, states, hit_limit = None, 0, False
        else:
            solution, states, hit_limit = _solve_partition(
                candidates,
                square_count=len(poses),
                exact_free_squares=free_count,
                maximum_off_frame_chunks=maximum_off_frame_chunks,
                maximum_states=maximum_states,
            )
        exhausted = exhausted or hit_limit
        option: dict[str, Any] = {
            "free_square_count": free_count,
            "search_states": states,
            "status": (
                "search-limit"
                if hit_limit
                else "no-partition"
                if solution is None
                else "partitioned"
            ),
            "chunk_count": None if solution is None else len(solution.candidates),
            "off_frame_chunk_count": (
                None
                if solution is None
                else sum(candidates[index].off_frame for index in solution.candidates)
            ),
            "maximum_contact_residual": (
                None if solution is None else f"{solution.maximum_contact_residual:.12g}"
            ),
            "free_squares": (
                []
                if solution is None
                else [poses[index].square_id for index in solution.free_squares]
            ),
            "chunks": [],
        }
        if solution is not None:
            option["chunks"] = [
                {
                    "id": candidate.key,
                    "shape": candidate.shape,
                    "members": list(candidate.members),
                    "angle_class": candidate.angle_class,
                    "angle_degrees": f"{candidate.angle_degrees:.12g}",
                    "off_frame": candidate.off_frame,
                    "maximum_contact_residual": (f"{candidate.maximum_contact_residual:.12g}"),
                    "contacts": [
                        {
                            "squares": [left, right],
                            "residual": f"{residual:.12g}",
                            "band": (
                                "exact" if residual <= EXACT_ADJACENCY_TOLERANCE else "near"
                            ),
                        }
                        for left, right, residual in candidate.contacts
                    ],
                }
                for candidate in (candidates[index] for index in solution.candidates)
            ]
        options.append(option)

    successful = [option for option in options if option["status"] == "partitioned"]
    within_budget_options = [
        option for option in successful if option["chunk_count"] <= REGISTERED_MAXIMUM_CHUNKS
    ]
    selected = min(
        within_budget_options or successful,
        key=lambda option: (
            option["free_square_count"],
            option["chunk_count"],
            float(option["maximum_contact_residual"]),
            tuple(chunk["id"] for chunk in option["chunks"]),
        ),
        default=None,
    )
    within_budget = (
        selected is not None and selected["chunk_count"] <= REGISTERED_MAXIMUM_CHUNKS
    )
    earlier_search_limit = selected is not None and any(
        option["status"] == "search-limit"
        and option["free_square_count"] < selected["free_square_count"]
        for option in options
    )
    selection_minimality_indeterminate = selected is not None and (
        (within_budget and earlier_search_limit) or (not within_budget and exhausted)
    )
    selected_partition_minimality = (
        "not-applicable"
        if selected is None
        else "indeterminate-search-limit"
        if selection_minimality_indeterminate
        else "complete"
    )
    minimality_limitation = (
        ""
        if not selection_minimality_indeterminate
        else (
            " The retained partition proves in-budget existence, but its F/C "
            "minimality is indeterminate because an earlier free-count slice hit "
            "the search limit."
            if within_budget
            else " The retained partition proves candidate-universe existence, but "
            "whether an in-budget partition exists and its F/C minimality remain "
            "indeterminate because at least one free-count slice hit the search limit."
        )
    )
    return {
        "n": witness["n"],
        "witness_id": witness["id"],
        "adjacency_tolerance": f"{tolerance:.12g}",
        "angle_tolerance_radians": f"{ANGLE_TOLERANCE_RADIANS:.12g}",
        "candidate_count": len(candidates),
        "angle_fit_valid": component_document["angle_fit_valid"],
        "status": (
            "established"
            if within_budget
            else "not-established-search-limit"
            if exhausted
            else "outside-registered-budget"
            if selected is not None
            else "not-established"
        ),
        "selected_free_square_count": (
            None if selected is None else selected["free_square_count"]
        ),
        "selected_chunk_count": None if selected is None else selected["chunk_count"],
        "selected_partition_minimality": selected_partition_minimality,
        "options": options,
        "limitation": (
            "Complete for bars, filled rectangles, and corner Ls within the reported "
            "maximal lattice components. Sliding contact assemblies and angle-class "
            "splits are outside this candidate universe; a non-establishment is not an "
            "H-044 refutation." + minimality_limitation
        ),
    }


def _contact_edge(
    left: Pose,
    right: Pose,
    angle_degrees: float,
    *,
    contact_tolerance: float,
) -> tuple[float, str] | None:
    delta_u, delta_v = _lattice_delta(left, right, angle_degrees)
    candidates = []
    # A positive-length edge overlap is required. Diagonal point contacts do not glue
    # two squares into one chunk and would otherwise connect every grid diagonal.
    if abs(delta_v) < 1 - contact_tolerance:
        candidates.append((abs(abs(delta_u) - 1), "u-normal"))
    if abs(delta_u) < 1 - contact_tolerance:
        candidates.append((abs(abs(delta_v) - 1), "v-normal"))
    if not candidates:
        return None
    residual, normal = min(candidates)
    residual = _clean_residual(residual)
    return (residual, normal) if residual <= contact_tolerance else None


def _contact_topology(size: int, edges: list[dict[str, Any]]) -> str:
    if size == 1:
        return "singleton"
    degrees: Counter[str] = Counter()
    for edge in edges:
        left, right = edge["squares"]
        degrees[left] += 1
        degrees[right] += 1
    if len(edges) == size - 1 and max(degrees.values()) <= 2:
        return "contact-chain"
    if len(edges) == size - 1:
        return "contact-tree"
    return "contact-patch"


def _contact_freedom(
    member_ids: list[str], edges: list[dict[str, Any]]
) -> tuple[int, int, int]:
    positions = {square_id: index for index, square_id in enumerate(member_ids)}
    directional_components = {}
    for normal in ("u-normal", "v-normal"):
        connected = _UnionFind(len(member_ids))
        for edge in edges:
            if edge["normal"] != normal:
                continue
            left, right = edge["squares"]
            connected.union(positions[left], positions[right])
        directional_components[normal] = len(connected.groups())
    rank = sum(len(member_ids) - count for count in directional_components.values())
    internal_slide_dof = max(0, 2 * len(member_ids) - rank - 2)
    cycle_rank = max(0, len(edges) - len(member_ids) + 1)
    return rank, internal_slide_dof, cycle_rank


def _square_wall_contacts(witness: dict[str, Any], *, tolerance: float) -> dict[str, list[str]]:
    squares, side = materialize_witness(witness, digits=80)
    side_value = float(side)
    result = {}
    for source, corners in zip(witness["squares"], squares, strict=True):
        converted = [(float(x), float(y)) for x, y in corners]
        minimum_x = min(x for x, _y in converted)
        maximum_x = max(x for x, _y in converted)
        minimum_y = min(y for _x, y in converted)
        maximum_y = max(y for _x, y in converted)
        result[str(source["id"])] = [
            wall
            for wall, residual in (
                ("left", abs(minimum_x)),
                ("right", abs(side_value - maximum_x)),
                ("bottom", abs(minimum_y)),
                ("top", abs(side_value - maximum_y)),
            )
            if residual <= tolerance
        ]
    return result


def contact_component_census(
    witness: dict[str, Any],
    *,
    angle_tolerance_radians: float,
    contact_tolerance: float,
) -> dict[str, Any]:
    """Measure same-angle positive-edge-contact assemblies without naming their shape.

    This broader descriptive view tests the owner's assembly intuition without silently
    equating a contact chain or irregular patch with the enumerator's narrower
    bar/L/rectangle grammar.
    """
    if angle_tolerance_radians <= 0 or contact_tolerance <= 0:
        raise ValueError("contact census tolerances must be positive")
    poses = _poses(witness)
    wall_contacts = _square_wall_contacts(witness, tolerance=contact_tolerance)
    angle_tolerance_degrees = math.degrees(angle_tolerance_radians)
    classes = _fitted_angle_classes(poses, angle_tolerance_degrees=angle_tolerance_degrees)
    class_fit_residuals = [
        _clean_residual(
            max(
                _orientation_distance(
                    poses[index].angle_degrees,
                    _representative_orientation(poses, members),
                )
                for index in members
            )
        )
        for members in classes
    ]
    components = []
    for class_id, members in enumerate(classes, start=1):
        representative = _representative_orientation(poses, members)
        adjacency = _UnionFind(len(members))
        local = {source: index for index, source in enumerate(members)}
        edges: list[dict[str, Any]] = []
        for left_position, left in enumerate(members):
            for right in members[left_position + 1 :]:
                contact = _contact_edge(
                    poses[left],
                    poses[right],
                    representative,
                    contact_tolerance=contact_tolerance,
                )
                if contact is None:
                    continue
                residual, normal = contact
                adjacency.union(local[left], local[right])
                edges.append(
                    {
                        "squares": [poses[left].square_id, poses[right].square_id],
                        "normal": normal,
                        "residual": f"{residual:.12g}",
                    }
                )
        for component_id, local_members in enumerate(adjacency.groups(), start=1):
            source_members = tuple(members[index] for index in local_members)
            ids = {poses[index].square_id for index in source_members}
            component_edges = [
                edge
                for edge in edges
                if edge["squares"][0] in ids and edge["squares"][1] in ids
            ]
            member_ids = [poses[index].square_id for index in source_members]
            normal_rank, internal_slide_dof, cycle_rank = _contact_freedom(
                member_ids, component_edges
            )
            seated_members = {
                square_id: wall_contacts[square_id]
                for square_id in member_ids
                if wall_contacts[square_id]
            }
            components.append(
                {
                    "id": f"a{class_id:02d}-c{component_id:02d}",
                    "angle_class": class_id,
                    "angle_degrees": f"{representative:.12g}",
                    "members": member_ids,
                    "size": len(source_members),
                    "topology": _contact_topology(len(source_members), component_edges),
                    "normal_constraint_rank": normal_rank,
                    "internal_slide_dof": internal_slide_dof,
                    "contact_graph_cycle_rank": cycle_rank,
                    "wall_contacts": sorted(
                        {wall for walls in seated_members.values() for wall in walls}
                    ),
                    "wall_seated_squares": seated_members,
                    "edges": component_edges,
                }
            )
    chunks = [component for component in components if component["size"] >= 2]
    singletons = [component for component in components if component["size"] == 1]
    structured = sum(component["size"] for component in chunks)
    return {
        "n": witness["n"],
        "witness_id": witness["id"],
        "angle_tolerance_radians": f"{angle_tolerance_radians:.12g}",
        "contact_tolerance": f"{contact_tolerance:.12g}",
        "angle_class_count": len(classes),
        "angle_fit_valid": all(
            residual <= angle_tolerance_degrees for residual in class_fit_residuals
        ),
        "maximum_angle_fit_residual_radians": (
            f"{math.radians(max(class_fit_residuals)):.12g}"
        ),
        "contact_chunk_count": len(chunks),
        "free_square_count": len(singletons),
        "structured_square_count": structured,
        "structured_fraction": f"{structured / witness['n']:.12g}",
        "internal_slide_dof": sum(component["internal_slide_dof"] for component in chunks),
        "wall_seated_square_count": len(
            {
                square_id
                for component in components
                for square_id in component["wall_seated_squares"]
            }
        ),
        "within_six_chunks_and_three_free": len(chunks) <= 6 and len(singletons) <= 3,
        "limitation": (
            "Contact components establish assembly, not bar/L/rectangle expressibility; "
            "normal-equality rank counts internal slide degrees before overlap intervals "
            "or wall contacts are applied; tolerance-connected angle chains are split "
            "until each class fits one representative angle; angle and contact tolerances "
            "are descriptive numerical choices."
        ),
        "components": components,
    }
