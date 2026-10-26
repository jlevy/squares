"""`devtools.build_field_configuration`: contacts, the stationary solve and the field."""

from __future__ import annotations

from fractions import Fraction

import mpmath as mp
import pytest

from devtools import build_field_configuration as build


def _half_angle_rotation(t: Fraction) -> tuple[Fraction, Fraction]:
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def _grid() -> build.Certificate:
    """Four unit squares in a 2 x 2 grid, every contact opened by 1e-60."""
    gap = Fraction(1, 10**60)
    poses = [
        (
            Fraction(1, 2) + i * (1 + gap),
            Fraction(1, 2) + j * (1 + gap),
            Fraction(1),
            Fraction(0),
        )
        for i in range(2)
        for j in range(2)
    ]
    return build.Certificate(n=4, side=2 + gap, poses=tuple(poses))


def _diamond() -> build.Certificate:
    """One square turned near 45 degrees, its corners within 1e-50 of the walls."""
    t = Fraction(str(mp.nstr(mp.sqrt(2) - 1, 80)))
    c, s = _half_angle_rotation(t)
    reach = (abs(c) + abs(s)) / 2
    side = 2 * reach + Fraction(1, 10**55)
    return build.Certificate(n=1, side=side, poses=((side / 2, side / 2, c, s),))


def _prepared(cert: build.Certificate) -> tuple[build.System, list, build.Structure]:
    contacts, poses = build.extract_contacts(cert)
    system = build.System(cert.n, contacts, build.Classes(cert.n, contacts))
    start = build.initial_values(system, poses)
    start[2 * cert.n] = build.mpf_of(cert.side)
    return system, start, build.structure(system, [float(v) for v in start])


def test_grid_contacts_are_typed_and_held_at_zero() -> None:
    contacts, _ = build.extract_contacts(_grid())
    assert contacts.kinds == {"edge-wall": 8, "edge-edge": 4, "corner-corner": 2}
    classes = build.Classes(4, contacts)
    assert classes.count == 0
    assert all(cls == build.Classes.AXIS for cls in classes.of)


def test_grid_side_is_two() -> None:
    system, start, _ = _prepared(_grid())
    point = build.stationary_refine(system, start, digits=80, log=lambda *_: None)
    mp.mp.dps = 90
    assert abs(point.values[2 * system.n] - 2) < mp.mpf(10) ** -78


def test_an_undecided_margin_is_refused() -> None:
    cert = _grid()
    x, y, c, s = cert.poses[3]
    poses = (*cert.poses[:3], (x + Fraction(1, 10**20), y, c, s))
    with pytest.raises(build.BuildError) as refused:
        build.extract_contacts(build.Certificate(n=4, side=cert.side + 1, poses=poses))
    assert refused.value.kind == "undecided"


def test_the_diamond_is_held_by_stationarity_and_its_side_is_root_two() -> None:
    system, start, shape = _prepared(_diamond())
    assert system.contacts.kinds == {"corner-wall": 4}
    # The contacts leave the turn free at first order; the side is stationary in it.
    assert [system.names()[k] for k in shape.free] == ["t[0]"]
    point = build.stationary_refine(system, start, digits=120, log=lambda *_: None)
    assert not point.pinned
    side = point.values[2 * system.n]
    found, _ = build.relation([side**k for k in range(3)], 120)
    assert found is not None
    assert [abs(c) for c in found] == [2, 0, 1]


def test_a_relation_that_holds_only_to_its_search_precision_is_refused() -> None:
    mp.mp.dps = 200
    value = mp.pi
    found, attempts = build.relation([value**k for k in range(6)], 200)
    assert found is None
    assert attempts


def test_pins_are_small_denominators_within_the_tolerance() -> None:
    mp.mp.dps = 60
    value = mp.mpf(1) / 3 + mp.mpf(10) ** -20
    pinned = build.pin(value)
    assert pinned == Fraction(1, 3)
    assert abs(build.mpf_of(pinned) - value) < build.mpf_of(build.PIN_TOLERANCE)


def test_canonical_rotation_is_in_range() -> None:
    mp.mp.dps = 30
    for degrees in (-170, -91, -44, 0, 44.9, 46, 135, 180):
        c, s = build.canonical_rotation(
            mp.cos(mp.radians(degrees)), mp.sin(mp.radians(degrees))
        )
        angle = mp.degrees(mp.atan2(s, c))
        assert -45 < angle <= 45


def test_the_diamond_is_rebuilt_exactly_in_its_field() -> None:
    system, start, _ = _prepared(_diamond())
    point = build.stationary_refine(system, start, digits=120, log=lambda *_: None)
    t = point.values[2 * system.n + 1]
    found, _ = build.relation([t**k for k in range(3)], 120)
    assert found is not None
    receipt = {
        "generator": "t[0]",
        "generator_relation": {"high_to_low": [str(c) for c in reversed(found)]},
        "classes": {"t[0]": {"kind": "generator"}},
    }
    field_ = build.field_of(receipt, t, 120)
    tangents = build.class_tangents(system, receipt, field_)
    rot = [build.rotation_in(tangents[0], field_)]
    rows = build.affine_rows(system, rot, field_)
    values, stats = build.solve_over_field(rows, 3, {}, field_)
    assert stats["constraints"] >= 1
    # t = 1 - sqrt(2) on the canonical side of the quarter turn, and the side is sqrt(2).
    assert (values[2] * values[2] - 2).is_zero()
    assert (values[2] + field_.alpha - 1).is_zero()


def test_an_inconsistent_row_is_refused() -> None:
    system, _start, _ = _prepared(_grid())
    field_ = build.NumberField([1, 0, -2], (Fraction(1), Fraction(2)))
    rot = [(field_.one, field_.zero)] * 4
    rows = build.affine_rows(system, rot, field_)
    coefficients, constant = rows[0]
    rows[0] = (coefficients, constant + Fraction(1, 10**6))
    with pytest.raises(build.BuildError) as refused:
        build.solve_over_field(rows, 9, {}, field_)
    assert refused.value.kind == "inconsistent"
