"""Every containment and non-overlap inequality of a fixed-side pose, in the chart.

The local-rigidity question is not "is the pose a vertex of the twenty active
inequalities". It is "on some neighborhood, is the feasible set *exactly* those twenty".
Answering the second needs the whole system written down -- every wall against every
corner, and for every pair of squares every separating axis, every orientation of that
axis, and every support feature -- with an exact base margin for each. The margins that
are strictly nonzero are what a continuity argument turns into a neighborhood; the ones
that are exactly zero are the local system.

**Counts are computed, never adopted.** `ConstraintSystem.counts` reports what this pose
actually has. Comparing that against a planning document's expectation is the caller's
job, and `verify_counts` returns the disagreement rather than raising, so a discrepancy is
reported loudly instead of being smoothed over.

The non-overlap encoding is the separating-axis theorem in its conjunctive form. Two
convex polygons have disjoint interiors exactly when some edge normal of one of them puts
the whole of the other on its outer side. For a square that is four edges each, so eight
branches per pair, and each branch is the conjunction of four corner-versus-edge
inequalities -- one per support feature of the opposite square. Writing the branch as a
conjunction rather than as `min over corners` is what keeps every inequality polynomial:
a `min` is not, and a `min` linearised at a tie is the error `D-388` records.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from sqpack.field import FieldElement
from sqpack.local_rigidity.chart import DOF, Chart
from sqpack.local_rigidity.polynomial import Poly

WALLS: tuple[str, ...] = ("left", "bottom", "right", "top")
"""Container sides, in the order the receipt lists them."""


class InfeasibleBaseError(ValueError):
    """The declared base pose violates one of its own constraints, exactly.

    Nothing downstream means anything after this: a neighborhood of an infeasible point is
    a neighborhood of nothing, and a "certificate" built there certifies an impossible
    packing. This is `D-354`'s failure mode with the sign flipped.
    """


class DisjunctiveTouchError(ValueError):
    """A touching pair whose local non-overlap set is a union, not a single inequality.

    Two branches reaching margin zero means two independent axes hold the pair apart, and
    non-overlap asks for *either*. Intersecting them reports a smaller feasible set and so
    a more rigid pose than the geometry has -- the flattering direction, and exactly what
    `devtools.assess_n5_rigidity.DisjunctiveContactError` refuses at first order.
    """


class IncompleteEnumerationError(ValueError):
    """The constraint enumeration is missing inequalities the pose's combinatorics need."""


class OverlapError(ValueError):
    """A pair of squares whose every separating branch is strictly violated at base."""


@dataclass(frozen=True, slots=True)
class WallConstraint:
    """`corner of square k is on the inner side of one container wall`."""

    square: int
    corner: int
    wall: str
    polynomial: Poly
    denominator: str
    margin: FieldElement

    @property
    def key(self) -> str:
        return f"wall/{self.square}/{self.corner}/{self.wall}"

    def describe(self) -> str:
        return f"square {self.square} corner {self.corner} against the {self.wall} wall"


@dataclass(frozen=True, slots=True)
class PairCornerConstraint:
    """`corner j of the moving square is on the outer side of edge e of the host`."""

    host: int
    edge: int
    moving: int
    corner: int
    polynomial: Poly
    denominator: str
    margin: FieldElement

    @property
    def key(self) -> str:
        return f"pair/{self.host}/{self.edge}/{self.moving}/{self.corner}"

    def describe(self) -> str:
        return (
            f"square {self.moving} corner {self.corner} outside square {self.host} "
            f"edge {self.edge}"
        )


@dataclass(frozen=True, slots=True)
class PairBranch:
    """One separating-axis branch: a host edge, and the four support features it tests."""

    host: int
    edge: int
    moving: int
    constraints: tuple[PairCornerConstraint, ...]

    @property
    def pair(self) -> tuple[int, int]:
        return (min(self.host, self.moving), max(self.host, self.moving))

    @property
    def key(self) -> str:
        return f"branch/{self.host}/{self.edge}/{self.moving}"

    def minimum(self) -> PairCornerConstraint:
        """The support feature attaining the branch's least margin, exactly.

        Ties are broken by corner index so the choice is deterministic and the receipt is
        byte-stable; which of two equal minima is named does not affect any decision.
        """
        best = self.constraints[0]
        for candidate in self.constraints[1:]:
            if (candidate.margin - best.margin).sign() < 0:
                best = candidate
        return best

    def describe(self) -> str:
        return (
            f"square {self.host} edge {self.edge} separates square {self.moving} "
            f"(4 support features)"
        )


PairStatus = Literal["touching", "noncontact"]


@dataclass(frozen=True, slots=True)
class PairReport:
    """What the eight branches of one pair say, and which of them is load-bearing."""

    pair: tuple[int, int]
    status: PairStatus
    branches: tuple[PairBranch, ...]
    active_branch: PairBranch | None
    active_constraint: PairCornerConstraint | None
    witness_branch: PairBranch | None
    witness_margin: FieldElement | None

    @property
    def key(self) -> str:
        return f"pair/{self.pair[0]}-{self.pair[1]}"


@dataclass(frozen=True, slots=True)
class InequalityBook:
    """Every inequality of the pose, enumerated and evaluated, but not yet classified.

    Separated from `ConstraintSystem` because classification can refuse -- an overlapping
    or corner-on-corner pose raises -- while feasibility of some *other* chart point is a
    question worth asking about exactly those poses. `controls.exp034_angle_and_slide`
    needs the feasibility predicate at a pose whose contact structure this reduction does
    not cover, and it would be a poor instrument that could not answer there.
    """

    chart: Chart
    walls: tuple[WallConstraint, ...]
    pairs: tuple[tuple[PairBranch, ...], ...]

    def expected_cardinality(self) -> dict[str, int]:
        """What the pose's combinatorics require, computed from the pose alone.

        The guard `controls.omitted_constraint` trips: an enumeration that quietly lost a
        branch still produces margins, still produces a neighborhood, and still produces a
        smaller feasible set than the geometry has.
        """
        count = self.chart.pose.count
        corners = [len(square) for square in self.chart.pose.corners]
        walls = sum(corner * len(WALLS) for corner in corners)
        branches = 0
        inequalities = 0
        for first in range(count):
            for second in range(first + 1, count):
                for host, moving in ((first, second), (second, first)):
                    branches += self.chart.pose.edge_count(host)
                    inequalities += self.chart.pose.edge_count(host) * corners[moving]
        return {
            "wall_corner_inequalities": walls,
            "pairs": count * (count - 1) // 2,
            "sat_branches": branches,
            "sat_corner_inequalities": inequalities,
        }

    def actual_cardinality(self) -> dict[str, int]:
        return {
            "wall_corner_inequalities": len(self.walls),
            "pairs": len(self.pairs),
            "sat_branches": sum(len(group) for group in self.pairs),
            "sat_corner_inequalities": sum(
                len(branch.constraints) for group in self.pairs for branch in group
            ),
        }

    def enumeration_is_complete(self) -> bool:
        return self.expected_cardinality() == self.actual_cardinality()


@dataclass(frozen=True, slots=True)
class ConstraintSystem:
    """The complete inequality description of one pose, with exact base margins."""

    chart: Chart
    walls: tuple[WallConstraint, ...]
    pairs: tuple[PairReport, ...]
    book: InequalityBook

    # -- classification ----------------------------------------------------

    @property
    def active_walls(self) -> tuple[WallConstraint, ...]:
        return tuple(constraint for constraint in self.walls if constraint.margin.sign() == 0)

    @property
    def inactive_walls(self) -> tuple[WallConstraint, ...]:
        return tuple(constraint for constraint in self.walls if constraint.margin.sign() > 0)

    @property
    def touching_pairs(self) -> tuple[PairReport, ...]:
        return tuple(report for report in self.pairs if report.status == "touching")

    @property
    def noncontact_pairs(self) -> tuple[PairReport, ...]:
        return tuple(report for report in self.pairs if report.status == "noncontact")

    def all_pair_constraints(self) -> tuple[PairCornerConstraint, ...]:
        return tuple(
            constraint
            for report in self.pairs
            for branch in report.branches
            for constraint in branch.constraints
        )

    def active_constraints(self) -> tuple[tuple[str, Poly], ...]:
        """The local system: exactly the constraints with margin zero at the pose."""
        rows: list[tuple[str, Poly]] = [
            (constraint.key, constraint.polynomial) for constraint in self.active_walls
        ]
        rows.extend(
            (report.active_constraint.key, report.active_constraint.polynomial)
            for report in self.touching_pairs
            if report.active_constraint is not None
        )
        return tuple(rows)

    def counts(self) -> dict[str, int]:
        """What this pose actually has. Never read from a plan."""
        pair_constraints = self.all_pair_constraints()
        return {
            "squares": self.chart.pose.count,
            "chart_variables": self.chart.arity,
            "wall_corner_inequalities": len(self.walls),
            "wall_corner_active": len(self.active_walls),
            "wall_corner_inactive": len(self.inactive_walls),
            "pairs": len(self.pairs),
            "touching_pairs": len(self.touching_pairs),
            "noncontact_pairs": len(self.noncontact_pairs),
            "sat_branches": sum(len(report.branches) for report in self.pairs),
            "sat_corner_inequalities": len(pair_constraints),
            "active_pair_inequalities": len(self.touching_pairs),
            "active_total": len(self.active_walls) + len(self.touching_pairs),
        }

    def verify_counts(self, expected: dict[str, int]) -> dict[str, tuple[int, int]]:
        """Return `{field: (expected, actual)}` for every disagreement, empty if none."""
        actual = self.counts()
        return {
            field: (value, actual[field])
            for field, value in expected.items()
            if field in actual and actual[field] != value
        }


def _wall_polynomial(chart: Chart, square: int, corner: int, wall: str) -> Poly:
    px, py = chart.cleared_corner(square, corner)
    denominator = chart.denominator(square)
    side = Poly.constant(chart.field, chart.arity, chart.pose.side)
    if wall == "left":
        return px
    if wall == "bottom":
        return py
    if wall == "right":
        return side * denominator - px
    if wall == "top":
        return side * denominator - py
    raise ValueError(f"unknown wall {wall!r}")


def _pair_polynomial(chart: Chart, host: int, edge: int, moving: int, corner: int) -> Poly:
    """`D_h D_k * (n_{h,e} . (p_{k,j} - c_h) - 1/2)`, cleared and exact.

    The `1/2` is the half-width of a unit square along its own edge normal, which is a
    constant only because `Chart.orthogonality_certificate` has already established that
    the cleared matrix is `D` times a rotation and `Chart.base_normal_certificate` that the
    base normal is a unit vector. Nothing here recomputes a normalisation, so nothing here
    can introduce an irrational length.
    """
    half = chart.field.rational(1) / chart.field.rational(2)
    host_denominator = chart.denominator(host)
    moving_denominator = chart.denominator(moving)
    nx, ny = chart.cleared_normal(host, edge)
    px, py = chart.cleared_corner(moving, corner)
    hx, hy = chart.centre(host)
    shifted_x = px - moving_denominator * hx
    shifted_y = py - moving_denominator * hy
    return nx * shifted_x + ny * shifted_y - (host_denominator * moving_denominator).scale(half)


def build_book(chart: Chart) -> InequalityBook:
    """Enumerate and evaluate every inequality, refusing nothing.

    The base margins are computed here because they are what every later step reads, and
    computing them twice would let the two copies disagree.
    """
    chart.require_valid()
    pose = chart.pose
    origin = chart.origin()

    walls: list[WallConstraint] = []
    for square in range(pose.count):
        for corner in range(len(pose.corners[square])):
            for wall in WALLS:
                polynomial = _wall_polynomial(chart, square, corner, wall)
                walls.append(
                    WallConstraint(
                        square=square,
                        corner=corner,
                        wall=wall,
                        polynomial=polynomial,
                        denominator=f"D{square}",
                        margin=polynomial.evaluate(origin),
                    )
                )

    pairs: list[tuple[PairBranch, ...]] = [
        _pair_branches(chart, first, second, origin)
        for first in range(pose.count)
        for second in range(first + 1, pose.count)
    ]
    return InequalityBook(chart=chart, walls=tuple(walls), pairs=tuple(pairs))


def build_system(chart: Chart) -> ConstraintSystem:
    """Enumerate every constraint of the pose and classify each base margin exactly."""
    book = build_book(chart)
    if not book.enumeration_is_complete():
        raise IncompleteEnumerationError(
            f"the enumeration produced {book.actual_cardinality()} where the pose's "
            f"combinatorics require {book.expected_cardinality()}; a missing inequality "
            "reports a larger feasible set than the geometry has"
        )
    for constraint in book.walls:
        if constraint.margin.sign() < 0:
            raise InfeasibleBaseError(
                f"square {constraint.square} corner {constraint.corner} is outside the "
                f"{constraint.wall} wall of {chart.pose.label!r} by an exactly negative "
                "margin; the declared base pose is not a packing"
            )
    reports = tuple(_pair_report(chart, group) for group in book.pairs)
    return ConstraintSystem(chart=chart, walls=book.walls, pairs=reports, book=book)


def _pair_branches(
    chart: Chart, first: int, second: int, origin: list[FieldElement]
) -> tuple[PairBranch, ...]:
    """The eight separating-axis branches of one pair, with exact base margins."""
    pose = chart.pose
    branches: list[PairBranch] = []
    for host, moving in ((first, second), (second, first)):
        for edge in range(pose.edge_count(host)):
            constraints = tuple(
                PairCornerConstraint(
                    host=host,
                    edge=edge,
                    moving=moving,
                    corner=corner,
                    polynomial=(
                        polynomial := _pair_polynomial(chart, host, edge, moving, corner)
                    ),
                    denominator=f"D{host}*D{moving}",
                    margin=polynomial.evaluate(origin),
                )
                for corner in range(len(pose.corners[moving]))
            )
            branches.append(
                PairBranch(host=host, edge=edge, moving=moving, constraints=constraints)
            )
    return tuple(branches)


def _pair_report(chart: Chart, branches: tuple[PairBranch, ...]) -> PairReport:
    """Decide, exactly, whether a pair is separated, singly touching, or overlapping."""
    label = chart.pose.label
    first, second = branches[0].pair
    minima = [branch.minimum().margin for branch in branches]
    best_index = 0
    for index in range(1, len(minima)):
        if (minima[index] - minima[best_index]).sign() > 0:
            best_index = index
    best = minima[best_index]

    if best.sign() < 0:
        raise OverlapError(
            f"squares {first} and {second} of {label!r} have every separating branch "
            "strictly violated at the base pose, so their interiors meet"
        )
    if best.sign() > 0:
        return PairReport(
            pair=(first, second),
            status="noncontact",
            branches=branches,
            active_branch=None,
            active_constraint=None,
            witness_branch=branches[best_index],
            witness_margin=best,
        )

    zero_branches = [branch for branch in branches if branch.minimum().margin.sign() == 0]
    if len(zero_branches) != 1:
        raise DisjunctiveTouchError(
            f"squares {first} and {second} of {label!r} are held apart by "
            f"{len(zero_branches)} branches at once; their local non-overlap set is a "
            "union of half-spaces and intersecting it reports a smaller feasible set"
        )
    active_branch = zero_branches[0]
    zero_corners = [
        constraint for constraint in active_branch.constraints if constraint.margin.sign() == 0
    ]
    if len(zero_corners) != 1:
        raise DisjunctiveTouchError(
            f"squares {first} and {second} of {label!r} touch along "
            f"{len(zero_corners)} support features of branch {active_branch.key}; that is "
            "an edge-flush or corner-on-corner contact, not the single-inequality case "
            "this reduction covers"
        )
    return PairReport(
        pair=(first, second),
        status="touching",
        branches=branches,
        active_branch=active_branch,
        active_constraint=zero_corners[0],
        witness_branch=None,
        witness_margin=None,
    )


# -- the neighborhood, as strict conditions rather than a radius -------------


@dataclass(frozen=True, slots=True)
class StrictCondition:
    """One strict inequality that is open, holds at the pose, and is checked exactly."""

    key: str
    role: str
    sense: Literal["positive", "negative"]
    margin: FieldElement
    polynomial: Poly

    def holds_at_base(self) -> bool:
        wanted = 1 if self.sense == "positive" else -1
        return self.margin.sign() == wanted


@dataclass(frozen=True, slots=True)
class Neighborhood:
    """`U`: the open set on which the local feasible system is exactly the active one.

    `U` is defined as the simultaneous strict inequalities below, not as a ball of some
    computed radius. Each is a polynomial -- hence continuous -- and each holds strictly at
    the pose, so `U` is an open set containing it; no radius is claimed, computed, or
    needed. That is the whole content of "continuity rather than a numerical radius".
    """

    conditions: tuple[StrictCondition, ...]
    active_keys: tuple[str, ...]

    def valid(self) -> bool:
        return all(condition.holds_at_base() for condition in self.conditions)

    def failures(self) -> tuple[str, ...]:
        return tuple(
            condition.key for condition in self.conditions if not condition.holds_at_base()
        )


def build_neighborhood(system: ConstraintSystem) -> Neighborhood:
    """Collect exactly the strict conditions the local reduction argument consumes.

    Four families, and each is needed for a different step:

    - every inactive wall inequality stays strictly positive, so it never binds;
    - for each non-touching pair, one branch stays strictly separating, so the pair is
      free;
    - for each touching pair, each of the other seven branches keeps one support feature
      strictly violated, so no other branch can take over as the separating axis;
    - for each touching pair's active branch, the three non-touching support features stay
      strictly positive, so the branch reduces to its single zero-margin inequality.

    On the intersection, a configuration is feasible exactly when the active inequalities
    hold. The pair step is the separating-axis theorem: with seven branches refuted, the
    disjunction collapses to the eighth.
    """
    conditions: list[StrictCondition] = [
        StrictCondition(
            key=constraint.key,
            role="inactive-wall-stays-slack",
            sense="positive",
            margin=constraint.margin,
            polynomial=constraint.polynomial,
        )
        for constraint in system.inactive_walls
    ]
    for report in system.pairs:
        if report.status == "noncontact":
            assert report.witness_branch is not None
            conditions.extend(
                StrictCondition(
                    key=constraint.key,
                    role="noncontact-pair-stays-separated",
                    sense="positive",
                    margin=constraint.margin,
                    polynomial=constraint.polynomial,
                )
                for constraint in report.witness_branch.constraints
            )
            continue
        assert report.active_branch is not None
        assert report.active_constraint is not None
        for branch in report.branches:
            if branch.key == report.active_branch.key:
                for constraint in branch.constraints:
                    if constraint.key == report.active_constraint.key:
                        continue
                    conditions.append(
                        StrictCondition(
                            key=constraint.key,
                            role="active-branch-nontouching-feature-stays-slack",
                            sense="positive",
                            margin=constraint.margin,
                            polynomial=constraint.polynomial,
                        )
                    )
                continue
            witness = branch.minimum()
            conditions.append(
                StrictCondition(
                    key=witness.key,
                    role="competing-branch-stays-refuted",
                    sense="negative",
                    margin=witness.margin,
                    polynomial=witness.polynomial,
                )
            )
    return Neighborhood(
        conditions=tuple(conditions),
        active_keys=tuple(key for key, _ in system.active_constraints()),
    )


# -- exact feasibility, for controls and for accumulating families -----------


def is_feasible(book: InequalityBook, point: list[FieldElement]) -> bool:
    """Exactly: is this chart point a valid packing?

    The full separating-axis test, not the local reduction: containment for every corner
    against every wall, and for every pair at least one branch whose four support-feature
    inequalities all hold. Decided by `FieldElement.sign` alone, so a control that exhibits
    a feasible neighbour is exhibiting one, not observing one within a tolerance.
    """
    for constraint in book.walls:
        if constraint.polynomial.evaluate(point).sign() < 0:
            return False
    for group in book.pairs:
        separated = any(
            all(
                inequality.polynomial.evaluate(point).sign() >= 0
                for inequality in branch.constraints
            )
            for branch in group
        )
        if not separated:
            return False
    return True


def chart_point(
    chart: Chart,
    displacements: dict[int, tuple[FieldElement, FieldElement]],
    angles: dict[int, FieldElement],
) -> list[FieldElement]:
    """Assemble a chart point from per-square displacements and half-angle parameters."""
    point = chart.origin()
    for square, (dx, dy) in displacements.items():
        point[square * DOF] = dx
        point[square * DOF + 1] = dy
    for square, value in angles.items():
        point[square * DOF + 2] = value
    return point
