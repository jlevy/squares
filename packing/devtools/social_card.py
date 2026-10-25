#!/usr/bin/env python3
"""Draw the picture a shared link to the site shows: the homepage's hero, as a card.

Every page of the site names one image in its link preview
(`render_overview.head_tags`): the homepage's hero, the best packing known of
`overview_sections.HERO_CASE` squares, at 1200 by 630, the size every consumer shows as
a large card without cropping it. This draws that image when the site is built. It is
the hero's own drawing, `render_frontier_page.default_svg` at the hero's 1000 units, so
its squares, its pose (the case's flip regularization, regularization policy section 13),
its colours and its line weights are the page's, in the page's ink on the
page's background as the light theme has them (`rung_scale.page_colours`, read from
kpress's tokens). Under it is the project's name as the bar sets the site's: the bar's
sans in capitals, at the bar's weight and letter spacing.

The name is drawn as outlines, from the face kpress ships, and not as text. A rasteriser
sets text in whatever font the machine has under that name, which on a runner is none of
the site's; outlines are the same on every machine, and the card needs no font installed.
Glyphs are placed by their advances with the bar's letter spacing and no kerning, which
capitals this widely spaced do not miss.

The card is built and not checked in, as the site's pages are: a raster is drawn by the
machine's Cairo, so its bytes are that machine's, and a committed copy would be a second
thing to keep in step with the drawing. `preview_site` writes it into the site it
builds, and the Pages workflow's `overview` job writes it beside the pages, into the
published directory and into the twin it compares that with, so a card that does not
reproduce itself fails there. A write is refused over `BYTE_CEILING`.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.social_card
    uv run --frozen --all-extras --group dev python -m devtools.social_card --output-dir DIR
    uv run --frozen --all-extras --group dev python -m devtools.social_card --check
    uv run --frozen --all-extras --group dev python -m devtools.social_card --plain --svg

`--check` compares the card in the directory with a fresh drawing and writes nothing.
`--plain` leaves the name out, and `--svg` writes the drawing itself beside the PNG, for
looking at; neither is what the site serves. On macOS the rasteriser needs Homebrew's
Cairo: `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib` (development.md, Supported
Environment).
"""

from __future__ import annotations

import argparse
import struct
import sys
from collections.abc import Sequence
from functools import cache
from pathlib import Path

from devtools import rung_scale
from devtools.overview_sections import HERO_CASE
from devtools.render_frontier_page import default_svg
from devtools.render_n11_lower_bounds_explainer import kpress_static
from devtools.render_overview import (
    OUTPUT,
    PROJECT_NAME,
    SOCIAL_CARD,
    SOCIAL_CARD_HEIGHT,
    SOCIAL_CARD_WIDTH,
)

#: The hero's own resolution (`overview_sections.hero`): whole units of a 1000-unit frame.
HERO_UNITS = 1000
#: The packing's side on the card, in its pixels, with and without the name under it.
#: Either leaves the picture inside the 630-pixel square at the card's centre, which is
#: what a consumer that shows a square thumbnail keeps.
PACKING_SIDE = 440
PLAIN_PACKING_SIDE = 510
#: The name's size, and the space between the packing and the line it stands on.
NAME_SIZE = 34
NAME_GAP = 44
#: How the bar sets the site's name (`site-nav.css`, `.site-nav .site-name`): its weight
#: and its letter spacing in ems, in capitals. A test holds these to that rule.
NAME_WEIGHT = 680
NAME_TRACKING = 0.06
#: The face the bar is set in, as kpress ships it: Source Sans 3, variable in weight.
SANS_FACE = "source-sans-3-latin-wght-normal.woff2"
#: The most a card may weigh. Consumers refuse a preview image well before a megabyte,
#: and the drawing is flat colour, so a card anywhere near this has gone wrong.
BYTE_CEILING = 300_000

_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def page_colours() -> tuple[str, str]:
    """The light theme's ink and paper, as hex: what the hero is drawn in and on."""
    light = rung_scale.page_colours()["light"]
    return rung_scale.hex_colour(light["text"]), rung_scale.hex_colour(light["bg"])


@cache
def name_outline(text: str, size: float) -> tuple[str, float, float]:
    """`text` as one SVG path in the bar's sans at `size` pixels, its baseline at y = 0
    and its left edge at x = 0, with the path's width and the height of its capitals."""
    from fontTools.pens.svgPathPen import SVGPathPen  # noqa: PLC0415
    from fontTools.pens.transformPen import TransformPen  # noqa: PLC0415
    from fontTools.ttLib import TTFont  # noqa: PLC0415
    from fontTools.varLib import instancer  # noqa: PLC0415

    face = kpress_static() / "fonts" / SANS_FACE
    if not face.is_file():
        raise SystemExit(f"kpress no longer ships {SANS_FACE}, the bar's face")
    font = instancer.instantiateVariableFont(TTFont(face), {"wght": NAME_WEIGHT})
    scale = size / font["head"].unitsPerEm  # pyright: ignore[reportAttributeAccessIssue]
    characters = font.getBestCmap()
    if characters is None:
        raise SystemExit(f"{SANS_FACE} has no Unicode character map")
    glyphs = font.getGlyphSet()
    advances = font["hmtx"]
    missing = sorted({character for character in text if ord(character) not in characters})
    if missing:
        raise SystemExit(f"{SANS_FACE} has no glyph for {missing}")

    def number(value: float) -> str:
        return f"{value:.2f}".rstrip("0").rstrip(".")

    spacing = NAME_TRACKING * size
    position = 0.0
    commands: list[str] = []
    for character in text:
        glyph = characters[ord(character)]
        pen = SVGPathPen(glyphs, ntos=number)
        # A font's y axis points up and an SVG's down, so the outline is flipped.
        glyphs[glyph].draw(TransformPen(pen, (scale, 0, 0, -scale, position, 0)))
        commands.append(pen.getCommands())
        position += advances[glyph][0] * scale + spacing  # pyright: ignore[reportIndexIssue]
    cap_height = font["OS/2"].sCapHeight * scale  # pyright: ignore[reportAttributeAccessIssue]
    return "".join(commands), position - spacing, cap_height


def card_svg(*, named: bool = True) -> str:
    """The card as an SVG: the hero's drawing centred on the page's background, with the
    project's name under it when `named`. The packing and the name are centred together,
    so the margins above and below are equal."""
    ink, paper = page_colours()
    width, height = SOCIAL_CARD_WIDTH, SOCIAL_CARD_HEIGHT
    side = PACKING_SIDE if named else PLAIN_PACKING_SIDE
    name = ""
    top = (height - side) / 2
    if named:
        outline, name_width, cap_height = name_outline(PROJECT_NAME.upper(), NAME_SIZE)
        block = side + NAME_GAP + cap_height
        top = (height - block) / 2
        name = (
            f'<path transform="translate({(width - name_width) / 2:.2f} {top + block:.2f})" '
            f'fill="{ink}" d="{outline}"/>'
        )
    packing = default_svg(HERO_CASE, units=HERO_UNITS, ink=ink).replace(
        "<svg ",
        f'<svg x="{(width - side) / 2:g}" y="{top:.2f}" width="{side}" height="{side}" ',
        1,
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
        f'<rect width="{width}" height="{height}" fill="{paper}"/>{packing}{name}</svg>'
    )


def card_png(*, named: bool = True) -> bytes:
    """The card's bytes, drawn by the rasteriser that draws the atlas's rasters."""
    # The drawing itself needs no native library; only this does.
    import cairosvg  # noqa: PLC0415

    content = cairosvg.svg2png(
        bytestring=card_svg(named=named).encode("utf-8"),
        output_width=SOCIAL_CARD_WIDTH,
        output_height=SOCIAL_CARD_HEIGHT,
    )
    if not isinstance(content, bytes):  # pragma: no cover - cairosvg returns bytes here
        raise TypeError("cairosvg returned no PNG bytes")
    problems = card_problems(content)
    if problems:
        raise SystemExit(f"the card as drawn is refused: {'; '.join(problems)}")
    return content


def png_dimensions(data: bytes) -> tuple[int, int] | None:
    """The pixel size a PNG's header declares; `None` when the bytes are not a PNG."""
    if data[:8] != _PNG_SIGNATURE or data[12:16] != b"IHDR" or len(data) < 24:
        return None
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def card_problems(data: bytes) -> list[str]:
    """What is wrong with these bytes as the site's card: not a PNG, not the size every
    page's head declares, or over `BYTE_CEILING`. Reads the header and the length, so it
    needs no rasteriser; `check_published_site` asks it of the card the site serves."""
    size = png_dimensions(data)
    if size is None:
        return ["it is not a PNG"]
    problems = []
    declared = (SOCIAL_CARD_WIDTH, SOCIAL_CARD_HEIGHT)
    if size != declared:
        problems.append(
            f"it is {size[0]}x{size[1]}, and every page declares {declared[0]}x{declared[1]}"
        )
    if len(data) > BYTE_CEILING:
        problems.append(f"it is {len(data)} bytes, over the {BYTE_CEILING}-byte ceiling")
    return problems


def write(directory: Path, *, named: bool = True) -> Path:
    """Write the card into `directory` under the name every page links, and return its
    path."""
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / SOCIAL_CARD
    target.write_bytes(card_png(named=named))
    return target


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT,
        help=f"the site directory the card is written into, as {SOCIAL_CARD}",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero if the card on disk is missing or differs from a fresh drawing",
    )
    parser.add_argument("--plain", action="store_true", help="leave the name out")
    parser.add_argument("--svg", action="store_true", help="write the SVG beside the PNG")
    args = parser.parse_args(argv)
    directory = args.output_dir.resolve()
    target = directory / SOCIAL_CARD
    named = not args.plain
    if args.check:
        fresh = card_png(named=named)
        if not target.is_file() or target.read_bytes() != fresh:
            print(f"stale or missing: {target}", file=sys.stderr)
            return 1
        print(f"{target} matches a fresh drawing ({len(fresh)} bytes)")
        return 0
    written = write(directory, named=named)
    if args.svg:
        written.with_suffix(".svg").write_text(card_svg(named=named), encoding="utf-8")
    size = png_dimensions(written.read_bytes())
    assert size is not None
    print(f"wrote {written} ({size[0]}x{size[1]}, {written.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
