"""Document-oriented visual tokens for packing SVGs."""

from __future__ import annotations

from dataclasses import dataclass

from sqpack.render.model import EvidenceTier


@dataclass(frozen=True)
class Theme:
    background: str
    panel: str
    ink: str
    muted: str
    container: str
    palette: tuple[str, ...]


@dataclass(frozen=True)
class LayoutMetrics:
    margin: int = 36
    caption_height: int = 72
    panel_gap: int = 32
    stroke_width: int = 3


PAPER_THEME = Theme(
    background="#ffffff",
    panel="#f7f8fa",
    ink="#17202a",
    muted="#5c6673",
    container="#263238",
    palette=("#4c78a8", "#f58518", "#54a24b", "#e45756", "#72b7b2", "#b279a2"),
)
LAYOUT = LayoutMetrics()


def color_for_square(index: int, theme: Theme = PAPER_THEME) -> str:
    return theme.palette[index % len(theme.palette)]


def evidence_style(evidence: EvidenceTier) -> tuple[str, str, str]:
    return {
        EvidenceTier.CANDIDATE: ("candidate", "8 5", "?"),
        EvidenceTier.VERIFIED_CONSTRUCTION: ("verified construction", "none", "V"),
        EvidenceTier.CERTIFIED_UPPER_BOUND: ("certified upper bound", "3 3", "U"),
        EvidenceTier.PROVED_OPTIMUM: ("proved optimum", "none", "P"),
    }[evidence]


def presentation_attributes(*, fill: str, stroke: str, width: int = 2) -> dict[str, str]:
    return {
        "fill": fill,
        "stroke": stroke,
        "stroke-width": str(width),
        "vector-effect": "non-scaling-stroke",
    }
