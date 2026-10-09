"""Retained Arial-compatible print faces and their deterministic design metrics.

The OFL-licensed Liberation Sans 2.1.5 outlines are retained under a unique family
name. Layout reads these files, never a host font. Native exporters register the
same files only in their process; standalone SVGs embed them with @font-face.

To reproduce the renamed assets from the official release's extracted directory:
    python -m devtools.atlas_print_font --prepare-fonts SOURCE_DIRECTORY
"""

from __future__ import annotations

import argparse
import base64
import ctypes
import ctypes.util
import os
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal
from functools import cache
from pathlib import Path
from textwrap import dedent

from fontTools.ttLib import TTFont

from sqpack.render.svg import PRINT_FONT_FAMILY, PRINT_ITALIC_FAMILY

FAMILY = PRINT_FONT_FAMILY
VERSION = "2.1.5"
# Quartz needs the exact italic face name; a family-level italic request can
# return the upright face even when both faces are registered.
ITALIC_FAMILY = PRINT_ITALIC_FAMILY
FONT_ROOT = Path(__file__).with_name("fonts") / "atlas-print"
FONT_PATHS = (
    FONT_ROOT / "SquaresAtlasPrint-Bold.ttf",
    FONT_ROOT / "SquaresAtlasPrint-BoldItalic.ttf",
)
LICENSE_PATH = FONT_ROOT / "LICENSE.txt"


@dataclass(frozen=True, slots=True)
class GlyphDesign:
    left: int
    top: int
    right: int
    bottom: int
    advance: int


@dataclass(frozen=True, slots=True)
class FontDesign:
    units_per_em: int
    glyphs: dict[int, GlyphDesign]


@cache
def design(*, italic: bool = False) -> FontDesign:
    """Read immutable design-unit bounds/advances from the retained face."""
    with TTFont(FONT_PATHS[int(italic)]) as font:
        cmap = font.getBestCmap()
        if cmap is None:
            raise ValueError("the retained atlas print face has no Unicode character map")
        glyphs = {}
        for codepoint, name in cmap.items():
            glyph = font["glyf"][name]
            glyphs[codepoint] = GlyphDesign(
                getattr(glyph, "xMin", 0),
                -getattr(glyph, "yMax", 0),
                getattr(glyph, "xMax", 0),
                -getattr(glyph, "yMin", 0),
                font["hmtx"][name][0],
            )
        return FontDesign(font["head"].unitsPerEm, glyphs)  # pyright: ignore[reportAttributeAccessIssue]


def _glyph(character: str, face: FontDesign) -> GlyphDesign:
    try:
        return face.glyphs[ord(character)]
    except KeyError as error:
        raise ValueError(f"atlas print font does not contain {character!r}") from error


def text_width(text: str, size: Decimal) -> Decimal:
    """Unkerned advance of text in the retained bold face."""
    face = design()
    return sum(_glyph(character, face).advance for character in text) * size / face.units_per_em


def ink_bounds(
    text: str, size: Decimal, *, italic: bool = False
) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    """Left/top/right/bottom ink bounds, in SVG's downward-positive coordinates."""
    face = design(italic=italic)
    advance = 0
    bounds = []
    for character in text:
        glyph = _glyph(character, face)
        if glyph.left != glyph.right or glyph.top != glyph.bottom:
            bounds.append(
                (advance + glyph.left, glyph.top, advance + glyph.right, glyph.bottom)
            )
        advance += glyph.advance
    if not bounds:
        return Decimal(0), Decimal(0), Decimal(0), Decimal(0)
    factor = size / face.units_per_em
    return (
        min(bound[0] for bound in bounds) * factor,
        min(bound[1] for bound in bounds) * factor,
        max(bound[2] for bound in bounds) * factor,
        max(bound[3] for bound in bounds) * factor,
    )


@cache
def embedded_css() -> str:
    """Self-contained font custody for SVG viewers that support embedded fonts."""
    rules = [f"/*\n{LICENSE_PATH.read_text(encoding='utf-8')}\n*/"]
    for path, style, family in zip(
        FONT_PATHS, ("normal", "italic"), (FAMILY, ITALIC_FAMILY), strict=True
    ):
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        rules.append(
            f'@font-face {{ font-family: "{family}"; font-style: {style}; '
            f'font-weight: 700; src: url("data:font/ttf;base64,{data}") format("truetype"); }}'
        )
    return "\n".join(rules)


def _register_coretext() -> None:
    # Quartz is Cairo's default toy-font backend on macOS. Fontconfig registration
    # alone has no effect on it. Scope 1 is process-only, never a font installation.
    core = ctypes.CDLL("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")
    text = ctypes.CDLL("/System/Library/Frameworks/CoreText.framework/CoreText")
    core.CFURLCreateFromFileSystemRepresentation.argtypes = [
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.c_long,
        ctypes.c_bool,
    ]
    core.CFURLCreateFromFileSystemRepresentation.restype = ctypes.c_void_p
    core.CFRelease.argtypes = [ctypes.c_void_p]
    core.CFRelease.restype = None
    text.CTFontManagerRegisterFontsForURL.argtypes = [
        ctypes.c_void_p,
        ctypes.c_uint32,
        ctypes.c_void_p,
    ]
    text.CTFontManagerRegisterFontsForURL.restype = ctypes.c_bool
    is_directory = False
    for path in FONT_PATHS:
        encoded = os.fsencode(path)
        url = core.CFURLCreateFromFileSystemRepresentation(
            None, encoded, len(encoded), is_directory
        )
        if not url:
            raise RuntimeError(f"cannot create atlas print font URL: {path}")
        try:
            if not text.CTFontManagerRegisterFontsForURL(url, 1, None):
                raise RuntimeError(f"cannot register process-local atlas print font: {path}")
        finally:
            core.CFRelease(url)


def _register_fontconfig() -> None:
    library = ctypes.util.find_library("fontconfig")
    if library is None:
        raise RuntimeError("native atlas print export requires Fontconfig")
    config = ctypes.CDLL(library)
    config.FcConfigGetCurrent.argtypes = []
    config.FcConfigGetCurrent.restype = ctypes.c_void_p
    current = config.FcConfigGetCurrent()
    if not current:
        raise RuntimeError("cannot initialize process-local atlas print Fontconfig")
    # Quartz requires the PostScript face name. Fontconfig matches family names,
    # so give that exact request the retained family before native fallback rules.
    alias = dedent(f"""
        <fontconfig>
          <alias binding="strong">
            <family>{ITALIC_FAMILY}</family>
            <prefer><family>{FAMILY}</family></prefer>
          </alias>
        </fontconfig>
        """).encode("utf-8")
    config.FcConfigParseAndLoadFromMemory.argtypes = [
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.c_int,
    ]
    config.FcConfigParseAndLoadFromMemory.restype = ctypes.c_int
    if not config.FcConfigParseAndLoadFromMemory(current, alias, 1):
        raise RuntimeError("cannot configure process-local atlas print italic family")
    config.FcConfigAppFontAddFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    config.FcConfigAppFontAddFile.restype = ctypes.c_int
    for path in FONT_PATHS:
        if not config.FcConfigAppFontAddFile(current, os.fsencode(path)):
            raise RuntimeError(f"cannot register process-local atlas print font: {path}")


def verify_cairo_face() -> None:
    """Refuse a substituted native face before an export or an ink measurement."""
    import cairocffi as cairo  # noqa: PLC0415

    context = cairo.Context(cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, None))
    options = cairo.FontOptions()
    options.set_hint_metrics(cairo.HINT_METRICS_OFF)
    context.set_font_options(options)
    for italic in (False, True):
        face = design(italic=italic)
        context.select_font_face(
            ITALIC_FAMILY if italic else FAMILY,
            cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL,
            cairo.FONT_WEIGHT_BOLD,
        )
        context.set_font_size(face.units_per_em)
        for character in "ns" if italic else "O=≈Rgjnsäö":
            glyph = _glyph(character, face)
            actual = context.text_extents(character)
            expected = (
                glyph.left,
                glyph.top,
                glyph.right - glyph.left,
                glyph.bottom - glyph.top,
                glyph.advance,
                0,
            )
            if any(
                abs(found - wanted) > 0.01
                for found, wanted in zip(actual, expected, strict=True)
            ):
                raise RuntimeError(
                    f"Cairo substituted the retained atlas print face "
                    f"({'italic' if italic else 'upright'}, {character!r}): "
                    f"{actual} != {expected}"
                )


@cache
def register_print_fonts() -> None:
    """Provision and verify the retained faces in this process, without host changes."""
    for path in FONT_PATHS:
        if not path.is_file():
            raise FileNotFoundError(f"retained atlas print font is missing: {path}")
    if sys.platform == "darwin":
        _register_coretext()
    else:
        _register_fontconfig()
    verify_cairo_face()


def prepare_fonts(source_directory: Path) -> None:
    """Reproduce only name/license metadata changes; retain all outlines and metrics."""
    FONT_ROOT.mkdir(parents=True, exist_ok=True)
    license_text = (source_directory / "LICENSE").read_text(encoding="utf-8")
    LICENSE_PATH.write_text(license_text, encoding="utf-8")
    for path, style in zip(FONT_PATHS, ("Bold", "BoldItalic"), strict=True):
        with TTFont(
            source_directory / f"LiberationSans-{style}.ttf", recalcTimestamp=False
        ) as font:
            names = {
                1: FAMILY,
                3: f"SquaresAtlasPrint-{style}-{VERSION}",
                4: f"{FAMILY} {style}",
                6: f"SquaresAtlasPrint-{style}",
                13: license_text,
                16: FAMILY,
            }
            for name in font["name"].names:
                if name.nameID in names:
                    name.string = names[name.nameID].encode(name.getEncoding())
            font.save(path, reorderTables=False)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare-fonts", type=Path)
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="check native resolution without provisioning",
    )
    args = parser.parse_args(argv)
    if args.prepare_fonts is not None:
        prepare_fonts(args.prepare_fonts)
    else:
        if args.verify_only:
            verify_cairo_face()
        else:
            register_print_fonts()
        print(f"Cairo resolved retained {FAMILY} {VERSION} bold and bold italic")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
