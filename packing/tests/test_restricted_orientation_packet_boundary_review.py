"""Cold packet-boundary review using source-side toys and mocked alarms only.

No producer geometry is imported. The partial-negative toy deliberately replaces the
source formula binding: it tests conjunction semantics, not the original theorem.
"""

from __future__ import annotations

import json
import signal
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_restricted_orientation_discriminator as reader


def test_cli_alarm_interrupts_loading_and_restores_timer_and_handler(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    alarms: list[int] = []
    handlers: list[Any] = []
    previous = signal.SIG_IGN

    def set_handler(number: int, handler: Any) -> Any:
        assert number == signal.SIGALRM
        handlers.append(handler)
        return previous

    def blocked_load(path: Path) -> Any:
        assert path.name == "alarm-control.json"
        assert alarms == [10]
        handler = handlers[0]
        assert callable(handler)
        handler(signal.SIGALRM, None)
        raise AssertionError("the installed alarm handler did not stop the input read")

    def forbidden_check(*_args: Any) -> Any:
        raise AssertionError("timeout reached packet geometry or a decision")

    monkeypatch.setattr(reader.signal, "signal", set_handler)
    monkeypatch.setattr(reader.signal, "alarm", alarms.append)
    monkeypatch.setattr(reader, "load_packet", blocked_load)
    monkeypatch.setattr(reader, "check_packet", forbidden_check)
    monkeypatch.setattr(
        sys,
        "argv",
        ["reader", "alarm-control.json", "--source-control", "--producer-exit-code", "0"],
    )
    assert reader.main() == 1
    output = capsys.readouterr()
    assert json.loads(output.out) == {
        "decision": "unresolved",
        "reason": "independent replay exceeded ten seconds",
    }
    assert not output.err
    assert alarms == [10, 0]
    assert len(handlers) == 2
    assert handlers[-1] == previous


def test_cli_partial_negative_rejects_conjunction_without_accepting_unchecked_clauses(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    zero = Fraction(0)
    ten: tuple[reader.Point, ...] = tuple(
        ((Fraction(3) + Fraction(index, 100), zero), (Fraction(3), zero)) for index in range(10)
    )
    # The nine integer-grid points cover all axis-unit centers in this source side
    # (<4); three extra distinct points do not remove that coverage. At (1/2,1/2),
    # only the first point, (1,1), is hit, on the closed square's corner.
    twelve: tuple[reader.Point, ...] = (
        *(((Fraction(x), zero), (Fraction(y), zero)) for x in (1, 2, 3) for y in (1, 2, 3)),
        ((Fraction(3, 2), zero), (Fraction(3, 2), zero)),
        ((Fraction(3, 2), zero), (Fraction(5, 2), zero)),
        ((Fraction(5, 2), zero), (Fraction(3, 2), zero)),
    )

    def toy_formulas(
        side: reader.Quadratic,
    ) -> tuple[set[reader.Point], tuple[reader.Point, ...]]:
        assert side == (Fraction(2), Fraction(4, 3))
        return set(ten), twelve

    def encoded(points: tuple[reader.Point, ...]) -> list[list[str]]:
        return [[f"poly[{a},{b}]" for a, b in point] for point in points]

    packet: dict[str, Any] = {
        "kind": "restricted-orientation-auxiliary-discriminator",
        "mode": "source-control",
        "complete": False,
        "h036_outcome": "unresolved",
        "theorem_acceptance": False,
        "perturbed_angles_evaluated": False,
        "inputs": {
            "kind": "input",
            "mode": "source-control",
            "field": "Q(sqrt(2)), positive root in (1,2)",
            "container_side_power_basis": "poly[2,4/3]",
            "ten_points_power_basis": encoded(ten),
            "twelve_points_power_basis": encoded(twelve),
        },
        "obligations": {
            "axis_ten_cover": False,
            "localization": None,
            "forced_A1": None,
            "forced_A2": None,
            "forced_A3": None,
            "twelve_cover_0": True,
            "twelve_cover_45": None,
        },
        "checked_obligations": ["axis_ten_cover", "twelve_cover_0"],
        "unchecked_obligations": [
            "localization",
            "forced_A1",
            "forced_A2",
            "forced_A3",
            "twelve_cover_45",
        ],
        "cases": [{"angle_degrees": 0, "reachable_event_strata_by_dimension": [1, 0, 0]}],
        "obstructions": [
            {
                "obligation": "axis_ten_cover",
                "angle_degrees": 0,
                "center_power_basis": ["poly[1/2,0]", "poly[1/2,0]"],
                "square_side": "1",
                "square_semantics": "closed",
                "ten_membership_mask": 0,
                "twelve_membership_mask": 1,
                "strict_box_counterexample_established": False,
            }
        ],
    }
    path = tmp_path / "partial-toy.json"
    path.write_text(json.dumps(packet))
    monkeypatch.setattr(reader, "formulas", toy_formulas)
    monkeypatch.setattr(
        sys, "argv", ["reader", str(path), "--source-control", "--producer-exit-code", "1"]
    )
    assert reader.main() == 0
    output = capsys.readouterr()
    assert not output.err
    result = json.loads(output.out)
    assert result["decision"] == "rejected"
    assert result["verified_escapes"] == ["axis_ten_cover"]
    assert result["h036_outcome"] == "unresolved"
    assert result["standalone_exhaustive_certificate"] is False

    # A claimed negative without its witness cannot inherit the previous rejection.
    packet["obstructions"] = []
    path.write_text(json.dumps(packet))
    assert reader.main() == 2
    refused = capsys.readouterr()
    assert not refused.out
    assert "each failed clause requires one verified escape" in refused.err


def test_quadratic_signs_and_rotated_closed_boundary_use_exact_arithmetic() -> None:
    for a, b, expected in (
        ("0", "0", 0),
        ("0", "1", 1),
        ("0", "-1", -1),
        ("1", "0", 1),
        ("-1", "0", -1),
        ("1", "1", 1),
        ("-1", "-1", -1),
        ("3/2", "-1", 1),
        ("7/5", "-1", -1),
        ("-3/2", "1", -1),
        ("-7/5", "1", 1),
    ):
        assert reader.sign((Fraction(a), Fraction(b))) == expected
    one = (Fraction(1), Fraction(0))
    upper = (Fraction(1), Fraction(1, 4))
    lower = (Fraction(1), Fraction(-1, 4))
    points = (
        (upper, upper),
        ((Fraction(1001, 1000), Fraction(1, 4)), upper),
        (lower, lower),
        ((Fraction(999, 1000), Fraction(-1, 4)), lower),
    )
    assert reader.membership((one, one), points, 45) == 0b0101
