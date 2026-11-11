"""The upper-bound import of the intake pass's lane L90 of 11 November 2026 (think-cen3).

Joost de Winter's certificates beyond the case corpus at JoostdeWinter/square-packing, in
three packets read by the ``evand-cert`` adapter: issue #941's fifteen in ``above324/`` at
``71da0d5`` (nine first committed at ``d3a020e``), issue #942's sixteen in
``above324_refined/`` at ``a9486ed``, and the six that ``a0c4fc8`` adds there, which #942's
addendum comment reports. The general importer's checks run on all three packets through
``test_upper_bound_reports``; these hold what is particular to them: the source's own
digest lists against the retained files, each print against its exact side, the row each
certificate is compared with, the ledger's verdicts, the retained sharp controls, the
contraction measurements the ledger's notes cite, and the rows: each count's current row
is this import's, at the side its source prints, and the row it beat is marked
superseded. Every test reads the packets, the ledger and the record only; none needs the
network.
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

from devtools import check_source_coverage as coverage
from devtools import upper_bound_reports as reports

P941 = "de-winter-issue941-2026-11-10"
P942 = "de-winter-issue942-2026-11-10"
PA0C = "de-winter-a0c4fc8-2026-11-10"
PACKETS = (P941, P942, PA0C)
LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-941-942-20261111"
#: Each packet's folder, report, report key in the ledger and first commits.
FOLDER = {P941: "above324", P942: "above324_refined", PA0C: "above324_refined"}
REPORT = {P941: "#941", P942: "#942", PA0C: "#942 addendum"}
D3A020E = frozenset({413, 494, 539, 543, 547, 590, 809, 810, 867})
#: The side the issue or the addendum prints at each count, rounded up at 10 places.
PRINTED = {
    P941: {
        413: "20.8239520077",
        494: "22.7365988643",
        539: "23.7365988643",
        543: "23.8024287170",
        547: "23.8787301198",
        590: "24.8024287170",
        738: "27.6912062515",
        739: "27.6912835939",
        753: "27.9026514302",
        794: "28.6912835939",
        809: "28.9079170470",
        810: "28.9079170470",
        851: "29.6912835939",
        867: "29.9079170470",
        910: "30.6912835939",
    },
    P942: {
        632: "25.6456954277",
        637: "25.7447388658",
        655: "25.9996711101",
        684: "26.6456964776",
        685: "26.6870020013",
        744: "27.7601633593",
        750: "27.8595204745",
        756: "27.9245802503",
        805: "28.8450303356",
        814: "28.9549571055",
        918: "30.7867372035",
        921: "30.8271449853",
        924: "30.8553857463",
        935: "30.9800571865",
        970: "31.6389903231",
        989: "31.8889473785",
    },
    PA0C: {
        597: "24.8969258585",
        754: "27.9075316299",
        864: "29.8530288378",
        865: "29.8693054513",
        869: "29.9122235088",
        991: "31.9019684133",
    },
}
I763, F43, R763 = (
    "couzo-issue763-2026-10-23",
    "couzo-43f666c-2026-10-24",
    "couzo-issue763-2026-10-23-recipes",
)
#: The row each certificate supersedes, by its source; 655 had none (the grid).
SUPERSEDED = {
    413: I763,
    494: I763,
    539: I763,
    543: "tymchishin-22-3662-2026-10-23",
    547: I763,
    590: I763,
    738: F43,
    739: I763,
    753: I763,
    794: I763,
    809: I763,
    810: I763,
    851: I763,
    867: F43,
    910: R763,
    632: F43,
    637: F43,
    684: F43,
    685: "tymchishin-reclosure-v3-2026-10-23",
    744: F43,
    750: I763,
    756: F43,
    805: I763,
    814: I763,
    918: F43,
    921: I763,
    924: F43,
    935: "couzo-964ee2b-2026-10-23",
    970: R763,
    989: F43,
    597: I763,
    754: F43,
    864: F43,
    865: F43,
    869: I763,
    991: F43,
}
#: Counts whose row is an L-border recipe on a parent certificate: the base count whose
#: margin the row carries.
RECIPE_BASES = {910: 851, 632: 583, 744: 691, 970: 850}
ALL = [(packet, n) for packet in PACKETS for n in PRINTED[packet]]


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _up(side: Fraction, places: int) -> Fraction:
    return Fraction(math.ceil(side * 10**places), 10**places)


def test_no_count_lies_above_the_1024_horizon_or_inside_the_corpus() -> None:
    counts = [n for _, n in ALL]
    assert len(counts) == len(set(counts)) == 37
    assert min(counts) > reports.HORIZON
    assert max(counts) <= 1024


@pytest.mark.parametrize("packet", PACKETS)
def test_the_retained_certificates_are_the_ones_the_source_digest_list_names(
    packet: str,
) -> None:
    folder = FOLDER[packet]
    root = reports.packet_path(packet)
    listed = {
        name: digest
        for digest, name in (
            line.split(maxsplit=1)
            for line in (root / f"source/{folder}/SHA256SUMS").read_text("utf-8").splitlines()
        )
    }
    manifest = {
        path.removeprefix("./"): digest
        for digest, path in (
            line.split(maxsplit=1)
            for line in (root / "acquisition/upstream-subtree.sha256")
            .read_text("utf-8")
            .splitlines()
        )
    }
    for name, digest in listed.items():
        assert manifest[f"{folder}/{name}"] == digest
    retained = {path.name for path in (root / f"source/{folder}").glob("n*.cert")}
    assert retained == {f"n{n:04d}.cert" for n in PRINTED[packet]}


@pytest.mark.parametrize("packet", PACKETS)
def test_each_print_is_its_exact_side_rounded_up_at_ten_places(packet: str) -> None:
    declaration = reports.load_declaration(reports.packet_path(packet))
    assert declaration["requested"] == declaration["replayed"] == list(PRINTED[packet])
    assert declaration["houses"] == []
    facts = reports.read_facts(reports.packet_path(packet))
    for row in declaration["certificates"]:
        n = row["n"]
        assert row["format"] == "evand-cert"
        assert row["offered"] == PRINTED[packet][n]
        assert _up(facts[n].side, 10) == Fraction(Decimal(row["offered"]))
        first = {
            P941: "2026-11-09T23:59:23Z" if n in D3A020E else "2026-11-10T06:15:17Z",
            P942: "2026-11-10T14:39:52Z",
            PA0C: "2026-11-10T15:37:44Z",
        }[packet]
        assert row["first_committed"] == first


@pytest.mark.parametrize("packet", PACKETS)
def test_each_certificate_is_below_its_row_and_goebels_construction(packet: str) -> None:
    record = reports.check_claims(reports.packet_path(packet))
    for row in record["results"]:
        n = row["n"]
        assert row["case"] is None
        assert row["smallest"] == reports.THIS
        assert row["construction"]["relation"] == "below"
        if n == 655:
            assert row["pending"] == []
            assert Fraction(row["exact_side"]) < 26
            continue
        (pending,) = row["pending"]
        assert (pending["report"], pending["relation"]) == (SUPERSEDED[n], "below")


def test_the_ledger_records_every_claim_in_report_order() -> None:
    ledger = _json(LEDGER / "ledger.json")
    verdicts = {
        (count["n"], step["report"]): step["verdict"]
        for count in ledger["counts"]
        for step in count["steps"]
    }
    assert verdicts == {(n, REPORT[packet]): "recorded" for packet, n in ALL}


@pytest.mark.parametrize(("packet", "n"), [(p, n) for p, n in ALL if n != 655])
def test_each_gain_lies_far_outside_the_row_certificates_padding(packet: str, n: int) -> None:
    """No gain here re-certifies its predecessor's padding (think-ruu2's RV-3): every
    one is at least a thousand times the row certificate's uniform-contraction margin, or
    its base's where the row is an L-border recipe."""
    base = RECIPE_BASES.get(n)
    name = f"contraction-n{n}.json" if base is None else f"contraction-n{n}-base-n{base}.json"
    record = _json(reports.packet_path(packet) / f"measure/{name}")
    margin = Fraction(record["margin"])
    if base is None:
        assert record["against"]["within_margin"] is False
        gain = Fraction(record["against"]["gain"])
    else:
        assert record["n"] == base
        gain = next(
            Fraction(row["pending"][0]["difference"])
            for row in _json(reports.packet_path(packet) / reports.CLAIMS)["results"]
            if row["n"] == n
        )
    assert gain > 1000 * margin


def test_the_rows() -> None:
    document = yaml.safe_load(coverage.COVERAGE.read_text("utf-8"))
    current = coverage.current_beyond_horizon(document)
    for packet, n in ALL:
        assert current[n]["source_id"] == packet
        assert current[n]["value"] == PRINTED[packet][n]
        assert current[n]["assurance"] == "reported"
        if n not in SUPERSEDED:
            continue
        (old,) = [
            row
            for row in document["beyond_horizon_claims"]
            if row["n"] == n and row["source_id"] == SUPERSEDED[n]
        ]
        assert (old["disposition"], old["superseded_by"]) == ("superseded", packet)
