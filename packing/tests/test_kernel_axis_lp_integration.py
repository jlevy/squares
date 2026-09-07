"""Source-free producer packets replayed by the independent objective-bound reader."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

import pytest

from devtools import check_kernel_axis_lp as reader
from devtools import kernel_axis_lp as producer

SIDE = Fraction(7, 2)


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
