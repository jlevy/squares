"""Synthetic retained-dual and apex-bound controls, with no target reads or solves."""

from __future__ import annotations

import copy
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_n17_widened_apex as apex


def synthetic_inputs() -> tuple[list[list[apex.core.Dyadic]], list[dict[str, Any]]]:
    rows = [[apex.core.Dyadic.point(0) for _ in range(29)] for _ in range(52)]
    for j in range(29):
        rows[j][j] = apex.core.Dyadic.point(1)
        rows[29][j] = apex.core.Dyadic.point(-1)
    documents = []
    for j, name in enumerate(apex.position_names()):
        for sign in ("+", "-"):
            weights = [0] * 52
            if sign == "+":
                weights[29] = 1
                for k in range(29):
                    if k != j:
                        weights[k] = 1
            else:
                weights[j] = 1
            documents.append(
                {
                    "direction": sign + name,
                    "cells": [
                        {
                            "cell": [[str(lo), str(hi)] for lo, hi in apex.forcing.DOMAIN],
                            "lambda": [weight * 2**apex.local.DUAL_BITS for weight in weights],
                            "mu": [[0] * 52 for _ in range(3)],
                        }
                    ],
                }
            )
    return rows, documents


@pytest.fixture
def packet(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    rows, documents = synthetic_inputs()
    monkeypatch.setattr(
        apex, "load_target", lambda _path: ({"synthetic": True}, rows, documents)
    )
    return apex.generate(Path("synthetic"))


def test_exact_synthetic_complete_duals_and_radius(packet: dict[str, Any]) -> None:
    assert apex.check(packet, Path("synthetic"))["verification_passed"]
    assert len(packet["signed_directions"]) == 58
    assert packet["epsilon"] == "0"
    mass, alpha = Q(packet["C"]), Q(packet["alpha0"])
    assert mass > 0
    assert alpha == min(Q(1, 5000), 1 / (10000 * mass))
    assert Q(packet["q0"]) == alpha / 2
    assert Q(packet["position_bound_at_alpha0"]) <= Q(1, 10000)


def test_large_dual_numerators_roundtrip_real_shape(monkeypatch: pytest.MonkeyPatch) -> None:
    rows, documents = synthetic_inputs()
    large = 2**180 + 17
    for document in documents:
        # Row 51 is zero, so large exact positive weights preserve the residual
        # control while exercising realistic 58 x (52 + 3 x 52) witness storage.
        cell = document["cells"][0]
        cell["lambda"][51] = large
        cell["mu"][0][51] = large
    monkeypatch.setattr(
        apex, "load_target", lambda _path: ({"synthetic": True}, rows, documents)
    )
    generated = apex.generate(Path("synthetic"))
    encoded = json.dumps(generated).encode()
    decoded = exact.decode(encoded)
    assert apex.check(decoded, Path("synthetic"))["verification_passed"]
    assert len(decoded["signed_directions"]) == 58
    for entry in decoded["signed_directions"]:
        cell = entry["selected_cell"]
        assert len(cell["lambda"]) == 52
        assert len(cell["mu"]) == 3
        assert all(len(values) == 52 for values in cell["mu"])
        assert cell["lambda"][51] == cell["mu"][0][51] == str(large)
        assert exact.rational(cell["lambda"][51]) == large
    # Changing one unit must fail even though it is below floating precision.
    decoded["signed_directions"][0]["selected_cell"]["mu"][0][51] = str(large + 1)
    with pytest.raises(exact.AuditError, match="differs from exact replay"):
        apex.check(decoded, Path("synthetic"))


def test_dual_encoding_preserves_bounded_decoder(packet: dict[str, Any]) -> None:
    damaged = copy.deepcopy(packet)
    damaged["signed_directions"][0]["selected_cell"]["lambda"][0] = 2**44
    with pytest.raises(exact.AuditError, match="oversized bare JSON integer"):
        exact.decode(json.dumps(damaged).encode())
    with pytest.raises(exact.AuditError, match="invalid rational string"):
        apex.retained_cell({"cell": [], "lambda": [True], "mu": []})


@pytest.mark.parametrize(
    "mutation", ["direction", "root", "columns", "rows", "radius", "constants", "scope"]
)
def test_changed_apex_certificate_refused(packet: dict[str, Any], mutation: str) -> None:
    damaged = copy.deepcopy(packet)
    if mutation == "direction":
        damaged["signed_directions"].pop()
    elif mutation == "root":
        damaged["inputs"] = {"synthetic": False}
    elif mutation == "columns":
        damaged["position_columns"].reverse()
    elif mutation == "rows":
        damaged["row_roster"].reverse()
    elif mutation == "radius":
        damaged["q0"] = "1/100"
    elif mutation == "constants":
        damaged["constants"]["pair_lipschitz"] = "2"
    else:
        damaged["scope"] = "global optimality"
    with pytest.raises(exact.AuditError):
        apex.check(damaged, Path("synthetic"))


def test_affine_origin_evaluation_is_not_cell_midpoint() -> None:
    _, documents = synthetic_inputs()
    document = documents[0]
    scale = 2**apex.local.DUAL_BITS
    document["cells"][0]["lambda"][0] = scale
    document["cells"][0]["mu"][0][0] = scale
    _, weights = apex.selected_weights(document)
    assert weights[0] == Q(7, 8)


def test_origin_on_closed_cell_boundary_and_lexicographic_selection() -> None:
    _, documents = synthetic_inputs()
    document = documents[0]
    second = copy.deepcopy(document["cells"][0])
    second["cell"][0] = ["-1/4", "0"]
    second["lambda"][0] = 2**apex.local.DUAL_BITS
    document["cells"].append(second)
    selected, weights = apex.selected_weights(document)
    assert selected is second
    assert weights[0] == 1


@pytest.mark.parametrize("mutation", ["negative", "boolean", "missing", "duplicate", "epsilon"])
def test_invalid_witness_or_large_residual_refused(mutation: str) -> None:
    rows, documents = synthetic_inputs()
    if mutation == "negative":
        documents[0]["cells"][0]["lambda"][0] = -1
    elif mutation == "boolean":
        documents[0]["cells"][0]["lambda"][0] = True
    elif mutation == "missing":
        documents.pop()
    elif mutation == "duplicate":
        documents[0] = documents[1]
    else:
        rows[29][0] = apex.core.Dyadic.point(-3)
    with pytest.raises(exact.AuditError):
        apex.evaluate(rows, documents)


def test_angle_and_side_columns_do_not_enter_position_projection() -> None:
    keys = apex.row_roster()
    rows = {key: [Q(0)] * 52 for key in keys}
    aux = {"u": (Q(3, 5), Q(4, 5))}
    before = apex.project_rows(rows, aux)
    for row in rows.values():
        for label in range(1, 18):
            row[apex.local.column(label, "angle")] = Q(987)
        row[-1] = Q(123)
    assert apex.project_rows(rows, aux) == before
    rows[keys[0]][apex.local.column(1, "x")] = Q(1)
    assert apex.project_rows(rows, aux) != before
