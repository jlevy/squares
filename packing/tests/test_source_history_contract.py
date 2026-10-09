"""Keep generated source-only histories complete without promoting their evidence.

These controls consume the retained register and source rows; the producer's exact
arithmetic and packet replay have separate tests and are not repeated here.
"""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from typing import Any

import pytest
from jsonschema_rs import Draft202012Validator

from devtools import collect_reported_exact_roots as roots
from devtools import evand_report_catalogue as reports
from devtools import validate_schemas
from devtools.retained_data import read_retained_text


@pytest.fixture(scope="module")
def register() -> dict[str, Any]:
    return json.loads(read_retained_text(validate_schemas.EXACT_VALUES))["register"]


@pytest.fixture(scope="module")
def schema() -> dict[str, Any]:
    return validate_schemas.load_schema("exact-values.schema.yaml")


def _validator(schema: dict[str, Any], definition: str) -> Draft202012Validator:
    return Draft202012Validator(
        {
            "$schema": schema["$schema"],
            "$defs": schema["$defs"],
            "$ref": f"#/$defs/{definition}",
        }
    )


def _reported_rows(register: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        row
        for row in register["historical_entries"]
        if row["algebraic_source"] == "reported-source-polynomial"
    ]


def test_generated_source_histories_preserve_complete_notes_and_source_rows(
    register: dict[str, Any], schema: dict[str, Any]
) -> None:
    Draft202012Validator(schema).validate(register)
    historical = _reported_rows(register)
    assert len(historical) == len(reports.NEW_DEGREES)
    assert {row["n"] for row in historical} == reports.NEW_DEGREES.keys()
    entries = {row["n"]: row for row in register["entries"]}
    sources = {row["n"]: row for row in json.loads(read_retained_text(roots.SOURCE_FILE))}
    for row in historical:
        n = row["n"]
        entry = entries[n]
        notes = [
            note for note in entry["notes"] if note["kind"] == "unreconciled-source-polynomial"
        ]
        assert len(notes) == 1
        assert row == {
            **notes[0],
            "n": n,
            "kind": "unreconciled-source",
            "algebraic_source": "reported-source-polynomial",
            "current_side": entry["side"]["value"],
        }
        source = copy.deepcopy(sources[n])
        for key in ("S_poly_ascending", "field_poly_ascending"):
            source[key] = [str(coefficient) for coefficient in source[key]]
        assert row["reported_source"]["row"] == source
        assert row["reported_source"]["revision"] == reports.REVISION
        assert row["degree"] == reports.NEW_DEGREES[n]
        assert row["sources"][0]["source_flags"] == [
            f"source-reported {key}={json.dumps(source[key])}"
            for key in ("verify_exact", "lean_packs", "lean_local_min", "new")
        ]
        assert row["assurance"] == {
            "verification": "V0",
            "confirmation": "C0",
            "algebraic_identity": "independently-checked",
            "geometry_replay": "not-attempted",
            "lean_replay": "not-attempted",
            "current_pose_identity": "not-established",
            "global_optimality": "not-established",
        }
        assert row["checks"]["catalogue"] == "not-in-catalogue"
        assert Fraction(row["checks"]["root"]["interval"][1]) < Fraction(entry["side"]["value"])
        assert row["polynomial"]["coefficients"] != entry["polynomial"]["coefficients"]


@pytest.mark.parametrize(
    "control",
    [
        "missing-custody",
        "missing-assurance",
        "missing-text",
        "wrong-origin",
        "superseded-packing",
        "null-root",
        "null-irreducibility",
        "null-decimal",
        "V1",
        "C1",
        "geometry-replayed",
        "lean-replayed",
        "current-pose-identified",
        "global-optimality",
        "missing-source-labels",
        "unknown-assurance",
        "unknown-source-row",
        "missing-source-flag",
        "mistyped-source-flag",
        "numeric-source-coefficient",
        "numeric-field-coefficient",
        "missing-acquisition",
    ],
)
def test_source_history_schema_refuses_lost_custody_and_promoted_evidence(
    control: str, register: dict[str, Any], schema: dict[str, Any]
) -> None:
    row = copy.deepcopy(_reported_rows(register)[0])
    validator = _validator(schema, "historical_entry")
    validator.validate(row)
    match control:
        case "missing-custody":
            del row["reported_source"]
        case "missing-assurance":
            del row["assurance"]
        case "missing-text":
            del row["text"]
        case "wrong-origin":
            row["algebraic_source"] = "catalogue"
        case "superseded-packing":
            row["kind"] = "superseded"
        case "null-root" | "null-irreducibility" | "null-decimal":
            key = {
                "null-root": "root",
                "null-irreducibility": "irreducible",
                "null-decimal": "decimal",
            }[control]
            row["checks"][key] = None
        case "V1":
            row["assurance"]["verification"] = "V1"
        case "C1":
            row["assurance"]["confirmation"] = "C1"
        case "geometry-replayed":
            row["assurance"]["geometry_replay"] = "passed"
        case "lean-replayed":
            row["assurance"]["lean_replay"] = "passed"
        case "current-pose-identified":
            row["assurance"]["current_pose_identity"] = "established"
        case "global-optimality":
            row["assurance"]["global_optimality"] = "established"
        case "missing-source-labels":
            del row["sources"][0]["source_flags"]
        case "unknown-assurance":
            row["assurance"]["optimal"] = True
        case "unknown-source-row":
            row["reported_source"]["row"]["independently_verified"] = True
        case "missing-source-flag":
            del row["reported_source"]["row"]["verify_exact"]
        case "mistyped-source-flag":
            row["reported_source"]["row"]["verify_exact"] = "true"
        case "numeric-source-coefficient":
            row["reported_source"]["row"]["S_poly_ascending"][0] = 1
        case "numeric-field-coefficient":
            row["reported_source"]["row"]["field_poly_ascending"][0] = 1
        case "missing-acquisition":
            del row["reported_source"]["acquisition"]
        case _:
            raise AssertionError(f"unhandled source history control: {control}")
    assert list(validator.iter_errors(row)), control


@pytest.mark.parametrize("control", ["catalogue", "unknown-check", "missing-expression"])
def test_derived_history_checks_remain_closed_and_identify_their_expression(
    control: str, register: dict[str, Any], schema: dict[str, Any]
) -> None:
    row = copy.deepcopy(
        next(
            row
            for row in register["historical_entries"]
            if row["algebraic_source"] == "derived-from-source-closed-form"
        )
    )
    validator = _validator(schema, "historical_entry")
    validator.validate(row)
    if control == "catalogue":
        row["checks"]["catalogue"] = "matches"
    elif control == "unknown-check":
        row["checks"]["unchecked_certificate"] = True
    else:
        del row["exact_form"]
    assert list(validator.iter_errors(row)), control


def test_n83_keeps_its_source_ordinal_without_claiming_a_computed_count(
    register: dict[str, Any], schema: dict[str, Any]
) -> None:
    entry = next(row for row in register["entries"] if row["n"] == 83)
    assert entry["checks"]["root"]["source_index"] == {"stated": 27, "counted": None}
    validator = _validator(schema, "entry")
    validator.validate(entry)
    broken = copy.deepcopy(entry)
    broken["checks"]["root"]["source_index"]["counted"] = 0
    assert list(validator.iter_errors(broken))
