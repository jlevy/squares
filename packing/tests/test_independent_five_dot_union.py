"""Target-blind controls for the independent five-dot polygon-union audit."""

from __future__ import annotations

import json
import subprocess
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import cast

import pytest

import cases.n11_five_dot_cover.independent_union as audit
from cases.n11_five_dot_cover.independent_union import (
    AuditError,
    Direction,
    FrozenInput,
    UnionMeasure,
    _manifest_record,  # pyright: ignore[reportPrivateUsage]
    _parse_frozen_receipt,  # pyright: ignore[reportPrivateUsage]
    bind_clean_tracked_source,
    collision_polygon,
    container_rectangle,
    core_offsets,
    exact_union_area,
    full_direction_manifest,
    polygon_area,
    run_full_net,
    validate_output_path,
)

F = Fraction
type Point = tuple[Fraction, Fraction]
type Polygon = tuple[Point, ...]


def _rectangle(x0: Fraction, y0: Fraction, x1: Fraction, y1: Fraction) -> Polygon:
    return ((x0, y0), (x1, y0), (x1, y1), (x0, y1))


@pytest.mark.parametrize(
    ("polygons", "expected"),
    [
        ((_rectangle(F(0), F(0), F(2), F(2)),), F(4)),
        ((_rectangle(F(0), F(0), F(2), F(2)),) * 2, F(4)),
        (
            (
                _rectangle(F(0), F(0), F(3, 2), F(2)),
                _rectangle(F(1, 2), F(0), F(2), F(2)),
            ),
            F(4),
        ),
        (
            (
                _rectangle(F(0), F(0), F(1), F(2)),
                _rectangle(F(1), F(0), F(2), F(2)),
            ),
            F(4),
        ),
        (
            (
                _rectangle(F(0), F(0), F(2), F(2)),
                _rectangle(F(1, 2), F(1, 2), F(3, 2), F(3, 2)),
            ),
            F(4),
        ),
    ],
)
def test_exact_union_handles_full_duplicate_overlap_tangent_and_nested_polygons(
    polygons: tuple[Polygon, ...], expected: Fraction
) -> None:
    container = _rectangle(F(0), F(0), F(2), F(2))
    measure = exact_union_area(container, polygons, max_subsets=(1 << len(polygons)) - 1)
    assert measure.covered_area == expected
    assert measure.uncovered_area == 0


def test_exact_union_reports_a_positive_gap_and_mutation() -> None:
    container = _rectangle(F(0), F(0), F(2), F(2))
    covered = (_rectangle(F(0), F(0), F(1), F(2)), _rectangle(F(1), F(0), F(2), F(2)))
    mutated = (covered[0], _rectangle(F(6, 5), F(0), F(2), F(2)))
    assert exact_union_area(container, covered, max_subsets=3).uncovered_area == 0
    assert exact_union_area(container, mutated, max_subsets=3).uncovered_area == F(2, 5)


def test_exact_union_clips_an_oblique_known_area_and_tangent_completion() -> None:
    container = _rectangle(F(0), F(0), F(1), F(1))
    diamond = (
        (F(-1, 4), F(1, 2)),
        (F(1, 2), F(-1, 4)),
        (F(5, 4), F(1, 2)),
        (F(1, 2), F(5, 4)),
    )
    corners = (
        ((F(0), F(0)), (F(1, 4), F(0)), (F(0), F(1, 4))),
        ((F(1), F(0)), (F(1), F(1, 4)), (F(3, 4), F(0))),
        ((F(1), F(1)), (F(3, 4), F(1)), (F(1), F(3, 4))),
        ((F(0), F(1)), (F(0), F(3, 4)), (F(1, 4), F(1))),
    )
    clipped = exact_union_area(container, (diamond,), max_subsets=1)
    assert clipped.covered_area == F(7, 8)
    assert clipped.uncovered_area == F(1, 8)

    completed = exact_union_area(container, (diamond, *corners), max_subsets=31)
    assert completed.covered_area == completed.container_area == F(1)
    assert completed.nonempty_subsets == 5

    def rotate(polygon: Polygon) -> Polygon:
        return tuple((F(4, 5) * x - F(3, 5) * y, F(3, 5) * x + F(4, 5) * y) for x, y in polygon)

    rotated = exact_union_area(
        rotate(container),
        (rotate(diamond), *(rotate(corner) for corner in corners)),
        max_subsets=31,
    )
    assert rotated.covered_area == rotated.container_area == F(1)
    assert rotated.nonempty_subsets == 5


def test_physical_rotation_builds_the_expected_core_and_container() -> None:
    direction = Direction("three-four-five", F(4, 5), F(3, 5))
    offsets = core_offsets(F(1), direction)
    dot_cover = collision_polygon(((F(2), F(3)),), offsets)
    assert polygon_area(offsets) == polygon_area(dot_cover) == 1
    assert container_rectangle(F(4), F(1), direction) == _rectangle(
        F(7, 10), F(7, 10), F(33, 10), F(33, 10)
    )


def test_independent_manifest_is_unique_complete_and_exact() -> None:
    manifest = full_direction_manifest(F(1, 3), 180)
    assert len(manifest) == 361
    assert [entry.index for entry in manifest] == list(range(361))
    assert len({(entry.direction.cosine, entry.direction.sine) for entry in manifest}) == 361
    assert manifest[0].direction == Direction("owner-000", F(1), F(0))
    assert all(
        entry.direction.cosine * entry.direction.cosine
        + entry.direction.sine * entry.direction.sine
        == 1
        for entry in manifest
    )


def _synthetic_receipt() -> dict[str, object]:
    outer = F(96, 25)
    base = _rectangle(F(1, 10), F(1, 10), F(1, 5), F(1, 5))
    footprints = (
        base,
        _rectangle(outer - F(1, 5), F(1, 10), outer - F(1, 10), F(1, 5)),
        _rectangle(F(1, 10), outer - F(1, 5), F(1, 5), outer - F(1, 10)),
        _rectangle(outer - F(1, 5), outer - F(1, 5), outer - F(1, 10), outer - F(1, 10)),
    )
    manifest = full_direction_manifest(F(1, 3), 180)
    selected = (0, 45, 90, 135, 180)
    provenance = [
        _manifest_record(entry)
        for entry in manifest
        if any(source.folded_index in selected for source in entry.sources)
    ]
    dots = ((F(1), F(1)), (F(1), F(2)), (F(2), F(1)), (F(2), F(2)), (F(3), F(3)))
    return {
        "schema": "owner-footprint-cover/v1",
        "status": "complete",
        "settings": {
            "outer_side": "96/25",
            "square_side": "9977/10000",
            "folded_source_indices": list(selected),
            "selected_canonical_directions": len(provenance),
            "full_owner_orientation_count": 361,
            "owner_footprints_derived_from_full_manifest": True,
            "owner_count": 4,
            "residual_square_count": 7,
        },
        "class": {
            "id": "bottom-left:m1:j0",
            "mark": ["1/10", "1/10"],
            "owner_count": 4,
            "four_owner_map": "(x,y),(q-x,y),(x,q-y),(q-x,q-y)",
        },
        "direction_provenance": provenance,
        "arms": {
            "endpoint": {
                "footprint_union": [
                    [[str(x), str(y)] for x, y in polygon] for polygon in footprints
                ],
                "proposal": {
                    "converged": True,
                    "rationalised_total_mass": "5",
                    "rationalised_atoms": [[str(x), str(y), "1"] for x, y in dots],
                },
            }
        },
    }


def test_parser_checks_serialized_geometry_net_and_equal_positive_weights() -> None:
    receipt = _synthetic_receipt()
    source = _parse_frozen_receipt(receipt, "synthetic.json", "commit", "blob")
    assert len(source.directions) == 361
    assert len(source.footprints) == 4
    assert len(source.dots) == 5
    assert source.common_weight == 1

    unequal = cast(dict[str, object], json.loads(json.dumps(receipt)))
    arms = cast(dict[str, object], unequal["arms"])
    endpoint = cast(dict[str, object], arms["endpoint"])
    proposal = cast(dict[str, object], endpoint["proposal"])
    atoms = cast(list[list[str]], proposal["rationalised_atoms"])
    atoms[0][2] = "2"
    proposal["rationalised_total_mass"] = "6"
    with pytest.raises(AuditError, match="one positive common weight"):
        _parse_frozen_receipt(unequal, "synthetic.json", "commit", "blob")

    changed_net = cast(dict[str, object], json.loads(json.dumps(receipt)))
    directions = cast(list[dict[str, object]], changed_net["direction_provenance"])
    directions[1]["ux"] = "0"
    with pytest.raises(AuditError, match="disagrees"):
        _parse_frozen_receipt(changed_net, "synthetic.json", "commit", "blob")


def _git(directory: Path, *args: str) -> str:
    return subprocess.run(
        ("git", *args),
        cwd=directory,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def test_source_binding_rejects_outside_modified_and_staged_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    _git(repository, "init", "-q")
    _git(repository, "config", "user.email", "audit@example.invalid")
    _git(repository, "config", "user.name", "Audit")
    source = repository / "source.json"
    source.write_text("{}\n", encoding="utf-8")
    _git(repository, "add", "source.json")
    _git(repository, "commit", "-qm", "fixture")
    monkeypatch.chdir(repository)
    blob = _git(repository, "hash-object", "source.json")
    _, relative, _, observed = bind_clean_tracked_source(source, blob)
    assert relative == "source.json"
    assert observed == blob

    outside = tmp_path / "outside.json"
    outside.write_text("{}\n", encoding="utf-8")
    with pytest.raises(AuditError):
        bind_clean_tracked_source(outside, blob)
    source.write_text('{"modified": true}\n', encoding="utf-8")
    with pytest.raises(AuditError, match="modified or staged"):
        bind_clean_tracked_source(source, blob)
    _git(repository, "add", "source.json")
    with pytest.raises(AuditError, match="modified or staged"):
        bind_clean_tracked_source(source, blob)


def test_driver_records_an_incomplete_deadline_without_claim(tmp_path: Path) -> None:
    directions = tuple(entry.direction for entry in full_direction_manifest(F(1, 3), 180))
    source = FrozenInput(
        "synthetic.json",
        "commit",
        "blob",
        F(4),
        F(1),
        F(1, 3),
        1,
        (_rectangle(F(0), F(0), F(1, 10), F(1, 10)),) * 4,
        ((F(1), F(1)),) * 5,
        F(1),
        F(5),
        directions,
    )
    output = tmp_path / "partial.json"
    result = run_full_net(source, max_subsets=511, deadline_seconds=0, output=output)
    written = cast(dict[str, object], json.loads(output.read_text(encoding="utf-8")))
    assert result["status"] == written["status"] == "partial"
    assert result["outcome"] == written["outcome"] == "unresolved"
    assert cast(dict[str, object], result["summary"])["checked_directions"] == 0


def test_driver_preserves_checked_prefix_on_geometry_refusal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    directions = tuple(entry.direction for entry in full_direction_manifest(F(1, 3), 180))
    source = FrozenInput(
        "synthetic.json",
        "commit",
        "blob",
        F(4),
        F(1),
        F(1, 3),
        180,
        (_rectangle(F(0), F(0), F(1, 10), F(1, 10)),) * 4,
        ((F(1), F(1)),) * 5,
        F(1),
        F(5),
        directions,
    )
    calls = 0

    def controlled_measure(*_args: object, **_kwargs: object) -> UnionMeasure:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise AuditError("synthetic geometry refusal")
        return UnionMeasure(F(4), F(4), 1)

    monkeypatch.setattr(audit, "measure_direction", controlled_measure)
    result = run_full_net(
        source, max_subsets=511, deadline_seconds=10, output=tmp_path / "partial.json"
    )
    assert result["status"] == "partial"
    assert result["outcome"] == "unresolved"
    assert len(cast(list[object], result["directions"])) == 1
    first = cast(dict[str, object], cast(list[object], result["directions"])[0])
    assert isinstance(first["wall_seconds"], float)
    assert result["error"] == "synthetic geometry refusal"


def test_driver_refuses_duplicate_manifest_and_short_subset_guard(tmp_path: Path) -> None:
    directions = tuple(entry.direction for entry in full_direction_manifest(F(1, 3), 180))
    source = FrozenInput(
        "synthetic.json",
        "commit",
        "blob",
        F(4),
        F(1),
        F(1, 3),
        180,
        (_rectangle(F(0), F(0), F(1, 10), F(1, 10)),) * 4,
        ((F(1), F(1)),) * 5,
        F(1),
        F(5),
        directions,
    )
    with pytest.raises(AuditError, match="511 subsets"):
        run_full_net(
            source, max_subsets=510, deadline_seconds=10, output=tmp_path / "short.json"
        )
    geometric_aliases = (
        Direction("relabeled", directions[0].cosine, directions[0].sine),
        Direction("quarter-turned", -directions[0].sine, directions[0].cosine),
    )
    for index, alias in enumerate(geometric_aliases):
        duplicate = replace(source, directions=(directions[0], alias, *directions[2:]))
        with pytest.raises(AuditError, match="unique directions modulo quarter turns"):
            run_full_net(
                duplicate,
                max_subsets=511,
                deadline_seconds=10,
                output=tmp_path / f"duplicate-{index}.json",
            )


def test_output_cannot_overwrite_input_or_project_code(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    source.write_text("{}\n", encoding="utf-8")
    with pytest.raises(AuditError, match="may not overwrite"):
        validate_output_path(source, source, tmp_path)
    checker = Path(__file__).parents[1] / "cases" / "n11_five_dot_cover" / "result.json"
    with pytest.raises(AuditError, match="checker source"):
        validate_output_path(checker, source, Path(__file__).parents[2])
    existing = tmp_path / "existing.json"
    existing.write_text("{}\n", encoding="utf-8")
    with pytest.raises(AuditError, match="must be fresh"):
        validate_output_path(existing, source, Path(__file__).parents[2])


@pytest.mark.parametrize("deadline", ["nan", "inf", "-inf", "0"])
def test_main_refuses_nonfinite_or_nonpositive_deadline(tmp_path: Path, deadline: str) -> None:
    output = tmp_path / f"deadline-{deadline}.json"
    status = audit.main(
        [
            "pyproject.toml",
            "--expect-receipt-blob",
            "0" * 40,
            f"--deadline-seconds={deadline}",
            "--output",
            str(output),
        ]
    )
    written = cast(dict[str, object], json.loads(output.read_text(encoding="utf-8")))
    assert status == 2
    assert written["status"] == "partial"
    assert written["outcome"] == "unresolved"
    assert "execution guards" in cast(str, written["error"])
