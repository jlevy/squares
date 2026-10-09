"""Finite source identities retain exact custody and honest adoption status."""

from __future__ import annotations

import copy
from collections import Counter
from fractions import Fraction
from types import SimpleNamespace
from typing import Any

import pytest
from jsonschema_rs import Draft202012Validator

from devtools import backfill_algebraic_facts as backfill
from devtools import build_exact_values as exact
from devtools import register_gupta_reports as gupta
from devtools import register_ryxu_reports as ryxu
from sqpack.exact_values import DERIVED_FROM_EXACT_FORM, derive_from_exact_form
from sqpack.yamlio import safe_load


def _current_case(n: int) -> dict[str, Any]:
    text = (exact.FRONTIER / f"n-{n:03d}.md").read_text()
    return safe_load(backfill.backfilled(text, n).split("---", 2)[1])["packing"]


@pytest.mark.parametrize(("writer", "n"), [(ryxu, 51), (ryxu, 70), (gupta, 88)])
def test_imported_writers_derive_current_identity_and_backfill_is_idempotent(writer, n):
    reported = writer.reported_bound(n)
    facts = derive_from_exact_form(reported["exact_form"])
    assert reported["minimal_polynomial"] == facts.text
    assert reported["algebraic_degree"] == facts.degree
    assert reported["algebraic_source"] == DERIVED_FROM_EXACT_FORM
    text = (exact.FRONTIER / f"n-{n:03d}.md").read_text()
    rendered = backfill.backfilled(text, n)
    assert backfill.backfilled(rendered, n) == rendered
    bound = safe_load(rendered.split("---", 2)[1])["packing"]["reported_upper_bound"]
    for field in backfill.FIELDS:
        assert bound[field] == reported[field]


@pytest.fixture(scope="module")
def current_imports():
    inputs = exact.VerifiedRationalInputs()
    return {
        n: exact.build_entry(
            n,
            _current_case(n),
            exact.catalogue_entries().get(n),
            None,
            verified_inputs=inputs,
        )
        for n in (*ryxu.houses.NUMBERS, *gupta.houses.NUMBERS)
    }


def test_all_thirty_two_imports_identify_native_sides_without_optimality(current_imports):
    assert len(current_imports) == 32
    for n, entry in current_imports.items():
        case = exact.load_packing(n)
        facts = derive_from_exact_form(case["reported_upper_bound"]["exact_form"])
        assert entry["polynomial"]["coefficients"] == list(map(str, facts.coefficients))
        assert entry["algebraic_source"] == DERIVED_FROM_EXACT_FORM
        assert entry["side"]["relation"] == "upper-bound"
        assert entry["state"] == ("closed-form" if n == 51 else "rational")
        provenance = next(
            note for note in entry["notes"] if note["kind"] == "verified-witness-side"
        )
        assert "finite" in provenance["text"]
        assert "optimality" in provenance["text"]


def test_current_n102_route_keeps_its_group_and_retained_pose_prerequisites(current_imports):
    current = current_imports[102]
    assert current["state"] == "rational"
    (route,) = [note for note in current["notes"] if note["kind"] == "route"]
    assert route["bead"] == "think-ohhz"
    text = route["text"]
    for prerequisite in (
        "bind and convert the already retained current ry-xu certificate",
        "8dc415296f697f5140caea27c7a0193d52deb4e6",
        "active, weak and forced contacts and frozen variables",
        "confirm the current-pose seed",
        "W7 driver and n11 control before a preregistered bounded W6 run",
        "evand 13ee36e5 input remains a historical fixture",
        "claims do not transfer to this new geometry",
    ):
        assert prerequisite in text
    assert "ideal contact research open" in text


@pytest.mark.parametrize(
    "control", ["form", "polynomial", "source", "evidence", "display", "degree"]
)
def test_current_import_refuses_mismatched_native_metadata(control):
    case = copy.deepcopy(_current_case(88))
    bound = case["reported_upper_bound"]
    if control == "form":
        bound["exact_form"] = case["verified_upper_bound"]["exact_form"] = "9"
    elif control == "polynomial":
        bound.update(minimal_polynomial="s - 9 = 0", algebraic_source=DERIVED_FROM_EXACT_FORM)
    elif control == "source":
        case["n"] = 87
    elif control == "evidence":
        case["verified_upper_bound"]["evidence"] = []
    elif control == "display":
        bound["value"] = case["verified_upper_bound"]["value"] = "9.8824510304812468"
    else:
        bound["algebraic_degree"] = 2
    with pytest.raises(exact.ExactValuesError, match="imported exact bound refused"):
        exact.build_entry(88, case, None, None)


def test_current_import_requires_evidence_certificate_path():
    inputs = exact.VerifiedRationalInputs()
    identifier = gupta.houses.reports.EXACT_EVIDENCE
    row = copy.deepcopy(inputs.evidence_row(88, identifier, gupta.houses.reports.SOURCE_KEY))
    row["certificate"] = "packing/resources/wrong-certificate.json.xz"
    inputs.evidence = {identifier: row}
    with pytest.raises(exact.ExactValuesError, match="certificate"):
        exact.build_entry(88, _current_case(88), None, None, verified_inputs=inputs)


def _standing_entries() -> list[dict[str, Any]]:
    # These lightweight standing entries use exact forms, not rounded display equality.
    entries = []
    for n in range(1, 325):
        bound = exact.load_packing(n)["reported_upper_bound"]
        entries.append(
            {
                "n": n,
                "side": {"value": bound["value"]},
                "exact_form": bound.get("exact_form"),
                "notes": [],
                "checks": {},
            }
        )
    return entries


@pytest.fixture(scope="module")
def source_history():
    return exact.source_certificate_history(_standing_entries())


def test_all_noncurrent_certificates_keep_disposition_native_identity_and_assurance(
    source_history,
):
    assert len(source_history) == 29
    assert Counter(row["kind"] for row in source_history) == {
        "superseded": 14,
        "unreconciled-source": 15,
    }
    identities = Counter((row["n"], Fraction(row["exact_form"])) for row in source_history)
    assert len(identities) == 28
    assert [(n, count) for (n, _side), count in identities.items() if count > 1] == [(155, 2)]
    pending105 = [
        row
        for row in source_history
        if row["n"] == 105 and row["kind"] == "unreconciled-source"
    ]
    assert len(pending105) == 2
    for row in source_history:
        rational = Fraction(row["exact_form"])
        assert row["polynomial"]["coefficients"] == [
            str(rational.denominator),
            str(-rational.numerator),
        ]
        assert row["checks"]["root"]["interval"] == [str(rational), str(rational)]
        custody = row["source_certificate"]
        assert custody["global_optimality"] == "not-established"
        if custody["result"] in ("T-128", "T-130", "T-131"):
            assert (custody["verification"], custody["confirmation"]) == ("V0", "C0")
            assert custody["geometry_replay"] == "native-replay-retained"
            assert custody["adoption"] == "pending"
        elif custody["result"] == "T-129":
            assert custody["geometry_replay"] == "not-replayed"
            assert custody["receipt"] is None
        else:
            assert (custody["verification"], custody["confirmation"]) == ("V3", "C3")


def test_record_hunt_retains_two_source_occurrences_without_replacing_couzo(source_history):
    hunt = exact.hunt_reports
    facts = hunt.read_facts()
    (new132,) = [
        row for row in source_history if row["source_certificate"]["result"] == "T-131"
    ]
    assert new132["n"] == 132
    assert Fraction(new132["exact_form"]) == facts[132].side
    assert new132["source_certificate"]["source_key"] == hunt.SOURCE_KEY
    equal155 = [row for row in source_history if row["n"] == 155]
    assert [row["source_certificate"]["source_key"] for row in equal155] == [
        exact.couzo_refinements.SOURCE_KEY,
        hunt.SOURCE_KEY,
    ]
    assert all(row["source_certificate"]["result"] == "T-128" for row in equal155)
    assert all(Fraction(row["exact_form"]) == facts[155].side for row in equal155)
    assert (
        equal155[0]["source_certificate"]["facts"] != equal155[1]["source_certificate"]["facts"]
    )
    assert (
        equal155[0]["source_certificate"]["receipt"]
        != equal155[1]["source_certificate"]["receipt"]
    )
    assert "equal-bound evidence update" in equal155[1]["text"]
    for row in (new132, equal155[1]):
        assert row["attribution"]["date_mentions"] == ["2026-10-09"]
        assert row["source_certificate"]["revision"] == hunt.REVISION
        assert row["source_certificate"]["original_certificate"] == hunt.certificate_path(
            row["n"]
        )
        assert (
            row["source_certificate"]["facts"]
            == (hunt.PACKET / "source" / hunt.certificate_path(row["n"]))
            .relative_to(exact.ROOT.parent)
            .as_posix()
        )
        assert (
            row["source_certificate"]["receipt"]
            == hunt.receipt_path().relative_to(exact.ROOT.parent).as_posix()
        )


@pytest.fixture(scope="module")
def equal_hunt_inputs(source_history):
    previous = next(
        row
        for row in source_history
        if row["n"] == 155
        and row["source_certificate"]["source_key"] == exact.couzo_refinements.SOURCE_KEY
    )
    certificate = exact.hunt_reports.read_facts()[155]
    comparison = next(
        row["equal_side"]
        for row in exact.hunt_reports.check_claims()["results"]
        if row["n"] == 155
    )
    return _standing_entries()[154], previous, certificate, comparison


@pytest.mark.parametrize(
    "control", ["result", "source", "side", "prior-custody", "missing-prior"]
)
def test_equal_bound_occurrence_refuses_wrong_comparison_or_couzo_custody(
    equal_hunt_inputs, control
):
    current, previous, certificate, comparison = copy.deepcopy(equal_hunt_inputs)
    if control == "result":
        comparison["result"] = "T-131"
    elif control == "source":
        comparison["source_key"] = exact.hunt_reports.SOURCE_KEY
    elif control == "side":
        comparison["exact_side"] = str(certificate.side + 1)
    elif control == "prior-custody":
        previous["source_certificate"]["receipt"] = "packing/resources/wrong-receipt.json.xz"
    else:
        previous = None
    with pytest.raises(exact.ExactValuesError, match="record-hunt equal-bound"):
        exact.hunt_equal_bound_occurrence(current, previous, certificate, comparison)


def test_equal_bound_occurrence_does_not_depend_on_source_zero_mode_claims(equal_hunt_inputs):
    current, previous, certificate, comparison = copy.deepcopy(equal_hunt_inputs)
    comparison["differing_are_zero_modes"] = False
    comparison["source_zero_mode_squares"] = []
    occurrence = exact.hunt_equal_bound_occurrence(current, previous, certificate, comparison)
    assert occurrence is not None
    assert "does not establish a connecting motion" in occurrence["text"]
    assert "equivalence of local minima" in occurrence["text"]


def test_other_duplicate_finite_identity_still_refuses_distinct_custody(monkeypatch):
    side = exact.couzo_refinements.read_facts()[105].side
    monkeypatch.setattr(
        exact.couzo_followup, "read_facts", lambda: {105: SimpleNamespace(side=side)}
    )
    monkeypatch.setattr(exact.couzo_followup, "check_certification", dict)
    with pytest.raises(
        exact.ExactValuesError, match="duplicate finite identity has distinct custody/assurance"
    ):
        exact.source_certificate_history(_standing_entries())


@pytest.mark.parametrize(
    "control", ["verification", "confirmation", "geometry_replay", "receipt"]
)
def test_record_hunt_schema_refuses_promoted_or_missing_replay(source_history, control):
    schema = safe_load((exact.FRONTIER / exact.SCHEMA).read_text())
    validator = Draft202012Validator(
        {"$ref": "#/$defs/historical_entry", "$defs": schema["$defs"]}
    )
    row = copy.deepcopy(
        next(row for row in source_history if row["source_certificate"]["result"] == "T-131")
    )
    assert validator.is_valid(row)
    row["source_certificate"][control] = {
        "verification": "V3",
        "confirmation": "C3",
        "geometry_replay": "not-replayed",
        "receipt": None,
    }[control]
    assert not validator.is_valid(row)


def test_superseded_daniel_source_keeps_custody_and_assurance_without_current_note(monkeypatch):
    candidate = next(row for row in exact.reported_roots.collect() if row["n"] == 102)
    monkeypatch.setattr(exact.reported_roots, "collect", lambda: [copy.deepcopy(candidate)])
    current = {"n": 102, "side": {"value": "10.6058286965106059"}, "notes": []}
    historical = exact.append_reported_source_notes([current])
    assert current["notes"] == []
    assert historical[0]["kind"] == "superseded"
    assert historical[0]["reported_source"] == candidate["reported_source"]
    assert historical[0]["assurance"] == candidate["assurance"]
    assert "below" not in historical[0]["text"]


def test_certificate_schema_requires_custody_and_honest_replay_status(source_history):
    schema = safe_load((exact.FRONTIER / exact.SCHEMA).read_text())
    validator = Draft202012Validator(
        {"$ref": "#/$defs/historical_entry", "$defs": schema["$defs"]}
    )
    for row in source_history:
        assert validator.is_valid(row), row["n"]
    row = copy.deepcopy(source_history[0])
    del row["source_certificate"]["facts"]
    assert not validator.is_valid(row)
    row = copy.deepcopy(
        next(row for row in source_history if row["source_certificate"]["result"] == "T-129")
    )
    row["source_certificate"].update(verification="V3", confirmation="C3")
    assert not validator.is_valid(row)


@pytest.mark.parametrize(
    ("kind", "adoption"),
    [("unreconciled-source", "not-selected"), ("superseded", "pending")],
)
def test_certificate_schema_refuses_adoption_disposition_contradiction(
    source_history, kind, adoption
):
    schema = safe_load((exact.FRONTIER / exact.SCHEMA).read_text())
    validator = Draft202012Validator(
        {"$ref": "#/$defs/historical_entry", "$defs": schema["$defs"]}
    )
    row = copy.deepcopy(
        next(row for row in source_history if row["source_certificate"]["result"] == "T-128")
    )
    assert validator.is_valid(row)
    row["kind"] = kind
    row["source_certificate"]["adoption"] = adoption
    assert not validator.is_valid(row)
    if kind == "unreconciled-source":
        for scoped in source_history:
            if scoped["source_certificate"]["result"] in ("T-125", "T-127"):
                contradiction = copy.deepcopy(scoped)
                contradiction["kind"] = kind
                assert not validator.is_valid(contradiction)


def test_new_build_reopens_complete_imported_house_custody(monkeypatch):
    def changed():
        raise ValueError("changed complete native jobs or selected house")

    monkeypatch.setattr(gupta.houses, "check_houses", changed)
    with pytest.raises(exact.ExactValuesError, match="complete native jobs"):
        exact.build_entry(
            88, _current_case(88), None, None, verified_inputs=exact.VerifiedRationalInputs()
        )


@pytest.mark.parametrize(("writer", "n"), [(ryxu, 51), (gupta, 88)])
def test_owner_adopters_keep_derived_identity_after_backfill(writer, n):
    text = (exact.FRONTIER / f"n-{n:03d}.md").read_text()
    existing = backfill.backfilled(text, n)
    draft = existing
    if n == 51:
        # Curated n51 has no generic lower section until its owner receives a draft.
        draft = draft.replace(
            "\n<!-- BEGIN verification code",
            "\n## The lower bound\n\nRetained lower-lane draft.\n"
            "\n<!-- BEGIN verification code",
            1,
        )
    regenerated = writer.adopt_case(n, existing, draft)
    assert backfill.backfilled(regenerated, n) == regenerated
    bound = safe_load(regenerated.split("---", 2)[1])["packing"]["reported_upper_bound"]
    assert bound["algebraic_source"] == DERIVED_FROM_EXACT_FORM
    assert bound["minimal_polynomial"] == writer.reported_bound(n)["minimal_polynomial"]
