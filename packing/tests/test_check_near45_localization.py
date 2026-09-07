"""Source-free polynomial controls; no H-123 target construction or evaluation."""

from __future__ import annotations

import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_near45_localization as reader


@pytest.fixture(autouse=True)
def forbid_target(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args: object) -> reader.Specification:
        raise AssertionError("target F/G reconstruction is forbidden in source-free controls")

    monkeypatch.setattr(reader, "reconstruct_target", forbidden)
    generic_constructor = reader.guard_polynomials

    def source_free_constructor(field: Any, width: Fraction) -> dict[str, reader.Polynomial]:
        assert width != Fraction(939, 1000), "frozen target width is forbidden in controls"
        return generic_constructor(field, width)

    monkeypatch.setattr(reader, "guard_polynomials", source_free_constructor)


def toy_specification() -> reader.Specification:
    field = reader.make_field()
    width = Fraction(1, 3)
    return reader.Specification(
        field,
        Fraction(8, 3),
        width,
        ((Fraction(-1, 8), Fraction(0)), (Fraction(0), Fraction(1, 8))),
        reader.guard_polynomials(field, width),
    )


def encode(poly: reader.Polynomial) -> list[list[str]]:
    return [[str(coefficient) for coefficient in value.coeffs] for value in poly]


def packet(spec: reader.Specification) -> dict[str, Any]:
    obligations = []
    for slab_index, (lower, upper) in enumerate(spec.slabs):
        for name in ("F", "G"):
            coefficients = reader.bernstein(spec.polynomials[name], lower, upper)
            obligations.append(
                {
                    "slab": slab_index,
                    "polynomial": name,
                    "bernstein": encode(coefficients),
                    "proved": True,
                }
            )
    return {
        "version": 1,
        "kind": "fixed-side-near45-localization-overlap",
        "hypothesis": "H-123",
        "side": str(spec.side),
        "width": str(spec.width),
        "coefficient_basis": ["1", "sqrt2-positive"],
        "half_angle_slabs": [[str(value) for value in slab] for slab in spec.slabs],
        "coefficients": {name: encode(poly) for name, poly in spec.polynomials.items()},
        "obligations": obligations,
        "status": "proved",
        "stop_reason": "complete",
    }


def test_exact_bernstein_conversion_retains_closed_zero_endpoints() -> None:
    field = reader.make_field()
    assert reader.bernstein((field.one, field.one), Fraction(-1), Fraction(1)) == (
        field.zero,
        2 * field.one,
    )
    # t^2 is nonnegative, but its degree-two certificate on [-1,1] is insufficient.
    assert reader.bernstein((field.zero, field.zero, field.one), Fraction(-1), Fraction(1)) == (
        field.one,
        -field.one,
        field.one,
    )


def test_symbolic_reconstruction_matches_independent_generic_coefficients() -> None:
    field = reader.make_field()
    root_half, width = field.alpha / 2, Fraction(2, 5)
    polynomials = reader.guard_polynomials(field, width)
    assert polynomials["F"] == (
        1 - 3 * width * root_half / 2,
        width * root_half,
        1 + 3 * width * root_half / 2,
    )
    assert polynomials["G"] == (
        root_half - 3 * width / 4,
        field.rational(-width),
        field.rational(5 * width / 2),
        field.rational(width),
        -root_half - 3 * width / 4,
    )


def test_bernstein_endpoint_values_and_both_slab_signs() -> None:
    field = reader.make_field()
    poly = (field.alpha, field.rational(-2), field.rational(3), field.rational(-1))
    for lower, upper in ((Fraction(-2, 3), Fraction(0)), (Fraction(0), Fraction(3, 4))):
        result = reader.bernstein(poly, lower, upper)
        for argument, value in ((lower, result[0]), (upper, result[-1])):
            assert value == sum(
                (coefficient * argument**i for i, coefficient in enumerate(poly)), field.zero
            )
    for lower, upper in ((Fraction(0), Fraction(0)), (Fraction(1), Fraction(-1))):
        with pytest.raises(reader.GuardError):
            reader.bernstein(poly, lower, upper)


def test_complete_toy_certificate_checks_all_four_obligations_and_16_coefficients() -> None:
    spec = toy_specification()
    result = reader.check_packet(packet(spec), expected=spec)
    assert result["status"] == "proved"
    assert result["obligations_checked"] == 4
    assert result["bernstein_coefficients_checked"] == 16
    assert result["complete"] is True
    assert result["unresolved"] == []


def test_complete_zero_guard_accepts_closed_boundary_equality() -> None:
    spec = toy_specification()
    zero = spec.field.zero
    changed = replace(spec, polynomials={"F": (zero,) * 3, "G": (zero,) * 5})
    result = reader.check_packet(packet(changed), expected=changed)
    assert result["status"] == "proved"
    assert result["bernstein_coefficients_checked"] == 16


def test_negative_sufficient_coefficient_is_unresolved_even_for_nonnegative_polynomial() -> (
    None
):
    spec = toy_specification()
    field = spec.field
    changed = replace(
        spec,
        slabs=((Fraction(-1), Fraction(1)), (Fraction(1), Fraction(2))),
        polynomials={
            "F": (field.zero, field.zero, field.one),
            "G": (field.one, field.zero, field.zero, field.zero, field.zero),
        },
    )
    with pytest.raises(reader.GuardError, match="sufficient Bernstein guard"):
        reader.check_packet(packet(changed), expected=changed)


def test_incomplete_duplicate_or_foreign_packets_never_reconstruct_target() -> None:
    spec = toy_specification()
    bad: list[Any] = [None, [], {}, packet(spec)]
    for key, value in (
        ("version", True),
        ("hypothesis", "H-122"),
        ("coefficient_basis", ["1", "sqrt2-negative"]),
        ("coefficients", None),
        ("status", "unresolved"),
        ("stop_reason", "timeout"),
        ("side", "8/3.0"),
        ("obligations", []),
        ("half_angle_slabs", []),
    ):
        raw = packet(spec)
        raw[key] = value
        bad.append(raw)
    raw = packet(spec)
    raw["obligations"][1] = raw["obligations"][0]
    bad.append(raw)
    raw = packet(spec)
    raw["side"], raw["width"] = "1939/500", "939/1000"
    raw["half_angle_slabs"] = [["-110880/50803079", "0"], ["0", "110880/50803079"]]
    raw["obligations"].pop()
    bad.append(raw)
    for raw in bad:
        with pytest.raises(reader.GuardError):
            reader.check_target_packet(raw)


def test_claimed_booleans_and_coefficients_are_not_evidence() -> None:
    spec = toy_specification()
    changed = []
    for index in range(4):
        raw = packet(spec)
        raw["obligations"][index]["proved"] = False
        changed.append(raw)
        raw = packet(spec)
        raw["obligations"][index]["bernstein"][0] = ["99", "0"]
        changed.append(raw)
    raw = packet(spec)
    raw["coefficients"]["F"][0] = ["99", "0"]
    changed.append(raw)
    raw = packet(spec)
    raw["coefficients"]["G"].pop()
    changed.append(raw)
    for raw in changed:
        with pytest.raises(reader.GuardError):
            reader.check_packet(raw, expected=spec)


def test_basis_lengths_rational_canonicalization_and_slab_identity() -> None:
    spec = toy_specification()
    for value in (["1"], [True, "0"], ["1.0", "0"], ["2/2", "0"], ["1/0", "0"]):
        raw = packet(spec)
        raw["coefficients"]["F"][0] = value
        with pytest.raises(reader.GuardError):
            reader.check_packet(raw, expected=spec)
    raw = packet(spec)
    raw["half_angle_slabs"][0][0] = "-1/9"
    with pytest.raises(reader.GuardError):
        reader.check_packet(raw, expected=spec)


def test_cli_success_and_unresolved_paths_are_source_free(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    spec = toy_specification()
    monkeypatch.setattr(
        reader, "check_target_packet", lambda raw: reader.check_packet(raw, expected=spec)
    )
    source = tmp_path / "toy.json"
    source.write_text(json.dumps(packet(spec)), encoding="utf-8")
    assert reader.main(["--input", str(source)]) == 0
    captured = capsys.readouterr()
    assert json.loads(captured.out)["status"] == "proved"
    assert captured.err == ""
    for content in (
        '{"version":',
        '{"version":1,"version":1}',
        " " * (reader.MAX_PACKET_BYTES + 1),
        json.dumps({**packet(spec), "status": "unresolved"}),
    ):
        source.write_text(content, encoding="utf-8")
        assert reader.main(["--input", str(source)]) == 2
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result["status"] == "unresolved"
        assert result["complete"] is False
        assert captured.err
