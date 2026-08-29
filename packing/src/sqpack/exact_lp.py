"""A linear program over certified coefficients, decided without a tolerance.

Fix every square's angle and fix, for each pair, which of the four candidate axes
separates it.  What is left is a linear program: corners are affine in the square's
translation, containment is linear, each separating-axis condition is a conjunction of
linear inequalities, and `min s` is linear.  That is the *cell* the quench solves, and
`sqpack.research.quench` solves it in `f64` through HiGHS.

D-021 is why this module exists.  HiGHS will not go tighter than `1e-10`, so a float
cell solve can be wrong by roughly `1e-11`, and no post-check written in floats can tell
a true contact from an overlap at that scale.  Raising precision moves the threshold and
never removes it: a tight packing has pairs whose true separation is exactly zero.

So this module carries the *same* cell into exact arithmetic and decides it there.  The
coefficients are whatever exact scalar the caller's pose is built from -- `Fraction` for
an axis-aligned cell, a `sqpack.field.FieldElement` for a tilted one -- and every
comparison goes through the injected `sign`, which is the seam `sqpack.verify` and
`sqpack.promote.contacts` already use.  Nothing here rounds, and nothing here compares
against a tolerance.

**What it solves, and what it does not.**  Given a feasible vertex it pivots to the
exact optimum by Bland's rule and returns a certificate: the exact optimal point, the
exact multipliers, and the active set they belong to.  Optimality is then checkable
without trusting the search -- `A_S z = b_S`, `A z <= b`, `A_S^T y = -c`, `y >= 0`, each
decided by exact sign.  It does **not** find that first vertex.  Phase 1 of the simplex
is not built here, and the intended supplier is the float path: HiGHS locates a basis in
milliseconds, and this module certifies or repairs it in exact arithmetic.  That
division is the standard one for exact LP, and it is why a float noise floor does not
propagate into the answer -- a wrong starting basis is repaired or refused, never
believed.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from sqpack.verify import Square, edge_axes, project

# The scalar type is the caller's, exactly as in `sqpack.promote.contacts`: pinning the
# annotation to `Fraction` or to `FieldElement` would contradict the seam that lets one
# implementation serve a rational cell and an algebraic one.
Scalar = Any

# A pivot budget large enough that Trump's cell cannot reach it, and small enough that a
# broken pivot rule is reported rather than run overnight.
DEFAULT_PIVOT_BUDGET = 400


class ExactLPError(ValueError):
    """A typed refusal from the exact LP, suitable for both human and machine callers."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


def is_exactly_zero(value: Scalar) -> bool:
    """Structural zero test, answered without arithmetic by both scalar types.

    A `FieldElement` is zero exactly when its reduced representative is, which is what
    `is_zero` reports; a `Fraction` answers the same question by comparison.  This is
    used only to skip terms and to find pivots, never to decide a constraint -- those go
    through the caller's `sign`.
    """
    is_zero = getattr(value, "is_zero", None)
    return bool(is_zero()) if is_zero is not None else value == 0


def rational_sign(value: Scalar) -> int:
    """Sign function for `Fraction` and `int` scalars, with no tolerance anywhere."""
    return (value > 0) - (value < 0)


@dataclass(frozen=True)
class LinearRow:
    """One labelled linear form, read as `coefficients . variables`.

    The shape the tangent-cone cases already use, kept here so an exact LP row and an
    exact tangent-cone row are the same object rather than two spellings of it.
    """

    label: str
    coefficients: tuple[Scalar, ...]


@dataclass(frozen=True)
class ExactLP:
    """`min objective . z` subject to `row . z <= rhs`, every variable free.

    `zero` and `one` are the caller's, because a program over `Q(u)` and a program over
    `Q` do not share a constant.
    """

    objective: tuple[Scalar, ...]
    rows: tuple[LinearRow, ...]
    rhs: tuple[Scalar, ...]
    zero: Scalar
    one: Scalar

    def __post_init__(self) -> None:
        if len(self.rows) != len(self.rhs):
            raise ExactLPError(
                "bad-request",
                f"{len(self.rows)} rows against {len(self.rhs)} right-hand sides",
            )
        width = len(self.objective)
        wrong = [row.label for row in self.rows if len(row.coefficients) != width]
        if wrong:
            raise ExactLPError(
                "bad-request",
                f"{len(wrong)} row(s) are not {width} wide, first {wrong[0]}",
            )

    @property
    def width(self) -> int:
        return len(self.objective)


@dataclass(frozen=True)
class ExactVertex:
    """A vertex of the program together with everything needed to re-check it."""

    active: tuple[int, ...]
    point: tuple[Scalar, ...]
    multipliers: tuple[Scalar, ...]
    objective_value: Scalar


@dataclass(frozen=True)
class ExactSolution:
    """An exactly optimal vertex and how much pivoting reaching it took."""

    vertex: ExactVertex
    pivots: int
    started_optimal: bool


def solve_square_system(
    matrix: Sequence[Sequence[Scalar]], rhs: Sequence[Scalar], one: Scalar
) -> list[Scalar]:
    """Solve a square system by Gauss-Jordan elimination in the scalars given.

    Pivots are chosen as the first structurally non-zero entry, which is exact and
    deterministic; there is no tolerance to choose because there is no rounding to
    protect against.  A rank-deficient system is a typed refusal, never a least-squares
    answer.
    """
    size = len(matrix)
    if any(len(row) != size for row in matrix) or len(rhs) != size:
        raise ExactLPError("bad-request", f"a {size}-row system needs {size} columns and rhs")
    tableau = [[*row, value] for row, value in zip(matrix, rhs, strict=True)]
    for column in range(size):
        pivot = next(
            (
                index
                for index in range(column, size)
                if not is_exactly_zero(tableau[index][column])
            ),
            None,
        )
        if pivot is None:
            raise ExactLPError(
                "singular-basis", f"the active set is rank deficient at column {column}"
            )
        tableau[column], tableau[pivot] = tableau[pivot], tableau[column]
        inverse = one / tableau[column][column]
        tableau[column] = [value * inverse for value in tableau[column]]
        for index in range(size):
            if index == column:
                continue
            factor = tableau[index][column]
            if is_exactly_zero(factor):
                continue
            tableau[index] = [
                left - factor * right
                for left, right in zip(tableau[index], tableau[column], strict=True)
            ]
    return [tableau[index][size] for index in range(size)]


def _support(rows: Sequence[LinearRow]) -> list[tuple[int, ...]]:
    """Column indices carrying a non-zero coefficient, per row.

    The cell's rows are sparse -- two non-zeros in a containment row, four in a
    separation row -- and exact multiplication is expensive enough that multiplying by a
    structural zero 1,000 times a pass is the difference between seconds and minutes.
    """
    return [
        tuple(
            index for index, value in enumerate(row.coefficients) if not is_exactly_zero(value)
        )
        for row in rows
    ]


def _dot(
    coefficients: Sequence[Scalar], point: Sequence[Scalar], support, zero: Scalar
) -> Scalar:
    total = zero
    for index in support:
        total = total + coefficients[index] * point[index]
    return total


def independent_rows(
    lp: ExactLP, candidates: Sequence[int], *, size: int | None = None
) -> tuple[int, ...]:
    """Greedily select linearly independent rows from `candidates`, in the order given.

    Exact elimination decides independence, so a row that a float rank test would call
    dependent at `1e-12` and independent at `1e-13` has one answer here.
    """
    wanted = lp.width if size is None else size
    chosen: list[int] = []
    basis: list[list[Scalar]] = []
    pivots: list[int] = []
    for candidate in candidates:
        reduced = list(lp.rows[candidate].coefficients)
        for row, column in zip(basis, pivots, strict=True):
            factor = reduced[column]
            if is_exactly_zero(factor):
                continue
            reduced = [left - factor * right for left, right in zip(reduced, row, strict=True)]
        column = next(
            (index for index, value in enumerate(reduced) if not is_exactly_zero(value)), None
        )
        if column is None:
            continue
        inverse = lp.one / reduced[column]
        basis.append([value * inverse for value in reduced])
        pivots.append(column)
        chosen.append(candidate)
        if len(chosen) == wanted:
            return tuple(chosen)
    raise ExactLPError(
        "no-vertex-basis",
        f"only {len(chosen)} of the {wanted} independent rows a vertex needs are among "
        f"the {len(candidates)} candidate(s) offered",
    )


def certify_vertex(
    lp: ExactLP, active: Sequence[int], sign: Callable[[Scalar], int]
) -> ExactVertex:
    """Return the exact vertex `active` defines, or refuse with the reason it is not one.

    Three exact conditions, and each has its own refusal kind so a caller can tell a
    starting basis that is merely not optimal from one that is not a vertex at all:
    the active rows must be independent, the point they determine must satisfy *every*
    row, and the multipliers reproducing the objective must be non-negative.
    """
    if len(active) != lp.width:
        raise ExactLPError(
            "bad-request",
            f"a vertex of a {lp.width}-variable program needs {lp.width} active rows, "
            f"got {len(active)}",
        )
    basis = [list(lp.rows[index].coefficients) for index in active]
    point = solve_square_system(basis, [lp.rhs[index] for index in active], lp.one)

    support = _support(lp.rows)
    for index, row in enumerate(lp.rows):
        slack = lp.rhs[index] - _dot(row.coefficients, point, support[index], lp.zero)
        if sign(slack) < 0:
            raise ExactLPError(
                "primal-infeasible",
                f"the point determined by the active set violates row {row.label}",
            )

    transpose = [[basis[row][column] for row in range(lp.width)] for column in range(lp.width)]
    multipliers = solve_square_system(transpose, [-value for value in lp.objective], lp.one)
    for position, value in enumerate(multipliers):
        if sign(value) < 0:
            raise ExactLPError(
                "dual-infeasible",
                f"row {lp.rows[active[position]].label} carries a negative multiplier, so "
                f"the active set is a vertex but not an optimal one",
            )
    return ExactVertex(
        active=tuple(active),
        point=tuple(point),
        multipliers=tuple(multipliers),
        objective_value=_dot(lp.objective, point, tuple(range(lp.width)), lp.zero),
    )


def solve(
    lp: ExactLP,
    start: Sequence[int],
    sign: Callable[[Scalar], int],
    *,
    pivot_budget: int = DEFAULT_PIVOT_BUDGET,
) -> ExactSolution:
    """Pivot from a feasible vertex to the exact optimum, by Bland's rule.

    `start` names `width` rows that are active and independent at a feasible point; a
    float solve is the intended supplier.  The primal feasibility of that starting point
    is checked exactly before anything moves, so a basis read off a noisy solution is
    refused rather than pivoted from.

    Bland's rule -- lowest index out, lowest index in among ties -- is chosen over the
    steepest one because the cell is degenerate at a tight packing, and a rule that
    cycles on degeneracy would turn an exact answer into a hang.  `pivot_budget` is the
    second line against that: Bland's rule proves termination, and the budget reports it
    if the proof is ever broken.
    """
    support = _support(lp.rows)
    active = list(start)
    inactive = [index for index in range(len(lp.rows)) if index not in set(active)]

    pivots = 0
    while True:
        basis = [list(lp.rows[index].coefficients) for index in active]
        point = solve_square_system(basis, [lp.rhs[index] for index in active], lp.one)
        slacks = [
            lp.rhs[index] - _dot(lp.rows[index].coefficients, point, support[index], lp.zero)
            for index in range(len(lp.rows))
        ]
        violated = next((index for index, value in enumerate(slacks) if sign(value) < 0), None)
        if violated is not None:
            raise ExactLPError(
                "primal-infeasible",
                f"row {lp.rows[violated].label} is violated at pivot {pivots}, so the "
                f"starting active set was not a feasible vertex",
            )

        transpose = [
            [basis[row][column] for row in range(lp.width)] for column in range(lp.width)
        ]
        multipliers = solve_square_system(transpose, [-value for value in lp.objective], lp.one)
        leaving = next(
            (position for position in range(lp.width) if sign(multipliers[position]) < 0),
            None,
        )
        if leaving is None:
            return ExactSolution(
                vertex=ExactVertex(
                    active=tuple(active),
                    point=tuple(point),
                    multipliers=tuple(multipliers),
                    objective_value=_dot(lp.objective, point, tuple(range(lp.width)), lp.zero),
                ),
                pivots=pivots,
                started_optimal=pivots == 0,
            )
        if pivots >= pivot_budget:
            raise ExactLPError(
                "pivot-budget",
                f"the exact simplex did not reach optimality within {pivot_budget} pivots",
            )

        unit = [lp.one if position == leaving else lp.zero for position in range(lp.width)]
        direction = solve_square_system(basis, [-value for value in unit], lp.one)

        entering: int | None = None
        best: Scalar | None = None
        for index in inactive:
            rate = _dot(lp.rows[index].coefficients, direction, support[index], lp.zero)
            if sign(rate) <= 0:
                continue
            step = slacks[index] / rate
            if best is None or sign(step - best) < 0:
                entering, best = index, step
        if entering is None:
            raise ExactLPError(
                "unbounded",
                f"the objective decreases without bound along the edge leaving "
                f"{lp.rows[active[leaving]].label}",
            )
        inactive.remove(entering)
        inactive.append(active[leaving])
        inactive.sort()
        active[leaving] = entering
        pivots += 1


@dataclass(frozen=True)
class CoefficientReport:
    """Whether a cell's program is rational, and by how much it is not."""

    total: int
    rational: int
    verdict: str

    @property
    def algebraic(self) -> int:
        return self.total - self.rational


def _is_rational(value: Scalar) -> bool:
    """True when the scalar lies in `Q`, whichever exact representation carries it."""
    coefficients = getattr(value, "coeffs", None)
    if coefficients is None:
        return True
    return not any(coefficients[1:])


def coefficient_report(lp: ExactLP) -> CoefficientReport:
    """Count how many of the program's coefficients leave `Q`.

    A cell whose angles are all multiples of a right angle has corner offsets `+-1/2`
    and edge normals `+-1`, so its program is rational and `Fraction` suffices.  One
    tilted square is enough to put every coefficient it touches into an algebraic
    extension, and then only a number field will do.
    """
    values = [
        *lp.objective,
        *lp.rhs,
        *(value for row in lp.rows for value in row.coefficients),
    ]
    rational = sum(1 for value in values if _is_rational(value))
    return CoefficientReport(
        total=len(values),
        rational=rational,
        verdict="rational" if rational == len(values) else "algebraic",
    )


def separating_axes(
    squares: Sequence[Square], sign: Callable[[Scalar], int]
) -> dict[tuple[int, int], tuple[int, int]]:
    """Read each pair's separating axis and orientation off the pose itself.

    This is the *combinatorial* half of the cell -- what a search has to discover and
    what the program takes as given.  Decided by the injected `sign`, so over exact
    scalars the choice is certified rather than measured.
    """
    choices: dict[tuple[int, int], tuple[int, int]] = {}
    for i in range(len(squares)):
        for j in range(i + 1, len(squares)):
            first, second = squares[i], squares[j]
            for position, axis in enumerate(edge_axes(first) + edge_axes(second)):
                first_lo, first_hi = project(first, axis, sign)
                second_lo, second_hi = project(second, axis, sign)
                if sign(second_lo - first_hi) >= 0:
                    choices[(i, j)] = (position, 1)
                    break
                if sign(first_lo - second_hi) >= 0:
                    choices[(i, j)] = (position, -1)
                    break
            else:
                raise ExactLPError(
                    "no-separating-axis", f"pair {(i, j)} has no separating axis in this pose"
                )
    return choices


def fixed_cell_lp(
    squares: Sequence[Square],
    sign: Callable[[Scalar], int],
    *,
    zero: Scalar,
    one: Scalar,
) -> ExactLP:
    """Assemble the exact program of the cell the pose sits in.

    Variables are `dx_0..dx_{n-1}, dy_0..dy_{n-1}, s`: each square's translation from
    where the pose put it, and the container side.  Writing it in translations rather
    than centres keeps every coefficient a difference of the pose's own exact
    coordinates, so no scalar is introduced that the certificate did not already carry.

    Two families, both sixteen rows wide, giving `16 * (n + C(n, 2))` rows:

    - **containment**, per square: four corners against four container edges;
    - **separation**, per pair: each corner of the earlier square at or before each
      corner of the later one along the pair's fixed axis.
    """
    count = len(squares)
    if count < 2:
        raise ExactLPError("bad-request", f"need at least two squares, got {count}")
    width = 2 * count + 1
    side_column = 2 * count
    rows: list[LinearRow] = []
    rhs: list[Scalar] = []

    def add(label: str, entries: dict[int, Scalar], bound: Scalar) -> None:
        coefficients = [zero] * width
        for column, value in entries.items():
            coefficients[column] = value
        rows.append(LinearRow(label, tuple(coefficients)))
        rhs.append(bound)

    for index, square in enumerate(squares):
        for corner, (px, py) in enumerate(square):
            add(f"wall:{index}:left:{corner}", {index: -one}, px)
            add(f"wall:{index}:bottom:{corner}", {count + index: -one}, py)
            add(f"wall:{index}:right:{corner}", {index: one, side_column: -one}, -px)
            add(f"wall:{index}:top:{corner}", {count + index: one, side_column: -one}, -py)

    for (i, j), (position, orientation) in separating_axes(squares, sign).items():
        axis = (edge_axes(squares[i]) + edge_axes(squares[j]))[position]
        lo, hi = (i, j) if orientation > 0 else (j, i)
        for first, (px, py) in enumerate(squares[lo]):
            for second, (qx, qy) in enumerate(squares[hi]):
                add(
                    f"pair:{i}:{j}:axis{position}:{first}-{second}",
                    {
                        lo: axis[0],
                        count + lo: axis[1],
                        hi: -axis[0],
                        count + hi: -axis[1],
                    },
                    (axis[0] * qx + axis[1] * qy) - (axis[0] * px + axis[1] * py),
                )

    objective = [zero] * width
    objective[side_column] = one
    return ExactLP(
        objective=tuple(objective), rows=tuple(rows), rhs=tuple(rhs), zero=zero, one=one
    )


def translated_squares(squares: Sequence[Square], point: Sequence[Scalar]) -> list[list[tuple]]:
    """Apply a solution of `fixed_cell_lp` back to the pose it was built from."""
    count = len(squares)
    return [
        [(px + point[index], py + point[count + index]) for px, py in square]
        for index, square in enumerate(squares)
    ]
