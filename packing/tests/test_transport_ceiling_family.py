"""Exact transport preserves geometry and rejects ambiguous direction identities."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools.transport_ceiling_family import main, transport
from sqpack.fractional.ceiling import CeilingCertificate, verify_ceiling


def source_family() -> dict:
    return {
        "n": 2,
        "outer_side": "2",
        "square_side": "1/2",
        "half_tangents": ["0", "1/5", "207107/500000"],
        "placements": [["0", "1/4", "1/4", "1", "1/2"], ["1/5", "3/2", "3/2", "1", "1/2"]],
    }


def test_unit_transport_matches_corner_geometry_and_independent_depth() -> None:
    source = CeilingCertificate.from_record(source_family())
    moved_record = transport(source_family(), Fraction(2), side=Fraction(5))
    moved = CeilingCertificate.from_record(moved_record)
    for original, scaled in zip(source.placements, moved.placements, strict=True):
        assert scaled.corners() == tuple(
            (2 * x + Fraction(1, 2), 2 * y + Fraction(1, 2)) for x, y in original.corners()
        )
    assert all(p.side == 1 for p in moved.placements)
    assert verify_ceiling(source).max_depth == 1
    assert verify_ceiling(moved).max_depth == 1
    assert moved.total_weight == 2


def test_state_remap_uses_tangent_identity_and_is_safe_to_resume_twice() -> None:
    family = source_family()
    state = {
        "outer_side": "2",
        "square_side": "1/2",
        "sites": [["1", "1"]],
        "rows": [[1, "1", "1"]],
        "best_family": family,
    }
    target = tuple(map(Fraction, ("0", "1/10", "1/5", "207107/500000")))
    first = transport(state, Fraction(2), half_tangents=target)
    second = transport(first, Fraction(1), half_tangents=target)
    assert first["rows"] == [[2, "2", "2"]]
    assert second["rows"] == first["rows"]
    assert second["half_tangents"] == [str(t) for t in target]
    with pytest.raises(ValueError, match="omits a source direction"):
        transport(first, Fraction(1), half_tangents=(Fraction(0), Fraction(1, 2)))
    first["half_tangents"] = family["half_tangents"]
    with pytest.raises(ValueError, match=r"disagree.*net"):
        transport(first, Fraction(1))


def test_invalid_transport_cannot_shrink_the_container_or_hide_closed_overlap() -> None:
    with pytest.raises(ValueError, match="positive"):
        transport(source_family(), Fraction(0))
    with pytest.raises(ValueError, match="smaller"):
        transport(source_family(), Fraction(2), side=Fraction(3))
    family = source_family()
    family["placements"] = [["0", "1/4", "1/4", "1", "1/2"], ["0", "3/4", "1/4", "1", "1/2"]]
    moved = CeilingCertificate.from_record(transport(family, Fraction(2)))
    assert verify_ceiling(moved).max_depth == 2


def test_verified_cli_refuses_closed_overlap_without_writing(tmp_path: Path) -> None:
    family = source_family()
    family["placements"] = [["0", "1/4", "1/4", "1", "1/2"]] * 2
    source = tmp_path / "source.json"
    output = tmp_path / "result.json"
    source.write_text(json.dumps(family))
    assert main([str(source), "--scale", "2", "--verify", "--out", str(output)]) == 1
    assert not output.exists()
    assert json.loads(source.read_text()) == family
