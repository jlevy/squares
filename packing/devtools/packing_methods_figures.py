"""Passive packing illustrations from retained, attributed source geometry.

The page builder reads these small inputs and projects their coordinates. It does not
run a search, a producer, or a feasibility checker. A picture illustrates a method;
its source's mathematical assurance and its historical lineage belong in the caption.
"""

from __future__ import annotations

import gzip
import json
import math
import re
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from xml.etree import ElementTree as ET

from devtools import paper_figures
from sqpack import yamlio
from sqpack.render import model
from sqpack.render import svg as svg_api

REPO = Path(__file__).resolve().parents[2]
PACKING = REPO / "packing"
TRUMP_DRAWING = PACKING / "atlas/rendering/trump11-overview.svg"
ANNEALING_DRAWING = PACKING / "atlas/known-best/rendering/n-029.svg"
ALGEBRAIC_DRAWING = PACKING / "atlas/known-best/rendering/n-051.svg"
CASSON_POSE = (
    PACKING
    / "resources/web/casson-square-packing-2026-09-23/griffcass-square-packing"
    / "results/packings/n106.txt"
)
SURGERY_PACKET = PACKING / "resources/web/squish-422-second-update-2026-10-07"
SURGERY_FACTS = SURGERY_PACKET / "facts/n-108.json.gz"
SURGERY_SOURCES = SURGERY_PACKET / "acquisition/sources.json"

#: Absolute paths: the native publication closure must include every retained input
#: and the project-owned helpers used to read and draw it.
FIGURE_INPUTS = (
    Path(__file__),
    TRUMP_DRAWING,
    ANNEALING_DRAWING,
    CASSON_POSE,
    SURGERY_FACTS,
    SURGERY_SOURCES,
    ALGEBRAIC_DRAWING,
    Path(paper_figures.__file__),
    Path(svg_api.__file__),
    Path(model.__file__),
    Path(yamlio.__file__),
    PACKING / "src/sqpack/render/__init__.py",
)

FIGURE_KEYS = (
    "HAND_CONSTRUCTION_SVG",
    "ANNEALING_SVG",
    "ANNEALING_SLP_SVG",
    "SURGERY_SVG",
    "ALGEBRAIC_WITNESS_SVG",
)

WIDTH = 390
MARGIN = 12
EXTENT = WIDTH - 2 * MARGIN
POSE_ROW = re.compile(r"Square ([0-9]+): x=([-+0-9.eE]+), y=([-+0-9.eE]+), deg=([-+0-9.eE]+)")
HEX_FILL = re.compile(r"#[0-9a-fA-F]{6}")
CASSON_URL = (
    "https://github.com/griffcass/square-packing/blob/"
    "82661bc8777beeecf458312e8aca9179a969da4f/results/packings/n106.txt"
)

type Points = tuple[tuple[float, float], ...]


@dataclass(frozen=True)
class Drawing:
    identifier: str
    n: int
    title: str
    credit: str
    source_path: Path
    source_url: str
    source_id: str
    squares: tuple[Points, ...]
    fills: tuple[str, ...]
    lineage: str = ""


def _retained_drawing(
    path: Path, *, identifier: str, n: int, title: str, credit: str
) -> Drawing:
    """Reuse only the container and square facts of a native standalone SVG."""
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    frame = root.find(f'.//{svg_api.svg_tag("rect")}[@data-feature="container-outline"]')
    if frame is None:
        raise ValueError(f"{path.name}: retained container is missing")
    left, top, side = (float(frame.attrib[key]) for key in ("x", "y", "width"))
    if side <= 0 or not math.isclose(side, float(frame.attrib["height"])):
        raise ValueError(f"{path.name}: retained container is not square")
    polygons = root.findall(f'.//{svg_api.svg_tag("polygon")}[@data-feature="square-fill"]')
    squares = tuple(
        tuple(
            ((float(x) - left) / side, (float(y) - top) / side)
            for x, y in (pair.split(",") for pair in polygon.attrib["points"].split())
        )
        for polygon in polygons
    )
    metadata = {
        node.attrib["name"]: node.text or "" for node in root.iter(svg_api.sqpack_tag("value"))
    }
    return Drawing(
        identifier,
        n,
        title,
        credit,
        path,
        metadata.get("source-url", ""),
        metadata["source-id"],
        squares,
        tuple(polygon.attrib["fill"] for polygon in polygons),
    )


def _project_corners(
    cx: Fraction, cy: Fraction, cosine: Fraction, sine: Fraction, side: Fraction
) -> Points:
    return tuple(
        (float(x / side), 1 - float(y / side))
        for x, y in paper_figures.square_corners((cx, cy), Fraction(1), cosine, sine)
    )


def _pose_fill(cosine: float, sine: float) -> str:
    # Orientation is also visible in each outline; colour does not carry a claim.
    return "#dcebef" if min(abs(cosine), abs(sine)) < 0.00001 else "#f2d7a6"


def _casson_drawing() -> Drawing:
    lines = CASSON_POSE.read_text(encoding="utf-8").splitlines()
    if not lines or not lines[0].startswith("s: "):
        raise ValueError("Casson source is missing its side header")
    side = Fraction(lines[0].removeprefix("s: "))
    if side <= 0:
        raise ValueError("Casson source side must be positive")
    squares: list[Points] = []
    fills: list[str] = []
    for index, line in enumerate(lines[1:], 1):
        match = POSE_ROW.fullmatch(line)
        if match is None or int(match[1]) != index:
            raise ValueError("Casson source has an incomplete or unordered square roster")
        x, y, degrees = (Fraction(match[key]) for key in (2, 3, 4))
        angle = math.radians(float(degrees))
        cosine, sine = math.cos(angle), math.sin(angle)
        squares.append(
            _project_corners(x + side / 2, y + side / 2, Fraction(cosine), Fraction(sine), side)
        )
        fills.append(_pose_fill(cosine, sine))
    return Drawing(
        "annealing-slp",
        106,
        "Casson's 106-square annealing and SLP example",
        "Griffin Casson; retained 2026-09-23; CC BY 4.0 coordinates, redrawn",
        CASSON_POSE,
        CASSON_URL,
        "casson-n106-2026-09-23",
        tuple(squares),
        tuple(fills),
    )


def _surgery_drawing() -> Drawing:
    facts = json.loads(gzip.decompress(SURGERY_FACTS.read_bytes()))
    sources = json.loads(SURGERY_SOURCES.read_text(encoding="utf-8"))
    source = next(record for record in sources["cases"] if record["n"] == 108)
    if facts["n"] != 108 or facts["side"] != source["exact_side"]:
        raise ValueError("historical SQUISH facts differ from their source identity")
    side = Fraction(facts["side"])
    if side <= 0:
        raise ValueError("SQUISH source side must be positive")
    squares: list[Points] = []
    fills: list[str] = []
    for square in facts["squares"]:
        x, y, t = (Fraction(square[key]) for key in ("x", "y", "t"))
        denominator = 1 + t * t
        cosine, sine = (1 - t * t) / denominator, 2 * t / denominator
        squares.append(_project_corners(x, y, cosine, sine, side))
        fills.append(_pose_fill(float(cosine), float(sine)))
    return Drawing(
        "surgery",
        108,
        "SQUISH's historical 108-square surgery example",
        "Nate Chaoweeraprasit (itsnaka), SQUISH, second update 2026-10-07",
        SURGERY_FACTS,
        source["source_url"],
        "squish-second-update-n108-2026-10-07",
        tuple(squares),
        tuple(fills),
        source["reported_seed"],
    )


def _render(drawing: Drawing) -> str:
    if len(drawing.squares) != drawing.n or len(drawing.fills) != drawing.n:
        raise ValueError(f"{drawing.identifier}: expected {drawing.n} retained squares")
    # SVG paint expressions can reference external URLs through CSS escapes.
    if any(HEX_FILL.fullmatch(fill) is None for fill in drawing.fills):
        raise ValueError(f"{drawing.identifier}: fill must be a six-digit hexadecimal colour")
    if any(
        len(square) != 4 or any(not math.isfinite(value) for point in square for value in point)
        for square in drawing.squares
    ):
        raise ValueError(f"{drawing.identifier}: invalid illustration coordinates")
    prefix = f"methods-{drawing.identifier}"
    root = svg_api.element(
        "svg",
        {
            "class": f"methods-diagram {prefix}",
            "width": str(WIDTH),
            "height": str(WIDTH),
            "viewBox": f"0 0 {WIDTH} {WIDTH}",
            "role": "img",
            "aria-labelledby": f"{prefix}-title {prefix}-description",
        },
    )
    svg_api.sub(root, "title", {"id": f"{prefix}-title"}).text = drawing.title
    svg_api.sub(root, "desc", {"id": f"{prefix}-description"}).text = (
        f"An illustration of {drawing.n} unit squares in a square container, projected "
        f"from retained source geometry. Credit: {drawing.credit}. "
        "The drawing does not run or establish a feasibility or optimality proof."
    )
    svg_api.append_metadata(
        root,
        {
            "credit": drawing.credit,
            "source-id": drawing.source_id,
            "source-url": drawing.source_url,
            "source-input": drawing.source_path.relative_to(REPO).as_posix(),
            "source-lineage": drawing.lineage,
            "purpose": "method illustration from retained geometry; no verification replay",
        },
        coordinates="retained geometry projected to normalized svg-y-down",
    )
    svg_api.sub(root, "rect", {"width": str(WIDTH), "height": str(WIDTH), "fill": "#ffffff"})
    group = svg_api.sub(root, "g", {"data-layer": "squares"})
    for index, (points, fill) in enumerate(zip(drawing.squares, drawing.fills, strict=True), 1):
        svg_api.sub(
            group,
            "polygon",
            {
                "data-feature": "square-fill",
                "data-square": f"square-{index:03}",
                "points": " ".join(
                    f"{MARGIN + EXTENT * x:.4f},{MARGIN + EXTENT * y:.4f}" for x, y in points
                ),
                "fill": fill,
                "stroke": "#172b3a",
                "stroke-width": "0.75",
                "stroke-linejoin": "round",
            },
        )
    svg_api.sub(
        root,
        "rect",
        {
            "data-feature": "container-outline",
            "x": str(MARGIN),
            "y": str(MARGIN),
            "width": str(EXTENT),
            "height": str(EXTENT),
            "fill": "none",
            "stroke": "#52667a",
            "stroke-width": "1.5",
        },
    )
    # The publication embeds SVG in HTML; an XML declaration belongs only to a file.
    return svg_api.serialize_svg(root).split("\n", 1)[1].strip()


def render_figures() -> dict[str, str]:
    """Five keyed SVG fragments for the native paper's numbered figure slots."""
    drawings = (
        _retained_drawing(
            TRUMP_DRAWING,
            identifier="hand-construction",
            n=11,
            title="Trump's eleven-square hand construction",
            credit="Walter Trump (1979)",
        ),
        _retained_drawing(
            ANNEALING_DRAWING,
            identifier="annealing",
            n=29,
            title="The 29-square Schadt and Ellsworth example",
            credit=(
                "Thomas Schadt (2025), improved by David Ellsworth; retained catalogue geometry"
            ),
        ),
        _casson_drawing(),
        _surgery_drawing(),
        _retained_drawing(
            ALGEBRAIC_DRAWING,
            identifier="algebraic-witness",
            n=51,
            title="Xu's 51-square algebraic witness example",
            credit="ry-xu, square_packing",
        ),
    )
    return {key: _render(drawing) for key, drawing in zip(FIGURE_KEYS, drawings, strict=True)}
