---
title: X-045 — n11 global capture and exact optimality
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-045
  title: N11 Global Capture and Exact Optimality
  date: '2026-09-22'
  author: GPT-6 Astra at max reasoning; reviewed by the root coordinator
  campaign: packing.squares
  brief: >-
    A separate owner-requested W3 block on closing the exact n11 optimum.
    Investigate an explicit cutoff L below Trump's exact upper value U such
    that every locally side-minimizing packing with side in [L,U] has side U;
    combine this with a certified lower bound. Develop global structural
    necessities, complete classification and capture routes, and bounded
    falsifiers. Consolidate prior work on few angles, sliding assemblies and
    configuration strata into exact and approximate structural reduction routes.
    Preserve the broader X043 and low-open-case X044 explorations.
    No full search campaign, registry promotion or new numerical bound.
  sources:
  - operating-rules.md
  - SYNOPSIS.md
  - packing/campaign/README.md
  - packing/campaign/ideas.md
  - packing/campaign/ledger.md
  - packing/campaign/explorations/X-002-creative-frontier-and-basin-maps.md
  - packing/campaign/explorations/X-003-stratified-chunk-enumeration.md
  - packing/campaign/explorations/X-005-identity-relation-and-its-controls.md
  - packing/campaign/explorations/X-017-compatibility-and-complete-case-covers.md
  - packing/campaign/explorations/X-018-hybrid-strength-and-angular-release.md
  - packing/campaign/explorations/X-043-new-lower-bound-proof-directions.md
  - packing/campaign/explorations/X-044-low-n-certificate-transfer.md
  - packing/campaign/explorations/X-040-lower-bound-mechanisms-beyond-the-one-body-ceiling.md
  - packing/campaign/explorations/X-042-what-is-left-at-low-n.md
  - packing/campaign/hypotheses/H-103-complete-typed-global-capture.md
  - packing/campaign/hypotheses/H-028-reference-cell-angle-sheets.md
  - packing/campaign/hypotheses/H-032-small-n-optimal-moduli.md
  - packing/campaign/hypotheses/H-044-chunk-expressibility-of-records.md
  - packing/campaign/hypotheses/H-046-regular-predecessor-continuation.md
  - packing/campaign/hypotheses/H-102-complete-restricted-angle-support-families.md
  - packing/campaign/hypotheses/H-112-six-axis-five-common-angle-optimum.md
  - packing/campaign/hypotheses/H-113-at-most-two-angle-optimum.md
  - packing/campaign/hypotheses/H-117-forced-angle-complexity.md
  - packing/campaign/hypotheses/H-120-rank-nine-release-exclusion.md
  - packing/campaign/hypotheses/H-121-axis-plus-one-minimizer.md
  - packing/campaign/hypotheses/H-126-insertion-saturation-corner-structure.md
  - packing/campaign/hypotheses/H-128-corner-skeleton-ownership.md
  - packing/campaign/hypotheses/H-129-unit-shrink-fractional-value-near-u.md
  - packing/campaign/hypotheses/H-131-near-axis-counts-at-q.md
  - packing/campaign/hypotheses/H-232-n11-all-deep-class-ring-centre-atom.md
  - packing/frontier/n-011.md
  - packing/cases/trump11/packing.py
  - packing/cases/trump11/isolation-theorem.md
  - packing/src/sqpack/field.py
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-245-typed-backbone-theorem-packet.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-028/bc-282-residual-skeleton-design.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-028/bc-282-residual-skeleton-admission.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/lane-a-corner-structure.md
  - packing/campaign/agent-sessions/session-051-block2-reprice-and-lp-gate.md
  - docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md
  - docs/project/reviews/review-2026-09-07-n11-hybrid-strategy.md
  - docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md
  - docs/project/reviews/review-2026-09-10-n11-structural-normal-forms.md
  - docs/project/reviews/review-2026-09-12-n11-post-bc329-strategy-audit.md
  - docs/project/research/research-2026-09-10-x027-structural-helpers.md
  - docs/project/reviews/review-2026-09-22-kleddamag-n11-mathematics.md
  - packing/resources/web/external-square-certificates-2026-09-22/kleddamag-11/global-certificate.json
  - https://link.springer.com/article/10.1007/s00574-023-00340-0
  - https://arxiv.org/abs/1409.1534
  - https://arxiv.org/abs/1005.5610
  proposes: []
---
# X-045: N11 Global Capture and Exact Optimality

The strongest formulation of the owner’s idea is to find an **explicit interval with no
smaller local-minimum value** immediately below Trump’s value.
Let

$$
\ell=31/8=3.875,
\qquad
U=3.87708359002281417730789706010096\ldots.
$$

Prove, for an explicit $L<U$, that every local minimum of the original packing problem
whose side lies in $[L,U]$ has side exactly $U$. If a verified lower bound reaches $L$,
attainment of the global minimum then gives $s(11)=U$. This would let a finite
classification of possible minimum values finish a numerical lower-bound program before
that program reaches the algebraic endpoint.

There is a useful general fact behind this proposal: **the packing problem has only
finitely many local-minimum side values**, even though its minimizing configurations may
include continuous families.
Consequently some such interval exists below $U$. The proof is given below.
No explicit useful $L$ has been established here or in the inspected record.
Existence of the interval supplies a research target, not an effective bound.

The most plausible practical route is a hybrid: use valid threshold-resource profiles to
restrict possible arrangements, use physical contact and minimum conditions to rule out
the surviving alternatives, and finish selected leaves with an admitted local theorem or
an exact side inequality.
Requiring every surviving arrangement to be Trump’s packing would impose a stronger
uniqueness task than exact optimality needs.

This is the separate W3 exploration tracked by `think-1uos`.
[X-043](X-043-new-lower-bound-proof-directions.md) retains the wider mechanism review;
[X-044](X-044-low-n-certificate-transfer.md) retains the other low open cases.
The present block contributes analytic deductions, a scoped prior-result inventory,
candidate hypotheses, and one tiny exact audit with a corrected display receipt.
It launches no global enumeration and changes no registered hypothesis or bound.

## The Endpoint and Its Dependencies

The [n11 case record](../../frontier/n-011.md) establishes the current strict lower
bound and exact feasible upper endpoint.
The upper is the designated real algebraic root of

$$
P(S)=S^8-20S^7+178S^6-842S^5+1923S^4-496S^3
-6754S^2+12420S-6865.
$$

All endpoint comparisons in a proof must use its exact root and isolating data.
A rounded decimal above $U$ is useful for an outer domain; it is not a substitute for
proving equality with $U$.

| Premise | Established scope | What remains separate |
| --- | --- | --- |
| Kleddamag’s lower certificate | $s(11)>31/8$, complete parent-angle and centre coverage, exact threshold budgets | Its minimum charge and selected cores apply at their declared parent size; moving the target side changes those premises. |
| Exact Trump witness | A valid packing at $U$, with six axis-aligned squares and five sharing a nonzero tilt | Its contact pattern is a construction, not a necessary pattern for every optimum. |
| Registered local rigidity | All 128 derivative-distinct fixed-side tangent cones are zero; the finite-branch argument gives qualitative local isolation and strict local side optimality | It does not quantify the neighborhood or capture any distant configuration. |
| BC-240/241 radius packet | Retained-record-dependent local acceptance of $\rho=808514697/200000000000=0.004042573485\ldots$ in the labelled anchored pose chart | No independent full radius-generator replay; weighted aggregate/all-face witness gaps and closure-manager disposition remain relevant. Admit the quantitative endpoint before using it as a machine-checked leaf. |
| H-103 / BC-245 | A typed finite-language and Fritz–John proof contract retaining abnormal branches, ties, zero multipliers and rattlers | The complete producer/verifier and BC-246/247 controls are not ready. Finiteness of the language is not a completed enumeration. |

The radius statement and its current assurance are recorded in the case file; the
[local theorem packet](../../cases/trump11/isolation-theorem.md) supplies the chart and
mathematics. Its historical header is not the latest review disposition.
The source-distinct review accepted the local packet at retained-record-dependent scope,
not as a new independently replayed quantitative computation.
This report neither upgrades that scope nor requires a duplicate full radius run.

The objective gap $U-\ell\approx0.002083590023$ and the pose radius $\rho$ cannot be
compared as if they measured the same thing.
The first is a difference of container sides.
The second is the maximum of centre-coordinate and angle changes in a 33-coordinate
chart, with angles measured in radians.
A theorem relating objective slack to pose distance is missing.

Even the packet’s inequality

$$S-U\ge -C\|z-z_*\|_\infty^2$$

is a local inequality with an already-assumed chart domain.
For $S<U$ it gives a lower bound on a possible displacement, not an upper bound forcing
closeness. It cannot supply the global capture step.

## An Exact Cutoff Theorem

Let $\mathcal F$ be the feasible set of labelled packings, with the container anchored
at the origin and its side $S$ variable.
Each square has a centre and an orientation modulo a quarter turn.
A **local side minimum** is a feasible point having a neighborhood in $\mathcal F$ on
which no smaller side occurs.
This definition includes non-strict minima, flat components and rattlers.
It permits collective translations and rotations of the squares.

The minimum condition is for the original problem.
Intersecting with $S\ge L$ first would create false boundary minima at $L$. Likewise,
minimizing inside a chosen contact class does not imply a minimum of the full packing
problem: another contact or sign branch can contain a descent.

**Cutoff composition theorem.** Suppose:

1. $U$ has a verified feasible witness.
2. The global minimum is attained.
3. A verified lower bound implies $s(11)\ge L$.
4. Every local side minimum with $L\le S\le U$ has $S=U$.

Then $s(11)=U$. Indeed, a global minimizer exists, is a local minimum of the original
problem, and has side in $[L,U]$. Premise 4 decides its side.

The present lower bound suffices whenever the proved cutoff has $L\le31/8$. A cutoff
above $31/8$ would instead specify a useful numerical target for a stronger lower
certificate.
Neither case requires that every minimum of side $U$ be equivalent to Trump.

The apparently similar statement “no feasible packing has side in $[L,U)$” is much
stronger. If a packing existed below $L$, placing it unchanged in a larger container
would produce a feasible side in $[L,U)$. Thus that statement already excludes *all*
packings below $U$, regardless of the lower bound.
Local minimum values are the part of the formulation that makes the two ingredients
complementary.

### Why Some Cutoff Exists

Encode the orientation of square $i$ by $(a_i,b_i)$ with $a_i^2+b_i^2=1$. Its
perpendicular axis is $(-b_i,a_i)$. Containment of its four vertices is polynomial.
Pairwise interior disjointness is a finite disjunction of separating-axis inequalities;
splitting their absolute values into sign cases makes these polynomial too.
The resulting feasible set is semialgebraic over the rationals.
The finite quarter-turn overrepresentation and square labels do not change local minimum
values.

For a feasible coordinate vector $x$, local minimality is the first-order condition

$$
\exists r>0\ \forall y\in\mathcal F:
\quad \|y-x\|^2<r^2\ \Longrightarrow\ S(y)\ge S(x).
\tag{1}
$$

Quantifier elimination implies that the set $\mathcal M$ of these points is
semialgebraic. It has finitely many semialgebraically connected components, each joined
by semialgebraic paths.
Take such a path $\gamma$ inside $\mathcal M$. At every interior parameter,
$S\circ\gamma$ has a local minimum, since $\gamma$ stays feasible and is continuous.
This one-variable semialgebraic function is differentiable on finitely many open pieces;
its derivative is zero on each piece.
Continuity joins the constant values.
Therefore $S$ is constant on each component of $\mathcal M$, and

$$\mathcal V=\{S(x):x\in\mathcal M\}$$

is finite. Because the definition is over the rationals, these isolated objective values
are real algebraic numbers.
This reasoning concerns values, not isolated configurations or isolated contacts.

The general semialgebraic ingredients are reviewed by
[Basu](https://arxiv.org/abs/1409.1534). An adjacent result, finite critical values on a
finite Whitney stratification, appears as Lemma 2.7 of
[Dutertre and Moya Pérez](https://link.springer.com/article/10.1007/s00574-023-00340-0).
The argument above derives the particular local-minimum statement needed here without
assuming isolated critical points or a generic packing.

If a local-minimum value below $U$ exists, let

$$\beta=\max(\mathcal V\cap(-\infty,U)).$$

Any $L$ with $\beta<L<U$ has the cutoff property.
If there is no such lower value, the property holds for every smaller $L$. The endpoint
must be handled correctly: choosing $L=\beta$ would retain the unwanted minimum in the
closed interval. An effective closure needs an explicit separator and a proof covering
every other minimum type; the existence proof provides neither.

This gap can exist even if Trump is not globally optimal.
In that case the true optimum is a lower local-minimum value, so $s(11)\le\beta<L$. The
numerical premise $s(11)\ge L$ required by the composition theorem would be false.
Existence of some cutoff is therefore not evidence of Trump’s global optimality.

There are three different levels of progress:

| Level | What is available or required |
| --- | --- |
| Existential gap | The finite-values argument above proves that some $L<U$ works. It supplies no useful number. |
| Effective in principle | Exact quantifier elimination and algebraic root isolation, or justified degree/height separation bounds, can produce a separator. This may be as difficult as solving the full optimization problem and may produce an unusably small gap. |
| Useful explicit cutoff | A structurally reduced proof must produce a concrete $L$ that a valid lower-bound certificate already reaches or could plausibly reach. This is the open research target. |

### Three Statements That Must Stay Distinct

| Statement | Why it helps | What it does not establish |
| --- | --- | --- |
| Local-minimum values near $U$ are only $U$ | Combines with a lower bound to decide the global value | Uniqueness of the configuration at $U$ |
| Every relevant minimizing representative lies in admitted local neighborhoods | Lets local theorems decide its value, and possibly its pose | Capture of arbitrary feasible packings, unless separately proved |
| Every feasible packing with side at most $U$ is a Trump image | Decides the value and all equality configurations | This is substantially stronger than required for exact optimality. |

Compactness alone does not bridge them.
Once all global minimizers are known to lie in an open neighborhood $N$, compactness of
a bounded feasible sublevel outside $N$ gives a positive objective gap above the minimum
there, if the complement is nonempty.
Using that gap to prove the original capture would assume the fact being sought.
The finite-value argument above is different: it isolates $U$ among *local-minimum
values* even if an undiscovered global minimum lies much farther below it.

## Structural Facts That Survive at the New Bracket

Several earlier deductions extend to the whole interval $[31/8,U]$. Their exact
quantifiers are useful because they say which variables a complete proof may remove.

### Four Blockers, but Only Three Literal Corners in Trump

The twelve-square certificate at $99/25$ gives insertion saturation with overhang.
Writing

$$\kappa(S)=1-(99/25-S)=S-74/25,$$

the
[corner-structure derivation](../series/series-000-smoke-and-calibration/results/agenda-030/lane-a-corner-structure.md)
shows that every corner’s open $\kappa(S)$-square is met in its interior by a unit
parent. Four chosen blockers are distinct: a square meeting two adjacent corner boxes
would need axis extent greater than

$$S-2\kappa(S)=148/25-S>\sqrt2$$

throughout this bracket.
Here the endpoint exclusion in the retained twelve-square certificate supplies the
overhang premise; a lower-bound statement without endpoint exclusion would instead
require strictly smaller overhangs and appropriate limits.

These blockers need not touch a wall or contain the container vertex.
For a parent in a corner frame, let $g_x,g_y\ge0$ be its wall gaps and let
$0\le\phi\le\pi/4$ be its folded tilt.
Its corner penetration satisfies the exact identity

$$\delta=\min_Q(x+y)=g_x+g_y+\sin\phi.\tag{2}$$

Thus a *proved* bound $\delta\le d<1$ would force $\phi\le\arcsin d$ and put the common
parent box $[d,1]^2$ inside that parent.
At most one packed parent can meet the corner triangle $x+y\le d$ when $d<1$, because
two would share a box with nonempty interior.
These are conditional consequences; saturation has not supplied the needed small $d$.
The box is parent material, and banking point charge on a selected strict core requires
an additional containment proof.

There is a simple obstruction to deriving deep penetration from the four blocker roles
alone. For any $S\in[31/8,U]$, place four axis-aligned unit squares at the four corner
frames with gaps $g_x=g_y=9/10$. Adjacent squares are separated by $S-19/5\ge3/40$. Each
meets its required open corner box because $9/10<\kappa(S)$, yet all four corner
penetrations are $9/5>1$. This is an exact *four-square partial configuration*, not an
eleven-square packing.
It refutes that proposed deduction from blocker roles and mutual compatibility alone;
the other seven squares and their shared resources have to do real work.

The desired endpoint itself rules out another tempting premise.
The exact audit below finds literal-corner occupants at bottom-left, bottom-right and
top-left only. Trump’s top-right corner has

$$\min_i\delta_i=0.8445252756731993902452807597862\ldots>0,$$

attained by square 2 in the retained labelling.
Thus “all four literal corners are occupied,” and “every corner has penetration below
$1/2$,” both fail at the known endpoint.
Near-corner marks, open-box blockers, snug parents and literal corner occupants are
different notions.

### Wall Counts and a Normalized Global Minimizer

Two parents touching one wall have centre coordinates perpendicular to that wall in
$[1/2,\sqrt2/2]$. Their open incircles have radius $1/2$ and cannot overlap, so their
separation along the wall is at least

$$\eta=\tfrac12\sqrt{1+2\sqrt2}.$$

Four wall-touching parents would require $S-1\ge3\eta$. But $U<97/25$ and

$$
9\eta^2>171/20>(97/25-1)^2,
\qquad
171/20-(72/25)^2=639/2500>0.
$$

Hence **at most three parents touch any wall throughout the entire bracket**, including
vertex contacts. This is the existing wall lemma evaluated at an upper envelope for $U$,
rather than transferred from a smaller trial side without checking its inequality.

The independently reviewed
[normal form S1](../../../docs/project/reviews/review-2026-09-10-n11-structural-normal-forms.md)
preserves a feasible side and all labelled orientations.
In each fixed-angle feasible component, it provides a representative whose physical
contact components all touch both left and bottom walls and whose genuine active
translation rows have rank 22. At a global minimum the representative remains a global
minimum. The wall cap implies at most three such contact components, so one contains at
least four parents. The four distinct corner blockers then put two corner roles in one
component, connected by a physical contact path.
That need not be the component with four or more parents.

A further elementary count is available in this normal form.
Let $W$ be the number of distinct parent-wall incidences and $E$ the number of physical
parent-pair contacts.
The selected fixed-angle system has at most one translation row per wall incidence and
per pair. Rank 22 therefore gives

$$E+W\ge22,\qquad W\le12,\qquad E\ge10.\tag{3}$$

This is a count for the admitted normalized representative, not a rotational-rigidity
test. Rank in centre coordinates does not establish rank in all 33 pose coordinates;
unilateral contacts can open.

Side optimality additionally forces some physical component to span one pair of opposite
walls. Otherwise small independent translations of components fit the packing inside a
smaller square. Together with S1, a normalized global optimum has a component touching
left, bottom, and at least one of right or top.
This does not force both opposite-wall spans in the same component or an assigned short
path. A path alternative can involve two through eleven parents.

There is an important limit on this reduction for the proposed cutoff theorem.
S1 may move a packing a long distance along a flat fixed-side component.
It therefore need not preserve *arbitrary non-strict local* minimality.
For an abstract semialgebraic example, take the horizontal segment $0\le x\le1$, $S=1$,
joined at $(0,1)$ to $-1\le x\le0$, $S=1+x$. Points with $0<x<1$ are local minima of
$S$; minimizing $x$ along their fixed-side component moves them to a point with a
descent exit. This is a quantifier counterexample, not a square-packing counterexample.
S1 is safe for global minimizers, or for a cutoff argument with an additional
local-minimum-preservation theorem.

### Existing Angle Counts Apply Near U

[H-131](../hypotheses/H-131-near-axis-counts-at-q.md) includes exactly replayed counts
at the rational enclosing side $3877084/10^6>U$. Every packing in the present bracket
embeds in that container, so those counts apply: at most nine parents in retained
direction cells 0–24, at most ten in cells 0–29, and at most ten in cells 175–180. The
cells have exact half-angle boundaries; rounded degree descriptions must not enlarge
them. These give genuine angle diversity, not exactly six axis squares and five equally
tilted squares.

The gap between these necessities and Trump’s full pattern is still substantial.
The next structural proposition should say what a missing pattern forces, such as a
resource excess or a certified descent, while retaining every complementary case.

## Earlier Exclusions and Their Actual Reach

The
[post-BC329 audit](../../../docs/project/reviews/review-2026-09-12-n11-post-bc329-strategy-audit.md),
the
[structural-helper report](../../../docs/project/research/research-2026-09-10-x027-structural-helpers.md),
and [X-040](X-040-lower-bound-mechanisms-beyond-the-one-body-ceiling.md) supply the
following distinctions.
Their historical side values remain part of the claim, even where the new lower bound
now makes the corresponding physical eleven-square premise impossible.

| Earlier item | Status and scope | Consequence for an exact-closure route |
| --- | --- | --- |
| T-023 four-owner five-dot exclusion | Proved for one specified owner/core-footprint class at $S=96/25$, with its admitted symmetry transports | No theorem routes all packings into that class; no upward transfer to $U$ follows. |
| T-031 corner-octagon exclusion | Proved at $96/25$: some parent meets an open corner triangle of depth $1/2$ | It says “some corner,” not all four, and does not extend automatically to $U$. |
| Four corner marks individually forced by a heavy measure, H-128 | Tested support failed the desired mass budget; the broader retained-domain question remained open | A finite support failure is not a theorem that corner ownership cannot be forced with new resources. |
| Seven of eight marks / eighty abstract ownership patterns | Proved under the admitted measure at $96/25$; one shared surplus account governs all owner groups | A reusable counting method, but its weights, charge and unused-mass allowance must be re-established at the new side. |
| Point-only unconditional ceiling | The transported 88-family gives a genuine all-source additive obstruction at its stated scale, including unshrunk parent/continuous-measure variants described in X-042 | Pure additive repricing cannot erase that obstruction. Thresholds and global compatibility violate premises of the obstructed program. |
| All-deep corner class in the retained point language | A scoped all-site obstruction from the transported family; corner clipping alone cannot close that tree at its stated shrink/net | It is not a physically compatible eleven-parent packing and is not an obstruction to all richer charges. H-232’s ring-centre atom charges the witness $5/4$ against budget 1. |
| Mixed owner/tree classes and fourteen bin vectors | Failures and neutral fractional survivors in named relaxations | They do not prove all physical packings have only neutral owner selections. Selection and joint parent consistency remain separate obligations. |
| Individual parent domains | The old obstructing cores have individual legal unit parents already from side 3.82345 | Unary parent restriction alone cannot remove that family there. Simultaneous parent compatibility is additional information. |
| Saved residual escapes | Some exact unary exclusions; exp152’s two escapes intersect, while exp156 already excludes its saved escape against the named top-right core owner | These are not disjoint two-residual witnesses against arbitrary additional mass, nor evidence of a new full-parent gain. |
| Bottom-left quenching / arbitrary cell vertices | Exact counterexamples refute interpreting every selected-axis equality as physical contact or extending an axis-parallel escape lemma to tilted squares | Use S1’s proved existential normal form, complete physical contacts and nonlinear feasibility. |
| Finite angle or isolated-pose enumeration from rigidity intuition | Continuous sliding and rotational-rattler controls exist in solved small cases | Enumerate types and minimum values while retaining continuous components; do not assume isolated configurations. |
| H-103 and BC-245 | Global-capture question and typed proof contract remain open | BC-246/247 are implementation/completeness prerequisites for that instrument, not existing evidence that only Trump survives. |

An obstruction to an exact-cover relaxation is not a capture theorem.
Likewise, removing a fractional obstruction only shows that this particular obstruction
has gone. Acceptance still requires complete physical coverage or a complete minimum
classification.

## Turn Certificate Slack Into Structural Information

Use unit parents in $[0,S]^2$ for this discussion.
For every parent choose one admitted strict core, or one admitted member of a core menu.
Let $q(P)$ be its nonnegative charge.
Point, threshold and suitable density resources give a proved global budget

$$\sum_{i=1}^{11}q(P_i)\le M(S).\tag{4}$$

Every use below requires a complete parent-pose coverage theorem for the same $S$ and
selector. Unknown cells remain in the domain.
A poor selected core does not prove that every alternative core for its parent has poor
charge.

### Mode A: Excess Charge Forces Concentration

Suppose all legal parents have $q(P)\ge g(S)$, and parents outside a preferred pose
region $R$ have $q(P)\ge g(S)+\varepsilon(S)$, with $\varepsilon(S)>0$. If $r$ parents
lie outside $R$, then

$$
11g+r\varepsilon\le M,
\qquad
r\le\left\lfloor\frac{M-11g}{\varepsilon}\right\rfloor.
\tag{5}
$$

In particular $M-11g<\varepsilon$ forces every parent into $R$. At $S=U$, feasibility of
Trump requires $M\ge11g$; a claimed strictly negative excess budget there is a failed
premise, not a proof excluding the known witness.
The region $R$ may be a union of role neighborhoods.
Placing every square somewhere in that union does not yet assign one square to each
Trump role.

There is a sharper resource identity for mixed atoms.
For resource $a$, let $c_a$ be its valid integer capacity, $w_a\ge0$ its weight, and
$N_a(P)$ the number of selected cores activating it in the packing.
For point tokens $c_a=1$; for $k$-of-$m$ features $c_a=\lfloor m/k\rfloor$. When these
are the budget’s resources, take $M=\sum_a w_ac_a$; then

$$
M-11g
=\sum_a w_a(c_a-N_a(P))
+\sum_i(q(P_i)-g).
\tag{6}
$$

Every term is nonnegative.
If $w_a>M-11g$, then $N_a(P)=c_a$ is forced.
For a point this forces unique core ownership.
For a threshold feature it forces capacity saturation, not ownership of each named
token: a saturated 2-of-5 feature uses two distinct cores, but a fifth token may remain
unused. Different features sharing tokens still have valid individual capacity
inequalities; their joint realizability must also be respected in an assignment model.

This suggests designing certificates for a small *unused-resource allowance*, with heavy
features placed to distinguish corner/contact roles.
The objective is then a profile theorem rather than an impossible strict exclusion at
$U$. Multiple valid certificates can give simultaneous inequalities on the same count
vector and avoid depending on one low-charge landscape.

### Mode B: Compatibility Limits Charge Deficits

Sometimes useful parents have charge above $g$, but a few difficult regions fall below
it.
Partition, or cover with a proved assignment rule, the entire parent-pose domain into
cells $C_j$, with certified charge floors $\ell_j$. Let $z_j$ be the number of actual
parents assigned to each cell.
Use a count relaxation $\mathcal R(S)$ containing every admissible physical count
vector, including the constraint $\sum_jz_j=11$. Then

$$
\min_{z\in\mathcal R(S)}\sum_j\ell_jz_j>M(S)
\tag{7}
$$

excludes the declared domain.
A possibly weaker sufficient bound uses $d_j=(g-\ell_j)_+$: a proved upper bound
$\max_{z\in\mathcal R}\sum_jd_jz_j\le D$ gives total charge at least $11g-D$. This
discards the positive surplus of cells with $\ell_j>g$, so it need not be equivalent to
(7). For capture, retain every count pattern for which this lower bound does not exclude
it and derive geometry from their simultaneous resource traces.

Here the direction of every relaxation matters: enlarging $\mathcal R$ lowers the
minimum charge and raises the maximum deficit, which is conservative.
A cell is not automatically capacity one.
For unit parents, centre diameter strictly less than one is one sufficient capacity-one
certificate, by the incircles; other cells need their own capacities.
Uncertain overlap does not certify a conflict.
Pairwise compatibility need not imply joint realizability, and independent D4 folding of
parents does not preserve their mutual geometry.

### The Existing Lower Certificate Cannot Be Transplanted

The source uses $L_0=191/50$, parent side $A_0=764/775$, and adaptive selected cores,
with

$$
\Gamma_0=31248829/31250000,\quad
M_0=1374934993/125000000,\quad
11\Gamma_0-M_0=13483/125000000>0.
$$

These establish the strict lower bound $L_0/A_0=31/8$. Keeping $L_0$ while targeting $U$
requires the smaller parent $A_U=L_0/U$. The exact audit tests only the first retained
row and already finds

$$
A_U=0.985276667707213845\ldots,
\qquad
B_0-A_U=0.000526633188054045\ldots>0.
$$

The frozen core is larger in area than its parent and cannot fit.
That row alone gives the necessary unchanged-core ceiling

$$
S\le\frac{L_0}{B_0}
=\frac{1989007624233276222295049420000000000}
{513290649600790138576760110307407081}
\approx3.8750123848548954.
\tag{8}
$$

This is an upper limit on unchanged geometry, not an attainable new bound or a limit on
new cores, weights or features.
Changing the cores and parent domains requires fresh coverage floors before either slack
mode can be used at $U$. The 107,864 source budget units cannot be reinterpreted as a
geometric concentration allowance at the new target.

## Discover the Cutoff by Working Backward From Structure

Choosing $L=3.875$ first and asking a generic solver to finish the remaining 34-variable
problem hides the main mathematical question.
A more informative route derives the side interval on which each structural exclusion or
minimum classification works, then compares their common cutoff with the verified lower
bound.

### A Minimum-Class Cover With Several Valid Endings

Let $\mathcal C_b$ be a finite cover of the local minima in a candidate band, retaining
continuous coordinates and every tie or degeneracy.
It is sufficient to close every member by one of these methods:

| Leaf disposition | Exact obligation |
| --- | --- |
| Infeasible | No physical packing realizes the whole leaf domain. |
| Descent | Every feasible point of side below $U$ in the leaf has arbitrarily nearby feasible configurations of smaller side in the original problem. |
| Side inequality | Every relevant point in the leaf has $S\ge U$; equality may have several configurations. |
| Local capture | The whole surviving pose box, after one exact global D4 transformation and label map, lies strictly inside an admitted local neighborhood whose theorem gives $S\ge U$. |
| Lower minimum values | Every local-minimum value represented by the leaf is at most a proved $b_b<L$, with the rest at least $U$. |

If each non-endpoint leaf is decided on $[L_b,U]$, the combined cutoff is
$L=\max_b L_b$, with strict lower-value endpoints raised as necessary.
An unresolved leaf has no usable cutoff and remains in the cover.
This maximum is a consequence of the branch coverage, not a choice made to match the
current lower bound.

An even weaker statement can suffice for global optimality: every hypothetical global
minimizer admits a side-preserving normalized representative and at least one valid
label in the closed family.
This is the route that can safely use S1 immediately.
It need not classify every flat local minimum, and it must not be reported as the
stronger all-local-minima cutoff theorem without the additional argument.

Raw owner-label exhaustion is sufficient, but an existential selection theorem can be
cheaper: each hypothetical minimizing representative must admit at least one closed
selection. The selection must use the same physical parents across its conditions.
Separately chosen unary witnesses do not give a common owner or a common packing.

### Resource Profiles Before Contact Enumeration

A plausible first classification has four layers:

1. Complete corner-blocker, angle-count and wall/contact-component alternatives at sides
   in the candidate band.
2. Valid charge floors and resource-saturation constraints for those roles, including
   the remaining parents and uncertain cells.
3. Joint geometric compatibility, with capacity, Hall-type, clique or higher-order
   restrictions only where their physical interpretation is proved.
4. Exact minimum conditions on the surviving patterns, followed by a local endpoint or a
   direct algebraic side inequality.

This extends X-043’s difficult-pose method to a classification of minimum values.
A globally valid coarse profile can make the typed contact systems smaller before the
hard algebra begins.
It avoids assuming that the near-optimal configuration has the same contacts as Trump.

A certificate for the missing quantitative bridge would have the form

$$
V(P)\le E(S),\qquad
V(P)\ge c\,d(P,Z)^p,
\qquad
\sup_{S\in[L,U]}E(S)<c\rho^p,
\tag{9}
$$

where $Z$ is a specified set of admitted endpoint charts, $d$ uses their stated pose
metric and exact matching maps, and $c,p>0$ are proved.
Then every packing in the declared class is captured.
The potential $V$ could combine unused resource capacity, excess charge and conditional
geometric penalties.
Equation (9) identifies the required inverse-stability statement; it is not supplied by
the current objective gap or by a generic appeal to compactness.
The zero set and constants are part of the proof obligation.

### Descent Can Be Easier Than Geometric Impossibility

For the cutoff route, a realizable non-Trump pattern need not be impossible.
It may simply fail to be a local side minimum.
This permits constructive geometric deformations as leaf certificates.

For a smooth support branch with inequalities $g_j(x)\ge0$, a direction $v$ with
negative side component and strictly positive derivatives on every active inequality
gives a local feasible descent, provided the branch and orientation chart are retained.
Inactive inequalities have positive slack and persist for a sufficiently short move.
A uniform version on a box can use

$$
Dg_j(x)v\ge a>0,
\qquad
\left|g_j(x+tv)-g_j(x)-tDg_j(x)v\right|\le Kt^2/2;
$$

then active constraints remain satisfied for $0<t<2a/K$, with an additional step bound
from the inactive slacks.
Use actual angle coordinates or an exactly feasible orientation path; a straight line in
$(\cos\theta,\sin\theta)$ usually leaves the unit circle.
Zero derivative rows require an exact invariant motion, a second-order argument or
another certificate.
A feasible linearized direction alone is insufficient.

The most promising deformations would move a small contact component or change a
corner-serving chain while leaving a certified feasible remainder.
One-square quenching cannot decide collective jamming.
For ruling out a local minimum, the deformation must give smaller-side configurations
arbitrarily close to the starting point.
A finite flat walk followed by a distant descent only disqualifies global optimality; it
can still be useful in the normalized-global-minimizer variant.

This distinction suggests two complementary instruments: local descent certificates and
side-preserving routing to a configuration with a descent exit.
Their outputs should have different claim strings.

### Typed Critical Values and Algebraic Separation

The
[BC-245 contract](../series/series-000-smoke-and-calibration/results/agenda-026/bc-245-typed-backbone-theorem-packet.md)
retains complete pair/wall inequalities and ordinary or abnormal Fritz–John multipliers.
Its normal form is

$$
\alpha\nabla S-\sum_j\lambda_j\nabla g_j=0,
\qquad
\lambda_jg_j=0,
\qquad
\alpha,\lambda_j\ge0,
\qquad
\alpha+\sum_j\lambda_j=1.
$$

Artificial partition rows, tied signs, zero multipliers and rattler variables cannot
silently be removed.
Algebraic equality embeddings require their equality multipliers or a proved regular
elimination.
BC-246’s Trump recovery and BC-247’s solved-case and adverse controls remain
prerequisites for that particular producer and verifier.

Raw Fritz–John values need not be finite, despite the theorem about local minima.
For example, minimize $S$ subject to $-x^2\ge0$ and $0\le S\le1$. Every feasible point
has $x=0$ and admits the abnormal choice $\alpha=0$, multiplier one on $-x^2$, so the
raw stationary system contains every $S\in[0,1]$. Only value zero is a local minimum.
This exact example explains why abnormal stationarity is a necessary condition to
retain, not a sufficient classification of minimum values.

In principle, quantifier elimination or a complete stratified critical-value analysis
could produce an integer polynomial $Q$ whose roots include every relevant minimum value
and $U$. Exact root isolation can then seek a root-free interval immediately below $U$.
Alternatively, a rigorous root-separation bound derived from $Q$'s degree and height
would suffice if the numerical lower bound lay within that distance of $U$. The
[Davenport–Mahler–Mignotte literature](https://arxiv.org/abs/1005.5610) gives relevant
separation methods; it does not supply the missing packing polynomial.

The degree-eight polynomial $P$ of Trump alone is insufficient.
Another minimum could satisfy a different polynomial with a nearby root.
Generic degree/height bounds from the full quantified packing problem are unlikely to
give a useful threshold at a gap of $0.00208$; no quantitative estimate was established
in this block. The practical opportunity is a much smaller *complete* list of
critical-value polynomials after structural pruning, including positive-dimensional
components.
Proving that this list is complete is likely harder than isolating its roots.

## A Closure Proof Need Not Classify Every Equality Packing

The endpoint task should distinguish these properties explicitly:

| Property | Meaning here |
| --- | --- |
| Individual immobilization | No single parent has an allowed motion with all others fixed. |
| Collective jamming at fixed side | No nontrivial allowed collective motion in the stated nearby component, after specified symmetries. |
| Fixed-side local isolation | The pose is the only feasible pose in a neighborhood at that side. |
| Local side optimality | No nearby packing has smaller container side; equality poses may form a family. |
| Exact optimum | No packing anywhere has side below $U$. |
| Equality classification | Every packing at $U$ is described, including any continuous components. |
| Uniqueness modulo symmetry | Every equality packing is one global D4 image and square relabelling of the same pose. |

The registered Trump theorem establishes more locally than a contact count does, but it
says nothing about another component far away.
A second, inequivalent packing at side $U$ would refute Trump-only capture and global
uniqueness, while leaving exact optimality entirely possible.
A verified packing below $U$ would refute exact optimality, regardless of whether it is
a local minimum; a further local-minimum proof is needed only to refute a particular
cutoff claim whose band does not necessarily contain the global minimum.

A sound final composition may therefore have several endpoint families.
For each captured family, prove a local side inequality; only Trump’s family currently
has the retained local theorem discussed here.
Other leaves may directly prove $S\ge U$ without a pose classification.
If all minimizing classes close in these ways, the value is decided even when equality
classification remains unfinished.

## Few Angles, Sliding Assemblies and a Complete Map of Families

The owner’s refinement suggests reducing the continuous problem before trying to capture
Trump: perhaps an optimal representative has only a few angles, or consists of a few
coherent assemblies seated in restricted regions.
Earlier records already propose this route and contain partial reductions and controls
against overclaiming.
The new opportunity is to combine it with the $3.875$ floor, valid resource profiles at
the stronger target, and the minimum-value cutoff above.
No inspected result already supplies the required global reduction.

### What the Earlier Exploration Actually Established

| Antecedent | Retained result or proposal | Consequence for this block |
| --- | --- | --- |
| [X-003](X-003-stratified-chunk-enumeration.md) and [H-044](../hypotheses/H-044-chunk-expressibility-of-records.md) | Same-angle contact assemblies describe many serialized records, but the corpus retained 859 internal sliding degrees under contact-normal equalities. The frozen lattice grammar misses n11; Trump’s tilted squares slide and become separate pieces in that narrow grammar. | Use assemblies with explicit slide parameters. Neither few angles nor positive-length contact makes an assembly rigid. Corpus calibration is not a minimizing-representative theorem. |
| [BC-095 / Session 051](../agent-sessions/session-051-block2-reprice-and-lp-gate.md) | The old raw chunk grammar counted about $4.357\times10^{20}$ labels at $K\le6$. Even its restricted $K\le3$ slice costed about $2.1\times10^8$ LP solves including the angular sweep under its stated assumptions; Trump’s decomposition lay outside that slice. | Finite types do not justify exhaustive enumeration. New structural pruning must change the admitted family count; relabelling the same grammar does not. |
| [X-005](X-005-identity-relation-and-its-controls.md) and [H-032](../hypotheses/H-032-small-n-optimal-moduli.md) | After quotienting by D4 and relabelling, the n3 optimum is a sliding interval with contact-changing endpoints and n4 is a point. The corrected X-005 controls do not make a contact signature a component identifier. | Keep actual path or closure evidence and the chosen labelled/unlabelled/D4 quotient. Matching descriptors cannot join two families. |
| [G-4/G-6 of the August strategy review](../../../docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md) and [H-028](../hypotheses/H-028-reference-cell-angle-sheets.md) | Kink codimension is a proposed corpus law. The reference six-plus-five angle sheet keeps one imported separating cell; it is not the lower envelope over all cells and assignments. | Tie loci may guide discovery, but every omitted cell remains a proof obligation. Do not promote a plot or a successful local continuation to a complete family. |
| [H-117](../hypotheses/H-117-forced-angle-complexity.md), [H-121](../hypotheses/H-121-axis-plus-one-minimizer.md), and the [September hybrid review](../../../docs/project/reviews/review-2026-09-07-n11-hybrid-strategy.md#what-few-angles-would-require) | The useful exact-angle normal form is already stated existentially: some global minimizer uses the axis and one other angle. A segment-equality graph gives a precise angular-rank test, but no global theorem forces that rank. | Continue this question rather than registering a duplicate. The new resource information may help prove its missing premise, or support the weaker tube route below. |
| [H-112](../hypotheses/H-112-six-axis-five-common-angle-optimum.md) and [H-113](../hypotheses/H-113-at-most-two-angle-optimum.md) | Complete lower bounds for six-axis/five-common-angle, and for all packings with at most two actual angles, remain unproved. | Trump’s local theorem proves neither restricted-family result. H-112 would still leave other multiplicities and the global normal form. |
| [H-120](../hypotheses/H-120-rank-nine-release-exclusion.md), [X-018](X-018-hybrid-strength-and-angular-release.md), and [BC-282 admission](../series/series-000-smoke-and-calibration/results/agenda-028/bc-282-residual-skeleton-admission.md) | Releasing one Trump segment produced a specific rank-nine family. Several closed subdomains were excluded; the remaining ten-square skeleton has an exact translation-fiber reduction. Uniform coverage of those fibers was not proved and its target was not admitted. | This is a useful family/degeneracy control, not a completed enumeration. Its historical $3.81\le S\le3.84$ exclusions do not extend to the present bracket without new proofs. |
| [X-017](X-017-compatibility-and-complete-case-covers.md#physical-stationarity-changes-a-formulation-not-every-existing-branch) and [BC-245](../series/series-000-smoke-and-calibration/results/agenda-026/bc-245-typed-backbone-theorem-packet.md) | Finite stationary-value reductions and typed case composition were already discussed. Physical stationarity, a fixed-angle LP basis and a complete configuration cover are different objects. | The direct local-minimum-values proof above removes the need to infer minimizers from a raw stationary set. Its contribution here is the precise cutoff composition, not a claim that finite-value reasoning was absent from earlier work. |

The inspected ledger records H-112, H-113 and H-121 as blocked, and H-117 and H-120 as
open questions. Their partial mathematics remains useful; these statuses must not be
replaced by an implicit assumption that the normal form or family bound is available.

### An Optimal Representative With Few Angles

Define the actual orientation count

$$
\kappa(P)=\#\{\theta_i\bmod\pi/2:i=1,\ldots,11\}.
$$

The sufficient reduction is **there exists a global minimizing packing with
$\kappa(P)\le k$**. It need not hold for every global minimizer, every local minimum, or
every feasible packing near $U$. A theorem restricted to the case $s(11)\in[L,U]$ would
suffice for this block when a verified lower bound reaches $L$. This weaker premise
still concerns minimizers of the original problem, not minima created by imposing a
lower side boundary.

There are three distinct candidate reductions:

| Reduction | Continuous angular variables before further equations | Missing global obligation |
| --- | ---: | --- |
| At most $k$ arbitrary actual orientations | Up to $k$ | Some global minimizer belongs to the union over every assignment and multiplicity. |
| Axis plus one angle, with arbitrary multiplicity | One | H-121’s representative theorem, including an empty axis class and coincident-angle boundaries. |
| Six axis squares and five at one common angle | One | The multiplicity reduction as well as the representative theorem; H-112 alone only supplies the proposed family inequality. |

The six-axis/five-common-tilt Trump packing is a positive control in all three families,
not a proof that one of them contains a global minimizer.
For arbitrary two-angle families both **absolute** angles remain variables: continuously
rotating one angle to zero also rotates the square container.
Only a common D4 transformation of the entire packing and a square relabelling may be
used for the present compatibility quotient.
Reducing each square’s orientation modulo $\pi/2$ represents the same individual square;
independently reflecting its tilt generally changes the packing.

For a finite angle-elimination argument, select a global minimizer with the fewest
nonaxis angle classes, as H-121 proposes.
If two such classes remain, prove a finite feasible path of nonincreasing side ending
with fewer classes, or a packing with strictly smaller side.
The latter contradicts global minimality; in the former case the endpoint remains a
global minimizer and contradicts the selected minimum class count.
Intermediate angles may split and contacts may release, but the entire path must remain
feasible and the endpoint reduction must be proved.
An infinitesimal motion or a sequence of numerical reoptimizations supplies neither.

This logical form also determines the falsifier.
A high-angle feasible packing, or even a high-angle global minimizer, does not by itself
exclude a different low-angle global minimizer.
A rigorous packing below a proved lower bound for the entire proposed low-angle family
would refute that family’s representative claim.
Conversely, a low-angle family lower bound of $U$ without the representative theorem
would say that any improvement must use more angles, not that improvement is impossible.

### Angle Classes Are Not Rigid Blocks

Four structures must have separate records:

- An **equal-angle class** is a set of parents with the same actual orientation; they
  need not touch or occupy one region.
- A **positive-segment assembly** connects parents through shared edges of positive
  length. Its members share an orientation, but tangential slides can remain.
- A **physical contact component** allows point contacts and can contain several
  orientations. Its connectivity does not imply rigidity.
- A **rigid block in a declared family** has no changing relative poses in that family’s
  feasible motions, after factoring out its common translation and rotation.
  Rigidity under preserved contact equalities does not by itself exclude motions that
  release those contacts in the original unilateral packing problem.

The simplest counterexample to conflating the first three with rigidity is

$$
Q_1=[0,1]\times[0,1],\qquad
Q_2=[1,2]\times[t,t+1],\qquad -1<t<1.
$$

The squares have equal angles and share an edge segment of length $1-|t|$, yet their
relative displacement changes with $t$. Keeping an exact contact normal has not removed
that slide. This analytic control is the small version of X-003’s retained corpus
warning.

There is nevertheless a useful exact angle lemma from the hybrid review.
Add one fixed wall vertex to the eleven squares, join squares only for positive-length
shared segments, and join a square to the wall vertex only for a flush edge.
If $k_0$ graph components are not connected to the wall vertex, a spanning forest gives
angular equality rank

$$r=11-k_0.$$

There is at most one free angular variable per unanchored component, plus the fixed axis
orientation if the wall component contains a square.
Thus $r\ge10$ is sufficient for axis-plus-one-angle structure; it is not necessary,
because disconnected components may happen to share an angle.
Trump has $r=10$. Releasing its segment $(9,10)$ while retaining the specified other
segments and flush wall incidences gives the rank-nine H-120 control.
Point contacts, sparse KKT stresses and the centre-contact count (3) do not imply this
angular rank. Nor does the rank prove that the remaining angular parameters are feasible
motions.

A **coherent assembly** can instead mean a deliberately parameterized family with slides
retained, for example

$$
C_6=p,\quad C_7=p+ae-f,\quad C_8=p+e+bf,\quad
C_9=p+(a+1)e+(b-1)f,
$$

where $e,f$ are perpendicular unit vectors at one common angle.
This is the actual four-square block in the
[BC-282 design](../series/series-000-smoke-and-calibration/results/agenda-028/bc-282-residual-skeleton-design.md),
with explicit slide variables $a,b$ and complete internal pair clauses; its old domain
also requires $ab\ge0$ and bounds the slides.
The displayed formula alone is not a valid arbitrary-packing reduction.
Its value is that translation, angle and internal slides remain visible rather than
being hidden in a supposedly fixed lattice shape.
Prescribed corner or wall regions must likewise be either proved consequences or named
family assumptions with complementary families retained.

With $k$ exact angle classes there are initially $22+k+1$ real coordinates: centres,
class angles and side.
An assembly representation using $b$ common body poses and $d$ internal parameters has
at most $3b+d+1$ generative coordinates before shared-angle identifications and wall
conditions.
These are parameter counts, not claims about the actual dimension or rigidity
of the constrained set.
Removing parameters requires a proved parametrization or rank/regularity argument;
singular branches must survive separately.

### Finite Types Must Cover Continuous Families and Their Boundaries

A useful proof map has a finite set of **types**, each carrying a continuous domain and
its exact defining constraints.
The rational/algebraic packing encoding permits finite semialgebraic decompositions in
principle; an effective sign-invariant decomposition is a standard construction, with
severe worst-case costs.
See [Basu, Theorem 2.4 and Section 3.5](https://arxiv.org/html/1409.1534v1). This
existence statement does not supply a small, already generated n11 map.

For this problem a type would retain at least:

| Type information | Boundary or ambiguity that must remain |
| --- | --- |
| Actual-angle charts and a declared equal-angle partition, when used | Quarter-turn seams, class collisions, an angle becoming zero, and separate independent angles if equality has not been proved |
| Physical wall and pair feature contacts | Segment-to-point degeneration, opening contacts, new contacts, tied separating alternatives and the complete remaining nonoverlap clauses |
| An assembly parametrization or a fixed-angle LP basis | Internal slides, basis changes, determinant-zero slices, duplicate bases and positive-dimensional solution sets |
| Minimum or stationary conditions, only where justified | Zero multipliers, rattlers, abnormal or singular branches unless a proved formulation-specific theorem removes them, and minima on type boundaries |
| Side and resource/role assumptions | Every region excluded by those assumptions needs a proved exclusion or another child; the side cutoff is not a substitute for an original-program minimum condition |

There are finitely many angle partitions and contact-feature labels, but generally
infinitely many angles and configurations within one type.
A sign or contact type can also have several disconnected pieces.
If a proof uses smooth-stratum or topological properties, it must refine the type into
pieces with those properties and establish the required boundary incidences.
For ordinary exclusion it may be cheaper to use overlapping closed parameter boxes with
proved coverage, without claiming a full topological stratification.
All 55 pair clauses and all containment conditions must be retained or discharged by
proved implications.

At fixed class angles, a selected full separating branch is an LP in the 22 centres and
side. A half-angle chart makes its coefficients rational in the angular parameters.
For one class angle, an invertible 23-row basis therefore gives rational centre and side
functions of one parameter.
Their determinant roots, slack roots, comparisons with the exact $U$, derivative roots
where needed, and endpoint limits can partition a candidate proof into intervals.
Every singular parameter needs an alternative basis or an exact slice argument;
identically zero expressions are retained identities, not roots to discard.
With two angles, corresponding exceptional sets include curves and singular
intersections, so a one-dimensional root list no longer suffices.

This is the already proposed H-102/H-112/H-113 route, strengthened here by asking which
resource profiles can remove entire branches before that algebra.
The family value is the lower envelope over **all** assignments, all separation branches
and all feasible centre solutions.
One imported Trump cell and its angle sheet do not provide it.
The earlier conjecture that a $k$-angle optimum should sit at a codimension-$k$ kink
cannot delete smooth minima, flat faces or degenerate critical sets without proof.
Nor may an angular grid turn a continuum into finitely many possible optimum angles.

The exact closure contract can be stated compactly.
Suppose a verified bound gives $s(11)\ge L$, and there is a theorem that **some global
minimizer** has a representative in a union of declared families
$\bigcup_{j=1}^{N}\mathcal F_j$. For every family, give a complete child cover including
all seams, and close every sub-$U$ leaf by one of the admitted arguments above: physical
infeasibility, a direct side inequality, original-program descent, valid routing of
global minima to a closed family, or a whole-domain inclusion in an admitted local
endpoint chart. Keep all proof dependencies in a DAG or prove a well-founded reduction
rank. Then a global minimizer below $U$ has no surviving leaf, so $s(11)=U$. This
requires neither a finite list of configurations nor uniqueness at $U$.

The stronger local-minimum cutoff needs a cover of **all original-program local minima**
in its band; an existential representative theorem only supports the weaker
global-minimizer composition just stated.
A minimum of a restricted equal-angle family may admit a descent that separates those
angles in the original problem, so family minima must not be relabelled as original
local minima. Conversely, an original global minimum is a minimum in every subfamily
containing it; this is why a complete restricted-family inequality can be enough after
the representative theorem.

### A Weaker Route: Resource-Forced Angle and Position Tubes

Proving exact equal-angle structure may be avoidable.
Instead seek a theorem that every relevant minimizing packing lies in a finite union of
quantitative tubes

$$
\mathcal T_a=\{P:\ d_{\pi/2}(\theta_i,\alpha_{a,c(i)})\le\delta_a,
\quad (x_i,y_i)\in R_{a,i}\ \text{for every }i\},
$$

with all necessary assignments, angle parameters, physical alternatives and boundary
cases retained. Here the class centres $\alpha_{a,c}$ may vary over declared intervals;
the parents’ angles remain independent inside the tube.
Pairwise closeness is not transitive, so a clustering routine must not silently replace
this explicit assignment-and-radius cover.
Such a theorem reduces domain widths and role possibilities without asserting an exact
two-angle normal form or reducing eleven independent angles to two.

The proposed chain is concrete: valid target-side charge floors and saturation
identities restrict resource profiles; joint capacities restrict the associated spatial
and angular assignments; complete interval geometry or parametric LP inequalities close
each resulting tube.
All remaining dispersed-angle profiles stay in the cover until excluded.
Near Trump, progressively stronger joint constraints would have to enclose **all**
centres and angles inside the admitted local chart; angular closeness alone does not
give pose capture or the correct labels.
This remains a proposed proof architecture, not a consequence already extracted from the
$31/8$ certificate.

There is an exact criterion for one useful thickening step.
Let $f(\alpha)$ minimize side over every centre placement and separation choice at a
labelled vector of exact angles, and suppose throughout a complete template domain
$f(\alpha)\ge U+\mu$ for some $\mu>0$. If $0\le\delta\le\pi/4$ and
$d_{\pi/2}(\theta_i,\alpha_i)\le\delta$ for every parent $i$, the reviewed
angular-transfer inequality gives

$$
f(\theta)\ge\frac{U+\mu}{\cos\delta+\sin\delta}\ge U
\quad\text{if}\quad
\cos\delta+\sin\delta\le1+\frac{\mu}{U}.
$$

Thus a strictly separated family can cover a positive angular neighborhood.
The floor must hold for the full rounded-angle problem: a bound for one contact cell or
a prescribed wall/assembly pattern cannot be reused unless the transfer preserves those
restrictions or a larger valid domain was proved.
Where the restricted margin tends to zero at Trump, this argument supplies no fixed
positive tube radius.
Use an admitted local theorem there, while retaining all other centre/contact branches
at the same angles. If another equality family exists, it needs its own endpoint
inequality or chart; exact optimality still need not imply Trump-only capture.

Relative to H-121, the tube route asks for weaker geometry but generally leaves more
continuous variables for the certifier.
Its attraction is that the new threshold and compatibility machinery already speaks in
quantitative pose regions and capacity profiles.
An exact angle-merging theorem could be far more powerful if found; neither route is
presently established or priced globally.

### What an Adjacency Map Can and Cannot Prove

The existing
[cartography review](../../../docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md)
already distinguishes a certified path and its maximum required side from an algorithmic
transition.
[H-046](../hypotheses/H-046-regular-predecessor-continuation.md) deliberately
treats aligned-predecessor continuation as numerical event discovery, not topology.
X-005’s corrected component controls should remain mandatory for any new map.

A node used in a proof should name a connected family, or explicitly state that its
connected components remain unresolved.
An edge can mean a certified common boundary, a validated continuous path, or a proved
side-nonincreasing deformation; those are different assertions.
For a path $\gamma$, record its side ceiling

$$h(\gamma)=\max_{t\in[0,1]}S(\gamma(t)).$$

One path gives an upper bound on the side needed to connect its endpoints.
Failure to find a path gives no lower bound; certified nonconnection needs a separate
complete separation argument.
For closed path-connected family pieces with certified nonempty intersections, a
connected intersection graph proves that their union is path connected.
A contact-label graph with unknown intersections does not satisfy these premises.
The side band must be part of the claim: a connection that leaves $S\le U$ is not a
connection in that sublevel set.

Even proved connectivity to Trump at side ceiling $U$ does not exclude a smaller packing
elsewhere in the same component.
The path may have to increase side.
For a proof of optimality, use value inequalities on all families, or a proved
nonincreasing-side reduction from every relevant global-minimum representative to an
endpoint family. If reductions are repeated, strict decrease of an integer such as the
completed angle-class count can give termination, but only after each entire reduction
path has been proved; a cyclic adjacency graph or an unfinished contact walk gives none.
Quotienting by D4 or relabelling can identify separate labelled components, so the
equivalence convention belongs on every such assertion.

The BC-282 control makes the gap between a finite map and a completed proof tangible:
ten envelope chambers and 24 exact open collision intervals preserve the whole declared
translation problem, including tied owners and singleton fibers.
The independently reviewed reduction proves no target fiber covered.
Its proposed six-source chain was only sufficient, while a general cover may require
repeated source labels and more intervals.
Mapping all interval births, deaths and endpoint-order changes could close this
**restricted** family, but neither the finite inventory nor its current lack of a cover
promotes it to a global exclusion or a physical counterexample.

### Additional Candidate Questions, With Explicit Controls

These continue existing hypotheses or add local candidate labels; they allocate no new H
identifiers and authorize no enumeration campaign.

| Candidate | Smallest discriminating proof or control | Success, falsifier and scope |
| --- | --- | --- |
| G8: A useful minimizing-representative angle reduction can be proved in the current band | Continue H-117/H-121 by selecting one complete two-nonaxis-component family and deriving a finite side-nonincreasing angle-merging motion, with release/recontact and endpoint siblings | A uniform motion proves one reduction edge. A configuration meeting its premises with a proved obstruction to every nonincreasing path in the actual allowed path domain rejects that motion claim; this domain may leave the starting family. A high-angle local minimum or trapping inside that starting family alone refutes neither the permitted nonlocal route nor the global existential normal form. Global acceptance needs every alternative or another complete reduction. |
| G9: A small assembly cover survives after retaining tangential slides | First encode one whole sliding-contact family and its boundary siblings; require the two-square slide control, the actual Trump control, and the n3/n4/n6 distinction between components, points and rattlers | A complete parametrization gives a valid cover for its declared family. A feasible pose satisfying the declared family assumptions but omitted by the parametrization rejects completeness. Recovering Trump alone does not prove a global grammar or its tractability. |
| G10: Valid resource profiles force a union of tractable angle/role tubes, with all dispersed alternatives closed | At an explicit rational outer side at least $U$, prove a profile exclusion or a tube implication on one complete coarse role domain; then test the claimed angular-thickening inequality against a full-family positive-margin control | A complete conditional tube theorem is information unavailable from an exact-angle ansatz alone. One feasible pose in its declared domain outside the tube union refutes that all-feasible conditional claim; an outer relaxation survivor is merely unresolved. A claim about every global minimizer needs a global-minimizing counterexample; an existential claim needs every proposed representative excluded. |
| G11: An exact map of one continuous restricted family can close its boundary obligations economically | Use the BC-282 design as a representation control, then declare a fresh useful domain and prove one full facet-transition/interval-chain template including births, ties, legal touches and singleton fibers | A checked closed-domain certificate supplies one honest costed family. A missing legal boundary pose rejects the cover; a diagram, finite chamber count or successful sample does not accept it. No old $3.84$ theorem is relabelled as a near-$U$ result. |

For discussion, G10 followed by a small G9/G11 family appears the most direct way to
connect the newly verified research to the owner’s structural intuition.
It can yield a useful conditional lemma without first proving H-121 or building a global
topological atlas.
G8 offers a larger reduction if a true finite-motion theorem is found,
but its present burden is precisely the unproved global normal form from the earlier
review. These are preliminary promise comparisons, not performance claims or a scheduled
execution plan.

## Candidate Hypotheses and Small Discriminators

These local labels are proposals for later codification, not new H identifiers or an
execution queue. The proposed pilots are deliberately smaller than a global search.
Their budget and exact domain would be fixed before any research-loop run.

| Label and hypothesis | Smallest useful discriminator | Acceptance, falsifier and information gained |
| --- | --- | --- |
| G1: An explicit local-minimum cutoff $L<U$ can be proved with $L$ reachable by the lower-bound machinery | Derive the cutoff for one complete non-endpoint minimum class, including its degeneracies, before estimating total enumeration | A checked interval on which the class has no lower local minimum is a useful partial theorem. One exact original-program local minimum in that interval refutes the class claim; an unresolved stationary box does not. Global acceptance requires all classes. |
| G2: A redesigned mixed certificate at $U$ has a small enough nonnegative excess allowance to force a useful role profile | Freeze a core selector valid at $U$ and exact resource weights; first evaluate necessary endpoint controls and a small declared set of non-endpoint parent poses | A single undercharged admissible pose rejects the proposed coverage floor. Passing finite controls only admits a complete coverage pilot; it does not prove (5). The immediate question is whether the hoped-for profile survives its cheapest counterexamples. |
| G3: Joint corner/contact information removes a difficult pattern that unary conditioning preserves | Choose one complete positive-width two-parent adjacent-wall contact class, retain every contact-feature alternative, and compare its residual relaxation with the same class after dropping only shared contact | A complete conditional exclusion or exact surplus improvement isolates relational value. A mutually compatible parent/residual witness refutes only the proposed local incompatibility; a fractional survivor is a scoped obstruction. No global corner normal form is assumed. |
| G4: Every surviving non-endpoint pattern in one declared family has a certified descent or a side-preserving route to a descent exit | Construct one symbolic or interval-validated deformation family and check all physical inequalities; separate local descents from nonlocal routing | A uniform descent leaf removes local minima in that family. A verified local minimum refutes it; a failed first-order direction leaves higher-order motion open. A routing leaf only removes global minima unless local preservation is proved. |
| G5: Several valid charge profiles plus capacity constraints force an admitted endpoint neighborhood | On one complete retained coarse role family, solve the conservative count/assignment relaxation, then enclose all surviving geometry | Every surviving box must be wholly within a chart or separately closed. A feasible packing outside the charts refutes the capture statement; a surviving outer box merely leaves it unresolved. |
| G6: A small complete critical-value polynomial set exists after structural pruning | Implement one nontrivial typed branch with ties/abnormal controls; isolate every stationary component or prove a direct side inequality | Recovering the known Trump root alone is insufficient. A missing valid control branch rejects completeness; one fully closed non-endpoint branch gives an honest price for this architecture. |
| G7: Three-corner or corner-chain structure can replace a blind global pose search | Form a complete alternative by literal-corner count and adjacent-wall serving chains; derive one implication conditional on local or global minimality, with all complementary cases retained | A proved conditional cutoff is useful. Trump’s empty fourth corner already rejects an all-four premise. No current result forces exactly three literal corners, six zero tilts, five common tilts or a short chain. |

For G3, the known top-right pair in Trump is a necessary positive control: one parent
serves the top wall and one the right wall, and they physically contact while the
literal corner stays empty.
A model that excludes this pair at $U$ has lost valid geometry.
It can be compared with other two-parent contact cells without claiming that every
global minimum has this pair arrangement.

For G6, begin with the retained n3 sliding optimum, n4 point orbit and explicit abnormal
fixture as representation controls.
They test finite values with non-isolated configurations and the difference between
stationarity and minimization.
They are not measurements of n11 enumeration cost.
The first meaningful price comes from one fully specified n11 branch, including its open
boundary and tie obligations.

My preliminary assessment is that **resource profiles followed by minimum-specific
geometric exclusions** offers the best match to the new machinery.
It uses the complete lower certificate as a source of candidate difficult regions, while
requiring new valid charge floors at the stronger side.
The local-minimum cutoff gives a sharper end condition than trying to force uniqueness.
Generic root separation is a useful conceptual fallback and a possible final step after
pruning, but an unstructured full algebraic elimination is not presently a credible
first pilot.

## The Retained Tiny Audit

The question was declared before execution: check exact Trump corner and wall profiles,
the rational H-131 upper envelope, the wall-cap comparison, and the necessary $B\le A$
condition for the first unchanged source core at $A=L_0/U$. The ceiling was 15 seconds,
one process, with no search, certificate replay or geometry optimization.

The retained tool is
[`structural_endpoint_audit.py`](../../cases/w3_lower_bound_directions/structural_endpoint_audit.py).
It verifies the imported witness, number-field implementation and frozen certificate
bytes against a recorded immutable Git revision before and after the audit.
The source code uses the project Python 3.14 and exact algebraic comparisons; rational
enclosures are retained for every algebraic output.
It consumes the already verified Trump construction rather than independently replaying
the whole feasibility proof.

| Receipt | Runtime | Outcome |
| --- | ---: | --- |
| [Initial audit](../../cases/w3_lower_bound_directions/structural-endpoint-audit.json) | 0.129912 s | All exact decisions passed; its human-readable tiny-number decimal field is superseded as described below. |
| [Corrected display audit](../../cases/w3_lower_bound_directions/structural-endpoint-audit-corrected.json) | 0.125146 s | Same exact decisions, with explicit fixed-point Decimal approximations and rational enclosures. |

The first serializer called the retained number-field `decimal()` helper.
For the small difference $3877084/10^6-U$, its common-prefix string dropped the
scientific exponent; the exact enclosure was correct.
The scratch serializer was repaired to print a clearly labelled Decimal approximation
from the rational midpoint.
The initial receipt is retained as display-error evidence, not as a source for that
decimal. No shared numerical implementation was changed.
The corrected difference is approximately $4.0997718582269210\times10^{-7}$.

Run from the repository root with a fresh output filename:

```bash
PYTHONPATH=packing:packing/src packing/.venv/bin/python3 \
  packing/cases/w3_lower_bound_directions/structural_endpoint_audit.py \
  --repo . \
  --commit be736b0ef05ac2f256691bc3ded21873ad1f2ab1 \
  --output /private/tmp/w3-structural-endpoint-audit-fresh.json \
  --seconds 15
```

The raw receipts preserve the actual commands and source revision.
The first-row area failure is a useful negative about literal certificate reuse.
It does not reject the cutoff, a new parent/core selector, threshold repricing, or
global capture. No numerical lower bound was measured in this block.

## What Is Ready for Review

The new mathematical deductions to review are the finite-local-minimum-values argument,
the cutoff composition and its endpoint convention, the distinction between S1 on global
and local minima, the all-bracket contact count (3), the two slack modes and
capacity-saturation identity, and the complete-leaf composition.
The exact audit supports only the small endpoint/profile statements it tested.
The later structural extension adds the prior-work crosswalk, explicit distinctions
between angle classes and sliding or rigid assemblies, complete family-cover and
transition-map obligations, and the resource-forced tube alternative to H-121. It is
analytic consolidation; no additional spike, hypothesis promotion or numerical result
was produced.

The central open question is now concrete: **can the surviving minimum classes be given
explicit lower cutoffs whose maximum is below a lower bound we can certify?** A second
viable success condition is a complete capture or side-inequality proof for normalized
global minimizers, even if the stronger classification of all local minima is left open.
Neither condition currently has a completed global proof or a measured useful $L$.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
