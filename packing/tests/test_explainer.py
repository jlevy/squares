"""The explainer renders, and what it renders fetches nothing.

`devtools.render_explainer` was exercised only by the Pages workflow, on the pull
requests whose paths its filters name; nothing in the suite rendered the page. A full
render is under a second, so it runs here, and the two properties the workflow used to
grep for are asserted on the string the renderer returns: no placeholder survived
substitution, and nothing in the page is a reference outside it.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from devtools.render_explainer import (
    CARD_ALT,
    CASE,
    COMPOSITE_ALT,
    COMPOSITE_ASSETS,
    COMPOSITE_CARD,
    COMPOSITE_PNG,
    MARKDOWN_OUTPUT,
    RENDER_INPUTS,
    REPO,
    RESULT_ID,
    SITE_URL,
    WALKTHROUGH,
    assert_self_contained,
    png_size,
    render,
)
from devtools.render_explainer import load_certificate as load
from sqpack.yamlio import safe_load


@pytest.fixture(scope="module")
def rendered():
    return render(WALKTHROUGH)


@pytest.fixture(scope="module")
def page(rendered) -> str:
    return rendered.page


@pytest.fixture(scope="module")
def document(rendered) -> str:
    return rendered.markdown


def test_the_page_renders_every_walkthrough_certificate(page: str) -> None:
    """Each certificate's slug is in the page: its switch button and its figure copies."""

    for path in WALKTHROUGH:
        certificate, _ = load(path)
        fragment = f"{certificate.outer_side.numerator}-{certificate.outer_side.denominator}"
        assert f'data-cert="{fragment}"' in page, fragment


def test_no_placeholder_survives_substitution(page: str) -> None:
    assert re.findall(r"\{\{[A-Z_]+\}\}", page) == []


def test_the_page_is_self_contained(page: str) -> None:
    """The renderer's own check passes on its own output; the workflow relies on this.

    The page carries exactly one `<link>`, and it is the canonical URL. That is not a
    fetch -- a browser reads it and does not request it -- but it is the one element in
    the head that could become one, so it is counted rather than merely permitted: a
    second `<link>` arriving here is a stylesheet, an icon or a preload, and the count
    fails before the refusal has to.
    """

    assert_self_contained(page)
    assert re.findall(r"<link[^>]*>", page) == [f'<link rel="canonical" href="{SITE_URL}">']
    assert re.search(r"<script[^>]*\ssrc=", page) is None


@pytest.mark.parametrize(
    "fragment",
    [
        '<script src="https://cdn.example/x.js"></script>',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=X">',
        "<style>@import url(https://example.org/a.css);</style>",
        "<style>body { background: url(https://example.org/a.png) }</style>",
        "<style>body { background: url('//example.org/a.png') }</style>",
        # The canonical exemption is the exact quoted form the shell emits and nothing
        # wider: every other rel is still a fetch, and a rel that merely contains the
        # word does not buy its way past.
        '<link rel="preload" as="font" href="https://example.org/a.woff2">',
        '<link rel="icon" href="https://example.org/favicon.png">',
        '<link rel="canonical stylesheet" href="https://example.org/a.css">',
        "<link rel=canonical href=https://example.org/>",
    ],
)
def test_an_external_reference_is_refused(fragment: str) -> None:
    with pytest.raises(SystemExit, match="not self-contained"):
        assert_self_contained(f"<html><body>{fragment}</body></html>")


@pytest.mark.parametrize(
    "fragment",
    [
        "<style>@font-face { src: url(data:font/woff2;base64,AAAA) }</style>",
        "<style>.a { fill: url(#gradient) }</style>",
        '<style>.b { background: url("data:image/svg+xml,%3Csvg%3E") }</style>',
        # Metadata for a crawler, read off the markup and never requested to display
        # the page. Both forms are outward addresses on purpose: a preview consumer
        # resolves them on its own machine and drops a relative one.
        '<link rel="canonical" href="https://jlevy.github.io/squares/">',
        '<meta property="og:image" content="https://jlevy.github.io/squares/a.png">',
    ],
)
def test_a_data_uri_or_fragment_is_not_a_fetch(fragment: str) -> None:
    assert_self_contained(f"<html><body>{fragment}</body></html>")


def test_the_published_document_is_markdown_and_not_the_template(document: str) -> None:
    """The chip offers this file, so it has to be the article rather than its source.

    The template states no bound: every number in it is a `{{PLACEHOLDER}}`, and the
    chip used to link to it. What is published is the same document with the
    certificate's own values in place, and it has to survive being read as text.
    """
    assert "{{" not in document
    assert "3.81" in document
    assert "1,121" in document
    assert "181" in document
    assert document.startswith("# s(11)")


def test_the_published_document_carries_no_html(document: str) -> None:
    """A canvas, a control panel and a drawn diagram are apparatus, not prose.

    None of them means anything in a text file, and together they were seventy per cent
    of the bytes. What a figure says is in its caption, so a figure here is its caption.
    """
    assert not re.search(r"</?[a-zA-Z][^>]*>", document)
    for number in (1, 3):
        assert f"**Figure {number}." in document


def test_the_published_document_states_each_figure_once(document: str) -> None:
    """The page carries a copy per certificate and switches between them; text cannot.

    Stating the same figure twice, once per certificate, reads as a duplication rather
    than as a choice, so only the certificate the page opens on is kept.
    """
    # A caption's bold lead carries the figure's own subtitle, so it is matched by
    # its number rather than by an exact string.
    for number in range(1, 8):
        assert document.count(f"**Figure {number}.") == 1, number


def test_the_published_document_sets_mathematics_without_typesetting_kerns(
    document: str,
) -> None:
    """`\\mkern1mu` is how KaTeX is told not to set `s` against `(`, and nothing more.

    It is a fact about typesetting, not about the mathematics, and a reader or a model
    taking this file should see `s(11)`.
    """
    assert "mkern" not in document
    assert "$s(11)$" in document or "s(11)" in document


#: Every `og:` and `twitter:` tag in the head, by name. Both vocabularies spell a tag
#: the same way and differ only in the attribute that carries the name -- Open Graph is
#: `property`, the Twitter tags are `name` -- so one pattern reads them together.
CARD_TAG = re.compile(r'<meta (?:property|name)="((?:og|twitter):[^"]+)" content="([^"]*)"')

#: What a card is: the tags without which a consumer shows something worse than the
#: page asked for. `og:image:type` is deliberately not here -- it is a hint, and a
#: consumer that ignores it still renders the card.
REQUIRED_CARD_TAGS = frozenset(
    {
        "og:type",
        "og:site_name",
        "og:title",
        "og:description",
        "og:url",
        "og:image",
        "og:image:width",
        "og:image:height",
        "og:image:alt",
        "twitter:card",
        "twitter:title",
        "twitter:description",
        "twitter:image",
        "twitter:image:alt",
    }
)


def card_tags(page: str) -> dict[str, str]:
    return dict(CARD_TAG.findall(page))


def test_the_link_preview_is_complete_and_its_urls_are_absolute(page: str) -> None:
    """A shared link previews with the atlas, or it previews with nothing.

    The page shipped with four `<meta>` tags, a title and a description and no card at
    all, so every unfurl of it -- X, Slack, Discord, Facebook, iMessage -- was a line of
    text on a blank rectangle. What makes a card is the set together rather than any one
    tag: a consumer that finds `og:image` and no `twitter:card` falls back to a
    thumbnail, and one that finds a relative `og:image` drops the image outright,
    because a crawler resolves it on its own machine and has no base to resolve
    against. Both are pinned here, since neither failure shows up in the page itself:
    a card is only ever seen somewhere else.
    """
    tags = card_tags(page)
    assert tags.keys() >= REQUIRED_CARD_TAGS, sorted(REQUIRED_CARD_TAGS - tags.keys())
    for key in ("og:url", "og:image", "twitter:image"):
        assert tags[key].startswith("https://"), (key, tags[key])
    assert f'<link rel="canonical" href="{SITE_URL}">' in page
    assert tags["og:url"] == SITE_URL


def test_the_card_image_is_one_the_render_serves_beside_the_page(page: str) -> None:
    """The card names a file the deploy actually publishes, at the size it actually is.

    Two ways a card breaks without the page changing at all. The image URL can name
    something the render does not copy into the site directory, which is a 404 a
    consumer answers by showing no image; and the declared width and height can drift
    from the file, which reflows the preview or loses it. So the URL is checked against
    the assets the render copies, and the dimensions against the PNG's own header --
    the same bytes that get served -- rather than against numbers typed here.
    """
    tags = card_tags(page)
    served = {asset.name for asset in COMPOSITE_ASSETS}
    assert tags["og:image"] == SITE_URL + COMPOSITE_CARD.name
    assert tags["og:image"].rsplit("/", 1)[-1] in served
    assert tags["twitter:image"] == tags["og:image"]
    width, height = png_size(COMPOSITE_CARD)
    assert (tags["og:image:width"], tags["og:image:height"]) == (str(width), str(height))
    assert max(width, height) <= 4096


def test_the_card_image_is_the_landscape_crop_and_not_the_portrait_canvas() -> None:
    """A portrait card is cropped by the platform, and it crops away the title.

    X and Facebook show a landscape card and take a band from the middle of whatever
    they are handed, so the full 150:181 canvas arrives as four rows out of the middle
    of the grid with the title, the date and the repository line gone. The atlas builder
    writes the top of the same drawing at 1.91:1 instead, which is the ratio those
    platforms want, so they crop nothing.

    What is pinned is the property rather than the number: landscape, and within a
    pixel of the ratio the croppers use. A future canvas can change the crop height as
    long as the card stays a card.
    """
    width, height = png_size(COMPOSITE_CARD)
    assert width > height, "a card cropped by the platform is a card without its title"
    assert abs(width / height - 1.91) < 0.01, (width, height, width / height)
    # The crop is of the composite, not a second drawing: same width, less height.
    full_width, full_height = png_size(COMPOSITE_PNG)
    assert width == full_width
    assert height < full_height


def test_the_card_alt_describes_the_crop_and_not_the_whole_atlas() -> None:
    """The alt text is read by the readers least able to check it against the picture.

    Figure 1 shows all hundred packings and the card shows the first forty, so one
    sentence cannot be true of both. They were the same string until the card became a
    crop, which is exactly the kind of change that leaves an alt text quietly wrong.
    """
    assert CARD_ALT != COMPOSITE_ALT
    assert "one hundred" in COMPOSITE_ALT
    assert "one hundred" not in CARD_ALT
    assert "forty" in CARD_ALT


def test_the_card_and_the_page_say_the_same_thing(page: str) -> None:
    """A preview that disagrees with the page it opens is worse than no preview.

    The title and the sentence are built once in the renderer and substituted into
    `<title>`, `<meta name="description">` and both card vocabularies, so there is one
    string and not four. This is what would catch a later edit that retyped one of them
    in the template instead.
    """
    tags = card_tags(page)
    title = re.search(r"<title>(.*?)</title>", page)
    assert title is not None
    described = re.search(r'<meta name="description" content="([^"]*)"', page)
    assert described is not None
    assert tags["og:title"] == tags["twitter:title"] == title.group(1)
    assert tags["og:description"] == tags["twitter:description"] == described.group(1)
    assert tags["og:image:alt"] == tags["twitter:image:alt"]
    # The bound is the certificate's, wherever it is stated.
    for text in (title.group(1), described.group(1)):
        assert "s(11) ≥ 381/100" in text


def test_the_published_document_is_named_for_the_result(document: str) -> None:
    """`conventions.md` names a document for the result and for what it is.

    It was `explainer.md`, which says what the file is and not which result it explains;
    the convention is `t-NNN-explainer.md`, the same name a case-local document would
    take, because what a file is called should not depend on the directory it is served
    from. The id is written once in the renderer and every name is derived from it, so
    what is pinned here is the shape and the sharing: the published document and the
    claim documents beside the certificates carry one id between them, not two.
    """
    assert re.fullmatch(r"t-\d{3}-explainer\.md", MARKDOWN_OUTPUT.name)
    assert MARKDOWN_OUTPUT.name == f"{RESULT_ID}-explainer.md"
    claims = sorted(CASE.glob("*-verifiable-claim-*.md"))
    assert claims, "the case carries no claim document to share an id with"
    for claim in claims:
        assert claim.name.startswith(f"{RESULT_ID}-"), claim.name
    # The document is what it is named after: the article, not the template.
    assert document.startswith("# s(11)")


def test_the_md_chip_offers_the_document_by_its_published_name(page: str) -> None:
    """The chip is a relative link, so it resolves to a file that has to be beside it.

    `SOURCE_URL` is the published document's own filename, so a rename moves both ends
    at once. A chip left pointing at the old name is a 404 on the deployed site and
    nothing in the render notices, which is why it is checked against the constant the
    writer uses rather than against a name spelled out here.
    """
    assert f'href="{MARKDOWN_OUTPUT.name}"' in page


def pages_filters() -> dict[str, list[str]]:
    """The `paths:` filter of each event the Pages workflow triggers on."""
    workflow = safe_load((REPO / ".github" / "workflows" / "pages.yml").read_text("utf-8"))
    triggers = workflow["on" if "on" in workflow else True]
    return {
        event: settings["paths"]
        for event, settings in triggers.items()
        if isinstance(settings, dict) and "paths" in settings
    }


def covered(path: Path, patterns: list[str]) -> bool:
    """Whether a GitHub `paths:` filter republishes on a change under `path`.

    A filter entry is matched against files, not directories, so a declared input that
    is a directory is covered by a pattern that would match a file inside it. `**` and a
    bare directory name both do that; the comparison below is deliberately the strict
    one, so an entry that covers the directory only by accident does not pass.
    """
    relative = path.relative_to(REPO).as_posix()
    return any(
        pattern == relative or pattern.rstrip("/*") in (relative, relative.rstrip("/"))
        for pattern in patterns
    )


def test_the_pages_filter_covers_every_render_input() -> None:
    """A render input outside the filter is a page that goes stale with the gate green.

    The workflow's `paths:` list and the renderer's imports are written in two languages
    and maintained by hand, so nothing but this comparison stops them drifting. They had
    drifted: the filter named the composite PNG and PDF but not the SVG the figure
    actually shows, and named neither the frontier register the opening counts nor the
    figure record the drawing is built from (think-bl0n). Any of those four could have
    changed on main and left the deployed page showing the previous render, with every
    check passing, which is the shape of D-455 rather than a new one.

    Both events are checked. A pull request that builds the page is the only review a
    render change gets, so a filter that publishes on an input but does not build it on
    the pull request is the same gap seen from the other side.
    """
    filters = pages_filters()
    assert set(filters) == {"push", "pull_request"}, sorted(filters)
    for event, patterns in filters.items():
        missing = [
            declared.relative_to(REPO).as_posix()
            for declared in RENDER_INPUTS
            if not covered(declared, patterns)
        ]
        assert not missing, f"{event}: RENDER_INPUTS not covered by paths: {missing}"


def test_every_declared_render_input_exists() -> None:
    """A path filter naming a file that is gone republishes on nothing, silently.

    The check above compares two lists to each other, which both of them can satisfy
    while naming a file the repository no longer has. This is the other half: every
    declared input resolves, so a rename cannot leave a matched pair of dead entries.
    """
    for declared in RENDER_INPUTS:
        assert declared.exists(), declared.relative_to(REPO).as_posix()
