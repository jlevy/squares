"""A sixteen-point unavoidable set at side 17/4, toward Green's `s(17)` bound.

DS7 records Green's Theorem 9 -- `s(17) >= (40 sqrt 2 + 19)/17`, about 4.4452 --
with Figure 34 unextractable and no primary source, so a certified set of our own
is the only route by which the verified lower lane can move at `n = 17` or
`n = 18`. This module carries one: sixteen points in `[0, 17/4]^2` such that every
box (open square of side above one) contains at least one. Any packing of 17 unit
squares in a side below 17/4 would scale to 17 disjoint boxes here, so
`s(17) >= 17/4 = 4.25` -- above Nagamochi's closed form (about 4.1623), below
Green's unadoptable value.

The construction is a rationalized Bentz grid pushed to its exact limit:

- four rows at `y = 457/500 + k * 433/500` (the row spacing `433/500` is just
  under `sqrt(3)/2`, so the mesh diagonals have squared length `249989/250000`);
- integer rows carry `x = 1, 2, 3, 7/2`; half rows carry `x = 1/2, 3/2, 5/2, 7/2`
  -- the appended `x = 7/2` column is what lets the right edge open to
  `17/4 - 7/2 = 3/4` of wall clearance;
- bottom and top Lemma 4 wall strips (ends anchored by wall vertices, which an
  open box inside the container cannot contain);
- three left-wall Lemma 5 quadrilaterals at `a = 433/500`, `b = 1/2` -- the same
  parameter family as the Theorem 8 certificate;
- a right margin band of width exactly `1/2` (no box centre can lie there), and
  four near-slabs anchored on the `x = 7/2` column whose worst corners sit at
  squared distance `249989/1000000 <= 1/4`;
- eighteen Lemma 2 triangles.

The side is exact: at `t = 17/4` the near-slab corner bound `(t - 4)^2 +
(433/1000)^2 <= 1/4` holds with slack `11/1000000`, and it fails for any larger
rational side with this structure. Held unresolved with needs_review per the
run's unattended rules; adoption into the frontier is a reviewed evidence-contract
change.
"""

from __future__ import annotations

from fractions import Fraction

from cases.bentz13.packing import CellPlan, Face, Point, Rat
from sqpack.cover import polygon_area2

EXPECTED_POINTS = 16
SIDE = Fraction(17, 4)

Y0 = Fraction(457, 500)
DY = Fraction(433, 500)
HALF_DY = Fraction(433, 1000)
ROWS = (Y0, Y0 + DY, Y0 + 2 * DY, Y0 + 3 * DY)
CUTS = (ROWS[0] + HALF_DY, ROWS[1] + HALF_DY, ROWS[2] + HALF_DY)
MARGIN_X = SIDE - Fraction(1, 2)

INTEGER_XS = (Fraction(1), Fraction(2), Fraction(3), Fraction(7, 2))
HALF_XS = (Fraction(1, 2), Fraction(3, 2), Fraction(5, 2), Fraction(7, 2))


def build() -> tuple[dict[str, Point], dict[str, Point], dict[str, CellPlan], Face]:
    """Return (set_points, vertices, plan, boundary) for the 17/4 configuration."""

    def pt(x: Fraction, y: Fraction) -> Point:
        return (Rat.of(x), Rat.of(y))

    set_points: dict[str, Point] = {}
    for row, y in enumerate(ROWS):
        xs = INTEGER_XS if row % 2 == 0 else HALF_XS
        for index, x in enumerate(xs):
            set_points[f"p{row}_{index}"] = pt(x, y)
    if len(set_points) != EXPECTED_POINTS:
        raise ValueError(f"expected {EXPECTED_POINTS} points, built {len(set_points)}")

    vertices: dict[str, Point] = dict(set_points)
    aux = {
        "w00": (Fraction(0), Fraction(0)),
        "w10": (Fraction(1), Fraction(0)),
        "w20": (Fraction(2), Fraction(0)),
        "w30": (Fraction(3), Fraction(0)),
        "w35": (Fraction(7, 2), Fraction(0)),
        "w40": (SIDE, Fraction(0)),
        "e_r0": (SIDE, ROWS[0]),
        "e_r3": (SIDE, ROWS[3]),
        "w44": (SIDE, SIDE),
        "t35": (Fraction(7, 2), SIDE),
        "t25": (Fraction(5, 2), SIDE),
        "t15": (Fraction(3, 2), SIDE),
        "t05": (Fraction(1, 2), SIDE),
        "w04": (Fraction(0), SIDE),
        "l_r3": (Fraction(0), ROWS[3]),
        "l_r2": (Fraction(0), ROWS[2]),
        "l_r1": (Fraction(0), ROWS[1]),
        "l_r0": (Fraction(0), ROWS[0]),
        "m_r0": (MARGIN_X, ROWS[0]),
        "m_r3": (MARGIN_X, ROWS[3]),
        "m_c0": (MARGIN_X, CUTS[0]),
        "m_c1": (MARGIN_X, CUTS[1]),
        "m_c2": (MARGIN_X, CUTS[2]),
        "s_c0": (Fraction(7, 2), CUTS[0]),
        "s_c1": (Fraction(7, 2), CUTS[1]),
        "s_c2": (Fraction(7, 2), CUTS[2]),
    }
    for name, (x, y) in aux.items():
        vertices[name] = pt(x, y)

    plan: dict[str, CellPlan] = {}

    def oriented(face: Face) -> Face:
        area2 = polygon_area2(tuple(vertices[name] for name in face))
        if area2.sign() == 0:
            raise ValueError(f"degenerate face: {face}")
        return face if area2.sign() > 0 else tuple(reversed(face))

    def add(name: str, face: Face, kind: str, **data: object) -> None:
        plan[name] = CellPlan(face=oriented(face), kind=kind, **data)  # type: ignore[arg-type]

    zero = Fraction(0)
    # Bottom wall strip: five Lemma 4 rectangles; the outer ends anchor on wall
    # vertices, uncontainable for an open box inside the container.
    r0 = ("p0_0", "p0_1", "p0_2", "p0_3")
    add(
        "rb0",
        ("w00", "w10", r0[0], "l_r0"),
        "lemma4",
        wall="bottom",
        outs=("l_r0", r0[0]),
        rect=(zero, Fraction(1), zero, ROWS[0]),
    )
    add(
        "rb1",
        ("w10", "w20", r0[1], r0[0]),
        "lemma4",
        wall="bottom",
        outs=(r0[0], r0[1]),
        rect=(Fraction(1), Fraction(2), zero, ROWS[0]),
    )
    add(
        "rb2",
        ("w20", "w30", r0[2], r0[1]),
        "lemma4",
        wall="bottom",
        outs=(r0[1], r0[2]),
        rect=(Fraction(2), Fraction(3), zero, ROWS[0]),
    )
    add(
        "rb3",
        ("w30", "w35", r0[3], r0[2]),
        "lemma4",
        wall="bottom",
        outs=(r0[2], r0[3]),
        rect=(Fraction(3), Fraction(7, 2), zero, ROWS[0]),
    )
    add(
        "rb4",
        ("w35", "w40", "e_r0", "m_r0", r0[3]),
        "lemma4",
        wall="bottom",
        outs=(r0[3], "e_r0"),
        rect=(Fraction(7, 2), SIDE, zero, ROWS[0]),
    )

    # Top wall strip: five Lemma 4 rectangles likewise.
    r3 = ("p3_0", "p3_1", "p3_2", "p3_3")
    add(
        "rt0",
        ("l_r3", r3[0], "t05", "w04"),
        "lemma4",
        wall="top",
        outs=("l_r3", r3[0]),
        rect=(zero, Fraction(1, 2), ROWS[3], SIDE),
    )
    add(
        "rt1",
        (r3[0], r3[1], "t15", "t05"),
        "lemma4",
        wall="top",
        outs=(r3[0], r3[1]),
        rect=(Fraction(1, 2), Fraction(3, 2), ROWS[3], SIDE),
    )
    add(
        "rt2",
        (r3[1], r3[2], "t25", "t15"),
        "lemma4",
        wall="top",
        outs=(r3[1], r3[2]),
        rect=(Fraction(3, 2), Fraction(5, 2), ROWS[3], SIDE),
    )
    add(
        "rt3",
        (r3[2], r3[3], "t35", "t25"),
        "lemma4",
        wall="top",
        outs=(r3[2], r3[3]),
        rect=(Fraction(5, 2), Fraction(7, 2), ROWS[3], SIDE),
    )
    add(
        "rt4",
        (r3[3], "m_r3", "e_r3", "w44", "t35"),
        "lemma4",
        wall="top",
        outs=(r3[3], "e_r3"),
        rect=(Fraction(7, 2), SIDE, ROWS[3], SIDE),
    )

    # Left wall: three Lemma 5 quadrilaterals at (a, b) = (433/500, 1/2).
    add(
        "ql0",
        ("l_r0", "l_r1", "p1_0", "p0_0"),
        "lemma5",
        wall="left",
        outs=("p0_0", "p1_0"),
        quad=(ROWS[0], DY, Fraction(1, 2)),
        direction=1,
    )
    add(
        "ql1",
        ("l_r2", "l_r1", "p1_0", "p2_0"),
        "lemma5",
        wall="left",
        outs=("p2_0", "p1_0"),
        quad=(ROWS[2], DY, Fraction(1, 2)),
        direction=-1,
    )
    add(
        "ql2",
        ("l_r2", "l_r3", "p3_0", "p2_0"),
        "lemma5",
        wall="left",
        outs=("p2_0", "p3_0"),
        quad=(ROWS[2], DY, Fraction(1, 2)),
        direction=1,
    )

    # Right margin band (width exactly 1/2) and the four near-slabs.
    add(
        "margin_r",
        ("m_r0", "e_r0", "e_r3", "m_r3", "m_c2", "m_c1", "m_c0"),
        "margin",
        wall="right",
    )
    add("s0", ("p0_3", "m_r0", "m_c0", "s_c0"), "near", outs=("p0_3",))
    add("s1", ("s_c0", "m_c0", "m_c1", "s_c1", "p1_3"), "near", outs=("p1_3",))
    add("s2", ("s_c1", "m_c1", "m_c2", "s_c2", "p2_3"), "near", outs=("p2_3",))
    add("s3", ("s_c2", "m_c2", "m_r3", "p3_3"), "near", outs=("p3_3",))

    # The eighteen Lemma 2 triangles; the right-column ones carry collinear cut
    # vertices so every edge pairs with a slab edge.
    triangles: tuple[tuple[str, Face, tuple[str, str, str] | None], ...] = (
        ("t01", ("p0_0", "p1_0", "p1_1"), None),
        ("t02", ("p0_0", "p0_1", "p1_1"), None),
        ("t03", ("p0_1", "p1_1", "p1_2"), None),
        ("t04", ("p0_1", "p0_2", "p1_2"), None),
        ("t05x", ("p0_2", "p1_2", "p1_3"), None),
        ("t06", ("p0_2", "p0_3", "s_c0", "p1_3"), ("p0_2", "p0_3", "p1_3")),
        ("t11", ("p1_0", "p2_0", "p1_1"), None),
        ("t12", ("p2_0", "p2_1", "p1_1"), None),
        ("t13", ("p1_1", "p2_1", "p1_2"), None),
        ("t14", ("p2_1", "p2_2", "p1_2"), None),
        ("t15x", ("p1_2", "p2_2", "p1_3"), None),
        ("t16", ("p1_3", "s_c1", "p2_3", "p2_2"), ("p1_3", "p2_3", "p2_2")),
        ("t21", ("p2_0", "p3_0", "p3_1"), None),
        ("t22", ("p2_0", "p2_1", "p3_1"), None),
        ("t23", ("p2_1", "p3_1", "p3_2"), None),
        ("t24", ("p2_1", "p2_2", "p3_2"), None),
        ("t25x", ("p2_2", "p3_2", "p3_3"), None),
        ("t26", ("p2_2", "p2_3", "s_c2", "p3_3"), ("p2_2", "p2_3", "p3_3")),
    )
    for name, face, corners in triangles:
        add(name, face, "lemma2", corners=corners)

    boundary: Face = (
        "w00",
        "w10",
        "w20",
        "w30",
        "w35",
        "w40",
        "e_r0",
        "e_r3",
        "w44",
        "t35",
        "t25",
        "t15",
        "t05",
        "w04",
        "l_r3",
        "l_r2",
        "l_r1",
        "l_r0",
    )
    return set_points, vertices, plan, boundary
