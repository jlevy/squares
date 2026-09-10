"""Independent controls for the exact corner dual-salvage screen."""

from __future__ import annotations

import gzip
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

import pytest

import devtools.screen_corner_dual_salvage as salvage
from devtools.owner_footprints import owner_branch_manifest
from devtools.screen_corner_dual_salvage import (
    CORNER_NAMES,
    REPO,
    Screen,
    build_screen,
    screen_footprint,
    source_binding,
    strict_separation,
    summarize_records,
    verify_survivors,
    write_record_atomic,
)
from sqpack.fractional.ceiling import CeilingCertificate, Placement

SIDE = Fraction(96, 25)
B = Fraction(9977, 10000)


def _square(low: Fraction, high: Fraction) -> tuple[tuple[Fraction, Fraction], ...]:
    return ((low, low), (high, low), (high, high), (low, high))


def _source(*placements: Placement) -> CeilingCertificate:
    manifest = owner_branch_manifest()
    tangents = tuple(
        direction.uy / (1 + direction.ux) for direction in manifest.directions.directions[:2]
    )
    return CeilingCertificate(11, Fraction(191, 50), B, tangents, placements)


def _record(family: CeilingCertificate) -> dict[str, object]:
    record = family.to_record()
    record["total_weight"] = str(family.total_weight)
    record["provenance"] = {
        "verify_ceiling": {
            "proved": False,
            "failures": ["K3 total weight at least n"],
            "max_depth": "1",
            "vertices": 17,
            "decided_exactly": 3,
            "regime": "net",
            "symmetric_only": True,
        }
    }
    return record


def test_positive_gap_is_required_and_tangency_is_discarded() -> None:
    square = _square(Fraction(0), Fraction(1))
    separated = strict_separation(square, _square(Fraction(2), Fraction(3)))
    assert separated is not None
    assert separated.gap > 0
    tangent = ((Fraction(1), Fraction(1, 3)),)
    assert strict_separation(square, tangent) is None
    assert strict_separation(square, _square(Fraction(1, 2), Fraction(3, 2))) is None


def test_screen_recovers_all_weight_or_none_and_uses_literal_orientation() -> None:
    placements = (
        Placement(Fraction(0), Fraction(1), Fraction(1), Fraction(2, 3), B),
        Placement(Fraction(1, 10), Fraction(2), Fraction(2), Fraction(1, 3), B),
    )
    family = _source(*placements)
    far = ((Fraction(10), Fraction(10)),)
    all_survive = screen_footprint(
        family,
        far,
        class_id="far",
        corner="bottom-left",
        kind="point",
        source_placements=placements,
        direction_axes=frozenset(
            (placement.direction.ux, placement.direction.uy) for placement in placements
        ),
    )
    assert all_survive.total_weight == 1
    assert len(all_survive.survivors) == 2

    covered = screen_footprint(
        family,
        _square(Fraction(0), Fraction(4)),
        class_id="whole",
        corner="bottom-left",
        kind="container",
        source_placements=placements,
        direction_axes=frozenset(
            (placement.direction.ux, placement.direction.uy) for placement in placements
        ),
    )
    assert covered.total_weight == 0
    assert not covered.survivors

    literal = screen_footprint(
        family,
        far,
        class_id="literal",
        corner="bottom-left",
        kind="point",
        source_placements=placements,
        direction_axes=frozenset({_orientation_axis(placements[0])}),
    )
    assert tuple(entry.source_index for entry in literal.survivors) == (0,)

    quarter_turn = Placement(Fraction(1), Fraction(1), Fraction(1), Fraction(1), B)
    canonical = screen_footprint(
        _source(quarter_turn),
        far,
        class_id="quarter-turn",
        corner="bottom-left",
        kind="point",
        source_placements=(quarter_turn,),
        direction_axes=frozenset({(Fraction(1), Fraction(0))}),
    )
    assert len(canonical.survivors) == 1


def _orientation_axis(placement: Placement) -> tuple[Fraction, Fraction]:
    return placement.direction.ux, placement.direction.uy


def test_survivor_replay_rejects_duplicate_indices_and_modified_weights() -> None:
    source = (
        Placement(Fraction(0), Fraction(1), Fraction(1), Fraction(2, 3), B),
        Placement(Fraction(0), Fraction(2), Fraction(2), Fraction(1, 3), B),
    )
    good = [
        {"source_index": 0, "weight": "2/3"},
        {"source_index": 1, "weight": "1/3"},
    ]
    assert verify_survivors(good, source) == (3, Fraction(1))
    with pytest.raises(ValueError, match="repeats source index"):
        verify_survivors([good[0], good[0]], source)
    altered = [dict(good[0], weight="1/2")]
    with pytest.raises(ValueError, match="altered source weight"):
        verify_survivors(altered, source)


def test_build_screen_emits_one_and_four_corner_class_products() -> None:
    family = _source(
        Placement(Fraction(0), Fraction(1), Fraction(2), Fraction(1), B),
    )
    result = cast(
        dict[str, Any],
        build_screen(
            _record(family),
            source_identity={"git_blob": "control"},
            kinds=("point",),
            corner_counts=(1, 4),
        ),
    )
    assert result["owner_manifest"]["raw_classes_per_corner"] == 16
    assert len(result["one_corner"]) == 16
    assert result["four_corner"]["point"]["class_count"] == 65_536
    assert result["four_corner"]["point"]["unique_survivor_masks"] >= 1
    assert result["source"]["depth_receipt"]["derived_depth_bound"].startswith(
        "at most 1 by deletion"
    )


def test_source_identity_binds_clean_tracked_git_blob() -> None:
    relative = Path(
        "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/"
        "bc-232-leg-01-family.json"
    )
    source = REPO / relative
    expected = "8a0bf1a264a1361649bc0acd0f70907ba8125f2f"
    assert source_binding(source, expected)["git_blob"] == expected
    with pytest.raises(ValueError, match="expected Git blob"):
        source_binding(source, "0" * 40)


def test_source_depth_receipt_is_required() -> None:
    family = _source(
        Placement(Fraction(0), Fraction(1), Fraction(2), Fraction(1), B),
    )
    record = _record(family)
    del record["provenance"]
    with pytest.raises(TypeError, match="lacks provenance"):
        build_screen(
            json.loads(json.dumps(record)),
            source_identity={"git_blob": "control"},
            kinds=("point",),
            corner_counts=(1,),
        )


def test_joint_mask_mass_is_measured_once_per_unique_mask(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    family = _source(
        Placement(Fraction(0), Fraction(1), Fraction(2), Fraction(1), B),
    )
    screen = Screen("same", "corner", "point", ((Fraction(10), Fraction(10)),), 1, ())
    screens = dict.fromkeys(CORNER_NAMES, (screen, screen))
    calls = 0
    original = salvage.__dict__["_mask_mass"]

    def counted(mask: int, scaled: tuple[int, ...]) -> tuple[int, int]:
        nonlocal calls
        calls += 1
        return original(mask, scaled)

    monkeypatch.setattr(salvage, "_mask_mass", counted)
    joint_records = salvage.__dict__["_joint_records"]
    rows, unique = joint_records(screens, family)
    assert len(rows) == 16
    assert unique == 1
    assert calls == 1


def test_deterministic_gzip_output_is_atomic_and_refuses_overwrite(tmp_path: Path) -> None:
    first = tmp_path / "first.json.gz"
    second = tmp_path / "second.json.gz"
    record: dict[str, object] = {"exact": "2/3", "count": 7}
    write_record_atomic(first, record)
    write_record_atomic(second, record)
    assert first.read_bytes() == second.read_bytes()
    assert json.loads(gzip.decompress(first.read_bytes())) == record
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        write_record_atomic(first, record)


def test_exact_summaries_retain_positive_and_negative_controls() -> None:
    rows: list[dict[str, object]] = [
        {"class_id": "negative", "survivor_weight": "13/2", "obstructs": False},
        {"class_id": "positive", "survivor_weight": "21/2", "obstructs": True},
        {"class_id": "positive-tie", "survivor_weight": "21/2", "obstructs": True},
    ]
    summary = summarize_records(rows, class_field="class_id")
    assert summary["obstructed_count"] == 2
    assert summary["minimum_survivor_weight"] == "13/2"
    assert summary["minimum_attaining_classes"] == ["negative"]
    assert summary["maximum_survivor_weight"] == "21/2"
    assert summary["maximum_attaining_classes"] == ["positive", "positive-tie"]
