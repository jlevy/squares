"""Keep the source-audit certificates replayable, including their negative controls."""

from __future__ import annotations

import json
from pathlib import Path

from cases.fibonacci_torus import algebra, geometry, periodic

CASE = Path(__file__).resolve().parents[1] / "cases/fibonacci_torus"


def _retained(name: str) -> object:
    return json.loads((CASE / name).read_text())


def test_algebra_certificates_and_counterexamples() -> None:
    # Round-trip tuples and integer-keyed histograms to the receipt's JSON form.
    assert json.loads(json.dumps(algebra.audit())) == _retained("algebra-result.json")


def test_contact_family_all_parameter_certificate() -> None:
    assert json.loads(json.dumps(geometry.check())) == _retained("geometry-result.json")


def test_bernstein_endpoint_only_false_positives_are_refused() -> None:
    geometry.test_bernstein_refuses_interior_negative_polynomial()
    geometry.test_bernstein_refuses_negative_denominator()


def test_periodic_controls_and_wrapped_overlaps() -> None:
    assert periodic.audit() == _retained("periodic-result.json")
