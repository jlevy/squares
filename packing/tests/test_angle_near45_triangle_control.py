"""Exact unrelated toys and mocked dispatch; actual/source geometry is forbidden."""

from __future__ import annotations

import json
import signal
import subprocess
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import angle_near45_triangle_control as near
from devtools.angle_tile_certificate import certify_nonnegative, evaluate

F = Fraction
TOY_SIDE = F(15, 4)
TOY_POINT = (F(3, 2), F(1))


@pytest.fixture(autouse=True)
def forbid_actual_geometry(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args, **_kwargs):
        raise AssertionError("a source-free control attempted actual target construction")

    monkeypatch.setattr(near, "target_input", forbidden)
    monkeypatch.setattr(subprocess, "run", forbidden)


def test_chart_identity_denominators_and_all_vertex_margin_identities() -> None:
    d, c, s = near.chart_polynomials()
    polynomials = near.triangle_polynomials(TOY_SIDE, TOY_POINT)
    assert len(polynomials) == 3
    assert all(len(row) == 4 for row in polynomials)
    assert all(len(p) <= 5 for row in polynomials for p in row)
    for t in (F(-1, 10), F(-1, 20), F(0), F(1, 20), F(1, 10)):
        den, cn, sn = (evaluate(p, t) for p in (d, c, s))
        cosine, sine = cn / den, sn / den
        assert den > 0
        assert cn > 0
        assert sn > 0
        assert cosine * cosine + sine * sine == 1
        height = (cosine + sine) / 2
        upper_u = cosine * TOY_SIDE / 2 + sine - F(1, 2)
        upper_v = cosine - sine - F(1, 2)
        vertices = (
            (upper_u, upper_v),
            ((height - cosine * upper_v) / sine, upper_v),
            (upper_u, (height - sine * upper_u) / cosine),
        )
        point_u = cosine * TOY_POINT[0] + sine * TOY_POINT[1]
        point_v = -sine * TOY_POINT[0] + cosine * TOY_POINT[1]
        multipliers = ((den,) * 4, (sn * den,) * 2 + (den,) * 2, (den,) * 2 + (cn * den,) * 2)
        for vertex, row, factors in zip(vertices, polynomials, multipliers, strict=True):
            margins = (
                F(1, 2) + point_u - vertex[0],
                F(1, 2) - point_u + vertex[0],
                F(1, 2) + point_v - vertex[1],
                F(1, 2) - point_v + vertex[1],
            )
            for polynomial, margin, factor in zip(row, margins, factors, strict=True):
                assert evaluate(polynomial, t) == margin * factor
    for polynomial in (d, c, s):
        assert certify_nonnegative(polynomial, F(-1, 4), F(1, 4)).proved


def test_toy_triangle_is_nonvacuous_and_bernstein_covers_both_closed_slabs() -> None:
    radius = F(1, 100)
    rows = list(near.triangle_obligations(TOY_SIDE, TOY_POINT, low=-radius, high=F(0)))
    assert [index for index, _ in rows] == [(v, m) for v in range(3) for m in range(4)]
    assert all(proved for _, proved in rows)
    assert all(
        proved
        for _, proved in near.triangle_obligations(TOY_SIDE, TOY_POINT, low=F(0), high=radius)
    )
    d, c, s = near.chart_polynomials()
    cosine, sine = evaluate(c, F(0)), evaluate(s, F(0))
    assert evaluate(d, F(0)) == 1
    x, y = F(23, 16), F(23, 32)
    height = (cosine + sine) / 2
    assert height <= x <= TOY_SIDE - height
    assert height <= y <= TOY_SIDE - height
    assert 1 <= x <= TOY_SIDE / 2
    assert 0 <= y <= 1
    assert sine * (x - 1) + cosine * (1 - y) > F(1, 2)
    assert cosine * (TOY_SIDE / 2 - x) + sine * (1 - y) > F(1, 2)


def test_closed_triangle_helper_preserves_edges_point_and_empty_cases() -> None:
    cosine, sine = F(3, 5), F(4, 5)
    assert near.closed_triangle(cosine, sine, F(1), F(1), F(7, 5)) == ((F(1), F(1)),) * 3
    assert near.closed_triangle(cosine, sine, F(1), F(1), F(3, 2)) == ()
    vertices = near.closed_triangle(cosine, sine, F(1), F(1), F(1))
    assert vertices == ((F(1), F(1)), (F(1, 2), F(1)), (F(1), F(1, 3)))
    for first in vertices:
        for second in vertices:
            u, v = ((first[i] + second[i]) / 2 for i in range(2))
            assert u <= 1
            assert v <= 1
            assert sine * u + cosine * v >= 1
    with pytest.raises(ValueError, match="positive"):
        near.closed_triangle(F(0), F(1), F(1), F(1), F(1))


def test_genuine_negative_point_is_unresolved_without_dropping_obligations() -> None:
    point = (F(0), F(0))
    polys = near.triangle_polynomials(TOY_SIDE, point)
    assert evaluate(polys[0][0], F(0)) < 0
    rows = list(near.triangle_obligations(TOY_SIDE, point, low=F(-1, 100), high=F(0)))
    assert len(rows) == 12
    assert not rows[0][1]
    assert any(not proved for _, proved in rows)


def test_exact_input_and_chart_domain_refusals() -> None:
    for side in (True, 3.75, F(2), F(4), F(2**2049)):
        with pytest.raises(ValueError, match=r"Fraction|side|bit limit"):
            near.triangle_polynomials(side, TOY_POINT)  # pyright: ignore[reportArgumentType]
    with pytest.raises(ValueError, match="Fraction"):
        near.triangle_polynomials(TOY_SIDE, (True, F(1)))  # pyright: ignore[reportArgumentType]
    for low, high in ((F(1), F(0)), (F(-1, 3), F(0)), (F(0), F(1, 3))):
        with pytest.raises(ValueError, match="slab"):
            list(near.triangle_obligations(TOY_SIDE, TOY_POINT, low=low, high=high))


def test_mocked_target_dispatch_has_full_inventory_and_real_toy_proof(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(near, "target_input", lambda: (TOY_SIDE, TOY_POINT))
    result = near.run_target()
    assert result["status"] == "proved"
    assert result["inequalities_checked"] == 24
    assert result["unresolved"] == []
    assert near.parse_worker(json.dumps(result)) == result


def test_interrupted_prefix_preserves_second_slab_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(near, "target_input", lambda: (TOY_SIDE, TOY_POINT))
    seen = []

    def interrupted(_side, _point, *, low, high):
        seen.append((low, high))
        if low < 0:
            for vertex in range(3):
                for margin in range(4):
                    yield (vertex, margin), True
        else:
            yield (0, 0), False
            raise TimeoutError("toy alarm")

    monkeypatch.setattr(near, "triangle_obligations", interrupted)
    result = near.run_target()
    assert seen == list(near.SLABS)
    assert result["status"] == "unresolved"
    assert result["inequalities_checked"] == 13
    assert result["unresolved"] == [[1, 0, 0]]
    assert near.parse_worker(json.dumps(result)) == result


def test_omitted_or_reordered_obligations_cannot_complete_a_prefix(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(near, "target_input", lambda: (TOY_SIDE, TOY_POINT))
    calls = []

    def incomplete(_side, _point, *, low, high):
        calls.append((low, high))
        yield (0, 0), True
        yield (0, 1), False

    monkeypatch.setattr(near, "triangle_obligations", incomplete)
    result = near.run_target()
    assert calls == [near.SLABS[0]]
    assert result["status"] == "unresolved"
    assert result["inequalities_checked"] == 2
    assert result["unresolved"] == [[0, 0, 1]]
    assert near.parse_worker(json.dumps(result)) == result
    for index, proved in (((0, 1), True), ((False, 0), True), ((0, 0), 1)):

        def malformed(_side, _point, *, low, high, index=index, proved=proved):
            del low, high
            yield index, proved

        monkeypatch.setattr(near, "triangle_obligations", malformed)
        with pytest.raises(ValueError, match="frozen complete order"):
            near.run_target()


def test_worker_full_negative_toy_preserves_both_slab_failure_inventories(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(near, "target_input", lambda: (TOY_SIDE, (F(0), F(0))))
    result = near.run_target()
    assert result["status"] == "unresolved"
    assert result["inequalities_checked"] == 24
    assert {index[0] for index in result["unresolved"]} == {0, 1}
    assert near.parse_worker(json.dumps(result)) == result


def test_wire_refuses_mutations_incomplete_proof_and_noncanonical_prefixes() -> None:
    original = near.packet(2, [(0, 0, 1)])
    for change in (
        {"version": True},
        {"kind": "full-H036"},
        {"side": "3.878"},
        {"point": ["3/2", "1"]},
        {"vertices": ["E", "G", "F"]},
        {"half_angle_slabs": [["0", "110880/50803079"]]},
        {"status": "proved"},
        {"extra": 0},
        {"inequalities_checked": True},
        {"inequalities_checked": 24.0},
        {"inequalities_checked": 25},
        {"inequalities_checked": float("nan")},
        {"unresolved": [[0, 0, 2]]},
        {"unresolved": [[0, 0, True]]},
        {"unresolved": [[0, 0, 1], [0, 0, 0]]},
        {"unresolved": [[0, 0, 1], [0, 0, 1]]},
    ):
        with pytest.raises(ValueError, match="packet"):
            near.parse_worker(json.dumps(original | change))
    with pytest.raises(ValueError, match="duplicate"):
        near.parse_worker('{"version":1,"version":1}')
    with pytest.raises(ValueError, match="256 KiB"):
        near.parse_worker(" " * 262145)


def test_cli_requires_fixed_dispatch_and_refuses_overrides(tmp_path: Path) -> None:
    for args in (
        [],
        ["--source-control"],
        ["--target-a3", "--side", "3"],
        ["--target-a3", "--point", "1", "1"],
        ["--target-a3", "--sign-depth", "1"],
        ["--target-a3", "--timeout-seconds", "11"],
        ["--target-a3", "--worker", "--output", str(tmp_path / "p")],
        ["--target-a3", "--output", str(tmp_path / "p"), "--log", str(tmp_path / "p")],
    ):
        with pytest.raises(SystemExit) as error:
            near.main(args)
        assert error.value.code == 2


def test_worker_alarm_restores_handler_and_parent_timeout_is_not_proof(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    previous = signal.getsignal(signal.SIGALRM)
    alarms = []
    monkeypatch.setattr(near.signal, "alarm", alarms.append)
    monkeypatch.setattr(near, "run_target", lambda: near.packet(0, []))
    assert near.main(["--target-a3", "--worker"]) == 1
    assert alarms == [10, 0]
    assert signal.getsignal(signal.SIGALRM) == previous
    assert json.loads(capsys.readouterr().out)["status"] == "unresolved"
    calls = []

    def timeout(command, **kwargs):
        calls.append((command, kwargs["timeout"]))
        raise subprocess.TimeoutExpired(command, 10, output=b"{partial", stderr=b"toy alarm")

    monkeypatch.setattr(subprocess, "run", timeout)
    output, log = tmp_path / "p.json", tmp_path / "p.log"
    assert near.main(["--target-a3", "--output", str(output), "--log", str(log)]) == 1
    assert len(calls) == 1
    assert calls[0][1] == 10
    assert json.loads(output.read_text()) == near.packet(0, [])
    retained = json.loads(log.read_text())
    assert retained["child_exit_code"] is None
    assert retained["stdout"] == "{partial"
    assert retained["stderr"] == "toy alarm"


def test_parent_requires_zero_exit_and_complete_well_formed_packet(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    output, log = tmp_path / "p.json", tmp_path / "p.log"
    for payload, exit_code, expected in (
        (json.dumps(near.packet(24, [])), 0, 0),
        (json.dumps(near.packet(24, [])), 1, 1),
        (json.dumps(near.packet(23, [])), 0, 1),
        ("{truncated", 2, 2),
    ):

        def worker(command, payload=payload, exit_code=exit_code, **_kwargs):
            return subprocess.CompletedProcess(command, exit_code, payload, "toy stderr")

        monkeypatch.setattr(subprocess, "run", worker)
        assert (
            near.main(["--target-a3", "--output", str(output), "--log", str(log)]) == expected
        )
        assert json.loads(output.read_text())["status"] == (
            "proved" if expected == 0 else "unresolved"
        )
        retained = json.loads(log.read_text())
        assert retained["stdout"] == payload
        assert retained["child_exit_code"] == exit_code
