# Eleven-Square Explainer: Adversarial Proof Reconciliation

**Date:** September 30, 2026\
**Reviewer:** Codex, Astra at max reasoning\
**Tracking:** `think-uqhd`, under `think-75cp`

**Disposition:** The [explainer][article] preserves the mathematical implication of the
[retained original proof][proof]. This review found no new blocking, high-severity, or
medium-severity mathematical error.
Both low-severity qualifications below have been applied and checked.
The illustration plan is mathematically suitable subject to its stated source-binding
and scope requirements, with one worked-row distinction clarified here.

The comparison starts from repository revision
`cbd01be8c38855edf3360f258faf0a1f479e250a` and the original project’s pinned revision
`f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c`. The original `PROOF.md` was read in full, as
was the explainer, including its placement and nonlinear-estimate appendices.
The original file’s SHA-256 is
`a431a62bb4ae04dba49848bbce64a839627e28d20abb15bd58745ea953856ce3`. Concurrent article
work is limited to attribution, citations and the identified qualifications; the
equations, case counts and accepted proof inputs are unchanged.

The audit checks the arguments’ quantifiers and implications, selected implementing
functions, the [accepted whole-proof review][acceptance], and the retained component
identities. It does not repeat the geometric executions or independently re-audit every
line of every checker.
The [final composition][composition], decoded SHA-256
`eaad8f14cf3404e8abe1bfee18cbd7f12a2fed2094f46f021d4e3bfb3088b141`, remains the accepted
composition of the previously observed and reviewed executions.
This exposition review adds no proof credit to a cached success flag.

## Section-by-Section Reconciliation

| Explainer section | Original argument and checked implementation | Adversarial conclusion |
| --- | --- | --- |
| The Result | Original §§1–2; [construction][]; [exact witness check][witness-check] | The isolated root, polynomial and expression for $T$ agree. The decimal is explanatory. The theorem allows independent rotations and legal contact, and asserts both attainment and exclusion of every smaller side. |
| From Weighted Points to a Global Proof | Original attribution and §12; [T-018, T-025, T-026, T-037 and T-059 records][results] | The older point and threshold results are antecedents, not additional premises that turn numerical proximity into equality. T-037’s strict lower bound and T-059’s row-minimum report are kept distinct from T-060. |
| The Construction Gives One Half of the Answer; Appendix A | Original §2; [exact placement formulas][construction]; [local endpoint check][local-check], `audit` | Six axis-aligned squares and five rigid images give eleven unit squares. All 44 vertices and 55 pairs are checked with weak feasible inequalities. Opposite-wall span, needed at the end, is a separate checked property. |
| Sixteen Regions Cover All Possible Centers | Original §§3–4; [D4 checker][d4-check], `check_cover`, `canonical_masks` | Nearest-site halfplanes establish coverage, not an area sum. The open inscribed disks give center distance at least one. Strict cell diameter makes every containing-label choice injective. Half-turn pairing gives 4,368 raw and 2,184 canonical masks without an assumed orientation pattern. |
| One Geometric Invariant Supports the Certificates | Original §5 and §14; [row checker][row-check], `strict_core`, `necessary_self_cuts`, `universal_collision`; [generic checker][generic-check] | The outer cover is an overestimate; ownership is a conclusion about the actual square in every packing satisfying the antecedent. Strict inner containment supports closed collision rejection. Complete legal-domain coverage and complete angle joins precede promotion. |
| Charge Budgets Exclude Many Patterns at Once | Original §§5, 9 and 12; [field review][field-review]; [field checker][field-check], `row_envelope`, `true_halfplanes`, `transferred_cases` | The article supplies an explanatory field-capacity lemma that the original exposition leaves mainly to its certificate implementation. The median-projection definition and strict separation proof agree with the independent consumer. Required owners and strict total charge are both necessary for mask transfer. |
| Conditional exclusions | Original §5; [baseline D4 cut checker][cut-check], `baseline_context`, `offending_regions`; [center partition][center-partition], `admit_center_partition` | Cases 2175 and 2176 depend on the exact 1,931-case baseline, not the later four-survivor conclusion. Case 1383 requires both closed children, each starting from its own copy of the same accepted parent. |
| Symmetry Reduces the Four Survivors to One | Original §6; [D4 checker][d4-check], `check_overlay`, `check_bans`, `solve_non_target_cases` | The argument concerns physical symmetries and independently chosen closed labels, not a permutation of irregular cells. All 220 regions, including eight singletons, and 1,572 strict bans belong to an exhaustive relaxation. An unrealizable assignment being allowed only weakens that relaxation. |
| Capture Forces Case 438 Near the Construction | Original §8; [child checker][child-check], `conditional_view`, `check_step`; [composition joins][joins], `capture_conditions`, `reviewed_capture_states` | The three closed splits cover all possibilities. All ten nodes and nine parent joins matter; a near-state file alone is insufficient. Empty far leaves and the live near enclosure have different conclusions. Trailing partial updates promote no state. |
| The Local Argument Excludes Every Nonzero Motion; Appendix B | Original §7; [local checker][local-check], `bridge_features`, `strict_feature_margin`, `strict_dual_margin`, `audit` | The feature census covers changing separation choices. Gradient aliases do not lose their nonlinear curvature bounds. All signed-coordinate duals and unavailable-feature estimates are needed; infinitesimal rigidity alone would not prove the declared finite rectangle. |
| Closing the Gap Between the Rational Cap and the Exact Optimum | Original §§3, 8 and 10; [pose inclusion][pose-check], `inverse_center`, `axis_angle_bound`, `slanted_angle_bound`, `check_pose` | The exact map divides out the field scale, undoes the checked quarter-turn and includes the $U-T$ translation. A concentric side-`S` container becomes a side-`S` container inside $[0,T]^2$. No physical small square is rescaled in the final deduction. |
| What Was Verified; Sources and Verification Record | Original §§9–15; [final composer][composer]; [epistemic policy][levels]; [reproduction guide][reproduction] | Mathematical rules, checked instances and composition are separate obligations. The article discloses shared primitives, same-method confirmation, the publisher’s stale bindings and the independent rerun-automation limit. It claims neither a distinct proof method nor proof-assistant verification. |

## Findings Ranked by Severity

**Blocking, high and medium findings:** none found within this review’s stated scope.
The original proof’s mathematical sequence is preserved; no missing global case,
uncancelled branch assumption, sign reversal or endpoint approximation was identified.

**Resolved, low: specify the core geometry in the finite-direction explanation.** The
field paragraph first refers to general strict inner cores, then uses square-axis
directions to reduce the median condition to finitely many checks.
Those directions are sufficient for the square cores used by the field certificates.
An arbitrary convex polygon would need its own support-function break directions.
The article now states:

> For the square cores used by these field certificates, directions parallel to the
> core’s axes and normals to site-pair lines divide the directions into sectors.

The [field checker][field-check] constructs a midpoint-oriented square in
`row_envelope`, rotates into its axes in `rotate`, and inserts the two coordinate
directions in `true_halfplanes`. Between successive direction events, the median site
and support formula are linear in the normal.
This qualification preserves that exact argument.

**Resolved, low: identify the special case’s height coordinate.** The case-1383 sentence
gave $y_{13}=4/3$ without identifying the coordinate as centered or scaled.
The article now adds:

> Here $y_{13}=p_y-U/2$ is the centered physical height of the square assigned to cell
> 13\.

The [center-partition helper][center-partition] reads `bound_centered_unit` and
constructs the field bound as $B(U/2+4/3)$, then checks the actual source halfplane.
Reading $4/3$ as a positive-frame or field coordinate would select another partition.
The accepted consumer already uses the correct frame; this is a prose qualification.

The [separate citation and documentation audit][citation-review] records other editorial
suggestions.
Expanding S5/V4/C5, stating orientation modulo $\pi/2$ beside the half-angle
chart, and replacing the forward reference to a “right-hand denominator” improve
orientation but do not repair a mathematical failure.
Citation edits and unused-alias cleanup likewise change navigation, not proof premises.

## Attempts to Falsify the Reductions

**A boundary center does not escape the mask census.** Every point of the normalized
center square has at least one nearest site.
If two physical centers could receive the same closed label, their distance would be
strictly less than one, contradicting their disjoint open inscribed disks.
Thus arbitrary independent choices at ties still give eleven distinct labels.
The D4 argument must consider all these assignments: exclusion of a closed antecedent
rules out a packing having even one such assignment.
It does not require a deterministic tie-break that commutes with symmetry.

**A closed collision boundary is not legal touching of the physical squares.** If
$x\in K-Q$, some $k=x+q$ belongs to the owned hull and translated strict core.
Both lie inside their respective physical square interiors.
Their common point therefore has a small open neighborhood in both squares, giving
interior overlap. Without strict containment this argument fails: two physical squares
may share an edge legally.
The stronger partner-cover rule is universal in both the partner’s angle row and its
center domain.
Its vertex inequalities use minimum support over every partner domain; one
convenient partner pose cannot justify a forbidden region.

**The raw source hint is not always the coverage obligation.** The accepted predecessor
outer domain, intersected with independently necessary wall and self-hull constraints,
contains all legal centers.
Covering that required domain is sufficient.
Covering a larger source hint may fail on physically impossible centers; shrinking
without a proved necessity implication would be unsound.
Residual regions may conservatively extend beyond the required domain.
A future picture must distinguish this geometric overestimate from the actual feasible
set.

**Median charge cannot be replaced by counting contained sites.** Take five sites
$(0,0),(1,0),(-1,0),(0,1),(0,-1)$. Every directional median is zero.
A small square core around the origin therefore receives the median-projection charge
while containing only one site.
A “three sites inside” explanation would not justify the accepted majority regions.
Conversely, two compact cores strictly inside disjoint physical interiors are strictly
separable; their disjoint projected intervals cannot both contain the same median.
Strictness also matters here: two closed squares touching at the origin could both
contain that median if used as their own non-strict cores.

**Endpoint probes cannot replace a whole-angle proof.** Even a rational quadratic can be
positive at both ends and negative between them: $t^2-t+3/16$ has this behavior on
$[0,1]$. The checkers inspect an interior minimum when required.
At a closed partition seam, a feasible pose is covered by the adjacent closed rows.
When a branch clips away an old interval whose overlap is only that seam, the retained
adjacent row still covers the endpoint; the actual branch checker also requires the full
allowed closed range.
This does not authorize dropping singleton center domains or accepting an unsupported
singleton angular branch.

**A linear obstruction alone does not prove a finite neighborhood.** The one-dimensional
system $h\ge0$, $-h+h^2\ge0$ has only zero in its linearized feasible cone, yet $h=1$ is
feasible. The article retains the quantitative Taylor estimates needed to exclude the
actual captured rectangle.
It also retains every available separation branch; fixing the witness’s contact choice
would not cover a nearby packing that uses another available separating axis.

For the accepted local calculation, let $r=\lambda^{\mathsf T}A-\sigma e_j^{\mathsf T}$
and choose $\sigma h_j=-\tau r_j$. Then

$$
-\frac{\tau^2M_j}{2}
\le\lambda^{\mathsf T}Ah
=-\tau r_j+rh
\le-\tau r_j+\epsilon_j\tau R.
$$

This checks the potentially troublesome dual sign directly.
Nonnegative weights preserve the necessary row inequalities.
The strict bound $M_j<2(r_j-\epsilon_jR)$ gives a positive denominator and
$\tau\le c_j\tau^2$ with $c_j<1$, impossible for $0<\tau\le1$. The implementation takes
the maximum curvature over elementary gaps sharing a gradient, so reducing identical
derivative systems does not substitute one alias’s smaller nonlinear error for
another’s.

**The local theorem is not an impossibility theorem at $U$.** For an arbitrary
hypothetical $S<T$ packing, concentric embedding into $U$, physical D4 symmetry,
capture, and the checked inverse frame put that same packing in
$[(T-S)/2,(T+S)/2]^2\subset[0,T]^2$. The fixed-`T` local theorem now applies.
It forces the spanning construction and contradicts $S<T$. This argument uses neither
compactness nor a limiting sequence, and does not assert that the cap itself has only
one feasible packing.

## Simplification Ledger

This is a bounded search for simplifications at the proof’s principal interfaces.
It is not an exhaustive search over all possible proofs or expositions.
Candidates were accepted only when their implication follows from the retained premises
without new geometric computation.
None reduces the accepted case, row or branch inventory.

| Candidate | Disposition and reason | Obligation that remains |
| --- | --- | --- |
| Explain exclusion and capture through one outer-cover/owned-hull invariant | **Safe expository consolidation, already adopted.** The same preservation implication serves both uses. | Full-angle strictness, complete legal-domain coverage, valid initial ownership, same-prior joins and justified compression remain separate checks. |
| Use one strict-core lemma for both collision rejection and charge capacity | **Safe explanatory consolidation.** Strict containment turns a shared core point into physical overlap and gives strict separation of different legal cores. | Do not conflate the different conclusions: a collision is impossible, whereas a charge counts against a finite resource. |
| Explain the majority feature by median projections | **Safe and shorter than listing all subset hulls.** It is the feature’s exact tested condition, with capacity one proved by separation. | Retain all normal sectors and specify the square-core support function. Literal majority point containment is not equivalent. |
| Summarize the nonlinear local proof by $\tau\le c_j\tau^2$, $c_j<1$ | **Safe expository consolidation, already adopted.** It follows from the displayed dual residual and Taylor bound. | All 8,448 margins, positive denominators, 88 unavailable features and alias curvature maxima support that summary. A rounded worst ratio is not its proof. |
| Finish by directly recentering a hypothetical smaller container | **Safe and sufficient, already adopted.** The exact frame maps side $S$ to the same side $S$ inside $T$. | Keep the $U-T$ translation, inverse quarter-turn, field scale and witness span. No unit-square rescaling or compactness argument is needed. |
| Replace the D4 overlay by permuting cell labels | **Rejected.** Only the checked half-turn permutes these irregular cells in the required way. | The closed four-view overlay, singleton regions and exhaustive assignment rejection remain. |
| Prove early D4 support cuts from the final four survivors | **Rejected as circular.** Those cuts are used in exclusions needed to reach the four-survivor set. | The fixed 1,931-case baseline and its 506 raw surviving masks discharge the early cut obligations independently. |
| Replace closed coverage by area totals, sampled angles or positive-area pieces | **Rejected.** These can omit a legal seam or a whole lower-dimensional domain. | Exact closed coverage and necessary full-interval inequalities remain. |
| Promote one illustrated row’s inner points, omit an intermediate parent, or merge sibling states | **Rejected.** These lose angle completeness or import conclusions proved under different assumptions. | Complete owner updates, exact parent-state transfer and independent closed branch copies remain. |
| Replace the focused rectangle by a simpler uniform radius, or remove more branches using a new lemma | **Deferred mathematical work.** No such replacement was established in this review. | It would need a new quantitative implication and matching inclusion evidence, or replacement certificates and review. |
| State a separate classification of every optimal packing | **Outside this exposition task.** A precise uniqueness statement would be a different registered conclusion, not a simplification needed for $s(11)=T$. | This review neither registers it nor uses it as a premise. |

## Mathematical Review of the Illustration Plan

The [illustration plan][illustrations] distinguishes diagrams of exact data from
schematics of proved implications.
Its proposed cell-capacity, field, D4, capture, local-inequality and frame figures have
the correct mathematical roles.
Their labels must retain the following distinctions:

- The cell diameter is measured after the $(U-1)$ scale.
  Hypothetical centers illustrate an impossibility argument; they are not a displayed
  feasible packing. A closed cell tie and a strict distance ban are different facts.
- Center positions and square-relative core offsets need distinct axes or labels.
  A Minkowski obstacle is a forbidden **center** set, not a region occupied by another
  physical square. The residual panels must cover the independently required legal
  domain, including any retained point or segment.
- A median-projection illustration must not become a three-contained-sites picture.
  The transfer example must check required-owner membership and strict charge excess for
  each selected mask. Collision alternatives are not additional charge resources.
- D4 images of a point can be illustrated on the cell map, but rotating a colored cell
  must not imply that it becomes one other cell.
  One displayed distance ban cannot replace the exhaustive finite search.
- Capture edges denote dependencies.
  All cut labels are closed; the near leaf gives an enclosure whose inclusion and
  fixed-`T` isolation are separate premises.
- The $\tau$ diagram is an algebraic consequence of all signed-coordinate certificates,
  not a sampled physical motion or a projection establishing a 33-dimensional theorem.
  The cap-to-`T` diagram must show the rigid physical map after undoing field scaling.

The initially proposed first capture row has an additional complexity: its single
supplied `collision_regions` entry is a universal partner-core region checked against
all 149 partner rows, 93 of them live.
It is not explained solely by one fixed owned hull’s $K-Q$ obstacle.
A picture of that row must show or explicitly name the universal partner-cover premise.

The revised plan selects case 2095, node `mask2095-hull-first-v5`, step 1, owner 10, row
17, with $t\in[17/32,9/16]$. Read-only inspection of the retained source finds six
input-domain vertices, eight core vertices, one triangular residual, and no universal
collision region. The [complete 2095 execution][generic-result] accepts its five steps
and 160 rows. The decoded source is
`68adba943c66ee60c65caf8094dfc18f68a622379acf506ed40558f87602f8aa`, retained in the
[2095 object directory][generic-objects]. This is a noncandidate-exclusion example, not
a case-438 capture row.

An empty `collision_regions` list does **not** mean that this row has no $K-Q$
obstacles.
The [fresh generic checker][fresh-check], `_check_row`, reconstructs them from
every different owner’s accepted hull and the query core before testing
`forbidden + residual`. The renderer must use the accepted predecessor after complete
step 0, and any promotion shown must refer to the complete step 1 join.
Selecting this row makes no new geometric acceptance claim; a faithful visual extraction
still needs its own source and rendering checks.

## Confirmation and Remaining Scope

The article’s attribution agrees with the source packet and current T-060 record:
Trump’s attaining construction, Ellsworth’s reconstruction, the Squares Project and
Kleddamag antecedents, and Ahmed’s Astra-assisted global argument have different roles.
This paper explains the imported argument and the repository’s confirmation; it does not
claim a new global proof method.

The accepted equality remains S5/V4/C5. Shared construction, derivative and arithmetic
primitives remain in the trust base.
The review is not distinct-method C4 confirmation or V5 proof-assistant verification.
The composer binds the completed observed ensemble; it does not recompute its geometry.
The publisher’s stale final-state bindings and the independent pipeline’s
receipt-rebinding work are disclosed reproduction limitations, not unacknowledged
mathematical premises of the accepted ensemble.

No broad test suite or geometric proof replay was run for this reconciliation.
No accepted proof source, receipt, count or frontier value was changed.

[article]: ../../../packing/devtools/templates/n11-optimality-article.md
[proof]: ../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md
[acceptance]: review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance
[composition]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/final-composition.json
[construction]: ../../../packing/cases/trump11/packing.py
[witness-check]: ../../../packing/cases/trump11/verify_exact.py
[results]: ../../../packing/frontier/results.yaml
[d4-check]: ../../../packing/devtools/check_n11_optimality_d4.py
[row-check]: ../../../packing/devtools/check_n11_capture_transition_pilot.py
[generic-check]: ../../../packing/devtools/check_n11_generic_sequential.py
[field-review]: review-2026-09-29-n11-optimality-census-contract.md#generic-weighted-field-admission
[field-check]: ../../../packing/devtools/check_n11_optimality_field_mask0.py
[cut-check]: ../../../packing/devtools/check_n11_baseline_d4_cuts.py
[center-partition]: ../../../packing/devtools/n11_nonfield_center_partition.py
[child-check]: ../../../packing/devtools/check_n11_capture_child_node.py
[joins]: ../../../packing/devtools/n11_composition_joins.py
[local-check]: ../../../packing/devtools/check_n11_optimality_local_isolation.py
[pose-check]: ../../../packing/devtools/check_n11_optimality_pose_inclusion.py
[composer]: ../../../packing/devtools/check_n11_final_composition.py
[levels]: ../../../epistemics.md
[reproduction]: ../../../packing/resources/web/n11-optimality-2026-09-29/README.md#reproducing-the-independent-checks
[citation-review]: review-2026-09-30-n11-explainer-citations-and-docs.md
[illustrations]: ../specs/active/plan-2026-09-30-n11-optimality-illustrations.md
[generic-result]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-mask2095-intake/full-result.json
[generic-objects]: ../../../packing/resources/web/n11-optimality-2026-09-29/receipts/generic-mask2095-intake/objects/
[fresh-check]: ../../../packing/devtools/check_n11_generic_fresh.py

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
