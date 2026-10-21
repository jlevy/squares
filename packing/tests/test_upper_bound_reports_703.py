"""Evan Daniel's issue #703: the #703 lane of 21 October 2026.

One certificate in the author's own text format, retained under the MIT licence and read
by the `evand-cert` adapter: s(270) of #703 at ``88385ab``. The general importer's checks
run on the packet through ``test_upper_bound_reports``; these hold what is particular to
it, as the stage 4 review of 19 October asked of the imports before it (RV-1 of
docs/project/reviews/review-2026-10-19-upper-bound-imports-659-664-669-674.md): the
digests the issue prints, how the side was made, that it is below every report at 270 by
the margin the records state, and that the house reader rebuilds it. Every test reads the
retained packet only; none needs the network.
"""

from __future__ import annotations

import hashlib
import math
import re
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import upper_bound_reports as reports

CANDIDATES = "search/packer/candidates"
PACKET = "evand-n270-sweep-2026-10-20"
N = 270
KEY = "[Daniel n270 sweep 2026-10-20]"
STEM = "s270_sw"
SIDE = Fraction(16928162252196750114897964982713, 10**30)
#: The SHA-256 digests issue #703 prints for the certificate and its regularized view.
PRINTED_DIGESTS = {
    f"{STEM}.cert": "a01114af338f092232c0b7de07bfd164a636ef6355e15259c7fcb5812aa6034f",
    f"{STEM}_regularized.cert": (
        "776433d8e89b43727dc9da72096fb581b8f4ec4c619732c637bc0d14be8bad30"
    ),
}
#: The two literal forms the format's comment line names: an integer or ``p/q``. The
#: `evand-cert` adapter also reads a plain decimal exactly (control F1 of the 21 October
#: review, A4); the retained certificates use neither that nor anything else, so a decimal
#: in a later import of this format is noticed here rather than read in silence.
LITERAL = re.compile(r"-?\d+(?:/[1-9]\d*)?")
#: The certificate's margin below T-174, the case ceiling it would replace, bracketed in
#: units of 10^-12.
MARGIN = ("T-174", 34_741_132, 34_741_133)


def _folder() -> Path:
    packet = reports.packet_path(PACKET)
    return reports.REPO / reports.acquisition(packet)["archived_path"] / CANDIDATES


def _row() -> dict[str, Any]:
    (row,) = (
        row
        for row in reports.check_claims(reports.packet_path(PACKET))["results"]
        if row["n"] == N
    )
    return row


def _ceil_at(value: Fraction, places: int) -> Fraction:
    return Fraction(math.ceil(value * 10**places), 10**places)


def test_the_retained_certificates_have_the_digests_the_issue_prints() -> None:
    for name, digest in PRINTED_DIGESTS.items():
        assert hashlib.sha256((_folder() / name).read_bytes()).hexdigest() == digest


def test_the_certificate_states_its_side_and_the_house_reader_rebuilds_it() -> None:
    (certificate,) = reports.read_facts(reports.packet_path(PACKET)).values()
    assert (certificate.n, certificate.side) == (N, SIDE)
    assert reports.house_side(KEY, N) == SIDE
    (row,) = reports.load_declaration(reports.packet_path(PACKET))["certificates"]
    assert row["path"] == f"{CANDIDATES}/{STEM}.cert"
    assert row["offered"] == "16.928162252197"
    assert _ceil_at(SIDE, 12) == Fraction(Decimal(row["offered"]))


def test_the_side_is_its_kkt_point_scaled_by_1e20_and_rounded_up_at_30_places() -> None:
    head = (_folder() / f"{STEM}.exact.txt").read_text("utf-8").split("\n")[0]
    count, kkt = head.split()
    assert int(count) == N
    assert _ceil_at(Fraction(Decimal(kkt)) * (1 + Fraction(1, 10**20)), 30) == SIDE
    regularized = (_folder() / f"{STEM}_regularized.cert").read_bytes()
    assert reports.evand_cert(regularized, N, {}).side == SIDE


def test_the_certificate_is_below_its_case_and_every_report_it_names() -> None:
    row = _row()
    assert row["smallest"] == reports.THIS
    assert row["case"]["relation"] == "below"
    assert {other["relation"] for other in row["pending"]} == {"below"}
    house, low, high = MARGIN
    assert row["case"]["result"] == house
    assert Fraction(low, 10**12) < Fraction(row["case"]["difference"]) < Fraction(high, 10**12)


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
