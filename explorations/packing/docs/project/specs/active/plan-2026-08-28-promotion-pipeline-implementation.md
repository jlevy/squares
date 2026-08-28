# Feature: Promotion Pipeline Implementation

**Date:** 2026-08-28

**Author:** Claude (agent), from a design discussion with the repository owner

**Status:** Draft

## Overview

Build the code that turns a numerical square packing into a certified algebraic one, and
carries it back to re-verify.
Five sequential phases, each a working deliverable with its own controls.

This document is written to be read cold.
A reviewer should be able to judge the plan without opening another file, and an
implementing agent should be able to build from it without asking what a term means.

## Background

### The problem

`s(n)` is the side of the smallest square that holds `n` unit squares.
It is trivial when `n` is a perfect square and hard otherwise; the best known packings
for most `n` are constructions nobody has proved optimal.

A *packing* here is `n` unit squares placed by centre and angle inside `[0, s]^2` with
pairwise-disjoint interiors.
A *witness* is a serialized packing.
This repository stores witnesses under a soft schema called `Witness/v1` and verifies
them at three assurance levels: `reported` (someone said so), `numerically-checked` (we
recomputed in floating or multiprecision arithmetic), and `verified` (exact predicates
over rational or algebraic numbers, which is a proof).

### Why exactness is not optional

A tight packing has pairs whose true separation is exactly zero.
In floating arithmetic that is indistinguishable from a tiny overlap, and raising
precision does not fix it — it only moves the threshold.
So feasibility must be decided by exact sign tests over a number field, not by
tolerance. `sqpack.verify.verify_packing` is generic over the sign function for exactly
this reason: with `exact_sign` it is a proof, with `float_sign` it is a check.

### The six-step route, and what exists

Turning a float vector into a certified algebraic number goes:

1. **Numeric solve.** Propose a configuration, then quench it to a local optimum.
2. **Read off the contact structure.** Which corner touches which edge, which corner
   touches which wall, which squares share an angle.
   This is a *discrete* hypothesis.
3. **Write and reduce the contact equations.** The raw system contains all centres; a
   good contact graph lets you eliminate them and keep only `s` and the distinct angles.
4. **Close the system.** It is underdetermined until you add the conditions that make
   the solution an extremum — Lagrange or Fritz-John conditions in determinant form.
   The determinant form matters because it keeps the problem *root-finding*, which
   reaches thousands of digits, rather than *minimization*, which does not.
5. **Solve exactly.** Elimination (Gröbner, resultants) or high-precision Newton
   followed by an integer-relation algorithm that recognizes the minimal polynomial.
6. **Certify.** Prove the polynomial irreducible, isolate the intended real root, and
   substitute back exactly.

Step 1 is built. Step 6 is **half built**: irreducibility, root isolation and the exact
separating-axis predicates exist, and they are sufficient for the exact-substitution
route this spec takes; interval-Newton, Krawczyk and the `PoseBox` scalar do not exist,
and they are what a purely numerical enclosure would need.
Phase 4 therefore discharges its candidate by exact substitution, and the certification
bridge is out of scope here — it is agenda-005’s BC-045, not a phase of this spec.
**Steps 2 through 5 are the gap**, and this spec builds them.

Two facts a reviewer should hold onto:

- Every exact entry in this repository today was either derived by hand or supplied by a
  publication. `n = 11` is exact because Trump published the degree-8 minimal polynomial
  in 1979; `cases/trump11/derive_field.py` takes “only the published minimal polynomial”
  and re-derives from it.
  That is step 6 work, not steps 2–5.
- `n = 29`’s best known packing has **no exact form anywhere**. Its evidence record
  carries `replay_status: public-certificate-missing` and the note that the public SVG
  “serializes a FindRoot result and supplies no formal certificate”.

### Two corrections that shaped this design, both from measurement

**Contact inference is not the blocker at `n = 29`.** It was first ranked as the hardest
step, on an ambiguity risk taken from D-021 — the float LP solver’s `1e-11` noise floor.
That floor governs *this project’s quench output*. It does not govern a published source
carrying ~99 digits per coordinate.
Running the existing reconstruction:

| Quantity | Value |
| --- | ---: |
| Pairs tested | 406 |
| Touching pairs | 52 |
| Container contacts | 37 |
| Worst touching margin | `-4.05e-101` |
| Smallest strict separation | `3.617e-02` |

Contact and non-contact are separated by about **ninety-nine orders of magnitude**. The
structure is already computed; the work is to freeze it, not to infer it.

**The serialized digits are not enough, but the closed system is already public.**
Running integer relation directly on the serialized side value returns relations at
almost every degree from 8 to 21 — the signature of an under-determined search.
The degree-8 candidate has a relative residual of order `1e-90` against ~100 available
digits, having consumed almost exactly the 90 it was allowed.
That first probe’s parameters were unrecorded and it is not reproducible as written;
X-004 carries a parameterized replacement that returns no relation at any degree through
16 at 700 digits, which is the contrast the margin rule below encodes.
A genuine minimal polynomial vanishes to full input precision.
**Ninety-eight digits cannot identify the polynomial**, so precision must be
*manufactured from the closed system*.

At `n = 29` that system does not have to be built.
The archived provenance SVG publishes all nine slide scalars and all six equations
`f1 … f6` in `{s, a, b, c, d, i}`, and
[`cases.kingbird29.verify_svg`](../../../../cases/kingbird29/verify_svg.py) already
transcribes every one of them — using them only to evaluate residuals at the serialized
pose, never to solve.
Handing that same transcription to a root finder reproduces the record to all 15
published digits and reaches a residual of `8.85e-421` in about two seconds.

So the phase order still holds — solve needs precision, precision needs refinement,
refinement needs the closed system — but phases 1 and 2 are **not** what unblocks
`n = 29`. They are what makes the route apply to sizes where no system was published.
`n = 29` can be driven from phase 3 onward today, and this spec’s phase order should be
read as building generality, not as clearing a blocker.

## Goals

- Extract and freeze a contact structure, reproducing the known `n = 11` structure.
- Assemble, reduce and close the contact system, reproducing the known `n = 11` form.
- Refine to precision far past the source, with a reported residual bound.
- Recover a minimal polynomial and discharge it through the existing exact machinery.
- Close the round trip, then run the whole chain at `n = 29`.
- Remove the `1e-11` float-LP floor so poses this project generates become promotable.

## Non-Goals

- **Optimality.** Certifying an upper bound leaves the `n = 29` bound gap of about
  `0.46` untouched. A lower bound is separate mathematics.
- **Record improvement.** This certifies an existing construction.
  Searching for a better one is the proposer layer, where H-002, H-016, H-018 and H-020
  are all refuted.
- **Generic inference from arbitrary geometry.** Where near-contacts are genuinely
  ambiguous, the answer is a typed refusal, not a guess.
- **Component identity.** `distinct_basins` counting endpoint keys blocks the atlas, but
  it is independent of this work.

## Design

### Approach

Every new stage is built against machinery that can catch it being wrong.
The existing back end is the oracle:

| Existing API | Use |
| --- | --- |
| `sqpack.field.NumberField` | `.element(coeffs)`, `.rational(v)`, `.alpha()`, `.sign(e)`, `.refine_to(digits)`, `.root_bounds()`, `.decimal(e, digits)`, `.precondition_certificate()` |
| `sqpack.verify.verify_packing(squares, side, sign=exact_sign)` | Returns a `Report`; a proof when `sign` is exact |
| `sqpack.verify.corners_from_poses(x, y, theta)` | Pose to corner polygon |
| `sqpack.witness.load_witness(path)` | `Witness/v1` loading with schema checks |
| `cases.n5.tangent_cones.LinearRow(label, coefficients)` | The existing linear-row shape, reused rather than reinvented |
| `cases.kingbird29.verify_svg` | The `n = 29` reconstruction that already computes contacts |

Third-party: SymPy 1.14 provides `groebner` and `resultant`; mpmath 1.3 provides `pslq`
and arbitrary-precision arithmetic.
Both are already dev dependencies.
“Unbuilt” in this repository means no code here, not no capability.

### Components

New code lives under `src/sqpack/promote/`, a new package, with thin devtools entry
points for the gate.
Each module is independently testable and returns typed refusals rather than raising
bare exceptions.

```
src/sqpack/promote/
  contacts.py   ContactStructure, extract_contacts(...)
  system.py     ContactSystem, assemble(...), close(...)
  refine.py     refine(system, seed, digits) -> RefinedSolution
  solve.py      minimal_polynomial(refined, max_degree) -> Candidate | Refusal
  roundtrip.py  certify(candidate, structure) -> Certificate | Refusal
src/sqpack/exact_lp.py       (phase 5)
devtools/promote_case.py     CLI: one case, one stage, JSON out
```

### Data shapes

Frozen, serializable, and soft-schema’d like every other durable artifact here.
Sketch:

```python
ContactType = Literal["corner-edge", "edge-edge", "corner-corner"]


@dataclass(frozen=True)
class Incidence:
    kind: str  # "pair" | "wall"
    contact: ContactType  # decides the equation's form, so it is not optional
    a: int  # square index
    a_feature: str  # "corner:0".."corner:3" | "edge:0".."edge:3"
    b: int | None  # square index, or None for a wall
    b_feature: str | None  # same vocabulary; None for a wall
    wall: str | None  # "x0" | "x1" | "y0" | "y1"
    margin: str  # exact decimal string of the measured separation


@dataclass(frozen=True)
class ContactStructure:
    n: int
    incidences: tuple[Incidence, ...]
    angle_classes: tuple[tuple[int, ...], ...]  # squares grouped by shared angle
    separation_floor: str  # smallest strict separation, as a decimal string
    ambiguous: tuple[Incidence, ...]  # MUST be empty to proceed
```

`ambiguous` is the load-bearing field.
An incidence is ambiguous when its margin is not separated from the strict floor by a
declared factor. A non-empty `ambiguous` is a refusal, not a warning.

**Why the feature fields are required.** A contact is not fully described by *which two
squares* touch; the equation depends on *which features* meet.
A corner-edge contact contributes one scalar equation and one free slide parameter along
the edge; an edge-edge contact contributes an angle identity plus an overlap-interval
condition, which is a different equation and not a single scalar; a corner-corner
contact is a codimension-two coincidence.
At `n = 29` fifteen of the twenty-nine squares are axis-aligned, so edge-edge contacts
are common rather than exceptional and cannot be folded into the corner-edge case.
Extraction must therefore identify the realising feature pair, and must refuse when the
realising pair is not unique.

```python
@dataclass(frozen=True)
class ContactSystem:
    unknowns: tuple[str, ...]  # surviving symbols, in a declared canonical order
    slides: tuple[str, ...]  # one scalar per corner-edge contact point
    centre_map: tuple[tuple[int, str, str], ...]  # square index -> (x, y) in unknowns
    equations: tuple[str, ...]  # SymPy srepr, one per incidence
    closure: tuple[str, ...]  # determinant conditions added by close()
```

`centre_map` is the elimination: every square’s centre is written as an anchor plus a
chain of rotations, so the unknowns reduce to `s`, the distinct angles, and the slide
scalars. The archived `n = 29` source is a worked instance of exactly this shape — nine
slide scalars `r1..rD`, each a closed-form expression in `{s, a, b, c, d, i}`, and six
closing equations `f1..f6` written as one rotated component of a difference of two
corner positions. `assemble` and `close` should be checked against it directly.

### API changes

No change to `Witness/v1` or the verification API. A promoted certificate enters the
record through the existing witness and evidence contracts, so assurance, method,
precision and novelty are recorded rather than asserted in prose.

## Implementation Plan

### Phase 1: Contact extraction

- [ ] `promote/contacts.py` with `ContactStructure` and
  `extract_contacts(squares, side, *, floor_ratio)`.
- [ ] Classify each of the `n(n-1)/2` pairs and `4n` wall relations by exact or
  high-precision margin; group squares into angle classes.
- [ ] Populate `ambiguous` for any incidence within `floor_ratio` of the strict floor.
- [ ] Extract `n = 29` from the existing reconstruction; assert 52 pair contacts, 37
  wall contacts, 6 angle classes, empty `ambiguous`.
- [ ] Extract `n = 11` from `cases.trump11.packing` and compare against the known
  structure.
- [ ] Retain both as soft-schema artifacts under `atlas/`.
- [ ] Negative control: perturb one margin to straddle the floor and require a refusal.

### Phase 2: System assembly and closure

- [ ] `promote/system.py` with `assemble(structure, unknowns)` producing equations in
  SymPy symbols, and `close(system)` adding Jacobian-determinant conditions.
- [ ] Eliminate centres where the contact graph permits; report which unknowns survive.
- [ ] Reproduce the known `n = 11` system: two unknowns after reduction.
- [ ] Refuse, with the specific incidence named, when the graph does not admit
  elimination.
- [ ] Negative control, two parts.
  Dropping an incidence is **not** a valid control: the raw system is redundant — 89
  incidences plus angle identities against 88 raw unknowns at `n = 29` — so removing one
  equation leaves it exactly as solvable, and a control that cannot fail is not a
  control. Instead:
  1. **Underdetermination.** Withhold `close()` and require the unclosed system to be
     reported as underdetermined, with the count of surviving unknowns and equations
     named. Closure is what makes the counts meet, so this control can genuinely fail.
  2. **Wrong structure.** Replace one true incidence with a nearby false one and require
     either a typed refusal at assembly or a reported non-convergence at phase 3 — never
     a silently returned root.

### Phase 3: High-precision refinement

- [ ] `promote/refine.py` with `refine(system, seed, digits)` using mpmath Newton from
  the serialized pose, returning the solution and a **reported residual bound**.
- [ ] Verify the residual falls with precision as a Newton step should; a residual that
  plateaus indicates a wrong system and must be reported as such.
- [ ] Reach 1000+ digits at `n = 11` and `n = 29`.
- [ ] Negative control: seed far from the root and require non-convergence to be typed,
  not silently returned.

### Phase 4: Exact solve and round trip

- [ ] `promote/solve.py` with two independent routes: elimination via SymPy, and integer
  relation via mpmath `pslq`.
- [ ] **Margin rule**, frozen as a decidable test rather than a caution.
  Let `C` be the largest absolute integer coefficient the relation *actually* carries —
  not the search’s `maxcoeff` bound, which overstates it — and let the manufacturable
  budget be `B = (d + 1) * log10(C)`. A candidate is accepted only when all three hold:
  1. **Budget.** The relative residual is below `10^-(B + M)`, with the margin fixed at
     `M = 200` decimal digits for this project.
  2. **Stability under precision.** Re-evaluated at `2B + 2M` digits, the residual keeps
     falling to the evaluation floor instead of resting at `10^-B`. A spurious relation
     is pinned to the budget that produced it; a genuine one is not.
     This is the cheap decisive test and it is mandatory.
  3. **Independent digits.** The value is supplied by a phase-3 refinement whose
     *reported residual bound* is below `10^-(B + M)`. “Digits available” always means
     that bound — never the number of digits a source happens to print.
     Record `d`, `C`, `B`, `M`, the residual at `B`, and the residual at `2B + 2M`.
     Clause 2 is what the planning probe lacked, and it is why that probe’s degree-8
     “relation” was reported as spurious.
- [ ] `promote/roundtrip.py`: build a `NumberField` from the candidate, prove
  irreducibility, isolate the root, rebuild the packing, and call `verify_packing` with
  `exact_sign`.
- [ ] Compare the reconstructed side against the input pose, not merely validity — a
  wrong contact structure can yield a *valid but suboptimal* packing, which verification
  alone does not catch.
- [ ] Recover Trump’s degree-8 polynomial at `n = 11` and close the loop against
  `cases.trump11.packing`.
- [ ] Run the chain at `n = 29` and record whatever it returns, including a refusal.
- [ ] Negative controls: a plausible wrong polynomial must fail back-substitution; a
  perturbed contact structure must fail the side comparison.

### Phase 5: Exact LP

- [ ] `src/sqpack/exact_lp.py`: LP over certified rational or algebraic coefficients,
  replacing the float solver where a certified answer is required.
- [ ] Agree with the float path on cells where both are valid; the existing float LP and
  its independent second formulation agree to `4.4e-16` on Trump’s cell and are the
  known-answer pair.
- [ ] Report which cells need algebraic rather than rational coefficients.
- [ ] Demonstrate that a pose quenched through the exact path has an empty `ambiguous`
  set, which the float path cannot guarantee.

## Testing Strategy

**`n = 11` is the test harness, not just a case.** Every stage has a published answer
that no implementation here can influence: the extraction against the known contact
structure, the assembly against the known two-unknown system, the solve against Trump’s
degree-8 polynomial, the round trip against `cases.trump11.packing`.

**Every stage that can refuse gets a negative control proving it refuses.** This
repository has 80 such controls and treats a guard without a control as untested — a
control that stopped firing is how a real defect shipped here before.
Each phase above lists its own.

**Two failure modes, discharged differently, one only partly:**

- A wrong minimal polynomial is caught by exact back-substitution: it will not satisfy
  the system.
- A wrong contact structure is caught by re-verifying the reconstruction — but
  verification catches *infeasibility*, not a structure yielding a valid yet suboptimal
  packing. That shows up as a reconstructed side strictly above the input, so the side
  comparison is mandatory and is not redundant with validity.

Gate integration: each phase registers a step in `packing-validate`, and the full tier
runs at every phase boundary rather than only before merge.

## Rollout Plan

Phases land in order behind the existing gate.
Nothing enters `frontier/` from this work without passing the witness and evidence
contracts; a promoted `n = 29` certificate is a deliberate reviewed change, never a
result written straight into the record.

An unattended runner may not write an accepting verdict from this chain.
A round passing its checks is recorded `unresolved` with `needs_review` and waits for a
human. That rule is unchanged and applied to exp-045 already.

## Open Questions

- **What degree is `s(29)`'s minimal polynomial?** Unknown, and it decides whether
  integer relation is viable and at what precision.
  The planning probe bounds only what 98 digits can reach, not the true degree.
- **Does elimination terminate at 6 unknowns?** `n = 11` reduces to 2 and `n = 17` to 3.
  `n = 29` has 6 orientation classes of which one is the axis class, so 5 tilted angles
  plus `s` gives 6 — settled by the source’s own six-by-six solve rather than estimated.
  Gröbner cost is severe in variable count.
  This is why phase 4 builds *two* routes rather than a route and a fallback.
- **Do the 5 tilted angle classes collapse to fewer exact relations**, lowering the
  effective unknown count below 6?
- **Is the exact LP purely rational for the cells that matter**, or does it need
  algebraic coefficients?
  It is rational only for rational-coefficient cells.
- **What `floor_ratio` makes `ambiguous` meaningful?** At `n = 29` the separation is 99
  orders of magnitude and any sane value works.
  On a quenched pose near the `1e-11` floor it is the whole question, and phase 5 may
  change the answer.

## References

- [X-004 — an exact algebraic characterization of the `n = 29` record](../../../../campaign/explorations/X-004-n29-exact-promotion.md)
- [plan-2026-08-28 — the numeric–symbolic round trip](plan-2026-08-28-numeric-symbolic-round-trip.md)
- [plan-2026-08-28 — the symbolic promotion gap](plan-2026-08-28-symbolic-promotion-and-the-atlas.md)
- [agenda-005](../../../../campaign/agendas/agenda-005-symbolic-promotion-and-identity.md)
- [TUTORIAL §5 — from a numeric solution to an exact one](../../../../TUTORIAL.md#from-a-numeric-solution-to-an-exact-one)
- [SYNOPSIS — What Is Built](../../../../SYNOPSIS.md#what-is-built)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
