"""The upper-bound import of the intake pass's lane L65 of 9 November 2026 (think-h96r).

Kaelan Yim's certificates in his watched profile repository vitamoon/vitamoon, which no
issue reports, in two packets read by the ``evand-cert`` adapter: the 14 certificates at the
head ``ac14112`` (yim-certificates-2026-11-09) and the first n303 of ``78eb9ea``, which
``546928a`` overwrote (yim-n303-2026-11-09). The general importer's checks run on both
packets through ``test_upper_bound_reports``; these hold what is particular to them: the
source's own digest list against the retained files, each print against its exact side,
the record each certificate is compared with, the ledger's verdicts, the retained sharp
controls, the identity and contraction measurements the register's notes cite, and the
holds: T-280 (299, 303) and T-281 (130) stay below the stage 4 exit for the owner
(think-ruu2's RV-3, think-ikku), at C1 with the stage 4 review mapped and no case moved,
while the eleven sides above the corpus are current, verified beyond-horizon rows. Every
test reads the packets, the ledger and the record only; none needs the network.
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
from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

MAIN = "yim-certificates-2026-11-09"
FIRST = "yim-n303-2026-11-09"
LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-yim-certificates-20261109"
SOURCE_KEY = "[Yim certificates 2026-11-09]"
REVIEW = "docs/project/reviews/review-2026-11-09-yim-vitamoon.md"
#: The side PACKINGS.md prints at each count of the head, rounded up at 12 places.
PRINTED = {
    130: "11.902430645983",
    299: "17.801004434255",
    303: "17.901789273154",
    553: "23.969145238668",
    599: "24.936479681246",
    600: "24.951090275321",
    601: "24.958070476928",
    602: "24.981298949631",
    604: "24.995880488226",
    645: "25.881385537401",
    647: "25.899272968790",
    648: "25.908803576981",
    699: "26.907311118315",
    700: "26.908036102718",
}
#: Above the corpus: the row each certificate supersedes, by its source.
SUPERSEDED = {n: "couzo-issue763-2026-10-23" for n in PRINTED if n > 324} | {
    604: "couzo-43f666c-2026-10-24"
}
#: In the corpus: the house each certificate is compared with, and the gap, rounded.
HOUSES = {130: ("T-259", "1.955e-14"), 299: ("T-277", "1.182e-12"), 303: ("T-278", "3.291e-12")}
#: The source key of each house's reported lane, which the holds leave in place.
HOUSE_KEYS = {
    130: "[Mishapolk issue 846 2026-10-30]",
    299: "[Özden s299 upper bound 2026-11-09]",
    303: "[Özden s303 upper bound 2026-11-09]",
}
#: Each in-corpus certificate's gain over its house as a share of the house certificate's
#: own uniform-contraction margin (measure/contraction-nNNN.json).
SHARES = {130: "0.0896", 299: "0.3472", 303: "0.9674"}


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _up(side: Fraction, places: int) -> Fraction:
    return Fraction(math.ceil(side * 10**places), 10**places)


def test_the_retained_files_are_the_ones_the_source_digest_list_names() -> None:
    packet = reports.packet_path(MAIN)
    listed = {
        name: digest
        for digest, name in (
            line.split(maxsplit=1)
            for line in (packet / "source/SHA256SUMS").read_text("utf-8").splitlines()
        )
    }
    manifest = {
        path.removeprefix("./"): digest
        for digest, path in (
            line.split(maxsplit=1)
            for line in (packet / "acquisition/upstream-subtree.sha256")
            .read_text("utf-8")
            .splitlines()
        )
    }
    assert {name for name in listed if name.endswith(".cert")} == {
        f"n{n}.cert" for n in [*PRINTED, 260]
    }
    for name, digest in listed.items():
        assert manifest[name] == digest


def test_each_print_is_its_exact_side_rounded_up() -> None:
    declaration = reports.load_declaration(reports.packet_path(MAIN))
    assert declaration["source_key"] == SOURCE_KEY
    assert declaration["issue"] == "(no issue)"
    assert declaration["replayed"] == sorted(PRINTED)
    assert 130 not in declaration["requested"]
    facts = reports.read_facts(reports.packet_path(MAIN))
    for row in declaration["certificates"]:
        assert row["format"] == "evand-cert"
        assert row["offered"] == PRINTED[row["n"]]
        assert _up(facts[row["n"]].side, 12) == Fraction(Decimal(row["offered"]))


def test_each_certificate_against_the_record() -> None:
    record = reports.check_claims(reports.packet_path(MAIN))
    rows = {row["n"]: row for row in record["results"]}
    for n, (result, gap) in HOUSES.items():
        case = rows[n]["case"]
        assert (case["result"], case["relation"], rows[n]["smallest"]) == (
            result,
            "below",
            reports.THIS,
        )
        assert f"{float(Fraction(case['difference'])):.3e}" == gap
    for n, source in SUPERSEDED.items():
        (pending,) = rows[n]["pending"]
        assert (pending["report"], pending["relation"]) == (source, "below")
        assert rows[n]["smallest"] == reports.THIS
    (first,) = reports.check_claims(reports.packet_path(FIRST))["results"]
    assert (first["n"], first["case"]["result"], first["case"]["relation"]) == (
        303,
        "T-278",
        "above",
    )


def test_the_ledger_records_all_but_the_first_303() -> None:
    ledger = _json(LEDGER / "ledger.json")
    verdicts: dict[tuple[int, str], str] = {}
    for count in ledger["counts"]:
        for claim in count["steps"]:
            verdicts[(count["n"], claim["report"])] = claim["verdict"]
    head = "vitamoon/vitamoon@"
    assert verdicts.pop((303, f"{head}78eb9ea")) == "not recorded"
    assert verdicts == {
        (130, f"{head}c10e094"): "recorded",
        (299, f"{head}e4209f6"): "recorded",
        (303, f"{head}546928a"): "recorded",
        **{(n, f"{head}78eb9ea"): "recorded" for n in SUPERSEDED},
    }


@pytest.mark.parametrize(("name", "n"), [*((MAIN, n) for n in sorted(PRINTED)), (FIRST, 303)])
def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it(
    name: str, n: int
) -> None:
    receipts = reports.packet_path(name) / "receipts"
    path = receipts / ("sharp-controls.json" if name == FIRST else f"sharp-controls-n{n}.json")
    record = _json(path)
    assert (record["n"], record["packet"], record["all_as_expected"]) == (n, name, True)
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)


@pytest.mark.parametrize("n", sorted(HOUSES))
def test_each_in_corpus_gain_lies_within_its_house_certificates_padding(n: int) -> None:
    record = _json(reports.packet_path(MAIN) / f"measure/contraction-n{n}.json")
    assert record["certificate"]["label"] == HOUSES[n][0]
    assert record["routes_accept"] is True
    assert record["against"]["within_margin"] is True
    assert record["against"]["gain_over_margin"] == SHARES[n]


@pytest.mark.parametrize("n", sorted(HOUSES))
def test_each_in_corpus_certificate_is_its_houses_packing(n: int) -> None:
    record = _json(reports.packet_path(MAIN) / f"measure/identity-n{n}.json")
    pair = next(item for item in record["pairs"] if item["against"] == HOUSES[n][0])
    assert pair["nearest_centre"]["one_to_one"] is True
    assert pair["assignment"]["moved_beyond"]["1e-3"] == 0


def test_the_holds_and_the_rows() -> None:
    register = yaml.safe_load((reports.ROOT / "frontier/results.yaml").read_text("utf-8"))
    entries = {entry["id"]: entry for entry in register["results"]}
    holds = (("T-280", [299, 303], "think-ruu2"), ("T-281", [130], "think-ikku"))
    for result, scope, link in holds:
        entry = entries[result]
        assert entry["scope"]["n_values"] == scope
        assert (entry["verification"], entry["confirmation"]) == ("V0", "C1")
        assert entry["evidence"] == ["E-yim-1109-certificate-report"]
        (review,) = entry["reviews"]
        assert (review["path"], review["verdict"]) == (REVIEW, "accepted")
        assert entry["attribution"]["source_keys"] == [SOURCE_KEY]
        assert entry["unfinished_confirmations"][0]["link"] == link
        assert [item["n"] for item in entry["regularizations"]] == scope
    for n, key in HOUSE_KEYS.items():
        case = coverage.parse_case(reports.ROOT / f"frontier/n-{n:03d}.md")
        assert case["reported_upper_bound"]["source_key"] == key
    document = yaml.safe_load(coverage.COVERAGE.read_text("utf-8"))
    current = coverage.current_beyond_horizon(document)
    for n, source in SUPERSEDED.items():
        assert current[n]["source_id"] == MAIN
        assert current[n]["value"] == PRINTED[n]
        (old,) = [
            row
            for row in document["beyond_horizon_claims"]
            if row["n"] == n and row["source_id"] == source and row.get("superseded_by") == MAIN
        ]
        assert old["disposition"] == "superseded"
        assert current[n]["assurance"] == "verified"
