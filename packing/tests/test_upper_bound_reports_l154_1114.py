"""The upper-bound imports of the intake pass's lane L154 of 14 November 2026 (think-g2ax).

Two packets from Joost de Winter's watched repository JoostdeWinter/square-packing. The
first retains n297/ at 7b4701f, which #977 names: a packing of 297 squares in T-174's
layout with a double step in each staircase, as a Witness/v2 whose verified claim names no
certificate, read by the ``witness-center-basis-unreplayed`` adapter, with the same packing
as JSON. The second retains above324_from_n297/ at c70defa, which #979 names: that packing
with a border at 332 and an L-border and a corner of ten squares at 409, beyond the
corpus, read by the ``center-direction-json`` adapter. The general importer's checks run on
each packet through ``test_upper_bound_reports``; these hold what is particular to them:
the stated digests, each print against its exact side, the 332 and 409 sides as the 297
side plus 1 and plus 3, the house and rows each is compared with, the ledger's verdicts,
the retained sharp controls, the identity measurements and the contraction margins the
records cite. Every test reads the packets and the ledger only; none needs the network.
"""

from __future__ import annotations

import json
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
import yaml

from devtools import evand_arrangement_reports as kernel
from devtools import goebel_construction as goebel
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-977-979-20261114"
S297 = "de-winter-s297-upper-bound-2026-11-14"
I979 = "de-winter-issue979-2026-11-14"
PACKETS = (S297, I979)
#: Each packet's pin and the folder its scope retains.
PINS = {
    S297: ("7b4701f35e815301e4f467d214fab4205ded5eb1", "n297"),
    I979: ("c70defaf39af47db220d1e7c2922590637ffb664", "above324_from_n297"),
}
#: Each count's 12-place print, as the issues print it, and its side rounded up at 16
#: places, as its claim record prints it.
PRINTS = {297: "17.739455558289", 332: "18.739455558289", 409: "20.739455558289"}
CEILINGS = {297: "17.7394555582889518", 332: "18.7394555582889518", 409: "20.7394555582889518"}
#: Each count's predecessor, the side it is compared with, and the gain to four figures.
PREDECESSORS = {
    297: ("T-174", "9.617e-04"),
    332: ("couzo-02f9690-2026-10-09", "9.617e-04"),
    409: ("tymchishin-reclosure-v3-2026-10-23", "9.617e-04"),
}


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _manifest(name: str) -> dict[str, str]:
    text = (reports.packet_path(name) / "acquisition/upstream-subtree.sha256").read_text(
        "utf-8"
    )
    return {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }


def _up(side: Fraction, places: int) -> Fraction:
    return Fraction(math.ceil(side * 10**places), 10**places)


def _sides() -> dict[int, Fraction]:
    sides: dict[int, Fraction] = {}
    for name in PACKETS:
        sides.update(
            {n: c.side for n, c in reports.read_facts(reports.packet_path(name)).items()}
        )
    return sides


@pytest.mark.parametrize("name", PACKETS)
def test_each_folder_s_stated_digests_hold_for_the_files_at_the_pin(name: str) -> None:
    pin, folder = PINS[name]
    record = _json(reports.packet_path(name) / "acquisition/sources.json")
    (source,) = record["sources"]
    assert source["source_commit"] == pin
    manifest = _manifest(name)
    stated = reports.packet_path(name) / f"source/{folder}/SHA256SUMS"
    rows = [line.split() for line in stated.read_text("utf-8").splitlines()]
    in_folder = {
        path.removeprefix(f"{folder}/") for path in manifest if path.startswith(folder)
    }
    assert {path for _digest, path in rows} == in_folder - {"SHA256SUMS"}
    for digest, path in rows:
        assert manifest[f"{folder}/{path}"] == digest


def test_the_297_witness_is_refused_by_the_loader_on_its_claim_alone() -> None:
    """The source's Witness/v2 passes the schema and every semantic rule but one: its claim
    is ``verified`` with no certificate record. The strict reader refuses it, and the
    unreplayed reader reads it as the same packing as the JSON."""
    folder = reports.packet_path(S297) / "source/n297"
    raw = (folder / "n297_witness.yaml").read_bytes()
    with pytest.raises(reports.ReportError, match="replayable certificate record"):
        reports.parse_certificate(raw, 297, "witness-center-basis")
    witness = reports.parse_certificate(raw, 297, "witness-center-basis-unreplayed")
    exact = reports.read_retained_bytes(folder / "n297_exact.json")
    assert reports.parse_certificate(exact, 297, "center-direction-json") == witness
    document = yaml.safe_load(raw)
    assert document["witness"]["claim"]["coordinate_provenance"] == "verified"
    assert "certificate" not in document["witness"]


def test_the_unreplayed_reader_refuses_a_replayable_or_otherwise_invalid_witness() -> None:
    """It reads past the one rule only: a document with any other problem, or none, is
    refused, so the strict reader stays the one for a valid witness."""
    raw = (reports.packet_path(S297) / "source/n297/n297_witness.yaml").read_bytes()
    document = yaml.safe_load(raw)
    unclaimed = {
        **document,
        "witness": {
            **document["witness"],
            "claim": {**document["witness"]["claim"], "coordinate_provenance": "reported"},
        },
    }
    text = yaml.safe_dump(unclaimed, sort_keys=False).encode()
    assert reports.parse_certificate(text, 297, "witness-center-basis") is not None
    with pytest.raises(reports.ReportError, match="replayable; read it as such"):
        reports.parse_certificate(text, 297, "witness-center-basis-unreplayed")
    bad = {
        **document,
        "witness": {
            **document["witness"],
            "coordinates": {**document["witness"]["coordinates"], "angle_unit": "degrees"},
        },
    }
    with pytest.raises(reports.ReportError, match="not a valid witness"):
        reports.parse_certificate(
            yaml.safe_dump(bad, sort_keys=False).encode(),
            297,
            "witness-center-basis-unreplayed",
        )


def test_each_print_is_its_exact_side_rounded_up_and_the_borders_add_one_and_three() -> None:
    sides = _sides()
    assert sorted(sides) == [297, 332, 409]
    for n, side in sides.items():
        assert _up(side, 12) == Fraction(Decimal(PRINTS[n]))
        assert _up(side, 16) == Fraction(Decimal(CEILINGS[n]))
    assert sides[332] == sides[297] + 1
    assert sides[409] == sides[297] + 3


def test_297_is_below_t174_and_the_rows_at_332_and_409() -> None:
    sides = _sides()
    (row,) = reports.check_claims(reports.packet_path(S297))["results"]
    assert (row["n"], row["smallest"], row["case"]["relation"]) == (297, reports.THIS, "below")
    assert row["case"]["result"] == "T-174"
    assert f"{float(Fraction(row['case']['difference'])):.3e}" == PREDECESSORS[297][1]
    beyond = reports.check_claims(reports.packet_path(I979))["results"]
    for claim in beyond:
        n = claim["n"]
        assert claim["smallest"] == reports.THIS
        (pending,) = claim["pending"]
        assert pending["report"] == PREDECESSORS[n][0]
        gap = Fraction(Decimal(pending["printed"])) - sides[n]
        assert f"{float(gap):.3e}" == PREDECESSORS[n][1]


def test_332_and_409_are_below_goebel_s_construction() -> None:
    """Neither row is above the classical construction, so each holds its count."""
    sides = _sides()
    for n in (332, 409):
        assert goebel.sign(sides[n], goebel.side(n)) < 0


def test_the_ledger_records_each_claim_as_a_new_packing() -> None:
    ledger = _json(LEDGER / "ledger.json")
    recorded: dict[int, list[str]] = {}
    for count in ledger["counts"]:
        for claim in count["steps"]:
            if claim["verdict"] == "recorded":
                recorded.setdefault(count["n"], []).append(claim["report"])
                assert claim["packing"]["kind"] == "new packing"
    assert recorded == {297: ["#977"], 332: ["#979"], 409: ["#979"]}
    times = {report["report"]: report["reported_at"] for report in ledger["reports"]}
    assert times == {"#977": "2026-11-14T10:13:18Z", "#979": "2026-11-14T10:41:23Z"}
    first = {count["n"]: count["steps"][0]["first_committed"] for count in ledger["counts"]}
    assert first == {
        297: "2026-11-14T10:02:54Z",
        332: "2026-11-14T10:39:38Z",
        409: "2026-11-14T10:39:38Z",
    }


@pytest.mark.parametrize("name", PACKETS)
def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it(name: str) -> None:
    receipts = reports.packet_path(name) / "receipts"
    counts = reports.load_declaration(reports.packet_path(name))["replayed"]
    paths = (
        [receipts / "sharp-controls.json"]
        if len(counts) == 1
        else [receipts / f"sharp-controls-n{n:03d}.json" for n in counts]
    )
    for n, path in zip(counts, paths, strict=True):
        record = _json(path)
        assert (record["n"], record["packet"], record["all_as_expected"]) == (n, name, True)
        assert record["epsilon"] == str(kernel.SHARP_EPSILON)
        assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
        for row in record["controls"]:
            assert row["as_expected"] is True
            assert set(row["routes"]) == set(kernel.ROUTES)


#: Each count's identity measurement: the packet, the receipt, the label it is measured
#: against, the squares the optimal assignment moves beyond a tenth, and the squares tilted
#: beyond a degree in the new packing and in the other.
IDENTITY: dict[int, tuple[str, str, str, int, tuple[int, int]]] = {
    297: (S297, "identity.json", "T-174", 55, (110, 107)),
    332: (I979, "identity-n332.json", "couzo-02f9690", 94, (110, 107)),
    409: (I979, "identity-n409.json", "tymchishin-reclosure-v3", 262, (111, 108)),
}


@pytest.mark.parametrize("n", sorted(IDENTITY))
def test_the_identity_measurement_the_records_cite(n: int) -> None:
    name, receipt, against, beyond_tenth, tilted = IDENTITY[n]
    record = _json(reports.packet_path(name) / "measure" / receipt)
    assert record["n"] == n
    pair = record["pairs"][0]
    assert pair["view"] in {"DEWINTER", "DE-WINTER"}
    assert pair["against"] == against
    assert pair["nearest_centre"]["one_to_one"] is False
    assert pair["assignment"]["moved_beyond"]["1e-1"] == beyond_tenth
    tilts = record["tilts"]
    assert (
        tilts[pair["view"]]["tilted_beyond_1_degree"],
        tilts[against]["tilted_beyond_1_degree"],
    ) == tilted
    for other in record["pairs"][1:]:
        assert other["assignment"]["moved_beyond"] == pair["assignment"]["moved_beyond"]


#: Each predecessor's uniform-contraction margin, to four figures: T-174's at 297 is 0, a
#: pair touching; the rows' at 332 and 409 are their certificates' padding.
MARGINS = {
    297: (S297, "contraction-n297.json", "0.000000e+00"),
    332: (I979, "contraction-n332.json", "1.874042e-19"),
    409: (I979, "contraction-n409.json", "1.545724e-09"),
}


@pytest.mark.parametrize("n", sorted(MARGINS))
def test_each_gain_lies_outside_its_predecessor_s_padding(n: int) -> None:
    """RV-3 (think-ruu2) asks about gains inside a predecessor's padding margin; none of
    these gains is, so nothing here is held for it."""
    name, receipt, margin = MARGINS[n]
    record = _json(reports.packet_path(name) / "measure" / receipt)
    assert record["n"] == n
    assert record["margin_float"] == margin
    assert record["against"]["within_margin"] is False
    assert record["against"]["gain_float"].startswith("9.617")


def test_the_297_certificate_s_own_margin_is_the_distance_its_readme_states() -> None:
    """The README says the side is 1.8e-59 above the 330-digit solution; the certificate's
    own uniform-contraction margin is 1.824e-59, 1 - lambda* = 1e-60."""
    record = _json(reports.packet_path(S297) / "measure/contraction-n297-own.json")
    assert record["one_minus_lambda_star"] == "1.000000e-60"
    assert record["margin_float"] == "1.823946e-59"
    assert record["routes_accept"] is True
