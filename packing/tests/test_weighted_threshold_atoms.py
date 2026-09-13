"""Weighted threshold atoms: the token count decides, and five sites are not seven tokens.

A weighted atom gives each distinct site an integer token count, so the threshold, the
budget and the inclusion--exclusion expansion are all measured in tokens while the geometry
stays one membership rectangle per site. Nearly every way of getting this wrong collapses
tokens back onto sites, which understates the charge and the expansion together, so these
tests pin the two quantities apart at every point they are used: exhaustively over all
``2^5`` site masks of the retained motif, across both coverage routes, through the record
round-trip, and against the five mutations the admission review names.

The retained seven-token, threshold-four motif ``(2, 2, 1, 1, 1)`` is the calibration object
throughout, and its published figures are the oracle: budget ``floor(7/4) = 1``, and an
expansion over ``64`` token subsets whose absolute coefficient mass is ``209``. Read as five
sites the same atom reports mass ``9``, which is the failure this file exists to catch.
"""

from __future__ import annotations

import itertools
import json
from collections.abc import Callable
from fractions import Fraction
from typing import Any

import pytest

from sqpack.fractional.generate import net_half_tangents
from sqpack.fractional.model import Atom, rotation_from_half_tangent
from sqpack.fractional.threshold import (
    WEIGHTED_VARIANT,
    ThresholdAtom,
    absolute_expansion_sum,
    charge_grid,
    charge_grid_direct,
    expansion_terms,
    threshold_weight_scale,
)

SIDE = Fraction(3)
SQUARE = Fraction(9, 10)
NET = net_half_tangents(Fraction(207107, 500000), 4)
DIRECTIONS = tuple(rotation_from_half_tangent(str(k), t) for k, t in enumerate(NET))

#: The retained motif's token counts. Its coordinates are immaterial to the counting, so
#: these tests place five distinct sites wherever the geometry under test needs them.
MOTIF = (2, 2, 1, 1, 1)
MOTIF_THRESHOLD = 4


def _sites(count: int = 5) -> tuple[tuple[Fraction, Fraction], ...]:
    return tuple((Fraction(6 + 4 * k, 10), Fraction(15, 10)) for k in range(count))


def _motif() -> ThresholdAtom:
    return ThresholdAtom(_sites(), MOTIF_THRESHOLD, Fraction(1), MOTIF)


def test_the_motif_reports_its_published_token_total_budget_and_expansion_mass() -> None:
    atom = _motif()
    assert atom.size == 5
    assert atom.token_count == 7
    assert atom.budget == 1
    assert absolute_expansion_sum(atom.token_count, atom.threshold) == 209
    subsets = sum(
        len(tuple(itertools.combinations(range(atom.token_count), j)))
        for j, _ in expansion_terms(atom.token_count, atom.threshold)
    )
    assert subsets == 64


def test_reading_the_tokens_as_sites_understates_the_expansion_mass() -> None:
    """The mutation the review names: ``size`` where ``token_count`` belongs."""

    atom = _motif()
    honest = absolute_expansion_sum(atom.token_count, atom.threshold)
    collapsed = absolute_expansion_sum(atom.size, atom.threshold)
    assert (honest, collapsed) == (209, 9)
    # The headroom check multiplies this mass by the scaled weight, so a 23x understatement
    # is a check that would pass a term list it cannot hold.
    assert honest > 20 * collapsed


def test_every_site_mask_agrees_with_explicit_token_counting() -> None:
    """All 32 masks, against a hand count: the review's first accept rule."""

    atom = _motif()
    sites = atom.points

    def membership(inside: frozenset[tuple[Fraction, Fraction]]) -> Callable[..., bool]:
        return lambda x, y: (x, y) in inside

    for mask in itertools.product((False, True), repeat=len(sites)):
        inside = frozenset(site for site, taken in zip(sites, mask, strict=True) if taken)
        expected_tokens = sum(a for a, taken in zip(MOTIF, mask, strict=True) if taken)
        assert atom.trace_count(membership(inside)) == expected_tokens
        expected_charge = Fraction(1) if expected_tokens >= MOTIF_THRESHOLD else Fraction(0)
        assert atom.charge(membership(inside)) == expected_charge
    # The two heavy sites reach the threshold; all three light sites fall short.
    assert atom.trace_count(membership(frozenset(sites[:2]))) == 4
    assert atom.trace_count(membership(frozenset(sites[2:]))) == 3


def test_an_all_ones_atom_is_exactly_the_unweighted_atom() -> None:
    """The identity mutation: nothing about a legacy atom may move."""

    sites = _sites()
    implicit = ThresholdAtom(sites, 3, Fraction(3, 4))
    explicit = ThresholdAtom(sites, 3, Fraction(3, 4), (1, 1, 1, 1, 1))
    assert implicit == explicit
    assert implicit.multiplicities == (1, 1, 1, 1, 1)
    assert implicit.size == implicit.token_count == 5
    assert implicit.budget == Fraction(3, 4) * 1
    assert implicit.key == explicit.key
    # A legacy record gains no keys, so retained records and their digests do not move.
    assert set(implicit.to_record()) == {"points", "threshold", "weight"}
    assert json.dumps(implicit.to_record()) == json.dumps(
        {"points": [[str(x), str(y)] for x, y in sites], "threshold": 3, "weight": "3/4"}
    )
    assert ThresholdAtom.from_record(implicit.to_record()) == implicit


def test_a_token_count_travels_with_its_own_site_under_d4() -> None:
    atom = _motif()
    for image in atom.images(SIDE):
        assert image.multiplicities == MOTIF
        assert image.token_count == 7
        for (x, y), a in zip(image.points, MOTIF, strict=True):
            assert (x, y, a) in dict.fromkeys(image.key[0])


def test_a_reflection_exchanging_a_heavy_site_for_a_light_one_is_not_a_symmetry() -> None:
    """Geometric support symmetry is not enough; the weighted key has to see the weights."""

    outer = Fraction(4)
    # The five sites are symmetric under x -> 4 - x, so the unweighted atom has the smaller
    # orbit. Under (2, 2, 1, 1, 1) that same reflection carries a heavy site onto a light
    # one, which is a different atom, and the orbit must not collapse it.
    sites = tuple((Fraction(x), Fraction(2)) for x in (0, 1, 2, 3, 4))
    flat = ThresholdAtom(sites, 4, Fraction(1))
    heavy = ThresholdAtom(sites, 4, Fraction(1), MOTIF)
    assert len(flat.orbit(outer)) == 2
    assert len(heavy.orbit(outer)) == 4
    assert len({image.key for image in heavy.orbit(outer)}) == 4


@pytest.mark.parametrize(
    "multiplicities",
    [
        pytest.param((2, 2, 1, 1, True), id="bool"),
        pytest.param((2, 2, 1, 1, 1.0), id="float"),
        pytest.param((2, 2, 1, 1, "1"), id="string"),
    ],
)
def test_a_token_count_that_is_not_an_integer_is_refused(
    multiplicities: tuple[object, ...],
) -> None:
    with pytest.raises(TypeError, match="not an integer"):
        ThresholdAtom(_sites(), 4, Fraction(1), multiplicities)  # type: ignore[arg-type]


@pytest.mark.parametrize("multiplicity", [0, -1])
def test_a_token_count_below_one_is_refused(multiplicity: int) -> None:
    with pytest.raises(ValueError, match="not positive"):
        ThresholdAtom(_sites(), 4, Fraction(1), (2, 2, 1, 1, multiplicity))


def test_one_token_count_per_site_is_required() -> None:
    with pytest.raises(ValueError, match="every site needs exactly one token count"):
        ThresholdAtom(_sites(), 4, Fraction(1), (2, 2, 1))


def test_a_repeated_coordinate_is_refused_so_the_token_count_is_the_only_encoding() -> None:
    sites = _sites()
    with pytest.raises(ValueError, match="must be distinct"):
        ThresholdAtom((*sites, sites[0]), 4, Fraction(1), (2, 2, 1, 1, 1, 1))


def test_the_threshold_range_is_measured_in_tokens() -> None:
    sites = _sites()
    # Seven tokens admit a threshold of seven; five sites alone would have refused it.
    assert ThresholdAtom(sites, 7, Fraction(1), MOTIF).budget == 1
    with pytest.raises(ValueError, match=r"outside 1\.\.7"):
        ThresholdAtom(sites, 8, Fraction(1), MOTIF)


def test_a_weighted_record_declares_its_variant_and_round_trips() -> None:
    atom = _motif()
    record = atom.to_record()
    assert record["variant"] == WEIGHTED_VARIANT
    assert record == {
        "variant": WEIGHTED_VARIANT,
        "weighted_points": [
            [str(x), str(y), count] for (x, y), count in zip(atom.points, MOTIF, strict=True)
        ],
        "threshold": 4,
        "weight": "1",
    }
    assert ThresholdAtom.from_record(record) == atom


def test_the_actual_legacy_decoder_refuses_a_weighted_record() -> None:
    """The decoder body from base 236132e7, retained without a Git runtime dependency.

    An added marker alone cannot protect a reader that ignores unknown fields. Its
    required `points` field must be absent from the new weighted representation.
    """

    def historical_decoder(record: dict[str, Any]) -> ThresholdAtom:
        points = tuple((Fraction(x), Fraction(y)) for x, y in record["points"])
        threshold = record["threshold"]
        if not isinstance(threshold, int) or isinstance(threshold, bool):
            raise TypeError("field 'threshold' must be a JSON integer")
        return ThresholdAtom(points, threshold, Fraction(record["weight"]))

    legacy = ThresholdAtom(_sites(), 4, Fraction(1))
    assert historical_decoder(legacy.to_record()) == legacy
    with pytest.raises(KeyError, match="points"):
        historical_decoder(_motif().to_record())


@pytest.mark.parametrize("record", [None, [], "record", 1])
def test_an_atom_record_must_be_a_json_object(record: object) -> None:
    with pytest.raises(TypeError, match="JSON object"):
        ThresholdAtom.from_record(record)


@pytest.mark.parametrize("rows", [None, [], "1,1", [None], [["1"]], [["1", "1", 1]]])
def test_legacy_rows_remain_nonempty_site_pairs(rows: object) -> None:
    record = {"points": rows, "threshold": 1, "weight": "1"}
    with pytest.raises((TypeError, ValueError), match="points"):
        ThresholdAtom.from_record(record)


def test_token_counts_without_the_variant_are_refused_as_a_silent_reread() -> None:
    """The lossy old-verifier read: an unweighted reader would skip the field it cannot see."""

    record = _motif().to_record()
    del record["variant"]
    with pytest.raises(ValueError, match=r"without.*variant"):
        ThresholdAtom.from_record(record)


def test_an_unknown_variant_is_refused_rather_than_read_as_unweighted() -> None:
    record = _motif().to_record()
    record["variant"] = "weighted-threshold/v2"
    with pytest.raises(ValueError, match="does not support"):
        ThresholdAtom.from_record(record)


def test_the_variant_without_its_token_counts_is_refused() -> None:
    record = _motif().to_record()
    del record["weighted_points"]
    with pytest.raises(ValueError, match="weighted_points"):
        ThresholdAtom.from_record(record)


@pytest.mark.parametrize("variant", [None, "", "weighted-threshold/v2", False, 1])
def test_an_explicit_invalid_variant_never_becomes_a_legacy_record(variant: object) -> None:
    record = ThresholdAtom(_sites(), 4, Fraction(1)).to_record()
    record["variant"] = variant
    with pytest.raises(ValueError, match="variant"):
        ThresholdAtom.from_record(record)


@pytest.mark.parametrize("multiplicities", [None, [], [2, 2, 1, 1, 1]])
def test_the_additive_prototype_is_refused_even_when_empty(multiplicities: object) -> None:
    record = ThresholdAtom(_sites(), 4, Fraction(1)).to_record()
    record["multiplicities"] = multiplicities
    for marked in (False, True):
        candidate = dict(record)
        if marked:
            candidate["variant"] = WEIGHTED_VARIANT
        with pytest.raises(ValueError, match="multiplicities"):
            ThresholdAtom.from_record(candidate)


@pytest.mark.parametrize("field", ["points", "multiplicities"])
def test_a_weighted_record_refuses_mixed_representations(field: str) -> None:
    record = _motif().to_record()
    record[field] = None
    with pytest.raises(ValueError, match=field):
        ThresholdAtom.from_record(record)


@pytest.mark.parametrize(
    "rows",
    [None, [], {}, "1,1,2", [None], [["1", "1"]], [["1", "1", 2, 3]]],
)
def test_weighted_rows_are_nonempty_site_triples(rows: object) -> None:
    record = {
        "variant": WEIGHTED_VARIANT,
        "weighted_points": rows,
        "threshold": 1,
        "weight": "1",
    }
    with pytest.raises((TypeError, ValueError), match="weighted_points"):
        ThresholdAtom.from_record(record)


@pytest.mark.parametrize("count", [True, False, 2.0, "2", None, 0, -1])
def test_weighted_record_counts_are_positive_json_integers(count: object) -> None:
    record = {
        "variant": WEIGHTED_VARIANT,
        "weighted_points": [["1", "1", count]],
        "threshold": 1,
        "weight": "1",
    }
    with pytest.raises((TypeError, ValueError), match="multiplicity"):
        ThresholdAtom.from_record(record)


@pytest.mark.parametrize("coordinate", [True, 1, 0.1, None, "1.5", "1/0"])
def test_weighted_record_coordinates_remain_exact_rational_strings(coordinate: object) -> None:
    record = {
        "variant": WEIGHTED_VARIANT,
        "weighted_points": [[coordinate, "1", 2]],
        "threshold": 1,
        "weight": "1",
    }
    with pytest.raises((TypeError, ValueError), match="rational string"):
        ThresholdAtom.from_record(record)


@pytest.mark.parametrize("tokens", [2**63 - 1, 2**63])
def test_the_direct_grid_bounds_token_counts_independently_of_charge(tokens: int) -> None:
    """An A-of-A atom has expansion mass one even when its token count exceeds int64."""
    sites = ((Fraction(1), Fraction(1)), (Fraction(3, 2), Fraction(1)))
    atom = ThresholdAtom(sites, tokens, Fraction(1), (2**62, tokens - 2**62))
    assert absolute_expansion_sum(atom.token_count, atom.threshold) == 1
    arguments = ((), (atom,), DIRECTIONS[0], SIDE, SQUARE)
    if tokens == 2**63:
        with pytest.raises(ValueError, match=r"token.*int64"):
            charge_grid_direct(*arguments, scale=1)
        return
    grid = charge_grid_direct(*arguments, scale=1)
    u, v = Fraction(5, 4), Fraction(1)
    i = next(
        i
        for i in range(len(grid.reduction.u_events) - 1)
        if grid.reduction.u_events[i] < u < grid.reduction.u_events[i + 1]
    )
    j = next(
        j
        for j in range(len(grid.reduction.v_events) - 1)
        if grid.reduction.v_events[j] < v < grid.reduction.v_events[j + 1]
    )
    assert any(slab == i and bottom <= j <= top for slab, bottom, top in grid.reduction.spans)
    assert grid.grid[i, j] == 1


def _weighted_instance() -> tuple[tuple[Atom, ...], tuple[ThresholdAtom, ...]]:
    atoms = (Atom("a", Fraction(12, 10), Fraction(12, 10), Fraction(1, 4)),)
    sites = _sites()
    return atoms, (
        ThresholdAtom(sites, MOTIF_THRESHOLD, Fraction(1, 2), MOTIF),
        # A second shape, so the cursor has to advance by sites while the expansion runs
        # over tokens: getting that pair backwards desynchronises the two atoms' rectangles.
        ThresholdAtom(_sites(3), 3, Fraction(1, 3), (3, 1, 1)),
    )


def test_the_token_expansion_matches_the_multiplicity_painted_count_grid() -> None:
    """The two coverage routes on weighted atoms, cell for cell.

    The sweep expands each site's rectangle to all of its tokens and signs the subsets; the
    direct route paints each rectangle with its own count and thresholds the total. They
    share nothing past the event grid, so agreement is evidence rather than a tautology.
    """

    atoms, threshold_atoms = _weighted_instance()
    scale = threshold_weight_scale(atoms, threshold_atoms)
    for direction in DIRECTIONS:
        fast = charge_grid(atoms, threshold_atoms, direction, SIDE, SQUARE, scale=scale)
        slow = charge_grid_direct(atoms, threshold_atoms, direction, SIDE, SQUARE, scale=scale)
        assert fast.reduction == slow.reduction
        assert (fast.grid == slow.grid).all()
        assert fast.grid.min() >= 0


def test_the_weighted_routes_differ_from_the_same_atom_read_unweighted() -> None:
    """Agreement above would be worthless if both routes ignored the token counts."""

    atoms, weighted = _weighted_instance()
    flat = tuple(ThresholdAtom(a.points, a.threshold, a.weight) for a in weighted)
    scale = threshold_weight_scale(atoms, (*weighted, *flat))
    differs = False
    for direction in DIRECTIONS:
        heavy = charge_grid(atoms, weighted, direction, SIDE, SQUARE, scale=scale)
        light = charge_grid(atoms, flat, direction, SIDE, SQUARE, scale=scale)
        if (heavy.grid != light.grid).any():
            differs = True
    assert differs, "the token counts made no difference to either route"
