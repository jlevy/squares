"""Target-free positive-turn symbolic, interval, custody and CLI controls."""

from __future__ import annotations

import copy
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest
import sympy as sp

from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_n17_widened_positive_cone as cone
from sqpack import retained_json


def layout() -> exact.Layout:
    axes = {
        "ex": (exact.point(1), exact.point(0)),
        "ey": (exact.point(0), exact.point(1)),
        "u": (exact.point(Q(4, 5)), exact.point(Q(3, 5))),
        "v": (exact.point(Q(-3, 5)), exact.point(Q(4, 5))),
        "p": (exact.point(Q(4, 5)), exact.point(Q(-3, 5))),
        "q": (exact.point(Q(3, 5)), exact.point(Q(4, 5))),
    }
    centres = {label: (exact.point(0), exact.point(0)) for label in range(1, 18)}
    centres[17] = exact.point(0), exact.point(Q(18, 5))
    return exact.Layout(centres, axes, {}, {}, exact.point(5))


@pytest.fixture
def packet(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    monkeypatch.setattr(cone, "load_inputs", lambda _path: ({"synthetic": True}, layout()))
    return cone.generate(Path("synthetic-features.json"))


def test_exact_symbolic_root_joins_cubic_and_weighted_incidence() -> None:
    symbolic = cone.symbolic_packet()
    assert symbolic["identities"]["centre_coefficients"] == ["0"] * 32
    assert len(symbolic["weighted_rows"]) == 17
    assert symbolic["retained_pairs"] == 19
    assert symbolic["raw_branches"] == 256
    assert symbolic["weighted_labels"] == sorted((*cone.SMALL, 16))
    assert set(symbolic["weighted_labels"]).isdisjoint(cone.FREE)
    assert symbolic["zero_root_join"].startswith("G(0)=F3+alpha_0*F2=0")
    assert symbolic["constant_residual_used"] is False
    assert symbolic["cubic_degree"] == 3
    assert len(symbolic["cubic_coefficients"]) == 4
    assert symbolic["interval_division_by_r"] is False
    pair = next(
        option
        for option in symbolic["selected_options"]
        if (option["left"], option["right"]) == (12, 16)
    )
    assert pair["owner"] == 12
    assert pair["axis"] == "u"


def test_synthetic_finite_certificate_keeps_endpoint_and_scope(packet: dict[str, Any]) -> None:
    result = cone.check(packet, Path("synthetic"))
    assert result["verification_passed"]
    assert result["cone_certified"]
    assert result["margin_gamma"] == cone.CONSTANTS["margin_gamma"]
    assert result["endpoint_excluded"] is False
    assert result["global_coverage_certified"] is False
    assert packet["domain"]["q16"] == "+r"
    assert packet["domain"]["radial_interval_checked"] == ["0", "1/200"]


@pytest.mark.parametrize(
    "mutation",
    [
        "weight",
        "sign",
        "owner",
        "F2",
        "F3",
        "cubic",
        "mass",
        "root",
        "domain",
        "constant",
        "gamma",
        "interval",
        "endpoint",
    ],
)
def test_changed_recipe_or_claim_refused(packet: dict[str, Any], mutation: str) -> None:
    damaged = copy.deepcopy(packet)
    if mutation == "weight":
        damaged["symbolic"]["weighted_rows"][0]["weight"] = "0"
    elif mutation in {"sign", "owner"}:
        damaged["symbolic"]["selected_options"][0][mutation] = 17
    elif mutation in {"F2", "F3"}:
        damaged["symbolic"][f"{mutation}_denominator"] = "1"
    elif mutation == "cubic":
        damaged["symbolic"]["cubic_coefficients"][0] = "0"
    elif mutation == "mass":
        damaged["symbolic"]["ordinary_pair_mass"] = "0"
    elif mutation == "root":
        damaged["inputs"]["synthetic"] = False
    elif mutation == "domain":
        damaged["domain"]["small_labels"].append(4)
    elif mutation == "constant":
        damaged["constants"]["epsilon"] = "1/256"
    elif mutation == "gamma":
        damaged["margin_gamma"] = "1"
    elif mutation == "interval":
        damaged["intervals"]["H"] = ["-2", "-2"]
    else:
        damaged["domain"]["endpoint_excluded"] = True
    with pytest.raises(exact.AuditError):
        cone.check(damaged, Path("synthetic"))


def test_generated_packet_does_not_alias_expected_recipe_or_domain(
    packet: dict[str, Any],
) -> None:
    packet["symbolic"]["weighted_rows"][0]["weight"] = "0"
    assert cone.symbolic_packet()["weighted_rows"][0]["weight"] != "0"
    with pytest.raises(exact.AuditError, match="symbolic recipe"):
        cone.check(packet, Path("synthetic"))
    packet["domain"]["small_labels"].append(4)
    assert cone.DOMAIN["small_labels"] == list(cone.SMALL)


def test_real_reconstructed_row_weight_and_owner_sign_mutations() -> None:
    c, s, dr, er = sp.symbols("c s d_r e_r", positive=True)
    options = cone.selected_options()
    rows = cone.symbolic_rows(options)
    weights = cone.weights(c, s, dr, er)
    weights[rows[0]["name"]] += 1
    with pytest.raises(exact.AuditError, match="centre coefficients"):
        cone.verify_rows(rows, weights)
    changed = copy.deepcopy(list(options))
    pair = next(option for option in changed if (option["left"], option["right"]) == (12, 16))
    pair["sign"] *= -1
    with pytest.raises(exact.AuditError, match="centre coefficients"):
        cone.verify_rows(cone.symbolic_rows(tuple(changed)), cone.weights(c, s, dr, er))


def test_cubic_coefficients_on_arbitrary_rational_geometry_without_root() -> None:
    c, s, d, e, side, y = Q(4, 5), Q(3, 5), Q(4, 5), Q(3, 5), Q(5), Q(18, 5)
    coefficients = cone.h_coefficients(c, s, d, e, side, y17=y)
    for r in (Q(0), Q(1, 400), Q(1, 200)):
        dr = (d * (1 - r * r) + 2 * e * r) / (1 + r * r)
        er = (e * (1 - r * r) - 2 * d * r) / (1 + r * r)
        h = sum(value * r**i for i, value in enumerate(coefficients))
        assert (1 + r * r) ** 2 * (
            cone.gap(c, s, dr, er, side, y17=y) - cone.gap(c, s, d, e, side, y17=y)
        ) == r * h


@pytest.mark.parametrize("field", ["H", "M", "alpha_r", "lambda:pair:12:16"])
def test_honest_wide_enclosures_are_inconclusive_not_packing_evidence(
    packet: dict[str, Any], field: str
) -> None:
    packet["intervals"][field] = ["-100", "100"]
    result = cone.check(packet, Path("synthetic"))
    assert result["verification_passed"] is True
    assert result["cone_certified"] is False
    assert result["status"] == "inconclusive"


def test_failed_feature_prerequisite_stops_before_root(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(exact, "read_bytes", lambda _path: b"{}")

    def refuse(_packet: dict[str, Any]) -> None:
        raise exact.AuditError("synthetic prerequisite refused")

    monkeypatch.setattr(cone.forcing, "check", refuse)
    monkeypatch.setattr(
        cone.forcing, "load_root", lambda: pytest.fail("root read after refusal")
    )
    with pytest.raises(exact.AuditError, match="prerequisite refused"):
        cone.load_inputs(Path("synthetic"))


def test_cli_exact_roundtrip_and_one_unit_margin_tamper(
    packet: dict[str, Any], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(cone, "provenance", lambda *_paths: {})
    path, replay = tmp_path / "certificate.json", tmp_path / "replay.json"
    assert cone.main(["--features", "synthetic", "--output", str(path)]) == 0
    assert (
        cone.main(
            ["--features", "synthetic", "--certificate", str(path), "--output", str(replay)]
        )
        == 0
    )
    decoded = exact.decode(exact.read_bytes(replay))
    assert exact.exact_structure(decoded["intervals"], packet["intervals"])
    assert decoded["checker"]["endpoint_excluded"] is False
    assert decoded["execution"]["features"] == "synthetic"
    decoded["margin_gamma"] = str(Q(decoded["margin_gamma"]) + Q(1, 102405120064))
    path.write_text(retained_json.dumps(decoded))
    assert cone.main(["--features", "synthetic", "--certificate", str(path)]) == 1
