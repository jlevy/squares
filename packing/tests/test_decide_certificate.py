"""Controls for the retention gate.

The gate exists so that a rung cannot join the record on one route's word, or on
a lane's report of bytes that have since changed. What matters is that it refuses:
a gate nobody has watched refuse is a gate nobody has tested.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
import warnings
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Never

import pytest

import devtools.decide_certificate as retention
import sqpack.fractional.interval as interval_verifier
from devtools.decide_certificate import decide, load

CASES = Path(__file__).resolve().parent.parent / "cases"
RUNG = CASES / "n11_fractional_certificate" / "certificate-19-5.json"
REPO = CASES.parent.parent
# The reader-facing surfaces that describe what the two routes share. A claim of
# method independence is a claim about the record, so it is checked where a reader
# meets it and not only where the gate states it.
INDEPENDENCE_SURFACES = (
    REPO / "README.md",
    REPO / "SYNOPSIS.md",
    REPO / "packing/frontier/results.yaml",
    REPO / "packing/frontier/evidence.yaml",
    REPO / "packing/frontier/RESULTS.md",
    REPO / "packing/cases/n11_fractional_certificate/thirdparty/README.md",
)
OVERSTATEMENTS = (
    "share no modelling assumption",
    "share no modeling assumption",
    "shares no modelling assumption",
    "shares no modeling assumption",
)


def collapsed(text: str) -> str:
    """One line, single-spaced, so a claim split over a line break is still found."""

    return " ".join(text.split())


@dataclass(frozen=True)
class FakeDirection:
    boxes: int = 1
    stalled: int = 0


@dataclass(frozen=True)
class FakeIntervalVerdict:
    accepted: bool = True
    enclosure: tuple[Fraction, Fraction] | None = (
        Fraction(50003, 50000),
        Fraction(50003, 50000),
    )
    failures: tuple[str, ...] = ()
    directions: tuple[FakeDirection, ...] = (FakeDirection(),)


@dataclass(frozen=True)
class FakeExactVerdict:
    accepted: bool = True
    minimum_cell_mass: Fraction | None = Fraction(50003, 50000)
    failures: tuple[str, ...] = ()


def bomb(*_args: object, **_kwargs: object) -> Never:
    raise AssertionError("a certificate sweep ran after a decisive refusal")


def no_sweeps(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(retention, "verify", bomb)
    monkeypatch.setattr(retention, "verify_by_intervals", bomb)


def write(tmp_path: Path, edit) -> Path:
    record = json.loads(RUNG.read_text())
    edit(record)
    path = tmp_path / "candidate.json"
    path.write_text(json.dumps(record, indent=1))
    return path


def test_the_gate_reads_the_bytes_and_recomputes_rather_than_trusting_the_summary() -> None:
    certificate, record = load(RUNG)
    total_mass = record["total_mass"]
    assert isinstance(total_mass, str)
    assert certificate.total_mass == Fraction(total_mass)
    assert certificate.outer_side == Fraction(19, 5)
    assert len(certificate.atoms) == 425


def test_the_gate_describes_its_independence_boundary() -> None:
    """The two routes share the ``Certificate`` and Conditions 2--4; only Condition 5 differs.

    "Share no modelling assumption" overstated it (PR 78's adversarial review, F3): the
    routes read one object and decide the closed-form conditions by the same formulas.
    What they do not share is the Condition 5 method, which is where a modelling error
    would live. The gate's own docstring says that, and so must every record surface a
    reader meets the claim on -- a claim about the record is not kept true by a docstring.
    """
    assert retention.__doc__ is not None
    words = " ".join(retention.__doc__.split())
    assert "Certificate" in words
    assert "Conditions 2--4" in words
    assert "share no modelling assumption" not in words
    for path in INDEPENDENCE_SURFACES:
        surface = collapsed(path.read_text(encoding="utf-8"))
        for phrase in OVERSTATEMENTS:
            assert phrase not in surface, f"{path.name} overstates the independence"


def test_a_declared_mass_that_disagrees_with_the_atoms_is_refused(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    no_sweeps(monkeypatch)
    path = write(tmp_path, lambda r: r.__setitem__("total_mass", "1/2"))
    assert decide(path, quick=True) is False
    assert "declared total_mass" in capsys.readouterr().out


def test_a_side_above_the_ceiling_is_refused_before_any_sweep_runs(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Four B-squares across fit at 4, so Condition 5 forces mass past eleven."""

    def widen(record: dict) -> None:
        record["outer_side"] = "4"
        record["total_mass"] = str(sum(Fraction(a[2]) for a in record["atoms"]))

    no_sweeps(monkeypatch)
    path = write(tmp_path, widen)
    assert decide(path, quick=True) is False
    errors = capsys.readouterr().out
    assert "above the ceiling" in errors


def test_a_mass_that_does_not_fall_below_n_is_refused(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def heavy(record: dict) -> None:
        record["atoms"] = [[x, y, str(Fraction(w) * 2)] for x, y, w in record["atoms"]]
        record["total_mass"] = str(sum(Fraction(a[2]) for a in record["atoms"]))

    no_sweeps(monkeypatch)
    path = write(tmp_path, heavy)
    assert decide(path, quick=True) is False
    assert "Condition 2 total mass below n failed" in capsys.readouterr().out


@pytest.mark.parametrize(
    "case",
    [
        ("symmetry", "bogus", "Condition 1"),
        ("angle_limit", "2/5", "Condition 3"),
        ("square_side", "1", "Condition 4"),
    ],
)
def test_closed_form_failures_are_refused_before_any_condition_5_sweep(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    case: tuple[str, object, str],
) -> None:
    field, value, condition = case
    no_sweeps(monkeypatch)
    path = write(tmp_path, lambda record: record.__setitem__(field, value))
    assert decide(path, quick=False) is False
    assert f"{condition} " in capsys.readouterr().out


def test_a_false_declared_claim_is_refused_before_any_sweep(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    no_sweeps(monkeypatch)
    path = write(tmp_path, lambda record: record.__setitem__("claim", "s(11) >= 4"))
    assert decide(path, quick=True) is False
    assert "theorem conclusion" in capsys.readouterr().out


@pytest.mark.parametrize("field", ["claim", "total_mass"])
def test_required_declarations_cannot_be_deleted(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    field: str,
) -> None:
    no_sweeps(monkeypatch)
    path = write(tmp_path, lambda record: record.pop(field))
    assert decide(path, quick=True) is False
    assert f"missing required field '{field}'" in capsys.readouterr().out


def test_quick_mode_allows_an_undecided_least_mass_but_cannot_retain(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = write(tmp_path, lambda record: record.pop("least_cell_mass"))
    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(),
    )
    monkeypatch.setattr(retention, "verify", bomb)
    assert decide(path, quick=True) is True
    assert "NOT ENOUGH TO RETAIN" in capsys.readouterr().out


def test_full_mode_requires_the_declared_least_mass_before_any_sweep(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    no_sweeps(monkeypatch)
    path = write(tmp_path, lambda record: record.pop("least_cell_mass"))
    assert decide(path, quick=False) is False
    assert "missing required field 'least_cell_mass'" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("n", 11.9),
        ("n", "11"),
        ("n", True),
        ("direction_steps", 180.9),
        ("direction_steps", "180"),
        ("direction_steps", True),
    ],
)
def test_integer_fields_refuse_lossy_or_coercive_types(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    value: object,
) -> None:
    no_sweeps(monkeypatch)
    path = write(tmp_path, lambda record: record.__setitem__(field, value))
    assert decide(path, quick=True) is False
    errors = capsys.readouterr().out
    assert f"field '{field}'" in errors or "inexact JSON number" in errors


def test_duplicate_keys_are_refused(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    no_sweeps(monkeypatch)
    text = RUNG.read_text().replace('"n": 11,', '"n": 11,\n "n": 12,', 1)
    path = tmp_path / "duplicate.json"
    path.write_text(text)
    assert decide(path, quick=True) is False
    assert "duplicate JSON object key 'n'" in capsys.readouterr().out


def test_oversized_rational_text_is_a_per_path_format_refusal(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    no_sweeps(monkeypatch)
    huge = "1" + "0" * 3000
    path = write(tmp_path, lambda record: record.__setitem__("outer_side", huge))
    assert decide(path, quick=True) is False
    assert "cannot load certificate" in capsys.readouterr().out


def test_file_size_is_bounded_before_json_parsing(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    no_sweeps(monkeypatch)
    path = tmp_path / "oversized.json"
    path.write_bytes(b" " * (retention.MAX_CERTIFICATE_BYTES + 1))
    assert decide(path, quick=True) is False
    assert "file exceeds" in capsys.readouterr().out


def test_direction_count_has_a_pre_allocation_limit(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    no_sweeps(monkeypatch)
    path = write(
        tmp_path,
        lambda record: record.__setitem__("direction_steps", 10**12),
    )
    assert decide(path, quick=True) is False
    assert "exceeds the supported maximum" in capsys.readouterr().out


def test_atom_count_has_a_boxes_by_atoms_memory_limit(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    no_sweeps(monkeypatch)

    def enlarge(record: dict[str, object]) -> None:
        record["atoms"] = [["0", "0", "0"]] * (retention.MAX_ATOMS + 1)

    path = write(tmp_path, enlarge)
    assert decide(path, quick=True) is False
    assert "field 'atoms' exceeds the supported maximum" in capsys.readouterr().out


def test_combined_weight_scale_is_refused_before_mass_formatting(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    denominators = (2**30, 3**19)

    def explode_scale(record: dict[str, object]) -> None:
        atoms = record["atoms"]
        assert isinstance(atoms, list)
        for atom, denominator in zip(atoms[:2], denominators, strict=True):
            assert isinstance(atom, list)
            atom[2] = f"1/{denominator}"

    path = write(tmp_path, explode_scale)
    original_lcm = math.lcm
    lcm_calls = 0

    def counted_lcm(left: int, right: int) -> int:
        nonlocal lcm_calls
        lcm_calls += 1
        if lcm_calls > 2:
            raise AssertionError("mass scaling continued after crossing the int64 limit")
        return original_lcm(left, right)

    monkeypatch.setattr(interval_verifier.math, "lcm", counted_lcm)
    monkeypatch.setattr(retention, "verify", bomb)
    monkeypatch.setattr(retention, "verify_by_intervals", bomb)
    assert decide(path, quick=True) is False
    assert "weight scale is too large" in capsys.readouterr().out
    assert lcm_calls == 2


def test_diagnostic_float_overflow_cannot_abort_preflight(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    no_sweeps(monkeypatch)
    huge = "1" + "0" * 400

    def enlarge(record: dict) -> None:
        record["outer_side"] = huge
        record["claim"] = f"s(11) >= {huge}"

    path = write(tmp_path, enlarge)
    assert decide(path, quick=True) is False
    captured = capsys.readouterr()
    assert "outside-float-range" in captured.out
    assert "above the ceiling" in captured.out


@pytest.mark.parametrize(
    "magnitude",
    [Fraction(10**400), Fraction(sys.float_info.max) + 1],
    ids=["overflow", "nextafter-overflow"],
)
def test_out_of_range_coordinates_are_a_per_path_interval_refusal(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    magnitude: Fraction,
) -> None:
    side = Fraction(19, 5)

    def add_zero_weight_orbit(record: dict[str, object]) -> None:
        atoms = record["atoms"]
        assert isinstance(atoms, list)
        x, y = magnitude, 2 * magnitude
        far_x, far_y = side - x, side - y
        orbit = (
            (x, y),
            (far_x, y),
            (x, far_y),
            (far_x, far_y),
            (y, x),
            (far_y, x),
            (y, far_x),
            (far_y, far_x),
        )
        atoms.extend([[str(a), str(b), "0"] for a, b in orbit])

    path = write(tmp_path, add_zero_weight_orbit)
    later = tmp_path / "later.json"
    later.write_text("{}")
    monkeypatch.setattr(retention, "verify", bomb)
    assert retention.main(["--quick", str(path), str(later)]) == 1
    errors = capsys.readouterr().out
    assert "interval route could not decide" in errors
    assert "finite float" in errors
    assert "later.json: REFUSED" in errors


def test_finite_boundary_arithmetic_is_a_per_path_interval_refusal(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    outer = int(sys.float_info.max)

    def move_to_float_boundary(record: dict[str, object]) -> None:
        record["n"] = (2 * outer) ** 2
        record["outer_side"] = str(outer)
        record["square_side"] = "1/2"
        record["angle_limit"] = "1/2"
        record["claim"] = f"s({record['n']}) >= {outer}"
        record["atoms"] = []
        record["total_mass"] = "0"

    path = write(tmp_path, move_to_float_boundary)
    later = tmp_path / "later.json"
    later.write_text("{}")
    monkeypatch.setattr(retention, "verify", bomb)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert retention.main(["--quick", str(path), str(later)]) == 1
    assert not caught
    errors = capsys.readouterr().out
    assert f"{path}: REFUSED: the interval route could not decide" in errors
    assert "finite float" in errors
    assert f"{later}: REFUSED" in errors


def test_finite_atom_geometry_overflow_is_a_quiet_per_path_refusal(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    side = Fraction(19, 5)
    magnitude = Fraction(sys.float_info.max)

    def add_boundary_orbit(record: dict[str, object]) -> None:
        atoms = record["atoms"]
        assert isinstance(atoms, list)
        x, y = magnitude, magnitude / 2
        far_x, far_y = side - x, side - y
        orbit = (
            (x, y),
            (far_x, y),
            (x, far_y),
            (far_x, far_y),
            (y, x),
            (far_y, x),
            (y, far_x),
            (far_y, far_x),
        )
        atoms.extend([[str(a), str(b), "0"] for a, b in orbit])

    path = write(tmp_path, add_boundary_orbit)
    later = tmp_path / "later.json"
    later.write_text("{}")
    monkeypatch.setattr(retention, "verify", bomb)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert retention.main(["--quick", str(path), str(later)]) == 1
    assert not caught
    errors = capsys.readouterr().out
    assert f"{path}: REFUSED: the interval route could not decide" in errors
    assert "finite float arithmetic" in errors
    assert f"{later}: REFUSED" in errors


def test_an_interval_refusal_stops_before_the_exact_sweep(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(
            accepted=False, failures=("Condition 5",)
        ),
    )
    monkeypatch.setattr(retention, "verify", bomb)
    assert decide(RUNG, quick=False) is False
    assert "interval route refused" in capsys.readouterr().out


def test_stalled_interval_boxes_stop_before_the_exact_sweep(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(directions=(FakeDirection(stalled=1),)),
    )
    monkeypatch.setattr(retention, "verify", bomb)
    assert decide(RUNG, quick=False) is False
    assert "boxes stalled" in capsys.readouterr().out


def test_an_interval_decision_error_is_a_refusal_before_exact(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail_interval(*_args: object, **_kwargs: object) -> Never:
        raise retention.IntervalInputError("unsafe mass scale")

    monkeypatch.setattr(retention, "verify_by_intervals", fail_interval)
    monkeypatch.setattr(retention, "verify", bomb)
    assert decide(RUNG, quick=False) is False
    assert "interval route could not decide" in capsys.readouterr().out


def test_an_unexpected_interval_error_remains_visible(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_interval(*_args: object, **_kwargs: object) -> Never:
        raise ValueError("internal interval invariant")

    monkeypatch.setattr(retention, "verify_by_intervals", fail_interval)
    monkeypatch.setattr(retention, "verify", bomb)
    with pytest.raises(ValueError, match="internal interval invariant"):
        decide(RUNG, quick=False)


@pytest.mark.parametrize(
    "enclosure",
    [None, (Fraction(1), Fraction(1001, 1000))],
)
def test_full_mode_refuses_an_unusable_interval_enclosure_before_exact(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    enclosure: tuple[Fraction, Fraction] | None,
) -> None:
    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(enclosure=enclosure),
    )
    monkeypatch.setattr(retention, "verify", bomb)
    assert decide(RUNG, quick=False) is False
    errors = capsys.readouterr().out
    assert "no enclosure" in errors or "enclosure has width" in errors


def test_an_exact_refusal_is_verdict_bearing(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(),
    )
    monkeypatch.setattr(
        retention,
        "verify",
        lambda _certificate: FakeExactVerdict(accepted=False, failures=("Condition 5",)),
    )
    assert decide(RUNG, quick=False) is False
    assert "exact sweep refused" in capsys.readouterr().out


def test_an_exact_result_without_a_minimum_is_refused(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(),
    )
    monkeypatch.setattr(
        retention,
        "verify",
        lambda _certificate: FakeExactVerdict(minimum_cell_mass=None),
    )
    assert decide(RUNG, quick=False) is False
    assert "exact sweep returned no least covered mass" in capsys.readouterr().out


def test_an_unexpected_exact_error_remains_visible(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_exact(_certificate: object) -> Never:
        raise ValueError("unusable event arrangement")

    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(),
    )
    monkeypatch.setattr(retention, "verify", fail_exact)
    with pytest.raises(ValueError, match="unusable event arrangement"):
        decide(RUNG, quick=False)


def test_exact_and_interval_disagreement_is_verdict_bearing(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(),
    )
    monkeypatch.setattr(
        retention,
        "verify",
        lambda _certificate: FakeExactVerdict(minimum_cell_mass=Fraction(1)),
    )
    assert decide(RUNG, quick=False) is False
    assert "two routes disagree" in capsys.readouterr().out


def test_a_declared_least_mass_must_match_both_routes(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = write(tmp_path, lambda record: record.__setitem__("least_cell_mass", "1"))
    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(),
    )
    monkeypatch.setattr(retention, "verify", bomb)
    assert decide(path, quick=False) is False
    assert "declared least_cell_mass 1 != interval enclosure 50003/50000" in (
        capsys.readouterr().out
    )


def test_every_positive_decision_message_is_flushed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    flushes: list[object] = []

    def record_print(*_args: object, **kwargs: object) -> None:
        flushes.append(kwargs.get("flush"))

    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(),
    )
    monkeypatch.setattr(retention, "verify", lambda _certificate: FakeExactVerdict())
    monkeypatch.setattr("builtins.print", record_print)
    assert decide(RUNG, quick=False) is True
    assert flushes
    assert all(flush is True for flush in flushes)


def test_rewriting_the_path_during_a_sweep_prevents_retention(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = write(tmp_path, lambda _record: None)

    def rewrite(*_args: object, **_kwargs: object) -> FakeIntervalVerdict:
        path.write_text('{"claim":"unverified replacement"}')
        return FakeIntervalVerdict()

    monkeypatch.setattr(retention, "verify_by_intervals", rewrite)
    monkeypatch.setattr(retention, "verify", bomb)
    assert decide(path, quick=False) is False
    assert "path changed while the decision was running" in capsys.readouterr().out


def test_rewriting_the_path_during_the_exact_sweep_prevents_retention(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = write(tmp_path, lambda _record: None)

    def rewrite(_certificate: object) -> FakeExactVerdict:
        path.write_text('{"claim":"unverified replacement"}')
        return FakeExactVerdict()

    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(),
    )
    monkeypatch.setattr(retention, "verify", rewrite)
    assert decide(path, quick=False) is False
    assert "path changed while the decision was running" in capsys.readouterr().out


def test_a_positive_full_decision_prints_the_accepted_digest(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(),
    )
    monkeypatch.setattr(retention, "verify", lambda _certificate: FakeExactVerdict())
    assert decide(RUNG, quick=False) is True
    digest = hashlib.sha256(RUNG.read_bytes()).hexdigest()
    assert f"sha256 {digest}" in capsys.readouterr().out


def test_a_final_reread_failure_prevents_retention(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    original_read = vars(retention)["_read_bounded"]
    rung_reads = 0

    def fail_final_reread(path: Path) -> bytes:
        nonlocal rung_reads
        if path == RUNG:
            rung_reads += 1
            if rung_reads == 3:
                raise OSError("vanished")
        return original_read(path)

    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(),
    )
    monkeypatch.setattr(retention, "verify", lambda _certificate: FakeExactVerdict())
    monkeypatch.setattr(retention, "_read_bounded", fail_final_reread)
    assert decide(RUNG, quick=False) is False
    assert "cannot reread accepted path: vanished" in capsys.readouterr().out


def test_main_continues_after_a_malformed_path_and_aggregates_failure(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    no_sweeps(monkeypatch)
    broken = tmp_path / "broken.json"
    broken.write_text("{")
    missing = tmp_path / "missing.json"
    missing.write_text("{}")
    assert retention.main(["--quick", str(broken), str(missing)]) == 1
    errors = capsys.readouterr().out
    assert "broken.json: REFUSED" in errors
    assert "missing.json: REFUSED" in errors


def test_batch_load_diagnostics_distinguish_equal_basenames(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    no_sweeps(monkeypatch)
    paths = (tmp_path / "a/candidate.json", tmp_path / "b/candidate.json")
    for path in paths:
        path.parent.mkdir()
        path.write_text("{}")
    assert retention.main(["--quick", *(str(path) for path in paths)]) == 1
    errors = capsys.readouterr().out
    assert all(f"{path}: REFUSED" in errors for path in paths)


def test_batch_decision_diagnostics_name_the_failing_equal_basename(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    paths = (tmp_path / "a/candidate.json", tmp_path / "b/candidate.json")
    for path in paths:
        path.parent.mkdir()
        path.write_bytes(RUNG.read_bytes())

    calls = 0

    def decide_in_order(*_args: object, **_kwargs: object) -> FakeIntervalVerdict:
        nonlocal calls
        calls += 1
        return FakeIntervalVerdict(accepted=calls != 1, failures=("Condition 5",))

    monkeypatch.setattr(retention, "verify_by_intervals", decide_in_order)
    monkeypatch.setattr(retention, "verify", bomb)
    assert retention.main(["--quick", *(str(path) for path in paths)]) == 1
    captured = capsys.readouterr()
    assert f"{paths[0]}: REFUSED: the interval route refused it" in captured.out
    assert f"{paths[1]}: REFUSED" not in captured.out
    assert all(str(path) in captured.out for path in paths)


def test_main_skips_a_duplicate_path_before_any_second_decision(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[Path] = []

    def record(path: Path, *, quick: bool) -> bool:
        assert quick is True
        calls.append(path)
        return True

    monkeypatch.setattr(retention, "decide", record)
    assert retention.main(["--quick", str(RUNG), str(RUNG)]) == 0
    assert calls == [RUNG]
    assert f"{RUNG}: SKIPPED duplicate path" in capsys.readouterr().out


@pytest.mark.exhaustive_exact
def test_quick_mode_says_it_cannot_retain(capsys: pytest.CaptureFixture[str]) -> None:
    """A passing quick run must not read as a retention decision.

    This one runs the real interval route on the retained ``19/5`` rung, about eleven
    seconds on four cores, beside its exhaustive twin below; the fast tier holds the
    same contract through ``test_quick_mode_allows_an_undecided_least_mass_but_cannot_retain``
    with the route stubbed.
    """
    assert decide(RUNG, quick=True) is True
    assert "NOT ENOUGH TO RETAIN" in capsys.readouterr().out


@pytest.mark.exhaustive_exact
def test_a_retained_rung_passes_both_routes_and_they_agree(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert decide(RUNG, quick=False) is True
    out = capsys.readouterr().out
    assert "RETAINABLE" in out
    assert "50003/50000" in out


@pytest.mark.parametrize("variant", ["class", "conditional"])
def test_a_certificate_declaring_another_variant_is_refused_by_name_before_any_sweep(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    variant: str,
) -> None:
    """The gate decides the unconditional theorem and nothing else.

    A class-restricted or conditional certificate that reached the routes would be
    decided under Conditions 1--5 as stated and could print RETAINABLE for a claim it
    never made. The refusal names the variant and says what the gate implements.
    """
    no_sweeps(monkeypatch)
    path = write(tmp_path, lambda record: record.__setitem__("variant", variant))
    assert decide(path, quick=True) is False
    errors = capsys.readouterr().out
    assert f"variant {variant!r}" in errors
    assert "implements only the unconditional conditions" in errors


@pytest.mark.parametrize("value", ["bogus", "Unconditional", 1, None])
def test_an_unknown_variant_is_refused_rather_than_read_as_unconditional(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    value: object,
) -> None:
    no_sweeps(monkeypatch)
    path = write(tmp_path, lambda record: record.__setitem__("variant", value))
    assert decide(path, quick=True) is False
    assert "field 'variant' must be one of" in capsys.readouterr().out


@pytest.mark.parametrize(
    "edit",
    [
        lambda record: record.pop("variant", None),
        lambda record: record.__setitem__("variant", "unconditional"),
    ],
    ids=["absent", "unconditional"],
)
def test_an_absent_or_unconditional_variant_is_accepted_as_before(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    edit,
) -> None:
    path = write(tmp_path, edit)
    certificate, record = load(path)
    assert len(certificate.atoms) == 425
    assert record.get("variant", "unconditional") == "unconditional"
    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(),
    )
    monkeypatch.setattr(retention, "verify", bomb)
    assert decide(path, quick=True) is True
