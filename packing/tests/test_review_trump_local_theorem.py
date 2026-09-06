"""Independent arithmetic and falsification controls for the retained local theorem."""

from __future__ import annotations

import copy
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import review_trump_local_theorem as review


def test_aggregate_caps_and_outward_rounding_reject_drift() -> None:
    record, theorem = review.load_records()
    checked = review.check_aggregate(record, theorem)
    assert checked["preferred_radius"] == "808514697/200000000000"
    assert checked["preferred_quadratic_constant"] == "2574612531/200000000"
    changed = copy.deepcopy(record)
    changed["rho_0"]["candidates"]["declared_box"] = "1/1000000"
    with pytest.raises(review.ReviewError, match="declared_box"):
        review.check_aggregate(changed, theorem)
    changed = copy.deepcopy(theorem)
    changed["constants"]["per_row_preferred"]["radius_rational_lower_bound"] = "1/200"
    with pytest.raises(review.ReviewError, match="preferred radius"):
        review.check_aggregate(record, changed)


def test_norm_factor_refuses_before_radius_comparison() -> None:
    curvature = Fraction(4972105219, 500000000)
    review.check_factor(curvature, 2 / curvature)
    with pytest.raises(review.ReviewError, match="product is 1, expected 2"):
        review.check_factor(curvature, 1 / curvature)


def test_git_content_binds_inputs_and_explains_source_drift(tmp_path: Path) -> None:
    binding = review.check_source_binding()
    assert binding["retained_inputs_unchanged_since_archive"] == [
        review.TANGENT,
        review.RADIUS,
        "packing/cases/trump11/packing.py",
    ]
    assert all(item["semantics_match"] for item in binding["declared_source_drift"])
    for path in binding["input_paths"]:
        destination = tmp_path / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(review.git_content(review.REVIEW_REVISION, path))
    changed = tmp_path / "packing/cases/trump11/tangent_cones.py"
    changed.write_bytes(changed.read_bytes() + b"\nUNDECLARED_CHANGE = True\n")
    with pytest.raises(review.ReviewError, match=r"input content mismatch.*tangent_cones\.py"):
        review.check_source_binding(tmp_path)


def test_source_binding_refuses_undeclared_archive_semantics(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = review.git_content

    def changed_archive(revision: str, path: str) -> bytes:
        content = original(revision, path)
        if revision == review.ARCHIVE and path.endswith("tangent_cones.py"):
            return content + b"\nUNDECLARED_CHANGE = True\n"
        return content

    monkeypatch.setattr(review, "git_content", changed_archive)
    with pytest.raises(review.ReviewError, match=r"undeclared source drift.*tangent_cones\.py"):
        review.check_source_binding()


def test_active_coefficient_and_retained_stress_sign_mutations() -> None:
    context = review.load_context()
    rows = context.branches[0]
    index = next(i for i, row in enumerate(rows) if row.label.startswith("pair:"))
    original = rows[index]
    assert review.row_curvature(context, original) > 0
    coefficients = list(original.coefficients)
    column = next(i for i, value in enumerate(coefficients) if not value.is_zero())
    coefficients[column] = coefficients[column] + 1
    with pytest.raises(review.ReviewError, match="active-row coefficient mismatch"):
        review.row_curvature(context, replace(original, coefficients=tuple(coefficients)))
    stress = review.reconstruct_stress(context, 0)
    reversed_rows = list(rows)
    reversed_rows[index] = replace(
        original, coefficients=tuple(-value for value in original.coefficients)
    )
    with pytest.raises(review.ReviewError, match="retained stress residual"):
        review.check_stress(reversed_rows, stress, context.field)


# The all-128-branch exact stress audit measured 27.21 s before selected faces;
# the fast tests above exercise each required falsification on a real branch.
@pytest.mark.slow
def test_full_retained_review_and_three_falsifying_controls() -> None:
    result = review.run_review()
    assert result["disposition"] == "accept_retained_record_dependent_local_scope"
    assert result["branch_arithmetic"]["branches_checked"] == 128
    assert result["row_audit"]["distinct_rows_checked"] == 56
    assert len(result["selected_faces"]) == 4
    assert all(item["rejected"] for item in result["mutations"])
    assert result["radius_generator_executed"] is False
