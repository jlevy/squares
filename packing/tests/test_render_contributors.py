"""Contributor pages preserve evidenced identities and safe prose on every route."""

import re
import shutil
import subprocess
from dataclasses import replace
from pathlib import Path

import pytest
import yaml

from devtools import (
    check_published_site,
    render_contributors,
    render_overview,
    site_documents,
    site_urls,
    validate_schemas,
)
from devtools.repo_links import RepositoryTree
from sqpack.contributor_occurrences import SCHEMA_PATH as OCCURRENCES_SCHEMA
from sqpack.contributor_occurrences import CreditOccurrence, CreditOrigin
from sqpack.contributors import (
    PEOPLE_DIR,
    SCHEMA_PATH,
    ContributorError,
    FieldProvenance,
    load_contributors,
    record_names,
)
from sqpack.yamlio import load_yaml


def test_profiles_share_one_complete_article_and_directory() -> None:
    registry = load_contributors()
    pages = {page.name: page.html for page in render_contributors.contributor_pages()}
    assert set(pages) == set(render_contributors.page_paths())
    index = pages["profiles/index.html"]
    assert "<h1>Profiles</h1>" in index
    assert 'aria-label="Profiles"' in index
    assert "<title>Profiles" in index
    assert 'rel="canonical" href="https://jlevy.github.io/squares/profiles/"' in index
    # The directory names cited authors as well as contributors, and calls none of them
    # contributors in its own voice; the colophon links it by the same name.
    assert "Contributors<" not in index
    assert '<a href="index.html">Profiles</a></span>' in index
    for contributor in registry.by_id.values():
        assert contributor.profile_path == f"profiles/{contributor.id}.html"
        assert f'href="{contributor.id}.html"' in index
        profile = pages[contributor.profile_path]
        assert '<article class="site-contributor"' in profile
        assert '<a href="index.html">Profiles</a></nav>' in profile
        assert contributor.display_name in profile
        assert "data-contributor-popover" in profile
        assert 'aria-label="Profile"' in profile
        assert "data-case-popover" in profile
        assert re.search(r'src="../assets/js/article-loader\.[a-f0-9]+\.js"', profile)
        assert re.search(r'src="../assets/js/contributor-popover\.[a-f0-9]+\.js"', profile)
        assert "contributors/" not in profile
    assert "Real name" not in pages["profiles/mira.html"]
    assert "site-contributor-bio" not in pages["profiles/mira.html"]


def test_biography_preserves_inline_markdown_but_refuses_unsafe_links() -> None:
    contributor = load_contributors().by_id["evan-daniel"]
    safe = replace(
        contributor,
        bio='An *exact* construction. <img src="https://example.com/x"> '
        "![image](https://example.com/x) [source](https://example.com/paper).",
    )
    rendered = render_contributors.contributor_article(safe, ())
    assert "<em>exact</em>" in rendered
    assert "<img" not in rendered
    assert "&lt;img src=" in rendered
    assert 'href="https://example.com/paper"' in rendered
    for unsafe in (
        "[bad](javascript:alert%281%29)",
        "[bad](//example.com/paper)",
        "[bad](https://user:pass@example.com/paper)",
        "[bad](file:///tmp/private)",
    ):
        with pytest.raises(ContributorError):
            render_contributors.contributor_article(replace(contributor, bio=unsafe), ())


def test_contributor_routes_aliases_and_stale_output_removal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    paths = render_contributors.page_paths()
    assert paths[0] == "profiles/index.html"
    assert all(path.startswith("profiles/") for path in paths)
    rows = site_urls.derive_registry(site_urls.load_registry())
    registered = {row.path: row for row in rows}
    assert set(paths) <= set(registered)
    sitemap = site_urls.render_sitemap(rows)
    for path in paths:
        assert registered[path].status == "live"
        assert render_overview.canonical_url(path) in sitemap
    tree = RepositoryTree(
        files=frozenset({"packing/contributors/people/mira.md"}), directories=frozenset()
    )
    assert site_documents.record_aliases(tree)["packing/contributors/people/mira.md"] == (
        "profiles/mira.html"
    )
    monkeypatch.setattr(render_overview, "asset_files", lambda _files: {})
    monkeypatch.setattr(render_overview, "support_files", dict)
    monkeypatch.setattr(site_urls, "write_crawl_files", lambda _output: None)
    for name in ("profiles", "contributors"):
        directory = tmp_path / name
        directory.mkdir()
        (directory / "retired.html").write_text("old")
    render_overview.write_site(
        tmp_path,
        [
            render_overview.Page("profiles/index.html", "new"),
            render_overview.Page("contributors/index.html", "forwarder"),
        ],
    )
    for name in ("profiles", "contributors"):
        assert not (tmp_path / name / "retired.html").exists()
    assert (tmp_path / "profiles/index.html").read_text() == "new"
    assert (tmp_path / "contributors/index.html").read_text() == "forwarder"


def test_each_earlier_contributor_address_forwards_to_its_profile() -> None:
    """The profiles moved from `contributors/` to `profiles/` (think-0v2c). The directory
    and each profile the preview served there keep a registered forwarder at the earlier
    address, which previews the profile, and no sitemap entry; the profile pages are where
    links lead now."""
    moved = dict(render_overview.MOVED_PAGES)
    earlier = {
        "contributors/index.html": "profiles/index.html",
        **{
            f"contributors/{old}.html": f"profiles/{new}.html"
            for old, new in render_overview.LEGACY_PROFILES.items()
        },
    }
    assert {old: moved[old] for old in earlier} == earlier
    assert {old for old in moved if old.startswith("contributors/")} == set(earlier)
    rows = {row.path: row for row in site_urls.load_registry()}
    sitemap = site_urls.render_sitemap(list(rows.values()))
    for old, new in earlier.items():
        row = rows[old]
        assert (row.kind, row.status, row.target) == ("forwarder", "forwarded", new), old
        assert row.canonical == site_urls.canonical_path(new)
        assert f"<loc>{render_overview.canonical_url(old)}</loc>" not in sitemap
        assert f"<loc>{render_overview.canonical_url(new)}</loc>" in sitemap
    forwarders = {page.name: page.html for page in render_overview.forwarder_pages()}
    metas = render_contributors.page_metas()
    for old, new in earlier.items():
        page = forwarders[old]
        # A script goes to the profile's address, the directory's as `profiles/`; the
        # no-script refresh and link name the file, as the deployed check requires.
        assert check_published_site.forwarder_says(page) == (
            check_published_site.forwarder_expected(old, new)
        )
        assert f'This page has moved: <a href="../{new}">' in page
        assert f"<title>{metas[new].name}" in page
    assert 'data-moved-to="../profiles/"' in forwarders["contributors/index.html"]


def test_credits_link_cases_and_results_preserving_roles_without_duplicates() -> None:
    contributor = load_contributors().by_id["mira"]
    case = CreditOccurrence(
        origin=CreditOrigin("packing/frontier/n-017.md", "17", "/found_by"),
        expected_text="Mira",
        start=0,
        end=4,
        label="Mira",
        role="construction",
        disposition="resolved",
        contributor_id="mira",
    )
    result = replace(
        case,
        origin=CreditOrigin("packing/frontier/results.yaml", "T-051", "/credit"),
        role="proof",
    )
    rendered = render_contributors.contributor_article(contributor, (case, case, result))
    assert rendered.count('href="cases/17.html" data-case="17"') == 1
    assert 'href="result/t-051.html"' in rendered
    assert "construction — Mira" in rendered
    assert "proof — Mira" in rendered


def test_separate_bibliography_credits_and_identifier_evidence_are_preserved() -> None:
    contributor = load_contributors().by_id["evan-daniel"]
    contributor = replace(
        contributor,
        provenance=(
            *contributor.provenance,
            *(
                FieldProvenance(field, (contributor.sources[0].id,))
                for field in ("/id", "/sources/0/id", "/bio_sources/0", "/provenance/0/field")
            ),
        ),
    )
    first = CreditOccurrence(
        origin=CreditOrigin(
            "packing/resources/bibliography.yaml",
            "[Daniel exact and local reports 2026]",
            "/authors/0",
        ),
        expected_text="Daniel",
        start=0,
        end=6,
        label="Daniel",
        role="author",
        disposition="resolved",
        contributor_id="evan-daniel",
    )
    second = replace(
        first,
        origin=CreditOrigin(
            "packing/resources/bibliography.yaml",
            "[Daniel new arrangements 2026-10-07]",
            "/authors/0",
        ),
    )
    article = render_contributors.contributor_article(contributor, (first, second))
    bibliography = (render_contributors.REPO / first.origin.path).read_text().splitlines()
    for occurrence in (first, second):
        match = re.search(
            rf'href="[^\"]*bibliography.yaml\?plain=1#L(\d+)">{re.escape(occurrence.origin.record_key)}</a>',
            article,
        )
        assert match is not None
        assert occurrence.origin.record_key in bibliography[int(match[1]) - 1]
    assert "Profile identifier:" in article
    assert "Sources:" in article
    assert "Biography sources:" in article
    assert "Field evidence:" in article


def test_occurrence_schema_gate_checks_stale_reviewed_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = render_contributors.MANIFEST
    _markdown, datasets = validate_schemas.corpus_paths()
    assert source in datasets
    document = load_yaml(source.read_text())
    document["occurrences"][0]["expected_text"] = "stale credit"
    target = tmp_path / source.name
    target.write_text(yaml.dump(document))
    (tmp_path / "schemas").mkdir()
    shutil.copyfile(source.parent / OCCURRENCES_SCHEMA, tmp_path / OCCURRENCES_SCHEMA)
    monkeypatch.setattr(validate_schemas, "CONTRIBUTOR_OCCURRENCES", target)
    assert "reviewed source text changed" in validate_schemas.check(target)[0]


def test_sparse_build_restores_only_declared_contributor_evidence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    checkout = tmp_path / "sparse"
    subprocess.run(
        ["git", "clone", "--shared", "--no-checkout", str(render_overview.REPO), str(checkout)],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "sparse-checkout", "set", "--no-cone", "/packing/contributors/people/"],
        cwd=checkout,
        check=True,
        capture_output=True,
    )
    subprocess.run(["git", "checkout", "HEAD"], cwd=checkout, check=True, capture_output=True)
    monkeypatch.setattr(render_contributors, "REPO", checkout)
    monkeypatch.setattr(render_contributors, "CONTRIBUTORS", checkout / "packing" / PEOPLE_DIR)
    monkeypatch.setattr(
        render_contributors, "MANIFEST", checkout / "packing/contributors/occurrences.yaml"
    )
    evidence = render_contributors.evidence_paths()
    assert evidence
    assert all(not path.exists() for path in evidence)
    assert render_contributors.main(["--checkout-evidence"]) == 0
    assert all(path.is_file() for path in evidence)
    unrelated = "packing/resources/papers/kearney-shiu-2002-efficient-packing-unit-squares.pdf"
    assert (render_overview.REPO / unrelated).is_file()
    assert not (checkout / unrelated).exists()


def test_legacy_profile_forwarders_are_the_fixed_preview_set() -> None:
    """Only the addresses the reviewed preview served forward; later profiles have none."""
    records = set(load_contributors().by_id)
    legacy = render_overview.LEGACY_PROFILES
    assert len(legacy) == 20
    assert set(legacy.values()) <= records
    assert legacy["kleddamag"] == "marc-leonard-overbeck"
    assert legacy["wand125"] == "hiroaki-hosono"
    assert legacy["queuingtheorydotcom"] == "manasseh-ahmed"
    moved = dict(render_overview.MOVED_PAGES)
    assert moved["contributors/index.html"] == "profiles/index.html"
    for old, new in legacy.items():
        assert moved[f"contributors/{old}.html"] == f"profiles/{new}.html"
    later = records - set(legacy.values())
    assert "john-bidwell" in later
    assert not any(f"contributors/{identifier}.html" in moved for identifier in later)


def test_profile_heads_need_no_archive_evidence(tmp_path: Path) -> None:
    """A paper's partial build checks the profile forwarders without the archive the
    records cite, so the heads come from the records' names alone and match the pages."""
    records = render_contributors.CONTRIBUTORS
    people, schemas = tmp_path / "people", tmp_path / "schemas"
    people.mkdir()
    schemas.mkdir()
    for path in records.glob("*.md"):
        shutil.copyfile(path, people / path.name)
    shutil.copyfile(records / SCHEMA_PATH, people / SCHEMA_PATH)
    names = record_names(people)
    with pytest.raises(ContributorError, match="archive_path"):
        load_contributors(people, repo=tmp_path)
    profiles = load_contributors().by_id
    assert names == {
        identifier: profile.display_name for identifier, profile in profiles.items()
    }
    metas = render_contributors.page_metas()
    for profile in profiles.values():
        assert metas[profile.profile_path] == render_contributors.profile_meta(profile)
