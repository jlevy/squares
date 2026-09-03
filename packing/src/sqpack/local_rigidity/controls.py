"""The refusals. Every control here must reject, and a control that passes is a kill.

A certificate that cannot fail is not evidence, so each control below perturbs one thing
the instrument depends on and records whether the instrument noticed. The eight are the
eight ways this particular instrument could be wrong and still print a clean receipt:

`changed_feature`
    name a different support feature of the same separating branch as the contact. The
    substituted inequality is slack at the pose, so it is not the local system, and its
    gradient is not the `T-012` row.
`zero_margin`
    offer a margin that is exactly zero where the neighborhood argument needs a strict
    sign. Continuity gives nothing at zero, and a receipt that accepted it would be
    claiming an open set it has not got.
`omitted_constraint`
    drop one separating branch. The remaining system has a *larger* feasible set than the
    geometry, which is the flattering direction and the reason this is checked by
    cardinality rather than by review.
`invented_contact`
    declare a slack inequality active. That shrinks the local system and reports a more
    rigid pose than the geometry has.
`side_release`
    let the container side grow. `H-060` is a fixed-side claim, and at a larger side the
    very same pose has exactly feasible neighbours -- exhibited here, not argued.
`wrong_chart`
    substitute a rationalising transform that is not the half-angle one. Its cleared
    denominator can vanish, or its matrix is not a positive multiple of a rotation, so its
    polynomials are not the constraints.
`certificate_drift`
    change one margin in the retained payload. The digest must move.
`exp034_angle_and_slide`
    `exp-034` exhibits an exact two-parameter fixed-side family of feasible packings. The
    instrument must find that family where it exists and must not import it to a pose
    where it does not. Which of those applies is *computed* here, never assumed: the
    control decides exactly whether `exp-034`'s side is Goebel's side, and separately
    whether the family's motion is feasible in Goebel's own chart.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any

from sqpack.field import FieldElement, NumberField
from sqpack.local_rigidity.binding import T012System, embed
from sqpack.local_rigidity.chart import (
    DOF,
    BasePose,
    Chart,
    ChartPreconditionError,
    HalfAngleTransform,
)
from sqpack.local_rigidity.instrument import Determination, probe_axes, probe_family
from sqpack.local_rigidity.receipt import build_payload, digest, element_algebraic
from sqpack.local_rigidity.system import (
    ConstraintSystem,
    IncompleteEnumerationError,
    InequalityBook,
    Neighborhood,
    StrictCondition,
    build_book,
    build_system,
    is_feasible,
)


@dataclass(frozen=True, slots=True)
class ControlOutcome:
    """One control, and whether the instrument refused what it was handed."""

    name: str
    rejected: bool
    mechanism: str
    detail: str
    findings: dict[str, Any]

    def as_record(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "rejected": self.rejected,
            "mechanism": self.mechanism,
            "detail": self.detail,
            "findings": self.findings,
        }


# -- C1 changed feature ------------------------------------------------------


def changed_feature(chart: Chart, system: ConstraintSystem, t012: T012System) -> ControlOutcome:
    """Rename each contact onto every sibling support feature of its own branch.

    Twelve substitutions at `n = 5`: four touching pairs, three siblings each. Every one
    must be refused, and the refusal that does the work is the exact base margin, because
    -- and this is a finding of the control rather than a nuisance -- the *gradients* do
    not always distinguish them. At Goebel's pose the pair rows are degenerate across the
    support features of a branch: the rotation columns vanish for every corner of the
    moving square, not only for the touching one, which is the same geometry that hides
    the middle square's rotation from `T-012`'s first order. A support feature identified
    by derivative agreement alone would therefore be identified wrongly, and the proof
    lane needs that stated rather than discovered later.
    """
    field = chart.field
    two = field.rational(2)
    active_keys = {key for key, _ in system.active_constraints()}
    t012_keys = set(t012.contact_keys)
    substitutions: list[dict[str, Any]] = []
    for report in system.touching_pairs:
        assert report.active_branch is not None and report.active_constraint is not None
        contact = report.active_constraint
        position = t012.contact_keys.index(contact.key)
        scale = embed(field, t012.scales[position])
        transported = [embed(field, target) for target in t012.rational_rows[position]]
        for substitute in report.active_branch.constraints:
            if substitute.key == contact.key:
                continue
            gradient = substitute.polynomial.gradient()
            differs = any(
                (value * scale - (target * two if index % DOF == 2 else target)).sign() != 0
                for index, (value, target) in enumerate(zip(gradient, transported, strict=True))
            )
            claimed = (active_keys - {contact.key}) | {substitute.key}
            substitutions.append(
                {
                    "contact": contact.key,
                    "substitute": substitute.key,
                    "substitute_margin": element_algebraic(substitute.margin),
                    "margin_is_nonzero": substitute.margin.sign() != 0,
                    "gradient_differs": differs,
                    "active_key_agreement_breaks": claimed != t012_keys,
                }
            )
    rejected = all(
        entry["margin_is_nonzero"] and entry["active_key_agreement_breaks"]
        for entry in substitutions
    )
    indistinguishable = sum(1 for entry in substitutions if not entry["gradient_differs"])
    return ControlOutcome(
        name="changed_feature",
        rejected=bool(substitutions) and rejected,
        mechanism=(
            "exact base margin must be zero for a contact, and the active key set must "
            "match T-012's contact list"
        ),
        detail=(
            f"all {len(substitutions)} sibling support features of the four contact "
            "branches have strictly nonzero base margin and break agreement with T-012's "
            f"contact list. {indistinguishable} of them nonetheless have exactly the same "
            "gradient as the contact they replace, so derivative agreement alone does not "
            "identify a support feature at this pose and the margin is what decides"
        ),
        findings={
            "substitutions": substitutions,
            "count": len(substitutions),
            "gradient_indistinguishable": indistinguishable,
            "finding": (
                "the pair rows are degenerate across the support features of a branch; "
                "support-feature identity is decided by exact margin, never by gradient"
            ),
        },
    )


# -- C2 zero margin ----------------------------------------------------------


def zero_margin(system: ConstraintSystem) -> ControlOutcome:
    """Offer a genuinely zero margin where the neighborhood needs a strict sign."""
    active = system.active_walls[0]
    forged = Neighborhood(
        conditions=(
            StrictCondition(
                key=active.key,
                role="inactive-wall-stays-slack",
                sense="positive",
                margin=active.margin,
                polynomial=active.polynomial,
            ),
        ),
        active_keys=(),
    )
    return ControlOutcome(
        name="zero_margin",
        rejected=not forged.valid(),
        mechanism="Neighborhood.valid requires every declared sign to be strict",
        detail=(
            f"{active.key} has base margin exactly zero; presenting it as a strictly "
            "positive neighborhood condition is refused, because continuity carries a "
            "strict sign into a neighborhood and carries nothing at all from zero"
        ),
        findings={
            "key": active.key,
            "margin": element_algebraic(active.margin),
            "declared_sense": "positive",
            "neighborhood_valid": forged.valid(),
            "failures": list(forged.failures()),
        },
    )


# -- C3 omitted constraint ---------------------------------------------------


def omitted_constraint(chart: Chart) -> ControlOutcome:
    """Delete one separating branch and see whether the cardinality guard notices."""
    book = build_book(chart)
    pruned_pairs = list(book.pairs)
    pruned_pairs[0] = pruned_pairs[0][1:]
    pruned = InequalityBook(chart=chart, walls=book.walls, pairs=tuple(pruned_pairs))
    complete = pruned.enumeration_is_complete()

    raised = False
    message = ""
    original = build_book

    def stub(_: Chart) -> InequalityBook:
        return pruned

    module = __import__("sqpack.local_rigidity.system", fromlist=["build_book"])
    module.build_book = stub  # type: ignore[assignment]
    try:
        build_system(chart)
    except IncompleteEnumerationError as error:
        raised = True
        message = str(error)
    finally:
        module.build_book = original  # type: ignore[assignment]

    return ControlOutcome(
        name="omitted_constraint",
        rejected=(not complete) and raised,
        mechanism="expected cardinality recomputed from the pose, compared to the actual",
        detail=(
            "dropping one of the eighty separating-axis branches leaves a system whose "
            "feasible set is larger than the geometry's; the cardinality guard refuses "
            f"before any margin is read ({message[:96]})"
        ),
        findings={
            "expected": pruned.expected_cardinality(),
            "actual": pruned.actual_cardinality(),
            "enumeration_reported_complete": complete,
            "build_system_raised": raised,
        },
    )


# -- C4 invented contact -----------------------------------------------------


def invented_contact(system: ConstraintSystem, t012: T012System) -> ControlOutcome:
    """Declare a slack inequality to be a contact."""
    invented = system.inactive_walls[0]
    claimed = {key for key, _ in system.active_constraints()} | {invented.key}
    agrees = claimed == set(t012.contact_keys)
    margin_is_zero = invented.margin.sign() == 0
    return ControlOutcome(
        name="invented_contact",
        rejected=(not agrees) and (not margin_is_zero),
        mechanism="active keys must match T-012's contacts, and each must have margin zero",
        detail=(
            f"{invented.key} has base margin {element_algebraic(invented.margin)}, which "
            "is strictly positive; adding it to the active set makes the local system "
            "smaller than the geometry's and breaks agreement with T-012's contact list"
        ),
        findings={
            "invented_key": invented.key,
            "margin": element_algebraic(invented.margin),
            "margin_is_zero": margin_is_zero,
            "active_keys_still_agree_with_t012": agrees,
        },
    )


# -- C5 side release ---------------------------------------------------------


def released_side_pose(pose: BasePose, growth: FieldElement) -> BasePose:
    """The same five squares, in a strictly larger container."""
    return BasePose(
        label=f"{pose.label}+side{growth.text()}",
        field=pose.field,
        side=pose.side + growth,
        centres=pose.centres,
        corners=pose.corners,
    )


def side_release(chart: Chart) -> ControlOutcome:
    """Grow the container and exhibit exactly feasible neighbours of the same pose."""
    field = chart.field
    growth = field.rational(1) / field.rational(1000)
    released = Chart(released_side_pose(chart.pose, growth), chart.transform)
    book = build_book(released)
    probe = probe_axes(book)
    fixed = probe_axes(build_book(chart))
    return ControlOutcome(
        name="side_release",
        rejected=probe.found_witness and not fixed.found_witness,
        mechanism="axis probe at a released side finds exactly feasible distinct poses",
        detail=(
            "at side + 1/1000 the identical pose has "
            f"{len(probe.witnesses)} exactly feasible chart neighbours on the coordinate "
            "axes, where at the declared fixed side it has none; the fixed-side qualifier "
            "is load-bearing and cannot be dropped from the claim"
        ),
        findings={
            "growth": element_algebraic(growth),
            "released_side": element_algebraic(released.pose.side),
            "released_witnesses": [
                {"variable": one.variable, "value": one.value} for one in probe.witnesses
            ],
            "fixed_side_witnesses": len(fixed.witnesses),
        },
    )


# -- C6 wrong chart ----------------------------------------------------------


WRONG_DENOMINATOR = HalfAngleTransform(
    name="wrong-denominator-1-minus-u-squared",
    denominator_coefficients=(1, 0, -1),
    matrix_builder="half-angle",
)
WRONG_MATRIX = HalfAngleTransform(
    name="wrong-matrix-unscaled-off-diagonal",
    denominator_coefficients=(1, 0, 1),
    matrix_builder="unscaled-off-diagonal",
)
WRONG_ORIENTATION = HalfAngleTransform(
    name="wrong-matrix-sign-flipped-off-diagonal",
    denominator_coefficients=(1, 0, 1),
    matrix_builder="sign-flipped-off-diagonal",
)


def wrong_chart(pose: BasePose) -> ControlOutcome:
    """Three impostor transforms, each of which must fail the chart's own checks."""
    results: dict[str, Any] = {}
    for transform in (WRONG_DENOMINATOR, WRONG_MATRIX, WRONG_ORIENTATION):
        try:
            Chart(pose, transform).require_valid()
        except ChartPreconditionError as error:
            results[transform.name] = {"refused": True, "reason": str(error)[:140]}
        else:
            results[transform.name] = {"refused": False, "reason": ""}
    return ControlOutcome(
        name="wrong_chart",
        rejected=all(entry["refused"] for entry in results.values()),
        mechanism="denominator sum-of-squares and M^T M = D^2 I, checked before margins",
        detail=(
            "1 - u^2 vanishes at u = +-1 so it cannot clear an inequality without "
            "flipping its sense, and both off-diagonal deviations break "
            "M^T M = D^2 I so the cleared normal is not a rotation of the base normal"
        ),
        findings=results,
    )


# -- C7 certificate drift ----------------------------------------------------


def certificate_drift(determination: Determination, system: ConstraintSystem) -> ControlOutcome:
    """Change one retained margin and require the digest to move."""
    payload = build_payload(determination, system)
    before = digest(payload)
    mutated = copy.deepcopy(payload)
    mutated["walls"][0]["margin"] = "poly[999,0]"
    after = digest(mutated)
    second = copy.deepcopy(payload)
    second["neighborhood"]["conditions"][0]["holds"] = False
    third = digest(second)
    return ControlOutcome(
        name="certificate_drift",
        rejected=before not in (after, third) and digest(payload) == before,
        mechanism="SHA-256 over canonical sorted JSON of the exact record",
        detail=(
            "mutating one wall margin and, separately, one neighborhood condition's "
            "verdict both move the digest, and rebuilding the untouched payload "
            "reproduces it"
        ),
        findings={
            "digest": before,
            "after_margin_mutation": after,
            "after_condition_mutation": third,
            "stable_on_rebuild": digest(build_payload(determination, system)) == before,
        },
    )


# -- C8 exp-034's fixed-side angle-and-slide family ---------------------------


def _axis_corners(field: NumberField, cx: FieldElement, cy: FieldElement):
    half = field.rational(1) / field.rational(2)
    return [
        (cx - half, cy - half),
        (cx + half, cy - half),
        (cx + half, cy + half),
        (cx - half, cy + half),
    ]


def _diagonal_corners(field: NumberField, cx: FieldElement, cy: FieldElement):
    reach = field.alpha / field.rational(2)
    return [
        (cx + reach, cy),
        (cx, cy + reach),
        (cx - reach, cy),
        (cx, cy - reach),
    ]


def exp034_pose(field: NumberField, slide: FieldElement) -> BasePose:
    """`exp-033`'s endpoint with `exp-034`'s square 0 slid by `slide` along `(1, 1)`.

    Coordinates are transcribed from the retained records
    `exp-033-h-023-n5-equal-side-face.json` (`exact_model.endpoint_a`, orientations
    `axis, axis, axis, diagonal, diagonal`) and `exp-034-h-023-n5-angle-sheet.json`
    (`sheet_certificate.parameters.moving_square`). Nothing is inferred from a figure.
    """
    q = field.rational
    root = field.alpha
    side = q(1) + root * q(5) / q(4)
    centres = [
        (q(1) / q(2) + slide, q(5) / q(2) - root / q(4) + slide),
        (q(1) / q(2) + root * q(5) / q(4), q(1) / q(2)),
        (q(1) / q(2), q(1) / q(2)),
        (q(1) + root * q(3) / q(4), q(1) + root * q(3) / q(4)),
        (q(1) / q(2) + root * q(5) / q(8), q(3) / q(2) - root / q(8)),
    ]
    corners = [
        _axis_corners(field, *centres[0]),
        _axis_corners(field, *centres[1]),
        _axis_corners(field, *centres[2]),
        _diagonal_corners(field, *centres[3]),
        _diagonal_corners(field, *centres[4]),
    ]
    return BasePose(
        label=f"exp034-angle-and-slide(u={slide.text()})",
        field=field,
        side=side,
        centres=tuple(centres),
        corners=tuple(tuple(square) for square in corners),
    )


def exp034_angle_and_slide(chart: Chart) -> ControlOutcome:
    """Decide, exactly, where `exp-034`'s family lives and whether Goebel's pose has it.

    Three questions, each answered by computation and none assumed:

    1. is `exp-034`'s container side Goebel's side? If not, the family is not in the
       fixed-side configuration space `H-060` is about, and cannot pass through the
       optimum whatever else is true of it;
    2. at its own side, is the family exactly feasible and nonconstant? The instrument's
       feasibility predicate must find the flex that `exp-034` certified, or the predicate
       is too strict to be trusted at Goebel's pose either;
    3. does the same angle-and-slide motion, applied in Goebel's own chart at Goebel's
       side, produce a feasible configuration? That is the import the control refuses.
    """
    field = chart.field
    q = field.rational
    root = field.alpha
    exp034_side = q(1) + root * q(5) / q(4)
    side_difference = exp034_side - chart.pose.side
    same_side = side_difference.sign() == 0

    # 1/2 of the declared slide strip 3*sqrt(2)/2 - 2, so the base sits in its interior.
    interior = (root * q(3) / q(2) - q(2)) / q(2)
    base = exp034_pose(field, interior)
    book = build_book(Chart(base, chart.transform))
    base_feasible = is_feasible(book, [field.zero] * (base.count * DOF))

    family: dict[str, list[FieldElement]] = {}
    for power in (1, 2, 3, 4):
        step = interior / q(2**power)
        for sign in (1, -1):
            point = [field.zero] * (base.count * DOF)
            point[0] = step * q(sign)
            point[1] = step * q(sign)
            family[f"slide{sign:+d}/2^{power}"] = point
        angle = q(sign := 1) / q(1000 * 2**power)
        for turn in (angle, -angle):
            point = [field.zero] * (base.count * DOF)
            point[2] = turn
            family[f"turn{turn.text()}"] = point
    at_home = probe_family(book, family)

    # The same motion pattern, imported to Goebel's fixed side.
    gobel_book = build_book(chart)
    imported: dict[str, list[FieldElement]] = {}
    for name, point in family.items():
        imported[name] = list(point)
    at_gobel = probe_family(gobel_book, imported)

    family_is_here = at_gobel.found_witness
    return ControlOutcome(
        name="exp034_angle_and_slide",
        rejected=(not same_side) and (not family_is_here) and at_home.found_witness,
        mechanism=(
            "exact side comparison, plus the instrument's own feasibility predicate run "
            "at both poses"
        ),
        detail=(
            f"exp-034's side is {element_algebraic(exp034_side)} and Goebel's is "
            f"{element_algebraic(chart.pose.side)}, differing by "
            f"{element_algebraic(side_difference)}, so the family is not in the fixed-side "
            f"configuration space of H-060. At its own side the family is real: "
            f"{len(at_home.witnesses)} of {at_home.tested} probed members are exactly "
            f"feasible. Imported to Goebel's side and chart, "
            f"{len(at_gobel.witnesses)} of {at_gobel.tested} are feasible"
        ),
        findings={
            "exp034_side": element_algebraic(exp034_side),
            "gobel_side": element_algebraic(chart.pose.side),
            "side_difference": element_algebraic(side_difference),
            "sides_are_equal": same_side,
            "exp034_base_is_feasible": base_feasible,
            "family_members_probed": at_home.tested,
            "family_members_feasible_at_own_side": len(at_home.witnesses),
            "family_members_feasible_at_gobel_side": len(at_gobel.witnesses),
            "family_passes_through_the_optimum": family_is_here and same_side,
        },
    )


# -- the suite ---------------------------------------------------------------


def run_all(
    chart: Chart, system: ConstraintSystem, determination: Determination, t012: T012System
) -> list[ControlOutcome]:
    """Every control, in a fixed order, so the receipt is byte-stable."""
    return [
        changed_feature(chart, system, t012),
        zero_margin(system),
        omitted_constraint(chart),
        invented_contact(system, t012),
        side_release(chart),
        wrong_chart(chart.pose),
        certificate_drift(determination, system),
        exp034_angle_and_slide(chart),
    ]
