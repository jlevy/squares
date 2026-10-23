"""Evan Daniel's issue #728: the #728 lane of 22 October 2026.

One dilation certificate in the author's own text format, retained under the MIT licence
and read by the `evand-cert` adapter: s(303) of #728 at ``f06521f``. The general
importer's checks run on the packet through ``test_upper_bound_reports``; these hold what
is particular to it, as the stage 4 review of 19 October asked of the imports before it
(RV-1 of docs/project/reviews/review-2026-10-19-upper-bound-imports-659-664-669-674.md):
the digests the issue prints, how the side was made, that it is below every report at 303
by the margin the records state, and that the house reader rebuilds it. Every test reads
the retained packet only; none needs the network.
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
PACKET = "evand-n303-2026-10-22"
N = 303
KEY = "[Daniel n303 2026-10-22]"
STEM = "s303_r303w0"
SIDE = Fraction(447744305431858194305431410441, 25 * 10**27)
#: The SHA-256 digests issue #728 prints for the certificate and its binary64 input.
PRINTED_DIGESTS = {
    f"{STEM}.cert": "929c2acf72ee54a1850183fc149f06dbf35bffa2f7ee68c8f833d888400e8080",
    f"{STEM}.input.txt": "8167bcb37498ded1029f8fea6b13665f59806cfb0a2beb750388852452f107b7",
}
#: The dilation's delta as `dilate_cert.py` reads it: the double nearest 10^-12.
DELTA = Fraction(1e-12)
#: The two literal forms the format's comment line names: an integer or ``p/q``.
LITERAL = re.compile(r"-?\d+(?:/[1-9]\d*)?")
#: The certificate's margin below T-186, the house it would replace, bracketed in units of
#: 10^-15.
MARGIN = ("T-186", 186_073_795_580, 186_073_795_581)


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


def test_the_retained_files_have_the_digests_the_issue_prints() -> None:
    for name, digest in PRINTED_DIGESTS.items():
        assert hashlib.sha256((_folder() / name).read_bytes()).hexdigest() == digest


def test_the_certificate_states_its_side_and_the_house_reader_rebuilds_it() -> None:
    (certificate,) = reports.read_facts(reports.packet_path(PACKET)).values()
    assert (certificate.n, certificate.side) == (N, SIDE)
    assert reports.house_side(KEY, N) == SIDE
    (row,) = reports.load_declaration(reports.packet_path(PACKET))["certificates"]
    assert row["path"] == f"{CANDIDATES}/{STEM}.cert"
    assert row["offered"] == "17.909772217275"
    assert _ceil_at(SIDE, 12) == Fraction(Decimal(row["offered"]))


def test_the_side_is_its_input_side_times_1_plus_delta_rounded_up_at_30_places() -> None:
    text = (_folder() / f"{STEM}.input.txt").read_text("utf-8")
    count, side = text.split("\n")[0].split()
    assert int(count) == N
    assert Fraction(1, 10**12) != DELTA
    assert _ceil_at(Fraction(Decimal(side)) * (1 + DELTA), 30) == SIDE


def test_the_certificate_is_below_its_case_and_every_report_it_names() -> None:
    row = _row()
    assert row["smallest"] == reports.THIS
    assert row["case"]["relation"] == "below"
    assert {other["relation"] for other in row["pending"]} == {"below"}
    house, low, high = MARGIN
    assert row["case"]["result"] == house
    assert Fraction(low, 10**15) < Fraction(row["case"]["difference"]) < Fraction(high, 10**15)


def test_the_replay_clears_walls_and_pairs_by_the_margins_its_construction_gives() -> None:
    positives = reports.check_certification(reports.packet_path(PACKET))
    (margins,) = reports.margins(positives).values()
    for route in ("exact_verify", "independent"):
        assert Fraction(margins[f"{route}_containment_clearance"]) >= Fraction(6, 10**13)
        assert Fraction(margins[f"{route}_best_pair_gap"]) >= Fraction(12, 10**13)


def test_the_retained_certificate_writes_only_integer_and_fraction_literals() -> None:
    rows = [
        line.split()
        for line in (_folder() / f"{STEM}.cert").read_text("ascii").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    assert len(rows) == N + 1
    assert rows[0][0] == str(N)
    literals = [rows[0][1], *(field for row in rows[1:] for field in row)]
    assert len(literals) == 1 + 3 * N
    assert all(LITERAL.fullmatch(literal) for literal in literals)
