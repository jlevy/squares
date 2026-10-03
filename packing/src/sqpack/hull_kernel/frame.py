"""The frame: everything about one packing problem that the kernel's arithmetic reads.

A frame fixes the physical cap `U` (the container is `[0, U]^2`), the field side `L` and
so the scale `B = L/U` (field coordinates are physical coordinates times `B`), the
closed owner cells as physical polygons inside the centre box `[1/2, U - 1/2]^2`, the
number of squares, the symmetry group as exact actions about `(U/2, U/2)` with the cell
permutations they induce, and the strict-core slack of the counting rows.

n11 is the frame `U = 387708359002281417731/10^20`, `L = 191/50`, sixteen cells and the
half-turn; n17 is `U = L = 1169/250`, `B = 1`, twenty-four cells and D4. Nothing else in
`sqpack.hull_kernel` names a size.

Group elements follow `check_n17_capacity_one_cover`: `r<k>` turns by `k` quarter turns
and `f<k>` reflects `x` first, then turns. A frame computes each permutation from the
geometry, by exact vertex-set matching, and refuses when an action does not map the cell
set onto itself or the actions are not closed under composition.

States are `occupancy`-subsets of cells as sorted tuples, and an orbit representative is
the lexicographically least state of its orbit. For n11 that is n11's own rule
(`min(mask, half_turn(mask))`), so the representatives in lexicographic order are its
2,184 canonical masks in their published order.

Capacity one is not asserted here. n11's cells have diameter below one; n17's corner
and side cells do not, and their capacity comes from the cover tool's wall lemma, so a
frame records where its cells came from in `provenance` and leaves capacity to that
source. `cells_reaching_diameter_one` reports which cells a diameter argument would
refuse.
"""

from __future__ import annotations

import itertools
from collections.abc import Sequence
from dataclasses import dataclass
from functools import cached_property

from sqpack.hull_kernel.geometry import (
    Point,
    Polygon,
    require,
    strictly_convex_counterclockwise,
)
from sqpack.hull_kernel.rational import Q, Rational

D4_ACTIONS = ("r0", "r1", "r2", "r3", "f0", "f1", "f2", "f3")
HALF_TURN_ACTIONS = ("r0", "r2")
DEFAULT_CORE_SLACK = Q(1, 10**12)

type Matrix = tuple[int, int, int, int]


def d4_matrix(name: str) -> Matrix:
    """`(a, b, c, d)` acting on offsets as `(x, y) -> (a x + b y, c x + d y)`."""
    require(name in D4_ACTIONS, f"unknown symmetry action: {name}")
    a, b, c, d = (-1, 0, 0, 1) if name[0] == "f" else (1, 0, 0, 1)
    for _ in range(int(name[1])):
        a, b, c, d = -c, -d, a, b  # the quarter turn (x, y) -> (-y, x) after the rest
    return a, b, c, d


def apply_matrix(matrix: Matrix, centre: Q, point: Point) -> Point:
    a, b, c, d = matrix
    x, y = point[0] - centre, point[1] - centre
    return centre + a * x + b * y, centre + c * x + d * y


def induced_permutation(
    cells: Sequence[Sequence[Point]], matrix: Matrix, centre: Q
) -> tuple[int, ...]:
    """The cell permutation an action induces, by exact vertex-set identity."""
    index = {frozenset(cell): number for number, cell in enumerate(cells)}
    require(len(index) == len(cells), "two cells have the same vertex set")
    images: list[int] = []
    for number, cell in enumerate(cells):
        image = frozenset(apply_matrix(matrix, centre, vertex) for vertex in cell)
        require(image in index, f"cell {number}: its image is not a cell of the frame")
        images.append(index[image])
    return tuple(images)


def compose(first: Sequence[int], second: Sequence[int]) -> tuple[int, ...]:
    """The permutation `i -> first[second[i]]`."""
    return tuple(first[image] for image in second)


def orbit_representatives(
    cell_count: int, size: int, permutations: Sequence[Sequence[int]]
) -> tuple[tuple[int, ...], ...]:
    """The lexicographically least state of every orbit, in lexicographic order.

    States are bit masks with cell `i` at bit `cell_count - 1 - i`, so among states of
    one size a larger mask is a lexicographically smaller sorted tuple: the least cell of
    the symmetric difference is the highest differing bit. A state is its orbit's
    representative exactly when no image has a larger mask. Images are formed bytewise
    through lookup tables; every operation is on exact integers.
    """
    require(0 <= size <= cell_count, "state size outside the cell count")
    identity = tuple(range(cell_count))
    byte_count = (cell_count + 7) // 8

    def bit(cell: int) -> int:
        return 1 << (cell_count - 1 - cell)

    tables: list[list[list[int]]] = []
    for permutation in permutations:
        require(sorted(permutation) == list(identity), "a symmetry action is not a permutation")
        if tuple(permutation) == identity:
            continue
        per_byte: list[list[int]] = []
        for byte in range(byte_count):
            table = [0] * 256
            for value in range(1, 256):
                image = 0
                for offset in range(8):
                    position = 8 * byte + offset
                    if value >> offset & 1 and position < cell_count:
                        image |= bit(permutation[cell_count - 1 - position])
                table[value] = image
            per_byte.append(table)
        tables.append(per_byte)
    full = (1 << cell_count) - 1
    complement = 2 * size > cell_count
    chosen = cell_count - size if complement else size
    shifts = tuple(8 * byte for byte in range(byte_count))
    found: list[int] = []
    for combination in itertools.combinations(range(cell_count), chosen):
        mask = 0
        for cell in combination:
            mask |= bit(cell)
        if complement:
            mask ^= full
        least = True
        for per_byte in tables:
            image = 0
            for shift, table in zip(shifts, per_byte, strict=True):
                image |= table[mask >> shift & 255]
            if image > mask:
                least = False
                break
        if least:
            found.append(mask)
    found.sort(reverse=True)
    return tuple(
        tuple(cell for cell in range(cell_count) if mask & bit(cell)) for mask in found
    )


def squared_diameter(polygon: Sequence[Point]) -> Q:
    return max(
        (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for p, q in itertools.combinations(polygon, 2)
    )


@dataclass(frozen=True)
class SymmetryAction:
    name: str
    matrix: Matrix
    permutation: tuple[int, ...]


@dataclass(frozen=True)
class Frame:
    """One packing problem's constants; build it with `make_frame`, which validates."""

    name: str
    cap: Q
    length: Q
    cells: tuple[tuple[Point, ...], ...]
    cell_names: tuple[str, ...]
    occupancy: int
    actions: tuple[SymmetryAction, ...]
    core_slack: Q = DEFAULT_CORE_SLACK
    provenance: str = ""
    capture_cap: Q | None = None

    @property
    def scale(self) -> Q:
        """`B = L/U`: a unit square is a square of side `B` in field coordinates."""
        return self.length / self.cap

    @property
    def inner_cap(self) -> Q:
        """`U'`, the side that confines the squares; `U` unless a capture cap is set."""
        return self.cap if self.capture_cap is None else self.capture_cap

    def centre_bounds(self, half_extent: Q) -> tuple[Q, Q]:
        """The closed legal centre interval on either axis, in physical coordinates.

        A square whose axis-parallel half-extent is at least `half_extent` lies in the
        container `[(U - U')/2, (U + U')/2]^2` only if its centre does in
        `[(U - U')/2 + h, (U + U')/2 - h]`. With no capture cap that is `[h, U - h]`,
        n11's one-sided wall bounds, as the same exact rationals.
        """
        offset = (self.cap - self.inner_cap) / 2
        return offset + half_extent, self.cap - offset - half_extent

    def field_centre_bounds(self, half_extent: Q) -> tuple[Q, Q]:
        """`centre_bounds` in field coordinates; `half_extent` stays physical."""
        low, high = self.centre_bounds(half_extent)
        return self.scale * low, self.scale * high

    def cell(self, index: int) -> Polygon:
        """The closed cell in physical coordinates."""
        return list(self.cells[index])

    def world(self, index: int) -> Polygon:
        """The closed cell in field coordinates (physical times `B`)."""
        scale = self.scale
        return [(scale * x, scale * y) for x, y in self.cells[index]]

    def rotate(self, p: Point, c: Q, s: Q) -> Point:
        """A field point in the frame of a square turned by `(c, s)` about `(L/2, L/2)`."""
        x, y = p[0] - self.length / 2, p[1] - self.length / 2
        return c * x + s * y, -s * x + c * y

    def image(self, action: SymmetryAction, state: Sequence[int]) -> tuple[int, ...]:
        return tuple(sorted(action.permutation[cell] for cell in state))

    @cached_property
    def representatives(self) -> tuple[tuple[int, ...], ...]:
        """One state per orbit, the least, in lexicographic order."""
        return orbit_representatives(
            len(self.cells), self.occupancy, [action.permutation for action in self.actions]
        )

    def states_containing(self, pattern: Sequence[int]) -> list[int]:
        """Representatives a symmetry image of which contains `pattern`: the states that an
        unconditional contradiction on the cells of `pattern` excludes, by containment
        (the other squares are unconstrained) and by the symmetry of container and cover.
        """
        target = set(pattern)
        return [
            index
            for index, state in enumerate(self.representatives)
            if any(target.issubset(self.image(action, state)) for action in self.actions)
        ]

    def cells_reaching_diameter_one(self) -> tuple[str, ...]:
        """Cells whose diameter is at least one, which a diameter argument would refuse."""
        return tuple(
            name
            for name, cell in zip(self.cell_names, self.cells, strict=True)
            if squared_diameter(cell) >= 1
        )


def make_frame(
    *,
    name: str,
    cap: Rational,
    length: Rational,
    cells: Sequence[Sequence[tuple[Rational, Rational]]],
    cell_names: Sequence[str],
    occupancy: int,
    action_names: Sequence[str],
    core_slack: Rational = DEFAULT_CORE_SLACK,
    provenance: str = "",
    capture_cap: Rational | None = None,
) -> Frame:
    """Validate the inputs and compute every action's cell permutation from geometry.

    Every number is taken into the kernel's rational type `Q` here, so the geometry
    downstream runs on one type whatever the caller passed (`Fraction` from the cover
    tools, integers from tests).
    """
    cap, length, core_slack = Q(cap), Q(length), Q(core_slack)
    capture_cap = None if capture_cap is None else Q(capture_cap)
    require(cap > 1 and length > 0, "the cap must exceed one and the field side be positive")
    require(0 < core_slack < length / cap, "the core slack must lie strictly inside (0, B)")
    require(
        capture_cap is None or 1 < capture_cap <= cap,
        "a capture cap must lie in (1, U]",
    )
    polygons = tuple(tuple((Q(x), Q(y)) for x, y in cell) for cell in cells)
    names = tuple(cell_names)
    require(
        len(names) == len(polygons) == len(set(names)), "cell names must be unique, one each"
    )
    low, high = Q(1, 2), cap - Q(1, 2)
    for cell_name, polygon in zip(names, polygons, strict=True):
        require(
            strictly_convex_counterclockwise(list(polygon)),
            f"cell {cell_name}: not a strictly convex counterclockwise polygon",
        )
        require(
            all(low <= x <= high and low <= y <= high for x, y in polygon),
            f"cell {cell_name}: leaves the centre box",
        )
    require(0 < occupancy <= len(polygons), "occupancy outside the cell count")
    require(
        bool(action_names) and action_names[0] == "r0", "the first action must be the identity"
    )
    require(len(set(action_names)) == len(action_names), "duplicate symmetry action")
    centre = cap / 2
    actions = tuple(
        SymmetryAction(
            action, d4_matrix(action), induced_permutation(polygons, d4_matrix(action), centre)
        )
        for action in action_names
    )
    permutations = {action.permutation for action in actions}
    require(
        all(
            compose(p.permutation, q.permutation) in permutations
            for p in actions
            for q in actions
        ),
        "the symmetry actions are not closed under composition",
    )
    return Frame(
        name=name,
        cap=cap,
        length=length,
        cells=polygons,
        cell_names=names,
        occupancy=occupancy,
        actions=actions,
        core_slack=core_slack,
        provenance=provenance,
        capture_cap=capture_cap,
    )
