"""The diamond-and-staircases construction of #992, built exactly and decided on both routes.

The stated recipe at 977 is checked against the certificate's own words: 441 squares turned
45 degrees, four staircases of 134, every bottom-left cell inside x + y <= 17. A small
recipe of the same shape, 41 squares at 5 + (3/2) sqrt 2, is decided on both exact routes
with every planned control, in a second. The 977 decision is the packet's receipt, which
`devtools.diamond_staircases decide --check` reproduces in about ten minutes at two jobs;
here it is held to its plan and its stated outcomes. The Göbel comparison is exact, and
its family test agrees with `cases.gobel_family`'s.
"""

from __future__ import annotations

import json
from fractions import Fraction

import pytest

from cases.gobel_family.packing import admits
from devtools import diamond_staircases as staircases

SMALL = staircases.Recipe(n=41, block=3, offset=5, widths=(3, 3, 2))
TURNED = [["0", "1/2"], ["0", "1/2"]]


def test_the_stated_recipe_is_the_certificates_construction() -> None:
    witness = staircases.build()
    placed = witness["squares"]
    assert witness["n"] == len(placed) == 977
    assert witness["side"] == ["17", "21/2"]
    assert sum(square["basis"] == TURNED for square in placed) == 441
    assert sum(square["basis"] == ["1", "0"] for square in placed) == 536
    cells = staircases.STATED.staircase()
    assert len(cells) == 134
    assert all(c + r + 2 <= 17 and c < 15 and r < 15 for c, r in cells)
    # Square 1 is (i, j) = (0, 0): u = v = -10, centre (L/2, L/2 - 10 sqrt 2).
    assert placed[0]["center"] == [["17/2", "21/4"], ["17/2", "-19/4"]]
    # Square 442 is the bottom-left cell (0, 0); square 576 starts its quarter turn,
    # (L - 1/2, 1/2).
    assert placed[441]["center"] == ["1/2", "1/2"]
    assert placed[575]["center"] == [["33/2", "21/2"], "1/2"]


def test_a_recipe_whose_count_is_not_its_squares_is_refused() -> None:
    with pytest.raises(staircases.RecipeError, match="hold 41 squares, not 42"):
        staircases.squares(staircases.Recipe(n=42, block=3, offset=5, widths=(3, 3, 2)))


@pytest.mark.parametrize("control", staircases.CONTROLS, ids=lambda c: c.name)
def test_a_small_recipe_meets_every_planned_control(control: staircases.Control) -> None:
    found = staircases.run_control(control, SMALL)
    assert found["as_expected"], found
    expected = not control.refused_for
    assert all(found["routes"][route]["passed"] is expected for route in staircases.ROUTES)


def test_the_goebel_comparison_is_exact() -> None:
    found = staircases.goebel_comparison()
    assert found["side"] == "17 + 21/2*sqrt(2)"
    assert found["goebel_construction"] == {
        "side": "17 + 11*sqrt(2)",
        "family": "Göbel square",
        "count": 1028,
        "relation": "below",
        "difference": "0 + 1/2*sqrt(2)",
    }
    border = found["l_border_of_member"]
    assert (border["a"], border["b"], border["admitted"]) == (15, 21, True)
    assert (border["count"], border["layer_adds"], border["capacity"]) == (921, 61, 982)
    assert border["side"] == "16 + 21/2*sqrt(2)"
    deeper = found["deeper_arrangement"]
    assert (deeper["a"], deeper["admitted"], deeper["count"]) == (16, False, 985)
    assert (deeper["staircase"], deeper["recipe_staircase"]) == (136, 134)
    assert found["grid"] == {"side": 32, "recipe_below": True}


@pytest.mark.parametrize("a", range(1, 30))
def test_the_family_condition_agrees_with_the_case_package(a: int) -> None:
    for b in range(1, 50):
        assert staircases.goebel_admits(a, b) == admits(a, b)


def test_the_floor_is_exact_at_the_boundaries() -> None:
    floor = staircases.floor_root_two
    assert floor(Fraction(16), Fraction(21, 2)) == 30
    assert floor(Fraction(0), Fraction(1)) == 1
    assert floor(Fraction(3), Fraction(0)) == 3


def test_the_retained_receipt_holds_to_its_plan() -> None:
    receipt = json.loads(staircases.RECEIPT.read_text(encoding="utf-8"))
    assert staircases.problems(receipt) == []
    assert receipt["plan"]["stated_at"] == staircases.PLAN_STATED_AT
    assert receipt["recipe"]["widths"] == list(staircases.STATED.widths)
    assert [control["control"] for control in receipt["controls"]] == [
        control.name for control in staircases.CONTROLS
    ]
    for control, planned in zip(receipt["controls"], staircases.CONTROLS, strict=True):
        assert control["expected_failures"] == list(planned.refused_for)
        for route in staircases.ROUTES:
            assert control["routes"][route]["passed"] is (not planned.refused_for)
    assert receipt["goebel"] == staircases.goebel_comparison()
