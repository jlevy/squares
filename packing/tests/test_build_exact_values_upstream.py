"""Finite source identities retain exact custody and honest adoption status."""

from __future__ import annotations

import copy
from collections import Counter
from dataclasses import replace
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
    legacy = [
        row
        for row in source_history
        if row["source_certificate"]["result"]
        in {"T-125", "T-127", "T-128", "T-129", "T-130", "T-131"}
    ]
    assert len(legacy) == 29
    assert Counter(row["kind"] for row in legacy) == {
        "superseded": 14,
        "unreconciled-source": 15,
    }
    identities = Counter((row["n"], Fraction(row["exact_form"])) for row in legacy)
    assert len(identities) == 28
    assert [(n, count) for (n, _side), count in identities.items() if count > 1] == [(155, 2)]
    pending105 = [
        row for row in legacy if row["n"] == 105 and row["kind"] == "unreconciled-source"
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
            assert (custody["verification"], custody["confirmation"]) == ("V3", "C3")
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
    equal155 = [
        row
        for row in source_history
        if row["n"] == 155 and row["source_certificate"]["result"] == "T-128"
    ]
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
@pytest.mark.parametrize("result", ["T-131", "T-146", "T-147", "T-148", "T-149", "T-150"])
def test_confirmed_source_schema_refuses_downgrade_or_missing_replay(
    source_history, control, result
):
    schema = safe_load((exact.FRONTIER / exact.SCHEMA).read_text())
    validator = Draft202012Validator(
        {"$ref": "#/$defs/historical_entry", "$defs": schema["$defs"]}
    )
    row = copy.deepcopy(
        next(row for row in source_history if row["source_certificate"]["result"] == result)
    )
    assert validator.is_valid(row)
    row["source_certificate"][control] = {
        "verification": "V0",
        "confirmation": "C0",
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


# Independent native identities reviewed in the 11 October intake, distinct from prints.
LATEST_CERTIFICATES = [
    {
        "result": "T-147",
        "n": 207,
        "exact_side": (
            "148809603730436756319360591381170501178639/100000000000000000000"
            "00000000000000000000"
        ),
        "ceiling": "14.8809603730436757",
        "source_key": "[PingYou n207 certificate 2026-10-11]",
        "source_commit": "9dc93b6ac2f8fefe038062a74c9a75bf05afdba6",
        "source_or_fact": (
            "packing/resources/web/pingyou-n207-certificate-2026-10-11/facts/n-207.yaml.gz"
        ),
        "native_receipt": (
            "packing/resources/web/pingyou-n207-certificate-2026-10-11/receip"
            "ts/exact-certification.json.xz"
        ),
        "original": "n207.cert.json",
    },
    {
        "result": "T-148",
        "n": 153,
        "exact_side": "6435006925203522001385040447/500000000000000000000000000",
        "ceiling": "12.8700138504070441",
        "source_key": "[PingYou n153 certificate 2026-10-11]",
        "source_commit": "bc328a7d727aedd0eabebd6ea80285f572b65d2d",
        "source_or_fact": (
            "packing/resources/web/pingyou-n153-certificate-2026-10-11/facts/n-153.yaml.gz"
        ),
        "native_receipt": (
            "packing/resources/web/pingyou-n153-certificate-2026-10-11/receip"
            "ts/exact-certification.json.xz"
        ),
        "original": "n153.cert.json",
    },
    {
        "result": "T-149",
        "n": 155,
        "exact_side": (
            "6476212703479228067826801266277003984977575753080931673578306476"
            "2127034792280678268012662770039849775757530809316735783/50000000"
            "0000000000000000000000000000000000000000000000000000000000000000"
            "0000000000000000000000000000000000000000000000"
        ),
        "ceiling": "12.9524254069584562",
        "source_key": "[Ostashev records 2026-10-11]",
        "source_commit": "c3d17ab08bd5db65dc5ffe69e41f7b2ff0c2fc49",
        "source_or_fact": (
            "packing/resources/web/dostashev-records-2026-10-11/source/records/n0155.sqcert"
        ),
        "native_receipt": (
            "packing/resources/web/dostashev-records-2026-10-11/receipts/exac"
            "t-certification.json.xz"
        ),
        "original": "records/n0155.sqcert",
    },
    {
        "result": "T-149",
        "n": 156,
        "exact_side": (
            "8111982883527766297069290937797918339306619994848173142743008111"
            "982883527766297069290937797918339306619994848173142743/625000000"
            "0000000000000000000000000000000000000000000000000000000000000000"
            "00000000000000000000000000000000000000000000"
        ),
        "ceiling": "12.9791726136444261",
        "source_key": "[Ostashev records 2026-10-11]",
        "source_commit": "c3d17ab08bd5db65dc5ffe69e41f7b2ff0c2fc49",
        "source_or_fact": (
            "packing/resources/web/dostashev-records-2026-10-11/source/records/n0156.sqcert"
        ),
        "native_receipt": (
            "packing/resources/web/dostashev-records-2026-10-11/receipts/exac"
            "t-certification.json.xz"
        ),
        "original": "records/n0156.sqcert",
    },
    {
        "result": "T-149",
        "n": 211,
        "exact_side": (
            "7498168360668157847329201553387328996546227450936608628725707498"
            "1683606681578473292015533873289965462274509366086287257/50000000"
            "0000000000000000000000000000000000000000000000000000000000000000"
            "0000000000000000000000000000000000000000000000"
        ),
        "ceiling": "14.9963367213363157",
        "source_key": "[Ostashev records 2026-10-11]",
        "source_commit": "c3d17ab08bd5db65dc5ffe69e41f7b2ff0c2fc49",
        "source_or_fact": (
            "packing/resources/web/dostashev-records-2026-10-11/source/records/n0211.sqcert"
        ),
        "native_receipt": (
            "packing/resources/web/dostashev-records-2026-10-11/receipts/exac"
            "t-certification.json.xz"
        ),
        "original": "records/n0211.sqcert",
    },
    {
        "result": "T-150",
        "n": 146,
        "exact_side": (
            "1162796491243115951268499610424932651360926707415737629286682777"
            "75998122712863472766532671969348798419026610394581005669/9240437"
            "1944551138870962994568170242433779780459571942094680604563058942"
            "40222303442118770000000000000000000000000000000"
        ),
        "ceiling": "12.5837822039510463",
        "source_key": "[Barnett refinements 2026-10-11]",
        "source_commit": "2573ff51c4b160c952bbb2d1c399e7430d9f9ae2",
        "source_or_fact": (
            "packing/resources/web/barnett-refinements-2026-10-11/facts/n-146.yaml.gz"
        ),
        "native_receipt": (
            "packing/resources/web/barnett-refinements-2026-10-11/receipts/ex"
            "act-certification.json.xz"
        ),
        "original": "certificates/n146.cert",
    },
    {
        "result": "T-150",
        "n": 261,
        "exact_side": (
            "2815119984437146057776712625526780010535117139958647843184531821"
            "56213791529093472577894719178723409384395264262601/1687845277338"
            "8004800535351238155816857400040173477095354881922318666694517637"
            "251382500000000000000000000000000000"
        ),
        "ceiling": "16.6787798753432078",
        "source_key": "[Barnett refinements 2026-10-11]",
        "source_commit": "2573ff51c4b160c952bbb2d1c399e7430d9f9ae2",
        "source_or_fact": (
            "packing/resources/web/barnett-refinements-2026-10-11/facts/n-261.yaml.gz"
        ),
        "native_receipt": (
            "packing/resources/web/barnett-refinements-2026-10-11/receipts/ex"
            "act-certification.json.xz"
        ),
        "original": "certificates/n261.cert",
    },
]


def test_declared_certificate_history_keeps_registered_native_sides_and_credit():
    entries = _standing_entries()
    before = copy.deepcopy(entries)
    rows = exact.declared_source_certificate_history(entries)
    assert entries == before
    assert Counter(row["source_certificate"]["result"] for row in rows) == {
        "T-134": 6,
        "T-135": 1,
        "T-136": 17,
        "T-137": 1,
        "T-138": 16,
        "T-139": 1,
        "T-140": 6,
        "T-141": 2,
        "T-146": 15,
        "T-147": 1,
        "T-148": 1,
        "T-149": 3,
        "T-150": 2,
    }
    for row in rows:
        side = Fraction(row["exact_form"])
        assert row["polynomial"]["coefficients"] == [
            str(side.denominator),
            str(-side.numerator),
        ]
        assert [Fraction(value) for value in row["checks"]["root"]["interval"]] == [side, side]
        custody = row["source_certificate"]
        assert (custody["verification"], custody["confirmation"]) == ("V3", "C3")
        assert custody["geometry_replay"] == "native-replay-retained"
        assert custody["adoption"] == "pending"
        assert custody["global_optimality"] == "not-established"
        assert (exact.ROOT.parent / custody["facts"]).is_file()
        assert (exact.ROOT.parent / custody["receipt"]).is_file()
    nondecimal = next(
        row
        for row in rows
        if row["n"] == 263 and row["source_certificate"]["result"] == "T-134"
    )
    assert Fraction(nondecimal["exact_form"]) == Fraction(
        7488939206954142477014939239, 447356905819500000000000000
    )
    regularized = next(
        row for row in rows if row["n"] == 70 and row["source_certificate"]["result"] == "T-146"
    )
    credit = " ".join(regularized["attribution"]["source_text"])
    assert "Ryan Xu" in credit
    assert "Eric Deleeuw" in credit
    assert "regularized" in credit
    assert "not a continuous proof" in credit
    assert regularized["attribution"]["date_mentions"] == ["2026-10-10"]


@pytest.mark.parametrize(
    "control",
    [
        "ambiguous",
        "source-key",
        "scope",
        "grade",
        "custody",
        "claims",
        "receipt",
        "missing-replay",
    ],
)
def test_declared_history_refuses_inconsistent_registration_or_retained_evidence(
    monkeypatch, control
):
    reports = exact.upper_bound_reports
    record = safe_load((exact.FRONTIER / "results.yaml").read_text())
    results = {row["id"]: row for row in record["results"]}
    if control == "ambiguous":
        results["duplicate"] = copy.deepcopy(results["T-140"])
    elif control == "source-key":
        results["T-140"]["attribution"]["source_keys"] = ["wrong source"]
    elif control == "scope":
        results["T-140"]["scope"]["n_values"] = [324]
    elif control == "grade":
        results["T-140"]["confirmation"] = "C0"
    monkeypatch.setattr(exact, "_finite_source_results", lambda: results)
    if control in {"custody", "claims", "receipt"}:

        def refuse(*_args, **_kwargs):
            raise reports.ReportError("changed " + control)

        operation = {
            "custody": "read_facts",
            "claims": "check_claims",
            "receipt": "check_certification",
        }[control]
        monkeypatch.setattr(reports, operation, refuse)
    elif control == "missing-replay":
        original = reports.check_certification

        def missing(*args, **kwargs):
            found = original(*args, **kwargs)
            if 132 in found:
                del found[132]
            return found

        monkeypatch.setattr(reports, "check_certification", missing)
    messages = {
        "ambiguous": "ambiguous",
        "source-key": "source key differs",
        "scope": "scope differs",
        "grade": "unsupported finite source grade",
        "custody": "changed custody",
        "claims": "changed claims",
        "receipt": "changed receipt",
        "missing-replay": "lacks native replay",
    }
    with pytest.raises(exact.ExactValuesError, match=messages[control]):
        exact.declared_source_certificate_history(_standing_entries())


def test_declared_tied_occurrences_keep_distinct_custody(monkeypatch):
    reports = exact.upper_bound_reports

    def facts(packet):
        return {
            row["n"]: SimpleNamespace(side=Fraction(3))
            for row in reports.load_declaration(packet)["certificates"]
        }

    monkeypatch.setattr(reports, "read_facts", facts)
    monkeypatch.setattr(reports, "check_claims", lambda *_args: {})
    monkeypatch.setattr(
        reports,
        "check_certification",
        lambda _packet, *, certificates: {n: {} for n in certificates},
    )
    rows = exact.declared_source_certificate_history(
        [row for row in _standing_entries() if row["n"] == 132]
    )
    assert len(rows) == 4
    assert {row["exact_form"] for row in rows} == {"3"}
    assert len({row["source_certificate"]["source_key"] for row in rows}) == 4
    assert len({row["source_certificate"]["facts"] for row in rows}) == 4
    assert len({row["source_certificate"]["receipt"] for row in rows}) == 4


@pytest.mark.parametrize(
    "expected", LATEST_CERTIFICATES, ids=lambda row: f"{row['result']}-{row['n']}"
)
def test_latest_source_native_identity_custody_and_credit(source_history, expected):
    (row,) = [
        row
        for row in source_history
        if row["n"] == expected["n"]
        and row["source_certificate"]["result"] == expected["result"]
    ]
    side = Fraction(expected["exact_side"])
    assert row["degree"] == 1
    assert Fraction(row["exact_form"]) == side
    assert row["polynomial"]["coefficients"] == [str(side.denominator), str(-side.numerator)]
    assert exact.evand.ceiling_decimal(side, 16) == expected["ceiling"]
    custody = row["source_certificate"]
    assert custody["source_key"] == expected["source_key"]
    assert custody["revision"] == expected["source_commit"]
    assert custody["facts"] == expected["source_or_fact"]
    assert custody["original_certificate"] == expected["original"]
    assert custody["receipt"] == expected["native_receipt"]
    assert custody["adoption"] == "pending"
    assert row["kind"] == "unreconciled-source"
    assert custody["global_optimality"] == "not-established"
    assert row["attribution"]["date_mentions"] == ["2026-10-11"]
    credit = " ".join(row["attribution"]["source_text"])
    names = {
        "T-147": ("PingYou Ltd", "Ryan Xu", "Evan Daniel"),
        "T-148": ("PingYou Ltd", "Ryan Xu", "Evan Daniel"),
        "T-149": ("Daniil Ostashev", "Yohei Nakajima", "Ryan Xu"),
        "T-150": ("Robert Barnett", "Ryan Xu", "Evan Daniel"),
    }
    assert all(name in credit for name in names[expected["result"]])
    if expected["result"] == "T-148":
        assert "degree-seven" in credit
        assert "no feasibility of the undilated contact solution" in row["text"]
    if expected["result"] == "T-149":
        issue_sides = {
            155: "12.952425406986414",
            156: "12.979172613722533",
            211: "14.996336737028043",
        }
        assert side < Fraction(issue_sides[row["n"]])


def test_barnett_unrequested_facts_stay_outside_the_registered_source_scope(source_history):
    reports = exact.upper_bound_reports
    packet = exact.ROOT / "resources/web/barnett-refinements-2026-10-11"
    facts = reports.read_facts(packet)
    claims = reports.check_claims(packet, facts)
    positives = reports.check_certification(packet, certificates=facts)
    assert set(facts) == set(positives) == {70, 103, 123, 146, 237, 261, 295}
    assert {row["n"] for row in claims["results"] if row["requested"]} == {146, 261}
    assert {
        row["n"] for row in source_history if row["source_certificate"]["result"] == "T-150"
    } == {146, 261}


@pytest.mark.parametrize("result", ["T-147", "T-148", "T-149", "T-150"])
@pytest.mark.parametrize("control", ["native-side", "frozen-claims", "missing-replay"])
def test_latest_source_projection_refuses_stale_identity_claims_or_replay(
    monkeypatch, result, control
):
    reports = exact.upper_bound_reports
    expected = next(row for row in LATEST_CERTIFICATES if row["result"] == result)
    n = expected["n"]
    packet = exact.ROOT.parent / expected["native_receipt"]
    packet = packet.parent.parent
    if control == "native-side":
        read_facts_original = reports.read_facts

        def changed_facts(path):
            certificates = read_facts_original(path)
            if path == packet:
                certificates[n] = replace(
                    certificates[n], side=certificates[n].side + Fraction(1, 10**1000)
                )
            return certificates

        monkeypatch.setattr(reports, "read_facts", changed_facts)
    elif control == "frozen-claims":
        # Change the stored comparison while leaving real claim recomputation active.
        stored_original = reports._stored  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]

        def changed_claims(path):
            record = stored_original(path)
            if path == packet / reports.CLAIMS:
                record = copy.deepcopy(record)
                record["results"][0]["exact_side"] = "3"
            return record

        monkeypatch.setattr(reports, "_stored", changed_claims)
    else:
        certification_original = reports.check_certification

        def missing_replay(path, **kwargs):
            positives = certification_original(path, **kwargs)
            if path == packet:
                del positives[n]
            return positives

        monkeypatch.setattr(reports, "check_certification", missing_replay)
    message = (
        "lacks native replay" if control == "missing-replay" else "frozen claim record differs"
    )
    with pytest.raises(exact.ExactValuesError, match=message):
        exact.declared_source_certificate_history(_standing_entries())
