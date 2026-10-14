"""Citation-scan scope, ordering and unknown-defect refusals."""

from pathlib import Path

import pytest
import yaml

from devtools import validate_schemas


def test_citation_sources_preserve_scope_and_yaml_before_markdown(tmp_path: Path) -> None:
    admitted = ["z.yaml", "a.yaml", "README.md", "nested/guide.md", "resources.md"]
    excluded = [
        ".hidden.md",
        ".private/secret.yaml",
        "resources/archive.md",
        "node_modules/package/README.md",
        ".venv/package/schema.yaml",
    ]
    for relative in admitted + excluded:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("D-000", encoding="utf-8")
    assert validate_schemas.defect_citation_paths(tmp_path) == [
        *(tmp_path / name for name in sorted(admitted) if name.endswith(".yaml")),
        *(tmp_path / name for name in sorted(admitted) if name.endswith(".md")),
    ]


def test_citation_scan_retains_unknown_refusal_and_regex_boundaries(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    frontier = tmp_path / "packing" / "frontier"
    frontier.mkdir(parents=True)
    (frontier.parent / "defects.yaml").write_text(
        yaml.dump(
            {
                "count": 1,
                "defects": [
                    {
                        "id": "D-001",
                        "status": "fixed",
                        "class": "process",
                        "recorded_in": "README.md",
                    }
                ],
            },
            Dumper=getattr(yaml, "CSafeDumper", yaml.SafeDumper),
        ),
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text(
        "D-001 D-000 D-0000 AD-000 D-000_suffix", encoding="utf-8"
    )
    (tmp_path / "plain.md").write_text("No defect citation here.", encoding="utf-8")
    for relative in [
        "controls.yaml",
        "defects.md",
        "review-2026-09-04-pr78-s11-adversarial.md",
        "resources/archive.md",
        ".private/notes.md",
        "node_modules/package/README.md",
    ]:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("D-999", encoding="utf-8")
    monkeypatch.setattr(validate_schemas, "REPO", tmp_path)
    monkeypatch.setattr(validate_schemas, "FRONTIER", frontier)
    assert validate_schemas.defect_checks() == ["README.md: cites D-000, not in defects.yaml"]
