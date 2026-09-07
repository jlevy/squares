#!/usr/bin/env python3
r"""Measure the reading face against the math faces, and see the difference on a page.

Four throwaway scripts produced the numbers and the montages in
`vendor/kpress/docs/math-text-face.research.md`, and none of them would have survived
the session that wrote them: absolute paths, one font list edited in place per run, a
red banner burned into every variant page. This is the same three measurements with the
throwaway taken out, because the question they answer comes back whenever either side
of the pairing moves -- a kpress font bump, a KaTeX bump, a change to the size token.

`metrics` reads the woff2 files kpress ships and prints the table the brief carries, in
units of 1/1000 em: the two x-heights, the declared one and the one the ink of `x`
actually reaches -- they differ by 11 units in KaTeX_Main and not at all in PT Serif --
the cap and digit heights, the ascender, then the centre and the thickness of the minus
sign, which are the axis every fraction bar and stretched delimiter is drawn on and the
rule thickness the OpenType MATH specification ties to that sign, and finally the stem
of `l` against the stroke of `o`, whose ratio is the face's contrast. Three rows of that
table are the whole diagnosis: PT Serif's x-height is 0.714 of its cap height and
Computer Modern's is 0.647, so no single scale factor can match both; PT Serif's stems
are 10-18% heavier, so no scale factor matches the weight either; and its operators are
centred at 344 against KaTeX's 250, which is why the operators do not move.

`variants` and `shots` are the other half, because the argument the table makes is
visual and the way to check it is to render the same paragraph several ways and look.
`variants` injects CSS into an already-rendered explainer page -- every face is inlined
in it, so a composite family can be built out of the page's own bytes with no network
and no rebuild -- and `shots` drives Playwright over the results and stacks the same
paragraph from every variant into one image.

What the variants are is `unicode-range` composites, and that is not a stylistic choice.
KaTeX picks the face by class, and digits, operator names and `\text{}` carry no class
at all: they are drawn by whatever family the root `.katex` rule names. So "digits from
PT Serif, operators from KaTeX" cannot be said in class selectors, only in a family that
answers differently per code point. Every range here is disjoint from its partner, so
nothing depends on which face wins an overlap.

`--metrics-patch` is the honest version of the same page. KaTeX lays out from a table of
`[depth, height, italic, skew, width]` baked into `katex.min.js`, so a swapped face is
drawn at one size and placed at another: PT Serif digits are 0.046em taller than the
Computer Modern digits KaTeX believes it is placing, and at 3x device scale the top of a
numerator clips. The flag rewrites the entries for exactly the code points a variant
swaps, from the PT Serif files' own bounds. Skew is left at KaTeX's value, because it
places an accent over a glyph rather than describing the glyph, and the scaled Greek is
the one case where every number moves, since there the glyph itself is scaled.
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import re
import shutil
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Imported at module scope because `_FlattenPen` below subclasses `BasePen`, and a class
# statement cannot wait for a lazy import. The cost is worth recording rather than
# hiding: this project runs a free-threaded 3.14, and `fontTools.misc.bezierTools` does
# not declare itself safe without the GIL, so importing this module re-enables the GIL
# in the process that did it -- including the one pytest worker that collects the test
# beside this file. Playwright and Pillow are imported where they are used instead,
# which is the pattern `render_explainer_pdf` sets and the reason a `metrics` run neither
# starts a browser nor loads an image library.
from fontTools.pens.basePen import BasePen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

from devtools.render_explainer_pdf import BROWSER_OVERRIDE, PAGE, READY

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent

#: kpress's static tree, which is where both sides of the pairing are shipped from.
STATIC = REPO / "vendor" / "kpress" / "src" / "kpress" / "format" / "static"
PROSE_FONTS = STATIC / "fonts"
KATEX_FONTS = STATIC / "katex" / "fonts"

#: The faces the pairing is made of, in the order the brief tabulates them: the reading
#: face in every style kpress ships, then the four KaTeX faces a Latin letter or a digit
#: can land in. Everything else KaTeX carries -- the sizes, AMS, script and typewriter
#: faces -- draws symbols only, and no route here proposes to touch it.
DEFAULT_FACES: tuple[tuple[str, Path], ...] = (
    ("PT Serif Regular", PROSE_FONTS / "pt-serif-latin-400-normal.woff2"),
    ("PT Serif Italic", PROSE_FONTS / "pt-serif-latin-400-italic.woff2"),
    ("PT Serif Bold", PROSE_FONTS / "pt-serif-latin-700-normal.woff2"),
    ("PT Serif Bold Italic", PROSE_FONTS / "pt-serif-latin-700-italic.woff2"),
    ("KaTeX_Main-Regular", KATEX_FONTS / "KaTeX_Main-Regular.woff2"),
    ("KaTeX_Main-Italic", KATEX_FONTS / "KaTeX_Main-Italic.woff2"),
    ("KaTeX_Math-Italic", KATEX_FONTS / "KaTeX_Math-Italic.woff2"),
    ("KaTeX_Main-Bold", KATEX_FONTS / "KaTeX_Main-Bold.woff2"),
)

#: How finely a curve is walked when an outline is flattened to polygons for the two
#: scan-line measurements, the stem and the round stroke. Converged rather than guessed:
#: at 96 steps every figure across the eleven faces measured for the brief is within
#: 0.001 of its value at 1536 steps. The scratch script used 24, which agreed with the
#: converged value on every face kpress ships but put STIX Two Math's `o` at 92.49
#: against a converged 92.56 -- the wrong side of a rounding boundary, and the one
#: figure in the brief's table this tool would otherwise fail to reproduce.
FLATTEN_STEPS = 96

#: The minus sign, not the hyphen: U+2212 is the character KaTeX sets for `-` in math,
#: and it is the glyph whose ink centre defines a font's math axis. Spelled by code
#: point because the two characters are indistinguishable in a source file.
MINUS = "\u2212"


class _FlattenPen(BasePen):
    """Walks an outline into polygons, one point list per contour.

    `BoundsPen` answers where the ink starts and stops, which covers every height in the
    table. It cannot answer how wide a stroke is, because that is a question about a
    horizontal slice rather than about the whole glyph, and a slice needs points. Curves
    are subdivided uniformly rather than adaptively: the reported figures are whole
    units of 1/1000 em and uniform subdivision is already two orders of magnitude finer
    than that.
    """

    def __init__(self, glyph_set: object, steps: int = FLATTEN_STEPS) -> None:
        super().__init__(glyph_set)
        self.contours: list[list[tuple[float, float]]] = []
        self.steps = steps

    def _moveTo(self, pt: tuple[float, float]) -> None:  # noqa: N802
        self.contours.append([pt])

    def _lineTo(self, pt: tuple[float, float]) -> None:  # noqa: N802
        self.contours[-1].append(pt)

    def _curveToOne(  # noqa: N802
        self,
        pt1: tuple[float, float],
        pt2: tuple[float, float],
        pt3: tuple[float, float],
    ) -> None:
        start = self.contours[-1][-1]
        for index in range(1, self.steps + 1):
            t = index / self.steps
            u = 1 - t
            weights = (u**3, 3 * u * u * t, 3 * u * t * t, t**3)
            points = (start, pt1, pt2, pt3)
            self.contours[-1].append(
                (
                    sum(w * p[0] for w, p in zip(weights, points, strict=True)),
                    sum(w * p[1] for w, p in zip(weights, points, strict=True)),
                )
            )

    def _qCurveToOne(  # noqa: N802
        self, pt1: tuple[float, float], pt2: tuple[float, float]
    ) -> None:
        start = self.contours[-1][-1]
        for index in range(1, self.steps + 1):
            t = index / self.steps
            u = 1 - t
            self.contours[-1].append(
                (
                    u * u * start[0] + 2 * u * t * pt1[0] + t * t * pt2[0],
                    u * u * start[1] + 2 * u * t * pt1[1] + t * t * pt2[1],
                )
            )

    def _closePath(self) -> None:  # noqa: N802
        contour = self.contours[-1]
        if contour and contour[0] != contour[-1]:
            contour.append(contour[0])

    def _endPath(self) -> None:  # noqa: N802
        self._closePath()


@dataclass(frozen=True)
class FaceMetrics:
    """One face measured, every figure in units of 1/1000 em.

    `x_height` is what OS/2 declares and `x_height_ink` is where the ink of `x` reaches.
    Both are reported because KaTeX_Main disagrees with itself by 11 units, and KaTeX's
    own layout constant is the ink figure (0.431, from `cmsy10`) rather than the
    declared one. A field is `None` where the face has no such glyph.
    """

    label: str
    x_height: float
    x_height_ink: float | None
    cap_height: float
    digit_height: float | None
    ascender: float | None
    operator_centre: float | None
    hairline: float | None
    stem: float | None
    round_stroke: float | None
    axis_height: float | None


def _ink_spans(
    contours: Sequence[Sequence[tuple[float, float]]], height: float
) -> list[tuple[float, float]]:
    """Where a horizontal line at `height` is inside the ink, left to right.

    Crossings are counted rather than filled: a closed outline crosses any scan line an
    even number of times, so pairing the sorted crossings gives the ink runs without
    needing to know the winding direction of each contour.
    """
    crossings: list[float] = []
    for contour in contours:
        for (x1, y1), (x2, y2) in itertools.pairwise(contour):
            if (y1 <= height < y2) or (y2 <= height < y1):
                crossings.append(x1 + (height - y1) * (x2 - x1) / (y2 - y1))
    crossings.sort()
    return [(crossings[i], crossings[i + 1]) for i in range(0, len(crossings) - 1, 2)]


def _units_per_em(font: TTFont) -> float:
    """`head.unitsPerEm`, past a checker that cannot see it.

    fontTools sets a table's fields on the object as it decompiles, rather than
    declaring them on the class, so a static reader sees an empty `head`. The cast is
    kept in this one function so nothing else in the module has to go untyped.
    """
    head: Any = font["head"]
    return float(head.unitsPerEm)


def _unicode_cmap(font: TTFont, path: Path) -> dict[int, str]:
    """The best Unicode character map, or a refusal.

    Every measurement here asks for a glyph by character, so a face that offers no
    Unicode subtable cannot be read at all rather than read incompletely.
    """
    cmap = font.getBestCmap()
    if cmap is None:
        raise SystemExit(f"{path.name} carries no Unicode cmap, so no glyph can be found")
    return cmap


def measure(label: str, path: Path) -> FaceMetrics:
    """Every figure in one row of the table, read from one font file."""
    if not path.is_file():
        raise SystemExit(f"no font file at {path}")
    font = TTFont(path)
    scale = 1000 / _units_per_em(font)
    os2 = font["OS/2"]
    glyphs = font.getGlyphSet()
    cmap = _unicode_cmap(font, path)

    def outline(character: str) -> list[list[tuple[float, float]]] | None:
        name = cmap.get(ord(character))
        if name is None:
            return None
        pen = _FlattenPen(glyphs)
        glyphs[name].draw(pen)
        return pen.contours

    def ink(character: str) -> tuple[float, float, float, float] | None:
        name = cmap.get(ord(character))
        if name is None:
            return None
        pen = BoundsPen(glyphs)
        glyphs[name].draw(pen)
        return pen.bounds

    x_ink, cap_ink = ink("x"), ink("H")
    digit_ink, ascender_ink, minus_ink, round_ink = ink("0"), ink("l"), ink(MINUS), ink("o")
    # OS/2 carries `sxHeight` and `sCapHeight` only from version 2 on, and a face may
    # declare either as zero; the ink of `x` and `H` is the fallback in both cases.
    x_units = getattr(os2, "sxHeight", 0) or (x_ink[3] if x_ink else 0.0)
    cap_units = getattr(os2, "sCapHeight", 0) or (cap_ink[3] if cap_ink else 0.0)

    stem = None
    if (letter := outline("l")) is not None:
        # Half the x-height is where the vertical of `l` is a plain stem: below it the
        # serif flares, above it the ascender leaves the scan line entirely.
        spans = _ink_spans(letter, x_units * 0.5)
        stem = (spans[0][1] - spans[0][0]) * scale if spans else None

    round_stroke = None
    if (letter := outline("o")) is not None and round_ink is not None:
        # The two spans at mid-height are the left and right thick strokes of the bowl.
        # Their mean is the figure, because an italic `o` is not symmetric and either
        # side alone would report the face as lighter or heavier than it reads.
        spans = _ink_spans(letter, (round_ink[1] + round_ink[3]) / 2)
        widths = [end - start for start, end in spans]
        round_stroke = sum(widths) / len(widths) * scale if widths else None

    axis_height = None
    if "MATH" in font:
        axis_height = font["MATH"].table.MathConstants.AxisHeight.Value * scale

    return FaceMetrics(
        label=label,
        x_height=x_units * scale,
        x_height_ink=x_ink[3] * scale if x_ink else None,
        cap_height=cap_units * scale,
        digit_height=digit_ink[3] * scale if digit_ink else None,
        ascender=ascender_ink[3] * scale if ascender_ink else None,
        operator_centre=(minus_ink[1] + minus_ink[3]) / 2 * scale if minus_ink else None,
        hairline=(minus_ink[3] - minus_ink[1]) * scale if minus_ink else None,
        stem=stem,
        round_stroke=round_stroke,
        axis_height=axis_height,
    )


def _cell(value: float | None) -> str:
    return "--" if value is None else f"{value:.0f}"


def metrics_table(faces: Sequence[FaceMetrics]) -> str:
    """The measured faces as the Markdown table the research brief carries."""
    header = (
        "| Face | x-height | Cap height | Digit height | Ascender (`l`) "
        "| Operator centre | Hairline | Stem `l` | `o` stroke |"
    )
    lines = [header, "| --- " * 9 + "|"]
    for face in faces:
        x_height = _cell(face.x_height)
        if face.x_height_ink is not None and _cell(face.x_height_ink) != x_height:
            x_height = f"{x_height} (ink {_cell(face.x_height_ink)})"
        centre = _cell(face.operator_centre)
        if face.axis_height is not None:
            centre = f"{centre} (MATH `AxisHeight` {_cell(face.axis_height)})"
        lines.append(
            f"| {face.label} | {x_height} | {_cell(face.cap_height)} "
            f"| {_cell(face.digit_height)} | {_cell(face.ascender)} | {centre} "
            f"| {_cell(face.hairline)} | {_cell(face.stem)} | {_cell(face.round_stroke)} |"
        )
    return "\n".join(lines)


# The variant pages.


@dataclass(frozen=True)
class PageFaces:
    """The three inlined faces a composite family is assembled from, as `data:` URLs.

    Taken out of the rendered page rather than out of the font files, so a variant is a
    string operation on one self-contained document: no network, no second render, and
    the composite is built from the same bytes the page already ships.
    """

    pt_regular: str
    katex_main: str
    katex_math_italic: str


def _prose_face(html: str, family: str, style: str, weight: str) -> str:
    """One of kpress's own `@font-face` blocks, which are pretty-printed."""
    pattern = (
        rf'@font-face\s*\{{[^}}]*?font-family:\s*"?{re.escape(family)}"?;[^}}]*?'
        rf"font-style:\s*{style};[^}}]*?font-weight:\s*{weight};[^}}]*?"
        r'src:\s*url\("(data:font/woff2;base64,[^"]+)"\)'
    )
    match = re.search(pattern, html, flags=re.DOTALL)
    if match is None:
        raise SystemExit(f"the page carries no inlined {family} {style} {weight} face")
    return match.group(1)


def _katex_face(html: str, name: str, style: str, weight: str) -> str:
    """One of KaTeX's, which arrive minified and in a fixed property order."""
    pattern = (
        rf"@font-face\{{font-display:swap;font-family:{re.escape(name)};"
        rf'font-style:{style};font-weight:{weight};src:url\("(data:[^"]+)"\)'
    )
    match = re.search(pattern, html)
    if match is None:
        raise SystemExit(f"the page carries no inlined KaTeX {name} {style} {weight} face")
    return match.group(1)


def page_faces(html: str) -> PageFaces:
    """The faces every composite below is built from."""
    return PageFaces(
        pt_regular=_prose_face(html, "PT Serif", "normal", "400"),
        katex_main=_katex_face(html, "KaTeX_Main", "normal", "400"),
        katex_math_italic=_katex_face(html, "KaTeX_Math", "italic", "400"),
    )


#: The code points a variant can move, as the metric table indexes them.
_DIGITS = tuple(range(0x30, 0x3A))
_LETTERS = tuple(range(0x41, 0x5B)) + tuple(range(0x61, 0x7B))
_ALPHANUMERIC = _DIGITS + _LETTERS
_GREEK = tuple(range(0x370, 0x400))
_GREEK_CAPITALS = tuple(range(0x391, 0x3AA))

#: Lowercase Greek to PT Serif's x-height, 500/441; capitals, which KaTeX sets upright
#: from Main-Regular, to its cap height, 700/683. Scaling by the x-height ratio also
#: thickens the strokes by the same 13%, which is the second half of why it helps.
GREEK_SCALE = 1.134
GREEK_CAPITAL_SCALE = 1.025


@dataclass(frozen=True)
class Variant:
    """One page variant: what to inject, what it shows, and what it moves.

    `swaps` and `scales` describe the same change to KaTeX's metric table that the CSS
    describes to the browser, so `--metrics-patch` rewrites exactly the entries whose
    glyphs the variant actually redirects and no others.
    """

    name: str
    label: str
    css: str
    #: `(metric face, PT Serif file, code points)` for glyphs drawn from another file.
    swaps: tuple[tuple[str, str, tuple[int, ...]], ...] = ()
    #: `(metric face, code points, factor)` for glyphs drawn from the same file, scaled.
    scales: tuple[tuple[str, tuple[int, ...], float], ...] = ()


_PT_REGULAR_FILE = "pt-serif-latin-400-normal.woff2"
_PT_ITALIC_FILE = "pt-serif-latin-400-italic.woff2"
_PT_BOLD_FILE = "pt-serif-latin-700-normal.woff2"

_DIGIT_SWAPS = (("Main-Regular", _PT_REGULAR_FILE, _ALPHANUMERIC),)
_LETTER_SWAPS = (*_DIGIT_SWAPS, ("Math-Italic", _PT_ITALIC_FILE, _LETTERS))
_ALL_SWAPS = (
    *_LETTER_SWAPS,
    ("Main-Italic", _PT_ITALIC_FILE, _LETTERS),
    ("Main-Bold", _PT_BOLD_FILE, _ALPHANUMERIC),
)

#: Upright text: `\text`, `\textrm` and `\mathrm` all reach the reading face, and the
#: root composite covers what carries no class at all, digits above everything else.
_UPRIGHT_CSS = """
.kpress .katex .mainrm, .kpress .katex .textrm, .kpress .katex .mathrm {
  font-family: "PT Serif", KaTeX_Main; }
"""

_ITALIC_CSS = """
.kpress .katex .mathnormal { font-family: "PT Serif", KaTeX_Math; font-style: italic; }
"""

_ALL_CSS = """
/* Operator names -- `tan`, `arctan` -- are included by the root rule, since KaTeX
   gives them no font class of their own. */
.kpress .katex .mainrm, .kpress .katex .textrm, .kpress .katex .mathrm {
  font-family: "PT Serif", KaTeX_Main; }
.kpress .katex .mathnormal, .kpress .katex .mathit {
  font-family: "PT Serif", KaTeX_Math; font-style: italic; }
.kpress .katex .mathbf { font-family: "PT Serif", KaTeX_Main; font-weight: 700; }
.kpress .katex .boldsymbol {
  font-family: "PT Serif", KaTeX_Math; font-style: italic; font-weight: 700; }
"""

_ONE_EM_CSS = """
.kpress { --kpress-katex-size-prose: 1em; }
"""


def _composite(family: str, faces: PageFaces, katex_range: str, prose_range: str) -> str:
    """A family that answers with KaTeX_Main over one range and PT Serif over another."""
    return (
        f'@font-face {{ font-family: "{family}"; font-style: normal; font-weight: 400;\n'
        f'  src: url("{faces.katex_main}") format("woff2");\n'
        f"  unicode-range: {katex_range}; }}\n"
        f'@font-face {{ font-family: "{family}"; font-style: normal; font-weight: 400;\n'
        f'  src: url("{faces.pt_regular}") format("woff2");\n'
        f"  unicode-range: {prose_range}; }}\n"
        f'.kpress .katex {{ font-family: "{family}", KaTeX_Main, "Times New Roman", serif; }}\n'
    )


def built_in_variants(faces: PageFaces) -> tuple[Variant, ...]:
    """The eight routes the research rendered, in the order it compares them."""
    digits = _composite("KaTeX_MainPT", faces, "U+0000-002F, U+003A-10FFFF", "U+0030-0039")
    latin = _composite(
        "KaTeX_MainPTL",
        faces,
        "U+0000-002F, U+003A-0040, U+005B-0060, U+007B-10FFFF",
        "U+0030-0039, U+0041-005A, U+0061-007A",
    )
    operators = _composite(
        "KaTeX_MainPTO",
        faces,
        "U+0000-002A, U+002C-002F, U+003A-003B, U+003F-0040, U+005B-0060, "
        "U+007B-2211, U+2213-10FFFF",
        "U+002B, U+0030-0039, U+003C-003E, U+0041-005A, U+0061-007A, U+2212",
    )
    size_adjusted = (
        '@font-face { font-family: "KaTeX_MathAdj"; font-style: italic; font-weight: 400;\n'
        f'  src: url("{faces.katex_math_italic}") format("woff2");\n'
        f"  size-adjust: {GREEK_SCALE * 100:.1f}%; }}\n"
        ".kpress .katex .mathnormal {\n"
        '  font-family: "KaTeX_MathAdj", KaTeX_Math; font-style: italic; }\n'
    )
    greek = (
        '@font-face { font-family: "KaTeX_MathGreek"; font-style: italic; font-weight: 400;\n'
        f'  src: url("{faces.katex_math_italic}") format("woff2");\n'
        f"  unicode-range: U+0370-03FF, U+1D6A4-1D6A5; "
        f"size-adjust: {GREEK_SCALE * 100:.1f}%; }}\n"
        '@font-face { font-family: "KaTeX_MainGreek"; font-style: normal; font-weight: 400;\n'
        f'  src: url("{faces.katex_main}") format("woff2");\n'
        f"  unicode-range: U+0391-03A9; size-adjust: {GREEK_CAPITAL_SCALE * 100:.1f}%; }}\n"
        ".kpress .katex .mathnormal {\n"
        '  font-family: "PT Serif", "KaTeX_MathGreek", KaTeX_Math; font-style: italic; }\n'
        ".kpress .katex {\n"
        '  font-family: "KaTeX_MainPTL", "KaTeX_MainGreek", KaTeX_Main, '
        '"Times New Roman", serif; }\n'
    )
    return (
        Variant(
            "current",
            "Route A: the page as it renders today, every glyph from the KaTeX faces",
            "",
        ),
        Variant(
            "digits",
            "Route B: digits and upright text from PT Serif; variables stay KaTeX_Math",
            digits + _UPRIGHT_CSS,
            swaps=_DIGIT_SWAPS,
        ),
        Variant(
            "letters",
            "Route C: B plus italic variables from PT Serif Italic",
            digits + _UPRIGHT_CSS + _ITALIC_CSS,
            swaps=_LETTER_SWAPS,
        ),
        Variant(
            "all",
            "Route D: every Latin letter and digit from PT Serif, in every style",
            latin + _ALL_CSS,
            swaps=_ALL_SWAPS,
        ),
        Variant(
            "all-1em",
            "Route E: D with the prose KaTeX size token at 1em instead of 1.05em",
            latin + _ALL_CSS + _ONE_EM_CSS,
            swaps=_ALL_SWAPS,
        ),
        Variant(
            "sizeadj",
            "Route F, eliminated: B plus KaTeX_Math size-adjusted to PT Serif's x-height",
            digits + _UPRIGHT_CSS + size_adjusted,
            swaps=_DIGIT_SWAPS,
            scales=(("Math-Italic", _LETTERS, GREEK_SCALE),),
        ),
        Variant(
            "ops",
            "Route H, eliminated: D plus + - = < > from PT Serif, as mathastext does",
            operators + _ALL_CSS,
            swaps=_ALL_SWAPS,
        ),
        Variant(
            "greek",
            "Route J: E plus Greek scaled to PT Serif, lowercase 113.4%, capitals 102.5%",
            latin + _ALL_CSS + _ONE_EM_CSS + greek,
            swaps=_ALL_SWAPS,
            scales=(
                ("Math-Italic", _GREEK, GREEK_SCALE),
                ("Main-Regular", _GREEK_CAPITALS, GREEK_CAPITAL_SCALE),
            ),
        ),
    )


def _spec_variants(spec: Path) -> tuple[Variant, ...]:
    """Extra variants from a `{name: {"css": ..., "label": ...}}` file.

    A name that repeats a built-in replaces it, which is how a route is tried against a
    changed stylesheet without editing this module.
    """
    declared = json.loads(spec.read_text(encoding="utf-8"))
    return tuple(
        Variant(name, str(body.get("label", name)), str(body["css"]))
        for name, body in declared.items()
    )


# The metric table, which lives as plain data inside the KaTeX bundle.

_ENTRY = re.compile(r"(\d+):\[([^\]]*)\]")


def _glyph_metrics(
    path: Path, code_points: Iterable[int]
) -> dict[int, tuple[float, float, float, float]]:
    """`(depth, height, italic correction, width)` in em, as KaTeX's extractor defines them.

    Italic correction is the ink that overhangs the advance width, which is the
    definition KaTeX's own Docker build uses; depth and height are the ink below and
    above the baseline, clamped at zero the same way.
    """
    if not path.is_file():
        raise SystemExit(f"no font file at {path}")
    font = TTFont(path)
    glyphs = font.getGlyphSet()
    cmap = _unicode_cmap(font, path)
    scale = 1 / _units_per_em(font)
    measured: dict[int, tuple[float, float, float, float]] = {}
    for code_point in code_points:
        name = cmap.get(code_point)
        if name is None:
            continue
        pen = BoundsPen(glyphs)
        glyphs[name].draw(pen)
        if pen.bounds is None:
            continue
        _, low, right, high = pen.bounds
        advance = glyphs[name].width
        measured[code_point] = (
            max(0.0, -low) * scale,
            max(0.0, high) * scale,
            max(0.0, right - advance) * scale,
            advance * scale,
        )
    return measured


def _rewrite_face_table(
    html: str,
    face: str,
    replacements: dict[int, tuple[float, float, float, float]],
    factors: dict[int, float],
) -> tuple[str, int]:
    """Rewrite one face's entries in place, returning the page and the count changed."""
    marker = f'"{face}":{{'
    start = html.find(marker)
    if start < 0:
        raise SystemExit(f"the page carries no KaTeX metric table for {face}")
    end = html.index("}", start) + 1
    rewritten = 0

    def entry(match: re.Match[str]) -> str:
        nonlocal rewritten
        code_point = int(match.group(1))
        values = [float(value) for value in match.group(2).split(",")]
        if code_point in replacements:
            depth, height, italic, width = replacements[code_point]
            rewritten += 1
            # Skew stays KaTeX's: it places an accent over a glyph rather than
            # describing the glyph, and no measurement here replaces it.
            return (
                f"{code_point}:[{depth:.5f},{height:.5f},{italic:.5f},{values[3]},{width:.5f}]"
            )
        if code_point in factors:
            factor = factors[code_point]
            rewritten += 1
            # Here the glyph itself is scaled by `size-adjust`, so every number moves.
            scaled = ",".join(f"{value * factor:.5f}" for value in values)
            return f"{code_point}:[{scaled}]"
        return match.group(0)

    patched = _ENTRY.sub(entry, html[start:end])
    return html[:start] + patched + html[end:], rewritten


def patch_metrics(html: str, variant: Variant, font_dir: Path) -> tuple[str, int]:
    """Bring KaTeX's table into step with the glyphs `variant` actually draws."""
    faces = {face for face, _, _ in variant.swaps} | {face for face, _, _ in variant.scales}
    total = 0
    for face in sorted(faces):
        replacements: dict[int, tuple[float, float, float, float]] = {}
        for swapped, filename, code_points in variant.swaps:
            if swapped == face:
                replacements |= _glyph_metrics(font_dir / filename, code_points)
        factors = {
            code_point: factor
            for scaled, code_points, factor in variant.scales
            if scaled == face
            for code_point in code_points
        }
        html, rewritten = _rewrite_face_table(html, face, replacements, factors)
        total += rewritten
    return html, total


# Building the pages.

#: Figures the page loads from beside itself; without them a variant renders broken art.
SIBLING_ASSETS = ("known-best-1-100*.png", "known-best-1-100*.svg")


def build_variants(
    page: Path,
    out: Path,
    spec: Path | None = None,
    font_dir: Path = PROSE_FONTS,
    *,
    metrics_patch: bool = False,
) -> list[Path]:
    """Write one page per variant beside a copy of the figures they reference."""
    if not page.is_file():
        raise SystemExit(f"no rendered page at {page}; render the explainer first")
    html = page.read_text(encoding="utf-8")
    variants = {variant.name: variant for variant in built_in_variants(page_faces(html))}
    if spec is not None:
        variants |= {variant.name: variant for variant in _spec_variants(spec)}
    out.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for variant in variants.values():
        page_html = html
        if variant.css:
            page_html = page_html.replace(
                "</head>", f"<style>\n{variant.css}</style>\n</head>", 1
            )
        note = ""
        if metrics_patch and (variant.swaps or variant.scales):
            page_html, rewritten = patch_metrics(page_html, variant, font_dir)
            note = f" ({rewritten} metric entries rewritten)"
        target = out / f"{variant.name}.html"
        target.write_text(page_html, encoding="utf-8")
        written.append(target)
        print(f"wrote {target.name}{note}")

    for pattern in SIBLING_ASSETS:
        for asset in sorted(page.parent.glob(pattern)):
            shutil.copy2(asset, out / asset.name)

    resolved = page.resolve()
    source = resolved.relative_to(REPO) if resolved.is_relative_to(REPO) else resolved
    readme = out / "README.txt"
    readme.write_text(
        "Variants of "
        + str(source)
        + ", built by devtools.compare_math_fonts.\n"
        + ("Metric tables patched to the swapped faces.\n" if metrics_patch else "")
        + "\n"
        + "\n".join(f"{variant.name:10} {variant.label}" for variant in variants.values())
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {readme.name}")
    return written


# The screenshots.

#: Paragraphs worth comparing, keyed by a fragment of their own text. Chosen for what
#: they mix: a number in a sentence, a variable beside a word, an operator name, a bold
#: symbol, and Greek, which is the one thing no route can move to the reading face.
PARAGRAPH_STARTS: dict[str, str] = {
    "p1": "This work presents a new lower bound",
    "p8": "The square packing problem asks",
    "p9": "is the smallest case still open",
    "p13": "The proof is a certificate",
    "ptheta": "theta_k = 2",
    "pbold": "mathbf{D}_4",
    "ptan": "The net reaches",
}

#: Single elements taken once each: the first visible one that actually contains math.
MATH_BEARING = (("caption", ".kpress-figcaption"), ("massline", ".mass-line"), ("kv", ".kv"))

#: How many display blocks to take. Three is where the research stopped: the fraction
#: whose numerator clips without patched metrics is among them.
DISPLAY_BLOCKS = 3

_MARK_PARAGRAPH = """({key, start}) => {
  const found = [...document.querySelectorAll('.cert-page p')].find(
    p => p.getBoundingClientRect().width > 0 && p.textContent.includes(start));
  if (!found) return false;
  found.setAttribute('data-shot', key);
  return true;
}"""


#: `built_in_variants` needs faces only to build CSS; the names and the order it returns
#: do not depend on them, and stacking the pages is the one caller that wants the names
#: on their own, from a directory rather than from a page.
_NAMES_ONLY = PageFaces("", "", "")


def _variant_order(directory: Path, only: Sequence[str]) -> list[Path]:
    """Variant pages in the order the routes are compared, extras after them.

    Order is a property of the montage rather than of the request: two stacks of the
    same routes should have their rows in the same places whatever order they were
    asked for, or reading one against another means re-checking the labels.
    """
    pages = {path.stem: path for path in directory.glob("*.html")}
    if only:
        missing = [name for name in only if name not in pages]
        if missing:
            raise SystemExit(f"no such variant page in {directory}: {', '.join(missing)}")
        pages = {name: pages[name] for name in only}
    known = [variant.name for variant in built_in_variants(_NAMES_ONLY)]
    ordered = [pages.pop(name) for name in known if name in pages]
    return ordered + [pages[name] for name in sorted(pages)]


def take_shots(variants_dir: Path, out: Path, only: Sequence[str] = ()) -> list[Path]:
    """Screenshot the same elements in every variant page, then stack them per element."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    pages = _variant_order(variants_dir, only)
    if not pages:
        raise SystemExit(f"no variant pages in {variants_dir}; run `variants` first")
    out.mkdir(parents=True, exist_ok=True)
    taken: dict[str, list[tuple[str, Path]]] = {}

    def record(name: str, key: str, path: Path) -> None:
        taken.setdefault(key, []).append((name, path))
        print(f"wrote {path.name}")

    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        try:
            context = browser.new_context(
                viewport={"width": 1100, "height": 800},
                device_scale_factor=3,
                reduced_motion="reduce",
            )
            page = context.new_page()
            for source in pages:
                name = source.stem
                page.goto(source.resolve().as_uri(), wait_until="load")
                page.wait_for_selector(READY, timeout=60_000)
                page.evaluate("document.fonts.ready")
                for key, start in PARAGRAPH_STARTS.items():
                    if not page.evaluate(_MARK_PARAGRAPH, {"key": key, "start": start}):
                        print(f"{name}: no paragraph containing {start!r}")
                        continue
                    element = page.locator(f'[data-shot="{key}"]').first
                    element.scroll_into_view_if_needed()
                    target = out / f"{name}-{key}.png"
                    element.screenshot(path=str(target))
                    record(name, key, target)
                for key, selector in MATH_BEARING:
                    candidates = page.locator(f".cert-page {selector}")
                    for index in range(candidates.count()):
                        candidate = candidates.nth(index)
                        if not candidate.locator(".katex").count():
                            continue
                        if not candidate.is_visible():
                            continue
                        candidate.scroll_into_view_if_needed()
                        target = out / f"{name}-{key}.png"
                        candidate.screenshot(path=str(target))
                        record(name, key, target)
                        break
                displays = page.locator(".cert-page .katex-display")
                for index in range(min(displays.count(), DISPLAY_BLOCKS)):
                    display = displays.nth(index)
                    display.scroll_into_view_if_needed()
                    target = out / f"{name}-disp{index}.png"
                    display.screenshot(path=str(target))
                    record(name, f"disp{index}", target)
        finally:
            browser.close()

    return [montage for key in sorted(taken) if (montage := _montage(out, key, taken[key]))]


#: Width of the label gutter each montage row carries, in device pixels. The shots are
#: taken at 3x, so a row is wide; the gutter is what makes a stack readable at all.
LABEL_GUTTER = 200
ROW_PADDING = 24


def _montage(out: Path, key: str, rows: Sequence[tuple[str, Path]]) -> Path | None:
    """Stack one element's shots in route order, each row named in its own gutter."""
    try:
        from PIL import Image, ImageDraw  # noqa: PLC0415
    except ImportError:  # pragma: no cover - Pillow arrives with cairosvg
        message = "Pillow is required to stack the shots; install the dev group"
        raise SystemExit(message) from None

    images = [(name, Image.open(path).convert("RGB")) for name, path in rows]
    if not images:
        return None
    width = max(image.width for _, image in images) + LABEL_GUTTER
    height = sum(image.height + ROW_PADDING for _, image in images)
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    offset = 0
    for name, image in images:
        draw.text((8, offset + 8), name, fill=(180, 0, 0))
        canvas.paste(image, (LABEL_GUTTER, offset + 12))
        offset += image.height + ROW_PADDING
        draw.line([(0, offset - 1), (width, offset - 1)], fill=(220, 220, 220))
    target = out / f"montage-{key}.png"
    canvas.save(target)
    print(f"wrote {target.name} ({canvas.size[0]}x{canvas.size[1]})")
    return target


def main(argv: Sequence[str] | None = None) -> int:
    command = argparse.ArgumentParser(description=__doc__)
    subcommands = command.add_subparsers(dest="command", required=True)

    table = subcommands.add_parser("metrics", help="measure the shipped faces")
    table.add_argument(
        "fonts", nargs="*", type=Path, help="extra font files to measure alongside them"
    )

    build = subcommands.add_parser("variants", help="build variant pages from a rendered page")
    build.add_argument("--page", type=Path, default=PAGE, help="the rendered explainer")
    build.add_argument("--out", type=Path, required=True, help="directory to write into")
    build.add_argument("--spec", type=Path, help="JSON of extra {name: {css, label}} variants")
    build.add_argument(
        "--metrics-patch",
        action="store_true",
        help="also rewrite KaTeX's metric table for the code points each variant swaps",
    )

    shots = subcommands.add_parser("shots", help="screenshot and stack the variant pages")
    shots.add_argument(
        "--variants", type=Path, required=True, help="directory of variant pages"
    )
    shots.add_argument("--out", type=Path, required=True, help="directory to write into")
    shots.add_argument("--only", nargs="+", default=(), help="variant names to shoot")

    arguments = command.parse_args(argv)
    if arguments.command == "metrics":
        faces = [*DEFAULT_FACES, *((path.stem, path) for path in arguments.fonts)]
        print(metrics_table([measure(label, path) for label, path in faces]))
    elif arguments.command == "variants":
        build_variants(
            arguments.page,
            arguments.out,
            arguments.spec,
            metrics_patch=arguments.metrics_patch,
        )
    else:
        take_shots(arguments.variants, arguments.out, arguments.only)
    return 0


if __name__ == "__main__":
    sys.exit(main())
