"""Controls for the independent exact corner dual-salvage receipt audit."""

from __future__ import annotations

import gzip
import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools.audit_corner_dual_salvage import (
    CORNERS,
    AuditedScreen,
    audit_component_screen,
    audit_joint_rows,
    exact_separation,
    git_blob_binding,
    load_receipt,
    summarize_rows,
    write_exclusive_atomic,
)
from sqpack.fractional.ceiling import Placement

B = Fraction(9977, 10000)


def _square(low: Fraction, high: Fraction) -> tuple[tuple[Fraction, Fraction], ...]:
    return ((low, low), (high, low), (high, high), (low, high))


def test_exact_sat_requires_positive_gap_and_rejects_touching() -> None:
    first = _square(Fraction(0), Fraction(1))
    separated = exact_separation(first, ((Fraction(5, 2), Fraction(1, 2)),))
    assert separated is not None
    assert separated.axis == (Fraction(-1), Fraction(0))
    assert separated.gap == Fraction(3, 2)
    assert exact_separation(first, ((Fraction(1), Fraction(1, 2)),)) is None
    assert exact_separation(first, _square(Fraction(1, 2), Fraction(3, 2))) is None


def _screen_record(*, gap: str = "3/2", weight: str = "1/3") -> dict[str, object]:
    return {
        "class_id": "bottom-left:control",
        "corner": "bottom-left",
        "footprint_kind": "point",
        "footprint": [["5/2", "1"]],
        "survivor_mask_hex": "0x1",
        "survivor_count": 1,
        "survivor_weight": "1/3",
        "threshold": "10",
        "obstructs": False,
        "survivors": [
            {
                "source_index": 0,
                "weight": weight,
                "separating_axis": ["9977/10000", "0"],
                "positive_projection_gap": gap,
            }
        ],
    }


def test_component_audit_binds_source_index_weight_polygon_and_sat_gap() -> None:
    placement = Placement(Fraction(0), Fraction(1), Fraction(1), Fraction(1, 3), B)
    polygon = ((Fraction(5, 2), Fraction(1)),)
    expected = exact_separation(placement.corners(), polygon)
    assert expected is not None
    row = _screen_record(gap=str(expected.gap))
    audited = audit_component_screen(
        row,
        expected_polygon=polygon,
        expected_class_id="bottom-left:control",
        expected_corner="bottom-left",
        expected_kind="point",
        source=(placement,),
        transported=(placement,),
        direction_axes=frozenset({(Fraction(1), Fraction(0))}),
    )
    assert audited.mask == 1
    assert audited.weight == Fraction(1, 3)

    changed_gap = _screen_record(gap=str(expected.gap + 1))
    with pytest.raises(ValueError, match="altered exact SAT witness"):
        audit_component_screen(
            changed_gap,
            expected_polygon=polygon,
            expected_class_id="bottom-left:control",
            expected_corner="bottom-left",
            expected_kind="point",
            source=(placement,),
            transported=(placement,),
            direction_axes=frozenset({(Fraction(1), Fraction(0))}),
        )
    changed_weight = _screen_record(gap=str(expected.gap), weight="1/2")
    with pytest.raises(ValueError, match="altered survivor weight"):
        audit_component_screen(
            changed_weight,
            expected_polygon=polygon,
            expected_class_id="bottom-left:control",
            expected_corner="bottom-left",
            expected_kind="point",
            source=(placement,),
            transported=(placement,),
            direction_axes=frozenset({(Fraction(1), Fraction(0))}),
        )


def _joint_fixture() -> tuple[
    dict[str, tuple[AuditedScreen, ...]], tuple[Placement, ...], list[dict[str, object]]
]:
    placements = (
        Placement(Fraction(0), Fraction(1), Fraction(1), Fraction(2), B),
        Placement(Fraction(0), Fraction(2), Fraction(2), Fraction(6), B),
    )
    screens = {
        corner: (
            AuditedScreen(f"{corner}:a", 0b11, 2, Fraction(8)),
            AuditedScreen(f"{corner}:b", 0b10, 1, Fraction(6)),
        )
        for corner in CORNERS
    }
    rows: list[dict[str, object]] = []
    for i in range(16):
        choices = tuple(screens[corner][(i >> (3 - n)) & 1] for n, corner in enumerate(CORNERS))
        mask = choices[0].mask & choices[1].mask & choices[2].mask & choices[3].mask
        weight = Fraction(8 if mask == 0b11 else 6)
        rows.append(
            {
                "class_ids": [choice.class_id for choice in choices],
                "survivor_mask_hex": hex(mask),
                "survivor_count": mask.bit_count(),
                "survivor_weight": str(weight),
                "threshold": "7",
                "obstructs": weight >= 7,
            }
        )
    return screens, placements, rows


def test_joint_audit_checks_product_masks_cardinality_mass_and_summary() -> None:
    screens, placements, rows = _joint_fixture()
    unique, summary = audit_joint_rows(rows, screens, placements)
    assert unique == 2
    assert summary["class_count"] == 16
    assert summary["obstructed_count"] == 1
    forged = [dict(row) for row in rows]
    forged[-1]["survivor_count"] = 2
    with pytest.raises(ValueError, match="wrong survivor_count"):
        audit_joint_rows(forged, screens, placements)


def test_summary_retains_all_exact_extrema_and_both_verdicts() -> None:
    rows = [
        {"id": "low", "survivor_weight": "13/2", "obstructs": False},
        {"id": "high-a", "survivor_weight": "15/2", "obstructs": True},
        {"id": "high-b", "survivor_weight": "15/2", "obstructs": True},
    ]
    summary = summarize_rows(rows, class_field="id")
    assert summary["obstructed_count"] == 2
    assert summary["minimum_attaining_classes"] == ["low"]
    assert summary["maximum_attaining_classes"] == ["high-a", "high-b"]


def test_bounded_gzip_load_and_exclusive_output(tmp_path: Path) -> None:
    receipt = tmp_path / "receipt.json.gz"
    receipt.write_bytes(gzip.compress(b'{"schema":"control"}', mtime=0))
    assert load_receipt(receipt, max_compressed_bytes=1_000, max_uncompressed_bytes=1_000) == {
        "schema": "control"
    }
    with pytest.raises(ValueError, match="uncompressed guard"):
        load_receipt(receipt, max_compressed_bytes=1_000, max_uncompressed_bytes=3)

    output = tmp_path / "audit.json"
    write_exclusive_atomic(output, {"status": "complete"})
    assert json.loads(output.read_text()) == {"status": "complete"}
    with pytest.raises(FileExistsError):
        write_exclusive_atomic(output, {"status": "complete"})


def test_git_blob_binding_refuses_source_confusion() -> None:
    source = Path(
        "campaign/series/series-000-smoke-and-calibration/results/agenda-025/"
        "bc-232-leg-01-family.json"
    )
    expected = "8a0bf1a264a1361649bc0acd0f70907ba8125f2f"
    assert git_blob_binding(source, expected, label="source family")["git_blob"] == expected
    with pytest.raises(ValueError, match="expected Git blob"):
        git_blob_binding(source, "0" * 40, label="source family")
