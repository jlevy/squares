"""The live-site check's parsing, on fixtures: the network half is not a unit of the gate."""

from __future__ import annotations

import pytest

from devtools import check_published_site
from devtools.check_published_site import (
    SERVED,
    WORKBENCH_HOME,
    WORKBENCH_REVISION,
    pdf_pages,
    repository_links,
)
from devtools.render_explainer import COMPOSITE_ASSETS, MARKDOWN_OUTPUT, REPO_URL
from devtools.render_explainer_pdf import EXPECTED_PAGE_COUNT
from devtools.render_explainer_pdf import OUTPUT as PDF_OUTPUT
from sqpack.release import PUBLICATION_STATUS, PUBLICATION_VERSION


def workbench_page(commit: str, *, home: str = "../") -> bytes:
    return (
        f'<meta name="squares-workbench-revision" content="{commit}">'
        f'<div id="site-note"><a href="{home}">the explainer</a></div>'
    ).encode()


def test_repository_links_are_read_from_markup_and_markdown_but_not_from_scripts() -> None:
    sha = "0123456789abcdef0123456789abcdef01234567"
    text = (
        f'<a href="{REPO_URL}/blob/{sha}/packing/a.py">a</a>\n'
        f"[atlas]({REPO_URL}/tree/{sha}/packing/atlas/known-best/)\n"
        f'<script>const u = "{REPO_URL}/blob/main/packing/hidden.py";</script>\n'
        f"plain {REPO_URL}/blob/main/README.md text\n"
    )
    assert repository_links(text) == {
        ("blob", sha, "packing/a.py"),
        ("tree", sha, "packing/atlas/known-best"),
        ("blob", "main", "README.md"),
    }


def test_pdf_pages_counts_page_objects_and_refuses_what_is_not_a_pdf() -> None:
    pdf = b"%PDF-1.7\n1 0 obj << /Type /Pages /Kids [2 0 R 3 0 R] >> endobj\n"
    pdf += b"2 0 obj << /Type /Page >> endobj\n3 0 obj << /Type/Page >> endobj\n%%EOF"
    assert pdf_pages(pdf) == 2
    assert pdf_pages(b"<html>not a pdf</html>") == 0


def test_the_served_files_are_the_markdown_edition_the_pdf_and_the_composite_assets() -> None:
    assert SERVED[0] == MARKDOWN_OUTPUT.name
    assert SERVED[1] == PDF_OUTPUT.name
    assert set(SERVED[2:]) == {asset.name for asset in COMPOSITE_ASSETS}


def test_check_accepts_the_requested_build_and_rejects_a_stale_stamp(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commit = "0123456789abcdef0123456789abcdef01234567"
    stamp = " ".join(
        part for part in (PUBLICATION_STATUS, f"{PUBLICATION_VERSION}-{commit[:8]}") if part
    )
    link = f'<a href="{REPO_URL}/blob/{commit}/README.md">Repository</a>'
    page = f"<p>({stamp})</p>{link}".encode()

    def fetch(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
        assert timeout == 1
        if url.endswith("/workbench/"):
            return 200, workbench_page(commit)
        if url.endswith(".pdf"):
            pages = b"1 0 obj << /Type /Page >> endobj\n" * EXPECTED_PAGE_COUNT
            return 200, b"%PDF-1.7\n" + pages + b"%%EOF"
        return 200, b"" if head else page

    monkeypatch.setattr(check_published_site, "fetch", fetch)
    results = check_published_site.check(
        "https://example.org", commit, timeout=1, browser=False
    )
    assert all(passed for passed, _ in results), results

    page = f"<p>({stamp.replace(commit[:8], 'deadbeef')})</p>{link}".encode()
    failures = [
        line
        for passed, line in check_published_site.check(
            "https://example.org", commit, timeout=1, browser=False
        )
        if not passed
    ]
    assert len(failures) == 1
    assert "edition stamp" in failures[0]


def test_check_rejects_a_deployed_pdf_that_crossed_a_page_boundary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commit = "0123456789abcdef0123456789abcdef01234567"
    stamp = " ".join(
        part for part in (PUBLICATION_STATUS, f"{PUBLICATION_VERSION}-{commit[:8]}") if part
    )
    page = (
        f'<p>({stamp})</p><a href="{REPO_URL}/blob/{commit}/README.md">Repository</a>'
    ).encode()

    def fetch(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
        assert timeout == 1
        if url.endswith("/workbench/"):
            return 200, workbench_page(commit)
        if url.endswith(".pdf"):
            pages = b"1 0 obj << /Type /Page >> endobj\n" * (EXPECTED_PAGE_COUNT + 1)
            return 200, b"%PDF-1.7\n" + pages + b"%%EOF"
        return 200, b"" if head else page

    monkeypatch.setattr(check_published_site, "fetch", fetch)
    failures = [
        line
        for passed, line in check_published_site.check(
            "https://example.org", commit, timeout=1, browser=False
        )
        if not passed
    ]
    assert len(failures) == 1
    assert f"{EXPECTED_PAGE_COUNT + 1} pages (expected {EXPECTED_PAGE_COUNT})" in failures[0]


def test_workbench_receipt_parses_exact_revision_and_project_relative_home() -> None:
    commit = "0123456789abcdef0123456789abcdef01234567"
    text = workbench_page(commit).decode()
    revision = WORKBENCH_REVISION.search(text)
    home = WORKBENCH_HOME.search(text)
    assert revision is not None
    assert revision.group(1) == commit
    assert home is not None
    assert home.group(1) == "../"


def test_check_rejects_a_stale_workbench_or_account_root_navigation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commit = "0123456789abcdef0123456789abcdef01234567"
    stamp = " ".join(
        part for part in (PUBLICATION_STATUS, f"{PUBLICATION_VERSION}-{commit[:8]}") if part
    )
    page = (
        f'<p>({stamp})</p><a href="{REPO_URL}/blob/{commit}/README.md">Repository</a>'
    ).encode()

    def fetch(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
        assert timeout == 1
        if url.endswith("/workbench/"):
            return 200, workbench_page("f" * 40, home="/")
        if url.endswith(".pdf"):
            pages = b"1 0 obj << /Type /Page >> endobj\n" * EXPECTED_PAGE_COUNT
            return 200, b"%PDF-1.7\n" + pages + b"%%EOF"
        return 200, b"" if head else page

    monkeypatch.setattr(check_published_site, "fetch", fetch)
    failures = [
        line
        for passed, line in check_published_site.check(
            "https://example.org/squares", commit, timeout=1, browser=False
        )
        if not passed
    ]
    assert len(failures) == 2
    assert "workbench source revision" in failures[0]
    assert "workbench home resolves" in failures[1]


def test_check_requires_the_workbench_browser_api_to_start(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    commit = "0123456789abcdef0123456789abcdef01234567"
    stamp = " ".join(
        part for part in (PUBLICATION_STATUS, f"{PUBLICATION_VERSION}-{commit[:8]}") if part
    )
    page = (
        f'<p>({stamp})</p><a href="{REPO_URL}/blob/{commit}/README.md">Repository</a>'
    ).encode()

    def fetch(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
        assert timeout == 1
        if url.endswith("/workbench/"):
            return 200, workbench_page(commit)
        if url.endswith(".pdf"):
            pages = b"1 0 obj << /Type /Page >> endobj\n" * EXPECTED_PAGE_COUNT
            return 200, b"%PDF-1.7\n" + pages + b"%%EOF"
        return 200, b"" if head else page

    monkeypatch.setattr(check_published_site, "fetch", fetch)
    monkeypatch.setattr(
        check_published_site,
        "workbench_startup",
        lambda _url, _root, *, timeout: (False, f"API missing after {timeout}s"),
    )
    failures = [
        line
        for passed, line in check_published_site.check("https://example.org", commit, timeout=1)
        if not passed
    ]
    assert failures == ["API missing after 1s"]
