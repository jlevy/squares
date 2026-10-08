"""The site links the repository on `main`, through one helper, at paths `main` has."""

from __future__ import annotations

import pytest

from devtools import (
    repo_links,
    result_overview,
    site_documents,
)
from devtools.repo_links import (
    DEFAULT_BRANCH,
    RAW_URL,
    REPO,
    REPO_URL,
    RepositoryTree,
    branch_paths,
    hash_pinned_links,
    path_kind,
    repo_url,
    repository_tree,
)
from tests import site_renders

SHA = "0123456789abcdef0123456789abcdef01234567"


def test_a_file_a_directory_and_an_image_link_main() -> None:
    assert repo_url(repo_links.STATUS) == f"{REPO_URL}/blob/main/packing/frontier/STATUS.md"
    assert repo_url(REPO / "packing" / "frontier") == f"{REPO_URL}/tree/main/packing/frontier"
    assert repo_url("docs/a b.md", "?plain=1#L3", kind="blob") == (
        f"{REPO_URL}/blob/main/docs/a%20b.md?plain=1#L3"
    )
    assert (
        repo_url("packing/atlas/n5.svg", kind="raw") == f"{RAW_URL}/main/packing/atlas/n5.svg"
    )
    with pytest.raises(SystemExit, match="outside the repository"):
        repo_url(REPO.parent / "elsewhere.md")


def test_a_path_the_checkout_lacks_is_asked_of_the_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The Pages jobs check the repository out without the directories under
    `packing/resources` and `packing/campaign`. What a path is, a file, a directory or
    nothing, is the same there as in a full checkout, because the commit answers where
    the disk does not; a directory is still linked under `tree/`, never `blob/`."""
    packet = "packing/resources/web/n11-optimality-2026-09-29"
    asked = (
        (packet, "tree"),
        (f"{packet}/README.md", "blob"),
        (REPO / packet / "source" / "PROOF.md", "blob"),
        ("packing/campaign/series", "tree"),
        ("packing/resources/bibliography.yaml", "blob"),
        ("packing/frontier", "tree"),
        (f"{packet}/no-such-file.md", None),
        ("packing/frontier/n-999.md", None),
        (REPO.parent / "elsewhere.md", None),
    )
    full = [path_kind(path) for path, _ in asked]
    assert full == [kind for _, kind in asked]
    site_renders.leave_out_the_archive_and_the_campaign(monkeypatch)
    # The stand-in hides what a partial checkout lacks and nothing else.
    assert not (REPO / packet).exists()
    assert not (REPO / packet / "README.md").is_file()
    assert (REPO / "packing/resources/bibliography.yaml").is_file()
    assert (REPO / "packing/frontier").is_dir()
    assert [path_kind(path) for path, _ in asked] == full
    assert repo_url(REPO / packet) == f"{REPO_URL}/tree/main/{packet}"


def test_the_named_documents_exist_and_are_the_pages_the_site_serves() -> None:
    """Each document the site links by name is defined once. The reader documents are
    served as pages; the three generated views are not, and each is either shown by a
    page built from the same record or linked on `main`."""
    documents = {
        repo_links.README,
        repo_links.TUTORIAL,
        repo_links.SYNOPSIS,
        repo_links.CONVENTIONS,
        repo_links.DEVELOPMENT,
        repo_links.EPISTEMICS,
    }
    views = {repo_links.DEFECTS, repo_links.RESULTS, repo_links.STATUS}
    for path in documents | views:
        assert (REPO / path).is_file(), path
    served = {doc.source.relative_to(REPO).as_posix() for doc in site_documents.DOCUMENTS}
    assert served == documents
    assert set(site_documents.RECORD_PAGES) == {repo_links.RESULTS, repo_links.STATUS}
    assert views - set(site_documents.RECORD_PAGES) == {repo_links.DEFECTS}


def test_a_commit_hash_is_refused_and_a_release_is_not() -> None:
    text = (
        f'<a href="{REPO_URL}/blob/{SHA}/README.md">a</a>'
        f'<a href="{REPO_URL}/tree/{SHA[:8]}/packing">b</a>'
        f'<img src="{RAW_URL}/{SHA}/packing/atlas/n5.svg">'
        f'<a href="{REPO_URL}/blob/main/README.md">c</a>'
        f'<a href="{REPO_URL}/releases/download/v1.0/{SHA}.zip">d</a>'
    )
    assert hash_pinned_links(text) == sorted(
        {
            f"{REPO_URL}/blob/{SHA}/README.md",
            f"{REPO_URL}/tree/{SHA[:8]}/packing",
            f"{RAW_URL}/{SHA}/packing/atlas/n5.svg",
        }
    )
    assert branch_paths(text) == {("blob", "README.md")}


def test_missing_names_each_absent_path() -> None:
    tree = RepositoryTree(files=frozenset({"README.md"}), directories=frozenset({"", "docs"}))
    links = {("blob", "README.md"), ("tree", "docs"), ("tree", "README.md"), ("raw", "x.svg")}
    assert tree.missing(links) == ["raw/x.svg", "tree/README.md"]


@pytest.mark.parametrize(
    "suffix",
    [
        "/issues/401",
        "/issues/401#issuecomment-6031977107",
        "/discussions/12",
        "/discussions/12#discussioncomment-345",
    ],
)
def test_numbered_first_party_reports_are_source_citations(suffix: str) -> None:
    assert repo_links.is_report_link(REPO_URL + suffix)


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/other/squares/issues/401",
        "https://github.com/jlevy/other/issues/401",
        "https://github.com.evil.test/jlevy/squares/issues/401",
        f"{REPO_URL}/issues/0",
        f"{REPO_URL}/issues/not-a-number",
        f"{REPO_URL}/issues/401#discussioncomment-345",
        f"{REPO_URL}/discussions/12#issuecomment-345",
        f"{REPO_URL}/issues/401/blob/main/README.md",
        f"{REPO_URL}/issues/401?redirect=/blob/{SHA}/README.md",
        f"{REPO_URL}/blob/{SHA}/README.md",
        f"{REPO_URL}/blob/review/README.md",
        f"{REPO_URL}/blob/main/README.md",
    ],
)
def test_report_citation_recognition_does_not_admit_other_locations(url: str) -> None:
    assert not repo_links.is_report_link(url)


@pytest.fixture(scope="module")
def pages() -> dict[str, str]:
    return site_renders.pages()


@pytest.fixture(scope="module")
def audit() -> result_overview.LinkAudit:
    """The link audit over the result overviews the test process shares."""
    return result_overview.link_audit(site_renders.overview(), site_renders.result_bodies())


def test_no_page_links_a_commit_hash(pages: dict[str, str]) -> None:
    """Every page the site renders links the repository on `main`, never at a commit."""
    pinned = {name: hash_pinned_links(text) for name, text in pages.items()}
    assert not {name: links for name, links in pinned.items() if links}


def test_every_path_a_page_links_on_main_is_in_head(pages: dict[str, str]) -> None:
    """`HEAD` is the tree `main` holds when the site deploys, so a path it lacks 404s."""
    tree = repository_tree()
    total = 0
    for name, text in pages.items():
        links = branch_paths(text)
        total += len(links)
        assert not tree.missing(links), (name, tree.missing(links))
    assert total > 100, f"only {total} links on {DEFAULT_BRANCH}"


def test_every_result_overview_links_main_at_paths_in_head(
    audit: result_overview.LinkAudit,
) -> None:
    """A result's overview is rendered for its row's popover, apart from any page, so it
    is audited on its own: every repository link in every overview names `main`, and
    every path it opens is in `HEAD`."""
    overview = site_renders.overview()
    assert audit.results >= 60
    assert not audit.off_main
    assert not audit.missing
    assert audit.github > 1000, f"only {audit.github} links on {DEFAULT_BRANCH}"
    assert audit.github_paths > 100
    assert audit.site > 500
    assert set(audit.sizes) == {result.id for result in overview.results}
