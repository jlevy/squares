"""A project-owned regularized house rebuilds from the certificate its run decided."""

from fractions import Fraction

import pytest

from devtools import register_candidates
from devtools import upper_bound_houses as houses
from devtools import upper_bound_reports as reports


def test_n127_project_house_rebuilds_the_registered_certificate() -> None:
    source = houses.writable_source("T-341", 127, reports.PROJECT_N127_KEY, algebraic=False)
    assert source is not None
    certificate = source.certificate(127)
    assert certificate.side == Fraction(11800793726614962238623103308879, 10**30)
    assert certificate.side == reports.house_side(source.key, 127)
    assert certificate == register_candidates.certificate(register_candidates.N127, 127)
    assert houses.source_for(127).key == source.key
    expected = houses.expected_house(127)
    assert Fraction(expected["side"]) == certificate.side
    assert expected["source"]["key"] == source.key
    assert expected["certificate"]["result"]["verification_passed"] is True


def test_project_house_refuses_a_different_copy_of_the_certified_pose() -> None:
    batch = register_candidates.N127
    raw = register_candidates.certificate_path(batch, 127).read_bytes()
    with pytest.raises(
        register_candidates.CandidateError, match="differs from the retained pose"
    ):
        register_candidates.admitted(batch, 127, raw + b"\n")


def test_n305_project_house_rebuilds_the_gmp_checked_certificate() -> None:
    source = houses.writable_source("T-342", 305, reports.PROJECT_N305_KEY, algebraic=False)
    assert source is not None
    assert source.rational_backend == "gmp"
    certificate = source.certificate(305)
    assert certificate.side == reports.house_side(source.key, 305)
    assert houses.source_for(305).key == source.key
    expected = houses.expected_house(305)
    assert Fraction(expected["side"]) == certificate.side
    assert expected["source"]["key"] == source.key
    assert expected["certificate"]["result"]["verification_passed"] is True
    assert expected["certificate"]["replay"].endswith("--rational-backend gmp")
