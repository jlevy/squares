"""Every page draws its text and its mathematics as the shared layers set them.

The explainer is the reference (`templates/paper-design.md`, Text and Math). The
optimality paper has its own renderer and shell, and its formulas once came out a sixth
lighter than the explainer's on macOS: its shell inlined the publication stylesheet,
whose math rule sets `text-rendering: geometricPrecision` and takes it back on macOS,
without the head script that tells the rule it is on macOS (think-jc3w). Nothing
compared the two pages, and no computed size, weight or face differed, so no check could
have named it.

This holds the pages to one another and to the layers, with `measure_site_pages glyphs`,
the measurement the difference was found with:

- no browser: the measurement's own arithmetic (ink, the weight a variable face is drawn
  at, the difference and summary tables, the problems it names) on fixed reports, and
  every shell that inlines the publication stylesheet to its head script;
- in Chromium: the paper against the explainer, property by property, and the same
  formula's ink on both; each paper told it is on macOS and told it is not, which is
  how the branch a runner would never take is run on it; a paper whose head script is
  taken out, which must be named; and every page against the values the shared tokens
  come to.

The pages are rendered and measured once, in module fixtures, so no test carries a
render or a page load in its own call time. The browser tests are skipped where no
Chromium can be launched; `SQPACK_CHROMIUM` names one the environment supplies, as the
other browser tools read it.
"""

from __future__ import annotations

import copy
import importlib
import io
import os
import re
import socket
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from kpress.format.markdown import parse_markdown
from PIL import Image

from devtools import measure_site_pages as measure
from devtools import render_n11_lower_bounds_explainer, render_overview, site_assets
from devtools import render_n11_optimality_review as paper
from devtools import render_n11_threshold_bound_review as threshold
from devtools.preview_site import serve
from devtools.render_n11_lower_bounds_explainer_pdf import BROWSER_OVERRIDE
from tests import site_renders

TEMPLATES = Path(render_n11_lower_bounds_explainer.__file__).with_name("templates")
#: The papers as this module writes them into one directory, each under its slug: the
#: explainer, the reference, and the two reviews, Part III (`PAPER`, the optimality
#: review, whose formulas once came out lighter) and Part II (`THRESHOLD`).
EXPLAINER, PAPER = "n11-lower-bounds-explainer.html", "n11-optimality-review.html"
THRESHOLD = "n11-threshold-bound-review.html"
#: Every paper of the site, in reading order, as written here.
PAPERS = (EXPLAINER, THRESHOLD, PAPER)
#: The figures each review draws (Part II's twelve, the series plan's §6.2).
REVIEW_FIGURES = {PAPER: 12, THRESHOLD: 12}
#: The site's own pages measured here: a long report, whose headings, tables and block
#: quotes hold formulas, and the homepage, whose cards, chips and tables do.
SITE_PAGES = ("tutorial.html", "index.html")
MAC, LINUX = "MacIntel", "Linux x86_64"
#: A formula both papers set in their prose, as the page's pipeline writes its TeX.
SHARED_FORMULA = r"s\mkern1mu(11)=T"
#: How far the same formula's ink may differ between the two papers. Measured at 0.2% or
#: less in four views; the difference this pins was 15 to 26%.
INK_TOLERANCE = 0.03
#: What each page is known to set off the shared layers, each a pattern over a problem
#: `glyph_problems` names and why it stands. All of them were found by this measurement
#: and are listed for the owner in think-jc3w; none is mathematics set off its text, and
#: anything not listed fails.
KNOWN: dict[str, dict[str, str]] = {
    PAPER: {
        r"figure label .*: drawn from .* \(host\)": (
            "the paper's diagrams label points with ≤, ≥, τ and subscripts as text, which "
            "Source Sans 3 does not carry, so the reader's machine draws them"
        ),
    },
    "tutorial.html": {
        r"(code block|inline code|other \(code in \.kpress-table\)) .*: drawn from .*host": (
            "mathematics written as code (≥, μ, Σ, √), in characters Planetaire Mono Text "
            "does not carry"
        ),
    },
    "index.html": {
        r"caption `The best packing known for .*`: 16.15px, not the role's 17.48\d*px": (
            "the homepage's hero caption is set at 0.85 of the sans base, written as a "
            "number in site.css, where every other caption is the note size, 0.92"
        ),
        r"other \(span in \.site-star\) `★`: drawn from .* \(host\)": (
            "the recent-bound star is a text character no shipped face carries"
        ),
    },
}
#: The site's sheets whose every rule that sets the sans face must set its weight. The
#: bar's own sheet, `site-nav.css`, is not among them: it is inlined in the explainer,
#: whose bytes this change leaves alone, and on every KPress page its three containers
#: already inherit the regular weight from KPress's header.
SANS_RULE_SHEETS = ("site.css", "site-result.css")
SANS_FAMILY = "font-family: var(--kpress-font-sans);"
SANS_WEIGHT = re.compile(
    r"font-weight: (var\(--site-font-weight-sans-(light|medium|bold)\)|inherit);"
)
#: The roles both papers set by one rule, compared on every property but colour, which
#: a link inside one changes. A paper's own emphasis and links are its prose's to choose,
#: and its diagrams' labels are its own figures'. These every paper has, so the
#: comparison cannot pass for want of anything to compare.
STRUCTURAL_ROLES = (
    "prose",
    "h2",
    "page title",
    "credits",
    "credits name",
    "caption",
    "caption lead",
    "footnote",
    "colophon",
    "source chip",
    "nav name",
    "nav link",
)
#: With them, the roles a paper's prose may or may not use, compared where both do.
SHARED_ROLES = (*STRUCTURAL_ROLES, "list item", "h3", "inline code")


def text_row(role: str, **changes: Any) -> dict[str, Any]:
    """One text sample as the probe reports it, the paper's prose unless changed."""
    row: dict[str, Any] = {
        "role": role,
        "family": "KPress Quotes",
        "weight": "400",
        "size": 18,
        "line_height": 27,
        "style": "normal",
        "color": "rgb(17 24 39)",
        "opacity": 1,
        "text_rendering": "auto",
        "smoothing": "auto",
        "synthesis": "weight style small-caps",
        "optical_sizing": "auto",
        "variation": "normal",
        "features": "normal",
        "letter_spacing": "normal",
        "transform": "none",
        "count": 1,
        "example": "Let",
        "drawn": "PTSerif-Regular",
        "host_faces": "",
    }
    return row | changes


def math_row(**changes: Any) -> dict[str, Any]:
    """One formula as the probe reports it, serif math in the prose unless changed."""
    row: dict[str, Any] = {
        "surface": "prose",
        "layout": "inline",
        "typeset": measure.TYPESET,
        "math": measure.SERIF_MATH,
        "glyphs": "KPress Math Text 400 italic",
        "weight": "400",
        "scale": 1,
        "text": "KPress Quotes",
        "text_weight": "400",
        "text_size": 18,
        "color": "rgb(17 24 39)",
        "text_color": "same",
        "opacity": 1,
        "text_rendering": "auto",
        "text_text_rendering": "auto",
        "smoothing": "auto",
        "synthesis": "weight style small-caps",
        "face_mark": "",
        "count": 1,
        "size": 18,
        "example": "n",
        "drawn": "KPress Math Text 400 italic: PTSerif-Italic",
        "host_faces": "",
        "ink": 0.1,
    }
    return row | changes


def entry(page: str = "paper.html", **changes: Any) -> dict[str, Any]:
    """One page's report as `measure_glyphs` returns it: a paper on macOS, set right."""
    found: dict[str, Any] = {
        "page": page,
        "width": 1280,
        "scheme": "light",
        "untypeset": 0,
        "font_requests": [],
        "failed_requests": [],
        "katex": "0.16.45",
        "platform": MAC,
        "publication": True,
        "reading": True,
        "sans": "Source Sans 3 Variable",
        "prose": "KPress Quotes",
        "root": {measure.NATIVE_METRICS: "true"},
        "tokens": {
            "--kpress-font-size-base": 18,
            "--kpress-font-size-h2": 21.6,
            "--kpress-font-weight-sans-regular": 410,
            "--paper-font-scale-sans": 1.0556,
            "--paper-font-weight-sans-medium": 550,
            "--paper-font-weight-sans-bold": 680,
            "--paper-title-scale": 1.5,
            "--paper-note-scale": 0.92,
            "--paper-colophon-scale": 0.85,
        },
        "text": [
            text_row("prose"),
            text_row("caption", family="Source Sans 3 Variable", weight="410", size=17.48),
        ],
        "math": [math_row()],
        "faces": [
            {
                "family": "PT Serif",
                "weight": "400",
                "style": "normal",
                "display": "block",
                "status": "loaded",
                "inlined": True,
                "faces": 1,
            }
        ],
    }
    return found | changes


def shot(*, ground: tuple[int, int, int], ink: tuple[int, int, int], covered: float) -> bytes:
    """A 40 by 20 shot whose middle 20 by 10 is `covered` of the way from the ground to
    the ink: 200 pixels of that coverage."""
    image = Image.new("RGB", (40, 20), ground)
    mixed = tuple(round(g + (i - g) * covered) for g, i in zip(ground, ink, strict=True))
    image.paste(mixed, (10, 5, 30, 15))
    out = io.BytesIO()
    image.save(out, format="PNG")
    return out.getvalue()


def test_ink_is_the_area_the_glyphs_cover_in_square_em() -> None:
    """Two hundred fully covered pixels at 10px and twice the scale are half a square em,
    on a light ground and on a dark one alike; the same pixels half covered are half of
    that, which is what a formula drawn thinner comes to."""
    black, white = (0, 0, 0), (255, 255, 255)
    full = measure.ink(
        shot(ground=white, ink=black, covered=1), color="rgb(0 0 0)", size=10, scale=2
    )
    assert full == 0.5
    dark = measure.ink(
        shot(ground=black, ink=white, covered=1), color="rgb(255 255 255)", size=10, scale=2
    )
    assert dark == 0.5
    thin = measure.ink(
        shot(ground=white, ink=black, covered=0.5), color="rgb(0 0 0)", size=10, scale=2
    )
    assert abs(thin - 0.25) < 0.005
    assert (
        measure.ink(shot(ground=white, ink=white, covered=1), color="rgb(0 0 0)", size=10) == 0
    )
    with pytest.raises(ValueError, match="not a colour"):
        measure.ink(shot(ground=white, ink=black, covered=1), color="black", size=10)


def test_a_platform_face_is_named_with_the_weight_it_is_drawn_at() -> None:
    """Blink names a variable face's instance by its weight in fixed point, which is the
    weight a run is drawn at and not only the one it asks for; a face the page did not
    ship is the reader's own."""
    face = measure._platform_face  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    sans = {"familyName": "Source Sans 3 ExtraLight", "isCustomFont": True}
    assert face(sans | {"postScriptName": "SourceSans3-Roman_wght19A0000"}) == (
        "SourceSans3-Roman@410"
    )
    assert face(sans | {"postScriptName": "SourceSans3-Italic_wght2A80000"}) == (
        "SourceSans3-Italic@680"
    )
    serif = {"familyName": "PT Serif", "postScriptName": "PTSerif-Italic", "isCustomFont": True}
    assert face(serif) == "PTSerif-Italic"
    host = {"familyName": "Times", "postScriptName": "Times-Roman", "isCustomFont": False}
    assert face(host) == "Times" + measure.HOST


def test_a_page_set_as_the_layers_define_has_no_problems() -> None:
    assert measure.glyph_problems(entry(), katex="0.16.45") == []
    site = entry("tutorial.html", publication=False, root={}, platform=LINUX)
    assert measure.glyph_problems(site, katex="0.16.45") == []
    # Off macOS the publication layer's own rule stands, and the flag stays off.
    linux = entry(root={}, platform=LINUX, math=[math_row(text_rendering="geometricprecision")])
    assert measure.glyph_problems(linux) == []


def test_checked_prepared_math_is_measured_without_a_browser_renderer() -> None:
    found = entry(prepared_katex="0.16.45", math=[math_row(prepared="yes")])
    assert measure.glyph_problems(found, katex="0.16.45") == []


@pytest.mark.parametrize("version", ["", "0.16.9", "0.16.45 / 0.16.9", "0.16.45 / 0.16.45"])
def test_prepared_math_requires_one_correct_renderer_version(version: str) -> None:
    found = entry(prepared_katex=version, math=[math_row(prepared="yes")])
    assert measure.glyph_problems(found, katex="0.16.45") == [
        f"the prepared math uses KaTeX {version or 'without provenance'}, not 0.16.45"
    ]


def test_prepared_metadata_cannot_stand_in_for_a_missing_runtime_renderer() -> None:
    found = entry(
        runtime_katex="",
        prepared_katex="0.16.45",
        math=[math_row(prepared="yes"), math_row(prepared="no")],
    )
    assert measure.glyph_problems(found, katex="0.16.45") == [
        "the page runs KaTeX not at all, not 0.16.45"
    ]


def test_a_paper_without_its_platform_flag_is_named_with_every_formula_it_draws() -> None:
    """The defect itself: on macOS the publication layer's flag is missing, so its math
    rule leaves every formula at `geometricPrecision` beside text at `auto`."""
    broken = entry(root={}, math=[math_row(text_rendering="geometricprecision")])
    assert measure.glyph_problems(broken) == [
        "the publication layer's platform flag is not set on MacIntel",
        "prose, inline formula `n`: text_rendering is geometricprecision, not auto",
    ]
    # Set where it should not be, the flag is named too: off macOS the prepared widths
    # need the linear advances the rule asks for.
    flagged = entry(platform=LINUX)
    assert measure.glyph_problems(flagged) == [
        "the publication layer's platform flag is set on Linux x86_64",
        "prose, inline formula `n`: text_rendering is auto, not geometricprecision",
    ]


@pytest.mark.parametrize(
    ("changes", "problem"),
    [
        ({"scale": 1.21}, "prose, inline formula `n`: scale is 1.21, not 1"),
        ({"weight": "300"}, "prose, inline formula `n`: weight is 300, not 400"),
        (
            {"math": measure.SANS_MATH, "weight": "400"},
            "prose, inline formula `n`: weight is 400, not 410",
        ),
        (
            {"text_color": "rgb(91 100 114)"},
            "prose, inline formula `n`: text_color is rgb(91 100 114), not same",
        ),
        (
            {"host_faces": "Times (host)"},
            "prose, inline formula `n`: host_faces is Times (host), not empty",
        ),
        (
            {"typeset": "no HTML + MathML"},
            f"prose, inline formula `n`: typeset is no HTML + MathML, not {measure.TYPESET}",
        ),
    ],
)
def test_a_formula_set_off_its_text_is_named(changes: dict[str, Any], problem: str) -> None:
    assert measure.glyph_problems(entry(math=[math_row(**changes)])) == [problem]


def test_text_off_the_shared_tokens_is_named() -> None:
    sans = "Source Sans 3 Variable"
    found = entry(
        text=[
            text_row("prose", size=16),
            text_row("caption", family=sans, weight="400", size=17.48, example="Figure 1."),
            text_row("nav link", family=sans, weight="550", size=16, example="Papers"),
            text_row("h3", family=sans, weight="550", size=21.6, host_faces=".SF NS (host)"),
            # A role in the other face is another rule's: the homepage's sans paragraphs.
            text_row("prose", family=sans, weight="410", size=17.48),
            # KPress's own table head keeps its 650.
            text_row("table head", family=sans, weight="650", size=16.2),
        ]
    )
    assert measure.glyph_problems(found) == [
        "prose `Let`: 16px, not the role's 18px",
        "caption `Figure 1.`: sans text at 400, which no token names",
        "caption `Figure 1.`: weight 400, not the role's 410",
        "nav link `Papers`: 16px, not the role's 17.4807px",
        "h3 `Let`: drawn from .SF NS (host)",
    ]
    # A page with no reading column, the workbench, is held to its formulas alone.
    assert measure.glyph_problems(found | {"reading": False}) == []


def test_a_face_of_the_shared_assets_is_shipped_and_not_fetched() -> None:
    """A face a site page fetches from its shared assets (`site_assets`) is one the page
    ships, as an inlined face is; any other fetch is still named."""
    face = {"family": "PT Serif", "weight": "400", "style": "normal", "display": "block"}
    shared = "http://127.0.0.1:1/assets/fonts/pt-serif-latin-400-normal.4271064a37f3ffc0.woff2"
    found = entry(
        font_requests=[shared, "http://127.0.0.1:1/fonts/pt-serif.woff2"],
        faces=[face | {"status": "loaded", "inlined": False, "shared": True, "faces": 1}],
    )
    assert measure.glyph_problems(found) == [
        "a face is fetched: http://127.0.0.1:1/fonts/pt-serif.woff2"
    ]


@pytest.mark.parametrize("family", ["Site Prose Georgia", "Site Prose Times"])
def test_an_unavailable_optional_local_prose_fallback_is_reported_without_font_failure(
    family: str,
) -> None:
    face = {
        "family": family,
        "weight": "400",
        "style": "normal",
        "display": "auto",
        "status": "error",
        "inlined": True,
        "shared": True,
        "optional_local": True,
        "faces": 1,
    }
    found = entry(faces=[face])
    assert measure.glyph_problems(found) == []
    assert measure.glyph_differences([entry(), found])[-1]["paper.html"] == (
        "auto, optional local, unavailable"
    )


@pytest.mark.parametrize("family", ["Site Prose Georgia", "PT Serif", "KaTeX_Main"])
def test_a_font_failure_without_verified_optional_local_sources_is_still_named(
    family: str,
) -> None:
    face = {
        "family": family,
        "weight": "400",
        "style": "normal",
        "display": "auto",
        "status": "error",
        "inlined": True,
        "shared": True,
        "optional_local": False,
        "faces": 1,
    }
    assert measure.glyph_problems(entry(faces=[face])) == [
        f"the face {family} 400 normal failed to load"
    ]


def test_a_page_that_fetches_or_fails_is_named() -> None:
    face = {"family": "KaTeX_Main", "weight": "400", "style": "normal", "display": "swap"}
    found = entry(
        untypeset=2,
        katex="0.16.9",
        font_requests=["https://example.org/a.woff2"],
        failed_requests=["https://example.org/a.woff2"],
        faces=[face | {"status": "error", "inlined": False, "faces": 1}],
    )
    assert measure.glyph_problems(found, katex="0.16.45") == [
        "2 formulas are left untypeset",
        "the page runs KaTeX 0.16.9, not 0.16.45",
        "a face is fetched: https://example.org/a.woff2",
        "a face failed to arrive: https://example.org/a.woff2",
        "the face KaTeX_Main 400 normal is neither inlined nor a shared asset",
        "the face KaTeX_Main 400 normal failed to load",
    ]


def test_the_difference_table_names_each_property_a_page_sets_differently() -> None:
    reference = entry(EXPLAINER)
    other = entry(
        root={},
        math=[math_row(text_rendering="geometricprecision"), math_row(surface="table cell")],
        text=[text_row("prose"), text_row("blockquote", size=17)],
    )
    assert measure.glyph_differences([reference, other]) == [
        {
            "width": 1280,
            "scheme": "light",
            "part": "math",
            "role": "prose, inline",
            "property": "text_rendering",
            EXPLAINER: "auto",
            "paper.html": "geometricprecision",
        },
        {
            "width": 1280,
            "scheme": "light",
            "part": "page",
            "role": "document",
            "property": measure.NATIVE_METRICS,
            EXPLAINER: "true",
            "paper.html": "-",
        },
    ]
    assert measure.glyph_differences([reference, copy.deepcopy(reference)]) == []


def test_the_summary_lists_each_roles_distinct_settings_with_their_pages() -> None:
    sans = "Source Sans 3 Variable"
    pages = [
        entry(EXPLAINER),
        entry("tutorial.html"),
        entry("index.html", text=[text_row("caption", family=sans, weight="410", size=16.15)]),
    ]
    rows = [row for row in measure.glyph_summary(pages) if row["role"] == "caption"]
    assert [(row["setting"], row["pages"]) for row in rows] == [
        (f"{sans} 410, 16.15/27", "index.html (1280)"),
        (f"{sans} 410, 17.48/27", f"{EXPLAINER} (1280), tutorial.html (1280)"),
    ]
    math = [row for row in measure.glyph_summary(pages) if row["part"] == "math"]
    assert [(row["role"], row["setting"]) for row in math] == [
        ("prose, inline", "KPress Math Text 400 at 1 of KPress Quotes 400, auto")
    ]


def test_every_shell_with_the_publication_stylesheet_carries_its_head_script() -> None:
    """The stylesheet's math rule reads the platform from an attribute its head script
    stamps, so a shell that names one names the other, in its head, where it runs before
    the body paints; and every paper takes the pair from one function."""
    shells = sorted(TEMPLATES.glob("*-shell.html"))
    assert {shell.name for shell in shells} >= {
        "n11-lower-bounds-explainer-shell.html",
        threshold.SHELL.name,
        paper.SHELL.name,
    }
    carrying = [shell for shell in shells if "{{PUBLICATION_CSS}}" in shell.read_text("utf-8")]
    assert {shell.name for shell in carrying} == {
        "n11-lower-bounds-explainer-shell.html",
        threshold.SHELL.name,
        paper.SHELL.name,
    }
    for shell in carrying:
        head = shell.read_text(encoding="utf-8").split("</head>", 1)[0]
        assert head.count("<style>{{PUBLICATION_CSS}}</style>") == 1, shell.name
        assert head.count("<script>{{NATIVE_MATH_METRICS}}</script>") == 1, shell.name
    layer = render_n11_lower_bounds_explainer.publication_layer()
    assert set(layer) == {"PUBLICATION_CSS", "NATIVE_MATH_METRICS"}
    assert measure.NATIVE_METRICS in layer["PUBLICATION_CSS"]
    name = measure.NATIVE_METRICS.removeprefix("data-")
    dataset = re.sub(r"-(\w)", lambda found: found.group(1).upper(), name)
    assert f"dataset.{dataset}" in layer["NATIVE_MATH_METRICS"]


def test_every_site_rule_that_sets_the_sans_face_sets_its_weight() -> None:
    """Weight is inherited and a face is not: a rule that sets the sans face and no
    weight leaves its text at the serif's 400, a step lighter than the sans's regular
    410 and lighter than the mathematics in it, which is always drawn at 410. Thirty-one
    rules did, among them a card's note, every popover, the table tools and the case
    records. So each rule that names the face names one of the three weights too."""
    for name in SANS_RULE_SHEETS:
        css = re.sub(r"/\*.*?\*/", "", (TEMPLATES / name).read_text("utf-8"), flags=re.DOTALL)
        rules = re.findall(r"([^{}]+)\{([^{}]*)\}", css)
        sans = [(selector, body) for selector, body in rules if SANS_FAMILY in body]
        assert sans, name
        for selector, body in sans:
            assert SANS_WEIGHT.search(body), f"{name}: {' '.join(selector.split())}"
    tokens = (TEMPLATES / "site.css").read_text(encoding="utf-8")
    assert "--site-font-weight-sans-light: var(--kpress-font-weight-sans-regular);" in tokens


def figure_row(**changes: Any) -> dict[str, Any]:
    """One figure as the probe reports it: a diagram of labels, centred, with a caption."""
    row: dict[str, Any] = {
        "page": PAPER,
        "width": 1280,
        "figure": 3,
        "drawing": "svg",
        "named": "n11-diagram",
        "drawings": 1,
        "drawing_width": 800,
        "column": 832,
        "offset": 0,
        "ink_offset": 0.01,
        "scrolls": False,
        "beside": False,
        "texts": 9,
        "longest": "Offsets inside each physical square",
        "share": 0.34,
        "sentences": "",
        "caption": "Figure 3. A schematic of one safe exclusion.",
    }
    return row | changes


def test_a_figure_set_as_the_papers_set_one_has_no_problems() -> None:
    assert measure.figure_problems(figure_row()) == []
    # A wide diagram scrolls sideways on a phone, and a figure with controls beside its
    # drawing centres the row: neither is held to the column's centre.
    assert measure.figure_problems(figure_row(offset=161, ink_offset=0.24, scrolls=True)) == []
    assert measure.figure_problems(figure_row(offset=-145.1, beside=True)) == []


@pytest.mark.parametrize(
    ("changes", "problem"),
    [
        ({"offset": -72}, "its drawing stands -72px off the centre"),
        # The first figure as it was: its box centred, the packing at the left of it.
        ({"ink_offset": -0.18}, "what it draws stands -18% of its width off the centre"),
        (
            {"longest": "Two routes to the exact optimum", "share": 0.72},
            "`Two routes to the exact optimum` is lettered across 72% of the drawing",
        ),
        (
            {"sentences": "Disk boundaries are open."},
            "a sentence is lettered into the drawing: Disk boundaries are open.",
        ),
        ({"caption": ""}, "no caption under it"),
    ],
)
def test_a_figure_off_the_papers_treatment_is_named(
    changes: dict[str, Any], problem: str
) -> None:
    assert measure.figure_problems(figure_row(**changes)) == [
        f"figure 3 (n11-diagram): {problem}"
    ]


# ---------- In Chromium ----------


@pytest.fixture(scope="module")
def chromium() -> None:
    """Skips the module's browser tests where no Chromium can be launched, before any
    page is rendered for them."""
    sync_api = pytest.importorskip("playwright.sync_api")
    with sync_api.sync_playwright() as driver:
        try:
            driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE)).close()
        except sync_api.Error as error:
            pytest.skip(f"no Chromium to launch: {error.message.splitlines()[0]}")


def test_the_probe_only_marks_exact_local_prose_fallback_sources_optional(
    chromium: None,  # noqa: ARG001
) -> None:
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    cases = [
        ("Site Prose Georgia", 'local("Georgia")', "400", "normal", "", True),
        (
            "Site Prose Times",
            'local("Times New Roman"), local("Liberation Serif")',
            "400",
            "normal",
            "",
            True,
        ),
        (
            "Site Prose Georgia",
            'local("Georgia"), url("/fonts/absent.woff2")',
            "400",
            "normal",
            "",
            False,
        ),
        ("Site Prose Times", 'local("Georgia")', "400", "normal", "", False),
        ("PT Serif", 'local("Georgia")', "400", "normal", "", False),
        ("Site Prose Georgia, malformed", 'local("Georgia")', "400", "normal", "", False),
        ("Site Prose Georgia", 'local("Georgia")', "700", "normal", "", False),
        ("Site Prose Georgia", 'local("Georgia")', "400", "italic", "", False),
        (
            "Site Prose Georgia",
            'local("Georgia")',
            "400",
            "normal",
            (
                '@font-face {font-family: "Site Prose Georgia";'
                ' src: url("/fonts/absent.woff2"); font-weight: 400; font-style: normal;}'
            ),
            False,
        ),
    ]
    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        try:
            page = browser.new_page()
            for family, src, weight, style, extra, optional in cases:
                page.set_content(
                    f'<style>@font-face {{font-family: "{family}"; src: {src};'
                    f" font-weight: {weight}; font-style: {style};}}{extra}</style>"
                )
                found = measure.read_glyphs(page)
                faces = found["faces"]
                assert faces, (family, src)
                assert all(face["optional_local"] is optional for face in faces), faces
        finally:
            browser.close()


@pytest.fixture(scope="module")
def site(chromium: None, tmp_path_factory: pytest.TempPathFactory) -> Path:  # noqa: ARG001
    """The two papers and the site's own pages, rendered once, in one directory, with
    the shared assets the site's pages link. The explainer is the unprepared page, which
    typesets in the client as the others do."""
    root = tmp_path_factory.mktemp("glyphs")
    explainer = render_n11_lower_bounds_explainer.render(
        render_n11_lower_bounds_explainer.WALKTHROUGH
    ).page
    (root / EXPLAINER).write_text(explainer, encoding="utf-8")
    html, _ = paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"),
        figures=paper.render_all_figures(),
        facts=paper.render_all_facts(),
        revision="a" * 40,
    )
    (root / PAPER).write_text(html, encoding="utf-8")
    # Part II, rendered as the optimality review is, by the renderer the site's registry
    # names for it.
    threshold = importlib.import_module(
        render_overview.paper_record(render_overview.N11_THRESHOLD_BOUND_REVIEW).module
    )
    threshold_html, _ = threshold.render(
        threshold.ARTICLE.read_text(encoding="utf-8"),
        figures=threshold.render_all_figures(),
        facts=threshold.render_all_facts(),
        revision="a" * 40,
    )
    (root / THRESHOLD).write_text(threshold_html, encoding="utf-8")
    script = render_n11_lower_bounds_explainer.publication_layer()["NATIVE_MATH_METRICS"]
    assert html.count(script) == 1
    (root / "unflagged.html").write_text(html.replace(script, ""), encoding="utf-8")
    site_renders.write(root, *SITE_PAGES)
    return root


@pytest.fixture(scope="module")
def served(site: Path) -> Iterator[str]:
    """That directory served, as `measure_site_pages` serves one it measures; the address,
    without its closing slash. A site page links its stylesheets, and a page opened from
    a file may not read the rules of a sheet it links, which the measurement does."""
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = int(probe.getsockname()[1])
    server = serve(site, port)
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        server.shutdown()
        server.server_close()


def measured(served: str, pages: tuple[str, ...], **options: Any) -> dict[str, dict[str, Any]]:
    """Each of `pages` as `measure_glyphs` reports it at a desktop width, by name."""
    report = measure.measure_glyphs(served, pages, widths=(1280,), every_ink=False, **options)
    return {found["page"]: found for found in report}


@pytest.fixture(scope="module")
def pages(served: str) -> dict[str, dict[str, Any]]:
    """Every page as this machine draws it."""
    return measured(served, (*PAPERS, *SITE_PAGES), tex=(SHARED_FORMULA,))


@pytest.fixture(scope="module")
def as_platform(served: str) -> dict[str, dict[str, dict[str, Any]]]:
    """The two papers, and the paper with its head script taken out, told they are on
    macOS and told they are not."""
    papers = (EXPLAINER, PAPER, "unflagged.html")
    return {platform: measured(served, papers, platform=platform) for platform in (MAC, LINUX)}


@pytest.mark.parametrize("review", [THRESHOLD, PAPER])
def test_the_paper_sets_every_shared_role_as_the_explainer_does(
    pages: dict[str, dict[str, Any]], review: str
) -> None:
    differences = [
        row
        for row in measure.glyph_differences([pages[EXPLAINER], pages[review]])
        if row["part"] == "text" and row["role"] in SHARED_ROLES and row["property"] != "color"
    ]
    assert differences == []
    for role in STRUCTURAL_ROLES:
        for name in (EXPLAINER, review):
            assert any(row["role"] == role for row in pages[name]["text"]), (name, role)


def test_the_papers_formulas_are_drawn_as_the_explainers_are(
    pages: dict[str, dict[str, Any]],
) -> None:
    """On every surface both papers set a formula on, and for the page as a whole: the
    typesetting, the faces, the weight, the scale against the text, the colour, and how
    the glyphs are rasterised. Then the same formula's ink, which is what thinner means."""
    differences = [
        row
        for row in measure.glyph_differences([pages[EXPLAINER], pages[PAPER]])
        if row["part"] in ("math", "page")
    ]
    assert differences == []
    ink = {
        name: [
            row["ink"]
            for row in pages[name]["math"]
            if row["compared"] and row["surface"] == "prose"
        ]
        for name in (EXPLAINER, PAPER)
    }
    assert len(ink[EXPLAINER]) == len(ink[PAPER]) == 1, ink
    assert abs(ink[PAPER][0] / ink[EXPLAINER][0] - 1) < INK_TOLERANCE, ink


@pytest.mark.parametrize("name", [EXPLAINER, PAPER])
@pytest.mark.parametrize("platform", [MAC, LINUX])
def test_a_paper_reads_its_platform_before_it_draws_a_formula(
    as_platform: dict[str, dict[str, dict[str, Any]]], platform: str, name: str
) -> None:
    """On macOS a formula is rasterised as the text around it is; elsewhere it takes the
    linear advances the publication layer asks for. Both papers, on both."""
    found = as_platform[platform][name]
    assert found["platform"] == platform
    assert found["root"].get(measure.NATIVE_METRICS) == ("true" if platform == MAC else None)
    wanted = "auto" if platform == MAC else "geometricprecision"
    assert {row["text_rendering"] for row in found["math"]} == {wanted}
    assert {row["text_text_rendering"] for row in found["math"]} == {"auto"}
    assert not [
        problem for problem in measure.glyph_problems(found) if "text_rendering" in problem
    ]


def test_a_paper_without_the_head_script_is_named_on_macos(
    as_platform: dict[str, dict[str, dict[str, Any]]],
) -> None:
    """The control: the paper as it was published, its stylesheet without its script.
    Told it is on macOS, every formula of it is named; off macOS nothing is, which is why
    no Linux runner saw it."""
    broken = as_platform[MAC]["unflagged.html"]
    problems = measure.glyph_problems(broken)
    assert "the publication layer's platform flag is not set on MacIntel" in problems
    lighter = [
        problem for problem in problems if "text_rendering is geometricprecision" in problem
    ]
    assert len(lighter) == len(broken["math"]) > 0
    elsewhere = measure.glyph_problems(as_platform[LINUX]["unflagged.html"])
    assert not [
        problem for problem in elsewhere if "text_rendering" in problem or "flag" in problem
    ]


@pytest.mark.parametrize("name", [*PAPERS, *SITE_PAGES])
def test_a_page_is_drawn_as_the_shared_layers_set_it(
    pages: dict[str, dict[str, Any]], name: str
) -> None:
    """Every formula at its text's size, colour and weight, from faces the page ships,
    rasterised as its text is; every role the shared layer sets at what its tokens come
    to; every sans run at a token's weight; nothing fetched."""
    problems = measure.glyph_problems(pages[name], katex=measure.shipped_katex())
    known = [re.compile(pattern) for pattern in KNOWN.get(name, {})]
    assert [found for found in problems if not any(k.match(found) for k in known)] == []
    # An exception that no longer matches anything has been fixed: take it out.
    assert [k.pattern for k in known if not any(k.match(found) for found in problems)] == []


@pytest.fixture(scope="module")
def figures(site: Path) -> list[dict[str, Any]]:
    """Every figure of every paper, at a desktop and a phone width."""
    return measure.measure_figures(site.as_uri(), PAPERS, widths=(1280, 390))


def test_every_paper_sets_every_figure_one_way(figures: list[dict[str, Any]]) -> None:
    """A figure is its drawing, centred in the column, with its caption under it as a
    `figcaption`. Nothing is lettered into a drawing but its labels: no title, no
    sentence, no run most of the drawing wide. A wide diagram scrolls sideways on a
    phone and an apparatus sets its controls beside its drawing; every other drawing
    stands on the column's centre within a pixel, and what it paints with it."""
    counted = {
        (name, width): sum(1 for row in figures if (row["page"], row["width"]) == (name, width))
        for name in PAPERS
        for width in (1280, 390)
    }
    for review, count in REVIEW_FIGURES.items():
        assert counted[(review, 1280)] == counted[(review, 390)] == count, review
    assert counted[(EXPLAINER, 1280)] == counted[(EXPLAINER, 390)] >= 7
    problems = [
        f"{row['page']} at {row['width']}: {problem}"
        for row in figures
        for problem in measure.figure_problems(row)
    ]
    assert problems == []
    # The check has something to hold: at a desktop width no figure of the paper scrolls,
    # so each of its twelve drawings is held to the centre.
    desktop = [row for row in figures if (row["page"], row["width"]) == (PAPER, 1280)]
    assert not [row["figure"] for row in desktop if row["scrolls"] or row["beside"]]
    assert all(abs(row["offset"]) <= measure.FIGURE_CENTRE_TOLERANCE for row in desktop)
    assert max(row["share"] for row in figures) <= measure.LETTERED_SHARE


def test_the_first_figure_is_the_drawing_alone_at_the_first_papers_width(
    figures: list[dict[str, Any]],
) -> None:
    """Both papers open on a packing: the drawing alone, with no lettering, at one width
    rule, centred, on a desktop and on a phone."""
    first = {(row["page"], row["width"]): row for row in figures if row["figure"] == 1}
    for width in (1280, 390):
        ours, reference = first[(PAPER, width)], first[(EXPLAINER, width)]
        assert ours["texts"] == reference["texts"] == 0, width
        assert ours["drawing_width"] == reference["drawing_width"], width
        assert ours["offset"] == reference["offset"] == 0, width
        assert abs(ours["ink_offset"]) <= 0.01, width
        assert ours["caption"].startswith("Figure 1."), width


@pytest.fixture(scope="module")
def fronts(site: Path) -> list[dict[str, Any]]:
    """The formats row and the credits of every paper, at a desktop and a phone width,
    as laid out."""
    return measure.measure_credits(site.as_uri(), PAPERS, widths=(1280, 390))


@pytest.mark.parametrize("width", [1280, 390])
def test_every_paper_lays_the_front_out_one_way(
    fronts: list[dict[str, Any]], width: int
) -> None:
    """Every paper writes its front from one record (`devtools.paper_front`), and the
    browser lays it out one way: the same three chips at the same size and weight; the
    credits one column the width of the page, every line at the regular weight with
    its names at the bold and its addresses at the regular; the grid's own gap between
    lines, a line's space more before the dates, before a review's own credits, which
    follow the proof it reviews, and before the series strip, whose lines name the
    other parts by title, each a link at the regular weight."""
    rows = {
        name: [row for row in fronts if (row["page"], row["width"]) == (name, width)]
        for name in PAPERS
    }
    chips = {
        name: [
            (r["text"], r["font_size"], r["weight"], r["block_size"])
            for r in found
            if r["part"] == "chip"
        ]
        for name, found in rows.items()
    }
    for name in PAPERS:
        assert chips[name] == chips[EXPLAINER], name
    assert [chip[0] for chip in chips[PAPER]] == ["MD", "PDF", "GITHUB"]
    lines_of = {
        name: [r for r in found if r["part"] == "credit"] for name, found in rows.items()
    }
    strip = len(PAPERS)
    assert len(lines_of[EXPLAINER]) == 4 + strip
    assert len(lines_of[PAPER]) == len(lines_of[THRESHOLD]) == 6 + strip
    regular, bold = "410", "680"
    reference = lines_of[EXPLAINER][0]
    for name, lines in lines_of.items():
        assert {line["weight"] for line in lines} == {regular}, name
        assert {line["font_size"] for line in lines} == {reference["font_size"]}, name
        assert {line["width_share"] for line in lines} == {reference["width_share"]}, name
        oversight, agents, version, dates = lines[-4 - strip : -strip]
        assert oversight["bold"] == bold
        assert oversight["links"] == f"{bold} (name)"
        assert set(agents["bold"].split()) == {bold}
        assert version["bold"] == ""
        assert dates["bold"] == ""
        assert dates["links"] == ""
        head, *others = lines[-strip:]
        assert {line["kind"] for line in (head, *others)} == {"series"}, name
        assert head["bold"] == head["links"] == "", name
        assert [line["links"] for line in others] == [regular] * (strip - 1), name
        assert {line["bold"] for line in others} == {""}, name
    for review in (THRESHOLD, PAPER):
        source, address = lines_of[review][:2]
        assert source["bold"] == bold
        assert address["bold"] == ""
        assert address["links"] == regular
    # The space between lines is the grid's gap, a fraction of a line; a line's space
    # more stands before the dates on every paper, before a review's own credits and
    # before the series strip.
    gaps = {name: [line["gap"] for line in lines] for name, lines in lines_of.items()}
    small = gaps[EXPLAINER][1]
    assert 0 < small < 0.3
    series = [small + 1, small, small]
    assert gaps[EXPLAINER] == pytest.approx([0, small, small, small + 1, *series], abs=0.05)
    for review in (THRESHOLD, PAPER):
        assert gaps[review] == pytest.approx(
            [0, small, small + 1, small, small, small + 1, *series], abs=0.05
        ), review


def test_the_pages_run_one_math_pipeline(pages: dict[str, dict[str, Any]]) -> None:
    """One KaTeX, the version KPress ships, and every formula typeset the same way."""
    assert {found["katex"] for found in pages.values()} == {measure.shipped_katex()}
    for name, found in pages.items():
        assert found["math"], name
        assert {row["typeset"] for row in found["math"]} == {measure.TYPESET}, name
        assert found["untypeset"] == 0, name
    for name in SITE_PAGES:
        assert pages[name]["prepared_katex"] == measure.shipped_katex()
        assert {row["prepared"] for row in pages[name]["math"]} == {"yes"}
        assert render_overview.MATH_SCRIPT.read_text(encoding="utf-8") not in (
            site_renders.served(name)
        )


@pytest.fixture(scope="module")
def prepared_controls(
    chromium: None,  # noqa: ARG001
    tmp_path_factory: pytest.TempPathFactory,
) -> Iterator[str]:
    """Real prepared formulas, and negative controls with a neighboring intact formula."""
    root = tmp_path_factory.mktemp("prepared-glyph-controls")
    body = parse_markdown("Inline $x$. Adjacent $y$.", title="Controls").html
    original = render_overview.static_content_page(
        body,
        meta=render_overview.PageMeta("Controls", "Prepared glyph controls.", "index.html"),
        current="overview",
    ).html
    one_math = re.search(r"<math\b.*?</math>", original, re.DOTALL)
    assert one_math is not None
    provenance = f'<meta name="site-math-katex" content="{measure.shipped_katex()}">'
    assert original.count(provenance) == 1
    variants = {
        "control.html": original,
        "missing.html": original.replace(one_math[0], "", 1),
        "duplicate.html": original.replace(one_math[0], one_math[0] * 2, 1),
        "unversioned.html": original.replace(provenance, ""),
        "body-version.html": original.replace(provenance, "").replace(
            "</body>", provenance + "</body>"
        ),
        "duplicate-version.html": original.replace(provenance, provenance * 2),
        "wrong-version.html": original.replace(
            provenance, provenance.replace(measure.shipped_katex(), "0.16.9")
        ),
    }
    for name, content in variants.items():
        (root / name).write_text(content, encoding="utf-8")
    for output, data in site_assets.shared().assets.referenced([original]).items():
        target = root / site_assets.ASSETS_DIR / output
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = int(sock.getsockname()[1])
    server = serve(root, port)
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.parametrize(
    ("name", "problem"),
    [
        ("control.html", None),
        ("missing.html", "typeset is KaTeX HTML, not KaTeX HTML + MathML"),
        ("duplicate.html", "typeset is KaTeX HTML + duplicate MathML, not KaTeX HTML + MathML"),
        ("unversioned.html", "prepared math uses KaTeX without provenance"),
        ("body-version.html", "prepared math uses KaTeX without provenance"),
        ("duplicate-version.html", "prepared math uses KaTeX 0.16.45 / 0.16.45"),
        ("wrong-version.html", "prepared math uses KaTeX 0.16.9"),
    ],
)
def test_prepared_probe_keeps_semantics_and_renderer_guards(
    prepared_controls: str, name: str, problem: str | None
) -> None:
    found = measured(prepared_controls, (name,))[name]
    assert found["untypeset"] == 0
    assert sum(row["count"] for row in found["math"]) == 2
    assert all(row["prepared"] == "yes" for row in found["math"])
    problems = measure.glyph_problems(found, katex=measure.shipped_katex())
    if problem is None:
        assert problems == []
    else:
        assert any(problem in item for item in problems), problems
        # A missing or duplicate subtree must fail even beside intact semantic math.
        if name in {"missing.html", "duplicate.html"}:
            assert (
                sum(row["count"] for row in found["math"] if row["typeset"] == measure.TYPESET)
                == 1
            )
