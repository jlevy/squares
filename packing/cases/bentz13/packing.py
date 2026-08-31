"""Bentz 2010, Section 3: the Figure 2 configuration for `s(13) = 4`.

Source: `resources/papers/bentz-2010-optimal-packings-13-and-46.md`, Section 3, with
the raw extraction as ground truth. Figure 2 is not extractable from the PDF, but the
prose determines the sixteen points completely: `A(1, 0.914)`, `B(0.914, 1)`,
`C(0.914, 2)`, `D(1.65, 1.65)`, "while the remaining ones are obtained through
mirroring at the lines x = 2, y = 2, and y = x". Every coordinate in Section 3 is a
rational decimal, so the whole layer lives over plain `Fraction` arithmetic -- the
only irrational in any premise is `2 sqrt 2`, and each such comparison is squared
into an exact rational sign.

The cover itself is reconstructed (Figure 2's regions are also unextractable):

- four **Lemma 1 corner pentagons** -- the corner unit square minus the sliver cut by
  the segment `A-B` (and its mirrors). Lemma 1's conclusion triangle at the corner,
  spanned by `(1, 1)`, `(0.9, 1)`, `(1, 0.9)`, contains both `A` and `B` on its
  boundary, so a box centred anywhere in the pentagon contains both near-corner
  points; the axes named in the lemma are container walls, which an open box inside
  the container never meets. Cutting the sliver keeps the unchargeable vertex
  `(1, 1)` out of every Lemma 2 cell: the `A-B-D` triangle beside the pentagon
  contains it strictly.
- eight **Lemma 4 wall rectangles** at `a = 1`, `b = 0.914`, whose slack
  `8 - (a + 2b)^2 = 0.002416` is strictly positive and whose two inner corners are
  both set points -- no wall-vertex outs are needed anywhere in this figure.
- eighteen **Lemma 2 triangles** through the `D` orbit; the longest side squared is
  `964196/1000000`.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from sqpack.cover import Face, Point, polygon_area2

EXPECTED_POINTS = 16
EXPECTED_FACES = 4 + 8 + 18
SIDE = 4


@dataclass(frozen=True)
class Rat:
    """Exact rational scalar carrying the cover scalar contract."""

    value: Fraction

    @classmethod
    def of(cls, value: int | Fraction) -> Rat:
        return cls(Fraction(value))

    def _coerce(self, other: object) -> Fraction:
        if isinstance(other, Rat):
            return other.value
        if isinstance(other, int | Fraction):
            return Fraction(other)
        raise TypeError(f"cannot coerce {other!r}")

    def __add__(self, other: object) -> Rat:
        return Rat(self.value + self._coerce(other))

    __radd__ = __add__

    def __sub__(self, other: object) -> Rat:
        return Rat(self.value - self._coerce(other))

    def __rsub__(self, other: object) -> Rat:
        return Rat(self._coerce(other) - self.value)

    def __mul__(self, other: object) -> Rat:
        return Rat(self.value * self._coerce(other))

    __rmul__ = __mul__

    def __truediv__(self, other: object) -> Rat:
        return Rat(self.value / self._coerce(other))

    def __pow__(self, exponent: int) -> Rat:
        return Rat(self.value**exponent)

    def __neg__(self) -> Rat:
        return Rat(-self.value)

    def __le__(self, other: object) -> bool:
        return self.value <= self._coerce(other)

    def __lt__(self, other: object) -> bool:
        return self.value < self._coerce(other)

    def __ge__(self, other: object) -> bool:
        return self.value >= self._coerce(other)

    def __gt__(self, other: object) -> bool:
        return self.value > self._coerce(other)

    def __eq__(self, other: object) -> bool:
        try:
            return self.value == self._coerce(other)
        except TypeError:
            return NotImplemented

    def __hash__(self) -> int:
        return hash(self.value)

    def sign(self) -> int:
        if self.value > 0:
            return 1
        return -1 if self.value < 0 else 0

    def is_zero(self) -> bool:
        return self.value == 0

    def text(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class CellPlan:
    """One cell of the cover: its oriented face and the lemma its certificate checks."""

    face: Face
    kind: str
    wall: str | None = None
    outs: tuple[str, ...] = ()
    corner: str | None = None


#: The near-corner offset 0.914 and the centre-block offset 1.65, exactly.
NEAR = Fraction(457, 500)
MID = Fraction(33, 20)


def build() -> tuple[dict[str, Point], dict[str, Point], dict[str, CellPlan]]:
    """Return (set_points, all_vertices, cell_plan) for the Figure 2 configuration."""

    def rat(value: int | Fraction) -> Rat:
        return Rat.of(value)

    def pt(x: int | Fraction, y: int | Fraction) -> Point:
        return (rat(x), rat(y))

    four = Fraction(4)
    set_points: dict[str, Point] = {
        # Near-corner pairs: A-type on a vertical wall offset, B-type horizontal.
        "a1": pt(1, NEAR),
        "b1": pt(NEAR, 1),
        "a2": pt(3, NEAR),
        "b2": pt(four - NEAR, 1),
        "a3": pt(1, four - NEAR),
        "b3": pt(NEAR, 3),
        "a4": pt(3, four - NEAR),
        "b4": pt(four - NEAR, 3),
        # Mid-edge points: the C orbit.
        "c1": pt(NEAR, 2),
        "c2": pt(four - NEAR, 2),
        "c3": pt(2, NEAR),
        "c4": pt(2, four - NEAR),
        # Centre block: the D orbit.
        "d1": pt(MID, MID),
        "d2": pt(four - MID, MID),
        "d3": pt(four - MID, four - MID),
        "d4": pt(MID, four - MID),
    }
    if len(set_points) != EXPECTED_POINTS:
        raise ValueError(f"expected {EXPECTED_POINTS} points, built {len(set_points)}")

    vertices: dict[str, Point] = dict(set_points)
    for i in range(5):
        vertices[f"w{i}0"] = pt(i, 0)
        vertices[f"w{i}4"] = pt(i, 4)
    for j in range(1, 4):
        vertices[f"w0{j}"] = pt(0, j)
        vertices[f"w4{j}"] = pt(4, j)

    plan: dict[str, CellPlan] = {}

    def oriented(face: Face) -> Face:
        area2 = polygon_area2(tuple(vertices[name] for name in face))
        if area2.sign() == 0:
            raise ValueError(f"degenerate face: {face}")
        return face if area2.sign() > 0 else tuple(reversed(face))

    def add(name: str, face: Face, kind: str, **data: object) -> None:
        plan[name] = CellPlan(face=oriented(face), kind=kind, **data)  # type: ignore[arg-type]

    # Lemma 1 corner pentagons: the corner unit square minus the A-B sliver.
    add(
        "pent_bl", ("w00", "w10", "a1", "b1", "w01"), "corner1", corner="w00", outs=("a1", "b1")
    )
    add(
        "pent_br", ("w30", "w40", "w41", "b2", "a2"), "corner1", corner="w40", outs=("a2", "b2")
    )
    add(
        "pent_tl", ("w03", "b3", "a3", "w14", "w04"), "corner1", corner="w04", outs=("a3", "b3")
    )
    add(
        "pent_tr", ("w43", "b4", "a4", "w34", "w44"), "corner1", corner="w44", outs=("a4", "b4")
    )

    # Lemma 4 wall rectangles, both inner corners set points.
    add("rb1", ("w10", "w20", "c3", "a1"), "lemma4", wall="bottom", outs=("a1", "c3"))
    add("rb2", ("w20", "w30", "a2", "c3"), "lemma4", wall="bottom", outs=("c3", "a2"))
    add("rl1", ("w01", "b1", "c1", "w02"), "lemma4", wall="left", outs=("b1", "c1"))
    add("rl2", ("w02", "c1", "b3", "w03"), "lemma4", wall="left", outs=("c1", "b3"))
    add("rr1", ("b2", "w41", "w42", "c2"), "lemma4", wall="right", outs=("b2", "c2"))
    add("rr2", ("c2", "w42", "w43", "b4"), "lemma4", wall="right", outs=("c2", "b4"))
    add("rt1", ("a3", "c4", "w24", "w14"), "lemma4", wall="top", outs=("a3", "c4"))
    add("rt2", ("c4", "a4", "w34", "w24"), "lemma4", wall="top", outs=("c4", "a4"))

    # Lemma 2 triangles: four corner slivers, eight edge fans, four mid fans, two centre.
    triangles = (
        ("t_c1", ("a1", "b1", "d1")),
        ("t_c2", ("a2", "b2", "d2")),
        ("t_c3", ("a3", "b3", "d4")),
        ("t_c4", ("a4", "b4", "d3")),
        ("t_e1", ("a1", "c3", "d1")),
        ("t_e2", ("c3", "a2", "d2")),
        ("t_e3", ("b1", "c1", "d1")),
        ("t_e4", ("c1", "b3", "d4")),
        ("t_e5", ("b2", "c2", "d2")),
        ("t_e6", ("c2", "b4", "d3")),
        ("t_e7", ("a3", "c4", "d4")),
        ("t_e8", ("c4", "a4", "d3")),
        ("t_m1", ("c3", "d1", "d2")),
        ("t_m2", ("c1", "d1", "d4")),
        ("t_m3", ("c2", "d2", "d3")),
        ("t_m4", ("c4", "d4", "d3")),
        ("t_x1", ("d1", "d2", "d3")),
        ("t_x2", ("d1", "d3", "d4")),
    )
    for name, face in triangles:
        add(name, face, "lemma2", outs=face)

    if len(plan) != EXPECTED_FACES:
        raise ValueError(f"expected {EXPECTED_FACES} faces, built {len(plan)}")
    return set_points, vertices, plan


#: The container boundary walk, counterclockwise from the origin.
BOUNDARY: Face = (
    "w00",
    "w10",
    "w20",
    "w30",
    "w40",
    "w41",
    "w42",
    "w43",
    "w44",
    "w34",
    "w24",
    "w14",
    "w04",
    "w03",
    "w02",
    "w01",
)
