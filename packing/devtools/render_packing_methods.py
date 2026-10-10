"""Publish the standalone tutorial on finding record square packings.

The canonical manuscript is templates/packing-methods-article.md. It uses the site's
shared paper front, typography, scholarly metadata, math preparation and PDF printer,
with its own version and dates. This tutorial belongs to no numbered series and
illustrates methods with retained source geometry, without running searches or checkers.

Run with --site SITE to write papers/square-packing-methods-survey.html and .md, and
add --pdf for its PDF. Use --check to compare prepared HTML and Markdown with a build.
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
from pathlib import Path
from xml.etree import ElementTree as ET

from strif import atomic_output_file

from devtools import (
    packing_methods_figures,
    paper_front,
    paper_links,
    render_n11_lower_bounds_explainer,
)
from devtools.render_n11_optimality_review import (
    FIGURE_SLOT,
    RELATIVE_ANCHOR,
    RELATIVE_LINK,
    RELATIVE_REFERENCE,
    caption_math,
    link_revision,
    math_scripts,
)
from devtools.render_n11_optimality_review import (
    _fill as fill_template,  # pyright: ignore[reportPrivateUsage]
)
from devtools.render_n11_optimality_review import (
    _print_pdf as print_pdf,  # pyright: ignore[reportPrivateUsage]
)
from devtools.render_n11_optimality_review import (
    _repository_links as repository_links,  # pyright: ignore[reportPrivateUsage]
)
from devtools.render_overview import (
    EMBED_SCRIPT,
    MATH_SCRIPT,
    PACKING_METHODS,
    PAPER_TYPE_CSS,
    PAPERS_ROOT,
    SITE_NAV,
    SITE_NAV_CSS,
    THEME_SCRIPT,
    PageMeta,
    colophon_lines,
    favicon_html,
    head_tags,
    nav_html,
    paper_path,
    paper_record,
)
from sqpack.release import (
    PACKING_METHODS_EDITION,
    PACKING_METHODS_FIRST_PUBLISHED,
    PACKING_METHODS_HISTORY,
    PACKING_METHODS_REVISED,
)
from sqpack.render.svg import validate_safe_tree

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
TEMPLATES = Path(__file__).with_name("templates")
ARTICLE = TEMPLATES / "packing-methods-article.md"
SHELL = TEMPLATES / "packing-methods-shell.html"
STYLE = TEMPLATES / "packing-methods.css"
SITE = PACKING / "site"
SLUG = PACKING_METHODS
SITE_PATH = paper_path(SLUG)
SITE_ROOT = PAPERS_ROOT
TITLE = paper_record(SLUG).title
DESCRIPTION = (
    "How record square packings are found: model the geometry, search and refine "
    "candidates, reconstruct exact coordinates, and verify the resulting upper bounds."
)
FRONT = paper_front.check(
    paper_front.PaperFront(
        slug=SLUG,
        title=TITLE,
        oversight=(paper_front.Person("Joshua Levy", "https://x.com/ojoshe"),),
        agents=("GPT-6 Astra", "GPT-6 Sol"),
        version=PACKING_METHODS_EDITION,
        history="version-history",
        dates=(
            paper_front.Dated("First published", PACKING_METHODS_FIRST_PUBLISHED),
            paper_front.Dated(paper_front.REVISED, PACKING_METHODS_REVISED),
        ),
    )
)


def citation_sources(article: Path = ARTICLE) -> tuple[Path, ...]:
    """The local files the manuscript cites and the renderer requires on disk.

    Declare these along with the rendering assets so scope and sparse-checkout checks
    cover citations into the archive and campaign, without hydrating their bulk data.
    """
    source = article.read_text(encoding="utf-8")
    targets = {
        (article.parent / match.group("url").partition("#")[0]).resolve()
        for pattern in (RELATIVE_LINK, RELATIVE_REFERENCE, RELATIVE_ANCHOR)
        for match in pattern.finditer(source)
    }
    if any(not target.is_relative_to(REPO) for target in targets):
        raise ValueError(f"{article.name}: citation escapes repository")
    return tuple(sorted(targets))


CITATION_SOURCES = citation_sources()
FIGURE_KEYS = packing_methods_figures.FIGURE_KEYS

#: Input discovery for Pages scope and local previews, without certificate hydration.
RENDER_INPUTS = (
    Path(__file__),
    ARTICLE,
    *CITATION_SOURCES,
    *packing_methods_figures.FIGURE_INPUTS,
    SHELL,
    STYLE,
    PAPER_TYPE_CSS,
    SITE_NAV,
    SITE_NAV_CSS,
    THEME_SCRIPT,
    EMBED_SCRIPT,
    MATH_SCRIPT,
    PACKING / "devtools/paper_front.py",
    PACKING / "devtools/paper_links.py",
    PACKING / "devtools/render_overview.py",
    PACKING / "devtools/render_n11_optimality_review.py",
    PACKING / "devtools/render_n11_lower_bounds_explainer.py",
    PACKING / "devtools/render_n11_lower_bounds_explainer_pdf.py",
    PACKING / "devtools/artifact_dates.py",
    PACKING / "devtools/site_assets.py",
    PACKING / "devtools/site_math.py",
    PACKING / "devtools/templates/site-math.css",
    PACKING / "devtools/node/render-site-math.mjs",
    PACKING / "devtools/prepare_n11_lower_bounds_explainer_math.py",
    PACKING / "devtools/sans_instances.py",
    PACKING / "devtools/templates/paper-publication.css",
    PACKING / "devtools/templates/fonts",
    PACKING / "devtools/probes",
    PACKING / "src/sqpack/probes.py",
    PACKING / "src/sqpack/release.py",
    *render_n11_lower_bounds_explainer.INLINE_SCRIPT_ASSETS.values(),
    REPO / "vendor/kpress",
    PACKING / "pyproject.toml",
    PACKING / "uv.lock",
)


def render_all_figures() -> dict[str, str]:
    """Project the five attributed examples from retained source geometry."""
    return packing_methods_figures.render_figures()


def render_all_facts() -> dict[str, str]:
    """The publication interface's data substitutions; this tutorial has none."""
    return {}


def version_history_markdown() -> str:
    """The paper's own editions, newest first, with publication date and changes."""
    return "\n".join(
        f"- **{entry.version} — {entry.first_published}.** {entry.result_scope}"
        for entry in PACKING_METHODS_HISTORY
    )


def expanded_markdown(
    source: str,
    *,
    revision: str,
    figures: Mapping[str, str],
    article: Path = ARTICLE,
    edition: paper_links.Edition = "page",
) -> str:
    """Fill the shared front and sibling-paper links, and pin source citations."""
    if set(figures) != set(FIGURE_KEYS):
        raise ValueError("figures must provide exactly the declared SVG slots")
    if set(FIGURE_SLOT.findall(source)) != set(FIGURE_KEYS):
        raise ValueError("article must use every declared figure slot exactly by name")
    if any(source.count("{{" + key + "}}") != 1 for key in FIGURE_KEYS):
        raise ValueError("article must use each figure slot exactly once")
    for key, svg in figures.items():
        try:
            tree = ET.fromstring(svg)
        except ET.ParseError as error:
            raise ValueError(f"{key} is not a complete SVG: {error}") from error
        try:
            validate_safe_tree(tree)
        except ValueError as error:
            raise ValueError(f"{key} contains active or remote SVG content: {error}") from error
    filled = paper_front.fill(source, FRONT)
    filled = paper_links.fill_paper_links(filled, edition=edition)
    filled = fill_template(
        filled, {**figures, "VERSION_HISTORY": version_history_markdown()}, source=article
    )
    return repository_links(filled, source=article, revision=revision)


def page_meta() -> PageMeta:
    """The tutorial's own publication identity in the shared scholarly head."""
    published = paper_front.iso_date(PACKING_METHODS_FIRST_PUBLISHED)
    modified = paper_front.iso_date(paper_front.revised(FRONT))
    return PageMeta(
        name=TITLE,
        description=DESCRIPTION,
        path=SITE_PATH,
        kind="article",
        published=published,
        modified=modified,
        **render_n11_lower_bounds_explainer.scholarly_metadata(
            FRONT, TITLE, published, modified
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
    """Return the self-contained paper page and the same paper's Markdown edition."""
    from kpress.format.markdown import parse_markdown  # noqa: PLC0415

    if facts:
        raise ValueError("the methods tutorial declares no fact substitutions")
    page_markdown = expanded_markdown(
        source, figures=figures, revision=revision, article=article
    )
    markdown = expanded_markdown(
        source, figures=figures, revision=revision, article=article, edition="markdown"
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
        "SITE_NAV": nav_html("papers", root=PAPERS_ROOT),
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
    page = fill_template(SHELL.read_text(encoding="utf-8"), values, source=SHELL, strict=True)
    render_n11_lower_bounds_explainer.assert_self_contained(page)
    return page, paper_front.published(markdown, FRONT)


def output_files(site: Path, html: str, markdown: str) -> dict[Path, str]:
    """The tutorial page and Markdown beside each other under the paper's slug."""
    return {site / SITE_PATH: html, site / paper_path(SLUG, ".md"): markdown}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=SITE, help="the site's root")
    parser.add_argument("--revision", default=None, help="full Git commit for source links")
    parser.add_argument("--pdf", action="store_true", help="also print the prepared HTML")
    parser.add_argument("--check", action="store_true", help="compare current HTML/Markdown")
    args = parser.parse_args(argv)
    if args.check and args.pdf:
        parser.error("--check compares HTML and Markdown; use --pdf for a fresh PDF")
    html, markdown = render(
        ARTICLE.read_text(encoding="utf-8"),
        figures=render_all_figures(),
        facts=render_all_facts(),
        revision=args.revision or link_revision(),
    )
    from devtools import artifact_dates, site_assets, site_math  # noqa: PLC0415

    site = args.site.resolve()
    html = site_math.prepare(html, page_path=SITE_PATH)
    html = html.replace(favicon_html(inline=True), favicon_html(root=PAPERS_ROOT))
    html, assets = site_assets.link_inline_assets(html, SITE_PATH)
    outputs = output_files(site, html, markdown)
    if args.check:
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
        print_pdf(
            site / SITE_PATH,
            site / paper_path(SLUG, ".pdf"),
            revised=artifact_dates.written_date(PACKING_METHODS_REVISED),
            site_path=SITE_PATH,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
