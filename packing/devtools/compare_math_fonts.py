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

The variants are built against the stock KaTeX baseline; the page's own math text face
is switched off first. That is not a nicety: the page this now runs on renders with
kpress's `KPress Math Text` composite as the root family and installs kpress's metric
tables inline, so a variant injected on top of it would compare two versions of the
feature rather than the routes the research compared. `stock_katex_baseline` stamps
`data-kpress-math-text="katex"` on `<html>`, which is the opt-out both halves read: the
stylesheet's rules are scoped to a `.kpress` with no opted-out ancestor, and the page's
metrics installer returns early. With that stamped, `current` is Route A again, each
variant's CSS lands on upstream's `.katex` rules, and `--metrics-patch` reaches the
table KaTeX actually lays out from.

What a variant is made of is `unicode-range` faces, and that is not a stylistic choice.
KaTeX picks the face by class, and digits, operators, operator names and `\text{}` carry
no class at all: they are drawn by whatever family the root `.katex` rule names. So
"digits from PT Serif, operators from KaTeX" cannot be said in class selectors, only in
a family restricted to the code points the route moves. Each is the reading face alone,
with KaTeX's own face after it in the rule's family list rather than inside it, so a
range a later family was added to serve is still there to be claimed -- a family covering
the whole plane shadows what follows it, which is how the scaled Greek capitals came to
be declared and never drawn.

`--metrics-patch` is the honest version of the same page. KaTeX lays out from a table of
`[depth, height, italic, skew, width]` baked into `katex.min.js`, so a swapped face is
drawn at one size and placed at another: PT Serif digits are 0.046em taller than the
Computer Modern digits KaTeX believes it is placing, and at 3x device scale the top of a
numerator clips. The flag rewrites the entries for exactly the code points a variant
swaps, from the PT Serif files' own bounds. Skew is left at KaTeX's value, because it
places an accent over a glyph rather than describing the glyph, and the scaled Greek is
the one case where every number moves, since there the glyph itself is scaled.

`check` and `verify` are what keep the two halves of a route in step, because a route is
described twice -- once to the browser as CSS and once to KaTeX as a metric plan -- and
four routes were shipped whose descriptions disagreed. `check` reads both descriptions
and reports the code points where they differ; it needs a rendered page for the faces and
no browser. `verify` reads the page they produced: it draws representative inputs in each
variant and compares the advance the browser inked with the width KaTeX summed from its
own table, which is the check that cannot be satisfied by writing the same mistake twice.
Neither is a nicety. A route that draws one face and measures another produces no error
anywhere -- only a montage answering a question nobody asked.
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
from strif import atomic_output_file

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
    # A face without an OS/2 table (some bare TrueType conversions) still has ink to
    # measure; the table is only the declared shortcut for the two heights.
    os2 = font.get("OS/2")
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
    """The inlined faces a route's families are assembled from, as `data:` URLs.

    Taken out of the rendered page rather than out of the font files, so a variant is a
    string operation on one self-contained document: no network, no second render, and
    the route is built from the same bytes the page already ships.

    One reading face per style KaTeX can put a Latin letter in, because a route that
    moves `\\mathbf` has to move it in bold or draw a weight the metric table is not
    describing. `file` names which woff2 each URL came from, which is how `reconcile`
    below joins a CSS rule back to the glyph coverage it actually has.
    """

    pt_regular: str
    pt_italic: str
    pt_bold: str
    katex_main: str
    katex_math_italic: str

    def file(self, url: str) -> str | None:
        """The woff2 a `data:` URL was taken from, for the reading faces only."""
        return {
            self.pt_regular: _PT_REGULAR_FILE,
            self.pt_italic: _PT_ITALIC_FILE,
            self.pt_bold: _PT_BOLD_FILE,
        }.get(url)


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
    """The faces every route below is built from."""
    return PageFaces(
        pt_regular=_prose_face(html, "PT Serif", "normal", "400"),
        pt_italic=_prose_face(html, "PT Serif", "italic", "400"),
        pt_bold=_prose_face(html, "PT Serif", "normal", "700"),
        katex_main=_katex_face(html, "KaTeX_Main", "normal", "400"),
        katex_math_italic=_katex_face(html, "KaTeX_Math", "italic", "400"),
    )


#: The code points a route can move, as the metric table indexes them.
_DIGITS = tuple(range(0x30, 0x3A))
_LETTERS = tuple(range(0x41, 0x5B)) + tuple(range(0x61, 0x7B))
_ALPHANUMERIC = _DIGITS + _LETTERS

#: The five characters the one operator-moving route adds, spelled out because they are
#: the whole of what separates it: `+`, `<`, `=`, `>`, and U+2212, which is the minus
#: KaTeX sets for `-` in math and not the hyphen a source file would otherwise carry.
_OPERATORS = (0x2B, 0x3C, 0x3D, 0x3E, 0x2212)

_GREEK = tuple(range(0x370, 0x400))
_GREEK_CAPITALS = tuple(range(0x391, 0x3AA))

#: Greek plus the two dotless letters KaTeX draws from the same italic math face. The
#: scaled family claims them, so the scaled metric plan has to reach them too, even
#: though this page sets no `\imath` and the table has no row for either.
_GREEK_SCALED = (*_GREEK, 0x1D6A4, 0x1D6A5)

#: Lowercase Greek to PT Serif's x-height, 500/441; capitals, which KaTeX sets upright
#: from Main-Regular, to its cap height, 700/683. Scaling by the x-height ratio also
#: thickens the strokes by the same 13%, which is the second half of why it helps.
GREEK_SCALE = 1.134
GREEK_CAPITAL_SCALE = 1.025

#: A face or a scale over `WHOLE_FACE` covers every glyph the file has rather than a
#: named range. That is what a `size-adjust` on a family with no `unicode-range` applies
#: to, and so what the metric patch has to move: every row of that face's table.
WHOLE_FACE: tuple[int, ...] | None = None


def _ranges(code_points: Iterable[int]) -> str:
    """A `unicode-range` list covering exactly these code points, runs collapsed.

    Written rather than hand-typed so one tuple is the whole description of a route: the
    range the browser reads and the entries the metric patch rewrites cannot then say
    different things, which is the failure this module is most prone to.
    """
    ordered = sorted(set(code_points))
    if not ordered:
        raise ValueError("a face restricted to no code points would never be reached")
    runs: list[list[int]] = []
    for point in ordered:
        if runs and point == runs[-1][1] + 1:
            runs[-1][1] = point
        else:
            runs.append([point, point])
    return ", ".join(
        f"U+{low:04X}" if low == high else f"U+{low:04X}-{high:04X}" for low, high in runs
    )


#: Which of KaTeX's metric tables each CSS rule a route writes is laid out from. This is
#: the join the whole reconciliation turns on, and the reason a route cannot be read off
#: its class selectors alone: KaTeX looks a character's box up by *face*, never by class,
#: so two selectors landing in the same table have to draw from the same font or one of
#: them is placed from a measurement of the other. `.katex` is the root rule, which draws
#: everything KaTeX gives no font class at all -- digits, operators, and the letters of
#: the built-in operator names `\sin`, `\cos`, `\tan` -- and it shares Main-Regular with
#: `\text` and `\mathrm`, which is why no route can move one of those and not the other.
SELECTOR_FACES: tuple[tuple[str, str], ...] = (
    (".katex", "Main-Regular"),
    (".mainrm", "Main-Regular"),
    (".textrm", "Main-Regular"),
    (".mathrm", "Main-Regular"),
    (".mathnormal", "Math-Italic"),
    (".mathit", "Main-Italic"),
    (".mathbf", "Main-Bold"),
)


@dataclass(frozen=True)
class Variant:
    """One page variant: what to inject, what it shows, and what it moves.

    `swaps` and `scales` describe the same change to KaTeX's metric table that the CSS
    describes to the browser, so `--metrics-patch` rewrites exactly the entries whose
    glyphs the variant actually redirects and no others. `reconcile` below is what holds
    the two descriptions to each other; every built-in route is checked by it in the
    tests, because the two were written by hand once and disagreed four ways.
    """

    name: str
    label: str
    css: str
    #: `(metric face, PT Serif file, code points)` for glyphs drawn from another file.
    swaps: tuple[tuple[str, str, tuple[int, ...]], ...] = ()
    #: `(metric face, code points or `WHOLE_FACE`, factor)` for glyphs drawn from the
    #: same file, scaled.
    scales: tuple[tuple[str, tuple[int, ...] | None, float], ...] = ()


_PT_REGULAR_FILE = "pt-serif-latin-400-normal.woff2"
_PT_ITALIC_FILE = "pt-serif-latin-400-italic.woff2"
_PT_BOLD_FILE = "pt-serif-latin-700-normal.woff2"

#: The families a route declares, named for what they carry rather than for the KaTeX
#: face they stand in front of. Each is the reading face alone, restricted to the route's
#: own code points; the KaTeX face follows it in the rule's family list, which is where
#: anything outside that range is answered. Two families rather than one composite,
#: because a composite claiming the whole plane also claims the ranges a later family in
#: the list was added to serve -- which is exactly how the scaled Greek capitals came to
#: be shadowed.
_UPRIGHT_FAMILY = "PT Math Upright"
_ITALIC_FAMILY = "PT Math Italic"
_BOLD_FAMILY = "PT Math Bold"


def _face(
    family: str,
    src: str,
    code_points: tuple[int, ...] | None,
    *,
    style: str = "normal",
    weight: str = "400",
    adjust: float | None = None,
) -> str:
    """One `@font-face`, restricted to the code points the route claims to move."""
    size_adjust = "" if adjust is None else f"\n  size-adjust: {adjust * 100:.1f}%;"
    restriction = "" if code_points is None else f"\n  unicode-range: {_ranges(code_points)};"
    return (
        f'@font-face {{ font-family: "{family}"; font-style: {style}; '
        f"font-weight: {weight};\n"
        f'  src: url("{src}") format("woff2");{size_adjust}{restriction} }}\n'
    )


def _upright_css(faces: PageFaces, code_points: tuple[int, ...], greek: str = "") -> str:
    r"""Upright glyphs from the reading face, everywhere KaTeX draws them upright.

    Two rules and one family, written together because both are laid out from
    Main-Regular's rows. The root rule draws every character KaTeX gives no font class:
    digits, operators, and the letters of `\sin` and `\tan`. The class rule draws `\text`
    and `\mathrm`. A route that moved one and left the other on KaTeX would be measured
    from a face it does not draw for whichever half it left behind, and there is no
    second Main-Regular table to give them different answers.
    """
    tail = f'"{_UPRIGHT_FAMILY}", {greek}KaTeX_Main'
    return (
        _face(_UPRIGHT_FAMILY, faces.pt_regular, code_points)
        + f'.kpress .katex {{ font-family: {tail}, "Times New Roman", serif; }}\n'
        + ".kpress .katex .mainrm, .kpress .katex .textrm, .kpress .katex .mathrm {\n"
        + f"  font-family: {tail}; }}\n"
    )


def _italic_css(faces: PageFaces, greek: str = "") -> str:
    """Italic variables from PT Serif Italic; Greek is left to the family after it."""
    return (
        _face(_ITALIC_FAMILY, faces.pt_italic, _LETTERS, style="italic")
        + ".kpress .katex .mathnormal {\n"
        + f'  font-family: "{_ITALIC_FAMILY}", {greek}KaTeX_Math; font-style: italic; }}\n'
    )


def _every_style_css(faces: PageFaces, greek: str = "") -> str:
    r"""The italic route plus the other two styles a Latin letter can be set in.

    `\boldsymbol` is deliberately absent. Its face is KaTeX_Math bold italic, which this
    page does not carry -- the renderer prunes it as unreachable, the same slot the
    shipped composite drops -- and no route here plans a Math-BoldItalic patch. A rule
    for it would draw the reading face out of a table nothing had rewritten, which is the
    one thing every route above is arranged not to do.
    """
    return (
        _italic_css(faces, greek)
        + ".kpress .katex .mathit {\n"
        + f'  font-family: "{_ITALIC_FAMILY}", KaTeX_Main; font-style: italic; }}\n'
        + _face(_BOLD_FAMILY, faces.pt_bold, _ALPHANUMERIC, weight="700")
        + ".kpress .katex .mathbf {\n"
        + f'  font-family: "{_BOLD_FAMILY}", KaTeX_Main; font-weight: 700; }}\n'
    )


_ONE_EM_CSS = """
.kpress { --kpress-katex-size-prose: 1em; }
"""

#: Upright text and the built-in operator names share Main-Regular, so every route that
#: moves one moves both, and the plan patches the letters as well as the digits.
_UPRIGHT_SWAPS = (("Main-Regular", _PT_REGULAR_FILE, _ALPHANUMERIC),)
_LETTER_SWAPS = (*_UPRIGHT_SWAPS, ("Math-Italic", _PT_ITALIC_FILE, _LETTERS))
_ALL_SWAPS = (
    *_LETTER_SWAPS,
    ("Main-Italic", _PT_ITALIC_FILE, _LETTERS),
    ("Main-Bold", _PT_BOLD_FILE, _ALPHANUMERIC),
)
#: The operator route draws five more characters from the reading face, and they are
#: Main-Regular's rows too: an unpatched `+` is placed in a box 0.24 em wider than the
#: glyph that lands in it.
_OPERATOR_SWAPS = (
    ("Main-Regular", _PT_REGULAR_FILE, _ALPHANUMERIC + _OPERATORS),
    *_ALL_SWAPS[1:],
)


def built_in_variants(faces: PageFaces) -> tuple[Variant, ...]:
    """The eight routes the research rendered, in the order it compares them.

    All eight are relative to stock KaTeX, which is what `stock_katex_baseline` restores
    before any of this CSS is injected: `current` is that baseline with nothing added,
    and every other route is one or more restricted reading faces on top of it.
    """
    upright = _upright_css(faces, _ALPHANUMERIC)
    every_style = _every_style_css(faces)
    size_adjusted = _face(
        "KaTeX_MathAdj",
        faces.katex_math_italic,
        WHOLE_FACE,
        style="italic",
        adjust=GREEK_SCALE,
    ) + (
        ".kpress .katex .mathnormal {\n"
        '  font-family: "KaTeX_MathAdj", KaTeX_Math; font-style: italic; }\n'
    )
    greek_faces = _face(
        "KaTeX_MathGreek",
        faces.katex_math_italic,
        _GREEK_SCALED,
        style="italic",
        adjust=GREEK_SCALE,
    ) + _face("KaTeX_MainGreek", faces.katex_main, _GREEK_CAPITALS, adjust=GREEK_CAPITAL_SCALE)
    return (
        Variant(
            "current",
            "Route A: stock KaTeX, every glyph from the KaTeX faces",
            "",
        ),
        Variant(
            "digits",
            "Route B: digits and upright text from PT Serif, operator names with them; "
            "variables stay KaTeX_Math",
            upright,
            swaps=_UPRIGHT_SWAPS,
        ),
        Variant(
            "letters",
            "Route C: B plus italic variables from PT Serif Italic",
            upright + _italic_css(faces),
            swaps=_LETTER_SWAPS,
        ),
        Variant(
            "all",
            "Route D: every Latin letter and digit from PT Serif, in every style",
            upright + every_style,
            swaps=_ALL_SWAPS,
        ),
        Variant(
            "all-1em",
            "Route E: D with the prose KaTeX size token at 1em instead of 1.05em",
            upright + every_style + _ONE_EM_CSS,
            swaps=_ALL_SWAPS,
        ),
        Variant(
            "sizeadj",
            "Route F, eliminated: B plus KaTeX_Math size-adjusted to PT Serif's x-height",
            upright + size_adjusted,
            swaps=_UPRIGHT_SWAPS,
            # The adjusted family carries no `unicode-range`, so it draws every glyph
            # `.mathnormal` reaches -- Greek as much as Latin -- and the plan scales the
            # whole table with it. Scaling only the letters left `\alpha` drawn 13.4%
            # larger than the box KaTeX had placed it in.
            scales=(("Math-Italic", WHOLE_FACE, GREEK_SCALE),),
        ),
        Variant(
            "ops",
            "Route H, eliminated: D plus + - = < > from PT Serif, as mathastext does",
            _upright_css(faces, _ALPHANUMERIC + _OPERATORS) + every_style,
            swaps=_OPERATOR_SWAPS,
        ),
        Variant(
            "greek",
            "Route J: E plus Greek scaled to PT Serif, lowercase 113.4%, capitals 102.5%",
            _upright_css(faces, _ALPHANUMERIC, greek='"KaTeX_MainGreek", ')
            + _every_style_css(faces, greek='"KaTeX_MathGreek", ')
            + _ONE_EM_CSS
            + greek_faces,
            swaps=_ALL_SWAPS,
            scales=(
                ("Math-Italic", _GREEK_SCALED, GREEK_SCALE),
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
    variants: list[Variant] = []
    for name, body in declared.items():
        # `label` has a default and `css` cannot: a variant with no CSS is the built-in
        # `current` under another name. Refused by sentence rather than by traceback,
        # which is what every other input failure in this module does.
        if "css" not in body:
            raise SystemExit(f"{spec}: variant {name!r} declares no `css`")
        variants.append(Variant(name, str(body.get("label", name)), str(body["css"])))
    return tuple(variants)


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
    whole_face: float | None = None,
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
        if len(values) != 5:
            raise SystemExit(
                f"KaTeX metric entry {code_point} has {len(values)} values, not five; "
                "the bundle's table shape has changed"
            )
        if code_point in replacements:
            depth, height, italic, width = replacements[code_point]
            rewritten += 1
            # Skew stays KaTeX's: it places an accent over a glyph rather than
            # describing the glyph, and no measurement here replaces it.
            return (
                f"{code_point}:[{depth:.5f},{height:.5f},{italic:.5f},{values[3]},{width:.5f}]"
            )
        factor = factors.get(code_point, whole_face)
        if factor is not None:
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
            if scaled == face and code_points is not None
            for code_point in code_points
        }
        # A `WHOLE_FACE` scale reaches rows this module never enumerates, so it is
        # applied by the rewrite itself rather than expanded into `factors` here: the
        # table is the only place the face's own row list exists.
        whole = next(
            (
                factor
                for scaled, code_points, factor in variant.scales
                if scaled == face and code_points is None
            ),
            None,
        )
        html, rewritten = _rewrite_face_table(html, face, replacements, factors, whole)
        total += rewritten
    return html, total


# Holding the CSS and the metric plan to each other.

#: The woff2 behind each of KaTeX's metric tables. A table is generated from its face, so
#: this is also what says whether a table has a row for a code point at all -- which is
#: what keeps the check below from reporting a disagreement about a row that cannot exist.
_METRIC_FACE_FILES = {
    "Main-Regular": "KaTeX_Main-Regular.woff2",
    "Main-Italic": "KaTeX_Main-Italic.woff2",
    "Main-Bold": "KaTeX_Main-Bold.woff2",
    "Math-Italic": "KaTeX_Math-Italic.woff2",
}

#: Where a route and its plan can disagree at all: the alphanumerics and operators any
#: route moves, and the Greek one route scales. Nothing outside it is redirected by any
#: built-in route, and the check is per code point, so a wider set would only be slower.
_PROBE_POINTS = _ALPHANUMERIC + _OPERATORS + _GREEK

#: A family named in a rule but declared nowhere in the variant's CSS: KaTeX's own, or
#: the generic tail. It draws the stock face at stock size, which is what a plan that
#: says nothing about a code point is asserting.
STOCK = "KaTeX"


@dataclass(frozen=True)
class _Declared:
    """One `@font-face` a variant's CSS declares, as the browser would match it."""

    family: str
    style: str
    weight: str
    source: str
    points: frozenset[int] | None
    adjust: float


_FONT_FACE = re.compile(r"@font-face\s*\{([^{}]*)\}")
_RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")
_RANGE = re.compile(r"U\+([0-9A-Fa-f]+)(?:-([0-9A-Fa-f]+))?")
#: Read on its own, because a `data:` URL carries the `;` every other property ends at.
_SRC = re.compile(r'src:\s*url\("([^"]+)"\)')


def _declaration(body: str, name: str, fallback: str = "") -> str:
    match = re.search(rf"(?:^|;)\s*{name}\s*:\s*([^;]+)", body)
    return match.group(1).strip() if match else fallback


def _declared_faces(css: str) -> list[_Declared]:
    """Every `@font-face` in a variant's CSS, in declaration order."""
    declared: list[_Declared] = []
    for match in _FONT_FACE.finditer(css):
        body = match.group(1)
        restriction = _declaration(body, "unicode-range")
        points = None
        if restriction:
            points = frozenset(
                point
                for low, high in _RANGE.findall(restriction)
                for point in range(int(low, 16), int(high or low, 16) + 1)
            )
        adjust = _declaration(body, "size-adjust", "100%")
        source = _SRC.search(body)
        if source is None:
            raise SystemExit(f"an @font-face in the variant's CSS declares no url(): {body}")
        declared.append(
            _Declared(
                family=_declaration(body, "font-family").strip("\"'"),
                style=_declaration(body, "font-style", "normal"),
                weight=_declaration(body, "font-weight", "400"),
                source=source.group(1),
                points=points,
                adjust=float(adjust.rstrip("%")) / 100,
            )
        )
    return declared


def _rules(css: str) -> list[tuple[list[str], str, str, list[str]]]:
    """Each rule that names a family, as `(selectors, style, weight, family list)`."""
    found: list[tuple[list[str], str, str, list[str]]] = []
    for match in _RULE.finditer(_FONT_FACE.sub("", css)):
        families = _declaration(match.group(2), "font-family")
        if not families:
            continue
        found.append(
            (
                [selector.strip() for selector in match.group(1).split(",")],
                _declaration(match.group(2), "font-style", "normal"),
                _declaration(match.group(2), "font-weight", "400"),
                [family.strip().strip("\"'") for family in families.split(",")],
            )
        )
    return found


def _drawn_by(
    families: Sequence[str],
    style: str,
    weight: str,
    code_point: int,
    *,
    declared: Sequence[_Declared],
    coverage: dict[str, frozenset[int]],
) -> tuple[str, float]:
    """Which face a rule's family list actually draws a code point from, and at what size.

    The browser's own order: each family in turn, and within a family the declaration
    whose style and weight match and whose `unicode-range` claims the character. A family
    that claims the character but whose file has no glyph for it does not answer, which is
    the difference between a route that moves a glyph and one that only says it does.
    """
    names = {face.family for face in declared}
    for family in families:
        if family not in names:
            # KaTeX's own, or the generic tail: whatever it is, it is not this route's.
            return STOCK, 1.0
        for face in declared:
            if face.family != family or face.style != style or face.weight != weight:
                continue
            if face.points is not None and code_point not in face.points:
                continue
            if code_point not in coverage[face.source]:
                continue
            return face.source, face.adjust
    return STOCK, 1.0


def _planned(variant: Variant, face: str, code_point: int) -> tuple[str, float]:
    """The file and size the plan says that face's row for a code point was rewritten to.

    A swap moves the row to another file at its own size; a scale keeps KaTeX's own file
    and multiplies every number in the row. A code point in neither is KaTeX's, untouched,
    which is the same pair as a scale of one over the face's own file -- so both sides of
    the comparison can be written as one `(file, factor)` and neither needs a third state.
    """
    for swapped, filename, points in variant.swaps:
        if swapped == face and code_point in points:
            return filename, 1.0
    for scaled, points, factor in variant.scales:
        if scaled == face and (points is None or code_point in points):
            return _METRIC_FACE_FILES[face], factor
    return _METRIC_FACE_FILES[face], 1.0


def reconcile(variant: Variant, faces: PageFaces, font_dir: Path = PROSE_FONTS) -> list[str]:
    r"""Every disagreement between the glyphs `variant` draws and the boxes it measures.

    Two independent descriptions of one route meet here. The CSS says which file draws a
    character; `swaps` and `scales` say which file KaTeX was told to lay it out from. They
    were written side by side once and disagreed four ways -- `\sin` drawn from KaTeX and
    measured from PT Serif, a whole face scaled in CSS and only its letters in the plan,
    five operators moved with no entries for them, and scaled Greek capitals shadowed by an
    earlier family claiming the whole plane. None of the four is an error at any point in
    the pipeline: each is a page that draws one font and places it from another, which is
    visible only as a montage answering a question nobody asked.

    Reported per metric face rather than per selector, because the table is per face: two
    selectors that reach the same table must draw from the same file, and a route that
    moves `\text` without moving the operator names is not a route the table can express.
    """
    declared = _declared_faces(variant.css)
    sources = {
        faces.pt_regular: font_dir / _PT_REGULAR_FILE,
        faces.pt_italic: font_dir / _PT_ITALIC_FILE,
        faces.pt_bold: font_dir / _PT_BOLD_FILE,
        faces.katex_main: KATEX_FONTS / "KaTeX_Main-Regular.woff2",
        faces.katex_math_italic: KATEX_FONTS / "KaTeX_Math-Italic.woff2",
    }
    coverage = {
        url: frozenset(_unicode_cmap(TTFont(path), path)) for url, path in sources.items()
    }
    named = {url: path.name for url, path in sources.items()}
    rules = _rules(variant.css)

    # Gathered before anything is reported, and keyed by what the disagreement is rather
    # than by where it was found, so that a run of code points saying the same thing is
    # one line naming a range instead of fifty-two naming a letter each.
    disagreements: dict[tuple[str, ...], list[int]] = {}
    for face, filename in _METRIC_FACE_FILES.items():
        path = KATEX_FONTS / filename
        rows = frozenset(_unicode_cmap(TTFont(path), path))
        selectors = [selector for selector, reached in SELECTOR_FACES if reached == face]
        for code_point in _PROBE_POINTS:
            if code_point not in rows:
                continue
            planned, scale = _planned(variant, face, code_point)
            for selector in selectors:
                matching = [
                    rule for rule in rules if any(one.endswith(selector) for one in rule[0])
                ]
                if not matching:
                    drawn, adjust = STOCK, 1.0
                else:
                    _, style, weight, families = matching[-1]
                    drawn, adjust = _drawn_by(
                        families,
                        style,
                        weight,
                        code_point,
                        declared=declared,
                        coverage=coverage,
                    )
                # An undeclared family is KaTeX's own face at its own size, which is the
                # same pair the plan writes for a row it leaves alone.
                source = named.get(drawn, filename)
                if source == planned and abs(adjust - scale) < 1e-9:
                    continue
                key = (
                    face,
                    selector,
                    f"{source} at {adjust:.3f}",
                    f"{planned} at {scale:.3f}",
                )
                disagreements.setdefault(key, []).append(code_point)

    return [
        f"{variant.name}: {face}'s rows for {_ranges(points)} are drawn through "
        f"`{selector}` from {source}, but the plan measures them from {plan}"
        for (face, selector, source, plan), points in disagreements.items()
    ]


# Building the pages.

#: Figures the page loads from beside itself; without them a variant renders broken art.
SIBLING_ASSETS = ("known-best-1-100*.png", "known-best-1-100*.svg")

#: kpress's opt-out for its own math text face, and the tag it is stamped on. One
#: attribute turns off both halves of the feature, which is why the baseline is a
#: stamp rather than a deletion: `katex-text-face.css` scopes every rule to a `.kpress`
#: with no opted-out ancestor, and the page's inline metrics installer reads the same
#: three selectors before it touches KaTeX's tables.
MATH_TEXT_OPT_OUT = 'data-kpress-math-text="katex"'
_HTML_TAG = re.compile(r"<html\b[^>]*>", re.IGNORECASE)
_MATH_TEXT_ATTRIBUTE = re.compile(r"""\s*data-kpress-math-text\s*=\s*(["'])[^"']*\1""")


def stock_katex_baseline(html: str) -> str:
    """Switch the page's own math text face off, so a variant measures against KaTeX.

    The routes below are defined against stock KaTeX: `current` is every glyph from the
    KaTeX faces, and every other variant is that page plus one injected family. The page
    this runs on no longer starts there, so the baseline is restored rather than assumed
    -- otherwise `current` would be kpress's feature, the injected families would sit on
    top of it, and `--metrics-patch` would be overwritten by the page's own tables at
    load.

    An existing `data-kpress-math-text` is replaced rather than joined, since a second
    copy of the attribute on one tag is ignored by the parser and the page's own value
    would stand.
    """
    match = _HTML_TAG.search(html)
    if match is None:
        raise SystemExit(
            "the page carries no <html> tag; the math text face cannot be switched off"
        )
    tag = match.group(0)
    if _MATH_TEXT_ATTRIBUTE.search(tag) is not None:
        tag = _MATH_TEXT_ATTRIBUTE.sub(f" {MATH_TEXT_OPT_OUT}", tag, count=1)
    else:
        tag = f"{tag[:-1].rstrip()} {MATH_TEXT_OPT_OUT}>"
    return html[: match.start()] + tag + html[match.end() :]


def build_variants(
    page: Path,
    out: Path,
    spec: Path | None = None,
    font_dir: Path = PROSE_FONTS,
    *,
    metrics_patch: bool = False,
) -> list[Path]:
    """Write one page per variant beside a copy of the figures they reference.

    Every variant is built against the stock KaTeX baseline: the page's own math text
    face is switched off first, by `stock_katex_baseline`, before any variant CSS is
    injected. The faces each composite is assembled from are still the page's own bytes;
    only the feature that would draw with them unbidden is off.
    """
    if not page.is_file():
        raise SystemExit(f"no rendered page at {page}; render the explainer first")
    html = stock_katex_baseline(page.read_text(encoding="utf-8"))
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
        with atomic_output_file(target) as temporary:
            temporary.write_text(page_html, encoding="utf-8")
        written.append(target)
        print(f"wrote {target.name}{note}")

    for pattern in SIBLING_ASSETS:
        for asset in sorted(page.parent.glob(pattern)):
            shutil.copy2(asset, out / asset.name)

    resolved = page.resolve()
    source = resolved.relative_to(REPO) if resolved.is_relative_to(REPO) else resolved
    readme = out / "README.txt"
    with atomic_output_file(readme) as temporary:
        temporary.write_text(
            "Variants of "
            + str(source)
            + ", built by devtools.compare_math_fonts, against the stock KaTeX baseline\n"
            + "(the page's own math text face switched off).\n"
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
_NAMES_ONLY = PageFaces("", "", "", "", "")


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


# Checking the pages in a browser.

#: One input for each way a route can reach a metric table, which is one input for each of
#: the four defects the reconciliation above was written for: the letters of a built-in
#: operator name and a digit run reach Main-Regular through the root rule, `\text` reaches
#: it through a class, an operator reaches it as itself; `\alpha` reaches Math-Italic and
#: `\Gamma` is the upright capital KaTeX draws from Main-Regular; `x` and `\mathbf{D}` are
#: the plain variable and the one bold letter this page actually sets.
#: One character per input wherever an input can be one. KaTeX merges adjacent symbols
#: that share a class into a single node and concatenates their text without summing
#: their widths, so a multi-character run's declared width is its first character's. The
#: probe below refuses such a node rather than comparing against it; `\sin` is exempt
#: because operator names are built without that merge, which is also why they are the
#: run this whole finding was reported on.
VERIFY_INPUTS: tuple[str, ...] = (
    r"\sin",
    r"\alpha",
    "+",
    r"\Gamma",
    "4",
    "x",
    r"\text{f}",
    r"\mathbf{D}",
)

#: How far a drawn advance may sit from the width KaTeX placed it in, in em. Every route
#: now agrees to within 0.0016 em, which is the browser's own rounding of a subpixel
#: advance; the four defects this was written for were 0.016, 0.086, 0.100 and 0.245 em
#: out. The threshold sits an order of magnitude clear of each side of that gap.
VERIFY_TOLERANCE_EM = 0.01

#: Draw each input into the page and read back both numbers: the advance the browser
#: actually inked, and the width KaTeX summed from its own table to place it. Both come
#: from one call, on the page's own KaTeX build, inside the column so that the rules and
#: the size the page sets are the ones in force -- a measurement taken in a bare document
#: would compare fonts nobody is looking at.
_ADVANCES = r"""(inputs) => {
  const column = document.querySelector('.kpress');
  const host = document.createElement('span');
  column.appendChild(host);
  const measured = [];
  try {
    for (const input of inputs) {
      host.textContent = '';
      const tree = katex.__renderToDomTree(input, {throwOnError: true, displayMode: false});
      host.appendChild(tree.toNode());
      const drawn = host.firstElementChild;
      const size = parseFloat(getComputedStyle(drawn).fontSize);
      measured.push({
        input,
        /* The sum of the leaves' own boxes: KaTeX's table is per glyph, and what it
           places is the run, so the run is what compares with the drawn advance. */
        metric: leaves(tree),
        drawn: drawn.getBoundingClientRect().width / size,
      });
    }
  } finally {
    host.remove();
  }
  return measured;

  /* A symbol's box is its advance plus its italic correction, because that is what
     KaTeX draws: `SymbolNode.toNode` puts the correction on the node as a right margin,
     and an inline margin widens the box the browser reports for the run around it. The
     two numbers are separate rows in the metric table and the patch rewrites both. */
  function leaves(node) {
    if (typeof node.width === 'number' && typeof node.text === 'string') {
      if ([...node.text].length > 1) {
        throw new Error(
          'KaTeX merged ' + JSON.stringify(node.text) + ' into one node, whose declared '
          + 'width is only its first character: pick a single-character input');
      }
      return node.width + (node.italic || 0);
    }
    return (node.children || []).reduce((sum, child) => sum + leaves(child), 0);
  }
}"""


def verify_advances(variants_dir: Path, only: Sequence[str] = ()) -> list[str]:
    r"""Compare what each variant page draws with what its metric table placed.

    The reconciliation above reads the two descriptions of a route; this reads the page
    they produced. It is the check that cannot be satisfied by writing the same mistake
    twice: the advance comes from the browser's own layout of the shipped woff2, and the
    width comes from the table `--metrics-patch` rewrote, so a route drawing one face and
    measuring another is a difference between two numbers rather than between two files.

    Run over pages built with `--metrics-patch`; without it every route disagrees by
    construction, which is the entire point of the flag.
    """
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    pages = _variant_order(variants_dir, only)
    if not pages:
        raise SystemExit(f"no variant pages in {variants_dir}; run `variants` first")
    failures: list[str] = []
    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        try:
            page = browser.new_page()
            for source in pages:
                page.goto(source.resolve().as_uri(), wait_until="load")
                page.wait_for_selector(READY, timeout=60_000)
                page.evaluate("document.fonts.ready")
                rows: list[dict[str, Any]] = page.evaluate(_ADVANCES, list(VERIFY_INPUTS))
                for row in rows:
                    off = abs(float(row["drawn"]) - float(row["metric"]))
                    mark = " " if off <= VERIFY_TOLERANCE_EM else "*"
                    print(
                        f"{mark} {source.stem:9} {row['input']:12} "
                        f"drawn {row['drawn']:.5f}em  metric {row['metric']:.5f}em  "
                        f"off {off:.5f}em"
                    )
                    if off > VERIFY_TOLERANCE_EM:
                        failures.append(
                            f"{source.stem}: {row['input']} is drawn {row['drawn']:.5f}em "
                            f"wide and placed in {row['metric']:.5f}em"
                        )
        finally:
            browser.close()
    return failures


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

    check = subcommands.add_parser(
        "check", help="hold every route's CSS to its own metric plan, without a browser"
    )
    check.add_argument("--page", type=Path, default=PAGE, help="the rendered explainer")

    verify = subcommands.add_parser(
        "verify", help="compare drawn advances with KaTeX's widths in a browser"
    )
    verify.add_argument(
        "--variants", type=Path, required=True, help="directory of variant pages"
    )
    verify.add_argument("--only", nargs="+", default=(), help="variant names to verify")

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
    elif arguments.command == "check":
        return _report(check_routes(arguments.page), "every route draws what it measures")
    elif arguments.command == "verify":
        return _report(
            verify_advances(arguments.variants, arguments.only),
            "every drawn advance matches the width it was placed in",
        )
    else:
        take_shots(arguments.variants, arguments.out, arguments.only)
    return 0


def check_routes(page: Path) -> list[str]:
    """Reconcile every built-in route against its own metric plan, from a rendered page."""
    if not page.is_file():
        raise SystemExit(f"no rendered page at {page}; render the explainer first")
    html = stock_katex_baseline(page.read_text(encoding="utf-8"))
    faces = page_faces(html)
    return [line for variant in built_in_variants(faces) for line in reconcile(variant, faces)]


def _report(failures: Sequence[str], clean: str) -> int:
    for failure in failures:
        print(failure)
    print(clean if not failures else f"{len(failures)} disagreement(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
