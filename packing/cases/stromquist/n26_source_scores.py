"""Compare retained n=26 source scores with Friedman's exact upper bound.

All score arithmetic is rational or in Q(sqrt(2)); JSON decimal tokens never
pass through binary floating point. A score comparison does not check the
source's square geometry or prove optimality. Rounded displays are intervals,
not exact construction scores. Deletion inherits the parent's unchanged
container and makes no claim about cropping or reoptimizing the survivors.

Run from packing/: uv run --frozen python -m cases.stromquist.n26_source_scores.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, localcontext
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any

from sqpack.cover import write_text_atomic
from sqpack.field import NumberField
from sqpack.yamlio import load_yaml

REPO = Path(__file__).resolve().parents[3]
INPUTS = Path(__file__).with_name("n26-source-score-inputs.json")
DIRECT = "unit-square-container-side"
INVERSE_SQUARED = "unit-container-minimum-square-side-squared"


def rational(value: object) -> Fraction:
    """Preserve source decimal tokens; reject floats, booleans and nonfinite values."""
    if isinstance(value, bool) or not isinstance(value, str | int | Decimal | Fraction):
        raise TypeError("a score requires exact text, an integer, Decimal, or Fraction")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError, OverflowError) as error:
        raise ValueError("a score must be a finite rational number") from error


def sqrt_bracket(value: Fraction, digits: int = 40) -> tuple[Fraction, Fraction]:
    """Enclose a positive square root using integer arithmetic only."""
    if value <= 0 or digits < 1:
        raise ValueError("a positive radicand and precision are required")
    scale = 10**digits
    lower = Fraction(isqrt(value.numerator * scale**2 // value.denominator), scale)
    return lower, lower if lower**2 == value else lower + Fraction(1, scale)


def _decimal(value: Fraction) -> str:
    with localcontext() as context:
        context.prec = 42
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def _require_n26(n: object) -> None:
    if type(n) is not int or n != 26:
        raise ValueError("this comparison requires exactly 26 squares")


def compare_score(score: object, *, n: int, metric: str, objective: str) -> dict[str, object]:
    """Compare a supplied positive scalar after converting to container side squared."""
    _require_n26(n)
    if not isinstance(score, Fraction):
        raise TypeError("a score must be a Fraction")
    if score <= 0:
        raise ValueError("a positive Fraction score is required")
    if (metric, objective) == (DIRECT, "minimize"):
        side_squared = score**2
    elif (metric, objective) == (INVERSE_SQUARED, "maximize"):
        if score > 1:
            raise ValueError("a minimum squared side in the unit container cannot exceed 1")
        side_squared = 1 / score
    else:
        raise ValueError("unsupported metric or incorrect optimization direction")
    field = NumberField((1, 0, -2), (1, 2))
    reference = (7 + 3 * field.alpha) / 2
    difference = field.rational(side_squared) - reference**2
    sign = difference.sign()
    digits = 40
    while True:
        field.refine_to(digits)
        reference_lo, reference_hi = field.enclose(reference)
        candidate_lo, candidate_hi = sqrt_bracket(side_squared, digits)
        gap = candidate_lo - reference_hi, candidate_hi - reference_lo
        if sign == 0 or (sign > 0 and gap[0] > 0) or (sign < 0 and gap[1] < 0):
            break
        digits *= 2
    return {
        "n": n,
        "metric": metric,
        "objective": objective,
        "score_rational": str(score),
        "normalized_container_side_squared": str(side_squared),
        "container_side_squared_minus_friedman_in_q_sqrt2": [
            str(value) for value in difference.coeffs
        ],
        "container_side_minus_friedman_sign": sign,
        "smaller_normalized_container_side": sign < 0,
        "container_side_interval": [str(candidate_lo), str(candidate_hi)],
        "container_side_approx": _decimal((candidate_lo + candidate_hi) / 2),
        "container_side_minus_friedman_interval": [str(value) for value in gap],
        "container_side_minus_friedman_approx": _decimal((gap[0] + gap[1]) / 2),
        "geometry_verified": False,
    }


def compare_rounded_side(display: str, quantum: str, *, n: int) -> dict[str, object]:
    """Compare a display assuming nearest rounding to an explicitly supplied quantum."""
    center, step = rational(display), rational(quantum)
    if step <= 0 or (center / step).denominator != 1 or center <= step / 2:
        raise ValueError("the display must be a positive multiple of its rounding quantum")
    low, high = center - step / 2, center + step / 2
    low_record = compare_score(low, n=n, metric=DIRECT, objective="minimize")
    high_record = compare_score(high, n=n, metric=DIRECT, objective="minimize")
    low_sign = low_record["container_side_minus_friedman_sign"]
    high_sign = high_record["container_side_minus_friedman_sign"]
    verdict = "undetermined-from-rounded-display"
    if low_sign == high_sign == 1:
        verdict = "larger-throughout-rounding-interval"
    elif low_sign == high_sign == -1:
        verdict = "smaller-throughout-rounding-interval"
    return {
        "n": n,
        "display": display,
        "assumption": "nearest rounding to the supplied quantum",
        "quantum": quantum,
        "rounding_interval": [str(low), str(high)],
        "endpoint_comparison_signs": [low_sign, high_sign],
        "verdict": verdict,
        "geometry_verified": False,
    }


def minmax_comparison(snapshot: dict[str, Any]) -> dict[str, object]:
    """Recompute P18's stored squared-side score from all 26 exact half-edge vectors."""
    if (
        snapshot.get("problem") != "tilted-squares-in-square"
        or snapshot.get("code") != "P18"
        or snapshot.get("objective") != "maximize"
    ):
        raise ValueError("expected the P18 unit-container maximization source")
    matches = [row for row in snapshot["instances"] if row["instanceId"] == "p18-n26-v1"]
    if len(matches) != 1:
        raise ValueError("expected exactly one P18 n=26 record")
    row = matches[0]
    _require_n26(row["parameters"]["n"])
    pieces = row["answer"]["squares"]
    if len(pieces) != 26 or row["objective"] != "maximize":
        raise ValueError("the n=26 score requires 26 pieces and maximization")
    squared_sides = [
        4 * (rational(piece["ux"]) ** 2 + rational(piece["uy"]) ** 2) for piece in pieces
    ]
    score = min(squared_sides)
    stored = row["scoreStored"]
    if not isinstance(stored, str) or not stored.isascii() or not stored.isdigit():
        raise ValueError("scoreStored must be the integer squared-side score, not a display")
    if score != Fraction(int(stored), 10**18):
        raise ValueError("stored score disagrees with the exact minimum squared side")
    result = compare_score(score, n=26, metric=INVERSE_SQUARED, objective="maximize")
    result.update(
        {
            "source_generated_at": snapshot["generatedAt"],
            "source_recorded_at": row["recordedAt"],
            "source_verifier_version": snapshot["verifierVersion"],
            "source_score_stored": stored,
            "source_score_display": row["scoreDisplay"],
            "score_derived_from_half_edge_vectors": True,
            "distinct_squared_sides": [str(value) for value in sorted(set(squared_sides))],
            "pieces_attaining_minimum": squared_sides.count(score),
        }
    )
    return result


def cached_side_comparison(snapshot: dict[str, Any], *, n: int) -> dict[str, object]:
    """Read a numerical reproduction's declared side, without verifying its geometry."""
    _require_n26(n)
    if len(snapshot["squares"]) != n:
        raise ValueError("the declared square count disagrees with the cached coordinates")
    return compare_score(rational(snapshot["s"]), n=n, metric=DIRECT, objective="minimize")


def read_source_json(path: Path) -> Any:
    """Keep decimal tokens exact and reject ambiguous duplicate object keys."""

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate source JSON key: {key}")
            result[key] = value
        return result

    return json.loads(path.read_text(), parse_float=Decimal, object_pairs_hook=unique_object)


def deletion_comparisons(entries: list[dict[str, Any]]) -> dict[str, object]:
    """Compare n=27..31 retained witness sides inherited by an unchanged container."""
    if sorted(entry["n"] for entry in entries) != [27, 28, 29, 30, 31]:
        raise ValueError("the deletion audit requires each parent n=27..31 exactly once")
    rows = []
    for entry in entries:
        witness = load_yaml((REPO / entry["witness"]).read_text())["witness"]
        if (
            witness["n"] != entry["n"]
            or len(witness["squares"]) != entry["n"]
            or rational(witness["square_size"]) != 1
        ):
            raise ValueError("parent witness count or unit-square normalization disagrees")
        comparison = compare_score(
            rational(witness["side"]), n=26, metric=DIRECT, objective="minimize"
        )
        rows.append({"source_n": entry["n"], "witness": entry["witness"], **comparison})
    field = NumberField((1, 0, -2), (1, 2))
    reference = (7 + 3 * field.alpha) / 2
    area_gap = 32 - reference**2
    if area_gap.sign() <= 0:
        raise ValueError("the claimed unchanged-container area cutoff failed")
    return {
        "scope": "delete to 26 and inherit the unchanged enclosing-square side",
        "comparison_inputs": "declared numerical witness sides; geometry not replayed here",
        "does_not_exclude": "cropping, re-enclosing, or reoptimizing the surviving squares",
        "entries": rows,
        "area_excludes_unchanged_parent_containers_for_n_at_least": 32,
        "32_minus_friedman_squared_in_q_sqrt2": [str(value) for value in area_gap.coeffs],
        "area_gap_sign": area_gap.sign(),
    }


def verified_record(inputs: Path = INPUTS) -> dict[str, object]:
    """Rebuild source comparisons from archived inputs and retained witness declarations."""
    settings = read_source_json(inputs)
    if settings["schema_version"] != 1:
        raise ValueError("unsupported source-score input version")
    minmax = settings["minmax"]
    cache = settings["forloopcodes_cache"]
    display = settings["forloopcodes_readme_display"]
    field = NumberField((1, 0, -2), (1, 2))
    reference = (7 + 3 * field.alpha) / 2
    return {
        "schema_version": 1,
        "scope": "exact source scalar comparisons; no geometry or optimality proof",
        "reference": {
            "n": 26,
            "unit_square_container_side": "(7 + 3*sqrt(2))/2",
            "unit_container_minimum_square_side": "(14 - 6*sqrt(2))/31",
            "side_squared_in_q_sqrt2": [str(value) for value in (reference**2).coeffs],
            "side_decimal": field.decimal(reference, 30),
            "field_preconditions": field.precondition_certificate(),
        },
        "minmax": {
            "source": minmax,
            **minmax_comparison(read_source_json(REPO / minmax["snapshot"])),
        },
        "forloopcodes_cache": {
            "source": cache,
            **cached_side_comparison(read_source_json(REPO / cache["snapshot"]), n=cache["n"]),
        },
        "forloopcodes_readme_display": {
            "source": display,
            **compare_rounded_side(display["display"], display["quantum"], n=display["n"]),
        },
        "deletion": {
            "source": settings["deletion_source"],
            **deletion_comparisons(settings["deletion_parents"]),
        },
    }


def main() -> int:
    """Print the rebuilt comparison record and optionally retain it atomically."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=INPUTS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(verified_record(args.inputs), indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        write_text_atomic(args.output, text)
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
