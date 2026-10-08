"""One R preserves source assurance, date precision, and the selected pose's identity."""

from __future__ import annotations

import json
import math
from copy import deepcopy
from dataclasses import replace
from typing import Any

import pytest
from jsonschema import Draft202012Validator

from devtools import build_bound_citations, build_composite_figure_data, validate_schemas
from devtools.rigidity_status import (
    SOURCES,
    RigidityContext,
    date_precision,
    load_context,
    rigidity_metadata,
)
from sqpack.known_best import KNOWN_BEST_CORPUS
from sqpack.yamlio import safe_load


@pytest.fixture(scope="module")
def context() -> RigidityContext:
    return load_context()


@pytest.fixture(scope="module")
def figure() -> dict[str, Any]:
    return build_composite_figure_data.build_record()["figure"]


def test_every_selected_packing_has_one_binary_assessment_and_one_matching_badge(
    figure: dict[str, Any],
) -> None:
    expected = {n for n in KNOWN_BEST_CORPUS.numbers if math.isqrt(n) ** 2 == n} | {
        5,
        11,
        28,
        40,
    }
    assert {e["n"] for e in figure["entries"] if e["rigidity"]["known_rigid"]} == expected
    for entry in figure["entries"]:
        rigidity = entry["rigidity"]
        assert type(rigidity["known_rigid"]) is bool
        badges = [badge for badge in entry["badges"] if badge["glyph"] == "R"]
        assert badges == (
            [{"glyph": "R", "meaning": "known rigid", "style": "solid"}]
            if entry["n"] in expected
            else []
        )
        assert rigidity["assessed_geometry"]["witness_id"] == f"W-known-best-n{entry['n']:03d}"
        assert rigidity["assessments"]
    assert figure["totals"]["rigidity_known"] == 22
    primary = next(c for c in figure["composites"] if c["stem"] == "known-best-1-100")
    assert primary["totals"]["rigidity_known"] == 14


def test_additive_rigidity_metadata_preserves_all_existing_mathematical_facts(
    figure: dict[str, Any],
) -> None:
    retained = json.loads(build_composite_figure_data.RECORD.read_text())["figure"]
    old_entries = {entry["n"]: entry for entry in retained["entries"]}
    for entry in figure["entries"]:
        old = old_entries[entry["n"]]
        for key in ("n", "side", "lower", "optimality", "exactness"):
            assert entry[key] == old[key]
        for key in ("state", "basis", "provenance", "evidence"):
            assert entry["rigidity"][key] == old["rigidity"][key]
    assert figure["totals"]["rigidity_established"] == 20
    assert figure["totals"]["rigidity_catalogue_annotated"] == 2


def test_source_reports_remain_reports_when_the_icon_is_unified(
    context: RigidityContext,
) -> None:
    for n in (28, 40):
        record = rigidity_metadata(n, build_bound_citations.load_case(n), context=context)
        assert record["known_rigid"]
        assert record["assessments"][0]["property"] == "undetermined"
        positive = [a for a in record["assessments"] if a["property"] == "locally-rigid"]
        assert [a["assurance"] for a in positive] == ["reported"]


def test_dates_name_the_actual_proof_source_and_import_events(context: RigidityContext) -> None:
    five = rigidity_metadata(5, build_bound_citations.load_case(5), context=context)
    source = next(
        s
        for s in five["assessments"][0]["sources"]
        if s["evidence_ref"] == "E-n005-fixed-side-local-rigidity"
    )
    assert source["determined_at"] == "2026-09-03"
    assert "X-012" in source["date_reference"]
    eleven = rigidity_metadata(11, build_bound_citations.load_case(11), context=context)
    local = eleven["assessments"][0]["sources"][0]
    assert local["determined_at"] == "2026-08-24"
    assert local["date_reference"] == (
        "packing/campaign/agent-sessions/session-006-h026-exact-tangent.md"
    )
    assert "completed session" in local["date_note"]
    assert "exp-013" in local["reference"]
    assert local["reviewed_at"] == "2026-08-30"
    trump = next(
        s
        for a in eleven["assessments"]
        for s in a["sources"]
        if s.get("source_id") == "trump-2023-rigidity-assertion"
    )
    assert trump["determined_at"] == "2023"
    assert trump["determination_precision"] == "year"
    for assessment in eleven["assessments"]:
        for dated in assessment["sources"]:
            assert dated["recorded_at"] == "2026-10-08"
            assert "Import" in dated["recording_event"]
    tiling = rigidity_metadata(16, build_bound_citations.load_case(16), context=context)
    assert tiling["assessments"][0]["sources"][0]["determined_at"] is None


def test_unselected_rigid_alternatives_are_retained_without_transferring_their_claim(
    context: RigidityContext,
) -> None:
    alternatives = {entry["n"]: entry for entry in context.audit["alternatives"]}
    assert set(alternatives) == {52, 149, 296}
    assert [alternatives[n]["determined_at"] for n in (52, 149, 296)] == [
        "2005",
        "2024-11",
        None,
    ]
    for n, alternative in alternatives.items():
        assessed = rigidity_metadata(n, build_bound_citations.load_case(n), context=context)
        assert not assessed["known_rigid"]
        assert assessed["assessments"][0]["property"] == "not-rigid"
        assert assessed["assessed_geometry"]["source_url"] == alternative["selected_source_url"]
        assert alternative["alternative_source_url"] != alternative["selected_source_url"]
        assert alternative["disposition"] == "not-selected"


def test_a_same_side_different_variant_cannot_inherit_a_catalogue_assertion(
    context: RigidityContext,
) -> None:
    entries = deepcopy(dict(context.entries))
    entries[28]["source"]["url"] = "https://kingbird.myphotos.cc/packing/square-28_r1b.svg"
    changed = replace(context, entries=entries)
    with pytest.raises(ValueError, match="no source assertion matching the selected geometry"):
        rigidity_metadata(28, build_bound_citations.load_case(28), context=changed)


def test_a_numerical_no_motion_finding_never_becomes_known_rigid(
    context: RigidityContext,
) -> None:
    case = build_bound_citations.load_case(52)
    case["rigidity"]["property"] = "undetermined"
    assert not rigidity_metadata(52, case, context=context)["known_rigid"]
    case["rigidity"].update(
        property="locally-rigid", assurance="verified", method="exact-algebraic"
    )
    with pytest.raises(
        ValueError, match="verified rigidity requires at least one verified evidence"
    ):
        rigidity_metadata(52, case, context=context)


def test_conflicting_positive_and_motion_assessments_require_review(
    context: RigidityContext,
) -> None:
    case = build_bound_citations.load_case(28)
    case["rigidity"]["property"] = "not-rigid"
    with pytest.raises(
        ValueError, match="conflicts with the selected packing's motion assessment"
    ):
        rigidity_metadata(28, case, context=context)


@pytest.mark.parametrize(
    ("value", "precision"),
    [(None, "unknown"), ("2005", "year"), ("2024-11", "month"), ("2026-09-03", "day")],
)
def test_partial_dates_keep_their_supported_precision(
    value: str | None, precision: str
) -> None:
    assert date_precision(value) == precision


@pytest.mark.parametrize("value", ["2026-02-30", "2026-13", "2026-1", "26", "2026-10-08-01"])
def test_invalid_calendar_dates_are_rejected(value: str) -> None:
    with pytest.raises(ValueError, match="invalid determination date"):
        date_precision(value)


def test_the_source_index_and_generated_metadata_satisfy_their_declared_schemas(
    figure: dict[str, Any],
) -> None:
    assert validate_schemas.check(SOURCES) == []
    assert SOURCES in validate_schemas.corpus_paths()[1]
    schema = safe_load(
        (build_composite_figure_data.RECORD.parent / "composite-figure.schema.yaml").read_text()
    )
    Draft202012Validator(schema).validate(figure)
