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
| `edge-edge` | the two edge lines coincide | 1 |
| `corner-corner` | the two corners are the same point | 2 |
| `corner-wall` | the corner's coordinate meets the wall | 1 |

A corner-edge contact also leaves the corner free to slide along the edge, which is a
*degree of freedom*, not an equation; an edge-edge contact leaves an overlap interval in
the same way.  Both are inequalities the packing satisfies and neither pins anything, so
neither appears here.  Folding the four rows above into "one equation per contact" is the
mistake this table exists to prevent: it would silently drop the second corner-corner
equation and produce a system that is square by accident.

**Why the raw system is not square, and what closes it.**  The unknowns are each
square's centre and angle plus the side: `3n + 1` of them.  Contacts alone do not
determine a *locally optimal* packing -- they describe the combinatorics of one, and a
continuum of nearby configurations shares them.  What singles out the optimum is that
the side cannot be decreased, which is a Lagrange or Fritz-John condition in determinant
form. :func:`close` adds it.

Assembly is deliberately literal.  It writes down what the structure says and reports
what that leaves, including when what it leaves is underdetermined.  It never invents a
constraint to make the counts meet.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import mpmath as mp
import sympy as sp

from sqpack.promote.contacts import ContactStructure, Incidence

#: How many scalar equations each contact type contributes.
EQUATIONS_PER_CONTACT = {
    "corner-edge": 1,
    "edge-edge": 1,
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
    sources: tuple[str, ...]
    angle_identities: int
    closure: tuple[str, ...] = ()

    @property
    def equation_count(self) -> int:
        return len(self.equations) + len(self.closure)

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


def _symbols(n: int) -> tuple[list, list, list, sp.Symbol]:
    xs = [sp.Symbol(f"x{i}", real=True) for i in range(n)]
    ys = [sp.Symbol(f"y{i}", real=True) for i in range(n)]
    ts = [sp.Symbol(f"t{i}", real=True) for i in range(n)]
    return xs, ys, ts, sp.Symbol("s", real=True, positive=True)


def _corner(index: int, corner: int, xs, ys, ts):
    """Corner `corner` of square `index`, as a symbolic point."""
    offset_x, offset_y = CORNER_OFFSETS[corner]
    half = sp.Rational(1, 2)
    cosine, sine = sp.cos(ts[index]), sp.sin(ts[index])
    local_x, local_y = half * offset_x, half * offset_y
    return (
        xs[index] + cosine * local_x - sine * local_y,
        ys[index] + sine * local_x + cosine * local_y,
    )


def _edge_endpoints(feature: str) -> tuple[int, int]:
    edge = int(feature.split(":")[1])
    return edge, (edge + 1) % 4


def _feature_corner(feature: str) -> int:
    return int(feature.split(":")[1])


def _edge_normal(index: int, feature: str, xs, ys, ts):
    """An outward normal of the named edge, and a point on it."""
    first, second = _edge_endpoints(feature)
    ax, ay = _corner(index, first, xs, ys, ts)
    bx, by = _corner(index, second, xs, ys, ts)
    return (-(by - ay), bx - ax), (ax, ay)


def _pair_equations(incidence: Incidence, xs, ys, ts) -> list:
    left = incidence.left
    right = int(incidence.right)
    if incidence.contact is None:
        raise SystemAssemblyError(
            "features-not-identified",
            f"incidence ({left}, {right}) does not say which features meet, so its "
            "equation is not determined; re-extract with a version that identifies them",
        )
    if incidence.contact == "corner-corner":
        px, py = _corner(left, _feature_corner(incidence.left_feature or ""), xs, ys, ts)
        qx, qy = _corner(right, _feature_corner(incidence.right_feature or ""), xs, ys, ts)
        return [sp.expand(px - qx), sp.expand(py - qy)]
    if incidence.contact == "corner-edge":
        if (incidence.left_feature or "").startswith("corner:"):
            corner_index, corner_feature = left, incidence.left_feature or ""
            edge_index, edge_feature = right, incidence.right_feature or ""
        else:
            corner_index, corner_feature = right, incidence.right_feature or ""
            edge_index, edge_feature = left, incidence.left_feature or ""
        normal, anchor = _edge_normal(edge_index, edge_feature, xs, ys, ts)
        px, py = _corner(corner_index, _feature_corner(corner_feature), xs, ys, ts)
        return [sp.expand(normal[0] * (px - anchor[0]) + normal[1] * (py - anchor[1]))]
    if incidence.contact == "edge-edge":
        normal, anchor = _edge_normal(left, incidence.left_feature or "", xs, ys, ts)
        other_first, _ = _edge_endpoints(incidence.right_feature or "")
        qx, qy = _corner(right, other_first, xs, ys, ts)
        return [sp.expand(normal[0] * (qx - anchor[0]) + normal[1] * (qy - anchor[1]))]
    raise SystemAssemblyError(
        "unknown-contact-type",
        f"incidence ({left}, {right}) is typed {incidence.contact!r}, which has no "
        "declared equation form",
    )


def _wall_equation(incidence: Incidence, xs, ys, ts, side) -> list:
    wall, corner = incidence.right.split(":")
    if wall not in WALL_AXIS:
        raise SystemAssemblyError(
            "unknown-wall", f"square {incidence.left} names wall {wall!r}"
        )
    axis, at_far_side = WALL_AXIS[wall]
    point = _corner(incidence.left, int(corner), xs, ys, ts)[axis]
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

    equations: list = []
    sources: list[str] = []

    for incidence in structure.pair_contacts:
        for equation in _pair_equations(incidence, xs, ys, ts):
            equations.append(equation)
            sources.append(f"pair({incidence.left},{incidence.right}):{incidence.contact}")

    for incidence in structure.wall_contacts:
        for equation in _wall_equation(incidence, xs, ys, ts, side):
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
    )


def close(system: ContactSystem, values: Sequence[float], *, tolerance: float = 1e-9):
    """Add the stationarity conditions the contact equations leave short.

    Closure is sized by the **rank** of the contact Jacobian, not by counting rows.
    Counting is the wrong instrument here and measurably so: at `n = 11` there are 35
    contact equations against 34 unknowns, which reads as overdetermined, while the
    Jacobian has rank 30 -- so the equations are redundant *and* four conditions short at
    the same time. A closure sized by the count would have added none.

    What the four are is the next step and is not derived here.  They are the Lagrange
    or Fritz-John conditions saying no admissible motion decreases the side, in
    determinant form; this reports how many are needed and refuses to invent them.
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
    conditions = tuple(
        f"stationarity condition {index + 1} of {shortfall}: a rank-deficiency "
        "determinant on the bordered Jacobian of the contact equations"
        for index in range(shortfall)
    )
    return ContactSystem(
        n=system.n,
        unknowns=system.unknowns,
        equations=system.equations,
        sources=system.sources,
        angle_identities=system.angle_identities,
        closure=conditions,
    )


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

    Centres are the mean of the four corners and the angle comes from the first edge, so
    this inverts :func:`_corner` rather than trusting a caller to order anything.

    **Reflected squares are refused, not silently mis-posed.**  The corner model here is
    a centre plus a *rotation*, which cannot produce a clockwise winding; a square whose
    corners run the other way is a different square from the one this pose describes.
    That is not hypothetical: the `n = 29` source builds seven of its twenty-nine squares
    inside `scale(-1 1)` mirror groups, and reading them as rotations left the assembled
    residual at 2.0 instead of the noise floor.  Fixing it properly means either
    re-indexing the contact features to match a re-wound square or giving the pose a
    chirality of its own, and both change what a feature name means -- so this refuses and
    names them rather than choosing one in passing.
    """
    reflected = [index for index, square in enumerate(squares) if _winding(square) <= 0]
    if reflected:
        raise SystemAssemblyError(
            "reflected-squares",
            f"squares {reflected} have clockwise corner winding, which a centre-plus-"
            "rotation pose cannot represent; assembly would describe their mirror images",
        )
    values: list[float] = []
    values.extend(float(sum(float(x) for x, _ in square)) / 4 for square in squares)
    values.extend(float(sum(float(y) for _, y in square)) / 4 for square in squares)
    for square in squares:
        (ax, ay), (bx, by) = square[0], square[1]
        values.append(
            float(mp.atan2(mp.mpf(float(by) - float(ay)), mp.mpf(float(bx) - float(ax))))
        )
    values.append(float(side_value))
    return values


def jacobian_rank(
    system: ContactSystem, values: Sequence[float], *, tolerance: float = 1e-9
) -> dict:
    """The rank of the contact Jacobian at a pose, and what it says about closure.

    This is the measurement that equation counting cannot make.  A contact system for a
    rigid packing is *redundant*: many contacts follow from others, so there are more
    equations than unknowns and the system is still not enough to pin the pose.  Counting
    rows answers neither question.  The rank does: if it equals the number of unknowns,
    the contact equations alone already isolate the configuration and no closure is
    needed; if it falls short, the shortfall is exactly how many stationarity conditions
    :func:`close` has to supply.

    Reported with the singular values around the cut, because a numerical rank is a
    judgement about a gap and hiding the gap makes it look like a fact.
    """
    equations = [sp.sympify(equation) for equation in system.equations]
    symbols = _symbols_by_name(system, equations)
    matrix = sp.Matrix(
        [[sp.diff(equation, symbol) for symbol in symbols] for equation in equations]
    )
    evaluate = sp.lambdify(symbols, matrix, "mpmath")
    numeric = mp.matrix(evaluate(*values))
    singular = mp.svd_r(numeric, compute_uv=False)
    ordered = sorted((float(value) for value in singular), reverse=True)
    largest = ordered[0] if ordered else 0.0
    cut = tolerance * largest if largest > 0 else tolerance
    rank = sum(1 for value in ordered if value > cut)
    return {
        "rank": rank,
        "unknowns": system.unknown_count,
        "equations": len(system.equations),
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
    """
    equations = [sp.sympify(equation) for equation in system.equations]
    symbols = _symbols_by_name(system, equations)
    substitution = dict(zip(symbols, values, strict=True))
    return [float(sp.Float(equation.subs(substitution))) for equation in equations]
