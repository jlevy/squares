"""Four sufficient near-45 localization sign obligations, not a packing theorem.

Only --target-h123 invokes the scientific constructor. For W=q/2-1, the
separately reviewed two-point overlap argument requires F=1-W(C+S/2)>=0
and G=(C+S)/2-W*S*(C+S/2)>=0. Both closed signs supply the C/S swaps.
The positive denominator D=1+t² clears F by D and G by D². Coefficients
use the positive sqrt(2) embedding; no old tile or triangle geometry is used.

This producer shares the generic exact Bernstein kernel. An independent reader
must reconstruct the coefficients, not trust these evidence arrays or counters.
Failed sufficient signs, errors and interrupted inventories are unresolved,
never localization counterexamples. A future protocol needs an external cap:
the internal ten-second alarm does not cover imports or final serialization.
"""

from __future__ import annotations

import argparse
import json
import signal
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from devtools.angle_tile_certificate import bernstein_coefficients, certify_nonnegative
from sqpack.field import FieldElement, NumberField

type Polynomial = tuple[FieldElement, ...]
type Slab = tuple[Fraction, Fraction]

SIDE = Fraction(1939, 500)
TARGET_WIDTH = Fraction(939, 1000)
T = Fraction(110880, 50803079)
SLABS = ((-T, Fraction(0)), (Fraction(0), T))
NAMES = ("F", "G")
KIND = "fixed-side-near45-localization-overlap"
WALL_CAP_SECONDS = 10
PACKET_BYTE_CAP = 65536
MAX_INPUT_BITS = 2048


def _rational(value: Fraction) -> None:
    if type(value) is not Fraction:
        raise ValueError("bounded exact Fraction required")
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > MAX_INPUT_BITS:
        raise ValueError("rational exceeds the input bit cap")


def localization_polynomials(width: Fraction) -> tuple[Polynomial, Polynomial]:
    """Generic toy-safe D*F and D²*G; no scientific defaults or target dispatch."""
    _rational(width)
    if not 0 < width < 1:
        raise ValueError("width must be strictly between zero and one")
    field = NumberField((1, 0, -2), ("1", "2"))
    root_half = field.alpha / 2
    w = field.rational(width)
    first = (
        1 - Fraction(3, 2) * w * root_half,
        w * root_half,
        1 + Fraction(3, 2) * w * root_half,
    )
    second = (
        root_half - Fraction(3, 4) * w,
        -w,
        Fraction(5, 2) * w,
        w,
        -root_half - Fraction(3, 4) * w,
    )
    return first, second


@dataclass(frozen=True)
class Obligation:
    slab: int
    polynomial: str
    bernstein: Polynomial
    proved: bool


@dataclass(frozen=True)
class Result:
    coefficients: tuple[Polynomial, Polynomial] | None
    obligations: tuple[Obligation, ...]
    stop_reason: str

    @property
    def proved(self) -> bool:
        expected = [(slab, name) for slab in range(2) for name in NAMES]
        return (
            self.stop_reason == "complete"
            and self.coefficients is not None
            and [(item.slab, item.polynomial) for item in self.obligations] == expected
            and all(type(item.proved) is bool and item.proved for item in self.obligations)
        )


def _sign_evidence(
    polynomial: Polynomial, low: Fraction, high: Fraction
) -> tuple[Polynomial, bool]:
    coefficients = bernstein_coefficients(polynomial, low, high)
    if len(coefficients) != len(polynomial) or not all(
        isinstance(value, FieldElement) and value.field is polynomial[0].field
        for value in coefficients
    ):
        raise ValueError("sign evidence changed coefficient field or inventory")
    evidence = tuple(value for value in coefficients if isinstance(value, FieldElement))
    proved = certify_nonnegative(polynomial, low, high, max_depth=0).proved
    if proved != all(value.sign() >= 0 for value in evidence):
        raise ValueError("sign decision disagrees with exact Bernstein evidence")
    return evidence, proved


def check_width(width: Fraction) -> Result:
    """Check one supplied toy or explicitly bound width on the four frozen slabs.

    Completed evidence is appended only after both the sign test and its exact
    Bernstein evidence agree. An exception retains that completed prefix.
    """
    _rational(width)
    rows = None
    completed: list[Obligation] = []
    reason = "complete"
    try:
        rows = localization_polynomials(width)
        for slab, (low, high) in enumerate(SLABS):
            for name, polynomial in zip(NAMES, rows, strict=True):
                evidence, proved = _sign_evidence(polynomial, low, high)
                completed.append(Obligation(slab, name, evidence, proved))
        if any(not item.proved for item in completed):
            reason = "sign obligations unresolved"
    except TimeoutError as error:
        reason = f"timeout: {error}"
    except (ArithmeticError, ValueError, TypeError, RuntimeError) as error:
        reason = f"error: {type(error).__name__}: {error}"
    return Result(rows, tuple(completed), reason)


def target_input() -> Fraction:
    """The immutable scientific binding, forbidden in source-free controls."""
    return TARGET_WIDTH


def _bound_target_width() -> Fraction:
    width = target_input()
    if type(width) is not Fraction or width != TARGET_WIDTH or 2 * (width + 1) != SIDE:
        raise ValueError("target constructor changed the frozen q/W identity")
    return width


def _pairs(polynomial: Polynomial) -> list[list[str]]:
    return [[str(value) for value in coefficient.coeffs] for coefficient in polynomial]


def packet(result: Result) -> dict[str, Any]:
    """Serialize evidence; this envelope is not an independent verification."""
    return {
        "version": 1,
        "kind": KIND,
        "hypothesis": "H-123",
        "side": str(SIDE),
        "width": str(TARGET_WIDTH),
        "coefficient_basis": ["1", "sqrt2-positive"],
        "half_angle_slabs": [[str(low), str(high)] for low, high in SLABS],
        "coefficients": None
        if result.coefficients is None
        else {name: _pairs(row) for name, row in zip(NAMES, result.coefficients, strict=True)},
        "obligations": [
            {
                "slab": item.slab,
                "polynomial": item.polynomial,
                "bernstein": _pairs(item.bernstein),
                "proved": item.proved,
            }
            for item in result.obligations
        ],
        "status": "proved" if result.proved else "unresolved",
        "stop_reason": result.stop_reason,
    }


def run_target() -> dict[str, Any]:
    """Only the explicit CLI dispatch may call this scientific binding."""
    try:
        result = check_width(_bound_target_width())
    except TimeoutError as error:
        result = Result(None, (), f"timeout: {error}")
    except (ArithmeticError, ValueError, TypeError, RuntimeError) as error:
        result = Result(None, (), f"refused: {type(error).__name__}: {error}")
    return packet(result)


def _unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ValueError("duplicate JSON object key")
    return result


def _nonfinite(_value: str) -> None:
    raise ValueError("nonfinite JSON number")


def _wire_polynomial(value: Any, degree_count: int) -> None:
    if type(value) is not list or len(value) != degree_count:
        raise ValueError("wrong polynomial coefficient inventory")
    for pair in value:
        if type(pair) is not list or len(pair) != 2:
            raise ValueError("each coefficient needs exactly two rational basis entries")
        for entry in pair:
            if type(entry) is not str or len(entry) > 1300:
                raise ValueError("bounded rational coefficient string required")
            try:
                number = Fraction(entry)
            except (ArithmeticError, ValueError) as error:
                raise ValueError("invalid rational coefficient") from error
            _rational(number)
            if str(number) != entry:
                raise ValueError("coefficient string is not canonical")


def parse_packet(raw: str) -> dict[str, Any]:
    """Admit the bounded identity and prefix, never trust it as a sign proof."""
    if type(raw) is not str or len(raw.encode()) > PACKET_BYTE_CAP:
        raise ValueError("packet must be bounded JSON text")
    value = json.loads(raw, object_pairs_hook=_unique, parse_constant=_nonfinite)
    template = packet(Result(None, (), "not started"))
    if type(value) is not dict or set(value) != set(template):
        raise ValueError("packet must have exactly the fixed eleven keys")
    if type(value["version"]) is not int or value["version"] != 1:
        raise ValueError("invalid version")
    for key in ("kind", "hypothesis", "side", "width", "coefficient_basis", "half_angle_slabs"):
        if value[key] != template[key]:
            raise ValueError("packet changes the frozen source identity or slabs")
    powers = value["coefficients"]
    if powers is not None:
        if type(powers) is not dict or set(powers) != set(NAMES):
            raise ValueError("coefficient names must be F and G")
        for name, length in zip(NAMES, (3, 5), strict=True):
            _wire_polynomial(powers[name], length)
    obligations = value["obligations"]
    if type(obligations) is not list or len(obligations) > 4:
        raise ValueError("invalid completed obligation prefix")
    for ordinal, item in enumerate(obligations):
        if type(item) is not dict or set(item) != {"slab", "polynomial", "bernstein", "proved"}:
            raise ValueError("malformed obligation")
        if (
            type(item["slab"]) is not int
            or item["slab"] != ordinal // 2
            or item["polynomial"] != NAMES[ordinal % 2]
            or type(item["proved"]) is not bool
        ):
            raise ValueError("missing, repeated or reordered obligation")
        _wire_polynomial(item["bernstein"], (3, 5)[ordinal % 2])
    if obligations and powers is None:
        raise ValueError("obligations lack their power coefficients")
    if type(value["stop_reason"]) is not str or not 0 < len(value["stop_reason"]) <= 2048:
        raise ValueError("invalid stop reason")
    if value["status"] not in ("proved", "unresolved"):
        raise ValueError("invalid status")
    if value["status"] == "proved" and (
        len(obligations) != 4
        or powers is None
        or value["stop_reason"] != "complete"
        or not all(item["proved"] for item in obligations)
    ):
        raise ValueError("positive status exceeds the completed evidence")
    return value


def _expired(_signum: int, _frame: Any) -> None:
    raise TimeoutError("ten-second H123 producer alarm")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-h123", action="store_true", required=True)
    parser.parse_args(argv)
    previous = signal.signal(signal.SIGALRM, _expired)
    old_timer = signal.setitimer(signal.ITIMER_REAL, WALL_CAP_SECONDS)
    try:
        result = run_target()
    except TimeoutError as error:
        result = packet(Result(None, (), f"timeout before receipt: {error}"))
    finally:
        signal.setitimer(signal.ITIMER_REAL, *old_timer)
        signal.signal(signal.SIGALRM, previous)
    print(json.dumps(result, sort_keys=True))
    if result["status"] != "proved":
        print(result["stop_reason"], file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
