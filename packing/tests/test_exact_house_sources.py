"""Current house identities retain exact source custody without inheriting old poses."""

from __future__ import annotations

import copy
from collections import Counter
from fractions import Fraction
from pathlib import Path

import pytest
from jsonschema_rs import Draft202012Validator

from devtools import adopt_houses
from devtools import backfill_algebraic_facts as backfill
from devtools import build_exact_values as exact
from devtools import exact_house_sources as sources
from devtools import upper_bound_houses as houses
from sqpack.exact_values import DERIVED_FROM_EXACT_FORM
from sqpack.yamlio import safe_load


def case(n: int) -> dict:
    text = (exact.FRONTIER / f"n-{n:03d}.md").read_text()
    return safe_load(backfill.backfilled(text, n).split("---", 2)[1])["packing"]


@pytest.fixture(scope="module")
def current():
    inputs = exact.VerifiedRationalInputs()
    return {
        n: exact.build_entry(
            n, case(n), exact.catalogue_entries().get(n), None, verified_inputs=inputs
        )
        for n in houses.NUMBERS
    }


def test_all_forty_two_current_native_identities_have_complete_adopted_custody(current):
    assert len(current) == 42
    assert Counter(row["source_certificate"]["result"] for row in current.values()) == {
        "T-128": 5,
        "T-130": 3,
        "T-134": 1,
        "T-136": 5,
        "T-139": 1,
        "T-140": 5,
        "T-141": 2,
        "T-146": 13,
        "T-147": 1,
        "T-148": 1,
        "T-149": 3,
        "T-150": 2,
    }
    schema = safe_load((exact.FRONTIER / exact.SCHEMA).read_text())
    validator = Draft202012Validator({"$defs": schema["$defs"], "$ref": "#/$defs/entry"})
    for n, row in current.items():
        packing = case(n)
        side = houses.certificate(n).side
        assert Fraction(row["exact_form"]) == side
        assert row["degree"] == 1
        assert row["state"] == "rational"
        assert row["side"] == {
            "value": packing["reported_upper_bound"]["value"],
            "relation": "upper-bound",
        }
        assert row["polynomial"]["coefficients"] == [
            str(side.denominator),
            str(-side.numerator),
        ]
        assert [Fraction(value) for value in row["checks"]["root"]["interval"]] == [side, side]
        custody = row["source_certificate"]
        assert (custody["verification"], custody["confirmation"], custody["adoption"]) == (
            "V3",
            "C3",
            "adopted",
        )
        assert custody["receipt"]
        assert custody["geometry_replay"] == "native-replay-retained"
        assert custody["global_optimality"] == "not-established"
        assert row["source_occurrences"][0]["path"] == custody["facts"]
        assert row["attribution"]["source_text"]
        assert not list(validator.iter_errors(row)), n


@pytest.mark.parametrize("n", [132, 308])
def test_exact_source_print_and_verified_ceiling_are_separate_lanes(current, n):
    packing = case(n)
    assert packing["reported_upper_bound"]["value"] != packing["verified_upper_bound"]["value"]
    assert Fraction(current[n]["side"]["value"]) == Fraction(current[n]["exact_form"])
    assert Fraction(packing["verified_upper_bound"]["value"]) > Fraction(
        current[n]["exact_form"]
    )


@pytest.mark.parametrize(
    "control",
    [
        "degree",
        "bool-degree",
        "polynomial",
        "origin",
        "form",
        "source",
        "unknown-source",
        "missing-source",
        "reported",
        "verified",
        "evidence",
        "status",
    ],
)
def test_adopted_current_identity_refuses_stale_metadata(control):
    packing = copy.deepcopy(case(102))
    bound = packing["reported_upper_bound"]
    if control == "degree":
        bound["algebraic_degree"] = 2
    elif control == "bool-degree":
        bound["algebraic_degree"] = True
    elif control == "polynomial":
        bound["minimal_polynomial"] = "2000000000000000000000s - 21211657393021211657393 = 0"
    elif control == "origin":
        bound["algebraic_source"] = "contact-system"
    elif control == "form":
        bound["exact_form"] = packing["verified_upper_bound"]["exact_form"] = "10"
    elif control == "source":
        bound["source_key"] = "[PingYou n153 certificate 2026-10-11]"
    elif control == "unknown-source":
        bound["source_key"] = "[unknown]"
    elif control == "missing-source":
        del bound["source_key"]
    elif control == "reported":
        bound["value"] = "10.6058286965106059"
    elif control == "verified":
        packing["verified_upper_bound"]["value"] = bound["exact_form"]
    elif control == "evidence":
        packing["verified_upper_bound"]["evidence"] = []
    else:
        packing["status"] = "proved"
    with pytest.raises(exact.ExactValuesError, match="adopted exact bound refused"):
        exact.build_entry(102, packing, None, None)


def test_adopted_source_cannot_supply_an_unscoped_count():
    packing = copy.deepcopy(case(102))
    packing["n"] = 5
    with pytest.raises(exact.ExactValuesError, match="adopted source has no scoped count"):
        exact.build_entry(5, packing, None, None)


def test_empty_reporting_evidence_is_refused(monkeypatch):
    monkeypatch.setattr(sources.selection, "reporting", lambda *_arguments: [])
    with pytest.raises(exact.ExactValuesError, match="current reporting evidence"):
        exact.build_entry(102, case(102), None, None)


def test_current_house_custody_refusal_propagates(monkeypatch):
    def refused(_numbers):
        raise houses.HouseError("retained house geometry or receipt differs")

    monkeypatch.setattr(houses, "check_houses", refused)
    with pytest.raises(
        exact.ExactValuesError, match="retained house geometry or receipt differs"
    ):
        exact.build_entry(102, case(102), None, None)


@pytest.mark.parametrize("n", houses.NUMBERS)
def test_adopted_backfill_replaces_stale_catalogue_and_contact_metadata_only(n):
    text = (exact.FRONTIER / f"n-{n:03d}.md").read_text()
    _, front, body = text.split("---", 2)
    document = safe_load(front)
    bound = document["packing"]["reported_upper_bound"]
    bound.update(
        algebraic_degree=7, minimal_polynomial="s^7 - 1 = 0", algebraic_source="contact-system"
    )
    import yaml  # noqa: PLC0415

    stale = "---\n" + yaml.safe_dump(document, sort_keys=False) + "---" + body
    rendered = backfill.backfilled(stale, n)
    actual = safe_load(rendered.split("---", 2)[1])
    native = Fraction(bound["exact_form"])
    expected = copy.deepcopy(document)
    expected["packing"]["reported_upper_bound"].update(
        algebraic_degree=1,
        minimal_polynomial=exact.format_polynomial((native.denominator, -native.numerator)),
        algebraic_source=DERIVED_FROM_EXACT_FORM,
    )
    assert actual == expected
    assert rendered.split("---", 2)[2] == body
    assert backfill.backfilled(rendered, n) == rendered


def test_unrelated_contact_system_metadata_is_preserved():
    text = (
        (exact.FRONTIER / "n-005.md")
        .read_text()
        .replace(
            "algebraic_source: derived-from-exact-form", "algebraic_source: contact-system"
        )
    )
    assert (
        safe_load(text.split("---", 2)[1])["packing"]["reported_upper_bound"][
            "algebraic_source"
        ]
        == "contact-system"
    )
    assert backfill.backfilled(text, 5) == text


@pytest.mark.parametrize(
    "field",
    [
        "source_occurrences",
        "attribution",
        "source_statuses",
        "receipt",
        "adoption",
        "verification",
        "degree",
        "status",
    ],
)
def test_current_adopted_schema_refuses_lost_custody_or_weakened_scope(current, field):
    row = copy.deepcopy(current[102])
    schema = safe_load((exact.FRONTIER / exact.SCHEMA).read_text())
    validator = Draft202012Validator({"$defs": schema["$defs"], "$ref": "#/$defs/entry"})
    if field in {"source_occurrences", "attribution", "source_statuses"}:
        del row[field]
    elif field == "receipt":
        row["source_certificate"][field] = None
    elif field == "adoption":
        row["source_certificate"][field] = "pending"
    elif field == "verification":
        row["source_certificate"][field] = "V0"
    elif field == "degree":
        row[field] = 7
    else:
        row[field] = "proved"
    assert list(validator.iter_errors(row)), field


def test_adopted_metadata_transfers_every_original_occurrence_and_quote(current):
    prior = sources.read_prior()
    for saved in prior["selected_occurrences"]:
        row = current[saved["n"]]
        expected = copy.deepcopy(saved["source_certificate"])
        expected["adoption"] = "adopted"
        assert row["source_certificate"] == expected
        assert row["source_occurrences"] == saved["sources"]
        assert row["attribution"] == saved["attribution"]
        assert row["source_statuses"] == [
            "adopted-current" if value == "pending-adoption" else value
            for value in saved["source_statuses"]
        ]


def test_prior_capture_is_complete_lossless_and_refuses_different_overwrite(tmp_path: Path):
    import json  # noqa: PLC0415

    prior = sources.read_prior()
    register = tmp_path / "prior-register.json"
    register.write_text(
        json.dumps(
            {
                "softschema": {"contract": "packing.squares:ExactValues/v1"},
                "register": {
                    "entries": prior["current_entries"],
                    "historical_entries": prior["selected_occurrences"],
                },
            }
        )
    )
    archive = tmp_path / "prior.json.xz"
    result = sources.retain_prior(register, archive)
    assert result["current_entries"] == result["selected_occurrences"] == 42
    decoded = houses.kernel.read_xz(archive)
    sources.validate_prior(decoded)
    assert decoded == prior
    with pytest.raises(sources.reports.ReportError, match="private repository file"):
        sources.read_prior(archive)
    assert sources.retain_prior(register, archive) == result
    previous = archive.read_bytes()
    archive.write_bytes(b"existing source")
    with pytest.raises(sources.HouseIdentityError, match="immutable"):
        sources.retain_prior(register, archive)
    assert archive.read_bytes() == b"existing source"
    assert previous != b"existing source"


@pytest.mark.parametrize(
    "control",
    ["coefficient", "exact-form", "selected-side", "missing-current", "duplicate-occurrence"],
)
def test_prior_identity_and_scope_mutations_are_refused(control):
    prior = copy.deepcopy(sources.read_prior())
    if control == "coefficient":
        prior["current_entries"][0]["polynomial"]["coefficients"][0] = "1"
    elif control == "exact-form":
        prior["current_entries"][0]["exact_form"] = "10"
    elif control == "selected-side":
        prior["selected_occurrences"][0]["exact_form"] = "10"
    elif control == "missing-current":
        prior["current_entries"].pop()
    else:
        prior["selected_occurrences"].append(copy.deepcopy(prior["selected_occurrences"][0]))
    with pytest.raises(sources.HouseIdentityError):
        sources.validate_prior(prior)


def test_every_displaced_coefficient_vector_and_occurrence_survives(current):
    prior = sources.read_prior()
    rows = []
    for saved in prior["current_entries"]:
        n = saved["n"]
        side = Fraction(saved["exact_form"]) if saved["degree"] == 1 else None
        if side is not None:
            checks, _ = exact.polynomial_checks(
                n,
                tuple(map(int, saved["polynomial"]["coefficients"])),
                saved["side"]["value"],
                None,
                upward_ceiling=True,
            )
            rows.append(
                {
                    "n": n,
                    "kind": "superseded",
                    "polynomial": copy.deepcopy(saved["polynomial"]),
                    "checks": checks,
                    "sources": [],
                }
            )
    before = copy.deepcopy(prior)
    exact.append_displaced_current_history(list(current.values()), rows)
    assert sources.read_prior() == before
    assert len(rows) == 42
    for saved in prior["current_entries"]:
        (row,) = [
            row
            for row in rows
            if row["n"] == saved["n"] and row["polynomial"] == saved["polynomial"]
        ]
        assert all(
            occurrence in row["sources"] for occurrence in saved.get("source_occurrences", [])
        )
        assert any(
            source["path"] == sources.PRIOR.relative_to(houses.REPO).as_posix()
            for source in row["sources"]
        )
        assert Fraction(row["checks"]["root"]["interval"][0]) > Fraction(
            current[row["n"]]["checks"]["root"]["interval"][1]
        )


def test_displaced_current_schema_refuses_an_unreconciled_identity(current):
    rows = []
    exact.append_displaced_current_history(list(current.values()), rows)
    schema = safe_load((exact.FRONTIER / exact.SCHEMA).read_text())
    validator = Draft202012Validator(
        {"$defs": schema["$defs"], "$ref": "#/$defs/historical_entry"}
    )
    assert len(rows) == 42
    for row in rows:
        assert not list(validator.iter_errors(row)), row["n"]
        row["kind"] = "unreconciled-source"
        assert list(validator.iter_errors(row)), row["n"]


def test_post_adoption_source_history_conserves_selected_and_displaced_native_occurrences(
    current,
):
    entries = [
        current[n]
        if n in current
        else {
            "n": n,
            "side": {"value": exact.load_packing(n)["reported_upper_bound"]["value"]},
            "exact_form": exact.load_packing(n)["reported_upper_bound"].get("exact_form"),
            "notes": [],
            "checks": {},
        }
        for n in range(1, 325)
    ]
    before = copy.deepcopy(entries)
    history = exact.source_certificate_history(entries)
    assert entries == before
    prior = {
        n: safe_load(text.split("---", 2)[1])["packing"]
        for n, text in adopt_houses.read_history().items()
    }
    legacy = {
        exact.ryxu_houses.SOURCE_KEY: exact.ryxu_houses.reports.read_facts(),
        exact.gupta_houses.reports.SOURCE_KEY: exact.gupta_houses.reports.read_facts(),
    }
    displaced = {
        n: packing
        for n, packing in prior.items()
        if packing["reported_upper_bound"]["source_key"] in legacy
    }
    assert set(displaced) == {
        70,
        84,
        86,
        102,
        103,
        105,
        108,
        123,
        126,
        127,
        129,
        131,
        146,
        153,
        154,
        175,
        180,
        207,
        209,
        236,
        237,
        261,
        267,
        295,
    }
    assert Counter(
        packing["reported_upper_bound"]["source_key"] for packing in displaced.values()
    ) == {exact.ryxu_houses.SOURCE_KEY: 17, exact.gupta_houses.reports.SOURCE_KEY: 7}
    # The dated history had 101 offers. PR518 moves 42 into current custody and
    # displaces 24 additional native legacy identities that previously were current.
    assert len(history) == 83
    assert Counter(row["kind"] for row in history) == {"superseded": 83}
    assert all(row["source_certificate"]["adoption"] == "not-selected" for row in history)
    assert len(history) + len(current) == 101 + len(displaced) == 125
    for n, packing in displaced.items():
        bound = packing["reported_upper_bound"]
        native = legacy[bound["source_key"]][n].side
        assert native == Fraction(bound["exact_form"])
        (row,) = [
            row
            for row in history
            if row["n"] == n and row["source_certificate"]["source_key"] == bound["source_key"]
        ]
        assert Fraction(row["exact_form"]) == native
        assert row["source_certificate"]["geometry_replay"] == "native-replay-retained"
        assert row["source_certificate"]["receipt"]
    assert {(row["n"], row["source_certificate"]["result"]) for row in current.values()} == set(
        houses.ADOPTED.items()
    )
    assert not {
        (
            row["n"],
            row["source_certificate"]["source_key"],
            row["source_certificate"]["facts"],
        )
        for row in history
    } & {
        (
            row["n"],
            row["source_certificate"]["source_key"],
            row["source_certificate"]["facts"],
        )
        for row in current.values()
    }
    equal155 = [
        row
        for row in history
        if row["n"] == 155 and row["source_certificate"]["result"] == "T-128"
    ]
    assert len(equal155) == 2
    assert len({row["source_certificate"]["facts"] for row in equal155}) == 2
    assert len({row["source_certificate"]["receipt"] for row in equal155}) == 2
    assert current[155]["source_certificate"]["result"] == "T-149"
