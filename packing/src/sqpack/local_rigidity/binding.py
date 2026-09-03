"""Exact transfer of the chart's derivatives onto `T-012`'s first- and second-order data.

`T-012` decides two things at Goebel's `n = 5` pose, in `(v, omega)` coordinates: the
first-order cone `{x : A x >= 0}` is one line, and a non-negative self-stress `w` with
`w . A = 0` and `w . q < 0` refuses every second-order correction along it. Those
certificates are about a *linearisation*. The curve-selection argument needs them about
the *chart*, and the two are the same statement only if the chart's polynomial derivatives
reproduce `A` and `q` under a declared coordinate change.

That is what this module certifies, exactly and row by row.

The coordinate change is forced by the chart, not chosen: a chart ray `z(t) = t * zeta`
moves square `k`'s centre at rate `(zeta_a, zeta_b)` and turns it at rate
`d/dt 2 atan(t zeta_u) = 2 zeta_u`, so

    S : (a-rate, b-rate, u-rate)  |->  (v_x, v_y, omega) = (a-rate, b-rate, 2 * u-rate),

block-diagonal, `diag(1, 1, 2)` per square, invertible with positive determinant. Two
consequences are used and both are checked rather than assumed:

- **Gradients.** The chart polynomial is `G_j = D_j * g_j` with `D_j` the cleared
  denominator. At the pose `g_j = 0` for every active constraint, so the product rule
  leaves `grad G_j = D_j(0) * (A_j S)` with no `grad D_j` term. Every `D_j(0)` is `1`
  here, and the identity is verified per coordinate rather than inferred from that.
- **Second jets.** Along the free direction, `g_j` and its chart gradient both vanish at
  the pose, so `G_j'' = D_j(0) * g_j''`. And `g_j''` along the chart ray equals `q_j`
  along the straight `(v, omega)` line, because `2 atan(t zeta)` is odd: its second
  derivative at zero is zero, so the two paths agree to second order even though they
  differ at third.

`T-012` uses rationalised rows, each scaled by a positive `s_j` in `{1, sqrt 2}`, and
scales `q` by the same factor. The certificate below therefore states the binding with
that single positive scalar per row, which is exactly the "positive row scalings" the
hypothesis allows.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqpack.field import FieldElement, NumberField
from sqpack.local_rigidity.chart import DOF, Chart
from sqpack.local_rigidity.system import ConstraintSystem


class BindingError(RuntimeError):
    """The chart and `T-012` disagree, which invalidates the transfer, not just a row."""


class FieldMismatchError(BindingError):
    """The two instruments are not working over the same exact field.

    `sqpack.field` decides equality by object identity of the `NumberField`, and both
    instruments build their own. Comparing elements across two instances is therefore
    refused by the arithmetic itself -- correctly, because two fields with different
    minimal polynomials or different isolating intervals are different fields and an
    element of one means nothing in the other. The remedy is not to loosen the check but
    to prove the two declarations coincide and then transport coefficients, which is what
    `embed` does.
    """


def embed(target: NumberField, element: FieldElement) -> FieldElement:
    """Re-express one field element in an identically declared field.

    Legitimate only after `require_same_field`: the power basis `1, alpha, ...` means the
    same thing in both fields exactly when both were declared from the same normalised
    minimal polynomial and the same isolating interval, and then transporting coefficients
    is the identity map, not an approximation.
    """
    return target.element(list(element.coeffs))


def require_same_field(left: NumberField, right: NumberField) -> None:
    """Refuse two field declarations that are not the same field, exactly."""
    if left is right:
        return
    left_certificate = left.precondition_certificate()
    right_certificate = right.precondition_certificate()
    for name in (
        "normalized_minimal_polynomial",
        "declared_isolating_interval",
        "irreducible_over_q",
    ):
        if left_certificate[name] != right_certificate[name]:
            raise FieldMismatchError(
                f"the chart and T-012 declare different fields: {name} is "
                f"{left_certificate[name]!r} against {right_certificate[name]!r}; their "
                "elements are not comparable and no binding between them is meaningful"
            )


@dataclass(frozen=True, slots=True)
class T012System:
    """`T-012`'s exact first- and second-order data, as this instrument consumes it."""

    field: NumberField
    contact_keys: tuple[str, ...]
    raw_rows: tuple[tuple[FieldElement, ...], ...]
    rational_rows: tuple[tuple[FieldElement, ...], ...]
    scales: tuple[FieldElement, ...]
    variable_names: tuple[str, ...]
    free_names: tuple[str, ...]
    second_order: dict[str, tuple[FieldElement, ...]]
    """Free-direction name -> the scaled `q` vector `T-012` runs its Farkas test on."""


def contact_key(kind: str, moving: int, corner: int, host: int | None, edge: int | None,
                wall: str | None) -> str:
    """One name for a contact, shared by both instruments, so rows match by identity.

    Matching by *position* would silently pass whenever both enumerations happened to
    agree in length, which is the failure `controls.omitted_constraint` exists to catch.
    """
    if kind == "wall":
        return f"wall/{moving}/{corner}/{wall}"
    return f"pair/{host}/{edge}/{moving}/{corner}"


def load_t012_system() -> T012System:
    """Read `T-012`'s rows, scales and second-order terms from the retained assessor.

    Imported lazily and named here rather than reimplemented, because a binding
    certificate against a private copy of the rows would certify agreement with itself.
    The import is deliberately not at module scope: `sqpack` is a library and `devtools`
    is a sibling tool tree, so the dependency is confined to the one function that needs
    it and is reported as a typed error if the tool tree is not on the path.
    """
    try:
        from devtools.assess_n5_rigidity import (  # noqa: PLC0415 - tool-tree dependency
            active_contacts,
            constraint_rows,
            load_pose,
            rationalize,
            row_scales,
            second_order_terms,
            unconstrained,
            variable_names,
        )
    except ImportError as error:  # pragma: no cover - path misconfiguration only
        raise BindingError(
            "devtools.assess_n5_rigidity is not importable, so T-012's rows cannot be "
            "read; the binding certificate must compare against that instrument and not "
            "against a private copy of it"
        ) from error

    pose = load_pose()
    contacts = active_contacts(pose)
    raw = constraint_rows(pose, contacts)
    rational = rationalize(pose, raw)
    scales = row_scales(pose, raw)
    names = variable_names(pose.count)
    free = [names[index] for index in range(len(names)) if unconstrained(rational, index)]

    second: dict[str, tuple[FieldElement, ...]] = {}
    for name in free:
        index = names.index(name)
        unit = [
            pose.field.rational(1 if position == index else 0)
            for position in range(len(names))
        ]
        terms = second_order_terms(pose, contacts, unit)
        second[name] = tuple(
            term * scale for term, scale in zip(terms, scales, strict=True)
        )
    return T012System(
        field=pose.field,
        contact_keys=tuple(
            contact_key(
                contact.kind, contact.moving, contact.corner, contact.host, contact.edge,
                contact.wall,
            )
            for contact in contacts
        ),
        raw_rows=tuple(tuple(row) for row in raw),
        rational_rows=tuple(tuple(row) for row in rational),
        scales=tuple(scales),
        variable_names=tuple(names),
        free_names=tuple(free),
        second_order=second,
    )


def transform_matrix_description(count: int) -> dict[str, Any]:
    """The declared coordinate change, as data the receipt can carry."""
    return {
        "name": "half-angle-rate-to-angular-velocity",
        "shape": f"block diagonal, {count} blocks of diag(1, 1, 2)",
        "chart_order": "(a_k, b_k, u_k)",
        "target_order": "(vx_k, vy_k, w_k)",
        "reason": "d/dt 2*atan(t*zeta) = 2*zeta at t = 0",
        "determinant_sign": "+1",
        "invertible": True,
    }


def _apply_transform(row: tuple[FieldElement, ...], count: int) -> list[FieldElement]:
    """`A_j S`: keep the translation columns, double the rotation column."""
    field = row[0].field
    two = field.rational(2)
    transformed = list(row)
    for square in range(count):
        transformed[square * DOF + 2] = row[square * DOF + 2] * two
    return transformed


@dataclass(frozen=True, slots=True)
class RowBinding:
    """One active constraint, bound to one `T-012` row by one positive scalar."""

    key: str
    t012_index: int
    scalar: str
    scalar_is_positive: bool
    denominator_at_base: str
    gradient_matches: bool
    second_jet_matches: dict[str, bool]


@dataclass(frozen=True, slots=True)
class BindingCertificate:
    """The complete, exact statement that the chart carries `T-012`'s certificates."""

    transform: dict[str, Any]
    rows: tuple[RowBinding, ...]
    active_key_agreement: bool
    missing_from_chart: tuple[str, ...]
    missing_from_t012: tuple[str, ...]
    chart_free_variables: tuple[str, ...]
    t012_free_variables: tuple[str, ...]
    free_variables_correspond: bool
    directions: tuple[str, ...]

    @property
    def holds(self) -> bool:
        return (
            self.active_key_agreement
            and not self.missing_from_chart
            and not self.missing_from_t012
            and self.free_variables_correspond
            and all(row.scalar_is_positive for row in self.rows)
            and all(row.gradient_matches for row in self.rows)
            and all(
                matched
                for row in self.rows
                for matched in row.second_jet_matches.values()
            )
        )


def bind(
    chart: Chart, system: ConstraintSystem, t012: T012System
) -> BindingCertificate:
    """Certify, exactly, that the chart's jets are `T-012`'s rows and `q` rescaled."""
    count = chart.pose.count
    field = chart.field
    origin = chart.origin()
    require_same_field(field, t012.field)

    active = dict(system.active_constraints())
    t012_keys = list(t012.contact_keys)
    missing_from_chart = tuple(key for key in t012_keys if key not in active)
    missing_from_t012 = tuple(key for key in active if key not in set(t012_keys))

    # The chart direction realising each T-012 free direction: S^{-1} applied to the unit
    # vector, so a rotation rate of one becomes a half-angle rate of one half.
    half = field.rational(1) / field.rational(2)
    directions: dict[str, list[FieldElement]] = {}
    for name in t012.free_names:
        index = t012.variable_names.index(name)
        vector = [field.zero] * chart.arity
        vector[index] = half if index % DOF == 2 else field.one
        directions[name] = vector

    rows: list[RowBinding] = []
    for position, key in enumerate(t012_keys):
        polynomial = active.get(key)
        if polynomial is None:
            continue
        scale = embed(field, t012.scales[position])
        gradient = polynomial.gradient()
        wanted = _apply_transform(
            tuple(embed(field, value) for value in t012.rational_rows[position]), count
        )
        gradient_matches = all(
            (value * scale - target).sign() == 0
            for value, target in zip(gradient, wanted, strict=True)
        )
        jets: dict[str, bool] = {}
        for name, direction in directions.items():
            observed = polynomial.second_derivative_along(direction) * scale
            expected = embed(field, t012.second_order[name][position])
            jets[name] = (observed - expected).sign() == 0
        denominator = _denominator_at_base(chart, key, origin)
        rows.append(
            RowBinding(
                key=key,
                t012_index=position,
                scalar=scale.text(),
                scalar_is_positive=scale.sign() > 0,
                denominator_at_base=denominator.text(),
                gradient_matches=gradient_matches,
                second_jet_matches=jets,
            )
        )

    chart_free = tuple(
        chart.variable_names()[index]
        for index in range(chart.arity)
        if all(
            polynomial.derivative(index).evaluate(origin).sign() == 0
            for polynomial in active.values()
        )
    )
    corresponds = tuple(
        name.replace("w", "u", 1) if name.startswith("w") else name
        for name in t012.free_names
    ) == chart_free
    return BindingCertificate(
        transform=transform_matrix_description(count),
        rows=tuple(rows),
        active_key_agreement=(set(active) == set(t012_keys)),
        missing_from_chart=missing_from_chart,
        missing_from_t012=missing_from_t012,
        chart_free_variables=chart_free,
        t012_free_variables=tuple(t012.free_names),
        free_variables_correspond=corresponds,
        directions=tuple(sorted(directions)),
    )


def _denominator_at_base(chart: Chart, key: str, origin: list[FieldElement]) -> FieldElement:
    """`D_j(0)` for one constraint key: the positive factor the chart clears by."""
    parts = key.split("/")
    if parts[0] == "wall":
        return chart.denominator(int(parts[1])).evaluate(origin)
    host, moving = int(parts[1]), int(parts[3])
    return chart.denominator(host).evaluate(origin) * chart.denominator(moving).evaluate(
        origin
    )
