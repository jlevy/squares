"""Repository-owned browser assets for deterministic Motion Lab artifacts."""

from __future__ import annotations

from importlib.resources import files

from sqpack.render.style import (
    CONTACT_HIGHLIGHT_COLOR,
    PACKING_BOUNDARY_COLOR,
    SQUARE_FILL_PALETTE,
)

_ASSET_NAMES = frozenset(
    {
        "exact-n5-model.js",
        "free-quench-model.js",
        "free-quench.js",
        "motion-lab.css",
        "motion-lab.js",
    }
)
_PACKING_TOKEN_MARKER = "  /* PACKING_RENDER_TOKENS */"


def asset_text(name: str) -> str:
    """Read one allow-listed text asset from the installed package."""
    if name not in _ASSET_NAMES:
        raise ValueError(f"unknown Motion Lab asset: {name}")
    return files(__package__).joinpath(name).read_text(encoding="utf-8")


def motion_lab_css() -> str:
    """Return shared CSS with the publication renderer's geometry tokens injected."""
    base = asset_text("motion-lab.css")
    palette = [
        f"  --packing-boundary: {PACKING_BOUNDARY_COLOR};",
        f"  --contact: {CONTACT_HIGHLIGHT_COLOR};",
        *(
            f"  --square-{index:02d}: {color};"
            for index, color in enumerate(SQUARE_FILL_PALETTE)
        ),
    ]
    if base.count(_PACKING_TOKEN_MARKER) != 1:
        raise ValueError("Motion Lab CSS must contain one packing-token marker")
    return base.replace(_PACKING_TOKEN_MARKER, "\n".join(palette))
