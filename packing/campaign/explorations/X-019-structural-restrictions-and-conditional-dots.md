---
title: X-019 — structural restrictions and conditional dots at n11
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-019
  title: Structural Restrictions and Conditional Dots at n11
  date: '2026-09-07'
  author: Codex coordinator, with three independent planning reviews
  campaign: packing.squares
  brief: >-
    Assess whether provable corner, contact and orientation restrictions can make
    conditional weighted-dot proofs substantially stronger at n11. Reconcile the
    previous explorations and results, identify competing preliminary spikes, and
    prepare three successive two-to-four-hour blocks for other research agents.
    This is planning only, based on PR116; no research spike is launched.
  sources:
  - packing/campaign/explorations/X-014-closing-from-both-ends.md
  - packing/campaign/explorations/X-016-after-381-two-managers-one-proof-boundary.md
  - packing/campaign/explorations/X-017-compatibility-and-complete-case-covers.md
  - packing/campaign/explorations/X-018-hybrid-strength-and-angular-release.md
  - docs/project/reviews/review-2026-09-07-n11-hybrid-strategy.md
  - docs/project/reviews/review-2026-09-07-research-throughput-and-timeboxes.md
  - packing/frontier/n-011.md
  - packing/frontier/n-012.md
  - packing/campaign/hypotheses/H-063-n11-class-certificate.md
  - packing/src/sqpack/fractional/classcert.py
  - https://github.com/jlevy/squares/blob/0701287c096dfce05a0164e3ca56f7088ea3756a/docs/project/reviews/review-2026-09-07-upstream-research-reconciliation.md
  proposes: [H-126]
---
# X-019 — Structural Restrictions and Conditional Dots at n11

**Seek geometric restrictions that a counting proof can actually use.** Start from four
distinct corner blockers, a global consequence of the existing twelve-square bound, and
investigate what their positions and angles force on the other seven squares.
In parallel, test weaker angle-count restrictions and conditional dot certificates.
A two-angle normal form would be powerful, but useful progress need not wait for that
theorem.

[Agenda 029](../agendas/agenda-029-structural-restrictions-and-conditional-dots.md)
contains the assignments, selection rules and copyable handoff.
It is paused: this document codifies the discussion and reviews existing arguments; its
proposed spikes have not begun.
The nominal allocation is eight hours in blocks of three, three and two hours, each
within the requested two-to-four-hour range.

The immediate numerical objective is a global exclusion at $q=96/25=3.84$. The retained
bracket is $3.810025723614703\ldots\le s(11)\le U=3.877083590022814\ldots$; reaching
$3.84$ would remove about 45% of this remaining gap.
That is an objective, not a prediction of what one night can prove.
[T-022](../../cases/n11_fractional_certificate/t-022-dilation-limit-proof.md) is a
weak-limit lower bound, not an endpoint no-fit certificate.

## What Would Move the Argument Forward

The intended chain is:

1. Prove a restriction satisfied by every relevant packing, or by at least one global
   minimizing representative.
   Alternatively, partition all possibilities and retain every branch.
2. Use that information to restrict admissible poses, force class counts, or prove joint
   capture by several squares.
3. Construct and independently verify a weighted-dot contradiction on the resulting
   domain.
4. Account for every remaining domain before claiming a global bound.

These steps can reinforce one another.
A certificate excluding a complete angle-count class strengthens the restrictions on the
surviving classes. A geometric lemma may then make the next conditional certificate
possible. An excluded class can be removed only from a parent whose coverage is proved.

The next blocks should earn at least one consequential intermediate result: a useful
global structural inequality; a continuous conditional exclusion with its complement
stated; or a verified counterexample that eliminates a proposed restriction.
A new descriptor catalogue, an accepted interface, or repeated recovery of Trump’s shape
is preparation rather than that result.

## A Global Starting Point: Four Distinct Corner Blockers

The following is an elementary deduction from the existing certified bounds, included
with its proof for review.
It is not a new frontier claim or experimental result.

Let eleven unit squares pack into $[0,L]^2$, where $3.810025723614703\ldots\le L\le U$.
The same argument applies directly at $L=q$. The
[T-017 certificate](../../frontier/n-012.md) rules out twelve squares at $3.96$.
Consequently **every contained unit-square probe overlaps the interior of an existing
square**. Otherwise that probe could be inserted as a twelfth square; mere boundary
touching would permit insertion.

Apply this fact to the four axis-aligned unit squares placed in the container corners.
The coordinate gap between opposing corner boxes is $L-2>\sqrt2$. Every unit square has
horizontal and vertical spans at most $\sqrt2$, so it cannot meet the interiors of two
different corner boxes.
We may therefore select four distinct existing squares, one blocker for each corner,
leaving seven other squares.

This gives a global four-plus-seven description with **all eleven angles still free**. A
corner box may have several blockers; the selected blocker need not touch a wall, be
axis-aligned, or approach the actual corner closely.
The remaining seven need not be central and may also meet corner boxes.
A complete parameterization must allow all these possibilities and all valid blocker
selections, or justify a canonical selection with ties covered.

Insertion saturation also applies to other contained unit probes.
A finite selection of probes might force useful capture patterns or compatibility
inequalities, in the spirit of unavoidable-point proofs.
Overlap with several probes alone is not a capacity bound; the missing implication must
be proved geometrically.
This structural question is registered as
[H-126](../hypotheses/H-126-insertion-saturation-corner-structure.md).

### What Corner Penetration Would Buy

For a unit square in the quadrant $x,y\ge0$, reduce its orientation modulo $\pi/2$ to
$\theta\in[-\pi/4,\pi/4]$ and set $\phi=|\theta|$. With center $(a,b)$, coordinate
half-width $h=(\cos\theta+|\sin\theta|)/2$, and wall gaps $g_x=a-h$, $g_y=b-h$,
containment gives $g_x,g_y\ge0$. The exact identity is

$$
\min_{p\in Q}(x+y)
=a+b-\cos\theta
=g_x+g_y+\sin\phi.
$$

Thus meeting the closed corner triangle $x+y\le\varepsilon$ forces

$$
g_x+g_y+\sin\phi\le\varepsilon,
\qquad \phi\le\arcsin\varepsilon.
$$

For $0\le\varepsilon<1/\sqrt2$, at most one packed square can meet this triangle.
Indeed its center lies in $a,b\ge1/2$, $a+b\le1+\varepsilon$, a triangle of diameter
$\sqrt2\varepsilon<1$. Two such centers would make their open radius-$1/2$ incircles
overlap. Occupants of different corner triangles are distinct whenever
$L-2\varepsilon>\sqrt2$, as throughout the relevant range.

The missing global premise is **occupation of useful small triangles, or a useful
constraint on the alternatives that avoid them**. Blocking a unit corner box only
ensures some intersection with $x+y<2$, which gives no useful angular restriction.
A $45^\circ$ square snug against both walls blocks that box while avoiding every such
triangle with $\varepsilon<1/\sqrt2$. An unoccupied corner also supplies no uniform
empty margin: squares may approach it arbitrarily closely.

Containing the exact corner forces $g_x=g_y=\phi=0$ and the flush square $[0,1]^2$.
Trump’s recorded packing occupies only three exact container corners.
That defeats a four-corner premise for all competitive packings; since global optimality
is unproved, it does not refute the existence of some four-corner minimizing
representative. A restriction confined to sides below $q$ likewise needs its own
argument.

## The Counting Proof to Feed

[X-014, Lemmas 2 and 3](X-014-closing-from-both-ends.md#branching-is-chunking-conditional-certificates)
already formulate conditional and class-dependent certificates.
The new contribution sought here is useful geometric premises and their complete
coverage, rather than the counting principle itself.

For a case $\lambda$, take one nonnegative measure $\mu_\lambda$ of total mass
$M_\lambda$. Let the types partition the eleven squares.
Suppose the case has $m_j$ squares of type $j$, and every such square captures at least
$a_j(\lambda)$ under a convention that makes the captured sets pairwise disjoint.
Then

$$
\sum_j m_j a_j(\lambda)\le M_\lambda.
$$

A strict reverse inequality excludes the case.
For a selected corner frame it could take the form
$a_{\mathrm{frame}}(\lambda)+7b(\lambda)>M_\lambda$, where $a_{\mathrm{frame}}$ bounds
the combined capture of the four selected blockers uniformly throughout the case.
For six axis squares and five with one common angle it could be
$6a_0(\theta)+5a_\theta(\theta)>M(\theta)$. These are examples of the implication, not
certificates we have obtained.

The quantifier is: **for every case, there exists a measure valid uniformly throughout
that case**. Measures can differ between cases.
A measure depending on a continuous anchor parameter needs a verified argument covering
every value of that parameter.
The theorem need not find one measure that works over all cases simultaneously.

Five distinctions determine whether geometry actually strengthens the certificate:

- Use strict interior capture or the existing safe witness cores.
  Atomic dots on shared boundaries can otherwise be counted twice when squares legally
  touch. A region common to the full anchor squares is not automatically inside every
  anchor witness core.
- Keep one common mass budget for the capture sum.
  Giving each square its own measure does not justify charging all eleven against one
  measure’s mass.
- For an anchor box, the union of residual pose domains over all anchors is a safe
  relaxation; replacing it by the midpoint domain is not.
  The union loses common anchor correlations, so a feasible relaxation point need not
  describe a packing.
- Pair compatibility or contact information strengthens a unary covering program only
  when it reduces allowed poses or yields class counts.
  A genuinely joint capture claim needs a joint geometric lemma or verification.
  Reuse H-119 only for its specific comparison of joint and sharp independent minima on
  the same box.
- Fixed angles plus a complete choice of SAT separation alternatives give an exact
  translation LP. A sound resource argument cannot contradict an actually feasible
  complete LP. Gains can come from angle/disjunction relaxations, missing compatibility,
  or proof cost; distinguish these from stronger mathematics.

### When Asymmetric Dots Help

For an unrestricted, fully D4-invariant covering problem whose admissible measure family
is closed under D4 averaging, that averaging preserves mass and coverage.
A D4-closed site set with unrestricted nonnegative weights suffices; a bound on the
number of supported sites need not survive averaging.
Asymmetry by itself therefore gives no better optimum in that setting.

A selected corner frame or labeled count case can break that invariance.
Use asymmetric measures there, average only over a subgroup preserving the entire case
and its type labels, or transport a certificate to symmetry-related cases.
The existing folded D4 class solver is not automatically a verifier for an asymmetric
anchor domain. A general oriented case needs a full quarter-turn domain unless a smaller
one is justified. Independently reflecting individual square angles can change
compatibility.

## Weaker Restrictions Before a Two-Angle Theorem

**Composition is already constrained in one direction.** The nine-point argument in
X-014 bounds the number of sufficiently near-axis squares by nine; it forces at least
two tilted squares, rather than at most a few.
At $q=96/25$, the explicit band $|\tan\theta|\le1/24$ is a valid example: the contained
axis-aligned core has side at least $\sqrt{577}/25>q/4$. Each such core contains at
least one of the nine quarter-pitch grid points strictly in its interior, which is
enough for the counting argument.
For the existing finite-net implementation, use whole half-gap cells contained in the
proved band; an arbitrary angular cut can misclassify a witness core.

This suggests a complete split by near-axis count $n_0=0,\ldots,9$ and its complementary
angle class. The cases with zero or one tilted square are already gone.
Further bins can distinguish intermediate from near-diagonal angles, provided the whole
complement and cell boundaries survive.
This requires no assumed shared angle.
Existing two-band localization results can assist only where their premises hold.

**Positive-length edge contacts propagate orientation.** Form a graph with eleven square
vertices and one wall vertex.
Join squares only when they share a positive-length edge segment; join a square to the
wall vertex only for a flush positive-length wall edge.
Each square-square edge equates orientations modulo $\pi/2$, and every wall-connected
square is axis-aligned.
With $k$ unanchored components there are at most $k$ independent nonaxis angles.
Forcing many wall-connected squares, or few unanchored components, would therefore be a
useful intermediate theorem.

Ordinary point contacts and generic adjacency do not have this implication.
The
[PR108 review](../../../docs/project/reviews/review-2026-09-07-n11-hybrid-strategy.md)
gives Trump’s rank-ten graph as a control and an optimal $n=6$ angular rattler as a
warning against general claims about every optimum.
The ordinary contact-component spanning argument also supplies no flush-edge count.

[H-121](../hypotheses/H-121-axis-plus-one-minimizer.md) asks whether **some** global
minimizer has an axis-plus-one-angle representative.
A sufficient ambitious route is to choose a minimizer with the fewest nonaxis angles and
prove a finite feasible, nonincreasing-side motion eliminating one when two or more
remain. The path must cover releases, new contacts and degeneracies.
Infinitesimal flexes, torque balance, sparse stress or repeated numerical alignment do
not establish that path.

Keep [H-117](../hypotheses/H-117-forced-angle-complexity.md) for broader
angle-complexity questions.
An arbitrary two-angle family retains **both absolute angles**: the square container
cannot be rotated continuously to make one angle zero.
Even H-121 plus the six-plus-five H-112 theorem would leave other multiplicities open.
Quantitative angle bands or a clustered/dispersed split may pay sooner, but both
branches must be addressed.

## How the Earlier Work Fits

The mathematical survey used PR116 at `394451a4`; the planning branch also includes its
owner’s `e2655fe8` integration, including main’s PR111 atlas expansion.
PR110’s published `0701287c` contains additional X-018 results; those are reviewed below
as separate-branch evidence, not silently treated as files or gates on this branch.
Incorporating this plan does not merge PR110; later parent updates retain their owner’s
integration record.

| Earlier explorations | What carries forward | What they do not supply |
| --- | --- | --- |
| X-001–X-002: search philosophy and creative frontier | Proof/search separation and fixed-cell LPs | Search recurrence is not a universal structural restriction |
| X-003 and X-008: chunks and axis-aligned residue | Contact components and explicit grammar audits | An aligned component need not be a bar, L or rectangle; a construction grammar is not a complete normal form |
| X-004 and X-009: exact promotion and reachable construction families | Reliable witnesses and case-specific geometry | An upper-bound packing does not force the contacts of every competitor |
| X-005–X-007 and X-012: identity, flex and local closure | Exact local arguments and careful treatment of connected families | A contact signature, local rigidity or infinitesimal motion is not a global classification |
| X-010–X-011: lanes and controls | Controls must transfer to a target question | Readiness and repeated controls are not the desired mathematical output |
| X-013: next certificate directions | Successful weighted dots and witness-shrink limits | One witness language’s ceiling is not a barrier to all measures |
| X-014: closing from both ends | The conditional and class certificate theorems used here | Geometric anchor-domain conditioning is not implemented merely because class thresholds exist |
| X-015–X-016: portfolio and post-3.81 proof boundaries | Global/local separation, complete capture and restricted-family questions | Historical priority rankings do not fund fresh runs |
| X-017: compatibility and complete covers | H-111 global anchor goal, H-112/H-113 restricted families, H-117 global bridge | A complete anchor cover and a global angle theorem remain open |
| X-018: hybrid strength and angular release | H-118 fair comparisons, H-119 shared anchors, H-121 representative question | Guarded release families are not all packings or the new four-blocker frame |

All eighteen reports remain in this directory; their reasoning is retained rather than
rewritten into another archive.
The present plan selects from them as follows.

| Result or attempt | Evidence status and implication for this direction |
| --- | --- |
| T-017, T-018 and T-022 | Verified lower-bound inputs. They justify insertion saturation and fix the starting bracket; this plan changes neither bound. |
| [exp-064](../series/series-000-smoke-and-calibration/experiments/exp-064-h-063-two-threshold-class-program.md) | Its frozen shrunken-core/two-end-cell program was refuted at its stated target. With $B=0.9977$, eleven such cores already fit there by the exact axis/diagonal construction. Class conditioning showed some benefit, but this was no global improvement. Check headroom at the new target before running a successor; do not reopen H-063 unchanged. |
| [H-106](../hypotheses/H-106-continuous-near-axis-ten-point-cover.md), [H-123](../hypotheses/H-123-near45-coordinate-localization.md) and [H-124](../hypotheses/H-124-full-distinguished-square-compatibility.md) | Near-axis coverage and near-45 localization are accepted under their precise premises. The full-square diagonal compatibility cover passed; axis compatibility returned `no_chain` and remains unresolved. Neither establishes a global two-band world. |
| H-110 / exp-121 and H-122 / exp-122 | The accepted P12 escape refuted the unconditional near-axis twelve-point cover; a separate exact square refuted H-122’s diamond-conditioned cover. Preserve the full distinguished square when weaker common obstacles lose essential geometry. |
| H-099 / exp-128 | Exact optimum eleven on the fixed Trump-D4 support. This is a support-specific negative, not a theorem against conditional dots or every density. |
| X-018 results on PR110 | Guarded central-band capacity and signed release exclusions are accepted in their stated domains. Disk/octagon controls defeated weaker capacity shortcuts. BC282 gives an exact ten-square translation/fiber reduction, but no fiber was covered and no feasible skeleton was established. All remain conditional on their wall/angle setup. |
| Scalar and kernel attempts | exp-116 was unconverged; H-107’s adapter was deferred. PR116 proves a cubic feature obstruction, while H-125’s richer-family scientific discriminator was never invoked. Unrun questions and time limits are not mathematical refutations. |

The PR110 outcomes and their limitations are retained in its immutable
[strategy reconciliation](https://github.com/jlevy/squares/blob/0701287c096dfce05a0164e3ca56f7088ea3756a/docs/project/reviews/review-2026-09-07-upstream-research-reconciliation.md)
and
[BC282 admission](https://github.com/jlevy/squares/blob/0701287c096dfce05a0164e3ca56f7088ea3756a/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-028/bc-282-residual-skeleton-admission.md).
Their preassigned six-axis frame cannot be identified with the globally selected four
corner blockers without an additional theorem.

## Preliminary Spikes and Their Payoffs

The first three are complementary initial assignments.
The fourth is an ambitious replacement or later lead, with one available worker slot
rather than an additional parallel build.
A worker may propose a different mechanism if it states a sharper consequence for the
same complete packing domain.

| Priority and commitment | First discriminating question | Result that earns sustained attention |
| --- | --- | --- |
| 1 — BC-285, corner structure / H-126 | Which quantitative pose, penetration-or-alternative, or residual-capacity restriction follows from insertion saturation? | A useful uniform inequality with all alternatives retained, or an exact feasible counterexample to a proposed restriction at its stated side |
| 2 — BC-286, composition / H-102 | Can proved angle counts and class-weighted demand remove a meaningful surviving composition at $q$? | A certified nontrivial profile exclusion, or an exact obstruction for the frozen resource relaxation; preserve all unexcluded counts |
| 3 — BC-287, conditional dots / H-111 | Can the four-blocker description support a stronger asymmetric capture inequality on a continuous case? | A uniform positive surplus with a complete parent and explicit sibling remainder, or an exact relaxation obstruction identifying the geometric information lost |
| 4 — BC-288, contact and angles / H-117, H-121 | Is there a provable route to many wall-connected squares or fewer free angle components? | A finite feasible reduction or a useful structural lemma on a stated domain; alternatively a verified counterexample to the proposed local implication |

The conditional-dot worker starts from the already proved blocker description and need
not wait for a penetration theorem.
The corner worker should seek information that changes admissible poses or capture,
rather than classifying diagrams in isolation.
The composition worker provides a cheap independent test of whether angular demand alone
still has headroom.

Use `sqpack.fractional.classcert` and `devtools.run_class_program` where their existing
two-class, half-gap-cell semantics fit.
They do not implement geometric anchor conditioning, equality of several actual angles,
or a complete retained class certificate reader.
A candidate that earns a small extension can justify it; a general new engine is not the
initial deliverable.
Preserve BC-261’s single geometry-interface ownership when consuming its work.

At the first block boundary, choose the one or two leads with the clearest route to a
substantial theorem or decisive counterexample.
Give them uninterrupted mathematical attention in block two.
Block three finishes the selected scope and independently checks what it implies for the
global problem. If the spikes expose missing premises rather than promising proofs,
finish the strongest obstruction and state what would change the decision; do not spend
the remaining allocation expanding an instrument without a mathematical target.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
