"""Target-free controls for the n17 endpoint owner-axis feature inventory."""

# ruff: noqa: SLF001
# pyright: reportPrivateUsage=false

from __future__ import annotations

import copy
import json
from fractions import Fraction as Q
from pathlib import Path

import pytest
import sympy as sp

from devtools import check_n17_endpoint_feasibility as endpoint_module
from devtools import check_n17_endpoint_features as features
from devtools.check_n17_endpoint_feasibility import Box, _layout, symbolic_identities


def test_owner_option_manifest_is_complete_and_keeps_duplicate_owners() -> None:
    rows = features.option_manifest()
    assert len(rows) == 168
    assert sum(row["kind"] == "identity" for row in rows) == 33
    assert len(features.PARALLEL_PAIRS) == 9
    assert set(features.PARALLEL_PAIRS) == {
        (1, 2),
        (1, 3),
        (5, 7),
        (9, 10),
        (9, 11),
        (10, 12),
        (11, 12),
        (12, 14),
        (13, 14),
    }
    zeros = [row for row in rows if row["kind"] == "identity"]
    face = [row for row in zeros if (row["left"], row["right"]) == (9, 10)]
    assert {(row["owner"], row["axis"], row["sign"]) for row in face} == {
        (9, "u", 1),
        (10, "u", 1),
    }
    cross = [row for row in zeros if (row["left"], row["right"]) == (8, 16)]
    assert [(row["owner"], row["axis"], row["sign"]) for row in cross] == [(16, "q", -1)]
    corner = [row for row in zeros if (row["left"], row["right"]) == (2, 3)]
    assert {(row["owner"], row["axis"], row["sign"]) for row in corner} == {
        (2, "ex", -1),
        (3, "ex", -1),
        (2, "ey", 1),
        (3, "ey", 1),
    }


def test_active_wall_ties_and_corner9() -> None:
    rows = features.active_wall_corners()
    assert len(rows) == 60
    assert sum(row["kind"] == "identity" for row in rows) == 29
    left9 = [row for row in rows if row["label"] == 9]
    assert [(row["corner"], row["kind"]) for row in left9] == [
        (0, "strict_positive"),
        (1, "strict_positive"),
        (2, "strict_positive"),
        (3, "identity"),
    ]


@pytest.mark.slow
def test_symbolic_zero_options_and_displacement_refusal() -> None:
    # A preceding test may have populated the foundation cache in this worker.
    symbolic_identities.cache_clear()
    features.symbolic_zero_proofs.cache_clear()
    result = features.symbolic_zero_proofs()
    assert result["pair_zero_options"] == 33
    assert result["pair_unique_identities"] == 22
    assert result["wall_zero_corners"] == 29
    assert result["parallel_offset_identities"] == 9
    t, b = sp.symbols("t b", real=True)
    side, aux, centres = _layout(t, b, sp.Rational(1, 2))
    shifted = list(centres)
    shifted[0] = (shifted[0][0] + sp.Rational(1, 10), shifted[0][1])
    assert (
        sp.cancel(
            features._directed_gap(1, 2, "ex", 1, aux, centres=tuple(shifted), symbolic=True)
        )
        != 0
    )
    assert (
        sp.cancel(features._wall_corner_gap(1, "left", 0, side, aux, centres=tuple(shifted)))
        != 0
    )


def test_signed_gap_and_parallel_offset_on_unrelated_rationals() -> None:
    side, aux, centres = _layout(Box.point(Q(1, 3)), Box.point(Q(1, 5)), Box.point(Q(1, 2)))
    del side
    active = features._directed_gap(1, 2, "ex", 1, aux, centres=centres, symbolic=False)
    reverse = features._directed_gap(1, 2, "ex", -1, aux, centres=centres, symbolic=False)
    assert active == Box.point(Q(0))
    assert reverse.hi < 0
    assert features._tau({"left": 1, "right": 2}, aux, centres) == Box.point(Q(0))
    assert features._directed_gap(
        2, 3, "ey", 1, aux, centres=centres, symbolic=False
    ) == Box.point(Q(0))
    assert features._directed_gap(
        2, 3, "ex", -1, aux, centres=centres, symbolic=False
    ) == Box.point(Q(0))


def test_full_unrelated_interval_inventory_and_strict_refusal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    result = features.interval_inventory((Q(1, 3), Q(1, 5)), (Q(1, 10**12), Q(1, 10**12)))
    assert result["counts"] == features.EXPECTED_COUNTS
    assert result["feature_passed"]
    assert not result["failures"]
    assert all(row["passed"] for row in result["parallel_offsets"])
    gap = features._directed_gap
    injected_gap = [Box(Q(-1), Q(1))]

    def straddling_pair(
        left: int,
        right: int,
        axis: str,
        sign: int,
        aux: dict[str, object],
        *,
        centres: tuple[tuple[object, object], ...],
        symbolic: bool,
    ) -> object:
        if (left, right, axis, sign) == (1, 2, "ey", 1):
            return injected_gap[0]
        return gap(left, right, axis, sign, aux, centres=centres, symbolic=symbolic)

    monkeypatch.setattr(features, "_directed_gap", straddling_pair)
    for candidate in (Box(Q(-1), Q(1)), Box(Q(-1), Q(0))):
        injected_gap[0] = candidate
        refused = features.interval_inventory((Q(1, 3), Q(1, 5)), (Q(1, 10**12), Q(1, 10**12)))
        assert not refused["feature_passed"]
        assert "pair.(1, 2, 'ey', 1)" in refused["failures"]
    wall_gap = features._wall_corner_gap

    def straddling_wall(
        label: int,
        wall: str,
        corner: int,
        side: object,
        aux: dict[str, object],
        *,
        centres: tuple[tuple[object, object], ...],
    ) -> object:
        if (label, wall, corner) == (1, "left", 1):
            return Box(Q(0), Q(1))
        return wall_gap(label, wall, corner, side, aux, centres=centres)

    monkeypatch.setattr(features, "_wall_corner_gap", straddling_wall)
    refused = features.interval_inventory((Q(1, 3), Q(1, 5)), (Q(1, 10**12), Q(1, 10**12)))
    assert "wall.1.left.1" in refused["failures"]


def test_coverage_rejects_owner_loss_duplicate_corner_and_bool_label() -> None:
    pairs = list(features.option_manifest())
    walls = list(features.active_wall_corners())
    features.validate_coverage(pairs, walls)
    with pytest.raises(ValueError, match="owner-axis coverage"):
        features.validate_coverage(pairs[:-1], walls)
    with pytest.raises(ValueError, match="wall-corner coverage"):
        features.validate_coverage(pairs, [*walls[:-1], walls[0]])
    changed = copy.deepcopy(pairs)
    changed[0]["owner"] = True
    with pytest.raises(ValueError, match="malformed owner-axis"):
        features.validate_coverage(changed, walls)


def test_prerequisites_elsewhere_or_tampered_are_refused_without_target_io(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Prerequisites are named by revision and path, and their content is then checked."""
    source = tmp_path / "fake-source.json"
    source.write_bytes(b"{}")
    elsewhere = tmp_path / "fake-root.json"
    assert features.main([str(elsewhere), str(elsewhere), "--source", str(source)]) == 2
    assert "expected the retained" in json.loads(capsys.readouterr().out)["error"]
    paths = []
    for reference in (features.FROZEN_ROOT_REF, features.FROZEN_ENDPOINT_REF):
        path = tmp_path / reference.partition(":")[2]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"{}")
        paths.append(str(path))
    monkeypatch.setattr(endpoint_module, "REPO", tmp_path)
    assert features.main([*paths, "--source", str(source)]) == 2
    out = json.loads(capsys.readouterr().out)
    assert out["criterion_passed"] is False
    assert "retained" not in out["error"]
