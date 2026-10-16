"""Reviewed source spans survive source drift and preserve literal credit output."""

from __future__ import annotations

import copy
import html
import re
import shutil
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest
import yaml

from devtools.contributor_census import (
    _join,  # pyright: ignore[reportPrivateUsage]
    _spelling_identities,  # pyright: ignore[reportPrivateUsage]
    census,
    reconcile,
    stale_occurrences,
    structured_occurrences,
)
from devtools.contributor_credit import render_credit
from devtools.result_credit import credit_line, result_credit_html
from sqpack.contributor_occurrences import (
    SCHEMA_PATH,
    CreditOccurrence,
    CreditOrigin,
    OccurrenceError,
    load_occurrences,
)
from sqpack.contributors import load_contributors
from sqpack.project import require_project_root
from sqpack.yamlio import load_yaml

PACKING = require_project_root()
REPO = PACKING.parent


def text_content(markup: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", markup))


def test_live_manifest_and_literal_result_credits() -> None:
    registry = load_occurrences()
    assert registry.occurrences
    profiles = load_contributors()
    for item in registry.occurrences:
        rendered = render_credit(item.origin, item.expected_text, registry=registry)
        assert text_content(rendered) == item.expected_text
        if item.disposition == "resolved":
            assert item.contributor_id in profiles.by_id
    bibliography = load_yaml((PACKING / "resources/bibliography.yaml").read_text())
    sources = {row["key"]: row for row in bibliography["sources"]}
    records = load_yaml((PACKING / "frontier/results.yaml").read_text())["results"]
    for record in records:
        output = result_credit_html(record, sources)
        assert text_content(output) == credit_line(record, sources).replace(r"\|", "|")
    stromquist = render_credit(
        CreditOrigin("packing/resources/bibliography.yaml", "[Stromquist 2003]", "/authors/0"),
        "Stromquist",
    )
    assert 'href="profiles/walter-stromquist.html" data-contributor' in stromquist
    assert ">Stromquist</a>" in stromquist


@pytest.fixture
def manifest(tmp_path: Path) -> tuple[Path, dict[str, Any]]:
    source = PACKING / "contributors/occurrences.yaml"
    (tmp_path / "schemas").mkdir()
    shutil.copyfile(source.parent / SCHEMA_PATH, tmp_path / SCHEMA_PATH)
    document = load_yaml(source.read_text())
    document["occurrences"] = [
        next(row for row in document["occurrences"] if row["disposition"] == "resolved")
    ]
    document["inspections"] = []
    return tmp_path / source.name, document


def test_stale_spans_sources_ids_and_evidence_are_rejected(
    manifest: tuple[Path, dict[str, Any]],
) -> None:
    path, pristine = manifest
    mutations = [
        ("expected_text", "changed source"),
        ("label", "wrong label"),
        ("end", 9999),
        ("start", -1),
        ("end", 0),
        ("contributor_id", "no-such-person"),
        ("evidence", ["no-such-source"]),
    ]
    for field, value in mutations:
        document = copy.deepcopy(pristine)
        document["occurrences"][0][field] = value
        path.write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=True))
        with pytest.raises(OccurrenceError):
            load_occurrences(path, repo=REPO)
    document = copy.deepcopy(pristine)
    document["occurrences"].append(copy.deepcopy(document["occurrences"][0]))
    path.write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=True))
    with pytest.raises(OccurrenceError, match="overlap"):
        load_occurrences(path, repo=REPO)
    for unsafe in ("../LICENSE", "/LICENSE", "packing/../LICENSE"):
        document = copy.deepcopy(pristine)
        document["occurrences"][0]["origin"]["path"] = unsafe
        path.write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=True))
        with pytest.raises(OccurrenceError):
            load_occurrences(path, repo=REPO)


def test_reconcile_replaces_stale_spans_and_joins_only_reviewed_labels(
    manifest: tuple[Path, dict[str, Any]],
) -> None:
    path, _ = manifest
    document = load_yaml((PACKING / "contributors/occurrences.yaml").read_text())
    rows = document["occurrences"]
    stale = next(
        row
        for row in rows
        if row["disposition"] == "resolved"
        and row["origin"]["path"].startswith("packing/frontier/n-")
    )
    stale.update(expected_text="Somebody Else", label="Somebody Else", start=0, end=13)
    levy = next(row for row in rows if row["label"] == "Levy")["origin"]
    open_label = next(
        row
        for row in rows
        if row["label"] == "Chaoweeraprasit" and row["disposition"] == "unresolved"
    )
    removed = (levy, open_label["origin"])
    document["occurrences"] = [row for row in rows if row["origin"] not in removed]
    path.write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=True))

    assert [item["origin"] for item in stale_occurrences(REPO, path)] == [stale["origin"]]
    with pytest.raises(OccurrenceError, match="reviewed source text changed"):
        load_occurrences(path, repo=REPO)
    report = reconcile(REPO, path)
    assert len(report["dropped"]) == 1
    assert stale_occurrences(REPO, path) == []
    registry = load_occurrences(path, repo=REPO)
    by_origin = {
        (origin.path, origin.record_key, origin.field): items
        for origin, items in registry.by_origin.items()
    }
    restored = by_origin[
        (stale["origin"]["path"], stale["origin"]["record_key"], stale["origin"]["field"])
    ]
    assert all(item.label != "Somebody Else" for item in restored)
    levy_items = by_origin[(levy["path"], levy["record_key"], levy["field"])]
    joined = next(item for item in levy_items if item.label == "Levy")
    assert (joined.disposition, joined.contributor_id) == ("resolved", "joshua-levy")
    assert joined.note.startswith("Joined by the reviewed identity")
    origin = open_label["origin"]
    reopened = by_origin[(origin["path"], origin["record_key"], origin["field"])]
    assert [item.disposition for item in reopened if item.label == "Chaoweeraprasit"] == [
        "unresolved"
    ]


def test_a_renamed_credit_joins_by_the_spelling_its_record_sources() -> None:
    spellings = _spelling_identities(load_contributors())
    overbeck = {
        "contributor_id": "marc-leonard-overbeck",
        "evidence": ["citation-cff", "owner-confirmation"],
    }
    assert spellings["Overbeck"] == overbeck
    assert spellings["Kleddamag"]["contributor_id"] == "marc-leonard-overbeck"
    origin = CreditOrigin(
        "packing/frontier/n-017.md", "17", "/reported_lower_bound/proved_by/0"
    )
    span = CreditOccurrence(
        origin, "Overbeck", 0, 8, "Overbeck", "lower-bound-prover", "unresolved", note="pending"
    )
    join, key, _ = _join(span, {}, spellings, set())
    assert (join, key) == (overbeck, "joined_by_spelling")
    assert _join(span, {}, spellings, {"Overbeck"})[:2] == (None, "unresolved")
    reviewed = {"contributor_id": "joshua-levy", "evidence": ["primary-byline"], "count": 2}
    assert _join(span, {"Overbeck": reviewed}, spellings, set())[:2] == (reviewed, "joined")


def test_unknown_and_conflicting_duplicate_credit_remain_plain() -> None:
    registry = load_occurrences()
    origin = CreditOrigin(
        "packing/resources/bibliography.yaml", "[Stromquist 2003]", "/authors/0"
    )
    assert render_credit(replace(origin, record_key="unmapped"), "Stromquist") == "Stromquist"
    with pytest.raises(OccurrenceError, match="source text"):
        render_credit(origin, "changed", registry=registry)
    source = {"authors": ["Stromquist"]}
    sources = {"[Stromquist 2003]": source, "unmapped": source}
    record = {"attribution": {"source_keys": list(sources)}}
    output = result_credit_html(record, sources)
    assert output == "Stromquist"
    resolved = result_credit_html(
        {"attribution": {"source_keys": ["[Stromquist 2003]", "[Stromquist 2003]"]}}, sources
    )
    assert resolved.count("data-contributor") == 1
    assert text_content(resolved) == "Stromquist"


def test_unresolved_disposition_never_uses_candidate_aliases() -> None:
    registry = load_occurrences()
    item = next(item for item in registry.occurrences if item.disposition == "resolved")
    unresolved = replace(item, disposition="unresolved", contributor_id=None, evidence=())
    plain_registry = replace(registry, by_origin={item.origin: (unresolved,)})
    output = render_credit(item.origin, item.expected_text, registry=plain_registry)
    assert "data-contributor" not in output
    assert text_content(output) == item.expected_text


def test_conflicting_reviewed_ids_cannot_choose_a_deduplicated_person(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registry = load_occurrences()
    origin = CreditOrigin(
        "packing/resources/bibliography.yaml", "[Stromquist 2003]", "/authors/0"
    )
    first = registry.by_origin[origin][0]
    other_origin = replace(origin, record_key="synthetic-shared-surname")
    second = replace(first, origin=other_origin, contributor_id="mira")
    conflict = replace(registry, by_origin={origin: (first,), other_origin: (second,)})
    monkeypatch.setattr("devtools.contributor_credit.occurrence_registry", lambda: conflict)
    sources = {
        origin.record_key: {"authors": ["Stromquist"]},
        other_origin.record_key: {"authors": ["Stromquist"]},
    }
    assert (
        result_credit_html({"attribution": {"source_keys": list(sources)}}, sources)
        == "Stromquist"
    )
    assert render_credit(origin, "Stromquist", prefix="../").startswith(
        '<a href="../profiles/walter-stromquist.html"'
    )
    unknown = replace(origin, record_key="unknown")
    assert render_credit(unknown, '<b title="&">credit</b>') == (
        "&lt;b title=&quot;&amp;&quot;&gt;credit&lt;/b&gt;"
    )


def test_census_retains_prerequisite_roles_and_pending_pdf_scope() -> None:
    rows = structured_occurrences(REPO)
    lineage = [
        row
        for row in rows
        if row.origin.record_key == "[Ahmed 11SquaresFormalized 2026]"
        and row.origin.field == "/credit"
    ]
    assert [(row.label, row.role) for row in lineage] == [
        ("Ahmed", "credited-contributor"),
        ("et al.", "collective-abbreviation"),
        ("Levy", "prerequisite"),
        ("Daniel", "prerequisite"),
    ]
    registry = load_occurrences()
    byline_only = replace(
        registry,
        inspections=tuple(
            receipt
            for receipt in registry.inspections
            if receipt.scope != "PDF full credit census"
        ),
    )
    report = census(REPO, byline_only)
    assert sum(report["dispositions"].values()) == len(rows)
    assert report["dispositions"].get("unreviewed", 0) == 0
    assert report["pdfs"]["tracked"] == report["pdfs"]["pending"]
    assert report["pdfs"].get("inspected", 0) == 0
