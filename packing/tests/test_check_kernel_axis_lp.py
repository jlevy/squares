"""Source-free controls for the independently authored objective-bound reader."""

from __future__ import annotations

import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_kernel_axis_lp as reader


@pytest.fixture(autouse=True)
def forbid_scientific_source(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden() -> object:
        raise AssertionError("scientific source must not run in source-free controls")

    monkeypatch.setattr(reader, "scientific_source", forbidden)


def grid_packet() -> dict[str, Any]:
    coordinates = ("3/4", "7/4", "11/4")
    return {
        "format": "bc264-axis-objective/v1",
        "source": "synthetic-axis-poses-v1",
        "side": "7/2",
        "poses": [[x, y] for x in coordinates for y in coordinates],
        "alpha": ["1/9"] * 9,
        "beta": [{"i": i, "j": j, "weight": "2/9"} for i in range(9) for j in range(i + 1, 9)],
        "bound": "9",
    }


def check_toy(packet: object, *, minimum_bound: Fraction = Fraction(9)) -> dict[str, object]:
    return reader.check_synthetic_packet(
        packet,
        side=Fraction(7, 2),
        poses=grid_packet()["poses"],
        minimum_bound=minimum_bound,
    )


def test_nine_grid_exact_objective_bound() -> None:
    result = check_toy(grid_packet())
    assert result["status"] == "verified_objective_bound"
    assert result["bound"] == "9"
    assert result["projected_psd_verified"] is True
    assert result["scientific_family_refuted"] is False


def test_nine_bound_does_not_refute_eleven() -> None:
    with pytest.raises(reader.KernelCertificateError, match="threshold"):
        check_toy(grid_packet(), minimum_bound=Fraction(11))


def test_singular_psd_and_zero_pivot_refusal() -> None:
    f = Fraction
    assert reader.check_psd(((f(0), f(0)), (f(0), f(1)))) == 1
    assert reader.check_psd(((f(1), f(1)), (f(1), f(1)))) == 1
    with pytest.raises(reader.KernelCertificateError, match="PSD"):
        reader.check_psd(((f(0), f(1)), (f(1), f(0))))
    with pytest.raises(reader.KernelCertificateError, match="PSD"):
        reader.check_psd(((f(1), f(2)), (f(2), f(1))))


def test_mixed_vector_projection_keeps_both_spatial_coordinates() -> None:
    f = Fraction
    left = tuple(map(f, (1, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4)))
    right = tuple(map(f, (1, 0, 0, 0, 0, 0, 0, 5, 6, 7, 8)))
    result = reader.projected_matrices((left, right), (f(0), f(0)), ((0, 1, f(2)),))
    assert result.t == ((f(34), f(62)), (f(62), f(106)))
    assert result.a[0][0] == 2


def test_exact_axis_feature_order_on_unrelated_pose() -> None:
    result = reader.axis_features((Fraction(5, 2), Fraction(3)), Fraction(4))
    assert result == tuple(
        map(Fraction, (1, "5/4", "1/4", 1, 0, "-3/4", "1/2", "1/2", 1, "1/2", "1/4"))
    )


@pytest.mark.parametrize("case", ["extra", "missing", "format", "source", "side", "bound"])
def test_envelope_and_bound_mutations(case: str) -> None:
    packet = grid_packet()
    if case == "extra":
        packet["gamma"] = []
    elif case == "missing":
        del packet["alpha"]
    elif case == "format":
        packet["format"] = "different/v1"
    elif case == "source":
        packet["source"] = "five-tight-axis-grids-v1"
    elif case == "side":
        packet["side"] = "15/4"
    else:
        packet["bound"] = "11"
    with pytest.raises(reader.KernelCertificateError):
        check_toy(packet)


@pytest.mark.parametrize("case", ["drop", "duplicate", "reverse", "change", "wall", "width"])
def test_full_pose_identity_and_containment(case: str) -> None:
    packet = grid_packet()
    if case == "drop":
        packet["poses"].pop()
    elif case == "duplicate":
        packet["poses"][1] = packet["poses"][0]
    elif case == "reverse":
        packet["poses"].reverse()
    elif case == "change":
        packet["poses"][0][0] = "4/5"
    elif case == "wall":
        packet["poses"][0][0] = "0"
    else:
        packet["poses"][0].append("0")
    with pytest.raises(reader.KernelCertificateError):
        check_toy(packet)


@pytest.mark.parametrize(
    "case", ["bool", "diagonal", "reverse", "duplicate", "zero", "negative", "extra"]
)
def test_sparse_pair_admission(case: str) -> None:
    packet = grid_packet()
    first = packet["beta"][0]
    if case == "bool":
        first["i"] = False
    elif case == "diagonal":
        first["j"] = first["i"]
    elif case == "reverse":
        packet["beta"].reverse()
    elif case == "duplicate":
        packet["beta"].insert(1, deepcopy(first))
    elif case == "zero":
        first["weight"] = "0"
    elif case == "negative":
        first["weight"] = "-2/9"
    else:
        first["unused"] = 0
    with pytest.raises(reader.KernelCertificateError):
        check_toy(packet)


@pytest.mark.parametrize(
    "raw", ["0.0", "NaN", "1/0", "01", "+1", "-0", "2/2", "1/1", " 1", "1e0", True, 1]
)
def test_rationals_are_canonical_strings(raw: object) -> None:
    packet = grid_packet()
    packet["alpha"][0] = raw
    with pytest.raises(reader.KernelCertificateError):
        check_toy(packet)


def test_bit_size_and_inventory_limits() -> None:
    packets = [grid_packet() for _ in range(5)]
    packets[0]["alpha"][0] = "9" * (reader.MAX_CERTIFICATE_CHARS + 1)
    packets[1]["alpha"][0] = str(1 << reader.MAX_CERTIFICATE_BITS)
    packets[2]["poses"][0][0] = str(1 << reader.MAX_SOURCE_BITS)
    packets[3]["poses"] = [["1", "1"]] * (reader.MAX_POSES + 1)
    packets[4]["beta"] = [packets[4]["beta"][0]] * (reader.MAX_PAIRS + 1)
    for packet in packets:
        with pytest.raises(reader.KernelCertificateError):
            check_toy(packet)
    with pytest.raises(reader.KernelCertificateError, match="arithmetic"):
        reader.check_psd(((Fraction(1 << reader.MAX_ARITHMETIC_BITS),),))


def test_alpha_normalization_and_length_are_exact() -> None:
    for replacement in ([], ["1/8"] * 9, ["-1/9"] + ["1/9"] * 8):
        packet = grid_packet()
        packet["alpha"] = replacement
        with pytest.raises(reader.KernelCertificateError, match="alpha"):
            check_toy(packet)


def test_caller_fraction_limits_precede_decimal_rendering() -> None:
    packet = grid_packet()
    with pytest.raises(reader.KernelCertificateError, match="caller rational bit"):
        reader.check_synthetic_packet(packet, side=Fraction(1 << 20000), poses=packet["poses"])


def two_pose_packet(
    second: list[str], *, weight: str = "1", bound: str = "2"
) -> dict[str, Any]:
    return {
        "format": "bc264-axis-objective/v1",
        "source": "synthetic-axis-poses-v1",
        "side": "4",
        "poses": [["1", "1"], second],
        "alpha": ["1/2", "1/2"],
        "beta": [{"i": 0, "j": 1, "weight": weight}],
        "bound": bound,
    }


@pytest.mark.parametrize("second", [["2", "1"], ["2", "2"], ["9/4", "1"]])
def test_closed_touching_and_gap_pairs_are_compatible(second: list[str]) -> None:
    packet = two_pose_packet(second)
    result = reader.check_synthetic_packet(
        packet, side=Fraction(4), poses=packet["poses"], minimum_bound=Fraction(2)
    )
    assert result["bound"] == "2"


def test_overlapping_pair_cannot_be_weighted() -> None:
    packet = two_pose_packet(["3/2", "1"])
    with pytest.raises(reader.KernelCertificateError, match="overlapping"):
        reader.check_synthetic_packet(
            packet, side=Fraction(4), poses=packet["poses"], minimum_bound=Fraction(2)
        )


def test_projected_negative_scalar_is_refused() -> None:
    packet = two_pose_packet(["1", "3"], weight="2", bound="3")
    with pytest.raises(reader.KernelCertificateError, match="scalar"):
        reader.check_synthetic_packet(
            packet, side=Fraction(4), poses=packet["poses"], minimum_bound=Fraction(2)
        )


def test_changed_dual_must_still_have_psd_projection() -> None:
    packet = grid_packet()
    pair = next(row for row in packet["beta"] if (row["i"], row["j"]) == (0, 4))
    pair["weight"] = "1/3"
    packet["bound"] = "82/9"
    with pytest.raises(reader.KernelCertificateError, match="PSD"):
        check_toy(packet)


def test_sparse_zero_omissions_and_wall_contact() -> None:
    packet = two_pose_packet(["2", "1"])
    packet["poses"] = [["1/2", "1/2"], ["7/2", "7/2"]]
    packet["alpha"] = ["1", "0"]
    packet["beta"] = []
    packet["bound"] = "1"
    result = reader.check_synthetic_packet(
        packet, side=Fraction(4), poses=packet["poses"], minimum_bound=Fraction(1)
    )
    assert result["pair_count"] == 0


def test_reader_does_not_mutate_its_source_or_packet() -> None:
    packet = grid_packet()
    before = deepcopy(packet)
    check_toy(packet)
    assert packet == before


def test_bounded_json_and_fixed_cli_refusal(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "packet.json"
    packet = grid_packet()
    path.write_text(json.dumps(packet), encoding="utf-8")
    assert reader.load_packet(path) == packet
    assert reader.main(["--input", str(path)]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "source" in captured.err
    with pytest.raises(SystemExit):
        reader.main(["--input", str(path), "--minimum-bound", "9"])
    capsys.readouterr()


@pytest.mark.parametrize(
    "text", ['{"a":1,"a":2}', '{"x":NaN}', '{"x":0.1}', '{"i":12345}', "[" * 9 + "]" * 9, "{"]
)
def test_json_lexical_and_nesting_refusals(tmp_path: Path, text: str) -> None:
    path = tmp_path / "invalid.json"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(reader.KernelCertificateError):
        reader.load_packet(path)


def test_json_byte_limit_and_nonregular_input(tmp_path: Path) -> None:
    path = tmp_path / "large.json"
    path.write_bytes(b" " * (reader.MAX_INPUT_BYTES + 1))
    with pytest.raises(reader.KernelCertificateError, match="byte"):
        reader.load_packet(path)
    assert reader.main(["--input", str(tmp_path)]) == 2
