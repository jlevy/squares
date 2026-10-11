"""The independent check of Ryu's Theorem 1.6 certificate at k = 10^5, and its controls.

The certificate is the one the 2026-10-09 packet retains; the two largest are hosted and
are decided by the tool's own runs, recorded in that packet's receipts.
"""

from __future__ import annotations

import gzip
from pathlib import Path

import pytest

from cases.asymptotic import ryu_upper_certificates as certificates
from cases.asymptotic.ryu_upper_certificates import (
    MUTATIONS,
    RETAINED,
    certificate_path,
    check_certificate,
    load,
)

K = 100000


@pytest.fixture(scope="module")
def document_path() -> Path:
    path = certificate_path(K)
    assert path == RETAINED / "stair_k100000.json.gz"
    return path


def test_the_k_10_5_certificate_gives_c_star_at_most_1583(document_path: Path) -> None:
    report = check_certificate(load(document_path), K)
    assert report.passed
    assert report.matches_table_2
    assert (report.b, report.y0, report.squares, report.deficit) == (
        623,
        "257/4",
        9999998416,
        1584,
    )
    assert report.rows == {"right": 99868, "top": 99245}
    assert report.waste_identity
    assert report.box_pairs == 22274
    assert report.bound == "c*(100000) <= 1583"
    assert [end.pieces for end in report.ends] == [719, 725, 719, 724]


@pytest.mark.parametrize("scope", ["whole", "first-end"])
@pytest.mark.parametrize("mutation", sorted(MUTATIONS))
def test_every_control_is_refused(document_path: Path, mutation: str, scope: str) -> None:
    first_end_only = scope == "first-end"
    report = check_certificate(load(document_path), K, mutation, first_end_only=first_end_only)
    assert not report.passed
    assert report.bound == "none"


def test_the_first_end_alone_passes_but_bounds_nothing(document_path: Path) -> None:
    report = check_certificate(load(document_path), K, first_end_only=True)
    assert report.passed
    assert len(report.ends) == 1
    assert report.bound == "none"


def test_a_certificate_for_another_k_is_refused(document_path: Path) -> None:
    with pytest.raises(ValueError, match="not 1000000"):
        check_certificate(load(document_path), 1000000)


def test_decompression_is_bounded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "big.json.gz"
    path.write_bytes(gzip.compress(b" " * 4096))
    monkeypatch.setattr(certificates, "MAX_DECOMPRESSED", 1024)
    with pytest.raises(ValueError, match="decompresses past"):
        load(path)
