"""Reviewed source spans survive source drift and preserve literal credit output."""

from __future__ import annotations

import copy
import html
import json
import re
import shutil
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any

import pytest
import yaml

from devtools import contributor_census, validate_schemas
from devtools.contributor_census import (
    BOUNDARY_REVIEW,
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
    ROLES,
    SCHEMA_PATH,
    CreditOccurrence,
    CreditOrigin,
    MissingSourceError,
    OccurrenceError,
    load_occurrences,
    source_text,
)
from sqpack.contributors import load_contributors
from sqpack.project import require_project_root
from sqpack.yamlio import load_yaml

PACKING = require_project_root()
REPO = PACKING.parent


def text_content(markup: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", markup))


def reviewed_source_text(markup: str, items: tuple[CreditOccurrence, ...]) -> str:
    """The original reviewed wording and joins stay in the source occurrence record."""
    resolved = iter(item for item in items if item.disposition == "resolved")

    def restore(match: re.Match[str]) -> str:
        item = next(resolved)
        assert match[1] == item.contributor_id
        assert html.unescape(match[2]) == public_names()[match[1]].label
        return html.escape(item.label)

    restored = re.sub(
        r'<a href="profiles/([^"]+)\.html">([^<]*)</a>',
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
        assert (
            reviewed_source_text(rendered, registry.by_origin[item.origin])
            == item.expected_text
        )
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
    assert '<a href="profiles/walter-stromquist.html">Stromquist</a>' in stromquist


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
        assert "profiles/" not in render_credit(origin, label, registry=registry)
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
    assert resolved.count('href="profiles/walter-stromquist.html"') == 1
    assert text_content(resolved) == "Stromquist"


def test_unresolved_disposition_never_uses_candidate_aliases() -> None:
    registry = load_occurrences()
    item = next(item for item in registry.occurrences if item.disposition == "resolved")
    unresolved = replace(item, disposition="unresolved", contributor_id=None, evidence=())
    plain_registry = replace(registry, by_origin={item.origin: (unresolved,)})
    output = render_credit(item.origin, item.expected_text, registry=plain_registry)
    assert "profiles/" not in output
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


def write_yaml(path: Path, document: Any) -> None:
    path.write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=True), "utf-8")


def set_bibliography(repo: Path, authors: list[str], credit: str | None = None) -> None:
    source: dict[str, Any] = {"key": "test-source", "authors": authors}
    if credit is not None:
        source["credit"] = credit
    write_yaml(repo / "packing/resources/bibliography.yaml", {"sources": [source]})


@pytest.fixture
def manual_origin(
    census_repo: tuple[Path, Path, dict[str, Any]],
) -> tuple[Path, Path, dict[str, Any]]:
    """A reviewed join on a generator constant, which no extractor produces."""
    repo, path, document = census_repo
    (repo / "packing/devtools").mkdir()
    (repo / "packing/devtools/result_credit.py").write_text('PROJECT_AUTHOR = "Xu"\n')
    row = {
        **copy.deepcopy(document["occurrences"][0]),
        "origin": {
            "path": "packing/devtools/result_credit.py",
            "record_key": "constants",
            "field": "/PROJECT_AUTHOR",
        },
        "role": "project-author",
    }
    document["occurrences"].append(row)
    write_yaml(path, document)
    load_occurrences(path, repo=repo)
    return repo, path, load_yaml(path.read_text())["occurrences"][-1]


def test_census_counts_manual_origins_the_extractor_does_not_produce(
    manual_origin: tuple[Path, Path, dict[str, Any]], monkeypatch: pytest.MonkeyPatch
) -> None:
    repo, path, row = manual_origin
    monkeypatch.setattr("devtools.contributor_census.tracked_pdfs", lambda _repo: ())
    report = census(repo, load_occurrences(path, repo=repo))
    assert report["manual_origin_count"] == 1
    assert report["manual_occurrences"] == [
        {
            "origin": row["origin"],
            "label": "Xu",
            "role": "project-author",
            "disposition": "resolved",
            "contributor_id": "ryan-xu",
        }
    ]
    assert report["structured_occurrence_count"] == len(structured_occurrences(repo))


def test_reconcile_refuses_a_changed_manual_origin_and_drops_only_a_removed_one(
    manual_origin: tuple[Path, Path, dict[str, Any]],
) -> None:
    repo, path, row = manual_origin
    origin = CreditOrigin(**row["origin"])
    constant = repo / "packing/devtools/result_credit.py"
    before = path.read_bytes()
    for text, expected in (
        ('PROJECT_AUTHOR = "Ryan Xu"\n', "manual origin changed; review by hand"),
        ('<<<<<<< HEAD\nPROJECT_AUTHOR = "Xu"\n=======\n', "manual origin unreadable"),
    ):
        constant.write_text(text)
        assert [item["origin"] for item in stale_occurrences(repo, path)] == [row["origin"]]
        with pytest.raises(OccurrenceError, match=expected):
            reconcile(repo, path)
        assert path.read_bytes() == before
    constant.write_text('OTHER_CONSTANT = "Xu"\n')
    report = reconcile(repo, path)
    assert report["removed_fields"] == [row["origin"]]
    assert report["dropped"] == [row]
    assert report["dropped_resolved_count"] == 1
    assert origin not in load_occurrences(path, repo=repo).by_origin


def test_reconcile_reports_dropped_resolved_joins_as_prior_and_exits_3(
    census_repo: tuple[Path, Path, dict[str, Any]],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo, path, _ = census_repo
    reviewed = load_yaml(path.read_text())["occurrences"]
    # An inserted author shifts every reviewed field by one index.
    set_bibliography(repo, ["New Person", "Xu", "Xu", "Evan Daniel(evand)", "Xu", "evand"])
    monkeypatch.setattr(
        "devtools.contributor_census.require_project_root", lambda: repo / "packing"
    )
    assert contributor_census.main(["--reconcile"]) == contributor_census.EXIT_DROPPED_RESOLVED
    output = capsys.readouterr()
    assert "2 resolved joins dropped" in output.err
    report = json.loads(output.out)
    assert report["dropped_resolved_count"] == 2
    proposals = {row["origin"]["field"]: row for row in report["unresolved"]}
    assert proposals["/authors/0"]["prior"] == []
    (shifted,) = proposals["/authors/1"]["prior"]
    assert shifted["contributor_id"] == "ryan-xu"
    assert proposals["/authors/2"]["prior"] == [shifted]
    (moved,) = proposals["/authors/3"]["prior"]
    assert moved == reviewed[1]
    assert (moved["contributor_id"], moved["evidence"]) == ("evan-daniel", ["profile"])
    registry = load_occurrences(path, repo=repo)
    assert all(item.disposition == "unresolved" for item in registry.occurrences)
    assert contributor_census.main(["--reconcile"]) == 0


def test_draft_refuses_the_live_manifest_under_any_name(
    census_repo: tuple[Path, Path, dict[str, Any]],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo, path, _ = census_repo
    before = path.read_bytes()
    alias = repo / "alias.yaml"
    alias.symlink_to(path)
    monkeypatch.setattr("devtools.contributor_census.tracked_pdfs", lambda _repo: ())
    monkeypatch.setattr(
        "devtools.contributor_census.require_project_root", lambda: repo / "packing"
    )
    for target in (path, alias, path.parent / ".." / "contributors" / path.name):
        with pytest.raises(OccurrenceError, match="live manifest"):
            contributor_census.draft(repo, target)
        assert contributor_census.main(["--draft", str(target)]) == 1
        assert "live manifest" in capsys.readouterr().err
        assert path.read_bytes() == before
    proposal = path.with_name("draft.yaml")
    assert contributor_census.main(["--draft", str(proposal)]) == 0
    assert len(load_occurrences(proposal, repo=repo).occurrences) == 6
    assert path.read_bytes() == before


def test_clause_and_organization_labels_are_flagged_without_changing_spans(
    census_repo: tuple[Path, Path, dict[str, Any]], monkeypatch: pytest.MonkeyPatch
) -> None:
    flagged = contributor_census.needs_boundary_or_non_person_review
    for label in ("register seed data from Levy", "PingYou Ltd", "Example Inc", "A GmbH"):
        assert flagged(label)
    assert flagged("UnitSquare Project")
    assert flagged("Square LLC")
    for label in (
        "Evan Daniel",
        "de Winter",
        "van der Waerden",
        "Nate Chaoweeraprasit (itsnaka)",
        "squarepacker (Ryu Sungjoon)",
        "chelokot",
    ):
        assert not flagged(label)
    repo, path, _ = census_repo
    authors = ["Xu", "Xu", "Evan Daniel(evand)", "Xu", "evand", "PingYou Ltd"]
    set_bibliography(repo, authors, "Daniel after Couzo; register seed data from Levy")
    labels = [(row.label, row.role) for row in structured_occurrences(repo)][len(authors) :]
    assert labels == [
        ("Daniel", "credited-contributor"),
        ("Couzo", "prerequisite"),
        ("register seed data from Levy", "credited-contributor"),
    ]
    report = reconcile(repo, path)
    marks = {row["label"]: row[BOUNDARY_REVIEW] for row in report["unresolved"]}
    assert marks == {
        "Xu": False,
        "evand": False,
        "PingYou Ltd": True,
        "Daniel": False,
        "Couzo": False,
        "register seed data from Levy": True,
    }
    monkeypatch.setattr("devtools.contributor_census.tracked_pdfs", lambda _repo: ())
    summary = census(repo, load_occurrences(path, repo=repo))
    assert summary[f"{BOUNDARY_REVIEW}_count"] == 2
    assert [row["label"] for row in summary["pending_occurrences"] if row[BOUNDARY_REVIEW]] == [
        "PingYou Ltd",
        "register seed data from Levy",
    ]
    proposal = path.with_name("draft.yaml")
    assert contributor_census.draft(repo, proposal)[BOUNDARY_REVIEW] == 2
    drafted = load_occurrences(proposal, repo=repo).occurrences
    notes = {item.label: item.note for item in drafted}
    assert "boundary or non-person review" in notes["PingYou Ltd"]
    assert "boundary or non-person review" not in notes["Couzo"]


def test_summary_refuses_a_stale_manifest_without_a_traceback(
    census_repo: tuple[Path, Path, dict[str, Any]],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo, _, _ = census_repo
    set_bibliography(repo, ["Ryan Xu", "Xu", "Evan Daniel(evand)", "Xu", "evand"])
    monkeypatch.setattr("devtools.contributor_census.tracked_pdfs", lambda _repo: ())
    monkeypatch.setattr(
        "devtools.contributor_census.require_project_root", lambda: repo / "packing"
    )
    for arguments in ([], ["--json"]):
        assert contributor_census.main(arguments) == 1
        output = capsys.readouterr()
        assert output.out == ""
        assert "reviewed source text changed" in output.err
        assert "--stale" in output.err
        assert "--reconcile" in output.err
    assert contributor_census.main(["--stale"]) == 1


def test_malformed_sources_are_listed_as_stale_and_reported_by_validation(
    census_repo: tuple[Path, Path, dict[str, Any]], monkeypatch: pytest.MonkeyPatch
) -> None:
    repo, path, document = census_repo
    bibliography = repo / "packing/resources/bibliography.yaml"
    pristine = bibliography.read_text()
    bibliography.write_text(f"<<<<<<< HEAD\n{pristine}=======\n{pristine}>>>>>>> main\n")
    stale = stale_occurrences(repo, path)
    assert len(stale) == len(document["occurrences"])
    assert all(row["live_text"] is None for row in stale)
    assert all("does not parse (ScannerError)" in row["live_error"] for row in stale)
    with pytest.raises(OccurrenceError, match="does not parse"):
        load_occurrences(path, repo=repo)
    monkeypatch.setattr(validate_schemas, "REPO", repo)
    monkeypatch.setattr(validate_schemas, "CONTRIBUTOR_OCCURRENCES", path)
    (problem,) = validate_schemas.check(path)
    assert "does not parse" in problem
    assert str(bibliography) in problem
    origin = CreditOrigin(**document["occurrences"][0]["origin"])
    for text, expected in (
        ("softschema: plain\nsources: []\n", "softschema must be a mapping"),
        ("softschema: {envelope: missing}\nsources: []\n", "envelope must name a mapping"),
        ("- not\n- a mapping\n", "structured mapping"),
    ):
        bibliography.write_text(text)
        with pytest.raises(OccurrenceError, match=expected):
            source_text(origin, repo=repo)
    bibliography.write_text(pristine)
    gone = replace(origin, record_key="no-such-source")
    with pytest.raises(MissingSourceError, match="does not exist"):
        source_text(gone, repo=repo)
    with pytest.raises(MissingSourceError, match="does not exist"):
        source_text(replace(origin, path="packing/missing.yaml"), repo=repo)


def test_roles_are_one_published_vocabulary_enforced_by_schema_and_loader(
    manifest: tuple[Path, dict[str, Any]],
) -> None:
    schema = load_yaml((PACKING / "contributors" / SCHEMA_PATH).read_text("utf-8"))
    role = schema["properties"]["occurrences"]["items"]["properties"]["role"]
    assert set(role["enum"]) == ROLES
    assert {item.role for item in load_occurrences().occurrences} == ROLES
    assert {item.role for item in structured_occurrences(REPO)} <= ROLES
    path, document = manifest
    document["occurrences"][0]["role"] = "mastermind"
    write_yaml(path, document)
    with pytest.raises(OccurrenceError, match="mastermind"):
        load_occurrences(path, repo=REPO)
    # A schema copy without the enum still meets the loader's own check.
    role.pop("enum")
    role["type"] = "string"
    write_yaml(path.parent / SCHEMA_PATH, schema)
    with pytest.raises(OccurrenceError, match="unknown credit role 'mastermind'"):
        load_occurrences(path, repo=REPO)
