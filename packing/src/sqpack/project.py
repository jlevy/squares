"""Locate and validate the repository state used by project applications.

The reusable ``sqpack`` library can be imported from an ordinary wheel. The campaign,
ledger, and validation commands are different: they operate on the packing checkout's
retained evidence and developer tools. This module makes that boundary explicit and
turns an installed command with no checkout into an actionable failure.
"""

from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT_ENV = "PACKING_PROJECT_ROOT"
PROJECT_MARKERS = ("pyproject.toml", "campaign", "cases", "devtools", "frontier")


class ProjectLayoutError(RuntimeError):
    """A repository application cannot find the packing project it operates on."""


def _missing_markers(root: Path) -> list[str]:
    return [name for name in PROJECT_MARKERS if not (root / name).exists()]


def configured_project_root() -> Path:
    """Return the explicit, source-layout, or working-directory project candidate."""
    override = os.environ.get(PROJECT_ROOT_ENV)
    if override:
        return Path(override).expanduser().resolve()

    source_candidate = Path(__file__).resolve().parents[2]
    if not _missing_markers(source_candidate):
        return source_candidate

    working_directory = Path.cwd().resolve()
    for candidate in (working_directory, *working_directory.parents):
        if not _missing_markers(candidate):
            return candidate
    return source_candidate


def require_project_root(root: Path | None = None) -> Path:
    """Return a validated packing checkout or raise with recovery instructions."""
    candidate = configured_project_root() if root is None else root.resolve()
    missing = _missing_markers(candidate)
    if missing:
        joined = ", ".join(missing)
        raise ProjectLayoutError(
            f"packing project checkout not found at {candidate}; missing {joined}. "
            f"Run from packing or set {PROJECT_ROOT_ENV} to that directory."
        )
    return candidate
