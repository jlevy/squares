"""Publish Part II, the review of T-037, as an offline HTML page and readable Markdown.

The article and its exact-data figures are maintained separately. This renderer only
substitutes the declared figure slots and caption facts, fills the links to the other two
papers, gives repository citations immutable links, and uses KPress for Markdown, math,
footnotes, typography and PDF print, as `render_n11_optimality_review` does for Part III,
on which it is modelled.

The page is one of the site's papers, so it carries the site's navigation bar with
Papers current, the shared publication layer and the site's math pipeline, all through
the same helpers Part III uses. Its slug is `n11-threshold-bound-review`
(`render_overview.N11_THRESHOLD_BOUND_REVIEW`), and that is its name everywhere: this
module, its templates and tests, and what it writes. Given the site's root (`--site`),
it writes `papers/n11-threshold-bound-review.html` and `.md`, and with `--pdf` the
`.pdf` beside them.

The figures come from `devtools.n11_threshold_figures` (`render_figures`,
`caption_facts`, `FIGURE_INPUTS`), drawn only on the real render path, so the tests can
pass a fake figures dict and fake facts, as Part III's do. `FIGURE_KEYS` and
`CAPTION_FACT_KEYS` below are the contract between the article and that module: every
slot is used exactly once, every fact at least once, and a fact the article does not use
is refused.
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

from devtools import (
    n11_threshold_figures,
    paper_front,
    paper_links,
    render_n11_lower_bounds_explainer,
)
from devtools.render_n11_lower_bounds_explainer_pdf import dated
from devtools.render_n11_optimality_review import (
    ABSOLUTE_LINKS,
    MATH_WAIT_MS,
    TYPESET_ALL,
    caption_math,
    math_scripts,
)
from devtools.render_overview import (
    EMBED_SCRIPT,
    MATH_SCRIPT,
    N11_THRESHOLD_BOUND_REVIEW,
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
from sqpack.release import (
    THRESHOLD_PROOF_PUBLISHED,
    THRESHOLD_REVIEW_EDITION,
    THRESHOLD_REVIEW_HISTORY,
    THRESHOLD_REVIEW_REVISED,
)

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
TEMPLATES = Path(__file__).with_name("templates")
ARTICLE = TEMPLATES / "n11-threshold-bound-review-article.md"
SHELL = TEMPLATES / "n11-threshold-bound-review-shell.html"
STYLE = TEMPLATES / "n11-threshold-bound-review.css"
#: The paper's term registry, read by the define-before-use gate (`devtools.paper_terms`).
TERMS = TEMPLATES / "n11-threshold-bound-review-terms.yaml"
FIGURES_MODULE = Path(__file__).with_name("n11_threshold_figures.py")
#: The site's root as this build writes it; the paper goes under `papers/` in it.
SITE = PACKING / "site"
#: The paper's slug, which names its page, its Markdown and its PDF.
SLUG = N11_THRESHOLD_BOUND_REVIEW
#: Where the paper is served, from the site's root, and the way back up to the root.
SITE_PATH = paper_path(SLUG)
SITE_ROOT = PAPERS_ROOT
#: The title, plain, for the head and the registry; the hero writes its one formula as
#: Markdown math, which KPress typesets on the page like every other formula of this
#: paper and which the Markdown edition keeps as `$...$`. Part I's `.tex` span is typeset
#: only by Part I's own math preparation, so here it would print its TeX raw.
TITLE = "A Review of the Certified Lower Bound s(11) > 31/8 for 11 Squares"
HERO_TITLE = TITLE.replace("s(11) > 31/8", "$s(11) > 31/8$")
#: One line of at most 160 characters, the §8 one-liner cut to the head's limit.
DESCRIPTION = (
    "Explains Kleddamag's proof that s(11) > 31/8 (T-037): five-site k-of-m charges, "
    "strict cores on shrunken parents, and a certificate over 12,028 angle rows."
)
#: The archived copy of the source proof, which the article cites file by file, and this
#: project's receipts of its replay and audit beside it.
ARCHIVE = PACKING / "resources/web/external-square-certificates-2026-09-22/kleddamag-11"
RECEIPTS = PACKING / "resources/web/external-square-certificates-2026-09-22/receipts/n11"
#: The paper's front, in the papers' one form (`devtools.paper_front`): the proof it
#: explains, credited first by its author and address; then who oversaw the review and
#: which agents wrote it; its own version, which links its version history at the foot
#: of the page; and its dates, the day the source published the proof and the day the
#: article last changed, all from `sqpack.release`.
FRONT = paper_front.check(
    paper_front.PaperFront(
        slug=SLUG,
        title=HERO_TITLE,
        source=paper_front.Source(
            "Kleddamag", "https://github.com/Kleddamag/11-squares-certified-bound"
        ),
        oversight=(paper_front.Person("Joshua Levy", "https://x.com/ojoshe"),),
        agents=("Fable 5.1", "Opus 5.5"),
        version=THRESHOLD_REVIEW_EDITION,
        dates=(
            paper_front.Dated("First published", THRESHOLD_REVIEW_HISTORY[-1].first_published),
            paper_front.Dated("Original proof", THRESHOLD_PROOF_PUBLISHED),
            paper_front.Dated(paper_front.REVISED, THRESHOLD_REVIEW_REVISED),
        ),
        history="version-history",
        series=paper_front.series(SLUG),
    )
)
#: The twelve figures, plan figures II.1 to II.12 in reading order; the figure module
#: supplies exactly these and the article uses each exactly once.
FIGURE_KEYS = (
    "CHANGES_SVG",
    "LADDER_SVG",
    "ROADMAP_SVG",
    "CHARGE_SVG",
    "BUDGET_SVG",
    "FAMILIES_SVG",
    "CORE_SVG",
    "CATALOGUE_SVG",
    "ENVELOPE_SVG",
    "SIGNED_SVG",
    "FIELD_SVG",
    "MINIMA_SVG",
)
#: Facts about the whole certificate, which the prose and several captions name.
CERTIFICATE_FACT_KEYS = (
    "CERT_GAMMA",
    "CERT_M",
    "CERT_ELEVEN_GAMMA",
    "CERT_SURPLUS_UNITS",
    "CERT_ROWS",
    "CERT_SITES",
    "CERT_POINT_SITES",
    "CERT_ORBITS",
    "CERT_CHARGE_ORBITS",
    "CERT_FEATURES",
    "CERT_A",
    "CERT_L0",
    "CERT_BOUND",
)
#: Every caption fact the article names, `<FIGURE>_<FACT>` for a fact about one figure
#: and `CERT_<FACT>` for one about the whole certificate. `caption_facts()` supplies
#: exactly these.
CAPTION_FACT_KEYS = (
    *CERTIFICATE_FACT_KEYS,
    # Figure 1: what changed from T-026 to T-037.
    "CHANGES_T026_POINTS",
    "CHANGES_T026_TRIPLES",
    "CHANGES_T026_POINT_SHARE",
    "CHANGES_T037_POINT_SHARE",
    "CHANGES_T026_B",
    "CHANGES_T026_NET",
    # Figure 2: the series bound ladder, and the bound gap the prose states.
    "LADDER_GAP",
    # Figure 4: one k-of-m charge, orbit 72.
    "CHARGE_ORBIT",
    "CHARGE_WEIGHT",
    "CHARGE_SITES",
    "CHARGE_ROW",
    # Figure 5: budget bars.
    "BUDGET_POINTS",
    "BUDGET_TWO_OF_THREE",
    "BUDGET_TWO_OF_FIVE",
    "BUDGET_THREE_OF_FIVE",
    "BUDGET_M",
    "BUDGET_SURPLUS",
    "BUDGET_RATIO",
    # Figure 6: the site system, the census and the gallery.
    "FAMILIES_POINT_ORBITS",
    "FAMILIES_POINT_ONLY",
    "FAMILIES_SHARED",
    "FAMILIES_CHARGE_ONLY",
    "FAMILIES_IN_CHARGE",
    "FAMILIES_NEAR_ORBITS",
    "FAMILIES_NEAR_SHARE",
    "FAMILIES_WIDE_SHARE",
    "FAMILIES_POINT_MAX",
    "FAMILIES_POINT_MAX_SITE",
    "FAMILIES_TABLE",
    "FAMILIES_TRIPLE_ORBIT",
    "FAMILIES_TRIPLE_WEIGHT",
    "FAMILIES_TRIPLE_CENTRE",
    "FAMILIES_PAIR_ORBIT",
    "FAMILIES_PAIR_WEIGHT",
    # Figure 7: parent and core.
    "CORE_EXAGGERATION",
    # Figure 8: the catalogue strip.
    "CATALOGUE_ROWS",
    "CATALOGUE_END",
    "CATALOGUE_B_MIN",
    "CATALOGUE_B_MAX",
    "CATALOGUE_TIGHT_ROW",
    "CATALOGUE_TIGHT_ANGLES",
    "CATALOGUE_TIGHT_MIN",
    "CATALOGUE_PAIR_ROWS",
    "CATALOGUE_PAIR_ANGLES",
    "CATALOGUE_PAIR_MIN",
    # Figure 9: signed rectangles, and the expansion's weight.
    "SIGNED_ORBIT",
    "SIGNED_ABS_SUMS",
    "SIGNED_EXPANSION_WEIGHT",
    # Figure 10: the envelope.
    "ENVELOPE_RHO",
    "ENVELOPE_HALF",
    # Figure 11: the charge field.
    "FIELD_ROW",
    "FIELD_MIN",
    "FIELD_WITNESS",
    "FIELD_GRID",
    # Figure 12: per-row minima and the native band.
    "MINIMA_VALUES",
    "MINIMA_TOP",
    "MINIMA_TOP_ROWS",
    "MINIMA_NATIVE_BELOW_ONE",
    "MINIMA_NATIVE_EQUAL",
    "MINIMA_NATIVE_MIN",
)
FIGURE_SLOT = re.compile(r"\{\{([A-Z_]+_SVG)\}\}")
LEFTOVER_SLOT = re.compile(r"\{\{[A-Z][A-Z_]*\}\}")
RELATIVE_LINK = re.compile(r"(?P<start>\]\()(?P<url>\.\.?/[^\s)]+)(?P<end>\))")
RELATIVE_REFERENCE = re.compile(r"(?m)^(?P<start>\[[^\]\n]+\]:[ \t]*)(?P<url>\.\.?/[^\s]+)")
RELATIVE_ANCHOR = re.compile(r'(?P<start><a\b[^>]*\bhref=")(?P<url>\.\.?/[^"]+)(?P<end>")')
#: Words that address a reader who has the page in front of them, which a paper's prose
#: never does (Part I's publisher refuses the same words in its Markdown edition).
ONLY_ON_SCREEN = re.compile(
    r"\b(?:chooser|hover|tap|drag|click|button|slider|toggle)\b", re.IGNORECASE
)
#: The archived Kleddamag files the article links, each pinned to a repository blob.
ARCHIVED_CITATION_SOURCES = (
    ARCHIVE / "README.md",
    ARCHIVE / "PROOF.md",
    ARCHIVE / "ATTRIBUTION.md",
    ARCHIVE / "AUTHORS.md",
    ARCHIVE / "VERIFIED.json",
    ARCHIVE / "global-certificate.json",
    ARCHIVE / "exact_mixed.py",
    ARCHIVE / "integer_sweep.py",
    ARCHIVE / "independent_controls.py",
    ARCHIVE / "verify_threshold_algebra.py",
    ARCHIVE / "threshold-algebra.json",
    ARCHIVE / "NOTICES/Mira-ATTRIBUTION.md",
    ARCHIVE / "NOTICES/Guzhou-NOTICE.md",
    ARCHIVE / "evidence/portable/python.json",
    ARCHIVE / "evidence/portable/controls.json",
)
#: Every file the page is built from: the Pages workflow's path filter and the scope
#: job read it (`devtools.pages_scope`). The figure module's own data inputs are its
#: `FIGURE_INPUTS`, repository-relative; a file both lists name is declared once.
RENDER_INPUTS = tuple(
    dict.fromkeys(
        (
            Path(__file__),
            PACKING / "devtools/site_assets.py",
            PACKING / "devtools/site_math.py",
            PACKING / "devtools/node/render-site-math.mjs",
            PACKING / "devtools/templates/site-math.css",
            ARTICLE,
            SHELL,
            STYLE,
            TERMS,
            *ARCHIVED_CITATION_SOURCES,
            # The front of the paper is written by the component the papers share, and the
            # links between papers by the shared placeholder.
            PACKING / "devtools" / "paper_front.py",
            PACKING / "devtools" / "paper_links.py",
            render_n11_lower_bounds_explainer.PUBLICATION_STYLE,
            FIGURES_MODULE,
            PACKING / "devtools" / "paper_figures.py",
            *(REPO / path for path in n11_threshold_figures.FIGURE_INPUTS),
            PACKING / "devtools" / "render_n11_optimality_review.py",
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
            # The front prints the paper's own version and dates, which are declared here.
            PACKING / "src" / "sqpack" / "release.py",
            # The certificate and the loader the figures and the register test read it through.
            PACKING / "src" / "sqpack" / "fractional" / "parent_core.py",
            # The retained evidence the paper cites and the figures draw from.
            ARCHIVE / "evidence/portable/RESULT.json",
            ARCHIVE / "evidence/portable/secondary/RESULT.json",
            RECEIPTS / "full-replay/RESULT.json",
            RECEIPTS / "independent-audit.json",
            PACKING / "resources/web/wand125-tools-2026-09-29/README.md",
            PACKING
            / "resources/web/wand125-tools-2026-09-29/receipts/n11-bound-full-summary.json",
            PACKING / "campaign/agent-sessions/session-153-native-full.json",
            PACKING / "campaign/agent-sessions/session-153-native-reconciliation.json",
            REPO / "vendor" / "kpress",
        )
    )
)


def version_history_markdown() -> str:
    """The paper's own editions, newest first, each with the day it was first published
    and what changed in the paper: `sqpack.release.THRESHOLD_REVIEW_HISTORY`."""
    return "\n".join(
        f"- **{entry.version} — {entry.first_published}.** {entry.result_scope}"
        for entry in THRESHOLD_REVIEW_HISTORY
    )


def render_all_figures() -> dict[str, str]:
    """The twelve figures, drawn from their hash-pinned inputs."""
    return dict(n11_threshold_figures.render_figures())


def render_all_facts() -> dict[str, str]:
    """What the captions and the prose say of the certificate that is data, from the
    module that draws the figures: each value is read from the hash-pinned file its
    figure is drawn from, so the article can name a number and cannot retype one."""
    facts = dict(n11_threshold_figures.caption_facts())
    if set(facts) != set(CAPTION_FACT_KEYS):
        missing = sorted(set(CAPTION_FACT_KEYS) - set(facts))
        extra = sorted(set(facts) - set(CAPTION_FACT_KEYS))
        raise ValueError(
            f"caption facts differ from the article's: missing {missing}, extra {extra}"
        )
    return facts


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
    """Every relative link pinned to a blob of the repository at `revision`; a link to a
    file that is not in the repository, or outside it, is refused."""
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


def refuse_screen_only_prose(markdown: str, *, source: Path) -> None:
    """A paper has no apparatus, so a sentence that tells its reader to hover or tap is
    wrong in every edition; it is refused rather than stripped, because the fix belongs
    in the article."""
    leaked = [line for line in markdown.split("\n") if ONLY_ON_SCREEN.search(line)]
    if leaked:
        joined = "\n  ".join(leaked[:5])
        raise ValueError(
            f"{source.name}: prose addresses a reader who has the page:\n  {joined}"
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
    """Fill the paper's front, the declared figure slots, the caption facts and the
    links to the other papers for `edition`, and pin local source citations to a Git
    commit. A fact the article does not use is refused, as a slot it does not fill is:
    the two lists are the article's and the figure module's alike."""
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
    refuse_screen_only_prose(source, source=article)
    # The links to the other papers are filled before the repository pinning, so a
    # sibling paper's page is never mistaken for a file of the repository.
    linked = paper_links.fill_paper_links(source, edition=edition)
    filled = _fill(
        linked,
        {**figures, **facts, "VERSION_HISTORY": version_history_markdown()},
        source=article,
    )
    return _repository_links(filled, source=article, revision=revision)


def page_meta() -> PageMeta:
    """Use the paper's credits and edition history for publication metadata."""
    return PageMeta(
        name=TITLE,
        description=DESCRIPTION,
        path=SITE_PATH,
        kind="article",
        published=paper_front.iso_date(THRESHOLD_REVIEW_HISTORY[-1].first_published),
        modified=paper_front.iso_date(paper_front.revised(FRONT)),
        **render_n11_lower_bounds_explainer.scholarly_metadata(
            FRONT,
            TITLE,
            paper_front.iso_date(THRESHOLD_REVIEW_HISTORY[-1].first_published),
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

    The page typesets the expanded article with page-relative links to the other papers;
    the edition is the same document with those links absolute, since it is read away
    from the site, and with its front in the Markdown edition's form
    (`paper_front.published`). The rest, the figures as their SVG among it, is kept
    whole."""
    from kpress.format.markdown import parse_markdown  # noqa: PLC0415

    page_markdown = expanded_markdown(
        source, figures=figures, article=article, revision=revision, facts=facts
    )
    edition_markdown = expanded_markdown(
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
    return page, paper_front.published(edition_markdown, FRONT)


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
    (`render_n11_lower_bounds_explainer_pdf.dated`).
    """
    from datetime import date  # noqa: PLC0415

    from playwright.sync_api import expect, sync_playwright  # noqa: PLC0415

    revised = date.fromisoformat(paper_front.iso_date(paper_front.revised(FRONT)))
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
            write_bytes_atomic(pdf_path, dated(drawn, revised))
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
