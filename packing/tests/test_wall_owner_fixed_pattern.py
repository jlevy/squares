"""Synthetic exact controls for the fixed-pattern discriminator."""

from __future__ import annotations

import json
import time
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

import devtools.wall_owner_fixed_pattern as fixed_pattern
from cases.n11_five_dot_cover.independent_union import (
    Direction,
    FrozenInput,
    full_direction_manifest,
)
from devtools.owner_footprints import ANGLE_LIMIT, CORE_SIDE, OUTER_SIDE, Polygon
from devtools.wall_owner_containment import CLASS_IDS, WallClass, WallInput
from devtools.wall_owner_fixed_pattern import (
    CandidateCheck,
    FixedPatternError,
    FixedPatternResult,
    MaskWitness,
    SourceReferences,
    WitnessBank,
    build_witness_bank,
    check_one_candidate,
    component_means,
    core_disjoint_from_polygon,
    fixed_seed_indices,
    mask_product_bits,
    merge_mask_product,
    ordinal_tuple,
    parse_completed_containment,
    run_fixed_pattern,
    select_first_candidate,
    selected_wall_footprints,
    strict_dot_free,
    tuple_ordinal,
    witness_masks,
)

F = Fraction


def _rectangle(
    x0: int | Fraction,
    y0: int | Fraction,
    x1: int | Fraction,
    y1: int | Fraction,
) -> Polygon:
    return ((F(x0), F(y0)), (F(x1), F(y0)), (F(x1), F(y1)), (F(x0), F(y1)))


def _source() -> FrozenInput:
    directions = tuple(item.direction for item in full_direction_manifest(ANGLE_LIMIT, 180))
    return FrozenInput(
        "synthetic-endpoint.json",
        "commit",
        "blob",
        F(4),
        F(1),
        ANGLE_LIMIT,
        180,
        (_rectangle(0, 0, F(1, 4), F(1, 4)),) * 4,
        (
            (F(1), F(1)),
            (F(3, 2), F(1)),
            (F(2), F(1)),
            (F(5, 2), F(1)),
            (F(3), F(1)),
        ),
        F(1),
        F(5),
        directions,
    )


def _wall() -> WallInput:
    polygon = _rectangle(0, 0, F(1, 4), F(1, 4))
    classes = tuple(WallClass(class_id, polygon, "possible", polygon) for class_id in CLASS_IDS)
    return WallInput("synthetic-wall.json", "commit", "blob", "constructor", classes)


def test_thin_strip_has_a_rational_interior_component_mean() -> None:
    container = _rectangle(0, 0, 4, 1)
    obstacle = _rectangle(0, 0, 4, F(7, 8))
    centres = component_means(container, (obstacle,))
    assert centres == ((F(2), F(15, 16)),)


def test_strict_dot_and_owner_replays_reject_all_three_boundaries() -> None:
    direction = Direction("axis", F(1), F(0))
    assert strict_dot_free(
        (F(1), F(2)),
        direction,
        outer_side=F(4),
        core_side=F(1),
        dots=((F(3), F(3)),),
    )
    assert not strict_dot_free(
        (F(1, 2), F(2)),
        direction,
        outer_side=F(4),
        core_side=F(1),
        dots=((F(3), F(3)),),
    )
    assert not strict_dot_free(
        (F(1), F(2)),
        direction,
        outer_side=F(4),
        core_side=F(1),
        dots=((F(3, 2), F(2)),),
    )

    owner = _rectangle(2, 2, 3, 3)
    assert not core_disjoint_from_polygon((F(3, 2), F(5, 2)), direction, F(1), owner)
    assert core_disjoint_from_polygon((F(7, 5), F(5, 2)), direction, F(1), owner)


def test_mask_products_deduplicate_overlap_and_guard_certificates() -> None:
    masks = (0b11, 0b11, 0b11, 0b11)
    first = mask_product_bits(masks)
    assert first.bit_count() == 16
    second = mask_product_bits((0b110, 0b110, 0b110, 0b110))
    assert second.bit_count() == 16
    assert (first | second).bit_count() == 31
    assert mask_product_bits((0b11, 0b11, 0, 0b11)) == 0

    merged, added = merge_mask_product(0, masks, frozenset())
    assert merged == first
    assert added == 16
    merged_again, added_again = merge_mask_product(merged, masks, frozenset())
    assert merged_again == merged
    assert added_again == 0
    with pytest.raises(FixedPatternError, match="already-certified"):
        merge_mask_product(0, masks, frozenset({(0, 0, 0, 0)}))

    for values in ((0, 0, 0, 0), (0, 0, 0, 1), (15, 15, 15, 15)):
        assert ordinal_tuple(tuple_ordinal(values)) == values


def test_nine_seed_manifest_and_independent_sat_masks_are_exact() -> None:
    source = _source()
    indices = fixed_seed_indices(source)
    assert len(indices) == 9
    assert indices == tuple(sorted(indices))
    masks = witness_masks((F(2), F(5, 2)), source.directions[0], source=source, wall=_wall())
    assert masks == ((1 << 16) - 1,) * 4


def test_seed_deadline_preserves_a_typed_empty_prefix() -> None:
    source = _source()
    result = build_witness_bank(
        source,
        _wall(),
        frozenset(),
        seed_deadline=time.perf_counter() - 1,
        total_deadline=time.perf_counter() + 10,
    )
    assert result.status == "partial"
    assert result.checked_seed_indices == ()
    assert result.failure_bits == 0
    assert result.error == "seed-stage deadline reached"


def test_one_candidate_stops_at_first_deficit_and_broadcasts_escape() -> None:
    source = _source()
    indices = fixed_seed_indices(source)
    bank = WitnessBank(
        status="complete",
        witnesses=(),
        failure_bits=0,
        checked_seed_indices=indices,
        expected_seed_indices=indices,
        all_uncertified_refuted=False,
        wall_seconds=0.0,
    )
    candidate = select_first_candidate(bank, frozenset())
    assert candidate == (0, 0, 0, 0)
    assert candidate is not None
    checked = check_one_candidate(
        source,
        _wall(),
        bank,
        candidate,
        frozenset(),
        deadline=time.perf_counter() + 30,
    )
    assert checked.status == "uncovered"
    assert len(checked.directions) == 1
    assert checked.directions[0].uncovered_area > 0
    assert checked.escape is not None
    assert mask_product_bits(checked.escape.masks) & (1 << tuple_ordinal(candidate))
    assert checked.broadcast_failure_bits_hex.startswith("0x")
    assert checked.footprint_source.endpoint_git_commit == "commit"
    assert checked.footprint_source.wall_git_commit == "commit"


def test_seed_deadline_is_rechecked_after_an_empty_last_component(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = iter((0.0, 0.0, 2.0, 2.0))

    def one_seed(_source: FrozenInput) -> tuple[int]:
        return (0,)

    def no_centres(_source: FrozenInput, _direction: Direction) -> tuple[()]:
        return ()

    monkeypatch.setattr(fixed_pattern, "fixed_seed_indices", one_seed)
    monkeypatch.setattr(fixed_pattern, "_dot_free_centres", no_centres)
    monkeypatch.setattr(fixed_pattern.time, "perf_counter", lambda: next(clock))
    result = build_witness_bank(
        _source(), _wall(), frozenset(), seed_deadline=1.0, total_deadline=10.0
    )
    assert result.status == "partial"
    assert result.checked_seed_indices == ()


def test_candidate_escape_can_finish_the_global_refutation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = replace(_source(), outer_side=OUTER_SIDE, core_side=CORE_SIDE)
    wall = _wall()
    candidate = (0, 0, 0, 0)
    all_bits = (1 << (16**4)) - 1
    bank = WitnessBank(
        status="complete",
        witnesses=(),
        failure_bits=all_bits ^ 1,
        checked_seed_indices=(0,),
        expected_seed_indices=(0,),
        all_uncertified_refuted=False,
        wall_seconds=0.0,
    )
    references = SourceReferences(
        "endpoint", "commit", "blob", "wall", "commit", "blob", "constructor"
    )
    escape = MaskWitness(0, "owner-000", (F(2), F(2)), (1, 1, 1, 1), 1, (), references)
    checked = CandidateCheck(
        "uncovered", candidate, (), escape, references, 0.0, broadcast_failure_bits=1
    )

    def built(*_args: object, **_kwargs: object) -> WitnessBank:
        return bank

    def candidate_check(*_args: object, **_kwargs: object) -> CandidateCheck:
        return checked

    monkeypatch.setattr(fixed_pattern, "build_witness_bank", built)
    monkeypatch.setattr(fixed_pattern, "check_one_candidate", candidate_check)
    result = run_fixed_pattern(source, wall, frozenset())
    assert result.verdict == "refute-expansion-by-d"
    assert result.bank.failure_bits == all_bits


def test_selected_footprints_use_the_loaded_outer_side() -> None:
    selected = selected_wall_footprints(_wall(), (0, 0, 0, 0), outer_side=F(4))
    assert max(x for x, _ in selected[3]) == 4
    assert max(y for _, y in selected[3]) == 4


def test_oblique_sat_and_direct_dot_incidence_are_strict() -> None:
    direction = Direction("three-four-five", F(3, 5), F(4, 5))
    centre = (F(2), F(2))
    tangent_dot = (F(23, 10), F(12, 5))
    separated_dot = (F(1153, 500), F(301, 125))
    assert not strict_dot_free(
        centre,
        direction,
        outer_side=F(4),
        core_side=F(1),
        dots=(tangent_dot,),
    )
    assert strict_dot_free(
        centre,
        direction,
        outer_side=F(4),
        core_side=F(1),
        dots=(separated_dot,),
    )

    u, v = (F(3, 5), F(4, 5)), (F(-4, 5), F(3, 5))

    def uv_point(a: Fraction, b: Fraction) -> tuple[Fraction, Fraction]:
        return centre[0] + a * u[0] + b * v[0], centre[1] + a * u[1] + b * v[1]

    tangent_owner = (
        uv_point(F(1, 2), F(-1, 10)),
        uv_point(F(3, 5), F(-1, 10)),
        uv_point(F(3, 5), F(1, 10)),
        uv_point(F(1, 2), F(1, 10)),
    )
    separated_owner = tuple((x + F(3, 500), y + F(4, 500)) for x, y in tangent_owner)
    assert not core_disjoint_from_polygon(centre, direction, F(1), tangent_owner)
    assert core_disjoint_from_polygon(centre, direction, F(1), separated_owner)


def test_completed_containment_parser_binds_exact_retained_set() -> None:
    document: dict[str, object] = {
        "schema": "wall-owner-containment/v1",
        "status": "complete",
        "verdict": "refute-containment-expansion",
        "sources": {
            "implementation": {"git_commit": "containment-revision"},
            "endpoint": {"git_blob": "endpoint-blob"},
            "wall": {"git_blob": "wall-blob"},
        },
        "settings": {
            "orientation_count": 361,
            "class_order": list(fixed_pattern.CLASS_IDS),
            "corner_order": list(fixed_pattern.CORNERS),
        },
        "summary": {"logical_slots": 128, "unresolved_relations": 0},
        "counts": {
            "raw_label_universe": 65536,
            "impossible": 0,
            "new_covered": 0,
            "covered": 2,
        },
        "masks": [[1, 1, 1, 1], [32768, 32768, 32768, 32768]],
    }
    certified = parse_completed_containment(
        document,
        endpoint_blob="endpoint-blob",
        wall_blob="wall-blob",
        containment_revision="containment-revision",
    )
    assert certified == frozenset({(0, 0, 0, 0), (15, 15, 15, 15)})
    counts = document["counts"]
    assert isinstance(counts, dict)
    counts["new_covered"] = 1
    with pytest.raises(FixedPatternError, match="conditional entry"):
        parse_completed_containment(
            document,
            endpoint_blob="endpoint-blob",
            wall_blob="wall-blob",
            containment_revision="containment-revision",
        )


def test_cli_writes_complete_and_refused_receipts(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    source, wall = _source(), _wall()
    all_uncertified = ((1 << 65536) - 1) ^ 1 ^ (1 << 65535)
    bank = WitnessBank(
        status="complete",
        witnesses=(),
        failure_bits=all_uncertified,
        checked_seed_indices=(0,),
        expected_seed_indices=(0,),
        all_uncertified_refuted=True,
        wall_seconds=0.0,
    )
    result = FixedPatternResult("refute-expansion-by-d", bank, None, None)

    monkeypatch.setattr(
        fixed_pattern, "validate_own_revision", lambda _revision: (tmp_path, "own-revision")
    )
    monkeypatch.setattr(
        fixed_pattern,
        "validate_output_path",
        lambda output, _repository, _inputs: output,
    )
    monkeypatch.setattr(fixed_pattern, "load_frozen_input", lambda _path, _blob: source)

    def load_wall(_path: Path, _blob: str, **_kwargs: object) -> WallInput:
        return wall

    monkeypatch.setattr(fixed_pattern, "load_wall_input", load_wall)
    monkeypatch.setattr(
        fixed_pattern,
        "load_completed_containment",
        lambda *_args, **_kwargs: (
            fixed_pattern.RETAINED_TUPLES,
            {"path": "containment.json", "git_blob": "containment-blob"},
        ),
    )
    monkeypatch.setattr(fixed_pattern, "run_fixed_pattern", lambda *_args, **_kwargs: result)
    common = [
        "endpoint.json",
        "wall.json",
        "containment.json",
        "--expect-wall-blob",
        "wall-blob",
        "--expect-wall-source",
        "wall-source",
        "--expect-containment-blob",
        "containment-blob",
        "--expect-containment-revision",
        "containment-revision",
        "--expect-git-revision",
        "own-revision",
    ]
    complete_output = tmp_path / "complete.json"
    assert (
        fixed_pattern.main(
            [
                *common,
                "--expect-endpoint-blob",
                fixed_pattern.RETAINED_ENDPOINT_BLOB,
                "--output",
                str(complete_output),
            ]
        )
        == 0
    )
    assert json.loads(complete_output.read_text())["status"] == "complete"

    refused_output = tmp_path / "refused.json"
    assert (
        fixed_pattern.main(
            [
                *common,
                "--expect-endpoint-blob",
                "0" * 40,
                "--output",
                str(refused_output),
            ]
        )
        == 2
    )
    refused = json.loads(refused_output.read_text())
    assert refused["status"] == "invalid"
    assert "exp143 authority" in refused["error"]
