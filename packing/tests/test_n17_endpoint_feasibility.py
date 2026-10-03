"""Synthetic controls for the H-256 exact endpoint feasibility instrument."""

# ruff: noqa: SLF001
# pyright: reportPrivateUsage=false

from __future__ import annotations

import copy
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest
import sympy as sp

from devtools import check_n17_endpoint_feasibility as endpoint


def test_exact_box_arithmetic_and_refusals() -> None:
    left = endpoint.Box(Q(-3), Q(-2))
    right = endpoint.Box(Q(4), Q(5))
    assert left * right == endpoint.Box(Q(-15), Q(-8))
    assert right.reciprocal() == endpoint.Box(Q(1, 5), Q(1, 4))
    assert endpoint.Box(Q(-2), Q(3)).absolute() == endpoint.Box(Q(0), Q(3))
    with pytest.raises(ValueError, match="denominator includes zero"):
        endpoint.Box(Q(-1), Q(2)).reciprocal()
    with pytest.raises(ValueError, match="exact integer or Fraction"):
        endpoint.Box.point(0.5)  # type: ignore[arg-type]
    bad_boolean = True
    with pytest.raises(ValueError, match="exact integer or Fraction"):
        endpoint.Box.point(bad_boolean)


def test_synthetic_support_matches_direct_absolute_projections() -> None:
    t, b = Q(1, 3), Q(1, 5)
    _, exact, _ = endpoint._layout(t, b, Q(1, 2))
    _, boxed, _ = endpoint._layout(
        endpoint.Box.point(t), endpoint.Box.point(b), endpoint.Box.point(Q(1, 2))
    )
    bases = {
        1: ((Q(1), Q(0)), (Q(0), Q(1))),
        9: (exact["u"], exact["v"]),
        16: (exact["p"], exact["q"]),
    }
    for label, basis in bases.items():
        for axis in ("ex", "ey", "u", "v", "w", "p", "q"):
            direct = (
                sum((abs(endpoint._dot(exact[axis], vector)) for vector in basis), Q(0)) / 2
            )
            assert endpoint._support(label, axis, exact, Q(1, 2)) == direct
            assert endpoint._support_interval(label, axis, boxed) == endpoint.Box.point(direct)


# Hosted run36864534354 measured31.66s call time on2026-10-01.
# Full symbolic replay remains in the slow lane; the eight bounded controls stay fast.
@pytest.mark.slow
def test_symbolic_identities_and_displacements() -> None:
    # Exercise the proof even when another slow test warmed its cache.
    endpoint.symbolic_identities.cache_clear()
    assert endpoint.symbolic_identities() == {
        "wall_identities": 15,
        "pair_identities": 21,
        "normalizations": 3,
        "slider_identity": True,
    }
    t, b = sp.symbols("t b", real=True)
    side, aux, centres = endpoint._layout(t, b, sp.Rational(1, 2))
    shifted = list(centres)
    shifted[0] = (shifted[0][0] + sp.Rational(1, 10), shifted[0][1])
    assert (
        sp.cancel(
            endpoint._wall_gap(1, "left", side, aux, tuple(shifted), half=sp.Rational(1, 2))
        )
        != 0
    )
    assert (
        sp.cancel(
            endpoint._directed_gap(1, 2, "ex", aux, tuple(shifted), half=sp.Rational(1, 2))
        )
        != 0
    )
    shifted = list(centres)
    shifted[2] = (shifted[2][0] + sp.Rational(1, 10), shifted[2][1])
    assert (
        sp.cancel(
            endpoint._directed_gap(3, 2, "ex", aux, tuple(shifted), half=sp.Rational(1, 2))
        )
        != 0
    )
    shifted = list(centres)
    shifted[15] = (shifted[15][0] + sp.Rational(1, 10), shifted[15][1])
    original = endpoint._directed_gap(16, 17, "p", aux, centres, half=sp.Rational(1, 2))
    changed = endpoint._directed_gap(16, 17, "p", aux, tuple(shifted), half=sp.Rational(1, 2))
    assert sp.cancel(changed - original) != 0


def synthetic_geometry() -> dict[str, Any]:
    return endpoint.interval_geometry((Q(1, 3), Q(1, 5)), (Q(1, 10**12), Q(1, 10**12)))


def test_synthetic_interval_roster_is_complete_but_not_a_root_claim() -> None:
    result = synthetic_geometry()
    assert result["counts"] == {
        "walls": 68,
        "wall_identities": 15,
        "wall_strict": 53,
        "pairs": 136,
        "pair_identities": 21,
        "pair_strict": 115,
    }
    assert result["geometry_passed"] is False
    assert len(result["walls"]) == 68
    assert len(result["pairs"]) == 136
    identity = next(row for row in result["pairs"] if (row["left"], row["right"]) == (2, 3))
    assert identity["identity"]["reason"] == "corner"
    assert len(identity["identity"]["axes"]) == 2
    assert identity["bound_scope"] == "certified_root"


def test_synthetic_overlap_and_q_separation() -> None:
    _, aux, _ = endpoint._layout(
        endpoint.Box.point(Q(1, 3)), endpoint.Box.point(Q(1, 5)), endpoint.Box.point(Q(1, 2))
    )
    coincident = tuple((endpoint.Box.point(Q(0)), endpoint.Box.point(Q(0))) for _ in range(17))
    for axis in endpoint.AXIS_ORDER:
        for sign in (-1, 1):
            assert (
                endpoint._directed_gap_interval(1, 2, axis, aux, coincident, direction=sign).hi
                < 0
            )
    separated = list(coincident)
    q = aux["q"]
    separated[15] = (3 * q[0], 3 * q[1])
    assert (
        endpoint._directed_gap_interval(14, 16, "q", aux, tuple(separated), direction=1).lo > 0
    )


def test_coverage_rejects_missing_duplicate_kind_and_bool_label() -> None:
    result = synthetic_geometry()
    walls, pairs = result["walls"], result["pairs"]
    endpoint.validate_coverage(walls, pairs)
    with pytest.raises(ValueError, match="wall coverage"):
        endpoint.validate_coverage(walls[:-1], pairs)
    with pytest.raises(ValueError, match="pair coverage"):
        endpoint.validate_coverage(walls, [*pairs[:-1], pairs[0]])
    changed = copy.deepcopy(pairs)
    changed[0]["kind"] = "strict"
    with pytest.raises(ValueError, match="pair obligation kind"):
        endpoint.validate_coverage(walls, changed)
    changed = copy.deepcopy(walls)
    changed[0]["label"] = True
    with pytest.raises(ValueError, match="malformed wall"):
        endpoint.validate_coverage(changed, pairs)


def test_duplicate_json_and_tampered_root_refusal_without_target_io(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A tampered root at the retained path is refused by the root checker, not a blob."""
    with pytest.raises(ValueError, match="duplicate JSON key"):
        endpoint._object_unique([("box", 1), ("box", 2)])
    relative = endpoint.FROZEN_ROOT_REF.partition(":")[2]
    certificate = tmp_path / relative
    certificate.parent.mkdir(parents=True)
    certificate.write_text('{"schema":"tampered"}')
    source = tmp_path / "fake-source.json"
    source.write_bytes(b"{}")
    monkeypatch.setattr(endpoint, "REPO", tmp_path)
    assert endpoint.main([str(certificate), "--source", str(source)]) == 2
    out = json.loads(capsys.readouterr().out)
    assert out["criterion_passed"] is False
    assert "retained" not in out["error"]


def test_the_root_is_named_by_its_retained_path(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    relative = endpoint.FROZEN_ROOT_REF.partition(":")[2]
    endpoint.require_retained_path(endpoint.REPO / relative, endpoint.FROZEN_ROOT_REF)
    copy_elsewhere = tmp_path / "certificate.json"
    with pytest.raises(ValueError, match="expected the retained"):
        endpoint.require_retained_path(copy_elsewhere, endpoint.FROZEN_ROOT_REF)
    assert endpoint.main([str(copy_elsewhere)]) == 2
    assert "expected the retained" in json.loads(capsys.readouterr().out)["error"]


def test_large_exact_fraction_serializes_under_receipt_cap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    long_value = Q(1, 10**5000 + 7)
    encoded = endpoint._fraction_string(long_value)
    assert encoded.startswith("1/")
    assert len(encoded) == 5003
    assert endpoint.Box.point(long_value).as_json() == [encoded, encoded]
    monkeypatch.setattr(endpoint, "MAX_DECIMAL_DIGITS", 20)
    with pytest.raises(ValueError, match="serialization cap"):
        endpoint._integer_decimal(10**20)
