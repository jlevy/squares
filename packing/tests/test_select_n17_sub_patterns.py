"""Controls for the H-267 sub-pattern selector, a heuristic and not a certificate."""

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
from devtools.provenance import git_blob
from devtools.select_n17_sub_patterns import (
    MARGIN,
    Budget,
    Geometry,
    Problem,
    all_states,
    canonical,
    consume,
    contact_clusters,
    count_classes,
    cover_geometry,
    endpoint_pose,
    endpoint_witnesses,
    greedy_order,
    image_mask,
    main,
    make_geometry,
    mask_of,
    missing_pairs,
    occurring_classes,
    orbit,
    pattern_rng,
    polygon_distance,
    recheck_flag,
    run,
    search,
    split_classes,
    survivors,
    sweep,
    tight_control,
    transform_pose,
)

QUICK = Budget(starts=4, hops=4, deep_starts=4, deep_hops=4)


def box(x0: float, x1: float, y0: float, y1: float) -> np.ndarray:
    return np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])


@cache
def cover() -> Geometry:
    return cover_geometry()


@cache
def endpoint() -> dict[str, Any]:
    return endpoint_pose()


@cache
def strip() -> Geometry:
    """Three cells on the bottom wall: each adjacent pair fits only touching, all three never.

    A centre at height at most 0.6 allows a turn of about 0.2 rad, so the squares are
    nearly upright and need about one unit of `x` each; A and C are at most 1.6 apart.
    """
    return make_geometry(
        [box(0.5, 0.7, 0.5, 0.6), box(1.1, 1.5, 0.5, 0.6), box(1.9, 2.1, 0.5, 0.6)],
        ["A", "B", "C"],
    )


@cache
def strip_with_roof() -> Geometry:
    """The strip with a cell above each end: A to C crowd, every other pattern fits.

    With five-cell states the one state holds A to C, so once that triple is flagged no
    state survives and every arity-4 class that is not its superset is restricted out.
    """
    return make_geometry(
        [
            box(0.5, 0.7, 0.5, 0.6),
            box(1.1, 1.5, 0.5, 0.6),
            box(1.9, 2.1, 0.5, 0.6),
            box(0.5, 0.7, 1.6, 1.7),
            box(1.9, 2.1, 1.6, 1.7),
        ],
        ["A", "B", "C", "D", "E"],
    )


LEVEL_KEYS = {
    "classes",
    "pruned_as_supersets",
    "searched",
    "feasible",
    "feasible_by",
    "flagged",
    "attempts",
    "seconds",
}


def without_seconds(record: dict[str, Any]) -> dict[str, Any]:
    levels = {arity: dict(level) for arity, level in record["levels"].items()}
    for level in levels.values():
        level.pop("seconds")
    return {**{k: v for k, v in record.items() if k != "seconds"}, "levels": levels}


def ring_group() -> tuple[tuple[int, ...], ...]:
    """D4 on the eight boundary cells of a 3 x 3 grid, as permutations."""
    cells = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if (x, y) != (0, 0)]
    index = {cell: k for k, cell in enumerate(cells)}
    group: list[tuple[int, ...]] = []
    for reflect in (False, True):
        for turns in range(4):
            images = []
            for x, y in cells:
                u, v = (-x, y) if reflect else (x, y)
                for _ in range(turns):
                    u, v = -v, u
                images.append(index[(u, v)])
            group.append(tuple(images))
    return tuple(group)


def test_polygon_distance_sees_crossings_and_not_collinear_edges() -> None:
    assert polygon_distance(box(0, 3, 1, 2), box(1, 2, 0, 3)) == 0.0  # a plus, no vertex inside
    assert abs(polygon_distance(box(0, 1, 0, 1), box(3, 4, 0, 1)) - 2.0) < 1e-12
    assert int(np.count_nonzero(np.triu(cover().interact, 1))) == 212


def test_endpoint_pose_is_a_witness_in_its_own_state() -> None:
    point = endpoint()
    cells = point["cells"]
    assert len(set(cells)) == 17
    violations = Problem(cover(), cells).violations(point["pose"])
    assert max(violations.values()) <= 1e-12
    names = dict(zip(point["labels"], (cover().names[c] for c in cells), strict=True))
    assert names[13] == "side-S1"  # the unique-state design moved square 13 into S1


def test_endpoint_sub_patterns_are_witnessed_before_any_search() -> None:
    witnessed, record = endpoint_witnesses(cover(), endpoint(), 3)
    expected = {
        canonical(mask_of(sub), cover().group)
        for arity in (1, 2, 3)
        for sub in itertools.combinations(endpoint()["cells"], arity)
    }
    assert record["passed"]
    assert witnessed == expected


def test_penalty_gradient_matches_central_differences() -> None:
    problem = Problem(cover(), (0, 4, 16, 18))
    rng = np.random.default_rng(5)
    z = problem.pack(problem.random_pose(rng)) + rng.normal(0.0, 0.05, 12 + 2 * problem.p)
    _, gradient = problem.penalty(z)
    step = 1e-6
    numeric = [
        (problem.penalty(z + step * unit)[0] - problem.penalty(z - step * unit)[0]) / (2 * step)
        for unit in np.eye(len(z))
    ]
    assert np.max(np.abs(np.array(numeric) - gradient)) < 1e-6


def test_touching_pairs_pass_and_the_crowded_triple_is_flagged() -> None:
    geometry = strip()
    for pair in ((0, 1), (1, 2)):
        verdict = search(geometry, pair, pattern_rng(3, mask_of(pair)), QUICK)
        assert verdict.feasible
        assert verdict.violation <= MARGIN
    triple = search(geometry, (0, 1, 2), pattern_rng(3, 7), QUICK)
    assert not triple.feasible
    assert triple.violation > 0.1


def test_sweep_is_deterministic_under_a_seed() -> None:
    first = sweep(strip(), max_arity=3, seed=11, budget=QUICK)
    second = sweep(strip(), max_arity=3, seed=11, budget=QUICK)
    for record in (first, second):
        for level in record["levels"].values():
            level.pop("seconds")
        record.pop("seconds")
    assert first == second
    assert first["flagged_masks"] == [0b111]
    rng_a, rng_b = pattern_rng(1, 0b10001), pattern_rng(1, 0b10001)
    a = search(cover(), (0, 4), rng_a, QUICK)
    b = search(cover(), (0, 4), rng_b, QUICK)
    assert np.array_equal(a.pose, b.pose)


def test_a_witnessed_pattern_is_never_flagged() -> None:
    record = sweep(strip(), max_arity=3, seed=11, budget=QUICK, witnessed={0b111})
    assert record["flagged"] == []
    assert [entry["indices"] for entry in record["false_flags"]] == [[0, 1, 2]]


def test_tight_endpoint_cluster_reaches_the_margin() -> None:
    rows = contact_clusters(endpoint(), 3)[0]
    record = tight_control(cover(), endpoint(), rows, seed=1, budget=QUICK)
    assert record["passed"]
    assert record["best_violation"] <= MARGIN


def test_witnesses_travel_under_d4() -> None:
    point = endpoint()
    rows = list(range(6))
    cells = tuple(point["cells"][row] for row in rows)
    for element, permutation in enumerate(cover().group):
        image_cells, image_pose = transform_pose(cover(), cells, point["pose"][rows], element)
        assert mask_of(image_cells) == image_mask(mask_of(cells), permutation)
        assert Problem(cover(), image_cells).violation(image_pose) <= 1e-12


def brute_force(
    group: tuple[tuple[int, ...], ...], size: int, flagged: list[int]
) -> tuple[int, int]:
    forbidden = [
        frozenset(permutation[c] for c in range(8) if mask >> c & 1)
        for mask in flagged
        for permutation in group
    ]
    alive = [
        frozenset(subset)
        for subset in itertools.combinations(range(8), size)
        if not any(pattern <= frozenset(subset) for pattern in forbidden)
    ]
    orbits = {
        min(tuple(sorted(permutation[c] for c in state)) for permutation in group)
        for state in alive
    }
    return len(alive), len(orbits)


def test_consumer_matches_brute_force_on_a_toy_cover() -> None:
    group = ring_group()
    for flagged in ([], [0b11], [0b11, 0b10100], [0b1001001]):
        record = consume(8, group, flagged, size=4)
        assert (record["surviving_states"], record["orbits"]) == brute_force(group, 4, flagged)
    # Burnside on the ring: (70 + 2 + 6 + 2 + 4 * 6) / 8 for identity, turns, reflections.
    assert consume(8, group, [], size=4)["orbits"] == 13
    order = greedy_order(8, group, [0b11, 0b10100], size=4)
    assert order[0]["removes"] >= order[-1]["removes"]


def test_consumer_without_flags_reproduces_the_h266_census() -> None:
    record = consume(24, cover().group, [], endpoint_state=mask_of(endpoint()["cells"]))
    assert record["states"] == 346104
    assert record["orbits"] == 43593
    assert record["endpoint_survives"]


def ring_classes(arity: int) -> list[int]:
    group = ring_group()
    return sorted(
        {canonical(mask_of(c), group) for c in itertools.combinations(range(8), arity)}
    )


def occurs_by_brute_force(
    group: tuple[tuple[int, ...], ...], size: int, flagged: list[int], mask: int
) -> bool:
    """Some state avoiding every flagged image holds some image of the class."""
    images = [image_mask(m, permutation) for m in flagged for permutation in group]
    for state in itertools.combinations(range(8), size):
        held = mask_of(state)
        if any(image & held == image for image in images):
            continue
        if any(image_mask(mask, p) & held == image_mask(mask, p) for p in group):
            return True
    return False


def test_restriction_matches_brute_force_and_goes_beyond_pruning_on_the_ring() -> None:
    group = ring_group()
    beyond = 0
    for size, flagged in ((4, [0b11]), (5, [0b10100]), (5, [0b11, 0b10100]), (4, [])):
        images = sorted({image for mask in flagged for image in orbit(mask, group)})
        alive = survivors(all_states(8, size), images)
        for arity in (2, 3, 4):
            classes = ring_classes(arity)
            occurring = occurring_classes(classes, alive)
            assert occurring == {
                m for m in classes if occurs_by_brute_force(group, size, flagged, m)
            }
            pruned, restricted, tested = split_classes(classes, images, alive)
            assert set(tested) == occurring
            assert sorted(pruned + restricted + tested) == classes
            beyond += len(restricted)
    # On an eight-cycle with adjacent pairs flagged, {0, 2, 5} in cycle order is
    # independent but in no independent four-set: the restriction is not just pruning.
    assert beyond > 0


def test_restriction_is_exact_for_the_consumer_on_the_ring() -> None:
    group = ring_group()
    for size, prior in ((4, [0b11]), (5, [0b10100]), (5, [])):
        images = sorted({image for mask in prior for image in orbit(mask, group)})
        alive = survivors(all_states(8, size), images)
        for arity in (2, 3, 4):
            candidates = split_classes(ring_classes(arity), images, None)[2]
            kept = sorted(occurring_classes(candidates, alive))
            for chosen in (candidates, candidates[::2], candidates[1::3]):
                full = consume(8, group, prior + chosen, size=size)
                restricted = consume(
                    8, group, prior + [m for m in chosen if m in kept], size=size
                )
                assert full["surviving_states"] == restricted["surviving_states"]
                assert full["orbits"] == restricted["orbits"]


def test_restricted_sweep_agrees_with_the_full_sweep_on_every_survivor() -> None:
    geometry = strip_with_roof()
    for size, skipped in ((4, 0), (5, 3)):
        full = sweep(geometry, max_arity=5, seed=11, budget=QUICK, size=size)
        cut = sweep(geometry, max_arity=5, seed=11, budget=QUICK, size=size, restrict_from=1)
        assert full["flagged_masks"] == cut["flagged_masks"] == [0b111]
        assert cut["restricted_out"] == skipped
        assert cut["levels"]["4"]["restricted_out"] == skipped
        assert cut["levels"]["4"]["searched"] == full["levels"]["4"]["searched"] - skipped
        assert cut["flagged"] == full["flagged"]
        for arity in ("1", "2", "3"):
            level = without_seconds(cut)["levels"][arity]
            assert level.pop("restricted_out") == 0
            assert level.pop("surviving_states_used") == (5 if size == 4 else 1)
            assert level == without_seconds(full)["levels"][arity]
        for flagged in (full["flagged_masks"], cut["flagged_masks"]):
            record = consume(5, geometry.group, flagged, size=size)
            assert record == consume(5, geometry.group, [0b111], size=size)


def test_default_sweep_records_nothing_new() -> None:
    record = sweep(strip(), max_arity=3, seed=11, budget=QUICK)
    assert set(record) == {
        "levels",
        "flagged",
        "flagged_masks",
        "false_flags",
        "complete",
        "seconds",
    }
    assert all(set(level) == LEVEL_KEYS for level in record["levels"].values())
    late = sweep(strip(), max_arity=3, seed=11, budget=QUICK, restrict_from=4)
    assert late.pop("restricted_out") == 0
    assert without_seconds(late) == without_seconds(record)


def test_count_only_matches_the_restricted_sweep() -> None:
    geometry = strip_with_roof()
    levels = count_classes(geometry, max_arity=5, flagged=[0b111], size=5)
    assert levels["4"] == {
        "classes": 5,
        "flags_below": 1,
        "surviving_states_used": 0,
        "pruned_as_supersets": 2,
        "restricted_out": 3,
        "in_survivors": 0,
        "in_survivors_by_missing_pairs": [],
        "flags_by_missing_pairs": [],
    }
    assert levels["3"]["flags_by_missing_pairs"] == [1]
    assert levels["3"]["in_survivors"] == levels["3"]["classes"]
    # A and E, and C and D, are the two pairs that do not interact.
    assert missing_pairs(geometry, 0b11111) == 2
    assert missing_pairs(geometry, 0b00111) == 0


def test_priority_subset_defers_the_least_crowded() -> None:
    geometry = strip_with_roof()
    record = sweep(
        geometry, max_arity=4, seed=11, budget=QUICK, size=4, restrict_from=4, max_missing=1
    )
    level = record["levels"]["4"]
    # The arity-4 classes in survivors are ABDE and BCDE, missing one pair each, and ACDE,
    # missing both A-E and C-D: only ACDE is deferred.
    assert [missing_pairs(geometry, m) for m in (0b11011, 0b11110, 0b11101)] == [1, 1, 2]
    assert level["deferred_by_missing_pairs"] == 1
    assert level["searched"] == 2
    with pytest.raises(ValueError, match="max_missing"):
        _ = sweep(geometry, max_arity=1, seed=11, budget=QUICK, max_missing=0)


def test_receipts_name_the_bytes_imported_not_the_file_at_write_time(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The provenance is read at import, so a receipt written after the file was edited on
    disk still names the bytes the run imported (the defect fixed in `1d8577bca`)."""
    imported = selector.PROVENANCE
    blob = git_blob(Path(selector.__file__).read_bytes())
    assert list(imported["files"].values()) == [blob]
    edited = tmp_path / "select_n17_sub_patterns.py"
    _ = edited.write_text("# edited on disk after the run imported the module\n")
    monkeypatch.setattr(selector, "__file__", str(edited))
    assert run(max_arity=1, tight_sizes=())["provenance"] == imported
    output = tmp_path / "count.json"
    assert main(["--count-only", "--max-arity", "1", "--output", str(output)]) == 0
    assert json.loads(output.read_text(encoding="utf-8"))["provenance"] == imported


def test_the_finish_places_what_the_short_search_leaves() -> None:
    # The endpoint's own state, warm started near its pose: every short attempt stalls
    # near 2e-3, and one long descent from the best of them places it exactly.
    point = endpoint()
    rng = np.random.default_rng(0)
    start = point["pose"].copy()
    start[:, :2] += rng.normal(0.0, 0.03, (17, 2))
    start[:, 2] += rng.normal(0.0, 0.05, 17)
    short = Budget(starts=1, hops=0, deep_starts=0, deep_hops=0, finish=False)
    cells = point["cells"]
    unfinished = search(cover(), cells, np.random.default_rng(1), short, [(0, start)])
    assert not unfinished.feasible
    assert unfinished.violation > 1e-4
    finished = search(
        cover(),
        cells,
        np.random.default_rng(1),
        replace(short, finish=True),
        [(0, start)],
    )
    assert finished.feasible
    assert finished.found_by == "finish"
    assert finished.violation <= MARGIN
    assert finished.attempts == unfinished.attempts + 1


def test_without_the_finish_the_search_never_descends_long(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[int] = []

    def counted(_problem: Any, pose: Any) -> Any:
        calls.append(1)
        return pose

    monkeypatch.setattr(selector, "finish", counted)
    off = replace(QUICK, finish=False)
    record = sweep(strip(), max_arity=3, seed=11, budget=off)
    assert record["flagged_masks"] == [0b111]
    assert calls == []
    _ = sweep(strip(), max_arity=3, seed=11, budget=replace(QUICK, finish=True))
    assert calls == [1]  # only the crowded triple is unplaced, and it is finished once


def test_a_recheck_keeps_the_crowded_triple_and_places_a_pair() -> None:
    kept = recheck_flag(strip(), 0b111, seed=1, budget=QUICK)
    assert kept["status"] == "still-flagged"
    assert kept["best_penetration"] > 0.1
    assert kept["sub_pattern_witnesses"] == 3  # AB, BC and AC, each placed
    placed = recheck_flag(strip(), 0b011, seed=1, budget=QUICK)
    assert placed["status"] == "placed"
    assert len(placed["pose"]) == 2


def test_the_vectorised_penalty_is_the_penalty() -> None:
    rng = np.random.default_rng(3)
    for cells in ((0, 4, 16, 18), (0, 5, 6, 10, 14, 16, 18, 17)):
        problem = Problem(cover(), cells)
        for _ in range(10):
            pose = problem.random_pose(rng)
            z = problem.pack(pose) + rng.normal(0.0, 0.05, 3 * problem.k + 2 * problem.p)
            value, gradient = problem.penalty(z)
            fast_value, fast_gradient = problem.penalty_vectorised(z)
            assert abs(fast_value - value) <= 1e-12 * max(1.0, value)
            assert np.max(np.abs(fast_gradient - gradient)) <= 1e-12 * max(
                1.0, float(np.max(np.abs(gradient)))
            )


def test_an_early_stop_ends_a_descent_only_once_it_is_placed() -> None:
    problem = Problem(strip(), (0, 1))
    start = problem.random_pose(np.random.default_rng(5))
    stopped = problem.descend(start, polish=False, early_stop=True)
    assert problem.violation(stopped) <= MARGIN
    crowded = Problem(strip(), (0, 1, 2))
    stalled = crowded.descend(crowded.random_pose(np.random.default_rng(5)), polish=False)
    early = crowded.descend(
        crowded.random_pose(np.random.default_rng(5)), polish=False, early_stop=True
    )
    assert np.array_equal(stalled, early)  # never negligible, so never stopped early


def test_the_witness_cache_changes_no_verdict() -> None:
    cache: dict[Any, Any] = {}
    plain = recheck_flag(strip(), 0b111, seed=1, budget=QUICK)
    first = recheck_flag(strip(), 0b111, seed=1, budget=QUICK, witness_cache=cache)
    second = recheck_flag(strip(), 0b111, seed=1, budget=QUICK, witness_cache=cache)
    for record in (first, second):
        assert record["status"] == plain["status"]
        assert record["best_penetration"] == plain["best_penetration"]
        assert record["pose"] == plain["pose"]
    assert second["sub_pattern_attempts"] == 0


@pytest.mark.parametrize("screen_deep_starts", [0, 4])
def test_a_full_search_resumed_from_the_screen_is_the_full_search(
    screen_deep_starts: int,
) -> None:
    screen = Budget(starts=4, hops=4, deep_starts=screen_deep_starts, deep_hops=4)
    full = Budget(starts=4, hops=4, deep_starts=12, deep_hops=8)
    cells = (0, 1, 2)
    scratch = search(strip(), cells, pattern_rng(1, 7), full)
    screened, checkpoint = selector.search_resumable(
        strip(), cells, pattern_rng(1, 7), screen, checkpoint_at=screen.deep_starts
    )
    assert not screened.feasible
    assert checkpoint is not None
    assert checkpoint.attempts == 8 + screen_deep_starts
    resumed, _ = selector.search_resumable(
        strip(), cells, pattern_rng(1, 7), full, resume=checkpoint
    )
    assert resumed.violation == scratch.violation
    assert resumed.attempts == scratch.attempts
    assert resumed.found_by == scratch.found_by
    assert resumed.components == scratch.components
    assert np.array_equal(resumed.pose, scratch.pose)


def test_a_checkpoint_resumes_only_its_own_pattern_seed_and_prefix() -> None:
    screen = Budget(starts=4, hops=4, deep_starts=4, deep_hops=4)
    full = Budget(starts=4, hops=4, deep_starts=12, deep_hops=8)
    _, checkpoint = selector.search_resumable(
        strip(), (0, 1, 2), pattern_rng(1, 7), screen, checkpoint_at=4
    )
    assert checkpoint is not None
    wrong = {
        "budget prefix": ((0, 1, 2), pattern_rng(1, 7), replace(full, hops=5), None),
        "finish": ((0, 1, 2), pattern_rng(1, 7), replace(full, finish=False), None),
        "seed": ((0, 1, 2), pattern_rng(2, 7), full, None),
        "pattern": ((0, 1), pattern_rng(1, 7), full, None),
        "warm starts": ((0, 1, 2), pattern_rng(1, 7), full, []),
        "deep starts": ((0, 1, 2), pattern_rng(1, 7), replace(full, deep_starts=3), None),
    }
    for cells, rng, budget, warm in wrong.values():
        with pytest.raises(ValueError, match="checkpoint"):
            _ = selector.search_resumable(strip(), cells, rng, budget, warm, resume=checkpoint)
    # The finish ends every sub-pattern search, so it decides the warm starts: it is prefix.
    assert selector.budget_prefix(full) != selector.budget_prefix(replace(full, finish=False))
    assert selector.budget_prefix(full) == selector.budget_prefix(
        replace(full, deep_starts=1, deep_hops=1, wide_centre=1.0, wide_angle=1.0)
    )


def test_a_placed_search_leaves_no_checkpoint() -> None:
    placed, checkpoint = selector.search_resumable(
        strip(), (0, 1), pattern_rng(1, 3), QUICK, checkpoint_at=QUICK.deep_starts
    )
    assert placed.feasible
    assert checkpoint is None


def test_a_recheck_resumed_from_the_screen_is_the_recheck_from_scratch() -> None:
    screen = Budget(starts=4, hops=4, deep_starts=4, deep_hops=4)
    full = Budget(starts=4, hops=4, deep_starts=12, deep_hops=8)
    scratch = recheck_flag(strip(), 0b111, seed=1, budget=full)
    screened = recheck_flag(strip(), 0b111, seed=1, budget=screen, checkpoint_at=4)
    checkpoint = screened.pop("checkpoint")
    assert checkpoint is not None
    assert len(checkpoint.templates) == 3  # the deep stage redraws warm starts
    resumed = recheck_flag(strip(), 0b111, seed=1, budget=full, resume=checkpoint)
    assert resumed["sub_pattern_attempts"] == 0
    assert scratch["sub_pattern_attempts"] > 0
    for record in (scratch, resumed):
        _ = record.pop("sub_pattern_attempts")
    assert resumed == scratch
