"""Fixed document-oriented visual tokens shared by every packing SVG."""

from __future__ import annotations

from dataclasses import dataclass

from sqpack.render.model import EvidenceTier

# Base hues for the twenty angle families. Slot 0 is pinned to right angles and
# slot 1 to 45 degree tilts, so those two carry most of the atlas and are chosen
# to stay quiet under repetition. Hues are spread with a minimum separation so no
# two families read as the same colour; see tests/test_render_colors.py.
SQUARE_HUE_PALETTE = (
    "#1faa8e",
    "#c3c45f",
    "#aa5585",
    "#166eac",
    "#b3543b",
    "#c9a13a",
    "#23b4e8",
    "#158655",
    "#a7539d",
    "#75951c",
    "#c8691e",
    "#1990a2",
    "#714fad",
    "#67b45c",
    "#e26e82",
    "#8286e9",
    "#ce871b",
    "#147e7c",
    "#4571c9",
    "#a86cc6",
)
SQUARE_FILL_PALETTE = SQUARE_HUE_PALETTE
SQUARE_FILL_OPACITY = 1.0
PACKING_BOUNDARY_COLOR = "#000000"
PACKING_BOUNDARY_WIDTH = 1.25
CONTACT_HIGHLIGHT_COLOR = "#e3c64a"
CONTACT_HIGHLIGHT_OPACITY = 0.6
CONTACT_HIGHLIGHT_STROKE_WIDTH = 9
CONTACT_HIGHLIGHT_POINT_RADIUS = 5.5
CONTACT_CLIP_POLICY = "participating-square-union"
CONTACT_CENSUS_COLOR = "#d95f02"
CONTACT_CENSUS_OPACITY = 0.78
CONTACT_CENSUS_STROKE_WIDTH = 2.5
CONTACT_CENSUS_DASH = "7 5"


@dataclass(frozen=True)
class Theme:
    background: str
    panel: str
    ink: str
    muted: str
    container: str
    contact: str
    palette: tuple[str, ...]


@dataclass(frozen=True)
class LayoutMetrics:
    margin: int = 36
    caption_height: int = 72
    panel_gap: int = 32
    stroke_width: float = PACKING_BOUNDARY_WIDTH
    contact_stroke_width: int = CONTACT_HIGHLIGHT_STROKE_WIDTH
    contact_point_radius: float = CONTACT_HIGHLIGHT_POINT_RADIUS


PAPER_THEME = Theme(
    background="#ffffff",
    panel="#f7f8fa",
    ink="#17202a",
    muted="#5c6673",
    container=PACKING_BOUNDARY_COLOR,
    contact=CONTACT_HIGHLIGHT_COLOR,
    palette=SQUARE_FILL_PALETTE,
)
LAYOUT = LayoutMetrics()


def color_for_square(index: int, theme: Theme = PAPER_THEME) -> str:
    return theme.palette[index % len(theme.palette)]


def evidence_style(evidence: EvidenceTier) -> tuple[str, str, str]:
    return {
        EvidenceTier.CANDIDATE: ("candidate", "8 5", "?"),
        EvidenceTier.NUMERICALLY_CHECKED: ("numerically checked", "none", "N"),
        EvidenceTier.CERTIFIED_UPPER_BOUND: ("certified upper bound", "3 3", "U"),
        EvidenceTier.PROVED_OPTIMUM: ("proved optimum", "none", "P"),
    }[evidence]


def presentation_attributes(
    *, fill: str, stroke: str, width: int | float = 2
) -> dict[str, str]:
    return {
        "fill": fill,
        "stroke": stroke,
        "stroke-width": str(width),
        "vector-effect": "non-scaling-stroke",
    }
