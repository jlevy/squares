"""Target-free homogeneous cone controls; no scientific input or LP calls."""

from __future__ import annotations

import copy
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest
import sympy as sp

from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_n17_widened_cone as cone
from sqpack import retained_json


def layout() -> exact.Layout:
    axes = {
        "ex": (exact.point(1), exact.point(0)),
        "ey": (exact.point(0), exact.point(1)),
        "u": (exact.point(Q(3, 5)), exact.point(Q(4, 5))),
        "v": (exact.point(Q(-4, 5)), exact.point(Q(3, 5))),
        "p": (exact.point(Q(3, 5)), exact.point(Q(-4, 5))),
        "q": (exact.point(Q(4, 5)), exact.point(Q(3, 5))),
    }
    centres = {label: (exact.point(0), exact.point(0)) for label in range(1, 18)}
    centres[15] = exact.point(Q(7, 2)), exact.point(0)
    centres[17] = exact.point(0), exact.point(Q(18, 5))
    return exact.Layout(centres, axes, {}, {}, exact.point(5))


@pytest.fixture
def packet(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    monkeypatch.setattr(cone, "load_inputs", lambda _path: ({"synthetic": True}, layout()))
    return cone.generate(Path("synthetic-features.json"))


def test_symbolic_cancellation_exact_root_normalization_and_free_labels() -> None:
    symbolic = cone.symbolic_packet()
    assert symbolic["identities"]["centre_coefficients"] == ["0"] * 32
    assert len(symbolic["weighted_rows"]) == 16
    assert symbolic["raw_branches"] == 256
    assert symbolic["weighted_labels"] == sorted((*cone.SMALL, 16))
    assert set(symbolic["weighted_labels"]).isdisjoint(cone.FREE)
    assert symbolic["constant_residual_used"] is False
    assert symbolic["F2_exact_root_join"].startswith("Pi2=0")
    # Pair 3/9 is the vertical axis of square 3; never the theta v axis.
    options = [
        row for row in symbolic["selected_options"] if (row["left"], row["right"]) == (3, 9)
    ]
    assert len(options) == 1
    assert options[0]["owner"] == 3
    assert options[0]["axis"] == "ey"


def test_synthetic_positive_gamma_and_endpoint_retained(packet: dict[str, Any]) -> None:
    result = cone.check(packet, Path("synthetic"))
    assert result["verification_passed"]
    assert result["cone_certified"]
    assert result["gamma"] == "638375/40961024"
    assert result["endpoint_excluded"] is False
    assert result["global_coverage_certified"] is False
    assert packet["domain"]["radial_interval_checked"][0] == "0"
    assert packet["domain"]["excluded_radial_domain"].startswith("0 <")


def test_direct_generated_weight_mutation_does_not_change_expected_cache(
    packet: dict[str, Any],
) -> None:
    packet["symbolic"]["weighted_rows"][0]["weight"] = "0"
    with pytest.raises(exact.AuditError, match="symbolic weights"):
        cone.check(packet, Path("synthetic"))
    assert cone.symbolic_packet()["weighted_rows"][0]["weight"] != "0"


def test_direct_generated_domain_mutation_does_not_change_frozen_domain(
    packet: dict[str, Any],
) -> None:
    packet["domain"]["small_labels"].append(4)
    packet["domain"]["radial_interval_checked"][1] = "1/400"
    with pytest.raises(exact.AuditError, match="domain"):
        cone.check(packet, Path("synthetic"))
    assert cone.DOMAIN["small_labels"] == list(cone.SMALL)
    assert cone.DOMAIN["radial_interval_checked"] == ["0", "1/200"]


@pytest.mark.parametrize(
    "mutation",
    [
        "weight",
        "sign",
        "owner",
        "F2",
        "root",
        "domain",
        "constant",
        "gamma",
        "interval",
        "endpoint",
    ],
)
def test_changed_claim_or_exact_evidence_refused(packet: dict[str, Any], mutation: str) -> None:
    damaged = copy.deepcopy(packet)
    if mutation == "weight":
        damaged["symbolic"]["weighted_rows"][0]["weight"] = "0"
    elif mutation in {"sign", "owner"}:
        damaged["symbolic"]["selected_options"][0][mutation] = 17
    elif mutation == "F2":
        damaged["symbolic"]["F2_denominator"] = "1"
    elif mutation == "root":
        damaged["inputs"]["synthetic"] = False
    elif mutation == "domain":
        damaged["domain"]["radial_interval_checked"][1] = "1/400"
    elif mutation == "constant":
        damaged["constants"]["epsilon"] = "1/4096"
    elif mutation == "gamma":
        damaged["gamma"] = "1"
    elif mutation == "interval":
        damaged["intervals"]["K"] = ["-1", "-1"]
    else:
        damaged["domain"]["endpoint_excluded"] = True
    with pytest.raises(exact.AuditError):
        cone.check(damaged, Path("synthetic"))


def test_actual_weight_and_owner_sign_controls() -> None:
    c, s, dr, er = sp.symbols("c s d_r e_r", positive=True)
    rows = cone.symbolic_rows(cone.selected_options())
    weights = cone.weights(c, s, dr, er)
    weights[rows[0]["name"]] += 1
    with pytest.raises(exact.AuditError, match="centre coefficients"):
        cone.verify_rows(rows, weights)
    changed = copy.deepcopy(list(cone.selected_options()))
    owner16 = next(row for row in changed if (row["left"], row["right"]) == (15, 16))
    owner16["sign"] *= -1
    with pytest.raises(exact.AuditError, match="centre coefficients"):
        cone.verify_rows(cone.symbolic_rows(tuple(changed)), cone.weights(c, s, dr, er))


def test_wide_valid_enclosures_are_inconclusive_not_packing_evidence(
    packet: dict[str, Any],
) -> None:
    packet["intervals"]["K"] = ["-1", "1"]
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


def test_cli_exact_roundtrip_and_one_unit_tamper(
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
    decoded["gamma"] = str(Q(decoded["gamma"]) + Q(1, 40961024))
    path.write_text(retained_json.dumps(decoded))
    assert cone.main(["--features", "synthetic", "--certificate", str(path)]) == 1
