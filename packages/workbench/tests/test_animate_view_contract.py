"""The angle-stable colour contract's one allowance, tested without a browser.

`animate_view_contract.colours` holds the angles the retained frames share to one palette
slot, except where two class centres within the colourer's tolerance fall either side of a
five-degree band edge (#553 C1). `split_across_band_edge` is that rule, written once for the
core frames and the wide check; these are its admitted and refused cases. #554 tracks the fix
that would retire it.
"""

from __future__ import annotations

import pytest

from workbench_tools.animate_view_contract import split_across_band_edge

BAND, TOLERANCE = 5.0, 0.5


def test_n29_and_n272_straddle_the_65_degree_edge_and_are_admitted() -> None:
    # The pair the colourer splits at the head of #553: 0.35 degrees apart, slots 14 and 15.
    assert split_across_band_edge((64.9387, 14), (65.2889, 15), BAND, TOLERANCE)
    assert split_across_band_edge((65.2889, 15), (64.9387, 14), BAND, TOLERANCE)


@pytest.mark.parametrize(
    ("first", "second", "why"),
    [
        ((64.9387, 14), (65.2889, 16), "slots two apart across the edge"),
        ((64.9387, 14), (65.2889, 14), "one slot is no split to admit"),
        ((62.1, 14), (62.4, 15), "slots one apart with no edge between the centres"),
        ((64.4, 14), (65.2, 15), "an edge between them, but beyond the tolerance of one"),
        ((44.4, 10), (44.6, 1), "the 45-degree class is its own slot, not the next band's"),
    ],
)
def test_every_other_split_is_refused(
    first: tuple[float, int], second: tuple[float, int], why: str
) -> None:
    assert not split_across_band_edge(first, second, BAND, TOLERANCE), why


def test_the_rule_folds_tilts_as_the_page_does() -> None:
    # A quarter turn on, the same two classes are the same split.
    assert split_across_band_edge((154.9387, 14), (-24.7111, 15), BAND, TOLERANCE)
