"""Contact equations assembled from a structure, and the closure that makes them square.

This is the step between "which features touch" and "a system a solver can drive".
:mod:`sqpack.promote.contacts` decides the first; :mod:`sqpack.promote.refine` needs the
second; nothing joined them, so the pipeline ran from a frozen structure straight to a
refinement of a system somebody had transcribed by hand.

**Each contact type contributes a different equation, and that is why the feature fields
are not optional.**

| Contact | Condition | Scalar equations |
| --- | --- | ---: |
| `corner-edge` | the corner lies on the edge's line | 1 |
| `edge-edge` | the two edge lines *coincide* | 2 |
| `corner-corner` | the two corners are the same point | 2 |
| `corner-wall` | the corner's coordinate meets the wall | 1 |

A corner-edge contact also leaves the corner free to slide along the edge, which is a
*degree of freedom*, not an equation; an edge-edge contact leaves an overlap interval in
the same way.  Both are inequalities the packing satisfies and neither pins anything, so
neither appears here.  Folding the four rows above into "one equation per contact" is the
mistake this table exists to prevent: it would silently drop the second corner-corner
equation and produce a system that is square by accident.

**`edge-edge` is two, and reading it as one was a real bug.**  Coincident lines in the
plane are two conditions -- the edges parallel, and one point shared -- so putting a
single endpoint of one edge onto the other's line leaves the second square free to
*rotate about that point*.  The rotation keeps the equation satisfied to first order
while the edge digs into its neighbour linearly, which is exactly what was measured: at
`n = 11` a motion in the Jacobian's null space drove three declared edge-edge pairs to
overlaps of `-5.1e-6`, `-4.2e-6` and `-3.2e-6` at a step of `1e-5`, growing linearly in
the step.  The second equation puts the *other* endpoint on the same line, which is
collinearity.

**The raw system is not short of stationarity conditions; it was short of contact
equations.**  The unknowns are each square's centre and angle plus the side: `3n + 1` of
them.  With `edge-edge` counted correctly the contact Jacobian reaches full rank at both
retained sizes -- `34` of `34` at `n = 11` and `88` of `88` at `n = 29` -- so the
contacts alone isolate the pose and nothing needs adding.  Göbel's `n = 5` has no
`edge-edge` contact at all and keeps a genuine shortfall of one, which is where a real
stationarity condition lives.  :func:`close` supplies conditions only when the rank says
one is missing, and now refuses at the two sizes where it was previously inventing four
and seven.

**The `n = 5` shortfall is a degenerate root, not an unpinned optimum, and that is why
the condition is second-order.**  The single direction the contacts leave free is a
rotation of the centre square about its own centre; its `s` component measures `1.0e-16`
and `side_leak` reads `1.00e-16`, so no contact-preserving first-order motion changes the
side and first-order optimality already holds.  Stepping along that direction violates
the contacts at `-0.25 t^2`, the same in both signs across three decades of step.  The pose
is therefore infinitesimally flexible and second-order rigid, and what the contact map
lacks at it is an invertible differential rather than a stationarity statement.
:func:`close` supplies the second-order information by differentiating the contact map
along the free direction; the condition is written out there.

**The pose of a square is a centre, an angle, and a chirality.**  Not just the first
two.  A packing may place a square by a reflection as readily as by a rotation, and a
reflected square's corners wind clockwise, which no centre-plus-angle can produce.  The
corner model is therefore

    corner_k = c + R(t) . (sigma * ox_k / 2, oy_k / 2),    sigma = +1 or -1

with `sigma` reflecting the *local* x axis before the rotation turns it.  `sigma = +1` is
the ordinary case and the formula collapses to a rotation; `sigma = -1` reverses the
corner order, which is exactly what a mirrored square needs.  Chirality is discrete data
about the packing, read off the winding by :mod:`sqpack.promote.contacts` and carried
through here -- it is never an unknown, because there is nothing continuous to solve for.

Assembly is deliberately literal.  It writes down what the structure says and reports
what that leaves, including when what it leaves is underdetermined.  It never invents a
constraint to make the counts meet.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import NamedTuple

import mpmath as mp
import sympy as sp

from sqpack.promote.contacts import ContactStructure, Incidence

#: How many scalar equations each contact type contributes.
EQUATIONS_PER_CONTACT = {
    "corner-edge": 1,
    "edge-edge": 2,
    "corner-corner": 2,
    "corner-wall": 1,
}

#: Half-edge offsets of a unit square's four corners, in the corner order
#: :func:`sqpack.verify.corners_from_poses` produces.
CORNER_OFFSETS = ((-1, -1), (1, -1), (1, 1), (-1, 1))

#: Wall names as `sqpack.promote.contacts.WALLS` spells them, and what each pins:
#: which coordinate, and whether it meets the far side rather than the origin.
WALL_AXIS = {
    "left": (0, False),
    "bottom": (1, False),
    "right": (0, True),
    "top": (1, True),
}


class SystemAssemblyError(ValueError):
    """A typed assembly failure, carrying a `kind` a caller can branch on."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


@dataclass(frozen=True)
class ContactSystem:
    """The assembled system, with everything needed to judge whether it is solvable."""

    n: int
    unknowns: tuple[str, ...]
    equations: tuple[str, ...]
    #: What each scalar equation came from, parallel to :attr:`all_equations` rather than
    #: to `equations` alone -- so a closure condition names the contact it was
    #: differentiated from and is not an anonymous extra row.
    sources: tuple[str, ...]
    angle_identities: int
    #: Per-square `+1` / `-1`, in square order.  Kept on the system because the equations
    #: were written with these signs baked in: a pose fed back in under the other
    #: chirality solves a different system, so :func:`pose_values` checks rather than
    #: assumes.  Required rather than defaulted, for the same reason
    #: :func:`_chirality_of` refuses a structure without one -- a default would be right
    #: for most packings and wrong for the one that motivated the field.
    chirality: tuple[int, ...]
    closure: tuple[str, ...] = ()

    @property
    def all_equations(self) -> tuple[str, ...]:
        """Every scalar equation the system carries: the contacts, then the closure.

        The two fields stay apart because their provenance differs -- one is read off the
        structure, the other is derived from the first -- and nothing downstream should
        care.  Everything that evaluates or differentiates the system reads this, which
        is the difference between a closure a solver can use and a closure that only
        moves :attr:`equation_count`.  While `closure` held prose and
        :func:`contact_jacobian` read `equations` alone, changing a count was the only
        thing a condition could do -- which is the shape of the failure D-361 records:
        conditions sized to a shortfall and named for something they were not.
        """
        return self.equations + self.closure

    @property
    def equation_count(self) -> int:
        return len(self.all_equations)

    @property
    def unknown_count(self) -> int:
        return len(self.unknowns)

    @property
    def deficit(self) -> int:
        """Unknowns minus equations: positive is underdetermined, negative overdetermined."""
        return self.unknown_count - self.equation_count

    def state(self) -> str:
        if self.deficit > 0:
            return "underdetermined"
        if self.deficit < 0:
            return "overdetermined"
        return "square"

    def summary(self) -> str:
        return (
            f"n = {self.n}: {self.equation_count} equations "
            f"({len(self.equations)} from contacts, {len(self.closure)} from closure) "
            f"against "
            f"{self.unknown_count} unknowns -- {self.state()} by {abs(self.deficit)}"
        )


def _chirality_of(structure: ContactStructure) -> tuple[int, ...]:
    """The structure's per-square chirality, refusing a structure that does not carry it.

    An extraction that predates chirality cannot simply be read as all-`+1`.  That is the
    common case, so the default would be right most of the time and wrong exactly where it
    matters -- the `n = 29` layout, seven of whose squares are mirrored.  A silent default
    turns that into a residual nobody looks at, so a structure without the field is a
    refusal naming the fix.
    """
    signs = getattr(structure, "chirality", ()) or ()
    if len(signs) != structure.n:
        raise SystemAssemblyError(
            "chirality-missing",
            f"the structure carries {len(signs)} chirality signs for {structure.n} "
            "squares; it predates the reflected-pose model and must be re-extracted "
            "before its equations mean anything",
        )
    if any(sign not in (1, -1) for sign in signs):
        raise SystemAssemblyError(
            "chirality-malformed",
            f"chirality must be +1 or -1 per square; got {sorted(set(signs))}",
        )
    return tuple(int(sign) for sign in signs)


class _Pose(NamedTuple):
    """The symbolic pose of every square: centres, angles, and chiralities.

    Bundled rather than passed as four parallel sequences because they are only ever
    used together and only ever indexed by the same square index -- and because writing
    a corner needs all four, so any function that takes three of them is taking the
    wrong three.
    """

    xs: list
    ys: list
    ts: list
    sigmas: tuple[int, ...]


def _symbols(n: int) -> tuple[list, list, list, sp.Symbol]:
    xs = [sp.Symbol(f"x{i}", real=True) for i in range(n)]
    ys = [sp.Symbol(f"y{i}", real=True) for i in range(n)]
    ts = [sp.Symbol(f"t{i}", real=True) for i in range(n)]
    return xs, ys, ts, sp.Symbol("s", real=True, positive=True)


def _corner(index: int, corner: int, pose: _Pose):
    """Corner `corner` of square `index`, as a symbolic point.

    `pose.sigmas[index]` reflects the local x axis before the rotation, so a `-1` square
    presents its corners in the reversed order a mirrored square actually has.
    """
    offset_x, offset_y = CORNER_OFFSETS[corner]
    half = sp.Rational(1, 2)
    cosine, sine = sp.cos(pose.ts[index]), sp.sin(pose.ts[index])
    local_x, local_y = half * offset_x * pose.sigmas[index], half * offset_y
    return (
        pose.xs[index] + cosine * local_x - sine * local_y,
        pose.ys[index] + sine * local_x + cosine * local_y,
    )


def _edge_endpoints(feature: str) -> tuple[int, int]:
    edge = int(feature.split(":")[1])
    return edge, (edge + 1) % 4


def _feature_corner(feature: str) -> int:
    return int(feature.split(":")[1])


def _edge_normal(index: int, feature: str, pose: _Pose):
    """A normal of the named edge, and a point on it.

    Its orientation follows the square's chirality and is not normalised, because every
    caller only ever asks whether a point lies on the edge's line -- a zero set that a
    sign or a scale leaves alone.
    """
    first, second = _edge_endpoints(feature)
    ax, ay = _corner(index, first, pose)
    bx, by = _corner(index, second, pose)
    return (-(by - ay), bx - ax), (ax, ay)


def _pair_equations(incidence: Incidence, pose: _Pose) -> list:
    left = incidence.left
    right = int(incidence.right)
    if incidence.contact is None:
        raise SystemAssemblyError(
            "features-not-identified",
            f"incidence ({left}, {right}) does not say which features meet, so its "
            "equation is not determined; re-extract with a version that identifies them",
        )
    if incidence.contact == "corner-corner":
        px, py = _corner(left, _feature_corner(incidence.left_feature or ""), pose)
        qx, qy = _corner(right, _feature_corner(incidence.right_feature or ""), pose)
        return [sp.expand(px - qx), sp.expand(py - qy)]
    if incidence.contact == "corner-edge":
        if (incidence.left_feature or "").startswith("corner:"):
            corner_index, corner_feature = left, incidence.left_feature or ""
            edge_index, edge_feature = right, incidence.right_feature or ""
        else:
            corner_index, corner_feature = right, incidence.right_feature or ""
            edge_index, edge_feature = left, incidence.left_feature or ""
        normal, anchor = _edge_normal(edge_index, edge_feature, pose)
        px, py = _corner(corner_index, _feature_corner(corner_feature), pose)
        return [sp.expand(normal[0] * (px - anchor[0]) + normal[1] * (py - anchor[1]))]
    if incidence.contact == "edge-edge":
        # Both endpoints of the right edge on the left edge's line.  One endpoint alone
        # says the lines *meet*, not that they coincide, and leaves the right square free
        # to pivot about that point -- a motion that satisfies the equation and overlaps
        # the squares at first order.
        normal, anchor = _edge_normal(left, incidence.left_feature or "", pose)
        first, second = _edge_endpoints(incidence.right_feature or "")
        return [
            sp.expand(normal[0] * (px - anchor[0]) + normal[1] * (py - anchor[1]))
            for px, py in (_corner(right, first, pose), _corner(right, second, pose))
        ]
    raise SystemAssemblyError(
        "unknown-contact-type",
        f"incidence ({left}, {right}) is typed {incidence.contact!r}, which has no "
        "declared equation form",
    )


def _wall_equation(incidence: Incidence, pose: _Pose, side) -> list:
    wall, corner = incidence.right.split(":")
    if wall not in WALL_AXIS:
        raise SystemAssemblyError(
            "unknown-wall", f"square {incidence.left} names wall {wall!r}"
        )
    axis, at_far_side = WALL_AXIS[wall]
    point = _corner(incidence.left, int(corner), pose)[axis]
    return [sp.expand(side - point if at_far_side else point)]


def assemble(structure: ContactStructure) -> ContactSystem:
    """Turn a decided contact structure into scalar equations in the pose unknowns.

    Every square keeps its own centre and angle, and each angle class contributes
    `m - 1` identities rather than being collapsed to one symbol.  Collapsing would hide
    the identities inside the variable naming and make the equation count unfalsifiable;
    written out, they are countable and a wrong class shows up as a wrong count.
    """
    if structure.ambiguous:
        raise SystemAssemblyError(
            "ambiguous-structure",
            f"{len(structure.ambiguous)} incidences sit in the refused band; assembly "
            "needs a decided structure",
        )
    n = structure.n
    xs, ys, ts, side = _symbols(n)
    pose = _Pose(xs, ys, ts, _chirality_of(structure))

    equations: list = []
    sources: list[str] = []

    for incidence in structure.pair_contacts:
        for equation in _pair_equations(incidence, pose):
            equations.append(equation)
            sources.append(f"pair({incidence.left},{incidence.right}):{incidence.contact}")

    for incidence in structure.wall_contacts:
        for equation in _wall_equation(incidence, pose, side):
            equations.append(equation)
            sources.append(f"wall({incidence.left},{incidence.right})")

    # No angle identities are emitted, and that is a correction rather than an omission.
    # `contacts` groups squares whose orientations agree **modulo ninety degrees**,
    # because that is what an exact cross-or-dot-product test decides. `t_i - t_j` asserts
    # something strictly stronger, and it is false for any class member that is a quarter
    # or half turn from another. Measured: emitting them left the n = 11 residual at the
    # noise floor -- that packing's classes happen to have equal angles -- and drove the
    # n = 29 residual to 3.142, one whole pi, which is exactly the half-turn the identity
    # denied. The rank measurement below reaches full rank at both sizes without them.
    identities = 0

    unknowns = tuple([str(symbol) for symbol in (*xs, *ys, *ts)] + [str(side)])
    return ContactSystem(
        n=n,
        unknowns=unknowns,
        equations=tuple(sp.srepr(equation) for equation in equations),
        sources=tuple(sources),
        angle_identities=identities,
        chirality=pose.sigmas,
    )


class NullDirection(NamedTuple):
    """A direction the equations leave free, and how cleanly the measurement read it.

    The gap travels with the vector because the vector is a *measurement*: its small
    components are set to zero at the same relative tolerance that decided the rank, and
    a reader who is told the direction without being told the gap cannot tell a clean
    reading from a marginal one.  At Göbel's `n = 5` the largest component dropped is
    `1.0e-16` against a smallest kept of `1.0`, so the denoising spans sixteen decades and
    decides nothing; a narrow gap there would make the emitted condition a judgement call
    and should be treated as one.
    """

    components: tuple[float, ...]
    largest_dropped: float
    smallest_kept: float


def null_directions(
    system: ContactSystem, values: Sequence[float], *, tolerance: float = 1e-9
) -> list[NullDirection]:
    """An orthonormal basis of the directions the system's equations do not constrain.

    Individually these vectors are not claims about anything -- a null space has no
    preferred basis, which is the correction D-360 records -- but the conditions
    :func:`close` derives from them span the same space whichever basis is used, because
    a directional derivative is linear in its direction.  So the basis is an
    implementation detail of the emission and not of the system it emits.
    """
    _left, singular, right = mp.svd_r(contact_jacobian(system, values))
    ordered = [float(singular[index]) for index in range(singular.rows)]
    largest = max(ordered, default=0.0)
    rank = sum(1 for value in ordered if value > tolerance * largest)
    directions: list[NullDirection] = []
    for row in range(rank, right.rows):
        raw = [float(right[row, column]) for column in range(right.cols)]
        cut = tolerance * max(abs(value) for value in raw)
        kept = [value if abs(value) > cut else 0.0 for value in raw]
        norm = math.sqrt(sum(value * value for value in kept))
        if norm == 0:
            continue
        directions.append(
            NullDirection(
                components=tuple(value / norm for value in kept),
                largest_dropped=max(
                    (abs(value) for value in raw if abs(value) <= cut), default=0.0
                ),
                smallest_kept=min(abs(value) for value in kept if value),
            )
        )
    return directions


def _directional_derivative(row, direction: Sequence[float], symbols: Sequence):
    """`sum_j v_j * d(row)/d(u_j)`: how one equation changes along one direction."""
    return sp.expand(
        sum(
            sp.Float(component) * sp.diff(row, symbol)
            for component, symbol in zip(direction, symbols, strict=True)
            if component
        )
    )


def close(system: ContactSystem, values: Sequence[float], *, tolerance: float = 1e-9):
    """Add the conditions the contact equations leave short, by differentiating them.

    Closure is sized by the **rank** of the contact Jacobian, not by counting rows.
    Counting remains the wrong instrument: at `n = 11` there are 42 contact equations
    against 34 unknowns, and the question of whether they determine the pose is not
    answered by the surplus of eight.

    **Most of the time there is nothing to add, and believing otherwise was a bug.**
    With `edge-edge` contributing its second equation the Jacobian reaches full rank at
    `n = 11` and at `n = 29`, so both take the `already-determined` refusal -- where an
    earlier version of this function reported four and seven missing "stationarity
    conditions" that were in fact missing collinearity equations.  Göbel's `n = 5` has no
    `edge-edge` contact and is one short.

    **The condition `n = 5` needs is not a first-order optimality statement, and this
    docstring used to say it was.**  It promised "the Lagrange or Fritz-John statement
    that no admissible motion decreases the side, in determinant form".  That statement
    cannot close `n = 5`, for the plainest of reasons: it is already true there.  The one
    direction the contacts leave free is a rotation of the centre square about its own
    centre, carrying an `s` component of `1.0e-16`, and `side_leak` -- the norm of the
    projection of `e_s` onto the null space, which is exactly the quantity that assertion
    is about -- reads `1.00e-16`.  A true statement adds a dependent row and no rank.

    **What is missing is second-order.**  Stepping along the free direction violates the
    contacts at `-0.25 t^2`, identical to the four figures
    `devtools.probe_contact_system --case gobel5 --walk` prints at every step and in both
    signs, so the pose is infinitesimally flexible and second-order rigid.  The
    contact map has an isolated root there with a singular differential -- a degenerate
    root, not an unpinned optimum -- and what removes the degeneracy is the statement
    that the map is *stationary along the direction it leaves free*:

        sum_j v_j * dg_k/du_j (u) = 0,   for every equation `g_k` the system carries

    with `v` the direction :func:`null_directions` measures.  This is the deflation step
    of Leykin, Verschelde and Zhao, *Newton's method with deflation for isolated
    singularities of polynomial systems* (Theoretical Computer Science 359, 2006,
    111-122), specialised in one way that is a restriction rather than a result: their
    kernel vector is carried as unknowns under a normalisation, and here it is fixed at a
    measured value, which is only available because this kernel is one-dimensional and
    reads cleanly.  The closed system's roots are therefore a subset of the contact
    system's, containing the retained pose and non-degenerate at it -- which is what a
    Newton step and a Krawczyk certification need, and is less than a proof that the pose
    is optimal.

    **Nothing here is chosen to make the counts meet, and two things say so.**  The
    conditions are emitted for *every* equation rather than for a shortfall's worth --
    four survive at `n = 5`, where the shortfall is one -- so the emission is not sized;
    and each surviving condition turns out to be, symbolically and not merely numerically,
    the statement that the contacting corner sits at the **midpoint of the contacted
    edge**.  That is an identity of the corner-edge contact type in the unknowns, not a
    fact about Göbel's packing, and `tests/test_promote_system.py` checks it against a
    midpoint expression written independently of the derivative.

    At `n = 5` the sixteen wall equations contribute nothing, and for a reason worth
    stating: a wall equation does not mention the rotating square, so its derivative along
    that rotation is identically zero, and `0 = 0` is not a condition.  Dropping those is
    the only filtering that happens.
    """
    info = jacobian_rank(system, values, tolerance=tolerance)
    shortfall = info["shortfall"]
    if shortfall <= 0:
        raise SystemAssemblyError(
            "already-determined",
            f"the contact Jacobian already has rank {info['rank']} against "
            f"{info['unknowns']} unknowns, so the equations isolate this pose and a "
            "closure added anyway would be an invented constraint",
        )
    rows = [sp.sympify(equation) for equation in system.all_equations]
    symbols = _symbols_by_name(system, rows)
    conditions: list[str] = []
    sources: list[str] = []
    for index, direction in enumerate(null_directions(system, values, tolerance=tolerance)):
        for row, source in zip(rows, system.sources, strict=True):
            condition = _directional_derivative(row, direction.components, symbols)
            if condition == 0:
                continue
            conditions.append(sp.srepr(condition))
            sources.append(f"stationary(v{index}):{source}")

    closed = ContactSystem(
        n=system.n,
        unknowns=system.unknowns,
        equations=system.equations,
        sources=system.sources + tuple(sources),
        angle_identities=system.angle_identities,
        chirality=system.chirality,
        closure=system.closure + tuple(conditions),
    )
    after = jacobian_rank(closed, values, tolerance=tolerance)
    if after["shortfall"] > 0:
        raise SystemAssemblyError(
            "closure-does-not-close",
            f"differentiating the contact map along the {shortfall} direction(s) it "
            f"leaves free produced {len(conditions)} non-trivial condition(s), and the "
            f"rank only moved from {info['rank']} to {after['rank']} against "
            f"{after['unknowns']} unknowns; the conditions are dependent on the equations "
            "they came from, so this formulation does not close this contact graph",
        )
    return closed


def _symbols_by_name(system: ContactSystem, equations: Sequence) -> list:
    """The system's unknowns as the symbol objects its equations actually contain.

    Rebuilding them from names alone does not work: `s` carries a `positive` assumption
    the others do not, and a symbol that differs by an assumption is a different symbol
    to substitution.  Taking them from the equations keeps names and assumptions
    together, and any unknown no equation mentions falls back to a plain real symbol.
    """
    present = {
        str(symbol): symbol for equation in equations for symbol in equation.free_symbols
    }
    return [present.get(name, sp.Symbol(name, real=True)) for name in system.unknowns]


def _winding(square: Sequence) -> float:
    """Twice the signed area: positive counter-clockwise, negative for a reflection."""
    total = 0.0
    for index in range(4):
        x1, y1 = square[index]
        x2, y2 = square[(index + 1) % 4]
        total += float(x1) * float(y2) - float(x2) * float(y1)
    return total


def pose_values(system: ContactSystem, squares: Sequence, side_value: float) -> list[float]:
    """A pose in this system's unknown order, read off a corner representation.

    Centres are the mean of the four corners; the angle is recovered from the first edge,
    which under the corner model runs along `sigma * (cos t, sin t)` -- so a mirrored
    square's first edge points backwards along its own x axis and its angle is the edge
    direction turned by half a turn.  Nothing here is chosen: this inverts :func:`_corner`
    exactly, for either chirality.

    **The chirality is checked against the system, not taken from it.**  The equations
    were written with particular signs baked in, so a pose whose squares wind the other
    way is a pose of a different system, and substituting it would produce residuals that
    look like a bad structure rather than a mismatched caller.
    """
    measured = tuple(1 if _winding(square) > 0 else -1 for square in squares)
    expected = tuple(system.chirality)
    if len(expected) != len(measured):
        raise SystemAssemblyError(
            "chirality-length-mismatch",
            f"the system was assembled for {len(expected)} squares and this pose has "
            f"{len(measured)}",
        )
    disagreeing = [i for i, (a, b) in enumerate(zip(expected, measured, strict=True)) if a != b]
    if disagreeing:
        raise SystemAssemblyError(
            "chirality-mismatch",
            f"squares {disagreeing} wind the opposite way from the structure this system "
            "was assembled from, so these corners describe their mirror images rather "
            "than the poses the equations constrain",
        )

    values: list[float] = []
    values.extend(float(sum(float(x) for x, _ in square)) / 4 for square in squares)
    values.extend(float(sum(float(y) for _, y in square)) / 4 for square in squares)
    for square, sigma in zip(squares, measured, strict=True):
        (ax, ay), (bx, by) = square[0], square[1]
        direction = float(
            mp.atan2(mp.mpf(float(by) - float(ay)), mp.mpf(float(bx) - float(ax)))
        )
        values.append(direction if sigma > 0 else direction - float(mp.pi))
    values.append(float(side_value))
    return values


def contact_jacobian(system: ContactSystem, values: Sequence[float]):
    """The contact equations differentiated at a pose, as an `mpmath` matrix.

    Public because more than one caller needs it and the alternative is reaching into
    :func:`_symbols_by_name`, which couples them to how this module names things.
    :func:`jacobian_rank` summarises it; `devtools.probe_contact_system` walks its null
    space; a solver would use it directly.

    It differentiates :attr:`ContactSystem.all_equations`, so a closed system is
    differentiated *with* its closure.  Reading `equations` alone here is what made a
    closure condition unable to do anything but change a count.
    """
    equations = [sp.sympify(equation) for equation in system.all_equations]
    symbols = _symbols_by_name(system, equations)
    matrix = sp.Matrix(
        [[sp.diff(equation, symbol) for symbol in symbols] for equation in equations]
    )
    return mp.matrix(sp.lambdify(symbols, matrix, "mpmath")(*values))


def jacobian_rank(
    system: ContactSystem, values: Sequence[float], *, tolerance: float = 1e-9
) -> dict:
    """The rank of the system's Jacobian at a pose, and what it says about closure.

    On an assembled system that is the contact Jacobian.  On a closed one it is the
    Jacobian of the contacts *and* the closure, which is what makes "the closure took the
    rank to full" a measurement rather than a hope.

    This is the measurement that equation counting cannot make.  A contact system for a
    rigid packing is *redundant*: many contacts follow from others, so there are more
    equations than unknowns and the system is still not enough to pin the pose.  Counting
    rows answers neither question.  The rank does: if it equals the number of unknowns,
    the contact equations alone already isolate the configuration and no closure is
    needed; if it falls short, the shortfall is exactly how many stationarity conditions
    :func:`close` has to supply.

    Reported with the singular values around the cut, because a numerical rank is a
    judgement about a gap and hiding the gap makes it look like a fact.

    `side_leak` is the norm of the projection of the side's unit vector onto the null
    space, and it is the quantity that says whether the pose is pinned *as an optimum*.
    A direction `v` with `A v = 0` preserves every contact to first order along both `+v`
    and `-v`, so if it also changes the side then one of the two shrinks the container
    while every contact holds -- and the packing is not a strict local minimum of its own
    system. It reads zero at every retained size and is reported rather than asserted,
    because it was `1.86e-1` at `n = 11` and `1.14e-1` at `n = 29` while `edge-edge` was
    assembled as one equation, and that is how the missing one was found.
    """
    numeric = contact_jacobian(system, values)
    _left, singular, right = mp.svd_r(numeric)
    ordered = sorted((float(value) for value in singular), reverse=True)
    largest = ordered[0] if ordered else 0.0
    cut = tolerance * largest if largest > 0 else tolerance
    rank = sum(1 for value in ordered if value > cut)
    side_index = list(system.unknowns).index("s")
    leak = math.sqrt(
        sum(float(right[index, side_index]) ** 2 for index in range(rank, right.rows))
    )
    return {
        "rank": rank,
        "side_leak": leak,
        "unknowns": system.unknown_count,
        # Reported apart rather than summed: on a closed system the rank is a verdict on
        # both, and a reader who cannot see how many rows came from the closure cannot
        # tell a rank the contacts reached from one the closure carried.
        "equations": len(system.equations),
        "closure": len(system.closure),
        "shortfall": system.unknown_count - rank,
        "largest_singular_value": largest,
        "smallest_counted": ordered[rank - 1] if rank else None,
        "largest_discarded": ordered[rank] if rank < len(ordered) else None,
        "relative_cut": tolerance,
    }


def residual_at(system: ContactSystem, values: Sequence[float]) -> list[float]:
    """Every contact equation evaluated at a pose, for checking a structure numerically.

    A structure that describes the packing it was extracted from has residuals at the
    noise floor here.  One that does not -- a perturbed incidence, a mistyped feature --
    shows up as a residual that is not small, which is the cheapest available test that
    assembly wrote down the right equations.

    Closure conditions are evaluated too, on the same argument as in
    :func:`contact_jacobian`: a condition nobody evaluates cannot be wrong at the pose,
    and "the residual is unmoved" is a claim about the closed system or it is not a claim.
    """
    equations = [sp.sympify(equation) for equation in system.all_equations]
    symbols = _symbols_by_name(system, equations)
    substitution = dict(zip(symbols, values, strict=True))
    return [float(sp.Float(equation.subs(substitution))) for equation in equations]
