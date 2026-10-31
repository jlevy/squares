"""The register candidates of 31 October 2026 (T-261 to T-263): custody, construction, receipts.

`devtools.register_candidates` retains Evan Daniel's regularizer's views at 130 and 307,
each bound to the Git blob and exact side its run's retained report records, and builds
293 as T-257's 260 certificate plus one L strip. This holds each certificate to what the
register states, the construction to its count, the receipts to their certificates, and
refuses a view whose bytes are not the run's.
"""

from __future__ import annotations

import gzip
import json
from fractions import Fraction

import pytest

from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import register_candidates as candidates

BATCH = candidates.RUU2
#: Each candidate's exact side, as T-261, T-262 and T-263 state it, and its house's.
SIDES = {
    130: (
        Fraction(1487803830747751967474793359227, 125 * 10**27),
        Fraction(5951215322991132879306459820277, 5 * 10**29),
    ),
    293: (
        Fraction(8816991251060941991251052624833, 5 * 10**29),
        Fraction(8816991251061390991251052573823, 5 * 10**29),
    ),
    307: (
        Fraction(4494812820921068365908930695861, 25 * 10**28),
        Fraction(
            2707897969116659515550794271467451840032974544063449693,
            150612387934832692306604131393579915999000000000000000,
        ),
    ),
}


def test_each_side_is_the_registered_side_below_its_house() -> None:
    rows = {row["n"]: row for row in candidates.table(BATCH)}
    for n, (side, house) in SIDES.items():
        assert candidates.side(BATCH, n) == side
        assert side < house
        assert rows[n]["side"] == f"{side.numerator}/{side.denominator}"
    # 130 rounds to its house's 12-place print, so it is held for the owner (think-ikku);
    # 293 and 307 cross theirs.
    assert [rows[n]["same_print"] for n in (130, 293, 307)] == [True, False, False]


def test_the_l_strip_completes_the_count_and_refuses_another() -> None:
    parent = legacy.Certificate(
        1, Fraction(3, 2), (legacy.Pose(Fraction(3, 4), Fraction(3, 4), Fraction(0)),)
    )
    built = candidates.l_strip(parent, 4)
    assert built.side == Fraction(5, 2)
    assert len(built.poses) == 4
    with pytest.raises(candidates.CandidateError):
        candidates.l_strip(parent, 5)
    assert candidates.construction(BATCH, 293).n == 293


def test_a_view_that_is_not_the_runs_is_refused(tmp_path, monkeypatch) -> None:
    raw = gzip.decompress(candidates.view_path(BATCH, 307).read_bytes())
    forged = tmp_path / "views/n-307.yaml.gz"
    forged.parent.mkdir()
    forged.write_bytes(gzip.compress(raw.replace(b"id: 1\n", b"id: 1 \n", 1), mtime=0))
    monkeypatch.setattr(candidates, "view_path", lambda *_: forged)
    candidates.view.cache_clear()
    try:
        with pytest.raises(candidates.CandidateError, match="not the run's"):
            candidates.view(BATCH, 307)
    finally:
        candidates.view.cache_clear()


def test_each_receipt_holds_its_certificates_three_jobs() -> None:
    for n in SIDES:
        record = candidates.check_receipt(BATCH, n)
        assert [row["control"] for row in record["cases"]] == list(kernel.JOBS)


def test_each_sharp_control_receipt_met_its_expectations() -> None:
    for n, (side, _house) in SIDES.items():
        record = json.loads(candidates.controls_path(BATCH, n).read_text(encoding="utf-8"))
        assert record["n"] == n
        assert Fraction(record["side"]) == side
        assert record["all_as_expected"] is True
        assert {row["control"] for row in record["controls"]} == set(candidates.sharp.CONTROLS)
