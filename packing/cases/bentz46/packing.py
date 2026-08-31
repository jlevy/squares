"""Bentz 2010, Theorem 8: the 45-point unavoidable set proving `s(46) = 7`.

Source: `resources/papers/bentz-2010-optimal-packings-13-and-46.md`, Section 2, with
the raw extraction as ground truth. Figure 1 is not extractable from the PDF, but the
prose determines the construction completely: the lowest row of points is
`(i, sqrt(2) - 1/2)` for `i = 1..6`, and the rows above are arranged so that all
shown triangles are equilateral of side one -- so row `k` sits at
`y_k = sqrt(2) - 1/2 + k sqrt(3)/2` for `k = 0..6`, with rows alternating six points
at integer `x` and seven points at half-integer `x`. The paper's own check that the
top row is within `sqrt(2) - 1/2` of the upper edge is replayed exactly here.

Everything decisive lives in `Q(sqrt 2, sqrt 3)`, realized as `Q(alpha)` for
`alpha = sqrt(2) + sqrt(3)` with minimal polynomial `x^4 - 10x^2 + 1`; the radicals
are recovered inside the field and verified by squaring, the `printed_cover` pattern.

The cell complex tiles `[0, 7]^2` with 92 faces: 7 bottom and 7 top wall rectangles
(Lemma 4 with the wall as its axis), 66 unit equilateral triangles in the six
inter-row strips (Lemma 2), and 12 edge quadrilaterals (Lemma 5 at `a = sqrt(3)/2`,
`b = 1/2`), one per strip per side. `verify_cover` certifies the tiling and every
cell's lemma premises exactly; face tuples here are oriented counterclockwise
programmatically so the tiling validator sees one orientation.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from sqpack.cover import Face, Point, Scalar, checked_number_field, polygon_area2
from sqpack.field import FieldElement, NumberField


@dataclass(frozen=True)
class CellPlan:
    """One cell of the cover: its oriented face and the lemma its certificate checks."""

    face: Face
    kind: str
    wall: str | None = None
    outs: tuple[str, ...] = ()
    width: Scalar | None = None
    height: Scalar | None = None
    far: str | None = None
    near: str | None = None


ROW_COUNT = 7
SIDE = 7
EXPECTED_POINTS = 45
EXPECTED_FACES = 7 + 7 + 66 + 12

#: alpha = sqrt(2) + sqrt(3): x^4 - 10x^2 + 1, the biquadratic compositum.
MIN_POLY = (1, 0, -10, 0, 1)
ISOLATING = (Fraction(31, 10), Fraction(32, 10))


def build() -> tuple[
    NumberField,
    FieldElement,
    FieldElement,
    dict[str, Point],
    dict[str, Point],
    dict[str, CellPlan],
]:
    """Return (field, sqrt2, sqrt3, set_points, all_vertices, cell_plan).

    ``set_points`` are the 45 unavoidable points; ``all_vertices`` additionally
    carries the container corners and wall anchor vertices the tiling needs.
    ``cell_plan`` maps each cell name to its counterclockwise face tuple, its lemma
    kind, and the data its certificate checks.
    """
    field, _checks = checked_number_field(MIN_POLY, ISOLATING)
    rational = field.rational
    alpha = field.alpha
    sqrt2 = (alpha**3 - rational(9) * alpha) / 2
    sqrt3 = (rational(11) * alpha - alpha**3) / 2
    if not (sqrt2 * sqrt2 - rational(2)).is_zero():
        raise ValueError("sqrt(2) reconstruction failed")
    if not (sqrt3 * sqrt3 - rational(3)).is_zero():
        raise ValueError("sqrt(3) reconstruction failed")
    if sqrt2.sign() <= 0 or sqrt3.sign() <= 0:
        raise ValueError("a radical reconstruction chose a negative conjugate")

    side = rational(SIDE)
    y0 = sqrt2 - rational(Fraction(1, 2))
    dy = sqrt3 / 2
    row_y = [y0 + rational(k) * dy for k in range(ROW_COUNT)]
    top = row_y[-1]
    if (side - top - y0).sign() >= 0:
        raise ValueError("top row is not within sqrt(2) - 1/2 of the upper edge")

    def row_xs(row: int) -> list[FieldElement]:
        if row % 2 == 0:
            return [rational(i) for i in range(1, 7)]
        return [rational(Fraction(2 * i + 1, 2)) for i in range(7)]

    set_points: dict[str, Point] = {}
    for row in range(ROW_COUNT):
        for index, x in enumerate(row_xs(row)):
            set_points[f"p{row}_{index}"] = (x, row_y[row])
    if len(set_points) != EXPECTED_POINTS:
        raise ValueError(f"expected {EXPECTED_POINTS} points, built {len(set_points)}")

    vertices: dict[str, Point] = dict(set_points)
    zero = rational(0)
    vertices["c_bl"] = (zero, zero)
    vertices["c_br"] = (side, zero)
    vertices["c_tl"] = (zero, side)
    vertices["c_tr"] = (side, side)
    for j in range(1, 7):
        vertices[f"b{j}"] = (rational(j), zero)
        vertices[f"t{j}"] = (rational(j), side)
    for row in range(ROW_COUNT):
        vertices[f"wl{row}"] = (zero, row_y[row])
        vertices[f"wr{row}"] = (side, row_y[row])

    def bottom_name(j: int) -> str:
        return "c_bl" if j == 0 else ("c_br" if j == 7 else f"b{j}")

    def top_name(j: int) -> str:
        return "c_tl" if j == 0 else ("c_tr" if j == 7 else f"t{j}")

    def row0_name(j: int) -> str:
        return "wl0" if j == 0 else ("wr0" if j == 7 else f"p0_{j - 1}")

    def row6_name(j: int) -> str:
        return "wl6" if j == 0 else ("wr6" if j == 7 else f"p6_{j - 1}")

    plan: dict[str, CellPlan] = {}

    def oriented(face: Face) -> Face:
        area2 = polygon_area2(tuple(vertices[name] for name in face))
        if area2.sign() == 0:
            raise ValueError(f"degenerate face: {face}")
        return face if area2.sign() > 0 else tuple(reversed(face))

    def add(name: str, face: Face, kind: str, **data: object) -> None:
        plan[name] = CellPlan(face=oriented(face), kind=kind, **data)  # type: ignore[arg-type]

    # Bottom and top wall rectangles: Lemma 4 with the wall as the axis.
    for j in range(7):
        add(
            f"bottom_{j}",
            (bottom_name(j), bottom_name(j + 1), row0_name(j + 1), row0_name(j)),
            "lemma4",
            wall="bottom",
            outs=(row0_name(j), row0_name(j + 1)),
            width=rational(1),
            height=y0,
        )
        add(
            f"top_{j}",
            (top_name(j), row6_name(j), row6_name(j + 1), top_name(j + 1)),
            "lemma4",
            wall="top",
            outs=(row6_name(j), row6_name(j + 1)),
            width=rational(1),
            height=side - top,
        )

    # Inter-row strips: 11 unit equilateral triangles plus two Lemma 5 edge quads.
    for row in range(ROW_COUNT - 1):
        low_even = row % 2 == 0
        low = [f"p{row}_{i}" for i in range(len(row_xs(row)))]
        high = [f"p{row + 1}_{i}" for i in range(len(row_xs(row + 1)))]
        wide, narrow = (high, low) if low_even else (low, high)
        # ``wide`` holds seven half-integer points, ``narrow`` six integer points.
        for i in range(6):
            add(f"tri_{row}_{i}_w", (narrow[i], wide[i], wide[i + 1]), "lemma2")
        for i in range(5):
            add(f"tri_{row}_{i}_n", (wide[i + 1], narrow[i], narrow[i + 1]), "lemma2")
        left_far, left_near = (low[0], high[0]) if low_even else (high[0], low[0])
        add(
            f"quadL_{row}",
            (f"wl{row}", left_far, left_near, f"wl{row + 1}")
            if low_even
            else (f"wl{row}", left_near, left_far, f"wl{row + 1}"),
            "lemma5",
            wall="left",
            far=left_far,
            near=left_near,
        )
        right_far, right_near = (low[-1], high[-1]) if low_even else (high[-1], low[-1])
        add(
            f"quadR_{row}",
            (f"wr{row}", right_far, right_near, f"wr{row + 1}")
            if low_even
            else (f"wr{row}", right_near, right_far, f"wr{row + 1}"),
            "lemma5",
            wall="right",
            far=right_far,
            near=right_near,
        )

    if len(plan) != EXPECTED_FACES:
        raise ValueError(f"expected {EXPECTED_FACES} faces, built {len(plan)}")
    return field, sqrt2, sqrt3, set_points, vertices, plan
