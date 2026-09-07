# BC-252 — Complete Rows on the Retained Sites

Assessment under `think-csgu`, starting `2026-09-07T02:24:24Z`. Workflow entry:
`insight-iteration`. This is a proposal from retained evidence and source inspection; no
LP, geometry, profiling, target execution, or implementation was performed.

Prefer fixed-site row completion before adapting the dual support.
Keep the density and continuous-angle control gates ahead of a new scalar launch during
the remaining roughly two hours.
H-093 and exp-116 remain unresolved.

The [terminal summary](bc-234-scalar-61-16-leg-01-summary.json) records 24,653 sites in
3,180 D4 orbits and 11,885 rows.
At iteration 18 the numerical LP objective is `10.717562359067587`, while the extracted
rational family weighs `9.902499441` and has maximum depth `7994824851/8000000000`,
about `0.999353106375`. The LP-to-family mass gap is about `0.81506`. All 19 row solves
hit the two-round limit.
The best independently replayed family came from iteration 14 and has mass about
`10.08018` at depth one, as recorded in
[exp-116](../../experiments/exp-116-h-093-scalar-61-16.md).

The [cutting loop](../../../../../src/sqpack/fractional/cutting.py) caps the number of
**dual placement rows**, not the number of primal atom sites.
`support_entries` keeps the 96 heaviest positive row weights and rounds them to
denominator `10^9`; each retained row then contributes eight D4 placements.
Its depth separation therefore prices a truncated family.
The final empty selection stops the loop even when `solution.converged` is false.
This extracted family has no violating vertex; neither the full dual nor the site set is
shown to have saturated.
The discarded full dual and primal weights are not stored in the state.

In [solve_rows](../../../../../src/sqpack/fractional/colgen.py), row completion is a
different operation: it finds undercovered placements in every net direction and adds up
to three rows per direction per round.
With sites fixed, adding valid rows can only increase the exact covering optimum.
Adding sites can only decrease it.
Alternating both while truncating the dual obscures which limitation matters.
The value near `10.71756` is neither a certified cover nor the upper endpoint of a
bracket on the unrestricted covering problem.

## Proposed Hypothesis and Decision

Register a new, narrower H-094 descendant before execution: **the terminal exp-116 site
set admits a rational covering measure of mass below eleven at side `61/16` under
fixed-site row completion.** H-094 is an open question and cannot supply its acceptance
criterion; the changed recipe is not an unchanged H-093 retry.

Freeze the terminal state, side, core `9977/10000`, all 181 directions, site orbits,
initial exact rows, three rows per direction, snapping rule, and rationalization scale.
Use one row-only invocation with at most eight additional separation rounds and a
1,800-second cooperative row deadline.
Hold sites fixed throughout; do not run arrangement-depth separation or change a support
cap. These are proposed limits, not an allocation or a launched experiment.

- Accept the site-sufficiency claim only after a rational mass-below-eleven candidate
  passes the existing production sweep, interval decision, and standalone verifier.
  A row-converged numerical value below eleven merely triggers that sequence.
- Reject only with an independently checked rational dual on valid retained placements
  satisfying every fixed-site orbit constraint and total at least eleven.
  This excludes that site set; global depth at most one would still be required to
  reject H-093. Any finite subset of valid rows can furnish the fixed-site rejection;
  row convergence is unnecessary for it.
- Stop row generation on convergence, a numerical objective at least eleven, a technical
  refusal, the round cap, or the cooperative deadline.
  Preserve all rows and costs.
  A numerical crossing triggers exact dual checking and is not a rejection.
  Failure to obtain either exact outcome is unresolved, with no retry or budget
  increase.

## Readiness, Cost, and Allocation

The [bridge](../../../../../devtools/freeze_cutting_primal.py) already performs
fixed-site row completion, but it writes no JSON receipt or updated state when it
refuses. Before commissioning this test, retain per-round `RoundTiming`, exact rows,
terminal primal and full dual vectors, stop reason, and outer wall/CPU costs on every
exit. Reuse its snapped-row reconstruction and rationalization.
A new finite-site dual acceptance path needs exact incidence checking; the numerical
coefficient matrix’s coverage slack is not an exact geometry certificate.

Controls should exercise the existing side-two positive cover and mass-threshold
refusal, an unconverged empty-site-selection case that continues row work, and
deadline/refusal publication that preserves the input and all added rows.
Check that the fixed site set and supplied net remain identical, because the state
stores direction indices without their net.
Independently replay any proposed finite-site dual and mutate one inequality to ensure
its checker refuses it.

The last two-round phase cost `454.01` seconds; its subsequent snapped LP solve cost
`122.11` seconds, while depth separation cost `9.00` seconds.
Phases 13–18 ranged from `214.28` to `454.01` seconds.
These retained timings support a **planning allowance**, not a runtime prediction, of
30–40 minutes for a capped completion and tail, plus 15–20 minutes for receipt/control
work and review. The finite-site exact dual route is not commissioned, and its
implementation and verification costs are unpriced.
Exact covering-candidate verification also needs a separate allocation.
Complete that pricing before launch; this assessment does not establish that the whole
discriminator fits the remaining session.

A larger dual support could expose missing site cuts, but its full cardinality is
unrecorded and larger arrangements increase both vertex generation and depth work.
It also leaves row completion unresolved.
Defer that experiment until fixed-site completion produces an exact obstruction or a
retained failure that specifically justifies support adaptation.
Do not spend the remaining session on an unpriced support sweep.

Source provenance in exp-116 names `4d305597`. This assessment read the current
repository copies of the cited functions; the recorded detached checkout path was
absent, so no independent frozen-source identity comparison was completed.
Git and shared campaign records were untouched.
The mathematical assessment ended at `2026-09-07T02:30:45Z`; document finalization
followed. Practical Prose supplied the document structure and footer; Flowmark formats
this assessment only.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
