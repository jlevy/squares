"""Independent rational controls for normalization, source decimals, and assurance scope."""

from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Callable
from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
from functools import partial
from pathlib import Path
from typing import Any

from cases.stromquist.n26_source_scores import (
    DIRECT,
    INPUTS,
    INVERSE_SQUARED,
    REPO,
    cached_side_comparison,
    compare_rounded_side,
    compare_score,
    deletion_comparisons,
    minmax_comparison,
    rational,
    read_source_json,
    sqrt_bracket,
)


def _settings() -> dict[str, Any]:
    return json.loads(INPUTS.read_text())


def _minmax() -> dict[str, Any]:
    source = REPO / _settings()["minmax"]["snapshot"]
    return json.loads(source.read_text(), parse_float=Decimal)


def _row(snapshot: dict[str, Any]) -> dict[str, Any]:
    return next(row for row in snapshot["instances"] if row["instanceId"] == "p18-n26-v1")


def _rejected(call: Callable[[], object]) -> None:
    try:
        call()
    except TypeError, ValueError:
        return
    raise AssertionError("an invalid score or normalization was accepted")


def test_minmax_exact_minimum_and_independent_integer_comparison() -> None:
    result = minmax_comparison(_minmax())
    score = 4 * (Fraction(62_895_084, 10**9) ** 2 + Fraction(62_895_074, 10**9) ** 2)
    assert score == Fraction(1_977_895_481_208_133, 62_500_000_000_000_000)
    assert result["score_rational"] == str(score)
    assert result["source_score_stored"] == "31646327699330128"
    assert result["normalized_container_side_squared"] == str(1 / score)
    assert result["pieces_attaining_minimum"] == 9
    # 1/U^2 = (268 - 168*sqrt(2))/961. These integer inequalities prove
    # score < 1/U^2, independently of the production NumberField predicates.
    residual = 268 - 961 * score
    assert residual > 0
    assert residual**2 > 2 * 168**2
    assert result["container_side_minus_friedman_sign"] == 1
    assert result["smaller_normalized_container_side"] is False
    assert result["geometry_verified"] is False
    assert result["distinct_squared_sides"] == [
        str(score),
        str(Fraction(177_894_148, 10**9) ** 2),
    ]
    endpoints = result["container_side_minus_friedman_interval"]
    assert isinstance(endpoints, list)
    gap = [rational(value) for value in endpoints]
    assert Fraction("0.00000005566066280") < gap[0] < gap[1]
    assert gap[1] < Fraction("0.00000005566066281")


def test_cached_json_tokens_are_preserved_and_a_future_smaller_score_is_not_geometry() -> None:
    path = REPO / _settings()["forloopcodes_cache"]["snapshot"]
    source = json.loads(path.read_text(), parse_float=Decimal)
    side = Fraction("5.621320343794426")
    assert rational(source["s"]) == side
    result = cached_side_comparison(source, n=26)
    assert result["score_rational"] == str(side)
    # U=(7+3sqrt(2))/2; positivity makes this squared comparison equivalent.
    assert 2 * side - 7 > 0
    assert (2 * side - 7) ** 2 > 18
    assert result["container_side_minus_friedman_sign"] == 1
    assert result["geometry_verified"] is False
    _rejected(lambda: cached_side_comparison(json.loads(path.read_text()), n=26))
    improved = compare_score(Fraction("5.62"), n=26, metric=DIRECT, objective="minimize")
    assert (2 * Fraction("5.62") - 7) ** 2 < 18
    assert improved["smaller_normalized_container_side"] is True
    assert improved["geometry_verified"] is False


def test_rounding_interpretations_straddle_reference_and_cannot_rank_a_construction() -> None:
    # These are explicit nearest-rounding interpretations, not assertions that a
    # source guarantees that rounding convention or that the display is geometry.
    for display, quantum in (
        ("5.621320343560", "0.000000000001"),
        ("5.62132034355964", "0.00000000000001"),
    ):
        result = compare_rounded_side(display, quantum, n=26)
        assert result["endpoint_comparison_signs"] == [-1, 1]
        assert result["verdict"] == "undetermined-from-rounded-display"
        assert result["geometry_verified"] is False
    _rejected(lambda: compare_rounded_side("5.62", "0.03", n=26))
    _rejected(lambda: compare_rounded_side("5.62", "-0.01", n=26))


def test_metric_direction_square_count_and_invalid_scores_fail_closed() -> None:
    for metric, objective in (
        (DIRECT, "maximize"),
        (INVERSE_SQUARED, "minimize"),
        ("unit-container-minimum-square-side", "maximize"),
    ):
        _rejected(
            partial(compare_score, Fraction(1, 32), n=26, metric=metric, objective=objective)
        )
    for n in (25, 27, True):
        _rejected(partial(compare_score, Fraction(6), n=n, metric=DIRECT, objective="minimize"))
    for value in (Fraction(0), Fraction(-1), 5.62, True):
        _rejected(partial(compare_score, value, n=26, metric=DIRECT, objective="minimize"))
    _rejected(
        lambda: compare_score(Fraction(2), n=26, metric=INVERSE_SQUARED, objective="maximize")
    )
    for value in (0.177894147, True, "NaN", "Infinity", Decimal("NaN"), Decimal("Infinity")):
        _rejected(partial(rational, value))


def test_minmax_rejects_display_substitution_score_drift_and_wrong_instance() -> None:
    original = _minmax()
    for field, value in (
        ("scoreStored", "0.177894147"),
        ("scoreStored", "31646327699330129"),
        ("scoreStored", "-1"),
        ("objective", "minimize"),
        ("parameters", {"n": 27}),
    ):
        altered = deepcopy(original)
        _row(altered)[field] = value
        _rejected(partial(minmax_comparison, altered))
    altered = deepcopy(original)
    _row(altered)["answer"]["squares"].pop()
    _rejected(lambda: minmax_comparison(altered))
    altered = deepcopy(original)
    _row(altered)["answer"]["squares"][0]["ux"] = "0"
    _row(altered)["answer"]["squares"][0]["uy"] = "0"
    _rejected(lambda: minmax_comparison(altered))
    altered = deepcopy(original)
    altered["instances"].append(deepcopy(_row(altered)))
    _rejected(lambda: minmax_comparison(altered))
    altered = deepcopy(original)
    altered["code"] = "P12"
    _rejected(lambda: minmax_comparison(altered))
    # Ignoring centers is intentional: score arithmetic cannot certify geometry.
    altered = deepcopy(original)
    for piece in _row(altered)["answer"]["squares"]:
        piece["cx"] = piece["cy"] = "0.5"
    assert minmax_comparison(altered)["geometry_verified"] is False


def test_rational_root_enclosures_and_unchanged_container_deletion_scope() -> None:
    for value in (Fraction(2), Fraction(9, 4), Fraction(1, 10**20)):
        low, high = sqrt_bracket(value)
        assert low**2 <= value <= high**2
        assert high - low <= Fraction(1, 10**40)
    _rejected(lambda: sqrt_bracket(Fraction(0)))
    result = deletion_comparisons(_settings()["deletion_parents"])
    entries = result["entries"]
    assert isinstance(entries, list)
    assert [entry["source_n"] for entry in entries] == [27, 28, 29, 30, 31]
    assert all(entry["container_side_minus_friedman_sign"] == 1 for entry in entries)
    assert result["32_minus_friedman_squared_in_q_sqrt2"] == ["61/4", "-21/2"]
    assert 2 * 42**2 < 61**2
    assert result["area_excludes_unchanged_parent_containers_for_n_at_least"] == 32
    scope, exclusion = result["scope"], result["does_not_exclude"]
    assert isinstance(scope, str)
    assert isinstance(exclusion, str)
    assert "unchanged" in scope
    assert "cropping" in exclusion
    _rejected(lambda: deletion_comparisons(_settings()["deletion_parents"][:-1]))


def test_cli_output_and_retained_record_agree(tmp_path: Path) -> None:
    output = tmp_path / "n26-source-scores.json"
    completed = subprocess.run(
        [sys.executable, "-m", "cases.stromquist.n26_source_scores", "--output", str(output)],
        cwd=REPO / "packing",
        check=True,
        capture_output=True,
        text=True,
    )
    assert completed.stdout == output.read_text()
    retained = INPUTS.with_name("n26-source-scores.json")
    assert json.loads(completed.stdout) == json.loads(retained.read_text())


def test_source_parser_rejects_ambiguous_json_keys(tmp_path: Path) -> None:
    source = tmp_path / "ambiguous.json"
    source.write_text('{"s":5.7,"s":5.6}')
    _rejected(lambda: read_source_json(source))
