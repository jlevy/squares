"""The live-site check's parsing, on fixtures: the network half is not a unit of the gate."""

from __future__ import annotations

import hashlib
import re
import struct
from collections.abc import Callable, Sequence
from pathlib import Path

import pytest

from devtools import check_published_site, render_case_pages, render_overview
from devtools import render_n11_lower_bounds_explainer_pdf as pdf
from devtools.check_published_site import (
    LINK_CHECKED_PAGES,
    LOWER_BOUNDS_MARKDOWN,
    LOWER_BOUNDS_PDF,
    OMITTED_TREES,
    OPTIMALITY_PAPER,
    OPTIMALITY_PAPER_FILES,
    OPTIMALITY_PAPER_MARKDOWN,
    PAPER_VERSIONS,
    PAPERS_CURRENT,
    RECORD_FILE_SAMPLE,
    RECORD_LINK_PAGES,
    RECORD_LINK_SAMPLE,
    REVIEW_PAPERS,
    SERVED,
    SITE_PAGES,
    WORKBENCH_HOME,
    WORKBENCH_REVISION,
    RecordLinks,
    absent_links,
    cross_paper_link_checks,
    heading_ids,
    paper_citations,
    paper_files,
    pdf_pages,
    record_link_checks,
    rendered_record_links,
    repository_links,
    row_records,
)
from devtools.check_published_site import LOWER_BOUNDS_PAPER as EXPLAINER
from devtools.overview_sections import result_fragment
from devtools.render_n11_lower_bounds_explainer import (
    COMPOSITE_ASSETS,
    MARKDOWN_OUTPUT,
    PAGE_URL,
)
from devtools.render_n11_lower_bounds_explainer_pdf import EXPECTED_PAGE_COUNT
from devtools.render_n11_lower_bounds_explainer_pdf import OUTPUT as PDF_OUTPUT
from devtools.repo_links import DEFAULT_BRANCH, REPO_URL, RepositoryTree, branch_paths
from sqpack.release import EXPLAINER_VERSION, OPTIMALITY_REVIEW_EDITION, PUBLICATION_EDITION
from tests import site_renders
from tests.site_renders import prepared_forwarders

pytestmark = pytest.mark.usefixtures(prepared_forwarders.__name__)

#: A page's text linking into the repository four ways: from markup, from Markdown, from plain
#: text, and from inside a script, which the check must not read. `{{REPO_URL}}` and `{{SHA}}`
#: are filled in by the test; the script makes it a page, so it is a fixture and not a string.
REPOSITORY_LINKS = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "check_published_site"
    / "repository-links.html"
)

COMMIT = "0123456789abcdef0123456789abcdef01234567"

#: The tree `main` holds at the deploy: every path a fixture page links on `main`.
TREE = RepositoryTree(
    files=frozenset({"README.md", *(f"packing/{name}.md" for name in SITE_PAGES)}),
    directories=frozenset({"", "packing"}),
)

Fetch = Callable[..., tuple[int, bytes]]

#: The check's own reading of the checkout's commit, to tell it from a test's stand-in.
CHECKOUT_COMMIT = check_published_site.checkout_commit
#: The check's own head checks, which `failures` leaves out unless a test asks for them.
HEAD_CHECKS = check_published_site.head_checks


#: The pages a forwarder leads to, by their addresses, each with the record it writes its
#: own head from. A fixture page there says what the page says, as a deployed one does,
#: since the check holds each forwarder's preview to the head of the page it leads to.
FORWARDED = {
    render_overview.canonical_url(path): meta
    for path, meta in render_overview.forwarded_metas().items()
}


def head(path: str, *, description: str | None = None) -> str:
    """A page's head as the site writes one (`render_overview.head_tags`, then the
    site's icon), for the page served at `path` under the root, saying something of its
    own: a page a forwarder leads to, what its own record says."""
    meta = FORWARDED.get(render_overview.canonical_url(path)) or render_overview.PageMeta(
        name=f"Page {path}", description=f"What a reader finds at {path}.", path=path
    )
    if description is not None:
        meta = meta._replace(description=description)
    tags = f"{render_overview.head_tags(meta)}{render_overview.favicon_html(root='/squares/')}"
    return f'<!doctype html><html lang="en"><head>{tags}</head>'


def card(width: int = render_overview.SOCIAL_CARD_WIDTH, height: int = 630) -> bytes:
    """The start of a PNG of this size, which is all the check reads of the card."""
    header = b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR"
    return header + struct.pack(">II", width, height) + b"\x08\x06\x00\x00\x00"


def workbench_page(commit: str, *, home: str = "../") -> bytes:
    return (
        head(check_published_site.WORKBENCH_PAGE)
        + f'<meta name="squares-workbench-revision" content="{commit}">'
        f'<div id="site-note"><a href="{home}">the overview</a></div>'
    ).encode()


def source_receipt(page: bytes) -> bytes:
    return f"\n%sqpack-source-html-sha256: {hashlib.sha256(page).hexdigest()}\n".encode()


#: How many cases the fake deploy's record page indexes.
CASE_COUNT = 324


def page(
    canonical: str,
    *,
    ref: str = DEFAULT_BRANCH,
    stamp: str = PUBLICATION_EDITION,
    link: str = "README.md",
    bar: str = "",
) -> bytes:
    """A served page as the check reads one: the head of the page served at `canonical`,
    with its canonical link, then for a paper its bar's current entry (`bar`), the stamp
    and a repository link; the record page also indexes every case's record file."""
    path = canonical.removeprefix(render_overview.SITE_URL) or "index.html"
    index = (
        "".join(f'<a href="{n}.html" data-case="{n}">{n}</a>' for n in range(1, CASE_COUNT + 1))
        if path == render_case_pages.CASES_HOME
        else ""
    )
    return (
        f"{head(path)}{bar}"
        f'<p>({stamp})</p><a href="{REPO_URL}/blob/{ref}/{link}">Repository</a>{index}'
    ).encode()


def explainer_page(canonical: str = PAGE_URL, **kwargs: str) -> bytes:
    """The lower-bounds explainer as the check reads it: a page with Papers current in
    its bar, linked from a level below the root, carrying the paper's own version and
    not the site's edition."""
    kwargs.setdefault("stamp", EXPLAINER_VERSION)
    return page(canonical, bar=PAPERS_CURRENT + "Papers</a>", **kwargs)


#: The result overviews the fixture's results table names, by address beside the pages.
OVERVIEWS = ("result/t-001.html", "result/t-002.html")


def case_record(n: int) -> bytes:
    """A case's record file as it is served: a page's head for its own address, then
    its record, which names its case."""
    canonical = render_overview.canonical_url(render_case_pages.case_url(n))
    return page(canonical) + f'<article class="site-case" data-case="{n}"></article>'.encode()


def result_overview(
    result_id: str, *, ref: str = DEFAULT_BRANCH, link: str = "README.md"
) -> bytes:
    """A result's overview as it is served: the one block, with a repository link."""
    return (
        f'<article class="site-result" data-result-overview="{result_id}">'
        f'<a href="{REPO_URL}/blob/{ref}/{link}">Register</a></article>\n'
    ).encode()


#: The record link the fixture's renderer writes for every result: the one file `TREE`
#: holds at the root.
RECORD = f"{REPO_URL}/blob/{DEFAULT_BRANCH}/README.md"
#: What the renderer is taken to write for the fixture site: one record link in each of
#: two result rows, and the first overview, sampled, with the link `result_overview` gives.
EXPECTED_RECORDS = RecordLinks(
    rows={"t-001": RECORD, "t-002": RECORD},
    overviews={OVERVIEWS[0]: result_overview("t-001").decode()},
)


def result_row(row: str, *, here: bool, records: bool = True) -> str:
    """A result's row and the popover it opens, as a table of results writes them: the
    row named by `id` on the results page (`here`) and by `data-result` anywhere else,
    and its popover, whose short form ends with its line of record links."""
    link = f'<a href="{RECORD}">register</a>' if records else ""
    return (
        f'<tr {"id" if here else "data-result"}="{row}" data-s="3"><td>{row}</td>'
        '<td class="site-col-result">A result</td></tr>'
        f'<div class="site-popover site-row-pop" id="pop-result-{row}" popover role="dialog">'
        f'<dl class="site-detail"><dt>Records</dt><dd><div class="site-records">{link}</div>'
        "</dd></dl></div>"
    )


def results_table(*, here: bool) -> bytes:
    """The table of results on a page, every row's popover with its record link."""
    rows = "".join(result_row(row, here=here) for row in EXPECTED_RECORDS.rows)
    return f"<table><tbody>{rows}</tbody></table>".encode()


def review_paper(review: str, *, ref: str = COMMIT, link: str = "README.md") -> bytes:
    """A review's page as the check reads one: the bar with Papers current, its own
    version, and one citation, which the paper pins to the commit it was built from."""
    slug = review.removeprefix("papers/").removesuffix(".html")
    return (
        head(review)
        + PAPERS_CURRENT
        + f"Papers</a><p>({PAPER_VERSIONS[slug]})</p>"
        + f'<a href="{REPO_URL}/blob/{ref}/{link}#anchor">Receipt</a>'
    ).encode()


def optimality_paper(*, ref: str = COMMIT, link: str = "README.md") -> bytes:
    """The optimality paper's page as the check reads one (`review_paper`)."""
    return review_paper(OPTIMALITY_PAPER, ref=ref, link=link)


def optimality_markdown(*, ref: str = COMMIT, link: str = "README.md") -> bytes:
    """The paper's Markdown, with the same citation as a Markdown link."""
    return f"[Receipt]({REPO_URL}/blob/{ref}/{link}#anchor)\n".encode()


def site_pages(**overrides: bytes) -> dict[str, bytes]:
    """Every page a good deploy serves, by served name, each named as its renderer names it,
    and the result overviews its results table names, by their address."""
    return site_naming(OVERVIEWS, **overrides)


def site_naming(named: Sequence[str], /, **overrides: bytes) -> dict[str, bytes]:
    """`site_pages`, with the results table, whichever page stands for it, naming the
    overviews in `named`."""
    pages = {
        name: page(render_overview.canonical_url(name), link=f"packing/{name}.md")
        for name in SITE_PAGES
    }
    pages[EXPLAINER] = explainer_page()
    # The record files a check samples, beside the record page that indexes them all.
    for n in {1, RECORD_FILE_SAMPLE, CASE_COUNT}:
        pages[render_case_pages.case_url(n)] = case_record(n)
    for address in OVERVIEWS:
        pages[address] = result_overview(address.rsplit("/", 1)[1].removesuffix(".html"))
    for review in REVIEW_PAPERS:
        pages[review] = review_paper(review)
        pages[paper_files(review)[0]] = optimality_markdown()
    pages[LOWER_BOUNDS_MARKDOWN] = b"the Markdown edition\n"
    pages[render_overview.SOCIAL_CARD] = card()
    # What keeps the links written before the papers moved: the forwarders the
    # overview's build writes, and each moved file again at its old address.
    for forwarder in render_overview.forwarder_pages():
        pages[forwarder.name] = forwarder.html.encode()
    pages.update(overrides)
    for old, new in render_overview.MOVED_FILES:
        if new in pages:
            pages.setdefault(old, pages[new])
    pages[render_overview.RESULTS_PAGE] += "".join(
        f'<div class="site-row-pop-body" data-row-pop-src="{address}"></div>'
        for address in named
    ).encode()
    for name in RECORD_LINK_PAGES:
        pages[name] += results_table(here=name == render_overview.RESULTS_PAGE)
    return pages


def test_fake_deploy_variants_keep_the_prepared_forwarders_immutable(
    prepared_forwarders: tuple[render_overview.Page, ...],
) -> None:
    first = render_overview.forwarder_pages()
    second = render_overview.forwarder_pages()
    assert first is not second
    assert tuple(first) == tuple(second) == prepared_forwarders
    first.pop()
    assert tuple(render_overview.forwarder_pages()) == prepared_forwarders
    changed = site_pages(**{"cases.html": b"a deliberately broken forwarder"})
    original = site_pages()
    assert changed is not original
    assert original["cases.html"] == next(
        page.html.encode() for page in prepared_forwarders if page.name == "cases.html"
    )
    assert changed["cases.html"] != original["cases.html"]


def fake_site(
    pages: dict[str, bytes],
    *,
    workbench: bytes | None = None,
    pdf_page_count: int = EXPECTED_PAGE_COUNT,
    receipt: bytes | None = None,
    requested: list[str] | None = None,
    lost: Sequence[str] = (),
) -> Fetch:
    """A deployed site at any root: its pages, the workbench, the PDF, and every link.
    An address ending in one of `lost` is a 404."""

    def fetch(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
        assert timeout == 1
        if requested is not None:
            requested.append(url)
        if any(url.endswith(name) for name in lost):
            return 404, b"Not found"
        if url.startswith(REPO_URL):
            return 200, b""
        if url.endswith("/workbench/"):
            return 200, workbench if workbench is not None else workbench_page(COMMIT)
        if url.endswith(".pdf"):
            pages_ = b"1 0 obj << /Type /Page >> endobj\n" * pdf_page_count
            tail = receipt if receipt is not None else source_receipt(pages[EXPLAINER])
            return 200, b"%PDF-1.7\n" + pages_ + b"%%EOF" + tail
        name = "index.html" if url.endswith("/") else url.rsplit("/", 1)[1]
        nested = "/".join(url.rsplit("/", 2)[1:])
        if nested.startswith("result/") and nested not in pages:
            return 404, b"Not found"
        body = pages.get(nested, pages.get(name, b"served"))
        return 200, b"" if head else body

    return fetch


def fixture_records(monkeypatch: pytest.MonkeyPatch) -> None:
    """Hold the fixture site to the fixture's record links, as rendered at its commit.
    A test that asks about the renderer itself, or about another checkout, sets its own
    first, and that is kept."""
    monkeypatch.setattr(
        check_published_site, "deployed_registry_checks", lambda *_args, **_kwargs: []
    )
    if check_published_site.rendered_record_links is rendered_record_links:
        monkeypatch.setattr(
            check_published_site, "rendered_record_links", lambda: EXPECTED_RECORDS
        )
    if check_published_site.checkout_commit is CHECKOUT_COMMIT:
        monkeypatch.setattr(check_published_site, "checkout_commit", lambda: COMMIT)


def failures(
    monkeypatch: pytest.MonkeyPatch,
    fetch: Fetch,
    *,
    site: str = "https://example.org",
    browser: bool = False,
    heads: bool = False,
) -> list[str]:
    """What the check fails on this site. The head checks read every page again for what
    it says of itself, so a page a test breaks in one way fails them in others; they are
    left out unless `heads` asks for them, and the tests of the heads ask."""
    monkeypatch.setattr(check_published_site, "fetch", fetch)
    # These fixtures test specialized assurance; the complete walk has its own fixtures.
    monkeypatch.setattr(
        check_published_site, "deployed_registry_checks", lambda *_args, **_kwargs: []
    )
    monkeypatch.setattr(
        check_published_site, "head_checks", HEAD_CHECKS if heads else lambda *_: []
    )
    monkeypatch.setattr(
        check_published_site,
        "repository_tree",
        lambda commit: TREE if commit == COMMIT else None,
    )
    fixture_records(monkeypatch)
    return [
        line
        for passed, line in check_published_site.check(site, COMMIT, timeout=1, browser=browser)
        if not passed
    ]


def test_repository_links_are_read_from_markup_and_markdown_but_not_from_scripts() -> None:
    sha = "0123456789abcdef0123456789abcdef01234567"
    text = (
        REPOSITORY_LINKS.read_text(encoding="utf-8")
        .replace("{{REPO_URL}}", REPO_URL)
        .replace("{{SHA}}", sha)
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
    """The Markdown and the PDF are beside the page under `papers/`, by the paper's slug
    and as the renderer and the exporter name them; the atlas's files are at the root."""
    assert SERVED[0] == LOWER_BOUNDS_MARKDOWN == "papers/n11-lower-bounds-explainer.md"
    assert SERVED[1] == LOWER_BOUNDS_PDF == "papers/n11-lower-bounds-explainer.pdf"
    assert LOWER_BOUNDS_MARKDOWN.endswith(f"/{MARKDOWN_OUTPUT.name}")
    assert LOWER_BOUNDS_PDF.endswith(f"/{PDF_OUTPUT.name}")
    assert set(SERVED[2:]) == {asset.name for asset in COMPOSITE_ASSETS}


def test_the_checked_pages_are_every_page_the_site_serves_but_the_workbench() -> None:
    """The overview's renderer is the list: a page added there is checked without an edit.

    The explainer is served under `papers/` by its slug, where the Papers card links it
    and where its own canonical URL says it is, so the three cannot disagree.
    """
    assert tuple(render_overview.PAGES) == SITE_PAGES
    assert SITE_PAGES.index("index.html") == 0
    assert PAGE_URL.endswith(f"/squares/{EXPLAINER}")
    assert EXPLAINER == "papers/n11-lower-bounds-explainer.html"
    assert {*SITE_PAGES, EXPLAINER, "workbench/index.html"} <= set(render_overview.SITE_PAGES)
    assert {"index.html", "frontier.html", "all-results.html"} == LINK_CHECKED_PAGES
    assert render_overview.canonical_url("index.html") == check_published_site.SITE_URL
    assert render_overview.canonical_url("tutorial.html").endswith("/squares/tutorial.html")
    # The papers page was added to the renderer alone, and is checked here for it.
    assert "papers.html" in SITE_PAGES
    assert render_overview.canonical_url("papers.html").endswith("/squares/papers.html")


def test_live_source_check_accepts_the_receipt_written_by_the_pdf_exporter(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    page = tmp_path / "n11-lower-bounds-explainer.html"
    page.write_bytes(b"<html>the exact publication source</html>\n")
    output = page.with_suffix(".pdf")
    monkeypatch.setattr(pdf, "PAGE", page)
    monkeypatch.setattr(pdf, "OUTPUT", output)
    monkeypatch.setattr(pdf, "render_pdf_bytes", lambda: b"%PDF-1.7\n%%EOF\n")
    pdf.update()
    assert check_published_site.pdf_source_matches(output.read_bytes(), page.read_bytes())


def test_check_accepts_the_requested_build_and_rejects_a_stale_stamp(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requested: list[str] = []
    assert failures(monkeypatch, fake_site(site_pages(), requested=requested)) == []
    assert "https://example.org/" in requested
    assert f"https://example.org/{EXPLAINER}" in requested
    assert "https://example.org/index.html" not in requested, "the overview is the root"

    stale = site_pages(**{EXPLAINER: explainer_page(stamp="v0.0.0")})
    (failure,) = failures(monkeypatch, fake_site(stale))
    assert failure == f"version {EXPLAINER_VERSION!r} is not on {EXPLAINER}"

    stale = site_pages(**{"index.html": page(render_overview.SITE_URL, stamp="v0.0.0-deadbe")})
    (failure,) = failures(monkeypatch, fake_site(stale))
    assert failure == f"version {PUBLICATION_EDITION!r} is not on index.html"

    # A paper carries its own version and not the site's edition (the owner,
    # 2026-10-01); a paper that prints the site's edition beside its own fails for that.
    site_edition = f"<p>({PUBLICATION_EDITION})</p>".encode()
    for name, paper in ((EXPLAINER, explainer_page()), (OPTIMALITY_PAPER, optimality_paper())):
        stamped = site_pages(**{name: paper + site_edition})
        (failure,) = failures(monkeypatch, fake_site(stamped))
        assert failure == (
            f"the site's edition {PUBLICATION_EDITION!r} is on {name}, which carries its "
            "own version"
        )
    unversioned = site_pages(
        **{
            OPTIMALITY_PAPER: optimality_paper().replace(
                OPTIMALITY_REVIEW_EDITION.encode(), b""
            )
        }
    )
    (failure,) = failures(monkeypatch, fake_site(unversioned))
    assert failure == f"version {OPTIMALITY_REVIEW_EDITION!r} is not on {OPTIMALITY_PAPER}"


def test_check_requires_each_page_to_name_its_own_canonical_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A page served under another's name, or the explainer still claiming the root.

    The explainer's canonical URL is how a search engine and a share card find it; one
    left at `/` after the move would point both at the overview.
    """
    swapped = site_pages(**{EXPLAINER: explainer_page(render_overview.SITE_URL)})
    (failure,) = failures(monkeypatch, fake_site(swapped))
    assert f"{EXPLAINER} names canonical URL" in failure

    for name in SITE_PAGES:
        wrong = site_pages(**{name: page(PAGE_URL)})
        found = failures(monkeypatch, fake_site(wrong))
        assert any(f"{name} names canonical URL" in line for line in found), name
        # The record page served as another page has lost its index of record files too.
        assert len(found) == (2 if name == render_case_pages.CASES_PAGE else 1), found

    missing = site_pages(**{"index.html": b"<p>(" + PUBLICATION_EDITION.encode() + b")</p>"})
    found = failures(monkeypatch, fake_site(missing))
    assert any("index.html names canonical URL None" in line for line in found), found


def test_check_refuses_a_repository_link_pinned_to_a_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A link to the commit a page was built from 404s once a squash merge leaves that
    commit on no branch, so every page, full hash or short, is held to `main`.

    Only the overview, the frontier atlas and the explainer have each link asked of
    GitHub as well.
    """
    for name in SITE_PAGES:
        for ref in (COMMIT, COMMIT[:8]):
            pinned = page(render_overview.canonical_url(name), ref=ref)
            found = failures(monkeypatch, fake_site(site_pages(**{name: pinned})))
            url = f"{REPO_URL}/blob/{ref}/README.md"
            assert found == [f"{name}: 1 repository links pinned to a commit: [{url!r}]"], (
                name,
                found,
            )

    requested: list[str] = []
    assert failures(monkeypatch, fake_site(site_pages(), requested=requested)) == []
    asked = {url.removeprefix(f"{REPO_URL}/blob/{DEFAULT_BRANCH}/") for url in requested}
    for name in SITE_PAGES:
        assert (f"packing/{name}.md" in asked) == (name in LINK_CHECKED_PAGES), name
    assert "README.md" in asked, "the explainer's links are still asked"


def test_check_requires_every_path_linked_on_main_to_be_in_the_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A path on `main` that the deployed commit's tree lacks is a 404 from the start."""
    for name in SITE_PAGES:
        gone = page(render_overview.canonical_url(name), link="packing/gone.md")
        found = failures(monkeypatch, fake_site(site_pages(**{name: gone})))
        assert found == [
            f"{name}: linked on main but not in {COMMIT[:12]}: ['blob/packing/gone.md']"
        ], name


def test_check_requires_every_result_overview_the_results_table_names(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A row's popover fetches its result's overview from beside the page, so a deploy
    without one, or with another result's under its name, shows only as a popover that
    keeps its short detail. Each named overview is asked for, and its repository links
    are held to `main` and to the commit's tree as a page's are."""
    requested: list[str] = []
    assert failures(monkeypatch, fake_site(site_pages(), requested=requested)) == []
    for address in OVERVIEWS:
        assert f"https://example.org/{address}" in requested

    lost = site_naming((*OVERVIEWS, "result/t-003.html"))
    assert failures(monkeypatch, fake_site(lost)) == [
        "result overview result/t-003.html: HTTP 404, 9 bytes, but it is None"
    ]

    swapped = site_pages(**{"result/t-002.html": result_overview("t-001")})
    (failure,) = failures(monkeypatch, fake_site(swapped))
    assert failure.startswith("result overview result/t-002.html: HTTP 200, ")
    assert failure.endswith("but it is 'result/t-001.html'")

    assert failures(monkeypatch, fake_site(site_naming(()))) == [
        "all-results.html names 0 result overviews",
        f"result overview {OVERVIEWS[0]}: sampled for its record links and not served",
    ]

    # The second overview is not one the fixture samples for its record links, so each
    # of these is the one failure.
    pinned = site_pages(**{"result/t-002.html": result_overview("t-002", ref=COMMIT[:8])})
    url = f"{REPO_URL}/blob/{COMMIT[:8]}/README.md"
    assert failures(monkeypatch, fake_site(pinned)) == [
        f"the result overviews: 1 repository links pinned to a commit: [{url!r}]"
    ]

    gone = site_pages(**{"result/t-002.html": result_overview("t-002", link="packing/gone.md")})
    missing = f"linked on main but not in {COMMIT[:12]}: ['blob/packing/gone.md']"
    assert failures(monkeypatch, fake_site(gone)) == [f"the result overviews: {missing}"]


def test_absent_links_names_what_a_deploy_dropped_and_rows_are_read_one_by_one() -> None:
    packet = f"{REPO_URL}/blob/{DEFAULT_BRANCH}/packing/resources/web/a-packet/README.md"
    line = f"{RECORD}?plain=1#L12"
    rendered = f'<a href="{line}">register</a> <a href="{packet}">packet</a>'
    assert absent_links(rendered, rendered) == []
    assert absent_links(rendered, f'<a href="{RECORD}">register</a>') == [
        "blob/packing/resources/web/a-packet/README.md"
    ]
    # The path is what is asked for, not the anchor into it or the link's words.
    assert (
        absent_links(f"{line}\n{packet}", f'<a href="{RECORD}">r</a><a href="{packet}">p</a>')
        == []
    )
    # A commit-pinned link to the same file is not the link on `main`.
    pinned = packet.replace(f"/{DEFAULT_BRANCH}/", f"/{COMMIT}/")
    assert absent_links(packet, f'<a href="{pinned}">packet</a>') == [
        "blob/packing/resources/web/a-packet/README.md"
    ]

    table = (
        "<table><thead><tr><th>ID</th></tr></thead><tbody>"
        + result_row("t-001", here=True, records=False).replace(
            '<div class="site-records"></div>', ""
        )
        + result_row("t-002", here=True)
        + "</tbody></table>"
        + '<div class="site-popover site-row-pop" id="pop-case-18" popover>'
        + '<div class="site-records">not a result</div></div>'
    )
    # A popover without its line is not given the next one's, and only result rows'
    # popovers are read.
    assert row_records(table) == {"t-002": f'<a href="{RECORD}">register</a>'}
    assert row_records(result_row("t-007", here=False)) == {
        "t-007": f'<a href="{RECORD}">register</a>'
    }


def test_check_requires_every_record_link_the_renderer_writes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Every other check asks whether a link that was written resolves, so a deploy that
    wrote fewer links passed all of them (D-512): the Pages jobs' partial checkout dropped
    each link into the literature archive and the campaign. The renderer says what the
    rows and the sampled overviews link, and a page that lacks one link fails."""
    assert failures(monkeypatch, fake_site(site_pages())) == []

    for name in RECORD_LINK_PAGES:
        here = name == render_overview.RESULTS_PAGE
        pages = site_pages()
        full, bare = (result_row("t-002", here=here, records=keep) for keep in (True, False))
        assert pages[name].count(full.encode()) == 1
        pages[name] = pages[name].replace(full.encode(), bare.encode())
        lacks = (
            f"{name}: 1 of 2 result rows lack record links the renderer writes: "
            "t-002 lacks ['blob/README.md']"
        )
        assert failures(monkeypatch, fake_site(pages)) == [lacks], name
        # A row that is gone lacks its links as one that lost them does.
        pages[name] = pages[name].replace(bare.encode(), b"")
        (failure,) = failures(monkeypatch, fake_site(pages))
        assert failure.startswith(f"{name}: 1 of 2 result rows lack record links"), name

    # The sampled overview with its record link dropped: it links another file `main`
    # holds, so every link that was written resolves and only this check fails.
    address = OVERVIEWS[0]
    dropped = site_pages(**{address: result_overview("t-001", link="packing/index.html.md")})
    lacks = (
        f"result overview {address}: lacks 1 of the 1 repository links the renderer "
        "writes for it: ['blob/README.md']"
    )
    assert failures(monkeypatch, fake_site(dropped)) == [lacks]

    # The expectation rendered in a checkout that is not at the deployed commit says so,
    # since the failure may then be the checkout's.
    monkeypatch.setattr(check_published_site, "checkout_commit", lambda: "f" * 40)
    (failure,) = failures(monkeypatch, fake_site(dropped))
    assert failure.endswith(f" (expected as rendered at {'f' * 12}, not {COMMIT[:12]})")
    assert failures(monkeypatch, fake_site(site_pages())) == []


def test_check_fails_when_the_record_links_cannot_be_rendered(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def refuses() -> RecordLinks:
        raise SystemExit("the register has no T-060 to sample")

    monkeypatch.setattr(check_published_site, "rendered_record_links", refuses)
    refused = (
        "the record links cannot be rendered in this checkout: "
        "the register has no T-060 to sample"
    )
    assert failures(monkeypatch, fake_site(site_pages())) == [refused]


def test_the_sample_cites_the_archive_and_the_campaign_whatever_the_checkout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """What the deploy is held to is what the renderer writes from the register: every
    result's row, and the overviews of `RECORD_LINK_SAMPLE`, which between them cite
    files under directories of both trees a partial checkout omits. The answer is the
    same in such a checkout, which is where the deployed pages are rendered."""
    expected = rendered_record_links()
    assert set(expected.overviews) == {result_fragment(result) for result in RECORD_LINK_SAMPLE}
    assert len(expected.rows) >= 61
    assert set(expected.rows) >= {result.lower() for result in RECORD_LINK_SAMPLE}
    cited = {path for body in expected.overviews.values() for _, path in branch_paths(body)}
    for tree in OMITTED_TREES:
        assert any(path.startswith(tree) and "/" in path.removeprefix(tree) for path in cited)
    packet = "packing/resources/web/n11-optimality-2026-09-29"
    settled = {path for _, path in branch_paths(expected.overviews[result_fragment("T-060")])}
    assert {f"{packet}/receipts/final-composition.json", f"{packet}/source/PROOF.md"} <= settled
    assert f"{packet}/source/PROOF.md" in expected.rows["t-060"]
    # Held to itself the expectation passes; T-060's overview without its packet's links
    # does not, and the line names what is gone.
    held = record_link_checks(expected, {}, expected.overviews)
    assert [passed for passed, _ in held] == [True] * len(RECORD_LINK_SAMPLE)
    address = result_fragment("T-060")
    served = {address: expected.overviews[address].replace(f"/{packet}/", "/packing/frontier/")}
    ((passed, line),) = record_link_checks(
        RecordLinks({}, {address: expected.overviews[address]}), {}, served
    )
    assert not passed
    assert f"blob/{packet}/receipts/final-composition.json" in line

    site_renders.leave_out_the_archive_and_the_campaign(monkeypatch)
    assert rendered_record_links() == expected


@pytest.mark.parametrize(
    ("review", "label"),
    [
        ("papers/n11-threshold-bound-review.html", "Part II"),
        ("papers/n11-optimality-review.html", "Part III"),
    ],
)
def test_check_requires_each_review_where_its_papers_card_points(
    monkeypatch: pytest.MonkeyPatch, review: str, label: str
) -> None:
    """The Papers page's cards open each review, which a build of its own writes under
    `papers/`: a deploy without it, or with a page there whose bar does not mark Papers,
    or that lacks its own version, fails, and so does one without its Markdown or its
    PDF."""
    assert review in REVIEW_PAPERS
    assert OPTIMALITY_PAPER == "papers/n11-optimality-review.html"
    assert OPTIMALITY_PAPER_FILES == (
        "papers/n11-optimality-review.md",
        "papers/n11-optimality-review.pdf",
    )
    assert review in render_overview.SITE_PAGES
    files = paper_files(review)
    requested: list[str] = []
    assert failures(monkeypatch, fake_site(site_pages(), requested=requested)) == []
    for name in (review, *files):
        assert f"https://example.org/{name}" in requested, name

    (failure,) = failures(monkeypatch, fake_site(site_pages(), lost=(review,)))
    assert failure.startswith(f"{label} {review}: HTTP 404, ")
    assert failure.endswith("Papers is not the bar's current entry")

    bare = site_pages(**{review: review_paper(review).replace(b' aria-current="page"', b"")})
    (failure,) = failures(monkeypatch, fake_site(bare))
    assert failure.startswith(f"{label} {review}: HTTP 200, ")
    assert failure.endswith("Papers is not the bar's current entry")

    slug = review.removeprefix("papers/").removesuffix(".html")
    unversioned = site_pages(
        **{review: review_paper(review).replace(PAPER_VERSIONS[slug].encode(), b"v0")}
    )
    (failure,) = failures(monkeypatch, fake_site(unversioned))
    assert failure == f"version {PAPER_VERSIONS[slug]!r} is not on {review}"

    # A lost file is also what its old address was to be a copy of, where it had one.
    for name in files:
        found = failures(monkeypatch, fake_site(site_pages(), lost=(f"/{name}",)))
        assert found[0] == f"served {name}: HTTP 404", name
        assert all(line.startswith("moved file ") for line in found[1:]), found


def test_the_versions_the_check_holds_are_the_papers_own() -> None:
    """Every paper of the site has the version its front prints, and only those."""
    assert set(PAPER_VERSIONS) == {paper.slug for paper in render_overview.PAPERS}
    assert PAPER_VERSIONS[render_overview.N11_OPTIMALITY_REVIEW] == OPTIMALITY_REVIEW_EDITION
    assert PAPER_VERSIONS[render_overview.N11_LOWER_BOUNDS_EXPLAINER] == EXPLAINER_VERSION


def _paper_page(*headings: str, links: str = "") -> str:
    """A paper's page as the link check reads it: its headings, each with its id, and
    its links."""
    return "".join(f'<h2 id="{anchor}">{anchor}</h2>' for anchor in headings) + links


def test_every_link_between_papers_names_a_paper_and_a_heading_it_has() -> None:
    """A link from one paper to another (`devtools.paper_links`) names a paper the site
    serves and, with an anchor, a heading of that paper, on the page and in the Markdown
    edition alike. A link to a paper not in the build is reported and not failed; one to
    a paper the site does not serve, or to a heading the paper does not have, fails."""
    explainer, threshold, optimality = (
        render_overview.paper_path(paper.slug) for paper in render_overview.PAPERS
    )
    site = render_overview.SITE_URL + "papers/"
    pages = {
        explainer: _paper_page(
            "the-result-and-proof-roadmap",
            links='<a href="n11-threshold-bound-review.html#the-result">II</a>'
            '<a href="n11-optimality-review.html">III</a><a href="papers.html">Papers</a>',
        ),
        threshold: _paper_page("the-result", "what-is-new"),
        optimality: _paper_page(
            "the-result",
            links=(
                '<a href="n11-lower-bounds-explainer.html#the-result-and-proof-roadmap">I</a>'
            ),
        ),
    }
    markdowns = {
        paper_files(optimality)[0]: (
            f"[I]({site}n11-lower-bounds-explainer.html#the-result-and-proof-roadmap) "
            f"[II]({site}n11-threshold-bound-review.html#what-is-new)\n"
        ),
    }
    assert heading_ids(pages[threshold]) == {"the-result", "what-is-new"}
    found = cross_paper_link_checks(pages, markdowns)
    assert [passed for passed, _ in found] == [True, True, True]
    assert found[0][1] == (
        f"{explainer}: 2 links to other papers, "
        "each to a paper served here and a heading it has"
    )
    assert paper_files(optimality)[0] in found[2][1]

    broken = {
        **pages,
        explainer: pages[explainer].replace("#the-result", "#no-such-heading"),
    }
    (failure, *_) = cross_paper_link_checks(broken, {})
    assert not failure[0]
    assert f"{threshold}#no-such-heading, no heading of that paper" in failure[1]
    stray = {paper_files(optimality)[0]: f"[x]({site}n11-no-such-paper.html)\n"}
    ((_, line),) = [found for found in cross_paper_link_checks(pages, stray) if not found[0]]
    assert line.startswith(paper_files(optimality)[0])
    assert "n11-no-such-paper.html, no paper of the site" in line
    unbuilt = {name: text for name, text in pages.items() if name != threshold}
    (first, *_) = cross_paper_link_checks(unbuilt, {})
    assert first[0]
    assert "not in this build, so not checked" in first[1]


def test_the_optimality_papers_citations_name_the_deployed_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The paper is the one page whose repository links are held to a commit and not to
    `main`: it cites the evidence as it stood when it was typeset, and the deploy builds
    it from the commit it deploys, which `main` keeps. So each citation, on the page and
    in its Markdown, names the expected commit, and every cited path is in that commit's
    tree. A citation on `main` or at another commit fails, as does a page with none and
    a cited path the tree lacks."""
    assert OPTIMALITY_PAPER_MARKDOWN == "papers/n11-optimality-review.md"
    assert OPTIMALITY_PAPER_MARKDOWN in OPTIMALITY_PAPER_FILES
    other = "f" * 40
    text = (
        f'<a href="{REPO_URL}/blob/{COMMIT}/packing/a.md#part">a</a>'
        f'<a href="{REPO_URL}/blob/{COMMIT}/packing/b.json?plain=1">b</a>'
        f'<a href="{REPO_URL}/blob/main/README.md">c</a>'
        f'<a href="{REPO_URL}/tree/{other}/packing">d</a>'
        f'<a href="{REPO_URL}">the repository itself is not a citation</a>'
    )
    assert paper_citations(text, COMMIT) == (
        {("blob", "packing/a.md"), ("blob", "packing/b.json")},
        ["blob/main/README.md", f"tree/{other}/packing"],
    )

    requested: list[str] = []
    assert failures(monkeypatch, fake_site(site_pages(), requested=requested)) == []
    assert f"https://example.org/{OPTIMALITY_PAPER_MARKDOWN}" in requested

    for name, made in (
        (OPTIMALITY_PAPER, optimality_paper),
        (OPTIMALITY_PAPER_MARKDOWN, optimality_markdown),
    ):
        stray = f"{name}: 1 repository links not pinned to {COMMIT[:12]}: "
        on_main = site_pages(**{name: made(ref=DEFAULT_BRANCH)})
        assert failures(monkeypatch, fake_site(on_main)) == [
            stray + "['blob/main/README.md#anchor']"
        ]
        elsewhere = site_pages(**{name: made(ref=other)})
        assert failures(monkeypatch, fake_site(elsewhere)) == [
            stray + f"['blob/{other}/README.md#anchor']"
        ]
        gone = site_pages(**{name: made(link="packing/gone.md")})
        assert failures(monkeypatch, fake_site(gone)) == [
            f"{name}: cited at {COMMIT[:12]} but not in its tree: ['blob/packing/gone.md']"
        ]
    uncited = site_pages(**{OPTIMALITY_PAPER_MARKDOWN: b"# A paper citing nothing\n"})
    assert failures(monkeypatch, fake_site(uncited)) == [
        f"{OPTIMALITY_PAPER_MARKDOWN}: 0 citations, each pinned to {COMMIT[:12]}"
    ]


def test_check_fails_when_the_commit_tree_cannot_be_read(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unreadable(commit: str) -> RepositoryTree:
        raise SystemExit(f"git ls-tree {commit} failed")

    monkeypatch.setattr(check_published_site, "fetch", fake_site(site_pages()))
    monkeypatch.setattr(check_published_site, "repository_tree", unreadable)
    fixture_records(monkeypatch)
    found = [
        line
        for passed, line in check_published_site.check(
            "https://example.org", COMMIT, timeout=1, browser=False
        )
        if not passed
    ]
    assert found == [f"the tree of {COMMIT} cannot be read here: git ls-tree {COMMIT} failed"]


def test_check_rejects_a_deployed_pdf_that_crossed_a_page_boundary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    found = failures(
        monkeypatch, fake_site(site_pages(), pdf_page_count=EXPECTED_PAGE_COUNT + 1)
    )
    assert len(found) == 1
    assert f"{EXPECTED_PAGE_COUNT + 1} pages (expected {EXPECTED_PAGE_COUNT})" in found[0]


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
    found = failures(
        monkeypatch,
        fake_site(site_pages(), workbench=workbench_page("f" * 40, home="/")),
        site="https://example.org/squares",
    )
    assert len(found) == 2
    assert "workbench source revision" in found[0]
    assert "workbench home resolves" in found[1]


def test_check_requires_the_workbench_browser_api_to_start(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        check_published_site,
        "workbench_startup",
        lambda _url, _root, *, timeout: (False, f"API missing after {timeout}s"),
    )
    monkeypatch.setattr(check_published_site, "forwarders_followed", lambda _site, **_: [])
    assert failures(monkeypatch, fake_site(site_pages()), browser=True) == [
        "API missing after 1s"
    ]


@pytest.mark.parametrize(
    "receipt_kind",
    ["missing", "malformed", "wrong-source", "duplicate", "uppercase", "trailing-data"],
)
def test_check_rejects_a_pdf_without_the_deployed_html_source_receipt(
    monkeypatch: pytest.MonkeyPatch, receipt_kind: str
) -> None:
    pages = site_pages()
    explainer = pages[EXPLAINER]
    valid = source_receipt(explainer)
    receipt = {
        "missing": b"",
        "malformed": b"\n%sqpack-source-html-sha256: not-a-digest\n",
        "wrong-source": source_receipt(explainer + b"<!-- old source -->"),
        "duplicate": valid + valid,
        "uppercase": valid[: valid.index(b":") + 1] + valid[valid.index(b":") + 1 :].upper(),
        "trailing-data": valid + b"unbound suffix",
    }[receipt_kind]
    found = failures(monkeypatch, fake_site(pages, receipt=receipt))
    assert len(found) == 1
    assert "source HTML receipt" in found[0]


def test_check_compares_the_exact_fetched_html_bytes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pages = site_pages(**{EXPLAINER: explainer_page() + b"<!-- byte-exact source: \xff -->"})
    assert failures(monkeypatch, fake_site(pages)) == []

    overview_receipt = source_receipt(pages["index.html"])
    (found,) = failures(monkeypatch, fake_site(pages, receipt=overview_receipt))
    assert "source HTML receipt" in found, "the receipt names the explainer, not the root"


def test_fetch_retries_a_transient_answer_before_reporting_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Pages can answer 404 or 5xx for a short while after a deploy reports success, and
    the check runs straight after it (#160 R26). A lasting answer is still reported."""
    answers = [(404, b""), (503, b""), (200, b"page")]
    pauses: list[float] = []
    monkeypatch.setattr(
        check_published_site, "fetch_once", lambda _url, **_kwargs: answers.pop(0)
    )
    status = check_published_site.fetch(
        "https://example.org/", timeout=1, delays=(1.0, 2.0, 4.0), sleep=pauses.append
    )
    assert status == (200, b"page")
    assert pauses == [1.0, 2.0]

    pauses.clear()
    monkeypatch.setattr(check_published_site, "fetch_once", lambda _url, **_kwargs: (0, b""))
    status = check_published_site.fetch(
        "https://example.org/", timeout=1, delays=(1.0, 2.0), sleep=pauses.append
    )
    assert status == (0, b"")
    assert pauses == [1.0, 2.0]

    pauses.clear()
    monkeypatch.setattr(check_published_site, "fetch_once", lambda _url, **_kwargs: (403, b""))
    status = check_published_site.fetch(
        "https://example.org/", timeout=1, delays=(1.0, 2.0), sleep=pauses.append
    )
    assert status == (403, b"")
    assert pauses == [], "a refusal is an answer, not a deploy still settling"


def test_check_requires_a_forwarder_at_every_address_a_page_used_to_have(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A page that moved or was withdrawn is still served at its old address, as a
    forwarder naming where a visit goes now (`render_overview.MOVED_PAGES`): the three
    repository documents that left the site, the papers, which moved under `papers/`,
    and the one page of every case record, whose records moved under `cases/`. A deploy
    without one 404s every link written before the change. It fails when an old address
    is gone, when the page there still is the old page, and when a forwarder leads
    anywhere but where a visit should go, in any one of the four places it says where
    that is."""
    moved = dict(render_overview.MOVED_PAGES)
    assert set(moved) == {
        "results.html",
        "status.html",
        "defects.html",
        "explainer.html",
        "n11-optimality/t-060-explainer.html",
        "n11-optimality/index.html",
        "cases.html",
    }
    assert not set(moved) & set(render_overview.SITE_PAGES)
    requested: list[str] = []
    assert failures(monkeypatch, fake_site(site_pages(), requested=requested)) == []
    for old in moved:
        assert f"https://example.org/{old}" in requested, old

    for old, new in moved.items():
        # The slash keeps `results.html` from also losing `all-results.html`.
        (failure,) = failures(monkeypatch, fake_site(site_pages(), lost=(f"/{old}",)))
        assert failure.startswith(f"forwarder {old}: HTTP 404, says "), failure

        # The page that was there before, still served in place of its forwarder.
        stale = site_pages(**{old: explainer_page()})
        (failure,) = failures(monkeypatch, fake_site(stale))
        assert failure.startswith(f"forwarder {old}: HTTP 200, says "), failure
        assert "'script': None" in failure, "an old page is not a forwarder"

        good = site_pages()[old]
        expected = check_published_site.forwarder_expected(old, new)
        target, canonical = expected["script"], expected["canonical"]
        file_target = expected["file"]
        assert target is not None
        assert canonical is not None
        assert file_target is not None
        elsewhere = (file_target + "-elsewhere").encode()
        wrong = {
            "canonical": good.replace(
                b'rel="canonical" href="' + canonical.encode(),
                b'rel="canonical" href="https://example.org/',
            ),
            "script": good.replace(b'data-moved-to="' + target.encode(), b'data-moved="'),
            "file": good.replace(
                b'data-file-moved-to="' + file_target.encode(), b'data-file-moved="'
            ),
            "refresh": good.replace(b"0; url=" + file_target.encode(), b"0; url=" + elsewhere),
            "link": good.replace(b'<a href="' + file_target.encode(), b'<a href="' + elsewhere),
        }
        for place, body in wrong.items():
            assert body != good, place
            (failure,) = failures(monkeypatch, fake_site(site_pages(**{old: body})))
            assert failure.startswith(f"forwarder {old}: HTTP 200, says "), (place, failure)
            says = check_published_site.forwarder_says(body.decode())
            assert {name for name in says if says[name] != expected[name]} == {place}

    # A page of the site is named relative to the old address, climbing out of its
    # directory; a page that left the site is named whole.
    says = check_published_site.forwarder_says(
        site_pages()["n11-optimality/index.html"].decode()
    )
    assert says["script"] == "../papers/n11-optimality-review.html"
    says = check_published_site.forwarder_says(site_pages()["defects.html"].decode())
    assert says["script"] == says["canonical"] == f"{REPO_URL}/blob/{DEFAULT_BRANCH}/defects.md"


def test_check_requires_each_moved_file_at_its_old_address_with_the_same_bytes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A paper's Markdown and PDF cannot forward, so each old address serves a copy of
    the file (`render_overview.MOVED_FILES`): a deploy fails when the old address is
    gone and when it serves anything but the bytes the new one serves."""
    moved = dict(render_overview.MOVED_FILES)
    assert set(moved) == {
        "t-018-explainer.md",
        "t-018-explainer.pdf",
        "n11-optimality/t-060-explainer.md",
        "n11-optimality/t-060-explainer.pdf",
    }
    requested: list[str] = []
    assert failures(monkeypatch, fake_site(site_pages(), requested=requested)) == []
    for old, new in moved.items():
        assert f"https://example.org/{old}" in requested, old
        assert f"https://example.org/{new}" in requested, new

        (failure,) = failures(monkeypatch, fake_site(site_pages(), lost=(f"/{old}",)))
        assert failure.startswith(f"moved file {old}: HTTP 404, "), failure
        assert f"not the bytes of {new}" in failure

    for old in ("t-018-explainer.md", "n11-optimality/t-060-explainer.md"):
        stale = site_pages(**{old: b"the edition before the move\n"})
        (failure,) = failures(monkeypatch, fake_site(stale))
        assert failure.startswith(f"moved file {old}: HTTP 200, "), failure
        assert f"not the bytes of {moved[old]}" in failure


def test_check_visits_the_forwarders_only_with_a_browser(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Whether a forwarder forwards is the browser's to say, so with a browser the check
    visits each old address and reports where it arrived; `tests/test_site_forwarders.py`
    runs that visit for real."""
    monkeypatch.setattr(
        check_published_site, "workbench_startup", lambda _url, _root, **_: (True, "ok")
    )
    visited: list[str] = []

    def followed(site: str, *, timeout: float) -> list[tuple[bool, str]]:
        visited.append(site)
        return [(False, f"visiting {site}explainer.html arrives nowhere in {timeout}s")]

    monkeypatch.setattr(check_published_site, "forwarders_followed", followed)
    assert failures(monkeypatch, fake_site(site_pages())) == []
    assert visited == []
    assert failures(monkeypatch, fake_site(site_pages()), browser=True) == [
        "visiting https://example.org/explainer.html arrives nowhere in 1s"
    ]
    assert visited == ["https://example.org/"]
    assert check_published_site.visited_address("n11-optimality/index.html") == (
        "n11-optimality/"
    )
    assert check_published_site.visited_address("explainer.html") == "explainer.html"


def test_a_site_served_on_this_machine_may_be_asked_and_no_other_plain_http_one() -> None:
    """The check runs on a build before it is deployed, served locally as
    `preview_site --serve` serves one; any other address has to be https."""
    local = check_published_site.LOCAL_SITE
    for url in (
        "http://127.0.0.1:8765/",
        "http://localhost:8765/papers.html",
        "http://127.0.0.1/",
    ):
        assert local.match(url), url
    for url in (
        "http://example.org/",
        "http://127.0.0.1.example.org/",
        "http://localhost.example.org:8765/",
        "ftp://127.0.0.1/",
        "file:///tmp/site/index.html",
    ):
        assert not local.match(url), url
        with pytest.raises(ValueError, match="neither https nor local"):
            check_published_site.fetch_once(url)
    # Nothing listens on port 9: a local address is asked, and answers unreachable.
    assert check_published_site.fetch_once("http://127.0.0.1:9/", timeout=2) == (0, b"")


def test_check_holds_every_page_to_its_head_and_the_site_to_its_card(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Every page that can be shared is read for what it says of itself: the site's
    pages, the explainer, the optimality paper and the workbench, each at the address it
    is served at, and the sampled case records, in one line. The forwarders, the paper's
    landing address among them, are read by their rule: a preview of the page each leads
    to, or, for the one that leads off the site, a canonical link and no card. The card is
    fetched from the site under test. A good deploy passes, and the head checks cost one
    request, the card's: the pages are read from the text already fetched."""
    requested: list[str] = []
    fetch = fake_site(site_pages(), requested=requested)
    assert failures(monkeypatch, fetch, heads=True) == []
    assert requested.count(f"https://example.org/{render_overview.SOCIAL_CARD}") == 1
    landing = "n11-optimality/index.html"
    for name in (*SITE_PAGES[1:], EXPLAINER, *REVIEW_PAPERS, landing):
        assert requested.count(f"https://example.org/{name}") == 1, name

    monkeypatch.setattr(check_published_site, "fetch", fetch)
    # These fixtures test specialized assurance; the complete walk has its own fixtures.
    monkeypatch.setattr(
        check_published_site, "deployed_registry_checks", lambda *_args, **_kwargs: []
    )
    monkeypatch.setattr(check_published_site, "head_checks", HEAD_CHECKS)
    lines = [
        line
        for _, line in check_published_site.check(
            "https://example.org", COMMIT, timeout=1, browser=False
        )
    ]
    clean = "one of each identity and card tag, agreeing with its address"
    shared = check_published_site.shared_pages()
    assert shared == (*SITE_PAGES, EXPLAINER, *REVIEW_PAPERS, "workbench/index.html")
    assert REVIEW_PAPERS == (
        "papers/n11-threshold-bound-review.html",
        "papers/n11-optimality-review.html",
    )
    # The record files the check samples are pages a reader shares too.
    records = [
        render_case_pages.case_url(n)
        for n in sorted({1, check_published_site.RECORD_FILE_SAMPLE, CASE_COUNT})
    ]
    for name in shared:
        assert f"{name}: {clean}" in lines, name
    assert f"case records: each of {len(records)} carries {clean}" in lines
    pages = len(shared) + len(records)
    assert f"each of {pages} pages has a description of its own" in lines
    # The address the paper's directory had is one of the renderer's forwarders now.
    assert dict(render_overview.MOVED_PAGES)[landing] == OPTIMALITY_PAPER
    paper_url = render_overview.canonical_url(OPTIMALITY_PAPER)
    assert paper_url == f"{render_overview.SITE_URL}papers/n11-optimality-review.html"
    assert f"forwarder {landing}: previews {paper_url} as that page's own head does" in lines
    defects = dict(render_overview.MOVED_PAGES)["defects.html"]
    assert f"forwarder defects.html: names {defects} as canonical, and carries no card" in lines
    verbs = ("names", "previews")
    for forwarder in render_overview.forwarder_pages():
        starts = tuple(f"forwarder {forwarder.name}: {verb} " for verb in verbs)
        assert any(line.startswith(starts) for line in lines), forwarder.name
    assert f"card {render_overview.SOCIAL_CARD}: a PNG of 1200x630, 29 bytes" in lines


def test_check_fails_a_page_whose_head_is_not_the_sites(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The heads as they were before the site wrote them from one definition: the
    optimality paper and the workbench with a title and no card, a page with the site's
    name after its preview's title and no image, two pages saying one thing."""

    def found(**overrides: bytes) -> list[str]:
        return failures(monkeypatch, fake_site(site_pages(**overrides)), heads=True)

    # A head with a title and a description and nothing else of the set, as the paper's
    # was: every other tag is named as missing.
    bare = '<html lang="en"><head><title>A Review</title><meta name="description" content="A.">'
    body = (
        f"</head>{PAPERS_CURRENT}Papers</a><p>({OPTIMALITY_REVIEW_EDITION})</p>"
        f'<a href="{REPO_URL}/blob/{COMMIT}/README.md">R</a>'
    )
    (failure,) = found(**{OPTIMALITY_PAPER: (bare + body).encode()})
    assert failure.startswith(
        f"{OPTIMALITY_PAPER}: head: 0 canonical links, not one; 0 og:type"
    )
    assert "the title 'A Review' does not end in ' · The Squares Project'" in failure
    assert "0 canonical links, not one" in failure
    assert "0 og:image tags, not one" in failure
    assert "0 twitter:card tags, not one" in failure

    old = page(render_overview.canonical_url("papers.html")).replace(
        b'og:title" content="Page papers.html',
        b'og:title" content="Papers \xc2\xb7 Square Packing',
    )
    (failure,) = found(**{"papers.html": old})
    assert failure.startswith("papers.html: head: og:title is 'Papers · Square Packing', not")

    said = "The site-wide sentence, on every page."
    same = {
        name: (head(name, description=said) + f"<p>({PUBLICATION_EDITION})</p>").encode()
        for name in ("papers.html", "visualize.html")
    }
    (failure,) = found(**same)
    assert (
        failure == f"descriptions shared between pages: papers.html, visualize.html: {said!r}"
    )


#: Where each forwarder to a page of the site leads, as an address in full.
FORWARDED_URLS = {
    old: render_overview.canonical_url(new)
    for old, new in render_overview.MOVED_PAGES
    if not new.startswith("https://")
}


def test_check_fails_a_forwarder_that_previews_its_page_by_another_name_or_kind(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A forwarder's preview is held to the head the deploy serves at the address it leads
    to. The old address of the frontier atlas previewing it by a name the page no longer
    has, and the explainer's previewing it as a website, as both did, each fail, though
    each forwarder's own set is whole."""
    forwarders = {moved.name: moved.html for moved in render_overview.forwarder_pages()}

    def found(name: str, text: str) -> list[str]:
        assert (
            check_published_site.head_problems(
                text, FORWARDED_URLS[name], page_url=render_overview.SITE_URL + name
            )
            == []
        )
        site = fake_site(site_pages(**{name: text.encode()}))
        return failures(monkeypatch, site, heads=True)

    renamed = forwarders["status.html"].replace("The Frontier Survey", "The Frontier Atlas")
    (failure,) = found("status.html", renamed)
    assert failure == (
        "forwarder status.html: head: its og:title is ['The Frontier Atlas'], and the page's "
        "own is ['The Frontier Survey']"
    )
    dated = re.compile(r'<meta property="article:\w+" content="[^"]*">\n')
    website = dated.sub("", forwarders["explainer.html"]).replace(
        'og:type" content="article"', 'og:type" content="website"'
    )
    (failure,) = found("explainer.html", website)
    assert failure == (
        "forwarder explainer.html: head: its og:type is ['website'], and the page's own is "
        "['article']"
    )


def test_check_fails_a_card_that_is_missing_or_not_the_declared_size(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Every page names one image, so one missing file is a blank preview on every page,
    and one of another size is a preview that reflows or is dropped."""
    name = render_overview.SOCIAL_CARD
    (failure,) = failures(monkeypatch, fake_site(site_pages(), lost=(name,)), heads=True)
    assert failure == f"card {name}: not served"
    wrong = site_pages(**{name: card(2400, 1256)})
    (failure,) = failures(monkeypatch, fake_site(wrong), heads=True)
    assert failure == f"card {name}: it is 2400x1256, and every page declares 1200x630"
    (failure,) = failures(monkeypatch, fake_site(site_pages(**{name: b"<html>"})), heads=True)
    assert failure == f"card {name}: it is not a PNG"


def test_check_fails_a_forwarder_whose_canonical_link_is_not_its_targets_address(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The paper's landing address once named the paper by its file name alone, which a
    crawler has no base to resolve; a forwarder names its target's address in full. A
    relative one fails twice: where the forwarder says it sends a visit is not the address
    it should name, and its preview's canonical link is not the page it leads to."""
    name = "n11-optimality/index.html"
    landing = site_pages()[name].decode()
    target = render_overview.canonical_url(OPTIMALITY_PAPER)
    assert f'<link rel="canonical" href="{target}">' in landing
    relative = landing.replace(
        f'rel="canonical" href="{target}"',
        'rel="canonical" href="../papers/n11-optimality-review.html"',
    ).encode()
    says, heads = failures(monkeypatch, fake_site(site_pages(**{name: relative})), heads=True)
    assert says.startswith(f"forwarder {name}: HTTP 200, says ")
    assert heads.startswith(
        f"forwarder {name}: head: the canonical link is '../papers/n11-optimality-review"
    )
