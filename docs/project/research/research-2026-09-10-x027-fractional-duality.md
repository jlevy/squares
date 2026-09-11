# Fractional Packing, Duality, and the Next $n=11$ Discriminators

A **physical packing** places a positive integer number $n$ of unit squares inside a
larger square, with no overlap between the small squares’ interiors.
A unit square has side length one.
Edges and corners may touch.
Write $s(n)$ for the smallest container side that permits such a packing.

A **fractional packing** assigns nonnegative weights to square placements.
Its total weight, also called its **mass**, takes the place of the number of squares.
Its **depth** at a point is the sum of the weights of the squares containing that point.
The capacity requirement is that depth never exceed one.
The squares may overlap; their weights must respect that requirement.

An **ordinary point cover** assigns nonnegative mass to points so that every allowed
square contains mass at least one.
Its **budget** is its total mass.
Summing those coverage requirements against a fractional packing shows that the cover’s
budget cannot be smaller than the packing’s mass.
This inequality is **weak duality**. Section 2 specifies the boundary convention needed
to make it valid when squares touch.

**Result of this analytical spike, September 10, 2026.** An existing fractional family
uses 88 smaller squares, called **cores**, of side $B=9977/10000$ in a container of side
$L_0=191/50$. Rescaling both their positions and their sides by $1/B$ gives unit squares
of total mass eleven in a container of side

$$
L_*=\frac{L_0}{B}
=\frac{191/50}{9977/10000}
=\frac{38200}{9977}
\approx3.8288.
$$

Here $L_*$ names the side supplied by this particular witness; it is not a claimed
optimum. Ordinary point covers of budget below eleven are therefore impossible at $L_*$
and every larger side, including the interval $[3.83,3.85]$. Section 1 proves the
rescaling and its scope.
A search for that existence result would duplicate retained evidence.

Two further results explain what to do with that obstruction.
Section 3 proves **strong duality**, meaning equality of the best packing value and the
best covering value, under an explicit continuous formulation.
Allowing a continuous point density does not evade the obstruction.
Section 5 explains **threshold charges**: counting rules that charge a square only when
it contains sufficiently many of a specified set of points.
Their additional capacities can exclude a fractional family that ordinary point depth
allows.

These are analytical arguments independently reviewed here, with no frontier admission
or claim of novelty.
No numerical target was run, and the physical bound remains

$$
3.826447410572939744\ldots
\leq s(11)\leq
3.877083590022814\ldots.
$$

The lower endpoint is below $L_*$. Thus the retained fractional witness does not yet
prove that eleven physical unit squares need a strictly larger container than eleven
units of fractional mass.

## Inputs, Outputs, and Reading Order

[X-027](../../../packing/campaign/explorations/X-027-stromquist-fractional-and-structural-strategy.md)
is the entry-point synthesis that uses this report.
It is not a premise for the proofs below.
This report supplies their definitions, derivations, examples, and limitations.

| Input | Role in this report |
| --- | --- |
| [Retained 88-core family](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/ceiling-family-191-50.json) and [independent exact receipt](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/ceiling-family-191-50-independent-reader.json) | Geometric premises for §1: contained cores, their weights, and depth at most one at every point |
| [BC-242 density contract](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-242-full-size-density-proof-contract.md) | Baseline continuous problem for §§2–3, including continuity of coverage for integrable densities; this report supplies the value-equality argument |
| [T-025 proof packet](../../../packing/cases/n11_threshold_certificate/t-025-threshold-certificate-proof.md) | Premise for the matched core-model gap in §5: the specified core family has a threshold cover of budget below eleven |
| [A6 scope and exact evidence](research-2026-09-09-n11-evidence-and-inference.md#13-the-later-a6-and-h157-results-what-has-been-checked), [current physical bracket](../../../SYNOPSIS.md#current-handoff), and [the $n=6$ case](../../../packing/frontier/n-006.md) | Retained results used to distinguish conclusions about fixed families from physical packing claims in §§5–7 |
| [Stromquist correspondence](../../../packing/resources/private-correspondence/email-stromquist-2026-09-07.md), [X-023](../../../packing/campaign/explorations/X-023-three-losses-and-a-new-atom.md), and [X-026](../../../packing/campaign/explorations/X-026-what-conditioning-does-and-does-not-buy.md) | Motivation and research context; the letter and strategic summaries are not proofs of the new derivations |

An exact **receipt** is a retained record of a verifier’s checks.
The source family and receipt were inspected, not rerun here.
**Retained exact evidence** means a previously checked mathematical input; **analytic
derivation** means the argument displayed here; **prospective experiment** means
proposed work with no result.

The logical order is:

1. Section 1 uses the retained finite family to obtain a unit-square obstruction.
2. Section 2 defines the continuous packing and covering problems and proves weak
   duality. Section 3 then proves equality of their values.
3. Section 4 uses the geometric model and finite linear programming to obtain finite
   packing witnesses after a small enlargement of the container.
   It does not require a numerical result about the optimum.
4. Sections 5–7 combine those results with T-025, A6, and the solved $n=6$ case to state
   useful discriminators.

The [certificate-mechanisms report](research-2026-09-10-x027-certificate-mechanisms.md)
uses the distinction between point depth and additional counting capacities.
The [structural-helper report](research-2026-09-10-x027-structural-helpers.md) uses the
requirement to recheck a witness after restricting its allowed poses.
Neither report’s new lemma is a premise of this report.
Their independent reviews are assurance checks, recorded in §8, rather than steps in the
proofs.

## 1. Exact Rescaling Already Answers the Mass-Eleven Question

Write $\mathbb R$ for the real numbers and $\mathbb R^2$ for the plane of points with
two real coordinates.
For a side $L>0$, write $K_L=[0,L]^2$ for the square container.
A **closed square** includes its edges and corners; its **interior** excludes them.
For any set $E$, the indicator $\mathbf 1_E(x)$ is one when the point $x$ belongs to $E$
and zero otherwise.

Index the retained cores by $i=1,\ldots,88$, call them $C_i$, and write $a_i=1/8$ for
their weights. Each core has side $B=9977/10000$ and lies in $K_{L_0}$, where
$L_0=191/50$. The independent receipt checks containment of all 352 corners and
closed-square depth at the 20,376 vertices of the edge-line arrangement.
An **arrangement** divides the plane by the squares’ edge lines; its vertices are
intersections of those lines.
For this finite family of closed squares, the exact reader’s arrangement argument makes
the vertex checks a proof about every point:

$$
\sum_{i=1}^{88}a_i\mathbf 1_{C_i}(x)\leq1
\qquad\text{for every }x\in\mathbb R^2.
$$

**Analytic derivation.** Define the unit squares $U_i=B^{-1}C_i$, meaning that every
coordinate is multiplied by $1/B$. They lie in $K_{L_*}$ and satisfy

$$
\sum_{i=1}^{88}a_i\mathbf 1_{U_i}(x)
=\sum_{i=1}^{88}a_i\mathbf 1_{C_i}(Bx)\leq1,
\qquad
\sum_{i=1}^{88}a_i=11.
$$

Uniform rescaling preserves every point-membership relation, including boundary
membership. The same squares can be placed unchanged in a larger container.
Also

$$
\frac{383}{100}-L_*=\frac{1191}{997700}>0,
$$

so this witness exists below $3.83$.

A **direction net** is a finite list of square orientations used to select cores.
Folding an orientation means replacing it by a reflected orientation in a designated
angular range.
The group $D_4$ consists of the eight rotations and reflections preserving
the square container.
A $D_4$-symmetric cover gives the same mass to a set and to each of its symmetry images.

The reader’s literal `symmetric_only` flag concerns its folded-net covering problem: 44
retained placements have mirrored directions, so a cover required to cover only the
listed net directions needs symmetry to cover those reflected placements.
In the full-unit problem, every actual orientation of all 88 squares is allowed.
Any cover of every contained unit square must cover each $U_i$ directly.
Thus the rescaled family obstructs arbitrary point covers, including asymmetric ones.

Let $\mu$ be a nonnegative distribution of mass on container points, with $\mu(E)$
denoting the mass in a set $E$. Section 2 makes this **measure** notation precise.
If $\mu(U_i)\geq1$ for every $i$, finite summation gives

$$
11
\leq\sum_{i=1}^{88}a_i\mu(U_i)
=\int_{K_{L_*}}\sum_{i=1}^{88}a_i\mathbf 1_{U_i}(x)\,d\mu(x)
\leq\mu(K_{L_*}).
$$

The integral means mass-weighted addition over points.
The same conclusion holds when coverage must come from each square’s interior, because
that requirement is stronger than coverage of its closed square.

A **core-selection rule** chooses a smaller closed square strictly inside each unit
parent.
A sound rule must prove that every selected core belongs to the family covered by
the proposed certificate.
Choose such a core $C_i'$ inside each $U_i$. Since

$$
\mathbf 1_{C_i'}(x)\leq\mathbf 1_{\operatorname{int}U_i}(x)
\leq\mathbf 1_{U_i}(x),
$$

the selected cores still have weighted depth at most one.
A cover of their allowed family with budget below eleven is impossible.
This deduction applies to any direction net and core size with a proved selection rule;
the new net need not contain the original six folded directions.

This obstruction concerns the **unconditional** problem, whose pose family imposes no
additional assumption about other packed squares.
A **conditional** problem adds such an assumption, for example a specified corner owner
and a region it must occupy.
To use the same witness there, one must prove that its placements obey the additional
restrictions. The unconditional witness supplies no physical eleven-square packing.

## 2. The Measure Spaces and the Boundary Convention

Fix a container side $L\geq1$. Let $Q=[-1/2,1/2]^2$ be the unit square centered at the
origin. A **pose** specifies a center $c\in\mathbb R^2$ and an angle $\theta$, measured
in radians. The rotation by that angle is the matrix

$$
R_\theta=
\begin{pmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{pmatrix}.
$$

A square repeats after a quarter turn.
Write $\mathbb T_4=\mathbb R/((\pi/2)\mathbb Z)$ for angles with values differing by an
integer multiple of $\pi/2$ identified.
Here $\pi/2$ radians is a quarter turn and $\mathbb Z$ denotes the integers.
A pose $p=(c,\theta)$ represents the closed unit square $S_p=c+R_\theta Q$. The **legal
pose space** is

$$
P_L=\{(c,\theta)\in K_L\times\mathbb T_4:S_p\subseteq K_L\}.
$$

A space is **compact** when every cover by open sets has a finite subcover.
For this metric pose space, this is equivalent to every sequence having a convergent
subsequence with limit in the space.
Centers and orientations range over a compact set, and containment is preserved under
pose limits. Hence $P_L$ is compact.
It includes wall-touching poses.

### Measures, atoms, and densities

A finite nonnegative **Borel measure** assigns nonnegative mass to sets, with finite
total mass and countable additivity on disjoint sets.
Borel sets are the sets generated from open sets by complements and countable unions;
the geometric sets used here are Borel.
For a compact space $Y$, write $\mathcal M_+(Y)$ for these measures on $Y$. “Finite”
refers to total mass, not to the number of points carrying it.

A **point atom** of mass $a\geq0$ at a point $x$ is written $a\delta_x$: its mass in $E$
is $a$ if $x\in E$, and zero otherwise.
A **finite atomic measure** is a finite sum of such atoms.
A measure can also spread mass continuously.
An **absolutely continuous measure** has the form $\mu(E)=\int_E\rho(x)\,dx$, where $dx$
denotes ordinary two-dimensional area and the **density** $\rho$ is nonnegative and
integrable. The notation $L^1$ denotes integrable functions.
Their norm, measuring total absolute mass, is $\|\rho\|_1=\int_{K_L}|\rho(x)|\,dx$. A
**singular measure** has all its mass concentrated on a set of zero area; a point atom
is an example.

Use $\lambda\in\mathcal M_+(P_L)$ for a packing measure on poses and
$\mu\in\mathcal M_+(K_L)$ for a covering measure on container points.
These are different spaces.
Atomic packing measures must be allowed because physical packings are finite lists of
poses.

Define the **interior incidence function**, which records whether a point lies in a
square’s interior, by

$$
A(x,p)=\mathbf 1_{\operatorname{int}S_p}(x).
$$

The set of pairs $(x,p)$ with $A(x,p)=1$ is open in $K_L\times P_L$: strict membership
persists under small changes of both point and pose.
Define the interior and closed depths of $\lambda$ by

$$
d_\lambda^\circ(x)=\int_{P_L}A(x,p)\,d\lambda(p),
\qquad
d_\lambda^{\mathrm{cl}}(x)
=\int_{P_L}\mathbf 1_{S_p}(x)\,d\lambda(p).
$$

### The two optimization problems

A **supremum** is the least upper bound of possible objective values; an **infimum** is
the greatest lower bound.
Either can exist without a feasible object achieving it.
An **optimizer** is a feasible object that does achieve the value; this is called
**attainment**.

The packing value $\nu_\circ(L)$ maximizes mass subject to interior depth at most one.
The covering value $\tau_\circ(L)$ minimizes mass subject to interior coverage at least
one for every legal pose:

$$
\begin{aligned}
\nu_\circ(L)
&=\sup\{\lambda(P_L):
\lambda\in\mathcal M_+(P_L),\
d_\lambda^\circ(x)\leq1\text{ for every }x\in K_L\},\\
\tau_\circ(L)
&=\inf\{\mu(K_L):
\mu\in\mathcal M_+(K_L),\
\mu(\operatorname{int}S_p)\geq1\text{ for every }p\in P_L\}.
\end{aligned}
$$

The circle subscript records the interior convention.
Let $\tau_{\mathrm{fin}}(L)$ be the covering infimum when $\mu$ must be finite atomic.
Let $\tau_{\mathrm{ac}}(L)$ be the covering infimum when $\mu$ must have an integrable
density. Square boundaries have area zero, so using closed or interior coverage makes no
difference to the latter value.
It is BC-242’s density value.

**Weak duality.** For any feasible $\lambda$ and $\mu$, Tonelli’s theorem permits
interchanging the two integrals because their integrand is nonnegative.
It gives

$$
\begin{aligned}
\lambda(P_L)
&\leq\int_{P_L}\mu(\operatorname{int}S_p)\,d\lambda(p)\\
&=\int_{K_L}\int_{P_L}A(x,p)\,d\lambda(p)\,d\mu(x)\\
&\leq\mu(K_L).
\end{aligned}
$$

Consequently $\nu_\circ(L)\leq\tau_\circ(L)$. A physical packing
$\mathcal P=\{p_1,\ldots,p_n\}$ gives the measure
$\lambda_{\mathcal P}=\sum_{i=1}^n\delta_{p_i}$, of mass $n$. Its interior depth is at
most one even when squares touch.
Integrating the depth of any feasible packing measure over area also gives

$$
\lambda(P_L)=\int_{K_L}d_\lambda^\circ(x)\,dx\leq L^2,
$$

because every unit square has area one.

### Two boundary counterexamples

Take two touching unit squares $[0,1]^2$ and $[1,2]\times[0,1]$. Their interiors have
depth one. A unit atom at $(1,1/2)$ belongs to both closed squares, so it covers this
two-square family with mass one.
Thus interior capacities cannot be paired with closed coverage of an arbitrary singular
measure.

**Weak convergence of measures** means convergence of integrals against every continuous
function. Closed-depth feasibility need not survive it.
In the fixed container $K_3$, consider $[0,1]^2$ and $[1+1/j,2+1/j]\times[0,1]$, each of
weight one, where $j$ is a positive integer.
Every such pair has closed depth one.
As $j$ tends to infinity, its pose measure converges weakly to the touching pair, whose
closed depth is two on the common edge.
The interior-depth limit remains feasible.
Compactness of the pose space alone therefore does not establish compactness of the
closed-depth feasible set.

## 3. A Strong-Duality Argument with Finite Covers

**Analytical theorem, independently reviewed.** For the full-unit interior model in §2,

$$
\nu_\circ(L)=\tau_\circ(L)
=\tau_{\mathrm{fin}}(L)
=\tau_{\mathrm{ac}}(L).
$$

The packing supremum is attained by a Borel measure on $P_L$. The argument does not
assert an attained covering optimum, density optimum, or finite packing optimum.

A **linear program**, abbreviated LP, optimizes a linear function subject to linear
equalities or inequalities.
Finite LP duality pairs a packing maximization problem with a covering minimization
problem having the same optimum, when both are feasible and have finite optimal values.
The proof below reduces the relevant intermediate problems to such finite LPs.

### Finite hitting set and compact packing measures

For each container point $x$, let

$$
V_x=\{p\in P_L:x\in\operatorname{int}S_p\}.
$$

Each $V_x$ is open. Together they cover $P_L$, since every legal square has an interior
point.
Compactness supplies a finite **hitting set** $F_0\subset K_L$, meaning that every
pose interior contains at least one point of $F_0$. Equivalently,

$$
P_L=\bigcup_{x\in F_0}V_x.
$$

Here $|F_0|$ denotes the number of points in $F_0$. A packing measure satisfying just
the capacities at these points has the uniform mass bound

$$
\lambda(P_L)
\leq\sum_{x\in F_0}\lambda(V_x)
\leq|F_0|.
$$

A function is **lower semicontinuous** when its value at a limit is no larger than the
lower limit of its values along a convergent sequence.
For open $V_x$, weak convergence $\lambda_j\to\lambda$ gives

$$
\lambda(V_x)\leq\liminf_{j\to\infty}\lambda_j(V_x).
$$

Thus the capacity set $\{\lambda:\lambda(V_x)\leq1\}$ is closed under weak limits.
The standard compactness theorem for measures on a compact metric space says that
nonnegative measures of uniformly bounded mass form a compact space in the weak
topology. Apply it with the common bound $|F_0|$. Intersecting its closed capacity sets
gives a compact full feasible set.
Total mass is continuous under weak convergence, because it is the integral of the
constant function one.
A packing optimizer follows.

### Exact finite LPs and their direction

Let $F\subset K_L$ be any finite point set containing $F_0$, and impose only the
capacities at points of $F$. A pose has **incidence mask**

$$
I(p)=\{x\in F:x\in\operatorname{int}S_p\},
$$

the subset of tested points it contains.
Let $\mathcal I_F$ be the collection of masks realized by at least one legal pose.
It contains at most $2^{|F|}$ masks, all nonempty because $F_0$ hits every pose.

The poses realizing one mask form a Borel set: a finite intersection of sets $V_x$ and
their complements. Aggregate a measure’s mass on each such set into a number $b_I\geq0$,
for $I\in\mathcal I_F$. Conversely, choosing one legal representative pose for each
realized mask turns any such list of masses into a finite atomic pose measure.
Therefore the relaxed packing problem has exactly the finite LP value

$$
v_F=\max\left\{
\sum_{I\in\mathcal I_F}b_I:
b_I\geq0,\
\sum_{\substack{I\in\mathcal I_F\\x\in I}}b_I\leq1
\text{ for every }x\in F
\right\}.
$$

Its dual assigns point weights $a_x\geq0$ to $x\in F$ and has value

$$
v_F=\min\left\{
\sum_{x\in F}a_x:
a_x\geq0,\
\sum_{x\in I}a_x\geq1
\text{ for every }I\in\mathcal I_F
\right\}.
$$

Both programs are feasible and have finite optimal values.
The finite dual covers every legal pose, because every legal pose has a realized mask.
Its optimizer is therefore a globally feasible finite atomic interior cover of mass
$v_F$. Enumerating every realized mask may be expensive; this is an existence reduction,
not a bound on the cost of a current algorithm.

Dropping point capacities permits more packings, so $v_F\geq\nu_\circ(L)$. To show these
upper approximations approach the full value, choose a real number $\alpha>\nu_\circ(L)$
and suppose every finite $F$ permitted mass at least $\alpha$. In the same compact space
of measures bounded by $|F_0|$, impose the closed condition $\lambda(P_L)\geq\alpha$ and
all point capacities.
Every finite collection of these conditions would have a solution.
Compactness then gives a solution to all of them together, contradicting the definition
of $\nu_\circ(L)$. Hence

$$
\inf_{\substack{F\supseteq F_0\\F\text{ finite}}}v_F=\nu_\circ(L).
$$

The finite dual covers imply $\tau_{\mathrm{fin}}(L)\leq\nu_\circ(L)$. Weak duality and
inclusion of finite atomic covers among all covers give

$$
\nu_\circ(L)\leq\tau_\circ(L)
\leq\tau_{\mathrm{fin}}(L)\leq\nu_\circ(L).
$$

All three values are equal.
In particular, if $\nu_\circ(L)<n$, a finite atomic interior cover of mass below $n$
exists.

### Smearing the atoms gives the BC-242 density value

Take a finite atomic interior cover $\mu=\sum_{i=1}^r a_i\delta_{x_i}$, where $r$ is its
number of atoms. Remove zero weights and atoms on the container boundary, since no
contained square’s interior can use a boundary atom.

At each pose $p$, the atoms strictly inside $S_p$ carry mass at least one.
Each of those finitely many atoms has positive distance from the square boundary.
Their membership, with a smaller positive margin, persists on a neighborhood of $p$.
Compactness supplies finitely many such pose neighborhoods.
Taking the smallest of their margins gives one radius $\delta>0$ such that every legal
square contains whole $\delta$-balls around a subset of atoms of total weight at least
one.
A $\delta$-ball consists of points at Euclidean distance less than $\delta$ from its
center. Reduce $\delta$ also below every retained atom’s distance to the container
boundary.

Replace each atom by a nonnegative density supported in its $\delta$-ball and having the
same mass. The resulting density lies in $K_L$, retains the total mass, and covers every
legal square by at least one.
Thus $\tau_{\mathrm{ac}}(L)\leq\tau_{\mathrm{fin}}(L)$. An absolutely continuous cover
is itself a Borel cover, so $\tau_\circ(L)\leq\tau_{\mathrm{ac}}(L)$. This proves the
remaining equality.

The topological hypotheses matter.
A **hypergraph** is a ground set together with a family of subsets of it; fractional
packing and covering can be defined from that membership relation.
For arbitrary infinite hypergraphs, value equality can fail.
[Aharoni and Holzman’s 1992 paper](https://holzman.net.technion.ac.il/files/2012/09/gcoptimal.pdf)
gives such examples.
Its terminology differs: it calls value equality weak duality and reserves strong
duality for a stronger statement involving attained optima.
This report uses strong duality for value equality and states attainment separately.

### Why BC-242’s a.e. packing value is the same value

“Almost everywhere,” abbreviated **a.e.**, means except on a set of area zero.
Write $\nu_{\mathrm{ae}}(L)$ for BC-242’s packing supremum with
$d_\lambda^{\mathrm{cl}}(x)\leq1$ required only a.e.

Let $\partial S_p$ denote the boundary of $S_p$. The difference between closed and
interior depth is

$$
b_\lambda(x)=d_\lambda^{\mathrm{cl}}(x)-d_\lambda^\circ(x)
=\int_{P_L}\mathbf 1_{\partial S_p}(x)\,d\lambda(p).
$$

Every square boundary has area zero.
Tonelli therefore gives

$$
\int_{K_L}b_\lambda(x)\,dx
=\int_{P_L}\left(\int_{K_L}\mathbf 1_{\partial S_p}(x)\,dx\right)d\lambda(p)
=0.
$$

This argument works even when the pose measure is not atomic.
The two depths agree a.e. Interior depth is lower semicontinuous as a function of the
point $x$. If it exceeded one at an interior point of $K_L$, it would exceed one
throughout a neighborhood of positive area.
On the container boundary it is zero.
Thus

$$
d_\lambda^{\mathrm{cl}}\leq1\text{ a.e.}
\quad\Longleftrightarrow\quad
d_\lambda^\circ\leq1\text{ everywhere}.
$$

Consequently $\nu_{\mathrm{ae}}(L)=\nu_\circ(L)=\tau_{\mathrm{ac}}(L)$, with an attained
packing supremum. This does not determine the value at Trump’s side, the known upper
endpoint $3.877083590022814\ldots$ displayed above, or classify the cases of equality.
It does not permit singular closed-square covers to be paired with a.e. capacities.

There is also a separate **minimax** check: a theorem allowing the order of a
maximization and a minimization to be exchanged.
Normalize a nonnegative density $\rho$ and a pose measure $\eta$ to total mass one.
A measure of total mass one is called a **probability measure**. Define

$$
F_\rho(p)=\int_{S_p}\rho(x)\,dx,
\qquad
\Phi(\rho,\eta)=\int_{P_L}F_\rho(p)\,d\eta(p).
$$

Both normalized classes are **convex**: mixing two members with nonnegative coefficients
summing to one stays in the class.
BC-242 proves that $F_\rho$ is continuous on $P_L$. The payoff $\Phi$ is linear in each
argument and separately continuous for the $L^1$ norm on densities and weak convergence
on pose measures. The probability measures $\eta$ form a compact set.
The one-compact-side corollary in
[Sion’s minimax theorem](https://msp.org/pjm/1958/8-1/pjm-v8-n1-p14-p.pdf) therefore
applies. Restoring the mass normalization gives the same value equality.
The finite-mask proof also supplies the finite atomic-cover conclusion.

## 4. What Finite Witnesses Follow, and What Does Not

The compactness proof supplies finite covering witnesses when $\nu_\circ(L)<n$. It does
not bound their size, provide an algorithm for finding them, or give a finite packing
attaining $\nu_\circ(L)$ at exactly the same side.

An abstract example separates equality of values from finite attainment.
Let both the point space $X$ and pose space $P$ be $[0,1]$, and define incidence by

$$
A(x,p)=
\begin{cases}
1,&x\ne p,\\
0,&x=p.
\end{cases}
$$

This incidence set is open.
The common value is one: an atomless probability measure on $X$ covers every pose, and
one unit atom on $P$ is a feasible packing.
Here **atomless** means that each individual point has mass zero.
A finite atomic cover of total mass $M$, with largest atom weight $a_{\max}>0$, must
satisfy $M-a_{\max}\geq1$, so $M>1$. Assigning weight $1/(r-1)$ to each of $r\geq2$
distinct sites gives total mass $r/(r-1)$, approaching one.
This is a topological example, not a claimed unit-square counterexample.

**Lemma with side enlargement, proof sketch.** If a Borel fractional packing at side $L$
has mass at least a positive integer $n$, then for every real $\varepsilon>0$ there is a
finite fractional packing of unit squares of mass at least $n$ at side $L+\varepsilon$.

Choose a rational number $b$ with $0<b<1$ and $L/b<L+\varepsilon$. Here $b$ is the
temporary core side, separate from the retained family’s fixed $B$. Divide the compact
pose space into finitely many sufficiently small, disjoint Borel pieces.
Choose a representative pose in each nonempty piece.
Its concentric closed $b$-square has margin $(1-b)/2$, measured perpendicular to each
edge, inside its own unit parent.
Uniformly small pose pieces preserve part of that margin inside every unit square
represented by the piece.

Give each representative core the mass of its piece.
A point in that core belongs to every original unit square of the piece, so the finite
core family has depth at most one.
Its total mass is unchanged.
Rescaling by $1/b$ makes its cores unit squares in a container of side $L/b$.

The construction also admits rational coordinates.
A **rational pose** here means rational center coordinates and rational sine and cosine,
not a rational angle in radians.
A rational half-angle parameter $t=\tan(\theta/2)$ supplies

$$
\cos\theta=\frac{1-t^2}{1+t^2},
\qquad
\sin\theta=\frac{2t}{1+t^2}.
$$

Reserve some containment margin, then approximate each representative by such a rational
pose before dilation.
Its square still lies inside every original parent of its piece.
On the resulting finite rational family, closed depth at every point is decided by
finitely many arrangement vertices.
The allowed weights therefore form a bounded rational LP. The constructed real weights
are feasible, so a rational optimal weight vector has mass at least $n$.

Scale those rational weights down to total exactly $n$ and clear their denominators.
This produces a positive integer $k$ and a list of $nk$ unit-square placements, allowing
repetitions, with at most $k$ placements covering any point.
Such a list is a **$k$-fold packing**; assigning weight $1/k$ to each occurrence gives
fractional mass $n$. The container side is less than $L+\varepsilon$.

Margins are needed in both the pose approximation and the dilation construction.
A bounded search restricted to $k=2$ or $k=4$ is therefore not a complete decision.
At the exact side, the following equivalence remains unproved: $\nu_\circ(L)\geq n$ if
and only if some positive integer $k$ admits a finite $k$-fold family of $nk$ unit
squares in $K_L$. Finite attainment there needs another argument.
The retained family already supplies the particular case $k=8$, $n=11$ at $L_*$, without
relying on general exact-side attainment.

## 5. Integrality Gaps and Threshold Capacities

Let $m(L)$ be the maximum number of physical unit squares with disjoint interiors that
fit in $K_L$. An **integrality gap** occurs when allowing fractional weights gives a
strictly larger packing value than the integer number of physical squares.
Weak and strong duality give

$$
m(L)\leq\nu_\circ(L)=\tau_\circ(L).
$$

A fractional mass-eleven family proves such a physical gap at a side only after a
separate theorem gives $m(L)\leq10$. The current lower bound does not supply that
theorem at $L_*$. A physical exclusion at $L_*$ or a larger side would establish a gap
there when combined with the retained fractional family.

### The matched core-model gap

There is already a gap in a different, precisely matched model.
T-025 uses the same $L=L_0=191/50$, core side $B=9977/10000$, and 181-direction net as
the 88-core family, with the same $D_4$ reflection convention.
Its charges cover every allowed core with budget below eleven.
The counting argument excludes eleven pairwise disjoint **closed cores** in that domain,
while the fractional core family has mass eleven.

The
[T-025 packet](../../../packing/cases/n11_threshold_certificate/t-025-threshold-certificate-proof.md)
is the premise for that core exclusion.
Its physical theorem uses strict core containment.
A gap between closed-core packing and closed-core fractional packing does not itself
give the unresolved full-unit gap at $L_*$, where physical boundaries may touch.

### How a threshold adds a capacity

Let $S\subset K_L$ be a finite, nonempty set of sites.
Vertical bars around a finite set denote its number of elements.
Let $k$ be an integer with $1\leq k\leq|S|$. A **threshold charge** is one when a square
contains at least $k$ of these sites and zero otherwise.
For a condition, the indicator is one when that condition holds and zero otherwise.
The floor $\lfloor z\rfloor$ is the greatest integer at most a real number $z$. Define
its interior version by

$$
q_{S,k}(p)=
\mathbf 1_{\{|S\cap\operatorname{int}S_p|\geq k\}},
\qquad
c_{S,k}=\left\lfloor\frac{|S|}{k}\right\rfloor.
$$

The **capacity** $c_{S,k}$ bounds how many squares in a physical packing can be charged.
Their **traces**, the sets $S\cap\operatorname{int}S_p$, are disjoint, and each charged
square consumes at least $k$ sites.
Thus a physical packing $\mathcal P$ satisfies

$$
\sum_{p\in\mathcal P}q_{S,k}(p)\leq c_{S,k}.
$$

A **threshold atom** multiplies this charge by a nonnegative weight $a$ and contributes
$a\,c_{S,k}$ to a certificate’s budget.
A fractional packing measure can violate

$$
\int_{P_L}q_{S,k}(p)\,d\lambda(p)\leq c_{S,k}
$$

while respecting every point capacity.
Closed cores use closed traces and require disjoint closed cores.
Either boundary convention is sound when used consistently.

### An explicit three-square example

In $K_3$, take unit squares $S_1,S_2$ aligned with the coordinate axes, centered at
$(1,1)$ and $(8/5,8/5)$, respectively.
Let $S_3$ have center $(19/10,7/10)$ and orientation with cosine $3/5$ and sine $4/5$.
Give all three weight $1/2$.

The first two intersect on $[11/10,3/2]^2$. Membership in $S_3$ requires each of its two
edge-normal coordinates to have absolute value at most $1/2$. The second such
coordinate, for a point with coordinates $(x,y)$, is

$$
\ell(x,y)=-\frac45\left(x-\frac{19}{10}\right)
+\frac35\left(y-\frac7{10}\right).
$$

On $[11/10,3/2]^2$, its minimum is $14/25>1/2$. The triple intersection is therefore
empty. Each pair nevertheless intersects in its interior, as shown by these points:

$$
\begin{aligned}
x_{12}&=(13/10,13/10)\in\operatorname{int}S_1\cap\operatorname{int}S_2,\\
x_{13}&=(7/5,7/10)\in\operatorname{int}S_1\cap\operatorname{int}S_3,\\
x_{23}&=(19/10,6/5)\in\operatorname{int}S_2\cap\operatorname{int}S_3.
\end{aligned}
$$

This is a **non-Helly triple** in the sense used here: all pairs intersect, but the
three sets have no common point.
Its depth is at most one and its mass is $3/2$. On this **fixed support**, meaning that
only these three square placements are allowed, a physical packing has size at most one
because every pair overlaps.

Each square contains exactly two points of the set $\{x_{12},x_{13},x_{23}\}$. The
two-of-three capacity is one, but the fractional family charges it $3/2$. This is the
rational control retained in
[the plateau-reader tests](../../../packing/tests/test_plateau_reader.py), with its
geometry made explicit.

### What A6 does and does not obstruct

A certificate combining points and thresholds can be obstructed by a fractional family
only if that family satisfies both all point capacities and the capacities of every
threshold atom used.
It is not proved that imposing every threshold inequality is enough to recover all
constraints on physical packings.

An **atom catalog** is a specified list of allowed certificate charges.
An **atom orbit** is the set of images of one atom under the container symmetries, with
repeated identical images identified.
The A6 family has 64 placements of total mass eleven and satisfies all point capacities
and the retained 2,566 atom orbits.
Thus that catalog cannot produce budget below eleven on the stated core domain,
regardless of added ordinary point sites.

Later atoms exclude particular fractional families.
The exact upper bound $2605263163/250000000\approx10.421$ concerns a separate support of
280 allowed placements with the stated cuts.
Here a **cut** is an additional inequality valid for physical packings.
The bound concerns reweighting those placements, not every possible support or every
threshold atom. In the larger covering LP, adding the six atoms left the numerical
objective at eleven.
No global improvement follows from the fixed-support upper bound.
These two outcomes are retained together in
[§13 of the inference account](research-2026-09-09-n11-evidence-and-inference.md#13-the-later-a6-and-h157-results-what-has-been-checked).

## 6. N6 Is a Cleaner Physical-Gap Control

The retained [$n=6$ case](../../../packing/frontier/n-006.md) has $s(6)=3$, with a
published proof and archived earlier work.
Any exact full-unit fractional family of mass six at a side below three would therefore
prove a physical integrality gap immediately.
For eleven squares, the corresponding physical exclusion at $L_*$ is still missing.

The correspondence’s five-dot failure concerns five unweighted sites: each chosen site
has weight one. It does not concern arbitrary positive weights on arbitrary numbers of
sites. An abstract example shows why the distinction matters.
Take three disjoint copies of the three-site set system with sites $a,b,c$ and subsets

$$
\{a,b\},\qquad\{b,c\},\qquad\{c,a\}.
$$

A hitting set must choose at least two sites in each copy, hence six in all.
Weight $1/2$ on each of the nine sites covers every subset with mass one and uses total
mass $9/2<6$. Thus a failure of five unweighted sites need not prevent a weighted cover
below six. This example claims no realization by the full square pose family.

A useful six-square experiment should seek one of two positive witnesses at a specified
side below three: an exact fractional family of mass at least six, or a globally valid
interior cover of mass below six.
The latter excludes fractional mass six at that side.
A finite support whose maximum stays below six is inconclusive, because other poses may
permit a larger fractional mass.
An unsuccessful five-dot search supplies neither witness.

## 7. Next Discriminators and Their Prerequisites

A **discriminator** is a result that separates proposed explanations or changes the next
research choice. These comparisons are ordered by dependencies and new information, not
by measured runtime.
Each numerical implementation would need a maintained tool and its own prospective
experiment contract.

For the conditional question below, a **corner owner** is a square whose selected core
contains a prescribed corner mark.
An **owner class** specifies allowed poses for that owner.
A **guaranteed patch** is a region proved to lie inside every owner in its class.
A **residual domain** is the set of allowed placements for the remaining squares after
chosen owners have been accounted for.
**Joint compatibility** requires the chosen owners and remaining squares to coexist in
one physical packing.

A conditional global proof needs every hypothetical physical packing to admit at least
one valid owner selection whose residual domain has been excluded.
A surviving fractional witness for one selection does not prove that this global
requirement fails.

| Question or mechanism | First useful decision | Prerequisite and scope of a negative result |
| --- | --- | --- |
| Does fractional mass eleven exist for full units in $[3.83,3.85]$? | The rescaling in §1 already proves existence at $38200/9977$ | Export the unit family and replay it independently if a program needs to consume it; no search is required |
| Does the ordinary point obstruction begin below $L_*$? | Freeze a smaller target and obtain an exact finite witness or a globally certified cover below eleven | An interior/a.e. arrangement reader must accept touching controls and reject excess depth on positive area; a fixed-support value below eleven does not refute existence |
| Do additional atoms improve the covering problem at a fixed side? | Add an exactly violated atom, then require globally verified better coverage or a valid obstruction for the enlarged catalog | Alternate support and atom changes with full point-depth checks; a candidate with depth above one can suggest cuts but is not an obstruction |
| Does a retained obstruction satisfy conditional ownership? | Check the witness’s membership in the actual residual domain and the proposed ownership inequalities | Parent, mark, patch, joint-compatibility, and selection requirements must all be stated and checked |
| Is there a physical fractional gap for six squares below side three? | Exact fractional mass six proves a gap; a cover below six excludes such mass at the chosen side | Use integral controls at $L=3$ and a frozen target below three; bounded failure to find a family is inconclusive |
| Can the duality theorem become an admitted premise for later tools? | Retain the independent checks of the finite hitting set, weak closedness, mask LP, and smearing margin | This supplies value equality, not a numerical optimum, equality classification, or automatically complete separation algorithm |

Past $L_*$, the direct eleven-square problem needs counting capacities or geometric
relations beyond ordinary point depth.
Threshold charges already demonstrate that mechanism on the matched core model.
The next comparison must measure their effect on a globally covered pose domain or an
admitted conditional proof; eliminating one finite support is insufficient.

## 8. Review Provenance and Remaining Scope

The X-027 [structural-helper worker](research-2026-09-10-x027-structural-helpers.md)
independently reconstructed the interior-incidence duality argument before reading its
first draft. It then checked the rescaling, removal of the folded-net symmetry
restriction, compactness direction, finite Borel masks, smearing margin, and a.e.
equivalence. It also checked the rational finite-witness construction in §4 and the
three-square geometry in §5. Its disposition was PASS.

The X-027
[certificate-mechanisms worker](research-2026-09-10-x027-certificate-mechanisms.md)
independently checked the same arguments, the general core-selection implication, and A6
and six-square scope.
Its disposition was PASS. Its suggestions to state the reflection convention explicitly
and restrict the six-square negative to mass-six feasibility are incorporated.

These reviews are assurance checks on the arguments, not mathematical premises imported
from the sibling reports.
The source evidence and deductions are identified in the input table and the proofs.
The notation and explanatory revision preserves those claims, including the distinction
between finite-mass measures and finite lists of placements.

The results remain analytical and independently reviewed here, with no frontier
admission or novelty claim.
No finite optimal packing at the same side, attained optimal cover, exact value at
Trump’s side, new physical eleven-square integrality gap, or new global lower bound has
been established. The unit-family export, separate interior-depth instrument, and
prospective geometric comparisons remain unrun.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
