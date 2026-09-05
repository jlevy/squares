#!/usr/bin/env python3
"""Behavior checks for the Experiment/v2 assurance migration."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from devtools.migrate_experiments_v2 import migrate_experiment
from sqpack.assurance import check_experiment_semantics

ROOT = Path(__file__).resolve().parent.parent


def legacy_experiment(precision: str = "f64_screen", experiment_id: str = "exp-001") -> dict:
    """Return the minimal historical payload needed to exercise the migration."""
    return {
        "id": experiment_id,
        "subject": {
            "label": "historical engine run",
            "engine": "test engine 0.1.0",
            "precision": precision,
        },
        "method": {
            "operator": "test",
            "entry_point": "tools/check.py",
            "command": "python tools/check.py",
            "record": "campaign/results/test.json",
        },
        "results": [
            {
                "shape": "record",
                "metric": "side",
                "direction": "lower",
                "score": 2.0,
                "standing_best": 2.0,
                "beat_record": False,
            }
        ],
    }


def require_error(errors: list[str], fragment: str) -> None:
    assert any(fragment in error for error in errors), errors


def require_dict(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError(f"expected object, got {type(value).__name__}")
    return value


def require_list(value: object) -> list[object]:
    if not isinstance(value, list):
        raise TypeError(f"expected list, got {type(value).__name__}")
    return value


def main() -> int:
    numeric = migrate_experiment(legacy_experiment())
    subject = require_dict(numeric["subject"])
    assert subject["assurance"] == "numerically-checked"
    assert subject["method"] == "numerical-f64"
    assert subject["precision"] == {"binary_bits": 53, "rounding": "nearest-even"}
    assert subject["tolerance"] == "unrecorded-historical"
    assert check_experiment_semantics(numeric) == []

    multiprecision = migrate_experiment(legacy_experiment("polished", "exp-012"))
    subject = require_dict(multiprecision["subject"])
    assert subject["method"] == "numerical-multiprecision"
    assert subject["precision"] == {"decimal_digits": 160, "rounding": "nearest"}
    assert subject["tolerance"] == "1e-80"
    assert check_experiment_semantics(multiprecision) == []

    exact = migrate_experiment(legacy_experiment("exact", "exp-013"))
    subject = require_dict(exact["subject"])
    assert subject["assurance"] == "verified"
    assert subject["method"] == "exact-algebraic"
    assert "precision" not in subject
    assert "tolerance" not in subject
    assert check_experiment_semantics(exact) == []

    false_record = deepcopy(numeric)
    first_result = require_dict(require_list(false_record["results"])[0])
    first_result["beat_record"] = True
    require_error(check_experiment_semantics(false_record), "beat_record requires verified")

    schema_document = yaml.safe_load(
        (ROOT / "campaign/schemas/experiment.schema.yaml").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema_document)
    complete = yaml.safe_load(
        next((ROOT / "campaign").glob("series/*/experiments/*.md"))
        .read_text(encoding="utf-8")
        .split("---\n")[1]
    )["experiment"]
    migrated_complete = migrate_experiment(complete)
    validator.validate(migrated_complete)
    legacy_complete = deepcopy(migrated_complete)
    require_dict(legacy_complete["subject"])["precision"] = "polished"
    legacy_serialized = yaml.safe_load(yaml.safe_dump(legacy_complete))
    assert list(validator.iter_errors(legacy_serialized))

    print("experiment assurance contract selftest passed")
    return 0


def test_experiment_assurance_contract() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
