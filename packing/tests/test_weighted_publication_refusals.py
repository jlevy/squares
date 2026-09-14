"""Unadmitted weighted records cannot become unweighted figures, claims, or exports."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import render_explainer, render_verifiable_claim
from devtools.check_rung_figures import load_certificate
from devtools.measure_threshold_net_refinement import rescaled_record

CASE = Path(__file__).resolve().parents[1] / "cases" / "n11_threshold_certificate"


def _weighted_record(path: Path, *, prototype: bool) -> dict[str, Any]:
    record = json.loads(path.read_text(encoding="utf-8"))
    atom = record["threshold_atoms"][0]
    counts = (2, 1, 1)
    atom["variant"] = "weighted-threshold/v1"
    if prototype:
        atom["multiplicities"] = list(counts)
    else:
        atom["weighted_points"] = [
            [*point, count] for point, count in zip(atom.pop("points"), counts, strict=True)
        ]
    return record


@pytest.mark.parametrize(
    "prototype", [False, True], ids=["weighted-sites", "additive-prototype"]
)
@pytest.mark.parametrize("consumer", ["refinement", "rung-figures", "claim-facts"])
@pytest.mark.parametrize("point_family", ["retained", "empty"])
def test_public_record_consumers_refuse_weighted_input(
    tmp_path: Path, consumer: str, point_family: str, *, prototype: bool
) -> None:
    record = _weighted_record(CASE / "certificate.json", prototype=prototype)
    if point_family == "empty":
        record["atoms"] = []
    if consumer == "refinement":
        with pytest.raises(ValueError, match="weighted"):
            rescaled_record(
                record, record["direction_steps"], Fraction(record["square_side"]), Fraction(1)
            )
    else:
        path = tmp_path / "certificate.json"
        path.write_text(json.dumps(record), encoding="utf-8")
        if consumer == "rung-figures":
            with pytest.raises(ValueError, match="weighted"):
                load_certificate(path)
        else:
            with pytest.raises(SystemExit, match="weighted"):
                render_verifiable_claim.render_threshold_claim(
                    render_verifiable_claim.T025_CLAIM, path, limit_path=None
                )


@pytest.mark.parametrize(
    "prototype", [False, True], ids=["weighted-sites", "additive-prototype"]
)
@pytest.mark.parametrize("input_name", ["THRESHOLD_CERTIFICATE", "THRESHOLD_FINE_CERTIFICATE"])
def test_explainer_refuses_weighted_coarse_and_fine_sources(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, input_name: str, *, prototype: bool
) -> None:
    original = getattr(render_explainer, input_name)
    path = tmp_path / original.name
    path.write_text(
        json.dumps(_weighted_record(original, prototype=prototype)), encoding="utf-8"
    )
    monkeypatch.setattr(render_explainer, input_name, path)
    render_explainer.current_bound_facts.cache_clear()
    try:
        with pytest.raises(SystemExit, match="weighted"):
            render_explainer.current_bound_facts()
    finally:
        render_explainer.current_bound_facts.cache_clear()
