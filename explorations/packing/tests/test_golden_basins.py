"""Regression contracts for the expensive basin-map golden."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

from devtools import check_golden_basins


def test_deep_golden_ignores_yaml_wrapping(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Equivalent YAML must not become a platform-specific golden failure."""
    document: dict[str, object] = {
        "golden": {
            "note": (
                "A long explanatory note whose serializer wrapping may vary while its "
                "parsed value remains unchanged."
            ),
            "convergence_ladder": [],
            "cases": [],
        }
    }
    wrapped = yaml.safe_dump(document, sort_keys=False, width=48)
    rendered = yaml.safe_dump(document, sort_keys=False, width=100)
    assert wrapped != rendered
    assert yaml.safe_load(wrapped) == yaml.safe_load(rendered)

    golden = tmp_path / "basin-maps.yaml"
    golden.write_text(wrapped, encoding="utf-8")

    def no_build() -> None:
        return None

    def rebuilt() -> tuple[dict[str, object], list[str]]:
        return document, []

    monkeypatch.setattr(check_golden_basins, "GOLDEN", golden)
    monkeypatch.setattr(check_golden_basins, "build_engine", no_build)
    monkeypatch.setattr(check_golden_basins, "build", rebuilt)
    monkeypatch.setattr(sys, "argv", ["check_golden_basins", "--deep"])

    assert check_golden_basins.main() == 0
    output = capsys.readouterr().out
    assert "parsed golden content is identical" in output
    assert "GOLDEN BASIN CHECKS PASSED" in output


def test_semantic_yaml_comparison_preserves_types_and_rejects_duplicate_keys() -> None:
    """Only presentation differences may disappear from the deep golden diff."""
    assert check_golden_basins.canonical_yaml("value: 1\n") != (
        check_golden_basins.canonical_yaml("value: 1.0\n")
    )
    with pytest.raises(yaml.constructor.ConstructorError, match="duplicate key 'value'"):
        check_golden_basins.canonical_yaml("value: 1\nvalue: 1\n")
