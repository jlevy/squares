"""Source algebraic identities never decide source geometry or the current bound."""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from typing import Any

import pytest

from devtools import collect_reported_exact_roots as roots


@pytest.fixture(scope="module")
def collected() -> list[dict[str, Any]]:
    return roots.collect()


def test_all_four_complete_source_identities_are_independently_checked(
    collected: list[dict[str, Any]],
) -> None:
    assert [row["n"] for row in collected] == [102, 106, 152, 177]
    assert [row["degree"] for row in collected] == [8, 32, 40, 32]
    for row in collected:
        reported = row["reported_source"]
        original = reported["row"]
        assert row["polynomial"]["coefficients"] == list(reversed(original["S_poly_ascending"]))
        assert len(row["polynomial"]["coefficients"]) == row["degree"] + 1
        assert row["side"] == original["S"]
        lo, hi = map(Fraction, original["S_interval"])
        isolated_lo, isolated_hi = map(Fraction, row["checks"]["root"]["interval"])
        assert lo <= isolated_lo < isolated_hi <= hi
        assert reported["interval_root_count"] == 1
        assert reported["isolated_root_contained"] is True
        assert row["checks"]["root"]["unique"] is True
        assert row["checks"]["root"]["contains_recorded_side"] is True
        assert row["checks"]["irreducible"]["method"] in {
            "factorization",
            "modular-degree-patterns",
        }
        assert row["checks"]["catalogue"] == "not-in-catalogue"
        assert row["checks"]["kkt_agreement_digits"] is None
        assert reported["revision"] == roots.reports.REVISION
        assert all(isinstance(c, str) for c in original["field_poly_ascending"])
        (source,) = row["sources"]
        assert source["locator"]["section"] == str(row["n"])
        assert source["locator"]["line"] > 1
        assert roots.reports.REVISION in source["url"]
        assert source["path"].endswith("exact_forms.json.gz")


def test_reports_and_feasible_bounds_are_not_promoted(
    collected: list[dict[str, Any]],
) -> None:
    for row in collected:
        assert row["assurance"] == {
            "verification": "V0",
            "confirmation": "C0",
            "algebraic_identity": "independently-checked",
            "geometry_replay": "not-attempted",
            "lean_replay": "not-attempted",
            "current_pose_identity": "not-established",
            "global_optimality": "not-established",
        }
        assert {"status", "current_side", "verified_upper_bound", "kind"}.isdisjoint(row)
        assert "geometry-not-retained" in row["source_statuses"]
        assert row["reported_source"]["row"]["verify_exact"] is True
        assert row["reported_source"]["row"]["lean_local_min"] == ""
        assert row["bead"] == "think-8sm2"
        assert any("Evan Daniel" in text for text in row["attribution"]["source_text"])


@pytest.fixture
def octic() -> dict[str, Any]:
    return copy.deepcopy(roots.read_source_rows()[0][102])


@pytest.mark.parametrize("corruption", ["coefficient", "interval", "side"])
def test_an_altered_algebraic_identity_is_refused(
    octic: dict[str, Any],
    corruption: str,
) -> None:
    if corruption == "coefficient":
        octic["S_poly_ascending"][0] += 1
    elif corruption == "interval":
        octic["S_interval"] = [str(Fraction(value) + 1) for value in octic["S_interval"]]
    else:
        octic["S"] = "20.00000000000000000"
    with pytest.raises(roots.ReportedRootError, match="n = 102"):
        roots.verify_source_root(octic)


def test_primitive_normalization_does_not_trust_source_checker_flags(
    octic: dict[str, Any],
) -> None:
    original = tuple(reversed(octic["S_poly_ascending"]))
    octic["S_poly_ascending"] = [-7 * coefficient for coefficient in octic["S_poly_ascending"]]
    octic["verify_exact"] = False
    octic["lean_packs"] = False
    coefficients, checks = roots.verify_source_root(octic)
    assert coefficients == original
    assert checks["irreducible"]["method"] == "factorization"


def test_a_reducible_polynomial_cannot_be_called_minimal(octic: dict[str, Any]) -> None:
    # (s^2 - 2) * (s^6 + 1) has exactly one positive root near sqrt(2),
    # but the complete degree-eight expression is not its minimal polynomial.
    octic.update(S="1.41421356237309505", S_poly_ascending=[-2, 0, 1, 0, 0, 0, -2, 0, 1])
    octic["S_interval"] = [
        "14142135623730950488016887/10000000000000000000000000",
        "14142135623730950488016889/10000000000000000000000000",
    ]
    with pytest.raises(roots.ReportedRootError, match="reducible"):
        roots.verify_source_root(octic)


@pytest.mark.parametrize("corruption", ["source-bytes", "revision", "reported-view"])
def test_source_binding_is_checked_on_the_consumed_bytes(
    monkeypatch: pytest.MonkeyPatch,
    corruption: str,
) -> None:
    read = roots.read_retained_bytes

    def altered(path: Any, **kwargs: Any) -> bytes:
        raw = read(path, **kwargs)
        if corruption == "source-bytes" and path == roots.SOURCE_FILE:
            value = json.loads(raw)
            value[101]["S_poly_ascending"][0] += 1
            return json.dumps(value).encode()
        if corruption == "revision" and path == roots.PACKET / roots.acquire_source.RECORD:
            value = json.loads(raw)
            value["sources"][0]["source_commit"] = "0" * 40
            return json.dumps(value).encode()
        if corruption == "reported-view" and path == roots.PACKET / "reported-catalogue.json":
            value = json.loads(raw)
            value["new_form_claims"]["102"]["polynomial_ascending"][0] += 1
            return json.dumps(value).encode()
        return raw

    monkeypatch.setattr(roots, "read_retained_bytes", altered)
    with pytest.raises(roots.ReportedRootError, match=r"source|reported catalogue"):
        roots.read_source_rows()


def test_failed_acquisition_never_reaches_mathematics(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(roots.acquire_source, "check", lambda *_args: ["altered source bytes"])
    monkeypatch.setattr(
        roots, "verify_source_root", lambda *_args, **_kwargs: pytest.fail("unchecked source")
    )
    with pytest.raises(roots.ReportedRootError, match="altered source bytes"):
        roots.collect()


def test_three_nearby_real_roots_are_not_one_source_identity(octic: dict[str, Any]) -> None:
    scale = 10**14
    coefficients = [1]
    for offset in (1, 3, 7):
        product = [0] * (len(coefficients) + 1)
        for index, coefficient in enumerate(coefficients):
            product[index] -= (scale + offset) * coefficient
            product[index + 1] += scale * coefficient
        coefficients = product
    # Multiply by s^5 + 1: keep degree eight with three positive roots in the cell.
    complete = [0] * 9
    for index, coefficient in enumerate(coefficients):
        complete[index] += coefficient
        complete[index + 5] += coefficient
    octic.update(
        S="1.00000000000000000",
        S_poly_ascending=complete,
        S_interval=["1", str(Fraction(scale + 10, scale))],
    )
    with pytest.raises(roots.ReportedRootError, match="does not contain one root"):
        roots.verify_source_root(octic)


def test_exhausted_irreducibility_budget_is_a_refusal() -> None:
    row = roots.read_source_rows()[0][106]
    with pytest.raises(roots.ReportedRootError, match="no irreducibility certificate"):
        roots.verify_source_root(row, prime_budget=1)
