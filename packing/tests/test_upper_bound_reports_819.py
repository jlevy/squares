"""Amund Kristiansen's issue #819: the intake records of 26 October 2026 (think-p7cq).

One dilation certificate in Evan Daniel's text format at 344, beyond the ``n <= 324`` case
corpus, retained under the CC0 1.0 dedication the gist and the issue state and read by the
`evand-cert` adapter: a beyond-horizon row of the source register that supersedes Francisco
Couzo's 964ee2b row there. The general importer's checks run on the packet through
``test_upper_bound_reports``; these hold what is particular to it: the digests and side
the issue prints, the walk's verdict, the row and what it supersedes, the replay's
margins, the sharp controls, and the identity measured against Couzo's packing. Every test
reads the retained packet, the walk and the source register only; none needs the network.
"""

from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from devtools import check_source_coverage as coverage_check
from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from sqpack.yamlio import safe_load

PACKET = "amundsk-issue819-2026-10-25"
WALK = reports.ROOT / "campaign/issue-intake/upper-bounds-issue819-20261026"
COVERAGE = reports.REPO / "packing/frontier/source-coverage.yaml"
N = 344
#: The side the issue prints, rounded up at 12 places, and the certificate's header.
PRINTED = "18.992567544845"
EXACT = "9496283772422138783772412642309/500000000000000000000000000000"
#: The row on main 5c50803d6 at 344, which this one supersedes.
SUPERSEDED = "couzo-964ee2b-2026-10-23"


def _packet() -> Path:
    return reports.packet_path(PACKET)


def _manifest() -> dict[str, str]:
    text = (_packet() / "acquisition/upstream-subtree.sha256").read_text("utf-8")
    return {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }


def test_the_packet_retains_the_gists_three_files_under_cc0() -> None:
    manifest = _manifest()
    assert sorted(manifest) == ["README.md", "s344_amund.cert", "s344_amund.input.txt"]
    record = json.loads((_packet() / "acquisition/sources.json").read_text("utf-8"))
    (source,) = record["sources"]
    assert source["source_commit"] == "f916f69f0ae570935991440712a08ad930469da3"
    assert source["retained_file_count"] == 3
    assert source["pinned_only"] == []
    assert source["license"].startswith("CC0 1.0")
    folder = reports.REPO / source["archived_path"]
    for name, digest in manifest.items():
        assert hashlib.sha256((folder / name).read_bytes()).hexdigest() == digest
    assert "CC0 1.0" in (folder / "README.md").read_text("utf-8")


def test_the_certificate_has_the_digests_and_the_side_the_issue_prints() -> None:
    body = json.loads((_packet() / "acquisition/issue.json").read_text("utf-8"))["body"]
    manifest = _manifest()
    assert manifest["s344_amund.cert"] in body
    assert manifest["s344_amund.input.txt"] in body
    assert EXACT in body
    (certificate,) = reports.read_facts(_packet()).values()
    assert certificate.side == Fraction(EXACT)
    ceiling = Fraction(math.ceil(Fraction(EXACT) * 10**12), 10**12)
    assert ceiling == Fraction(Decimal(PRINTED))


def test_the_walk_records_the_row_below_964ee2b_and_goebel() -> None:
    declaration = reports.load_declaration(_packet())
    assert declaration["requested"] == declaration["replayed"] == [N]
    assert declaration["houses"] == []
    ledger = json.loads((WALK / "ledger.json").read_text("utf-8"))
    (count,) = ledger["counts"]
    (step,) = count["steps"]
    assert (count["n"], step["report"], step["verdict"]) == (N, "#819", "recorded")
    (row,) = reports.check_claims(_packet())["results"]
    assert row["case"] is None
    assert row["smallest"] == reports.THIS
    assert row["construction"]["relation"] == "below"
    assert [(other["report"], other["relation"]) for other in row["pending"]] == [
        (SUPERSEDED, "below")
    ]


def test_the_row_supersedes_964ee2bs_row_and_reads_its_claims_record() -> None:
    claims = coverage_check.load_claims(_packet() / reports.BEYOND)
    assert claims == {N: PRINTED}
    coverage = safe_load(COVERAGE.read_text(encoding="utf-8"))
    current = coverage_check.current_beyond_horizon(coverage)
    assert (current[N]["source_id"], current[N]["value"]) == (PACKET, PRINTED)
    rows = {row["source_id"]: row for row in coverage["beyond_horizon_claims"] if row["n"] == N}
    assert rows[SUPERSEDED]["disposition"] == "superseded"
    assert rows[SUPERSEDED]["superseded_by"] == PACKET


def test_the_replay_clears_walls_and_pairs_by_the_margins_a_dilation_gives() -> None:
    margins = reports.margins(reports.check_certification(_packet()))
    assert list(margins) == [N]
    for route in ("exact_verify", "independent"):
        assert Fraction(margins[N][f"{route}_containment_clearance"]) >= Fraction(605, 10**15)
        assert Fraction(margins[N][f"{route}_best_pair_gap"]) >= Fraction(121, 10**14)


def test_the_retained_sharp_controls_are_as_expected() -> None:
    record = json.loads((_packet() / "receipts/sharp-controls.json").read_text("utf-8"))
    assert record["all_as_expected"] is True
    assert Fraction(record["epsilon"]) == kernel.SHARP_EPSILON
    assert (record["packet"], record["n"]) == (PACKET, N)


def test_the_identity_finds_another_arrangement_than_964ee2bs() -> None:
    """The issue counts 67 squares beyond a tenth under its matching; the optimal
    assignment here, best under symmetry 5, moves 82, and nearest centres pair the two
    packings under no symmetry. Either way it is not a refinement of Couzo's packing."""
    record = json.loads((_packet() / "measure/identity-n344.json").read_text("utf-8"))
    (pair,) = record["pairs"]
    assert pair["against"] == "964ee2b"
    assert pair["nearest_centre"]["one_to_one"] is False
    assert pair["assignment"]["symmetry"] == 5
    assert pair["assignment"]["moved_beyond"]["1e-1"] == 82
    tilted = {name: tilts["tilted_beyond_1_degree"] for name, tilts in record["tilts"].items()}
    assert tilted == {"#819": 114, "964ee2b": 125}
