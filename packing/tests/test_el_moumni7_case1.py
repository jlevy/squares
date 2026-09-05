"""Exact local controls for El Moumni Theorem 1, Case 1."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction

import pytest

from cases.small_n.el_moumni7 import (
    ElMoumniSourceControlError,
    derive_figure4_coordinate_packet,
    prove_case1_minimum_repair,
    replay_figure4_coordinate_packet,
    transcribe_printed_figure4_length,
    transcribe_printed_figure4_line_center,
)


def test_case1_repair_keeps_both_proposition_2_branches_exact() -> None:
    certificate = prove_case1_minimum_repair()

    assert certificate.epsilon_upper == (Fraction(1, 3), Fraction(-1, 6))
    assert certificate.minimum_branch_threshold == (Fraction(3, 2), Fraction(-1))
    assert certificate.threshold_gap == (Fraction(-7, 6), Fraction(5, 6))
    assert certificate.threshold_gap_sign == 1
    assert certificate.low_branch_contradiction_margin == (Fraction(-8), Fraction(6))
    assert certificate.low_branch_contradiction_sign == 1
    assert certificate.high_branch_required_length == 3
    assert certificate.high_branch_available_strict_upper == 2
    assert certificate.conclusion == "case-1-repair-only"


def test_unbranched_source_substitution_rejects() -> None:
    with pytest.raises(ElMoumniSourceControlError) as caught:
        prove_case1_minimum_repair(preserve_minimum=False)
    assert caught.value.kind == "proposition-2-minimum-dropped"


def test_deleted_third_contribution_rejects() -> None:
    with pytest.raises(ElMoumniSourceControlError) as caught:
        prove_case1_minimum_repair(required_contributions=2)
    assert caught.value.kind == "case-1-contribution-count"


def test_printed_figure4_length_is_typed_source_blocker() -> None:
    with pytest.raises(ElMoumniSourceControlError) as caught:
        transcribe_printed_figure4_length()
    assert caught.value.kind == "negative-source-length"
    assert caught.value.exact_value == (Fraction(-4), Fraction(2))


def test_printed_figure4_line_center_is_typed_source_blocker() -> None:
    with pytest.raises(ElMoumniSourceControlError) as caught:
        transcribe_printed_figure4_line_center()
    assert caught.value.kind == "wrong-source-center"


def test_figure4_coordinate_packet_has_literal_interior_oracle() -> None:
    packet = derive_figure4_coordinate_packet((Fraction(1, 20), Fraction(0)))
    points = dict(packet.points)

    assert packet.contract == "packing.squares:ElMoumniFigure4Coordinates/v1"
    assert packet.epsilon_upper == (Fraction(1, 3), Fraction(-1, 6))
    assert packet.h == (Fraction(19, 20), Fraction(0))
    assert packet.delta == (Fraction(-2), Fraction(2))
    assert packet.k == (Fraction(59, 20), Fraction(-2))
    assert packet.p_prime_parameter == (Fraction(-1, 40), Fraction(9, 40))
    assert points["p"].x == (Fraction(59, 20), Fraction(-2))
    assert points["p"].y == (Fraction(0), Fraction(0))
    assert points["q"].x == (Fraction(-2), Fraction(2))
    assert points["r"].y == (Fraction(-59, 20), Fraction(2))
    assert points["s"].y == (Fraction(2), Fraction(-2))
    assert points["p_prime"].x == (Fraction(-779, 800), Fraction(571, 800))
    assert points["p_prime"].y == (Fraction(779, 800), Fraction(-171, 800))
    assert points["r_prime"].x == (Fraction(-779, 800), Fraction(171, 800))
    assert points["r_prime"].y == (Fraction(779, 800), Fraction(-571, 800))
    assert points["i_candidate"].x == (Fraction(-19, 40), Fraction(0))
    assert points["i_candidate"].y == (Fraction(19, 40), Fraction(0))
    assert packet.corrected_pr_length == (Fraction(-4), Fraction(59, 20))
    assert packet.pr_length_squared == (Fraction(6681, 200), Fraction(-118, 5))
    assert packet.diagonal_delta.x == (Fraction(0), Fraction(1, 2))
    assert packet.diagonal_delta.y == (Fraction(0), Fraction(1, 2))
    assert packet.diagonal_length_squared == (Fraction(1), Fraction(0))
    assert packet.midpoint_residual.x == (Fraction(0), Fraction(0))
    assert packet.midpoint_residual.y == (Fraction(0), Fraction(0))
    assert packet.radius_symmetry_residual == (Fraction(0), Fraction(0))
    assert packet.radius_squared_margin == (
        Fraction(-354483, 320000),
        Fraction(148029, 160000),
    )
    assert packet.conclusion == "figure-4-coordinate-prerequisite-only"
    replay_figure4_coordinate_packet(packet)


def test_figure4_coordinate_packet_has_literal_upper_endpoint_oracle() -> None:
    packet = derive_figure4_coordinate_packet((Fraction(1, 3), Fraction(-1, 6)))
    points = dict(packet.points)

    assert packet.h == (Fraction(2, 3), Fraction(1, 6))
    assert packet.k == (Fraction(8, 3), Fraction(-11, 6))
    assert packet.p_prime_parameter == (Fraction(0), Fraction(1, 6))
    assert points["p_prime"].x == (Fraction(-11, 18), Fraction(4, 9))
    assert points["p_prime"].y == (Fraction(11, 18), Fraction(1, 18))
    assert points["r_prime"].x == (Fraction(-11, 18), Fraction(-1, 18))
    assert points["r_prime"].y == (Fraction(11, 18), Fraction(-4, 9))
    assert points["i_candidate"].x == (Fraction(-1, 3), Fraction(-1, 12))
    assert points["i_candidate"].y == (Fraction(1, 3), Fraction(1, 12))
    assert packet.corrected_pr_length == (Fraction(-11, 3), Fraction(8, 3))
    assert packet.radius_squared_margin == (Fraction(-23, 108), Fraction(25, 81))
    replay_figure4_coordinate_packet(packet)


@pytest.mark.parametrize(
    "epsilon",
    [
        (Fraction(0), Fraction(0)),
        (Fraction(1, 2), Fraction(0)),
    ],
)
def test_figure4_coordinate_packet_rejects_out_of_domain_epsilon(
    epsilon: tuple[Fraction, Fraction],
) -> None:
    with pytest.raises(ElMoumniSourceControlError) as caught:
        derive_figure4_coordinate_packet(epsilon)
    assert caught.value.kind == "figure4-epsilon-domain"


@pytest.mark.parametrize("epsilon", [(1, 0), (True, False), (0.05, 0.0)])
def test_figure4_coordinate_packet_rejects_inexact_epsilon(epsilon: object) -> None:
    with pytest.raises(ElMoumniSourceControlError) as caught:
        derive_figure4_coordinate_packet(epsilon)  # pyright: ignore[reportArgumentType]
    assert caught.value.kind == "exact-control-input-required"


def test_figure4_coordinate_packet_rejects_printed_segment_mutation() -> None:
    packet = derive_figure4_coordinate_packet((Fraction(1, 20), Fraction(0)))
    printed = (Fraction(-81, 20), Fraction(2))

    with pytest.raises(ElMoumniSourceControlError) as caught:
        replay_figure4_coordinate_packet(replace(packet, corrected_pr_length=printed))
    assert caught.value.kind == "figure4-segment-identity"


def test_figure4_coordinate_packet_rejects_source_point_role_swap() -> None:
    packet = derive_figure4_coordinate_packet((Fraction(1, 20), Fraction(0)))
    points = dict(packet.points)
    mutated = tuple(
        (
            label,
            points["q"] if label == "p" else points["p"] if label == "q" else point,
        )
        for label, point in packet.points
    )

    with pytest.raises(ElMoumniSourceControlError) as caught:
        replay_figure4_coordinate_packet(replace(packet, points=mutated))
    assert caught.value.kind == "figure4-source-point"


def test_figure4_coordinate_packet_rejects_diagonal_mutation() -> None:
    packet = derive_figure4_coordinate_packet((Fraction(1, 20), Fraction(0)))
    points = dict(packet.points)
    mutated = tuple(
        (
            label,
            points["r_prime"]
            if label == "p_prime"
            else points["p_prime"]
            if label == "r_prime"
            else point,
        )
        for label, point in packet.points
    )

    with pytest.raises(ElMoumniSourceControlError) as caught:
        replay_figure4_coordinate_packet(replace(packet, points=mutated))
    assert caught.value.kind == "figure4-diagonal-construction"


def test_figure4_coordinate_packet_rejects_midpoint_mutation() -> None:
    packet = derive_figure4_coordinate_packet((Fraction(1, 20), Fraction(0)))
    points = dict(packet.points)
    mutated = tuple(
        (
            label,
            points["a_prime"]
            if label == "i_candidate"
            else points["i_candidate"]
            if label == "a_prime"
            else point,
        )
        for label, point in packet.points
    )

    with pytest.raises(ElMoumniSourceControlError) as caught:
        replay_figure4_coordinate_packet(replace(packet, points=mutated))
    assert caught.value.kind == "figure4-midpoint-role"


def test_figure4_coordinate_packet_rejects_non_tuple_point_record() -> None:
    packet = derive_figure4_coordinate_packet((Fraction(1, 20), Fraction(0)))

    with pytest.raises(ElMoumniSourceControlError) as caught:
        replay_figure4_coordinate_packet(
            replace(
                packet,
                points=list(packet.points),  # pyright: ignore[reportArgumentType]
            )
        )
    assert caught.value.kind == "figure4-source-point"


def test_figure4_coordinate_packet_rejects_broadened_claim_boundary() -> None:
    packet = derive_figure4_coordinate_packet((Fraction(1, 20), Fraction(0)))

    with pytest.raises(ElMoumniSourceControlError) as caught:
        replay_figure4_coordinate_packet(
            replace(packet, promotion_boundary="the complete theorem is proved")
        )
    assert caught.value.kind == "figure4-claim-boundary"


@pytest.mark.parametrize(
    ("preserve_minimum", "required_contributions"),
    [(1, 3), (True, True), (True, 3.0)],
)
def test_inexact_or_boolean_control_inputs_reject(
    preserve_minimum: object, required_contributions: object
) -> None:
    with pytest.raises(ElMoumniSourceControlError) as caught:
        prove_case1_minimum_repair(
            preserve_minimum=preserve_minimum,  # pyright: ignore[reportArgumentType]
            required_contributions=required_contributions,  # pyright: ignore[reportArgumentType]
        )
    assert caught.value.kind == "exact-control-input-required"
