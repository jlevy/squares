# Registered Questions and Acceptance Boundaries

The original claim metadata is retained as fenced YAML, including complete quantifiers, controls and accept rules. These registrations document the research; the reviewer may propose a different strategy. Instrument readiness is scoped in each record and never means that its target hypothesis has been proved.

<a id="source-1"></a>

## Source 1: `packing/campaign/hypotheses/H-036-robust-restricted-orientation.md`

Snapshot `4d305597a505`, source lines 1-end.

```yaml
title: H-036 — Stromquist's restricted-orientation gap survives a neighborhood
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-036
  kind: hypothesis
  claim: >-
    If every n = 11 square orientation modulo quarter turns lies within 0.25 degrees of
    either 0 or 45 degrees, then the containing side is at least 3.878.
  lane: proof
  derived_from: [X-002]
  strategy_refs: ['proof:9', 'proof:10', 'proof:15']
  criterion:
    shape: determination
    metric: certified lower bound over the declared restricted-orientation configuration space
    direction: at least 3.878
    threshold: 3.878
  instrument: >-
    First reproduce Stromquist's exact 0/45-degree lower bound. Then run interval branch
    and bound over centers and the two angle neighborhoods, using unavoidable-set and
    containment cuts, while an independent search tries to falsify the 3.878 threshold.
  instrument_ready: false
  regime: n = 11; every folded angle within 0.25 degrees of 0 or 45 degrees
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: tier S numerical falsifier; certified proof is an hour-to-day ladder
  prereqs: [checked Stromquist restricted-orientation control, interval PoseBox]
  replication: true
  registered: '2026-08-24'
  notes: >-
    Stromquist proves the exact 0/45-degree optimum is about 3.8856. This claim asks for
    a much weaker but robust neighborhood statement above Trump's side. A valid packing
    below 3.878 refutes it immediately.
```

<a id="source-1-h-036--a-structural-theorem-between-one-slice-and-the-full-problem"></a>

### H-036 — a structural theorem between one slice and the full problem

The threshold and angle radius are fixed before computation.
If refuted, retain the pose and shrink the radius only in a newly registered claim
rather than moving the goal.

<a id="source-2"></a>

## Source 2: `packing/campaign/hypotheses/H-093-n11-scalar-61-16-certificate.md`

Snapshot `4d305597a505`, source lines 1-end.

```yaml
title: H-093 — the scalar certificate language reaches 61/16 for n = 11
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-093
  kind: hypothesis
  claim: >-
    At container side 61/16, the retained 181-direction net and scalar core side
    B = 9977/10000 admit a finite D4-invariant measure of nonnegative rational
    point atoms with total mass strictly below eleven and mass at least one in
    every admissible core. Such a certificate proves s(11) >= 61/16.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:21', 'proof:22']
  criterion:
    shape: determination
    metric: exact scalar certificate at side 61/16
    direction: >-
      Accept only after the rationalized certificate passes the production sweep
      and interval decisions and the standalone verifier, including complete
      coverage and total mass below eleven. Reject only upon an exact
      verify_ceiling family at this side, core side and net with maximum
      pointwise depth at most one and total weight at least eleven.
    threshold: exact certificate at side 61/16 with total mass strictly below eleven
  instrument: >-
    The existing frozen scalar 61/16 recipe using packing/devtools/run_fractional_cutting.py,
    its seed certificate, packing/devtools/freeze_cutting_primal.py, and the existing
    declaration, production decision and standalone verification commands.
  instrument_ready: true
  regime: >-
    n = 11; side 61/16; B = 9977/10000; the retained rational 181-direction net;
    exact rational certificate decisions and the unchanged scalar recipe.
  instance: {axis: side, point: '61/16'}
  prereqs: [BC-250 publication, frozen scalar recipe and fresh output paths]
  registered: '2026-09-06'
```

<a id="source-2-h-093--a-scalar-certificate-at-6116"></a>

### H-093 — A Scalar Certificate at 61/16

Session 089 restored instrument readiness after integrating PR100’s exact depth fixes
and PR98’s validation improvements.
The focused depth, seed, driver and bridge controls and a zero-iteration retained-seed
control passed in an isolated checkout of `5267bd34`. The
[readiness audit (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-251-readiness-audit.md#landed-code-replay)
retains the commands and limits.
No H-093 experiment has started; its prospective freeze, fresh target paths and full
single-invocation allocation remain separate requirements.

The [scalar probe in Agenda 025](04-child-agendas.md#source-1)
tests the first selected side between the retained 3.81 certificate and the unfinished
3.82 bracket. The
[continuation addendum (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/docs/project/handoff-2026-09-06-post-381-t2-t10-continuation.md)
owns its literal command, seed mapping and cooperative process deadline.

A row-converged objective below eleven starts the existing rationalization and
verification sequence; it does not establish the bound itself.
A timeout, missing convergence or finite-site optimum above eleven leaves this existence
claim unresolved. An exact ceiling closes only the declared scalar formulation.

Stop variant search when a candidate requires BC-238 review.
Exact basis recovery may support that candidate if rounding consumes its margin.
A different side, net or core mechanism requires a prospective claim; H-064’s 3.85
ceiling and H-090–092’s fixed-weight probes retain their original scopes.

<a id="source-3"></a>

## Source 3: `packing/campaign/hypotheses/H-094-n11-weight-and-site-redesign.md`

Snapshot `4d305597a505`, source lines 1-end.

```yaml
title: H-094 — reweighting and support changes beyond the fixed-atom obstruction
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-094
  kind: open_question
  claim: >-
    Which changes to relative atom weights and D4 site orbits overcome the retained
    fixed-weight coverage obstruction and permit a stronger n = 11 certificate?
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:21', 'proof:22']
  instrument_ready: false
  regime: >-
    Nonnegative rational atomic measures; the target side, net, witness geometry,
    site set and row-generation rule must be fixed for each proposed test.
  instance: {axis: n, point: 11}
  registered: '2026-09-06'
```

<a id="source-3-h-094--change-weights-and-sites"></a>

### H-094 — Change Weights and Sites

The
[contributed strategy, A3–A4](06-alternative-strategies.md#source-1)
proposes support seeding followed by unrestricted pricing.
The
[fixed-weight obstruction](10-fractional-barriers-and-negatives.md#source-5)
leaves changed relative weights and sites open.
H-070’s rejected inset/release comparison covers its particular seed rule.

The first proposed discriminator is a finite rational covering LP on retained D4 site
orbits and exact bad-pose rows, transported to a selected target with their geometry
checked.
An exact dual floor of eleven rules out a mass-below-eleven certificate on those
sites at that target.
A smaller finite-row objective requires global separation before it can support a bound.

If that screen justifies new sites, use active witness boundaries or intersections to
propose orbit additions or splits, then compare the released search with an unrelated
seed. Refining support at several scales remains the same atomic proof language.
Moving sites without changing incidence cannot improve the fixed incidence LP.

Register each measurable successor with its rows or row-generation rule frozen before
its comparison. Retain a fixed-site obstruction at its stated scope; reopen that family
only when its sites, target or witness geometry changes.
Stop a seed variant that fails its declared matched comparison, without concluding that
every support prior fails.

<a id="source-4"></a>

## Source 4: `packing/campaign/hypotheses/H-095-n11-adaptive-core-certificate.md`

Snapshot `4d305597a505`, source lines 1-end.

```yaml
title: H-095 — adaptive cores certify side 61/16 for n = 11
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-095
  kind: hypothesis
  claim: >-
    At container side 61/16, the BC-230 adaptive-core language admits a finite
    D4-invariant measure of nonnegative rational point atoms with total mass below
    eleven, nonconstant rational core sides B_k, and mass at least one in every
    admissible core at every declared net direction.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:21', 'proof:22']
  criterion:
    shape: determination
    metric: exact adaptive-core certificate at side 61/16
    direction: >-
      Accept only if the project sweep, interval route and source-distinct
      standalone verifier all accept the same certificate under BC-230's
      legacy-linear-v1 contract, with complete angle-cell coverage, safe
      containment, D4 invariance, nonconstant core sides and total mass below
      eleven. Incomplete verification or a failed search leaves the claim unresolved.
    threshold: exact adaptive certificate at side 61/16 with total mass below eleven
  instrument: >-
    BC-231's planned adaptive project sweep, interval route and standalone verifier,
    followed by BC-234 synthesis and BC-238 independent candidate review.
  instrument_ready: false
  regime: >-
    n = 11; side 61/16; exact rational atoms, weights and BC-230 angle-cell data;
    legacy-linear-v1 containment. The synthesis rule is frozen before measurement.
  instance: {axis: side, point: '61/16'}
  prereqs: [reviewed BC-230 contract, all BC-231 routes and controls accepted]
  registered: '2026-09-06'
```

<a id="source-4-h-095--adaptive-cores-at-6116"></a>

### H-095 — Adaptive Cores at 61/16

The
[BC-230 contract](04-child-agendas.md#source-5)
proves the containment and counting implication.
The
[contributed strategy, B1](06-alternative-strategies.md#source-1)
motivates using each angle cell’s mismatch instead of one global shrink.
BC-231 implementation and controls remain prerequisites for a target run.

BC-234’s 25-percent reduction of same-support excess is a routing test, not acceptance
of this certificate-existence claim.
A matched comparison needs its own frozen scalar control, support and synthesis rule.
A successful adaptive certificate alone does not establish an advantage over H-093.

Stop variant synthesis when a candidate requires independent verification.
If H-093 already certifies this side, reassess the value of running this target before
spending more work; retain H-095’s side and criterion unchanged.
Exact basis recovery may support a candidate, while a new side or containment contract
requires a separate prospective claim.

<a id="source-5"></a>

## Source 5: `packing/campaign/hypotheses/H-096-n11-angle-cell-kernels.md`

Snapshot `4d305597a505`, source lines 1-end.

```yaml
title: H-096 — rational angle-cell kernels beyond square cores
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-096
  kind: open_question
  claim: >-
    Can finite rational inner kernels, contained throughout their assigned angle
    cells, improve verified atomic coverage enough to extend the n = 11 bound
    beyond the adaptive-square-core route?
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:21', 'proof:22']
  instrument_ready: false
  regime: >-
    Rational polygonal inner witnesses, nonnegative atomic mass, complete closed
    angle cells and D4 accounting; exact containment and translation coverage.
  instance: {axis: n, point: 11}
  prereqs: [BC-235 representation and containment proof before BC-236 implementation]
  registered: '2026-09-06'
```

<a id="source-5-h-096--rational-angle-cell-kernels"></a>

### H-096 — Rational Angle-Cell Kernels

The
[contributed strategy, B2](06-alternative-strategies.md#source-1)
proposes a rational polygon inside the common intersection of unit squares across an
angle cell. That intersection need not itself have a polygonal boundary.
[BC-235 and BC-236](04-child-agendas.md#source-1) own the
theory and verifier work.

The first proposed discriminator fixes one limiting pose and angle cell from an adaptive
result, constructs a rational inner polygon, and proves containment for every angle in
the cell. Check whether the added region captures positive mass that the square core
misses. Extra area without useful captured mass does not justify a build.

That local calculation cannot establish universal translation coverage.
A global candidate needs a complete center-cell decision procedure, independent
verification and strict interior containment before disjoint mass can be counted.

Keep the declared adaptive-disposition prerequisite before implementation.
Price a verifier only after a useful containment and coverage comparison; retain
BC-236’s existing four-times square-core decision-cost guard.
A failed polygon or local test disposes that proposal, without ruling out every kernel.

<a id="source-6"></a>

## Source 6: `packing/campaign/hypotheses/H-097-n11-existential-witness-menus.md`

Snapshot `4d305597a505`, source lines 1-end.

```yaml
title: H-097 — existential witness menus for n = 11
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-097
  kind: open_question
  claim: >-
    Can a finite witness menu certify that every admissible unit-square pose
    contains at least one strictly interior witness of sufficient mass where
    universal coverage by a single core family fails?
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:7', 'proof:21', 'proof:22']
  instrument_ready: false
  regime: >-
    One nonnegative measure and a finite menu of witnesses; a complete
    for-every-pose, there-exists-a-witness containment and mass statement.
  instance: {axis: n, point: 11}
  prereqs: [identified universal-witness restriction and a specified pose domain]
  registered: '2026-09-06'
```

<a id="source-6-h-097--choose-a-witness-within-each-square"></a>

### H-097 — Choose a Witness Within Each Square

The
[contributed strategy, B5](06-alternative-strategies.md#source-1)
allows witness options to differ in offset, orientation or shape.
The counting proof requires at least one heavy witness strictly inside each packed
square; it need not require every menu member to be heavy.

The first proposed discriminator fixes a closed pose box containing a difficult pose, a
measure and a finite menu.
Prove that every pose in the box admits a contained menu member with mass at least one.
The selected member may vary across the box, so the proof must cover the selection
boundaries as well as the interiors.

A result on that box proves only the stated local selection property.
A global certificate requires a complete pose-domain cover and total measure below
eleven. Sampling poses does not establish the quantified statement.

Nested concentric sizes add no choice when the largest member is admissible throughout
the box. Translation also cannot enlarge the maximum inscribed square at a fixed
orientation; any benefit must come from capturing mass.
Stop an unproved containment or selection proposal before building a global verifier.
Register a measurable successor only after its box, menu and measure are fixed.

<a id="source-7"></a>

## Source 7: `packing/campaign/hypotheses/H-098-n11-segment-measures.md`

Snapshot `4d305597a505`, source lines 1-end.

```yaml
title: H-098 — segment-supported measures for n = 11
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-098
  kind: open_question
  claim: >-
    Can nonnegative segment-supported measures give stronger or cheaper n = 11
    lower-bound certificates than atomic measures while admitting exact
    intersection-length and continuum-coverage verification?
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:8', 'proof:12', 'proof:22']
  instrument_ready: false
  regime: >-
    Nonnegative measures on finitely many line segments, counted through witnesses
    strictly inside the original unit squares; exact intersection mass.
  instance: {axis: n, point: 11}
  prereqs: [kernel-route disposition and a costed BC-237 verifier design]
  registered: '2026-09-06'
```

<a id="source-7-h-098--segment-supported-measures"></a>

### H-098 — Segment-Supported Measures

The
[contributed strategy, B3](06-alternative-strategies.md#source-1)
proposes replacing dense rows of atoms with measure on line segments.
[BC-237](04-child-agendas.md#source-1) owns the deferred theory
and cost assessment.
Strictly interior witnesses keep the selected sets disjoint, including any segment mass
that an original square boundary could otherwise share.

The first proposed discriminator chooses one segment and a declared witness family,
derives its intersection-length formula and all changes of regime, and checks that
formula on exact contained, disjoint and boundary cases.
Identify which persistent atom support it would replace before pricing a complete
summed-mass minimizer.

A binary segment-hit predicate cannot measure captured mass.
The complete decision needs every intersection regime and the minimum of the summed
piecewise formulas over admissible poses.
A representation of one segment supplies neither that verifier nor a new bound.

Keep implementation deferred until the kernel route is disposed and the complete
verifier has a measured future allocation.
A later comparison must freeze the measure family and its exact decision rule.
A costly or unhelpful segment design is a reason to park that design; it does not
exclude every singular measure.

<a id="source-8"></a>

## Source 8: `packing/campaign/hypotheses/H-099-trump-d4-finite-support-dual.md`

Snapshot `4d305597a505`, source lines 1-end.

```yaml
title: H-099 — Trump's D4 placement support admits dual mass above eleven
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-099
  kind: hypothesis
  claim: >-
    At the exact Trump side U, the deduplicated D4 images of the eleven exact Trump
    squares admit nonnegative rational placement weights with total mass D > 11 and
    overlap depth at most one Lebesgue-almost everywhere in the container.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:11', 'proof:17', 'proof:22']
  criterion:
    shape: determination
    metric: verified dual mass above eleven or an exact ceiling for the specified support
    direction: >-
      Accept with D > 11 only after exact containment, complete a.e.-depth verification,
      and independent BC-243 soundness controls pass. Reject this support claim with
      an exact finite necessary-row LP upper certificate at most 11. A sampled
      objective above 11, an invalid candidate, or an incomplete run is inconclusive.
    threshold: 11
  instrument: >-
    Proposed exact geometric support deduplication, necessary-row LP ceiling certificate,
    and, only for a surviving candidate, BC-243's complete a.e.-depth arrangement
    verifier with independent replay. The exact ceiling route passed its source and
    independent readiness controls; this does not authorize acceptance
    of a D > 11 candidate without the complete depth verifier.
  instrument_ready: true
  regime: >-
    n = 11; exact algebraic Trump side; only the geometric D4 closure of the retained
    Trump witness, with no added placements or assumed strong duality
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: price the finite-row ceiling screen before funding a full BC-243 verifier
  prereqs: [reviewed BC-242 semantics, frozen exact support and row-generation rule]
  replication: true
  registered: '2026-09-06'
  notes: >-
    Freeze initial test rows, their deterministic extension rule, and the run bound
    before execution. Exact LP or cutting-plane search is a candidate method, not the
    accept rule. Extending the geometric support requires a separately registered claim.
    The uniform average of eight D4 copies of the complete Trump packing has D = 11;
    reproducing this control is not evidence for D > 11.
```

<a id="source-8-h-099--a-finite-support-ceiling-before-the-arrangement-build"></a>

### H-099 — A Finite-Support Ceiling Before the Arrangement Build

Session 089 accepted readiness for the finite-row ceiling route after the
[independent review (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-254-target-readiness-independent-review.md)
and its parser correction.
Complete almost-everywhere depth verification is not implemented here.

[Exp-113](11-density-contract-candidate-and-results.md#source-2)
tested the prospectively frozen support and returned a separately replayed finite-row
ceiling of $56/5$. Together with the feasible mass-eleven average, it gives the bracket
$[11,56/5]$ for the full fixed-support supremum.
H-099 remains unresolved: the matching finite-row primal weights have not passed
complete almost-everywhere depth verification, so the screen does not certify an
a.e.-feasible mass-above-eleven weighting.

Let $F$ be the distinct geometric squares in all eight container symmetries of the
[exact Trump witness](09-trump-construction-and-local-proof.md#source-1), identifying local quarter-turn
reparameterizations and duplicate placements.
For each D4 orbit $O$, let $a_O$ be the weight of each distinct member, giving
$D=\sum_O |O|a_O$. Symmetrization preserves full feasibility and $D$, so orbit weights
lose no full-support solutions.
A test-row coefficient counts the distinct members of $O$ whose interiors contain the
test point; it is not merely zero or one.

Every necessary test point must be off all square boundaries, with a certified
positive-area neighborhood of constant incidence.
These rows relax full a.e. feasibility: an exact LP ceiling at most eleven rejects the
support; a larger optimum still needs every positive-area arrangement face checked.

[BC-242](11-density-contract-candidate-and-results.md#source-1)
supplies the weak-duality semantics.
[Agenda 026](04-child-agendas.md#source-3) routes the
screen through `think-01q4` and any justified BC-243 certification through `think-mt6q`.
A verified $D>11$ rules out mass-eleven area density at $U$, not below-$U$ density.
This is the finite discriminator for
[X-016’s closure route (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/explorations/X-016-after-381-two-managers-one-proof-boundary.md#closure-route).

<a id="source-9"></a>

## Source 9: `packing/campaign/hypotheses/H-100-below-trump-area-density.md`

Snapshot `4d305597a505`, source lines 1-end.

```yaml
title: H-100 — can full-size area density improve the lower bound below Trump?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-100
  kind: open_question
  claim: >-
    Is there a side L strictly between the retained verified lower bound and the exact
    Trump side, and a nonnegative integrable area density on its container, whose total
    mass is below 11 while every contained full unit-square placement has integral at
    least one?
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:12', 'proof:15', 'proof:17', 'proof:22']
  instrument: >-
    No runnable instrument yet. A concrete successor must freeze its target L, density
    family, exact mass representation, and continuum coverage verifier before
    measurements; BC-257 owns target selection and the decision to commission a
    separately tracked below-Trump primal certificate build.
  instrument_ready: false
  regime: >-
    n = 11; full-size unit squares at all admissible centers and angles, including wall
    strata; nonnegative absolutely continuous measure, not atoms or segment mass
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: price one specified side and density family before a continuum build
  prereqs: [reviewed BC-242 semantics, prospectively specified target and density family]
  replication: true
  registered: '2026-09-06'
  notes: >-
    A finite-pose fit or sampled minimum supplies a candidate, not a certified upper
    bound on covering mass. A strict mass-below-11 certificate excludes eleven squares
    at its stated L only. H-099 finding a feasible dual above 11 at Trump's side does
    not refute this below-Trump question; a non-kill there does not justify a build here.
```

<a id="source-9-h-100--a-below-trump-primal-route-with-its-own-gate"></a>

### H-100 — A Below-Trump Primal Route with Its Own Gate

The
[BC-242 contract](11-density-contract-candidate-and-results.md#source-1)
proves why an area density with mass below eleven excludes a packing of eleven
interior-disjoint squares.
Its boundary convention works because shared square edges have area measure zero.
The remaining mathematical obligation is coverage of the entire continuous placement
space, with exact mass and rigorous lower coverage bounds for every pose box and wall
stratum.

Inverse design in a finite density basis is one possible candidate method.
Its basis, side, and verifier must become a concrete prospective hypothesis before a
measurement; this open question is not an executable queue item.
Failed fits or a failed density family do not exclude all absolutely continuous
densities.

This below-side arm is distinct from [H-101](15-registered-mathematical-questions.md#source-10), which
asks about mass eleven at Trump’s exact side.
[Agenda 026’s BC-257](04-child-agendas.md#source-3)
prices this route separately from BC-244’s equality design.
The below-side mathematical question has no dependency on a non-killing H-099 result.
The common origin is
[X-016’s density route (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/explorations/X-016-after-381-two-managers-one-proof-boundary.md#closure-route).

<a id="source-10"></a>

## Source 10: `packing/campaign/hypotheses/H-101-trump-equality-density.md`

Snapshot `4d305597a505`, source lines 1-end.

```yaml
title: H-101 — does a Trump-side equality density force the complete packing?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-101
  kind: open_question
  claim: >-
    Does the exact Trump-side container admit a nonnegative integrable area density of
    mass exactly 11 covering every full unit-square placement by at least one; if so,
    can its complete compatible eleven-placement equality set be proved to consist
    only of Trump configurations modulo container D4 and square relabelling?
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:11', 'proof:12', 'proof:15', 'proof:17', 'proof:22']
  instrument: >-
    No continuum primal instrument exists. A separately commissioned BC-244 successor
    must fix an exact density family, prove coverage on all pose and wall strata,
    certify mass exactly 11, and classify all compatible equality placements.
  instrument_ready: false
  regime: >-
    exact Trump side; absolutely continuous nonnegative density; complete full-size
    placement space and compatible eleven-tuples, not just retained contact branches
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: separately price a concrete equality candidate before any continuum build
  prereqs: [reviewed BC-242 semantics, prospective density and equality-classification specification]
  replication: true
  registered: '2026-09-06'
  notes: >-
    A verified H-099 dual mass above 11 refutes density existence at this side by weak
    duality. A finite-support ceiling of 11 proves neither existence nor equality
    classification. Uniform D4 packing averages already give dual mass 11 as a control.
    No strong-duality theorem, primal attainment, or complementarity is assumed.
```

<a id="source-10-h-101--equality-requires-a-density-and-a-complete-equality-set"></a>

### H-101 — Equality Requires a Density and a Complete Equality Set

[BC-242](11-density-contract-candidate-and-results.md#source-1-conditional-equality-consequences)
derives saturation conditions conditionally on matched explicit primal and dual
certificates.
An actual mass-eleven density and the exact Trump packing suffice for those
conditions; an optimizer-existence conjecture does not.
Coverage equal to one on Trump’s eleven squares alone is only a necessary finite test.

A possible inverse-design method imposes these finite coverage equalities in a
D4-symmetric density basis, followed by the full continuum check.
Any stationarity conditions require justified differentiability and the correct
constrained wall-normal terms; ambient zero-gradient equations are not automatic.
After coverage, all compatible eleven-tuples of equality placements still need a
complete classification before an optimality or uniqueness theorem follows.

[Agenda 026’s BC-244](04-child-agendas.md#source-3)
owns this separately priced equality arm; a non-killing BC-243 result is not funding.
[H-100](15-registered-mathematical-questions.md#source-9) keeps below-Trump certificates separate.
Both descend from
[X-016 (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/explorations/X-016-after-381-two-managers-one-proof-boundary.md#closure-route).

<a id="source-11"></a>

## Source 11: `packing/campaign/hypotheses/H-102-complete-restricted-angle-support-families.md`

Snapshot `4d305597a505`, source lines 1-end.

```yaml
title: H-102 — which complete restricted angle and support families admit exclusion?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-102
  kind: open_question
  claim: >-
    Which explicitly delimited n = 11 angle-composition or wall-support families admit
    a complete exclusion theorem below a declared side, and which such families admit
    a verified counterexample instead?
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:9', 'proof:10', 'proof:15']
  instrument: >-
    Select a finite family and side before a run. Use complete disjunctive containment
    and separation cases, exact fixed-angle center LP/Farkas certificates or rigorous
    interval bounds over angle boxes, with an independent feasible-witness falsifier.
    No general complete-family producer and verifier exists.
  instrument_ready: false
  regime: >-
    n = 11; only the angle and support family stated in the concrete hypothesis;
    every covered center, angle, wall, and degeneracy case retains its original scope
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: first reuse H-036's bounded falsifier and price one complete proof family
  prereqs: [prospectively fixed family and threshold, checked feasible control for the chosen branch]
  replication: true
  registered: '2026-09-06'
  notes: >-
    H-036 already supplies the first concrete proof target and independent falsifier:
    every folded angle within 0.25 degrees of 0 or 45 implies side at least 3.878.
    Keep that claim and its threshold unchanged. A new family or radius needs its own
    prospective claim. Partial case closure and solver timeout leave a family unresolved.
```

<a id="source-11-h-102--a-restricted-theorem-before-a-global-enumeration"></a>

### H-102 — A Restricted Theorem Before a Global Enumeration

Use [H-036](15-registered-mathematical-questions.md#source-1) for the first theorem attempt and
the adversarial packing search.
A rigorously feasible witness within its angle regime and below 3.878 refutes that
claim; an unsuccessful search is not proof.
No additional hypothesis is needed merely to run its independent falsifier.

A fixed-angle LP closes only its declared separation branch.
Angle intervals require bounds valid throughout each box, and a family theorem requires
every disjunction, boundary, and degeneracy case covered.
A wall-support signature must identify the square, supporting feature, wall, and any
angle or order restrictions; an incomplete signature catalogue remains a restricted
result.
[H-063’s refuted two-threshold language (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/hypotheses/H-063-n11-class-certificate.md) does not
refute richer families, but cannot be revived by renaming it.

[Agenda 026](04-child-agendas.md#source-3) routes
these structural precursors through think-dene and the paired falsifier through
think-pjk7. BC-246/247 can supply reusable controls and branch prices; a self-contained
restricted lemma need not await a full typed producer, density construction, or global
atlas. This implements
[X-016’s distinction between proof layers](05-current-assessment-and-review.md#source-3-proof-layers-and-fractional-objects).

<a id="source-12"></a>

## Source 12: `packing/campaign/hypotheses/H-103-complete-typed-global-capture.md`

Snapshot `4d305597a505`, source lines 1-end.

```yaml
title: H-103 — can complete typed coverage reduce every minimizer to Trump?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-103
  kind: open_question
  claim: >-
    Can a complete typed finite cover of every n = 11 side-minimizing configuration
    between the retained lower bound and Trump's exact side be rigorously excluded or
    mapped wholly into the retained strict Trump isolation neighborhood, modulo D4 and
    square relabelling?
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:10', 'proof:11', 'proof:15', 'proof:17', 'proof:22', 'proof:27']
  instrument: >-
    BC-245's compactness and typed Fritz-John branch contract, independently replayed
    BC-246 endpoint and BC-247 completeness/pricing controls, then a separately priced
    complete cover using sound branch-specific exclusions and local capture.
    The general producer and complete-cover verifier are not ready.
  instrument_ready: false
  regime: >-
    all side minimizers in the declared interval; ordinary and abnormal Fritz-John
    branches, ties, zero multipliers, rattlers, and every feasibility inequality retained
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: price one nontrivial complete branch before any global enumeration
  prereqs: [reviewed BC-245 contract, exact local endpoint and complete branch-specific controls]
  replication: true
  registered: '2026-09-06'
  notes: >-
    Typed SAT/LP/interval exclusion, geometric conflicts, clique or Hall constraints,
    and conditional covering certificates are possible methods, not evidence of
    completeness. A valid covering measure M and epsilon = M - 11 are prerequisites
    only for mass-forcing or near-tight deductions that use them, not every geometric
    incompatibility or independently justified conditional certificate.
```

<a id="source-12-h-103--complete-global-capture-with-restricted-precursors-kept-separate"></a>

### H-103 — Complete Global Capture, with Restricted Precursors Kept Separate

[BC-245](13-typed-global-structure.md#source-1)
reduces the target to typed minimizers without assuming constraint qualification.
A finite branch language does not prove that enumeration is affordable or complete.
The [H-032 controls (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/hypotheses/H-032-small-n-optimal-moduli.md) cover all n = 3 and n = 4 optimum
strata; a known n = 5 packing is only a positive local control.

Every conditional certificate must name the configuration domain it excludes.
Clique, odd-cycle, Hall, and hyperedge cuts need a sound integral assignment model;
heavy-atom and near-tight forcing additionally need the actual valid covering measure.
[H-102](15-registered-mathematical-questions.md#source-11) permits independently
useful restricted theorems without asserting this global cover.

The retained BC-240/241 endpoint is accepted only at its local,
retained-record-dependent scope.
A capture leaf must put its whole surviving box strictly inside that radius after an
exact symmetry and label map; the remaining leaves must cover the whole complement.
[Agenda 026’s BC-248](04-child-agendas.md#source-3)
keeps its existing valid-measure, at-most-2,311,290-of-23,112,904 survivor, and
below-four-CPU-hour pricing guards, plus BC-246/247 prerequisites.
These guards apply to that global residue, not all structural precursor lemmas.
The distinction comes from
[X-016’s exact-cover and closure routes (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/explorations/X-016-after-381-two-managers-one-proof-boundary.md#closure-route).

<a id="source-13"></a>

## Source 13: `packing/campaign/hypotheses/H-104-fixed-side-point-cover-auxiliaries.md`

Snapshot `4d305597a505`, source lines 1-end.

```yaml
title: H-104 — the fixed-side point formulas satisfy the exact-angle auxiliaries
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-104
  kind: hypothesis
  claim: >-
    At q = 1939/500, the frozen P10, P12 and A-triple point formulas satisfy all
    seven BC255 auxiliary clauses for contained closed unit squares at exactly
    zero and45 degrees, including boundary placements and the four K4 reflections.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:9', 'proof:10', 'proof:15']
  criterion:
    shape: determination
    metric: conjunction of the seven fixed-side exact-angle auxiliary clauses
    direction: >-
      Accept only when all seven clauses are completely checked by the reviewed
      exhaustive algorithm and independent receipt review passes. Reject on any
      independently checked exact counterexample to one clause, even if other
      clauses remain unchecked. Otherwise leave unresolved.
    threshold: all seven clauses
  instrument: >-
    packing/devtools/run_restricted_orientation_discriminator.py at e45c8a63,
    source-preserving exact event strata with a ten-second child cap. Independent
    source/toy review passed; returned escapes are directly rechecked. Positive
    coverage relies on the reviewed exhaustive algorithm, not counts alone.
  instrument_ready: true
  regime: fixed q=1939/500, fixed point formulas, exact zero and45 degrees only
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: one ten-second producer and a separately bounded ten-second output review
  prereqs: [independent BC255 adapter readiness, prospectively committed experiment]
  replication: false
  registered: '2026-09-06'
  notes: >-
    This is a sufficient proof-mechanism discriminator, not H036's full packing
    statement. Acceptance does not cover nearby angles; rejection does not refute
    H036. A changed point formula, side or angle family requires a new claim.
```

<a id="source-13-h-104--test-the-fixed-point-cover-mechanism-first"></a>

### H-104 — Test the Fixed Point-Cover Mechanism First

Accepted by
[exp-114](12-restricted-orientations.md#source-2):
all seven clauses passed the reviewed exact computation and an independent input/receipt
check. This is only the fixed-formula exact-angle precursor; H-036 remains unresolved.

This claim tests the smallest concrete precursor to
[H-036](15-registered-mathematical-questions.md#source-1), under the
[H-102](15-registered-mathematical-questions.md#source-11) restricted-family agenda.
It does not change H-036’s side threshold or quarter-degree neighborhoods.

Set $q=1939/500$. The frozen `point_sets(q)` formulas in
[the source module](12-restricted-orientations.md#source-1), committed at
`e45c8a63`, define the ten-point set $P_{10}$, twelve-point set $P_{12}$, and
distinguished points $A_1,A_2,A_3$ in their original order (the first three entries of
$P_{12}$). Substitute $q$ into the formulas; do not homothetically scale the source
point sets. The canonical region is $R=[1,q/2]\times[0,1]$; $K_4$ consists of the
identity and reflections in the container’s horizontal and vertical midlines.
The seven clauses are:

- Every contained axis-aligned closed unit square hits $P_{10}$.
- Every such axis-aligned square hits $P_{12}$.
- Every contained 45-degree closed unit square avoiding $P_{10}$ has its center in a
  $K_4$ image of $R$.
- Every such avoider with center in $R$ contains $A_1$.
- Every such avoider with center in $R$ contains $A_2$.
- Every such avoider with center in $R$ contains $A_3$.
- Every contained 45-degree closed unit square hits $P_{12}$.

Containment and point hits include the boundary.
Source-control avoider counts are not requirements on this target; a universally
quantified clause can hold vacuously.
Incomplete receipts are not positive results.
Any retained negative witness must be independently checked against its exact square
corners, point membership, and relevant region.
One valid falsifier rejects the conjunction even if the remaining clauses are unchecked.

The
[adapter review (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-255-fixed-side-discriminator-independent-review.md)
explains the exhaustive source algorithm and its independence limits.
The all-true result is computationally verified for these exact angles, not a standalone
certificate of H-036 or of a continuous-angle theorem.

<a id="source-14"></a>

## Source 14: `packing/campaign/hypotheses/H-105-exp113-overweight-pair-obstruction.md`

Snapshot `4d305597a505`, source lines 1-end.

```yaml
title: H-105 — exp-113's fixed weights have an overweight-pair obstruction
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-105
  kind: hypothesis
  claim: >-
    Among the 60 distinct D4 placements of trump11-v1, with exactly exp-113's
    retained per-member orbit weights (1,0,2/5,1/10,0,1/10,3/10,0), two distinct
    placements have weight sum greater than one and intersecting interiors.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:11', 'proof:17', 'proof:22']
  criterion:
    shape: determination
    metric: existence of a strict positive-area overweight-pair witness
    direction: >-
      Accept with one independently checked strict positive-area witness for an
      eligible pair. Reject only with independently checked separating axes for
      all 134 eligible pairs. Incomplete output, timeout or failed replay is
      unresolved. Neither outcome resolves H099 or certifies global a.e. depth.
    threshold: one overweight pair with intersecting interiors
  instrument: >-
    packing/devtools/run_full_size_density_pair_separator.py and the separately
    reviewed packing/devtools/check_full_size_density_pair_separator.py at cf299e6c.
    Exact separating axes or strict rational-radius boxes, with separate 30-second caps.
  instrument_ready: true
  regime: exact retained Trump side and D4 support; exp113 weights unchanged
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: one 30-second producer and one separately bounded 30-second file replay
  prereqs: [independent pair-instrument readiness, prospectively committed experiment]
  replication: false
  registered: '2026-09-06'
  notes: >-
    This predicts a candidate obstruction, not a feasible dual. A checked
    candidate-refuted packet therefore accepts H105. No-hit is not a.e.
    feasibility because three or more squares can cause excess depth without an
    overweight pair. No new row, LP, weights or geometric support is authorized.
```

<a id="source-14-h-105--does-a-pair-already-invalidate-the-candidate"></a>

### H-105 — Does a Pair Already Invalidate the Candidate?

Rejected by
[exp-115](11-density-contract-candidate-and-results.md#source-3):
all 134 eligible pairs have independently checked separating axes.
This leaves the fixed candidate’s higher-order overlap depth and H-099 unresolved.

[Exp-113](11-density-contract-candidate-and-results.md#source-2)
retained an exact finite-row optimum of $56/5$, not a feasible full-size density dual.
This hypothesis asks whether two squares alone invalidate those fixed weights on a
region of positive area.
It is narrower than [H-099](15-registered-mathematical-questions.md#source-8).

The four unit-weight placements and 32 other positive-weight placements give
$\binom42+4\cdot32=134$ pairs whose weights sum to more than one.
The remaining positive weights are at most $2/5$, so no other pair is eligible.
Touching at an edge or corner does not qualify: the intersection must contain an open
box with a positive rational radius.
Nonnegative remaining weights preserve the excess throughout that box.

The
[independent instrument review (source archive)](https://github.com/jlevy/squares/blob/4d305597a505ebfbe85f1851fa7148374661e622/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-254-pair-separator-independent-review.md)
checks the strict-area argument and complete eligible-pair ordering.
Its file checker uses edge determinants for a witness and direct corner projections for
separation, while sharing the exact number field and accepted original-source
validation. It does not repeat the parent LP.

A witness accepts H-105 and retires only this candidate.
Exhausting all eligible pairs rejects H-105 but leaves possible higher-order excess
depth unchecked. H-099 remains unresolved either way.
The witness point must not become a new LP row without a separate full-support
off-boundary check: it may lie on a third square’s boundary.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
