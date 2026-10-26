"""The exact audit of Friedman's DS7 Theorem 2 and its negative controls (think-vvjk).

The positive direction replays the whole record byte for byte. The two controls are
mutated certificates whose claims are false, since Göbel's packing puts five unit squares
in a square of side exactly `2 + 1/sqrt 2`, and each must be refused at the premise it
breaks:

- **the widened gap**: the four points `1/sqrt 2 + 1/100` apart in a container of side
  `2 + 1/sqrt 2 + 1/100`, which claims `s(5) >= 2.717...`; the central triangles'
  hypotenuse exceeds one, so Lemma 3 refuses;
- **the pushed points**: the points `1 + 1/100` from the walls in a container of side
  `2 + 1/sqrt 2 + 1/50`, which claims `s(5) >= 2.727...`; the corner cells are no longer
  unit squares (Lemma 1) and the wall cells are deeper than one (Lemma 2).
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from cases.friedman5.verify_cover import (
    EXPECTED_FACES,
    RECORD,
    CoverCertificateError,
    build,
    certify,
    certify_wall,
    lemma2_angle_minimum,
    record_text,
)


def test_the_retained_record_replays_byte_for_byte() -> None:
    assert record_text() == RECORD.read_text(encoding="utf-8")


def test_the_cover_is_friedmans_and_every_cell_holds_its_lemma() -> None:
    cover = build()
    record = certify(cover)
    assert record["cell_kinds"] == {"lemma1": 4, "lemma2": 4, "lemma3": 2}
    assert record["tiling"]["face_count"] == EXPECTED_FACES  # type: ignore[index]
    assert record["tiling"]["euler_characteristic"] == 1  # type: ignore[index]
    # The side is 2 + 1/sqrt 2: 2 rational, 1/2 on sqrt 2.
    assert record["container_side"] == "poly[2,1/2]"
    for name in ("wall_bottom", "wall_top", "wall_left", "wall_right"):
        wall = record["cells"][name]  # type: ignore[index]
        assert (wall["x"], wall["y"]) == ("poly[0,1/2]", "poly[1,0]")
        # 2 sqrt 2 - (1/sqrt 2 + 2) = 3 sqrt 2 / 2 - 2 > 0: Friedman's strict hypothesis.
        assert wall["two_sqrt2_minus_x_minus_2y"] == "poly[-2,3/2]"
        # The lowest corner reaches the wall with equality at theta = 0, pi/2.
        assert wall["lowest_corner"]["minimum_equals_depth"] is True
    for name in ("triangle_low", "triangle_high"):
        lengths = record["cells"][name]["squared_edge_lengths"]  # type: ignore[index]
        # Legs of 1/sqrt 2 and a hypotenuse of exactly one.
        assert sorted(lengths.values()) == sorted(["poly[1/2,0]", "poly[1/2,0]", "poly[1,0]"])


def test_the_widened_gap_is_refused_at_its_triangles() -> None:
    with pytest.raises(CoverCertificateError, match="triangle has an edge longer than one"):
        certify(build(gap_shift=Fraction(1, 100)))


def test_the_pushed_points_are_refused_at_the_corners_and_the_walls() -> None:
    cover = build(offset_shift=Fraction(1, 100))
    with pytest.raises(CoverCertificateError, match="not the unit square at its container"):
        certify(cover)
    for name in ("wall_bottom", "wall_top", "wall_left", "wall_right"):
        with pytest.raises(CoverCertificateError, match=r"Lemma 2 needs 0 < y <= 1"):
            certify_wall(cover, name, cover.cells[name])


def test_a_displaced_point_breaks_the_cover() -> None:
    cover = build()
    x, y = cover.vertices["p22"]
    moved = dict(cover.vertices)
    moved["p22"] = (x + cover.field.rational(Fraction(1, 100)), y)
    tampered = type(cover)(
        cover.field,
        cover.sqrt2,
        cover.offset,
        cover.gap,
        cover.side,
        {**cover.set_points, "p22": moved["p22"]},
        moved,
        cover.cells,
    )
    with pytest.raises(CoverCertificateError):
        certify(tampered)


def test_a_point_no_cell_charges_is_refused() -> None:
    cover = build()
    points = {name: point for name, point in cover.set_points.items() if name != "p22"}
    tampered = type(cover)(
        cover.field,
        cover.sqrt2,
        cover.offset,
        cover.gap,
        cover.side,
        points,
        cover.vertices,
        cover.cells,
    )
    with pytest.raises(CoverCertificateError, match="expected 4 points of P"):
        certify(tampered)


def test_lemma2_minimum_moves_to_the_diagonal_for_wide_rectangles() -> None:
    cover = build()
    one = cover.field.one
    # At x = 1 the diagonal value sqrt 2 - 1/2 is below 1, so the minimum is at pi/4.
    wide = lemma2_angle_minimum(cover.sqrt2, one, cover.sqrt2 - one / 2)
    assert wide["minimum_at"] == "t = sqrt 2 (theta = pi/4)"
    assert wide["minimum_equals_depth"] is True
    with pytest.raises(CoverCertificateError, match="lowest corner stays above the wall"):
        lemma2_angle_minimum(cover.sqrt2, one, one)
