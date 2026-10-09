"""Synthetic root/cap arithmetic and custody controls; no accepted-root target reads."""

from __future__ import annotations

import copy
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_n17_capture_cap as cap


def inputs() -> dict[str, Any]:
    return {
        "root_path": "synthetic.json",
        "root_reference": {"synthetic": True},
        "root_search_box": {"midpoint": ["2/5", "1/4"]},
        "root_inclusion_box_used": [["2/5", "2/5"], ["1/4", "1/4"]],
        "root_verification_passed": True,
    }


@pytest.fixture
def packet(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    side = exact.point(cap.formula(Q(2, 5)))
    monkeypatch.setattr(cap, "load_inputs", lambda _path: (inputs(), side))
    return cap.generate(Path("synthetic.json"))


def test_symbolic_layout_identity_derivative_and_upper_excess() -> None:
    symbolic = cap.symbolic_packet()
    assert symbolic["F"] == "(6+4*t)/(1+2*t-t^2)"
    assert symbolic["F_prime"] == "4*(t^2+3*t-2)/(1+2*t-t^2)^2"
    assert symbolic["endpoint_layout_side_identity"] is True
    assert symbolic["beta_independent"] is True
    assert symbolic["all_root_upper_excess"] == "cap-side.lo"
    assert symbolic["interval_overlap_used_as_identity"] is False


def test_generic_synthetic_point_cap_certifies_both_boxes() -> None:
    t = exact.point(Q(2, 5))
    side = cap.formula(t[0])
    result = cap.finite_bounds(t, exact.point(side), cap=side + cap.EPSILON / 2)
    assert result["cap_certified"] is True
    assert all(result["guards"].values())
    assert result["excess"]["monotone_minimum_excess"] == str(cap.EPSILON / 2)
    assert result["excess"]["consumer_maximum_excess"] == str(cap.EPSILON / 2)


@pytest.mark.parametrize("adversary", ["monotone", "consumer"])
def test_upper_excess_uses_lower_side_endpoint(adversary: str) -> None:
    t = (Q(2, 5), Q(2, 5) + Q(1, 10**11)) if adversary == "monotone" else exact.point(Q(2, 5))
    lower, upper = cap.formula(t[1]), cap.formula(t[0])
    consumer = (lower, upper) if adversary == "monotone" else (lower - 2 * cap.EPSILON, upper)
    candidate = upper + cap.EPSILON / 2
    assert 0 < candidate - consumer[1] <= cap.EPSILON
    assert candidate - consumer[0] > cap.EPSILON
    result = cap.finite_bounds(t, consumer, cap=candidate)
    assert result["cap_certified"] is False
    assert result["guards"]["both_all_root_excesses_within_allowance"] is False


@pytest.mark.parametrize(
    "failure",
    ["zero_gap", "above_outer", "not_enclosure", "nonmonotone", "nonpositive_t", "t_one"],
)
def test_honest_failed_finite_guard_is_uncertified(failure: str) -> None:
    t = exact.point(Q(2, 5))
    side = cap.formula(t[0])
    consumer, candidate = exact.point(side), side + cap.EPSILON / 2
    if failure == "zero_gap":
        candidate = side
    elif failure == "above_outer":
        candidate = cap.OUTER_CAP + 1
    elif failure == "not_enclosure":
        consumer = side + cap.EPSILON / 4, side + cap.EPSILON / 4
    elif failure == "nonmonotone":
        t = exact.point(Q(3, 5))
    elif failure == "nonpositive_t":
        t = exact.point(Q(0))
    else:
        t = exact.point(Q(1))
    assert cap.finite_bounds(t, consumer, cap=candidate)["cap_certified"] is False


def test_full_synthetic_packet_is_honestly_inconclusive(packet: dict[str, Any]) -> None:
    # The test root is deliberately unrelated to the accepted endpoint. The fixed
    # scientific cap must not be tuned to make this synthetic root pass.
    assert packet["constants"] == cap.CONSTANTS
    result = cap.check(packet, Path("synthetic.json"))
    assert result["verification_passed"] is True
    assert result["status"] == "inconclusive"
    assert result["cap_certified"] is False
    assert all(result[name] is False for name in cap.FALSE_FLAGS)


@pytest.mark.parametrize(
    "mutation",
    ["cap", "outer", "epsilon", "root", "root_box", "side", "sign", "pass", "capture", "extra"],
)
def test_changed_constants_root_formula_or_claim_refused(
    packet: dict[str, Any], mutation: str
) -> None:
    damaged = copy.deepcopy(packet)
    if mutation in {"cap", "outer", "epsilon"}:
        field = {
            "cap": "numeric_capture_cap",
            "outer": "outer_cover_cap",
            "epsilon": "maximum_all_root_excess",
        }[mutation]
        damaged["constants"][field] = "1"
    elif mutation == "root":
        damaged["inputs"]["root_path"] = "other.json"
    elif mutation == "root_box":
        damaged["inputs"]["root_inclusion_box_used"][0][0] = "1/3"
    elif mutation == "side":
        value = Q(damaged["finite"]["consumer_side_enclosure"][0])
        damaged["finite"]["consumer_side_enclosure"][0] = str(value + Q(1, value.denominator))
    elif mutation == "sign":
        damaged["symbolic"]["F_prime"] = "positive"
    elif mutation == "pass":
        damaged["finite"]["cap_certified"] = True
    elif mutation == "capture":
        damaged["capture_proved"] = True
    else:
        damaged["extra"] = True
    with pytest.raises(exact.AuditError, match="custody differs"):
        cap.check(damaged, Path("synthetic.json"))


def test_mutation_does_not_poison_cached_identity(packet: dict[str, Any]) -> None:
    packet["symbolic"]["F"] = "altered"
    assert cap.symbolic_packet()["F"] == "(6+4*t)/(1+2*t-t^2)"
    with pytest.raises(exact.AuditError):
        cap.check(packet)


def test_failed_root_prerequisite_stops_before_bounds(monkeypatch: pytest.MonkeyPatch) -> None:
    layout = exact.Layout({}, {}, {}, {}, exact.point(Q(5)))
    bad = inputs()
    bad["root_verification_passed"] = False
    monkeypatch.setattr(cap.root_loader, "load_root", lambda _path: (bad, layout, layout))
    with pytest.raises(exact.AuditError, match="prerequisite"):
        cap.generate(Path("synthetic"))


def test_root_loader_side_and_complete_domain_are_retained(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    side = Q(4), Q(5)
    layout = exact.Layout({}, {}, {}, {}, side)
    monkeypatch.setattr(cap.root_loader, "load_root", lambda _path: (inputs(), layout, layout))
    packet = cap.generate(Path("synthetic"))
    assert packet["inputs"]["root_inclusion_box_used"] == inputs()["root_inclusion_box_used"]
    assert packet["finite"]["consumer_side_enclosure"] == ["4", "5"]
    assert packet["finite"]["cap_certified"] is False


def test_cli_roundtrip_refuses_one_unit_tamper(
    packet: dict[str, Any],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert packet["finite"]["cap_certified"] is False
    monkeypatch.setattr(cap, "provenance", lambda *_args: {"synthetic": True})
    certificate, replay = tmp_path / "certificate.json", tmp_path / "replay.json"
    assert cap.main(["--root", "synthetic", "--output", str(certificate)]) == 1
    saved = exact.decode(certificate.read_bytes())
    assert saved["checker"]["status"] == "inconclusive"
    assert (
        cap.main(
            ["--root", "synthetic", "--certificate", str(certificate), "--output", str(replay)]
        )
        == 1
    )
    assert exact.decode(replay.read_bytes())["checker"] == saved["checker"]
    damaged = copy.deepcopy(saved)
    damaged["constants"]["numeric_capture_cap"] = str(cap.CAP + Q(1, cap.CAP.denominator))
    certificate.write_text(json.dumps(damaged))
    assert (
        cap.main(
            ["--root", "synthetic", "--certificate", str(certificate), "--output", str(replay)]
        )
        == 1
    )
    assert exact.decode(replay.read_bytes())["status"] == "refused"
    capsys.readouterr()
