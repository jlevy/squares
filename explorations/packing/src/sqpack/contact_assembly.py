"""Finite canonical labels for small abstract contact-scaffold candidates.

This module is deliberately geometry-free. It quotients colored contact graphs by
square relabeling and the eight symmetries of the container, and it returns typed limit
receipts instead of treating a truncated orbit or candidate stream as complete.
"""

from __future__ import annotations

import json
import math
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import combinations, islice, permutations
from typing import Literal

type Axis = Literal["u", "v"]
type Wall = Literal["left", "right", "bottom", "top"]
type LimitKind = Literal["orbit-image-cap", "candidate-cap", "emitted-label-cap"]
type ProposalLimitKind = Literal["coloring-space-cap", "emitted-scaffold-cap"]

MAX_SCAFFOLD_SIZE = 5
WALL_ORDER: dict[Wall, int] = {"left": 0, "right": 1, "bottom": 2, "top": 3}
WALL_VECTORS: dict[Wall, tuple[int, int]] = {
    "left": (-1, 0),
    "right": (1, 0),
    "bottom": (0, -1),
    "top": (0, 1),
}
VECTOR_WALLS: dict[tuple[int, int], Wall] = {
    vector: wall for wall, vector in WALL_VECTORS.items()
}


class ScaffoldError(ValueError):
    """A typed malformed-label or unsupported-slice failure."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


@dataclass(frozen=True, order=True)
class ContactEdge:
    """One directed signed normal relation, stored on an unordered vertex pair."""

    left: int
    right: int
    normal: Axis
    sign: int


@dataclass(frozen=True)
class ContactScaffold:
    """A connected colored contact graph with optional container-wall colors.

    ``vertex_colors`` are semantic, caller-normalized tokens. The orbit action preserves
    them exactly; arbitrary source-local angle-class names must therefore be normalized
    before constructing a scaffold.
    """

    vertex_colors: tuple[str, ...]
    edges: tuple[ContactEdge, ...]
    wall_contacts: tuple[tuple[Wall, ...], ...]

    def __post_init__(self) -> None:
        size = len(self.vertex_colors)
        if not 1 <= size <= MAX_SCAFFOLD_SIZE:
            raise ScaffoldError(
                "unsupported-size",
                f"contact scaffolds require 1..{MAX_SCAFFOLD_SIZE} vertices",
            )
        if any(not isinstance(color, str) or not color for color in self.vertex_colors):
            raise ScaffoldError("malformed-color", "vertex colors must be nonempty strings")
        if len(self.wall_contacts) != size:
            raise ScaffoldError(
                "wall-count-mismatch", "wall_contacts must have one entry per vertex"
            )

        normalized_walls: list[tuple[Wall, ...]] = []
        for walls in self.wall_contacts:
            if len(set(walls)) != len(walls) or any(wall not in WALL_ORDER for wall in walls):
                raise ScaffoldError(
                    "malformed-wall-color", "wall colors must be unique known wall names"
                )
            normalized_walls.append(tuple(sorted(walls, key=WALL_ORDER.__getitem__)))

        normalized_edges: list[ContactEdge] = []
        seen_pairs: set[tuple[int, int]] = set()
        for edge in self.edges:
            if edge.normal not in {"u", "v"} or edge.sign not in {-1, 1}:
                raise ScaffoldError(
                    "malformed-edge-color", "edge normal and sign must be u/v and -1/+1"
                )
            if edge.left == edge.right:
                raise ScaffoldError("self-contact", "contact edges cannot be self-loops")
            if not 0 <= edge.left < size or not 0 <= edge.right < size:
                raise ScaffoldError(
                    "vertex-out-of-range", "contact edge vertex is out of range"
                )
            if edge.left < edge.right:
                normalized = edge
            else:
                normalized = ContactEdge(edge.right, edge.left, edge.normal, -edge.sign)
            pair = (normalized.left, normalized.right)
            if pair in seen_pairs:
                raise ScaffoldError(
                    "duplicate-contact-pair", "a vertex pair has more than one contact color"
                )
            seen_pairs.add(pair)
            normalized_edges.append(normalized)

        normalized_edges.sort()
        if size > 1 and not _connected(size, normalized_edges):
            raise ScaffoldError("disconnected-scaffold", "a contact scaffold must be connected")
        object.__setattr__(self, "edges", tuple(normalized_edges))
        object.__setattr__(self, "wall_contacts", tuple(normalized_walls))


@dataclass(frozen=True)
class D4Transform:
    """One signed permutation matrix acting on axes and container walls."""

    name: str
    xx: int
    xy: int
    yx: int
    yy: int


D4_TRANSFORMS: tuple[D4Transform, ...] = (
    D4Transform("identity", 1, 0, 0, 1),
    D4Transform("rotate-90", 0, -1, 1, 0),
    D4Transform("rotate-180", -1, 0, 0, -1),
    D4Transform("rotate-270", 0, 1, -1, 0),
    D4Transform("reflect-x", 1, 0, 0, -1),
    D4Transform("reflect-y", -1, 0, 0, 1),
    D4Transform("reflect-diagonal", 0, 1, 1, 0),
    D4Transform("reflect-antidiagonal", 0, -1, -1, 0),
)
D4_BY_NAME = {transform.name: transform for transform in D4_TRANSFORMS}


@dataclass(frozen=True)
class OrbitWitness:
    """The exact group element mapping an input scaffold to its canonical label."""

    symmetry: str
    old_to_new: tuple[int, ...]


@dataclass(frozen=True)
class CanonicalScaffold:
    status: Literal["canonical"]
    canonical_label: str
    scaffold: ContactScaffold
    witness: OrbitWitness
    raw_image_count: int
    unique_image_count: int


@dataclass(frozen=True)
class CanonicalizationLimit:
    status: Literal["limit"]
    kind: Literal["orbit-image-cap"]
    limit: int
    required_images: int
    examined_images: int
    partial_best_label: str


type CanonicalizationResult = CanonicalScaffold | CanonicalizationLimit


@dataclass(frozen=True)
class ScaffoldLimits:
    maximum_candidates: int
    maximum_emitted_labels: int
    maximum_orbit_images: int = 960

    def __post_init__(self) -> None:
        if (
            min(
                self.maximum_candidates,
                self.maximum_emitted_labels,
                self.maximum_orbit_images,
            )
            < 1
        ):
            raise ScaffoldError("malformed-cap", "all scaffold caps must be positive")


@dataclass(frozen=True)
class ScaffoldEnumeration:
    status: Literal["completed", "limit"]
    canonical_labels: tuple[str, ...]
    examined_candidates: int
    duplicate_candidates: int
    limit_kind: LimitKind | None
    limit: int | None
    encountered_candidates: int


@dataclass(frozen=True)
class IsomorphFreeScaffoldEnumeration:
    """A complete or explicitly bounded quotient of one uniform wall-free slice."""

    status: Literal["completed", "limit"]
    scaffolds: tuple[ContactScaffold, ...]
    topology_count: int
    required_colorings: int
    examined_colorings: int
    orbit_action_images: int
    limit_kind: ProposalLimitKind | None
    limit: int | None


def _connected(size: int, edges: list[ContactEdge]) -> bool:
    adjacent = [set() for _ in range(size)]
    for edge in edges:
        adjacent[edge.left].add(edge.right)
        adjacent[edge.right].add(edge.left)
    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in adjacent[vertex] - reached:
            reached.add(neighbor)
            frontier.append(neighbor)
    return len(reached) == size


def _connected_pairs(size: int, edges: tuple[tuple[int, int], ...]) -> bool:
    return _connected(size, [ContactEdge(left, right, "u", 1) for left, right in edges])


def _mapped_pair(left: int, right: int, old_to_new: tuple[int, ...]) -> tuple[int, int]:
    mapped_left, mapped_right = old_to_new[left], old_to_new[right]
    return (
        (mapped_left, mapped_right)
        if mapped_left < mapped_right
        else (mapped_right, mapped_left)
    )


def connected_topology_representatives(
    size: int,
) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Enumerate connected simple graph topologies once, modulo vertex relabeling."""
    if not 1 <= size <= MAX_SCAFFOLD_SIZE:
        raise ScaffoldError(
            "unsupported-size",
            f"topology enumeration requires 1..{MAX_SCAFFOLD_SIZE} vertices",
        )
    pairs = tuple(combinations(range(size), 2))
    representatives: set[tuple[tuple[int, int], ...]] = set()
    relabelings = tuple(permutations(range(size)))
    for mask in range(1 << len(pairs)):
        edges = tuple(pair for index, pair in enumerate(pairs) if mask & (1 << index))
        if not _connected_pairs(size, edges):
            continue
        representatives.add(
            min(
                tuple(sorted(_mapped_pair(left, right, relabeling) for left, right in edges))
                for relabeling in relabelings
            )
        )
    return tuple(sorted(representatives, key=lambda edges: (len(edges), edges)))


def _topology_automorphisms(
    size: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, ...], ...]:
    edge_set = set(edges)
    return tuple(
        relabeling
        for relabeling in permutations(range(size))
        if {_mapped_pair(left, right, relabeling) for left, right in edges} == edge_set
    )


_EDGE_COLORS: tuple[tuple[Axis, int], ...] = (
    ("u", -1),
    ("u", 1),
    ("v", -1),
    ("v", 1),
)
_EDGE_COLOR_INDEX: dict[tuple[Axis, int], int] = {
    color: index for index, color in enumerate(_EDGE_COLORS)
}


def _coloring_actions(
    size: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[tuple[int, ...], ...], ...]:
    """Precompute base-four contributions for Aut(topology) x D4."""
    edge_index = {edge: index for index, edge in enumerate(edges)}
    powers = tuple(4 ** (len(edges) - index - 1) for index in range(len(edges)))
    actions: list[tuple[tuple[int, ...], ...]] = []
    for relabeling in _topology_automorphisms(size, edges):
        for symmetry in D4_TRANSFORMS:
            contributions: list[tuple[int, ...]] = []
            for left, right in edges:
                mapped_left, mapped_right = relabeling[left], relabeling[right]
                target = (
                    (mapped_left, mapped_right)
                    if mapped_left < mapped_right
                    else (mapped_right, mapped_left)
                )
                target_power = powers[edge_index[target]]
                mapped_states = []
                for normal, sign in _EDGE_COLORS:
                    mapped_normal, mapped_sign = _edge_color(symmetry, normal, sign)
                    if mapped_left > mapped_right:
                        mapped_sign = -mapped_sign
                    mapped_states.append(
                        _EDGE_COLOR_INDEX[(mapped_normal, mapped_sign)] * target_power
                    )
                contributions.append(tuple(mapped_states))
            actions.append(tuple(contributions))
    return tuple(actions)


def _scaffold_from_coloring(
    size: int, edges: tuple[tuple[int, int], ...], coloring: int
) -> ContactScaffold:
    colored_edges = []
    for left, right in edges:
        power = 4 ** (len(edges) - len(colored_edges) - 1)
        normal, sign = _EDGE_COLORS[(coloring // power) % 4]
        colored_edges.append(ContactEdge(left, right, normal, sign))
    return ContactScaffold(
        ("one-angle-class",) * size,
        tuple(colored_edges),
        ((),) * size,
    )


def enumerate_isomorph_free_scaffolds(
    size: int,
    *,
    maximum_colorings: int,
    maximum_emitted_scaffolds: int,
) -> IsomorphFreeScaffoldEnumeration:
    """Enumerate one representative per S_n-by-D4 orbit without labeled candidates."""
    if (
        isinstance(maximum_colorings, bool)
        or isinstance(maximum_emitted_scaffolds, bool)
        or not isinstance(maximum_colorings, int)
        or not isinstance(maximum_emitted_scaffolds, int)
        or min(maximum_colorings, maximum_emitted_scaffolds) < 1
    ):
        raise ScaffoldError("malformed-cap", "isomorph-free caps must be positive integers")
    topologies = connected_topology_representatives(size)
    required = sum(4 ** len(edges) for edges in topologies)
    if required > maximum_colorings:
        return IsomorphFreeScaffoldEnumeration(
            "limit",
            (),
            len(topologies),
            required,
            0,
            0,
            "coloring-space-cap",
            maximum_colorings,
        )

    scaffolds: list[ContactScaffold] = []
    examined = 0
    orbit_images = 0
    for edges in topologies:
        coloring_count = 4 ** len(edges)
        seen = bytearray(coloring_count)
        actions = _coloring_actions(size, edges)
        for coloring in range(coloring_count):
            examined += 1
            if seen[coloring]:
                continue
            if len(scaffolds) >= maximum_emitted_scaffolds:
                return IsomorphFreeScaffoldEnumeration(
                    "limit",
                    tuple(scaffolds),
                    len(topologies),
                    required,
                    examined,
                    orbit_images,
                    "emitted-scaffold-cap",
                    maximum_emitted_scaffolds,
                )
            digits = tuple(
                (coloring // (4 ** (len(edges) - index - 1))) % 4 for index in range(len(edges))
            )
            for action in actions:
                image = sum(
                    contribution[state]
                    for contribution, state in zip(action, digits, strict=True)
                )
                seen[image] = 1
            orbit_images += len(actions)
            scaffolds.append(_scaffold_from_coloring(size, edges, coloring))
    return IsomorphFreeScaffoldEnumeration(
        "completed",
        tuple(scaffolds),
        len(topologies),
        required,
        examined,
        orbit_images,
        None,
        None,
    )


def _vector(transform: D4Transform, x: int, y: int) -> tuple[int, int]:
    return transform.xx * x + transform.xy * y, transform.yx * x + transform.yy * y


def _edge_color(transform: D4Transform, normal: Axis, sign: int) -> tuple[Axis, int]:
    source = (sign, 0) if normal == "u" else (0, sign)
    x, y = _vector(transform, *source)
    if x:
        return "u", x
    return "v", y


def _wall_color(transform: D4Transform, wall: Wall) -> Wall:
    return VECTOR_WALLS[_vector(transform, *WALL_VECTORS[wall])]


def transform_scaffold(
    scaffold: ContactScaffold,
    *,
    symmetry: D4Transform,
    old_to_new: tuple[int, ...],
) -> ContactScaffold:
    """Apply one explicitly supplied D4 action and vertex relabeling."""
    size = len(scaffold.vertex_colors)
    if tuple(sorted(old_to_new)) != tuple(range(size)):
        raise ScaffoldError("malformed-permutation", "old_to_new must be a permutation")
    colors = [""] * size
    walls: list[tuple[Wall, ...]] = [()] * size
    for old, new in enumerate(old_to_new):
        colors[new] = scaffold.vertex_colors[old]
        walls[new] = tuple(_wall_color(symmetry, wall) for wall in scaffold.wall_contacts[old])
    edges = []
    for edge in scaffold.edges:
        normal, sign = _edge_color(symmetry, edge.normal, edge.sign)
        edges.append(
            ContactEdge(
                old_to_new[edge.left],
                old_to_new[edge.right],
                normal,
                sign,
            )
        )
    return ContactScaffold(tuple(colors), tuple(edges), tuple(walls))


def replay_orbit_witness(scaffold: ContactScaffold, witness: OrbitWitness) -> ContactScaffold:
    """Replay a retained orbit witness against its source scaffold."""
    try:
        symmetry = D4_BY_NAME[witness.symmetry]
    except KeyError as error:
        raise ScaffoldError(
            "unknown-symmetry", f"unknown D4 symmetry {witness.symmetry!r}"
        ) from error
    return transform_scaffold(
        scaffold,
        symmetry=symmetry,
        old_to_new=witness.old_to_new,
    )


def scaffold_label(scaffold: ContactScaffold) -> str:
    """Serialize a normalized scaffold to deterministic comparison bytes."""
    document = {
        "contract": "packing.squares:ContactScaffoldLabel/v1",
        "vertices": [
            {"color": color, "walls": list(walls)}
            for color, walls in zip(scaffold.vertex_colors, scaffold.wall_contacts, strict=True)
        ],
        "edges": [[edge.left, edge.right, edge.normal, edge.sign] for edge in scaffold.edges],
    }
    return json.dumps(document, sort_keys=True, separators=(",", ":"))


def scaffold_orbit(
    scaffold: ContactScaffold,
) -> Iterable[tuple[OrbitWitness, ContactScaffold]]:
    """Yield the full raw D4-by-permutation orbit in fixed order."""
    size = len(scaffold.vertex_colors)
    for symmetry in D4_TRANSFORMS:
        for old_to_new in permutations(range(size)):
            witness = OrbitWitness(symmetry.name, old_to_new)
            yield (
                witness,
                transform_scaffold(
                    scaffold,
                    symmetry=symmetry,
                    old_to_new=old_to_new,
                ),
            )


def canonicalize_scaffold(
    scaffold: ContactScaffold, *, maximum_orbit_images: int = 960
) -> CanonicalizationResult:
    """Return a canonical label or a typed incomplete-orbit receipt."""
    if maximum_orbit_images < 1:
        raise ScaffoldError("malformed-cap", "maximum_orbit_images must be positive")
    required = len(D4_TRANSFORMS) * math.factorial(len(scaffold.vertex_colors))
    best: tuple[str, OrbitWitness, ContactScaffold] | None = None
    unique: set[str] = set()
    examined = 0
    for witness, image in islice(scaffold_orbit(scaffold), maximum_orbit_images):
        examined += 1
        label = scaffold_label(image)
        unique.add(label)
        if best is None or label < best[0]:
            best = label, witness, image
    if best is None:
        raise AssertionError("a nonempty scaffold has an empty symmetry orbit")
    if examined < required:
        return CanonicalizationLimit(
            status="limit",
            kind="orbit-image-cap",
            limit=maximum_orbit_images,
            required_images=required,
            examined_images=examined,
            partial_best_label=best[0],
        )
    return CanonicalScaffold(
        status="canonical",
        canonical_label=best[0],
        scaffold=best[2],
        witness=best[1],
        raw_image_count=required,
        unique_image_count=len(unique),
    )


def enumerate_canonical_scaffolds(
    candidates: Iterable[ContactScaffold], *, limits: ScaffoldLimits
) -> ScaffoldEnumeration:
    """Deduplicate a finite stream or stop with one explicit partial-coverage reason."""
    labels: set[str] = set()
    duplicates = 0
    examined = 0
    encountered = 0
    for encountered, candidate in enumerate(candidates, start=1):
        if encountered > limits.maximum_candidates:
            return ScaffoldEnumeration(
                "limit",
                tuple(sorted(labels)),
                examined,
                duplicates,
                "candidate-cap",
                limits.maximum_candidates,
                encountered,
            )
        result = canonicalize_scaffold(
            candidate, maximum_orbit_images=limits.maximum_orbit_images
        )
        examined += 1
        if isinstance(result, CanonicalizationLimit):
            return ScaffoldEnumeration(
                "limit",
                tuple(sorted(labels)),
                examined,
                duplicates,
                "orbit-image-cap",
                result.limit,
                encountered,
            )
        if result.canonical_label in labels:
            duplicates += 1
            continue
        if len(labels) >= limits.maximum_emitted_labels:
            return ScaffoldEnumeration(
                "limit",
                tuple(sorted(labels)),
                examined,
                duplicates,
                "emitted-label-cap",
                limits.maximum_emitted_labels,
                encountered,
            )
        labels.add(result.canonical_label)
    return ScaffoldEnumeration(
        "completed",
        tuple(sorted(labels)),
        examined,
        duplicates,
        None,
        None,
        encountered,
    )
