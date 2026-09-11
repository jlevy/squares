#!/usr/bin/env python3
"""Build the v1 slideshow candidate for the known-best atlas video.

Reads the repository record (composite-figure.json, manifest.json, the frontier
records, the per-n SVG renderings and the vendored fonts) and writes one
self-contained `index.html` that opens from file:// with no server and no network.

Deterministic: same inputs, same bytes. No timestamps, no git, no randomness.

    build_candidate.py [--repo PATH] [--out DIR] [--decimals 2|3] [--radical svg|text]
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
import sys
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path

import yaml

DEFAULT_REPO = Path(
    "/Users/levy/wrk/github/squares/.claude/worktrees/squares-viz-explanations-4ae624"
)
FIRST_N = 1
LAST_N = 324

# The packing occupies the 536x536 box at (36, 36) of every per-n rendering
# (`_append_packing_panel`, packing/src/sqpack/render/packing.py). Coordinates are
# re-based to that box so the slideshow's viewBox is the packing, not the canvas.
PANEL_ORIGIN = Decimal(36)
PANEL_SIDE = Decimal(536)

DEFAULT_DWELL = 1.5
DEFAULT_FADE = 0.5
SETTLE = 0.02

BASE36 = "0123456789abcdefghijklmnopqrstuvwxyz"

# ---- the poster's badge, copied number for number from build_known_best_atlas.py
# (`SUMMARY_BADGE_SIZE`, the `rx`/`stroke-width` in `_append_badge`,
# `SUMMARY_BADGE_FONT_SIZE`, `SUMMARY_STAR_POINTS`, `SUMMARY_STAR_INSET`,
# `SUMMARY_BADGE_STAR_SPAN`). The badge is drawn in its own 19-unit box and scaled
# as a whole by CSS, so every proportion is the poster's.
BADGE_SIZE = Decimal(19)
BADGE_RX = "4.5"
BADGE_STROKE = "1.2"
BADGE_FONT_SIZE = Decimal(15)
STAR_POINTS = (
    (Decimal(0), Decimal(-6)),
    (Decimal("1.411"), Decimal("-1.942")),
    (Decimal("5.706"), Decimal("-1.854")),
    (Decimal("2.283"), Decimal("0.742")),
    (Decimal("3.527"), Decimal("4.854")),
    (Decimal(0), Decimal("2.4")),
    (Decimal("-3.527"), Decimal("4.854")),
    (Decimal("-2.283"), Decimal("0.742")),
    (Decimal("-5.706"), Decimal("-1.854")),
    (Decimal("-1.411"), Decimal("-1.942")),
)
STAR_INSET = Decimal(6)
STAR_SPAN = Decimal("0.92")
# The poster's colours (sqpack.render.style PAPER_THEME).
BADGE_MUTED = "#5c6673"
BADGE_PAPER = "#ffffff"
# The open-question badge is this candidate's one addition: the same box, outlined
# and lettered in a grey lighter than the poster's muted, so it reads as quieter.
BADGE_FAINT = "#9ca5ae"
# The glyph in a badge is set at the poster's 15 units. Source Sans 3 (the panel's
# own sans, embedded) supplies O, =, R and ?, instanced at weight 650 as the poster
# asks for; KaTeX_Main supplies ≈, which the latin subset does not carry, at a
# smaller size because its wave is wider than Source Sans's equals. The outlines
# are extracted at build time and drawn as paths, so the badge depends on no font
# at view time.
BADGE_WEIGHT = 650
APPROX_FONT_SIZE = Decimal(13)
APPROX_STROKE_UNITS = Decimal(26)  # thickens KaTeX's regular-weight wave to match
# (glyph, style) as the record writes them -> symbol id. Nothing else is a badge.
BADGE_IDS = {
    ("O", "solid"): "badge-o",
    ("=", "solid"): "badge-eq",
    ("≈", "muted"): "badge-approx",
    ("R", "solid"): "badge-r",
    ("R", "muted"): "badge-r-muted",
}
STAR_ID = "badge-star"
OPEN_ID = "badge-open"
# What each badge row says, in a word or two. The record's `meaning` ("proved
# optimal", "exact value known") is longer and is kept for the spoken mirror.
BADGE_LABELS = {
    ("O", "solid"): "optimal",
    ("=", "solid"): "exact",
    ("≈", "muted"): "numerical",
    ("R", "solid"): "rigid",
    ("R", "muted"): "rigid (catalogue)",
}
STAR_LABEL = "new lower bound"
# The open group's rows: what the record has not yet proved, found or established.
OPEN_LABELS = ("optimality", "exact value", "rigidity")

# ---- the type scale. Four sizes on the stage and nothing smaller than the first,
# so the panel reads at video resolution: 28 for the small-caps notes, the open
# group's heading, the record block, the footer and the progress bar's numbers; 34
# for the `n =` line and the badge and open rows; 44 for the three value lines; 96
# for the numeral, set in PT Serif Regular. The numeral is 3.4 times the smallest.
TYPE_SCALE = (28, 34, 44, 96)
SMALL, MEDIUM, LARGE, NUMERAL_SIZE = TYPE_SCALE
# Scarlet means new. It is written once, on the new-lower-bound row; the star in
# that row is drawn in currentColor and takes the colour from its label.
NEW_COLOR = "#a3123f"
# Selectors outside the stage (the review chrome), which the type-scale rule does
# not cover. Every other rule in the CSS styles stage text.
CHROME_SELECTORS = (
    "html",
    "body",
    "#app",
    "#controls",
    "#readout",
    "#length",
    ".hint",
    ".visually-hidden",
)

FONT_DIR = Path("vendor/kpress/src/kpress/format/static/fonts")
KATEX_FONT_DIR = Path("vendor/kpress/src/kpress/format/static/katex/fonts")

# (family, style, weight, file). The families and files are the ones
# style-tokens.css declares, less the two PT Serif 700 faces: nothing on the stage
# is set bold in the serif (the numeral is Regular), so they are not embedded and
# the test's font list (`FACES`) does not expect them. "Atlas Symbols" is this
# candidate's name for the KaTeX_Main-Regular face restricted to the relation and
# radical code points the latin subsets of PT Serif and Source Sans do not carry
# (checked with fontTools).
FONT_FACES = (
    ("PT Serif", "normal", "400", FONT_DIR / "pt-serif-latin-400-normal.woff2"),
    ("PT Serif", "italic", "400", FONT_DIR / "pt-serif-latin-400-italic.woff2"),
    (
        "Source Sans 3 Variable",
        "normal",
        "200 900",
        FONT_DIR / "source-sans-3-latin-wght-normal.woff2",
    ),
    (
        "Source Sans 3 Variable",
        "italic",
        "200 900",
        FONT_DIR / "source-sans-3-latin-wght-italic.woff2",
    ),
    ("Atlas Symbols", "normal", "400", KATEX_FONT_DIR / "KaTeX_Main-Regular.woff2"),
)

# The latin unicode-range style-tokens.css gives the PT Serif and Source Sans faces.
LATIN_RANGE = (
    "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, "
    "U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, "
    "U+FEFF, U+FFFD"
)
# Relations, the radical, approximately, element-of and the floor/ceiling brackets.
SYMBOL_RANGE = "U+2208, U+221A, U+2248, U+2264-2265, U+2308-230B"

# KaTeX's `sqrtMain` path (svgGeometry.js) with extraVinculum 0 and hLinePad 80,
# resolved from the vendored katex.min.js. It is the outline of U+221A in
# KaTeX_Main with the vinculum drawn as part of the path across a 400000-unit-wide
# viewBox, so the rule and the surd are one shape and cannot misalign. KaTeX is
# MIT-licensed; the glyph comes from the KaTeX fonts (SIL OFL).
SQRT_MAIN_PATH = (
    "M95,702 c-2.7,0,-7.17,-2.7,-13.5,-8c-5.8,-5.3,-9.5,-10,-9.5,-14 "
    "c0,-2,0.3,-3.3,1,-4c1.3,-2.7,23.83,-20.7,67.5,-54 "
    "c44.2,-33.3,65.8,-50.3,66.5,-51c1.3,-1.3,3,-2,5,-2c4.7,0,8.7,3.3,12,10 "
    "s173,378,173,378c0.7,0,35.3,-71,104,-213c68.7,-142,137.5,-285,206.5,-429 "
    "c69,-144,104.5,-217.7,106.5,-221 l0 -0 c5.3,-9.3,12,-14,20,-14 "
    "H400000v40H845.2724 s-225.272,467,-225.272,467s-235,486,-235,486c-2.7,4.7,-9,7,-19,7 "
    "c-6,0,-10,-1,-12,-3s-194,-422,-194,-422s-65,47,-65,47z M834 80h400000v40h-400000z"
)

CONSTRUCTION_LABELS = {
    "trivial-grid": "trivial grid",
    "simulated-annealing": "simulated annealing",
    "hand-construction": "hand construction",
    "extension": "extension",
    "diagonal-strip": "diagonal strip",
    "composition": "composition",
    "unknown": "not recorded",
}

# The kind of a lower-bound argument, printed after its author and year. The
# `nagamochi` kind does not repeat the name: 289 of the 324 rows are his, and at
# 28px "Hiroshi Nagamochi, 2005 (general bound)" is the one spelling that fits.
LOWER_KIND_LABELS = {
    "nagamochi": "general bound",
    "perfect-square": "perfect square",
    "unavoidable-points": "unavoidable points",
    "counting": "counting argument",
    "monotonicity": "monotonicity",
}

SOURCE_LABELS = {
    "[Kingbird]": "Kingbird catalogue",
    "[UnitSquare 2026]": "UnitSquare project, 2026",
}


# --------------------------------------------------------------------------- record


def read_composite(repo: Path) -> dict[int, dict]:
    doc = json.loads((repo / "packing/atlas/known-best/composite-figure.json").read_text())
    entries = {e["n"]: e for e in doc["figure"]["entries"]}
    assert sorted(entries) == list(range(FIRST_N, LAST_N + 1)), "composite range"
    return entries


def read_manifest(repo: Path) -> dict[int, dict]:
    doc = json.loads((repo / "packing/atlas/known-best/manifest.json").read_text())
    entries = {e["n"]: e for e in doc["atlas"]["entries"]}
    assert sorted(entries) == list(range(FIRST_N, LAST_N + 1)), "manifest range"
    return entries


FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def read_frontier(repo: Path, n: int) -> dict:
    text = (repo / f"packing/frontier/n-{n:03d}.md").read_text()
    match = FRONTMATTER.match(text)
    assert match, f"frontier n={n}: no frontmatter"
    packing = yaml.safe_load(match.group(1))["packing"]
    assert packing["n"] == n
    return packing


# ------------------------------------------------------------------------- geometry

POLYGON = re.compile(r'<polygon data-feature="square-fill"(.*?)/>', re.DOTALL)
POINTS = re.compile(r'points="([^"]+)"')
FILL = re.compile(r'fill="(#[0-9a-fA-F]{6})"')
CONTAINER = re.compile(
    r'<rect data-feature="container-outline" x="([^"]+)" y="([^"]+)" '
    r'width="([^"]+)" height="([^"]+)"'
)


def make_rounder(decimals: int):
    quantum = Decimal(1).scaleb(-decimals)

    def coordinate(raw: str) -> str:
        value = (Decimal(raw) - PANEL_ORIGIN).quantize(quantum, rounding=ROUND_HALF_EVEN)
        if value == 0:
            value = Decimal(0)  # never "-0"
        text = format(value, "f")
        if "." in text:
            text = text.rstrip("0").rstrip(".")
        return text or "0"

    return coordinate


def extract_geometry(svg_text: str, n: int, coordinate) -> tuple[list[str], list[str]]:
    """Per square: the rounded, re-based `points` string and the fill colour."""
    match = CONTAINER.search(svg_text)
    assert match, f"n={n}: container rect missing"
    x, y, w, h = (Decimal(v) for v in match.groups())
    assert x == PANEL_ORIGIN, f"n={n}: container origin {x},{y}"
    assert y == PANEL_ORIGIN, f"n={n}: container origin {x},{y}"
    assert abs(w - PANEL_SIDE) < Decimal("0.01"), f"n={n}: container side {w}x{h}"
    assert abs(h - PANEL_SIDE) < Decimal("0.01"), f"n={n}: container side {w}x{h}"
    polygons: list[str] = []
    fills: list[str] = []
    for attrs in POLYGON.findall(svg_text):
        points = POINTS.search(attrs).group(1).split()
        assert len(points) == 4, f"n={n}: polygon with {len(points)} points"
        corners = []
        for pair in points:
            px, py = pair.split(",")
            corners.append(coordinate(px) + "," + coordinate(py))
        polygons.append(" ".join(corners))
        fills.append(FILL.search(attrs).group(1).lower())
    assert len(polygons) == n, f"n={n}: {len(polygons)} fill polygons"
    return polygons, fills


# ----------------------------------------------------------------- exact-form maths

TOKEN = re.compile(r"\s*(sqrt\(|\d+|[()+\-/])")


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    pos = 0
    while pos < len(text):
        match = TOKEN.match(text, pos)
        if not match:
            if text[pos:].strip() == "":
                break
            raise ValueError(f"exact form: cannot tokenize {text!r} at {pos}")
        tokens.append(match.group(1))
        pos = match.end()
    return tokens


def parse_exact_form(text: str):
    """Parse the record's `exact_form` grammar into a small tree.

    expr    := product (('+' | '-') product)*
    product := factor factor*            (juxtaposition multiplies: `4 sqrt(2)`)
    factor  := atom ('/' atom)?
    atom    := INT | '(' expr ')' | 'sqrt(' expr ')'
    """
    tokens = tokenize(text)
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def take():
        nonlocal pos
        token = tokens[pos]
        pos += 1
        return token

    def expect(token):
        got = take()
        if got != token:
            raise ValueError(f"exact form {text!r}: expected {token} got {got}")

    def expr():
        terms = [(1, product())]
        while peek() in ("+", "-"):
            sign = 1 if take() == "+" else -1
            terms.append((sign, product()))
        return terms[0][1] if len(terms) == 1 else ("sum", terms)

    def product():
        factors = [factor()]
        while peek() is not None and (peek() == "sqrt(" or peek() == "(" or peek().isdigit()):
            factors.append(factor())
        return factors[0] if len(factors) == 1 else ("prod", factors)

    def factor():
        left = atom()
        if peek() == "/":
            take()
            return ("frac", left, atom())
        return left

    def atom():
        token = take()
        if token.isdigit():
            return ("int", int(token))
        if token == "(":
            inner = expr()
            expect(")")
            return ("paren", inner)
        if token == "sqrt(":
            inner = expr()
            expect(")")
            return ("sqrt", inner)
        raise ValueError(f"exact form {text!r}: unexpected {token}")

    tree = expr()
    if pos != len(tokens):
        raise ValueError(f"exact form {text!r}: trailing tokens")
    return tree


def evaluate(node) -> float:
    kind = node[0]
    if kind == "int":
        return float(node[1])
    if kind == "frac":
        return evaluate(node[1]) / evaluate(node[2])
    if kind == "paren":
        return evaluate(node[1])
    if kind == "sqrt":
        return evaluate(node[1]) ** 0.5
    if kind == "prod":
        result = 1.0
        for factor in node[1]:
            result *= evaluate(factor)
        return result
    if kind == "sum":
        return sum(sign * evaluate(term) for sign, term in node[1])
    raise ValueError(kind)


def sqrt_depth(node) -> int:
    kind = node[0]
    if kind == "int":
        return 0
    if kind == "frac":
        return max(sqrt_depth(node[1]), sqrt_depth(node[2]))
    if kind == "paren":
        return sqrt_depth(node[1])
    if kind == "sqrt":
        return 1 + sqrt_depth(node[1])
    if kind == "prod":
        return max(sqrt_depth(f) for f in node[1])
    if kind == "sum":
        return max(sqrt_depth(t) for _, t in node[1])
    raise ValueError(kind)


def render_math(node, radical: str) -> str:  # noqa: PLR0911
    # One return per node kind: the grammar has nine, and a dispatch table would put
    # the recursion behind a layer without making the cases easier to read.
    kind = node[0]
    if kind == "int":
        return str(node[1])
    if kind == "frac":
        return (
            '<span class="frac"><span class="num">'
            + render_math(node[1], radical)
            + '</span><span class="den">'
            + render_math(node[2], radical)
            + "</span></span>"
        )
    if kind == "paren":
        if node[1][0] == "frac":
            return render_math(node[1], radical)
        return "(" + render_math(node[1], radical) + ")"
    if kind == "sqrt":
        inner = render_math(node[1], radical)
        if radical == "text":
            if node[1][0] in ("int", "frac"):
                return "√" + inner
            return "√(" + inner + ")"
        tall = " tall" if sqrt_depth(node[1]) > 0 else ""
        return (
            f'<span class="sqrt{tall}"><svg class="surd" viewBox="0 0 400000 1080" '
            'preserveAspectRatio="xMinYMin slice" aria-hidden="true"><use href="#surd"></use>'
            '</svg><span class="radicand">' + inner + "</span></span>"
        )
    if kind == "prod":
        return "".join(render_math(f, radical) for f in node[1])
    if kind == "sum":
        parts = []
        for index, (sign, term) in enumerate(node[1]):
            if index == 0:
                # U+2212 MINUS SIGN, the typographic minus the page sets: RUF001's
                # hyphen-minus would be a different glyph in the rendered formula.
                parts.append(
                    ("−" if sign < 0 else "") + render_math(term, radical)  # noqa: RUF001
                )
            else:
                op = "−" if sign < 0 else "+"  # noqa: RUF001
                parts.append(f'<span class="op">{op}</span>' + render_math(term, radical))
        return "".join(parts)
    raise ValueError(kind)


def render_math_plain(node) -> str:
    kind = node[0]
    if kind == "int":
        return str(node[1])
    if kind == "frac":
        return render_math_plain(node[1]) + "/" + render_math_plain(node[2])
    if kind == "paren":
        return "(" + render_math_plain(node[1]) + ")"
    if kind == "sqrt":
        return "sqrt(" + render_math_plain(node[1]) + ")"
    if kind == "prod":
        return " ".join(render_math_plain(f) for f in node[1])
    if kind == "sum":
        out = ""
        for index, (sign, term) in enumerate(node[1]):
            if index == 0:
                out = ("-" if sign < 0 else "") + render_math_plain(term)
            else:
                out += (" - " if sign < 0 else " + ") + render_math_plain(term)
        return out
    raise ValueError(kind)


# ----------------------------------------------------------------------- badges


def fmt_units(value: Decimal, places: int = 3) -> str:
    text = format(value.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_EVEN), "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return "0" if text in ("", "-0") else text


def badge_glyph_outlines(repo: Path) -> dict[str, tuple[str, Decimal, Decimal, Decimal]]:
    """glyph -> (SVG path in font units, advance, ink yMin, ink yMax).

    Source Sans 3 Variable is instanced at `BADGE_WEIGHT` for O, =, R and ?; the
    KaTeX_Main face gives ≈. Outline coordinates are rounded to a tenth of a font
    unit, so the emitted paths are the same bytes on every build.
    """
    # fontTools is imported here rather than at the top: it is needed only when the
    # badge glyphs are traced, and importing it re-enables the GIL on this build of
    # Python. PLC0415 is waived for that reason, not overlooked.
    from fontTools.pens.boundsPen import BoundsPen  # noqa: PLC0415
    from fontTools.pens.svgPathPen import SVGPathPen  # noqa: PLC0415
    from fontTools.ttLib import TTFont  # noqa: PLC0415
    from fontTools.varLib.instancer import instantiateVariableFont  # noqa: PLC0415

    def ntos(value: float) -> str:
        return format(round(value, 1), "g")

    def outline(font: TTFont, char: str) -> tuple[str, Decimal, Decimal, Decimal]:
        glyph_set = font.getGlyphSet()
        name = font.getBestCmap()[ord(char)]
        pen = SVGPathPen(glyph_set, ntos=ntos)
        glyph_set[name].draw(pen)
        bounds = BoundsPen(glyph_set)
        glyph_set[name].draw(bounds)
        _x0, y0, _x1, y1 = bounds.bounds
        return (
            pen.getCommands(),
            Decimal(glyph_set[name].width),
            Decimal(str(round(y0, 1))),
            Decimal(str(round(y1, 1))),
        )

    sans = instantiateVariableFont(
        TTFont(repo / FONT_DIR / "source-sans-3-latin-wght-normal.woff2"),
        {"wght": BADGE_WEIGHT},
    )
    assert sans["head"].unitsPerEm == 1000
    katex = TTFont(repo / KATEX_FONT_DIR / "KaTeX_Main-Regular.woff2")
    assert katex["head"].unitsPerEm == 1000
    cap_height = Decimal(sans["OS/2"].sCapHeight)
    outlines = {char: outline(sans, char) for char in "O=R?"}
    outlines["≈"] = outline(katex, "≈")
    outlines["cap"] = ("", cap_height, Decimal(0), Decimal(0))
    return outlines


def badge_symbols(outlines: dict[str, tuple[str, Decimal, Decimal, Decimal]]) -> str:
    """The seven badges as `<symbol>`s in the poster's 19-unit box.

    Glyph placement follows `_append_badge` and `_badge_baseline`: a letter is
    centred on its cap height, so its baseline is half a cap below the box's middle;
    a math symbol is centred on its own ink. Both are centred horizontally on the
    advance width, as `text-anchor: middle` does.
    """
    half = BADGE_SIZE / 2
    cap_height = outlines["cap"][1]

    def glyph_path(char: str, fill: str) -> str:
        d, advance, y0, y1 = outlines[char]
        size = APPROX_FONT_SIZE if char == "≈" else BADGE_FONT_SIZE
        k = size / 1000
        if char.isalpha() or char == "?":
            baseline = (BADGE_SIZE + cap_height * k) / 2
        else:
            baseline = half + (y0 + y1) / 2 * k
        tx = half - advance * k / 2
        stroke = ""
        if char == "≈":
            stroke = (
                f' stroke="{fill}" stroke-width="{fmt_units(APPROX_STROKE_UNITS)}"'
                ' stroke-linejoin="round"'
            )
        return (
            f'<path d="{d}" fill="{fill}"{stroke} '
            f'transform="translate({fmt_units(tx)} {fmt_units(baseline)}) '
            f'scale({fmt_units(k, 4)} -{fmt_units(k, 4)})"/>'
        )

    def box(fill: str, stroke: str) -> str:
        return (
            f'<rect x="0" y="0" width="{fmt_units(BADGE_SIZE)}" '
            f'height="{fmt_units(BADGE_SIZE)}" '
            f'rx="{BADGE_RX}" fill="{fill}" stroke="{stroke}" stroke-width="{BADGE_STROKE}"/>'
        )

    symbols = []
    for (glyph, style), ident in BADGE_IDS.items():
        if style == "solid":
            body = box(BADGE_MUTED, "none") + glyph_path(glyph, BADGE_PAPER)
        else:
            body = box("none", BADGE_MUTED) + glyph_path(glyph, BADGE_MUTED)
        symbols.append(f'<symbol id="{ident}">{body}</symbol>')
    scale = BADGE_SIZE * STAR_SPAN / (STAR_INSET * 2)
    points = " ".join(
        f"{fmt_units(half + dx * scale)},{fmt_units(half + dy * scale)}"
        for dx, dy in STAR_POINTS
    )
    symbols.append(
        f'<symbol id="{STAR_ID}"><polygon points="{points}" fill="currentColor"/></symbol>'
    )
    symbols.append(
        f'<symbol id="{OPEN_ID}">'
        + box("none", BADGE_FAINT)
        + glyph_path("?", BADGE_FAINT)
        + "</symbol>"
    )
    return "".join(symbols)


def badge_svg(ident: str) -> str:
    # One unit of margin on every side keeps the outlined box's stroke inside the view.
    return (
        f'<svg class="badge" viewBox="-1 -1 21 21" aria-hidden="true">'
        f'<use href="#{ident}"></use></svg>'
    )


# -------------------------------------------------------------------- facts panel

SIDE_DISPLAY = re.compile(r"^s\((\d+)\) ([=≤≥]) (.+)$")


def function_line(n: int, relation: str, value: str) -> str:
    return (
        f'<span class="fn"><i>s</i><span class="arg">({n})</span></span>'
        f'<span class="rel">{relation}</span>'
        f'<span class="val">{html.escape(value)}</span>'
    )


def join_names(names: list[str]) -> str:
    names = [html.escape(name, quote=False) for name in names]
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]


def strip_scheme(url: str) -> str:
    return re.sub(r"^https?://", "", url)


def build_facts(n: int, entry: dict, manifest: dict, frontier: dict, radical: str):
    """Return (template html, aria text, source url or None) for one case."""
    side = entry["side"]
    match = SIDE_DISPLAY.match(side["display"])
    assert match, f"n={n}: side display {side['display']!r}"
    assert int(match.group(1)) == n, f"n={n}: side display {side['display']!r}"
    relation, side_value = match.group(2), match.group(3)
    assert (relation == "=") == (side["relation"] == "equality"), f"n={n}: relation"

    lower = entry["lower"]
    lower_value = None
    if lower["shown"]:
        lmatch = SIDE_DISPLAY.match(lower["display"])
        assert lmatch, f"n={n}: lower display"
        assert lmatch.group(2) == "≥", f"n={n}: lower display"
        lower_value = lmatch.group(3)

    exactness = entry["exactness"]
    exact_html = ""
    exact_plain = ""
    exact_depth = 0
    if exactness["exact_form"] is not None:
        tree = parse_exact_form(exactness["exact_form"])
        numeric = evaluate(tree)
        recorded = float(side["value"])
        assert abs(numeric - recorded) <= 1e-9 * max(1.0, recorded), (
            f"n={n}: exact form {exactness['exact_form']!r} evaluates to {numeric}, "
            f"record says {recorded}"
        )
        if tree[0] != "int":  # a bare integer duplicates the side line
            exact_html = render_math(tree, radical)
            exact_plain = render_math_plain(tree)
            exact_depth = sqrt_depth(tree)
    degree = exactness["degree"]
    degree_html = ""
    if degree is not None and degree >= 2:
        degree_html = f'<span class="degree">algebraic degree {degree}</span>'

    # Status badges exactly as the poster's `_case_badges` assembles them: the star
    # from lower.first_proved_here first, then badges[] in record order, each drawn
    # with the poster's glyph and style. (symbol id, css class, label, meaning)
    labels: list[tuple[str, str, str, str]] = []
    if lower["first_proved_here"]:
        labels.append((STAR_ID, "star", STAR_LABEL, "lower bound first proved here"))
    for badge in entry["badges"]:
        key = (badge["glyph"], badge["style"])
        assert key in BADGE_IDS, f"n={n}: badge {key!r} is not one the poster draws"
        labels.append((BADGE_IDS[key], badge["style"], BADGE_LABELS[key], badge["meaning"]))
    assert len(labels) <= 3, f"n={n}: {len(labels)} badges"

    # What the record leaves open for this n, from the same three fields the badges
    # are derived from: optimality not proved, exact value not known, rigidity not
    # established, each named by the thing that is open.
    open_items: list[str] = []
    if entry["optimality"]["status"] == "open":
        open_items.append(OPEN_LABELS[0])
    if exactness["state"] not in ("closed-form", "minimal-polynomial"):
        open_items.append(OPEN_LABELS[1])
    if entry["rigidity"]["state"] == "not-established":
        open_items.append(OPEN_LABELS[2])
    assert len(open_items) <= 3, f"n={n}: {len(open_items)} open items"
    assert len(labels) + max(len(open_items), 1) <= 4, f"n={n}: status rows"

    # Record-only facts from the frontier record and the atlas manifest.
    upper = frontier["reported_upper_bound"]
    rows: list[tuple[str, str, str]] = []  # (label, html, plain)
    construction = CONSTRUCTION_LABELS[upper["construction_method"]]
    rows.append(("Construction", construction, construction))
    if upper["found_by"] or upper["found_year"] is not None:
        who = join_names(upper["found_by"])
        year = "" if upper["found_year"] is None else str(upper["found_year"])
        text = ", ".join(part for part in (who, year) if part)
        rows.append(("Found", text, text))
    if upper["improved_by"]:
        text = join_names(upper["improved_by"])
        rows.append(("Improved", text, text))
    if lower_value is not None:
        reported_lower = frontier["reported_lower_bound"]
        who = join_names(reported_lower["proved_by"])
        proved_year = reported_lower["proved_year"]
        year = "" if proved_year is None else str(proved_year)
        kind = LOWER_KIND_LABELS.get(reported_lower["kind"], reported_lower["kind"])
        pieces = [p for p in (who, year) if p]
        text = kind if not pieces else f"{', '.join(pieces)} ({kind})"
        rows.append(("Lower bound", text, text))
    # No minimal-polynomial row: at 28px the shortest that printed (n = 302, 38
    # characters) takes two lines and its label alone is 309px wide; the degree
    # note under the exact line carries what the row would add.
    source_label = SOURCE_LABELS.get(upper["source_key"], upper["source_key"].strip("[]"))
    source_url = manifest["source"].get("url")
    if not source_url:
        for resource in frontier["resources"]:
            if resource["role"] == "record-catalogue" and resource.get("url"):
                source_url = resource["url"]
                break
    source_bits = [html.escape(source_label, quote=False)]
    if upper["catalogue_pictured"]:
        source_bits.append("pictured")
    source_html = ", ".join(source_bits)
    rows.append(("Source", source_html, source_label))

    # ---- template markup. Every slot is present for every n, empty or not, so the
    # panel is the same shape from 1 to 324: value lines each with a note line
    # beneath, three badge rows, the open group's heading and three rows.
    parts = [f'<div class="facts" data-n="{n}">']
    parts.append('<p class="kicker">Best known packing</p>')
    parts.append('<p class="lead"><span class="var">n</span><span class="eq">=</span></p>')
    parts.append(f'<p class="headline"><span class="nval">{n}</span></p>')
    parts.append('<div class="lines">')
    parts.append(f'<p class="line side">{function_line(n, relation, side_value)}</p>')
    degree_sub = (
        f'<p class="sub">{degree_html}</p>' if degree_html else '<p class="sub empty"></p>'
    )
    if exact_html:
        # Side, exact form, degree note: the note sits under the form it describes.
        tall = " tall" if exact_depth > 1 else ""
        parts.append(
            f'<p class="line exact{tall}"><span class="eqsign">=</span>'
            f'<span class="form">{exact_html}</span></p>'
        )
        parts.append(degree_sub)
    else:
        # No exact form: the degree note goes directly under the side value it
        # annotates and the empty exact slot follows it, so the note cannot read as
        # a label for the lower bound beneath. The three slots are the same 50 + 58
        # + 30 in either order, so the lower line and everything below it stay put.
        parts.append(degree_sub)
        parts.append('<p class="line exact empty"></p>')
    if lower_value is not None:
        parts.append(f'<p class="line lower">{function_line(n, "≥", lower_value)}</p>')
        parts.append('<p class="sub"><span class="note">proved lower bound</span></p>')
    else:
        parts.append('<p class="line lower empty"></p>')
        parts.append('<p class="sub empty"></p>')
    parts.append("</div>")
    parts.append('<ul class="status">')
    for ident, style, label, _meaning in labels:
        parts.append(
            f'<li class="{style}">{badge_svg(ident)}{html.escape(label, quote=False)}</li>'
        )
    parts.append("</ul>")
    parts.append('<div class="open"><p class="open-head">Open</p><ul>')
    if open_items:
        parts.extend(f"<li>{badge_svg(OPEN_ID)}{item}</li>" for item in open_items)
    else:
        parts.append('<li class="none">nothing open</li>')
    parts.append("</ul></div>")
    parts.append('<dl class="record">')
    for label, value_html, _plain in rows:
        parts.append(f"<div><dt>{label}</dt><dd>{value_html}</dd></div>")
    # The source URL is the block's last line, across both columns: the longest
    # (52 characters) is 664px at 28px, wider than the value column but not the panel.
    if source_url:
        url_text = html.escape(strip_scheme(source_url))
        parts.append(f'<div class="urlrow"><dd class="url">{url_text}</dd></div>')
    parts.append("</dl>")
    parts.append("</div>")
    template = f'<template id="facts-{n}">' + "".join(parts) + "</template>"

    # ---- aria text
    rel_words = {"=": "equals", "≤": "is at most"}[relation]
    aria = [f"n = {n}.", f"s({n}) {rel_words} {side_value}"]
    if exact_plain:
        aria[-1] += f", exactly {exact_plain}"
    if degree is not None and degree >= 2:
        aria[-1] += f", algebraic degree {degree}"
    aria[-1] += "."
    if lower_value is not None:
        aria.append(f"s({n}) is at least {lower_value}.")
    if labels:
        aria.append("; ".join(meaning for _, _, _, meaning in labels).capitalize() + ".")
    aria.append("Open: " + ("; ".join(open_items) if open_items else "nothing") + ".")
    for label, _html, plain in rows:
        aria.append(f"{label}: {plain}.")
    return template, " ".join(aria), source_url


# -------------------------------------------------------------------------- assets


def font_css(repo: Path) -> tuple[str, list[tuple[str, int]]]:
    blocks = []
    sizes = []
    for family, style, weight, path in FONT_FACES:
        data = (repo / path).read_bytes()
        sizes.append((path.name, len(data)))
        encoded = base64.b64encode(data).decode("ascii")
        fmt = "woff2-variations" if " " in weight else "woff2"
        unicode_range = SYMBOL_RANGE if family == "Atlas Symbols" else LATIN_RANGE
        extra = "  size-adjust: 102.5%;\n" if family == "Atlas Symbols" else ""
        blocks.append(
            "@font-face {\n"
            f'  font-family: "{family}";\n'
            f"  font-style: {style};\n"
            f"  font-weight: {weight};\n"
            "  font-display: block;\n"
            f"{extra}"
            f'  src: url("data:font/woff2;base64,{encoded}") format("{fmt}");\n'
            f"  unicode-range: {unicode_range};\n"
            "}\n"
        )
    return "".join(blocks), sizes


# The stage stylesheet, emitted into the page byte for byte. Its line lengths are the
# stylesheet's own formatting, not Python's, and rewrapping them would change the
# generated `index.html`; E501 is waived for the literal as a whole.
CSS = r"""
:root {
  --paper: #ffffff;
  --ink: #17202a;
  --muted: #5c6673;
  --label: #47525f;
  --rule: #d5d9de;
  --faint: __FAINT__;
  --chrome: #f7f8fa;
  --surround: #dfe3e8;
  --serif: "PT Serif", "Atlas Symbols", Georgia, "Times New Roman", serif;
  --sans: "Source Sans 3 Variable", "Atlas Symbols", system-ui, -apple-system, "Segoe UI", sans-serif;
}
html, body { margin: 0; height: 100%; background: var(--surround); color: var(--ink); }
body { font-family: var(--sans); font-size: 14px; }
#app { display: flex; flex-direction: column; height: 100vh; }
#stage-wrap { position: relative; flex: 1 1 auto; overflow: hidden; }
/* Four sizes on the stage: __S1__, __S2__, __S3__ and __S4__px, the first being the
   stage's own default so nothing on it can fall below it. */
#stage {
  position: absolute; left: calc(50% - 960px); top: calc(50% - 540px);
  width: 1920px; height: 1080px; background: var(--paper); overflow: hidden;
  transform-origin: 50% 50%; box-shadow: 0 0 0 1px rgba(23, 32, 42, 0.12);
  font-size: __S1__px;
}
body.capture { background: var(--paper); }
body.capture #controls { display: none; }
body.capture #stage { box-shadow: none; }

/* ---- the two cross-fading picture layers, then the panel, footer and bar on top */
.layer { position: absolute; inset: 0; background: var(--paper); }
.pic { position: absolute; left: 90px; top: 80px; width: 880px; height: 880px; transform-origin: 50% 50%; }
.pic svg { display: block; width: 100%; height: 100%; }
.pic .squares { stroke: #000000; stroke-width: 1.1; stroke-linejoin: round; }
.pic .container { fill: none; stroke: #000000; stroke-width: 1.4; }
.facts-host { position: absolute; left: 1080px; top: 80px; width: 750px; height: 880px; z-index: 3; }

/* ---- facts panel: fixed slots, the same shape for every n */
.facts { font-family: var(--serif); color: var(--ink); }
.facts p { margin: 0; }
.kicker { font-family: var(--sans); font-weight: 550; font-size: __S1__px; line-height: 30px; height: 30px;
  letter-spacing: 0.14em; text-transform: uppercase; color: var(--label); white-space: nowrap; }
/* `n =` on its own line directly above the numeral and flush left with it: the
   italic n, an upright equals, in the notes' grey. */
.lead { margin-top: 6px; height: 36px; line-height: 36px; font-size: __S2__px; color: var(--label);
  white-space: nowrap; }
.lead .var { font-style: italic; }
.lead .eq { margin-left: 0.24em; }
/* The numeral, PT Serif Regular, in an 84px slot: the lining digits' ink (67 to 73px
   tall at 96px) sits inside it and the slot is the same for every n. */
.headline { height: 84px; line-height: 84px; font-size: __S4__px; font-weight: 400; white-space: nowrap;
  font-variant-numeric: lining-nums; }
.lines { margin-top: 8px; }
.line { white-space: nowrap; display: flex; align-items: baseline; }
.line.side { font-size: __S3__px; height: 50px; line-height: 50px; }
/* The exact form sits at the top of a 58px slot so a drawn radical or a stacked
   fraction clears the note beneath. Its 50px strut is tall enough that neither the
   radical's box nor the fraction's reaches above it, so the baseline the flex row
   aligns on is the strut's for every form and the line does not shift between n. */
.line.exact { font-size: __S3__px; height: 58px; line-height: 50px; color: var(--ink); }
.line.lower { font-size: __S3__px; height: 50px; line-height: 50px; }
/* A nested radical does rise above that strut and would push the baseline down by
   5px; the line is lifted by the same so its baseline stays where every other n's is. */
.line.exact.tall { position: relative; top: -5px; }
.sub { height: 30px; line-height: 30px; white-space: nowrap; }
.fn i { font-style: italic; margin-right: 0.055em; }
.rel { margin: 0 0.32em; }
.eqsign { margin-right: 0.32em; color: var(--muted); }
.val { font-variant-numeric: tabular-nums lining-nums; }
.degree, .note { font-family: var(--sans); font-weight: 550; font-size: __S1__px; line-height: 30px;
  letter-spacing: 0.06em; text-transform: uppercase; color: var(--label); }
.op { margin: 0 0.22em; }
/* A stacked fraction's digits are the stage's smallest size, not a fraction of the line's. */
.frac { display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle;
  font-size: __S1__px; line-height: 1; margin: 0 0.1em 0 0.05em; }
.frac .num { padding: 0 0.12em; border-bottom: 2px solid currentColor; }
.frac .den { padding: 0 0.12em; }
.sqrt { display: inline-block; position: relative; line-height: 1; vertical-align: baseline;
  padding: 0.03em 0.08em 0.16em 0.92em; }
.sqrt.tall { padding-left: 1.16em; }
.sqrt .sqrt { margin-top: 0.12em; }
.sqrt > .surd { position: absolute; left: 0; top: 0; width: 100%; height: 100%; overflow: hidden;
  fill: currentColor; pointer-events: none; }
.sqrt > .radicand { display: inline-block; line-height: 1; }
/* Three badge rows, then the open group's heading and three rows: fixed heights
   whether or not the rows are filled, so nothing below moves between n. */
.status, .open ul { list-style: none; margin: 0; padding: 0;
  font-family: var(--sans); font-weight: 550; font-size: __S2__px; line-height: 36px; color: var(--ink); }
.status { margin-top: 10px; height: 108px; }
.status li, .open li { display: flex; align-items: center; gap: 12px; white-space: nowrap; height: 36px; }
.status li.muted { color: var(--muted); font-weight: 450; }
/* Scarlet means new. This is the one place it is written; the star in the row is
   drawn in currentColor and so is the same colour as its label. */
.status li.star { color: __NEW__; }
.badge { display: block; width: 30px; height: 30px; flex: none; }
.open { margin-top: 6px; height: 138px; }
.open-head { font-family: var(--sans); font-weight: 550; font-size: __S1__px; line-height: 30px; height: 30px;
  letter-spacing: 0.08em; text-transform: uppercase; color: var(--label); }
.open ul { height: 108px; }
.open li { color: var(--muted); font-weight: 450; }
.open li.none { color: var(--faint); font-style: italic; }
.record { margin: 8px 0 0; padding-top: 8px; border-top: 1px solid var(--rule);
  font-family: var(--sans); font-weight: 400; font-size: __S1__px; line-height: 32px; color: var(--label); }
/* 224px holds the widest label (CONSTRUCTION, 222px); 514px is left for the value. */
.record div { display: grid; grid-template-columns: 224px 1fr; column-gap: 12px; align-items: baseline; }
.record dt { font-weight: 550; letter-spacing: 0.08em; text-transform: uppercase; }
.record dd { margin: 0; overflow-wrap: anywhere; }
.record .urlrow { grid-template-columns: 1fr; }
.record .url { color: var(--muted); }
.stage-footer { position: absolute; left: 90px; right: 90px; top: 972px; height: 28px; z-index: 3;
  font-family: var(--sans); font-size: __S1__px; line-height: 28px; color: var(--muted); white-space: nowrap;
  display: flex; justify-content: space-between; gap: 40px; }
.stage-footer i { font-family: var(--serif); font-style: italic; margin-right: 0.055em; }
.stage-footer .m { font-family: var(--serif); font-style: normal; }

/* ---- progress bar: 1 to 324 along the bottom of the stage, driven by the clock.
   The n rides above the fill's leading edge; the ends sit beside the track, centred on it. */
#progress { position: absolute; left: 90px; right: 90px; top: 1008px; height: 52px; z-index: 3;
  font-family: var(--sans); font-weight: 550; font-size: __S1__px; line-height: 30px; letter-spacing: 0.04em;
  color: var(--label); font-variant-numeric: tabular-nums lining-nums; }
#progress .track { position: absolute; left: 0; right: 0; top: 32px; height: 4px; background: var(--rule); }
#progress .fill { position: absolute; left: 0; top: 0; height: 4px; width: 0; background: var(--label); }
#progress .cursor { position: absolute; top: 0; height: 30px; transform: translateX(-50%); white-space: nowrap; }
#progress .end { position: absolute; top: 19px; height: 30px; white-space: nowrap; }
#progress .end.lo { right: 100%; margin-right: 18px; }
#progress .end.hi { left: 100%; margin-left: 18px; }

/* ---- review controls (outside the stage) */
#controls { flex: none; background: var(--chrome); border-top: 1px solid var(--rule); padding: 8px 14px; font-size: 14px; }
#controls .row { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; min-height: 30px; }
#controls .row + .row { margin-top: 6px; }
#controls button { font: inherit; font-weight: 550; padding: 4px 12px; border: 1px solid #b9c0c8; border-radius: 4px; background: #fff; color: var(--ink); cursor: pointer; }
#controls button:hover { background: #eef1f4; }
#controls input[type="range"] { flex: 1 1 200px; min-width: 120px; }
#controls input[type="number"] { font: inherit; width: 64px; padding: 2px 4px; }
#controls label { display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; }
#readout { font-variant-numeric: tabular-nums; min-width: 22em; white-space: nowrap; }
#length, .hint { color: var(--muted); white-space: nowrap; }
.visually-hidden { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
"""  # noqa: E501

# The player, emitted into the page byte for byte, on the same terms as `CSS` above.
# RUF001 is waived with it: the separator in the length readout is U+00D7, the
# multiplication sign the review chrome shows, not a letter x.
JS = r"""
(function () {
  'use strict';
  var W = 1920, H = 1080;
  var data = JSON.parse(document.getElementById('atlas-data').textContent);
  var slides = data.slides, first = data.first, count = slides.length;
  var timing = { dwell: data.timing.dwell, fade: data.timing.fade };
  var settleOn = true, settleAmount = data.settle;
  var state = { time: 0, playing: false, stamp: null, raf: 0, liveN: 0, scrubbing: false };

  var stage = document.getElementById('stage');
  var wrap = document.getElementById('stage-wrap');
  var live = document.getElementById('live');
  var layerEls = [document.getElementById('layer-a'), document.getElementById('layer-b')];
  var layerN = [0, 0];
  var base = 0, top = 1;
  var factsHost = document.getElementById('facts');
  var factsN = 0;
  var barFill = document.getElementById('progress-fill');
  var barCursor = document.getElementById('progress-cursor');
  var proto = document.getElementById('proto').content;
  var gProto = proto.querySelector('g');
  var polyProto = proto.querySelector('polygon');
  var built = {};

  function slot() { return timing.dwell + timing.fade; }
  function duration() { return count * slot(); }
  function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }
  function smooth(p) { return p * p * (3 - 2 * p); }
  function easeOut(p) { var q = 1 - p; return 1 - q * q * q; }

  function ensure(n) {
    var c = built[n];
    if (c) return c;
    var slide = slides[n - first];
    var g = gProto.cloneNode(false);
    g.setAttribute('data-n', String(n));
    var polys = slide.p.split(';');
    for (var i = 0; i < polys.length; i++) {
      var el = polyProto.cloneNode(false);
      el.setAttribute('points', polys[i]);
      el.setAttribute('fill', data.palette[parseInt(slide.f.charAt(i), 36)]);
      g.appendChild(el);
    }
    var tpl = document.getElementById('facts-' + n);
    c = { squares: g, facts: tpl.content.firstElementChild.cloneNode(true) };
    built[n] = c;
    return c;
  }

  function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }

  function load(index, n) {
    if (layerN[index] === n) return;
    var picHost = layerEls[index].querySelector('.squares-host');
    clear(picHost);
    if (n) picHost.appendChild(ensure(n).squares);
    layerN[index] = n;
  }

  function loadFacts(n) {
    if (factsN === n) return;
    clear(factsHost);
    if (n) factsHost.appendChild(ensure(n).facts);
    factsN = n;
  }

  function positionAt(t) {
    var s = slot(), D = timing.dwell, F = timing.fade;
    var k = Math.floor(t / s);
    if (k > count - 1) k = count - 1;
    if (k < 0) k = 0;
    var u = t - k * s;
    var p = 0;
    if (u >= D) p = F > 0 ? clamp((u - D) / F, 0, 1) : 1;
    // The panel cuts at the fade's midpoint: text is never half there, and the
    // panel always belongs to whichever picture the dissolve favours.
    var panel = (p >= 0.5) ? ((k + 1 < count) ? first + k + 1 : 0) : first + k;
    // The bar advances one step of 323 across each fade and rests through each dwell.
    var bar = count > 1 ? clamp((k + p) / (count - 1), 0, 1) : 1;
    return { index: k, n: first + k, next: (k + 1 < count) ? first + k + 1 : 0, progress: p, within: u, panel: panel, bar: bar };
  }

  function stateAt(t) {
    var pos = positionAt(t);
    return { time: t, n: pos.n, next: pos.next, progress: pos.progress, phase: pos.progress > 0 ? 'fade' : 'dwell', panel: pos.panel, bar: pos.bar };
  }

  function barAt(t) { return positionAt(t).bar; }

  function render() {
    var pos = positionAt(state.time);
    var nCur = pos.n, nNext = pos.next, p = pos.progress;
    if (layerN[top] === nCur) { var tmp = base; base = top; top = tmp; }
    load(base, nCur);
    load(top, nNext);
    var e = smooth(p);
    var baseEl = layerEls[base], topEl = layerEls[top];
    baseEl.style.zIndex = '1';
    topEl.style.zIndex = '2';
    // Always: a layer hidden while it was on top must show when a seek makes it the base.
    baseEl.style.visibility = 'visible';
    if (nNext) {
      baseEl.style.opacity = '1';
      topEl.style.opacity = String(e);
      topEl.style.visibility = p > 0 ? 'visible' : 'hidden';
    } else {
      baseEl.style.opacity = String(1 - e);
      topEl.style.opacity = '0';
      topEl.style.visibility = 'hidden';
    }
    var topPic = topEl.querySelector('.pic');
    topPic.style.transform = (settleOn && nNext) ? 'scale(' + (1 - settleAmount * (1 - easeOut(p))) + ')' : '';
    baseEl.querySelector('.pic').style.transform = '';
    loadFacts(pos.panel);
    var pct = (pos.bar * 100).toFixed(4) + '%';
    barFill.style.width = pct;
    barCursor.textContent = String(pos.panel || nCur);
    // The label rides above the fill's leading edge and is held inside the track at
    // either end, so it never runs into the 1 and the 324 beside the track.
    var trackW = barFill.parentNode ? (barFill.parentNode.offsetWidth || 0) : 0;
    var half = (barCursor.offsetWidth || 0) / 2;
    barCursor.style.left = trackW > 0 ? clamp(pos.bar * trackW, half, trackW - half).toFixed(2) + 'px' : pct;
    var liveN = pos.panel || nCur;
    if (liveN !== state.liveN) {
      state.liveN = liveN;
      live.textContent = slides[liveN - first].a;
    }
    updateReadout(pos);
  }

  function fmt(t) {
    var m = Math.floor(t / 60);
    var s = t - m * 60;
    var whole = Math.floor(s);
    var tenth = Math.floor((s - whole) * 10);
    return (m < 10 ? '0' : '') + m + ':' + (whole < 10 ? '0' : '') + whole + '.' + tenth;
  }

  var readout = document.getElementById('readout');
  var scrub = document.getElementById('scrub');
  var jump = document.getElementById('jump');
  var playBtn = document.getElementById('btn-play');
  var lengthEl = document.getElementById('length');

  function updateReadout(pos) {
    var text = 'n ' + pos.n;
    if (pos.progress > 0) {
      text += pos.next ? (' → ' + pos.next + ' (fade ' + Math.round(pos.progress * 100) + '%)') : ' (fade out)';
    }
    text += ' · ' + fmt(state.time) + ' / ' + fmt(duration());
    readout.textContent = text;
    if (!state.scrubbing) scrub.value = String(state.time);
    if (document.activeElement !== jump) jump.value = String(pos.n);
  }

  function syncTiming() {
    scrub.max = String(duration());
    lengthEl.textContent = 'length ' + fmt(duration()) + ' at ' + count + ' × (' + timing.dwell.toFixed(2) + ' + ' + timing.fade.toFixed(2) + ') s';
    document.getElementById('dwell').value = String(timing.dwell);
    document.getElementById('fade').value = String(timing.fade);
  }

  function frame(stamp) {
    if (!state.playing) return;
    if (state.stamp !== null) state.time += (stamp - state.stamp) / 1000;
    state.stamp = stamp;
    if (state.time >= duration()) {
      state.time = duration();
      render();
      pause();
      return;
    }
    render();
    state.raf = requestAnimationFrame(frame);
  }

  function play() {
    if (state.playing) return;
    if (state.time >= duration()) state.time = 0;
    state.playing = true;
    state.stamp = null;
    playBtn.textContent = 'Pause';
    state.raf = requestAnimationFrame(frame);
  }

  function pause() {
    if (state.raf) cancelAnimationFrame(state.raf);
    state.raf = 0;
    state.playing = false;
    state.stamp = null;
    playBtn.textContent = 'Play';
  }

  function seek(seconds) {
    state.time = clamp(Number(seconds) || 0, 0, duration());
    render();
    return stateAt(state.time);
  }

  function frameAt(index, fps) {
    return seek(index / fps);
  }

  function setTiming(options) {
    var pos = positionAt(state.time);
    var frac = pos.progress > 0 ? 1 + pos.progress : (timing.dwell > 0 ? pos.within / timing.dwell : 0);
    if (options && typeof options.dwell === 'number' && options.dwell > 0) timing.dwell = options.dwell;
    if (options && typeof options.fade === 'number' && options.fade >= 0) timing.fade = options.fade;
    var t = pos.index * slot() + (frac <= 1 ? frac * timing.dwell : timing.dwell + (frac - 1) * timing.fade);
    state.time = clamp(t, 0, duration());
    syncTiming();
    render();
    return { dwell: timing.dwell, fade: timing.fade, duration: duration() };
  }

  function setSettle(on) { settleOn = !!on; document.getElementById('settle').checked = settleOn; render(); }

  function fit() {
    var r = wrap.getBoundingClientRect();
    var k = Math.min(r.width / W, r.height / H);
    stage.style.transform = 'scale(' + k + ')';
  }

  function setCapture(on) {
    document.body.classList.toggle('capture', !!on);
    document.getElementById('capture').checked = !!on;
    fit();
  }

  function goSlide(k) {
    k = clamp(k, 0, count - 1);
    seek(k * slot());
  }

  // ---- controls
  playBtn.addEventListener('click', function () { if (state.playing) pause(); else play(); });
  document.getElementById('btn-prev').addEventListener('click', function () { goSlide(positionAt(state.time).index - 1); });
  document.getElementById('btn-next').addEventListener('click', function () { goSlide(positionAt(state.time).index + 1); });
  scrub.addEventListener('input', function () { state.scrubbing = true; seek(Number(scrub.value)); });
  scrub.addEventListener('change', function () { state.scrubbing = false; seek(Number(scrub.value)); });
  jump.addEventListener('change', function () { goSlide(Math.round(Number(jump.value)) - first); jump.blur(); });
  document.getElementById('dwell').addEventListener('change', function (ev) { setTiming({ dwell: Number(ev.target.value) }); });
  document.getElementById('fade').addEventListener('change', function (ev) { setTiming({ fade: Number(ev.target.value) }); });
  document.getElementById('settle').addEventListener('change', function (ev) { setSettle(ev.target.checked); });
  document.getElementById('capture').addEventListener('change', function (ev) { setCapture(ev.target.checked); });
  document.addEventListener('keydown', function (ev) {
    var tag = ev.target && ev.target.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'BUTTON') return;
    if (ev.key === ' ') { ev.preventDefault(); if (state.playing) pause(); else play(); }
    else if (ev.key === 'ArrowRight') { ev.preventDefault(); goSlide(positionAt(state.time).index + 1); }
    else if (ev.key === 'ArrowLeft') { ev.preventDefault(); goSlide(positionAt(state.time).index - 1); }
    else if (ev.key === 'Home') { ev.preventDefault(); seek(0); }
    else if (ev.key === 'End') { ev.preventDefault(); goSlide(count - 1); }
  });
  window.addEventListener('resize', fit);

  window.atlasVideo = {
    seek: seek,
    frameAt: frameAt,
    duration: duration,
    play: play,
    pause: pause,
    setTiming: setTiming,
    stateAt: stateAt,
    barAt: barAt,
    setSettle: setSettle,
    setCapture: setCapture,
    timing: function () { return { dwell: timing.dwell, fade: timing.fade }; },
    count: count,
    ready: (document.fonts && document.fonts.ready) ? document.fonts.ready : Promise.resolve()
  };

  syncTiming();
  if (/[?&]capture=1/.test(window.location.search)) setCapture(true);
  fit();
  render();
})();
"""  # noqa: E501, RUF001

FOOTER_LEFT = (
    '<span><i>s</i><span class="m">(</span><i>n</i><span class="m">)</span> is the side of the '
    "smallest square known to contain <i>n</i> unit squares</span>"
)
FOOTER_RIGHT = (
    "<span>colour marks tilt angle within a packing · darker, more full-side contacts</span>"
)


def layer_markup(ident: str) -> str:
    return (
        f'<div class="layer" id="{ident}">'
        '<div class="pic"><svg viewBox="-2 -2 540 540" role="img" aria-hidden="true">'
        '<g class="squares-host"></g>'
        '<rect class="container" x="0" y="0" width="536" height="536"></rect>'
        "</svg></div>"
        "</div>"
    )


PROGRESS_MARKUP = (
    '<div id="progress" aria-hidden="true">'
    f'<span class="end lo">{FIRST_N}</span>'
    '<div class="track"><div class="fill" id="progress-fill"></div></div>'
    f'<span class="cursor" id="progress-cursor">{FIRST_N}</span>'
    f'<span class="end hi">{LAST_N}</span>'
    "</div>"
)


def page_css() -> str:
    return (
        CSS.replace("__S1__", str(SMALL))
        .replace("__S2__", str(MEDIUM))
        .replace("__S3__", str(LARGE))
        .replace("__S4__", str(NUMERAL_SIZE))
        .replace("__NEW__", NEW_COLOR)
        .replace("__FAINT__", BADGE_FAINT)
    )


def assemble(fonts_css: str, symbols: str, facts_templates: list[str], data_json: str) -> str:
    head = (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; '
        "script-src 'unsafe-inline'; style-src 'unsafe-inline'; font-src data:; img-src data:; "
        "connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'\">\n"
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>Known-best square packings, n = 1 … 324 — slideshow candidate v1</title>\n"
        "<style>\n" + fonts_css + page_css() + "</style>\n"
        "</head>\n"
    )
    body = (
        "<body>\n"
        '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
        f'<path id="surd" d="{SQRT_MAIN_PATH}"></path>' + symbols + "</defs></svg>\n"
        '<div id="app">\n'
        '<div id="stage-wrap"><div id="stage">\n'
        + layer_markup("layer-a")
        + "\n"
        + layer_markup("layer-b")
        + "\n"
        '<div id="facts" class="facts-host"></div>\n'
        + f'<div class="stage-footer">{FOOTER_LEFT}{FOOTER_RIGHT}</div>\n'
        + PROGRESS_MARKUP
        + "\n"
        "</div></div>\n"
        '<div id="controls">\n'
        '<div class="row">'
        '<button id="btn-prev" type="button" title="Previous (←)">'
        "‹ prev</button>"  # noqa: RUF001
        '<button id="btn-play" type="button" title="Play / pause (space)">Play</button>'
        '<button id="btn-next" type="button" title="Next (→)">'
        "next ›</button>"  # noqa: RUF001
        '<input id="scrub" type="range" min="0" max="1" step="0.01" '
        'value="0" aria-label="Timeline">'
        '<span id="readout"></span>'
        '<label>go to n <input id="jump" type="number" min="1" max="324" '
        'step="1" value="1"></label>'
        "</div>\n"
        '<div class="row">'
        f'<label>dwell <input id="dwell" type="number" min="0.1" step="0.1" '
        f'value="{DEFAULT_DWELL}"> s</label>'
        f'<label>fade <input id="fade" type="number" min="0" step="0.1" '
        f'value="{DEFAULT_FADE}"> s</label>'
        '<label><input id="settle" type="checkbox" checked> 2% scale settle '
        "(picture only; the panel cuts at the fade midpoint)</label>"
        '<label><input id="capture" type="checkbox"> capture preview (stage only, 16:9)</label>'
        '<span id="length"></span>'
        '<span class="hint">space play/pause · ← → step · Home/End · '
        "?capture=1 in the URL for the stage alone</span>"
        "</div>\n"
        "</div>\n"
        "</div>\n"
        '<div id="live" class="visually-hidden" aria-live="polite" aria-atomic="true"></div>\n'
        "<noscript>This slideshow needs JavaScript to step through the packings.</noscript>\n"
        '<template id="proto"><svg><g class="squares">'
        "<polygon></polygon></g></svg></template>\n"
        + "\n".join(facts_templates)
        + "\n"
        '<script id="atlas-data" type="application/json">' + data_json + "</script>\n"
        "<script>" + JS + "</script>\n"
        "</body>\n"
        "</html>\n"
    )
    return head + body


# ---------------------------------------------------------------------------- main


def build(repo: Path, out_dir: Path, decimals: int, radical: str) -> dict:
    composite = read_composite(repo)
    manifest = read_manifest(repo)
    coordinate = make_rounder(decimals)
    rendering = repo / "packing/atlas/known-best/rendering"

    per_n_polys: dict[int, list[str]] = {}
    per_n_fills: dict[int, list[str]] = {}
    for n in range(FIRST_N, LAST_N + 1):
        text = (rendering / f"n-{n:03d}.svg").read_text()
        per_n_polys[n], per_n_fills[n] = extract_geometry(text, n, coordinate)
    palette = sorted({fill for fills in per_n_fills.values() for fill in fills})
    assert len(palette) <= len(BASE36), f"{len(palette)} fills exceed one base-36 digit"
    index = {fill: BASE36[i] for i, fill in enumerate(palette)}

    templates: list[str] = []
    slides: list[dict] = []
    for n in range(FIRST_N, LAST_N + 1):
        frontier = read_frontier(repo, n)
        template, aria, source_url = build_facts(
            n, composite[n], manifest[n], frontier, radical
        )
        templates.append(template)
        slide = {
            "n": n,
            "p": ";".join(per_n_polys[n]),
            "f": "".join(index[f] for f in per_n_fills[n]),
            "a": aria,
        }
        if source_url:
            slide["src"] = source_url
        slides.append(slide)

    data = {
        "contract": "atlas-video-slideshow/v1-candidate-r4",
        "first": FIRST_N,
        "last": LAST_N,
        "container": int(PANEL_SIDE),
        "decimals": decimals,
        "palette": palette,
        "timing": {"dwell": DEFAULT_DWELL, "fade": DEFAULT_FADE},
        "settle": SETTLE,
        "slides": slides,
    }
    data_json = json.dumps(data, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
    data_json = data_json.replace("</", "<\\/")

    fonts_css, font_sizes = font_css(repo)
    symbols = badge_symbols(badge_glyph_outlines(repo))
    page = assemble(fonts_css, symbols, templates, data_json)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    out_path.write_bytes(page.encode("utf-8"))

    geometry_bytes = sum(len(s["p"]) + len(s["f"]) for s in slides)
    return {
        "index_html": str(out_path),
        "bytes": len(page.encode("utf-8")),
        "geometry_bytes": geometry_bytes,
        "facts_template_bytes": sum(len(t.encode("utf-8")) for t in templates),
        "font_bytes_raw": sum(size for _, size in font_sizes),
        "font_css_bytes": len(fonts_css.encode("utf-8")),
        "fonts": font_sizes,
        "squares": sum(len(p) for p in per_n_polys.values()),
        "palette_size": len(palette),
        "decimals": decimals,
        "duration_seconds": LAST_N * (DEFAULT_DWELL + DEFAULT_FADE),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--decimals", type=int, default=2, choices=(1, 2, 3))
    parser.add_argument("--radical", choices=("svg", "text"), default="svg")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    report = build(args.repo, args.out, args.decimals, args.radical)
    if not args.quiet:
        for key, value in report.items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
