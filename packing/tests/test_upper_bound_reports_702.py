"""Evan Daniel's issue #702: the #702 lane of 21 October 2026.

One certificate in the author's own text format, retained under the MIT licence and read
by the `evand-cert` adapter: s(343) of #702 at ``88385ab``, beyond the ``n <= 324`` case
corpus, so a beyond-horizon row of the source register and no register entry. The general
importer's checks run on the packet through ``test_upper_bound_reports``; these hold what
is particular to it, as the stage 4 review of 19 October asked of the imports before it
(RV-1 of docs/project/reviews/review-2026-10-19-upper-bound-imports-659-664-669-674.md):
the digests the issue prints, how the side was made, that it is below every row the
register held at 343 by the margins the records state, that the row supersedes #678's in
report order, and that the packet's own reader rebuilds it. Every test reads the retained
packet and the source register only; none needs the network.
"""

from __future__ import annotations

import hashlib
import math
import re
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import check_source_coverage as coverage_check
from devtools import upper_bound_reports as reports
from sqpack.yamlio import safe_load

CANDIDATES = "search/packer/candidates"
PACKET = "evand-n343-sweep-2026-10-20"
N = 343
STEM = "s343_sw"
SIDE = Fraction(18977682482404124568634475670459, 10**30)
PRINTED = "18.977682482405"
#: The SHA-256 digests issue #702 prints for the certificate and its regularized view.
PRINTED_DIGESTS = {
    f"{STEM}.cert": "18415455772cb1b9cdfd3b7384695ea202fb6a02291e2ede2db777e93d207dfa",
    f"{STEM}_regularized.cert": (
        "f9a147750b51bfb3d24fa5469e93aeab903bad472f8d294b15250f2c3473e2b8"
    ),
}
#: The two literal forms the format's comment line names: an integer or ``p/q``.
LITERAL = re.compile(r"-?\d+(?:/[1-9]\d*)?")
#: Each row the source register held at 343 when the issue was read, with the exact
#: margin `claims.json` records below it: #678's print, which stood, then #489's exact
#: side, which #678 had superseded, and #484's, which #489 had.
MARGINS = {
    "couzo-issue678-2026-10-18": Fraction(549722418875431365524329541, 10**30),
    "evand-record-hunt3-2026-10-10": Fraction(137510307871677774009108891, 25 * 10**28),
    "fang-two-wedge-certificates-2026-10-10": Fraction(
        666206980387357549497215734802998628885949191983887537, 2**85 * 10**30
    ),
}
#: The source this import supersedes at 343, the later one that supersedes it, and the
#: release that supersedes that one in turn.
SUPERSEDED = "couzo-issue678-2026-10-18"
LATER = "couzo-issue715-2026-10-21"
CURRENT = "mishapolk-issue732-f1ceee4-2026-10-23"
COVERAGE = reports.REPO / "packing/frontier/source-coverage.yaml"


def _folder() -> Path:
    packet = reports.packet_path(PACKET)
    return reports.REPO / reports.acquisition(packet)["archived_path"] / CANDIDATES


def _row() -> dict[str, Any]:
    (row,) = reports.check_claims(reports.packet_path(PACKET))["results"]
    assert row["n"] == N
    return row


def _ceil_at(value: Fraction, places: int) -> Fraction:
    return Fraction(math.ceil(value * 10**places), 10**places)


def test_the_retained_certificates_have_the_digests_the_issue_prints() -> None:
    for name, digest in PRINTED_DIGESTS.items():
        assert hashlib.sha256((_folder() / name).read_bytes()).hexdigest() == digest


def test_the_certificate_states_its_side_and_the_packet_reader_rebuilds_it() -> None:
    (certificate,) = reports.read_facts(reports.packet_path(PACKET)).values()
    assert (certificate.n, certificate.side) == (N, SIDE)
    assert reports.import_side(PACKET, N) == SIDE
    (row,) = reports.load_declaration(reports.packet_path(PACKET))["certificates"]
    assert row["path"] == f"{CANDIDATES}/{STEM}.cert"
    assert row["offered"] == PRINTED
    assert _ceil_at(SIDE, 12) == Fraction(Decimal(PRINTED))


def test_the_side_is_its_kkt_point_scaled_by_1e20_and_rounded_up_at_30_places() -> None:
    head = (_folder() / f"{STEM}.exact.txt").read_text("utf-8").split("\n")[0]
    count, kkt = head.split()
    assert int(count) == N
    assert _ceil_at(Fraction(Decimal(kkt)) * (1 + Fraction(1, 10**20)), 30) == SIDE
    regularized = (_folder() / f"{STEM}_regularized.cert").read_bytes()
    assert reports.evand_cert(regularized, N, {}).side == SIDE


def test_the_certificate_is_below_every_row_at_343_by_the_margins_the_records_state() -> None:
    row = _row()
    assert row["case"] is None
    assert row["grid_side"] == "19"
    assert row["smallest"] == reports.THIS
    pending = {other["report"]: other for other in row["pending"]}
    assert set(pending) == set(MARGINS)
    assert {other["relation"] for other in pending.values()} == {"below"}
    for report, margin in MARGINS.items():
        assert Fraction(pending[report]["difference"]) == margin
    # #678 is compared by its print, rounded up, so the margin holds whatever it rounds.
    assert (pending[SUPERSEDED]["printed"], pending[SUPERSEDED]["rounding"]) == (
        "18.978232204823",
        "up",
    )


def test_the_row_supersedes_678s_at_343_and_reads_its_claims_record() -> None:
    """The row superseded #678's at 343; #715's row, reported later, supersedes it in
    turn (couzo-issue715-2026-10-21), and Polkovskyi's f1ceee4 row, reported on #732 on
    23 October, supersedes #715's. The row stays listed as its source printed it."""
    claims = coverage_check.load_claims(reports.packet_path(PACKET) / reports.BEYOND)
    assert claims == {N: PRINTED}
    coverage = safe_load(COVERAGE.read_text(encoding="utf-8"))
    rows = {row["source_id"]: row for row in coverage["beyond_horizon_claims"] if row["n"] == N}
    assert rows[PACKET]["value"] == PRINTED
    assert rows[SUPERSEDED]["disposition"] == "superseded"
    assert rows[SUPERSEDED]["superseded_by"] == PACKET
    assert rows[PACKET]["disposition"] == "superseded"
    assert rows[PACKET]["superseded_by"] == LATER
    assert rows[LATER]["superseded_by"] == CURRENT
    assert coverage_check.current_beyond_horizon(coverage)[N]["source_id"] == CURRENT


def test_the_replay_clears_walls_and_pairs_by_the_margins_its_construction_gives() -> None:
    positives = reports.check_certification(reports.packet_path(PACKET))
    (margins,) = reports.margins(positives).values()
    for route in ("exact_verify", "independent"):
        assert Fraction(margins[f"{route}_containment_clearance"]) >= Fraction(1, 2 * 10**20)
        assert Fraction(margins[f"{route}_best_pair_gap"]) >= Fraction(999, 10**23)


def test_the_retained_certificates_write_only_integer_and_fraction_literals() -> None:
    for name in PRINTED_DIGESTS:
        rows = [
            line.split()
            for line in (_folder() / name).read_text("ascii").splitlines()
            if line.strip() and not line.startswith("#")
        ]
        assert len(rows) == N + 1
        assert rows[0][0] == str(N)
        literals = [rows[0][1], *(field for row in rows[1:] for field in row)]
        assert len(literals) == 1 + 3 * N
        assert all(LITERAL.fullmatch(literal) for literal in literals)
