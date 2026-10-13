"""The Wang and Li n11 certificate: its change from Overbeck's, and the native wrapper.

The coverage decisions themselves are retained receipts under
``resources/web/wang-li-n11-2026-09-29/receipts/``; these tests check the exact
description of the change, the mutations every checker must refuse, and that the native
wrapper decides a Kleddamag row exactly as the frozen tool does.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_wang_li_n11 as audit
from devtools import verify_kleddamag_n11_native as frozen
from devtools import verify_n11_parent_core_native as wrapper
from sqpack.fractional.parent_core import load_kleddamag_parent_core, validate_parent_core


@pytest.fixture(scope="module")
def certificates() -> tuple[audit.Certificate, audit.Certificate]:
    return audit.load(audit.SOURCE), audit.load(audit.IMPROVED)


def test_diff_derives_the_stated_change_from_the_two_files(
    certificates: tuple[audit.Certificate, audit.Certificate],
) -> None:
    result = audit.diff(*certificates)
    assert result["changed_keys"] == [
        "A", "bound", "budget_units", "charge_orbits", "entries", "minimum_units",
    ]  # fmt: skip
    assert {orbit["orbit"]: orbit["delta"] for orbit in result["changed_orbits"]} == (
        audit.STATED_DELTAS
    )
    assert result["factor"] == "999999999/1000000000"
    assert result["parent_side_before"] == "764/775"
    assert result["parent_side_after"] == "190999999809/193750000000"
    assert result["bound_before"] == "31/8"
    assert result["bound_after"] == "3875000000/999999999"
    assert result["improvement"] == "31/7999999992"
    assert Fraction(3875000000, 999999999) - Fraction(31, 8) == Fraction(31, 7999999992)
    assert (result["budget_units_before"], result["budget_units_after"]) == (
        10999479944,
        11000095024,
    )
    assert (result["surplus_units_before"], result["surplus_units_after"]) == (107864, 428125)
    assert result["premises"]["strict_core_margin_after"] == "999999999/10" + "0" * 20


def test_diff_refuses_a_core_side_that_is_not_scaled(
    certificates: tuple[audit.Certificate, audit.Certificate],
) -> None:
    source, improved = certificates
    mutated: dict[str, Any] = {
        **improved,
        "entries": [list(row) for row in improved["entries"]],
    }
    mutated["entries"][7][3] = source["entries"][7][3]
    with pytest.raises(ValueError, match="row 7: core side not scaled"):
        audit.diff(source, mutated)


def test_every_mutation_changes_what_it_says(
    certificates: tuple[audit.Certificate, audit.Certificate],
) -> None:
    source, improved = certificates
    built = {name: spec[3](improved, source) for name, spec in audit.MUTATIONS.items()}
    assert built["gamma_plus_one"]["minimum_units"] == improved["minimum_units"] + 1
    closed = built["counting_gap_closed"]
    assert 11 * closed["minimum_units"] <= closed["budget_units"]
    reverted = built["orbit_130_reverted"]
    assert reverted["budget_units"] == audit.budget_units(reverted) < improved["budget_units"]
    assert 11 * reverted["minimum_units"] > reverted["budget_units"]
    further = built["scaled_one_step_further"]
    assert Fraction(further["A"]) == Fraction(source["A"]) * (1 - Fraction(2, 10**9))
    assert Fraction(further["entries"][615][3]) == Fraction(source["entries"][615][3]) * (
        1 - Fraction(2, 10**9)
    )
    beyond = built["scaled_past_known_packing"]
    assert Fraction(beyond["L"]) / Fraction(beyond["A"]) >= audit.KNOWN_PACKING_SIDE
    assert improved["minimum_units"] == 1000047559


@pytest.mark.slow
def test_native_premises_hold_for_the_new_parameters(tmp_path: Path) -> None:
    plain = tmp_path / "improved-global-certificate.json"
    plain.write_bytes(audit.read_bytes(audit.IMPROVED))
    certificate = load_kleddamag_parent_core(plain)
    premises = validate_parent_core(certificate)
    assert certificate.parent_side == Fraction(190999999809, 193750000000)
    assert certificate.outer_side / certificate.parent_side == Fraction(3875000000, 999999999)
    assert premises.rows == 12028
    assert premises.minimum_containment_numerator == Fraction(999999999, 10**21)
    assert premises.budget < 11 * certificate.minimum_charge


def _decisions(receipt: dict[str, Any]) -> dict[str, Any]:
    kept = ("bound", "parent_side", "minimum_charge", "budget", "scale", "threshold_units")
    rows = [
        {key: value for key, value in row.items() if key != "seconds"}
        for row in receipt["rows"]
    ]
    return {
        **{key: receipt[key] for key in kept},
        "premises": receipt["premises"],
        "rows": rows,
    }


@pytest.mark.slow
def test_wrapper_decides_a_kleddamag_row_as_the_frozen_tool_does(tmp_path: Path) -> None:
    state = ("0" * 40, False)
    pin = frozen.REVIEWED_SHA256
    with (tmp_path / "frozen.rows.jsonl").open("x", encoding="utf-8") as journal:
        expected = frozen.run(
            frozen.SOURCE, (12027,), 2048, trace_allocations=False, journal=journal,
            source_state=state,
        )  # fmt: skip
    result = wrapper.run_certificate(
        frozen.SOURCE,
        (12027,),
        2048,
        1,
        journal_path=tmp_path / "wrapper.rows.jsonl",
        source_state=state,
    )
    assert _decisions(result) == _decisions(expected)
    assert expected["provenance"]["certificate_sha256"] == frozen.REVIEWED_SHA256
    assert result["provenance"]["certificate_sha256"] is None
    assert result["certificate"] == str(frozen.SOURCE.relative_to(wrapper.REPO))
    assert pin == frozen.REVIEWED_SHA256
