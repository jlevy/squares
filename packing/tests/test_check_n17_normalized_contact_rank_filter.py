"""Synthetic finite ranks, exact incidence boundaries and fresh certificate checks."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import time
from fractions import Fraction as Q
from itertools import pairwise
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n17_normalized_contact_rank_filter as rank


def forest() -> list[rank.Clone]:
    x = [rank.Clone(i, i + 1, f"p:{i}:{i + 1}", None) for i in range(16)]
    order = list(range(0, 17, 2)) + list(range(1, 17, 2))
    y = [
        rank.Clone(a + 18, b + 18, f"p:{min(a, b)}:{max(a, b)}", None)
        for a, b in pairwise(order)
    ]
    return (
        x
        + y
        + [
            rank.Clone(0, 17, "w:L:0", "L"),
            rank.Clone(18, 35, "w:B:0", "B"),
            rank.Clone(36, 37, "w:R:1", "R"),
        ]
    )


def test_two_rooted_forests_and_side_column_give_35_common_witness() -> None:
    elements = forest()
    certificate = rank.search(elements, rank.Work(time.monotonic() + 10))
    assert certificate["kind"] == "survival"
    assert certificate["augmentations"] == 35
    assert rank.check_certificate(elements, certificate) == "survival"
    assert rank.graphic_rank(elements, set(range(35))) == 35
    assert rank.capacity_rank(elements, set(range(35))) == 35


def test_search_exchange_path_replaces_a_greedy_physical_clone(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Greedy clone0 pins x; clone1 with the same physical row pins y. Clone2
    # supplies x independently. Reaching rank2 requires replacing clone0.
    elements = [
        rank.Clone(0, 17, "same", "R"),
        rank.Clone(18, 35, "same", "R"),
        rank.Clone(0, 17, "other", "L"),
    ]
    monkeypatch.setattr(rank, "TARGET", 2)
    result = rank.search(elements, rank.Work(time.monotonic() + 10))
    assert result["kind"] == "survival"
    assert result["indices"] == [1, 2]
    assert rank.check_certificate(elements, result) == "survival"


def test_parallel_side_clones_have_graphic_rank_one() -> None:
    elements = [rank.Clone(36, 37, f"w:R:{i}", "R") for i in range(5)]
    assert rank.graphic_rank(elements, set(range(5))) == 1
    assert rank.capacity_rank(elements, set(range(5))) == 4


def test_clone_duplicates_and_four_wall_capacity_are_separate_constraints() -> None:
    elements = [rank.Clone(i, 17, f"w:L:{i}", "L") for i in range(5)]
    elements.append(rank.Clone(18, 35, "w:L:0", "L"))
    assert rank.capacity_rank(elements, {0, 1, 2, 3}) == 4
    assert rank.capacity_rank(elements, set(range(6))) == 4
    assert not rank.independent(elements, {0, 5}, graphic=False)


def test_disconnected_unpinned_component_cannot_supply_full_graphic_rank() -> None:
    elements = forest()[:32]
    assert rank.graphic_rank(elements, set(range(32))) == 32
    result = rank.search(elements, rank.Work(time.monotonic() + 10))
    assert result["kind"] == "rank_obstruction"
    assert rank.check_certificate(elements, result) == "rank_obstruction"


@pytest.mark.parametrize("change", ["rank", "subset", "duplicate", "bool", "survival"])
def test_fresh_checker_refuses_false_finite_certificate(change: str) -> None:
    elements = [rank.Clone(36, 37, "w:R:0", "R")]
    certificate: dict[str, Any] = {
        "kind": "rank_obstruction",
        "subset_A": [0],
        "rank_graph": 1,
        "rank_capacity_complement": 0,
        "rank_sum": 1,
    }
    if change == "rank":
        certificate["rank_sum"] = 0
    elif change == "subset":
        certificate["subset_A"] = [1]
    elif change == "duplicate":
        certificate["subset_A"] = [0, 0]
    elif change == "bool":
        certificate["rank_graph"] = True
    else:
        certificate = {"kind": "survival", "indices": [0]}
    with pytest.raises(ValueError, match=r"certificate|subset|witness"):
        rank.check_certificate(elements, certificate)


def test_closed_box_distance_equality_retained_and_strict_gap_removed() -> None:
    origin = (Q(0), Q(0), Q(0), Q(0))
    assert rank.pair_possible(origin, (Q(1), Q(1), Q(1), Q(1)))
    assert not rank.pair_possible(origin, (Q(1), Q(1), Q(1001, 1000), Q(1001, 1000)))


def test_moving_wall_interval_equality_and_side_clones() -> None:
    delta = (rank.U - rank.LOWER) / 2
    x = Q(3, 4) + delta
    boxes = [(x, x, Q(2), Q(2))] + [(Q(2), Q(2), Q(2), Q(2))] * 16
    assert any(e.physical == "w:L:0" for e in rank.ground_set(boxes))
    boxes[0] = (x + Q(1, 100000), x + Q(1, 100000), Q(2), Q(2))
    assert all(e.physical != "w:L:0" for e in rank.ground_set(boxes))
    boxes[0] = (rank.U - Q(1, 2), rank.U - Q(1, 2), Q(2), Q(2))
    right = [e for e in rank.ground_set(boxes) if e.physical == "w:R:0"]
    assert {(e.left, e.right) for e in right} == {(0, 17), (36, 37)}


def test_exact_named_d4_mask_transport() -> None:
    group = {"r0": list(range(24)), "f0": list(reversed(range(24)))}
    mask = (1 << 0) | (1 << 7)
    assert rank.images(mask, group) == {mask, (1 << 23) | (1 << 16)}


@pytest.mark.parametrize("tamper", ["distance", "names", "orbit"])
def test_partition_cannot_hide_an_orbit_by_changing_distance_metadata(tamper: str) -> None:
    endpoint = (1 << 17) - 1
    mask = endpoint ^ 1 ^ (1 << 17)
    names = [f"cell-{i}" for i in range(24)]
    row = {
        "mask": mask,
        "cells": [names[i] for i in range(24) if mask & (1 << i)],
        "orbit_size": 1,
        "distance": 2,
    }
    group = {"r0": list(range(24))}
    rank.named_row(row, names, group, {endpoint})
    if tamper == "distance":
        row["distance"] = 4
    elif tamper == "names":
        row["cells"] = list(reversed(row["cells"]))
    else:
        row["orbit_size"] = 8
    with pytest.raises(ValueError, match="join differs"):
        rank.named_row(row, names, group, {endpoint})


@pytest.mark.parametrize("value", ["1e999999999", "1.0", "01", "2/2", "1/0", True])
def test_bounded_canonical_parser_refuses_noncanonical_before_geometry(value: Any) -> None:
    with pytest.raises(ValueError, match="rational"):
        rank.rational(value)


def test_used_geometry_and_exchange_ceilings_are_incomplete(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with pytest.raises(rank.IncompleteError, match="bit ceiling"):
        rank.bounded(Q(1 << 4096))
    monkeypatch.setattr(rank, "EXCHANGE_STATE", 1)
    with pytest.raises(rank.IncompleteError, match="exchange"):
        rank.search(forest(), rank.Work(time.monotonic() + 10))
    with pytest.raises(rank.IncompleteError, match="wall"):
        rank.search(forest(), rank.Work(time.monotonic() - 1))


@pytest.mark.parametrize("text", ['{"x":1,"x":2}', '{"x":NaN}', '{"x":1e999999}'])
def test_duplicate_or_nonfinite_json_refused(text: str, tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text(text)
    with pytest.raises(ValueError, match=r"duplicate|number"):
        rank.read(path)


def test_accepted_partition_timing_metadata_float_is_not_geometry(tmp_path: Path) -> None:
    path = tmp_path / "timing.json"
    path.write_text('{"seconds":12.25}')
    assert rank.read(path)[1]["seconds"] == 12.25


def test_input_byte_ceiling(tmp_path: Path) -> None:
    path = tmp_path / "large.json"
    path.write_text('{"x":1}')
    with pytest.raises(rank.IncompleteError, match="byte ceiling"):
        rank.read(path, 3)


def fake_intake(_document: dict[str, Any]) -> tuple[list[Any], dict[str, bytes]]:
    return [(17, [(Q(2), Q(2), Q(2), Q(2))] * 17)], {}


def test_complete_generate_fresh_reconstructs_roster_without_rerunning_search(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(rank, "intake", fake_intake)
    document = {"schema": "explicit synthetic context"}
    certificate = rank.generate(document, time.monotonic() + 10)
    monkeypatch.setattr(
        rank, "search", lambda *_args: pytest.fail("fresh checker reran search")
    )
    fresh = rank.generate(document, time.monotonic() + 10, certificate)
    assert fresh["verification_passed"]
    assert rank.payload(fresh) == certificate
    assert not fresh["ordinary_assignment_exclusion_proved"]
    assert not fresh["global_nonexistence_proved"]
    changed = copy.deepcopy(certificate)
    changed["outcomes"][0]["mask"] = 18
    with pytest.raises(ValueError, match="order"):
        rank.generate(document, time.monotonic() + 10, changed)


def test_accepted_bytes_mutation_refuses(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    path = tmp_path / "premise.json"
    path.write_bytes(b"original")
    monkeypatch.setattr(rank, "intake", lambda _d: ([], {str(path): b"original"}))
    path.write_bytes(b"changed")
    with pytest.raises(ValueError, match="changed"):
        rank.generate({}, time.monotonic() + 10)


def test_one_valid_obstruction_does_not_complete_an_unresolved_selected_roster(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    states, _ = fake_intake({})
    monkeypatch.setattr(rank, "intake", lambda _d: ([*states, (18, states[0][1])], {}))
    proposals = iter(
        [
            {
                "kind": "rank_obstruction",
                "subset_A": list(range(272)),
                "rank_graph": 32,
                "rank_capacity_complement": 0,
                "rank_sum": 32,
            },
            {"kind": "unresolved"},
        ]
    )
    monkeypatch.setattr(rank, "search", lambda *_a: next(proposals))
    result = rank.generate({}, time.monotonic() + 10)
    assert result["counts"]["rank_obstruction"] == 1
    assert result["status"] == "unresolved"
    assert not result["criterion_met"]
    assert not result["complete_classification"]


def test_two_clean_cli_refusals_preserve_inputs_and_unique_outputs(tmp_path: Path) -> None:
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text(json.dumps({"schema": "foreign"}))
    for index in range(2):
        output = tmp_path / f"result-{index}.json"
        done = subprocess.run(
            [
                sys.executable,
                "-m",
                rank.__name__,
                "--descriptor",
                str(descriptor),
                "--output",
                str(output),
            ],
            check=False,
            timeout=10,
            capture_output=True,
        )
        assert done.returncode == 1, done.stderr
        result = json.loads(output.read_bytes())
        assert result["status"] == "refused"
        assert not result["ordinary_census_admission_proved"]
    assert descriptor.read_text() == '{"schema": "foreign"}'
