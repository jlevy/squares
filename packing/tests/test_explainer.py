"""The explainer renders, and what it renders fetches nothing.

`devtools.render_explainer` was exercised only by the Pages workflow, on the pull
requests whose paths its filters name; nothing in the suite rendered the page. A full
render is under a second, so it runs here, and the two properties the workflow used to
grep for are asserted on the string the renderer returns: no placeholder survived
substitution, and nothing in the page is a reference outside it.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

from devtools import render_explainer
from devtools.render_explainer import (
    ATLAS,
    BEST_RENDERING,
    CARD_ALT,
    CASE,
    COMPOSITE_ALT,
    COMPOSITE_ASSETS,
    COMPOSITE_CARD,
    COMPOSITE_PNG,
    GENERATOR,
    MARKDOWN_OUTPUT,
    OUTPUT,
    RENDER_INPUTS,
    REPO,
    REPO_URL,
    RESULT_ID,
    SITE_URL,
    THIRDPARTY,
    VERIFIER,
    WALKTHROUGH,
    assert_self_contained,
    link_revision,
    page_edition,
    png_size,
    render,
)
from devtools.render_explainer import load_certificate as load
from devtools.render_explainer_pdf import OUTPUT as PDF_OUTPUT
from sqpack.release import PUBLICATION_STATUS, PUBLICATION_VERSION
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


@pytest.mark.parametrize(
    ("paths", "comparison", "pinned_check"),
    [
        (WALKTHROUGH[:1], False, False),
        (WALKTHROUGH, True, True),
        (WALKTHROUGH[::-1], False, True),
        (WALKTHROUGH[1:], False, True),
    ],
    ids=["single", "both", "headline-first", "headline-only"],
)
def test_certificate_comparisons_match_the_rendered_certificates(
    paths: tuple[Path, ...], *, comparison: bool, pinned_check: bool
) -> None:
    rendered = render(paths)
    document = " ".join(rendered.markdown.split())
    assert ("simpler certificate for the weaker bound" in document) is comparison
    assert ("looser of the two bounds" in document) is comparison
    assert ("The figures below illustrate this certificate." in document) is not comparison
    assert "the theorem written out, the 19/5 certificate as plain data" in document
    assert ("one-file checker" in document) is pinned_check
    assert "A certificate written by a wrong program" not in document
    assert (
        "The verifier rejects a certificate that fails the conditions, "
        "regardless of how it was generated."
    ) in document
    assert "{{" not in rendered.markdown
    if len(paths) != 1:
        return
    facts = render_explainer.derive(paths[0])
    assert f"{len(facts.atoms):,} rationally weighted points" in document
    assert f"{facts.steps + 1} rationally parameterized" in document


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


def test_no_screen_only_prose_survives_into_the_published_document(document: str) -> None:
    """A multi-line `screen-only` span used to leak, and reads as ordinary prose when it does.

    `_SCREEN_ONLY` is compiled `re.DOTALL` so it can span lines, but it was applied one
    line at a time, so a span opening on one line and closing on the next matched
    nothing; `_SIMPLE_TAG` then stripped the bare tags and the sentence shipped. "The
    chooser under each figure switches every figure between the two at once" reached a
    published edition that has no chooser in it, and nothing objected, because the leak
    is well-formed Markdown in a well-formed document.

    Checked on the words rather than on the markup, for the same reason the publisher's
    own guard is: an edition that tells its reader to hover or tap is wrong however it
    got that way, and the markup is exactly what is missing by the time it is wrong.
    """
    for word in ("chooser", "hover", "tap", "drag", "click", "slider"):
        assert word not in document.lower(), f"{word!r} addresses a reader who has the page"


def test_the_published_document_says_what_it_is_and_where_the_figures_are(
    document: str,
) -> None:
    """Six of the seven figures are captions here, and a reader cannot tell that alone.

    Figure 1 carries its image; the rest are drawn by the page, so they arrive as
    captions with nothing above them -- readable, and describing something the reader
    cannot see. Without a word of explanation that reads as images that failed to load,
    and the chip row that would have pointed at the real page is one of the things this
    edition drops.
    """
    assert "Markdown edition" in document
    assert SITE_URL in document


def _style_blocks(page: str) -> list[str]:
    return re.findall(r"<style>(.*?)</style>", page, re.DOTALL)


def test_the_page_stylesheet_has_no_orphaned_comment_delimiter(page: str) -> None:
    """A comment that ends early turns the prose after it into CSS, silently.

    This shipped. A block comment was extended with a second paragraph, but the original
    `*/` was left in place above it, so eleven lines of English became two invalid
    qualified rules -- and the second one's prelude ran on until it swallowed the `{
    text-align: left !important; }` underneath, which is a real rule the printed document
    depends on. CSS error recovery is silent by specification: the browser dropped both,
    printed prose reverted to the vendor's justification, and every render, every
    reproducibility check and every screenshot still passed.

    Checked on the delimiters rather than by parsing, so it needs no CSS parser: strip
    the balanced comments and nothing that opens or closes one may remain.
    """
    for index, css in enumerate(_style_blocks(page)):
        stripped = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
        for orphan in ("*/", "/*"):
            assert orphan not in stripped, (
                f"style block {index}: an unbalanced {orphan} leaves prose outside a comment"
            )


def test_no_rule_in_the_page_stylesheet_has_prose_for_a_selector(page: str) -> None:
    """The other half of the same failure: a selector that is really a sentence.

    An unbalanced comment is one way to get there and a stray `}` is another. A selector
    cannot contain a semicolon or the word `important`, and a real one here is never
    hundreds of characters long, so a prelude with any of those is prose that the parser
    is about to discard along with the rule it was standing in front of.
    """
    for index, css in enumerate(_style_blocks(page)):
        stripped = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
        # Preludes only: what stands between the end of one rule and the `{` of the next.
        for prelude in re.findall(r"(?:^|[}])([^{}]*)\{", stripped):
            text = prelude.strip()
            assert ";" not in text, f"style block {index}: selector holds a `;`: {text[:80]!r}"
            assert "important" not in text, (
                f"style block {index}: selector holds `important`: {text[:80]!r}"
            )
            assert len(text) < 400, f"style block {index}: selector is prose: {text[:80]!r}"


def test_every_relative_link_in_the_page_names_a_file_the_deploy_serves(page: str) -> None:
    """A chip that 404s on the deployed site is invisible to every other check here.

    The page is served from a directory, so each relative `href` and `src` resolves
    against whatever the Pages artifact happens to contain. The MD chip is checked above
    against the constant the writer uses; this asks the same question of all of them at
    once, which is what the PDF chip needed -- its file is written by a different module
    from the one that writes the page, so nothing else relates the two.

    Two links already shipped as `file:///home/.../known-best-1-100.pdf`, absolute paths
    to the machine that built them, and the atlas figure was one of them.
    """
    served = {
        OUTPUT.name,
        MARKDOWN_OUTPUT.name,
        PDF_OUTPUT.name,
        *(asset.name for asset in COMPOSITE_ASSETS),
    }
    # Markup only. The page inlines KaTeX and kpress's client, and a minified
    # `'+a(this.src)+'` in one of them reads as an attribute to a regex that does not
    # know where the script ends.
    markup = re.sub(r"<(script|style)\b.*?</\1>", "", page, flags=re.DOTALL | re.IGNORECASE)
    links = {
        match.group(2)
        for match in re.finditer(r'\b(href|src)="([^"]+)"', markup)
        if not re.match(r"[a-z][a-z0-9+.-]*:|#|//", match.group(2), re.IGNORECASE)
    }
    missing = sorted(link for link in links if link.split("#")[0].split("?")[0] not in served)
    assert not missing, f"relative links to files the deploy does not serve: {missing}"


def test_the_pdf_chip_offers_the_pdf_the_exporter_writes(page: str) -> None:
    """Named against the exporter's own constant, so a rename moves both ends at once."""
    assert f'href="{PDF_OUTPUT.name}"' in page
    assert PDF_OUTPUT.parent == OUTPUT.parent, "the PDF must land beside the page it links from"


#: A link into this repository as GitHub spells one: the ref, then the path, under
#: `blob/` for a file and `tree/` for a directory.
REPOSITORY_LINK = re.compile(
    re.escape(REPO_URL) + r"/(?:blob|tree)/([^/\s\"<>)]+)/([^\s\"<>?#)]*)"
)


def repository_links(text: str) -> set[tuple[str, str]]:
    """Repository (ref, path) pairs, excluding fragments, queries, scripts and styles."""
    markup = re.sub(r"<(script|style)\b.*?</\1>", "", text, flags=re.DOTALL | re.IGNORECASE)
    return {(ref, path.rstrip("/")) for ref, path in REPOSITORY_LINK.findall(markup)}


def test_every_repository_link_is_a_permalink_to_the_commit_the_page_is_built_from(
    page: str, document: str
) -> None:
    """A link on `main` names whatever is there when the reader clicks, not this build.

    The certificate digests the page prints identify the data; the links are what
    identify the verifier, the generator, the checking package and the exposition a
    reported run used, and every one of them was built as `blob/main/...` (review of
    2026-09-05, Finding 8). So each link into the repository names the commit the page
    is rendered from, in full, in the page and in the Markdown edition alike, and that
    commit is read from the checkout rather than pinned, so that no merge leaves the
    deployed page linking to files older than the ones it describes. The set of linked
    paths is checked with it: a permalink to the wrong file is pinned just as firmly.
    """
    revision = link_revision()
    assert re.fullmatch(r"[0-9a-f]{40}", revision), revision
    links = repository_links(page) | repository_links(document)
    assert links, "the page links nothing in the repository"
    unpinned = sorted(f"{ref}/{path}" for ref, path in links if ref != revision)
    assert not unpinned, f"repository links not pinned to {revision}: {unpinned}"
    linked = {path for _, path in links}
    evidence = (
        VERIFIER,
        GENERATOR,
        THIRDPARTY,
        BEST_RENDERING,
        ATLAS,
        Path(render_explainer.__file__),
        *WALKTHROUGH,
        *sorted(CASE.glob("*-verifiable-claim-*.md")),
    )
    for path in evidence:
        assert path.resolve().relative_to(REPO).as_posix() in linked, path.name


def test_every_permalinked_path_exists_at_the_linked_commit(page: str, document: str) -> None:
    """A permalink to a path the commit does not have is a 404 from the day it is published.

    The linked commit is the checkout's `HEAD` and the paths are resolved against the
    working tree, so what this catches is a linked file that is new and not yet
    committed, or renamed in the tree but not in the commit. Asked of git rather than of
    the working tree, since the working tree is exactly what a permalink does not point
    at. Skipped where git cannot answer for the commit, which a source tarball cannot.
    """

    def exists(spec: str) -> bool:
        result = subprocess.run(
            ["git", "cat-file", "-e", spec], cwd=REPO, capture_output=True, check=False
        )
        return result.returncode == 0

    revision = link_revision()
    if not exists(f"{revision}^{{commit}}"):
        pytest.skip(f"{revision} is not in this clone; the check needs git")
    links = repository_links(page) | repository_links(document)
    pinned = sorted(path for ref, path in links if ref == revision)
    assert pinned, "nothing is linked at the build commit"
    missing = [path for path in pinned if not exists(f"{revision}:{path}")]
    assert not missing, f"linked at {revision} but not in that commit: {missing}"


def test_the_page_stamps_the_commit_it_is_built_from(page: str, document: str) -> None:
    """The version is the edition's; the hash is this build's, so it moves on every push.

    The atlas footer keeps the pinned revision, because the atlas is committed and
    compared byte for byte; the page is rendered on every deploy and says which commit
    the reader is looking at. Both spell the status and the version the same way.
    """
    edition = page_edition()
    assert edition.endswith(link_revision()[:8]), edition
    lead = f"{PUBLICATION_STATUS} " if PUBLICATION_STATUS else PUBLICATION_VERSION
    assert edition.startswith(lead), edition
    assert f"({edition})" in page
    assert f"({edition})" in document
