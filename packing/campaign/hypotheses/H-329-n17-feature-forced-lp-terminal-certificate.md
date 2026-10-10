---
title: H-329 — an exact dual-sheet certificate proves the widened projection theorem over the feature-forced angle box
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-329
  kind: hypothesis
  claim: >-
    Every packing of 17 unit squares of side at most U' = 935106018721/200000000000 in
    the family's occupancy state whose sixteen non-free angles lie within 5e-3 of the
    family's (H254 lifts), whose centres lie within 1e-2 of the family's in the exact
    root's frame, and whose sliders lie in the H256 domain widened by 1e-2, has S >= S*
    with equality only on the family; and this is certified by at most 10^5
    branch-qualified direction patches on the sphere of the seven backbone angles.
    Every surviving feature branch on every patch has a dual lower bound at least S*
    throughout its angle domain, or a certificate of infeasibility; the patch cover,
    radial bounds, other-angle checks and equality classification are exact.
  lane: proof
  derived_from: [X-051]
  criterion:
    shape: determination
    metric: >-
      First a numerical pilot: 2,000 sampled directions at four radii, distinct active
      row sets, their ranks and conditioning, Chao1 category-richness diagnostics and
      sampled slopes. Then an actual certification pilot: exact patch coverage,
      certified patch count, feasibility and interval failures, unresolved regions and
      measured time per patch. The completed build records, for every feature branch
      and patch, dual feasibility throughout the patch, the retained affine term and
      certified remainder proving the lower bound, or infeasibility; complete sphere
      and radial coverage; the nine non-backbone angle checks; the 135 unavailable
      options forced negative throughout the box; and equality only on the family.
    direction: >-
      Confirm only when the exact build covers the full stated domain with at most 1e5
      branch-qualified patches, every branch on every patch has the required lower
      bound or is proved infeasible, and the equality classification passes. A weak
      dual sheet does not refute the LP. A rigorously established deficient LP optimum
      at a point shows that this relaxation cannot certify that point; an exploratory
      deficiency requires exact diagnosis. Chao1 counts and sampled slopes guide pilot
      budgeting only; unresolved patches leave the certificate claim unresolved.
    threshold: at most 1e5 certified branch-qualified patches; complete domain cover; every branch exact; equality only on the family.
  instrument: >-
    Unbuilt: a numerical patch counter over the fixed-feature LP with HiGHS proposals,
    followed by an actual exact coverage pilot and certifier using exp-244's kernel and
    duals, interval Krawczyk solves and outward rounding as the widened-projection scope
    review specifies; feature-forcing extension of the option margins to the box;
    explicit branch-infeasibility and equality checks.
  instrument_ready: false
  regime: >-
    n = 17; the exact root's frame; the family's state; cap U'; the slider domain of
    H256 plus 1e-2; square 6 coarse and absent from every row; angles as H254 lifts.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: >-
    Numerical pilot: 8,000 LPs, one W7 slice plus review. Price the exact build from
    actual certified patch coverage and measured patch times before assigning a
    CPU-day budget; basis-richness counts do not bound certification cost.
  prereqs: [H-261, H-268, H-278, H-288]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051's route C and candidate C4. Corrections of 9 October following review C8 and
    C15: a feasible feature branch minimizes the primal objective and maximizes the
    feasible dual objective; the minimum is over feature branches, not dual sheets.
    Chao1 is a lower-bound diagnostic for category richness, not an upper bound on
    certification patches. An active-row set can be rank-deficient, several bases can
    represent one sheet, and one sheet can need several interval patches. The
    exploratory evidence remains all 32 coordinate slopes positive from 1e-5 to 3e-2
    radians, softest 0.0155 along -omega16, and sheet curvature of order 0.3. It
    certifies nothing. A completed exact theorem would supersede the 1/5000 terminal
    target; the outer route must establish all of its localization premises.
---
# H-329: The Terminal Theorem as an LP Certificate

**Mechanism.** Where the 135 unavailable owner-axis options stay negative, every contact
pair is separated along an endpoint feature.
For a fixed feature branch, nonoverlap and containment are linear in the centres and
side at fixed angles.
Under LP duality the value has the form

$$
v(\theta)=\min_f\sup_{\lambda\in D_f(\theta)}\lambda^{\mathsf T}b_f(\theta),
$$

where $f$ ranges over feasible feature branches and $D_f(\theta)$ is the feasible dual
set. Every surviving branch and angle patch needs one valid lower sheet at least
$S^\ast$, or an infeasibility certificate.
A weak feasible sheet says nothing about the best available dual bound.
The proposed certifier retains the sheet’s affine term over each patch and bounds its
remainder throughout that patch; it must also prove the complete angle-domain cover and
the equality case.

**Falsifier.** A rigorously established deficient LP optimum at a point defeats this
relaxation’s certification there.
Exceeding $10^5$ actual certified patches rejects the registered completion budget.
Numerical active-row counts alone establish neither.

**Expected information.** Whether the terminal region can be certified at angle radius
$5\times10^{-3}$, and the measured patch cost of doing so.

**Limits.** The frame, cap and $u^\ast$-enclosure obligations of the composition review
remain required.
Square 6 stays coarse; the outer route from the cells must establish the
centre, angle, slider and feature premises.
Only the completed exact cover proves the theorem.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
