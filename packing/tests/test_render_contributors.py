"""Contributor pages preserve evidenced identities and safe prose on every route."""

import re
import shutil
import subprocess
from dataclasses import replace
from html.parser import HTMLParser
from pathlib import Path

import pytest
import yaml

from devtools import (
    check_published_site,
    paper_structure,
    record_presentation,
    render_changelog,
    render_contributors,
    render_overview,
    site_documents,
    site_urls,
    validate_schemas,
)
from devtools.profile_records import RecordIndex
from devtools.repo_links import RepositoryTree, repo_url
from devtools.result_credit import PROJECT_AUTHOR_ORIGIN
from devtools.site_resources import Resource
from devtools.site_tallies import TALLY_SEPARATOR
from sqpack.contributor_occurrences import SCHEMA_PATH as OCCURRENCES_SCHEMA
from sqpack.contributor_occurrences import CreditOccurrence, CreditOrigin, load_occurrences
from sqpack.contributors import (
    PEOPLE_DIR,
    SCHEMA_PATH,
    ContributorError,
    ContributorLink,
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
    assert "<h1>Contributor Profiles</h1>" in index
    assert 'class="kpress-table site-table site-profile-table"' in index
    assert re.findall(r"<th\b[^>]*>([^<]+)</th>", index) == [
        "Name",
        "Accounts",
        "Records",
        "Results",
        "Credits",
        "Years active",
        "Resources",
    ]
    assert index.count('data-sort="num"') == 4
    assert index.count('data-sort="text"') == 3
    assert 'data-sort="text" aria-sort="ascending">Name</th>' in index
    assert re.search(r'src="../assets/js/table\.[a-f0-9]+\.js"', index)
    assert render_overview.TABLE_SCRIPT in render_contributors.inputs()
    assert '<div class="site-table-wrap site-wide">' in index
    # The owner's three-paragraph introduction (2026-10-23) comes before the summary
    # line, in order, as written.
    intro = [
        (
            "<p>Below are people whose work is cited or credited in the square-packing "
            "record.</p>"
        ),
        (
            "<p>This list includes people with notable historic results on square packing "
            "and all known current work, including everyone who has built on results in "
            "the Squares Project.</p>"
        ),
        (
            "<p>All original sources and all known repositories or publications of each "
            "person are listed on their profile page.</p>"
        ),
    ]
    positions = [index.index(paragraph) for paragraph in intro]
    assert positions == sorted(positions)
    assert positions[-1] < index.index('<p class="site-profile-summary">')
    assert "People whose work is cited" not in index
    assert "Results lists authored work" not in index
    assert "<title>Contributor Profiles" in index
    assert 'rel="canonical" href="https://squaremath.org/profiles/"' in index
    # The directory names cited authors as well as contributors, and calls none of them
    # contributors in its own voice.
    assert "Contributors<" not in index
    assert "data-person" not in index
    directory_tree = paper_structure.parse(index)
    breadcrumb = directory_tree.find("nav", "site-breadcrumbs")
    assert breadcrumb is not None
    assert not breadcrumb.find_all("a")
    assert [
        (span.text(), span.attrs.get("aria-current")) for span in breadcrumb.find_all("span")
    ] == [
        ("About", None),
        ("Contributor Profiles", "page"),
    ]
    for cell in directory_tree.find_all("td"):
        if cell.classes.intersection(
            {"site-profile-records", "site-profile-stats", "site-profile-credits"}
        ):
            assert all(number.text().isdigit() for number in cell.find_all("strong"))
            if cell.attrs.get("data-value", "0") != "0":
                assert cell.find("strong") is not None
    assert 'site-profile-table" data-contributor-plain' in index
    for contributor in registry.by_id.values():
        assert contributor.profile_path == f"profiles/{contributor.id}.html"
        assert f'href="{contributor.id}.html"' in index
        profile = pages[contributor.profile_path]
        assert '<article class="site-contributor"' in profile
        trail = paper_structure.parse(profile).find("nav", "site-breadcrumbs")
        assert trail is not None
        assert [(a.text(), a.attrs["href"]) for a in trail.find_all("a")] == [
            ("Contributor Profiles", "./"),
        ]
        assert any(
            span.text() == "About" and "aria-current" not in span.attrs
            for span in trail.find_all("span")
        )
        assert contributor.display_name in profile
        assert "data-contributor-popover" not in profile
        assert 'aria-label="Profile"' not in profile
        assert "data-case-popover" in profile
        assert re.search(r'src="../assets/js/article-loader\.[a-f0-9]+\.js"', profile)
        assert not re.search(r'src="../assets/js/contributor-popover\.[a-f0-9]+\.js"', profile)
        assert not re.search(r'href="(?:\.\./|/)?contributors/[^"]*"', profile)
        sources = profile.split(
            '<details class="site-contributor-sources"><summary>Sources</summary>', 1
        )[1].split("</details>", 1)[0]
        assert "<details" not in sources
        assert "<h2>Sources</h2>" not in profile
        assert "Identity evidence" in sources
        for source in contributor.sources:
            assert f'id="source-{source.id}"' in sources
        if contributor.bio:
            assert "Biography sources:" in sources
            assert (
                "Biography sources:"
                not in profile.split('<details class="site-contributor-sources">', 1)[0]
            )
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
        origin=CreditOrigin("packing/frontier/results.yaml", "T-051", "/builds_on/credit/0"),
        role="proof",
    )
    rendered = render_contributors.contributor_article(contributor, (case, case, result))
    assert rendered.count('href="cases/17.html" data-case="17"') == 1
    assert 'href="result/t-051.html"' in rendered
    assert "construction — Mira" in rendered
    assert "proof — Mira" in rendered
    directory = render_contributors.profile_table(
        [replace(contributor, real_name="Full Public Name")], (case, case, result)
    )
    assert ">Full Public Name</a>" in directory
    assert 'class="site-credit-tally"' in directory
    assert '><strong>1</strong> credit</a> <span class="site-tally-levels">(at S' in directory
    assert "<details open>" not in rendered
    long_credits = tuple(
        replace(
            result,
            origin=replace(result.origin, record_key=f"T-{number:03d}"),
        )
        for number in range(1, 14)
    )
    expanded = render_contributors.contributor_article(contributor, long_credits)
    assert "<details open><summary>Credits: 13</summary>" in expanded


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
    # With no result naming either source, each keeps its own bibliography line.
    article = render_contributors.contributor_article(contributor, (first, second), results=())
    bibliography = (render_contributors.REPO / first.origin.path).read_text().splitlines()
    for occurrence in (first, second):
        match = re.search(
            rf'href="[^\"]*bibliography.yaml\?plain=1#L(\d+)">{re.escape(occurrence.origin.record_key)}</a>',
            article,
        )
        assert match is not None
        assert occurrence.origin.record_key in bibliography[int(match[1]) - 1]
    # Each evidence item names the value it supports, under its field's own name.
    source = contributor.sources[0].id
    evidence = article[
        article.index('<p class="site-contributor-evidence">Identity evidence</p>') :
    ]
    assert f'Profile identifier: evan-daniel (<a href="#source-{source}">' in evidence
    assert f"Source: {source} (" in evidence
    assert f"Biography source: {contributor.bio_sources[0]} (" in evidence
    assert f"Field evidence: {contributor.provenance[0].field} (" in evidence


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


def test_profile_presents_selected_names_accounts_and_existing_news(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        render_contributors,
        "_related_news",
        lambda: {
            "manasseh-ahmed": [
                ("changelog-entry-proof", "Existing proof announcement", "2026-10-12")
            ]
        },
    )
    registry = load_contributors()
    ahmed = registry.by_id["manasseh-ahmed"]
    article = render_contributors.contributor_article(ahmed, ())
    identity = article.split('<dl class="site-contributor-identity">', 1)[1].split("</dl>", 1)[
        0
    ]
    assert "<dt>Handles</dt>" in identity
    assert "MathCompSciFTW, Square Packing Fan" in identity
    assert "Queuingtheorydotcom" not in identity
    filtered = render_contributors.contributor_article(
        replace(
            ahmed,
            display_aliases=(
                *ahmed.display_aliases,
                "Queuingtheorydotcom",
                "@ManassehA06",
                "Ahmed",
                "Manasseh Ahmed",
                "Manasseh-Ahmed",
            ),
        ),
        (),
    )
    filtered_identity = filtered.split('<dl class="site-contributor-identity">', 1)[1].split(
        "</dl>", 1
    )[0]
    assert filtered_identity == identity
    nate = render_contributors.contributor_article(registry.by_id["nate-chaoweeraprasit"], ())
    assert "<dt>Handles</dt><dd>natcha</dd>" in nate
    directory = render_contributors.profile_table(
        [ahmed, registry.by_id["nate-chaoweeraprasit"]], ()
    )
    assert "Manasseh Ahmed</a>" in directory
    assert "Nate Chaoweeraprasit</a>" in directory
    ryu = render_contributors.contributor_article(
        replace(
            registry.by_id["ryu-sungjoon"],
            links=(
                ContributorLink("github", "https://github.com/squarepacker", "squarepacker"),
            ),
        ),
        (),
    )
    assert "<dt>Handles</dt>" not in ryu
    assert 'aria-label="GitHub: Queuingtheorydotcom"' in article
    assert 'aria-label="Twitter / X: @ManassehA06"' in article
    assert article.count('class="site-account-icon"') == 2
    assert 'href="news.html#changelog-entry-proof"' in article
    assert '<time datetime="2026-10-12">2026-10-12</time>' in article
    for identifier in ("oscar-fitzharding", "david-r-maciver"):
        person = registry.by_id[identifier]
        rendered = render_contributors.contributor_article(person, ())
        assert "site-contributor-identity" not in rendered
        if identifier == "oscar-fitzharding":
            assert "site-contributor-bio" not in rendered
    own = (
        render_contributors.contributor_article(
            replace(ahmed, bio="Manasseh Ahmed and Joshua Levy"), ()
        )
        .split('<p class="site-contributor-bio">', 1)[1]
        .split("</p>", 1)[0]
    )
    assert own.startswith("Manasseh Ahmed and <a")
    assert 'href="profiles/joshua-levy.html">Levy</a>' in own


def test_accounts_share_destinations_and_icons_in_profiles_and_compact_rows() -> None:
    person = replace(
        load_contributors().by_id["evan-daniel"],
        links=(
            ContributorLink("github", "https://github.com/evand", "evand"),
            ContributorLink("twitter", "https://x.com/evand", "evand"),
            ContributorLink("personal", "https://example.org/?a=1&b=2"),
            ContributorLink("publication", "https://example.org/papers"),
        ),
    )
    full = render_contributors.account_links(person)
    compact = render_contributors.account_links(person, compact=True)
    assert full.count('class="site-account-icon"') == 2
    assert compact.count('class="site-account-icon"') == 2
    assert "<span>evand</span>" in full
    assert "<span>@evand</span>" in full
    assert "<span>evand</span>" in compact
    assert "<span>@evand</span>" in compact
    assert "example.org" not in compact
    for link in person.links[:2]:
        target = link.url.replace("&", "&amp;")
        assert f'href="{target}"' in full
        assert f'href="{target}"' in compact
    assert 'aria-label="GitHub: evand (Evan Daniel)"' in compact
    assert 'title="Twitter / X: @evand (Evan Daniel)"' in compact
    assert 'aria-label="Personal website:' not in compact
    assert 'aria-label="Publication website:' not in compact
    assert "data-person" not in compact
    assert render_contributors.account_links(replace(person, links=()), compact=True) == ""


def test_related_news_uses_only_eligible_explicit_person_links() -> None:
    summary = "[Alice](packing/contributors/people/alice.md) and Bob Person."
    entry = {
        "id": "proof",
        "title": "A proof",
        "date": "2026-10-12",
        "summary": summary,
        "details": summary,
        "significance": {"score": 4, "rationale": "New proof."},
    }
    entries = [
        entry,
        {**entry, "id": "low", "significance": {"score": 2, "rationale": "Minor change."}},
        {**entry, "id": "excluded", "news_exclusion": {}},
    ]
    related = render_contributors.news_by_profile(
        render_changelog.news_entries({"entries": entries})
    )
    assert related == {"alice": [("changelog-entry-proof", "A proof", "2026-10-12")]}


def test_profile_invitation_requires_no_identity_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def no_records(*_args: object) -> None:
        raise AssertionError("Home/About invitation should not read person records")

    monkeypatch.setattr(render_contributors, "record_metadata", no_records)
    invitation = render_contributors.profile_preview()
    assert "All Profiles" in invitation
    assert "site-contributor-list" not in invitation


def _credit(
    key: str, field: str, label: str, role: str, contributor: str = "hiroaki-hosono"
) -> CreditOccurrence:
    return CreditOccurrence(
        origin=CreditOrigin("packing/resources/bibliography.yaml", key, field),
        expected_text=label,
        start=0,
        end=len(label),
        label=label,
        role=role,
        disposition="resolved",
        contributor_id=contributor,
    )


#: A register of three results: two attributed to sources, one of this project's own.
REGISTER = (
    {
        "id": "T-201",
        "significance": {"score": 4},
        "kind": "upper-bound",
        "scope": {"n_values": [61]},
        "attribution": {"source_keys": ["[A]", "[B]"]},
    },
    {
        "id": "T-030",
        "significance": {"score": 3},
        "kind": "lower-bound",
        "scope": {"n_min": 10, "n_max": 20},
        "attribution": {"source_keys": ["[A]"]},
    },
    {
        "id": "T-002",
        "significance": {"score": 5},
        "kind": "lower-bound",
        "scope": {"n_values": [17]},
        "builds_on": {"credit": ["Bentz"]},
    },
)


def test_a_source_credit_lists_under_each_result_naming_it_with_its_roles(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Profiles link back to the results whose credit their spans are printed in: one
    line a result, in register order, each role once with the spelling it credits, and
    the sources as secondary text. A source no result names keeps its bibliography line,
    and no role appears that a span does not give."""
    monkeypatch.setattr(
        render_contributors,
        "_reference_documents",
        lambda: (
            {"sources": []},
            {"repository": "https://github.com/jlevy/squares", "entries": []},
        ),
    )
    contributor = load_contributors().by_id["hiroaki-hosono"]
    author = _credit("[A]", "/authors/0", "Hiroaki Hosono", "source-author")
    credit = _credit("[A]", "/credit", "Hosono", "credited-contributor")
    again = _credit("[B]", "/credit", "Hosono", "credited-contributor")
    unnamed = _credit("[Kingbird]", "/credit", "Hosono", "prerequisite")
    other = _credit("[A]", "/credit", "Bentz", "source-author", contributor="wolfram-bentz")
    article = render_contributors.contributor_article(
        contributor, (author, credit, credit, again, unnamed, other), results=REGISTER
    )
    assert any(
        section.attrs.get("id") == "results"
        for section in paper_structure.parse(article).find_all("section")
    )
    assert '<section id="other-reviewed-records">' in article
    section = "".join(
        render_contributors.credited_work(
            contributor.id, (author, credit, credit, again, unnamed, other), results=REGISTER
        ).parts
    )
    primary_and_credits = re.sub(
        r'<section id="records">.*?</section>', "", section, flags=re.DOTALL
    )
    lines = re.findall(r"<li>.*?</li>", primary_and_credits)
    assert lines == [
        (
            '<li><a href="result/t-030.html">T-030</a> (lower bound, 11 cases, n = 10 to 20): '
            "source author — Hiroaki Hosono; credited contributor — Hosono, in [A]</li>"
        ),
        (
            '<li><a href="result/t-201.html">T-201</a> (upper bound, n = 61): '
            "source author — Hiroaki Hosono; credited contributor — Hosono, in [A]; [B]</li>"
        ),
        lines[2],
    ]
    bibliography = (render_contributors.REPO / render_contributors.BIBLIOGRAPHY).read_text()
    line = bibliography.splitlines().index("  - key: '[Kingbird]'") + 1
    assert lines[2] == (
        f'<li><a href="{repo_url(render_contributors.BIBLIOGRAPHY, f"?plain=1#L{line}")}">'
        "[Kingbird]</a>: prerequisite — Hosono</li>"
    )
    assert "Bentz" not in section
    projected = render_contributors.credited_work(
        contributor.id, (author, credit, credit, again, unnamed, other), results=REGISTER
    )
    assert projected.count == len(lines) == 3
    assert "<details>" not in section
    # A role two spans give with one spelling reads once, beside that spelling.
    same = render_contributors.contributor_article(
        contributor,
        (replace(author, label="Hosono", expected_text="Hosono", end=6), credit),
        results=REGISTER,
    )
    assert (
        "(upper bound, n = 61): source author, credited contributor — Hosono, in [A]</li>"
    ) in same


def test_the_project_author_reads_as_one_line_for_the_first_party_results(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The project author's credit comes from one generator constant; the profile says
    whose results it credits rather than linking the constant's source file."""
    monkeypatch.setattr(
        render_contributors,
        "_reference_documents",
        lambda: (
            {"sources": []},
            {"repository": "https://github.com/jlevy/squares", "entries": []},
        ),
    )
    contributor = load_contributors().by_id["joshua-levy"]
    authored = CreditOccurrence(
        origin=PROJECT_AUTHOR_ORIGIN,
        expected_text="Levy",
        start=0,
        end=4,
        label="Levy",
        role="project-author",
        disposition="resolved",
        contributor_id="joshua-levy",
    )
    article = render_contributors.contributor_article(
        contributor, (authored,), results=REGISTER
    )
    assert (
        '<ul class="site-contributor-credits"><li><a href="results.html">'
        "The register\u2019s 1 first-party result</a>: project author — Levy</li></ul>"
    ) in article
    assert "result_credit.py" not in article
    assert "constants" not in article


def test_published_profiles_link_the_results_they_credit() -> None:
    """On the register itself: the people the review found unlinked now reach their
    results, and every result a profile links is one the register has."""
    registry = load_contributors()
    occurrences = load_occurrences().occurrences
    register = {
        str(record["id"]).lower()
        for record in load_yaml(render_contributors.RESULTS.read_text())["results"]
    }
    for identifier in ("joshua-levy", "hiroaki-hosono", "evan-daniel"):
        article = render_contributors.contributor_article(
            registry.by_id[identifier], occurrences
        )
        core_work = re.sub(r'<section id="records">.*?</section>', "", article, flags=re.DOTALL)
        linked = re.findall(r'href="result/(t-\d+)\.html"', core_work)
        record_section = re.search(r'<section id="records">.*?</section>', article, re.DOTALL)
        if record_section:
            assert (
                set(re.findall(r'href="result/(t-\d+)\.html"', record_section[0])) <= register
            )
        assert len(linked) >= 50, identifier
        assert len(linked) == len(set(linked)), identifier
        assert set(linked) <= register
        assert "result_credit.py" not in article
    levy = render_contributors.contributor_article(registry.by_id["joshua-levy"], occurrences)
    assert '<a href="results.html">The register\u2019s ' in levy


def test_identity_evidence_names_each_claimed_value() -> None:
    """One evidence item a JSON pointer, each naming what it supports; aliases include X
    display names and former handles, so they read as names the person is known by."""
    contributor = load_contributors().by_id["hiroaki-hosono"]
    article = render_contributors.contributor_article(contributor, ())
    assert "Credit spellings" not in article
    assert "Also credited as" not in article
    assert "site-contributor-identity" not in article
    assert '<details class="site-contributor-sources"><summary>Sources</summary>' in article
    evidence = article[
        article.index('<p class="site-contributor-evidence">Identity evidence</p>') :
    ]
    for alias in contributor.aliases:
        assert evidence.count(f"<li>Also known as: {alias} (") == 1
    for link in contributor.links:
        assert evidence.count(f"<li>Public website: {link.url} (") == 1
    assert "<li>Public name: Hiroaki Hosono (" in evidence
    unknown = replace(
        contributor,
        provenance=(FieldProvenance("/<b>_note", (contributor.sources[0].id,)),),
    )
    rendered = render_contributors.contributor_article(unknown, ())
    assert "<li>/&lt;b&gt; note: <a" in rendered
    assert "<b>" not in rendered


def test_directory_summary_unions_work_and_years_exclude_import_dates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        render_contributors, "record_index", lambda: RecordIndex(("T-201",), {}, {})
    )
    registry = load_contributors()
    people = [registry.by_id["manasseh-ahmed"], registry.by_id["nate-chaoweeraprasit"]]
    first = _credit("[A]", "/authors/0", "Ahmed", "source-author", people[0].id)
    second = _credit("[A]", "/authors/1", "Chaoweeraprasit", "source-author", people[1].id)
    case = replace(first, origin=CreditOrigin("packing/frontier/n-017.md", "17", "/found_by/0"))
    records = (
        {
            "id": "T-201",
            "significance": {"score": 5},
            "registered": "2026-10-21",
            "attribution": {"source_keys": ["[A]"]},
        },
    )
    resource = Resource(
        "https://example.org/shared",
        "Shared work",
        "A result.",
        "Manasseh Ahmed and Nate Chaoweeraprasit",
        tuple(person.id for person in people),
        "website",
    )
    summary = render_contributors.profile_summary(
        people, (first, first, second, case), results=records, resources=(resource, resource)
    )
    assert re.sub(r"<[^>]+>", "", summary) == (
        "2 people · 1 record · 1 result · 0 credits · 1 resource"
    )
    # Each dot is the shared separator, which the tally spacing tokens style.
    assert summary.count(TALLY_SEPARATOR) == 4
    assert render_contributors.profile_years(people[0].id, (first,), records) is None


def test_credit_thread_references_stay_with_the_result_they_document(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        render_contributors,
        "_reference_documents",
        lambda: (
            {
                "sources": [
                    {
                        "source_key": "[A]",
                        "url": "https://github.com/example/work/issues/7#issuecomment-1",
                    }
                ]
            },
            {
                "repository": "https://github.com/jlevy/squares",
                "entries": [{"result_ids": ["T-030"], "pull_requests": [8], "references": []}],
            },
        ),
    )
    contributor = load_contributors().by_id["hiroaki-hosono"]
    article = render_contributors.contributor_article(
        contributor,
        (_credit("[A]", "/credit", "Hosono", "credited-contributor"),),
        results=REGISTER,
    )
    section = article.split('<section id="credited-work">', 1)[1].split("</section>", 1)[0]

    class CreditItems(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.items: list[tuple[list[str], list[str], list[str]]] = []
            self.current: tuple[list[str], list[str], list[str]] | None = None

        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            attributes = dict(attrs)
            if tag == "li":
                self.current = ([], [], [])
                self.items.append(self.current)
            if self.current is not None:
                if tag == "a" and (href := attributes.get("href")):
                    self.current[1].append(href)
                self.current[2].extend((attributes.get("class") or "").split())

        def handle_data(self, data: str) -> None:
            if self.current is not None:
                self.current[0].append(data)

        def handle_endtag(self, tag: str) -> None:
            if tag == "li":
                self.current = None

    parser = CreditItems()
    parser.feed(section)
    first = next(item for item in parser.items if "result/t-030.html" in item[1])
    second = next(item for item in parser.items if "result/t-201.html" in item[1])
    first_words, second_words = "".join(first[0]), "".join(second[0])
    assert "Source:" in first_words
    assert "Registered in:" in first_words
    assert "#8" in first_words
    assert "Source:" in second_words
    assert "Registered in:" not in second_words
    assert "#8" not in second_words
    evidence = "https://github.com/example/work/issues/7#issuecomment-1"
    registration = "https://github.com/jlevy/squares/pull/8"
    assert evidence in first[1]
    assert evidence in second[1]
    assert registration in first[1]
    assert registration not in second[1]
    assert "site-contributor-references" in first[2]


def test_directory_unknown_years_and_zero_work_cells_are_blank() -> None:
    person = load_contributors().by_id["manasseh-ahmed"]
    table = render_contributors.profile_table((person,), (), results=())
    assert '<td class="site-profile-years" data-value=""></td>' in table
    assert '<td class="site-profile-stats" data-value="0"></td>' in table
    assert '<td class="site-profile-credits" data-value="0"></td>' in table
    assert '<td class="site-profile-records" data-value="0"></td>' in table
    assert "0 results" not in table
    assert "0 credits" not in table


def test_profile_tally_and_sections_order_records_results_then_credits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    identifier = "wolfram-bentz"
    author = _credit("[A]", "/authors/0", "Bentz", "source-author", identifier)
    credited = replace(
        _credit("T-002", "/builds_on/credit/0", "Bentz", "credited-contributor", identifier),
        origin=CreditOrigin("packing/frontier/results.yaml", "T-002", "/builds_on/credit/0"),
    )
    occurrences = (author, credited)
    index = RecordIndex(("T-201",), {}, {"T-030": ("comparison pending",)})
    monkeypatch.setattr(render_contributors, "record_index", lambda: index)
    monkeypatch.setattr(record_presentation, "record_index", lambda: index)
    target = "profiles/wolfram-bentz.html"
    tally = render_contributors.profile_tally(
        identifier, occurrences, target=target, results=REGISTER
    )
    assert re.sub(r"<[^>]+>", "", tally) == (
        "1 record (at S4) · Review pending · 2 results (1 at S4, 1 at S3) · 1 credit (at S5)"
    )
    assert tally.count(TALLY_SEPARATOR) == 3
    assert re.findall(r'<a href="([^"]+)">', tally) == [
        target + "#records",
        target + "#records",
        target + "#results",
        target + "#credited-work",
    ]
    work = render_contributors.credited_work(identifier, occurrences, results=REGISTER)
    rendered = "".join(work.parts)
    assert re.findall(r'<section id="([^"]+)"><h2[^>]*>', rendered) == [
        "records",
        "results",
        "credited-work",
    ]
    assert work.count == 3
    record_section = rendered.split('<section id="records">', 1)[1].split("</section>", 1)[0]
    assert 'href="result/t-201.html"' in record_section
    assert 'href="result/t-030.html">T-030</a>: comparison pending' in record_section
    index = RecordIndex(
        (), {}, {"T-201": ("priority unknown",), "T-030": ("comparison pending",)}
    )
    pending = render_contributors.profile_tally(identifier, occurrences, results=REGISTER)
    assert re.sub(r"<[^>]+>", "", pending) == (
        "Review pending · 2 results (1 at S4, 1 at S3) · 1 credit (at S5)"
    )


def test_profile_tally_preserves_known_zero_counts_in_display_order() -> None:
    # Each dot is the shared separator, as in every other tally.
    assert render_contributors.profile_tally("wolfram-bentz", (), results=()) == (
        '<span class="site-credit-tally">'
        f"0 records{TALLY_SEPARATOR}0 results{TALLY_SEPARATOR}0 credits</span>"
    )


def test_profile_directory_intro_is_serif_and_accounts_remain_whole_at_narrow_widths(
    tmp_path: Path,
) -> None:
    from devtools import preview_site, site_assets  # noqa: PLC0415
    from sqpack.probes import probe  # noqa: PLC0415
    from tests import site_browser  # noqa: PLC0415

    directory = next(
        page
        for page in render_contributors.contributor_pages()
        if page.name == "profiles/index.html"
    )
    target = tmp_path / directory.name
    target.parent.mkdir(parents=True)
    target.write_text(directory.html)
    site_assets.write_assets(tmp_path, render_overview.asset_files([directory]))
    measure = probe(Path(__file__).with_name("probes"), "site_contributor/directory")
    server = preview_site.serve(tmp_path, 0)
    try:
        with site_browser.api().sync_playwright() as driver:
            browser = site_browser.launch(driver)
            page = browser.new_page()
            page.goto(f"http://127.0.0.1:{server.server_port}/profiles/", wait_until="load")
            for width in (1280, 390, 320):
                page.set_viewport_size({"width": width, "height": 900})
                found = page.evaluate(measure)
                assert found["intro"] == (
                    "Below are people whose work is cited or credited in the "
                    "square-packing record."
                )
                assert "PT Serif" in found["introFont"]
                assert "Source Sans" in found["tableFont"]
                assert found["names"]
                assert all(name["weight"] == "680" for name in found["names"])
                assert all(name["weight"] == "410" for name in found["otherLinks"])
                assert found["overflow"] == 0
                assert found["accounts"]
                for account in found["accounts"]:
                    assert account["width"] >= 16 * 16
                    for label in account["links"]:
                        assert label["nowrap"] == "nowrap"
                        assert label["lines"] <= 1
                        assert label["inside"]
                if width < 768:
                    assert found["tableWidth"] > found["wrapperWidth"]
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
