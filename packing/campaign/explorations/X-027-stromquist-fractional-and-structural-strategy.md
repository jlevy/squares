---
title: X-027 — fractional obstructions and structural proof mechanisms
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-027
  title: Fractional Obstructions and Structural Proof Mechanisms
  date: '2026-09-10'
  author: GPT-6 Astra coordinator, with independent Astra mathematical lanes
  campaign: packing.squares
  brief: >-
    The owner requested a new analytical exploration after Stromquist's September 7
    and 9 correspondence was archived in PR153. Explain the recent certified advances,
    examine the structural constraints that open other proof routes, develop
    fractional-packing and related mathematical ideas in independent spikes, and
    consolidate a strategic comparison with explicit evidence, falsifiers and next steps.
  sources:
  - SYNOPSIS.md
  - packing/campaign/ideas.md
  - packing/resources/private-correspondence/email-stromquist-2026-09-07.md
  - packing/campaign/explorations/X-023-three-losses-and-a-new-atom.md
  - packing/campaign/explorations/X-026-what-conditioning-does-and-does-not-buy.md
  - docs/project/research/research-2026-09-09-n11-evidence-and-inference.md
  - docs/project/research/research-2026-09-10-x027-fractional-duality.md
  - docs/project/research/research-2026-09-10-x027-structural-helpers.md
  - docs/project/research/research-2026-09-10-x027-certificate-mechanisms.md
  proposes: []
---
# X-027: Fractional Obstructions and Structural Proof Mechanisms

This exploration asks how to prove that eleven unit squares cannot fit in a given square
container, allowing the small squares to rotate and touch but not overlap in their
interiors. It explains the recent progress, develops consequences of Stromquist’s
suggestions, and selects the next questions worth testing.

## Reading Order and Proof Dependencies

**Start here for definitions and strategy.** The three companion research reports supply
the detailed arguments.
Each defines its own notation, so a reader following a proof link does not need to
reconstruct definitions from another report.

| Document | Read it for | Inputs on which its arguments depend | What this exploration takes from it |
| --- | --- | --- | --- |
| [Fractional packing and duality](../../../docs/project/research/research-2026-09-10-x027-fractional-duality.md) | Weighted families of overlapping squares, the limitation of point covers, and continuous duality | The retained 88-core family and exact verification; BC242’s boundary convention; T-025 only for the comparison with its core model | Exact transport to unit squares, equality of specified packing and covering values, and the limits of finite-witness claims in §2 |
| [Certificate mechanisms](../../../docs/project/research/research-2026-09-10-x027-certificate-mechanisms.md) | What improved the bounds, stronger counting rules, and tests for a useful new rule | T-018–T-026 and their certificates; the A6 finite-model records; direct counting and finite linear-programming arguments. The full-unit point-cover limitation uses the fractional report’s transport result | The historical mechanism account in §1 and the charge comparisons in §3 |
| [Structural helpers](../../../docs/project/research/research-2026-09-10-x027-structural-helpers.md) | Consequences of corner-mark ownership, shared unit-square parents, and contacts | BC303’s admitted point cover; exact square geometry; S1’s translation normal form for the contact-component consequence | The ownership, wall, contact, and joint-compatibility deductions in §4 |
| This exploration, X-027 | How the arguments fit together and which experiment should follow | The three reports above and the [corrected historical evidence account](../../../docs/project/research/research-2026-09-09-n11-evidence-and-inference.md) | The ranked choices and reopening conditions in §§5–6; these are research judgments |

The logical direction is **retained evidence → a report’s derivation → this synthesis →
a proposed test**. Reading order starts with this synthesis and follows links outward;
that does not reverse the proof dependencies.
A link back here supplies orientation, not a premise.
The reports’ reciprocal reviews are checks on their reasoning, not premises in one
another’s proofs.
The specific one-way use of the fractional transport in the certificate
report concerns the limitation of point covers; its counting lemmas do not depend on
that transport.

The certificate report’s
[input/output table](../../../docs/project/research/research-2026-09-10-x027-certificate-mechanisms.md#inputs-and-outputs)
enumerates the additional A5, weighted-atom, BC329, and angle-count premises used in its
individual comparisons; the table above is a reading map rather than an exhaustive
source list.

The
[correspondence](../../resources/private-correspondence/email-stromquist-2026-09-07.md)
and earlier explorations X-023 and X-026 motivate questions.
Exact certificates, admitted geometric statements, and the displayed derivations supply
evidence for answers.
Identifiers beginning `T-` refer to retained frontier statements; `BC` labels refer to
declared work items or contracts, whose admission status must be checked; `exp` labels
refer to experiment records.
An identifier alone does not confer proof status.

## Foundations and Common Notation

### Squares, poses, and cores

For a real side length $L\geq 1$, let $K_L=[0,L]^2$ be the closed container.
A **pose** $p=(z,\theta)$ specifies a centre $z\in\mathbb R^2$ and an angle $\theta$,
understood modulo $\pi/2$ because a quarter-turn gives the same square.
If $R_\theta$ denotes rotation by $\theta$, the posed unit square is

$$
S_p=z+R_\theta[-1/2,1/2]^2.
$$

The pose is **legal** when $S_p\subseteq K_L$; $P_L$ is the set of legal poses.
Write $S_p^\circ$ for the interior, obtained by deleting the boundary.
A **physical packing** $\mathcal P=(S_{p_1},\ldots,S_{p_n})$ has legal poses and
$S_{p_i}^\circ\cap S_{p_j}^\circ=\varnothing$ whenever $i\ne j$. Its squares may touch.
The quantity we want to bound is

$$
s(n)=\inf\{L:\text{a physical packing of }n\text{ unit squares exists in }K_L\}.
$$

A **strict core** is a closed square $C_i$ of side $B<1$ contained in $S_{p_i}^\circ$;
the unit square $S_{p_i}$ is its **parent**. Strict cores from distinct parents in a
packing are disjoint even on their boundaries.
An **angular net** is a finite list of allowed core orientations.
A containment argument must show that every legal unit-square pose has a selected core
in the proposed core domain, denoted $\mathcal C$. Finer nets can permit larger $B$. A
**dilation** multiplies every length by the same positive factor; it converts a
certified core exclusion into an exclusion for unit squares in a correspondingly scaled
container.

### Covers, charges, and fractional packings

A **point measure** assigns nonnegative weight to points.
For a finite site set $F$, write $\mu=\sum_{x\in F}w_x\delta_x$, where $w_x\geq0$ and
$\delta_x$ is one unit of mass at $x$. Its charge on a core is
$\mu(C)=\sum_{x\in F\cap C}w_x$, and its total mass is $M=\mu(K_L)$. An **ordinary point
cover** has $\mu(C)\geq1$ for every $C\in\mathcal C$. Disjoint cores consume disjoint
point weights, so $n$ selected cores would imply

$$
n\leq\sum_{i=1}^n\mu(C_i)\leq M.
$$

Thus $M<n$, together with the containment argument, excludes $n$ unit squares.
A general nonnegative measure can spread weight continuously; a **density** $\rho$
assigns $\mu(E)=\int_E\rho(x)\,dx$ to a region $E$, where $dx$ is planar area and
$\rho\geq0$. Boundary conventions for such measures are specified in §2.

A more general **charge atom** is a nonnegative function $f_j(C)$ with a proved
**budget** $b_j$: every allowed disjoint core family satisfies
$\sum_i f_j(C_i)\leq b_j$. Nonnegative coefficients $\alpha_j$ give a combined charge
$g(C)=\sum_j\alpha_j f_j(C)$ and budget $M=\sum_j\alpha_jb_j$. A **covering
certificate** proves both $g(C)\geq1$ throughout its stated domain and $M<n$. An
unconditional certificate covers a selectable core for every physical pose; a
conditional certificate requires additional geometric premises, which must be justified
before it can exclude a physical packing.

A **fractional packing** instead allows overlapping squares $Q_i$ with weights
$\lambda_i\geq0$. Under the closed-square convention its **point depth** and **mass**
are

$$
d(x)=\sum_i\lambda_i\mathbf 1_{\{x\in Q_i\}}\leq1,
\qquad v=\sum_i\lambda_i.
$$

Here $\mathbf 1_{\{\cdot\}}$ is $1$ when the stated condition holds and $0$ otherwise.
If a point cover charges every $Q_i$ by at least $1$, then

$$
v\leq\sum_i\lambda_i\mu(Q_i)
=\int d(x)\,d\mu(x)\leq M.
$$

This is an **obstruction** to a point cover of mass below $v$, even when the $Q_i$ do
not form a physical packing.
The relaxation retains point capacities while forgetting some relations among whole
squares. A **strict physical integrality gap** at mass $n$ means that the fractional
problem admits mass at least $n$ at a side where a physical packing of $n$ unit squares
is impossible. The core model and the unit-square model have different domains; a gap in
one does not automatically prove a gap in the other.

An **owner** of a marked site is a selected core containing that site; its unit-square
parent must also contain the site.
A conditional **owner selection** chooses specified owners at the container’s corners.
Later sections define contact components, site traces, thresholds, and linear programs
at their first use. Symbols such as $M$ denote a budget for the particular certificate
under discussion, not one constant shared by every example.

## Outcome and Evidence Status

A covering proof past $L_* = 38200/9977$ needs a counting rule or a geometric relation
that ordinary point depth forgets.
Recent work has made both kinds of progress: threshold charges produced T-025, and owner
restrictions produced T-023’s conditional exclusion.
Finer angular containment then carried the threshold certificate to T-026. The threshold
and ownership rules are defined in §§3–4.

**Entry: W3 analytical exploration**, requested after the correspondence review, under
`think-jx95` and
[Session 126](../agent-sessions/session-126-stromquist-analytical-exploration.md).
The source baseline is `e0c2583e`, the merge of PR153. Three independent mathematical
lanes produced retained derivations and counterexamples, then cross-reviewed them.
Their new lemmas are independently reviewed arguments within this exploration; they are
not registered frontier results or claims of novelty.
No numerical target was run and no new packing bound is asserted.
The bracket remains

$$
3.826447410572939744\ldots \leq s(11)
\leq 3.877083590022814\ldots.
$$

The most consequential deductions are:

- The retained 88-core obstruction scales exactly to **full unit squares** of fractional
  mass $11$ at $L_* = 38200/9977$, approximately $3.8288$. It obstructs arbitrary
  unconditional point measures at that side and above, without a symmetry assumption.
  A new search for such a witness at $3.83\leq L\leq3.85$ is unnecessary.
- An open-interior formulation gives a self-contained strong-duality argument, including
  equality with the continuous-density problem.
  Passing from dots to arbitrary density therefore does not evade that obstruction.
- At side $q=96/25$, a hypothetical packing must contain at least **seven of eight
  specified corner marks** in its selected cores.
  After a permitted translation of its squares, it has at most **three groups connected
  by touching squares**, so a contact path joins parents whose cores contain marks from
  different corners. These strengthen the inputs available to a helper argument.
- A five-site example separates a floor charge from every mixture of ordinary threshold
  charges by an exact factor $5/4$ for a specified demand profile.
  Whether square geometry retains such an advantage is a well-defined next test.

## 1. What the Recent Results Actually Improved

The core-covering method has three distinct opportunities: lose less in selecting the
cores, cover them more efficiently, or use a stronger rule for sharing resources.

| Retained result | Lower bound | What changed |
| --- | --- | --- |
| T-018 | $3.81$ | A complete ordinary point cover on 1,121 retained sites |
| T-022 | $3.810025723614703\ldots$ | Sharper angular containment and dilation of the same certificate |
| T-024 | $3.816609502788862\ldots$ | A finer net, larger cores, measured coverage, and common normalization of the same relative point weights |
| T-025 | $3.82$ | A new integer counting rule: point atoms plus two-of-three threshold atoms |
| T-026 | $3.826447410572939\ldots$ | Re-certification of those threshold atoms on a finer net, followed by dilation |

The
[certificate analysis](../../../docs/project/research/research-2026-09-10-x027-certificate-mechanisms.md#what-produced-the-retained-gains)
links each exact proof and distinguishes direct rational-side exclusions from limiting
dilation statements.
T-022, T-024, and T-026 prove ordinary exact lower bounds.
In particular, T-026 proves $s(11)\ge C=3.826447410572939744\ldots$ at V4/C5. The
separate strict inequality $s(11)>C$ remains unproved; this does not qualify the lower
bound.

For frozen relative weights, let $M$ be their original total resource budget and
$m=\inf_{C\in\mathcal C}g(C)$ the least charge on the proposed core domain.
The infimum is the greatest lower bound, whether or not some core attains it.
Common normalization succeeds exactly when $m>M/11$: multiply every weight by $1/m$. The
remaining geometric gain depends on core side and angular gaps.
A finer net’s geometric headroom is not a coverage result.

That is why **BC329 remains the next direct-bound target**. Its frozen $B=0.9981$,
2880-step packet has a geometric limit $3.826721480476156460\ldots$, but coverage is
unmeasured. It first needs the admitted bounded runner and the exact comparison of raw
least charge with $M/11=685457679/687500000$. The existing adaptive refinement CLI
performs a different experiment.
See the
[packet preflight](../../../docs/project/reviews/review-2026-09-10-n11-bc329-packet-preflight.md).
This remains worthwhile as a bounded continuation of a mechanism that has worked.

The structural line has a different achievement: **T-023 excludes one specified
four-owner branch at $3.84$**. Its exact full-net cover and geometric transfer are
retained. A global theorem still needs to show that every physical packing admits a
selection belonging to an excluded branch.
Later wall footprints enlarged twelve of sixteen classes, but exp147’s containment test
added no selection. Those outcomes do not measure the productivity of the two lines
against each other.

The
[combined evidence account](../../../docs/project/research/research-2026-09-09-n11-evidence-and-inference.md#12-the-combined-series-takeaways-and-open-comparisons)
is the historical authority.
X-027 adds deductions and prospective discriminators to that corrected account.

## 2. What Stromquist’s Fractional Suggestion Settles

### The full-unit obstruction is already retained by exact transport

The archived
[September 7 and 9 correspondence](../../resources/private-correspondence/email-stromquist-2026-09-07.md)
suggests weighted families of squares with depth at most one.
Such a family can obey every point capacity even though its squares cannot all occur in
one physical packing.
Integrating any point cover against the family bounds the cover’s total weight below.

The existing exact family has 88 closed squares of side $B=9977/10000$ in container side
$191/50$, each of weight $1/8$, with closed depth at most one everywhere.
Scaling all positions and sides by $1/B$ gives unit squares in

$$
L_* = \frac{191/50}{9977/10000} = \frac{38200}{9977}
< \frac{383}{100}.
$$

The scaled family still has total weight eleven and closed depth at most one.
Any nonnegative point measure covering every legal unit square must therefore have mass
at least eleven. This includes asymmetric measures: in the full-unit problem, all the
family’s actual orientations are legal, so the old folded-net symmetry qualification is
unnecessary.
The same obstruction applies to any sound unconditional point-core selection
rule, since selecting a core inside each unit square only decreases depth.

The
[fractional derivation, §1](../../../docs/project/research/research-2026-09-10-x027-fractional-duality.md#1-exact-rescaling-already-answers-the-mass-eleven-question)
retains the source and independent certificate receipt.
A directly consumable full-unit export would be useful engineering; another existence
search at $3.83\leq L\leq3.85$ would not.

**A strict physical integrality gap remains unproved.** The current physical lower bound
lies below $L_*$. To prove that the fractional relaxation actually permits more squares
than physical packing at $L_*$, we still need a physical exclusion there.
A global lower bound strictly above $L_*$, for example $3.83$, would establish both a
stronger bound and this gap.
T-025 already demonstrates a matched gap in its declared closed-core model; the
unit-square statement is separate.

### Continuous density has the same optimum under a precise convention

The legal pose space $P_L$ is **compact**: every sequence of poses has a subsequence
converging to a legal pose.
Use **interior incidence** $A(x,p)=\mathbf 1_{\{x\in S_p^\circ\}}$, which records
whether the point $x$ lies strictly inside the square at pose $p$. A pose measure
$\lambda$ assigns weight to families of legal poses, extending the finite sums above.
A point measure $\mu$ assigns covering weight in $K_L$. Define

$$
\begin{aligned}
\nu_\circ(L)
&=\sup_{\lambda\geq0}
\left\{\lambda(P_L):
\int_{P_L}A(x,p)\,d\lambda(p)\leq1\quad\forall x\in K_L\right\},\\
\tau_\circ(L)
&=\inf_{\mu\geq0}
\left\{\mu(K_L):
\int_{K_L}A(x,p)\,d\mu(x)\geq1\quad\forall p\in P_L\right\}.
\end{aligned}
$$

The supremum is the least upper bound of feasible packing masses.
Let $\tau_{\mathrm{fin}}(L)$ be the covering infimum restricted to finite sums of point
masses, and $\tau_{\mathrm{ac}}(L)$ the infimum restricted to densities.
The subscript $\mathrm{ac}$ means **absolutely continuous** with respect to area: a
region of zero area receives zero measure, and the measure has a density.
All these definitions use nonnegative finite measures and the same interior convention.

The independently reviewed argument gives

$$
\nu_\circ(L)=\tau_\circ(L)=\tau_{\mathrm{fin}}(L)=\tau_{\mathrm{ac}}(L).
$$

This is **strong duality**: the greatest feasible packing mass equals the least possible
covering cost. The density value agrees with the existing BC242 contract.
The packing supremum is **attained**, meaning some feasible measure achieves it; no
covering optimizer or finite optimal packing is asserted.

The proof has four substantive steps.
Compactness gives a finite set of points hitting every pose interior, which uniformly
bounds packing mass.
Interior point capacities are closed conditions under **weak convergence**, which means
convergence of integrals of every continuous test function.
Finite sets of point constraints give finite **linear programs** (LPs): optimization
problems with linear objectives and inequalities.
Their variables group poses by **incidence masks**, the subsets of those points lying
inside a pose. Compactness and finite LP duality identify their limiting value with the
full problem. Finally, after discarding unused boundary atoms, a finite atomic cover has
a uniform usable interior margin over the compact pose space, so its atoms can be
smeared into densities at no larger cost.
Tonelli’s theorem, which permits interchanging nonnegative integrals, and **lower
semicontinuity**, here the fact that a strict depth violation persists near a point,
also show that closed depth at most $1$ **almost everywhere** (except on a set of area
zero) is equivalent to interior depth at most $1$ everywhere.
Full proofs and boundary counterexamples are in
[§§2–4 of the fractional analysis](../../../docs/project/research/research-2026-09-10-x027-fractional-duality.md#2-the-measure-spaces-and-the-boundary-convention).

This answers the value-equality part of the continuous question under explicit
hypotheses. It does not classify equality at the best retained construction side
$3.877083590022814\ldots$ associated with Walter Trump, compute the optimum at any new
side, or pair singular closed-square covers with almost-everywhere capacities.
Touching edges make that last combination unsound.

A second lemma supplies finite rational $k$-fold witnesses after **arbitrarily small
side enlargement**. Such a witness is a finite multiset of rationally described squares
with at most $k$ copies covering any point; assigning each copy weight $1/k$ yields a
fractional packing. Rational description uses rational centre coordinates and rational
rotation matrices. The proof shrinks a finite partition of pose space to strictly
interior representative cores, rationalizes with margin, and dilates.
Exact-side finite attainment is not proved.
The retained family already supplies a concrete $k=8$ witness at $L_*$.

## 3. Stronger Charges: Test Expressiveness Before a Large Covering Run

Fix a finite site set $F$. The **trace** of a core $C$ is $T(C)=F\cap C$, the subset of
sites it contains; $\lvert T\rvert$ denotes the number of sites in a subset $T$. A
**realizable trace** occurs for some core in the stated geometric domain.
An abstract or **Boolean trace** is any subset $T\subseteq F$, without requiring
geometric realization.

An ordinary point atom is $f_x(C)=\mathbf 1_{\{x\in C\}}$, with budget $1$. For
$r=\lvert F\rvert$ and an integer threshold $1\leq k\leq r$, an **ordinary threshold
atom** is

$$
f_{F,k}(C)=\mathbf 1_{\{\lvert T(C)\rvert\geq k\}},
\qquad b_{F,k}=\left\lfloor\frac rk\right\rfloor.
$$

The floor $\lfloor a\rfloor$ is the greatest integer no larger than $a$. Each charged
core consumes at least $k$ distinct sites, so at most $\lfloor r/k\rfloor$ disjoint
cores receive this charge.
It uses indivisibility of site consumption, which fractional point depth alone forgets.
The retained **non-Helly** three-square example has pairwise intersections but no common
intersection of all three squares.
Its exact rational unit-square coordinates permit fractional mass $3/2$, while a
two-of-three site capacity is $1$.

The A6 plateau shows why merely finding one violated atom is insufficient.
A $64$-placement family of mass $11$ satisfies all point capacities and all $2{,}566$
retained atom orbits on its declared domain.
An **orbit** groups atoms related by the rotations and reflections of the container; the
reported count uses the A6 contract’s symmetry convention.
Additional point sites cannot defeat that catalog.
Later cuts certified the upper bound $2605263163/250000000$, approximately
$10.421052652$, on a different, fixed $280$-placement support; the larger covering LP
stayed numerically at $11$. Its displayed lower candidate also violates full point
depth, so it is not a new fractional packing.
The [A6 admission](../../cases/n11_fractional_certificate/a6_dual_upper/README.md)
preserves these scopes.

### Weighted binary atoms and floor atoms ask different questions

Give each site $x\in F$ a positive integer **token count** $a_x$, which allows one site
to contribute more than one unit of resource.
Let $t$ be a positive integer threshold, $h(C)=\sum_{x\in F\cap C}a_x$ the tokens inside
a core, and $A=\sum_{x\in F}a_x$ the total tokens.
The two globally valid charges are

$$
f_{\mathrm{bin}}(C)=\mathbf 1_{\{h(C)\geq t\}},\qquad
f_{\mathrm{floor}}(C)=\left\lfloor\frac{h(C)}{t}\right\rfloor,
\qquad b=\left\lfloor\frac A t\right\rfloor.
$$

Disjoint core traces consume disjoint site tokens, proving both budgets.
The existing weighted motif $(2,2,1,1,1)$ at threshold four has only seven tokens, so
binary and floor charges coincide there.
Its abstract $4/3$ gain tests multiplicities, not genuinely multilevel floor values.

The new five-site example uses $f(T)=\lfloor\lvert T\rvert/2\rfloor$ on all Boolean
traces $T\subseteq F$, where $\lvert F\rvert=5$. This is a **demand profile**: the
required charge depends on the trace, and can exceed $1$. One floor atom has budget $2$.
Every nonnegative mixture of ordinary threshold atoms on those same five sites
dominating this profile costs at least $5/2$, and point weights $1/2$ at each site
attain it. An explicit fifteen-trace dual witness, a feasible weighting of the demand
constraints that certifies a lower bound on cost, proves the lower bound.
Here **domination** means charging every trace by at least its demanded amount.
This is an exact profile-domination separation of $5/4$; rows of demand $2$ are
essential. It is not a measured improvement of a unit-demand square-cover LP. The
[certificate analysis](../../../docs/project/research/research-2026-09-10-x027-certificate-mechanisms.md)
gives the complete capacity table and proof.

The cheapest geometric test starts with one retained weighted five-site motif.
Admit the realizable site traces on its frozen core domain, then compare its charge with
the 80 ordinary threshold atoms supported on those sites.
Exact domination cost at most one over **all realizable traces** rules out its
multiplicity advantage over all ordinary atoms on those sites.
Its ordinary replacement could still add useful columns missing from the current
catalog. A witnessed realizable trace subset with cost above one proves that some local
advantage survives geometry.
Neither result settles the full covering budget.
A genuine floor test should likewise retain traces requiring multiple charge levels.

### Alternate atom and support changes; test the whole optimal dual face

The existing `think-yc80` continuation should alternate proposing atoms and updating the
fractional **support**, the poses assigned positive weight, with full depth checks
before calling a support an obstruction.
A finite LP dual vector can propose useful cuts even when it fails those checks, but it
supplies no packing impossibility claim.

One exact discriminator improves the interpretation of a stalled finite covering LP. For
a finite core list and atom list, let $A$ be the matrix whose entry $A_{ij}$ is atom
$j$’s charge on core $i$, let $b$ be the vector of atom budgets, and let $y$ be the
vector of nonnegative dual weights on the cores.
Assume the old covering program is feasible with finite optimum $v$. Its **optimal dual
face** is the entire set of dual solutions attaining $v$:

$$
\mathcal F_{\mathrm{old}}
=\{y\geq0:A^{\mathsf T}y\leq b,\ \mathbf 1^{\mathsf T}y=v\}.
$$

The superscript $\mathsf T$ means transpose, $\mathbf 1$ is the vector of ones, and
vector inequalities apply in every coordinate.
Proposed new atom columns have matrix $A_{\mathrm{new}}$ and budgets $b_{\mathrm{new}}$.
The new columns strictly lower the finite covering optimum **if and only if**

$$
\{y\in\mathcal F_{\mathrm{old}}:
A_{\mathrm{new}}^{\mathsf T}y\leq b_{\mathrm{new}}\}=\varnothing.
$$

In words, no old optimal dual solution satisfies all the new capacity inequalities.
Violating the particular dual returned by a solver does not establish this.
An exact feasibility problem on the old optimal dual face decides whether the new
columns matter to that finite control; omitted geometric poses remain a separate
obligation.

**Higher-rank floor compositions** build a new charge by combining existing charges and
rounding down, possibly repeatedly.
If the nonnegative integer-valued charges $f_j$ have globally valid budgets $b_j$ and
the coefficients $\alpha_j\geq0$ are rational, then

$$
f(C)=\left\lfloor\sum_j\alpha_jf_j(C)\right\rfloor,
\qquad b=\left\lfloor\sum_j\alpha_jb_j\right\rfloor
$$

is another globally valid charge and budget.
This follows because the sum of floors is at most the floor of the sum.
It creates a precise future charge language.
It earns an implementation block after an explicit composition separates a retained
obstruction and has a complete geometric evaluation rule.
An arbitrary finite-support cut is insufficient.

## 4. Structural Helpers Now Have Stronger Premises

Stromquist’s helper arguments use more than a collection of dots: ownership and
incidence restrict what another square can occupy.
The current structural results make that approach concrete at eleven, but the relevant
owner choices must coexist in one physical packing.

### Seven marks, common surplus, and co-owned segments

Here the container side is fixed at $q=96/25$ and the strict-core side at
$B=9977/10000$. The admitted BC303 point measure $\mu$ has mass $M=22524199/2000000$.
Its eight corner marks each have weight $w=106251/800000$. Eleven disjoint selected
cores collect at least eleven units of this measure, leaving unused mass at most
$\varepsilon=M-11$. Since

$$
2w-\varepsilon=\frac{441}{125000}>0,
$$

at most one corner mark can be unowned.
Exact cross-corner distances prevent a core from owning marks at different corners.
Thus at least three corner pairs are fully owned; a full pair is either co-owned by one
core, which contains their joining segment, or split between two cores.
If $\sigma$ fully owned pairs are split, there are $4+\sigma$ corner-owner cores and
$7-\sigma$ remaining cores.

The abstract zero-or-one-missing-mark patterns number $2^4+8\cdot2^3=80$. These are
labels with continuous geometry still to decide, not eighty feasible packing classes or
a reason to launch eighty LPs.
The unused mass is $U_\mu=M-\sum_{i=1}^{11}\mu(C_i)\geq0$. Each **surplus** $\mu(C_i)-1$
is the amount by which a core exceeds its required charge.
Their exact shared accounting is

$$
U_\mu+\sum_{i=1}^{11}(\mu(C_i)-1)=\varepsilon.
$$

If a geometry lemma forces a charge surplus for several distinct owners, their surpluses
and any missing mark must fit this **one** allowance.
Charging the same owner’s surplus twice would invalidate the argument.
The
[structural proof, §2](../../../docs/project/research/research-2026-09-10-x027-structural-helpers.md#2-seven-of-eight-marks-are-owned)
also retains counterexamples: a co-owning core can have a **neutral patch restriction**,
which leaves the retained fractional family at the required residual weight rather than
strictly below it. Split ownership is also locally realizable.
A useful next lemma needs the actual parent geometry, additional avoided marks, or a
strict common-surplus bound.

### Wall contact gives a finite component restriction

A **contact graph** has one vertex for each physical unit square and an edge when two
squares touch. A **contact component** is a maximal group connected by paths in this
graph; it refers to parents, not their strict cores.
A square’s **incircle** is the radius-$1/2$ circle centred at its centre and contained
in the square.

For two unit squares touching the left wall, their centre $x$ coordinates differ by at
most $(\sqrt2-1)/2$. Their open incircle disks are disjoint, so their vertical
separation is at least

$$
\eta=\frac{\sqrt{1+2\sqrt2}}{2}.
$$

Four such centres would span at least $3\eta>q-1$; therefore at most three squares touch
any wall, including vertex contact.
The admitted **fixed-angle normal form** S1 translates squares while retaining their
orientations and preserving a packing in the same container.
It gives an equivalent packing whose every physical contact component touches both left
and bottom walls. It consequently has at most three components, one containing at least
four squares.

Select the corner owners **after** normalization.
Four distinct corner owners in at most three components force a parent-contact path
joining owners at two different corners.
The six unordered corner pairs provide endpoint types.
Neither a short path, positive-length contacts, common angles, rigidity (being unable to
move while preserving a packing), nor touching strict cores follows.
The
[full proof and limits](../../../docs/project/research/research-2026-09-10-x027-structural-helpers.md#5-a-wall-has-at-most-three-touching-squares)
keep the normalization and the original packing distinct.

### Joint owner consistency is stronger than independent compatibility

Write $\mathrm{BL},\mathrm{BR},\mathrm{TL},\mathrm{TR}$ for the bottom-left,
bottom-right, top-left, and top-right corner roles.
A **residual** square is one not selected as a corner owner.
An owner and a residual square are **compatible** if they can coexist under the stated
core or parent constraints.
A **unary owner domain** imposes compatibility with just one residual; a joint domain
imposes all residual conditions on the same owner.

Individual unit parents for an obstruction’s cores do not make those parents coexist.
Likewise, an owner compatible with residual square $R_1$ and an owner compatible with
$R_2$ need not be the **same** owner.
A pair test can expose this loss: each unary owner domain must be nonempty, but their
intersection can be empty.
A **positive unary control** exhibits a compatible owner for each residual separately.
The pair test first needs these controls and disjoint residuals, so a failure genuinely
tests the requirement of a common owner.
Exp149 and exp151 are unsuitable: their cores intersect, and exp151 already fails the
complete TR unary test.

BC337 already proposes a stronger **unary** forbidden region derived from all allowed
owners. It remains blocked on its constructor, clipping, bounded runner, and independent
reader. It is not a new joint-consistency experiment.
Exp156 established old-model TR incompatibility for the saved exp151 pose, so repeating
a narrower parent-restricted TR test cannot show added gain.
Its frozen run leaves BL, BR, and TL untested.

**Selection routing** asks whether a physical packing necessarily offers at least one
selection covered by an existing conditional exclusion.
For a physical packing $\mathcal P$, let $A_c(\mathcal P)$ be the available owner labels
at corner role $c$, and let $\mathcal G$ be the set of excluded selections.
The Cartesian product chooses one available label at each corner:

$$
\Gamma(\mathcal P)
=\prod_{c\in\{\mathrm{BL},\mathrm{BR},\mathrm{TL},\mathrm{TR}\}}
A_c(\mathcal P).
$$

Let $\mathfrak P_{11}(q)$ denote the physical eleven-square packings in $K_q$, equipped
with their admitted selected cores.
The global obligation is

$$
\forall\mathcal P\in\mathfrak P_{11}(q),\qquad
\Gamma(\mathcal P)\cap\mathcal G\ne\varnothing.
$$

Showing that one allowed selection survives says nothing about whether another available
selection is excluded.
The seven-mark constraints can reduce the abstract availability patterns that avoid
$\mathcal G$; each remaining pattern still needs geometry.
This is an appropriate small combinatorial precursor to further conditional covers.

### Segment and angle profiles connect the two proof routes

For strict cores, the lengths they occupy on a fixed line segment are additive resources
because their intersections with the segment are disjoint.
For an owner of a mark on a segment, another disjoint owner restricts it to the
connected free portion accessible from that mark.
A uniform lower length demand exceeding this accessible capacity excludes the joint
**incidence-and-angle cell**: a specified combination of contained marks and allowed
angle intervals. Co-owned mark segments and split-pair incidence now supply a reason to
select such cells. The constants in Stromquist’s helper for $n=6$ cannot be carried to
$n=11$ unchanged.

The first test should derive exact formulas on one **positive-width angle cell**, an
interval $[a,b]$ with $a<b$, including endpoints and facet changes, where a different
square edge begins to determine the intersection with the segment.
A midpoint violation is proposal evidence only.
If independently minimizing each owner’s demand loses the gap, a joint angle profile may
retain it on a proved compatibility relation.

Mixed angle counts offer a parallel certificate route.
Partition the admitted core angles into classes $\mathcal C_j$ and define the least
charge in a class by $d_j=\inf_{C\in\mathcal C_j}g(C)$. A **count profile** $(n_j)_j$
specifies how many selected cores lie in each class, with $\sum_j n_j=11$. With one
universal charge budget $M$, a proved profile excludes the packing when

$$
M<\sum_j n_jd_j.
$$

For two classes with $(n_0,n_1)=(9,2)$, this is $M<9d_0+2d_1$. The existing angle
theorems use exact rational cell boundaries, not rounded degree labels, and every
physical unit-to-core assignment must respect those boundaries.
Two separate controls isolate the mechanisms: hold the charge language fixed while
comparing uniform and class-specific demands, then hold the profile fixed while
comparing point-only and ordinary-threshold charges.
For the charge comparison, both arms optimize nonnegative certified demand lower bounds
$d_0,d_1$ on the same classified core rows, under $9d_0+2d_1=1$; only the treatment
receives threshold columns.
The uniform-demand control at this scale has $d_0=d_1=1/11$. Complete geometric coverage
and $M<1$ are still required for the conditional exclusion.
The optimized $d_j$ are lower bounds on the infima defined above; equality with those
infima is not assumed during optimization.
A four-arm comparison would measure both effects and their interaction.
Existing charge types suffice before multiplicity machinery is built.

## 5. Ranked Continuations and Explicit Stop Conditions

This ordering is a judgment about readiness and information, not a measured runtime or
productivity ranking.
The numerical targets require prospective registration and maintained instruments.
`proposes: []` records that this analytical block promotes no new hypothesis or theorem
identifier.

| Order | Bounded next slice | What would change the decision | Stop or limit |
| --- | --- | --- | --- |
| 1, direct bound | Admit and run the already frozen BC329 packet | Exact least charge exceeds $M/11$, with the frozen normalization and independent covering evidence | An exact failing pose rejects this packet; timeout or incomplete coverage is unresolved. Neither closes re-optimization or finer nets generally |
| 2, language | Test one weighted five-site motif on admitted realizable traces against all ordinary atoms on those sites | A strict exact domination gap survives geometry; then compare a covering LP on a common control | No gap rejects its multiplicity advantage on that domain; ordinary replacement columns may still help the current catalog. A gap alone is not a global cover |
| 3, obstruction loop | Continue `think-yc80` with atom/support updates and an exact optimal-dual-face test | Added columns remove the whole old optimal face, or an admitted replacement depth-one obstruction survives | A cut of one support or one dual vector supplies no general closure |
| 4, structural | Apply the seven-mark premises to one source-bound co-owner geometry, or a disjoint pair with positive unary controls | Parent geometry, shared surplus, or common-owner consistency removes a witness that the matched weaker model admits | Fixed poses need positive-width continuation; co-ownership alone has a retained neutral counterexample |
| 5, profile | Test a proved mixed angle-count branch, holding language fixed for the demand comparison and profile fixed for the charge comparison | Class demands improve on uniform demands, or ordinary-threshold charges improve on points under the same profile | These are distinct effects; unproved angle assignments, exact-angle substitutes, or ignored profiles invalidate either comparison |
| 6, theoretical admission | Retain independent review of the interior-duality and finite-witness arguments; export the transported unit family if a consumer needs it | A maintained reader can consume the already proved transport; BC242 can use a precise value-equality theorem | This does not calculate the fractional optimum or classify equality |
| 7, next structural depth | One anchored component or segment/angle cell joining corner roles | Exact joint geometry yields a strict resource inequality on the whole cell | Graph counts, sampled contacts, and isolated orientations are insufficient |
| 8, richer closure | A genuine multilevel floor or higher-rank charge | A globally valid new charge separates an obstruction and has a complete pose evaluator | Abstract profile separation or finite-support cuts alone do not justify a full format expansion |

BC337 and its existing prerequisites remain the separate unary-domain continuation.
The new structural work should share its geometry tools when appropriate, while testing
a newly declared premise.
A new agenda can select two or three of these slices after instrument readiness is
known; X-027 is not an instruction to run every row at once.

## 6. Parked Questions, with Reasons to Reopen Them

- **Find fractional mass eleven at $3.83\leq L\leq3.85$.** Already answered by exact
  transport. Reopen for a smaller frozen side or a new capacity family, not existence in
  that range.
- **Replace point sites by unrestricted continuous density to cross $L_*$.** The
  retained family and the duality argument block this unconditional method.
  Reopen with a richer charge or conditional domain whose witness membership is checked.
- **Split the same neutral endpoint patches again.** These guaranteed occupied regions
  are derived from the retained angular endpoint classes.
  H-157’s six neutral subclasses are a result for that finite patch universe.
  Additional marks, parent consistency, segment demand, or selection routing could
  change the domain; relabelling it cannot.
- **Treat removal of one fractional support as a global breakthrough.** A5 and A6 show
  the replacement-support problem.
  Reopen only with full covering evidence or a theorem controlling every support on the
  declared domain.
- **Broad contact-graph enumeration.** The new component cap is useful, but it gives no
  rigidity or short-path theorem.
  Start with one complete component cell that changes a resource inequality.
- **Use $n=6$ as evidence that five-dot failure implies weighted failure.** The letter
  concerns unweighted sites.
  A simple set-system counterexample separates those statements.
  The case $n=6$ is still a clean physical-gap control: its proved $s(6)=3$ means an
  exact fractional family of mass $6$ at $L<3$ would establish a gap immediately.
  A failed finite-support search would be inconclusive.
- **Conflate the author’s Figure14 repair with the repository’s verified repair.** The
  archived suggested $G=(0.8,s/2-0.05)$ or $(0.8,1.845)$ differs from the independently
  verified $G=(0.79,1.85)$. Here $G$ is the relocated site and $s$ is the container-side
  variable used in the letter, separate from our function $s(n)$. A paired exact replay
  would settle that historical detail; it is a lower-priority source-control question,
  not evidence for an $n=11$ bound.
  The $n=18$ priority and $n=26$ relevance withdrawals likewise change attribution and
  scope, not the validity of the archived constructions.

## 7. Review Record and Research Disposition

| Independent lane | Retained report | Mathematical review |
| --- | --- | --- |
| Fractional packing and duality, Astra max | [Full-unit transport, continuous duality, finite witnesses, and controls](../../../docs/project/research/research-2026-09-10-x027-fractional-duality.md) | Structural and certificate lanes passed transport and duality; structural lane also checked the rational finite-witness lemma and explicit three-square control |
| Structural helpers, Astra max | [Seven marks, joint owners, contact components, and segments](../../../docs/project/research/research-2026-09-10-x027-structural-helpers.md) | Fractional and certificate lanes independently checked the BC303 arithmetic, ownership counting, wall bound, and normalized contact consequence |
| Certificate mechanisms, Astra extra high | [Recent gains, multiplicities, floor profiles, and optimal faces](../../../docs/project/research/research-2026-09-10-x027-certificate-mechanisms.md) | Structural lane and coordinator checked the five-site dual witness, global floor budget, and finite optimal-face criterion |

The coordinator checked the source scopes and consequential deductions, and assembled
the comparison. A separate integrated review found no mathematical blocker and prompted
four scope corrections: limit the introductory cap claim to sides past $L_*$,
distinguish timeouts from exact packet rejection, preserve the possible usefulness of
ordinary replacement columns, and separate the angle-demand and charge-language
controls. Its broken structural-section link was also corrected.
The session record carries validation, resource usage, and the final review disposition.
The source reports preserve the full proofs and counterexamples so later numerical work
can cite an exact premise rather than a strategic summary.

The notation revision adds local definitions and an explicit dependency table to all
four documents. Its review also makes the fixed-support upper-bound scope and the shared
normalization for mixed-demand comparisons explicit.
Mathematical spans use KaTeX-compatible dollar delimiters; code formatting is reserved
for literal record identifiers, paths, and commands.
The retained [KaTeX syntax checker](../../devtools/check_katex.py) parses recognized
spans with the renderer pinned through kpress; the separate formatter check verifies
that Flowmark preserves those spans.
These are syntax and source-format checks, not mathematical proof verification or
browser-layout certification.

The [idea board](../ideas.md#stromquist-fractional-and-structural-strategy--x-027)
retains the new shaped directions.
Existing direct-bound and unary-domain work keeps its existing identity.
The next implemented block should declare one mathematical question, the matched control
that isolates it, and the exact evidence that would justify expansion.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
