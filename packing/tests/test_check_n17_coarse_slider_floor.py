"""Target-free controls for the independent coarse physical-pair lemma."""

from __future__ import annotations

import copy
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_n17_coarse_slider_floor as floor
from sqpack import retained_json


def layout(c: Q = Q(4, 5), s: Q = Q(3, 5)) -> exact.Layout:
    axes = {"u": (exact.point(c), exact.point(s))}
    centres = {label: (exact.point(0), exact.point(0)) for label in range(1, 18)}
    return exact.Layout(centres, axes, {}, {}, exact.point(5))


@pytest.fixture
def packet(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    monkeypatch.setattr(floor, "load_inputs", lambda _path: ({"synthetic": True}, layout()))
    return floor.generate(Path("synthetic-root.json"))


def test_symbolic_displacement_units_and_floor_rearrangement() -> None:
    symbolic = floor.symbolic_packet()
    assert symbolic["nominal_displacement"] == "x9*-x11*=tau0*u+v"
    assert symbolic["b_definition"] == "b=-v dot (x11-x11*)"
    assert symbolic["v"] == ["-s", "c"]
    assert symbolic["positive_v_projection"] == "cos(delta_i)*V-sin(delta_i)*U"
    assert "sec(delta)-1" in symbolic["surviving_row_rearrangement"]
    assert symbolic["nominal_corner_witness_used"] is False


def test_synthetic_guard_inventory_strict_headroom_and_scope(packet: dict[str, Any]) -> None:
    result = floor.check(packet, Path("synthetic"))
    assert result["floor_certified"] is True
    assert result["verification_passed"] is True
    assert len(packet["finite"]["omitted"]) == 6
    assert len(packet["finite"]["survivors"]) == 2
    assert {option["id"] for option in packet["finite"]["survivors"]} == {"9:v:1", "11:v:1"}
    assert all(Q(option["gap_upper"]) < 0 for option in packet["finite"]["omitted"])
    assert Q(result["floor"]) == -Q(1, 5000) - Q(3600, 24999999)
    assert Q(result["strict_headroom"]) == Q(6999999, 124999995000) > 0
    assert Q(result["floor"]) > -Q(1, 2500)
    assert result["physical_pair_non_overlap_required"] == [9, 11]
    assert result["H278_required"] is False
    assert result["BW_prime_required"] is False
    assert result["LP_relaxation_consequence"] is False
    assert result["leaf_predicate_checked"] is False
    assert result["global_coverage_certified"] is False


@pytest.mark.parametrize(
    "mutation",
    [
        "sign",
        "displacement",
        "missing",
        "one_sided",
        "circular",
        "H278",
        "BW",
        "root",
        "constant",
        "headroom",
        "floor",
        "witness",
    ],
)
def test_changed_premise_or_recipe_refused(packet: dict[str, Any], mutation: str) -> None:
    damaged = copy.deepcopy(packet)
    if mutation == "sign":
        damaged["finite"]["survivors"][0]["sign"] = -1
    elif mutation == "displacement":
        damaged["symbolic"]["nominal_displacement"] = "x11*-x9*=tau0*u+v"
    elif mutation == "missing":
        damaged["finite"]["omitted"].pop()
    elif mutation == "one_sided":
        damaged["coarse_domain"]["q11"][1] = "1/200"
    elif mutation == "circular":
        damaged["coarse_domain"]["b_independent_coarse"][0] = "-1/2500"
    elif mutation in {"H278", "BW"}:
        damaged["coarse_domain"][
            "H278_required" if mutation == "H278" else "BW_prime_required"
        ] = True
    elif mutation == "root":
        damaged["inputs"]["synthetic"] = False
    elif mutation == "constant":
        damaged["constants"]["sqrt2_upper"] = "7/5"
    elif mutation in {"headroom", "floor"}:
        damaged["finite"]["strict_headroom" if mutation == "headroom" else "floor"] = "1"
    else:
        damaged["finite"]["omitted"][0]["witness"] = "nominal corner"
    with pytest.raises(exact.AuditError):
        floor.check(damaged, Path("synthetic"))


def test_honest_wide_root_guard_inconclusive(packet: dict[str, Any]) -> None:
    packet["root_intervals"]["tau0"] = ["-1", "0"]
    result = floor.check(packet, Path("synthetic"))
    assert result["verification_passed"] is True
    assert result["floor_certified"] is False
    assert result["status"] == "inconclusive"


def test_synthetic_root_outside_guard_inconclusive(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        floor, "load_inputs", lambda _path: ({"synthetic": True}, layout(Q(3, 5), Q(4, 5)))
    )
    assert floor.check(floor.generate())["status"] == "inconclusive"


def test_root_interval_non_enclosure_refused(packet: dict[str, Any]) -> None:
    packet["root_intervals"]["tau0"] = ["-3/10", "-1/5"]
    with pytest.raises(exact.AuditError, match="does not enclose"):
        floor.check(packet)


def test_generated_packet_cannot_mutate_domain_or_cached_identity(
    packet: dict[str, Any],
) -> None:
    packet["coarse_domain"]["b_independent_coarse"][0] = "-1/2500"
    packet["symbolic"]["v"][0] = "s"
    assert floor.DOMAIN["b_independent_coarse"][0] == "-1/2"
    assert floor.symbolic_packet()["v"][0] == "-s"


def test_loader_checks_root_only_without_feature_receipt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[Path] = []

    def root(path: Path) -> tuple[dict[str, Any], exact.Layout, exact.Layout]:
        calls.append(path)
        return {"checked_root": True}, layout(), layout()

    def forbidden(*_args: Any, **_kwargs: Any) -> None:
        pytest.fail("feature/BW predicate must not be loaded")

    monkeypatch.setattr(floor.root_loader, "load_root", root)
    monkeypatch.setattr(floor.root_loader, "generate", forbidden)
    monkeypatch.setattr(floor.root_loader, "check", forbidden)
    inputs, _ = floor.load_inputs(Path("root.json"))
    assert calls == [Path("root.json")]
    assert inputs == {"root": {"checked_root": True}, "root_only_prerequisite": True}


def test_root_refusal_stops_generation(monkeypatch: pytest.MonkeyPatch) -> None:
    def refuse(_path: Path) -> None:
        raise exact.AuditError("synthetic root admission refused")

    monkeypatch.setattr(floor, "load_inputs", refuse)
    with pytest.raises(exact.AuditError, match="root admission"):
        floor.generate()


@pytest.mark.parametrize("mutation", ["duplicate", "missing", "wrong_angle"])
def test_finite_inventory_independently_refuses_incomplete_contract(
    monkeypatch: pytest.MonkeyPatch, mutation: str
) -> None:
    options = floor.sat_options()
    if mutation == "duplicate":
        options[-1] = options[0]
    elif mutation == "missing":
        options.pop()
    else:
        domain = copy.deepcopy(floor.DOMAIN)
        domain["q11"] = ["-1/200", "1/200"]
        monkeypatch.setattr(floor, "DOMAIN", domain)
    monkeypatch.setattr(floor, "sat_options", lambda: options)
    with pytest.raises(exact.AuditError):
        floor.finite_packet()


def test_rational_projection_envelopes_and_one_sided_floor() -> None:
    finite = floor.finite_packet()
    u_bound, v_lo, v_hi = Q(9, 25), *map(Q, finite["V_closed_bounds"])
    for u_projection in (-u_bound, -Q(1, 8)):
        for v_projection in (v_lo, v_hi):
            for q in (Q(-1, 200), Q(0), Q(1, 5000)):
                cosine, sine = (1 - q * q) / (1 + q * q), 2 * q / (1 + q * q)
                for sign in (-1, 1):
                    assert (
                        sign * (cosine * u_projection + sine * v_projection)
                        <= Q(finite["omitted"][0]["projection_upper"])
                        < 1
                    )
                negative_v = -(cosine * v_projection - sine * u_projection)
                omitted_v = next(row for row in finite["omitted"] if row["axis"] == "v")
                assert negative_v <= Q(omitted_v["projection_upper"]) < 1
                for ev in (-Q(1, 5000), Q(1, 5000)):
                    required_b = 1 / cosine - 1 + (sine / cosine) * u_projection - ev
                    assert required_b >= Q(finite["floor"])
    # A symmetric positive cap would violate the claimed floor; it is not silently allowed.
    q = Q(1, 200)
    cosine, sine = (1 - q * q) / (1 + q * q), 2 * q / (1 + q * q)
    assert 1 / cosine - 1 + (sine / cosine) * (-u_bound) - Q(1, 5000) < Q(finite["floor"])


def test_cli_fresh_roundtrip_and_tampered_floor(
    packet: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(floor, "provenance", lambda *_args: {"synthetic_sources": True})
    generated, replay = tmp_path / "certificate.json", tmp_path / "replay.json"
    assert floor.main(["--root", "synthetic-root.json", "--output", str(generated)]) == 0
    assert json.loads(capsys.readouterr().out)["floor_certified"] is True
    assert (
        floor.main(
            [
                "--root",
                "synthetic-root.json",
                "--certificate",
                str(generated),
                "--output",
                str(replay),
            ]
        )
        == 0
    )
    saved = exact.decode(replay.read_bytes())
    assert saved["checker"]["floor_certified"] is True
    assert saved["execution"]["root"] == "synthetic-root.json"
    assert saved["provenance"]["synthetic_sources"] is True
    assert saved["checker"]["leaf_predicate_checked"] is False
    capsys.readouterr()
    packet["finite"]["floor"] = "0"
    generated.write_text(retained_json.dumps(packet))
    assert floor.main(["--certificate", str(generated), "--output", str(replay)]) == 1
    assert exact.decode(replay.read_bytes())["status"] == "refused"
    capsys.readouterr()


def test_cli_honest_failed_guard_is_not_refusal(
    packet: dict[str, Any],
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(floor, "provenance", lambda *_args: {})
    packet["root_intervals"]["tau0"] = ["-1", "0"]
    saved = tmp_path / "wide.json"
    saved.write_text(retained_json.dumps(packet))
    assert floor.main(["--certificate", str(saved)]) == 1
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "inconclusive"
    assert result["verification_passed"] is True
    assert result["floor_certified"] is False
