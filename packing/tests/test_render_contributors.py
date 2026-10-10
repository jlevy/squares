"""Contributor pages preserve evidenced identities and safe prose on every route."""

import re
import shutil
import subprocess
from dataclasses import replace
from pathlib import Path

import pytest
import yaml

from devtools import (
    render_contributors,
    render_overview,
    site_documents,
    site_urls,
    validate_schemas,
)
from devtools.repo_links import RepositoryTree
from sqpack.contributor_occurrences import CreditOccurrence, CreditOrigin
from sqpack.contributors import ContributorError, FieldProvenance, load_contributors
from sqpack.yamlio import load_yaml


def test_profiles_share_one_complete_article_and_directory() -> None:
    registry = load_contributors()
    pages = {page.name: page.html for page in render_contributors.contributor_pages()}
    index = pages["contributors/index.html"]
    assert 'aria-label="Contributors"' in index
    assert 'rel="canonical" href="https://jlevy.github.io/squares/contributors/"' in index
    for contributor in registry.by_id.values():
        assert f'href="{contributor.id}.html"' in index
        profile = pages[contributor.profile_path]
        assert '<article class="site-contributor"' in profile
        assert contributor.display_name in profile
        assert "data-contributor-popover" in profile
        assert "data-case-popover" in profile
        assert re.search(r'src="../assets/js/article-loader\.[a-f0-9]+\.js"', profile)
        assert re.search(r'src="../assets/js/contributor-popover\.[a-f0-9]+\.js"', profile)
    assert "Real name" not in pages["contributors/mira.html"]
    assert "site-contributor-bio" not in pages["contributors/mira.html"]


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
    rows = site_urls.derive_registry(site_urls.load_registry())
    registered = {row.path: row for row in rows}
    assert set(paths) <= set(registered)
    sitemap = site_urls.render_sitemap(rows)
    for path in paths:
        assert render_overview.canonical_url(path) in sitemap
    tree = RepositoryTree(
        files=frozenset({"packing/contributors/mira.md"}), directories=frozenset()
    )
    assert site_documents.record_aliases(tree)["packing/contributors/mira.md"] == (
        "contributors/mira.html"
    )
    directory = tmp_path / "contributors"
    directory.mkdir()
    (directory / "retired.html").write_text("old")
    monkeypatch.setattr(render_overview, "asset_files", lambda _files: {})
    monkeypatch.setattr(render_overview, "support_files", dict)
    monkeypatch.setattr(site_urls, "write_crawl_files", lambda _output: None)
    render_overview.write_site(
        tmp_path, [render_overview.Page("contributors/index.html", "new")]
    )
    assert not (directory / "retired.html").exists()
    assert (directory / "index.html").read_text() == "new"


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
    source = render_contributors.CONTRIBUTORS / "occurrences.yaml"
    _markdown, datasets = validate_schemas.corpus_paths()
    assert source in datasets
    document = load_yaml(source.read_text())
    document["occurrences"][0]["expected_text"] = "stale credit"
    target = tmp_path / source.name
    target.write_text(yaml.dump(document))
    shutil.copyfile(
        source.with_name("occurrences.schema.yaml"), tmp_path / "occurrences.schema.yaml"
    )
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
        ["git", "sparse-checkout", "set", "--no-cone", "/packing/contributors/*.md"],
        cwd=checkout,
        check=True,
        capture_output=True,
    )
    subprocess.run(["git", "checkout", "HEAD"], cwd=checkout, check=True, capture_output=True)
    monkeypatch.setattr(render_contributors, "REPO", checkout)
    monkeypatch.setattr(render_contributors, "CONTRIBUTORS", checkout / "packing/contributors")
    evidence = render_contributors.evidence_paths()
    assert evidence
    assert all(not path.exists() for path in evidence)
    assert render_contributors.main(["--checkout-evidence"]) == 0
    assert all(path.is_file() for path in evidence)
    unrelated = "packing/resources/papers/kearney-shiu-2002-efficient-packing-unit-squares.pdf"
    assert (render_overview.REPO / unrelated).is_file()
    assert not (checkout / unrelated).exists()
