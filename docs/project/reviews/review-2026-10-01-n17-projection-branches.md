---
title: n17 Conditional Minimum Under Directed Projection Branches
date: 2026-10-01
status: mathematical-review
---
# n17 Conditional Minimum Under Directed Projection Branches

The n17 necessary inequalities $F_1\ge0$, $F_2\ge0$, and $G_3=F_3+\alpha F_2\ge0$ hold
under weaker orientation assumptions than the equality chart.
Squares 1 through 8 and square 13 may have arbitrary orientations.
Squares 15 and 17 may rotate in an explicit interval about axis alignment.
The remaining premises include 19 directed projection inequalities and a common
orientation for squares 9, 10, 11, 12, and 14. These premises define the conditional
family; their validity for all nearby feasible packings remains unproved.

This is an analytic derivation, without target sampling or a new solver run.
The
[opening review](review-2026-10-01-post-optimality-w3-opening.md#necessary-inequalities-with-slack-contacts)
contains the original necessary system and its monotonicity proof.
[H-254](../../../packing/campaign/hypotheses/H-254-n17-contact-chart-fidelity.md)
records chart fidelity and the contact labels;
[H-255](../../../packing/campaign/hypotheses/H-255-n17-exact-polynomial-root.md)
establishes the exact equality root.
The separate
[H-256 criterion](../../../packing/campaign/hypotheses/H-256-n17-exact-endpoint-feasibility.md)
checks a packing at that root and supplies the strict-clearance premise used in the
rotational argument below.

## Definitions and Premises

For square $i$, let $r_i=(x_i,y_i)$ be its centre and let $H_i(a)$ be its support radius
in unit direction $a$. A unit square at orientation $\phi$ has

$$
H_\phi(a)=\frac{|a\cdot(\cos\phi,\sin\phi)|+
|a\cdot(-\sin\phi,\cos\phi)|}{2}.
$$

Write

$$
u=(c,s),\quad v=(-s,c),\quad w=-v,\quad
p=(d,-e),\quad q=(e,d),
$$

$$
c=\frac{1-t^2}{1+t^2},\quad s=\frac{2t}{1+t^2},\quad
d=\frac{1-b^2}{1+b^2},\quad e=\frac{2b}{1+b^2},
\qquad \alpha=cd-se,\quad\gamma=ce+sd.
$$

Thus $t=\tan(\theta/2)$ and $b=\tan(\beta/2)$. Work throughout the H254 box

$$
S\in[4.675,4.676],\qquad t\in[0.36,0.37],\qquad b\in[0.33,0.34].
$$

Every terminating decimal in this review denotes an exact rational number.
The denominators and $c,s,d,e,\alpha,\gamma$ are positive on this box.
Squares 9, 10, 11, 12, and 14 have basis $u,v$; square 16 has basis $p,q$. All squares
are contained in $[0,S]^2$. No wall equality is assumed.

For the other squares define

$$
h_i=H_i(e_x)=H_i(e_y),\qquad g_i=H_i(u)=H_i(w),\qquad k_i=H_i(p)=H_i(q).
$$

These equalities hold for every square orientation, since a square is invariant under a
quarter turn. Require the following directed inequalities, where an entry $i\to j$ in
direction $a$ means $a\cdot(r_j-r_i)\ge H_i(a)+H_j(a)$:

| Direction | Directed pairs |
| --- | --- |
| $e_x$ | $1\to2$ |
| $e_y$ | $1\to3$, $5\to7$, $3\to9$ |
| $u$ | $9\to10$, $10\to15$, $3\to11$, $11\to12$, $2\to13$, $13\to14$, $14\to17$, $12\to16$ |
| $w$ | $4\to10$, $10\to12$, $12\to14$, $14\to7$ |
| $p$ | $15\to16$, $16\to17$ |
| $q$ | $16\to8$ |

These are the 19 H254 branches used by the necessary-system proof.
The defining equality-chart contact $9\to11$ along $w$ is unused.
Square 6 occurs in none of these inequalities.

The last orientation assumptions are the two weighted support bounds

$$
W_{15}:=\gamma h_{15}+d g_{15}+c k_{15}\ge cd+\gamma,
\qquad
W_{17}:=\gamma h_{17}+e g_{17}+s k_{17}\ge se+\gamma.
$$

The explicit angle windows proved below suffice for both bounds.
Angles of squares 1 through 8 and square 13 are otherwise unrestricted.
Containment and pairwise nonoverlap with square 6 do not enter the lower-bound argument:
it applies to the specified 16-square arrangement even before a seventeenth square is
added. This does not assert a lower bound for arbitrary arrangements of 16 squares.

## Universal Support Bound

For every unit-square orientation $\phi$ and $u=(c,s)$ with $c,s>0$ and $c^2+s^2=1$,

$$
(c+s)H_\phi(e_x)+H_\phi(u)\ge c+s.
$$

To prove this, reduce $\phi$ modulo $\pi/2$ to $[0,\pi/2]$. With
$h_\phi=(\cos\phi+\sin\phi)/2$, the left side is

$$
\begin{cases}
(c+s)\cos\phi+s\sin\phi,&0\le\phi\le\theta,\cr
c\cos\phi+(c+s)\sin\phi,&\theta\le\phi\le\pi/2.
\end{cases}
$$

Each expression has negative second derivative on its interval, so its minimum is
attained at an endpoint.
The values at $0,\pi/2$ are $c+s$; the value at $\theta$ is $1+cs$, and

$$
1+cs-c-s=(1-c)(1-s)>0.
$$

This proves the bound, with equality only at axis alignment modulo $\pi/2$. Since
$H_\phi(w)=H_\phi(u)$, it also applies along $w$. Applying the same result to the
positive components of $q$ gives

$$
(d+e)h_i+H_i(q)\ge d+e.
$$

Every unit square also satisfies $h_i\ge1/2$ and $H_i(a)\ge1/2$ for any unit $a$.

## Necessary Inequalities

Define the same scalar functions as in the equality chart:

$$
X_0=\frac12+\frac{2+cs+3s-sS}{c},\qquad
Y_0=\frac32+\frac{2+3c-cS}{s},
$$

$$
A_0=d(X_0+1/2)-e(S-1)+1/2,\qquad
A_{\max}=d(S-1)-e(Y_0+1/2)-1/2,
$$

$$
B_0=(d+e)(S-1)-1/2,
$$

$$
F_1=c(S-3)+s(S-2)-3,\qquad F_2=A_{\max}-A_0,
$$

$$
F_3=\alpha(A_0-1/2)+\gamma(B_0-1/2)-(c+2s+2),
\qquad G_3=F_3+\alpha F_2.
$$

**Initial bounds.** Containment and the first three directed branches imply

$$
x_2\ge x_1+h_1+h_2\ge2h_1+h_2\ge1+h_2,
$$

$$
y_3\ge y_1+h_1+h_3\ge1+h_3,\qquad
y_7\ge y_5+h_5+h_7\ge1+h_7.
$$

This uses only $h_1,h_5\ge1/2$, so the orientations of squares 1 and 5 are free.
Let $U_i=u\cdot r_i$. The universal support bound and $3\to11\to12$ give

$$
U_3\ge s+(c+s)h_3,\qquad
U_{11}\ge U_3+g_3+1/2\ge c+2s+1/2,
\qquad U_{12}\ge c+2s+3/2.
$$

For square 9 put $h=(c+s)/2$. Containment gives $x_9\ge h$, while $3\to9$ gives
$y_9\ge1+2h_3+h\ge2+h$. Therefore

$$
U_9\ge\frac12+cs+2s,\qquad
U_{15}\ge C_{15}+g_{15},\qquad C_{15}=2+cs+2s.
$$

Similarly, using $2\to13\to14\to17$,

$$
U_2\ge c+(c+s)h_2,\qquad U_{13}\ge2c+s+g_{13},
$$

$$
U_{14}\ge2c+s+2g_{13}+1/2\ge2c+s+3/2,
\qquad U_{17}\ge C_{17}+g_{17},\qquad C_{17}=2c+s+2.
$$

Only $g_{13}\ge1/2$ was used; square 13 need not share the common orientation when both
of its projection inequalities along $u$ are retained.

**The $w$ chain.** The chain $4\to10\to12\to14\to7$ requires projected distance at least
$g_4+g_7+3$. Containment and $y_7\ge1+h_7$ give

$$
w\cdot(r_7-r_4)\le(c+s)S-c-(c+s)(h_4+h_7).
$$

Consequently

$$
(c+s)S-c-3\ge[(c+s)h_4+g_4]+[(c+s)h_7+g_7]\ge2(c+s),
$$

which is $F_1\ge0$.

**The bridge through square 16.** Write $A=p\cdot r_{16}$ and $B=q\cdot r_{16}$ for the
actual projections. Square 16 has $H_{16}(p)=H_{16}(q)=1/2$. Since
$p\cdot r=(d/c)(u\cdot r)-(\gamma/c)y$, the branch $15\to16$ implies

$$
A\ge\frac{dC_{15}-\gamma S+W_{15}}{c}+\frac12
\ge\frac{dC_{15}-\gamma S+cd+\gamma}{c}+\frac12=A_0.
$$

Here $U_{15}\ge C_{15}+g_{15}$ and $y_{15}\le S-h_{15}$ were used.
Likewise, $p\cdot r=(\gamma/s)x-(e/s)(u\cdot r)$, so $16\to17$ gives

$$
A\le\frac{\gamma S-eC_{17}-W_{17}}{s}-\frac12
\le\frac{\gamma S-eC_{17}-se-\gamma}{s}-\frac12=A_{\max}.
$$

This time use $x_{17}\le S-h_{17}$ and $U_{17}\ge C_{17}+g_{17}$. The branch $16\to8$
and the universal support bound for $q$ give

$$
B\le(d+e)(S-h_8)-H_8(q)-\frac12
\le(d+e)(S-1)-\frac12=B_0.
$$

Thus $F_2=A_{\max}-A_0\ge0$. Finally, $u=\alpha p+\gamma q$, $H_{12}(u)=1/2$, and
$H_{16}(u)=(\alpha+\gamma)/2$. The branch $12\to16$ yields

$$
\alpha(A-1/2)+\gamma(B-1/2)\ge U_{12}+1/2\ge c+2s+2.
$$

Both $\alpha$ and $\gamma$ are positive.
Substituting the upper bounds on $A,B$ therefore gives $G_3\ge0$. No selected contact
has been assumed saturated.

## Explicit Angle Windows for Squares 15 and 17

Choose the representative of each square’s angle near zero modulo $\pi/2$. The required
support formulas hold whenever $0<\theta-\phi<\pi/2$ and $0<\beta+\phi<\pi/2$:

$$
H_\phi(u)=\frac{(c+s)\cos\phi+(s-c)\sin\phi}{2},\qquad
H_\phi(p)=\frac{(d+e)\cos\phi+(d-e)\sin\phi}{2}.
$$

Put $a_{15}=cd+\gamma$ and $a_{17}=se+\gamma$. Direct substitution in the two weighted
expressions gives, for either $j=15,17$,

$$
W_j(\phi)=
\begin{cases}
a_j\cos\phi+ds\sin\phi,&\phi\ge0,\cr
a_j\cos\phi-ce\sin\phi,&\phi\le0.
\end{cases}
$$

For $r=\tan(\phi/2)\ge0$,

$$
W_j-a_j=\frac{2r(ds-a_jr)}{1+r^2}.
$$

For $r\le0$, put $z=-r\ge0$; then

$$
W_j-a_j=\frac{2z(ce-a_jz)}{1+z^2}.
$$

The rational coarse bounds from the opening review are

| Quantity | Lower | Upper |
| --- | --- | --- |
| $c$ | $0.7591$ | $0.7706$ |
| $s$ | $0.6373$ | $0.651$ |
| $d$ | $0.792$ | $0.804$ |
| $e$ | $0.595$ | $0.610$ |
| $\alpha$ | $0.204$ | $0.241$ |
| $\gamma$ | $0.956$ | $0.994$ |

They imply

$$
ds\ge0.5047416,\qquad ce\ge0.4516645,\qquad
a_{15}\le1.6135624,\qquad a_{17}\le1.39111.
$$

Hence the fixed windows

$$
\left|\tan\frac{\phi_{15}}2\right|\le\frac1{10},\qquad
\left|\tan\frac{\phi_{17}}2\right|\le\frac1{10}
$$

imply both weighted support bounds, strictly away from axis alignment.
Their support signs also hold uniformly: $|\phi|\le2\arctan(1/10)<0.2$;
$\theta\ge s\ge0.6373$, $\beta\ge e\ge0.595$, and $\theta,\beta<\pi/4$. Therefore both
$\theta-\phi$ and $\beta+\phi$ belong to $(0,\pi/2)$. This is a sufficient local
interval; no assertion about the weighted expressions at all orientations is needed.

## Conditional Minimum and the Capture Problem

The opening review proves, throughout the same parameter box, that
$g(\theta)=2+(c+3)/(c+s)$ strictly decreases and that, with $J=F_2+G_3$,

$$
(F_2)_S>0,\quad(F_2)_\theta<0,\quad(F_2)_\beta<0,
\qquad J_S>0,\quad J_\theta<0,\quad J_\beta>0.
$$

Let $(S_{\ast},\theta_{\ast},\beta_{\ast})$ be the H255 equality root.
If a packing satisfying the premises above had $S<S_{\ast}$, then $F_1\ge0$ would force
$\theta>\theta_{\ast}$. The signs of the $F_2$ derivatives would then force
$\beta<\beta_{\ast}$. All three changes strictly decrease $J$ from its root value zero,
contradicting $F_2,G_3\ge0$. Thus every packing in this conditional family has
$S\ge S_{\ast}$. Endpoint feasibility is the separate H256 obligation.

**Equality of the backbone angles.** Suppose $S=S_{\ast}$ and use the explicit windows
for squares 15 and 17. The same monotonicity argument first gives
$\theta=\theta_{\ast}$: $F_1\ge0$ forces $\theta\ge\theta_{\ast}$, and a strict
inequality would force $\beta<\beta_{\ast}$ and then $J<0$. With $\theta=\theta_{\ast}$,
$F_2\ge0$ forces $\beta\le\beta_{\ast}$, while a strict inequality again makes $J<0$.
Thus $\beta=\beta_{\ast}$ and $F_1=F_2=G_3=0$.

All inequalities used above have nonnegative slack.
Equality in the $w$ chain forces the universal support bounds for squares 4 and 7 to be
equalities, so those squares are axis-aligned.
Equality in its endpoint containment bound also gives $y_7=1+h_7$. Since
$y_7\ge2h_5+h_7$, square 5 has $h_5=1/2$ and is axis-aligned.

From $F_2=0$ and $A_0\le A\le A_{\max}$, both bounds on $A$ are equalities.
The coefficients $d/c,\gamma/c,e/s,\gamma/s$ are strictly positive.
Hence the weighted support bounds for squares 15 and 17 are equalities, and the explicit
windows force both angles to be zero modulo $\pi/2$. Their chains also satisfy
$U_{15}=C_{15}+g_{15}$ and $U_{17}=C_{17}+g_{17}$. The first equality forces
$U_9=1/2+cs+2s$, hence $x_9=h$ and $y_9=2+h$. But the earlier branches give
$y_9\ge2h_1+2h_3+h$; since each of $h_1,h_3$ is at least $1/2$, both equal $1/2$.
Squares 1 and 3 are therefore axis-aligned.

The second chain equality forces $U_{14}=2c+s+3/2$. Its lower bound contains the
nonnegative terms $(c+s)h_2+g_2-(c+s)$ and $2(g_{13}-1/2)$, so both vanish.
The universal support equality makes square 2 axis-aligned, and $H_{13}(u)=1/2$ makes
square 13 aligned with $u,v$ modulo a quarter turn.
Finally $G_3=0$, $A=A_{\max}$, $B\le B_0$, and $\gamma>0$ force $B=B_0$. The universal
support bound for square 8 is then an equality, so square 8 is axis-aligned.

Thus all relaxed backbone angles recover the original classes at the endpoint side,
under the directed projection premises.
This conclusion concerns orientations; it does not fix every centre or remove the
translational sliders.
Square 6 remains absent from the argument.
It does not establish that arbitrary nearby feasible packings satisfy these projection
premises.

A directed projection inequality in a specified direction guarantees separation.
Mere nonoverlap guarantees separation along at least one appropriate square edge normal,
which can vary with the square orientations.
When both owners of an active axis rotate, the fixed direction in the table need not
remain an edge normal.
Even when one owner keeps that direction, the other owner’s rotated normal may supply
the separating branch instead.
Nonoverlap alone therefore does not imply the table’s fixed projection inequality.
The arbitrary-angle conclusion for square 13 has this same qualification: both directed
$u$ inequalities remain explicit premises.

A local minimum theorem needs a neighbourhood in which every feasible perturbation,
possibly after an allowed relabelling or symmetry, satisfies these premises or belongs
to another family with its own lower bound.
The two small windows for squares 15 and 17 follow from sufficiently small angular
perturbations. Common orientation of 9, 10, 11, 12, and 14 and coverage of the directed
branches still require proof.
The parameter box supplies no coverage of distant configurations.

## Rotational Freedom and the Next H027 Discriminator

At the H256 centroid reconstruction, square 6 has centre $(a,1/2)$ and only its bottom
wall is declared active.
H256 requires strict separation for all 16 pairs involving square 6, and strict
clearance from its other three walls.
Once these strict clauses are certified, keep the side and all other squares fixed and
replace square 6 by

$$
\phi_6=\varepsilon,\qquad
r_6(\varepsilon)=\left(a,
\frac{|\cos\varepsilon|+|\sin\varepsilon|}{2}\right).
$$

The bottom support clearance stays zero.
Every other required clearance is continuous and strictly positive at $\varepsilon=0$,
so all remain positive for sufficiently small $|\varepsilon|$. This is a continuous
family of feasible rotations at unchanged side.
It disproves a proposed capture statement requiring every nearby packing to retain all
original angle classes.
It supplies neither a smaller packing nor a refutation of local or global minimality.
The strengthened necessary theorem already omits square 6.

[H-027](../../../packing/campaign/hypotheses/H-027-record-angle-cones.md) asks about
independent *class-angle* directions with class assignments fixed.
An individual square-6 rotation is outside that stated regime, so it does not reject
H027. Any extension to independent square angles must account for this zero-side
direction and the translational sliders before claiming a positive lower bound on a unit
sphere.

A bounded next discriminator under H027 is a complete first-order feasibility cone at
the endpoint, with an explicit distinction between class-angle directions and split
orientations. Its input contract must certify all active walls, owner-axis alternatives
at the 21 zero-contact pairs, and strictly inactive alternatives.
At parallel faces, the two owner normals coincide at the endpoint but split when the
owners rotate; they cannot be discarded by deduplicating their base directions.
The additional 2/3 corner contact requires its two possible separating axes as well.
The fixed contact-equality rank alone omits these alternatives.

For each complete first-order branch, a nonnegative dual proving $\dot S\ge0$ would
establish first-order stationarity.
A zero-side direction needs higher-order or exact continuation analysis before it can
support or refute a local minimum.
A putative negative-side direction likewise needs a feasible continuation to demonstrate
an improvement. H027’s numerical derivative threshold additionally needs its declared
quotient, norm and competing LP bases; a stationarity certificate alone does not meet
that criterion.

The existing [Trump tangent-cone tool](../../../packing/cases/trump11/tangent_cones.py)
retains owner-axis branches, while the generic
[local-rigidity system](../../../packing/src/sqpack/local_rigidity/system.py) explicitly
refuses disjunctive touches.
These are implementation references, not an already complete n17 instrument.
The separate
[H-248 weighted-family test](../../../packing/campaign/hypotheses/H-248-n17-clique-weighted-family-at-4-675.md)
concerns a global lower-bound architecture; it does not discharge local branch capture.

## Scope Note After the Route Review

*Added 2026-10-01 by Session 166.* The
[route review](review-2026-10-01-n17-route-after-pr265.md) re-derived this theorem and
found no error. Three scope facts stated above in passing are worth reading together:

- The box covers $S\in[4.675,4.676]$ only.
  Premise-satisfying packings with $S\in(4.66044,4.675)$ are outside it, although a grid
  shows the same derivative signs on $[4.66,4.676]$.
- The angle box reaches only $0.17^\circ$ below $\theta^{\ast}$, and its monotonicity
  proof does not extend unchanged to $t\in[0.33,0.40]$, $b\in[0.30,0.37]$.
- The premise $W_{17}\ge se+\gamma$ holds at every orientation of square 17. The premise
  $W_{15}\ge cd+\gamma$ fails when square 15 is co-oriented with square 16, which is a
  separate branch.

The theorem therefore remains a conditional sanity bound.
The terminal theorem is now H-261, a local minimum modulo the slider cone.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
