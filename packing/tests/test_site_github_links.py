"""GitHub link marks work without script and on inert fetched article clones."""

from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from devtools import preview_site, render_overview
from devtools.site_github_links import decorate_github_links
from devtools.site_icons import account_icon, github_link_css, github_reference_icon
from sqpack.probes import probe
from tests import site_browser

pytest_plugins = ["tests.test_site_popover_controls"]

LAYOUT = probe(Path(__file__).with_name("probes"), "github_links/layout")


@pytest.fixture(scope="module")
def github_site(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    links = [
        ("repo", "https://github.com/owner/repo", "owner/repo"),
        ("doc", "https://github.com/owner/repo/blob/main/README.md", "Source document"),
        (
            "nested-doc",
            "https://github.com/owner/repo/blob/main/issues/1.md",
            "Archived issue notes",
        ),
        ("issue", "https://github.com/owner/repo/issues/12#issuecomment-9", "Issue #12"),
        ("pull", "https://github.com/owner/repo/pull/34", "Pull request #34"),
        ("account", "https://github.com/owner", "@owner"),
        ("query", "https://github.com/owner/repo?next=/issues/7", "Repository query"),
        ("owner-issues", "https://github.com/issues/project", "issues/project"),
        ("owner-pull", "https://github.com/pull/project", "pull/project"),
        ("other", "https://example.com/owner/repo/issues/12", "Unrelated issue"),
        ("lookalike", "https://github.com.example.com/owner/repo/pull/34", "Unrelated host"),
    ]
    body = "<h1>GitHub link marks</h1>" + "".join(
        f'<p><a id="{key}" href="{href}">{label}</a></p>' for key, href, label in links
    )
    body += (
        '<p><a id="existing-svg" href="https://github.com/owner/repo">'
        + account_icon("github")
        + 'Existing repository</a></p><p><a id="existing-issue" '
        'href="https://github.com/owner/repo/issues/12">'
        + github_reference_icon("issue")
        + 'Existing issue</a></p><p><a id="existing-img" href="https://github.com/owner/repo">'
        '<img alt="Repository" src="data:image/gif;base64,'
        'R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==">'
        '</a></p><p><a id="existing-card" class="site-card" '
        'href="https://github.com/owner/repo">Existing card</a></p>'
        '<p style="max-width: 9em"><a id="multiline" '
        'href="https://github.com/owner/repo/blob/main/README.md">'
        "A source document with a long descriptive title that wraps across lines</a></p>"
        '<p><a id="math" href="https://github.com/owner/repo/blob/main/proof.md">'
        "<math><msqrt><mn>2</mn></msqrt></math> proof</a></p>"
        '<div class="site-row-pop"><div class="site-detail"><p class="site-records">'
        '<a id="record-first" href="https://github.com/owner/repo/blob/main/a.md">First</a>'
        '<a id="record-next" href="https://github.com/owner/repo/blob/main/b.md">Second</a>'
        "</p></div></div>"
    )
    page = render_overview.kpress_page(
        body,
        name="index.html",
        title="GitHub links",
        description="Link marks.",
        current="",
        toc=False,
    )
    root = tmp_path_factory.mktemp("github-links")
    render_overview.write_site(root, [page])
    server = preview_site.serve(root, 0)
    try:
        yield f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()
        server.server_close()


def test_shared_css_embeds_the_canonical_glyphs_once() -> None:
    css = github_link_css()
    assert "__SITE_GITHUB_" not in css
    assert css.count("data:image/svg+xml;base64,") == 3


@pytest.mark.parametrize("javascript", [False, True])
@pytest.mark.parametrize("width", [390, 1280])
def test_static_github_link_marks_preserve_labels_and_existing_icons(
    browser: Any,
    github_site: str,
    *,
    javascript: bool,
    width: int,
) -> None:
    context = browser.new_context(
        java_script_enabled=javascript, viewport={"width": width, "height": 900}
    )
    page = context.new_page()
    try:
        page.goto(github_site)
        page.locator("#multiline").wait_for()
        marks = {item["id"]: item for item in page.locator("body").evaluate(LAYOUT)}
        for key in (
            "repo",
            "doc",
            "nested-doc",
            "issue",
            "pull",
            "account",
            "query",
            "owner-issues",
            "owner-pull",
            "multiline",
            "math",
            "record-first",
            "record-next",
        ):
            mark = marks[key]
            assert mark["mask"].startswith('url("data:image/svg+xml;base64,'), mark
            assert mark["width"] == mark["height"] > 0, mark
            assert mark["ink"] == mark["color"], mark
        assert marks["repo"]["mask"] == marks["doc"]["mask"] == marks["nested-doc"]["mask"]
        assert len({marks[key]["mask"] for key in ("repo", "issue", "pull")}) == 3
        for key in ("query", "owner-issues", "owner-pull"):
            assert marks[key]["mask"] == marks["repo"]["mask"], marks[key]
        for key in (
            "other",
            "lookalike",
            "existing-svg",
            "existing-issue",
            "existing-img",
            "existing-card",
        ):
            assert marks[key]["mask"] == "none", marks[key]
        assert marks["existing-svg"]["svgs"] == marks["existing-issue"]["svgs"] == 1
        assert marks["existing-img"]["images"] == 1
        assert marks["account"]["text"] == "@owner"
        assert marks["doc"]["text"] == "Source document"
        assert marks["issue"]["href"].endswith("#issuecomment-9")
        multiline = marks["multiline"]
        assert multiline["display"] == "inline", multiline
        assert multiline["lines"] > 1, multiline
        assert multiline["firstTextTop"] == pytest.approx(multiline["firstLineTop"], abs=1), (
            multiline
        )
        assert page.locator("#math math").count() == 1
        assert (
            page.locator("#record-first").evaluate(
                probe(Path(__file__).with_name("probes"), "github_links/separator")
            )
            == '"·"'
        )
        assert (
            page.locator("body").evaluate(
                probe(Path(__file__).with_name("probes"), "github_links/page_width")
            )
            <= width
        )
    finally:
        context.close()


def test_fetched_result_links_receive_the_same_mark_without_dom_rewriting(
    browser: Any,
    served: str,
) -> None:
    page = browser.new_page(viewport={"width": 390, "height": 900})
    try:
        page.goto(served)
        page.locator("#result-row").press("Enter")
        panel = page.locator("#pop-result")
        link = panel.locator(".github-dynamic-check")
        site_browser.api().expect(link).to_be_visible()
        marks = panel.evaluate(LAYOUT)
        source = next(mark for mark in marks if mark["text"] == "Source document")
        assert source["mask"].startswith('url("data:image/svg+xml;base64,'), source
        assert source["svgs"] == source["images"] == 0
        assert source["href"] == "https://github.com/owner/repo/blob/main/README.md"
    finally:
        page.close()


def test_exact_route_classification_is_idempotent_and_preserves_link_markup() -> None:
    markup = (
        '<p><a href="https://github.com/owner/repo/issues/7?x=1&amp;y=2">'
        "<code>Issue</code> &amp; proof</a>\n"
        '<a href="https://github.com/owner/repo/pull/9#discussion">PR</a>'
        '<a href="https://github.com/issues/project">issues/project</a>'
        '<a href="https://github.com/owner/repo?next=/issues/7">Repository</a></p>'
    )
    decorated = decorate_github_links(markup)
    assert decorated.count('data-site-github-kind="issue"') == 1
    assert decorated.count('data-site-github-kind="pull-request"') == 1
    assert (
        decorated.replace(' data-site-github-kind="issue"', "").replace(
            ' data-site-github-kind="pull-request"', ""
        )
        == markup
    )
    assert decorate_github_links(decorated) == decorated
