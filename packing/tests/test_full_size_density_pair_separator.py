"""Source and toy controls only; never evaluate exp-113 candidate pair geometry."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_full_size_density_pair_separator as checker
from devtools import run_full_size_density_pair_separator as runner
from devtools.check_full_size_density_pair_separator import control_family, replay_packet
from devtools.run_full_size_density_pair_separator import make_packet
from sqpack.field import NumberField
from sqpack.full_size_density import pair_separator
from sqpack.full_size_density.pair_separator import eligible_pairs, make_family, separate
from sqpack.full_size_density.support_ceiling import SupportError, axis_square


def test_strict_overlap_produces_a_positive_box_but_contact_does_not() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    side = field.rational(3)
    first = axis_square(field.one, field.one)
    overlap = axis_square(field.rational("3/2"), field.one)
    family = make_family((first, overlap), side, (Fraction(1), Fraction(1, 2)))
    result = separate(family)
    assert result.eligible == 1
    assert result.witness is not None
    assert result.witness.radius > 0
    assert result.witness.excess == Fraction(1, 2)
    contact = axis_square(field.rational(2), field.one)
    no_hit = separate(make_family((first, contact), side, (Fraction(1), Fraction(1, 2))))
    assert no_hit.witness is None
    assert len(no_hit.separations) == 1


def test_toy_packet_replays_overlap_and_honest_no_hit_results() -> None:
    for source, expected in (
        ("toy-overlap-v1", "candidate-refuted"),
        ("toy-edge-v1", "no-pair-obstruction"),
        ("toy-corner-v1", "no-pair-obstruction"),
        ("toy-gap-v1", "no-pair-obstruction"),
        ("toy-equal-v1", "no-pair-obstruction"),
        ("toy-triple-v1", "no-pair-obstruction"),
        ("toy-prefix-v1", "candidate-refuted"),
        ("toy-narrow-overlap-v1", "candidate-refuted"),
        ("toy-algebraic-v1", "candidate-refuted"),
        ("toy-rotated-algebraic-v1", "candidate-refuted"),
    ):
        family = control_family(source)
        packet = make_packet(source, family, separate(family))
        assert replay_packet(packet) == expected


def test_triple_overweight_is_deliberately_outside_pair_completeness() -> None:
    family = control_family("toy-triple-v1")
    q = family.side.field.rational
    point = q("5/4"), q(1)
    for entry in family.placements:
        xs, ys = zip(*entry.square, strict=True)
        assert min(xs) < point[0] < max(xs)
        assert min(ys) < point[1] < max(ys)
    assert sum(entry.weight for entry in family.placements) == Fraction(6, 5)
    assert eligible_pairs(family) == ()
    assert separate(family).witness is None


def test_canonical_geometry_preserves_cyclic_and_reflected_corner_order() -> None:
    source = "toy-rotated-algebraic-v1"
    original = control_family(source)
    squares = tuple(
        tuple(reversed(entry.square[1:] + entry.square[:1])) for entry in original.placements
    )
    altered = make_family(
        squares, original.side, tuple(entry.weight for entry in original.placements)
    )
    assert checker.family_signature(altered) == checker.family_signature(original)
    assert replay_packet(make_packet(source, altered, separate(altered))) == "candidate-refuted"
    contact = control_family("toy-edge-v1")
    altered_contact = make_family(
        tuple(tuple(reversed(entry.square)) for entry in contact.placements),
        contact.side,
        tuple(entry.weight for entry in contact.placements),
    )
    assert (
        replay_packet(make_packet("toy-edge-v1", altered_contact, separate(altered_contact)))
        == "no-pair-obstruction"
    )
    rotated = make_family(
        tuple(
            tuple((contact.side - y, x) for x, y in entry.square)
            for entry in contact.placements
        ),
        contact.side,
        tuple(entry.weight for entry in contact.placements),
    )
    assert separate(rotated).witness is None


def test_strict_rational_sliver_is_not_rounded_to_contact() -> None:
    family = control_family("toy-narrow-overlap-v1")
    result = separate(family)
    assert result.witness is not None
    assert 0 < result.witness.radius < Fraction(1, 10**30)
    assert (
        replay_packet(make_packet("toy-narrow-overlap-v1", family, result))
        == "candidate-refuted"
    )


def test_first_witness_requires_the_entire_ordered_separated_prefix() -> None:
    packet = toy_packet("toy-prefix-v1")
    assert packet["eligible"] == 3
    assert len(packet["separations"]) == 2
    assert packet["witness"]["pair"] == [1, 2]
    assert replay_packet(packet) == "candidate-refuted"
    for records in (
        packet["separations"][:1],
        list(reversed(packet["separations"])),
        [packet["separations"][0]] * 2,
    ):
        altered = copy.deepcopy(packet)
        altered["separations"] = records
        with pytest.raises(SupportError, match="canonical eligible pair"):
            replay_packet(altered)


def test_duplicate_weight_is_not_added_and_bad_geometry_is_refused() -> None:
    family = control_family("toy-overlap-v1")
    square = family.placements[0].square
    duplicate = make_family(
        (square, tuple(reversed(square))), family.side, (Fraction(1), Fraction(1))
    )
    assert len(duplicate.placements) == 1
    assert duplicate.placements[0].weight == 1
    with pytest.raises(SupportError, match="inconsistent"):
        make_family((square, square), family.side, (Fraction(1), Fraction(1, 2)))
    with pytest.raises(SupportError, match="unit square"):
        make_family(
            ((square[0], square[2], square[1], square[3]),), family.side, (Fraction(1),)
        )
    bad_weights: tuple[Any, ...] = (True, -1, 0.5)
    for bad in bad_weights:
        with pytest.raises(SupportError, match="nonnegative exact"):
            make_family((square,), family.side, (bad,))


def toy_packet(source: str = "toy-overlap-v1") -> dict[str, Any]:
    family = control_family(source)
    return make_packet(source, family, separate(family))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("radius", "0"),
        ("radius", "-1"),
        ("radius", "10"),
        ("radius", "1e1000000000"),
        ("radius", "01"),
        ("radius", "2/4"),
        ("radius", True),
        ("radius", 0.5),
        ("radius", "1/0"),
        ("excess", "1"),
        ("point", [["1/2"], ["1"]]),
        ("point", [["1", "0"], ["1"]]),
        ("pair", [False, 1]),
        ("pair", [1, 0]),
    ],
)
def test_witness_tampering_is_refused(field: str, value: Any) -> None:
    packet = toy_packet()
    packet["witness"][field] = value
    with pytest.raises(SupportError):
        replay_packet(packet)


@pytest.mark.parametrize("value", [True, 1.0, "1", -1, 0, 2])
def test_eligible_count_requires_exact_canonical_integer(value: Any) -> None:
    packet = toy_packet()
    packet["eligible"] = value
    with pytest.raises(SupportError):
        replay_packet(packet)


def test_family_binding_and_complete_pair_coverage_are_not_trusted() -> None:
    for key, value in (("version", True), ("source", "unknown"), ("family", {})):
        packet = toy_packet()
        packet[key] = value
        with pytest.raises(SupportError):
            replay_packet(packet)
    packet = toy_packet()
    packet["family"]["placements"][0]["weight"] = "2"
    with pytest.raises(SupportError, match="binding"):
        replay_packet(packet)
    packet = toy_packet("toy-edge-v1")
    for axis in ([["0"], ["0"]], [["-1"], ["0"]], [["0"], ["1"]]):
        altered = copy.deepcopy(packet)
        altered["separations"][0]["axis"] = axis
        with pytest.raises(SupportError):
            replay_packet(altered)
    packet["separations"] = []
    with pytest.raises(SupportError, match="omits"):
        replay_packet(packet)


def test_checker_does_not_call_producer_sat_intersection_or_eligibility(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    witness = toy_packet("toy-rotated-algebraic-v1")
    contact = toy_packet("toy-edge-v1")

    def forbidden(*_args, **_kwargs):
        raise AssertionError("producer geometry or candidate mode called during replay")

    for name in ("separate", "separated", "eligible_pairs", "_intersection_center", "_forms"):
        monkeypatch.setattr(pair_separator, name, forbidden)
    monkeypatch.setattr(checker, "candidate_family", forbidden)
    assert replay_packet(witness) == "candidate-refuted"
    assert replay_packet(contact) == "no-pair-obstruction"


def test_exponent_refusal_precedes_fraction_conversion(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(_value):
        raise AssertionError("noncanonical exponent reached Fraction")

    monkeypatch.setattr(checker, "checked_rational", forbidden)
    with pytest.raises(SupportError, match="canonical"):
        checker.parse_rational("1e1000000000")


@pytest.mark.parametrize(
    ("source", "count", "pairs"),
    [
        ("trump-original-control-v1", 11, 55),
        ("trump-uniform-control-v1", 60, 6),
    ],
)
def test_exact_source_controls_never_invoke_candidate_weights(
    source: str, count: int, pairs: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    def forbidden(*_args, **_kwargs):
        raise AssertionError("target candidate must not run in a source control")

    monkeypatch.setattr(checker, "candidate_family", forbidden)
    monkeypatch.setattr(runner, "frozen_candidate", forbidden)
    family = control_family(source)
    assert len(family.placements) == count
    assert sum(entry.weight for entry in family.placements) == 11
    result = separate(family)
    assert result.eligible == pairs
    assert result.witness is None
    assert replay_packet(make_packet(source, family, result)) == "no-pair-obstruction"


def test_cli_modes_and_caps_refuse_before_any_target(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args, **_kwargs):
        raise AssertionError("unfunded worker was invoked")

    monkeypatch.setattr(runner, "worker", forbidden)
    for arguments in (
        [],
        ["--control", "toy-edge-v1", "--timeout-seconds", "31"],
        ["--control", "toy-edge-v1", "--candidate", "not-loaded.json"],
    ):
        with pytest.raises(SystemExit) as stopped:
            runner.main(arguments)
        assert stopped.value.code == 2
    with pytest.raises(SystemExit) as stopped:
        checker.main(["not-loaded.json", "--timeout-seconds", "31"])
    assert stopped.value.code == 2
    packet = toy_packet()
    packet["source"] = checker.CANDIDATE_SOURCE
    with pytest.raises(SupportError, match="requires the accepted parent"):
        replay_packet(packet)


@pytest.mark.parametrize(
    "source",
    ["toy-rotated-algebraic-v1", "trump-original-control-v1", "trump-uniform-control-v1"],
)
def test_cli_roundtrip_and_strict_json_reader(source: str, tmp_path: Path) -> None:
    command = [
        sys.executable,
        "-m",
        "devtools.run_full_size_density_pair_separator",
        "--control",
        source,
        "--timeout-seconds",
        "30",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False, timeout=30)
    assert completed.returncode == 0, completed.stderr
    packet = json.loads(completed.stdout)
    expected = "candidate-refuted" if source.startswith("toy-") else "no-pair-obstruction"
    assert replay_packet(packet) == expected
    path = tmp_path / "pair.json"
    path.write_text(completed.stdout)
    replay = subprocess.run(
        [sys.executable, "-m", "devtools.check_full_size_density_pair_separator", str(path)],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert replay.returncode == 0, replay.stderr
    assert json.loads(replay.stdout)["verdict"] == expected
    print(
        json.dumps(
            {
                "control": source,
                "producer": json.loads(completed.stderr),
                "checker": json.loads(replay.stderr),
            },
            sort_keys=True,
        )
    )
    for payload in ('{"version":1,"version":1}', '{"radius":0.5}', '{"radius":NaN}'):
        path.write_text(payload)
        with pytest.raises(SupportError):
            checker.load_packet(path)


@pytest.mark.parametrize("tool", [runner, checker])
def test_outer_process_cap_and_failure_never_publish_partial_output(
    tool: Any, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    arguments = ["--control", "toy-edge-v1"] if tool is runner else ["unused-control.json"]

    def timed_out(command, **options):
        assert options["timeout"] == 30
        assert "--worker" in command
        raise subprocess.TimeoutExpired(command, 30, output="partial")

    monkeypatch.setattr(tool.subprocess, "run", timed_out)
    assert tool.main(arguments) == 1
    captured = capsys.readouterr()
    assert not captured.out
    assert "unresolved" in captured.err

    def refused(command, **_options):
        return subprocess.CompletedProcess(
            command, 2, stdout="partial", stderr="refused control"
        )

    monkeypatch.setattr(tool.subprocess, "run", refused)
    assert tool.main(arguments) == 2
    captured = capsys.readouterr()
    assert not captured.out
    assert "refused control" in captured.err


def test_placement_and_eligible_pair_caps_are_explicit() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    squares = tuple(axis_square(q(1) + q(index) / 100, q(1)) for index in range(61))
    with pytest.raises(SupportError, match="placement cap"):
        make_family(squares, q(3), (Fraction(1),) * 61)
    family = make_family(squares[:17], q(3), (Fraction(1),) * 17)
    with pytest.raises(SupportError, match="eligible-pair cap"):
        eligible_pairs(family)
