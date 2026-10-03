"""Controls for the n17 residue survey, a heuristic measurement and not a certificate."""

from __future__ import annotations

import itertools
from functools import cache
from pathlib import Path

import numpy as np

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
