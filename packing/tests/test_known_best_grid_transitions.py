"""Grid thresholds follow retained source facts rather than a count formula."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from sqpack.known_best import GridTransition, grid_transitions


def _entries() -> list[dict[str, Any]]:
    return [
        {
            "n": n,
            "reported_side": str(1 if n == 1 else 2 if n <= 4 else 3),
            "source": {"kind": "packet-derived-facts" if n == 5 else "exact-grid"},
        }
        for n in range(1, 10)
    ]


def test_grid_transitions_read_the_actual_source_and_validate_its_suffix() -> None:
    entries = _entries()
    assert grid_transitions(entries) == (
        GridTransition(1, 1),
        GridTransition(2, 2),
        GridTransition(3, 6),
    )
    transition = grid_transitions(entries)[-1]
    assert (transition.first_n, transition.last_n, transition.has_irregular_prefix) == (
        5,
        9,
        True,
    )
    assert not grid_transitions(entries)[1].has_irregular_prefix
    assert grid_transitions([]) == ()
    entries[6]["source"]["kind"] = "packet-derived-facts"
    with pytest.raises(ValueError, match="non-grid n=7 follows first grid n=6"):
        grid_transitions(entries)


def test_grid_transitions_refuse_missing_partial_or_inconsistent_facts() -> None:
    with pytest.raises(ValueError, match="contiguous"):
        grid_transitions(_entries()[1:])
    with pytest.raises(ValueError, match="complete"):
        grid_transitions(_entries()[:-1])
    entries = _entries()
    entries[-1]["reported_side"] = "2.999"
    with pytest.raises(ValueError, match="reported side"):
        grid_transitions(entries)
    with pytest.raises(ValueError, match="inside"):
        GridTransition(3, 10)


def test_retained_thresholds_include_the_noninteger_n211_before_the_grid_suffix() -> None:
    manifest = Path(__file__).resolve().parents[1] / "atlas/known-best/manifest.json"
    entries = json.loads(manifest.read_text())["atlas"]["entries"]
    found = grid_transitions(entries)
    assert [item.first_grid_n for item in found] == [
        1,
        2,
        6,
        12,
        20,
        30,
        42,
        56,
        72,
        90,
        111,
        133,
        157,
        183,
        212,
        242,
        274,
        308,
    ]
    assert entries[210]["source"]["kind"] == "packet-derived-facts"
    assert found[14] == GridTransition(15, 212)
