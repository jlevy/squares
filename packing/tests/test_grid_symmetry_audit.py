"""Symmetry audit controls: synthetic empty and one-unit occupancies, and the H260 replay."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import cast

import pytest

from devtools import audit_grid_symmetry as audit

RESULTS = Path(__file__).resolve().parents[1] / (
    "campaign/series/series-000-smoke-and-calibration/results"
)
H259 = RESULTS / "exp-240-n17-mixed-capacity-census/run-001"
H260 = RESULTS / "exp-241-n17-closed-cell-symmetry/run-001"


def packet() -> dict[str, object]:
    counts = [25, 1, 1, 1, 5, 5, 5, 5]
    return {
        "schema": audit.SOURCE_SCHEMA,
        "grid_size": 5,
        "capacities": list(audit.CAPACITIES),
        "target": 1,
        "actions": [
            {"name": name, "cycle_profile": profile, "fixed_assignments": count}
            for name, profile, count in zip(audit.NAMES, audit.profiles(), counts, strict=True)
        ],
        "fixed_sum": 48,
        "orbit_assignments": 6,
        "counted_objects": audit.COUNTED_OBJECTS,
    }


def test_hand_derived_synthetic_counts() -> None:
    assert audit.fixed_counts(0) == [1] * 8
    assert audit.fixed_counts(1) == [25, 1, 1, 1, 5, 5, 5, 5]
    result = audit.audit_payload(packet(), 25, target=1)
    assert result["audit_passed"] is True
    assert result["orbit_assignments"] == 6


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("schema", "bad"),
        ("grid_size", True),
        ("target", True),
        ("capacities", [1] * 25),
        ("fixed_sum", 47),
        ("orbit_assignments", 5),
        ("counted_objects", "packings"),
        ("actions", []),
    ],
)
def test_mutations(key: str, value: object) -> None:
    receipt = packet()
    receipt[key] = value
    with pytest.raises(
        ValueError, match=r"schema|grid_size|target|capacities|sum|orbit|actions"
    ):
        audit.audit_payload(receipt, 25, target=1)


def test_action_and_identity_mutations() -> None:
    for field, value in [
        ("name", "r1"),
        ("fixed_assignments", 24),
        ("cycle_profile", [[True, 1]]),
    ]:
        receipt = deepcopy(packet())
        actions = cast(list[dict[str, object]], receipt["actions"])
        actions[0][field] = value
        with pytest.raises(ValueError, match=r"action|fixed|cycle"):
            audit.audit_payload(receipt, 25, target=1)
    with pytest.raises(ValueError, match="identity"):
        audit.audit_payload(packet(), 24, target=1)


def test_nonintegral_numbers_and_duplicates_refused() -> None:
    for raw in [b'{"a":1,"a":2}', b'{"a":1.0}', b'{"a":NaN}']:
        with pytest.raises(ValueError, match=r"duplicate|noninteger"):
            audit.decode(raw)


def test_non_target_fixture_cannot_pass_fixed_cli_contract() -> None:
    with pytest.raises(ValueError, match="target"):
        audit.audit_payload(packet(), 25)


def test_the_retained_h260_audit_replays_from_its_retained_inputs() -> None:
    """Closed-form arithmetic over the two retained receipts reproduces audit.json."""
    retained = json.loads((H260 / "audit.json").read_text())
    assert audit.audit(H260 / "count.json", H259 / "mixed.json") == retained


def test_identity_census_is_audited_by_content_not_bytes(tmp_path: Path) -> None:
    census = json.loads((H259 / "mixed.json").read_text())
    reformatted = tmp_path / "mixed.json"
    reformatted.write_text(json.dumps(census, indent=2) + "\n")
    result = audit.audit(H260 / "count.json", reformatted)
    assert result["identity_count"] == 161100756
    assert result["orbit_assignments"] == 20155518
    with pytest.raises(ValueError, match="different grid"):
        audit.identity_count_of(json.loads((H259 / "baseline.json").read_text()))
    with pytest.raises(ValueError, match="different target"):
        audit.identity_count_of(census, target=16)
    with pytest.raises(ValueError, match="target count"):
        audit.identity_count_of({**census, "target_assignments": 161100755})
