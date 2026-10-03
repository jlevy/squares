---
title: n17 Depth-Width Wall Lemma
date: 2026-10-02
status: planning-review
---
# n17 Depth-Width Wall Lemma

**Session:** 167, BC-406, lane G-proof.
**Baseline:** main at `e1f8b14b`, the commit of
`packing/devtools/check_n17_capacity_one_cover.py`. **Question:** is the depth-width
generalisation of the H259 wall lemma, which the
[bulk-exclusion design review](review-2026-10-02-n17-bulk-exclusion-design.md) uses and
[H-266](../../../packing/campaign/hypotheses/H-266-n17-minimal-capacity-one-cover.md)
rests on, a correct capacity-one proof for the side and corner cells of the 24-cell
cover, and with what margin?
It changes no bound, verdict or frontier field.
The numbers come from
[`wall_lemma.py.txt`](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-246-n17-capacity-one-cover/audit/wall_lemma.py.txt)
and `search2.py.txt`, retained under exp-246’s `audit/` (float maxima, an independent
exact Sturm count in sympy, and a pose search) and from the checker’s own receipt.

## Summary

- **The lemma is correct and sharp.** For a cell inside $[1/2,1/2+d]\times[y_0,y_0+w]$
  against the wall $x=0$, the separating gap of two contained interior-disjoint squares
  with centres in the cell is at most $G(c,s)=cd+sw-1-\tfrac c2(c+s-1)$ for every
  orientation of both squares.
  An explicit pair attains $G$ exactly, so $\max G<0$ over the closed quarter circle is
  necessary as well as sufficient.
- **The checker tests exactly this inequality,** with depth measured from the wall and a
  strict Sturm and Bernstein proof.
  Its side-cell interval $[-0.004663,-0.002578]$ contains the true maximum $-0.0035253$;
  its corner interval $[-0.028,-0.008125]$ contains $-0.0253242$.
- **Corner cells:** treating a corner as a wall cell of one wall is valid, since the
  second wall is not a premise; a square corner of side $0.78$ passes with margin
  $-0.0253$. Using both walls gives the exact condition
  $(d-\tfrac12)^2+(w-\tfrac12)^2<\tfrac14$, side below $(2+\sqrt2)/4=0.8536$, margin
  $-0.1040$ at $0.78$; the checker’s refusal of a $4/5$ corner is a refusal of the
  one-wall hypothesis, not a capacity-two finding.
- **Admissible curve:** $w_{\max}(0.911)=0.710292$, so the side width $529/750=0.70533$
  has $0.0050$ to spare; the curve lies strictly outside the unit circle, as it must.
  The pose search found nothing beyond the extremal pair, which penetrates by exactly
  $0.0035253=-\max G$.
- **One real subtlety, in the state model, not the lemma:** square 13 of the endpoint
  lies in two cells (`interior-S`, margin $0.0557$; `side-S1`, margin $0.0023$), so
  under the existential convention the family realises at least two states.
  “One state” in the receipt means a common state exists, not a unique one.

## 1. The Lemma and Its Proof

**Frame.** A unit square with centre $r$ and orientation $\varphi$ has orthonormal edge
directions $a_\varphi,b_\varphi$, support function
$H_\varphi(n)=(|n\cdot a_\varphi|+|n\cdot b_\varphi|)/2$ and axis support
$h_\varphi=H_\varphi(e_x)=H_\varphi(e_y)=(|\cos\varphi|+|\sin\varphi|)/2\in[\tfrac12,\tfrac1{\sqrt2}]$.
Containment in $x\ge0$ is $x\ge h_\varphi$. Two compact convex sets with disjoint
interiors have a unit $n$ with $g=n\cdot(r_j-r_i)-H_i(n)-H_j(n)\ge0$; touching gives
$g=0$, so every conclusion below needs a strict sign.

**Lemma 1 (support inequality).** For a unit normal $n=(c,s)$, $t=|c|+|s|$, and any
$A\ge0$, $$A\,h_\varphi+H_\varphi(n)\ \ge\ \min\Bigl(\frac{A+t}2,\ \frac{1+At}2\Bigr),$$
with the second value the minimum when $0\le A\le1$ and the first when $A\ge1$. This is
H259’s proof: reflecting $\varphi$ moves $n$ into the first quadrant without changing
$h_\varphi$; on each of $[0,\theta]$ and $[\theta,\pi/2]$ the function is a positive
combination of $\cos\varphi,\sin\varphi$, so concave, and its minimum is at an endpoint,
where the values are $(A+t)/2$ at the axes and $(1+At)/2$ at $\varphi=\theta$; their
difference is $(1-A)(t-1)$. H259 states the case $A\le1$; the case $A\ge1$ is used for
corners below.

**Lemma 2 (one-wall cell).** Let $S_i,S_j$ be unit squares with disjoint interiors, both
in $\lbrace x\ge0\rbrace$, with centres in the closed rectangle
$R=[\tfrac12,\tfrac12+d]\times[y_0,y_0+w]$. Then, after exchanging labels so that the
separating normal from $S_i$ to $S_j$ has $c\ge0$ and reflecting in the line $y=y_0+w/2$
so that $s\ge0$,
$$0\le g\le c\Bigl(\tfrac12+d\Bigr)+sw-\bigl[c\,h_i+H_i(n)\bigr]-H_j(n)\le G(c,s):=cd+sw-1-\frac c2(c+s-1).$$
Hence **$\max G<0$ on the closed quarter circle implies capacity one for the closed
cell.** The bound uses $x_j\le\tfrac12+d$ (this is the only place depth enters),
$|y_j-y_i|\le w$ (the only place width enters), $x_i\ge h_i$, Lemma 1 with $A=c$, and
$H_j(n)\ge\tfrac12$. It does not use $x_j\ge h_j$, the near edge of the cell, or any
other wall. Two consequences: the lemma holds for any cell contained in $R$, and $d$ is
the distance from the wall-side edge of the centre box to the cell’s far edge, not the
cell’s own extent; `wall_extents` in the checker computes $\max x-\tfrac12$, which is
right.

**The reductions preserve the premises for every $d,w$.** The label exchange replaces
$n$ by $-n$ and swaps $i,j$; support functions are even, so $g$ is unchanged.
The reflection $y\mapsto2y_0+w-y$ is an isometry fixing $x$: it preserves disjointness
and the half-plane, maps the cell onto itself whatever $d$ and $w$ are, and sends
$(c,s)$ to $(c,-s)$. It moves the other three container walls, which is why the lemma
must be stated with the one half-plane as its only wall premise.

**Sharpness.** Let $\theta^\ast$ maximise $G$ and
$t^\ast=\cos\theta^\ast+\sin\theta^\ast$. Put both squares at orientation $\theta^\ast$,
$S_i$ at $(t^\ast/2,\,y_0)$ on the wall, $S_j$ at $(\tfrac12+d,\,y_0+w)$. Every
inequality in Lemma 2 is an equality, so the gap along $n^\ast$ is exactly
$G(\theta^\ast)$: `search2.py` evaluates this pair directly and finds gap $=\max G$ to
seven decimals at four $(d,w)$. If $\max G\ge0$ the pair is a valid interior-disjoint
pair with both centres in the closed cell, so **the condition is necessary.** For the
design’s side cells the pair fits in $[0,U]^2$ (its extent is within $[0.57,2.70]$
tangentially and below $2.12$ in depth), so the side cells are admissible exactly when
$\max G<0$. If $\max G=0$ the pair touches, with both centres at corners of the closed
cell: strictness is needed and the closed cell is the right object.
A seam rule that assigns a centre to any containing closed cell inherits capacity one.

## 2. Corner Cells

A corner cell $[\tfrac12,\tfrac12+d]\times[\tfrac12,\tfrac12+w]$ is a wall cell of its
vertical wall with the same $d,w$; Lemma 2 applies verbatim and the horizontal wall is
unused, so the checker’s corner rule is valid.
For a square corner this certifies $a<a_1=0.798347$, and $a=0.78$ passes with
$\max G=-0.0253242$ at $57.77^\circ$.

**Lemma 3 (two walls).** With both squares in the quadrant $x,y\ge0$, exchange labels so
$c\ge0$; no reflection is needed.
If $s\ge0$, bound $x_j\le\tfrac12+d$, $y_j\le\tfrac12+w$, $x_i,y_i\ge h_i$ and apply
Lemma 1 with $A=t\ge1$: $g\le G_2:=cd+sw-(t+1)/2$. If $s\le0$, bound $x_j\le\tfrac12+d$,
$y_i\le\tfrac12+w$, $x_i\ge h_i$, $y_j\ge h_j$ and apply Lemma 1 twice with $A=c$ and
$A=|s|$: $g\le G_3:=cd+|s|w-1-t(t-1)/2=G_2-(t-1)^2/2$. Both are attained (an
axis-aligned square in the corner and a square at the far corner facing it along $n$;
two squares at orientation $\theta$ on the two walls), and $G-G_2=(t-1)(1-c)/2\ge0$, so
Lemma 3 is never worse than Lemma 2. For $d,w\ge\tfrac12$ the maximum of $G_2$ is
$\sqrt{(d-\tfrac12)^2+(w-\tfrac12)^2}-\tfrac12$: **a corner cell has capacity one
exactly when its far corner is within distance $\tfrac12$ of the point $(1,1)$,** the
far vertex of the axis-aligned square in the corner.
A square corner is admissible for $a<(2+\sqrt2)/4=0.853553$; at $0.78$ the margin is
$-0.104020$. The checker’s control “corner $4/5$ refused” is therefore a refusal of the
one-wall hypothesis ($\max G=+0.00228$); that cell has capacity one by Lemma 3 (margin
$-0.0757$).

## 3. Overlapping Cells and the Existential Convention

Capacity is a statement about one closed cell, so overlaps leave it untouched: under the
H260 convention every assignment of centres to containing cells is injective, every
packing has at least one state, and a packing with a centre in an overlap has several.
A sub-pattern certificate says that no $|J|$ squares have centres in the closed cells of
$J$, which is independent of any assignment, so excluding every state containing $J$ is
sound under overlaps and under any seam rule; nothing in the engine needs to change.

What changes is the reading of “the family lies in one state”.
The receipt’s `family_one_state_triangle: true` means one assignment holds every member
with margin $\ge1/1000$ inside its assigned cell.
The same receipt lists square 13 in both `interior-S` ($0.0557$) and `side-S1`
($0.0023$), and `side-S1` is empty in the chosen state, so the endpoint family also
realises the state with `interior-S` replaced by `side-S1`, and no sound engine can
exclude it.
The residue therefore contains at least two endpoint states, and capture must
cover each. The checker should report, beside the common state, whether every member is
in exactly one cell by margin, which needs distance $\ge1/1000$ *outside* every other
cell; today that is false for square 13. The $0.131$-squares where two side cells meet
near each corner hold no endpoint centre, but the same report covers them.

## 4. Margins and the Admissible Curve

| Cell | $(d,w)$ | $\max G$ (6 dp) | at $\theta^\ast$ | Checker interval | Sturm roots in $[0,1]$ |
| --- | --- | ---: | ---: | --- | ---: |
| Side | $(911/1000,\,529/750)$ | $-0.003525$ | $45.12^\circ$ | $[-0.004663,-0.002578]$ | 0 |
| Corner, one wall | $(39/50,\,39/50)$ | $-0.025324$ | $57.77^\circ$ | $[-0.028000,-0.008125]$ | 0 |
| Corner, Lemma 3 | $(39/50,\,39/50)$ | $-0.104020$ | $45^\circ$ | not computed | — |
| H259 cell | $(919/1250)^2$ | $-0.086996$ | $58.74^\circ$ | accepted | 0 |
| H259 bound | $(3/4,\,3/4)$ | $-0.066649$ | $58.40^\circ$ | accepted | 0 |
| Refused | $(4/5,\,4/5)$ | $+0.002283$ | $57.36^\circ$ | refused at $\tau=1/2$ | 2 |
| Refused | $(911/1000,\,3/4)$ | $+0.029010$ | $48.26^\circ$ | refused at $\tau=1/2$ | 2 |

The Sturm column is an independent sympy count on the same quartic
$P(\tau)=(1+\tau^2)^2G$, whose coefficients I re-derived and which match
`wall_polynomial`. The float maxima are refined by bounded scalar minimisation after a
$2\times10^5$-point grid; the checker’s intervals are the rigorous ones.

Solving $G<0$ for $w$ gives the admissible width for a depth $d<1$,
$$w_{\max}(d)=\inf_{0<\theta\le\pi/2}\ \frac{1-cd+\tfrac c2(c+s-1)}{s},$$ and the cell
is admissible exactly when $w<w_{\max}(d)$. Values: $d=0.5$: $0.9308$; $0.6$: $0.8969$;
$0.7$: $0.8534$; $0.735$: $0.8354$; $0.75$: $0.8272$; $0.78$: $0.8098$; $0.8$: $0.7973$;
$0.85$: $0.7625$; $0.9$: $0.7208$; $0.911$: $0.7103$; $0.95$: $0.6666$; $0.99$:
$0.5884$. The design review’s $0.705$ at $0.911$, $0.835$ at $0.735$ and corner $0.798$
agree to their stated precision.
At $0.911$ the side width has $0.004959$ to spare: thin, but exact.
Since the lemma is sharp and a cell of diameter below one has capacity one by the
inscribed-disc argument, $w_{\max}(d)>\sqrt{1-d^2}$ must hold, and it does at every
tabulated $d$ ($0.7103$ against $0.4124$ at $0.911$). n11’s cover used only the diameter
argument
([PROOF.md, section 4](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md)),
so its cells lie inside the circle and hence inside the admissible region.

## 5. Interior Cells

Each unit square contains the open disc of radius $\tfrac12$ about its centre, so two
interior-disjoint squares have centres at distance at least one, in every orientation,
and a cell of diameter strictly below one holds at most one centre.
Diameter exactly one is not enough for a closed cell: two squares both oriented along
the chord joining two points at distance one touch along an edge, so both endpoints can
be centres. The checker’s strict `squared_diameter < 1` over vertex pairs is the right
test for a convex polygon, and its unit-diameter control is refused; the tabbed axis
cells that reach into the ring pass by the same test.

## 6. Counterexample Search

`search2.py` maximises the separation $\sigma$, the largest projection gap over the
eight signed edge normals, which is nonnegative exactly when the squares are
interior-disjoint, over both centres in the cell and both orientations, with containment
in $[0,U]^2$ as a penalty: differential evolution from six seeds, then a bounded
Nelder–Mead polish, with the extremal pair as a seventh start.
For the side cell at $(0.911,529/750)$ the best pose is the extremal pair, centres
$(1.28,0.70711)$ and $(1.98533,1.411)$ at orientation $\pi/2-\theta^\ast$, with
$\sigma=-0.0035253$. At width $0.7104$, just past $w_{\max}$, it returns
$\sigma=+0.0000773=\max G$, a genuine two-centre pair; at $0.72$, $\sigma=+0.0069698$.
For the $0.78$ corner with both walls it returns $\sigma=-0.1040202=\max G_2$ at the
Lemma 3 pair, an axis-aligned square at $(\tfrac12,\tfrac12)$ and a diagonal one at
$(1.28,1.28)$. Rational witnesses for the checker’s refusals follow the same recipe: at
$(911/1000,3/4)$ the direction $(3/5,4/5)$ gives a pair with exact gap $133/5000$, and
at $(4/5,4/5)$ with one wall the direction $(28/53,45/53)$ gives $31/14045$. The best
near-miss inside the curve is always the extremal pair, as sharpness predicts.

## 7. What the Checker Should Do

1. Keep the inequality, the wall-measured depth and the strict Sturm-and-Bernstein proof
   as they are; they match the lemma as stated here.
2. Add the rational witness pairs above as negative controls, so that a refusal is seen
   to be geometric at $(911/1000,3/4)$ and merely one-wall at $(4/5,4/5)$.
3. Report a unique-state flag beside `one_state`, and record that the endpoint family
   realises at least two states through square 13; BC-410 can move the tab, accept both
   states in capture, or shrink `side-S1`.
4. If a future design needs corners above $0.798$, certify them by the circle condition
   of Lemma 3 rather than the one-wall quartic.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
