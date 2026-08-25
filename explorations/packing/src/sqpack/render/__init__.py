"""Deterministic, source-preserving SVG rendering for square packings."""

from sqpack.render.model import (
    AnnotationLevel,
    ContainerWall,
    EvidenceTier,
    Overlay,
    PackingFrame,
    PackingTrajectory,
    RenderSpec,
    TrajectoryKind,
    ViewLevel,
)

__all__ = [
    "AnnotationLevel",
    "ContainerWall",
    "EvidenceTier",
    "Overlay",
    "PackingFrame",
    "PackingTrajectory",
    "RenderSpec",
    "TrajectoryKind",
    "ViewLevel",
    "render_packing_svg",
]


def render_packing_svg(*args, **kwargs):
    """Import the renderer lazily so model-only users do not load XML helpers."""
    from sqpack.render.packing import render_packing_svg as render  # noqa: PLC0415

    return render(*args, **kwargs)
