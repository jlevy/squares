"""Shared semantic items for the website and poster atlas legends.

The caller supplies counts from the canonical assessments. This module chooses the
same wording, marker order and two-column grouping for each renderer, without I/O.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal

from devtools.build_bound_citations import RECENT_SINCE


@dataclass(frozen=True, slots=True)
class AtlasLegendCounts:
    proved_optimal: int
    exact_value_known: int
    only_known_numerically: int
    known_rigid: int
    recent_results: int


@dataclass(frozen=True, slots=True)
class LegendItem:
    key: str
    marker: Literal["O", "=", "≈", "R", "star", "angles", "shades"]
    label: str
    count: int | None = None
    marker_values: tuple[int, ...] = ()
    # Optional visible labels align with marker_values; empty labels leave a swatch plain.
    marker_labels: tuple[str, ...] = ()

    @property
    def text(self) -> str:
        return self.label if self.count is None else f"{self.label} ({self.count})"


@dataclass(frozen=True, slots=True)
class AtlasLegend:
    left: tuple[LegendItem, ...]
    right: tuple[LegendItem, ...]

    @property
    def items(self) -> tuple[LegendItem, ...]:
        return (*self.left, *self.right)


def recent_label(recent_since: date = RECENT_SINCE) -> str:
    return f"recent result, since {recent_since:%B, %Y}"


def atlas_legend(
    counts: AtlasLegendCounts, *, recent_since: date = RECENT_SINCE
) -> AtlasLegend:
    """The four status rows and three recency/color rows, in reading order."""
    return AtlasLegend(
        left=(
            LegendItem("optimal", "O", "proved optimal", counts.proved_optimal),
            LegendItem("exact", "=", "exact value known", counts.exact_value_known),
            LegendItem(
                "numerical", "≈", "only known numerically", counts.only_known_numerically
            ),
            LegendItem("rigid", "R", "rigid", counts.known_rigid),
        ),
        right=(
            LegendItem(
                "recent",
                "star",
                recent_label(recent_since),
                counts.recent_results,
            ),
            LegendItem(
                "angles",
                "angles",
                "colors indicate distinct tilt angles",
                marker_values=(0, 1, 2, 3),
                marker_labels=("90\N{DEGREE SIGN}", "45\N{DEGREE SIGN}", "", ""),
            ),
            LegendItem(
                "contacts",
                "shades",
                "shade indicates number of full-side contacts",
                marker_values=(4, 3, 2, 1, 0),
            ),
        ),
    )
