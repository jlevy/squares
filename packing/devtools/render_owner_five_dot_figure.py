"""Draw the exp143 owner patches and five dots, using the exp144 exact receipt.

The picture illustrates an existing conditional proof; rendering does not rerun it.
Run from packing with `python -m devtools.render_owner_five_dot_figure`.
`--check` compares the SVG with its sources; `--png` also exports a reading preview.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from xml.etree import ElementTree as ET

from strif import atomic_output_file

from sqpack.render.numbers import emission_precision, format_svg_number
from sqpack.render.svg import (
    append_metadata,
    append_title_desc,
    element,
    serialize_svg,
    sub,
    write_svg_atomic,
)

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
RESULTS = ROOT / "campaign/series/series-000-smoke-and-calibration/results/agenda-032"
PROPOSAL = RESULTS / "exp-143-four-owner-footprint-cover.json"
REPLAY = RESULTS / "exp-144-four-owner-endpoint-full-net-replay.json"
ARTIFACT = RESULTS / "four-owner-five-dot.svg"
Point = tuple[Fraction, Fraction]
Polygon = tuple[Point, ...]
INK = "#22333d"
MUTED = "#536670"
TEAL = "#087d7a"
PATCH = "#c6e8df"
BLUE = "#2853a2"
DOT = "#b63e24"
PLOT_X = 60
PLOT_BOTTOM = 710
PLOT_SIDE = 550


@dataclass(frozen=True)
class FigureData:
    outer_side: Fraction
    core_side: Fraction
    footprints: tuple[Polygon, ...]
    marks: tuple[Point, ...]
    dots: tuple[Point, ...]
    direction_count: int


def load_data(proposal: Path = PROPOSAL, replay: Path = REPLAY) -> FigureData:
    """Keep the displayed count tied to positive full-net evidence, not the LP score."""
    source = json.loads(proposal.read_text())
    exact = json.loads(replay.read_text())
    endpoint = source["arms"]["endpoint"]
    atoms = endpoint["proposal"]["rationalised_atoms"]
    directions = exact["directions"]
    beta = Fraction(atoms[0][2])
    if (
        len(atoms) != 5
        or beta <= 0
        or any(Fraction(atom[2]) != beta for atom in atoms)
        or exact["scope"]["direction_count"] != 361
        or exact["scope"]["directions"] != "full"
        or len(directions) != 361
        or [row["index"] for row in directions] != list(range(361))
        or any(Fraction(row["minimum_covered_mass"]) != beta for row in directions)
        or Fraction(exact["summary"]["minimum_covered_mass"]) != beta
        or Fraction(exact["summary"]["normalised_total_mass"]) != 5
        or source["settings"]["owner_count"] != 4
        or source["settings"]["residual_square_count"] != 7
    ):
        raise ValueError("The illustration requires the retained four-owner five-dot result")
    q = Fraction(source["settings"]["outer_side"])
    a, b = (Fraction(value) for value in source["class"]["mark"])
    return FigureData(
        outer_side=q,
        core_side=Fraction(source["settings"]["square_side"]),
        footprints=tuple(
            tuple((Fraction(x), Fraction(y)) for x, y in polygon)
            for polygon in endpoint["footprint_union"]
        ),
        marks=((a, b), (q - a, b), (a, q - b), (q - a, q - b)),
        dots=tuple((Fraction(x), Fraction(y)) for x, y, _ in atoms),
        direction_count=len(directions),
    )


def _text(
    root: ET.Element,
    words: str,
    x: int,
    y: int,
    *,
    size: int = 18,
    fill: str = INK,
    weight: int = 400,
    anchor: str = "start",
) -> None:
    sub(
        root,
        "text",
        {
            "x": str(x),
            "y": str(y),
            "font-size": str(size),
            "fill": fill,
            "font-weight": str(weight),
            "text-anchor": anchor,
        },
    ).text = words


def _polygon(root: ET.Element, points: Polygon, **attrs: str) -> ET.Element:
    return sub(
        root,
        "polygon",
        {
            "points": " ".join(
                f"{format_svg_number(x)},{format_svg_number(y)}" for x, y in points
            ),
            **attrs,
        },
    )


def _mark(root: ET.Element, point: Point) -> None:
    x, y = point
    _polygon(
        root,
        ((x, y - 5), (x + 5, y), (x, y + 5), (x - 5, y)),
        fill=BLUE,
        stroke="white",
        **{"stroke-width": "1.2"},
    )


def _box(root: ET.Element, x: int, y: int, width: int, height: int) -> None:
    sub(
        root,
        "rect",
        {
            "x": str(x),
            "y": str(y),
            "width": str(width),
            "height": str(height),
            "rx": "12",
            "fill": "#f4f7f7",
            "stroke": "#d9e2e3",
        },
    )


def _draw_container(root: ET.Element, data: FigureData) -> None:
    scale = Fraction(PLOT_SIDE) / data.outer_side

    def project(point: Point) -> Point:
        x, y = point
        return Fraction(PLOT_X) + x * scale, Fraction(PLOT_BOTTOM) - y * scale

    sub(
        root,
        "rect",
        {
            "x": str(PLOT_X),
            "y": str(PLOT_BOTTOM - PLOT_SIDE),
            "width": str(PLOT_SIDE),
            "height": str(PLOT_SIDE),
            "fill": "white",
            "stroke": INK,
            "stroke-width": "2",
        },
    )
    _text(root, f"Container side {float(data.outer_side):g}", 335, 139, anchor="middle")
    for label, polygon in zip("ABCD", data.footprints, strict=True):
        shape = _polygon(
            root,
            tuple(project(point) for point in polygon),
            fill=PATCH,
            stroke=TEAL,
            **{
                "stroke-width": "2",
                "data-footprint": label,
                "data-exact-vertices": json.dumps([[str(x), str(y)] for x, y in polygon]),
            },
        )
        sub(shape, "title").text = f"Patch {label}: inside its owner in every pose in this case"
    for mark, label, offset in zip(data.marks, "ABCD", (-19, 19, -19, 19), strict=True):
        point = project(mark)
        _mark(root, point)
        _text(
            root,
            label,
            round(point[0]) + offset,
            round(point[1]) + 6,
            fill=TEAL,
            weight=700,
            anchor="middle",
        )
    for index, dot in enumerate(data.dots, start=1):
        x, y = project(dot)
        circle = sub(
            root,
            "circle",
            {
                "cx": format_svg_number(x),
                "cy": format_svg_number(y),
                "r": "7",
                "fill": DOT,
                "data-dot": str(index),
                "data-exact-x": str(dot[0]),
                "data-exact-y": str(dot[1]),
            },
        )
        sub(circle, "title").text = f"Dot {index}: ({dot[0]}, {dot[1]}), weight 1"
        _text(root, str(index), round(x) + 13, round(y) - 10, fill=DOT, weight=650)
    for value in range(4):
        x, _ = project((Fraction(value), Fraction(0)))
        _, y = project((Fraction(0), Fraction(value)))
        _text(root, str(value), round(x), 733, size=15, fill=MUTED, anchor="middle")
        _text(root, str(value), 46, round(y) + 5, size=15, fill=MUTED, anchor="end")
    sub(
        root,
        "rect",
        {"x": "60", "y": "755", "width": "18", "height": "14", "fill": PATCH, "stroke": TEAL},
    )
    _text(root, "A\N{EN DASH}D: guaranteed occupied patches", 88, 768, size=17)
    sub(root, "circle", {"cx": "445", "cy": "762", "r": "6", "fill": DOT})
    _text(root, "1\N{EN DASH}5: proof dots", 460, 768, size=17)


def _draw_patch_construction(root: ET.Element, data: FigureData) -> None:
    _box(root, 650, 113, 420, 399)
    _text(root, "How a patch is forced", 674, 146, size=22, weight=650)
    _text(root, "The owner's core contains a square of", 674, 178)
    _text(root, "half its side, anchored at the mark.", 674, 202)
    h = data.core_side / 2
    mx, my = data.marks[0]
    patch = tuple((x - mx, y - my) for x, y in data.footprints[0])
    u, v = patch[1]
    quarter_zero = ((Fraction(0), Fraction(0)), (h, Fraction(0)), (h, h), (Fraction(0), h))
    quarter_end = ((Fraction(0), Fraction(0)), (u, v), (u - v, v + u), (-v, u))

    def zoom(points: Polygon) -> Polygon:
        return tuple((Fraction(850) + 240 * x, Fraction(404) - 240 * y) for x, y in points)

    for points, dash in ((quarter_zero, ""), (quarter_end, "6 4")):
        _polygon(
            root,
            zoom(points),
            fill="none",
            stroke="#84939c",
            **{"stroke-width": "2", "stroke-dasharray": dash},
        )
    _polygon(root, zoom(patch), fill=PATCH, stroke=TEAL, **{"stroke-width": "2.5"})
    _mark(root, (Fraction(850), Fraction(404)))
    _text(root, "mark", 850, 431, size=16, fill=BLUE, anchor="middle")
    _text(root, "0°", 985, 290, size=16, fill=MUTED)
    _text(root, "≈45°", 773, 252, size=16, fill=MUTED, anchor="end")
    _text(root, "Two endpoint orientations are outlined.", 674, 465, size=17)
    _text(root, "The overlap survives between these angles.", 674, 490, size=17)


@emission_precision()
def render_figure(data: FigureData | None = None) -> str:
    data = data or load_data()
    root = element(
        "svg",
        {
            "width": "1100",
            "height": "922",
            "viewBox": "0 0 1100 922",
            "role": "img",
            "aria-labelledby": "figure-title figure-description",
            "font-family": "Arial, Helvetica, sans-serif",
        },
    )
    append_title_desc(
        root,
        "Five dots exclude one four-owner case",
        (
            "The square container of side 3.84 contains four teal patches guaranteed to lie "
            "inside four distinct owner squares. Blue diamonds are their ownership marks. "
            "Five red dots meet every remaining selected inner core. Distinct cores cannot "
            "share a dot, so at most five further squares fit, while eleven total need seven. "
            "An inset shows the half-side square intersection that forces each patch. "
            "The result excludes this specified owner case, not every eleven-square packing."
        ),
    )
    append_metadata(
        root,
        {
            "proposal": PROPOSAL.relative_to(REPO).as_posix(),
            "exact-replay": REPLAY.relative_to(REPO).as_posix(),
            "analytic-transfer": (RESULTS / "proofs/five-dot-transfer-review.md")
            .relative_to(REPO)
            .as_posix(),
            "branch": "four reflected bottom-left:m1:j0 owner conditions",
            "normalised-dot-weight": "1",
            "scope": "existing conditional result; drawing does not rerun the proof",
        },
    )
    sub(root, "rect", {"width": "1100", "height": "922", "fill": "white"})
    _text(root, "Five dots rule out one four-owner case", 36, 45, size=29, weight=700)
    _text(
        root,
        "The four owner squares may vary in position and angle within this case.",
        36,
        78,
        size=19,
        fill=MUTED,
    )
    _draw_container(root, data)
    _draw_patch_construction(root, data)
    _box(root, 650, 530, 420, 243)
    _text(root, "Why five dots suffice", 674, 564, size=22, weight=650)
    _text(root, "An inner core is a slightly smaller", 674, 598)
    _text(root, "square strictly inside a unit square.", 674, 622)
    _text(root, "Each selected remaining core contains", 674, 663)
    _text(root, "at least one of the five red dots.", 674, 687, fill=DOT, weight=650)
    _text(root, "Separated cores cannot share a dot.", 674, 733)
    _box(root, 30, 799, 1040, 91)
    _text(root, "11 total \N{MINUS SIGN} 4 owners = 7 remaining", 54, 835, size=24, weight=650)
    _text(root, "Each remaining core needs its own dot.", 54, 867, size=18)
    _text(root, "7 required > 5 dots", 830, 838, size=29, fill=DOT, weight=700, anchor="middle")
    _text(root, "This case is impossible.", 830, 870, size=18, anchor="middle")
    _text(
        root,
        f"Exact coverage: {data.direction_count} core directions; "
        "all physical angles follow by the proved inner-core transfer.",
        550,
        914,
        size=15,
        fill=MUTED,
        anchor="middle",
    )
    return serialize_svg(root)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true", help="check SVG drift without writing")
    modes.add_argument("--png", action="store_true", help="also render a PNG reading preview")
    args = parser.parse_args(argv)
    svg = render_figure()
    if args.check:
        if not ARTIFACT.exists() or ARTIFACT.read_text() != svg:
            print(f"STALE {ARTIFACT.relative_to(REPO)}")
            return 1
        print("Owner five-dot figure matches the retained sources")
        return 0
    write_svg_atomic(ARTIFACT, svg)
    if args.png:
        import cairosvg  # noqa: PLC0415

        with atomic_output_file(ARTIFACT.with_suffix(".png")) as temporary:
            cairosvg.svg2png(bytestring=svg.encode(), write_to=str(temporary), scale=2)
    print(ARTIFACT.relative_to(REPO))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
