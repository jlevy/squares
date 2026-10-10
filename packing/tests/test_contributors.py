"""Contributor identity, evidence and paragraph boundaries survive record mutations."""

from __future__ import annotations

import copy
import shutil
from pathlib import Path
from typing import Any

import pytest
import yaml

from devtools import validate_schemas
from sqpack.contributors import (
    FOOTER,
    SCHEMA_NAME,
    ContributorError,
    load_contributor,
    load_contributors,
)
from sqpack.project import require_project_root
from sqpack.yamlio import load_yaml

PACKING = require_project_root()
REPO = PACKING.parent
RECORDS = PACKING / "contributors"


@pytest.fixture
def record(tmp_path: Path) -> tuple[Path, dict[str, Any]]:
    shutil.copyfile(RECORDS / SCHEMA_NAME, tmp_path / SCHEMA_NAME)
    document = load_yaml((RECORDS / "mira.md").read_text().split("---\n")[1])
    return tmp_path / "mira.md", document


def write_record(path: Path, document: dict[str, Any], body: str = "") -> None:
    text = yaml.dump(document, sort_keys=False, allow_unicode=True)
    path.write_text(f"---\n{text}---\n{body}\n\n{FOOTER}\n", encoding="utf-8")


def test_seed_records_keep_identity_and_optional_information_separate() -> None:
    registry = load_contributors(RECORDS, repo=REPO)
    assert list(registry.by_id) == ["evan-daniel", "mira", "walter-stromquist"]
    mira = registry.by_id["mira"]
    assert mira.display_name == "Mira"
    assert mira.real_name is None
    assert mira.bio is None
    assert mira.bio_sources == ()
    assert mira.profile_path == "contributors/mira.html"
    walter = registry.by_id["walter-stromquist"]
    assert walter.links == ()
    assert walter.bio is not None
    assert FOOTER not in walter.bio
    assert registry.candidates("STROMQUIST") == (walter,)
    assert registry.candidates("evand") == (registry.by_id["evan-daniel"],)
    assert registry.candidates("Mira-acc") == (mira,)
    assert registry.candidates("unknown person") == ()
    assert registry.candidates(" Mira") == ()


def test_shared_alias_is_ambiguous_without_losing_stable_ids(
    record: tuple[Path, dict[str, Any]],
) -> None:
    path, first = record
    write_record(path, first)
    second = copy.deepcopy(first)
    second["contributor"]["id"] = "another-person"
    second["contributor"]["display_name"] = "Another Person"
    second["contributor"].pop("links")
    second["contributor"]["provenance"].pop()
    write_record(path.with_name("another-person.md"), second)
    registry = load_contributors(path.parent, repo=REPO)
    assert registry.candidates("Mira-acc") == (
        registry.by_id["another-person"],
        registry.by_id["mira"],
    )
    assert registry.candidates("Mira") == (registry.by_id["mira"],)
    assert registry.candidates("Another Person") == (registry.by_id["another-person"],)


def test_duplicate_id_is_refused_by_the_filename_invariant(
    record: tuple[Path, dict[str, Any]],
) -> None:
    path, document = record
    write_record(path, document)
    write_record(path.with_name("duplicate.md"), document)
    with pytest.raises(ContributorError, match="filename stem"):
        load_contributors(path.parent, repo=REPO)


@pytest.mark.parametrize("field", ["contract", "schema", "envelope", "status"])
def test_contract_metadata_cannot_be_redirected(
    record: tuple[Path, dict[str, Any]], field: str
) -> None:
    path, document = record
    document["softschema"][field] = "wrong"
    write_record(path, document)
    with pytest.raises(ContributorError, match="contract"):
        load_contributor(path, repo=REPO)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", "Mira"),
        ("id", "mira/person"),
        ("id", "mira--person"),
        ("display_name", " "),
        ("real_name", None),
        ("real_name", ""),
        ("aliases", []),
        ("aliases", ["Mira-acc", "Mira-acc"]),
        ("links", []),
        ("bio_sources", []),
        ("extra_field", "unexpected"),
    ],
)
def test_malformed_payload_is_rejected(
    record: tuple[Path, dict[str, Any]], field: str, value: Any
) -> None:
    path, document = record
    document["contributor"][field] = value
    write_record(path, document)
    with pytest.raises(ContributorError):
        load_contributor(path, repo=REPO)


@pytest.mark.parametrize("field", ["display_name", "sources", "provenance"])
def test_required_identity_or_evidence_cannot_be_omitted(
    record: tuple[Path, dict[str, Any]], field: str
) -> None:
    path, document = record
    document["contributor"].pop(field)
    write_record(path, document)
    with pytest.raises(ContributorError):
        load_contributor(path, repo=REPO)


def test_duplicate_yaml_key_cannot_overwrite_identity(
    record: tuple[Path, dict[str, Any]],
) -> None:
    path, document = record
    write_record(path, document)
    path.write_text(path.read_text().replace("  id: mira\n", "  id: mira\n  id: replacement\n"))
    with pytest.raises(ContributorError, match="duplicate key"):
        load_contributor(path, repo=REPO)


@pytest.mark.parametrize(
    ("pointer", "sources", "expected"),
    [
        ("/missing", ["repository-citation"], "does not exist"),
        ("/aliases/01", ["repository-citation"], "does not exist"),
        ("/display_name~2", ["repository-citation"], "JSON Pointer"),
        ("/display_name", ["unknown"], "unknown provenance sources"),
    ],
)
def test_provenance_must_resolve_to_fields_and_declared_sources(
    record: tuple[Path, dict[str, Any]], pointer: str, sources: list[str], expected: str
) -> None:
    path, document = record
    document["contributor"]["provenance"][0] = {"field": pointer, "sources": sources}
    write_record(path, document)
    with pytest.raises(ContributorError, match=expected):
        load_contributor(path, repo=REPO)


@pytest.mark.parametrize("index", [0, 1, 2])
def test_each_identity_claim_requires_provenance(
    record: tuple[Path, dict[str, Any]], index: int
) -> None:
    path, document = record
    document["contributor"]["provenance"].pop(index)
    write_record(path, document)
    with pytest.raises(ContributorError, match="requires provenance"):
        load_contributor(path, repo=REPO)


def test_claimed_real_name_requires_evidence(record: tuple[Path, dict[str, Any]]) -> None:
    path, document = record
    document["contributor"]["real_name"] = "An Unsupported Name"
    write_record(path, document)
    with pytest.raises(ContributorError, match="/real_name"):
        load_contributor(path, repo=REPO)


def test_repeated_source_ids_and_provenance_fields_are_rejected(
    record: tuple[Path, dict[str, Any]],
) -> None:
    path, document = record
    document["contributor"]["sources"].append(document["contributor"]["sources"][0])
    write_record(path, document)
    with pytest.raises(ContributorError, match="source ids must be unique"):
        load_contributor(path, repo=REPO)
    document["contributor"]["sources"].pop()
    document["contributor"]["provenance"].append(document["contributor"]["provenance"][0])
    write_record(path, document)
    with pytest.raises(ContributorError, match="duplicate provenance field"):
        load_contributor(path, repo=REPO)


@pytest.mark.parametrize(
    "archive",
    ["../README.md", "/etc/hosts", "packing/../README.md", "packing\\README.md", "missing.md"],
)
def test_archive_reference_is_an_existing_repository_file(
    record: tuple[Path, dict[str, Any]], archive: str
) -> None:
    path, document = record
    document["contributor"]["sources"][0]["archive_path"] = archive
    write_record(path, document)
    with pytest.raises(ContributorError, match="archive_path"):
        load_contributor(path, repo=REPO)


def test_archive_symlink_cannot_escape_repository(record: tuple[Path, dict[str, Any]]) -> None:
    path, document = record
    repository = path.parent / "repo"
    repository.mkdir()
    (repository / "escape.md").symlink_to(path.parent / SCHEMA_NAME)
    document["contributor"]["sources"][0]["archive_path"] = "escape.md"
    write_record(path, document)
    with pytest.raises(ContributorError, match="archive_path"):
        load_contributor(path, repo=repository)


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "//github.com/Mira-acc",
        "https://github.com@evil.example/Mira-acc",
        "https://github.com\\evil.example/Mira-acc",
        "https:///Mira-acc",
        "https://github..com/Mira-acc",
        "https://-github.com/Mira-acc",
        "https://github.com:0/Mira-acc",
        "https://github.com:bad/Mira-acc",
    ],
)
def test_unsafe_links_and_source_urls_are_rejected(
    record: tuple[Path, dict[str, Any]], url: str
) -> None:
    path, document = record
    document["contributor"]["links"][0]["url"] = url
    write_record(path, document)
    with pytest.raises(ContributorError):
        load_contributor(path, repo=REPO)
    document["contributor"].pop("links")
    document["contributor"]["provenance"].pop()
    document["contributor"]["sources"][0]["url"] = url
    write_record(path, document)
    with pytest.raises(ContributorError):
        load_contributor(path, repo=REPO)


@pytest.mark.parametrize(
    ("kind", "url", "handle"),
    [
        ("github", "https://github.com/Mira-acc", "someone-else"),
        ("github", "https://github.com/Mira-acc/repo", "Mira-acc"),
        ("github", "https://github.com//Mira-acc", "Mira-acc"),
        ("github", "https://github.com:443/Mira-acc", "Mira-acc"),
        ("github", "https://example.com/Mira-acc", "Mira-acc"),
        ("github", "https://github.com/Mira-acc?other=person", "Mira-acc"),
        ("twitter", "https://x.com/user/status/1", "user"),
        ("substack", "https://name.substack.com/p/post", "name"),
        ("personal", "https://example.com/", "name"),
    ],
)
def test_platform_accounts_are_consistent_with_their_handles(
    record: tuple[Path, dict[str, Any]], kind: str, url: str, handle: str
) -> None:
    path, document = record
    document["contributor"]["links"][0] = {"kind": kind, "url": url, "handle": handle}
    write_record(path, document)
    with pytest.raises(ContributorError):
        load_contributor(path, repo=REPO)


@pytest.mark.parametrize(
    ("kind", "url", "handle"),
    [
        ("github", "https://github.com/Mira-acc/", "mira-acc"),
        ("twitter", "https://twitter.com/example_1", "example_1"),
        ("twitter", "https://x.com/example_1", "example_1"),
        ("substack", "https://example.substack.com/", "example"),
        ("substack", "https://substack.com/@example", "example"),
        ("personal", "https://example.com/", None),
        ("publication", "https://example.com/journal", None),
    ],
)
def test_supported_link_kinds_allow_optional_handles(
    record: tuple[Path, dict[str, Any]], kind: str, url: str, handle: str | None
) -> None:
    path, document = record
    link = {"kind": kind, "url": url}
    if handle is not None:
        link["handle"] = handle
    document["contributor"]["links"][0] = link
    write_record(path, document)
    contributor = load_contributor(path, repo=REPO)
    assert contributor.links[0].handle == handle


@pytest.mark.parametrize(
    "body",
    [
        "One paragraph.\n\nAnother paragraph.",
        "# Heading",
        "> Quoted biography.",
        "- A list item.",
        "```\ncode\n```",
        "    indented code",
        "Title\n=====",
        "first | second\n--- | ---\none | two",
        "<!-- An unrelated comment -->",
    ],
)
def test_bio_is_one_paragraph_without_blocks(
    record: tuple[Path, dict[str, Any]], body: str
) -> None:
    path, document = record
    document["contributor"]["bio_sources"] = ["repository-citation"]
    write_record(path, document, body)
    with pytest.raises(ContributorError, match="one Markdown paragraph"):
        load_contributor(path, repo=REPO)


def test_bio_preserves_inline_markdown_and_abbreviations(
    record: tuple[Path, dict[str, Any]],
) -> None:
    path, document = record
    document["contributor"]["bio_sources"] = ["repository-citation"]
    body = "Dr. Example wrote **a paper** (e.g. on packing).\nIt has a [source](https://example.com/)."
    write_record(path, document, body)
    assert load_contributor(path, repo=REPO).bio == body


@pytest.mark.parametrize(
    ("body", "sources", "expected"),
    [
        ("Biography.", None, "exactly when"),
        ("", ["repository-citation"], "exactly when"),
        ("Biography.", ["unknown"], "unknown bio sources"),
    ],
)
def test_bio_requires_its_own_declared_evidence(
    record: tuple[Path, dict[str, Any]], body: str, sources: list[str] | None, expected: str
) -> None:
    path, document = record
    if sources is not None:
        document["contributor"]["bio_sources"] = sources
    write_record(path, document, body)
    with pytest.raises(ContributorError, match=expected):
        load_contributor(path, repo=REPO)


@pytest.mark.parametrize(
    "footer", ["", FOOTER.replace("guidelines", "rules"), f"{FOOTER}\n{FOOTER}"]
)
def test_only_the_exact_guideline_footer_is_removed(
    record: tuple[Path, dict[str, Any]], footer: str
) -> None:
    path, document = record
    write_record(path, document)
    path.write_text(path.read_text().replace(FOOTER, footer))
    with pytest.raises(ContributorError, match="unchanged guideline footer"):
        load_contributor(path, repo=REPO)


def test_schema_gate_includes_contributors_and_runs_semantics(
    record: tuple[Path, dict[str, Any]], monkeypatch: pytest.MonkeyPatch
) -> None:
    corpus, _ = validate_schemas.corpus_paths()
    assert set(RECORDS.glob("*.md")) <= set(corpus)
    path, document = record
    write_record(path, document)
    monkeypatch.setattr(validate_schemas, "CONTRIBUTORS", path.parent)
    assert validate_schemas.check(path) == []
    document["contributor"]["provenance"][0]["sources"] = ["unknown"]
    write_record(path, document)
    assert "unknown provenance sources" in validate_schemas.check(path)[0]
