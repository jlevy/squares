"""Independent near45 reader controls on toys; the scientific target is forbidden."""

from __future__ import annotations

import json
from copy import deepcopy
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any

import pytest

from devtools import check_angle_near45_triangle_control as reader
from sqpack.field import NumberField


@pytest.fixture(autouse=True)
def _forbid_target(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden():
        raise AssertionError("author tests must not invoke target_input")

    monkeypatch.setattr(reader, "target_input", forbidden)


def _packet() -> dict[str, Any]:
    return {
        "version": 1,
        "kind": "fixed-side-near45-a3-forcing-triangle",
        "side": "1939/500",
        "point": ["3/2", "13/10"],
        "half_angle_slabs": [[str(left), str(right)] for left, right in reader.SLABS],
        "vertices": ["E", "F", "G"],
        "status": "proved",
        "inequalities_checked": 24,
        "unresolved": [],
    }


def _toy_input() -> tuple[Fraction, reader.Point]:
    return Fraction(19, 5), (Fraction(29, 20), Fraction(13, 10))


def test_polarized_bernstein_reconstructs_algebraic_quartics() -> None:
    field = NumberField((1, 0, -2), ("1", "2"))
    polynomial = (field.one, field.alpha, field.rational(-3), -field.alpha, field.one)
    left, right = Fraction(-2, 3), Fraction(4, 5)
    coefficients = reader.bernstein_coefficients(polynomial, left, right)
    for z in (Fraction(0), Fraction(1, 7), Fraction(1, 2), Fraction(1)):
        t = left + (right - left) * z
        expected = sum((a * t**k for k, a in enumerate(polynomial)), field.zero)
        observed = sum(
            (a * comb(4, k) * z**k * (1 - z) ** (4 - k) for k, a in enumerate(coefficients)),
            field.zero,
        )
        assert observed == expected


def test_vertex_quartics_equal_direct_rotated_triangle_margins() -> None:
    side, point = _toy_input()
    polynomials = reader.vertex_polynomials(side, point)
    field = polynomials[0][0][0].field
    for t in (Fraction(-1, 7), Fraction(0), Fraction(1, 9)):
        d = 1 + t * t
        c = field.alpha * (1 - 2 * t - t * t) / 2
        s = field.alpha * (1 + 2 * t - t * t) / 2
        cosine, sine = c / d, s / d
        h = (cosine + sine) / 2
        u = cosine * side / 2 + sine - Fraction(1, 2)
        v = cosine - sine - Fraction(1, 2)
        vertices = ((u, v), ((h - cosine * v) / sine, v), (u, (h - sine * u) / cosine))
        a = cosine * point[0] + sine * point[1]
        b = -sine * point[0] + cosine * point[1]
        for margins, (cu, cv), factor in zip(
            polynomials, vertices, (d * d, s * d, c * d), strict=True
        ):
            assert factor > 0
            expected = tuple(
                Fraction(1, 2) + sign * offset
                for offset in (a - cu, b - cv)
                for sign in (1, -1)
            )
            for polynomial, margin in zip(margins, expected, strict=True):
                assert len(polynomial) == 5
                value = sum(
                    (coefficient * t**k for k, coefficient in enumerate(polynomial)), field.zero
                )
                assert value == factor * margin


def test_unsplit_sign_rule_keeps_zero_contacts_and_is_not_a_disproof() -> None:
    field = NumberField((1, 0, -2), ("1", "2"))
    zero, one = Fraction(0), Fraction(1)
    assert reader.certifies_nonnegative((field.zero,) * 5, zero, one)
    assert reader.certifies_nonnegative((field.zero, field.one), zero, one)
    assert not reader.certifies_nonnegative((field.rational(-Fraction(1, 2**200)),), zero, one)
    # (t-1/2)² is nonnegative but its unsplit Bernstein coefficients are not all so.
    assert not reader.certifies_nonnegative(
        tuple(field.rational(v) for v in (Fraction(1, 4), -1, 1)), zero, one
    )
    with pytest.raises(ValueError, match="degree"):
        reader.bernstein_coefficients((field.one,) * 6, zero, one)
    with pytest.raises(ValueError, match="endpoints"):
        reader.bernstein_coefficients((field.one,), one, zero)
    other = NumberField((1, 0, -2), ("1", "2"))
    with pytest.raises(ValueError, match="field"):
        reader.bernstein_coefficients((field.one, other.one), zero, one)


def test_avoidance_reduction_on_exact_toy_centers() -> None:
    """Sample the independently stated implication, not the scientific target."""
    field = NumberField((1, 0, -2), ("1", "2"))
    side = Fraction(19, 5)
    avoiding = 0
    for tangent in (Fraction(-1, 20), Fraction(0), Fraction(1, 20)):
        denominator = 1 + tangent**2
        cosine = field.alpha * (1 - 2 * tangent - tangent**2) / (2 * denominator)
        sine = field.alpha * (1 + 2 * tangent - tangent**2) / (2 * denominator)
        assert cosine**2 + sine**2 == 1
        height = (cosine + sine) / 2
        assert Fraction(1, 2) < height < 1
        for x in map(Fraction, (1, "7/5", "29/20", "3/2", "19/10")):
            for fraction in map(Fraction, (0, "1/10", "1/5", "1/2", 1)):
                y = height + (1 - height) * fraction
                outside = []
                for px in (Fraction(1), side / 2):
                    du = cosine * (px - x) + sine * (1 - y)
                    dv = -sine * (px - x) + cosine * (1 - y)
                    outside.append(
                        any(
                            (offset - Fraction(1, 2)).sign() > 0
                            for offset in (du, -du, dv, -dv)
                        )
                    )
                if all(outside):
                    avoiding += 1
                    u = cosine * x + sine * y
                    v = -sine * x + cosine * y
                    assert u < cosine * side / 2 + sine - Fraction(1, 2)
                    assert v < cosine - sine - Fraction(1, 2)
                    assert sine * u + cosine * v >= height
    assert avoiding > 0


def test_toy_closed_triangle_checks_every_vertex_and_margin() -> None:
    side, point = _toy_input()
    slabs = ((Fraction(-1, 1000), Fraction(0)), (Fraction(0), Fraction(1, 1000)))
    result = reader.check_triangle(side, point, slabs)
    assert result.proved
    assert result.vertices_checked == 6
    assert result.inequalities_checked == 24
    failed = reader.check_triangle(side, (Fraction(0), Fraction(0)), slabs)
    assert not failed.proved
    assert failed.inequalities_checked == 24
    # The smaller q makes K empty near t=0. Testing its formal vertices may still fail.
    empty = reader.check_triangle(Fraction(3), point, slabs)
    assert not empty.proved
    assert empty.inequalities_checked == 24
    with pytest.raises(ValueError, match="slabs"):
        reader.check_triangle(
            side, point, ((Fraction(-1, 3), Fraction(0)), (Fraction(0), Fraction(1, 3)))
        )
    with pytest.raises(ValueError, match="side"):
        reader.check_triangle(Fraction(4), point, slabs)
    with pytest.raises(ValueError, match="point"):
        reader.vertex_polynomials(side, (1.0, Fraction(1)))  # type: ignore[arg-type]


def test_packet_binding_precedes_geometry_and_demands_complete_positive_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = []

    def toy():
        calls.append(1)
        return _toy_input()

    monkeypatch.setattr(reader, "target_input", toy)
    packet = _packet()
    assert reader.check_packet(packet)["decision"] == "proved"
    for key, value in (
        ("version", True),
        ("kind", "near-axis"),
        ("side", "3878/1000"),
        ("side", 3.878),
        ("point", ["1.5", "13/10"]),
        ("half_angle_slabs", [["0", "0"], ["0", "0"]]),
        ("vertices", ["F", "E", "G"]),
        ("inequalities_checked", True),
        ("inequalities_checked", 23),
        ("inequalities_checked", 25),
        ("status", "accepted"),
        ("unresolved", [[0, 0, 0]]),
    ):
        with pytest.raises(ValueError, match="packet"):
            reader.check_packet(packet | {key: value})
    with pytest.raises(ValueError, match="keys"):
        reader.check_packet(packet | {"subdivision_depth": 1})
    missing = deepcopy(packet)
    del missing["point"]
    with pytest.raises(ValueError, match="keys"):
        reader.check_packet(missing)
    assert calls == [1]


def test_incomplete_packets_never_construct_target_and_failure_prefix_is_strict() -> None:
    packet = _packet() | {"status": "unresolved"}
    for count, failures in ((0, []), (1, [[0, 0, 0]]), (24, [])):
        assert (
            reader.check_packet(
                packet | {"inequalities_checked": count, "unresolved": failures}
            )["decision"]
            == "unresolved"
        )
    for failures in (
        [[0, 0, 2]],
        [[0, 0, 1], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0]],
        [[False, 0, 0]],
        [[0, 0, 4]],
    ):
        with pytest.raises(ValueError, match="unresolved"):
            reader.check_packet(packet | {"inequalities_checked": 2, "unresolved": failures})


@pytest.mark.parametrize(
    "payload",
    [b'{"version":1,"version":1}', b'{"x":1.0}', b'{"x":NaN}', b"\xff", b"{", b" " * 262145],
)
def test_bounded_loader_refusals_never_construct_geometry(
    payload: bytes, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "packet.json"
    path.write_bytes(payload)
    assert reader.main([str(path), "--target-a3"]) == 2
    captured = capsys.readouterr()
    assert json.loads(captured.out)["decision"] == "refused"
    assert json.loads(captured.err)["wall_cap_seconds"] == 10


def test_cli_requires_absolute_dispatch_and_refuses_links(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "packet.json"
    source.write_text(json.dumps(_packet()))
    link = tmp_path / "link.json"
    link.symlink_to(source)
    for path in (link, tmp_path / "missing.json"):
        assert reader.main([str(path), "--target-a3"]) == 2
        assert json.loads(capsys.readouterr().out)["decision"] == "refused"
    for args in (
        [str(source)],
        ["relative.json", "--target-a3"],
        [str(source), "--target-a3", "--depth", "1"],
    ):
        with pytest.raises(SystemExit) as refusal:
            reader.main(args)
        assert refusal.value.code == 2


def test_cli_toy_positive_and_negative_replays_retain_outcome_and_costs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "packet.json"
    source.write_text(json.dumps(_packet()))
    monkeypatch.setattr(reader, "target_input", _toy_input)
    assert reader.main([str(source), "--target-a3"]) == 0
    captured = capsys.readouterr()
    receipt, cost = json.loads(captured.out), json.loads(captured.err)
    assert receipt["decision"] == "proved"
    assert receipt["inequalities_checked"] == 24
    assert receipt["h036_outcome"] == "unresolved"
    assert cost["subdivisions"] == 0
    assert cost["wall_seconds"] >= 0
    assert cost["cpu_seconds"] >= 0
    monkeypatch.setattr(
        reader, "target_input", lambda: (Fraction(19, 5), (Fraction(0), Fraction(0)))
    )
    assert reader.main([str(source), "--target-a3"]) == 1
    assert json.loads(capsys.readouterr().out)["decision"] == "unresolved"


def test_alarm_restores_handler_and_never_accepts_partial_work(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    alarms: list[int] = []
    previous = reader.signal.getsignal(reader.signal.SIGALRM)
    monkeypatch.setattr(reader.signal, "alarm", alarms.append)

    def interrupted(*_args: object, **_kwargs: object) -> Any:
        raise TimeoutError("toy interrupted admission")

    monkeypatch.setattr(reader, "load_packet", interrupted)
    assert reader.main([str(tmp_path / "packet.json"), "--target-a3"]) == 1
    captured = capsys.readouterr()
    assert json.loads(captured.out)["decision"] == "unresolved"
    assert json.loads(captured.err)["exit_code"] == 1
    assert alarms == [10, 0]
    assert reader.signal.getsignal(reader.signal.SIGALRM) == previous


def test_reader_refuses_an_incomplete_independent_calculation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(reader, "target_input", _toy_input)
    monkeypatch.setattr(
        reader, "check_triangle", lambda *_args: reader.TriangleResult(5, 20, ())
    )
    with pytest.raises(ValueError, match="all 24"):
        reader.check_packet(_packet())
