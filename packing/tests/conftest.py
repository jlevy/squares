"""Collection guards for the packing project's explicit fast-test surface."""

from __future__ import annotations

from pathlib import Path

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Refuse pytest's false-green fallback when a configured test root is missing."""
    root = Path(str(config.rootpath))
    missing = [
        path for value in config.getini("testpaths") if not (path := root / value).is_dir()
    ]
    if missing:
        rendered = ", ".join(str(path.relative_to(root)) for path in missing)
        message = f"configured test directories do not exist: {rendered}"
        raise pytest.UsageError(message)
