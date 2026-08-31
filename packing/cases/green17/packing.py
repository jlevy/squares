"""A sixteen-point unavoidable set at side 4426213/10^6, toward Green's `s(17)`.

DS7 records Green's Theorem 9 -- `s(17) >= (40 sqrt 2 + 19)/17`, about 4.4452 --
with Figure 34 unextractable and no primary source, so a certified set of our own
is the only route by which the verified lower lane can move at `n = 17` or
`n = 18`. This module carries one: sixteen points in `[0, t]^2` at
`t = 4426213/1000000` such that every box (open square of side above one)
contains at least one. Any packing of 17 unit squares in a side below `t` would
scale to 17 disjoint boxes here, so `s(17) >= 4.426213` -- above Nagamochi's
closed form (about 4.1623), a hair below Green's reported value.

The construction is a rationalized Bentz grid:

- four rows at `y = 457/500 + k * 433/500` (the row spacing `433/500` is just
  under `sqrt(3)/2`, so the mesh diagonals have squared length `249989/250000`);
- integer rows carry `x = 1, 2, 3, 7/2`; half rows carry `x = 1/2, 3/2, 5/2, 7/2`;
- bottom and top Lemma 4 wall strips (ends anchored by wall vertices, which an
  open box inside the container cannot contain);
- three left-wall Lemma 5 quadrilaterals at `a = 433/500`, `b = 1/2` -- the same
  parameter family as the Theorem 8 certificate;
- three right-wall Lemma 4 rectangles of depth `t - 7/2` whose inner corners are
  the `x = 7/2` column points;
- eighteen Lemma 2 triangles.

**The side is within `6 * 10^-7` of this set's exact ceiling.** The binding
constraint is the top wall strips' Lemma 4 hypothesis `a + 2b <= 2 sqrt 2` with
`a = 1` and `b = t - 439/125`, which holds exactly up to
`t* = 753/250 + sqrt 2 = 4.42621356...`; the first run of this construction
(2026-08-31, session-057) took the near-slab variant to `t = 17/4`, and the
independent interval audit (`cases/green17/interval_audit.py`) then showed the
set itself keeps working far past it -- certifying `t = 4426213/10^6` and
refuting `t = 4427/1000` with an exact escaping pose at `theta` near `pi/4`
between two unit-spaced strip points, exactly Lemma 4's tight case. Certifying
at `t*` itself needs `Q(sqrt 2)` arithmetic and is a typed follow-on; every
rational side at or below this module's `SIDE` inherits the certificate by
containment.
"""

from __future__ import annotations

from fractions import Fraction

from cases.bentz13.packing import CellPlan, Face, Point, Rat
from sqpack.cover import polygon_area2

EXPECTED_POINTS = 16
SIDE = Fraction(4_426_213, 1_000_000)

Y0 = Fraction(457, 500)
DY = Fraction(433, 500)
ROWS = (Y0, Y0 + DY, Y0 + 2 * DY, Y0 + 3 * DY)

INTEGER_XS = (Fraction(1), Fraction(2), Fraction(3), Fraction(7, 2))
HALF_XS = (Fraction(1, 2), Fraction(3, 2), Fraction(5, 2), Fraction(7, 2))


def build(
    side: Fraction = SIDE,
) -> tuple[dict[str, Point], dict[str, Point], dict[str, CellPlan], Face]:
    """Return (set_points, vertices, plan, boundary) for the configuration.

    `side` exists for the refusal controls: the plan is rebuilt against the
    given container side, so a side past the Lemma 4 ceiling must be refused
    by the certifier, not silently accepted.
    """

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
        "w40": (side, Fraction(0)),
        "e_r0": (side, ROWS[0]),
        "e_r1": (side, ROWS[1]),
        "e_r2": (side, ROWS[2]),
        "e_r3": (side, ROWS[3]),
        "w44": (side, side),
        "t35": (Fraction(7, 2), side),
        "t25": (Fraction(5, 2), side),
        "t15": (Fraction(3, 2), side),
        "t05": (Fraction(1, 2), side),
        "w04": (Fraction(0), side),
        "l_r3": (Fraction(0), ROWS[3]),
        "l_r2": (Fraction(0), ROWS[2]),
        "l_r1": (Fraction(0), ROWS[1]),
        "l_r0": (Fraction(0), ROWS[0]),
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
        ("w35", "w40", "e_r0", r0[3]),
        "lemma4",
        wall="bottom",
        outs=(r0[3], "e_r0"),
        rect=(Fraction(7, 2), side, zero, ROWS[0]),
    )

    # Top wall strip: five Lemma 4 rectangles likewise.
    r3 = ("p3_0", "p3_1", "p3_2", "p3_3")
    add(
        "rt0",
        ("l_r3", r3[0], "t05", "w04"),
        "lemma4",
        wall="top",
        outs=("l_r3", r3[0]),
        rect=(zero, Fraction(1, 2), ROWS[3], side),
    )
    add(
        "rt1",
        (r3[0], r3[1], "t15", "t05"),
        "lemma4",
        wall="top",
        outs=(r3[0], r3[1]),
        rect=(Fraction(1, 2), Fraction(3, 2), ROWS[3], side),
    )
    add(
        "rt2",
        (r3[1], r3[2], "t25", "t15"),
        "lemma4",
        wall="top",
        outs=(r3[1], r3[2]),
        rect=(Fraction(3, 2), Fraction(5, 2), ROWS[3], side),
    )
    add(
        "rt3",
        (r3[2], r3[3], "t35", "t25"),
        "lemma4",
        wall="top",
        outs=(r3[2], r3[3]),
        rect=(Fraction(5, 2), Fraction(7, 2), ROWS[3], side),
    )
    add(
        "rt4",
        (r3[3], "e_r3", "w44", "t35"),
        "lemma4",
        wall="top",
        outs=(r3[3], "e_r3"),
        rect=(Fraction(7, 2), side, ROWS[3], side),
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

    # Right wall: three Lemma 4 rectangles of depth `side - 7/2`, their inner
    # corners the x = 7/2 column points. This band is what the first run's
    # margin-and-near-slab variant capped at 17/4; Lemma 4 carries it to the
    # top-strip ceiling.
    add(
        "qr0",
        ("p0_3", "e_r0", "e_r1", "p1_3"),
        "lemma4",
        wall="right",
        outs=("p0_3", "p1_3"),
        rect=(Fraction(7, 2), side, ROWS[0], ROWS[1]),
    )
    add(
        "qr1",
        ("p1_3", "e_r1", "e_r2", "p2_3"),
        "lemma4",
        wall="right",
        outs=("p1_3", "p2_3"),
        rect=(Fraction(7, 2), side, ROWS[1], ROWS[2]),
    )
    add(
        "qr2",
        ("p2_3", "e_r2", "e_r3", "p3_3"),
        "lemma4",
        wall="right",
        outs=("p2_3", "p3_3"),
        rect=(Fraction(7, 2), side, ROWS[2], ROWS[3]),
    )

    # The eighteen Lemma 2 triangles.
    triangles: tuple[tuple[str, Face], ...] = (
        ("t01", ("p0_0", "p1_0", "p1_1")),
        ("t02", ("p0_0", "p0_1", "p1_1")),
        ("t03", ("p0_1", "p1_1", "p1_2")),
        ("t04", ("p0_1", "p0_2", "p1_2")),
        ("t05x", ("p0_2", "p1_2", "p1_3")),
        ("t06", ("p0_2", "p0_3", "p1_3")),
        ("t11", ("p1_0", "p2_0", "p1_1")),
        ("t12", ("p2_0", "p2_1", "p1_1")),
        ("t13", ("p1_1", "p2_1", "p1_2")),
        ("t14", ("p2_1", "p2_2", "p1_2")),
        ("t15x", ("p1_2", "p2_2", "p1_3")),
        ("t16", ("p1_3", "p2_3", "p2_2")),
        ("t21", ("p2_0", "p3_0", "p3_1")),
        ("t22", ("p2_0", "p2_1", "p3_1")),
        ("t23", ("p2_1", "p3_1", "p3_2")),
        ("t24", ("p2_1", "p2_2", "p3_2")),
        ("t25x", ("p2_2", "p3_2", "p3_3")),
        ("t26", ("p2_2", "p2_3", "p3_3")),
    )
    for name, face in triangles:
        add(name, face, "lemma2", corners=None)

    boundary: Face = (
        "w00",
        "w10",
        "w20",
        "w30",
        "w35",
        "w40",
        "e_r0",
        "e_r1",
        "e_r2",
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
