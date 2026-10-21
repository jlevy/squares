"""Reviewed source spans survive source drift and preserve literal credit output."""

from __future__ import annotations

import copy
import html
import re
import shutil
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any

import pytest
import yaml

from devtools.contributor_census import (
    census,
    reconcile,
    stale_occurrences,
    structured_occurrences,
)
from devtools.contributor_credit import render_credit
from devtools.profile_links import public_names
from devtools.result_credit import credit_line, result_credit_html
from sqpack.contributor_occurrences import (
    CONTRACT,
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


def source_text(markup: str, items: tuple[CreditOccurrence, ...]) -> str:
    """The original reviewed wording and joins stay in the source occurrence record."""
    resolved = iter(item for item in items if item.disposition == "resolved")

    def restore(match: re.Match[str]) -> str:
        item = next(resolved)
        assert match[1] == item.contributor_id
        assert html.unescape(match[2]) == public_names()[match[1]].label
        return html.escape(item.label)

    restored = re.sub(
        r'<a href="profiles/([^"]+).html" data-person>([^<]*)</a>',
        restore,
        markup,
    )
    assert next(resolved, None) is None
    return text_content(restored)


def test_live_manifest_and_literal_result_credits() -> None:
    registry = load_occurrences()
    assert registry.occurrences
    profiles = load_contributors()
    for item in registry.occurrences:
        rendered = render_credit(item.origin, item.expected_text, registry=registry)
        assert source_text(rendered, registry.by_origin[item.origin]) == item.expected_text
        if item.disposition == "resolved":
            assert item.contributor_id in profiles.by_id
    bibliography = load_yaml((PACKING / "resources/bibliography.yaml").read_text())
    sources = {row["key"]: row for row in bibliography["sources"]}
    records = load_yaml((PACKING / "frontier/results.yaml").read_text())["results"]
    for record in records:
        output = result_credit_html(record, sources)
        original = credit_line(record, sources).replace(r"\|", "|")
        assert re.findall(r" after |; |, ", text_content(output)) == re.findall(
            r" after |; |, ", original
        )
    stromquist = render_credit(
        CreditOrigin("packing/resources/bibliography.yaml", "[Stromquist 2003]", "/authors/0"),
        "Stromquist",
    )
    assert 'href="profiles/walter-stromquist.html" data-person' in stromquist
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


@pytest.fixture
def census_repo(tmp_path: Path) -> tuple[Path, Path, dict[str, Any]]:
    repo = tmp_path / "repo"
    packing = repo / "packing"
    profiles = packing / "contributors"
    (profiles / "people").mkdir(parents=True)
    shutil.copytree(PACKING / "contributors/schemas", profiles / "schemas")
    for profile_id, display_name, alias in (
        ("ryan-xu", "Ryan Xu", "Xu"),
        ("evan-daniel", "Evan Daniel", "evand"),
    ):
        source = PACKING / "contributors/people" / f"{profile_id}.md"
        document = load_yaml(source.read_text().split("---", 2)[1])
        document["contributor"] = {
            "id": profile_id,
            "display_name": display_name,
            "aliases": [alias],
            "sources": [
                {"id": "profile", "url": "https://example.com/author", "locator": "Byline"}
            ],
            "provenance": [
                {"field": "/display_name", "sources": ["profile"]},
                {"field": "/aliases", "sources": ["profile"]},
            ],
        }
        footer = source.read_text().split("<!-- This document follows", 1)[1]
        (profiles / "people" / source.name).write_text(
            "---\n"
            + yaml.safe_dump(document, sort_keys=False)
            + "---\n<!-- This document follows"
            + footer
        )
    (packing / "resources").mkdir()
    authors = ["Xu", "Xu", "Evan Daniel(evand)", "Xu", "evand", "Unknown Author"]
    (packing / "resources/bibliography.yaml").write_text(
        yaml.safe_dump({"sources": [{"key": "test-source", "authors": authors}]})
    )
    (packing / "frontier").mkdir()
    (packing / "frontier/results.yaml").write_text("results: []\n")
    rows = []
    for index, profile_id in ((0, "ryan-xu"), (2, "evan-daniel")):
        item = CreditOccurrence(
            CreditOrigin(
                "packing/resources/bibliography.yaml", "test-source", f"/authors/{index}"
            ),
            authors[index],
            0,
            len(authors[index]),
            authors[index],
            "source-author",
            "resolved",
            contributor_id=profile_id,
            evidence=("profile",),
            note="Reviewed this source.",
        )
        rows.append(asdict(item))
    document = {
        "softschema": {"contract": CONTRACT, "schema": SCHEMA_PATH, "status": "enforced"},
        "occurrences": rows,
        "inspections": [],
    }
    path = profiles / "occurrences.yaml"
    path.write_text(yaml.safe_dump(document, sort_keys=False))
    return repo, path, document


def test_reconcile_requires_review_for_each_new_source_occurrence(
    census_repo: tuple[Path, Path, dict[str, Any]],
) -> None:
    repo, path, document = census_repo
    report = reconcile(repo, path)
    registry = load_occurrences(path, repo=repo)
    assert [asdict(item) for item in registry.occurrences[:1]] == document["occurrences"][:1]
    for index, label, candidate_ids in (
        (1, "Xu", ["ryan-xu"]),
        (4, "evand", ["evan-daniel"]),
        (5, "Unknown Author", []),
    ):
        origin = CreditOrigin(
            "packing/resources/bibliography.yaml", "test-source", f"/authors/{index}"
        )
        (item,) = registry.by_origin[origin]
        assert (item.disposition, item.contributor_id, item.evidence) == (
            "unresolved",
            None,
            (),
        )
        assert text_content(render_credit(origin, label, registry=registry)) == label
        assert "data-person" not in render_credit(origin, label, registry=registry)
        proposal = next(row for row in report["unresolved"] if row["origin"] == asdict(origin))
        assert proposal["candidate_ids"] == candidate_ids


def test_changed_declined_span_stays_unresolved_and_unchanged_refusal_survives(
    census_repo: tuple[Path, Path, dict[str, Any]],
) -> None:
    repo, path, document = census_repo
    declined = {
        **copy.deepcopy(document["occurrences"][0]),
        "expected_text": "Xu and somebody else",
        "disposition": "unresolved",
        "evidence": [],
        "note": "Identity review declined; a surname does not establish this author.",
    }
    declined.pop("contributor_id")
    declined["origin"]["field"] = "/authors/3"
    unchanged = copy.deepcopy(declined)
    unchanged["origin"]["field"] = "/authors/5"
    unchanged.update(expected_text="Unknown Author", label="Unknown Author", end=14)
    document["occurrences"].extend([declined, unchanged])
    path.write_text(yaml.safe_dump(document, sort_keys=False))
    assert len(stale_occurrences(repo, path)) == 1
    report = reconcile(repo, path)
    assert report["dropped"] == [declined]
    assert stale_occurrences(repo, path) == []
    registry = load_occurrences(path, repo=repo)
    (changed,) = registry.by_origin[CreditOrigin(**declined["origin"])]
    assert (changed.label, changed.disposition, changed.contributor_id) == (
        "Xu",
        "unresolved",
        None,
    )
    (retained,) = registry.by_origin[CreditOrigin(**unchanged["origin"])]
    assert asdict(retained) == {**unchanged, "contributor_id": None, "evidence": ()}


def test_reconcile_preserves_reviewed_manual_field_coverage(
    census_repo: tuple[Path, Path, dict[str, Any]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo, path, document = census_repo
    manual = document["occurrences"][1]
    manual.update(end=11, label="Evan Daniel")
    path.write_text(yaml.safe_dump(document, sort_keys=False))
    original = load_occurrences(path, repo=repo).by_origin[CreditOrigin(**manual["origin"])]
    reconcile(repo, path)
    registry = load_occurrences(path, repo=repo)
    assert registry.by_origin[CreditOrigin(**manual["origin"])] == original
    monkeypatch.setattr("devtools.contributor_census.tracked_pdfs", lambda _repo: ())
    report = census(repo, registry)
    assert report["dispositions"].get("unreviewed", 0) == 0
    assert all(row["label"] != "Evan Daniel(evand)" for row in report["pending_occurrences"])


def test_reconcile_validates_complete_output_before_replacing_manifest(
    census_repo: tuple[Path, Path, dict[str, Any]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo, path, _ = census_repo
    before = path.read_bytes()
    malformed = replace(structured_occurrences(repo)[1], label="wrong label")
    monkeypatch.setattr(
        "devtools.contributor_census.structured_occurrences", lambda _repo: (malformed,)
    )
    with pytest.raises(OccurrenceError, match="label span"):
        reconcile(repo, path)
    assert path.read_bytes() == before
    load_occurrences(path, repo=repo)


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
    assert resolved.count("data-person") == 1
    assert text_content(resolved) == "Stromquist"


def test_unresolved_disposition_never_uses_candidate_aliases() -> None:
    registry = load_occurrences()
    item = next(item for item in registry.occurrences if item.disposition == "resolved")
    unresolved = replace(item, disposition="unresolved", contributor_id=None, evidence=())
    plain_registry = replace(registry, by_origin={item.origin: (unresolved,)})
    output = render_credit(item.origin, item.expected_text, registry=plain_registry)
    assert "data-person" not in output
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
