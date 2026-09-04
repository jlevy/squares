"""Focused regressions for the standalone n=11 third-party verifier."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

THIRDPARTY = (
    Path(__file__).resolve().parents[1] / "cases" / "n11_fractional_certificate" / "thirdparty"
)
VERIFY_PATH = THIRDPARTY / "verify.py"
MINIMAL_VERIFY_PATH = THIRDPARTY.parent / "minimal_verify.py"
FALSIFY_PATH = THIRDPARTY / "falsify.py"
CERTIFICATE_PATH = THIRDPARTY / "certificate.json"
CURRENT_CERTIFICATE_PATH = THIRDPARTY.parent / "certificate.json"


def load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


verify = load_script("n11_thirdparty_verify", VERIFY_PATH)
minimal_verify = load_script("n11_minimal_verify", MINIMAL_VERIFY_PATH)

# falsify.py prepends its own directory so its standalone ``import verify``
# works.  Restore both import globals after loading it to avoid polluting the
# rest of the project test process.
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


def test_load_rejects_duplicate_keys(tmp_path: Path) -> None:
    text = json.dumps(base_record()).replace('"n": 2', '"n": 2, "n": 3', 1)
    path = tmp_path / "duplicate.json"
    path.write_text(text, encoding="utf-8")
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
def test_load_rejects_lossy_or_boolean_integer_coercion(
    tmp_path: Path, field: str, value: object, message: str
) -> None:
    record = base_record()
    record[field] = value
    with pytest.raises(verify.CertificateFormatError, match=message):
        verify.load(write_record(tmp_path, record))


def test_load_rejects_non_string_atom_numbers(tmp_path: Path) -> None:
    record = base_record()
    record["atoms"] = [[0, "0", "1"]]
    with pytest.raises(verify.CertificateFormatError, match=r"atoms\[0\]\[0\]"):
        verify.load(write_record(tmp_path, record))


def test_atom_shape_is_checked_before_weight_indexing(tmp_path: Path) -> None:
    record = base_record()
    record["atoms"] = [["0", "0"]]
    with pytest.raises(verify.CertificateFormatError, match="three-element JSON array"):
        verify.load(write_record(tmp_path, record))

    cert = {
        "id": "programmatic-malformed",
        "n": 2,
        "L": Fraction(1),
        "B": Fraction(1),
        "tangents": [Fraction(0), Fraction(1, 2)],
        "atoms": [(Fraction(0), Fraction(0))],
        "declared": {"claim": "s(2) >= 1"},
    }
    checks = {name: holds for name, _detail, holds in verify.preconditions(cert)}
    assert checks["P4 every atom is an (x, y, weight) triple"] is False


def test_cli_refuses_malformed_input_without_traceback(tmp_path: Path) -> None:
    record = base_record()
    record["atoms"] = [["0", "0"]]
    completed = subprocess.run(
        [sys.executable, str(VERIFY_PATH), str(write_record(tmp_path, record))],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 1
    assert "REFUSED: malformed certificate:" in completed.stdout
    assert "Traceback" not in completed.stdout + completed.stderr


def test_cli_distinguishes_an_unreadable_path_from_a_mathematical_refusal(
    tmp_path: Path,
) -> None:
    missing = tmp_path / "missing.json"
    completed = subprocess.run(
        [sys.executable, str(VERIFY_PATH), str(missing)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 2
    assert "could not open" in completed.stdout
    assert "REFUSED" not in completed.stdout
    assert "Traceback" not in completed.stdout + completed.stderr


def test_singleton_domain_is_evaluated_directly_and_closed() -> None:
    cert = {
        "L": Fraction(1),
        "B": Fraction(1),
        # At direction zero, (0, 0) lies on the boundary of the only square.
        "atoms": [(Fraction(0), Fraction(0), Fraction(1))],
        "tangents": [Fraction(0), Fraction(1, 2)],
    }
    c, s = verify.direction(Fraction(0))
    minimum, centre, regions = verify.least_covered_weight(cert, c, s, [1], 1)
    assert (minimum, centre, regions) == (Fraction(1), (Fraction(1, 2), Fraction(1, 2)), 1)

    (_name, detail, holds), worst = verify.condition_c4(cert, log=lambda *_args: None)
    assert holds is True
    assert worst == (Fraction(1), 0, Fraction(0), (Fraction(1, 2), Fraction(1, 2)))
    assert "1 vacuous" in detail


def test_empty_feasible_domain_is_vacuously_true() -> None:
    cert = {
        "L": Fraction(1),
        "B": Fraction(2),
        "atoms": [(Fraction(0), Fraction(0), Fraction(1))],
        "tangents": [Fraction(0), Fraction(1, 2)],
    }
    c, s = verify.direction(Fraction(0))
    assert verify.least_covered_weight(cert, c, s, [1], 1) == (None, None, 0)

    (_name, detail, holds), worst = verify.condition_c4(cert, log=lambda *_args: None)
    assert holds is True
    assert worst is None
    assert "universal condition is vacuous" in detail


@pytest.mark.parametrize(("field", "wrong"), [("total_mass", "0"), ("least_cell_mass", "2")])
def test_declared_value_mismatch_is_verdict_bearing(field: str, wrong: str) -> None:
    cert = {
        "id": "declaration-control",
        "n": 2,
        "L": Fraction(1),
        "B": Fraction(3, 5),
        "tangents": [Fraction(0), Fraction(1, 2)],
        "atoms": [(Fraction(1, 2), Fraction(1, 2), Fraction(1))],
        "declared": {
            "angle_limit": "1/2",
            "claim": "s(2) >= 1",
            "total_mass": "1",
            "least_cell_mass": "1",
            field: wrong,
        },
    }
    messages: list[str] = []
    accepted, _results = verify.decide(cert, log=messages.append)
    assert accepted is False
    assert any(f"declared {field} disagrees with replay" in message for message in messages)


def test_degenerate_cli_case_has_no_traceback(tmp_path: Path) -> None:
    completed = subprocess.run(
        [sys.executable, str(VERIFY_PATH), str(write_record(tmp_path, base_record()))],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 1  # C0 and C3 fail, but C4 is decided.
    assert "PASS  C4 every admissible placement covers weight >= 1" in completed.stdout
    assert "Traceback" not in completed.stdout + completed.stderr


def test_falsification_oracle_detects_wrong_verdict_and_condition() -> None:
    results = {"P2 every weight is non-negative": ("fixture", True)}
    errors = falsify.expectation_errors(
        accepted=True, results=results, oracle=falsify.QUICK_EXPECTATION
    )
    assert any("verdict" in error for error in errors)
    assert any("P2 was PASS" in error for error in errors)


def test_quick_negative_control_is_bounded_and_assertive() -> None:
    completed = subprocess.run(
        [sys.executable, str(FALSIFY_PATH), "--quick", str(CERTIFICATE_PATH)],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert completed.returncode == 0
    assert "expected refusal and P2 result confirmed" in completed.stdout
    assert "EXPECTATION FAILED" not in completed.stdout + completed.stderr


def test_minimal_checker_binds_the_retained_bytes_and_closed_form_facts() -> None:
    record, atoms = minimal_verify.load(CURRENT_CERTIFICATE_PATH)
    side = minimal_verify.rational(record["outer_side"])
    assert minimal_verify.check_measure(
        atoms, side, minimal_verify.rational(record["total_mass"])
    ) == Fraction(434547, 40000)
    limit = minimal_verify.rational(record["angle_limit"])
    assert limit * limit + 2 * limit - 1 == Fraction(309449, 250000000000)


@pytest.mark.exhaustive_exact
def test_minimal_checker_replays_every_cell_and_its_mutation() -> None:
    completed = subprocess.run(
        [sys.executable, str(MINIMAL_VERIFY_PATH), str(CURRENT_CERTIFICATE_PATH)],
        check=False,
        capture_output=True,
        text=True,
        timeout=240,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "C4     PASS  minimum 4001/4000" in completed.stdout
    assert "567130649 cells" in completed.stdout
    assert "VERIFIED s(11) >= 381/100" in completed.stdout
    assert "MUTATION REFUSED" in completed.stdout
