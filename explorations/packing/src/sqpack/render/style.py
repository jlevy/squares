"""Fixed document-oriented visual tokens shared by every packing SVG."""

from __future__ import annotations

from dataclasses import dataclass

from sqpack.render.model import EvidenceTier

# The ordered families keep the prior palette's saturation/lightness character while
# spacing base hues by one twentieth of the color wheel (within RGB rounding).
SQUARE_HUE_PALETTE = (
    "#00b393",
    "#884853",
    "#a1ce85",
    "#8986ff",
    "#8a8c37",
    "#008aee",
    "#a0fbb4",
    "#c17deb",
    "#d8ad8d",
    "#d67fc3",
    "#7eb900",
    "#3b5cb3",
    "#8dff83",
    "#795eb1",
    "#b18000",
    "#00a8bf",
    "#008344",
    "#d078d7",
    "#be4d3d",
    "#e97aaf",
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
