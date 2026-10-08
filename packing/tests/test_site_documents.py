"""The tutorial page: links rewritten for the site, and every one resolved."""

from __future__ import annotations

import posixpath
import re

import pytest

from devtools import render_overview, site_documents
from devtools.repo_links import RAW_URL, REPO_URL, RepositoryTree
from devtools.site_documents import (
    INTRO,
    INTRO_BEGIN,
    INTRO_END,
    OVERVIEW_INTRO_CLOSE,
    OVERVIEW_INTRO_OPEN,
    SHARED_BLOCKS,
    LinkContext,
    LinkReport,
    intro_block,
    rewrite_article,
    rewrite_link,
    rewrite_overview_blocks,
    shared_blocks,
    unresolved,
)
from tests import site_renders

#: Every repository link on the site names the default branch, never a commit.
BRANCH = "main"
TREE = RepositoryTree(
    files=frozenset(
        {"README.md", "SYNOPSIS.md", "conventions.md", "packing/atlas/n5.svg", "docs/a b.md"}
    ),
    directories=frozenset({"", "packing", "packing/atlas", "docs", "vendor/kpress"}),
    submodules={"vendor/kpress": ("https://github.com/jlevy/kpress", "1" * 40)},
)


def context(page: str = "tutorial.html", base: str = "") -> LinkContext:
    return LinkContext(page, TREE, base)


def rewrite(
    url: str, *, tag: str = "a", page: str = "tutorial.html", base: str = ""
) -> tuple[str, LinkReport]:
    report = LinkReport()
    return rewrite_link(url, tag=tag, context=context(page, base), report=report), report


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("README.md", "readme.html"),
        ("README.md#the-problem", "readme.html#the-problem"),
        ("conventions.md#4-evidence", "conventions.html#4-evidence"),
        ("./conventions.md", "conventions.html"),
        ("packing/atlas/", f"{REPO_URL}/tree/{BRANCH}/packing/atlas"),
        ("packing", f"{REPO_URL}/tree/{BRANCH}/packing"),
        ("docs/a%20b.md?plain=1#L3", f"{REPO_URL}/blob/{BRANCH}/docs/a%20b.md?plain=1#L3"),
        ("docs/a%20b.md", f"{REPO_URL}/blob/{BRANCH}/docs/a%20b.md"),
        ("SYNOPSIS.md#terminology", "synopsis.html#terminology"),
        (
            "vendor/kpress/docs/x.md",
            f"https://github.com/jlevy/kpress/blob/{'1' * 40}/docs/x.md",
        ),
        ("TUTORIAL.md#start", "#start"),
        ("TUTORIAL.md", "tutorial.html"),
        ("#local", "#local"),
        ("https://example.org/x.md", "https://example.org/x.md"),
        ("mailto:someone@example.org", "mailto:someone@example.org"),
    ],
)
def test_a_link_is_rewritten_for_the_site(url: str, expected: str) -> None:
    rewritten, report = rewrite(url)
    assert rewritten == expected
    assert not report.missing


def test_an_image_becomes_its_raw_file_on_main() -> None:
    rewritten, _ = rewrite("packing/atlas/n5.svg", tag="img")
    assert rewritten == f"{RAW_URL}/{BRANCH}/packing/atlas/n5.svg"


def test_anchors_into_the_documents_are_recorded_for_checking() -> None:
    _, report = rewrite("TUTORIAL.md#start", page="frontier.html")
    assert report.anchors == [("tutorial.html", "start", "TUTORIAL.md#start")]
    _, report = rewrite("conventions.md#4-evidence")
    assert report.anchors == [("conventions.html", "4-evidence", "conventions.md#4-evidence")]


def test_a_relative_link_resolves_from_the_documents_directory() -> None:
    rewritten, report = rewrite("../README.md", base="packing")
    assert rewritten == "readme.html"
    assert not report.missing
    rewritten, _ = rewrite("n5.svg", tag="img", base="packing/atlas")
    assert rewritten == f"{RAW_URL}/{BRANCH}/packing/atlas/n5.svg"


@pytest.mark.parametrize("url", ["missing.md", "packing/nowhere/", "../outside.md"])
def test_an_unresolved_target_is_reported(url: str) -> None:
    rewritten, report = rewrite(url)
    assert rewritten == url
    assert len(report.missing) == 1


def test_unresolved_lists_missing_paths_and_anchors() -> None:
    report = LinkReport(
        missing=["missing.md"], anchors=[("tutorial.html", "gone", "TUTORIAL.md#gone")]
    )
    page = render_overview.Page("tutorial.html", '<article><h2 id="here">x</h2></article>')
    problems = unresolved({"tutorial.html": page}, report)
    assert problems == [
        "no heading #gone in tutorial.html: TUTORIAL.md#gone",
        "no such path in the tree: missing.md",
    ]


def test_only_the_article_is_rewritten() -> None:
    page = (
        '<nav><a href="frontier.html">F</a></nav>'
        '<article><a href="docs/a%20b.md">c</a>'
        '<img src="packing/atlas/n5.svg" alt=""></article>'
        '<footer><a href="conventions.md">c</a></footer>'
    )
    out = rewrite_article(page, context=context(), report=LinkReport())
    assert '<a href="frontier.html">' in out
    assert f'href="{REPO_URL}/blob/{BRANCH}/docs/a%20b.md"' in out
    assert f'src="{RAW_URL}/{BRANCH}/packing/atlas/n5.svg"' in out
    assert '<footer><a href="conventions.md">' in out


#: A tree with the three generated views that are not pages, a case file and a document.
RECORD_TREE = RepositoryTree(
    files=frozenset(
        {
            "README.md",
            "defects.md",
            "packing/frontier/RESULTS.md",
            "packing/frontier/STATUS.md",
            "packing/frontier/n-011.md",
        }
    ),
    directories=frozenset({"", "packing", "packing/frontier"}),
)


def _record_context(base: str = "") -> LinkContext:
    """A reader document's context, as `render_document` builds one."""
    return LinkContext(
        "synopsis.html",
        RECORD_TREE,
        base,
        served=frozenset(render_overview.SITE_PAGES),
        aliases=site_documents.record_aliases(RECORD_TREE),
    )


@pytest.mark.parametrize(
    ("link", "base", "expected"),
    [
        # A result's id, plain or as code, is its row in the results table.
        ('<a href="packing/frontier/RESULTS.md">T-060</a>', "", "all-results.html#t-060"),
        (
            '<a href="packing/frontier/RESULTS.md"><code>T-017</code></a>',
            "",
            "all-results.html#t-017",
        ),
        (
            '<a href="RESULTS.md"><code>T-018</code></a>',
            "packing/frontier",
            "all-results.html#t-018",
        ),
        # Any other text is the page that shows what the register or the table holds.
        ('<a href="packing/frontier/RESULTS.md">results register</a>', "", "all-results.html"),
        ('<a href="packing/frontier/STATUS.md">status table</a>', "", "frontier.html"),
        ('<a href="STATUS.md">the status table</a>', "packing/frontier", "frontier.html"),
        # A code span naming the file is about the file, which is on `main`.
        (
            '<a href="packing/frontier/RESULTS.md"><code>frontier/RESULTS.md</code></a>',
            "",
            f"{REPO_URL}/blob/{BRANCH}/packing/frontier/RESULTS.md",
        ),
        (
            '<a href="packing/frontier/STATUS.md"><code>STATUS.md</code></a>',
            "",
            f"{REPO_URL}/blob/{BRANCH}/packing/frontier/STATUS.md",
        ),
        # The defect log is not a page: a citation of a defect opens the file on `main`.
        ('<a href="defects.md">D-029</a>', "", f"{REPO_URL}/blob/{BRANCH}/defects.md"),
        (
            '<a href="../../defects.md">D-344</a>',
            "packing/frontier",
            f"{REPO_URL}/blob/{BRANCH}/defects.md",
        ),
        # A case file is that case's record.
        ('<a href="packing/frontier/n-011.md"><code>n-011</code></a>', "", "cases/11.html"),
    ],
)
def test_a_link_to_a_record_reaches_the_page_that_shows_it(
    link: str, base: str, expected: str
) -> None:
    """`RESULTS.md`, `STATUS.md` and `defects.md` are not pages of the site. A link to
    the first two leads to the page built from the same record, and one to the defect
    log to the file; none leads to `results.html`, `status.html` or `defects.html`."""
    report = LinkReport()
    out = site_documents.rewrite_links(link, context=_record_context(base), report=report)
    assert re.findall(r'href="([^"]*)"', out) == [expected]
    assert not report.missing
    assert not report.anchors
    assert out.split(">", 1)[1] == link.split(">", 1)[1], "the link's text is kept"


def test_a_result_id_the_register_lacks_is_reported() -> None:
    """A row link is only as good as its row: an id that is not a registered result's
    fails the render, as a missing file does."""
    report = LinkReport()
    link = '<a href="packing/frontier/RESULTS.md">T-999</a>'
    out = site_documents.rewrite_links(link, context=_record_context(), report=report)
    assert "all-results.html#t-999" not in out
    assert report.missing == ["packing/frontier/RESULTS.md (no result T-999 in the register)"]


def test_the_documents_are_the_cards_in_their_order_and_three_views_are_not_pages() -> None:
    """The reader documents served as pages are the tutorial and the overview's five
    cards, README and `epistemics.md` first. The results register, the status table and
    the defect log are not among them: each old address is a forwarder."""
    from devtools import overview_sections, repo_links  # noqa: PLC0415

    by_page = {
        doc.name: doc.source.relative_to(site_documents.REPO).as_posix()
        for doc in site_documents.DOCUMENTS
    }
    assert list(by_page) == ["tutorial.html", *render_overview.DOCUMENT_PAGES]
    assert render_overview.DOCUMENT_PAGES == (
        "readme.html",
        "epistemics.html",
        "synopsis.html",
        "conventions.html",
        "development.html",
    )
    cards = [path for path, _, _ in overview_sections.DOCUMENTS]
    assert cards[:2] == [repo_links.README, repo_links.EPISTEMICS]
    # A card and its page are paired by position, so the two lists must agree.
    assert cards == [by_page[page] for page in render_overview.DOCUMENT_PAGES]
    moved = dict(render_overview.MOVED_PAGES)
    assert {"results.html", "status.html", "defects.html"} <= set(moved)
    assert not set(moved) & set(render_overview.SITE_PAGES)
    assert not set(moved) & set(render_overview.PAGES)
    for old in moved:
        assert not overview_sections.is_site_page(old), old


def test_a_forwarder_stands_at_each_address_a_page_used_to_have() -> None:
    """Each forwarder names where a visit goes in `data-moved-to`, which `forward.js`
    reads; it carries that script, a refresh for a reader without scripts, a link for
    anyone neither reaches, and the canonical address of the place it stands for."""
    forwarders = {page.name: page.html for page in render_overview.forwarder_pages()}
    assert list(forwarders) == [old for old, _ in render_overview.MOVED_PAGES]
    script = render_overview.FORWARD_SCRIPT.read_text(encoding="utf-8")
    for old, destination in render_overview.MOVED_PAGES:
        external = destination.startswith("https://")
        physical = (
            destination if external else posixpath.relpath(destination, posixpath.dirname(old))
        )
        target = "cases/" if old == "cases.html" else physical
        canonical = destination if external else render_overview.canonical_url(destination)
        page = forwarders[old]
        opening = re.search(r"<html\b[^>]*>", page)
        assert opening is not None, old
        assert 'lang="en"' in opening[0], old
        assert f'data-moved-to="{target}"' in opening[0], old
        assert f'data-file-moved-to="{physical}"' in opening[0], old
        assert (
            f'<noscript><meta http-equiv="refresh" content="0; url={physical}"></noscript>'
            in page
        )
        assert f'<a href="{physical}">' in page, old
        assert f'<link rel="canonical" href="{canonical}">' in page, old
        assert f"<script>{script}</script>" in page, old
        assert "{{" not in page, old
        render_overview.assert_fetches_only_assets(old, page)
    assert not set(forwarders) & set(render_overview.PAGES)


#: A link or a frame naming a page that moved, from the root or from a directory under it.
MOVED_LINK = re.compile(
    r'\s(?:href|src)="(?:\.\./)*(?:'
    + "|".join(re.escape(old) for old, _ in render_overview.MOVED_PAGES)
    + r')(?:[?#][^"]*)?"'
)


@pytest.fixture(scope="module")
def every_page() -> dict[str, str]:
    """Every page of the site, rendered once for the process (`site_renders`): the
    render is this fixture's setup, not a test's call time."""
    return site_renders.pages()


@pytest.fixture(scope="module")
def every_result_body() -> dict[str, str]:
    """Every result's overview, rendered once for the process."""
    return site_renders.result_bodies()


def test_no_page_of_the_site_links_a_page_that_moved(
    every_page: dict[str, str], every_result_body: dict[str, str]
) -> None:
    """A forwarder is for links written before the change. The site's own pages, the
    reader documents and every result's overview name the page a reader is going to."""
    assert MOVED_LINK.search(' href="results.html#next-actions"')
    assert MOVED_LINK.search(' src="../defects.html?view=embed"')
    assert not MOVED_LINK.search(' href="all-results.html#t-060"')
    for name, text in every_page.items():
        assert not MOVED_LINK.findall(text), name
    for result, body in every_result_body.items():
        assert not MOVED_LINK.findall(body), result


def test_the_build_fails_on_an_unresolved_link(monkeypatch: pytest.MonkeyPatch) -> None:
    """A broken link in a document stops the render and names the link."""
    original = site_documents.render_document

    def with_a_broken_link(document: site_documents.SiteDocument, **kwargs: object) -> object:
        report = kwargs["report"]
        assert isinstance(report, LinkReport)
        report.missing.append("no/such/file.md")
        return original(document, **kwargs)  # pyright: ignore[reportArgumentType]

    site_documents.site_documents.cache_clear()
    monkeypatch.setattr(site_documents, "render_document", with_a_broken_link)
    try:
        with pytest.raises(SystemExit, match=r"no such path in the tree: no/such/file\.md"):
            site_documents.site_documents()
    finally:
        site_documents.site_documents.cache_clear()


@pytest.fixture(scope="module")
def pages() -> dict[str, render_overview.Page]:
    return {name: site_renders.page(name) for name in ("tutorial.html",)}


def test_the_pages_render_self_contained_with_a_toc(
    pages: dict[str, render_overview.Page],
) -> None:
    for name, page in pages.items():
        render_overview.assert_fetches_only_assets(name, page.html)
        assert "data-kpress-toc" in page.html, name
        assert 'aria-current="page"' in page.html, name


def test_no_relative_repository_link_survives(pages: dict[str, render_overview.Page]) -> None:
    from devtools.render_case_pages import case_url  # noqa: PLC0415

    served = {"./", *render_overview.SITE_PAGES, *(case_url(n) for n in range(1, 325))}
    for name, page in pages.items():
        article = re.search(r"<article\b.*?</article>", page.html, re.DOTALL)
        assert article is not None
        for url in re.findall(r'\s(?:href|src)="([^"]*)"', article.group(0)):
            if url.startswith(("#", "https://", "http://", "data:", "mailto:")):
                continue
            assert url.split("#")[0] in served, f"{name}: {url}"


def test_the_tutorial_math_is_kpress_math(pages: dict[str, render_overview.Page]) -> None:
    """Each formula retains KPress semantics and a visual prepared before publication."""
    body = pages["tutorial.html"].html
    assert len(re.findall(r'data-kpress-math="inline"', body)) >= 14
    assert 'data-kpress-math-error="true">' not in body
    assert len(re.findall(r'data-kpress-math-rendered="true"', body)) >= 14
    assert len(re.findall(r'class="katex-html"', body)) >= 14


def test_long_reports_get_a_contents_rail_and_short_ones_do_not(
    pages: dict[str, render_overview.Page],
) -> None:
    """kpress's own length rule decides, so a short report keeps the one centred
    column and a long one adds the rail beside it."""
    short = "\n\n".join(f"## Part {i}\n\nA line of text." for i in range(3))

    def rail(markdown: str) -> bool:
        page = render_overview.kpress_page(
            markdown,
            name="short.html",
            current="papers",
            title="T",
            description="D",
            toc="auto",
        )
        return 'class="kpress-toc ' in page.html

    assert not rail(short)
    assert 'class="kpress-toc ' in pages["tutorial.html"].html


def test_a_hand_written_contents_list_is_dropped_from_the_page(
    pages: dict[str, render_overview.Page],
) -> None:
    """The tutorial's own Contents list, written for GitHub, is not on its page, where
    the contents rail lists the headings; the text around it stays."""
    markdown = "Intro.\n\n## Contents\n\n1. [One](#one)\n2. [Two](#two)\n\n## One\n\nBody.\n"
    assert site_documents.without_manual_contents(markdown) == "Intro.\n\n## One\n\nBody.\n"
    page = pages["tutorial.html"].html
    assert 'id="contents"' not in page
    assert 'href="#contents"' not in page


def _readme(body: str) -> str:
    """A README with the one shared block, then two unmarked paragraphs after it, as
    README's own account of recent progress stands since 2026-10-02."""
    return (
        f"# Title\n\n{INTRO_BEGIN}\n\n{body}\n\n{INTRO_END}\n\n"
        "What the project covers.\n\nA recent result, [T-060](packing/frontier/RESULTS.md).\n"
    )


def test_the_introduction_is_the_block_between_readmes_markers() -> None:
    body = "One paragraph about $s(n)$.\n\nA second, with [a link](packing/atlas/)."
    assert intro_block(_readme(body)) == body


def test_readmes_one_shared_block_is_read_by_name() -> None:
    """The shared text is one block between its own markers, what the project studies.
    What it covers with its newest result was a second block, `recent-progress`, until
    2026-10-02, and is README's own prose after the markers now: the overview's Recent
    Results says that in one paragraph of its own, and a shared block must read the same
    in both places."""
    readme = _readme("What the project studies.")
    assert shared_blocks(readme) == {"project-intro": "What the project studies."}
    assert SHARED_BLOCKS == (INTRO,)
    assert INTRO.name == "project-intro"
    assert (
        INTRO.begin
        == INTRO_BEGIN
        == ("<!-- BEGIN SHARED: project-intro (devtools.site_documents) -->")
    )
    assert INTRO.end == INTRO_END == "<!-- END SHARED: project-intro -->"
    assert (INTRO.opened, INTRO.closed) == (
        "<!-- README project-intro -->",
        "<!-- /README project-intro -->",
    )
    assert not hasattr(site_documents, "PROGRESS")
    assert not hasattr(site_documents, "progress_block")
    assert not hasattr(site_documents, "overview_progress")
    # Prose after the block, however it reads, is not the check's business.
    assert shared_blocks(
        _readme("Studies.").replace(
            "What the project covers.", "## Covers\n\nThe central case."
        )
    ) == {"project-intro": "Studies."}


@pytest.mark.parametrize(
    ("readme", "refusal"),
    [
        (
            "# Title\n\nStudies.\n",
            "the project-intro markers must each appear exactly once",
        ),
        (
            f"{INTRO_BEGIN}\n\nStudies.\n\n{INTRO_END}\n\n{INTRO_BEGIN}\n\nAgain.\n\n{INTRO_END}\n",
            "the project-intro markers must each appear exactly once",
        ),
        (
            f"{INTRO_END}\n\nStudies.\n\n{INTRO_BEGIN}\n",
            "the project-intro block ends before it begins",
        ),
        (_readme(""), "the project-intro block is empty"),
        (_readme("Studies.\n\n### Newest\n\nMore."), "a heading or a comment"),
        (
            _readme("Eleven squares is its central open case."),
            "the project-intro block calls a case the central one",
        ),
    ],
)
def test_a_malformed_shared_block_is_refused(readme: str, refusal: str) -> None:
    with pytest.raises(ValueError, match=refusal):
        shared_blocks(readme)


@pytest.mark.parametrize(
    ("readme", "refusal"),
    [
        ("# Title\n\nNo markers.\n", "exactly once"),
        (_readme("Prose.") + _readme("Prose again."), "exactly once"),
        (f"{INTRO_END}\n\nProse.\n\n{INTRO_BEGIN}\n", "ends before it begins"),
        (_readme(""), "is empty"),
        (_readme("Prose.\n\n## A Heading\n\nMore."), "a heading or a comment"),
        (_readme("Prose.\n\n<!-- a note -->"), "a heading or a comment"),
        # A block that runs on into the next one holds that block's marker, a comment.
        (
            # The end marker drifted past README's own prose and a later heading.
            _readme("Prose.").replace(f"{INTRO_END}\n", "") + f"\n## Later\n\n{INTRO_END}\n",
            "a heading or a comment",
        ),
        (_readme(f"See [the site]({render_overview.SITE_URL})."), "links the site"),
    ],
)
def test_a_malformed_introduction_block_is_refused(readme: str, refusal: str) -> None:
    with pytest.raises(ValueError, match=refusal):
        intro_block(readme)


#: A tree with what README's introduction links: the registers, a case file, a document
#: served as a page, and a review that is only in the repository.
INTRO_TREE = RepositoryTree(
    files=frozenset(
        {
            "packing/frontier/RESULTS.md",
            "packing/frontier/STATUS.md",
            "packing/frontier/n-011.md",
            "docs/review.md",
            "epistemics.md",
        }
    ),
    directories=frozenset({"", "docs", "packing", "packing/frontier"}),
)


def _overview(intro: str) -> str:
    """A rendered overview with the one shared block between its markers and the same
    repository link three times outside it: before, after, and where README's
    `recent-progress` block stood until 2026-10-02."""
    outside = '<p><a href="packing/frontier/RESULTS.md">outside the block</a></p>'
    return f"{outside}{OVERVIEW_INTRO_OPEN}{intro}{OVERVIEW_INTRO_CLOSE}{outside}{outside}"


def test_the_introductions_links_reach_the_sites_own_pages(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A result's id goes to its row, the registers to the results table and the
    frontier atlas, a case file to its record, a served document to its page, and any
    other path to `main`; nothing outside the block is touched."""
    monkeypatch.setattr(site_documents, "repository_tree", lambda: INTRO_TREE)
    out = rewrite_overview_blocks(
        _overview(
            '<p><a href="packing/frontier/RESULTS.md">T-060</a> '
            '<a href="packing/frontier/RESULTS.md">results register</a> '
            '<a href="packing/frontier/STATUS.md">frontier</a> '
            '<a href="packing/frontier/n-011.md">case record</a> '
            '<a href="epistemics.md">the rungs</a> '
            '<a href="docs/review.md">review</a> '
            '<a href="https://example.org/proof">the proof</a></p>'
        )
    )
    intro = out.split(OVERVIEW_INTRO_OPEN, 1)[1].split(OVERVIEW_INTRO_CLOSE, 1)[0]
    assert re.findall(r'<a href="([^"]+)">([^<]+)</a>', intro) == [
        ("all-results.html#t-060", "T-060"),
        ("all-results.html", "results register"),
        ("frontier.html", "frontier"),
        ("cases/11.html", "case record"),
        ("epistemics.html", "the rungs"),
        (f"{REPO_URL}/blob/{BRANCH}/docs/review.md", "review"),
        ("https://example.org/proof", "the proof"),
    ]
    assert out.count('<a href="packing/frontier/RESULTS.md">outside the block</a>') == 3


def test_only_the_shared_block_has_its_links_rewritten(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """What lies outside the block, where README's second block stood included, is left
    as it was: a repository path in the overview's own prose is the template's business,
    written as a site link there."""
    monkeypatch.setattr(site_documents, "repository_tree", lambda: INTRO_TREE)
    out = rewrite_overview_blocks(
        _overview('<p><a href="packing/frontier/STATUS.md">frontier</a></p>')
    )
    intro = out.split(OVERVIEW_INTRO_OPEN, 1)[1].split(OVERVIEW_INTRO_CLOSE, 1)[0]
    assert intro == '<p><a href="frontier.html">frontier</a></p>'
    assert out.count('<a href="packing/frontier/RESULTS.md">outside the block</a>') == 3
    assert "recent-progress" not in out


def test_the_overview_fails_on_an_unresolved_introduction_link(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(site_documents, "repository_tree", lambda: INTRO_TREE)
    with pytest.raises(SystemExit, match="1 unresolved links in README's introduction"):
        rewrite_overview_blocks(_overview('<p><a href="docs/gone.md">gone</a></p>'))
    with pytest.raises(SystemExit, match="project-intro block is not marked in the page"):
        rewrite_overview_blocks('<p><a href="docs/review.md">no markers</a></p>')
    # A page that still marks the block README no longer shares is not refused: the
    # markers are comments kpress passes through, and nothing is rewritten inside them.
    stale = (
        f"{OVERVIEW_INTRO_OPEN}<p>Fine.</p>{OVERVIEW_INTRO_CLOSE}"
        '<!-- README recent-progress --><p><a href="docs/gone.md">gone</a></p>'
        "<!-- /README recent-progress -->"
    )
    assert rewrite_overview_blocks(stale) == stale
