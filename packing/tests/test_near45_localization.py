"""Unrelated exact toys only; no actual H123 constructor or target signs."""

from __future__ import annotations

import json
import signal
from dataclasses import replace
from fractions import Fraction

import pytest

from devtools import near45_localization as local
from devtools.angle_tile_certificate import certify_nonnegative, evaluate
from sqpack.field import NumberField

F = Fraction
TOY_WIDTH = F(3, 4)


@pytest.fixture(autouse=True)
def forbid_target(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden():
        raise AssertionError("source-free test attempted the scientific constructor")

    monkeypatch.setattr(local, "target_input", forbidden)


def test_generic_coefficients_match_unrelated_trigonometric_identities() -> None:
    first, second = local.localization_polynomials(TOY_WIDTH)
    field = first[0].field
    r = field.alpha / 2
    assert field.alpha > 0
    assert field.alpha * field.alpha == 2
    assert all(coefficient.field is field for row in (first, second) for coefficient in row)
    for t in (F(-1, 20), F(-1, 100), F(0), F(1, 100), F(1, 20)):
        den = 1 + t * t
        c = r * (1 - 2 * t - t * t) / den
        s = r * (1 + 2 * t - t * t) / den
        assert c * c + s * s == 1
        assert evaluate(first, t) == den * (1 - TOY_WIDTH * (c + s / 2))
        assert evaluate(second, t) == den**2 * ((c + s) / 2 - TOY_WIDTH * s * (c + s / 2))
        assert evaluate(first, -t) == den * (1 - TOY_WIDTH * (s + c / 2))
        assert evaluate(second, -t) == den**2 * ((c + s) / 2 - TOY_WIDTH * c * (s + c / 2))
    assert tuple(map(len, (first, second))) == (3, 5)


def test_closed_sign_kernel_keeps_zero_and_refuses_interior_negative() -> None:
    assert certify_nonnegative((F(0),), F(-1), F(1)).proved
    assert certify_nonnegative((F(0), F(1), F(-1)), F(0), F(1)).proved
    assert not certify_nonnegative((F(3, 16), F(-1), F(1)), F(0), F(1)).proved


def test_field_embedding_and_mixed_field_refusals() -> None:
    negative = NumberField((1, 0, -2), ("-2", "-1"))
    with pytest.raises(ValueError, match="positive"):
        local.bernstein_coefficients((negative.alpha,), F(0), F(1))
    first = NumberField((1, 0, -2), ("1", "2"))
    second = NumberField((1, 0, -2), ("1", "2"))
    with pytest.raises(ValueError, match="different"):
        local.bernstein_coefficients((first.alpha, second.alpha), F(0), F(1))


def test_toy_positive_prefix_and_exact_coefficient_wire() -> None:
    result = local.check_width(TOY_WIDTH)
    assert result.proved
    assert [(item.slab, item.polynomial) for item in result.obligations] == [
        (0, "F"),
        (0, "G"),
        (1, "F"),
        (1, "G"),
    ]
    # Mocked evidence exercises serialization, not scientific coefficient identity.
    wire = local.packet(result)
    assert local.parse_packet(json.dumps(wire)) == wire
    assert wire["coefficients"]["F"][0] == ["1", "-9/16"]
    assert wire["half_angle_slabs"] == [["-110880/50803079", "0"], ["0", "110880/50803079"]]


def test_negative_toy_retains_all_four_obligations() -> None:
    result = local.check_width(F(99, 100))
    assert not result.proved
    assert len(result.obligations) == 4
    assert any(not item.proved for item in result.obligations)
    assert local.packet(result)["status"] == "unresolved"


@pytest.mark.parametrize("width", [True, 0.75, F(0), F(1), F(-1), F(2**2049)])
def test_generic_builder_refuses_nonexact_or_out_of_scope_inputs(width) -> None:
    with pytest.raises(ValueError, match=r"Fraction|width|bit cap"):
        local.localization_polynomials(width)


def test_timeout_and_error_keep_only_completed_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = local.certify_nonnegative
    calls = 0

    def interrupted(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 3:
            raise TimeoutError("toy interruption")
        return original(*args, **kwargs)

    monkeypatch.setattr(local, "certify_nonnegative", interrupted)
    result = local.check_width(TOY_WIDTH)
    assert len(result.obligations) == 2
    assert result.coefficients is not None
    assert not result.proved
    assert result.stop_reason.startswith("timeout:")
    assert local.parse_packet(json.dumps(local.packet(result)))["status"] == "unresolved"

    def broken(_width):
        raise ArithmeticError("toy construction failure")

    monkeypatch.setattr(local, "localization_polynomials", broken)
    result = local.check_width(TOY_WIDTH)
    assert result.coefficients is None
    assert result.obligations == ()
    assert not result.proved
    assert result.stop_reason.startswith("error:")


def test_missing_duplicate_reordered_and_false_entries_cannot_prove() -> None:
    result = local.check_width(TOY_WIDTH)
    first = result.obligations[0]
    for entries in (
        result.obligations[:-1],
        (first,) * 4,
        tuple(reversed(result.obligations)),
        (replace(first, proved=False), *result.obligations[1:]),
    ):
        assert not replace(result, obligations=entries).proved
    for position in range(4):
        value = local.packet(result)
        value["obligations"].pop(position)
        with pytest.raises(ValueError, match=r"obligation|positive status"):
            local.parse_packet(json.dumps(value))
    value = local.packet(result)
    value["obligations"][1] = value["obligations"][0]
    with pytest.raises(ValueError, match="obligation"):
        local.parse_packet(json.dumps(value))


def test_missing_bernstein_evidence_is_not_an_empty_positive_proof(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(local, "bernstein_coefficients", lambda *_args: ())
    result = local.check_width(TOY_WIDTH)
    assert not result.proved
    assert result.obligations == ()
    assert "inventory" in result.stop_reason


def test_wire_refuses_changed_identity_noncanonical_and_missing_evidence() -> None:
    result = local.check_width(TOY_WIDTH)
    for key, changed in (
        ("hypothesis", "H-119"),
        ("side", "4"),
        ("width", "1/2"),
        ("coefficient_basis", ["1", "sqrt2-negative"]),
        ("half_angle_slabs", [["0", "0"], ["0", "1/1000"]]),
        ("coefficients", None),
        ("version", True),
        ("stop_reason", "timeout"),
    ):
        with pytest.raises(ValueError, match=r"frozen|coefficients|version|positive status"):
            local.parse_packet(json.dumps(local.packet(result) | {key: changed}))
    value = local.packet(result)
    value["coefficients"]["F"][0][0] = "01"
    with pytest.raises(ValueError, match="canonical"):
        local.parse_packet(json.dumps(value))
    for raw in ('{"version":1,"version":1}', '{"version":NaN}', "x" * 65537):
        with pytest.raises(ValueError, match=r"duplicate|nonfinite|bounded"):
            local.parse_packet(raw)


def test_target_binding_refuses_changed_input_without_building_target(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(local, "target_input", lambda: TOY_WIDTH)
    result = local.run_target()
    assert result["status"] == "unresolved"
    assert result["coefficients"] is None
    assert result["obligations"] == []
    assert result["stop_reason"].startswith("refused:")


def test_cli_requires_explicit_dispatch_and_restores_alarm(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as error:
        local.main([])
    assert error.value.code == 2
    capsys.readouterr()
    mock_packet = local.packet(local.check_width(TOY_WIDTH))
    monkeypatch.setattr(local, "run_target", lambda: mock_packet)
    previous = signal.getsignal(signal.SIGALRM)
    assert local.main(["--target-h123"]) == 0
    assert signal.getsignal(signal.SIGALRM) is previous
    assert json.loads(capsys.readouterr().out) == mock_packet
    mock_packet = local.packet(local.Result(None, (), "toy incomplete"))
    assert local.main(["--target-h123"]) == 1
    output = capsys.readouterr()
    assert json.loads(output.out)["status"] == "unresolved"
    assert "toy incomplete" in output.err


def test_cli_timeout_before_receipt_cannot_claim_completed_work(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def interrupted():
        raise TimeoutError("toy serialization seam")

    monkeypatch.setattr(local, "run_target", interrupted)
    assert local.main(["--target-h123"]) == 1
    value = json.loads(capsys.readouterr().out)
    assert value["status"] == "unresolved"
    assert value["coefficients"] is None
    assert value["obligations"] == []
