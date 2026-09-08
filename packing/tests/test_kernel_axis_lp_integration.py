"""Source-free producer packets replayed by the independent objective-bound reader."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

import pytest

from devtools import check_kernel_axis_lp as reader
from devtools import kernel_axis_lp as producer

SIDE = Fraction(7, 2)
ASYMMETRIC_SIDE = Fraction(4)
ASYMMETRIC_POSES = ((Fraction(1), Fraction(1)), (Fraction(2), Fraction(1)))
ASYMMETRIC_ALPHA = (Fraction(1, 2), Fraction(1, 2))
ASYMMETRIC_BETA = ((0, 1, Fraction(1)),)
EXPECTED_T = ((Fraction(5, 2), Fraction(3, 2)), (Fraction(3, 2), Fraction(1)))
EXPECTED_SCALARS = (Fraction(0), Fraction(1, 2), Fraction(1, 2))


@pytest.fixture(autouse=True)
def forbid_scientific_sources(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden() -> object:
        raise AssertionError("scientific factories must not run in integration controls")

    monkeypatch.setattr(producer, "scientific_source", forbidden)
    monkeypatch.setattr(reader, "scientific_source", forbidden)


def synthetic_packet() -> tuple[producer.Certificate, list[list[str]]]:
    coordinates = (Fraction(3, 4), Fraction(7, 4), Fraction(11, 4))
    poses = tuple((x, y) for x in coordinates for y in coordinates)
    packet = producer.make_certificate(
        SIDE,
        poses,
        [Fraction(1, 9)] * 9,
        [(i, j, Fraction(2, 9)) for i, j in combinations(range(9), 2)],
    )
    # Bind replay to the caller's source, not to a source copied from the packet.
    return packet, [[str(x), str(y)] for x, y in poses]


def asymmetric_packet() -> tuple[producer.Certificate, list[list[str]]]:
    """A packet whose V block and two scalar projections are all nonzero."""
    packet = producer.make_certificate(
        ASYMMETRIC_SIDE, ASYMMETRIC_POSES, ASYMMETRIC_ALPHA, ASYMMETRIC_BETA
    )
    return packet, [[str(x), str(y)] for x, y in ASYMMETRIC_POSES]


def producer_projection(
    features: list[tuple[Fraction, ...]],
) -> tuple[list[list[Fraction]], list[list[Fraction]], tuple[Fraction, ...]]:
    """Project the same weights with the producer's own definitions, not the reader's."""
    terms = [
        (weight, producer.pair_coefficients(feature, feature))
        for weight, feature in zip(ASYMMETRIC_ALPHA, features, strict=True)
    ]
    terms.extend(
        (weight, producer.pair_coefficients(features[i], features[j]))
        for i, j, weight in ASYMMETRIC_BETA
    )
    total = tuple(
        producer.bounded_sum(weight * row[k] for weight, row in terms)
        for k in range(producer.PARAMETERS)
    )
    return producer.projected_blocks(total)


def test_producer_packet_passes_independent_reader_at_nine() -> None:
    packet, poses = synthetic_packet()
    result = reader.check_synthetic_packet(
        packet, side=SIDE, poses=poses, minimum_bound=Fraction(9)
    )
    assert result["status"] == "verified_objective_bound"
    assert result["bound"] == "9"
    assert result["projected_psd_verified"] is True
    assert result["scientific_family_refuted"] is False
    assert result["new_packing_bound"] is False


def test_producer_packet_refused_at_eleven() -> None:
    packet, poses = synthetic_packet()
    with pytest.raises(reader.KernelCertificateError, match="threshold"):
        reader.check_synthetic_packet(
            packet, side=SIDE, poses=poses, minimum_bound=Fraction(11)
        )


def test_producer_packet_refused_for_changed_caller_source() -> None:
    packet, poses = synthetic_packet()
    # Keep the altered source sorted, distinct, and contained so identity is the refusal.
    poses[0][0] = "7/10"
    with pytest.raises(reader.KernelCertificateError, match="caller-bound source"):
        reader.check_synthetic_packet(packet, side=SIDE, poses=poses, minimum_bound=Fraction(9))


def test_producer_and_reader_agree_on_an_asymmetric_nonzero_v_block() -> None:
    """Pin the two conventions the D4-symmetric nine-grid control cannot see.

    At side 7/2 the nine-grid leaves the V block and all three scalars identically
    zero, so it admits a wrong block-trace factor and a wrong V-component grouping.
    Side 4 with poses (1,1) and (2,1) does not: T is [[5/2, 3/2], [3/2, 1]] and the
    scalars are (0, 1/2, 1/2). The case fails if either implementation halves or
    doubles the block trace; if either groups the four V features as (u, u v^2) and
    (v, u^2 v) instead of (u, v) and (u v^2, u^2 v), which sends T[0][0] to 1; or if
    it mixes the identically zero angular scalar with either nonzero one. The
    packet's own poses satisfy u v^2 == u^2 v, so they cannot separate those two
    features on their own; the probe pose below does, and catches a u <-> v or a
    u v^2 <-> u^2 v swap in one implementation's feature order.
    """
    packet, poses = asymmetric_packet()
    assert packet["bound"] == "2"

    producer_features = [
        producer.axis_features(ASYMMETRIC_SIDE, pose) for pose in ASYMMETRIC_POSES
    ]
    reader_features = [reader.axis_features(pose, ASYMMETRIC_SIDE) for pose in ASYMMETRIC_POSES]
    assert producer_features == reader_features

    produced_a, produced_t, produced_scalars = producer_projection(producer_features)
    projection = reader.projected_matrices(reader_features, ASYMMETRIC_ALPHA, ASYMMETRIC_BETA)
    assert tuple(tuple(row) for row in produced_t) == EXPECTED_T
    assert projection.t == EXPECTED_T
    assert tuple(produced_scalars) == EXPECTED_SCALARS
    assert projection.scalars == EXPECTED_SCALARS
    assert tuple(tuple(row) for row in produced_a) == projection.a

    result = reader.check_synthetic_packet(
        packet, side=ASYMMETRIC_SIDE, poses=poses, minimum_bound=Fraction(2)
    )
    assert result["status"] == "verified_objective_bound"
    assert result["bound"] == "2"
    # Rank two on the V block is what makes the block-trace factor observable here.
    assert result["projected_ranks"] == [1, 2]

    probe = (Fraction(1, 2), Fraction(7, 2))
    probe_features = producer.axis_features(ASYMMETRIC_SIDE, probe)
    assert probe_features == reader.axis_features(probe, ASYMMETRIC_SIDE)
    assert len(set(probe_features[7:])) == 4
