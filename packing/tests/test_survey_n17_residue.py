"""Controls for the n17 residue survey, a heuristic measurement and not a certificate."""

from __future__ import annotations

import itertools
import json
from dataclasses import replace
from functools import cache
from pathlib import Path

import numpy as np
import pytest
from numpy.typing import NDArray

from devtools import select_n17_sub_patterns as selector
from devtools import survey_n17_residue as survey

QUICK = selector.Budget(starts=4, hops=4, deep_starts=4, deep_hops=4, finish=False)


def box(x0: float, x1: float, y0: float, y1: float) -> np.ndarray:
    return np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])


@cache
def strip_with_roof() -> selector.Geometry:
    """Three cells on the bottom wall that never fit together, and one above each end.

    Each adjacent pair on the wall fits only touching; with four-cell states, exactly the
    two holding all three wall cells fail, and their minimal failing pattern is the three.
    """
    return selector.make_geometry(
        [
            box(0.5, 0.7, 0.5, 0.6),
            box(1.1, 1.5, 0.5, 0.6),
            box(1.9, 2.1, 0.5, 0.6),
            box(0.5, 0.7, 1.6, 1.7),
            box(1.9, 2.1, 1.6, 1.7),
        ],
        ["side-A", "side-B", "side-C", "interior-D", "interior-E"],
    )


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


def test_survivor_enumeration_matches_brute_force_on_the_ring() -> None:
    group = ring_group()
    for size, flags in ((4, []), (4, [0b11]), (5, [0b10100]), (4, [0b11, 0b10100])):
        alive, representatives = survey.surviving_orbits(8, group, flags, size)
        forbidden = [selector.image_mask(m, p) for m in flags for p in group]
        expected_states = [
            selector.mask_of(c)
            for c in itertools.combinations(range(8), size)
            if not any(f & selector.mask_of(c) == f for f in forbidden)
        ]
        expected = sorted(
            {min(selector.image_mask(s, p) for p in group) for s in expected_states}
        )
        assert sorted(int(s) for s in alive) == sorted(expected_states)
        assert representatives == expected


def test_survivor_enumeration_reproduces_the_arity8_count() -> None:
    geometry = selector.cover_geometry()
    path = survey.REPO / survey.ARITY8
    flags = selector.receipt_flags(path, geometry, selector.DEFAULT_DESIGN)
    endpoint = selector.endpoint_pose()
    pop = survey.population(
        geometry, flags, selector.TARGET, selector.mask_of(endpoint["cells"])
    )
    assert len(pop.representatives) == survey.EXPECTED_ORBITS["arity8"]
    assert int(pop.alive.size) == 17636
    assert pop.strata[survey.ENDPOINT_STRATUM] == [
        selector.canonical(selector.mask_of(endpoint["cells"]), geometry.group)
    ]
    representative, record, _ = survey.endpoint_check(geometry, endpoint)
    assert representative in pop.features
    assert record["violation_of_carried_pose"] <= 1e-12


def test_sample_is_deterministic_and_covers_every_stratum() -> None:
    strata = {"a": list(range(50)), "b": list(range(100, 110)), "c": [200]}
    first = survey.draw_sample(strata, 8, 3)
    assert first == survey.draw_sample(strata, 8, 3)
    allocation, drawn = first
    assert sum(allocation.values()) == 8
    assert min(allocation.values()) >= 1
    assert allocation["a"] > allocation["b"]
    for key, mask in drawn:
        assert mask in strata[key]
    assert len({mask for _, mask in drawn}) == 8
    seeds = {tuple(survey.draw_sample(strata, 8, seed)[1]) for seed in range(6)}
    assert len(seeds) > 1
    everything = survey.draw_sample(strata, 100, 3)[1]
    assert sorted(mask for _, mask in everything) == sorted(
        m for v in strata.values() for m in v
    )


def test_a_census_estimates_exactly() -> None:
    sizes = {"a": 3, "b": 2}
    estimate = survey.stratified_estimate(sizes, {"a": [1.0, 0.0, 1.0], "b": [1.0, 1.0]})
    assert estimate["total"] == 4.0
    assert estimate["se"] == 0.0


def test_tiny_synthetic_survey_finds_the_crowded_triple() -> None:
    geometry = strip_with_roof()
    endpoint_state = 0b11110  # B, C, D, E: fits
    knowledge = survey.Knowledge(
        geometry,
        4,
        (survey.Rule(max_arity=2, restrict_from=None, max_missing=None, flags=()),),
        {},
    )
    plan = survey.Plan(
        geometry=geometry,
        knowledge=knowledge,
        seed=1,
        full=survey.Effort(QUICK, 1),
        reduce=survey.Efforts(survey.Effort(QUICK, 1), survey.Effort(QUICK, 1)),
        confirm=survey.Effort(QUICK, 1),
        max_steps=10,
    )
    pop = survey.population(geometry, [], 4, endpoint_state)
    assert len(pop.representatives) == 5
    random_strata = {k: v for k, v in pop.strata.items() if k != survey.ENDPOINT_STRATUM}
    _, drawn = survey.draw_sample(random_strata, 10, 1)
    drawn = [(survey.ENDPOINT_STRATUM, endpoint_state), *drawn]
    receipt = survey.run_survey(
        plan, pop, drawn, workers=1, timeout=None, header={}, output=None, size=4
    )
    assert receipt["complete"]
    assert [c["full"]["placed"] for c in receipt["controls"]] == [True]
    by_mask = {record["mask"]: record for record in receipt["states"]}
    for mask, record in by_mask.items():
        crowded = mask & 0b111 == 0b111
        assert record["full"]["placed"] is not crowded
        if crowded:
            minimal = record["minimal"]
            assert minimal["cells"] == ["side-A", "side-B", "side-C"]
            assert minimal["irreducible"]
            assert minimal["class"] == "new"
            assert not minimal["confirm"]["placed"]
            assert minimal["decided_by"].get("selector-placed", 0) >= 1
        else:
            assert record["full"]["best_penetration"] <= selector.MARGIN
    assert receipt["placed_states"] != []  # off-control placements are reported
    distributions = receipt["distributions"]
    assert distributions["minimal_arity"]["sample"] == {"3": 2}
    assert distributions["minimal_class"]["new_share"] == 1.0
    found = receipt["found_classes"]
    assert found["distinct"] == 1
    assert found["classes"][0]["removes_states"] == 2
    assert found["survivors_if_new_classes_certified"]["states"] == 3


def test_knowledge_reads_the_selector_receipts() -> None:
    geometry = selector.cover_geometry()
    knowledge = survey.load_knowledge(
        geometry, selector.DEFAULT_DESIGN, survey.KNOWLEDGE_RECEIPTS, survey.REPO, 17
    )
    flags = sorted(knowledge.flags)
    assert len(flags) == 90
    flag = flags[0]
    assert knowledge.status(flag) == "flagged"
    endpoint = selector.endpoint_pose()["cells"]
    pair = next(p for p in itertools.combinations(endpoint, 2) if geometry.interact[p])
    assert knowledge.status(selector.mask_of(pair)) == "placed"
    outside = next(c for c in range(24) if not flag >> c & 1 and geometry.interact[c].any())
    assert knowledge.status(flag | 1 << outside) == "holds-flag"
    assert knowledge.status(selector.mask_of(endpoint)) == "unknown"
    assert knowledge.status(selector.mask_of((0, 1))) == "unknown"  # disconnected
    assert Path(survey.REPO / survey.ARITY7).is_file()


def test_weighted_allocation_oversamples_the_endpoint_neighbourhood() -> None:
    sizes = {"c4/i4/d2": 10, "c4/i4/d>=8": 100}
    plain = survey.allocate(sizes, 20)
    weighted = survey.allocate(sizes, 20, {key: survey.weight_of(key) for key in sizes})
    assert sum(weighted.values()) == 20
    assert weighted["c4/i4/d2"] > plain["c4/i4/d2"]
    assert survey.distance(0b1011, [0b0111, 0b1110000]) == 2
    assert survey.stratum_of({"corner": 4, "side": 9, "interior": 4}, 10) == "c4/i4/d>=8"


def test_the_frame_keeps_one_distance_and_the_control() -> None:
    """`frame_of` keeps the orbits at the given distance and the endpoint's control, with
    the survivors and flags whole; `draw_frame` with sample 0 takes every frame orbit."""
    features = {
        mask: {"distance": apart, "stratum": key}
        for mask, apart, key in (
            (1, 0, survey.ENDPOINT_STRATUM),
            (2, 2, "c4/i4/d2"),
            (3, 2, "c3/i4/d2"),
            (4, 2, "c3/i4/d2"),
            (5, 4, "c4/i4/d4"),
            (6, 8, "c4/i4/d>=8"),
        )
    }
    strata: dict[str, list[int]] = {}
    for mask, feature in features.items():
        strata.setdefault(feature["stratum"], []).append(mask)
    alive = np.arange(10, dtype=np.int64)
    pop = survey.Population([7], alive, sorted(features), features, strata)
    assert survey.frame_of(pop, None) is pop
    frame = survey.frame_of(pop, 2)
    assert frame.representatives == [1, 2, 3, 4]
    assert frame.strata == {
        survey.ENDPOINT_STRATUM: [1],
        "c4/i4/d2": [2],
        "c3/i4/d2": [3, 4],
    }
    assert frame.alive is alive
    assert frame.flags == [7]
    allocation, drawn = survey.draw_frame(frame, 0, 1)
    assert allocation == {"c3/i4/d2": 2, "c4/i4/d2": 1}
    assert sorted(mask for _, mask in drawn) == [2, 3, 4]
    assert len(survey.draw_frame(frame, 2, 1)[1]) == 2
    with pytest.raises(ValueError, match="every orbit"):
        _ = survey.draw_frame(frame, -1, 1)
    with pytest.raises(ValueError, match="no surviving orbit"):
        _ = survey.draw_frame(survey.frame_of(pop, 6), 0, 1)


def test_distance_two_with_sample_zero_is_every_one_cell_move(tmp_path: Path) -> None:
    """Under the arity-8 flags, 95 surviving orbits lie at distance 2 from the endpoint's
    orbit (H-273's frame); `--distance 2 --sample 0` draws all of them after the control."""
    output = tmp_path / "strata.json"
    command = ["--flag-set", "arity8", "--distance", "2", "--sample", "0", "--strata-only"]
    assert survey.main([*command, "--output", str(output)]) == 0
    header = json.loads(output.read_text(encoding="utf-8"))
    assert header["population"]["surviving_orbits"] == survey.EXPECTED_ORBITS["arity8"]
    assert header["population"]["frame"] == {"distance": 2, "orbits": 95, "drawn": 95}
    assert header["parameters"]["distance"] == 2
    drawn = header["drawn"]
    assert drawn[0]["stratum"] == survey.ENDPOINT_STRATUM
    assert len({row["mask"] for row in drawn[1:]}) == 95
    assert all(row["stratum"].endswith("/d2") for row in drawn[1:])


def test_shards_partition_the_draw_in_mask_order() -> None:
    """`shard_of` splits a draw into N interleaved parts by mask that cover it exactly once,
    and refuses a malformed or out-of-range shard."""
    drawn = [("a", 9), ("b", 3), ("a", 7), ("c", 1), ("b", 5)]
    parts = [survey.shard_of(drawn, f"{k}/2") for k in range(2)]
    assert parts == [[("c", 1), ("b", 5), ("a", 9)], [("b", 3), ("a", 7)]]
    assert sorted(item for part in parts for item in part) == sorted(drawn)
    assert survey.shard_of(drawn, None) is drawn
    for bad in ("2/2", "1", "a/b", "-1/2"):
        with pytest.raises(ValueError, match="shard"):
            _ = survey.shard_of(drawn, bad)


def test_ten_shards_cover_the_distance_two_frame_once(tmp_path: Path) -> None:
    """H-273's 95-orbit frame in ten shards: each places the control first, and the shards
    are disjoint and together hold all 95 orbits."""
    survey.clear_population_cache()
    seen: list[int] = []
    for k in range(10):
        output = tmp_path / f"shard-{k}.json"
        command = ["--flag-set", "arity8", "--distance", "2", "--sample", "0", "--strata-only"]
        assert survey.main([*command, "--shard", f"{k}/10", "--output", str(output)]) == 0
        header = json.loads(output.read_text(encoding="utf-8"))
        assert header["parameters"]["shard"] == f"{k}/10"
        drawn = header["drawn"]
        assert drawn[0]["stratum"] == survey.ENDPOINT_STRATUM
        assert header["population"]["frame"]["drawn"] == len(drawn) - 1 in (9, 10)
        seen.extend(row["mask"] for row in drawn[1:])
    assert len(seen) == len(set(seen)) == 95


def ring_geometry() -> selector.Geometry:
    return selector.make_geometry(
        [box(float(k), float(k) + 0.2, 0.0, 0.2) for k in range(8)],
        [f"corner-{k}" for k in range(8)],
        group=list(ring_group()),
    )


def assert_populations_equal(first: survey.Population, second: survey.Population) -> None:
    assert first.flags == second.flags
    np.testing.assert_array_equal(first.alive, second.alive)
    assert first.representatives == second.representatives
    assert first.features == second.features
    assert first.strata == second.strata


@pytest.mark.parametrize(("size", "flags"), [(4, []), (4, [0b11]), (5, [0b10100])])
def test_population_cache_matches_the_complete_ring_oracle(size: int, flags: list[int]) -> None:
    survey.clear_population_cache()
    geometry = ring_geometry()
    result = survey.population(geometry, flags, size, None)
    forbidden = {
        selector.image_mask(flag, permutation)
        for flag in flags
        for permutation in geometry.group
    }
    alive = [
        selector.mask_of(cells)
        for cells in itertools.combinations(range(8), size)
        if not any(flag & selector.mask_of(cells) == flag for flag in forbidden)
    ]
    representatives = sorted(
        {
            min(selector.image_mask(mask, permutation) for permutation in geometry.group)
            for mask in alive
        }
    )
    assert sorted(int(mask) for mask in result.alive) == sorted(alive)
    assert result.representatives == representatives
    assert sorted(mask for masks in result.strata.values() for mask in masks) == representatives
    assert set(result.features) == set(representatives)
    assert result.flags == flags


@pytest.mark.parametrize("changed", ["names", "group", "flags", "size", "endpoint"])
def test_population_cache_rechecks_every_combinatorial_input(
    monkeypatch: pytest.MonkeyPatch, changed: str
) -> None:
    survey.clear_population_cache()
    geometry, flags, size, endpoint = ring_geometry(), [], 4, 0b1111
    uncached = survey.surviving_orbits
    calls = 0

    def counted(
        cells: int, group: tuple[tuple[int, ...], ...], flags: list[int], size: int
    ) -> tuple[NDArray[np.int64], list[int]]:
        nonlocal calls
        calls += 1
        return uncached(cells, group, flags, size)

    monkeypatch.setattr(survey, "surviving_orbits", counted)
    survey.population(geometry, flags, size, endpoint)
    if changed == "names":
        geometry = replace(geometry, names=("interior-0", *geometry.names[1:]))
    elif changed == "group":
        geometry = replace(geometry, group=(tuple(range(8)),))
    elif changed == "flags":
        flags = [0b11]
    elif changed == "size":
        size = 5
    else:
        endpoint = 0b10101010
    result = survey.population(geometry, flags, size, endpoint)
    repeated = survey.population(geometry, flags, size, endpoint)
    assert calls == 2
    assert_populations_equal(result, repeated)
    survey.clear_population_cache()
    fresh = survey.population(geometry, flags, size, endpoint)
    assert calls == 3
    assert_populations_equal(result, fresh)


def test_population_cache_detaches_every_mutable_payload() -> None:
    survey.clear_population_cache()
    geometry, flags = ring_geometry(), []
    first = survey.population(geometry, flags, 4, 0b1111)
    expected = survey.population(geometry, flags, 4, 0b1111)
    first.flags.append(-1)
    first.alive[:] = -1
    first.representatives.append(-1)
    mask = next(iter(first.features))
    first.features[mask]["composition"]["corner"] = -1
    first.features[mask]["distance"] = -1
    next(iter(first.strata.values())).append(-1)
    assert flags == []
    assert_populations_equal(survey.population(geometry, flags, 4, 0b1111), expected)


def test_population_cache_normalizes_flags_without_changing_the_public_roster(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    survey.clear_population_cache()
    geometry = ring_geometry()
    uncached = survey.surviving_orbits
    calls = 0

    def counted(
        cells: int, group: tuple[tuple[int, ...], ...], flags: list[int], size: int
    ) -> tuple[NDArray[np.int64], list[int]]:
        nonlocal calls
        calls += 1
        return uncached(cells, group, flags, size)

    monkeypatch.setattr(survey, "surviving_orbits", counted)
    first_flags = [0b10100, 0b11, 0b10100]
    second_flags = [0b11, 0b10100]
    first = survey.population(geometry, first_flags, 4, None)
    second = survey.population(geometry, second_flags, 4, None)
    assert calls == 1
    assert first.flags == first_flags
    assert second.flags == second_flags
    np.testing.assert_array_equal(first.alive, second.alive)
    assert first.representatives == second.representatives
    assert first.features == second.features
    assert first.strata == second.strata
