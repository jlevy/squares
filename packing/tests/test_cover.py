"""The general unavoidable-set core certifies and refuses on a scalar it never met.

`sqpack.cover` was extracted from `cases/stromquist` under BC-093, whose replay
controls (exp-016 refusing, exp-017 certifying, both byte-stable) exercise it over Q5
and FieldElement. These tests pin the general half on a third scalar -- a plain
rational -- so a regression that happens to preserve the Stromquist records is still
caught, and the typed resource refusals stay refusals.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import pytest

from sqpack import cover


@dataclass(frozen=True)
class Rat:
    """Minimal exact scalar: rational arithmetic with the cover scalar contract."""

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
        return cover.fraction_text(self.value)


def rat_point(x: int | Fraction, y: int | Fraction) -> tuple[Rat, Rat]:
    return Rat.of(x), Rat.of(y)


UNIT_CORNERS = {
    "a": rat_point(0, 0),
    "b": rat_point(1, 0),
    "c": rat_point(1, 1),
    "d": rat_point(0, 1),
}


def test_square_tiling_certifies_the_two_triangle_unit_square() -> None:
    record = cover.validate_square_tiling(
        UNIT_CORNERS,
        (("a", "b", "c"), ("a", "c", "d")),
        side=Rat.of(1),
        expected_faces=2,
    )
    assert record["face_count"] == 2
    assert record["euler_characteristic"] == 1
    assert record["signed_area_twice"] == "2"


def test_square_tiling_refuses_a_face_shortfall() -> None:
    with pytest.raises(ValueError, match="do not sum to the exact container area"):
        cover.validate_square_tiling(
            UNIT_CORNERS, (("a", "b", "c"),), side=Rat.of(1), expected_faces=1
        )


def test_triangle_mesh_refuses_an_edge_longer_than_one() -> None:
    points = dict(UNIT_CORNERS)
    with pytest.raises(ValueError, match="edge longer than one"):
        cover.triangle_edge_certificate(points, ("a", "b", "c"))
    small = {
        "a": rat_point(0, 0),
        "b": rat_point(Fraction(1, 2), 0),
        "c": rat_point(0, Fraction(1, 2)),
    }
    record = cover.triangle_edge_certificate(small, ("a", "b", "c"))
    assert record["vertices"] == ["a", "b", "c"]


def test_noncrossing_refuses_crossing_diagonals() -> None:
    with pytest.raises(ValueError, match="nonadjacent edges cross"):
        cover.validate_noncrossing(
            UNIT_CORNERS, (cover.normalized_edge("a", "c"), cover.normalized_edge("b", "d"))
        )


def test_box_predicates_agree_on_an_axis_aligned_box() -> None:
    center = rat_point(1, 1)
    half, cosine, sine = Rat.of(Fraction(3, 4)), Rat.of(1), Rat.of(0)
    corners = cover.box_corners(center, half, cosine, sine)
    cover.validate_box_shape(corners, Rat.of(Fraction(3, 2)))
    clearances = dict(cover.corner_clearances(corners, Rat.of(2)))
    assert clearances["corner_0_left"] == Rat.of(Fraction(1, 4))
    assert clearances["corner_2_top"] == Rat.of(Fraction(1, 4))
    inside_margin, _ = cover.avoidance_margin(rat_point(1, 1), center, half, cosine, sine)
    assert inside_margin.sign() < 0
    outside_margin, axis = cover.avoidance_margin(rat_point(2, 1), center, half, cosine, sine)
    assert outside_margin == Rat.of(Fraction(1, 4))
    assert axis == "u"
    boundary_margin, _ = cover.avoidance_margin(
        rat_point(Fraction(7, 4), 1), center, half, cosine, sine
    )
    assert boundary_margin.is_zero()


def test_box_shape_refuses_a_sheared_box() -> None:
    corners = cover.box_corners(rat_point(0, 0), Rat.of(1), Rat.of(1), Rat.of(1))
    with pytest.raises(ValueError, match="declared exact side length"):
        cover.validate_box_shape(corners, Rat.of(2))


def test_resource_declaration_supports_points_and_refuses_the_rest_by_type() -> None:
    assert cover.declare_resources(("point", "point")) == ("point", "point")
    with pytest.raises(cover.ResourceKindNotSupportedError) as caught:
        cover.declare_resources(("point", "segment"))
    assert caught.value.kind == "segment"
    with pytest.raises(ValueError, match="unknown resource kind"):
        cover.declare_resources(("hyperplane",))


def test_exact_helpers_decide_by_sign() -> None:
    assert cover.exact_abs(Rat.of(-3)) == Rat.of(3)
    value, axis = cover.exact_max(Rat.of(2), Rat.of(5))
    assert value == Rat.of(5)
    assert axis == "v"
    label, value = cover.exact_min([("p", Rat.of(4)), ("q", Rat.of(1)), ("r", Rat.of(2))])
    assert (label, value) == ("q", Rat.of(1))
    with pytest.raises(ValueError, match="empty exact list"):
        cover.exact_min([])
