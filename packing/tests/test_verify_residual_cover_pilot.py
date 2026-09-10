"""Controls for exact replay of residual-cover pilot proposals."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from devtools.verify_residual_cover_pilot import (
    OUTER_SIDE,
    RATIONALISATION_SCALE,
    REPO,
    RETAINED_INDICES,
    SQUARE_SIDE,
    arm_summary,
    replay,
    source_identity,
    validate_source_record,
    write_exclusive_atomic,
)
from sqpack.fractional.colgen import rationalise_sites, site_set_from_grids
from sqpack.fractional.model import Atom


def _source_record() -> dict[str, Any]:
    sites = site_set_from_grids(OUTER_SIDE, (19,), Fraction(1, 2))
    coordinates = [[[str(x), str(y)] for x, y in orbit] for orbit in sites.orbits]
    digest = hashlib.sha256(json.dumps(coordinates, separators=(",", ":")).encode()).hexdigest()
    weights = np.zeros(len(sites.orbits))
    weights[0] = 1
    atoms = rationalise_sites(sites, weights, scale=RATIONALISATION_SCALE)
    atom_rows = [[str(atom.x), str(atom.y), str(atom.weight)] for atom in atoms]
    total = str(sum((atom.weight for atom in atoms), Fraction(0)))
    arm = {
        "converged": True,
        "rationalisation_scale": RATIONALISATION_SCALE,
        "orbit_weights": weights.tolist(),
        "rationalised_atoms": atom_rows,
        "rationalised_total_mass": total,
    }
    return {
        "schema": "residual-cover-pilot/v1",
        "status": "complete",
        "settings": {
            "outer_side": str(OUTER_SIDE),
            "square_side": str(SQUARE_SIDE),
            "direction_indices": list(RETAINED_INDICES),
            "directions": len(RETAINED_INDICES),
            "full_181_direction_net": False,
            "max_rounds_per_arm": 60,
            "rows_per_direction": 4,
            "deadline_seconds_per_arm": 120.0,
            "max_dense_event_cells_per_direction": 2_000_000,
            "max_dense_event_cells_per_round": 15_000_000,
            "rationalisation_scale": RATIONALISATION_SCALE,
        },
        "support": {
            "source": "grids=(19,);inset=1/2",
            "sha256": digest,
            "orbits": len(sites.orbits),
            "sites": sites.size,
            "coordinates": coordinates,
        },
        "arms": {"unrestricted": dict(arm), "residual": dict(arm)},
    }


def test_source_validation_reconstructs_atoms_without_changing_weights() -> None:
    record = _source_record()
    _, proposals = validate_source_record(record)
    assert set(proposals) == {"unrestricted", "residual"}
    assert len(proposals["residual"]) == 4
    total = sum((atom.weight for atom in proposals["residual"]), Fraction(0))
    assert str(total) == record["arms"]["residual"]["rationalised_total_mass"]


def test_wrong_settings_and_modified_atoms_are_refused() -> None:
    wrong_settings = _source_record()
    wrong_settings["settings"]["outer_side"] = "4"
    with pytest.raises(ValueError, match="setting outer_side"):
        validate_source_record(wrong_settings)

    wrong_atoms = _source_record()
    wrong_atoms["arms"]["residual"]["rationalised_atoms"][0][2] = "2"
    with pytest.raises(ValueError, match="atoms disagree"):
        validate_source_record(wrong_atoms)


def test_retained_residual_replay_streams_nine_exact_progress_rows(
    capsys: pytest.CaptureFixture[str],
) -> None:
    result = replay(
        _source_record(),
        source={"sha256": "control"},
        scope="subset",
        arm_mode="residual",
        max_atoms=10,
        max_event_cells=10_000,
    )
    assert set(result["arms"]) == {"residual"}
    arm = result["arms"]["residual"]
    assert (
        arm["unchanged_rationalised_total_mass"]
        == _source_record()["arms"]["residual"]["rationalised_total_mass"]
    )
    assert len(arm["directions"]) == 9
    progress = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    assert len(progress) == 10
    assert all(row["progress"] == "direction-complete" for row in progress[:-1])
    assert progress[-1]["progress"] == "arm-complete"


def test_atom_and_event_guards_stop_before_unbounded_replay() -> None:
    with pytest.raises(ValueError, match="atoms above guard"):
        replay(
            _source_record(),
            source={"sha256": "control"},
            scope="subset",
            arm_mode="residual",
            max_atoms=3,
            max_event_cells=10_000,
        )
    with pytest.raises(ValueError, match="exact event cells"):
        replay(
            _source_record(),
            source={"sha256": "control"},
            scope="subset",
            arm_mode="residual",
            max_atoms=10,
            max_event_cells=1,
        )


def test_source_identity_confusion_and_output_overwrite_are_refused(tmp_path: Path) -> None:
    relative = Path(
        "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/"
        "exp-136-paired-cover.json"
    )
    source = REPO / relative
    blob = "2b34bdc8842edc836402bd42fe8362e9103ab253"
    assert source_identity(source, blob)["git_blob"] == blob
    with pytest.raises(ValueError, match="expected Git blob"):
        source_identity(source, "0" * 40)

    output = tmp_path / "exact.json"
    record: dict[str, object] = {"status": "complete"}
    write_exclusive_atomic(output, record)
    assert json.loads(output.read_text()) == record
    with pytest.raises(FileExistsError):
        write_exclusive_atomic(output, record)


def test_normalized_mass_is_only_reported_for_positive_complete_residual_full_net() -> None:
    atoms = (Atom("a", Fraction(1), Fraction(1), Fraction(3)),)
    rows: list[dict[str, object]] = [
        {"direction_index": index, "minimum_covered_mass": "3/2"} for index in range(181)
    ]
    full = arm_summary(atoms, rows, scope="full-net", label="residual")
    assert full["normalized_mass"] == "2"
    assert "optimum-gap" in str(full["normalization"])
    assert "normalized_mass" not in arm_summary(
        atoms, rows[:9], scope="subset", label="residual"
    )
    zero = [dict(rows[0], minimum_covered_mass="0")]
    assert "normalized_mass" not in arm_summary(atoms, zero, scope="full-net", label="residual")
