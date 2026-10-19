# Mathematical Audit of Routes to Significant Progress on Small Square Packings

**Date:** September 14, 2026.

**Status:** Mathematical strategy audit from retained evidence.
No scientific target was run, no hypothesis was registered, and no frontier claim was
changed.

**Scientific evidence cutoff:** The record through revision
80bcdbb0819504354e1278c37f211dd8cc2158fb, as reconciled in the
[synopsis](../../../SYNOPSIS.md#research-program-status-and-roadmap).
The
[active strategy plan](../specs/archive/plan-2026-09-10-n11-daytime-strategy-and-explainer.md)
and
[agenda 036](../../../packing/campaign/agendas/agenda-036-n11-strategy-reset-roadmap.md)
own subsequent execution choices.

Route A remains the strongest candidate for a substantial lower-bound advance, but its
first executable block needs a complete geometric domain and a stronger comparison than
the existing owner-patch tests.
Route S has the best prospect of producing a bounded, useful mathematical deliverable
with the admitted tools.
Route B offers the strongest alternative mechanism, although its present description
understates the discretization and certification work.

Among the five routes shaped before this audit, the recommended order for the next
research allocation is **A, S, B, C, D**, with D treated as a separately budgeted
background search.
This is a judgment from the retained evidence and prerequisites, not a
measured success probability.
A global lower bound of $3.84$ would remove approximately 27% of the current interval;
$3.85$ would remove approximately 47%. Either would also prove a physical
fractional-packing gap beyond the known point/density ceiling.
Route S offers a different authorized outcome: a substantially simpler proof of the
existing $3.82$ bound.

## Evidence Boundary and Mathematical Payoff

The problem is to determine $s(n)$, the infimum of square-container sides admitting $n$
unit squares with pairwise disjoint interiors.
The squares may rotate and touch.
A selected **strict core** is a closed square contained in its unit parent’s interior;
cores from different parents are therefore disjoint even on their boundaries.
The [tutorial](../../../TUTORIAL.md#1-the-problem) defines the certificate construction,
and [conventions](../../../conventions.md#4-evidence) separates formal verification from
numerical evidence.

The following facts constrain the choice of route.

| Status | Retained result | Strategic implication |
| --- | --- | --- |
| Registered, V4/C5 | T-025 proves $s(11)\ge3.82$; T-026 proves $s(11)\ge3.826447410572939\ldots$ | The next bound should justify its cost relative to this frontier |
| Registered upper bound | Trump’s exact construction gives $s(11)\le3.877083590022814\ldots$ | A verified smaller construction would immediately change the upper bound |
| Registered conditional result, V3/C3 | T-023 excludes one specified four-owner branch at $3.84$, with admitted symmetry transports | Conditional coverage is productive, but global selection remains missing |
| Independently reviewed analytical deduction | The retained 88-core family transports to full unit squares with fractional mass eleven at $L_{\ast}=38200/9977\approx3.82880625$ | Unconditional point measures and the specified density formulation cannot prove a bound above $L_{\ast}$ |
| Exact local negative evidence | T1 has a local low-surplus counterexample; H-161’s literal parent union adds no mass there | The existing local resource cannot supply the missing availability theorem |
| Reviewed analytical deduction | X-031 extends that literal failure to a sufficiently small admissible neighborhood | Subdividing the same local domain does not remove its obstruction |
| Registered but unmeasured | H-160/H-162 have no scientific target receipt | Their pause carries no scientific verdict; even success would leave local availability open |

The [results register](../../../packing/frontier/results.yaml),
[n11 record](../../../packing/frontier/n-011.md),
[X-027](../../../packing/campaign/explorations/X-027-stromquist-fractional-and-structural-strategy.md),
[X-030](../../../packing/campaign/explorations/X-030-n11-post-t1-proof-obligations-draft.md),
and
[X-031](../../../packing/campaign/explorations/X-031-bc303-floor-normalized-t2-helper-draft.md)
supply these claims and their scope.
T-026’s dilation-limit argument proves the ordinary exact lower bound; the absence of an
individual-side certificate at its limiting endpoint does not weaken that conclusion.

The point/density ceiling is stronger than a limitation of the current sites, symmetry
convention, or core shape.
Selecting a core inside each member of the full-unit fractional family cannot increase
its point depth. Thus changing an unconditional point-core selection rule cannot evade
the obstruction. A physical integrality gap at $L_{\ast}$ remains unproved because the
current physical lower bound lies below it.

A6 has a narrower scope: it obstructs its specified threshold catalog and core domain.
It does not obstruct every threshold, floor, compatibility, or conditional certificate.
Removing one returned support is also insufficient because a replacement optimum can
survive. The exact
[optimal-face criterion](../../../packing/campaign/explorations/X-027-stromquist-fractional-and-structural-strategy.md#alternate-atom-and-support-changes-test-the-whole-optimal-dual-face)
is the appropriate finite-program comparison.

New derivations below are identified as such.
They have explicit arguments but are not registered results or independently confirmed
target outcomes. Rankings and proposed success thresholds are research judgments.
The geometric-waste route is speculative.

## Ranked Routes

| Order | Route | Information From the First Proper Discriminator | Potential Payoff | Main Missing Prerequisite |
| --- | --- | --- | --- | --- |
| 1 | A: occupancy/contact decomposition | High if a complete difficult family closes or a precise surviving relaxation is exposed | A global $3.84$–`3.85` bound and reusable subconfiguration exclusions | A complete partition, physical transfer, and a checker for the chosen conditional language |
| 2 | S: proof compression | High relative to the amount of new machinery | A substantially shorter exact $3.82$ proof and reusable certificate templates | A mathematical complexity target beyond smaller serialization |
| 3 | B: pairwise SDP | High for choosing a proof mechanism | A global bound beyond the point relaxation and a transferable solver architecture | A sound complete pose cover and independently checkable SDP certificate |
| 4 | C: orientation structure | Moderate initially; high if a complete continuous interval closes | A contact-independent restricted-family theorem or a bridge to optimality | Complete separation branching over continuous angles |
| 5 | D: constructive search | Moderate after a proposer passes an oblique recovery control | A new upper bound or useful competing configurations | A proposer that reaches oblique structure and an honest endpoint-classification contract |

### Route A: Complete Occupancy or Contact Cases

The central issue is completeness.
Most useful BC303/T-023 premises are fixed at $q=96/25=3.84$: seven-of-eight mark
ownership, the resulting 80 incidence patterns, the selected owner patches, and the
availability products avoiding the two certified tuples.
They do not automatically hold at $3.85$.

One existing argument does extend.
Put

$$
\eta=\frac{\sqrt{1+2\sqrt2}}2.
$$

The wall-contact proof bounds the vertical separation of two unit-square centers
touching the same vertical wall below by $\eta$. Four such parents would require span at
least $3\eta>3.85-1$. Therefore at most three parents touch each wall at $3.85$.
Together with S1’s fixed-angle translation normal form, this gives a representative with
at most three physical contact components.
This extension is an analytical deduction from the
[retained wall and normalization proofs](../../../packing/campaign/explorations/X-027-stromquist-fractional-and-structural-strategy.md#wall-contact-gives-a-finite-component-restriction).
It supplies neither a useful complete contact skeleton nor a short prescribed path or an
orientation-class theorem.

There are two defensible first targets:

- Retain $3.84$, where the owner premises already exist, and close a complete family
  among the existing availability blockers.
- Retain $3.85$, but make the new ownership and capacity premises part of the entry
  contract. The $3.84$ objects then serve as controls.

The first is preferable if it avoids rebuilding the foundation.
A global $3.84$ theorem would advance the present bound by about $0.01355$ and establish
a physical fractional-packing gap.
The extra hundredth in the stretch target should not conceal the cost of new premises.

**First discriminator:** Freeze one complete residual domain that includes a known
difficult configuration.
Compare coupled geometry alone with that same geometry augmented by conditional
threshold or subset-capacity rows.
A useful adversarial control is the four simultaneous literal corner parents underlying
T1/H-161: the frozen local charges cannot exclude them, so a residual exclusion would
demonstrate additional information.
A result on the literal poses needs a positive-width domain proof before it becomes a
reusable case exclusion.

For selection-based work, let $\Gamma(P)$ be the valid owner selections in one physical
packing $P$, and let $G$ contain the completely excluded selections.
The global obligation remains

$$
\forall P,\qquad \Gamma(P)\cap G\ne\varnothing.
$$

Enlarging $G$ can simplify this theorem; it is not necessary to keep trying to prove the
particular two-label T1/T2 mechanism.
The retained reduction has sixteen maximal availability products, three physical D4
types, and ten types in S1’s fixed left/bottom chart.
These give a useful fixed denominator at $3.84$, with continuous geometry still to
decide. They are not a census of feasible packings.
[Selection analysis](../research/research-2026-09-12-n11-selection-routing-first-principles.md)

The proposed “fraction of cases closed” needs a fixed denominator.
Subdividing easy leaves can increase that fraction without eliminating another physical
possibility. Report closed original root families, the unchanged denominator, and the
exact worst surviving domain.
Each survivor should carry the required residual count and its best rigorously justified
capacity. Abstract case counts are not probabilities over physical packings.

**Continue** when a complete difficult family closes, or a uniform geometric inequality
removes a relaxation witness that survives the matched baseline.
**Park the tested representation** when an exact admissible obstruction survives all its
resources and further subdivision repeats that obstruction.
A timeout supplies cost evidence and a remaining domain, not a refutation of A.

The capacity machinery can transfer to $n=12,17,18,20$. The n11 marks, owner selections,
and counting constants cannot be transferred without new proofs.

### Route S: Compress the Existing Proof

Start with T-025, whose budget margin is much larger than T-026’s. Measure compression
in orbit representatives, coordinate parameters, distinct weights, and coverage
templates. T-025 already has 79 point orbits and 40 threshold orbits: 119 independent
orbit representatives expanded to 904 atoms.
Its two per-direction minimum-charge values do not establish that there are only two
geometric tight-cell templates; near-equal values can result from optimization and
rationalization.
[T-025 proof](../../../packing/cases/n11_threshold_certificate/t-025-threshold-certificate-proof.md)

A useful analytical baseline follows immediately from the retained theorem.
Every atom has budget coefficient one.
Round each weight upward to the nearest multiple of $1/30000$. This preserves D4
symmetry and weakly increases every core charge.
The new budget $M'$ satisfies

$$
M'
<
\frac{685457679}{62500000}+\frac{904}{30000}
=
\frac{2062023037}{187500000}
<11.
$$

Thus weight-denominator simplification at $3.82$ is guaranteed.
This is a proved recipe from T-025’s premises, not a produced or replayed certificate.
The research question is how far the support and geometry can be simplified.

**First discriminator:** Group atoms by D4 orbit, weight, and tight-cell incidence, then
test one frozen sparse or quantized template family with counterexample-guided row
addition.
Numerical optimization proposes weights; the existing complete coverage checker
decides the candidate.
Moving sites requires full verification: coordinate rounding lacks the monotonicity
guarantee of rounding weights upward.

A proposed success threshold is a fivefold reduction in orbit representatives, or a
comparable reduction in independent geometric parameters, together with a short
generating rule and the unchanged $3.82$ conclusion.
The threshold is a planning choice, not a forecast.
Smaller JSON, simpler denominators, or deleted coefficients alone would not complete the
proof-simplification objective.

**Continue** when a reduced family survives the complete exact coverage and budget
replay and its description explains a recurring geometric mechanism.
**Park the selected family** after an exact infeasibility certificate or retained
counterexample cells establish why it cannot meet the frozen target.
Such a negative does not exclude every simple proof.

A compact motif explaining the two-of-three rule could transfer to other $n$. The
compression instrument itself can test all retained certificates.
These are mathematical uses beyond making one file faster to verify.

### Route B: Pairwise Semidefinite Relaxation

The $n=6$ control must separate soundness, strength, and mechanism.
At side $3$, the model must preserve a known six-square packing, including legal
contacts. A maximum-occupancy pose graph should also preserve the nine-square grid at
that side. At a rational side below $3$, a complete certified exclusion is a valid
negative control.

The theorem $s(6)=3$ does not establish that a point LP fails below three.
The corresponding fractional-gap question remains open in the retained analysis.
If the matching LP already excludes six, an SDP success validates the implementation but
does not demonstrate added strength.
[The n6 control boundary](../../../packing/campaign/explorations/X-027-stromquist-fractional-and-structural-strategy.md#6-parked-questions-with-reasons-to-reopen-them)

A sound finite conflict graph requires:

1. A cover of every contained parent pose.
2. A consistent assignment when cells overlap.
3. A proved capacity-one condition for each binary occupancy cell.
4. An edge only when every pair of parent poses in those two cells overlaps in its
   interiors.
5. Symmetry acting on the whole packing and its cells.

There is a simple capacity-one construction.
A spatial center tile of diameter strictly below one cannot contain two centers of unit
squares: their inscribed radius-`1/2` disks would overlap.
All angle cells over that tile share one occupancy budget.
This is a sound starting point, not a guarantee of useful conflict density.
The
[hybrid strategy review](review-2026-09-07-n11-hybrid-strategy.md#bottom-up-resources-capacities-and-anchor-correlations)
already distinguishes pose-cell capacities from ordinary point resources.

For a conflict graph $G$, the explicitly defined relaxation

$$
\max \langle J,X\rangle,\qquad
\operatorname{tr}X=1,\quad X\succeq0,\quad X\ge0,\quad
X_{ij}=0\quad\text{for }ij\in E(G)
$$

bounds its independence number from above.
Here $J$ is the all-ones matrix, $X\ge0$ is entrywise nonnegativity, and $X\succeq0$
means positive semidefiniteness.
An independent set $S$ of size $k$ gives the feasible matrix
$X=\mathbf1_S\mathbf1_S^{\mathsf T}/k$, with objective $k$. This argument fixes the
graph/complement convention directly.
A moment formulation is preferable when including resource and grouped-occupancy
constraints.

The n11 comparison should include the threshold-enhanced LP baseline.
A two-of-three threshold already supplies a continuous clique-type capacity: two
disjoint charged cores cannot consume disjoint pairs from three sites.
B therefore has to add relationships beyond the current threshold catalog, such as odd
cycles, larger subset structure, or correlations retained in the moment matrix.

**First discriminator:** Before a full pose graph, inspect the retained exact
obstruction’s conflict structure and compare edge, clique/odd-cycle, threshold, and SDP
bounds on that same finite support.
This is a mechanism screen.
Its successful bound applies only to the support and cannot replace complete pose
coverage. For added linear capacities, test the whole old optimal dual face.
For a moment relaxation, ask whether any old optimum admits a feasible moment extension;
rejecting the solver’s one returned vector is weaker.

The control-first execution in agenda 036 should follow this formulation audit.
**Continue** when a sound control shows a certified improvement over the strongest
matched LP and a complete-cover refinement remains affordable.
**Park the chosen graph and relaxation** when it retains the target count at the frozen
resolution and the next refinement exceeds the declared allowance.
This is a bounded model failure.
Numerical SDP infeasibility alone is not a certificate: the dual inequalities and
positive semidefiniteness need exact or rigorous interval verification.

B transfers broadly.
Convergence of a hierarchy in principle, however, supplies no evidence that an
affordable level will settle eleven.

### Route C: Orientation Structure

Three different statements must remain separate:

- [H-112](../../../packing/campaign/hypotheses/H-112-six-axis-five-common-angle-optimum.md):
  six axis-aligned squares and five sharing one arbitrary actual angle, with every
  center and contact arrangement allowed.
- [H-113](../../../packing/campaign/hypotheses/H-113-at-most-two-angle-optimum.md): all
  multiplicities with at most two actual orientations, both absolute angles free.
- [H-117](../../../packing/campaign/hypotheses/H-117-forced-angle-complexity.md) and its
  narrower representative questions: some minimizing representative belongs to a
  restricted orientation family.

Only the last bridge connects a complete restricted-family theorem to unrestricted
optimality. H-112 does not imply H-113. An arbitrary first angle cannot be rotated to
zero while preserving the square container.

There is a quantitative problem with one-degree bins near $3.87$. Suppose a bin is
handled by snapping to its midpoint and uniformly shrinking, and suppose the whole
midpoint family has lower bound $U$, Trump’s side.
For half-width $\delta$, every strict shrink $B<1/(\cos\delta+\sin\delta)$ transfers the
hypothetical packing to that fixed-angle family after rescaling.
Letting $B$ increase to its limit gives only

$$
L\ge \frac{U}{\cos\delta+\sin\delta}.
$$

At $\delta=0.5^\circ$, this is approximately $3.8437$, below $3.87$. Reaching $3.87$ by
this transfer would require half-width roughly $0.105^\circ$, even under the favorable
complete-family premise.
This is an analytical loss estimate, not a measurement of an interval solver.
One-degree bins need direct coupled interval geometry or a stronger mixed-size argument.

**First discriminator:** Reproduce the exact Trump-angle control, then prove a complete
positive-width angle interval at a rational target such as $3.87$, retaining all
separation alternatives.
Re-solving Trump’s retained cell is a control, not new restricted-family progress.

**Continue** when a full interval closes with reusable Farkas or interval certificates
and the surviving disjunctions remain manageable.
**Park the current enumeration** when the first complete interval exposes an
uncontrolled branching problem.
A verified three-angle packing challenges a universal restriction on all packings, but
does not alone refute an existential two-angle minimizing representative.

The $n=6$ optimal family with an angular rattler is an adversarial control against
informal arguments that optimality or crowding forces few angles.
[Few-angle analysis](review-2026-09-07-n11-hybrid-strategy.md#what-few-angles-would-require)

### Route D: Constructive Search

A hundredfold budget increase should follow a test that separates proposal failure from
verification success.
Replaying Trump’s supplied coordinates tests verification.
Recovering Trump from perturbed or independently generated starts tests the proposer.
The retained five-seed n11 and n17 failures show that the stock machinery has not
demonstrated reliable access to the required oblique structure.
[Search controls](../../../TUTORIAL.md#calibration-must-match-mechanism-not-just-difficulty)

**First discriminator:** Compare one changed proposal mechanism with the stock control
at equal pair-test work.
Existing candidates include inflation continuation, angle-profile-organized search,
coordinated contact release, and neighbor transfer.
A successful recovery ladder would justify a larger campaign.
A multiplier of an earlier wall-clock allowance is not an equivalent scientific-work
budget.

The endpoint contract also needs precision.
Exact polishing establishes a valid packing only after the walls and all pairs pass
verification; a contact-equation root alone is insufficient.
Neither exact polishing nor rigidity by itself establishes side optimality.
Retain competing valid packings, and call them local optima only when the corresponding
local statement is certified.
The
[tutorial’s contact and promotion discussion](../../../TUTORIAL.md#contact-graphs-stationary-branches-and-rattlers)
sets these boundaries.

**Continue** after the proposer reaches an oblique control within the declared work
budget, or finds a verified competing family that answers a structural question.
**Park or replace the proposer** when its matched recovery control fails.
A verified sub-Trump packing changes the upper bound immediately; a negative finite
search changes no lower bound.

D can search productively before a global terminal-component theory is complete.
It must report pose keys, contact signatures, and unresolved families as those objects,
not as a component census.
Another oblique case such as n17 is a stronger transfer control than only the $45^\circ$
n5/n10 constructions.

## Additional Mathematical Routes

The additional routes are candidates for W10, not new registered hypotheses.
Across the enlarged portfolio, the advisory decision order is **A, S, angular resources,
B, stronger charge algebra, geometry-dependent budgets, n12, C, D, then geometric
waste**. This order balances readiness and the information in the first complete
discriminator; it is not a ranking of theorem importance or a measured probability of
success.

| Priority | Route | Why It Sits Here |
| ---: | --- | --- |
| 1 | A: occupancy/contact decomposition | Strongest path to a material n11 lower bound; its $3.84$ premises and a complete root family must be frozen first |
| 1 | S: proof compression | Best bounded deliverable with admitted tools; it can substantially simplify the exact $3.82$ proof |
| 1 | E: global angular resources | Cheap optimal-face screen using existing H-131 caps; admission and coherent selection are the main costs |
| 1 | B: pairwise SDP | Strong alternative mechanism, but it must first earn sound discretization and exact-certificate machinery |
| 2 | F1: stronger charge algebra | Changes the obstructed relaxation; begin with an exact realizable-trace domination test |
| 2 | F2: geometry-dependent budgets | Uses a physical joint-parent theorem to lower one atom budget; keep it separate from charge-language expressiveness |
| 2 | N: n12 exact-value program | A larger possible theorem with weak present readiness; require a uniform lemma rather than a decimal ladder |
| 2 | C: orientation structure | Potential structural bridge, but a complete positive-width interval and an unrestricted-optimality bridge are both missing |
| 3 | D: constructive search | Run separately after the proposer, rather than only the verifier, recovers an oblique control |
| 3 | G: geometric waste | Genuinely distinct but speculative, with no admitted global accounting tool yet |

### Global Angular-Resource Certificates

This develops X-027’s mixed-profile proposal into a global resource question.
H-131’s larger-side certificates were run at $3877084/10^6$, above $3.85$, so three of
their capacities remain valid at $3.85$ by embedding: at most nine squares in cells
0–24, at most ten in 0–29, and at most ten in 175–180.
[H-131](../../../packing/campaign/hypotheses/H-131-near-axis-counts-at-q.md)

For a coherent selection on that same admitted net, let $(Q,C,j)$ be an equipped parent,
its strict core, and its selected folded source index.
Put

$$
f_J(Q,C,j)=\mathbf1_{\lbrace j\in J\rbrace}.
$$

If $j\in J$, the parent’s folded angle belongs to the union of the corresponding
physical source cells.
A proved physical count cap $k_J$ therefore gives

$$
\sum_i f_J(Q_i,C_i,j_i)\le k_J.
$$

This is an analytical interpretation of the existing count theorem as a resource budget.
It is valid on equipped physical packings, not on every arbitrary disjoint family of
cores.
That distinction and the coherent selection rule must be admitted by any consuming
certificate checker.

These resources can be combined with point and threshold atoms.
Equivalently, refine overlapping bands into a common disjoint angle partition, retaining
its seams under the selection convention, and optimize against every integer count
profile satisfying the caps:

$$
M<\min_{n\in\mathcal N}\sum_jn_jd_j.
$$

Here $\mathcal N$ contains every possible physical profile, $d_j$ is a certified
per-class charge lower bound, and $M$ is the one combined resource budget.
Testing only $(9,2)$ from a premise $n_0\le9$ is justified only when the demand ordering
makes that profile worst.
This route needs neither a two-orientation theorem nor an owner-selection theorem.

**First discriminator:** Check whether the retained fractional optimal face survives the
valid angular capacities before a large synthesis run.
Then compare complete class coverage on one common row and atom manifest.
**Continue** if integer count information removes an optimum retained by the strongest
matched charge baseline.
**Park the selected profile/cap family** if an exact old optimum satisfies it.
New angle bands, improved count theorems, and different charges remain separate
questions. The resource construction transfers wherever an independently proved
angle-count theorem is available.

### Stronger Charge Algebra and Geometry-Dependent Budgets

This section contains two execution candidates with related motivation but different
owners and proof obligations.
Weighted motifs, genuinely multilevel floor atoms, and higher-rank floor compositions
form the stronger-charge candidate; a physical joint-parent budget theorem forms the
geometry-dependent candidate.
The seven-token threshold-four motif has no multilevel floor behavior.
X-027’s five-site factor-`5/4` separation concerns domination of a demand profile, not
an improved unit-demand square-cover budget.
[Charge mechanisms](../../../packing/campaign/explorations/X-027-stromquist-fractional-and-structural-strategy.md#weighted-binary-atoms-and-floor-atoms-ask-different-questions)

**First discriminator:** Freeze one geometrically realizable trace universe and compare
a candidate charge with all ordinary threshold atoms on the same sites.
A strict exact domination gap justifies a larger support/atom comparison.
The full covering program must then remove the whole old optimal face and pass
continuous-domain coverage; a useful cut on one support is not enough.

A separate geometric test can start from an atom with ordinary budget at least two.
Prove that two simultaneous physical parents cannot both trigger it in the declared
domain. That would lower the atom’s budget through a geometric theorem rather than
through token counting.
[Proposed geometric-budget test](../../../packing/campaign/explorations/X-030-n11-post-t1-proof-obligations-draft.md#other-routes-to-an-improved-bound)

**Continue** after an exact trace separation or a complete joint-parent capacity
reduction with a defined evaluator.
**Park the motif** if an ordinary mixture dominates it on every realizable trace;
**reject the proposed budget-one reduction** if an actual simultaneous parent pair
triggers both copies.
Neither outcome closes the broader charge language.

The counting rules transfer across $n$, but their local motifs and containment
assumptions need new validation.
This route has higher potential than another fixed-weight net refinement because it
changes the relaxation responsible for the obstruction.

### An n12 Exact-Value Program

The next open case has $3.96\le s(12)\le4$. Proving $s(12)=4$ would resolve a case,
which is a larger mathematical outcome than another small decimal advance at eleven.
The integer endpoint alone is not evidence of a cheaper proof.
The retained record includes flexible grid configurations and does not classify the
optimal set. [n12 record](../../../packing/frontier/n-012.md)

A fixed-shrink point certificate cannot reach four.
A parameterized family approaching four remains logically possible, but its existence is
unproved.
The reports at $3.97$–`3.99` do not establish a universal n12 ceiling: some are
finite-site failures, and the historical cutting floor lacks its replayable generating
family. They cannot justify a limiting-value extrapolation.
[Covering-value evidence](../../../packing/frontier/CERTIFICATE-REACH.md)

**First discriminator:** Seek one uniform boundary-capacity or deformation lemma for
$L=4-\varepsilon$, covering an interval of $\varepsilon$, with n6 and n13 as solved
controls. The output should be a stable finite case reduction or an exact parameterized
inequality, rather than a ladder of decimal sides.

**Continue** when the lemma handles a full family, including the relevant side-four
flexible configurations and its boundary strata.
**Park the mechanism** when a legal flex or degeneration defeats its claimed uniformity.
Numerical returns to the grid do not supply that missing proof.
The approach could transfer to other open integer endpoints, such as n20 and n21, after
their boundary mechanisms are identified.

### Geometric Waste Accounting

This is a speculative independent line.
Assign uncovered area or boundary loss to local arrangements of two or three parents,
retaining their relative orientations.
Seek a lower bound on unavoidable empty area that contradicts $L^2-11$. An unconditional
one-body density reformulation cannot work above $L_{\ast}$; a useful version must
preserve shared geometric information.

**First discriminator:** Derive one exact local gap lemma, calibrate it against Trump
and the n6 angular-rattler family, then give an accounting rule that sums it over a
complete contact or boundary decomposition without double counting.

**Continue** only when both the uniform local deficit and its global accounting rule are
proved on a named domain.
**Park the candidate** if a legal contact degeneration makes the claimed deficit
arbitrarily small or if the sum counts the same empty region repeatedly.
This route has less direct tooling support than A, B, or the charge-algebra route, and
no measured advantage in the retained record.

## Transfer to Other Small n

n6 is the most useful proof control, and n17 is a useful oblique-search control.
The open cases n18–n21 and n26 offer more numerical room for stronger certificate
languages, but headroom is not an attainability estimate.
n18 already has finite-site plateaus at $4.68$, and n20 has measured failures above the
$4.85$ certificate.
Any transfer should begin with a frozen comparison rather than assume
that eleven’s successful motif scales.

The frontier’s reported and verified upper bounds must remain separate, especially at
n17. Formalizing a reported construction can be useful, but it is a different payoff
from finding a better packing.
[Current frontier](../../../packing/frontier/STATUS.md),
[certificate reach and evidence qualifications](../../../packing/frontier/CERTIFICATE-REACH.md)

## W10 Decision Frame

W10 should select one execution entry after reconstructing the efficiency-checkpoint
cadence. A due W5 checkpoint is an operational prerequisite to price from actual
receipts; administrative work does not reset that cadence.
This audit supplies the mathematical ranking, not a finding that the checkpoint is or is
not due.
[Agenda 036](../../../packing/campaign/agendas/agenda-036-n11-strategy-reset-roadmap.md)

For each candidate, the decision record should name:

1. The mathematical payoff: a complete $3.84$ or $3.85$ exclusion, a substantially
   simpler $3.82$ proof, a defined structural theorem, or a verified upper bound.
2. The exact domain and imported premises, including which survive at the proposed
   target side.
3. The matched control and the information the treatment adds.
4. The smallest complete discriminator, its independent replay, and its scientific work
   and wall-clock allowances.
5. The precise continue, bounded-negative, partial, invalid, and timeout meanings.
6. The terminal artifact that permits the following block to be selected.

The recommended scientific choice is one complete A discriminator at $3.84$, or at
$3.85$ after its new premises are stated.
Select S instead if A still requires a general conditional-proof framework before any
complete case can be tested.
B should earn its formulation through the matched controls above.
The angular-resource proposal is a useful additional candidate when its existing count
theorems can be consumed without a larger admission project.

Keep BC329 and the unchanged local BC303 helper targets paused under the current payoff
policy. Their remaining questions are real, but their present implication chains do not
match the requested outcome.
The W10 record should explicitly continue, pause, or stop the unselected routes, update
the handoff and active plan together, and select exactly one next block rather than
promise simultaneous execution of the portfolio.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
