"""The hull kernel on the n11 frame reproduces n11's mask-0 field packet exactly."""

from __future__ import annotations

import copy
import dataclasses
import time
from fractions import Fraction
from typing import Any

import pytest

from devtools import check_hull_kernel_mask0 as tool
from devtools import check_n11_optimality_field_mask0 as frozen
from sqpack.hull_kernel import Budget, RefusalError, counting, n11
from sqpack.hull_kernel.geometry import clip
from sqpack.hull_kernel.rational import Q, as_fraction
from sqpack.hull_kernel.sweep import exact_union_cover

type Sources = tuple[dict[str, Any], dict[str, Any], dict[str, Any]]


@pytest.fixture(scope="module")
def sources() -> Sources:
    return tool.load_sources()


@pytest.fixture(scope="module")
def receipt() -> dict[str, Any]:
    return tool.load_receipt()


def budget() -> Budget:
    return Budget(time.monotonic() + 30, 100000)


def test_the_primitives_reproduce_the_frozen_functions_bit_for_bit(sources: Sources) -> None:
    packet, _, _ = sources
    frame, library_packet, rows = tool.library_inputs(sources)
    denominator = packet["certificate"]["coordinate_denominator"]
    for _, _, interval in rows[::9]:
        envelope = counting.row_envelope(frame, interval)
        assert envelope == frozen.row_envelope(
            (as_fraction(interval[0]), as_fraction(interval[1]))
        )
        core, _, c, s = envelope
        sites = [frame.rotate(site, c, s) for site in library_packet.sites]
        assert sites == [
            frozen.rotate(
                (Fraction(x, denominator), Fraction(y, denominator)),
                as_fraction(c),
                as_fraction(s),
            )
            for x, y in packet["certificate"]["sites"]
        ]
        assert counting.majority_halfplanes(sites, core / 2, 3) == frozen.true_halfplanes(
            [(as_fraction(x), as_fraction(y)) for x, y in sites], as_fraction(core / 2)
        )
    square = [(Q(0), Q(0)), (Q(1), Q(0)), (Q(1), Q(1)), (Q(0), Q(1))]
    left, right = clip(square, (Q(1), Q(0), Q(1, 2))), clip(square, (Q(-1), Q(0), Q(-1, 2)))
    frozen_square = [(as_fraction(x), as_fraction(y)) for x, y in square]
    frozen_left = frozen.clip(frozen_square, (Fraction(1), Fraction(0), Fraction(1, 2)))
    frozen_right = frozen.clip(frozen_square, (Fraction(-1), Fraction(0), Fraction(-1, 2)))
    assert left == frozen_left
    frozen_budget = frozen.Budget(time.monotonic() + 30, 500)
    assert exact_union_cover(square, [left, right], budget=budget()) == (
        frozen.exact_union_cover(
            frozen_square, [frozen_left, frozen_right], budget=frozen_budget
        )
    )
    shifted = clip(square, (Q(-1), Q(0), -(Q(1, 2) + Q(1, 10**50))))
    with pytest.raises(RefusalError, match="row uncovered"):
        exact_union_cover(square, [left, shifted], budget=budget())


def test_every_ownership_proof_and_the_transfer_match_the_receipt(
    sources: Sources, receipt: dict[str, Any]
) -> None:
    frame, library_packet, _ = tool.library_inputs(sources)
    result = counting.replay_counting_packet(frame, library_packet, [], budget=budget())
    assert result["status"] == "PASS_PARTIAL_REPLAY"
    assert result["geometry_verified"] is False
    assert result["canonical_cases_excluded"] == 0
    assert result["ownership_points"] == 55
    assert result["ownership_checked"] == receipt["ownership_checked"]
    assert result["transfer"] == receipt["transfer"]
    assert len(result["transfer"]["direct_case_ids"]) == 453
    assert len(result["transfer"]["transferred_case_ids"]) == 459


def test_a_sample_matches_the_frozen_checker_and_the_receipt(sources: Sources) -> None:
    result = tool.sample_replay(
        sources,
        points=[(0, 5), (6, 0)],
        row_positions=[0, 67],
        max_seconds=30,
        max_nodes=100000,
    )
    assert result["status"] == "PASS_PARTIAL_SAMPLE"
    assert result["geometry_verified"] is False
    assert result["direct_cases"] == 453
    assert result["transferred_cases"] == 459


def test_a_perturbed_owned_point_is_refused(sources: Sources, receipt: dict[str, Any]) -> None:
    packet, audit, cover = sources
    changed = copy.deepcopy(packet)
    x, y = changed["ownership_points_field"][0][5]
    changed["ownership_points_field"][0][5] = [str(Q(x) + Q(1, 10**9)), y]
    with pytest.raises(RefusalError, match="packet content differs"):
        tool.sample_replay(
            (changed, audit, cover),
            points=[(0, 5)],
            row_positions=[0],
            max_seconds=30,
            max_nodes=100000,
        )
    # Past the content pin, the changed point's own proof differs from the receipt's.
    frame = n11.frame_from_cover(cover)
    result = counting.replay_counting_packet(
        frame,
        n11.packet_from_field(frame, changed),
        [],
        budget=budget(),
        points=[(0, 5)],
        transfer=False,
    )
    assert result["status"] == "PASS_PARTIAL_REPLAY"
    with pytest.raises(RefusalError, match="maximum_vertex_distance_squared"):
        tool.require_same(
            result["ownership_checked"], [receipt["ownership_checked"][5]], "points"
        )


def test_a_perturbed_row_partition_or_premise_is_refused(sources: Sources) -> None:
    packet, audit, cover = sources
    changed = copy.deepcopy(audit)
    changed["independent_row_proofs"][0]["interval"][1] = "1/65"
    with pytest.raises(RefusalError, match="audit content differs"):
        tool.library_inputs((packet, changed, cover))
    frame = n11.frame_from_cover(cover)
    library_packet = n11.packet_from_field(frame, packet)
    with pytest.raises(RefusalError, match="row gap or overlap"):
        counting.partition_rows(n11.rows_from_audit(changed), library_packet.positive_cells)
    capped = copy.deepcopy(packet)
    capped["parent_Uplus"] = str(Q(capped["parent_Uplus"]) + Q(1, 10**30))
    with pytest.raises(RefusalError, match="U premise changed"):
        n11.packet_from_field(frame, capped)
    heavier = dataclasses.replace(library_packet, budget=2)
    with pytest.raises(RefusalError, match="unit-weight"):
        counting.replay_counting_packet(frame, heavier, [], budget=budget())


@pytest.mark.slow
def test_the_full_replay_reproduces_the_receipt_and_the_frozen_checker(
    sources: Sources,
) -> None:
    result = tool.full_replay(sources, max_seconds=600, max_nodes=100000, workers=2)
    assert result["status"] == "PASS_LIBRARY_REPRODUCES_MASK0"
    assert result["geometry_verified"] is True
    assert result["ownership_points"] == 55
    assert result["positive_cell_rows"] == 136
    assert result["rows_by_cell"] == {1: 67, 2: 69}
    assert result["direct_cases"] == 453
    assert result["transferred_cases"] == 459
    assert result["work_units"] == result["receipt_counts"]["work_units"] == 27544
