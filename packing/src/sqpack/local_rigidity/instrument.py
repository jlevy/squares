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

from dataclasses import dataclass, field as dataclass_field

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


def probe_family(
    book: InequalityBook, points: dict[str, list[FieldElement]]
) -> ProbeResult:
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
            and not self.refusals
        )


def assess(
    chart: Chart, t012: T012System | None = None
) -> tuple[Determination, ConstraintSystem]:
    """Run the full instrument at one pose, refusing rather than guessing."""
    system = build_system(chart)
    neighborhood = build_neighborhood(system)
    certificate = bind(chart, system, t012) if t012 is not None else None
    probe = probe_axes(system.book)
    refusals: list[str] = []
    if not neighborhood.valid():
        refusals.extend(f"non-strict neighborhood condition: {key}" for key in
                        neighborhood.failures())
    if certificate is not None and not certificate.holds:
        refusals.append("the T-012 binding does not hold row by row")
    if probe.found_witness:
        refusals.append(
            f"{len(probe.witnesses)} exactly feasible chart neighbours were exhibited"
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
        refusals=tuple(refusals),
    )
    return determination, system
