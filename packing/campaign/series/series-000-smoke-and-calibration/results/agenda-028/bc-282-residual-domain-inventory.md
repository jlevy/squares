# BC-282: Independent Residual-Domain Inventory

**Deleting square 10 gives a complete necessary ten-square domain, with seven
parameters, 40 containment inequalities and 45 full pair disjunctions.** Every
eleven-square point in the retained BC281 remainder maps into this domain.
The converse requires an extension by square 10 and is not established.

This is the independent domain inventory for
[session097](../../../../agent-sessions/session-097-residual-skeleton.md), BC282 and
`think-s6e7`. It reconstructs the definition from the frozen
[BC280 domain](bc-280-full-angle-release-domain.md) and
[BC281 independent audit](bc-281-full-angle-independent-review.md).
It does not assess the new BC282 design or supply a new geometric implication.
The separate design admission has not begun.

## Exact Retained Parameters and Geometry

Write

$$
q=(L,z,p_x,p_y,a,b,t),\qquad p=(p_x,p_y),
$$

with the unchanged bounds

$$
\begin{gathered}
381/100\le L\le96/25,\qquad 2\le z\le L-1,\qquad
p\in[1/2,7/2]^2,\\
-1/4\le a,b\le1/4,\qquad
t\in J_1\cup J_2,\\
J_1=[1/24,1/3],\qquad J_2=[1/2,23/25].
\end{gathered}
$$

Define

$$
c=\frac{1-t^2}{1+t^2},\quad s=\frac{2t}{1+t^2},\quad
e=(c,s),\quad f=(-s,c),\quad E=(1,0),\quad F=(0,1).
$$

The four block squares share this actual physical orientation.
There is no independent angle for each block square, averaged angle, fixed-side
substitution or reflection identifying the two retained intervals.
The denominator is positive.
In the retained intervals both $c$ and $s$ are positive; neither physical axis endpoint
is part of this remainder.

Squares 0–5 have basis $(E,F)$ and squares 6–9 have basis $(e,f)$. Their centers remain
exactly

$$
\begin{aligned}
C_0&=(1/2,1/2),&C_1&=(L-1/2,1/2),\\
C_2&=(z+1/2,L-1/2),&C_3&=(1/2,L-1/2),\\
C_4&=(3/2,L-1/2),&C_5&=(1/2,L-3/2),\\
C_6&=p,&C_7&=p+ae-f,\\
C_8&=p+e+bf,&C_9&=p+(a+1)e+(b-1)f.
\end{aligned}
$$

Each is an actual unit square $C_i+\{\xi e_i+\eta f_i:|\xi|,|\eta|\le1/2\}$. The
counterclockwise corner order is $C_i-(e_i+f_i)/2$, $C_i+(e_i-f_i)/2$,
$C_i+(e_i+f_i)/2$, $C_i+(-e_i+f_i)/2$. The source labels and contact sides are retained.

The nine flush wall incidences survive unchanged: square 0 left/bottom, 1 bottom/right,
2 top, 3 left/top, 4 top and 5 left.
The retained segments are 3–4 and 3–5 of length one; 6–7 and 8–9 of length $1-|a|$; and
6–8 and 7–9 of length $1-|b|$. The four latter lengths are at least $3/4$. The forced
4–5 point contact also survives.
Additional contacts are permitted.
This parameterization supplies no feasible motion or normal-form theorem.

## All Forty Containment Rows and Forty-Five Pair Clauses

For each retained square set

$$
H_i(n)=\frac{|n\cdot e_i|+|n\cdot f_i|}{2},\qquad
h_i=H_i(E)=H_i(F).
$$

Here $h_i=1/2$ for $0\le i\le5$ and $h_i=(c+s)/2$ for $6\le i\le9$. Retain all four
scalar inequalities for every $i\in\{0,\ldots,9\}$:

$$
C_{i,x}\ge h_i,\quad C_{i,x}\le L-h_i,\quad
C_{i,y}\ge h_i,\quad C_{i,y}\le L-h_i.
\tag{W}
$$

These are $10\cdot4=40$ rows, including rows already implied by the fixed centers and
parameter bounds. Since $h_i\ge1/2$, target containment puts every center in
$[1/2,167/50]^2$; the retained box bound on $p$ therefore omits no contained pose.

For every $0\le i<j\le9$, retain the single complete disjunction

$$
\bigvee_{n\in\{e_i,f_i,e_j,f_j\},\ \sigma\in\{-1,1\}}
\left[\sigma(C_j-C_i)\cdot n\ge H_i(n)+H_j(n)\right].
\tag{P}
$$

There are eight directed alternatives per pair, with repeated axes allowed.
They are alternatives in a union, not eight inequalities imposed simultaneously.
The complete inventory is

| Pair group | Pairs retained | Count |
| --- | --- | ---: |
| Six fixed axis squares | $0\le i<j\le5$ | $\binom62=15$ |
| Axis–block | $0\le i\le5$, $6\le j\le9$ | $6\cdot4=24$ |
| Four block squares | $6\le i<j\le9$ | $\binom42=6$ |
| Total | Every pair among 0–9 | $45$ |

Weak inequalities retain disjoint interiors with legal edge or point touching.
No source-selected axis or positive separation margin is imposed.
Every block diagonal, cross pair and wall row remains.
The deletion removes precisely square 10’s four wall rows and the ten pair clauses
$(i,10)$, $0\le i\le9$: $44-4=40$ and $55-10=45$.

## Four Closed Children and Their Boundaries

The block diagonal displacements in the common orthonormal basis are

$$
C_9-C_6=(1+a)e+(b-1)f,\qquad
C_8-C_7=(1-a)e+(1+b)f.
$$

Within the declared slide bounds, the first full pair clause reduces to
$(a\ge0\ \text{or}\ b\le0)$ and the second to $(a\le0\ \text{or}\ b\ge0)$. Together they
are equivalent to $ab\ge0$. Thus the complete domain is covered by the following four
closed children, each retaining every condition (W) and (P):

| Angle interval | Slide child |
| --- | --- |
| $J_1=[1/24,1/3]$ | $0\le a,b\le1/4$ |
| $J_1=[1/24,1/3]$ | $-1/4\le a,b\le0$ |
| $J_2=[1/2,23/25]$ | $0\le a,b\le1/4$ |
| $J_2=[1/2,23/25]$ | $-1/4\le a,b\le0$ |

The two sign children at a given angle intersect at $a=b=0$. If exactly one slide is
zero, the other slide determines its child.
All four slide endpoint faces, both side endpoints, both $z$ endpoints, containment
equalities, pair equalities and new contacts remain.
Retain the diagonal clauses even after writing this equivalent sign cover.

All four angle endpoints deliberately overlap previously excluded closed regions.
They remain in this definition so that no open-complement convention removes a seam.
The intervals are not identified by an established symmetry.
The former $c=s$ seam lies inside the already excluded intervening angle interval and is
not a missing child.
The domain is bounded and closed: its equations are continuous and each pair clause is a
finite union of closed conditions.

## Necessary Inclusion and Witness Meaning

Let $D_{10}$ denote exactly the seven-parameter domain above, and let
$R=\mathcal S_{\rm full}\cap\{t\in J_1\cup J_2\}$ be the retained eleven-square domain
from BC281. Let $\pi$ forget $(w_x,w_y,v)$. Directly deleting those coordinates and
their incident geometric conditions establishes

$$
\pi(R)\subseteq D_{10}.
\tag{I}
$$

This inclusion is enough for a uniform contradiction on $D_{10}$ to exclude $R$. It does
not establish $\pi(R)=D_{10}$. More precisely,

$$
\pi(R)=\left\{q\in D_{10}:\exists w\in[1/2,7/2]^2,\ v\in[0,1]
\text{ satisfying square 10's four wall rows and ten pair clauses}\right\}.
$$

The deleted variables have a nonempty standalone parameter box, so $D_{10}$ is the exact
projection of the *relaxed* eleven-square domain obtained by deleting those fourteen
geometric conditions while retaining the original ten scalar parameters.
It is not an established exact projection of the original feasible family.
No strictness or equality of inclusion (I) has been determined.

An exact feasible point of $D_{10}$ must satisfy the side, center, feature and sign
conditions together with all 40 wall rows and all 45 full pair clauses.
Such a point would refute the stronger claim that the ten-square skeleton is empty.
An eleven-square exclusion would still have to rule out this pose’s extension.
It would neither refute H120’s eleven-square family exclusion nor supply an
eleven-square packing upper bound.
An actual eleven-square witness additionally needs an exact $w,v$ and verification of
all four deleted wall rows and all ten deleted pair clauses.
Its chosen $v$ comes from the full $[0,1]$ chart; both endpoint lifts, $v=t$ and
possible recontacts stay legal.

The accepted BC281 lemmas keep their stated domains.
In particular, the count allowing four independent common-angle centers does not free
this domain’s four block contact equations: it is a reusable necessary lemma, not a
replacement definition.
The scalar failed-transfer controls from BC281 specify no feasible skeleton.
This inventory proves no target exclusion, finds no witness and admits no new target.

## Work Receipt

The independent domain-inventory assignment began at **17:21:22 UTC on September 7,
2026**, with a hard stop of **17:30:00 UTC**, including writing and checks.
This reviewer authored the frozen BC281 independent audit but has not read the new BC282
design, contacted its author about its reasoning, or proposed its novel implication.
The separate ten-minute design admission is reserved for dispatch after that design
freezes.

The checks are static reconstruction of the retained coordinates, unit-square supports,
row and pair counts, diagonal sign cover, closed endpoints and the direction of the
projection implication.
No scientific target, proof attempt, code, optimizer, new ID, source modification, Git
operation or shared-record edit is part of this inventory.
Only this assigned document is written.
Design admission and the complete residual determination remain open; the coordinator
owns their subsequent allocation.

Static reconstruction and content readback froze at **17:25:43 UTC**, 261 seconds after
the first clock. The common-document and prose passes were applied.
At **17:25:44 UTC**, the three linked native source files were confirmed to exist, the
required footer occurred once and the trailing-whitespace scan had no matches.
Installed Flowmark formatted only this file with its cache disabled; the final receipt
receives the same scoped formatting check before delivery.
No substantive continuation follows the freeze.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
