"""Target-blind controls for the bounded BC318 containment adapter."""

from __future__ import annotations

import copy
import json
import os
import subprocess
import time
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import cast

import pytest

import devtools.wall_owner_containment as containment
from cases.n11_five_dot_cover.independent_union import load_frozen_input
from devtools.owner_footprints import (
    HALF_CORE,
    OUTER_SIDE,
    Point,
    Polygon,
    endpoint_footprint,
    full_owner_direction_manifest,
    owner_branch_manifest,
)
from devtools.wall_owner_containment import (
    CLASS_IDS,
    RETAINED_ENDPOINT_BLOB,
    ContainmentDeadlineError,
    ContainmentError,
    WallClass,
    WallInput,
    count_tuple_dispositions,
    evaluate_relations,
    exact_containment,
    load_wall_input,
    normalise_convex_polygon,
    relation_sets,
    run_controls,
    validate_certificate_receipt,
    validate_frame_record,
    validate_output_path,
    validate_transport,
)
from devtools.wall_owner_footprints import (
    RetainedOwnerFrame,
    retained_owner_frames,
    support_rectangle,
)

F = Fraction
REPO = Path(__file__).parents[2]
ENDPOINT = REPO / (
    "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/"
    "exp-143-four-owner-footprint-cover.json"
)
REPLAY = REPO / (
    "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/"
    "exp-144-four-owner-endpoint-full-net-replay.json"
)
COVERAGE = REPO / (
    "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/"
    "exp-145-independent-five-dot-union.json"
)


def _rectangle(x0: int, y0: int, x1: int, y1: int) -> Polygon:
    return ((F(x0), F(y0)), (F(x1), F(y0)), (F(x1), F(y1)), (F(x0), F(y1)))


def _rotate(point: Point) -> Point:
    return F(3, 5) * point[0] - F(4, 5) * point[1], F(4, 5) * point[0] + F(3, 5) * point[1]


def test_exact_containment_preserves_direction_boundary_and_failure_witness() -> None:
    outer = _rectangle(0, 0, 3, 3)
    shared = _rectangle(0, 0, 2, 2)
    strict = _rectangle(1, 1, 2, 2)
    translated = _rectangle(4, 0, 7, 3)

    assert exact_containment(outer, outer).contained
    assert exact_containment(outer, shared).contained
    assert exact_containment(outer, strict).contained
    assert exact_containment(outer, tuple(reversed(shared))).contained
    assert not exact_containment(strict, outer).contained
    failure = exact_containment(outer, translated)
    assert not failure.contained
    assert failure.failure_vertex == (F(4), F(0))
    assert failure.failure_edge == ((F(3), F(0)), (F(3), F(3)))
    assert failure.failure_cross == F(-3)

    rotated_outer = tuple(map(_rotate, outer))
    rotated_strict = tuple(map(_rotate, strict))
    assert exact_containment(rotated_outer, rotated_strict).contained
    assert not exact_containment(rotated_strict, rotated_outer).contained

    nonconvex = ((F(0), F(0)), (F(2), F(0)), (F(1), F(1)), (F(2), F(2)), (F(0), F(2)))
    with pytest.raises(ContainmentError, match="convex boundary"):
        normalise_convex_polygon(nonconvex)
    star = (
        (F(0), F(0)),
        (F(3), F(2)),
        (F(-1), F(2)),
        (F(2), F(0)),
        (F(1), F(4)),
    )
    with pytest.raises(ContainmentError, match="every directed edge"):
        normalise_convex_polygon(star)


def test_cartesian_products_count_union_instead_of_per_coordinate_union() -> None:
    possible = (frozenset({0, 1, 2}),) * 4
    accepted = ((frozenset({0, 1}),) * 4, (frozenset({1, 2}),) * 4)
    counts = count_tuple_dispositions(possible, accepted, universe_size=4)
    assert (counts.impossible, counts.covered, counts.unresolved) == (175, 31, 50)
    assert counts.family_products == (16, 16)
    assert counts.overlap == 1
    direct = {
        item
        for item in __import__("itertools").product(range(4), repeat=4)
        if all(value in {0, 1, 2} for value in item)
        and (all(value in {0, 1} for value in item) or all(value in {1, 2} for value in item))
    }
    assert len(direct) == counts.covered
    with pytest.raises(ContainmentError, match="four possible-coordinate"):
        count_tuple_dispositions(possible[:3], accepted, universe_size=4)

    all_impossible = count_tuple_dispositions(
        (frozenset(),) * 4,
        ((frozenset(),) * 4, (frozenset(),) * 4),
        universe_size=4,
    )
    assert (all_impossible.impossible, all_impossible.covered, all_impossible.unresolved) == (
        256,
        0,
        0,
    )


def _old_classes() -> tuple[Polygon, ...]:
    manifest = full_owner_direction_manifest()
    return tuple(
        normalise_convex_polygon(
            endpoint_footprint(
                owner_class.mark,
                owner_class.sector,
                manifest.directions,
                half=HALF_CORE,
            )
        )
        for owner_class in owner_branch_manifest(manifest).classes
    )


def _synthetic_wall(*, impossible: frozenset[int] = frozenset()) -> WallInput:
    container = (
        (F(0), F(0)),
        (OUTER_SIDE, F(0)),
        (OUTER_SIDE, OUTER_SIDE),
        (F(0), OUTER_SIDE),
    )
    classes = tuple(
        WallClass(
            CLASS_IDS[index],
            old,
            "impossible" if index in impossible else "possible",
            None if index in impossible else container,
        )
        for index, old in enumerate(_old_classes())
    )
    return WallInput("synthetic", "commit", "blob", "constructor", classes)


def test_whole_certificate_transport_and_exact_128_slot_driver() -> None:
    source = load_frozen_input(ENDPOINT, RETAINED_ENDPOINT_BLOB)
    manifest = full_owner_direction_manifest()
    wall = _synthetic_wall(impossible=frozenset({3, 12}))
    transport = validate_transport(source, wall, manifest)
    rows = cast(
        list[dict[str, object]],
        transport["certificate_transports"],
    )
    assert [row["corner_permutation"] for row in rows] == [
        ["BL", "BR", "TL", "TR"],
        ["BR", "BL", "TR", "TL"],
        ["BL", "TL", "BR", "TR"],
        ["TL", "BL", "TR", "BR"],
    ]
    assert all(len(cast(list[object], row["orientation_bijection"])) == 361 for row in rows)

    relations, polygon_tests = evaluate_relations(
        source, wall, deadline=time.perf_counter() + 10
    )
    assert len(relations) == 128
    assert polygon_tests == 112
    impossible_rows = [row for row in relations if row["disposition"] == "impossible-class"]
    assert len(impossible_rows) == 16
    possible, accepted = relation_sets(relations, wall)
    assert all(3 not in row and 12 not in row for family in accepted for row in family)
    assert all(len(row) == 14 for row in possible)
    assert all(len(row) == 14 for family in accepted for row in family)
    with pytest.raises(ContainmentDeadlineError, match="128 slots"):
        evaluate_relations(source, wall, deadline=time.perf_counter() - 1)

    classes = list(wall.classes)
    classes[0] = replace(classes[0], old_endpoint=classes[1].old_endpoint)
    with pytest.raises(ContainmentError, match="base E differs"):
        validate_transport(source, replace(wall, classes=tuple(classes)), manifest)
    classes = list(wall.classes)
    classes[15] = replace(classes[15], old_endpoint=classes[14].old_endpoint)
    with pytest.raises(ContainmentError, match=r"S\(E\) differs"):
        validate_transport(source, replace(wall, classes=tuple(classes)), manifest)


def test_target_refuses_a_deadline_overrun_after_the_final_slot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = load_frozen_input(ENDPOINT, RETAINED_ENDPOINT_BLOB)
    wall = _synthetic_wall(impossible=frozenset(range(16)))
    rows = [
        {
            "family": family,
            "corner": corner,
            "class_index": class_index,
            "class_id": CLASS_IDS[class_index],
            "disposition": "impossible-class",
            "failure": None,
        }
        for family in range(2)
        for corner in ("BL", "BR", "TL", "TR")
        for class_index in range(16)
    ]

    monkeypatch.setattr(containment, "run_controls", lambda _manifest: ["controlled"])
    monkeypatch.setattr(
        containment,
        "validate_transport",
        lambda _source, _wall, _manifest: {"controlled": True},
    )

    def completed_rows(
        _source: object, _wall: object, *, deadline: float
    ) -> tuple[list[dict[str, object]], int]:
        assert deadline == 10
        return rows, 0

    monkeypatch.setattr(
        containment,
        "evaluate_relations",
        completed_rows,
    )
    clock = iter((0.0, 1.0, 11.0))
    monkeypatch.setattr(containment.time, "perf_counter", lambda: next(clock))
    with pytest.raises(ContainmentDeadlineError, match="completing receipt"):
        containment.run_target(
            source,
            wall,
            implementation_revision="revision",
            replay_source={},
            coverage_source={},
            deadline_seconds=10,
        )


def test_public_control_bundle_covers_oblique_transport_and_toy_counts() -> None:
    controls = run_controls(full_owner_direction_manifest())
    assert len(controls) == 4
    assert "175/31/50" in controls[-1]


def _empty_frame_record(frame: RetainedOwnerFrame) -> dict[str, object]:
    return {
        "ray": [str(frame.ray[0]), str(frame.ray[1])],
        "orientation_index": frame.orientation_index,
        "quarter_turn": frame.quarter_turn,
        "sources": [
            {"folded_index": source.folded_index, "reflected": source.reflected}
            for source in frame.sources
        ],
        "centre_dimension": -1,
        "centre_set": [],
        "disposition": "empty",
        "support_r": None,
        "support_jr": None,
        "common_rectangle": None,
    }


def _empty_wall_receipt(source_revision: str) -> dict[str, object]:
    manifest = full_owner_direction_manifest()
    branch = owner_branch_manifest(manifest)
    classes: list[dict[str, object]] = []
    for owner_class in branch.classes:
        frames = retained_owner_frames(owner_class, manifest)
        old = endpoint_footprint(
            owner_class.mark,
            owner_class.sector,
            manifest.directions,
            half=HALF_CORE,
        )
        classes.append(
            {
                "class_id": owner_class.class_id,
                "mark": [str(value) for value in owner_class.mark],
                "sector": owner_class.sector,
                "old_endpoint": [[str(x), str(y)] for x, y in old],
                "disposition": "impossible",
                "frames": [_empty_frame_record(frame) for frame in frames],
                "nonempty_frame_count": 0,
                "empty_frame_count": len(frames),
                "point_frame_count": 0,
                "segment_frame_count": 0,
                "wall_footprint": None,
                "old_endpoint_contained": False,
                "proper_inclusion": None,
            }
        )
    return {
        "schema": "wall-owner-footprints/v1",
        "status": "complete",
        "evidence_tier": "synthetic exact control",
        "source": {
            "git_commit": source_revision,
            "owner_module": "packing/devtools/owner_footprints.py",
        },
        "settings": {
            "outer_side": "96/25",
            "core_side": "9977/10000",
            "half_core": "9977/20000",
            "angle_limit": "207107/500000",
            "direction_steps": 180,
            "orientation_count": 361,
            "signed_ray_count": 1444,
            "class_count": 16,
            "boundary_policy": "retain nonempty point and segment centre sets",
        },
        "classes": classes,
        "summary": {
            "completed_classes": 16,
            "expected_classes": 16,
            "possible_classes": 0,
            "impossible_classes": 16,
            "enlarged_classes": 0,
            "equal_classes": 0,
            "wall_seconds": 0.0,
        },
        "error": None,
    }


def _git_env() -> dict[str, str]:
    env = os.environ.copy()
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(name, None)
    env.update(
        {
            "GIT_AUTHOR_NAME": "BC318 Control",
            "GIT_AUTHOR_EMAIL": "control@example.invalid",
            "GIT_COMMITTER_NAME": "BC318 Control",
            "GIT_COMMITTER_EMAIL": "control@example.invalid",
        }
    )
    return env


def _commit_receipt(repository: Path, document: dict[str, object]) -> tuple[Path, str]:
    receipt = repository / "wall.json"
    receipt.write_text(json.dumps(document) + "\n", encoding="utf-8")
    env = _git_env()
    if not (repository / ".git").exists():
        subprocess.run(("git", "init", "-q"), cwd=repository, env=env, check=True)
    subprocess.run(("git", "add", "wall.json"), cwd=repository, env=env, check=True)
    subprocess.run(
        ("git", "commit", "-q", "-m", "control"),
        cwd=repository,
        env=env,
        check=True,
    )
    blob = subprocess.run(
        ("git", "hash-object", "wall.json"),
        cwd=repository,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return receipt, blob


def test_wall_input_distinguishes_all_empty_and_refuses_partial_mutations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source_revision = "1" * 40
    document = _empty_wall_receipt(source_revision)
    receipt, blob = _commit_receipt(tmp_path, document)
    monkeypatch.chdir(tmp_path)
    loaded = load_wall_input(receipt, blob, expected_source=source_revision)
    assert len(loaded.classes) == 16
    assert all(item.disposition == "impossible" for item in loaded.classes)

    mutations = []
    partial = copy.deepcopy(document)
    cast(list[object], partial["classes"]).pop()
    mutations.append((partial, "sixteen classes"))
    missing_frame = copy.deepcopy(document)
    first = cast(dict[str, object], cast(list[object], missing_frame["classes"])[0])
    cast(list[object], first["frames"]).pop()
    mutations.append((missing_frame, "partial frame list"))
    wrong_class = copy.deepcopy(document)
    cast(dict[str, object], cast(list[object], wrong_class["classes"])[0])["class_id"] = "wrong"
    mutations.append((wrong_class, "class identity"))
    wrong_setting = copy.deepcopy(document)
    cast(dict[str, object], wrong_setting["settings"])["outer_side"] = "4"
    mutations.append((wrong_setting, "frozen settings"))
    absent_polygon = copy.deepcopy(document)
    first = cast(dict[str, object], cast(list[object], absent_polygon["classes"])[0])
    first["disposition"] = "possible"
    first["old_endpoint_contained"] = True
    first["proper_inclusion"] = False
    mutations.append((absent_polygon, "lacks a wall polygon"))

    for mutation, message in mutations:
        receipt, blob = _commit_receipt(tmp_path, mutation)
        with pytest.raises(ContainmentError, match=message):
            load_wall_input(receipt, blob, expected_source=source_revision)


def test_frame_validation_retains_point_and_segment_and_rejects_provenance() -> None:
    manifest = full_owner_direction_manifest()
    owner_class = owner_branch_manifest(manifest).classes[0]
    frame = retained_owner_frames(owner_class, manifest)[0]
    short_ray = (frame.ray[0] / 4, frame.ray[1] / 4)
    for centre_set, dimension in (
        (((F(1), F(1)),), 0),
        (((F(0), F(0)), short_ray), 1),
    ):
        rectangle, support_r, support_jr = support_rectangle(
            centre_set, frame.ray, half=HALF_CORE
        )
        record = _empty_frame_record(frame)
        record.update(
            {
                "centre_dimension": dimension,
                "centre_set": [[str(x), str(y)] for x, y in centre_set],
                "disposition": "allowed",
                "support_r": [str(value) for value in support_r],
                "support_jr": [str(value) for value in support_jr],
                "common_rectangle": [[str(x), str(y)] for x, y in rectangle],
            }
        )
        assert validate_frame_record(record, frame, label="control") == "allowed"

    duplicate = _empty_frame_record(frame)
    duplicate["sources"] = cast(list[object], duplicate["sources"]) * 2
    with pytest.raises(ContainmentError, match="generated frame provenance"):
        validate_frame_record(duplicate, frame, label="control")


def test_adopted_replay_and_coverage_bind_the_retained_endpoint() -> None:
    replay = validate_certificate_receipt(
        REPLAY, "e445cca80d95c77226cdf324414ab269152e26d0", kind="replay"
    )
    coverage = validate_certificate_receipt(
        COVERAGE, "4688678bfd4e64d9cb345b48f065c1c82bebdea0", kind="coverage"
    )
    assert replay["git_blob"] == "e445cca80d95c77226cdf324414ab269152e26d0"
    assert coverage["git_blob"] == "4688678bfd4e64d9cb345b48f065c1c82bebdea0"


def test_output_guard_requires_fresh_json_outside_code(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    source.write_text("{}\n", encoding="utf-8")
    assert validate_output_path(tmp_path / "fresh.json", tmp_path, (source,)) == (
        tmp_path / "fresh.json"
    )
    with pytest.raises(ContainmentError, match="overwrite"):
        validate_output_path(source, tmp_path, (source,))
    with pytest.raises(ContainmentError, match="project code"):
        validate_output_path(
            tmp_path / "packing" / "devtools" / "result.json", tmp_path, (source,)
        )
