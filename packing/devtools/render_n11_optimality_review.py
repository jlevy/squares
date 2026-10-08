"""Publish the T-060 paper as an offline HTML page and readable Markdown.

The article and exact-data figures are maintained separately. This renderer only
substitutes the declared reviewed figure slots, gives repository citations immutable
links, and uses KPress for Markdown, math, footnotes, typography, and PDF print.

The page is one of the site's papers (`overview_sections.PAPERS`), so it carries the
site's navigation bar, with Papers current, as the explainer does: the shared partial
and stylesheet through `render_overview.nav_html`, the gear's program, and the script
that drops the bar when the page is framed in a card's popover. The bar is hidden in
print.

Its slug is `n11-optimality-review`, and that is its name everywhere: this module, its
templates and tests, and what it writes. Given the site's root (`--site`), it writes
`papers/n11-optimality-review.html` and `.md`, and with `--pdf` the `.pdf` beside them.
A paper is served a level below the site's root, so the bar's links climb one. Until
2026-10-01 it was served at `n11-optimality/t-060-explainer.html`, which
`render_overview` now serves as a forwarder.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from collections.abc import Mapping, Sequence
from html import escape
from pathlib import Path

from kpress.format.pdf import _await_print_fonts  # pyright: ignore[reportPrivateUsage]
from kpress.output import write_bytes_atomic
from strif import atomic_output_file

from devtools import artifact_dates, paper_front, paper_links, render_n11_lower_bounds_explainer
from devtools.render_n11_lower_bounds_explainer_pdf import dated
from devtools.render_overview import (
    EMBED_SCRIPT,
    MATH_SCRIPT,
    N11_OPTIMALITY_REVIEW,
    PAPER_TYPE_CSS,
    PAPERS_ROOT,
    SITE_NAV,
    SITE_NAV_CSS,
    SITE_URL,
    THEME_SCRIPT,
    PageMeta,
    colophon_lines,
    favicon_html,
    head_tags,
    nav_html,
    paper_path,
)
from sqpack.probes import probe
from sqpack.release import (
    OPTIMALITY_PROOF_PUBLISHED,
    OPTIMALITY_REVIEW_EDITION,
    OPTIMALITY_REVIEW_HISTORY,
    OPTIMALITY_REVIEW_REVISED,
)

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
TEMPLATES = Path(__file__).with_name("templates")
ARTICLE = TEMPLATES / "n11-optimality-review-article.md"
SHELL = TEMPLATES / "n11-optimality-review-shell.html"
STYLE = TEMPLATES / "n11-optimality-review.css"
FIGURES_MODULE = Path(__file__).with_name("n11_optimality_figures.py")
#: The site's root as this build writes it; the paper goes under `papers/` in it.
SITE = PACKING / "site"
#: The paper's slug, which names its page, its Markdown and its PDF.
SLUG = N11_OPTIMALITY_REVIEW
#: Where the paper is served, from the site's root, and the way back up to the root.
SITE_PATH = paper_path(SLUG)
SITE_ROOT = PAPERS_ROOT
TITLE = "A Review of the Optimality Proof of the Trump Packing of 11 Squares"
DESCRIPTION = (
    "A review of Queuingtheorydotcom's computer-assisted proof that Trump's 1979 packing "
    "of eleven unit squares is optimal, explained step by step."
)
#: The paper's front, in the two papers' one form (`devtools.paper_front`): the proof it
#: explains, credited first by its author and address; then who oversaw the review and
#: which agents wrote it; its own version, a draft, which links its version history at
#: the foot of the page, and never the site's edition; and its dates, the day the source
#: published the proof and the day the article last changed, all from `sqpack.release`.
#: The head states the second to a link preview (`page_meta`).
FRONT = paper_front.check(
    paper_front.PaperFront(
        slug=SLUG,
        title=TITLE,
        source=paper_front.Source(
            "Queuingtheorydotcom", "https://github.com/Queuingtheorydotcom/11SquaresOptimal"
        ),
        oversight=(paper_front.Person("Joshua Levy", "https://x.com/ojoshe"),),
        agents=("GPT-6 Astra", "GPT-6 Sol"),
        version=OPTIMALITY_REVIEW_EDITION,
        dates=(
            paper_front.Dated("First published", OPTIMALITY_REVIEW_HISTORY[-1].first_published),
            paper_front.Dated("Original proof", OPTIMALITY_PROOF_PUBLISHED),
            paper_front.Dated(paper_front.REVISED, OPTIMALITY_REVIEW_REVISED),
        ),
        history="version-history",
        series=paper_front.series(SLUG),
    )
)
FIGURE_KEYS = (
    "WITNESS_SVG",
    "ROADMAP_SVG",
    "LADDER_SVG",
    "COVER_SVG",
    "MASK_SVG",
    "CAPACITY_SVG",
    "POSE_SVG",
    "ROW_SVG",
    "CHARGE_SVG",
    "SYMMETRY_SVG",
    "CAPTURE_SVG",
    "LOCAL_SVG",
    "ENDPOINT_SVG",
)
MATH_WAIT_MS = 15_000
#: Asks the page's math driver for every formula at once, before a print.
TYPESET_ALL = probe(
    render_n11_lower_bounds_explainer.PROBES, "render_n11_optimality_review/typeset_all"
)
#: Rewrites the page's relative links against its published address before a print, so
#: the PDF's links to the site and to the other papers of the series do not point at the
#: build machine's disk; the explainer's PDF does the same.
ABSOLUTE_LINKS = probe(
    render_n11_lower_bounds_explainer.PROBES,
    "render_n11_lower_bounds_explainer_pdf/absolute_links",
)
FIGURE_SLOT = re.compile(r"\{\{([A-Z_]+_SVG)\}\}")
#: A figure's caption, and a formula in one. A caption is an HTML block, where KPress
#: leaves `$…$` as it is written, so the renderer typesets a caption's formulas itself.
FIGCAPTION = re.compile(r"<figcaption>.*?</figcaption>", re.DOTALL)
CAPTION_MATH = re.compile(r"\$([^$\n]+)\$")
LEFTOVER_SLOT = re.compile(r"\{\{[A-Z][A-Z_]*\}\}")
RELATIVE_LINK = re.compile(r"(?P<start>\]\()(?P<url>\.\.?/[^\s)]+)(?P<end>\))")
RELATIVE_REFERENCE = re.compile(r"(?m)^(?P<start>\[[^\]\n]+\]:[ \t]*)(?P<url>\.\.?/[^\s]+)")
RELATIVE_ANCHOR = re.compile(r'(?P<start><a\b[^>]*\bhref=")(?P<url>\.\.?/[^"]+)(?P<end>")')
ARCHIVED_CITATION_SOURCES = (
    PACKING / "resources/papers/kingbird-square-11-provenance.svg",
    PACKING / "resources/web/external-square-certificates-2026-09-22/kleddamag-11/README.md",
)
RENDER_INPUTS = (
    Path(__file__),
    PACKING / "devtools/site_assets.py",
    PACKING / "devtools/probes/site_assets/preload_fonts.js",
    PACKING / "devtools/site_math.py",
    PACKING / "devtools/node/render-site-math.mjs",
    PACKING / "devtools/templates/site-math.css",
    ARTICLE,
    SHELL,
    STYLE,
    *ARCHIVED_CITATION_SOURCES,
    # The front of the paper is written by the component both papers share.
    PACKING / "devtools" / "paper_front.py",
    render_n11_lower_bounds_explainer.PUBLICATION_STYLE,
    FIGURES_MODULE,
    # The series bound ladder, drawn from the register's headlines.
    PACKING / "devtools/paper_figures.py",
    PACKING / "frontier/results.yaml",
    PACKING / "devtools/n11_optimality_overview_figures.py",
    PACKING / "devtools/n11_optimality_mechanism_figures.py",
    PACKING / "devtools" / "check_n11_optimality_d4.py",
    PACKING / "devtools" / "render_n11_lower_bounds_explainer.py",
    PACKING / "devtools" / "n11-lower-bounds-explainer" / "diagram-labels.js",
    PACKING / "devtools" / "render_overview.py",
    PACKING / "devtools" / "render_frontier_page.py",
    PAPER_TYPE_CSS,
    SITE_NAV,
    SITE_NAV_CSS,
    THEME_SCRIPT,
    EMBED_SCRIPT,
    MATH_SCRIPT,
    render_n11_lower_bounds_explainer.INLINE_SCRIPT_ASSETS["NATIVE_MATH_METRICS"],
    render_n11_lower_bounds_explainer.PROBES
    / "render_n11_lower_bounds_explainer"
    / "host_math_init.js",
    render_n11_lower_bounds_explainer.PROBES
    / "render_n11_optimality_review"
    / "typeset_all.js",
    PACKING / "atlas" / "rendering" / "trump11-overview.svg",
    PACKING / "devtools" / "packing_render_adapters.py",
    PACKING / "src" / "sqpack" / "render",
    # The front prints the paper's own version and dates, which are declared here.
    PACKING / "src" / "sqpack" / "release.py",
    PACKING / "cases" / "trump11" / "packing.py",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/final-composition.json",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/d4-independent/objects",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/exclusion-inventory.json",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json",
    # The paper's exact tables: the role guard and the focused rectangle's radii.
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/guard.json",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/local-dual-residual/objects",
    PACKING / "devtools/check_n11_generic_fresh.py",
    PACKING / "devtools/check_n11_optimality_field_mask0.py",
    PACKING
    / "resources/web/n11-optimality-2026-09-29/receipts/generic-mask2095-intake"
    / "provenance.json",
    PACKING
    / "resources/web/n11-optimality-2026-09-29/receipts/generic-mask2095-intake"
    / "full-result.json",
    PACKING
    / "resources/web/n11-optimality-2026-09-29/receipts/generic-mask2095-intake/objects",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/field-mask0/result.json",
    PACKING / "resources/web/n11-optimality-2026-09-29/receipts/field-mask0/objects",
    REPO / "vendor" / "kpress",
)


def version_history_markdown() -> str:
    """The paper's own editions, newest first, each with the day it was first published
    and what changed in the paper: `sqpack.release.OPTIMALITY_REVIEW_HISTORY`."""
    return "\n".join(
        f"- **{entry.version} — {entry.first_published}.** {entry.result_scope}"
        for entry in OPTIMALITY_REVIEW_HISTORY
    )


def render_all_figures() -> dict[str, str]:
    """Load the figure renderers only in a full publication checkout. The bound ladder
    is the series' (`paper_figures.bound_ladder`), with this paper's result lit."""
    from devtools import paper_figures  # noqa: PLC0415
    from devtools.n11_optimality_figures import render_figures  # noqa: PLC0415
    from devtools.n11_optimality_mechanism_figures import (  # noqa: PLC0415
        render_mechanism_figures,
    )
    from devtools.n11_optimality_overview_figures import (  # noqa: PLC0415
        render_overview_figures,
    )

    groups = (
        render_figures(),
        render_overview_figures(),
        render_mechanism_figures(),
        {"LADDER_SVG": paper_figures.bound_ladder("T-060")},
    )
    figures: dict[str, str] = {}
    for group in groups:
        if figures.keys() & group.keys():
            raise ValueError("figure renderers supplied duplicate slots")
        figures.update(group)
    return figures


def render_all_facts() -> dict[str, str]:
    """What the captions say of the figures that is data, from the modules that draw
    them: each value comes from the receipt its figure is drawn from, once that receipt
    checks, so a caption can name a count and cannot retype one."""
    from devtools import (  # noqa: PLC0415
        n11_optimality_figures,
        n11_optimality_mechanism_figures,
        n11_optimality_overview_figures,
    )

    groups = (
        n11_optimality_figures.caption_facts(),
        n11_optimality_overview_figures.caption_facts(),
        n11_optimality_mechanism_figures.caption_facts(),
    )
    facts: dict[str, str] = {}
    for group in groups:
        if facts.keys() & group.keys():
            raise ValueError("figure modules supplied duplicate caption facts")
        facts.update(group)
    return facts


def caption_math(markdown: str) -> str:
    """The article with each caption's `$…$` formulas in KPress's own math markup.

    A figure and its caption are an HTML block, where KPress leaves `$…$` literal, so a
    caption used to write its mathematics as text (`17/32 ≤ t ≤ 9/16`, `tᵢ = tan(θᵢ/2)`),
    in characters the sans face does not carry and the reader's machine drew. A caption
    writes LaTeX as the prose does, the page's math pipeline typesets it in the
    caption's own face, and the Markdown edition keeps the `$…$` as written."""
    from devtools.render_frontier_page import math_html  # noqa: PLC0415

    return FIGCAPTION.sub(
        lambda caption: CAPTION_MATH.sub(
            lambda formula: math_html(formula.group(1)), caption.group(0)
        ),
        markdown,
    )


def link_revision() -> str:
    """The commit the paper's repository citations name: the one it is built from.

    The paper pins each citation to a commit, so a cited receipt reads as it did when
    the paper was typeset; the site's own pages link `main` instead (`repo_links`). The
    deploy renders from `main`, so `HEAD` there is a commit `main` keeps. Where git
    cannot answer (a source tarball), `--revision` has to say which commit it is.
    """
    found = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=REPO, capture_output=True, text=True, check=False
    )
    revision = found.stdout.strip()
    if found.returncode != 0 or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise SystemExit("git names no HEAD here: give --revision, a full commit ID")
    return revision


def _fill(
    template: str, values: Mapping[str, str], *, source: Path, strict: bool = False
) -> str:
    """Substitute every `{{NAME}}`; a placeholder left over fails, and with `strict` so
    does a value the template has no place for, which is how a shell that drops one
    half of a shared layer is refused rather than rendered without it."""
    if strict:
        unused = [key for key in values if "{{" + key + "}}" not in template]
        if unused:
            raise ValueError(f"{source.name}: values with no placeholder: {sorted(unused)}")
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    remaining = LEFTOVER_SLOT.findall(rendered)
    if remaining:
        raise ValueError(f"{source.name}: unresolved placeholders: {sorted(set(remaining))}")
    return rendered


def _repository_links(markdown: str, *, source: Path, revision: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("repository-link revision must be a full lowercase Git commit ID")

    def pin(url: str) -> str:
        path_text, mark, fragment = url.partition("#")
        target = (source.parent / path_text).resolve()
        if not target.is_relative_to(REPO):
            raise ValueError(f"{source.name}: link escapes repository: {path_text}")
        if not target.is_file():
            raise ValueError(f"{source.name}: linked source does not exist: {path_text}")
        path = target.relative_to(REPO).as_posix()
        result = f"https://github.com/jlevy/squares/blob/{revision}/{path}"
        if mark:
            result += "#" + fragment
        return result

    markdown = RELATIVE_LINK.sub(
        lambda match: match.group("start") + pin(match.group("url")) + match.group("end"),
        markdown,
    )
    markdown = RELATIVE_REFERENCE.sub(
        lambda match: match.group("start") + pin(match.group("url")), markdown
    )
    return RELATIVE_ANCHOR.sub(
        lambda match: (
            match.group("start")
            + escape(pin(match.group("url")), quote=True)
            + match.group("end")
        ),
        markdown,
    )


def expanded_markdown(
    source: str,
    *,
    figures: Mapping[str, str],
    article: Path = ARTICLE,
    revision: str,
    facts: Mapping[str, str] | None = None,
    edition: paper_links.Edition = "page",
) -> str:
    """Fill the paper's front, the declared figure slots and the caption facts, and pin
    local source citations to a Git commit. A fact the article does not use is refused,
    as a slot it does not fill is: the two lists are the article's and the figure
    modules' alike. A link to another paper of the series (`{{PAPER:<slug>#<anchor>}}`)
    is filled for `edition` before the pinning, which would otherwise refuse it as a
    file the repository does not hold (`devtools.paper_links`)."""
    facts = facts or {}
    source = paper_front.fill(source, FRONT)
    unused = sorted(key for key in facts if "{{" + key + "}}" not in source)
    if unused or any(FIGURE_SLOT.fullmatch("{{" + key + "}}") for key in facts):
        raise ValueError(f"{article.name}: caption facts unused or named as figures: {unused}")
    if set(figures) != set(FIGURE_KEYS):
        raise ValueError("figures must provide exactly the declared SVG slots")
    if set(FIGURE_SLOT.findall(source)) != set(FIGURE_KEYS):
        raise ValueError("article must use every declared figure slot exactly by name")
    if any(source.count("{{" + key + "}}") != 1 for key in FIGURE_KEYS):
        raise ValueError("article must use each figure slot exactly once")
    for key, svg in figures.items():
        if not svg.lstrip().startswith("<svg") or "</svg>" not in svg:
            raise ValueError(f"{key} is not a complete SVG")
        if re.search(
            r"<script\b|<foreignObject\b|\b(?:href|src)=[\"']https?://",
            svg,
            re.IGNORECASE,
        ):
            raise ValueError(f"{key} contains active or remote SVG content")
    filled = _fill(
        source,
        {**figures, **facts, "VERSION_HISTORY": version_history_markdown()},
        source=article,
    )
    filled = paper_links.fill_paper_links(filled, edition=edition)
    return _repository_links(filled, source=article, revision=revision)


def _script(text: str, *, name: str) -> str:
    """A program's text, refused if it would close its own script element early."""
    if "</script" in text.lower():
        raise ValueError(f"{name} closes its inline script")
    return text


def math_scripts(static: Path) -> dict[str, str]:
    """The paper's mathematics, typeset as every page of the site typesets its own.

    `KATEX_JS` is the explainer's pipeline (`render_n11_lower_bounds_explainer.katex_js`):
    KaTeX, KPress's metric tables and shared runtime, and the host adapter `squaresMath`.
    `SITE_MATH` is the site pages' driver (`overview/math.js`), which runs the adapter over
    KPress's math markup and marks the page `math-ready`. So a formula here gets what it gets on
    the explainer and on every other page: the one-mu kern after a function's name, the face of
    the text it sits in read from that text's computed face, and a reveal only once the faces
    its glyphs need have loaded, so a formula that asks for a face the page does not ship keeps
    its MathML and fails the PDF rather than being drawn from the reader's machine. KPress's own
    entry points, `auto-render.min.js` and `katex-init.js`, which the paper used to inline, do
    none of the three.
    """
    return {
        "KATEX_JS": _script(
            render_n11_lower_bounds_explainer.katex_js(static), name="the math pipeline"
        ),
        "SITE_MATH": _script(MATH_SCRIPT.read_text(encoding="utf-8"), name=MATH_SCRIPT.name),
    }


def page_meta() -> PageMeta:
    """Use the paper's credits and edition history for publication metadata."""
    return PageMeta(
        name=TITLE,
        description=DESCRIPTION,
        path=SITE_PATH,
        kind="article",
        published=paper_front.iso_date(OPTIMALITY_REVIEW_HISTORY[-1].first_published),
        modified=paper_front.iso_date(paper_front.revised(FRONT)),
        **render_n11_lower_bounds_explainer.scholarly_metadata(
            FRONT,
            TITLE,
            paper_front.iso_date(OPTIMALITY_REVIEW_HISTORY[-1].first_published),
            paper_front.iso_date(paper_front.revised(FRONT)),
        ),
    )


def render(
    source: str,
    *,
    figures: Mapping[str, str],
    revision: str,
    article: Path = ARTICLE,
    facts: Mapping[str, str] | None = None,
) -> tuple[str, str]:
    """Return self-contained HTML and the Markdown edition of the same document.

    The page typesets the expanded article, its front included; the edition is that
    document with its front in the Markdown edition's form (`paper_front.published`):
    the title as a heading and the credits as a list, and no formats row, which is the
    page's navigation. The rest, the figures as their SVG among it, is kept whole. A link
    to another paper is page-relative on the page and the site's address in the edition,
    which is read away from the site."""
    from kpress.format.markdown import parse_markdown  # noqa: PLC0415

    page_markdown = expanded_markdown(
        source, figures=figures, article=article, revision=revision, facts=facts
    )
    markdown = expanded_markdown(
        source,
        figures=figures,
        article=article,
        revision=revision,
        facts=facts,
        edition="markdown",
    )
    document = parse_markdown(
        caption_math(page_markdown), title=TITLE, trust_mode="trusted", math="auto"
    )
    errors = [item.message for item in document.diagnostics if item.severity == "error"]
    if errors:
        raise ValueError(f"{article.name}: KPress refused the article: {'; '.join(errors)}")
    static = render_n11_lower_bounds_explainer.kpress_static()
    values = {
        "PAGE_HEAD": head_tags(page_meta()),
        "KPRESS_CSS": render_n11_lower_bounds_explainer.kpress_css(static),
        "KATEX_CSS": render_n11_lower_bounds_explainer.katex_css(static)
        if document.has_math
        else "",
        "RELATION_CSS": render_n11_lower_bounds_explainer.relation_face_css(static),
        "PAPER_TYPE_CSS": PAPER_TYPE_CSS.read_text(encoding="utf-8"),
        **render_n11_lower_bounds_explainer.publication_layer(),
        "PAPER_CSS": STYLE.read_text(encoding="utf-8"),
        "SITE_FAVICON": favicon_html(inline=True),
        "SITE_NAV_CSS": SITE_NAV_CSS.read_text(encoding="utf-8"),
        "SITE_NAV": nav_html("papers", root=SITE_ROOT),
        # A paper's closing credit carries no version: its own is in its credits, and
        # the site's goes on no paper.
        "COLOPHON": colophon_lines(edition=""),
        "SITE_EMBED": EMBED_SCRIPT.read_text(encoding="utf-8"),
        "SITE_THEME": THEME_SCRIPT.read_text(encoding="utf-8"),
        "THEME_BOOTSTRAP": render_n11_lower_bounds_explainer.theme_bootstrap(static),
        "BODY_HTML": document.html,
        **(math_scripts(static) if document.has_math else {"KATEX_JS": "", "SITE_MATH": ""}),
        "DIAGRAM_LABEL_SCRIPT": render_n11_lower_bounds_explainer.INLINE_SCRIPT_ASSETS[
            "DIAGRAM_LABEL_SCRIPT"
        ].read_text(encoding="utf-8"),
    }
    page = _fill(SHELL.read_text(encoding="utf-8"), values, source=SHELL, strict=True)
    render_n11_lower_bounds_explainer.assert_self_contained(page)
    return page, paper_front.published(markdown, FRONT)


def output_files(site: Path, html: str, markdown: str) -> dict[Path, str]:
    """What a render writes under the site's root `site`: the page and its Markdown,
    beside each other under the paper's slug."""
    return {
        site / SITE_PATH: html,
        site / paper_path(SLUG, ".md"): markdown,
    }


def _print_pdf(html_path: Path, pdf_path: Path) -> None:
    """Print only after KPress math and its print fonts have settled.

    The document's two date fields are set to the day the article says the review was
    last revised, not left at the second Chromium printed it
    (`render_n11_lower_bounds_explainer_pdf.dated`, `devtools.artifact_dates`).
    """
    from playwright.sync_api import expect, sync_playwright  # noqa: PLC0415

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = None
        try:
            page = browser.new_page()
            page.goto(html_path.as_uri(), wait_until="networkidle")
            page.evaluate(ABSOLUTE_LINKS, SITE_URL + SITE_PATH)
            page.emulate_media(media="print")
            hosts = page.locator(".kpress-math")
            if hosts.count() == 0:
                raise ValueError("the paper has no typeset math")
            # The driver leaves the formulas far from the window to idle time; a print
            # asks for them all, so the wait below is for work already under way.
            page.evaluate(TYPESET_ALL)
            try:
                expect(page.locator(".kpress-math:not(:has(.katex))")).to_have_count(
                    0, timeout=MATH_WAIT_MS
                )
            except AssertionError as exc:
                raise ValueError("the paper has unrendered math") from exc
            if page.locator(".katex-error, math merror").count():
                raise ValueError("the paper contains a math rendering error")
            _await_print_fonts(page)  # pyright: ignore[reportArgumentType]
            drawn = page.pdf(format="Letter", prefer_css_page_size=True, print_background=True)
            write_bytes_atomic(pdf_path, dated(drawn, artifact_dates.optimality_revised()))
        finally:
            if page is not None:
                page.close()
            browser.close()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--site",
        type=Path,
        default=SITE,
        help="the site's root; the paper is written under papers/ in it",
    )
    parser.add_argument("--revision", default=None, help="full Git commit for source links")
    parser.add_argument("--pdf", action="store_true", help="also print the HTML with KPress")
    parser.add_argument("--check", action="store_true", help="compare current HTML/Markdown")
    args = parser.parse_args(argv)
    html, markdown = render(
        ARTICLE.read_text(encoding="utf-8"),
        figures=render_all_figures(),
        facts=render_all_facts(),
        revision=args.revision or link_revision(),
    )
    from devtools import site_assets, site_math  # noqa: PLC0415

    site = args.site.resolve()
    html = site_math.prepare(html, page_path=SITE_PATH)
    html = html.replace(favicon_html(inline=True), favicon_html(root="../"))
    html, assets = site_assets.link_inline_assets(html, SITE_PATH)
    outputs = output_files(site, html, markdown)
    if args.check:
        if args.pdf:
            parser.error("--check compares HTML and Markdown; use --pdf for a fresh PDF")
        stale = [site / path for path in site_assets.stale_assets(site, assets)] + [
            path
            for path, content in outputs.items()
            if not path.is_file() or path.read_text(encoding="utf-8") != content
        ]
        if stale:
            raise SystemExit(f"stale {SLUG} output: " + ", ".join(str(path) for path in stale))
        return 0
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        with atomic_output_file(path) as temporary:
            temporary.write_text(content, encoding="utf-8")
    site_assets.write_assets(site, assets)
    if args.pdf:
        _print_pdf(site / SITE_PATH, site / paper_path(SLUG, ".pdf"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
