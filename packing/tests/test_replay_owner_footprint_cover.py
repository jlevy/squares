"""Synthetic controls for source-bound exact owner-cover replay."""

from __future__ import annotations

import subprocess
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

import pytest

import devtools.replay_owner_footprint_cover as replay_module
from devtools.replay_owner_footprint_cover import (
    BoundSource,
    _endpoint_atoms,  # pyright: ignore[reportPrivateUsage]
    _source_configuration,  # pyright: ignore[reportPrivateUsage]
    bind_clean_tracked_source,
    exact_event_cell_count,
    exact_replay,
)
from devtools.run_owner_footprint_cover import Arm, build_receipt
from sqpack.fractional.colgen import SiteSet
from sqpack.fractional.model import Atom, rotation_from_half_tangent


def _completed_source(owner_count: int = 1) -> tuple[dict[str, Any], Arm]:
    raw_receipt, arms, _ = build_receipt(
        owner_count=owner_count,
        grid_count=5,
        folded_indices=(0,),
    )
    receipt = cast(dict[str, Any], raw_receipt)
    receipt["status"] = "complete"
    receipt["settings"]["execution"] = {
        "max_rounds_per_arm": 10,
        "rows_per_direction": 2,
        "deadline_seconds_per_arm": 5,
        "max_dense_event_cells_per_direction": 1000,
        "max_dense_event_cells_per_round": 1000,
        "rationalisation_scale": 100,
    }
    endpoint = next(arm for arm in arms if arm.label == "endpoint")
    x, y = endpoint.sites.positions()[0]
    endpoint_record = receipt["arms"]["endpoint"]
    endpoint_record["proposal"] = {
        "converged": True,
        "rationalisation_scale": 100,
        "rationalised_total_mass": "1",
        "rationalised_atoms": [[str(x), str(y), "1"]],
    }
    return receipt, endpoint


def test_reconstructs_declared_support_geometry_and_exact_atoms_without_reweighting() -> None:
    receipt, _ = _completed_source()
    _, arms, directions, owner_count = _source_configuration(receipt)
    assert owner_count == 1
    assert len(directions) == 1
    reconstructed = next(arm for arm in arms if arm.label == "endpoint")
    atoms, total = _endpoint_atoms(receipt, reconstructed)
    assert atoms[0].weight == total == 1
    assert (atoms[0].x, atoms[0].y) in reconstructed.sites.positions()
    assert exact_event_cell_count(atoms, reconstructed, directions[0], 0) > 0


def test_rejects_tampered_geometry_support_weight_and_incomplete_receipt() -> None:
    receipt, _ = _completed_source()
    tampered = deepcopy(receipt)
    tampered["settings"]["inset"] = "1/3"
    with pytest.raises(ValueError, match="does not match reconstructed"):
        _source_configuration(tampered)

    wrong_manifest = deepcopy(receipt)
    wrong_manifest["settings"]["full_owner_orientation_count"] = 360
    with pytest.raises(ValueError, match="does not match reconstruction"):
        _source_configuration(wrong_manifest)

    _, arms, _, _ = _source_configuration(receipt)
    endpoint = next(arm for arm in arms if arm.label == "endpoint")
    outside = deepcopy(receipt)
    outside["arms"]["endpoint"]["proposal"]["rationalised_atoms"] = [["999", "999", "1"]]
    with pytest.raises(ValueError, match="outside reconstructed support"):
        _endpoint_atoms(outside, endpoint)

    wrong_total = deepcopy(receipt)
    wrong_total["arms"]["endpoint"]["proposal"]["rationalised_total_mass"] = "2"
    with pytest.raises(ValueError, match="does not equal"):
        _endpoint_atoms(wrong_total, endpoint)

    negative = deepcopy(receipt)
    negative["arms"]["endpoint"]["proposal"]["rationalised_atoms"][0][2] = "-1"
    negative["arms"]["endpoint"]["proposal"]["rationalised_total_mass"] = "-1"
    with pytest.raises(ValueError, match="nonpositive weight"):
        _endpoint_atoms(negative, endpoint)

    incomplete = deepcopy(receipt)
    incomplete["status"] = "partial"
    with pytest.raises(ValueError, match="not a completed"):
        _source_configuration(incomplete)


def test_git_binding_accepts_clean_tracked_bytes_and_rejects_wrong_blob() -> None:
    root = Path.cwd().parent
    path = root / "packing" / "pyproject.toml"
    blob = subprocess.run(
        ("git", "hash-object", "--", "packing/pyproject.toml"),
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    _, _, observed = bind_clean_tracked_source(path, blob)
    assert observed == blob
    with pytest.raises(ValueError, match="does not match expected"):
        bind_clean_tracked_source(path, "0" * 40)


def test_four_owner_source_uses_conditional_threshold_inputs_without_float_recovery() -> None:
    receipt, _ = _completed_source(owner_count=4)
    _, arms, directions, owner_count = _source_configuration(receipt)
    endpoint = next(arm for arm in arms if arm.label == "endpoint")
    atoms, total = _endpoint_atoms(receipt, endpoint)
    assert owner_count == 4
    assert total == Fraction(1)
    assert len(directions) == 1
    assert len(endpoint.footprints) == 4
    assert len(atoms) == 1


def test_full_scope_detects_an_escape_omitted_by_a_retained_scope(monkeypatch) -> None:
    axis = rotation_from_half_tangent("axis", Fraction(0))
    near = (
        (Fraction(-1, 10), Fraction(-1, 10)),
        (Fraction(1, 10), Fraction(-1, 10)),
        (Fraction(1, 10), Fraction(1, 10)),
        (Fraction(-1, 10), Fraction(1, 10)),
    )
    far = tuple((x + 2, y + 2) for x, y in near)
    sites = SiteSet(Fraction(4), (((Fraction(0), Fraction(0)),),))
    retained_arm = Arm("endpoint", None, sites, (), ((near,),), (None,))
    full_arm = Arm("endpoint", None, sites, (), ((near,), (far,)), (None, None))
    atom = Atom("only", Fraction(0), Fraction(0), Fraction(1))
    source = BoundSource(
        Path("synthetic.json"),
        "synthetic",
        "synthetic",
        {},
        retained_arm,
        (axis,),
        (atom,),
        Fraction(1),
        1,
    )

    def scopes(_source: BoundSource, scope: str):
        return (retained_arm, (axis,)) if scope == "retained" else (full_arm, (axis, axis))

    monkeypatch.setattr(replay_module, "replay_directions", scopes)
    retained = exact_replay(
        source,
        scope="retained",
        max_atoms=10,
        max_event_cells=100,
        max_total_event_cells=200,
        deadline_seconds=10,
    )
    full = exact_replay(
        source,
        scope="full",
        max_atoms=10,
        max_event_cells=100,
        max_total_event_cells=200,
        deadline_seconds=10,
    )
    assert retained["summary"]["minimum_covered_mass"] == "1"
    assert full["summary"]["minimum_covered_mass"] == "0"
