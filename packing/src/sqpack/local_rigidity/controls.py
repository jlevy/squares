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
import dataclasses
from dataclasses import dataclass
from typing import Any

from sqpack.field import FieldElement, NumberField
from sqpack.local_rigidity.binding import T012System, bind
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
    ActiveMarginError,
    ConstraintSystem,
    IncompleteEnumerationError,
    InequalityBook,
    Neighborhood,
    StrictCondition,
    build_book,
    build_system,
    is_feasible,
    require_active_margins_zero,
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


# -- mutating the instrument's own inputs, so the controls exercise its refusals ----


def with_active_pair(system: ConstraintSystem, report, constraint) -> ConstraintSystem:
    """The same system, with one touching pair's declared contact replaced.

    Public because the tests mutate a system the same way the controls do, and reaching
    into a private helper to do it would couple them to how the mutation is spelled.
    """
    replaced = dataclasses.replace(report, active_constraint=constraint)
    pairs = tuple(
        replaced if existing.key == report.key else existing for existing in system.pairs
    )
    return dataclasses.replace(system, pairs=pairs)


def with_forged_active_wall(system: ConstraintSystem, constraint) -> ConstraintSystem:
    """The same system, with one slack wall inequality carrying a forged zero margin.

    Public for the same reason as `with_active_pair`.
    """
    forged = dataclasses.replace(constraint, margin=system.chart.field.zero)
    walls = tuple(
        forged if existing.key == constraint.key else existing for existing in system.walls
    )
    return dataclasses.replace(system, walls=walls)


def _guard_refuses(system: ConstraintSystem) -> tuple[bool, str]:
    """Does the recomputing active-margin guard refuse this system?"""
    try:
        require_active_margins_zero(system)
    except ActiveMarginError as error:
        return True, str(error)[:120]
    return False, ""


# -- C1 changed feature ------------------------------------------------------


def changed_feature(chart: Chart, system: ConstraintSystem, t012: T012System) -> ControlOutcome:
    """Rename each contact onto every sibling support feature, and make the tool refuse.

    Twelve substitutions at `n = 5`: four touching pairs, three siblings each. Each is
    applied twice, and each mutated system is handed back to the instrument rather than
    adjudicated here -- which is the correction the `BC-153` review required. The first
    version of this control compared keys and margins inline and never called `bind` or
    any guard, so it restated its own premises and could not have failed.

    - *key-swapped*: the active set names the sibling. `require_active_margins_zero`
      refuses because the sibling does not vanish at the pose, and `bind` refuses because
      the active keys no longer match `T-012`'s contact list.
    - *key-preserving forgery*: the contact keeps its name and its cached margin, but
      carries the sibling's polynomial. Only a guard that *recomputes* can see this, and
      only a gradient comparison can see it inside `bind`. Both are run.

    The finding the second version preserves: four of the twelve siblings have exactly the
    same gradient as the contact they replace -- the degeneracy that hides the middle
    square's rotation from first order -- so the gradient check alone catches eight, and
    the recomputing margin guard is what catches all twelve.

    The restricted second jet also separates all twelve, and that is **not** a second
    independent identifier. Along the host rotation the cleared jet is an exact affine
    function of the support feature's own base margin,

        G''(e_u4) = D'' * g(0) + 2 D'(0) g'(0) + D(0) * g''
                  = 2 * m - 4 * (m + 1/2)
                  = -2 * (m + 1),

    using `D = D_h D_k` with `D(0) = 1`, `D'(0) = 0`, `D''(0) = 2`, and the geometric
    `q = -omega^2 (m + 1/2)` at `omega = 2`. So the jet orders the support features exactly
    as their margins do and adds nothing the margin has not already decided. The identity
    is verified per substitution below rather than asserted, and the statement that
    survives is the plain one: the recomputed base margin is what decides.
    """
    field = chart.field
    one = field.one
    two = field.rational(2)
    unit_rotation = [field.zero] * chart.arity
    unit_rotation[chart.arity - 1] = one
    substitutions: list[dict[str, Any]] = []
    for report in system.touching_pairs:
        contact = report.active_constraint
        branch = report.active_branch
        if contact is None or branch is None:
            continue
        for substitute in branch.constraints:
            if substitute.key == contact.key:
                continue
            swapped = with_active_pair(system, report, substitute)
            swapped_guard, swapped_reason = _guard_refuses(swapped)
            swapped_certificate = bind(chart, swapped, t012)

            forgery = with_active_pair(
                system,
                report,
                dataclasses.replace(contact, polynomial=substitute.polynomial),
            )
            forged_guard, _ = _guard_refuses(forgery)
            forged_certificate = bind(chart, forgery, t012)
            forged_row = next(
                (row for row in forged_certificate.rows if row.key == contact.key), None
            )

            substitutions.append(
                {
                    "contact": contact.key,
                    "substitute": substitute.key,
                    "substitute_margin": element_algebraic(substitute.margin),
                    "key_swapped_guard_refused": swapped_guard,
                    "key_swapped_binding_refused": not swapped_certificate.holds,
                    "key_swapped_missing_from_t012": list(
                        swapped_certificate.missing_from_t012
                    ),
                    "key_swapped_reason": swapped_reason,
                    "forgery_guard_refused": forged_guard,
                    "forgery_binding_refused": not forged_certificate.holds,
                    "forgery_gradient_caught": bool(
                        forged_row is not None and not forged_row.gradient_matches
                    ),
                    "forgery_second_jet_caught": bool(
                        forged_row is not None
                        and not all(forged_row.second_jet_matches.values())
                    ),
                    "second_jet_is_affine_in_the_margin": (
                        substitute.polynomial.second_derivative_along(unit_rotation)
                        - (-(substitute.margin + one) * two)
                    ).sign()
                    == 0,
                }
            )
    rejected = bool(substitutions) and all(
        entry["key_swapped_guard_refused"]
        and entry["key_swapped_binding_refused"]
        and entry["forgery_guard_refused"]
        for entry in substitutions
    )
    gradient_caught = sum(1 for entry in substitutions if entry["forgery_gradient_caught"])
    jet_caught = sum(1 for entry in substitutions if entry["forgery_second_jet_caught"])
    affine_law = all(entry["second_jet_is_affine_in_the_margin"] for entry in substitutions)
    return ControlOutcome(
        name="changed_feature",
        rejected=rejected,
        mechanism=(
            "require_active_margins_zero recomputes every active margin, and bind "
            "re-checks key agreement and gradients; both are invoked on the mutated system"
        ),
        detail=(
            f"all {len(substitutions)} sibling substitutions are refused. Renaming the "
            "contact onto a sibling is refused by the recomputing margin guard and by the "
            "binding's key agreement; forging the contact's polynomial while keeping its "
            f"name and cached margin is refused by the recomputing guard in all "
            f"{len(substitutions)} cases and by the binding's gradient check in "
            f"{gradient_caught} of them, the other {len(substitutions) - gradient_caught} "
            "being gradient-degenerate against the contact they replace. The restricted "
            f"second jet also separates all {jet_caught}, but it is not an independent "
            "identifier: along the host rotation it is the exact affine function "
            "G''(e_u4) = -2*(margin + 1) of the support feature's own base margin "
            f"(verified here on all {len(substitutions)}: {affine_law}), so it separates "
            "support features precisely when their margins do. The recomputed base margin "
            "is what decides"
        ),
        findings={
            "substitutions": substitutions,
            "count": len(substitutions),
            "forgery_gradient_caught": gradient_caught,
            "forgery_second_jet_caught": jet_caught,
            "second_jet_affine_law": "G''(e_u4) = -2*(margin + 1), exactly",
            "second_jet_affine_law_holds": affine_law,
            "second_jet_is_an_independent_identifier": False,
            "finding": (
                "the pair rows are gradient-degenerate across some support features of a "
                "branch, and the restricted second jet is an affine reparametrisation of "
                "the base margin rather than an independent test of feature identity; the "
                "recomputed base margin is what decides"
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


def invented_contact(
    chart: Chart, system: ConstraintSystem, t012: T012System
) -> ControlOutcome:
    """Forge a zero margin onto a slack wall inequality and make the tool refuse.

    The first version of this control compared the enlarged key set against `T-012`'s and
    found it different -- which it was by construction, since the added key was chosen not
    to be in it. Nothing was invoked and nothing could have failed. This version builds
    the mutated `ConstraintSystem`, so that the enlarged active set is what the instrument
    actually reads, and requires both refusals: the guard, which recomputes the margin and
    finds it strictly positive, and `bind`, which finds a contact `T-012` does not have.
    """
    invented = system.inactive_walls[0]
    mutated = with_forged_active_wall(system, invented)
    claimed = {key for key, _ in mutated.active_constraints()}
    guard_refused, reason = _guard_refuses(mutated)
    certificate = bind(chart, mutated, t012)
    return ControlOutcome(
        name="invented_contact",
        rejected=(
            guard_refused
            and not certificate.holds
            and invented.key in certificate.missing_from_t012
        ),
        mechanism=(
            "require_active_margins_zero recomputes the forged margin, and bind reports "
            "the contact as absent from T-012's list; both run on the mutated system"
        ),
        detail=(
            f"{invented.key} carries a forged zero margin while its polynomial still "
            f"evaluates to {element_algebraic(invented.margin)} at the pose. The active "
            f"set grows to {len(claimed)}, the recomputing guard refuses, and the binding "
            "reports the invented key as missing from T-012's contact list"
        ),
        findings={
            "invented_key": invented.key,
            "recomputed_margin": element_algebraic(invented.margin),
            "forged_margin": "0",
            "active_set_size_after_mutation": len(claimed),
            "guard_refused": guard_refused,
            "guard_reason": reason,
            "binding_holds": certificate.holds,
            "binding_active_key_agreement": certificate.active_key_agreement,
            "binding_missing_from_t012": list(certificate.missing_from_t012),
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
        invented_contact(chart, system, t012),
        side_release(chart),
        wrong_chart(chart.pose),
        certificate_drift(determination, system),
        exp034_angle_and_slide(chart),
    ]
