"""A project-owned regularized house rebuilds from the certificate its run decided."""

from fractions import Fraction

import pytest

from devtools import evand_arrangement_reports as kernel
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


@pytest.mark.parametrize(
    ("batch", "result", "key"),
    [
        (register_candidates.N127, "T-341", reports.PROJECT_N127_KEY),
        (register_candidates.N305, "T-342", reports.PROJECT_N305_KEY),
    ],
)
def test_project_house_binds_receipts_to_geometry_instead_of_certificate_bytes(
    batch: register_candidates.Batch, result: str, key: str
) -> None:
    n = batch.candidates[0].n
    source = houses.project_candidate_source(result, key)
    raw = register_candidates.certificate_path(batch, n).read_bytes()
    exact = register_candidates.admitted(batch, n, raw + b"\n")
    assert exact == source.certificate(n)
    assert source.jobs(n, exact)["positive"]["n"] == n

    kind, target, mutate = houses._mutants(n)[1]  # noqa: SLF001 -- actual custody control
    assert kind == "certificate bytes"
    assert target == register_candidates.certificate_path(batch, n)
    changed = register_candidates.admitted(batch, n, mutate(raw))
    assert changed.side == exact.side
    assert changed.poses[0].x == exact.poses[0].x + 1
    assert changed.poses[1:] == exact.poses[1:]
    with pytest.raises(kernel.ReportError, match="full native deciding input differs"):
        source.jobs(n, changed)


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
