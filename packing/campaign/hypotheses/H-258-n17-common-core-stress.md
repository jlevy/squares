---
title: "H-258 \u2014 exact common-core n17 first-order stress"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-258
  kind: hypothesis
  claim: The fixed analytic common-core stress at the accepted n17 endpoint has nonnegative weights and
    exact normalized stationarity identities, thereby excluding negative-side first-order directions in
    both complete corner branches.
  lane: proof
  derived_from:
  - X-048
  criterion:
    shape: determination
    metric: Exact52column stress residual identities, complete58commonrow weights and zero corner weight,
      with exact interval guards and nonnegative weights.
    direction: Confirm only if all52 normalized residuals vanish exactly at the H255root, all prescribed
      weights are nonnegative by exact identities or interval lowerbounds at leastzero, every denominator
      and normal-force guard is strictpositive, H257feature completeness is accepted, syntheticcontrols
      pass and independent mathematical/code/output review finds no blocking defect. Failed or unresolved
      bounds test only this fixed common-core stress; they do not refute stationarity or optimality.
    threshold: Exact A-transpose-lambda=e-side identity at the certified root; weight lowerbounds at leastzero
      with no tolerance; strictpositive denominator/force guards.
  instrument: devtools.check_n17_core_stress; deterministic symbolic stress construction, exact rational-function
    residual reduction and fixed256bit outward dyadic interval sign audit using exact Fraction operations.
    No numerical optimizer or fitted parameters.
  instrument_ready: true
  regime: Unchanged H255 inclusion box and accepted H256centroid/H257feature inventory; fixed analytic
    force and torque allocation, no rootrefinement or alternate allocation.
  instance:
    axis: n
    point: 17
  priority: 1
  cost_estimate: One25minute controlled implementation/review slice; one300second singleworker target,10MiB
    per output; independent output review beforeacceptance.
  prereqs:
  - think-wrgx
  - think-6dg0
  replication: false
  registered: '2026-10-01'
  notes: This is first-order stationarity of the complete local model, not local minimality, rigidity,
    nonlinear continuation or global optimality. H027 quantitativeclass-angle threshold remains separate.
---
# H-258: An Exact Common-Core First-Order Stress

This round tests one deterministic dual for the two complete n17 first-order branches.
The accepted [H255 root](H-255-n17-exact-polynomial-root.md),
[H256 endpoint](H-256-n17-exact-endpoint-feasibility.md), and accepted
[H257 feature inventory](H-257-n17-endpoint-contact-features.md) are prerequisites.
H257 output review is accepted before any H258 target arithmetic.
The
[core-stress derivation](../../../docs/project/reviews/review-2026-10-01-n17-core-stress.md)
fixes the complete force, torque and row-order contract.

The
[first-order derivation](../../../docs/project/reviews/review-2026-10-01-n17-first-order-branches.md)
fixes all 52 variables and both 59-row branches.
This candidate assigns zero weight to each branch’s corner row and uses the same 58
common rows for both.
Preserve every row and variable, including structural zero weights and rattler
coordinates.

## Frozen Analytic Allocation

Use the H254 functions $F_1,F_2,G_3$ before eliminating the independent side $S$.
Differentiate with respect to the class angles while holding $S$ fixed, and only then
substitute $S=(6+4t)/(1+2t-t^2)$. Set

$$
\nu=(G_3)_\beta,\qquad \rho=-(F_2)_\beta,\qquad
\mu=-\frac{\nu(F_2)_\theta+\rho(G_3)_\theta}{(F_1)_\theta},
$$

$$
Z=\nu+\alpha\rho,\qquad L=\nu d/c,\qquad R=Ze/s.
$$

The contact-force and wall-force roster, axis torque allocation and five oblique-tree
moment formulas are fixed by the independently reviewed core-stress derivation before
instrument freeze. There is no numerical LP, coefficient fitting or alternative stress
search in this round.
For the five oblique tree edges use the prescribed baseline angular residuals $b_i$:

$$
q_{9,10}=-b_9,\quad q_{10,12}=-b_9-b_{10},\quad q_{11,12}=-b_{11},
\quad q_{13,14}=-b_{13},\quad q_{12,14}=b_{13}+b_{14}.
$$

A face with normal force $f$, offset $\tau$ and moment $q$ splits into the two reduced
row weights $E_-\mapsto(f+q/k)/2$ and $E_+\mapsto(f-q/k)/2$, with $k=(1-|\tau|)/2$.
Prove the sign branches used to simplify $|\tau|$; do not infer them from decimal
display. Axis-wall torque $m$ splits into $W_-\mapsto f/2-m$ and $W_+\mapsto f/2+m$. The
linked derivation fixes the complete row and variable order.
Normalize every weight by

$$
K=(c+s)\mu+\gamma\nu/c+\gamma Z/s+\gamma\rho(d+e)>0.
$$

Require every prescribed weight to be nonnegative.
The five oblique moment capacities $kf\pm q$ are explicit obligations.
An interval containing negative values and zero does not certify nonnegativity.
A structurally zero weight needs an exact identity.

For the stationarity equation $A^{\mathsf T}\lambda=e_\sigma$, prove 50 residuals
identically zero and reduce the remaining two to the prescribed opposite multiples at
$\omega_{12}$ equal to $+\rho\gamma F_2/K$ and at $\omega_{16}$ equal to
$-\rho\gamma F_2/K$, then use the accepted root identity $F_2=0$. An interval merely
containing zero is insufficient: the cone variables are unbounded.
Independently review every normalization and sign direction.

## Controls, Bounds and Disposition

Before the target, test parallel owner derivatives against the reduced rows for both
signs of relative angular velocity, including nonzero offsets and the corner limit;
check a rotating owner at a nonparallel contact; mutate a force, moment, residual sign,
normalization, row or required input.
Synthetic controls must not read the target.
Retain exact symbolic equalities and independently audit all interval conclusions.

For a future admitted implementation, the interval contract uses a fixed 256-bit dyadic
grid. Enclose each input and every arithmetic result by rounding its lower endpoint down
and upper endpoint up to multiples of $2^{-256}$, using exact integer floor and ceiling
operations. Division requires a denominator interval excluding zero.
This widens the unchanged accepted root enclosure; it does not refine the root or change
any sign threshold. Synthetic controls must check containment, including negative values
and division. The independent auditor implements the enclosure operations separately and
reports any differences between its bounds and the producer’s bounds; both must
establish the required signs.

This proposed arithmetic contract was selected before any H258 target evaluation; it has
not been implemented or validated.
An unrelated synthetic 58-weight assembly at $(t,b)=(1/3,1/5)\pm10^{-12}$ took 0.049
seconds but produced 128,454 characters for weight bounds alone with unrestricted
rational denominators.
Fixed outward rounding bounds representation cost without weakening the exact
containment requirement.
The separate symbolic identity calculation continues to use exact rational functions,
with no numerical tolerance.

Freeze the criterion, analytic recipe, instrument, controls and prerequisite Git blobs
before one target run.
Use existing dependencies, project Python, one worker, a 300-second process limit and 10
MiB per output; record an optional 1 GiB data-segment limit if supported.
Retain preparation, symbolic proof, interval checking and output costs separately where
measured. No automatic retry, root refinement or changed torque allocation is allowed
after observing output.

Acceptance proves nonnegative side velocity throughout the complete first-order model,
conditional on its accepted feature premises.
A certified strictly negative weight or moment-capacity interval rejects this fixed
allocation only. An interval straddling zero or a time limit leaves its sign unresolved.
A defective identity or invalid instrument requires repair and a separately registered
run, not an inference about feasible packing motions.
Other stresses may still work.
Even success leaves zero-side motions, higher-order local analysis and global
capture/exclusion as separate obligations.
It does not meet H027’s stronger quantitative class-angle criterion by substitution.

## Instrument Stop Before Target Use

Three synthetic symbolic preparation attempts did not finish: the fully substituted
calculation was interrupted after about two minutes; the formal-load and block-cancelled
versions each reached a 90-second ceiling.
The overnight three-failure guard stopped this instrument.
No target stress was evaluated, so the candidate is neither confirmed nor refuted.

The
[preparation record](../explorations/X048-stress-preparation/preparation-2026-10-01.json)
and [observed output](../explorations/X048-stress-preparation/observed-tool-output.txt)
retain the commands, exits, controls, missing measurements and source-snapshot limits.
Both draft command-line tools refuse before reading target files.
The producer has three passing fast synthetic controls; full identity completion,
derivative and mutation controls, outward dyadic arithmetic, and independent receipt
binding remain unfinished.
A future attempt requires a new readiness review and a separately admitted run.

## Repaired Instrument and Accepted Run

*Added 2026-10-02 by Session 167.* The Session 166 route review traced the stop to
`sympy.cancel` expression swell, not to the mathematics.
Lane A1 of BC-406 rebuilt the identity proof at `2fbf8d29`. Each value is now a
numerator polynomial over registered monic irreducible denominator factors, and the
outward audit gains a strict-sign guard on every factor.
The identities checked and the criterion above are unchanged.
The controls the stop section lists as unfinished are now complete: derivative and
mutation controls, outward dyadic arithmetic and receipt binding.
The
[independent output review](../series/series-000-smoke-and-calibration/results/exp-242-n17-core-stress/output-review.md)
is the readiness and output review this section asked for.
[exp-242](../series/series-000-smoke-and-calibration/experiments/exp-242-h258-n17-core-stress.md)
records the accepted outcome, together with a clean replay from the committed
instrument.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
