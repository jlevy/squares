"""The instrument's determination: what it certifies, and what it deliberately does not.

`H-060` is a claim about *isolation*, and no computation in this package decides it. What
the instrument produces is the object the curve-selection and coefficient argument needs
and did not have: an exact statement that on a declared open neighborhood `U` of the pose,
the feasible set is *exactly* the active inequality system, together with an exact transfer
of that system's first- and second-order data onto `T-012`'s certificates.

So the determination below carries `isolation_decided = False` unconditionally. The two
findings it does carry are:

- `neighborhood_certified` -- on `U`, a configuration is feasible exactly when the active
  constraints hold. This rests on exact base margins and continuity, never on a radius.
- `binding_holds` -- the chart's gradients and second jets are `T-012`'s `A` and `q` under
  the declared transform and one positive scalar per row.

`probe` searches for feasible neighbours along the chart axes. Finding one *refutes* the
proposed neighborhood or the pose's isolation and is decisive; finding none proves nothing
at all, and `probe_is_not_a_proof` says so in the record so that a later reader cannot mistake
an empty search for a theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field as dataclass_field

from sqpack.field import FieldElement
from sqpack.local_rigidity.binding import BindingCertificate, T012System, bind
from sqpack.local_rigidity.chart import Chart
from sqpack.local_rigidity.system import (
    ConstraintSystem,
    InequalityBook,
    Neighborhood,
    build_neighborhood,
    build_system,
    is_feasible,
)

PROBE_DENOMINATORS: tuple[int, ...] = (10, 100, 1000, 10**4, 10**5, 10**6)
"""Reciprocals probed along each chart axis, in both directions."""


@dataclass(frozen=True, slots=True)
class FeasibleNeighbour:
    """One exactly feasible chart point that is not the pose."""

    variable: str
    value: str
    feasible: bool


@dataclass(frozen=True, slots=True)
class ProbeResult:
    """What the axis search found, and what its emptiness is worth."""

    tested: int
    witnesses: tuple[FeasibleNeighbour, ...]
    probe_is_not_a_proof: str = (
        "an empty probe is not isolation: it tests finitely many points on fifteen "
        "coordinate axes and says nothing about a curve leaving the pose along any other "
        "direction, nor about an arc whose first nonzero coefficient is above order one"
    )

    @property
    def found_witness(self) -> bool:
        return bool(self.witnesses)


def probe_axes(
    book: InequalityBook, denominators: tuple[int, ...] = PROBE_DENOMINATORS
) -> ProbeResult:
    """Test `base +- 1/d * e_i` for feasibility, exactly, on every chart axis."""
    chart = book.chart
    field = chart.field
    names = chart.variable_names()
    witnesses: list[FeasibleNeighbour] = []
    tested = 0
    for index in range(chart.arity):
        for denominator in denominators:
            for sign in (1, -1):
                value = field.rational(sign) / field.rational(denominator)
                point = chart.origin()
                point[index] = value
                tested += 1
                if is_feasible(book, point):
                    witnesses.append(
                        FeasibleNeighbour(
                            variable=names[index],
                            value=f"{sign}/{denominator}",
                            feasible=True,
                        )
                    )
    return ProbeResult(tested=tested, witnesses=tuple(witnesses))


def probe_family(book: InequalityBook, points: dict[str, list[FieldElement]]) -> ProbeResult:
    """Test a named family of chart points for exact feasibility.

    Used by the `exp-034` control, where the family is not axis-aligned and where finding
    feasible members is the expected -- and required -- outcome.
    """
    witnesses: list[FeasibleNeighbour] = []
    for name, point in points.items():
        if is_feasible(book, point):
            witnesses.append(FeasibleNeighbour(variable=name, value="family", feasible=True))
    return ProbeResult(tested=len(points), witnesses=tuple(witnesses))


@dataclass(frozen=True, slots=True)
class Determination:
    """The instrument's whole output, with its scope boundary stated in the record."""

    pose_label: str
    chart_name: str
    counts: dict[str, int]
    active_keys: tuple[str, ...]
    enumeration_complete: bool
    neighborhood: Neighborhood
    neighborhood_certified: bool
    binding: BindingCertificate | None
    binding_holds: bool
    probe: ProbeResult
    audit: ReductionAudit | None = None
    refusals: tuple[str, ...] = ()
    isolation_decided: bool = False
    scope: str = (
        "fixed side; one labeled pose; the local feasible set on U only. Isolation, a "
        "numerical radius, global uniqueness and prior-art novelty are all outside this"
    )
    notes: tuple[str, ...] = dataclass_field(default_factory=tuple)

    @property
    def instrument_ready(self) -> bool:
        """Every certificate exact, and no exhibited feasible neighbour."""
        return (
            self.enumeration_complete
            and self.neighborhood_certified
            and self.binding_holds
            and not self.probe.found_witness
            and self.audit is not None
            and self.audit.consistent
            and not self.refusals
        )


def assess(
    chart: Chart, t012: T012System | None = None, *, audit: bool = True
) -> tuple[Determination, ConstraintSystem]:
    """Run the full instrument at one pose, refusing rather than guessing."""
    system = build_system(chart)
    neighborhood = build_neighborhood(system)
    certificate = bind(chart, system, t012) if t012 is not None else None
    probe = probe_axes(system.book)
    reduction = audit_reduction(system, neighborhood) if audit else None
    refusals: list[str] = []
    if not neighborhood.valid():
        refusals.extend(
            f"non-strict neighborhood condition: {key}" for key in neighborhood.failures()
        )
    if certificate is not None and not certificate.holds:
        refusals.append("the T-012 binding does not hold row by row")
    if probe.found_witness:
        refusals.append(
            f"{len(probe.witnesses)} exactly feasible chart neighbours were exhibited"
        )
    if reduction is not None and not reduction.consistent:
        refusals.append(
            f"the local reduction disagreed with full feasibility at "
            f"{len(reduction.counterexamples)} sampled points inside U"
        )
    determination = Determination(
        pose_label=chart.pose.label,
        chart_name=chart.transform.name,
        counts=system.counts(),
        active_keys=tuple(key for key, _ in system.active_constraints()),
        enumeration_complete=system.book.enumeration_is_complete(),
        neighborhood=neighborhood,
        neighborhood_certified=neighborhood.valid(),
        binding=certificate,
        binding_holds=bool(certificate is not None and certificate.holds),
        probe=probe,
        audit=reduction,
        refusals=tuple(refusals),
    )
    return determination, system


@dataclass(frozen=True, slots=True)
class ReductionAudit:
    """Does the claimed local reduction actually hold, at exactly evaluated points?

    The reduction -- *on `U`, feasible exactly when the twenty active inequalities hold* --
    is established by exact base margins and continuity, and the argument is the proof.
    This audit is not that proof and does not replace it. It is the check that the
    *statement* is the right statement: at every sampled point that lies inside `U`, the
    full separating-axis feasibility predicate and the twenty-inequality local system are
    compared, and a single disagreement would mean the reduction as written is false.

    A disagreement here is decisive against the instrument. Agreement is corroboration and
    nothing more, which `audit_is_not_a_proof` records so the distinction survives.
    """

    points_tested: int
    points_inside: int
    agreements: int
    counterexamples: tuple[dict[str, str], ...]
    audit_is_not_a_proof: str = (
        "agreement at finitely many sampled points corroborates the reduction; the "
        "reduction itself holds by the exact base margins and continuity of the "
        "polynomials, and nothing here narrows or replaces that argument"
    )

    @property
    def consistent(self) -> bool:
        return not self.counterexamples


def sample_points(chart: Chart) -> dict[str, list[FieldElement]]:
    """A fixed, deterministic set of exact chart points around the pose.

    Deterministic by construction rather than by a seeded generator, so a reviewer replays
    the same points and the receipt stays byte-stable.
    """
    field = chart.field
    names = chart.variable_names()
    points: dict[str, list[FieldElement]] = {}
    for index in range(chart.arity):
        for denominator in (8, 64, 512, 4096):
            for sign in (1, -1):
                point = chart.origin()
                point[index] = field.rational(sign) / field.rational(denominator)
                points[f"axis:{names[index]}:{sign}/{denominator}"] = point
    for index in range(chart.arity):
        partner = (index + 1) % chart.arity
        for denominator in (16, 256):
            for signs in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                point = chart.origin()
                point[index] = field.rational(signs[0]) / field.rational(denominator)
                point[partner] = field.rational(signs[1]) / field.rational(denominator)
                key = (
                    f"pair:{names[index]}{signs[0]:+d}:"
                    f"{names[partner]}{signs[1]:+d}:1/{denominator}"
                )
                points[key] = point
    for denominator in (32, 1024):
        for sign in (1, -1):
            point = [
                field.rational(sign * (1 if position % 2 == 0 else -1))
                / field.rational(denominator)
                for position in range(chart.arity)
            ]
            points[f"alternating:{sign}/{denominator}"] = point
    return points


def audit_reduction(system: ConstraintSystem, neighborhood: Neighborhood) -> ReductionAudit:
    """Compare the full feasibility predicate against the local system, inside `U`."""
    active = system.active_constraints()
    inside = 0
    agreements = 0
    counterexamples: list[dict[str, str]] = []
    for name, point in sorted(sample_points(system.chart).items()):
        in_u = True
        for condition in neighborhood.conditions:
            value = condition.polynomial.evaluate(point).sign()
            wanted = 1 if condition.sense == "positive" else -1
            if value != wanted:
                in_u = False
                break
        if not in_u:
            continue
        inside += 1
        full = is_feasible(system.book, point)
        local = all(polynomial.evaluate(point).sign() >= 0 for _, polynomial in active)
        if full == local:
            agreements += 1
        else:
            counterexamples.append(
                {
                    "point": name,
                    "full_separating_axis_feasibility": str(full),
                    "active_system_holds": str(local),
                }
            )
    return ReductionAudit(
        points_tested=len(sample_points(system.chart)),
        points_inside=inside,
        agreements=agreements,
        counterexamples=tuple(counterexamples),
    )


DECLARED_MATHEMATICAL_INPUTS: tuple[dict[str, str], ...] = (
    {
        "name": "separating-axis theorem for convex polygons",
        "statement": (
            "two convex polygons have disjoint interiors exactly when some edge normal "
            "of one of them separates them; equivalently the origin is outside their "
            "Minkowski difference, whose supporting normals are those edge normals"
        ),
        "used_for": (
            "the eight-branch disjunctive encoding of every pair, and the collapse of "
            "that disjunction to one branch inside U"
        ),
        "machine_checked_here": "no -- a cited theorem, not a computation",
    },
    {
        "name": "the rotation group's topology",
        "statement": (
            "u -> 2 atan(u) is a homeomorphism from R onto the open arc (-pi, pi), so "
            "the chart's image is an open neighborhood of the pose in (R^2 x S^1)^5"
        ),
        "used_for": "that a chart curve and a configuration curve are the same object",
        "machine_checked_here": (
            "partly -- injectivity and the punctured-circle image are verified as exact "
            "polynomial identities; the topological statement itself is cited"
        ),
    },
    {
        "name": "convexity of container and squares",
        "statement": (
            "a convex square lies inside a convex rectangle exactly when all four of its "
            "corners do, since the square is the convex hull of its corners"
        ),
        "used_for": (
            "reducing containment to the eighty corner-versus-wall inequalities rather "
            "than to a condition on the square's whole area"
        ),
        "machine_checked_here": "no -- standard",
    },
    {
        "name": "continuity of polynomials",
        "statement": (
            "a real polynomial map is continuous, so a strict sign is an open condition"
        ),
        "used_for": "that U is open and contains the pose, with no radius computed",
        "machine_checked_here": "no -- standard",
    },
)
"""What the instrument takes from mathematics rather than from its own computation.

Listed so that a reviewer auditing the theorem transfer can see the boundary without
reverse-engineering it from the code. Everything not on this list is decided here by
exact arithmetic.
"""
