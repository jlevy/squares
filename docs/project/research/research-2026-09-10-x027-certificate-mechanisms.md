# Certificate Mechanisms After the N11 Fractional Ceilings

**Date:** September 10, 2026. **Entry:** W3 analytical exploration, X-027, session 126,
bead `think-jx95`. **Source baseline:** `e0c2583e`. **Status:** source synthesis and
reviewed analytical deductions; proposed numerical comparisons remain unrun.
No new placement search, LP, coverage measurement, or packing bound is reported.

The coordinator and structural-helper lane independently checked the five-site floor
table, its matching ordinary-atom upper construction, and the finite optimal-dual-face
argument. The structural-helper lane also checked the iterated-floor resource proof.
Their reviews found no correction to those deductions at the scopes stated below.

The retained gains support two different next moves.
One frozen core/net packet can test a small further improvement using the existing
certificate language.
Weighted site multiplicities can test a new integer counting rule against a common
finite control. The fractional ceiling families make arbitrary point-site additions
insufficient when the atom set and core domain are held fixed; they leave changed atoms,
changed core geometry, and coupled parent restrictions open.
The next atom experiment must allow for a replacement fractional family after the first
is cut.

The current lower bound remains T-026’s `3.826447410572939744...`; the upper
construction remains `3.877083590022814...`. The
[current handoff](../../../SYNOPSIS.md#current-handoff),
[combined evidence](research-2026-09-09-n11-evidence-and-inference.md#12-the-combined-series-takeaways-and-open-comparisons),
and
[corrected X-024](../../../packing/campaign/explorations/X-024-two-lines-at-eleven.md#current-combined-reading--september-10-2026)
govern the historical interpretations used below.

## What Produced the Retained Gains

A certificate has two obligations.
It must charge every admissible closed core, and the total charge that disjoint cores
can collect must be below eleven.
A strict containment argument puts one such core inside each hypothetical unit square.
Three changes can improve the result: reduce the loss in that containment step, improve
the placement or relative weights of the atoms, or strengthen the integer resource rule
that assigns their budgets.

| Result | Lower Bound | Mechanism That Changed | Evidence |
| --- | --- | --- | --- |
| T-018 | `3.81` | A complete point cover on 1,121 retained sites, at core side `9977/10000` and 181 directions, with total mass below eleven | The frozen source premises in [T-022](../../../packing/cases/n11_fractional_certificate/t-022-dilation-limit-proof.md#frozen-premise) give mass `434547/40000` and least charge `4001/4000`. |
| T-022 | `3.810025723614703...` | Sharpened angular support containment and uniform dilation of the same certificate | [The proof](../../../packing/cases/n11_fractional_certificate/t-022-dilation-limit-proof.md) changes no site, relative weight, or charge rule. |
| T-024 | `3.816609502788862...` | A 1440-step net, larger core side `2494953/2500000`, a measured minimum, common weight normalization, then dilation | [The proof](../../../packing/cases/n11_fractional_certificate/t-024-dilation-limit-proof.md) retains the same point coordinates and relative weights. |
| T-025 | `3.82` | A new charge language: 584 point atoms and 320 two-of-three threshold atoms, with a complete cover and total budget `10.967322864` | [The proof](../../../packing/cases/n11_threshold_certificate/t-025-threshold-certificate-proof.md) establishes the integer resource rule and both covering decisions. |
| T-026 | `3.826447410572939...` | Re-certification of T-025’s atoms on a 1440-step net at core side `249507/250000`, common normalization, then dilation | [The proof](../../../packing/cases/n11_threshold_certificate/t-026-dilation-limit-proof.md) retains the sites, thresholds, and relative weights. |

For fixed relative weights, write `M` for their original resource budget and `m` for
their least charge on the proposed core domain.
A common positive rescaling works exactly when `m > M/11`: choosing `alpha=1/m` then
gives minimum one and budget `M/m < 11`. The geometric dilation limit for a uniform core
side `B` and worst half-gap tangent `D` is

$$
S=L\frac{\sqrt{1+D^2}}{B(1+D)}.
$$

This formula alone proves no improvement.
The coverage decision supplies the missing premise at that particular `B` and net.
Increasing the number of directions at unchanged `B` adds constraints and can lower `m`;
increasing `B` increases charge and removes some boundary placements from the
admissible-center domain.
T-024 and T-026 measured that tradeoff.
T-026’s 720- and 1440-step certificates have the same `B`, minimum, and weights, so the
extra gain between those two records comes entirely from halving `D`.

T-025 supplies the separate combinatorial gain.
Three pairwise-overlapping cores with no common point can carry fractional weight one
half each under point-depth constraints.
If three sites can be chosen so that each core contains two of them, one two-of-three
atom charges all three but has budget one: two disjoint cores cannot both consume two of
three sites. The retained 88-core family violates a two-of-three inequality at charge
`5/4`. The accepted threshold certificate closes the declared core problem at `3.82`,
where that family obstructs point covers.
It does not exceed the separately transported unit-scale point cap near `3.8288`. The
original
[X-023 derivation](../../../packing/campaign/explorations/X-023-three-losses-and-a-new-atom.md#threshold-atoms)
and corrected X-024 distinguish those comparisons.

T-022, T-024, and T-026 exclude every side strictly below their limiting values.
Their strict core-containment argument does not decide the limiting endpoint.
T-025 retains its direct certificate at the rational container side `191/50`.

## What the Ceiling Families Require Us to Change

| Object | Supported Conclusion | Next Premise It Leaves Open |
| --- | --- | --- |
| The 88-core, mass-eleven family at `3.82` | Point-depth constraints cannot give a budget below eleven on its stated core domain; threshold inequalities cut it | A different atom language, a changed domain, or changed core geometry |
| A5’s retained 88-placement supports | Complete budget-one cuts give exact optimum `32/3`; the valid floor rows give an upper bound of ten for the full rank-one closure on those supports | A different placement support may still carry eleven; these upper bounds supply no global cover |
| A6’s 64-placement family at `153/40` | Every point-depth inequality and all 2,566 retained ordinary atom orbits hold, at total weight eleven | Additional ordinary or weighted atoms; point-site additions alone cannot defeat this fixed atom set |
| A6’s admitted seven-row upper certificate | Its 280-placement support cannot carry more than `2605263163/250000000`, approximately `10.421052652`, under the admitted constraints | A different support can; the larger covering program stayed numerically at eleven after the six ordinary atom additions |

The
[A5 correction](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a5-the-fixed-support-maximum-under-the-atom-classes.md)
and
[A6 admission](../../../packing/cases/n11_fractional_certificate/a6_dual_upper/README.md)
state the support and row scope.
A6’s displayed lower candidate has depth greater than one, so it does not make the
admitted upper bound an exact full-depth optimum.
The
[later evidence account](research-2026-09-09-n11-evidence-and-inference.md#13-the-later-a6-and-h157-results-what-has-been-checked)
keeps those two facts separate.

Each language extension must be checked against its own inequalities.
A depth-one family is a point-cover obstruction; it becomes a threshold-cover
obstruction only after every required threshold inequality is checked.
Conversely, an integral packing of admissible cores satisfies every valid
packing-capacity inequality, including higher-rank or geometric ones.
A new syntax cannot remove such a witness without changing the admissible domain or the
core construction. The corrected
[X-026 ladder](../../../packing/campaign/explorations/X-026-what-conditioning-does-and-does-not-buy.md#3-the-ladder)
also prevents transferring an unconditional core witness into an owner-conditioned
domain without verifying its owners, classes, patches, and additional restrictions.

## Integer Site Multiplicities and Genuine Floor Charges

Let each distinct site `s` carry a positive integer multiplicity `a_s`. These are
labelled tokens at the same coordinate; a core contains either all tokens at that site
or none. Put `A=sum_s a_s` and `h(P)=sum_{s in P} a_s`. For a positive integer threshold
`t`, both charge rules

$$
f_{\rm binary}(P)=\mathbf1_{h(P)\ge t},\qquad
f_{\rm floor}(P)=\left\lfloor\frac{h(P)}t\right\rfloor
$$

have the valid resource budget `floor(A/t)`. For disjoint closed cores,
`sum_i h(P_i) <= A`, and hence

$$
\sum_i\left\lfloor\frac{h(P_i)}t\right\rfloor
\le\left\lfloor\frac{\sum_i h(P_i)}t\right\rfloor
\le\left\lfloor\frac At\right\rfloor.
$$

The floor charge dominates the binary charge at the same budget.
They coincide when `A<2t`. This is exactly the retained seven-token, threshold-four
case: its two weighted five-site candidates require only a binary representation with
multiplicities. The
[weighted-atom review](../reviews/review-2026-09-10-n11-weighted-five-site-atoms.md)
already specifies that bounded admission, including weighted symmetry keys, strict
decoding, two independent covering implementations, and matched source replay of the
reported `3/2` violations.

The review proves an abstract `4/3` advantage: the weighted pattern `(2,2,1,1,1)`,
threshold four, costs one, while ordinary binary atoms on the same five sites need
budget `4/3` to charge all its positive traces by one.
That theorem concerns all Boolean traces.
It does not prove that the necessary traces occur at the retained coordinates, that more
ordinary sites cannot remove the advantage, or that the larger geometric covering
program improves.

A small intermediate discriminator could test that first gap directly.
For one frozen weighted motif, determine the traces realized by admissible cores on the
declared net and center domain, then minimize the budget of ordinary atoms dominating
its charge on those traces.
There are at most 32 traces and exactly 80 nonempty-support ordinary atom types, since
`sum_{S subset {1,...,5}} |S| = 5*2^4`. A verified ordinary mixture of cost at most one
on the complete trace inventory removes this motif’s expressive advantage on that
domain. A dual lower bound above one, supported on traces with exact realizing core
witnesses, proves that a local advantage survives the geometry.
The positive direction needs only its witnessed traces; the no-advantage direction needs
complete coverage of the trace universe.
Neither proves a gain in the full covering program or compares atoms on additional
sites. This is a proposed maintained-tool comparison, not a performed measurement.

### A Separate Five-Site Floor Example

The following analytical deduction isolates the reason to consider genuine floor charges
after weighted binary admission.
It is a finite Boolean comparison, with no square-realizability claim.

On five distinct sites, require the charge profile

$$
f(T)=\left\lfloor\frac{|T|}{2}\right\rfloor
\quad\text{for every trace }T.
$$

One unweighted floor atom has resource budget two.
Any nonnegative combination of ordinary binary threshold atoms on those same five sites
that dominates this entire profile has budget at least `5/2`. Point weights one half on
each site attain that upper bound, since `|T|/2 >= floor(|T|/2)`.

For the lower bound, assign auxiliary mass `3/20` to each of the ten two-site traces and
`1/10` to each of the five four-site traces.
Its total mass is two.
Permutation symmetry makes the charge depend only on the atom’s support size `r` and
threshold `k`. These are all permitted cases:

| Support Size `r` | Threshold `k` | Resource Budget `floor(r/k)` | Exact Auxiliary Charge |
| --- | --- | --- | --- |
| 1 | 1 | 1 | `1` |
| 2 | 1 | 2 | `31/20` |
| 2 | 2 | 1 | `9/20` |
| 3 | 1 | 3 | `37/20` |
| 3 | 2 | 1 | `19/20` |
| 3 | 3 | 1 | `1/5` |
| 4 | 1 | 4 | `2` |
| 4 | 2 | 2 | `7/5` |
| 4 | 3 | 1 | `1/2` |
| 4 | 4 | 1 | `1/10` |
| 5 | 1 | 5 | `2` |
| 5 | 2 | 2 | `2` |
| 5 | 3 | 1 | `1/2` |
| 5 | 4 | 1 | `1/2` |
| 5 | 5 | 1 | `0` |

For example, a three-site, threshold-two atom charges three two-site traces and all five
four-site traces, giving `3(3/20)+5(1/10)=19/20`. A point atom charges four traces of
each size, giving one.
For every row, the counts are `sum_{j=k}^2 C(r,j)C(5-r,2-j)` among two-site traces and
`sum_{j=k}^4 C(r,j)C(5-r,4-j)` among four-site traces, with out-of-range binomial
coefficients zero. In particular, every atom of budget at least two is also bounded by
the auxiliary family’s total mass two.
Thus every ordinary atom satisfies its capacity inequality, while the required profile
has weighted demand

$$
10\frac3{20}\cdot1+5\frac1{10}\cdot2=\frac52.
$$

Summing the capacity inequalities proves the lower bound.
The resulting `5/4` cost ratio is about domination of a profile that sometimes requires
charge two. If the sole requirement were charge one on traces of size at least two, the
ordinary two-of-five atom would already have budget two.
The example therefore does not demonstrate a better unit-demand cover by itself.
It identifies extra charge that a floor atom can supply to rows sharing the same
resource budget.

The identity `floor(h/t)=sum_{j>=1}[h>=jt]` is useful for evaluation but loses that
joint budget if every level is separately priced.
With five unit tokens and `t=2`, separately buying the threshold-two and threshold-four
atoms costs three; the single floor resource costs two.
A producer and verifier must preserve the joint resource proof when expanding its charge
into simpler terms.

### Tighter Budgets and Higher-Rank Candidates

Token division gives a sufficient budget.
Sites are indivisible, so the exact maximum number of disjoint winning site subsets can
be smaller.
For example, multiplicities `(3,3,2)` and threshold four have token bound two
but permit at most one disjoint winning subset: every winning subset uses at least two
of the three sites. This rule is just an ordinary two-of-three atom with its correct
budget one; the tighter accounting creates no new expressive advantage here.

More generally, for a nonnegative monotone trace function `f` with `f(empty)=0`, define
its resource capacity as the maximum of `sum_i f(T_i)` over disjoint subsets of its
finite site set. Every disjoint core family satisfies that budget.
It can be evaluated by `beta(empty)=0` and
`beta(U)=max_{empty != T subset U}(f(T)+beta(U\T))`; monotonicity and nonnegativity
allow unused sites to be assigned to a part without decreasing the sum.
For a five-site motif this is a small exact subset recurrence.
This is a possible admission control for proposed budgets, not a reason to implement an
arbitrary truth-table language before the retained weighted motifs are tested.

A higher-rank floor rule can also retain a direct global validity argument.
Suppose already justified nonnegative integer-valued charges `f_j(P)` satisfy
`sum_i f_j(P_i)<=b_j` for every disjoint core family, with integer budgets `b_j`. For
nonnegative rational multipliers `lambda_j`, define

$$
g(P)=\left\lfloor\sum_j\lambda_j f_j(P)\right\rfloor,
\qquad
b_g=\left\lfloor\sum_j\lambda_j b_j\right\rfloor.
$$

Then `sum_i g(P_i)<=b_g`, by summing before the final floor.
Starting from point indicators gives a rank-one floor construction; applying it to
earlier integer charges gives an iterated construction.
Every coefficient remains a function of the actual core, rather than a coefficient
attached only to a sampled placement.
This is the necessary provenance for using such a cut in a continuum certificate.
A valid inequality on a finite placement support alone does not provide it.

If the input charges are monotone functions of finitely many site memberships, so is
`g`. The same finite event arrangement can decide it, with an independent direct
evaluation of each trace.
Representation size, exact integer headroom, and an independent interval lower bound
still need admission.
Negative charges or multipliers require a different boundary and resource argument.
The existing [plateau reader](../../../packing/devtools/plateau_reader.py) searches
bounded rank-one candidates; a negative search is not a certificate that all rank-one
cuts hold.
A higher-rank pilot should therefore name one retained family and one explicit
derived cut, verify its integer resource proof, and demonstrate an exact violation
before commissioning a wider hierarchy.

## Why Support and Atom Generation Must Interact

A finite covering LP minimizes resource budget over atom columns, requiring charge one
on its current placement rows.
Its dual puts fractional weights on those placements, subject to the current atom
inequalities. Adding a new atom cuts dual solutions and can decrease the minimum budget.
Adding a previously missing placement adds a coverage constraint and can increase it.
Both operations can be needed to reach a complete certificate; only complete coverage
makes the covering objective a global bound of the required kind.

A6 supplies an exact reason to add atoms before repeating arbitrary point-site growth
with its old atom set.
It does not justify abandoning point pricing after the atom set changes.
The replacement family may have depth above one at an unpriced site.
A4’s and A6’s unchanged numerical objectives after valid cuts show why one should also
retain and inspect the replacement families.

There is a precise finite discriminator for the common failure mode.
Suppose the old finite LP has exact optimum `v`. The new atom columns improve that
optimum strictly if and only if no old optimal dual remains feasible for all the new
columns. In exact finite notation, the question is feasibility of

$$
y\ge0,\qquad A^Ty\le c,\qquad C_{\rm new}^Ty\le c_{\rm new},
\qquad\mathbf1^Ty=v.
$$

Here `A` is the old row-by-atom charge matrix and `c` its resource costs.
This equivalence assumes the old covering problem is feasible with a finite optimum;
adding finitely many nonnegative-cost columns preserves that property, and finite LP
duality and attainment apply.
A violated atom removes the particular dual that priced it.
It need not remove the rest of the optimal face.
An exact feasible `y` in the displayed system proves a finite tie; an exact
infeasibility witness proves that the finite optimum decreases.
Neither decides omitted placements.

The first new comparison should follow the
[weighted review’s common-matrix contract](../reviews/review-2026-09-10-n11-weighted-five-site-atoms.md#a-valid-common-finite-comparison).
Use a reproducible row union, common point sites, common ordinary atoms, and weighted
columns only in treatment.
If weighted sites become point columns, include them in both arms.
Strict improvement requires an independently checked treatment primal upper bound below
a control dual lower bound.
A printed decimal tie or zero weights on new columns is insufficient.

After that comparison, a separately declared alternating procedure can add violated
placement rows, reoptimize, and price point sites or atoms against the new family.
Retain every exact witness and distinguish a fractional family with proved full depth
from a numerical separation source.
Freeze the rule that chooses the next operation before comparing procedures.
Translating every row and site from `3.825` to `3.83` preserves the finite matrix
exactly and provides no test of newly admitted boundary placements; those need their own
row generation or the complete covering gate.

## Angle Profiles Change the Required Charge

An unconditional point weight depending on direction has a safe budget given by the sum
of each site’s maximum directional weight.
Replacing each directional weight by that maximum weakly increases every charge at the
same budget. That particular construction gives no advantage.
It does not rule out a certificate that uses a proved restriction on the numbers of
squares in different angle classes.

Keep one universal resource charge `c(P)` with budget `M`, and require `c(P)>=d_j` for
every admissible core in class `j`. If a physical packing has exact count profile
`(n_0,...,n_r)`, its total charge is at least `sum_j n_j d_j`. Thus `M<sum_j n_j d_j`
excludes that profile.
This uses the same resource inequalities for all classes; no site is sold repeatedly
with separate unjustified budgets.

For the proposed `(9,2)` profile, normalize `9d_0+2d_1=1`, with nonnegative demands, and
seek `M<1`. A zero demand for one class is permitted only because the stated profile
still forces enough charge in the other.
Without a restriction on counts, minimizing over all eleven-square profiles gives only
`11 min_j d_j`, recovering the ordinary unconditional requirement.
The potential gain comes from the count theorem.

The
[September 10 strategy review](../reviews/review-2026-09-10-n11-strategy-frontier.md#5-mixed-charges-for-a-partial-angle-profile)
proposes a common point-only control and ordinary-threshold treatment for that one
profile. It can use the existing two-of-three language without waiting for multiplicity
admission. Read the exact angle cells and count premises from
[H-131](../../../packing/campaign/hypotheses/H-131-near-axis-counts-at-q.md), not
rounded angle descriptions.
Every physical square needs an assigned class under the actual core-selection and tie
convention. Full coverage of both class domains is separate from the finite comparison.
A global result needs every allowed count profile covered, or sufficient routing to an
excluded profile. The old grid-79 point programs neither establish nor refute that mixed
comparison.

Direction-dependent core sizes are another distinct question.
If source angle cell `I_j` uses direction `r_j` and core side `B_j`, a sufficient
transfer condition is `lambda B_j(cos d+sin d)<1` throughout `I_j`, together with
complete coverage at each `(r_j,B_j)` and complete angle-cell assignment.
This avoids combining the worst core size from one direction with the worst mismatch
from another. No gain has been measured for it here, and a failed uniform packet would
not settle it.

## Discriminating Checks and Allocation

The ordering below is a feasibility judgment about the next bounded deliverables, not a
measured productivity comparison.
Each numerical target needs the coordinator’s prospective registration and a maintained
runner.

| Direction | Cheapest Useful Next Check | What a Positive Result Would Establish | Stop or Scope Boundary |
| --- | --- | --- | --- |
| BC329 uniform core/net packet | After runner admission, decide the one frozen candidate at `B=9981/10000`, 2880 steps, using `m>M/11` and common normalization | With both complete coverage routes and dilation replay, the proposed stronger weak limit | Exact headroom `3.826721480476156460...` is conditional; no candidate coverage has been measured in this review. An escape at charge `<=M/11` rejects only this packet. |
| Weighted binary atoms | Admit exact multiplicities and replay the two retained motif-family pairs; then compare common finite programs | Correct representation first; a strict finite budget improvement only after rational witness separation | The abstract `4/3` advantage and reported source charge `3/2` do not predict geometric improvement. |
| Joint row and atom generation | Inspect whether an exact old optimal dual survives the new columns; retain the replacement source | Why the fixed finite objective stays or moves, and which constraint type is still violated | An exact tie concerns that finite program; a new support can change it. |
| Genuine floor atoms | Admit one explicit retained floor resource, preserving its joint budget; use the five-site profile as an exact control | A representable charge above one and a verified matched-family violation | The `5/4` toy ratio concerns profile domination, not a unit-demand or geometric gain. |
| Mixed angle-profile demand | One exact common `(9,2)` point-only versus threshold comparison with fixed class assignments | A finite gain; a conditional exclusion only after complete class coverage and budget below one | Remaining profiles, physical assignment, and domain coverage stay explicit. |
| Higher-rank floor construction | One explicit composition with integer budgets and a matched exact violating family | A sound cut outside the chosen existing finite set | No exhaustion claim from a bounded rank-one search; no hierarchy campaign before a useful cut is exhibited. |

The [BC329 preflight](../reviews/review-2026-09-10-n11-bc329-packet-preflight.md) has
already checked the candidate’s geometric headroom and normalization rule.
Its missing fixed-core runner remains a prerequisite.
The existing adaptive net refinement CLI is a different experiment.
The inserted directions are the unknown coverage obligations: old directions remain
covered when the core grows, but the final retention still needs both complete routes on
the same normalized bytes.

Weighted binary admission is the next certificate-language block because it has retained
candidates, an exact budget proof, and a finite control that can distinguish it from
ordinary thresholds.
Genuine floor and higher-rank charges should follow specific separated resources, rather
than expand the verifier before those resources show a useful effect.
Structural helper work remains a parallel route: actual contact, joint parent
feasibility, and owner routing impose information absent from a single-core charge
language, and the corrected conditional obstructions do not close that route.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
