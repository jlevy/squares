"""Collection guards for the packing project's explicit fast-test surface."""

from __future__ import annotations

import sys
from collections.abc import Iterator
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


@pytest.fixture(autouse=True)
def isolate_n050_producer_refusal_module(
    request: pytest.FixtureRequest,
) -> Iterator[None]:
    """Give the frozen-import tests the clean module state their protocol requires."""

    module_name = "cases.n050_exact.source_semantics"
    if Path(str(request.node.path)).name != "test_n050_producer_refusal.py":
        yield
        return

    previous = sys.modules.pop(module_name, None)
    try:
        yield
    finally:
        sys.modules.pop(module_name, None)
        if previous is not None:
            sys.modules[module_name] = previous
