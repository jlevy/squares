---
title: H-346 — an angle branch and bound with retained affine LP models prices the outer capture bridge
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-346
  kind: hypothesis
  claim: >-
    A branch and bound from the family's full occupancy cells at cap U', retaining all
    cell-allowed centre and slider positions and a covering set of angle charts and
    separating-feature alternatives, has a Knuth pricing estimate below 10^8 nodes at
    the widened H-329 terminal target and below 10^10 at the H-340 uniform-floor
    1/1216 radius-vector target. Each exclusion uses a lower model valid throughout
    its node, retaining and minimizing the affine angle term before subtracting a
    certified remainder. Each terminal leaf establishes every premise of its target theorem for all target
    packings in that leaf: packings with s <= S* normalized in C(S*). The leaf
    implication carries angle, centre, slider, frame and feature bounds; C(S*)
    containment is inherited from the target class, not inferred from the U' node.
  lane: proof
  derived_from: [X-052]
  criterion:
    shape: determination
    metric: >-
      Knuth inverse-probability path weights, with all child alternatives counted,
      over at least four independent batches of 500 probes at each target; batch
      means, 95 per cent empirical t intervals over batch means, probe maxima and
      dispersion, feature-stratified coverage, lower-model and localization costs.
      Report separately exclusion leaves, validated terminal leaves, unresolved feature
      disjunctions, depth or resolution floors, LP failures and censored probes. Record
      all domain restrictions and the proved implication or covering branch that
      justifies each, including centre and slider localization universal over target packings in the leaf.
    direction: >-
      Confirm the sampled pricing claim only when the upper endpoints of the
      predeclared empirical intervals are below 1e8 at the widened target and below
      1e10 at the 1/1216 target, with no unresolved or censored terminal outcomes in
      the reported probes. A lower endpoint above either threshold refutes that
      conjunct for this tested design and budget. Threshold overlap, an unavailable
      terminal theorem, or any unresolved probe leaves proof-tree pricing unresolved.
      Empirical intervals can miss rare costly subtrees and are not mathematical tree
      bounds. Floor-truncated estimates are labelled separately and cannot confirm the
      proof-tree claim.
    threshold: both empirical upper endpoints below their node budgets; 1e8 widened; 1e10 uniform-floor 1/1216; no unresolved probe terminals.
  instrument: >-
    Unbuilt: adapt devtools/pilot_n17_subpattern_bb.py with outer LP relaxations over
    full cell-allowed centre and slider domains, covering angle charts and feature
    branches; box-valid dual sheets or nonlinear outer relaxations retaining angle
    increments; certified affine-plus-remainder bounds; coordinate-support LPs bounding
    both signs of every required centre and slider coordinate; explicit target-conditional terminal-premise
    checks; and independent-batch Knuth probes that account for every child. Numerical
    LP proposals must pass the validity tests before their outcomes count as exclusion
    or terminal leaves; failed checks remain unresolved.
  instrument_ready: false
  regime: >-
    n = 17; the family's state at U' = 935106018721/200000000000; the exact root's
    frame; full H-266 cell domains at the root, including square 6; H254 lifts only in
    angle charts where they apply. Pricing only, no exclusion admission. The widened
    target is conditional on H-329; the uniform-floor vector and slide composition are
    those of H-340. Target packings have s <= S* and are normalized in C(S*); the
    larger U' domain is an outer relaxation. No narrow slider or centre premise is
    imposed at the root without a proved implication for that target class.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: >-
    Initial build estimate about 25 agent-hours on the existing branch and bound;
    corrected full-domain model, feature branches and universal localization costs
    must be measured in the pilot. Price both targets before funding a full run.
  prereqs: [H-329, H-340]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-052's direction 5 and the after-pilot review's route (b). Corrections of 9 October
    following review C1, C2 and C6: the original restatement omitted first-order
    variation, imported the scope review's narrow slider premise into the outer root,
    and confirmed using only the widened-target threshold. The operative model retains
    the affine term, proves the target-conditional terminal implication from full cells, and requires
    both pricing thresholds. The sampled curvature near the family (about 0.3 per
    squared radian) is exploratory and cannot justify a node closure; quadratic error
    describes a retained affine model, not the variation of the value across a box.
    Basis or feature changes require explicit feasibility checks or covering branches.
    An expensive estimate rejects this design's budget, not every capture method.
---
# H-346: Price the Bridge Before Building It

**Mechanism.** At fixed angles and a fixed separating-feature branch, containment and
nonoverlap are linear in the centres and side.
For an angle box $B$ centred at $c$, use a dual lower sheet $L_B\le v$ valid throughout
that branch and box, with certified expansion remainder $R_B$. The lower bound retains
first-order variation:

$$
\inf_{\theta\in B}v(\theta)\ge
L_B(c)+\min_{\delta\in B-c}g_B^{\mathsf T}\delta-R_B.
$$

For a rectangular box with half-widths $\rho_j$, the affine minimum is
$-\sum_j|g_{B,j}|\rho_j$. Dual feasibility must hold throughout $B$; basis and feature
changes require checks or covering branches.
An outer relaxation retaining angle increments and bounding all nonlinear terms is
another admissible construction.
A node closes only if its certified lower bound exceeds $U'$.

Root nodes retain every cell-allowed centre and slider position and every unresolved
feature alternative.
Narrow slider bounds from the scope review are terminal premises; entering them requires
a proved implication or complete branching.
An angle box alone cannot localize centres: maximizing both signs of each required
coordinate over an outer feasible relaxation is one way to certify universal bounds.
One nearby LP optimizer supplies no such implication.

Let $\mathcal P$ be the possible counterexamples with $s\le S^\ast$, normalized in the
centred container $C(S^\ast)$. A leaf $L$ with terminal target $T$ must prove
$\mathcal P\cap L\subseteq T$. Bounds proved on the full $U'$ outer node imply bounds on
this subset, but the local theorem’s original $C(S^\ast)$ containment and its geometric
consequences, such as the lower slider face $a\ge0$, may instead be inherited from
$\mathcal P$. A small translation of the endpoint can fit $C(U')$ while leaving
$C(S^\ast)$, so requiring that containment of every outer-node packing would be false.
The widened H-329 target and the H-340 local target must each carry their own
conditional premise contract.

**Falsifier.** The empirical interval’s lower endpoint exceeds $10^8$ nodes at the
widened target or $10^{10}$ at the uniform-floor $1/1216$ target.
An interval crossing a threshold or a probe ending unresolved leaves the pricing verdict
unresolved.

**Expected information.** The sampled cost of the corrected full-domain tree at both
terminal targets, including feature branching and universal localization.

**Limits.** Knuth probes provide pricing evidence and can miss rare expensive subtrees.
Depth floors, unresolved features, LP failures and censored probes are not validated
leaves. Their reported truncated-tree costs cannot be read as proof-tree costs.
The widened leaf remains conditional on H-329, and this proposal admits no certificate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
