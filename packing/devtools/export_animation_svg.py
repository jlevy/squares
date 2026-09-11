#!/usr/bin/env python3
"""Export a PackingAnimation as one self-contained animated SVG.

The embeddable artifact. No build step, no framework, no JavaScript -- a single `.svg` that
animates on its own, so it works inline, in an `<img>`, or in a static-site build that runs
no script at all. That constraint is the strictest of the four consumers in the plan, which
is why it decides the shape: a renderer that can produce this can trivially serve the
workbench, the atlas view and the video capture, while one built for the workbench first
could not.

Usage, from `packing/`:
    uv run --frozen python -m devtools.export_animation_svg run.json --out run.svg
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal
from pathlib import Path
from typing import Any

from devtools.animation_from_trace import trajectory_from_animation
from sqpack.render import render_packing_svg
from sqpack.render.model import (
    AnnotationLevel,
    HueScheme,
    RenderSpec,
    ShadeScheme,
    ViewLevel,
)


class GuidedWithoutLabelError(ValueError):
    """A guided animation was asked to export without saying so."""


def export_svg(document: dict[str, Any], *, width: int = 720) -> str:
    """One animated SVG from one animation document.

    Refuses a guided animation whose frames do not carry the label. That is not
    bookkeeping: a run that ends on a retained packing ended there because it was pulled,
    and the same instruments report what searches actually reach. An export that drops the
    mark produces a file indistinguishable from a result.
    """
    if document.get("guided") and not any(frame.get("guided") for frame in document["frames"]):
        msg = (
            "animation is marked guided but no frame carries it; "
            "an exported file would be indistinguishable from a search result"
        )
        raise GuidedWithoutLabelError(msg)

    trajectory = trajectory_from_animation(document)
    duration = document.get("duration_seconds", 8.0)
    palette = document.get("palette") or {}
    spec = RenderSpec(
        # The animation says what its colours should MEAN and the renderer owns what they
        # are. Reading this was missing on the first pass, so every export came out under
        # the renderer's default angle-hue scheme while its own document asked for colour
        # by identity -- the field was defined and then ignored.
        hue_scheme={"identity": HueScheme.INDEX, "angle-class": HueScheme.ANGLE}.get(
            palette.get("hue", "identity"), HueScheme.INDEX
        ),
        shade_scheme={"full-side-contact": ShadeScheme.CONTACTS}.get(
            palette.get("shade", "none"), ShadeScheme.CONTRAST
        ),
        title=document.get("name", "packing animation"),
        description=_describe(document),
        duration_seconds=Decimal(str(duration)),
        width=width,
        annotations=AnnotationLevel.MINIMAL,
        overlays=frozenset(),
        # The motion is gated on this, and the default is OVERVIEW. A spec that forgets it
        # renders the final frame perfectly and silently drops every other one, which is
        # how a still picture ships as an animation.
        view=ViewLevel.TRAJECTORY,
    )
    svg = render_packing_svg(trajectory.frames[-1], trajectory=trajectory, spec=spec)
    if len(trajectory.frames) > 1 and "@keyframes" not in svg:
        msg = "an animation of several frames rendered without motion; it would be a still"
        raise ValueError(msg)
    return svg


def _describe(document: dict[str, Any]) -> str:
    """The description a screen reader gets, which is also where the honesty lives."""
    n = document["n"]
    parts = [f"An animation of {n} unit squares in a square container."]
    if document.get("guided"):
        parts.append(
            "Some frames were guided onto a known packing rather than found by search."
        )
    unpacked = sum(1 for frame in document["frames"] if not frame.get("feasible", True))
    if unpacked:
        parts.append(f"{unpacked} of {len(document['frames'])} frames are not valid packings.")
    return " ".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("animation", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--width", type=int, default=720)
    o = ap.parse_args()

    document = json.loads(o.animation.read_text(encoding="utf-8"))
    svg = export_svg(document, width=o.width)
    o.out.write_text(svg, encoding="utf-8")
    scripted = "<script" in svg
    print(
        f"{o.out}: {len(svg) / 1024:.0f} kB, {len(document['frames'])} frames, "
        f"{'CONTAINS SCRIPT' if scripted else 'no script'}, "
        f"{'guided' if document.get('guided') else 'unguided'}"
    )
    return 1 if scripted else 0


if __name__ == "__main__":
    raise SystemExit(main())
