"""Controls for the standalone third-party package's verifier.

The package under `cases/n11_fractional_certificate/thirdparty/` is the one
artifact here written to be read and run by someone who trusts nothing else in
the repository: standard library only, CPython 3.8 or later, no import from
`sqpack`. Nothing in the suite decided it until this file, so a change that
broke it would have been found by a stranger rather than by a gate.

The modules are loaded by path, not imported as packages, because that is how a
reader runs them.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from types import ModuleType

import pytest

THIRDPARTY = (
    Path(__file__).resolve().parents[1] / "cases" / "n11_fractional_certificate" / "thirdparty"
)
VERIFY_PATH = THIRDPARTY / "verify.py"
FALSIFY_PATH = THIRDPARTY / "falsify.py"
CERTIFICATE_PATH = THIRDPARTY / "certificate.json"


def load_script(name: str, path: Path) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


verify = load_script("n11_thirdparty_verify", VERIFY_PATH)

# falsify.py prepends its own directory to sys.path so that its standalone
# `import verify` works when a reader runs it. Both import globals are restored
# afterwards so that loading it here cannot change what the rest of the test
# process imports.
_saved_path = list(sys.path)
_saved_verify = sys.modules.get("verify")
sys.modules.pop("verify", None)
try:
    falsify = load_script("n11_thirdparty_falsify", FALSIFY_PATH)
finally:
    sys.path[:] = _saved_path
    if _saved_verify is None:
        sys.modules.pop("verify", None)
    else:
        sys.modules["verify"] = _saved_verify


def base_record() -> dict[str, object]:
    """A minimal well-formed record; the conditions it fails are not the point."""

    return {
        "id": "degenerate-fixture",
        "n": 2,
        "outer_side": "1",
        "square_side": "1",
        "angle_limit": "1/2",
        "direction_steps": 1,
        "claim": "s(2) >= 1",
        "atoms": [["0", "0", "1"]],
    }


def write_record(tmp_path: Path, record: dict[str, object]) -> Path:
    path = tmp_path / "certificate.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    return path


def run_script(
    path: Path, *arguments: str, timeout: int = 60
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(path), *arguments],
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def test_a_duplicate_json_key_is_refused(tmp_path: Path) -> None:
    """JSON allows a repeated key and Python keeps the last; a checker must not.

    Otherwise a file can carry two values for `n` and be decided as whichever
    one it wrote second.
    """

    path = tmp_path / "duplicate.json"
    path.write_text(
        json.dumps(base_record()).replace('"n": 2', '"n": 2, "n": 3', 1), encoding="utf-8"
    )
    with pytest.raises(verify.CertificateFormatError, match="duplicate JSON object key 'n'"):
        verify.load(path)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("n", True, "must be a JSON integer"),
        ("n", "2", "must be a JSON integer"),
        ("direction_steps", 1.5, "inexact JSON number"),
        ("direction_steps", False, "must be a JSON integer"),
    ],
)
def test_an_integer_field_refuses_coercion_truncation_and_booleans(
    tmp_path: Path, field: str, value: object, message: str
) -> None:
    record = base_record()
    record[field] = value
    with pytest.raises(verify.CertificateFormatError, match=message):
        verify.load(write_record(tmp_path, record))


def test_an_atom_coordinate_must_be_an_exact_rational_string(tmp_path: Path) -> None:
    record = base_record()
    record["atoms"] = [[0, "0", "1"]]
    with pytest.raises(verify.CertificateFormatError, match=r"atoms\[0\]\[0\]"):
        verify.load(write_record(tmp_path, record))


def test_a_rational_may_not_carry_a_trailing_newline() -> None:
    """`$` matches before a trailing newline, so the anchored regex is not enough."""

    assert verify.rational("1/2") == Fraction(1, 2)
    with pytest.raises(ValueError, match="not an exact rational string"):
        verify.rational("1/2\n")


def test_atom_shape_is_settled_before_any_weight_is_indexed(tmp_path: Path) -> None:
    record = base_record()
    record["atoms"] = [["0", "0"]]
    with pytest.raises(verify.CertificateFormatError, match="three-element JSON array"):
        verify.load(write_record(tmp_path, record))

    # `decide` is also called on objects built in code, so the precondition has
    # to report a malformed row rather than raise IndexError out of P2.
    certificate = {
        "n": 2,
        "L": Fraction(1),
        "B": Fraction(1),
        "tangents": [Fraction(0), Fraction(1, 2)],
        "atoms": [(Fraction(0), Fraction(0))],
        "declared": {"claim": "s(2) >= 1"},
    }
    checks = {name: holds for name, _detail, holds in verify.preconditions(certificate)}
    assert checks["P4 every atom is an (x, y, weight) triple"] is False
    assert checks["P2 every weight is non-negative"] is False


def test_a_declared_bookkeeping_field_must_itself_be_an_exact_rational(tmp_path: Path) -> None:
    record = base_record()
    record["total_mass"] = "1.5"
    with pytest.raises(verify.CertificateFormatError, match="total_mass"):
        verify.load(write_record(tmp_path, record))


def test_the_cli_refuses_a_malformed_file_without_a_traceback(tmp_path: Path) -> None:
    record = base_record()
    record["atoms"] = [["0", "0"]]
    completed = run_script(VERIFY_PATH, str(write_record(tmp_path, record)))
    assert completed.returncode == 1
    assert "REFUSED: not a certificate of the expected shape" in completed.stdout
    assert "Traceback" not in completed.stdout + completed.stderr


def test_the_cli_separates_an_unreadable_path_from_a_refusal(tmp_path: Path) -> None:
    """A file that was never read is a usage error, not a verdict about a claim."""

    completed = run_script(VERIFY_PATH, str(tmp_path / "missing.json"))
    assert completed.returncode == 2
    assert "could not open" in completed.stdout
    assert "REFUSED" not in completed.stdout


@pytest.mark.parametrize("arguments", [("--audit",), ("--audit", "x"), ("--audit", "-1")])
def test_the_audit_flag_requires_a_non_negative_integer(
    tmp_path: Path, arguments: tuple[str, ...]
) -> None:
    completed = run_script(VERIFY_PATH, str(write_record(tmp_path, base_record())), *arguments)
    assert completed.returncode == 2
    assert "--audit requires a non-negative integer" in completed.stdout


def test_a_singleton_domain_is_evaluated_as_the_closed_placement_it_is() -> None:
    """At 2h = L there is one admissible centre and no open cell to reason about."""

    certificate = {
        "L": Fraction(1),
        "B": Fraction(1),
        "atoms": [(Fraction(0), Fraction(0), Fraction(1))],
        "tangents": [Fraction(0), Fraction(1, 2)],
    }
    c, s = verify.direction(Fraction(0))
    assert verify.least_covered_weight(certificate, c, s, [1], 1) == (
        Fraction(1),
        (Fraction(1, 2), Fraction(1, 2)),
        1,
    )


def test_a_direction_admitting_no_placement_is_accepted_and_says_it_decided_nothing() -> None:
    """2h > L is vacuous truth: no unit square containing such a B-square fits either."""

    certificate = {
        "L": Fraction(1),
        "B": Fraction(2),
        "atoms": [(Fraction(0), Fraction(0), Fraction(1))],
        "tangents": [Fraction(0), Fraction(1, 2)],
    }
    c, s = verify.direction(Fraction(0))
    assert verify.least_covered_weight(certificate, c, s, [1], 1) == (None, None, 0)

    (_name, detail, holds), worst = verify.condition_5(certificate, log=lambda *_args: None)
    assert holds is True
    assert worst is None
    assert "vacuous and nothing was decided" in detail


@pytest.mark.parametrize(("field", "wrong"), [("total_mass", "0"), ("least_cell_mass", "2")])
def test_a_declared_value_that_disagrees_with_the_replay_prevents_acceptance(
    field: str, wrong: str
) -> None:
    """A file wrong about its own numbers must not end in VERIFIED."""

    declared = {
        "angle_limit": "1/2",
        "claim": "s(2) >= 1",
        "total_mass": "1",
        "least_cell_mass": "1",
    }
    declared[field] = wrong
    certificate = {
        "id": "declaration-control",
        "n": 2,
        "L": Fraction(1),
        "B": Fraction(3, 5),
        "tangents": [Fraction(0), Fraction(1, 2)],
        "atoms": [(Fraction(1, 2), Fraction(1, 2), Fraction(1))],
        "declared": declared,
    }
    messages: list[str] = []
    accepted, _results = verify.decide(certificate, log=messages.append)
    assert accepted is False
    assert any(f"declared {field} disagrees with the replay" in message for message in messages)


def test_the_falsification_oracle_reports_a_wrong_verdict_and_a_wrong_condition() -> None:
    """The oracle has to fail when handed a passing result, or it guards nothing."""

    errors = falsify.expectation_errors(
        accepted=True,
        results={"P2 every weight is non-negative": ("fixture", True)},
        oracle=falsify.QUICK_EXPECTATION,
    )
    assert any("verdict" in error for error in errors)
    assert any("P2 was PASS" in error for error in errors)


def test_the_quick_negative_control_is_bounded_and_refused() -> None:
    """A negative weight is refused at P2, before any Condition 5 sweep is paid for."""

    completed = run_script(FALSIFY_PATH, "--quick", str(CERTIFICATE_PATH), timeout=30)
    assert completed.returncode == 0
    assert "expected refusal and P2 result confirmed" in completed.stdout
    assert "EXPECTATION FAILED" not in completed.stdout + completed.stderr


def test_falsify_declines_a_certificate_its_oracles_are_not_about(tmp_path: Path) -> None:
    completed = run_script(FALSIFY_PATH, str(write_record(tmp_path, base_record())), timeout=30)
    assert completed.returncode == 2
    assert "only decides this directory's certificate.json" in completed.stdout


@pytest.mark.exhaustive_exact
def test_the_package_decides_its_own_shipped_certificate() -> None:
    """The whole point of the package, run as a stranger would run it."""

    completed = run_script(VERIFY_PATH, str(CERTIFICATE_PATH), "--audit", "2", timeout=600)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "90546593 cells over 181 directions" in completed.stdout
    assert "least covered weight 50003/50000" in completed.stdout
    assert "VERIFIED: s(11) >= 19/5" in completed.stdout
