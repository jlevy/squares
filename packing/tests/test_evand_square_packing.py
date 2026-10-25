"""Controls for Evan Daniel's certificates, retained from ``evand/square-packing``.

The packet under ``resources/web/evand-square-packing-2026-09-26/`` holds the source's
bytes; the replays that decide coverage take minutes to hours and leave receipts. These
tests are the fast part that has to stay true: the retained bytes are the pinned ones,
each certificate is well formed with nonnegative weights, is exactly invariant under
the container's symmetry group, and weighs less than the count it excludes, and the
frontier records carry exactly the side each certificate's header states.

Coverage itself, every closed unit square capturing weight at least one, is not decided
here: that is the source checkers' sweep, replayed in the packet's receipts.

The large certificates, run records and receipts are stored as deterministic gzip; every
read goes through `read_retained_bytes`, so each digest checked is the upstream one.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import pytest

from devtools.compare_evand_s32_sweep import compare
from devtools.retained_data import read_retained_bytes, read_retained_text
from sqpack.yamlio import safe_load

PACKING = Path(__file__).resolve().parents[1]
PACKET = PACKING / "resources" / "web" / "evand-square-packing-2026-09-26"
CERTIFICATES = PACKET / "square-packing" / "s12" / "certificates"
FRONTIER = PACKING / "frontier"
RECEIPTS = PACKET / "receipts"


@dataclass(frozen=True)
class Cover:
    side: Fraction
    coordinate_denominator: int
    weight_denominator: int
    points: tuple[tuple[int, int, int], ...]

    @property
    def total(self) -> Fraction:
        return Fraction(sum(w for _, _, w in self.points), self.weight_denominator)


def read_cover(path: Path) -> Cover:
    text = read_retained_text(path, encoding="ascii")
    rows = [line.split() for line in text.splitlines() if line.strip()]
    side_num, side_den = (int(v) for v in rows[0])
    denominator = int(rows[1][0])
    weight_denominator = int(rows[2][0])
    count = int(rows[3][0])
    points = tuple((int(x), int(y), int(w)) for x, y, w in rows[4:])
    assert len(points) == count
    return Cover(Fraction(side_num, side_den), denominator, weight_denominator, points)


#: (file, n, side, total weight): the values the frontier records and the packet state.
CLAIMS = (
    ("s32/s32_closed_cover_6.txt", 32, Fraction(6), Fraction(3171350535386, 10**11)),
    ("s12_lower_3.9686.txt", 12, Fraction(15680, 3951), Fraction(119738036, 10**7)),
    ("s21/s21_lower_4.9950.txt", 21, Fraction(5000, 1001), Fraction(260057, 12500)),
)


def test_retained_bytes_match_the_packet_manifest() -> None:
    lines = (PACKET / "retained-files.sha256").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 56
    for line in lines:
        digest, path = line.split("  ", 1)
        data = read_retained_bytes(PACKET / path)
        assert hashlib.sha256(data).hexdigest() == digest, path


@pytest.mark.parametrize(("name", "n", "side", "total"), CLAIMS)
def test_certificate_is_well_formed_symmetric_and_light(
    name: str, n: int, side: Fraction, total: Fraction
) -> None:
    cover = read_cover(CERTIFICATES / name)
    assert cover.side == side
    assert cover.total == total
    assert cover.total < n
    extent = cover.side * cover.coordinate_denominator
    assert extent.denominator == 1
    edge = extent.numerator
    weights: Counter[tuple[int, int]] = Counter()
    for x, y, w in cover.points:
        assert 0 <= x <= edge
        assert 0 <= y <= edge
        assert w >= 0
        weights[(x, y)] += w
    # The weighted multiset is invariant under the reflection x -> edge - x and the
    # diagonal swap, which generate the square's eight symmetries.
    assert weights == Counter({(edge - x, y): w for (x, y), w in weights.items()})
    assert weights == Counter({(y, x): w for (x, y), w in weights.items()})


def _case(n: int) -> dict:
    text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    return safe_load(text.split("---\n")[1])["packing"]


#: The claims whose certified side the frontier still carries. s(21) >= 5000/1001 was the
#: n = 21 bound until the same source's mixed cover proved s(21) = 5 on 2026-09-29; its
#: certificate stays above as a well-formed control, and the test below holds the value.
#: s(12) >= 15680/3951 was the n = 12 bound until squarepacker's rescaling of the same
#: certificate by 7902/7901 replaced it on 2026-10-03 (T-078), which the test after the
#: next holds.
CURRENT_CLAIMS = tuple(claim for claim in CLAIMS if claim[1] not in (12, 21))


@pytest.mark.parametrize(("name", "n", "side", "total"), CURRENT_CLAIMS)
def test_frontier_records_the_certified_side(
    name: str, n: int, side: Fraction, total: Fraction
) -> None:
    del name, total
    case = _case(n)
    verified = case["verified_lower_bound"]
    assert Fraction(verified["exact_form"]) == side
    assert any("evand" in e for e in verified["evidence"])
    assert case["reported_lower_bound"]["source_key"] == "[evand square-packing 2026]"


def test_the_n12_bounds_are_daniels_points_rescaled() -> None:
    """Every verified n = 12 lower bound since T-049 keeps Daniel's points at a larger
    side: the frontier verifies squarepacker's v1.1, the points dilated by
    31382793/31360000 and re-weighted (T-095, since 5 October 2026). Before it the
    verified bound was this project's re-weighting at a side scaled by 3951000/3949423
    (T-079, from 3 October). The reported bound was the same lineage, T-078's whole
    certificate times 7902/7901 and then T-095's, until T-243's reported Lean proof that
    s(12) = 4 took the reported lane on 25 October 2026; it is not Daniel's points."""
    (side,) = (claim[2] for claim in CLAIMS if claim[1] == 12)
    case = _case(12)
    verified = case["verified_lower_bound"]
    assert Fraction(verified["exact_form"]) == side * Fraction(31382793, 31360000)
    assert verified["evidence"] == [
        "E-n012-squarepacker-7943-2000-source-replay",
        "E-n012-squarepacker-7943-2000-native-parent-core",
    ]
    evidence = {
        entry["id"]: entry
        for entry in safe_load((FRONTIER / "evidence.yaml").read_text(encoding="utf-8"))[
            "evidence"
        ]
    }
    for key in verified["evidence"]:
        assert evidence[key]["source_key"] == "[squarepacker s12 2026-10-05]", key
    reported = case["reported_lower_bound"]
    assert reported["source_key"] == "[Jatloe n12 Lean 2026-10-16]"
    assert Fraction(reported["exact_form"]) == 4


@pytest.mark.parametrize("n", [21, 45])
def test_mixed_covers_prove_the_grid_side(n: int) -> None:
    """s(21) = 5 and s(45) = 7: the verified lower bound meets the grid's upper bound.

    Both rest on Daniel's mixed covers of 2026-09-28, replayed here by zmx2; the upper
    bound is the trivial grid in each case.
    """
    case = _case(n)
    assert case["status"] == "proved"
    assert case["reported_status"] == "proved"
    grid = case["verified_upper_bound"]
    assert grid["evidence"] == ["E-basic-grid-upper"]
    verified = case["verified_lower_bound"]
    assert Fraction(verified["exact_form"]) == Fraction(grid["exact_form"])
    assert Fraction(verified["exact_form"]) == math.isqrt(n - 1) + 1
    assert verified["evidence"] == [f"E-n{n:03d}-evand-mixed-cover-zmx2-replay"]
    reported = case["reported_lower_bound"]
    assert reported["source_key"] == "[evand square-packing 2026-09-28]"
    assert Fraction(reported["exact_form"]) == Fraction(verified["exact_form"])


def test_s32_is_proved_by_the_cover_and_the_grid() -> None:
    case = _case(32)
    assert case["status"] == "proved"
    assert case["verified_lower_bound"]["exact_form"] == "6"
    # The upper side is the trivial grid: 36 unit squares tile [0, 6]^2.
    assert case["verified_upper_bound"]["exact_form"] == "6"
    assert case["verified_upper_bound"]["evidence"] == ["E-basic-grid-upper"]


def test_native_s12_receipt_is_a_complete_clean_decision() -> None:
    """The retained native parent-core decision of the s(12) certificate is whole.

    It re-reads the receipt, not the coverage: every one of the 2,486 rows appears once in
    the journal, certified with no stalled box, on a clean commit and the pinned bytes.
    """
    receipt = json.loads((RECEIPTS / "s12_native_parent_core.json").read_text())
    assert receipt["status"] == "PASS_COMPLETE"
    assert receipt["complete"] is True
    assert receipt["refutations"] == []
    assert receipt["provenance"]["dirty"] is False
    assert (
        receipt["provenance"]["certificate_sha256"]
        == hashlib.sha256(
            read_retained_bytes(CERTIFICATES / "s12_lower_3.9686.txt")
        ).hexdigest()
    )
    lines = read_retained_text(RECEIPTS / "s12_native_parent_core.rows.jsonl").splitlines()
    rows = [json.loads(line) for line in lines[1:]]
    assert sorted(r["index"] for r in rows) == list(range(receipt["catalogue_rows"]))
    assert receipt["catalogue_rows"] == 2486
    for row in rows:
        assert row["status"] == "certified"
        assert row["stalled"] == 0
        assert not row["budget_exhausted"]
        assert int(row["lower"]) >= receipt["threshold_units"]


def test_s32_full_resweep_receipt_certifies_every_root_as_the_source_did() -> None:
    """The retained repository re-sweep of the s(32) cover is whole and agrees with the source.

    It re-reads the replay's per-root records, not the coverage: every one of the 7,200
    roots of the D4 region has a certified record from the pinned checker on the pinned
    cover, and every record at a depth the source also ran carries the source's census.
    """
    result = compare(
        CERTIFICATES / "s32" / "zeromargin_d4" / "roots.jsonl",
        RECEIPTS / "s32_zeromargin_roots.jsonl",
    )
    assert result["roots_in_region"] == 7200
    assert result["replay_roots"] == 7200
    assert result["missing_roots"] == 0
    assert result["extra_roots"] == []
    assert result["roots_uncertified_in_every_replay_record"] == []
    assert result["records_whose_census_differs"] == []
    assert result["records_at_a_depth_the_source_did_not_run"] == []
    assert result["records_with_census_identical_to_source"] == result["replay_records"]
    assert result["checker_sha256"] == [
        "640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab"
    ]
    cover = read_retained_bytes(CERTIFICATES / "s32" / "s32_closed_cover_6.txt")
    assert result["certificate_sha256"] == [hashlib.sha256(cover).hexdigest()]
    recorded = json.loads((RECEIPTS / "s32_sweep_comparison.json").read_text())
    assert recorded["replay_records_sha256"] == result["replay_records_sha256"]
