"""Targeted screen refresh preserves the complete validated corpus."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

from devtools import atlas_orientation
from devtools import screen_translation_escape as screen
from devtools.atlas_orientation import (
    Reflection,
    orient_atlas_witness,
    reflect_escape_case,
    reflect_x_axis,
)
from sqpack.known_best import exact_grid_witness
from sqpack.witness import witness_document


@pytest.fixture
def corpus(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    monkeypatch.setattr(screen, "ROOT", tmp_path)
    monkeypatch.setattr(screen, "OUTPUT", tmp_path / "screen.json")
    entries = []
    for n in (1, 2, 3):
        path = tmp_path / f"n-{n}.yaml"
        witness = exact_grid_witness(n, 3, frontier_path=f"frontier/n-{n}.md")
        path.write_text(witness_document(witness, schema="../witness.schema.yaml"))
        entries.append(
            {
                "n": n,
                "reported_side": "3",
                "witness": {"path": path.name},
                "source": {"kind": "exact-grid"},
            }
        )
    monkeypatch.setattr(screen, "manifest_entries", lambda: entries)
    screen.update(1)
    return entries


@pytest.mark.parametrize("exclude", [False, True])
def test_selected_geometry_is_replayed_and_unselected_results_are_preserved(
    corpus: list[dict[str, Any]], monkeypatch: pytest.MonkeyPatch, *, exclude: bool
) -> None:
    original = json.loads(screen.OUTPUT.read_text())["screen"]
    path = screen.ROOT / corpus[1]["witness"]["path"]
    witness = exact_grid_witness(2, 4, frontier_path="frontier/n-2.md")
    if exclude:
        witness["squares"][0]["corners"][1][0] = "1001/1000"
    path.write_text(witness_document(witness, schema="../witness.schema.yaml"))
    corpus[1]["reported_side"] = "4"
    expected = screen._screen_entry(corpus[1])  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    actual_screen = screen._screen_entry  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    seen = []

    def recording(entry: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
        seen.append(entry["n"])
        return actual_screen(entry)

    monkeypatch.setattr(screen, "_screen_entry", recording)
    screen.update(1, only=[2])
    updated = json.loads(screen.OUTPUT.read_text())["screen"]
    assert seen == [2]
    assert [row for row in updated["cases"] if row["n"] != 2] == [
        row for row in original["cases"] if row["n"] != 2
    ]
    records = updated["cases"] if expected[0] else updated["excluded"]
    assert next(row for row in records if row["n"] == 2) == expected[1]
    assert updated["aggregate"]["records_screened"] == (2 if exclude else 3)
    assert updated["aggregate"]["records_excluded"] == int(exclude)
    assert screen.identity_errors(updated, {row["n"]: row for row in corpus}) == []


def test_selected_exclusion_is_removed_when_new_geometry_can_be_screened(
    corpus: list[dict[str, Any]],
) -> None:
    path = screen.ROOT / corpus[1]["witness"]["path"]
    witness = exact_grid_witness(2, 3, frontier_path="frontier/n-2.md")
    witness["squares"][0]["corners"][1][0] = "1001/1000"
    path.write_text(witness_document(witness, schema="../witness.schema.yaml"))
    screen.update(1, only=[2])
    assert [
        row["n"] for row in json.loads(screen.OUTPUT.read_text())["screen"]["excluded"]
    ] == [2]
    witness = exact_grid_witness(2, 3, frontier_path="frontier/n-2.md")
    path.write_text(witness_document(witness, schema="../witness.schema.yaml"))
    screen.update(1, only=[2])
    updated = json.loads(screen.OUTPUT.read_text())["screen"]
    assert updated["excluded"] == []
    assert [row["n"] for row in updated["cases"]] == [1, 2, 3]
    assert updated["aggregate"]["records_screened"] == 3


@pytest.mark.parametrize(
    "failure", ["unknown", "missing", "duplicate", "method", "inputs", "contract", "stale"]
)
def test_invalid_subset_refresh_refuses_before_replacing_retained_output(
    corpus: list[dict[str, Any]], failure: str
) -> None:
    document = json.loads(screen.OUTPUT.read_text())
    only = [2]
    if failure == "unknown":
        only = [4]
    elif failure == "missing":
        document["screen"]["cases"] = document["screen"]["cases"][:-1]
    elif failure == "duplicate":
        document["screen"]["cases"].append(document["screen"]["cases"][0])
    elif failure == "method":
        document["screen"]["method"]["materialization_digits"] = 15
    elif failure == "inputs":
        document["screen"]["inputs"]["witnesses"] = "witnesses/another-corpus"
    elif failure == "contract":
        document["softschema"]["contract"] = "translation-escape-screen/future"
    else:
        corpus[2]["reported_side"] = "4"
    screen.OUTPUT.write_text(json.dumps(document))
    before = screen.OUTPUT.read_bytes()
    with pytest.raises(
        ValueError, match=r"absent|coverage|method|inputs|contract|stale records"
    ):
        screen.update(1, only=only)
    assert screen.OUTPUT.read_bytes() == before


def test_descriptive_prose_changes_preserve_unselected_decision_results(
    corpus: list[dict[str, Any]],
) -> None:
    document = json.loads(screen.OUTPUT.read_text())
    retained_cases = document["screen"]["cases"]
    original_description = document["screen"]["method"]["direction_search"]
    document["screen"]["method"]["direction_search"] = "An older explanatory sentence."
    screen.OUTPUT.write_text(json.dumps(document))
    screen.update(1, only=[corpus[1]["n"]])
    updated = json.loads(screen.OUTPUT.read_text())["screen"]
    assert updated["cases"] == retained_cases
    assert updated["method"]["direction_search"] == original_description


def test_subset_refresh_requires_an_existing_complete_screen(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(screen, "OUTPUT", tmp_path / "missing.json")
    with pytest.raises(ValueError, match="requires a retained screen"):
        screen.update(1, only=[2])
    assert not screen.OUTPUT.exists()


@pytest.mark.parametrize("args", [["--check", "--n", "2"], ["--update", "--jobs", "0"]])
def test_cli_refuses_invalid_targeted_modes(
    monkeypatch: pytest.MonkeyPatch, args: list[str]
) -> None:
    monkeypatch.setattr(sys, "argv", ["screen_translation_escape", *args])
    with pytest.raises(SystemExit, match=r"narrows|positive"):
        screen.main()


@pytest.mark.parametrize("operation", ["reflect-x-axis", "reflect-y-axis"])
def test_reflected_screen_replays_each_mapped_slide_against_the_selected_pose(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    operation: Reflection,
) -> None:
    witness = {
        "id": "W-pair",
        "n": 2,
        "side": "3",
        "square_size": "1",
        "representation": "center-angle",
        "scalar": {"kind": "decimal"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "radians",
        },
        "squares": [
            {"id": 7, "center": ["0.75", "0.75"], "angle": "0.2"},
            {"id": 3, "center": ["2.25", "2.25"], "angle": "0"},
        ],
        "claim": {
            "coordinate_provenance": "numerically-checked",
            "method": "numerical-multiprecision",
            "precision": {"decimal_digits": 120, "rounding": "nearest"},
            "tolerance": "1e-12",
            "limitations": "Synthetic finite-precision fixture.",
        },
        "source": {"path": "tests/pair"},
    }
    path = tmp_path / "pair.yaml"
    path.write_text(witness_document(witness, schema=str(screen.WITNESS_SCHEMA)))
    entry = {"n": 2, "reported_side": "3", "witness": {"path": str(path)}}
    _, original = screen._screen_entry(entry)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    monkeypatch.setattr(atlas_orientation, "REFLECTED_N", 2)
    monkeypatch.setattr(atlas_orientation, "PARENT_FACTS", "tests/pair")
    monkeypatch.setattr(atlas_orientation, "PARENT_SOURCE_KEY", "synthetic-parent")
    witness["source"]["key"] = "synthetic-parent"
    selected = orient_atlas_witness(witness)
    if operation == "reflect-x-axis":
        legacy = reflect_x_axis(witness)
        legacy["certificate"] = selected["certificate"]
        legacy["certificate"]["geometry_transform"]["operation"] = operation
        selected = legacy
    path.write_text(witness_document(selected, schema=str(screen.WITNESS_SCHEMA)))
    selected_squares, _, _ = screen.materialize_record(entry)
    replay = screen._replay  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    selected_replays = []

    def recording(geometry: screen.RecordGeometry, motion: dict, tolerance: Any) -> bool:
        if geometry.squares == selected_squares:
            selected_replays.append(motion["witness_square_id"])
        return replay(geometry, motion, tolerance)

    monkeypatch.setattr(screen, "_replay", recording)
    screened, reflected = screen._screen_entry(entry)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert screened is True
    assert reflected == reflect_escape_case(original, operation=operation)
    assert selected_replays == [7, 3]
    monkeypatch.setattr(screen, "_replay", lambda *_args: False)
    with pytest.raises(ValueError, match=r"reflected certificate.*did not replay"):
        screen._reflected_record(entry, original, [7, 3])  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
