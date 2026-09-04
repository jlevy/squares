#!/usr/bin/env python3
"""Render the weighted-atom and shrink-and-snap visual for result T-018.

The figure is derived from the retained ``n = 11`` certificate.  Its left panel
draws every atom and recomputes the direction-zero C4 witness; its right panel
shows the geometric containment step whose exact bound lets an arbitrary unit
square snap to the certificate's finite angle net.

Usage, from ``packing/``:
    uv run --frozen --all-extras --group dev python \
        -m devtools.render_t018_proof_visual
    uv run --frozen --all-extras --group dev python \
        -m devtools.render_t018_proof_visual --check
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import cast
from xml.etree import ElementTree as ET

from cases.n11_fractional_certificate.replay import CERTIFICATE_PATH, load
from sqpack.fractional.certificate import Certificate, sweep_direction_minimum
from sqpack.fractional.model import Atom, Direction
from sqpack.render.color import square_fill_palette
from sqpack.render.numbers import emission_precision, format_svg_number
from sqpack.render.style import LABEL_MUTED_COLOR, PACKING_BOUNDARY_COLOR, PAPER_THEME
from sqpack.render.svg import (
    append_metadata,
    append_title_desc,
    element,
    safe_id,
    serialize_svg,
    sub,
    write_svg_atomic,
)

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "cases/n11_fractional_certificate/t-018-proof-visual.svg"

EXPECTED_CERTIFICATE_ID = "C-n011-fractional-381-100"
EXPECTED_CLAIM = "s(11) >= 381/100"
EXPECTED_ATOM_COUNT = 1121
EXPECTED_DIRECTION_COUNT = 181
EXPECTED_WITNESS_DIRECTION = 0
EXPECTED_WITNESS_CENTRE = (Fraction(27, 50), Fraction(27, 50))

FIGURE_WIDTH = 1100
FIGURE_HEIGHT = 720
HEADER_X = 36
TITLE_Y = 43
SUBTITLE_Y = 72
PANEL_TOP = 95
PANEL_HEIGHT = 555
LEFT_PANEL_X = 30
LEFT_PANEL_WIDTH = 625
RIGHT_PANEL_X = 675
RIGHT_PANEL_WIDTH = 395
PANEL_RADIUS = 14
PANEL_INSET = 24
PANEL_TITLE_Y = 128
PANEL_SUBTITLE_Y = 151
PLOT_X = 70
PLOT_Y = 170
PLOT_SIDE = 430
PLOT_TICK_LENGTH = 6
PLOT_TICK_LABEL_OFFSET = 19
LEGEND_X = 525
LEGEND_CIRCLE_X = 539
LEGEND_TEXT_X = 558
SCHEMATIC_CENTRE_X = Fraction(1745, 2)
SCHEMATIC_CENTRE_Y = 325
SCHEMATIC_SIDE = 250
SCHEMATIC_INNER_SIDE = Fraction(4, 5)
SCHEMATIC_COSINE = Fraction(40, 41)
SCHEMATIC_SINE = Fraction(9, 41)
FOOTER_Y = 688

TITLE_SIZE = 27
SUBTITLE_SIZE = 14
PANEL_TITLE_SIZE = 17
BODY_SIZE = 14
SMALL_SIZE = 13
FOOTER_SIZE = 16
TITLE_WEIGHT = 750
LABEL_WEIGHT = 650
PANEL_STROKE_WIDTH = Decimal("1.5")
SHAPE_STROKE_WIDTH = Decimal("2")
GUIDE_STROKE_WIDTH = Decimal("1.25")
ATOM_SITE_RADIUS = Decimal("0.7")
MAX_ATOM_WEIGHT_RADIUS = Decimal("8")
FONT_FAMILY = "ui-sans-serif, system-ui, -apple-system, sans-serif"

_FAMILIES = square_fill_palette(hue_count=20, shades_per_hue=5)
ATOM_COLOR = _FAMILIES[0][2]
WITNESS_COLOR = _FAMILIES[4][2]
GUIDE_COLOR = PAPER_THEME.muted


@dataclass(frozen=True, slots=True)
class C4Witness:
    """One exact square attaining the retained direction-zero C4 minimum."""

    direction: Direction
    centre: tuple[Fraction, Fraction]
    atoms: tuple[Atom, ...]
    mass: Fraction


@dataclass(frozen=True, slots=True)
class ProofVisualData:
    """Certificate facts consumed by the two explanatory panels."""

    certificate_id: str
    claim: str
    certificate: Certificate
    declared_minimum: Fraction
    witness: C4Witness
    containment_product: Fraction
    clearance_bound: Fraction


def _fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def _decimal(value: Fraction | int) -> Decimal:
    fraction = value if isinstance(value, Fraction) else Fraction(value)
    return Decimal(fraction.numerator) / Decimal(fraction.denominator)


def _covered_atoms(
    atoms: tuple[Atom, ...],
    direction: Direction,
    square_side: Fraction,
    centre: tuple[Fraction, Fraction],
) -> tuple[Atom, ...]:
    half = square_side / 2
    centre_x, centre_y = centre
    covered = []
    for atom in atoms:
        dx, dy = atom.x - centre_x, atom.y - centre_y
        along = direction.ux * dx + direction.uy * dy
        across = direction.vx * dx + direction.vy * dy
        if -half <= along <= half and -half <= across <= half:
            covered.append(atom)
    return tuple(covered)


def load_visual_data() -> ProofVisualData:
    """Load and independently re-score the exact witness shown in the figure."""
    record = cast(dict[str, object], json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8")))
    certificate_id = record.get("id")
    claim = record.get("claim")
    declared_minimum = record.get("least_cell_mass")
    if (
        not isinstance(certificate_id, str)
        or certificate_id != EXPECTED_CERTIFICATE_ID
        or not isinstance(claim, str)
        or claim != EXPECTED_CLAIM
        or not isinstance(declared_minimum, str)
    ):
        raise ValueError("the T-018 visual received the wrong certificate declaration")

    certificate = load(CERTIFICATE_PATH)
    if len(certificate.atoms) != EXPECTED_ATOM_COUNT:
        raise ValueError(f"expected {EXPECTED_ATOM_COUNT} atoms, got {len(certificate.atoms)}")
    directions = certificate.directions
    if len(directions) != EXPECTED_DIRECTION_COUNT:
        raise ValueError(
            f"expected {EXPECTED_DIRECTION_COUNT} directions, got {len(directions)}"
        )
    direction = directions[EXPECTED_WITNESS_DIRECTION]
    mass, centre = sweep_direction_minimum(certificate, direction)
    if centre != EXPECTED_WITNESS_CENTRE:
        raise ValueError(f"direction-zero C4 witness moved from {EXPECTED_WITNESS_CENTRE}")
    witness_atoms = _covered_atoms(
        certificate.atoms, direction, certificate.square_side, centre
    )
    direct_mass = sum((atom.weight for atom in witness_atoms), start=Fraction())
    minimum = Fraction(declared_minimum)
    if mass != minimum or direct_mass != minimum:
        raise ValueError(
            f"direction-zero witness mass {direct_mass} disagrees with declared {minimum}"
        )

    containment_product = certificate.square_side * (1 + certificate.largest_half_gap_tangent)
    if containment_product >= 1:
        raise ValueError("the retained angle net no longer gives strict containment")
    return ProofVisualData(
        certificate_id=certificate_id,
        claim=claim,
        certificate=certificate,
        declared_minimum=minimum,
        witness=C4Witness(direction, centre, witness_atoms, direct_mass),
        containment_product=containment_product,
        clearance_bound=(1 - containment_product) / 2,
    )


def _text(
    parent: ET.Element,
    value: str,
    x: Fraction | Decimal | int,
    y: Fraction | Decimal | int,
    *,
    size: int = BODY_SIZE,
    fill: str = PAPER_THEME.ink,
    weight: int | None = None,
    anchor: str | None = None,
    **attributes: str,
) -> ET.Element:
    attrs = {
        "x": format_svg_number(x),
        "y": format_svg_number(y),
        "font-family": FONT_FAMILY,
        "font-size": str(size),
        "fill": fill,
        **attributes,
    }
    if weight is not None:
        attrs["font-weight"] = str(weight)
    if anchor is not None:
        attrs["text-anchor"] = anchor
    node = sub(parent, "text", attrs)
    node.text = value
    return node


def _line(
    parent: ET.Element,
    x1: Fraction | Decimal | int,
    y1: Fraction | Decimal | int,
    x2: Fraction | Decimal | int,
    y2: Fraction | Decimal | int,
    *,
    stroke: str = GUIDE_COLOR,
    width: Decimal = GUIDE_STROKE_WIDTH,
    **attributes: str,
) -> ET.Element:
    return sub(
        parent,
        "line",
        {
            "x1": format_svg_number(x1),
            "y1": format_svg_number(y1),
            "x2": format_svg_number(x2),
            "y2": format_svg_number(y2),
            "stroke": stroke,
            "stroke-width": format_svg_number(width),
            "vector-effect": "non-scaling-stroke",
            **attributes,
        },
    )


def _panel(root: ET.Element, x: int, width: int, label: str) -> ET.Element:
    panel = sub(root, "g", {"data-panel": label})
    sub(
        panel,
        "rect",
        {
            "x": str(x),
            "y": str(PANEL_TOP),
            "width": str(width),
            "height": str(PANEL_HEIGHT),
            "rx": str(PANEL_RADIUS),
            "fill": PAPER_THEME.panel,
            "stroke": GUIDE_COLOR,
            "stroke-width": format_svg_number(PANEL_STROKE_WIDTH),
        },
    )
    return panel


def _plot_point(x: Fraction, y: Fraction, outer_side: Fraction) -> tuple[Decimal, Decimal]:
    scale = Decimal(PLOT_SIDE) / _decimal(outer_side)
    return (
        Decimal(PLOT_X) + _decimal(x) * scale,
        Decimal(PLOT_Y + PLOT_SIDE) - _decimal(y) * scale,
    )


def _weight_radius(weight: Fraction, maximum: Fraction) -> Decimal:
    return MAX_ATOM_WEIGHT_RADIUS * (_decimal(weight) / _decimal(maximum)).sqrt()


def _draw_atom_field(panel: ET.Element, data: ProofVisualData) -> None:
    certificate = data.certificate
    witness = data.witness
    witness_labels = {atom.label for atom in witness.atoms}
    maximum_weight = max(atom.weight for atom in certificate.atoms)

    _text(
        panel,
        "Weighted atoms and one exact C4 witness",
        LEFT_PANEL_X + PANEL_INSET,
        PANEL_TITLE_Y,
        size=PANEL_TITLE_SIZE,
        weight=LABEL_WEIGHT,
    )
    _text(
        panel,
        "K = [0,381/100]²; each coloured disk's area is proportional to weight.",
        LEFT_PANEL_X + PANEL_INSET,
        PANEL_SUBTITLE_Y,
        size=SMALL_SIZE,
        fill=LABEL_MUTED_COLOR,
    )

    witness_half = certificate.square_side / 2
    witness_left = witness.centre[0] - witness_half
    witness_right = witness.centre[0] + witness_half
    witness_bottom = witness.centre[1] - witness_half
    witness_top = witness.centre[1] + witness_half
    witness_x, witness_y = _plot_point(witness_left, witness_top, certificate.outer_side)
    witness_far_x, witness_far_y = _plot_point(
        witness_right, witness_bottom, certificate.outer_side
    )
    sub(
        panel,
        "rect",
        {
            "x": format_svg_number(witness_x),
            "y": format_svg_number(witness_y),
            "width": format_svg_number(witness_far_x - witness_x),
            "height": format_svg_number(witness_far_y - witness_y),
            "fill": WITNESS_COLOR,
            "fill-opacity": "0.12",
            "stroke": "none",
            "data-feature": "c4-witness-fill",
        },
    )

    sites = sub(panel, "g", {"data-layer": "atom-sites", "aria-hidden": "true"})
    for atom in certificate.atoms:
        x, y = _plot_point(atom.x, atom.y, certificate.outer_side)
        sub(
            sites,
            "circle",
            {
                "cx": format_svg_number(x),
                "cy": format_svg_number(y),
                "r": format_svg_number(ATOM_SITE_RADIUS),
                "fill": GUIDE_COLOR,
                "fill-opacity": "0.5",
                "data-atom": atom.label,
            },
        )

    weights = sub(panel, "g", {"data-layer": "atom-weights", "aria-hidden": "true"})
    indexed_atoms = sorted(
        enumerate(certificate.atoms), key=lambda item: (item[1].weight, item[0])
    )
    for _index, atom in indexed_atoms:
        x, y = _plot_point(atom.x, atom.y, certificate.outer_side)
        inside = atom.label in witness_labels
        sub(
            weights,
            "circle",
            {
                "id": safe_id(f"atom-weight-{atom.label}"),
                "cx": format_svg_number(x),
                "cy": format_svg_number(y),
                "r": format_svg_number(_weight_radius(atom.weight, maximum_weight)),
                "fill": WITNESS_COLOR if inside else ATOM_COLOR,
                "stroke": "none",
                "data-atom": atom.label,
                "data-x": _fraction_text(atom.x),
                "data-y": _fraction_text(atom.y),
                "data-weight": _fraction_text(atom.weight),
                "data-inside-witness": str(inside).lower(),
            },
        )

    sub(
        panel,
        "rect",
        {
            "x": format_svg_number(witness_x),
            "y": format_svg_number(witness_y),
            "width": format_svg_number(witness_far_x - witness_x),
            "height": format_svg_number(witness_far_y - witness_y),
            "fill": "none",
            "stroke": WITNESS_COLOR,
            "stroke-width": format_svg_number(SHAPE_STROKE_WIDTH),
            "vector-effect": "non-scaling-stroke",
            "data-feature": "c4-witness-outline",
        },
    )
    centre_x, centre_y = _plot_point(
        witness.centre[0], witness.centre[1], certificate.outer_side
    )
    _line(
        panel,
        centre_x - 4,
        centre_y,
        centre_x + 4,
        centre_y,
        stroke=WITNESS_COLOR,
        width=SHAPE_STROKE_WIDTH,
    )
    _line(
        panel,
        centre_x,
        centre_y - 4,
        centre_x,
        centre_y + 4,
        stroke=WITNESS_COLOR,
        width=SHAPE_STROKE_WIDTH,
    )

    sub(
        panel,
        "rect",
        {
            "x": str(PLOT_X),
            "y": str(PLOT_Y),
            "width": str(PLOT_SIDE),
            "height": str(PLOT_SIDE),
            "fill": "none",
            "stroke": PACKING_BOUNDARY_COLOR,
            "stroke-width": format_svg_number(SHAPE_STROKE_WIDTH),
            "vector-effect": "non-scaling-stroke",
            "data-feature": "container-outline",
        },
    )

    ticks = (
        (Fraction(0), "0"),
        (Fraction(1), "1"),
        (Fraction(2), "2"),
        (Fraction(3), "3"),
        (certificate.outer_side, "L"),
    )
    for value, label in ticks:
        x, bottom = _plot_point(value, Fraction(0), certificate.outer_side)
        left, y = _plot_point(Fraction(0), value, certificate.outer_side)
        _line(panel, x, bottom, x, bottom + PLOT_TICK_LENGTH, stroke=PACKING_BOUNDARY_COLOR)
        _text(
            panel,
            label,
            x,
            bottom + PLOT_TICK_LABEL_OFFSET,
            size=SMALL_SIZE,
            anchor="middle",
        )
        _line(panel, left - PLOT_TICK_LENGTH, y, left, y, stroke=PACKING_BOUNDARY_COLOR)
        _text(
            panel,
            label,
            left - PLOT_TICK_LABEL_OFFSET + 5,
            y + 4,
            size=SMALL_SIZE,
            anchor="end",
        )

    _text(panel, "Weight", LEGEND_X, 194, size=BODY_SIZE, weight=LABEL_WEIGHT)
    _text(
        panel,
        "grey pin = atom site",
        LEGEND_X,
        216,
        size=SMALL_SIZE,
        fill=LABEL_MUTED_COLOR,
    )
    _text(
        panel,
        "area scales with w",
        LEGEND_X,
        236,
        size=SMALL_SIZE,
        fill=LABEL_MUTED_COLOR,
    )
    sorted_weights = sorted(atom.weight for atom in certificate.atoms)
    legend_weights = (
        sorted_weights[0],
        sorted_weights[len(sorted_weights) // 2],
        maximum_weight,
    )
    for row, weight in enumerate(legend_weights):
        y = 271 + 51 * row
        sub(
            panel,
            "circle",
            {
                "cx": str(LEGEND_CIRCLE_X),
                "cy": str(y),
                "r": format_svg_number(ATOM_SITE_RADIUS),
                "fill": GUIDE_COLOR,
            },
        )
        sub(
            panel,
            "circle",
            {
                "cx": str(LEGEND_CIRCLE_X),
                "cy": str(y),
                "r": format_svg_number(_weight_radius(weight, maximum_weight)),
                "fill": ATOM_COLOR,
            },
        )
        _text(panel, _fraction_text(weight), LEGEND_TEXT_X, y + 5, size=SMALL_SIZE)

    _text(panel, "Membership", LEGEND_X, 415, size=BODY_SIZE, weight=LABEL_WEIGHT)
    for y, colour, label in (
        (441, WITNESS_COLOR, "inside shown P"),
        (466, ATOM_COLOR, "elsewhere in K"),
    ):
        sub(
            panel,
            "circle",
            {"cx": str(LEGEND_CIRCLE_X), "cy": str(y), "r": "5", "fill": colour},
        )
        _text(panel, label, LEGEND_TEXT_X, y + 5, size=SMALL_SIZE)

    _text(panel, "Exact witness P", LEGEND_X, 500, size=BODY_SIZE, weight=LABEL_WEIGHT)
    _text(
        panel,
        "θ₀ = 0",
        LEGEND_X,
        522,
        size=SMALL_SIZE,
    )
    _text(
        panel,
        f"c = ({_fraction_text(witness.centre[0])}, {_fraction_text(witness.centre[1])})",
        LEGEND_X,
        544,
        size=SMALL_SIZE,
    )
    _text(
        panel,
        f"B = {_fraction_text(certificate.square_side)}",
        LEGEND_X,
        566,
        size=SMALL_SIZE,
    )
    _text(
        panel,
        f"{len(witness.atoms)} atoms",
        LEGEND_X,
        588,
        size=SMALL_SIZE,
    )
    _text(
        panel,
        f"μ(P) = {_fraction_text(witness.mass)}",
        LEGEND_X,
        610,
        size=SMALL_SIZE,
        fill=WITNESS_COLOR,
        weight=LABEL_WEIGHT,
    )
    _text(
        panel,
        (
            f"All {len(certificate.atoms):,} atoms:  μ(K) = "
            f"{_fraction_text(certificate.total_mass)} < {certificate.n}"
        ),
        PLOT_X,
        638,
        size=BODY_SIZE,
        weight=LABEL_WEIGHT,
    )


def _schematic_inner_points() -> tuple[tuple[Fraction, Fraction], ...]:
    half = Fraction(SCHEMATIC_SIDE) * SCHEMATIC_INNER_SIDE / 2
    along = (half * SCHEMATIC_COSINE, -half * SCHEMATIC_SINE)
    across = (half * SCHEMATIC_SINE, half * SCHEMATIC_COSINE)
    return tuple(
        (
            SCHEMATIC_CENTRE_X + along_sign * along[0] + across_sign * across[0],
            Fraction(SCHEMATIC_CENTRE_Y) + along_sign * along[1] + across_sign * across[1],
        )
        for along_sign, across_sign in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    )


def _draw_shrink_and_snap(panel: ET.Element, data: ProofVisualData) -> None:
    certificate = data.certificate
    gap = certificate.largest_half_gap_tangent
    _text(
        panel,
        "Shrink and snap to the angle net",
        RIGHT_PANEL_X + PANEL_INSET,
        PANEL_TITLE_Y,
        size=PANEL_TITLE_SIZE,
        weight=LABEL_WEIGHT,
    )
    _text(
        panel,
        "Rotate with Sᵢ; only d = |\N{GREEK SMALL LETTER ALPHA} - "
        "\N{GREEK SMALL LETTER THETA}\N{LATIN SUBSCRIPT SMALL LETTER K}| remains.",
        RIGHT_PANEL_X + PANEL_INSET,
        PANEL_SUBTITLE_Y,
        size=SMALL_SIZE,
        fill=LABEL_MUTED_COLOR,
    )
    _text(
        panel,
        "Display gap and shrink enlarged",
        SCHEMATIC_CENTRE_X,
        178,
        size=SMALL_SIZE,
        fill=LABEL_MUTED_COLOR,
        anchor="middle",
    )

    half = Fraction(SCHEMATIC_SIDE, 2)
    outer_x = SCHEMATIC_CENTRE_X - half
    outer_y = Fraction(SCHEMATIC_CENTRE_Y) - half
    sub(
        panel,
        "rect",
        {
            "x": format_svg_number(outer_x),
            "y": format_svg_number(outer_y),
            "width": str(SCHEMATIC_SIDE),
            "height": str(SCHEMATIC_SIDE),
            "fill": "none",
            "stroke": PACKING_BOUNDARY_COLOR,
            "stroke-width": format_svg_number(SHAPE_STROKE_WIDTH),
            "vector-effect": "non-scaling-stroke",
            "data-feature": "unit-square",
        },
    )
    inner_points = _schematic_inner_points()
    sub(
        panel,
        "polygon",
        {
            "points": " ".join(
                f"{format_svg_number(x)},{format_svg_number(y)}" for x, y in inner_points
            ),
            "fill": WITNESS_COLOR,
            "fill-opacity": "0.18",
            "stroke": WITNESS_COLOR,
            "stroke-width": format_svg_number(SHAPE_STROKE_WIDTH),
            "vector-effect": "non-scaling-stroke",
            "data-feature": "snapped-square",
        },
    )

    ray = Fraction(78)
    ray_end_x = SCHEMATIC_CENTRE_X + ray * SCHEMATIC_COSINE
    ray_end_y = Fraction(SCHEMATIC_CENTRE_Y) - ray * SCHEMATIC_SINE
    _line(
        panel,
        SCHEMATIC_CENTRE_X,
        SCHEMATIC_CENTRE_Y,
        SCHEMATIC_CENTRE_X + ray,
        SCHEMATIC_CENTRE_Y,
        stroke=PACKING_BOUNDARY_COLOR,
        width=GUIDE_STROKE_WIDTH,
        **{"stroke-dasharray": "5 4"},
    )
    _line(
        panel,
        SCHEMATIC_CENTRE_X,
        SCHEMATIC_CENTRE_Y,
        ray_end_x,
        ray_end_y,
        stroke=WITNESS_COLOR,
        width=SHAPE_STROKE_WIDTH,
    )
    sub(
        panel,
        "circle",
        {
            "cx": format_svg_number(SCHEMATIC_CENTRE_X),
            "cy": str(SCHEMATIC_CENTRE_Y),
            "r": "4",
            "fill": PAPER_THEME.ink,
            "data-feature": "common-centre",
        },
    )
    arc_radius = Fraction(48)
    arc_end_x = SCHEMATIC_CENTRE_X + arc_radius * SCHEMATIC_COSINE
    arc_end_y = Fraction(SCHEMATIC_CENTRE_Y) - arc_radius * SCHEMATIC_SINE
    sub(
        panel,
        "path",
        {
            "d": (
                f"M {format_svg_number(SCHEMATIC_CENTRE_X + arc_radius)} "
                f"{SCHEMATIC_CENTRE_Y} A {format_svg_number(arc_radius)} "
                f"{format_svg_number(arc_radius)} 0 0 0 {format_svg_number(arc_end_x)} "
                f"{format_svg_number(arc_end_y)}"
            ),
            "fill": "none",
            "stroke": WITNESS_COLOR,
            "stroke-width": format_svg_number(GUIDE_STROKE_WIDTH),
            "data-feature": "angle-error",
        },
    )
    _text(panel, "d", SCHEMATIC_CENTRE_X + 57, SCHEMATIC_CENTRE_Y - 7, size=BODY_SIZE)
    _text(
        panel,
        "unit Sᵢ at \N{GREEK SMALL LETTER ALPHA}",
        outer_x + 12,
        outer_y + 24,
        size=BODY_SIZE,
        weight=LABEL_WEIGHT,
    )
    _text(
        panel,
        "side-B Pᵢ at net angle",
        SCHEMATIC_CENTRE_X,
        SCHEMATIC_CENTRE_Y + 57,
        size=BODY_SIZE,
        fill=WITNESS_COLOR,
        weight=LABEL_WEIGHT,
        anchor="middle",
    )
    _text(
        panel,
        "same centre",
        SCHEMATIC_CENTRE_X - 8,
        SCHEMATIC_CENTRE_Y - 12,
        size=SMALL_SIZE,
        anchor="end",
    )

    _text(
        panel,
        "In Sᵢ's axes, Pᵢ has half-extent",
        RIGHT_PANEL_X + PANEL_INSET,
        474,
        size=BODY_SIZE,
        weight=LABEL_WEIGHT,
    )
    _text(
        panel,
        "(B/2)(cos d + sin d) <= (B/2)(1 + D).",
        RIGHT_PANEL_X + PANEL_INSET,
        498,
        size=SMALL_SIZE,
    )
    _text(
        panel,
        f"B = {_fraction_text(certificate.square_side)};  tan d <= D = {_fraction_text(gap)}",
        RIGHT_PANEL_X + PANEL_INSET,
        531,
        size=SMALL_SIZE,
    )
    _text(
        panel,
        f"B(1 + D) = {_fraction_text(data.containment_product)} < 1",
        RIGHT_PANEL_X + PANEL_INSET,
        555,
        size=SMALL_SIZE,
        fill=WITNESS_COLOR,
        weight=LABEL_WEIGHT,
    )
    _text(
        panel,
        "so Pᵢ lies strictly inside Sᵢ.",
        RIGHT_PANEL_X + PANEL_INSET,
        579,
        size=BODY_SIZE,
        weight=LABEL_WEIGHT,
    )
    _text(
        panel,
        f"Guaranteed per-side clearance > {_fraction_text(data.clearance_bound)}",
        RIGHT_PANEL_X + PANEL_INSET,
        607,
        size=SMALL_SIZE,
        fill=LABEL_MUTED_COLOR,
    )
    _text(
        panel,
        f"{len(certificate.half_tangents)} net angles cover [0, pi/4].",
        RIGHT_PANEL_X + PANEL_INSET,
        630,
        size=SMALL_SIZE,
        fill=LABEL_MUTED_COLOR,
    )


@emission_precision()
def render_visual(data: ProofVisualData | None = None) -> str:
    """Render the complete deterministic proof visual."""
    visual = data or load_visual_data()
    certificate = visual.certificate
    root = element(
        "svg",
        {
            "width": str(FIGURE_WIDTH),
            "height": str(FIGURE_HEIGHT),
            "viewBox": f"0 0 {FIGURE_WIDTH} {FIGURE_HEIGHT}",
            "role": "img",
            "aria-labelledby": "figure-title figure-description",
        },
    )
    append_title_desc(
        root,
        "How the T-018 weighted-atom lower-bound certificate works",
        (
            "The left panel plots all 1,121 rationally weighted atoms in the side-381/100 "
            "container. A grey pin marks every atom site; coloured disk area is proportional "
            "to exact weight. Orange identifies the 84 atoms in an exact side-9977/10000 "
            "C4 witness centred at 27/50 in both coordinates, whose mass is 4001/4000. "
            "The right panel is an explicitly enlarged schematic of the concentric shrink-"
            "and-snap step, followed by the exact containment inequality."
        ),
    )
    append_metadata(
        root,
        {
            "atom-count": str(len(certificate.atoms)),
            "certificate-id": visual.certificate_id,
            "claim": visual.claim,
            "container-side": _fraction_text(certificate.outer_side),
            "direction-count": str(len(certificate.half_tangents)),
            "largest-half-gap-tangent": _fraction_text(certificate.largest_half_gap_tangent),
            "total-mass": _fraction_text(certificate.total_mass),
            "view": "weighted-atoms-and-shrink-snap",
            "weight-encoding": (
                "grey pin marks each site; coloured disk area is proportional to exact weight"
            ),
            "witness-atom-count": str(len(visual.witness.atoms)),
            "witness-centre": ",".join(
                _fraction_text(value) for value in visual.witness.centre
            ),
            "witness-direction": visual.witness.direction.label,
            "witness-mass": _fraction_text(visual.witness.mass),
            "witness-square-side": _fraction_text(certificate.square_side),
        },
        coordinates="left panel mathematical-y-up; right panel explanatory schematic",
    )
    sub(
        root,
        "rect",
        {
            "width": str(FIGURE_WIDTH),
            "height": str(FIGURE_HEIGHT),
            "fill": PAPER_THEME.background,
        },
    )
    _text(
        root,
        "T-018: where the contradiction comes from",
        HEADER_X,
        TITLE_Y,
        size=TITLE_SIZE,
        weight=TITLE_WEIGHT,
    )
    _text(
        root,
        (
            "A finite weighted covering certificate turns every possible unit square "
            "into a mass budget."
        ),
        HEADER_X,
        SUBTITLE_Y,
        size=SUBTITLE_SIZE,
        fill=LABEL_MUTED_COLOR,
    )
    _draw_atom_field(_panel(root, LEFT_PANEL_X, LEFT_PANEL_WIDTH, "weighted atoms"), visual)
    _draw_shrink_and_snap(
        _panel(root, RIGHT_PANEL_X, RIGHT_PANEL_WIDTH, "shrink and snap"), visual
    )
    _line(root, HEADER_X, 665, FIGURE_WIDTH - HEADER_X, 665, stroke=GUIDE_COLOR)
    _text(
        root,
        (
            "Eleven disjoint Pᵢ force  μ(K) ≥ 11 \N{MULTIPLICATION SIGN} "
            "4001/4000 > 11, but the entire "
            "atom field has  μ(K) = 434547/40000 < 11."
        ),
        FIGURE_WIDTH // 2,
        FOOTER_Y,
        size=FOOTER_SIZE,
        weight=LABEL_WEIGHT,
        anchor="middle",
    )
    return serialize_svg(root)


def check_artifact() -> None:
    """Refuse a missing or stale retained visual."""
    expected = render_visual()
    if not ARTIFACT.is_file() or ARTIFACT.read_text(encoding="utf-8") != expected:
        raise ValueError(f"retained SVG differs from deterministic render: {ARTIFACT}")


def write_artifact() -> None:
    """Atomically replace the retained visual with the current deterministic render."""
    write_svg_atomic(ARTIFACT, render_visual())


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--check", action="store_true", help="report drift, write nothing")
    return command


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        if arguments.check:
            check_artifact()
            print(f"T-018 PROOF VISUAL CHECKED: {ARTIFACT.relative_to(ROOT.parent)}")
        else:
            write_artifact()
            print(f"wrote {ARTIFACT.relative_to(ROOT.parent)}")
    except (KeyError, OSError, TypeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
