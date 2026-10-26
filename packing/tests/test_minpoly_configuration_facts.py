"""Kim's exact configurations for T-244 on both exact routes (issue 804, think-4rzl).

The ``hyukdongkim-t244-configurations-2026-10-25`` packet keeps each configuration as a
derived fact; `devtools.minpoly_configuration_facts` reads it. This holds the reader's
custody check (the content rebuilds the author's bytes, and a changed coefficient is
refused), the empty-list zero, the side receipt to a fresh decision, both routes'
receipts to their required outcomes, two of route 2's controls refused by the retained
``verify_exact.py`` here, and the identity measurements T-244's regularization items cite.
"""

from __future__ import annotations

import gzip
import json
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import algebraic_witness_reports as algebraic
from devtools import minpoly_configuration_facts as facts

PACKING = Path(__file__).resolve().parents[1]
PACKET = PACKING / "resources/web/hyukdongkim-t244-configurations-2026-10-25"
LEDGER = PACKING / "campaign/issue-intake/upper-bounds-issue804-20261025/exact-sides.json"
COUNTS = (172, 263)


def test_each_fact_rebuilds_the_authors_certificate() -> None:
    rows = facts.check(PACKET)
    assert sorted(rows) == list(COUNTS)
    assert rows[172]["member_sha256"].startswith("9230aa7a")
    assert rows[263]["member_sha256"].startswith("de646870")
    assert (rows[172]["field_degree"], rows[263]["field_degree"]) == (24, 17)


def test_a_changed_coefficient_is_refused(tmp_path: Path) -> None:
    packet = tmp_path / PACKET.name
    (packet / "facts").mkdir(parents=True)
    shutil.copytree(PACKET / "acquisition", packet / "acquisition")
    fact = json.loads(gzip.decompress((PACKET / "facts/n172.json.gz").read_bytes()))
    square = fact["configuration"]["squares"][5]
    square["x"][0] = str(Fraction(square["x"][0]) + Fraction(1, 10**30))
    (packet / "facts/n172.json.gz").write_bytes(gzip.compress(json.dumps(fact).encode()))
    with pytest.raises(facts.FactError, match="does not rebuild"):
        facts.read_fact(packet, 172)


def test_an_empty_coefficient_list_is_the_fields_zero() -> None:
    read = algebraic._coefficients  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    assert read([], 17, "u") == [Fraction(0)]
    with pytest.raises(algebraic.ReportError):
        read(["1"] * 18, 17, "u")


def test_the_side_receipt_is_a_fresh_decision() -> None:
    stored = json.loads((PACKET / "receipts/side.json").read_text(encoding="utf-8"))
    assert facts.side(PACKET, LEDGER) == stored
    assert [row["n"] for row in stored["rows"]] == list(COUNTS)
    assert all(
        row["p_of_S_is_zero_in_K"] and row["S_enclosure_within_ledger_interval"]
        for row in stored["rows"]
    )


@pytest.mark.parametrize("n", COUNTS)
def test_route_1_decided_the_positive_and_refused_both_controls(n: int) -> None:
    record = facts.admit_route1(PACKET, n)
    positive, duplicate, outside = record["cases"]
    assert positive[facts.ROUTE]["verification_passed"] is True
    assert positive[facts.ROUTE]["pairs_tested"] == n * (n - 1) // 2
    assert duplicate[facts.ROUTE]["verification_passed"] is False
    assert outside[facts.ROUTE]["verification_passed"] is False


def test_route_2_accepted_both_and_refused_every_control() -> None:
    record = facts.admit_route2(PACKET)
    assert [row["n"] for row in record["rows"]] == list(COUNTS)
    assert sum(len(row["controls"]) for row in record["rows"]) == 2 * len(facts.CONTROLS)


@pytest.mark.parametrize("kind", ["enlarged-side", "side-below-root"])
def test_the_retained_checker_refuses_two_controls_here(kind: str, tmp_path: Path) -> None:
    assert facts.checker_digest() == facts.CHECKER_SHA256
    configuration = facts.read_fact(PACKET, 263)["configuration"]
    mutated, _ = facts.mutate(configuration, kind)
    path = tmp_path / f"n263.{kind}.minpoly.json"
    path.write_text(json.dumps(mutated), encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, "-I", str(facts.CHECKER), str(path)],
        capture_output=True,
        text=True,
        check=False,
        timeout=600,
    )
    assert completed.returncode == 1
    assert "NOT VERIFIED" in completed.stdout


@pytest.mark.parametrize(("n", "displacement"), [(172, 1e-15), (263, 1e-16)])
def test_each_configuration_is_t174s_packing(n: int, displacement: float) -> None:
    receipt = json.loads((PACKET / f"measure/identity-n{n}.json").read_text("utf-8"))
    (pair,) = receipt["pairs"]
    assert receipt["inputs"]["T-174"]["packet"] == "pingyou-pr574-certificates-2026-10-13"
    nearest = pair["nearest_centre"]
    assert nearest["one_to_one"] is True
    assert nearest["symmetry"] == 0
    assert float(nearest["largest_displacement"]) < displacement
    assert all(count == 0 for count in nearest["moved_beyond"].values())
