# Certificate Mechanisms After the $n=11$ Fractional Ceilings

**Date:** September 10, 2026. **Entry:** W3 analytical exploration, X-027, session 126,
bead `think-jx95`. **Source baseline:** `e0c2583e`. **Status:** source synthesis and
reviewed analytical deductions; proposed numerical comparisons remain unrun.
No new placement search, linear program, coverage measurement, or packing bound is
reported.

The retained certificates suggest two immediate tests: improve the geometric conversion
from a core certificate to a unit-square bound, and test weighted site counts as a new
way to assign charge.
The first has a specific unmeasured candidate.
The second has exact counting proofs and retained candidate atoms, but its advantage in
the actual geometry remains to be established.

The current bounds on $s(11)$, the least container side that accommodates eleven unit
squares, remain

$$
3.826447410572939744\ldots\le s(11)\le3.877083590022814\ldots.
$$

This report defines the certificate objects first, distinguishes the mechanisms behind
previous gains, then derives and orders the proposed tests.
[X-027](../../../packing/campaign/explorations/X-027-stromquist-fractional-and-structural-strategy.md)
is the downstream synthesis and suggested reading entry.
It is not a mathematical premise of this report.

## Objects, Notation, and Logical Dependencies

### From physical squares to a core certificate

Let $K_L=[0,L]^2$ be a square container of side $L>0$. A **pose** specifies a square’s
center and orientation.
Write $S_p$ for the closed unit square in pose $p$. A **physical packing**
$\mathcal P=\{S_{p_1},\ldots,S_{p_{11}}\}$ consists of eleven squares contained in $K_L$
with pairwise disjoint interiors; their boundaries may touch.

A **strict core** $C_i$ is a closed smaller square lying in the interior of $S_{p_i}$.
Strict cores selected from a physical packing are therefore disjoint as closed sets.
For the finite-direction certificates considered here, an **admissible core** is a
closed square of a specified side $B>0$, contained in $K_L$, whose orientation belongs
to a specified finite set of directions, called a **direction net**. Its center still
ranges over every position allowed by containment.
A complete core certificate must cover that entire domain, not just sampled centers.
A separate geometric argument must select an admissible strict core in every physical
unit square.

A **site** is a fixed point of the container.
For a finite set of distinct sites $V$, a core’s **trace** is $T(C)=V\cap C$. Membership
includes the core’s boundary.
A Boolean trace is any subset of $V$; only some such subsets may be realized by
admissible cores.

An **atom** is a nonnegative charge function $f_j(C)$ with a justified **resource
budget** $b_j\ge0$ such that

$$
\sum_i f_j(C_i)\le b_j
$$

for every disjoint family of admissible closed cores.
The index $j$ labels atoms.
A **point atom** at a site $x$ has charge $\mathbf 1_{\{x\in C\}}$ and budget one, where
$\mathbf 1_E$ is one when condition $E$ holds and zero otherwise.
An **ordinary binary threshold atom** chooses a nonempty site support $R\subseteq V$ and
an integer threshold $k$ with $1\le k\le\lvert R\rvert$:

$$
f_{R,k}(C)=\mathbf 1_{\{\lvert R\cap C\rvert\ge k\}},
\qquad
b_{R,k}=\left\lfloor\frac{\lvert R\rvert}{k}\right\rfloor.
$$

Here $\lvert R\rvert$ counts distinct sites, and $\lfloor z\rfloor$ is the greatest
integer at most $z$. The budget is valid because disjoint closed cores cannot consume
the same site. An ordinary point atom is the case $\lvert R\rvert=k=1$.

Choose nonnegative atom coefficients $\alpha_j$ and form a combined charge $F$ with
universal budget $M$:

$$
F(C)=\sum_j\alpha_j f_j(C),
\qquad
M=\sum_j\alpha_j b_j.
$$

If $F(C)\ge1$ for every admissible core and $M<11$, eleven disjoint such cores cannot
exist. Together with strict core selection, this excludes a physical packing.
We call $F(C)\ge1$ **unit demand**. A **charge profile** can instead require different,
possibly larger, charges on different traces or classes of cores; this distinction
matters in the floor example below.

### Finite covering programs and fractional obstructions

A **linear program**, abbreviated LP, optimizes a linear expression subject to linear
inequalities. For a finite list of $N$ admissible cores and $J$ atoms, define the
$N\times J$ charge matrix $A$ by $A_{ij}=f_j(C_i)$. Let $b=(b_1,\ldots,b_J)^T$ be the
vector of resource budgets, $\alpha$ the column vector of atom coefficients, and
$\mathbf 1_N$ the vector of $N$ ones.
The finite covering problem and its dual are

$$
\begin{aligned}
\text{cover:}\quad&\min_{\alpha\ge0} b^T\alpha
&&\text{subject to }A\alpha\ge\mathbf 1_N,\\
\text{dual:}\quad&\max_{y\ge0}\mathbf 1_N^T y
&&\text{subject to }A^T y\le b.
\end{aligned}
$$

The superscript $T$ denotes transpose.
A dual vector $y=(y_1,\ldots,y_N)^T$ assigns nonnegative **fractional weights** to cores
that may overlap. Its total mass is $\sum_i y_i$. Each atom requires the capacity
inequality $\sum_i y_i f_j(C_i)\le b_j$. Every feasible covering budget is at least
every feasible dual mass, by multiplying and summing these inequalities.
For a feasible finite covering problem with finite optimum, finite LP duality also makes
the two optimum values equal and attained.
A finite cover still needs a complete coverage check on the omitted cores before it
becomes a global certificate.

With all point atoms allowed, the capacity condition is **point depth at most one**:

$$
\sum_i y_i\mathbf 1_{\{x\in C_i\}}\le1
\qquad\text{for every point }x\in K_L.
$$

A mass-eleven family satisfying this condition obstructs every point-only cover on that
core domain from having budget below eleven.
It obstructs a larger atom language only if it satisfies every additional capacity
inequality in that language.
A **cut** is such an added valid inequality; it may remove fractional families while
remaining valid for disjoint cores.
A **rank-one floor cut** applies one rounding step to a nonnegative combination of
point-resource inequalities.
An iterated floor construction applies rounding to previously justified integer charges.
A **closure** means the whole specified family of cuts, not merely the finite ones
returned by a search.

Two kinds of support must be distinguished: an atom’s site support is $R$, whereas a
finite dual’s placement support is its list of cores.
An upper bound for one placement support does not rule out another support.
When sources count atom **orbits**, an orbit consists of the distinct images of an atom
under the eight rotations and reflections of the square, the symmetry group $D_4$.
Weighted atom images must retain the site multiplicities as well as coordinates.

### Inputs and outputs

The derivations have the following dependencies.
The cited packets and admission records supply retained premises; the local counting and
finite LP arguments below do not rely on X-027’s conclusions.

| Input Premise | Output Used Here | Where the Argument Lives |
| --- | --- | --- |
| Retained T-022, T-024, T-025, and T-026 certificate packets, including the frozen T-018 premise | Which geometry, sites, coefficients, and counting rules changed; the current lower bound | [Retained gains](#what-produced-the-retained-gains) and the primary packets linked there |
| A5’s corrected finite-support calculation and A6’s admitted upper certificate and family checks | Obstructions and upper bounds at their stated atom, domain, and support scopes | [Ceiling families](#what-the-ceiling-families-require-us-to-change) |
| The fractional sibling’s rescaling of the retained 88-core family | A point-only obstruction for full unit squares at $L_*=38200/9977$ | [Fractional report, exact rescaling](research-2026-09-10-x027-fractional-duality.md#1-exact-rescaling-already-answers-the-mass-eleven-question); this is the only mathematical result imported from a sibling report |
| Distinct sites and disjoint closed cores; nonnegative integer site counts | Globally valid weighted and floor resource budgets; exact finite profile comparisons | [Integer multiplicities](#integer-site-multiplicities-and-genuine-floor-charges), proved locally; the retained weighted comparison is separately attributed to its review |
| A feasible finite covering LP with finite optimum and the same placement rows in both comparisons | The whole-optimal-face discriminator for new atoms | [Joint generation](#why-support-and-atom-generation-must-interact), proved locally using finite LP duality |
| A specified angle classification and an exact count premise for physical squares | A conditional certificate with different class demands | [Angle profiles](#angle-profiles-change-the-required-charge), using the cited strategy and H-131 premises |
| BC329’s source-bound preflight, followed by an as-yet unmeasured complete coverage decision | A possible geometric improvement only if the frozen packet passes | [Next checks](#discriminating-checks-and-allocation) |

The dependency on the fractional sibling is one-way: this report uses its unit-square
rescaling result, while that result does not require any weighted or floor construction
here. Its continuum strong-duality theorem is not needed for these finite LP arguments.
The [handoff](../../../SYNOPSIS.md#current-handoff),
[combined evidence](research-2026-09-09-n11-evidence-and-inference.md#12-the-combined-series-takeaways-and-open-comparisons),
and
[corrected X-024](../../../packing/campaign/explorations/X-024-two-lines-at-eleven.md#current-combined-reading--september-10-2026)
provide historical context and navigation.

The coordinator and structural-helper reviewer independently checked the five-site floor
table, its matching ordinary-atom upper construction, and the finite optimal-dual-face
argument. The structural-helper reviewer also checked the iterated-floor resource proof.
Those checks are assurance, not mathematical input or a dependency on the structural
sibling’s conclusions.

## What Produced the Retained Gains

Three changes can improve a core certificate: reduce the geometric loss in selecting a
strict core, improve the sites or relative atom coefficients, or strengthen the integer
counting rule that supplies an atom’s budget.
The retained sequence contains examples of all three.

| Result | Lower Bound | Mechanism That Changed | Evidence |
| --- | --- | --- | --- |
| T-018 | $3.81$ | A complete point cover on 1,121 retained sites, at core side $9977/10000$ and 181 directions, with total mass below eleven | The frozen source premises in [T-022](../../../packing/cases/n11_fractional_certificate/t-022-dilation-limit-proof.md#frozen-premise) give mass $434547/40000$ and least charge $4001/4000$. |
| T-022 | $3.810025723614703\ldots$ | Sharpened angular containment and uniform dilation of the same certificate | [The proof](../../../packing/cases/n11_fractional_certificate/t-022-dilation-limit-proof.md) changes no site, relative coefficient, or charge rule. |
| T-024 | $3.816609502788862\ldots$ | A 1440-step net, larger core side $2494953/2500000$, a measured minimum, common coefficient normalization, then dilation | [The proof](../../../packing/cases/n11_fractional_certificate/t-024-dilation-limit-proof.md) retains the same point coordinates and relative coefficients. |
| T-025 | $3.82$ | A new charge language: 584 point atoms and 320 two-of-three threshold atoms, with a complete cover and total budget $10.967322864$ | [The proof](../../../packing/cases/n11_threshold_certificate/t-025-threshold-certificate-proof.md) establishes the integer resource rule and both independent covering decisions. |
| T-026 | $3.826447410572939\ldots$ | Re-certification of T-025’s atoms on a 1440-step net at core side $249507/250000$, common normalization, then dilation | [The proof](../../../packing/cases/n11_threshold_certificate/t-026-dilation-limit-proof.md) retains the sites, thresholds, and relative coefficients. |

For fixed relative coefficients, let $M$ be their original resource budget and $m$ their
least charge over the proposed core domain.
A common positive multiplier $a$ exists exactly when $m>M/11$:

$$
\bigl(\exists a>0:\;a m\ge1\ \text{and}\ aM<11\bigr)
\quad\Longleftrightarrow\quad
m>\frac M{11}.
$$

When this holds, choosing $a=1/m$ gives minimum charge one and budget $M/m<11$. This
changes coefficients by a common factor; it does not optimize their ratios.

For uniform core side $B$, let $d$ be the absolute orientation mismatch between a
physical unit square and its selected net direction, reduced by square symmetry.
Let $D$ be the greatest value of $\tan d$ needed for nearest-direction selection; the
retained nets have $0\le d<\pi/4$ and $0\le D<1$. The width of a core across either
parent edge normal is $B(\cos d+\sin d)$. If the container, sites, and cores are all
dilated by a factor $q>0$, strict containment follows from

$$
qB\frac{1+D}{\sqrt{1+D^2}}<1.
$$

The corresponding supremum of excluded container sides is

$$
S=L\frac{\sqrt{1+D^2}}{B(1+D)}.
$$

This formula supplies geometric room for improvement, not coverage.
The covering decision must establish the premise at that particular $B$ and net.
Adding directions at unchanged $B$ adds constraints and can lower $m$. Increasing $B$
increases charge at each surviving center and removes some centers from the domain
allowed by containment.
T-024 and T-026 measured that tradeoff.
T-026’s 720- and 1440-step certificates have the same $B$, minimum, and coefficients, so
the extra gain between those records comes entirely from halving $D$.

T-025 supplies the separate combinatorial gain.
Three pairwise-overlapping cores with no common point can each carry fractional weight
$1/2$ under point-depth constraints.
If three sites can be chosen so that each core contains two of them, one two-of-three
atom charges all three but has budget one: two disjoint cores cannot both consume two of
three sites. The retained 88-core family violates a two-of-three inequality at charge
$5/4$. The accepted threshold certificate closes its declared core problem at $3.82$,
where that family obstructs point covers.
It does not exceed the separately transported full-unit point cap
$L_*=38200/9977\approx3.8288$ imported from the fractional sibling.
The original
[X-023 derivation](../../../packing/campaign/explorations/X-023-three-losses-and-a-new-atom.md#threshold-atoms)
and corrected X-024 distinguish these comparisons.

T-022, T-024, and T-026 exclude every side strictly below their limiting values.
By order completeness, they therefore prove the corresponding ordinary lower bounds on
$s(11)$. In particular, T-026 proves $s(11)\ge C$ at V4/C5, where
$C=3.826447410572939744\ldots$. Its argument does not establish the separate stronger
inequality $s(11)>C$. T-025 separately excludes the rational container side $191/50$
directly.

## What the Ceiling Families Require Us to Change

| Object | Supported Conclusion | Next Premise It Leaves Open |
| --- | --- | --- |
| The 88-core, mass-eleven family at $3.82$ | Point-depth constraints cannot give a budget below eleven on its stated core domain; threshold inequalities cut it | A different atom language, a changed domain, or changed core geometry |
| A5’s retained 88-placement supports | Complete budget-one cuts give exact optimum $32/3$; valid floor rows give an upper bound of ten for the full rank-one closure on those supports | A different placement support may still carry eleven; these upper bounds supply no global cover |
| A6’s 64-placement family at $153/40$ | Every point-depth inequality and all 2,566 retained ordinary atom orbits hold, at total weight eleven | Additional ordinary or weighted atoms; point-site additions alone cannot defeat this family with the fixed atom set and core domain |
| A6’s admitted seven-row upper certificate | Its 280-placement support cannot carry more than $2605263163/250000000\approx10.421052652$ under the admitted constraints | A different support may carry more; the larger covering program stayed numerically at eleven after the six ordinary atom additions |

The
[A5 correction](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a5-the-fixed-support-maximum-under-the-atom-classes.md)
and
[A6 admission](../../../packing/cases/n11_fractional_certificate/a6_dual_upper/README.md)
state the placement support and constraint scope.
A6’s displayed lower candidate has point depth greater than one, so it does not make the
admitted upper bound an exact full-depth optimum.
The
[later evidence account](research-2026-09-09-n11-evidence-and-inference.md#13-the-later-a6-and-h157-results-what-has-been-checked)
keeps those facts separate.

Each language extension must be checked against its own inequalities.
A depth-one family becomes an obstruction to a threshold cover only after every required
threshold inequality is checked.
Conversely, an integral packing of admissible cores, with weight one on each core,
satisfies every valid packing-capacity inequality, including iterated or geometric ones.
Changing charge syntax cannot remove such a witness without changing the admissible
domain or core construction.

Conditioning restricts the admissible configurations by additional physical information.
For example, an **owner** of a marked site is a selected core containing it; its
physical unit-square parent also contains the site.
A **class** groups assignments or poses satisfying specified restrictions; a **patch**
is a planar region guaranteed to lie inside every owner core in the class.
The corrected
[X-026 ladder](../../../packing/campaign/explorations/X-026-what-conditioning-does-and-does-not-buy.md#3-the-ladder)
prevents transferring an unconditional core witness to such a restricted domain without
checking its owners, classes, patches, and all additional restrictions.

## Integer Site Multiplicities and Genuine Floor Charges

Give each distinct site $s\in V$ a positive integer multiplicity $a_s$. These are
labelled tokens at the same coordinate: a core contains all tokens at that site or none.
Let $H$ be the total number of tokens and $h(C)$ the number inside a core:

$$
H=\sum_{s\in V}a_s,
\qquad
h(C)=\sum_{s\in V\cap C}a_s.
$$

For a positive integer threshold $t$, define

$$
f_{\mathrm{binary}}(C)=\mathbf 1_{\{h(C)\ge t\}},
\qquad
f_{\mathrm{floor}}(C)=\left\lfloor\frac{h(C)}t\right\rfloor.
$$

Both have the valid resource budget $\lfloor H/t\rfloor$. For disjoint closed cores
$C_i$, no token is consumed twice, so

$$
\sum_i h(C_i)\le H,
\qquad
\sum_i\left\lfloor\frac{h(C_i)}t\right\rfloor
\le\left\lfloor\frac{\sum_i h(C_i)}t\right\rfloor
\le\left\lfloor\frac Ht\right\rfloor.
$$

The binary charge is at most the floor charge, proving its budget too.
The two charges coincide when $H<2t$. This is the retained seven-token, threshold-four
case: its weighted five-site candidates need only a binary representation with
multiplicities. The
[weighted-atom review](../reviews/review-2026-09-10-n11-weighted-five-site-atoms.md)
specifies that bounded admission: preserve multiplicities under symmetry, reject
malformed encodings, implement two independent covering checks, and replay each reported
$3/2$ violation against its exact source family.
Those source violations are not newly admitted measurements here.

That review proves an abstract cost ratio of $4/3$. The weighted pattern $(2,2,1,1,1)$
with threshold four has budget one, whereas ordinary binary atoms on those same five
sites need budget $4/3$ to charge every positive Boolean trace by one.
This does not establish that the necessary traces occur at the retained coordinates,
that additional ordinary sites cannot remove the advantage, or that the geometric
covering program improves.

A small intermediate test could resolve the first gap.
For one fixed weighted pattern and its coordinates, determine the traces realized by
admissible cores on the declared net and center domain, then minimize the budget of
ordinary atoms that dominate its charge on those traces.
There are at most $2^5=32$ traces and exactly 80 ordinary atom types on five sites:

$$
\sum_{\varnothing\ne R\subseteq\{1,\ldots,5\}}\lvert R\rvert
=5\cdot2^4=80.
$$

Each nonempty support $R$ contributes one type for each allowed threshold.
A verified ordinary mixture costing at most one on the complete realizable trace
inventory removes this pattern’s expressive advantage on that domain.
The replacement mixture could still supply useful ordinary columns missing from the
current program. An exact dual lower bound above one, supported on traces with exact
realizing core witnesses, proves that a local expressive advantage survives the
geometry. This positive direction needs only its witnessed traces; the no-advantage
direction needs the complete trace universe.
Neither establishes a full covering-budget gain or compares atoms on additional sites.
This is a proposed maintained-tool comparison, not a performed measurement.

### A Separate Five-Site Floor Example

This analytical example isolates a reason to consider charges above one after weighted
binary admission. It concerns all Boolean traces, with no square-realizability claim.
Let $V$ consist of five distinct sites and prescribe

$$
f(T)=\left\lfloor\frac{\lvert T\rvert}{2}\right\rfloor
\qquad(T\subseteq V).
$$

One unweighted floor atom has budget two.
For clarity, the exact comparison is the finite covering problem

$$
\begin{aligned}
\min_{\alpha_{R,k}\ge0}\quad&
\sum_{\varnothing\ne R\subseteq V}\sum_{k=1}^{\lvert R\rvert}
\alpha_{R,k}\left\lfloor\frac{\lvert R\rvert}{k}\right\rfloor\\
\text{subject to}\quad&
\sum_{\varnothing\ne R\subseteq V}\sum_{k=1}^{\lvert R\rvert}
\alpha_{R,k}\mathbf 1_{\{\lvert R\cap T\rvert\ge k\}}
\ge\left\lfloor\frac{\lvert T\rvert}{2}\right\rfloor
\qquad(T\subseteq V).
\end{aligned}
$$

Its optimum is $5/2$. A point coefficient of $1/2$ at each site attains this value
because $\lvert T\rvert/2\ge\lfloor\lvert T\rvert/2\rfloor$.

For the matching lower bound, assign auxiliary weight $3/20$ to each of the ten two-site
traces and $1/10$ to each of the five four-site traces, with zero weight on all other
traces. The total auxiliary mass is two.
Permutation symmetry makes an ordinary atom’s auxiliary charge depend only on its
support size $r=\lvert R\rvert$ and threshold $k$. The full capacity check is:

| Support Size $r$ | Threshold $k$ | Resource Budget $\lfloor r/k\rfloor$ | Exact Auxiliary Charge |
| --- | --- | --- | --- |
| $1$ | $1$ | $1$ | $1$ |
| $2$ | $1$ | $2$ | $31/20$ |
| $2$ | $2$ | $1$ | $9/20$ |
| $3$ | $1$ | $3$ | $37/20$ |
| $3$ | $2$ | $1$ | $19/20$ |
| $3$ | $3$ | $1$ | $1/5$ |
| $4$ | $1$ | $4$ | $2$ |
| $4$ | $2$ | $2$ | $7/5$ |
| $4$ | $3$ | $1$ | $1/2$ |
| $4$ | $4$ | $1$ | $1/10$ |
| $5$ | $1$ | $5$ | $2$ |
| $5$ | $2$ | $2$ | $2$ |
| $5$ | $3$ | $1$ | $1/2$ |
| $5$ | $4$ | $1$ | $1/2$ |
| $5$ | $5$ | $1$ | $0$ |

For example, a three-site, threshold-two atom charges three two-site traces and all five
four-site traces, giving $3(3/20)+5(1/10)=19/20$. A point atom charges four traces of
each size, giving one.
For either trace size $\ell\in\{2,4\}$, the number charged is

$$
N_{r,k,\ell}=\sum_{j=k}^{\ell}\binom rj\binom{5-r}{\ell-j}.
$$

The binomial coefficient $\binom ab$ counts subsets of size $b$ in a set of size $a$; it
is zero for $b<0$ or $b>a$. The exact auxiliary charge is
$(3/20)N_{r,k,2}+(1/10)N_{r,k,4}$. Every row is at most its resource budget; atoms of
budget at least two are also bounded by the total auxiliary mass two.
The weighted demand of the prescribed profile is

$$
10\frac3{20}\cdot1+5\frac1{10}\cdot2=\frac52.
$$

Multiplying each trace constraint in the displayed primal by its auxiliary weight and
summing proves the lower bound $5/2$. Together with the point construction, this proves
the stated exact optimum.

The cost ratio $(5/2)/2=5/4$ concerns domination of a profile that sometimes demands
charge two.
If only charge one were required on traces of size at least two, the ordinary
two-of-five atom would already cost two.
Thus the example supplies no unit-demand or geometric improvement by itself.
It identifies additional charge that a floor atom can supply under one shared budget.

For integer $h\ge0$ and threshold $t\ge1$, the identity

$$
\left\lfloor\frac ht\right\rfloor
=\sum_{j\ge1}\mathbf 1_{\{h\ge jt\}}
$$

is useful for evaluation; only finitely many terms are nonzero.
Pricing every level separately loses the joint budget.
For five unit tokens and $t=2$, the threshold-two and threshold-four atoms separately
cost $2+1=3$, while the single floor resource costs two.
A producer and verifier must retain the joint resource proof when expanding the charge
into simpler terms.

### Tighter Budgets and Higher-Rank Candidates

Token division gives a sufficient budget, which need not be the smallest valid one.
Sites are indivisible, so fewer disjoint winning subsets may exist than the token bound
allows. For multiplicities $(3,3,2)$ and threshold four, the token bound is two, but
every winning subset uses at least two of the three sites.
At most one disjoint winning subset is possible.
This function is just an ordinary two-of-three atom with budget one; the tighter
accounting gives no new expressive advantage in this example.

More generally, let $f:2^V\to\mathbb R_{\ge0}$ be a trace function with
$f(\varnothing)=0$. Here $2^V$ is the set of all subsets of $V$. Assume $f$ is
**monotone**: $T\subseteq U$ implies $f(T)\le f(U)$. Its resource capacity is the
maximum of $\sum_i f(T_i)$ over families of pairwise disjoint subsets of $V$. Every
disjoint core family satisfies that budget, because its traces are disjoint.
For $U\subseteq V$, this capacity can be computed recursively:

$$
\beta(\varnothing)=0,
\qquad
\beta(U)=\max_{\varnothing\ne T\subseteq U}
\bigl(f(T)+\beta(U\setminus T)\bigr)
\quad(U\ne\varnothing).
$$

Nonnegativity and monotonicity allow unused sites to be assigned to a part without
reducing the sum, so optimizing partitions suffices.
For five sites this is a small exact subset recurrence.
It is a possible admission check for proposed budgets, not a reason to implement
arbitrary trace functions before testing the retained weighted patterns.

An iterated floor rule also has a direct global validity proof.
Suppose nonnegative integer-valued charges $f_j(C)$ have integer budgets $b_j$ valid for
every disjoint core family.
For nonnegative rational multipliers $\eta_j$, define

$$
g(C)=\left\lfloor\sum_j\eta_j f_j(C)\right\rfloor,
\qquad
b_g=\left\lfloor\sum_j\eta_j b_j\right\rfloor.
$$

Then

$$
\sum_i g(C_i)
\le\left\lfloor\sum_j\eta_j\sum_i f_j(C_i)\right\rfloor
\le\left\lfloor\sum_j\eta_j b_j\right\rfloor=b_g.
$$

Starting from point indicators gives the rank-one construction defined above.
Applying the rule to earlier integer charges gives an iterated construction; it does not
by itself prove that the result lies outside every lower-rank class.
Every coefficient is evaluated on the actual core, so the proof covers all admissible
poses. A valid inequality only on sampled placement rows is insufficient for this use.

If the input charges depend monotonically on finitely many site memberships, so does
$g$. For a fixed direction, the site-entry and site-exit boundaries divide the permitted
center domain into finitely many regions with constant traces, including their boundary
cases. An exact covering algorithm can check those regions, while an independent
implementation can evaluate traces directly and bound charges on intervals of centers.
Encoding size, sufficient integer range to avoid overflow, and that independent lower
bound still need admission.
Negative charges or multipliers need a different resource and boundary argument.
The existing [plateau reader](../../../packing/devtools/plateau_reader.py) searches
bounded rank-one candidates; a negative search does not certify the whole closure.
A higher-rank pilot should name one retained family and one explicit derived cut, verify
its global integer-resource proof, and demonstrate an exact violation before
commissioning a broader hierarchy.

## Why Support and Atom Generation Must Interact

In the finite programs defined above, an atom is a column and a placement is a row.
Adding an atom adds a dual capacity constraint and can decrease the minimum covering
budget. Adding an omitted placement adds a coverage constraint and can increase it.
Both may be needed; only a complete coverage decision converts the resulting cover into
a global certificate.
**Pricing** an atom means looking for one whose capacity is violated by the current
fractional family. Point pricing looks for a site of depth greater than one.

A6 gives an exact reason to add atoms before repeating arbitrary point-site growth with
its old atom set. It does not justify abandoning point pricing after that set changes.
A replacement fractional family may have depth above one at an unpriced site.
The unchanged numerical objectives after valid cuts in A4 and A6 illustrate why the
replacement families must also be retained and inspected; they do not certify exact ties
by themselves.

There is an exact finite test for whether new atom columns improve the old optimum.
Let $v$ be that optimum, and let $E$ be the matrix of new atom charges on the same $N$
placement rows, with new budget vector $e\ge0$. The new optimum is strictly below $v$ if
and only if the following system is infeasible:

$$
y\ge0,
\qquad A^Ty\le b,
\qquad E^Ty\le e,
\qquad\mathbf 1_N^Ty=v.
$$

The **old optimal dual face** is the set of all old feasible dual vectors attaining $v$;
it may contain many vectors.
The system asks whether any member of that whole set survives every new constraint.
The old covering problem is assumed feasible with finite optimum.
Adding finitely many nonnegative-cost columns preserves feasibility and a finite
optimum. Finite duality and attainment therefore imply:

- A surviving old optimum remains feasible in the new dual, forcing the new value to
  equal $v$.
- If the new value equals $v$, an attained new dual optimum is a surviving old optimum.

An exact feasible vector proves a finite tie; an exact infeasibility witness proves a
strict finite decrease.
Cutting the one dual returned by a solver is insufficient, because another old optimum
may survive. Neither conclusion decides omitted placements.

The first weighted comparison should follow the
[weighted review’s common-matrix contract](../reviews/review-2026-09-10-n11-weighted-five-site-atoms.md#a-valid-common-finite-comparison).
Use a reproducible union of placement rows, common point sites, common ordinary atoms,
and weighted columns only in the treatment program.
If weighted sites become point columns, include them in the control too.
An exact feasible treatment cover gives an upper bound $U_{\mathrm{treat}}$ on its
finite optimum; an exact feasible control dual gives a lower bound
$L_{\mathrm{control}}$ on the control optimum.
The strict comparison

$$
U_{\mathrm{treat}}<L_{\mathrm{control}}
$$

proves a finite budget improvement.
Both witnesses need independent checking.
A printed decimal tie or zero coefficients on new columns is insufficient.

After that comparison, a separately declared procedure can alternate between adding
violated placement rows, optimizing again, and pricing sites or atoms against the new
fractional family. Keep every exact witness and distinguish a family with proved full
depth from a numerical source used only to suggest new constraints.
Fix the rule for choosing the next operation before comparing procedures.
Translating all sites and placement rows together from the $3.825$ container into the
$3.83$ container preserves their finite incidence matrix.
It provides no test of newly permitted boundary placements; those need row generation or
the complete covering check.

## Angle Profiles Change the Required Charge

A simple direction-dependent point construction has no advantage under its usual safe
budget. To see this, let $w_s(\theta)\ge0$ be the weight at site $s$ when a core has
orientation $\theta$, and let $\overline w_s=\sup_\theta w_s(\theta)$ be finite.
The safe budget is $\sum_s\overline w_s$, since each site can belong to at most one
disjoint core. Replacing every directional weight by the constant $\overline w_s$ weakly
increases all charges at the same budget.
This domination applies to that construction; it does not rule out using a proved
restriction on the numbers of physical squares in different angle classes.

Keep one universal charge $F(C)$ and its budget $M$. Partition admissible cores into
$r+1$ classes indexed by $j=0,\ldots,r$ and require $F(C)\ge d_j$ in class $j$, where
$d_j\ge0$ is the class demand.
Suppose every physical square has a specified selected core and assigned class, with
exact count profile $(n_0,\ldots,n_r)$, so $\sum_j n_j=11$. Then the eleven selected
cores satisfy

$$
\sum_{i=1}^{11} F(C_i)\ge\sum_{j=0}^r n_jd_j.
$$

Thus $M<\sum_j n_jd_j$ excludes that profile.
All classes use the same resource inequalities and the same budget; sites are not
assigned separate, unjustified budgets for each class.

For the proposed two-class profile $(9,2)$, normalize demands by

$$
d_0,d_1\ge0,
\qquad9d_0+2d_1=1,
\qquad M<1.
$$

A zero demand for one class is allowed because the specified profile still forces
sufficient charge in the other.
Without any count restriction, minimizing over every eleven-square profile gives only
$11\min_j d_j$, recovering the unconditional requirement.
The possible gain comes from the count premise.

The
[September 10 strategy review](../reviews/review-2026-09-10-n11-strategy-frontier.md#5-mixed-charges-for-a-partial-angle-profile)
proposes a point-only control and ordinary-threshold treatment for this profile.
Both programs must use the same placement rows, point sites, and assigned classes, and
**both must optimize $d_0,d_1$ under the same normalization $9d_0+2d_1=1$**. The
treatment alone receives the additional threshold columns.
Comparing fixed uniform demands in the control against adjustable demands in treatment
would confound the atom change with the demand change.
This comparison can use existing two-of-three atoms without waiting for multiplicity
admission.

Read the exact angle cells and count premises from
[H-131](../../../packing/campaign/hypotheses/H-131-near-axis-counts-at-q.md), not
rounded angle descriptions.
An angle cell is a specified interval of physical orientations, with its endpoint
assignment stated. Every physical square must receive a class under the actual
core-selection and tie convention.
Full coverage of both class domains remains separate from the finite comparison.
It yields a conditional exclusion only with $M<1$ and the stated count premise.
A global result must cover every allowed profile or prove that every remaining physical
packing falls into an excluded case.
The old grid-79 point programs neither establish nor refute this paired mixed-demand
comparison.

Direction-dependent core sizes are a separate geometric possibility.
Suppose angle cell $I_j$ uses representative direction $\theta_j$ and core side $B_j$.
For physical orientation $\theta\in I_j$, let $d$ be its absolute mismatch from
$\theta_j$, reduced by square symmetry to $0\le d\le\pi/4$. After a common geometric
dilation $q>0$, a sufficient transfer condition is

$$
qB_j(\cos d+\sin d)<1
\qquad\text{for every }\theta\in I_j.
$$

This also requires complete coverage for every pair $(\theta_j,B_j)$ and a complete
assignment of physical orientations to cells.
It avoids combining the worst core side from one direction with the worst mismatch from
another. No gain is measured here, and a failed uniform-core packet would not settle it.

## Discriminating Checks and Allocation

The ordering below is a feasibility judgment about bounded deliverables, not a measured
productivity comparison.
Each numerical target needs prospective registration by the coordinator and a maintained
runner.

| Direction | Cheapest Useful Next Check | What a Positive Result Would Establish | Stop or Scope Boundary |
| --- | --- | --- | --- |
| BC329 uniform core/net packet | Admit its fixed-core runner, then decide the frozen candidate using the original T-025 coefficients and $m>M/11$ | With both complete coverage routes and dilation replay, a stronger exact lower bound | The candidate limit is conditional on unmeasured coverage; a valid core of charge at most $M/11$ rejects only this fixed packet. |
| Weighted binary atoms | Admit exact multiplicities and replay the retained source pairs; test the at-most-32-trace, 80-ordinary-atom comparison before a large paired LP | Valid representation first, possible local geometric expressiveness second, and a finite budget gain only after the paired comparison | The abstract $4/3$ ratio and reported source charge $3/2$ do not predict geometric or global improvement. |
| Joint row and atom generation | Check whether any exact old optimal dual survives all new columns; retain the replacement family | Why the fixed finite objective stays or moves, and which constraint type remains violated | An exact tie concerns that finite program; omitted placements can change the result. |
| Genuine floor atoms | Admit one explicit retained floor resource with its joint budget; use the five-site profile as an exact control | A charge above one and, if exhibited, an exact violation by the matched family | The $5/4$ example concerns profile domination, not unit-demand or geometric gain. |
| Mixed angle-profile demand | A common $(9,2)$ point-only versus threshold comparison, with both programs optimizing the same class demands | A finite gain; a conditional exclusion only after complete class coverage and $M<1$ | Count premises, physical assignment, remaining profiles, and coverage remain explicit. |
| Higher-rank floor construction | One globally justified composition with integer budgets and a matched exact violating family | A sound useful cut outside the chosen existing finite set, if that separation is checked | A bounded search does not exhaust rank one; iterating a rule alone does not prove a higher-rank advantage. |

For BC329, the [preflight](../reviews/review-2026-09-10-n11-bc329-packet-preflight.md)
fixes the original T-025 coordinates, thresholds, and relative coefficients in
[`certificate.json`](../../../packing/cases/n11_threshold_certificate/certificate.json).
The acceptance threshold uses that original charge scale:

$$
L=\frac{191}{50},
\qquad M=\frac{685457679}{62500000},
\qquad B=\frac{9981}{10000},
\qquad\frac M{11}=\frac{685457679}{687500000}.
$$

The candidate has a 2880-step net with worst mismatch tangent $D=207107/1440000000$. Its
geometric limiting side is

$$
S=3.826721480476156460\ldots,
$$

conditional on the required coverage.
The least charge $m$ must be measured using those original coefficients; normalization
then multiplies all coefficients by $1/m$. Using T-026’s already normalized absolute
coefficients would require the corresponding changed budget and acceptance threshold,
rather than mixing the two source scales.

An exact admissible core of original-weight charge at most $M/11$ rejects this fixed
relative-weight packet, including at equality because the resource-budget condition is
strict. Charge below one alone does not reject it if it remains above $M/11$. A timeout
or incomplete interval check leaves the question unresolved; mismatched source bytes
invalidate the comparison rather than deciding it.
Failure at this one core side does not eliminate a larger core side with remaining
geometric room on the same net.

The missing bounded fixed-core runner is a prerequisite.
The existing adaptive net-refinement command performs a different experiment.
Increasing the core side preserves the coverage of the old directions on the smaller
admissible-center domain; the inserted directions introduce the unknown obligations.
Final retention still requires both complete coverage routes, including the reflected
interval net, on the same normalized bytes, followed by dilation replay.
Neither those coverage measurements nor a new target run occurred in this review.

Weighted binary admission is the next certificate-language block because it has retained
candidates, an exact budget proof, and a small comparison that can distinguish it from
ordinary thresholds.
Genuine floor and iterated charges should follow specific useful resources, keeping
profile expressiveness, separation of a fractional family, finite budget gain, and
complete geometric gain as separate outcomes.
Structural helper work remains a parallel route: actual contact, simultaneous
feasibility of physical parents, and justified assignment of owners supply information
absent from a single-core charge language.
The corrected conditional obstructions do not close that route.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
