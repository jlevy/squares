"""The residue-universe sweep: an exact universe, F1's order, and chunks that resume."""

from __future__ import annotations

import itertools
import json
from dataclasses import replace
from functools import cache
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from devtools import select_n17_sub_patterns as selector
from devtools import sweep_n17_residue_universe as tool

QUICK = selector.Budget(starts=4, hops=4, deep_starts=4, deep_hops=4)


def box(x0: float, x1: float, y0: float, y1: float) -> np.ndarray:
    return np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])


@cache
def toy() -> selector.Geometry:
    """Three crowded cells on the bottom wall (A to C) and two above its ends (D, E)."""
    return selector.make_geometry(
        [
            box(0.5, 0.7, 0.5, 0.6),
            box(1.1, 1.5, 0.5, 0.6),
            box(1.9, 2.1, 0.5, 0.6),
            box(0.5, 0.7, 1.6, 1.7),
            box(1.9, 2.1, 1.6, 1.7),
        ],
        ["A", "B", "C", "D", "E"],
    )


def test_the_universe_is_every_connected_class_in_a_residue_state_and_no_endpoint_image() -> (
    None
):
    geometry = toy()
    endpoint = 0b11010  # B, D and E: a feasible state standing in for the endpoint
    residue = tool.make_residue(geometry, [0b00111], endpoint, size=4)
    alive = set(residue.alive.tolist())
    assert alive == {0b11011, 0b11101, 0b11110}  # every 4-set but those holding A, B, C
    rows = tool.universe(geometry, residue, [2, 3])
    expected = set()
    for arity in (2, 3):
        for cells in itertools.combinations(range(5), arity):
            mask = selector.mask_of(cells)
            if not selector.connected(geometry, cells) or mask & endpoint == mask:
                continue
            if any(state & mask == mask for state in alive):
                expected.add(mask)
    assert {row["mask"] for row in rows} == expected
    for row in rows:
        assert row["coverage"] == sum(
            1 for state in alive if state & row["mask"] == row["mask"]
        )


def test_the_queue_follows_f1s_order_and_leaves_out_the_priority_subset() -> None:
    rows = [
        {"mask": 1, "arity": 9, "missing": 1, "coverage": 50},
        {"mask": 2, "arity": 8, "missing": 4, "coverage": 10},
        {"mask": 3, "arity": 8, "missing": 3, "coverage": 90},
        {"mask": 4, "arity": 8, "missing": 2, "coverage": 999},
        {"mask": 5, "arity": 8, "missing": 7, "coverage": 999},
    ]
    queued, left = tool.make_queue(rows)
    assert [r["mask"] for r in queued] == [3, 2, 1, 5]
    assert [r["mask"] for r in left] == [4]


def test_the_greedy_cover_takes_the_most_new_orbits_first() -> None:
    sets = {
        10: np.array([0, 1, 2], dtype=np.int64),
        20: np.array([2, 3], dtype=np.int64),
        30: np.array([0, 1], dtype=np.int64),
    }
    order = tool.greedy_cover(sets, 5)
    assert [(step["mask"], step["removes"]) for step in order] == [(10, 3), (20, 1)]
    assert order[-1]["orbits_left"] == 1


def write_plan(directory: Path) -> None:
    queue = [[mask, 2, 0, 1, 0] for mask in (0b00011, 0b00110, 0b00101)] + [
        [0b00111, 3, 0, 1, 0]
    ]
    _ = (directory / "plan.json").write_text(json.dumps({"queue": queue}), encoding="utf-8")


def test_a_sweep_resumes_where_it_stopped_with_the_same_verdicts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_plan(tmp_path)
    first = tool.sweep(tmp_path, chunk=2, geometry=toy(), screen=QUICK, full=QUICK)
    assert first == [0, 1]
    whole = [
        json.loads((tmp_path / f"chunk-{i:05d}.json").read_text(encoding="utf-8"))["classes"]
        for i in first
    ]
    assert [row["status"] for chunk in whole for row in chunk] == [
        "placed",
        "placed",
        "placed",
        "flagged",
    ]
    (tmp_path / "chunk-00001.json").unlink()
    searched: list[int] = []
    real = tool.search_class

    def counted(geometry: selector.Geometry, mask: int, **options: Any) -> dict[str, Any]:
        searched.append(mask)
        return real(geometry, mask, **options)

    monkeypatch.setattr(tool, "search_class", counted)
    again = tool.sweep(tmp_path, chunk=2, geometry=toy(), screen=QUICK, full=QUICK)
    assert again == [1]
    assert searched == [0b00101, 0b00111]
    redone = json.loads((tmp_path / "chunk-00001.json").read_text(encoding="utf-8"))["classes"]
    for old, new in zip(whole[1], redone, strict=True):
        old.pop("seconds")
        new.pop("seconds")
        assert old == new


def test_the_random_first_stage_places_cheaply_and_passes_the_rest_on_unchanged() -> None:
    first = tool.Levers(first=tool.FIRST)
    plain = tool.search_class(toy(), 0b00011, seed=1, screen=QUICK, full=QUICK)
    quick = tool.search_class(toy(), 0b00011, seed=1, screen=QUICK, full=QUICK, levers=first)
    assert plain["status"] == quick["status"] == "placed"
    assert quick["found_by"] == "random-first"
    crowded = tool.search_class(toy(), 0b00111, seed=1, screen=QUICK, full=QUICK)
    again = tool.search_class(
        toy(), 0b00111, seed=1, screen=QUICK, full=QUICK, levers=first, cache={}
    )
    assert crowded["status"] == again["status"] == "flagged"
    assert crowded["best_penetration"] == again["best_penetration"]
    assert crowded["pose"] == again["pose"]


RESUME_SCREEN = selector.Budget(starts=4, hops=4, deep_starts=4, deep_hops=4)
RESUME_FULL = selector.Budget(starts=4, hops=4, deep_starts=12, deep_hops=8)


def test_the_full_budget_resumed_from_the_screen_gives_the_same_row() -> None:
    screen, full = RESUME_SCREEN, RESUME_FULL
    plain = tool.search_class(toy(), 0b00111, seed=1, screen=screen, full=full)
    resumed = tool.search_class(
        toy(), 0b00111, seed=1, screen=screen, full=full, levers=tool.Levers(resume=True)
    )
    for row in (plain, resumed):
        row.pop("seconds")
    assert plain == resumed
    assert plain["status"] == "flagged"


def test_a_screen_with_another_finish_is_not_resumed() -> None:
    screen = replace(RESUME_SCREEN, finish=False)
    _, _, resumable = tool.tuned_budgets(screen, RESUME_FULL, tool.Levers(resume=True))
    assert not resumable
    _, _, resumable = tool.tuned_budgets(RESUME_SCREEN, RESUME_FULL, tool.Levers(resume=True))
    assert resumable
    plain = tool.search_class(toy(), 0b00111, seed=1, screen=screen, full=RESUME_FULL)
    resumed = tool.search_class(
        toy(), 0b00111, seed=1, screen=screen, full=RESUME_FULL, levers=tool.Levers(resume=True)
    )
    for row in (plain, resumed):
        row.pop("seconds")
    assert plain == resumed


def test_the_resume_check_compares_the_two_full_searches_field_for_field(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    levers = tool.LEVERS["combined-fast"]
    options: dict[str, Any] = {
        "seed": 1,
        "screen": RESUME_SCREEN,
        "full": RESUME_FULL,
        "levers": levers,
    }
    lines = [tool.resume_check(toy(), mask, cache={}, **options) for mask in (0b00011, 0b00111)]
    assert not lines[0]["reached_full"]
    crowded = lines[1]
    assert crowded["reached_full"]
    assert crowded["identical"]
    assert crowded["differing"] == []
    assert crowded["skipped_attempts"] == 3 + 4 + 4 + 4  # warm starts, starts, hops, deep
    row = tool.search_class(toy(), 0b00111, cache={}, **options)
    row.pop("seconds")
    assert crowded["row"] == row
    # A checkpoint on the wrong generator state must show up as a difference.
    real = selector.recheck_flag

    def corrupted(*args: Any, **kwargs: Any) -> dict[str, Any]:
        if kwargs.get("resume") is not None:
            other = selector.pattern_rng(2, 0b00111).bit_generator.state
            kwargs["resume"] = replace(kwargs["resume"], rng_state=other)
        return real(*args, **kwargs)

    monkeypatch.setattr(selector, "recheck_flag", corrupted)
    broken = tool.resume_check(toy(), 0b00111, cache={}, **options)
    assert not broken["identical"]
    assert "deep_start_state" in broken["differing"]
    results = tmp_path / "resume.jsonl"
    _ = results.write_text(
        "".join(json.dumps({**line, "reproduces_sweep": None}) + "\n" for line in lines),
        encoding="utf-8",
    )
    tally = tool.resume_tally(results)
    assert (tally["classes"], tally["reached_full"], tally["identical"]) == (2, 1, 1)
    assert tally["reached_full_by_status"]["flagged"]["classes"] == 1
