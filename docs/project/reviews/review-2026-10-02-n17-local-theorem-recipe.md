---
title: n17 Local Theorem Modulo Sliders — Argument Review and Instrument Recipe
date: 2026-10-02
status: planning-review
---
# n17 Local Theorem Modulo Sliders — Argument Review and Instrument Recipe

**Session:** 167 (BC-406), lane A2-review.
**Baseline:** main after PR 265 and PR 269. **Reviews:** the
[route review](review-2026-10-01-n17-route-after-pr265.md#the-endpoint-is-a-first-order-minimum-modulo-its-sliders)
(sections “The Endpoint Is a First-Order Minimum Modulo Its Sliders” and “The Terminal
Theorem”),
[H-261](../../../packing/campaign/hypotheses/H-261-n17-local-minimum-modulo-sliders.md),
[H-258](../../../packing/campaign/hypotheses/H-258-n17-common-core-stress.md), the
[core-stress](review-2026-10-01-n17-core-stress.md) and
[first-order](review-2026-10-01-n17-first-order-branches.md) derivations, the n11 proof
(PROOF.md, section 7), and the
[X-048 receipts](../../../packing/campaign/explorations/X048-route-review/README.md).

This is an adversarial read of the two arguments the route review gives for “the local
theorem needs no second-order analysis”, and a frozen recipe for what
`devtools/check_n17_local_minimum.py` must certify.
It changes no bound, frontier field or verdict.
Exploratory numbers below come from four scratch scripts (`local_theorem_probe.py`,
`probe2.py`, `probe3.py`, `probe4.py` in the session scratchpad, not in the record); the
section “Evidence Status” says which statements rest on them.

## Verdicts

| Claim | Verdict | Repair or gap |
| --- | --- | --- |
| (a) First-order conical minimum modulo the kernel, plus n11’s focused rectangle with sliders excluded from saturation, gives a strict local minimum modulo the slider family with an explicit radius | **Sound with stated repairs** | The base point must move with the sliders (expand about $x^\ast(w)$, $w$ read off the packing), so the duals and curvature constants are needed at every $w$ in the slider box, not at the centroid. The two-row parallel-face reduction needs a Taylor-remainder lemma (stated below). Square 6, the six zero-weight rows, the $2/3$ corner, the non-contact pairs and the inactive walls are dropped, which is a weakening. |
| (b) Direct argument: $o_i=A_ih$ plus a remainder $\le K\lvert h_{\rm ang}\rvert\lvert h\rvert$, injectivity of $A$ off the kernel, kernel carries no angle except $\omega_6$ | **Sound as an existence argument, with repairs; not the instrument** | Correct once the remainder excludes $\omega_6$ (true after square 6 leaves), the norm is on the non-slider coordinates after re-basing, and $s_{\min}$ and $\lambda_{\max}/\lambda_{\min}$ are taken uniformly over the slider box. Its radius $s_{\min}/C_1$ is far below the ratio test’s. “No angle except $\omega_6$ in the kernel” is exactly the hypothesis needed, in both arguments. |
| The product neighbourhood (box in 45 coordinates) × (whole physical slider domain) | **Legitimate**, with the slider domain replaced by a box in three translation parameters $(a,b,z)$ and square 6 unconstrained | $A(w)$ is affine in $(a,b,z)$ only within a sign branch of $\tau_{13,14}=\delta+T/3-z$ (it changes sign at $z\approx0.0806$) and of $\tau_{5,7}=-a$; the box must stay inside one branch. Square 6 appears in no retained row and needs no domain at all. |
| “Consequently the local theorem needs no second-order analysis” | **Sound** | No second-order effect survives; the checklist is in “Where a Second-Order Effect Could Hide”. |
| The $3\times10^{-4}$ radius estimate | **Holds only at the centroid** | The $-\omega_{11}$ ratio grows with $b$ (square 11’s slide): $0.84\to1.02\to1.32$ at $b=0,\,0.04,\,1/12$ for $r=3\times10^{-4}$. Over the physical domain the uniform radius is about $2\times10^{-4}$. |
| “The stress must be re-verified along the family … a small interval job” | **Not load-bearing** | The fixed-container theorem uses only the 90 coordinate duals; the stress is a consistency witness. The duals, not the stress, are what must hold uniformly in $w$, and that is a parametric LP, not a small interval job. |

No blocking mathematical gap was found.
The one item the route review underestimates is the uniform-in-$w$ dual certification;
the recipe below gives a scheme that exploratory runs show is feasible.

## Setting and Notation

Fix the container $[0,S^\ast]^2$ with $S^\ast$ the H255 root side.
A configuration is $x\in\mathbb R^{51}$: centres and one angle per square, angles
reduced modulo $\pi/2$ to the H254 lift (Lemma 6). Squares 11 and 13 use the $(u,v)$
frame of the exact root for their centre.
The **slider coordinates** are $a=-\xi_5\ge0$, $b=-v\cdot(r_{11}-r_{11}^\ast)\ge0$,
$z=v\cdot(r_{13}-r_{13}^\ast)$, and the three coordinates of square 6. The 45
**non-slider coordinates** $x_N$ are the rest.
The **affine family** is $x^\ast(w)$, $w=(a,b,z)$: the endpoint with 5 moved by $-ae_x$,
11 by $-bv$, 13 by $zv$, and square 6 absent.
Its non-slider coordinates do not depend on $w$.

The **retained system** is the 52 positively weighted H258 rows: 25 wall rows (13 active
walls minus 5-right and 6-bottom; square 9’s left wall smooth), 16 parallel-face rows
(eight faces, $9/11$ dropped) and 11 nonparallel rows.
Each row is a nonnegative combination of **elementary gap functions** $g$: a wall and a
corner, or an owner axis and a corner of the other square, exactly as in n11. Write
$A_N(w)$ for the $52\times45$ matrix of their derivatives in the non-slider coordinates
at $x^\ast(w)$.

Exploratory exact checks at the root midpoint confirm: the kernel of the 52 rows on all
52 columns is spanned exactly by the six slider directions; $A_N(0)$ has rank 45; the
H258 weights are positive and $\lambda^{\mathsf T}A_N(0)=0$ exactly (the two $F_2$
residual columns vanish at the root).

## The Theorem and Its Lemmas

**Theorem (fixed-container local theorem modulo sliders).** Let $B_W$ be a box in
$(a,b,z)$ and $r\in\mathbb Q_{>0}^{45}$ a radius vector.
Suppose certification items C1–C10 below hold.
Then every feasible configuration of the 16 squares other than 6 in $[0,S^\ast]^2$ with
$w(x)\in B_W$ and $\lvert x_N-x_N^\ast\rvert_j\le r_j$ for all $j$ equals
$x^\ast(w(x))$. In particular every feasible 17-square packing in the product
neighbourhood lies on the family, and spans $S^\ast$ in both coordinates (squares 1, 3,
4, 9 touch the left wall, 7, 8, 17 the right, 1, 2 the bottom, 4, 8, 15 the top, at
every family point).

**Corollary (H-261 form).** A packing of side $S<S^\ast$ whose rigid embedding into
$[0,S^\ast]^2$ lands in the product neighbourhood does not exist; so $S\ge S^\ast$
there, with equality only on the family.
The embedding is the capture step’s obligation, as in n11 (PROOF.md, section 8).

*Proof skeleton.* Let $x$ be feasible, $w=w(x)$, $h=x-x^\ast(w)$; then $h$ has zero
slider components. By Lemma 1 every retained row $i$ satisfies $A_i(w)h\ge-K_i\tau^2/2$
with $\tau=\max_j\lvert h_j\rvert/r_j\le1$. Pick the saturating $j$ and the sign
opposite $h_j$; the dual $\lambda^{(j,\pm)}(w)$ of Lemma 4 gives
$\tau r_j\le\varepsilon_j\tau R+\tau^2M_j/2$, and item C9 forces $\tau=0$. $\square$

**Lemma 1 (necessary local system).** If the 125 unavailable owner-axis options of the
19 retained pairs have a corner gap that is negative throughout the neighbourhood (C6),
then nonoverlap of each retained pair implies: for a nonparallel contact, the single
tight elementary gap is $\ge0$; for a parallel face, one of the two owners’ pairs of
tight corner gaps is $\ge0$. Wall rows are elementary gaps.
Dropping square 6, the $2/3$ corner, $9/11$, the right wall of 5, the 115 non-contact
pairs and the 53 inactive walls removes constraints and cannot exclude a feasible
packing.

**Lemma 2 (two-row reduction under Taylor remainders).** At a parallel face $i\to j$
with normal $n$ and base offset $\tau$, $0\le\tau<1$, let $a_\pm$ be the first-order
corner gaps of owner $i$ and $b_\pm$ those of owner $j$. Then exactly

$$
E_-=(1-\tau)\,a_++\tau\,a_-=b_+,\qquad E_+=a_-=\tau\,b_++(1-\tau)\,b_-,
$$

with the symmetric formulas for $\tau<0$. Hence if either owner’s two corner gaps are
nonnegative nonlinearly, $E_\pm(h)\ge-\max(K_{a\pm},K_{b\pm})\tau^2/2$. The curvature
constant of an $E_\pm$ row is the maximum over the four elementary corner gaps of the
pair. (Verified by hand; the coefficients are the base-point $\tau(w)$, so the lemma is
applied at each $w$.)

**Lemma 3 (tightness and affine dependence along the family).** Every retained
elementary gap vanishes identically at $x^\ast(w)$ for all $w$: the rows of 5, 11 and 13
retained are their bottom wall, $5\to7$ along $e_y$, $3\to11$ and $11\to12$ along $u$,
$2\to13$ and $13\to14$ along $u$, none of which is changed by the slides.
Within a sign branch of $\tau_{5,7}=-a$, $\tau_{11,12}=\delta+b$ and
$\tau_{13,14}=\delta+T/3-z$, the matrix is $A_N(w)=A_0+aA_a+bA_b+zA_z$ with $A_a$
supported on rows $(5,7)E_\pm$, columns $\omega_5,\omega_7$; $A_b$ on rows $(3,11)$,
$(11,12)E_\pm$, columns $\omega_{11},\omega_{12}$; $A_z$ on rows $(2,13)$,
$(13,14)E_\pm$, columns $\omega_{13},\omega_{14}$. (Exact check at the midpoint: affine
in $a$ and $b$; affine in $z$ only until $\tau_{13,14}$ changes sign near $z=0.0806$.)

**Lemma 4 (existence of coordinate duals).** If $\lambda>0$ on all 52 rows with
$\lambda^{\mathsf T}A_N(w)=0$ and $A_N(w)$ has rank 45, then
$\operatorname{cone}\{A_i(w)\}=\mathbb R^{45}$, so for every $j$ and sign there is
$\lambda^{(j,\pm)}\ge0$ with $\lambda^{\mathsf T}A_N(w)=\mp e_j^{\mathsf T}$. The side
column and the six slider columns of the H258 matrix play no role: $h$ has zero slider
components and the container is fixed.
(Existence is what the stress buys; the certificate is the duals themselves.)

**Lemma 5 (ratio test with residual).** With $\lambda\ge0$,
$\lVert\lambda^{\mathsf T}A_N(w)\pm e_j^{\mathsf T}\rVert_1\le\varepsilon_j$ on the
cell, $M_j=\sum_i\lambda_iK_i$ and $R=\max_kr_k$: if $M_j<2(r_j-\varepsilon_jR)$ for all
90 signed coordinates, the only feasible $h$ in the closed rectangle is $0$. This is
PROOF.md’s argument verbatim; nothing about sliders enters because $h_W=0$.

**Lemma 6 (angle chart modulo $\pi/2$).** A unit square’s orientation lives in
$\mathbb R/(\pi/2)\mathbb Z$; rotation by $\pi/2$ permutes corners and axis options, so
the set of eight owner-axis features and the set of four corner gaps per feature are
invariant.
The H254 lift ($0$ for axis squares, $\theta$ for 9–14, $-\beta$ for 16) fixes
which corner is “the tight one”.
“Within $r$ of the endpoint” means the lift in $(\phi^\ast-\pi/4,\phi^\ast+\pi/4]$ is
within $r$; capture must deliver angles in that sense.

**On argument (b).** With $h_W=0$ after re-basing, the gap functions are affine in
positions, so the remainder is $\le K\lvert h_{\rm ang}'\rvert\lvert h_N\rvert$ with
$h_{\rm ang}'$ the 16 retained angles ($\omega_6$ absent).
The stress gives $\sum_i\lambda_i\lvert A_ih\rvert\le2\sum_i\lambda_i\lvert R_i\rvert$,
so $\lVert A_Nh\rVert_1\le C_1\lvert h_{\rm ang}'\rvert\lvert h_N\rvert$ with
$C_1=104K\lambda_{\max}/\lambda_{\min}$; injectivity gives
$\lvert h_{\rm ang}'\rvert\le\lVert h_N\rVert\le(C_1/s_{\min})\lvert h_{\rm ang}'\rvert\lvert h_N\rvert$,
hence $h_{\rm ang}'=0$ for $\lvert h_N\rvert<s_{\min}/C_1$, after which the system is
exactly affine and the stress forces $A_Nh=0$, so $h_N=0$. Valid; the constants
($\lambda_{\max}/\lambda_{\min}\approx51$, $K$ of order ten per unit radius squared,
$s_{\min}$ well below one) make the radius orders of magnitude smaller than the ratio
test’s, so it is a proof that some positive radius exists, not the instrument.

## Where a Second-Order Effect Could Hide

- **Finite slider motions coupled with non-slider coordinates.** The coupling is the
  bilinear term angle × slide (for example $-\omega_5\,a$ in the $5\to7$ gap).
  Expanding about $x^\ast(w)$ with $w=w(x)$ moves it into the first-order matrix
  $A_N(w)$, where Lemma 3 makes it affine.
  Expanding about the centroid would leave a remainder of order
  $\lvert h_{\rm ang}\rvert\cdot0.1$, comparable to the first-order terms; that is why
  the base point must move.
- **The zero corner weight.** The $2/3$ pair is dropped altogether (Lemma 1). Squares 2
  and 3 are pinned by the $1$–$2$–$3$ block and the walls; the duals never need the
  corner rows.
- **The six zero-weight rows.** Dropped.
  Consequently the relaxed system treats $a$, $b$ and $z$ as two-sided and concludes
  equality with the *affine* family; physical feasibility then restricts $a,b\ge0$ and
  the rest. Nothing is lost because the conclusion is exact equality of the 45
  coordinates.
- **Rows whose coefficients depend on slider positions.** Only moment arms and offsets
  move (Lemma 3); normals depend on angles, none of which is a slider once 6 is gone.
  A row that is *not* tight along the family (for example $9/11$ at $b>0$) cannot be
  used in a dual: its slack enters the saturation inequality as a constant and the
  contradiction fails.
  Only tight rows are retained, so this cannot happen.
- **The sign branches of $\lvert\tau\rvert$.** The two-row reduction uses
  $k=(1-\lvert\tau\rvert)/2$. $\tau_{5,7}=-a\le0$, $\tau_{11,12}=\delta+b>0$,
  $\tau_{13,14}=\delta+T/3-z>0$ for $z<0.08$. The instrument proves each sign over the
  box; the H258 code’s $k=1/2$ for $(5,7)$ is correct only at $a=0$.
- **Non-tight corners of an available feature and the other three corners of a tight
  nonparallel contact.** Dropped; a feature’s other corners are strict and need no
  check.
- **The root box.** All inequalities are over the H255 box; the identities hold by
  construction or symbolically (C2).

## Frozen Instrument Recipe

Every item is a certification the checker must perform; “exact” means standard-library
`Fraction` identities, “outward” means outward interval arithmetic over the stated
region. The region $\Omega$ is (H255 root box) × $B_W$ with the declared box
$B_W=[0,\tfrac14]\times[0,\tfrac1{12}]\times[-\tfrac18,\tfrac1{16}]$ in $(a,b,z)$, and
the declared radius vector $r$ (uniform $1/5000$ recommended).

1. **C1 — Row roster and elementary decomposition.** Build the 52 retained rows from the
   frozen H258 roster minus the six zero-weight rows, and for each row record its
   elementary gap functions: wall rows one (wall, corner); nonparallel rows one (owner,
   axis, corner); $E_\pm$ rows the four (owner, corner) gaps of the face with the Lemma
   2 coefficients. Bind the roster to the accepted H257 inventory.
   *Exact; at the frozen inventory.*
2. **C2 — Tightness along the affine family.** For every elementary gap of C1, prove
   $g(x^\ast(w))\equiv0$ as a rational-function identity in $(t,b_{\rm ang},a,b,z)$ (the
   closing gaps reduce to $F_1\equiv0$, $F_2$, $F_3$, which vanish on the root by H255).
   *Symbolic, or exact evaluation on a grid beyond the degree bound; whole family.*
3. **C3 — Sign branches and overlap.** Prove $-1<\tau_{5,7}\le0$, $0<\tau_{11,12}<1$,
   $0<\tau_{13,14}<1$ and $0<\tau<1$ for the other faces, and all H258 denominator
   guards. *Outward over $\Omega$.*
4. **C4 — Affine structure.** Prove $A_N(w)=A_0+aA_a+bA_b+zA_z$ with $A_a,A_b,A_z$
   supported as in Lemma 3 (exact identity of the row formulas within the C3 branches).
   *Exact identity in $(a,b,z)$ at symbolic root parameters, or exact at the midpoint
   plus outward over the root box.*
5. **C5 — Rank.** $A_N(w)$ has rank 45 on $\Omega$: exhibit a $45\times45$ minor and
   prove its determinant is nonzero.
   *Outward over $\Omega$ (subdivide if needed); the duals of C8 imply this and may
   replace it.*
6. **C6 — Unavailability of the 125 options.** For each unavailable owner-axis option of
   the 19 retained pairs choose one corner $c$ and prove
   $g_{f,c}(x^\ast(w))+\sum_j\lvert\partial_jg_{f,c}(x^\ast(w))\rvert r_j+K_{f,c}/2<0$.
   *Outward over $\Omega$; $g(x^\ast(w))$ is affine in $w$.* Exploratory: the least
   negative base margin over $B_W$ is $-0.0558$ ($14/17$ and $7/14$), then $-0.0707$
   ($12/16$) and $-0.094$ ($3/11$ at $b=1/12$); the 27 retained options stay tight.
7. **C7 — Curvature constants.** For each elementary gap, $K=w_i^2/\sqrt2$ (wall) or
   $K=D_{op}w_o^2+2\rho_{op}w_o+(w_o+w_p)^2/\sqrt2$ (pair), with $D_{op}$ a rational
   upper bound on the centre separation over $\Omega$ (convex in $w$, so vertices
   suffice), $\rho_{op}$ the Euclidean bound of the two position-radius vectors (for 11
   and 13 only the $u$ component), $w$ the angle radii, square roots replaced by
   rational upper bounds.
   Row constants by Lemma 2. *Exact rationals.*
8. **C8 — Duals on cells.** Partition $B_W$ into cells.
   On each cell and for each of the 90 signed non-slider coordinates, a rational
   **affine dual** $\lambda(w)=\lambda_0+a\mu_a+b\mu_b+z\mu_z$ with: (i)
   $\lambda_0^{\mathsf T}A_0=\mp e_j^{\mathsf T}$ and
   $\mu_k^{\mathsf T}A_0+\lambda_0^{\mathsf T}A_k=0$ at the midpoint root parameters,
   their outward residual over the root box folded into $\varepsilon_j$; (ii)
   $\lambda(w)\ge0$ at the cell’s eight vertices (affine, so everywhere); (iii)
   $\varepsilon_j\ge\sum_{k,l}W_kW_l\lVert\mu_k^{\mathsf T}A_l\rVert_1$ plus the
   root-box and rounding residuals, with $W_k$ the cell half-widths about its centre;
   (iv) $M_j=\max_{\rm vertices}\sum_i\lambda_i(w)K_i$. *Exact.* A constant dual
   ($\mu=0$) with first-order residual is the degenerate case and suffices for most
   coordinates.
9. **C9 — Ratio test.** For every cell and signed coordinate,
   $M_j<2(r_j-\varepsilon_jR)$ with $R=\max_kr_k$, strict, exact rational comparison.
   Report the worst ratio $M_j/(2(r_j-\varepsilon_jR))$ and where it occurs.
10. **C10 — Spanning.** Prove the family touches both walls in each coordinate (the
    anchor identities of H256 for squares 1, 2, 3, 4, 7, 8, 9, 15, 17 are unchanged by
    the slides). *Exact.*
11. **C11 — Consistency witnesses, not load-bearing.** The H258 stress recomputed along
    the family (with $k_{5,7}=(1-a)/2$) nonnegative on $\Omega$; the kernel of the 52
    rows on 52 columns equal to the six slider directions at the midpoint.
    These are sanity checks against the frozen roster.
12. **C12 — Controls.** A synthetic family with a known non-tight row must fail C2; a
    flipped $\tau$ sign must fail C3; a perturbed $A_k$ must fail C4; a corner choice
    with positive gap must fail C6; a dual with a negative vertex value must fail C8; a
    radius vector above the ratio limit must fail C9; the n11 focused receipt replayed
    through the same ratio routine must reproduce $0.6765$.

The checker’s output is the declared $B_W$, $r$, the cell partition, the 90 worst
ratios, and the least negative C6 margin.
A failed C9 is inconclusive and selects a smaller radius or a smaller $B_W$; it refutes
nothing.

## Radius Recommendation

- **Uniform $r=1/5000$ over the declared $B_W$.** Exploratory ratios (float LP duals, my
  own curvature constants, which give $0.844$ where the receipts give $0.859$ at
  $3\times10^{-4}$): the binding coordinate is $-\omega_{11}$ everywhere; its ratio does
  not depend on $a$ or $z$ and grows with $b$, reaching $0.88$ at $b=1/12$ for
  $r=2\times10^{-4}$. The next coordinates are $-u_{11}$ ($0.47$ at $b=1/12$),
  $-\omega_{16}$, $-\omega_8$, $-\xi_8$ ($0.36$, $0.33$, $0.33$, independent of $w$).
- **The duals are essentially unique.** Minimising $\sum\lambda_i$ and minimising $M_j$
  give the same $-\omega_{11}$ dual (sum $921$ at $b=0$, $1407$ at $b=0.08$); its
  support is 44 of the 52 rows.
  There is no cheaper dual to find; the softness is physical: with $9/11$ open, square
  11 is held only by $3/11$ and $11/12$, whose face carries the smallest load.
- **Per-coordinate radius vectors** rebalance position against angle radii (the
  $-\omega_{11}$ ratio scales like $\sum\lambda_i(5.7r_{\rm pos}+3.9r_{\rm ang})$); the
  gain is well under $2\times$ and the volume of the rectangle favours the uniform
  choice. The instrument should accept a vector but the declared radius should be
  uniform.
- **Cell count.** With constant duals and first-order residual, 77 of 90 coordinates
  need one cell for all of $B_W$, 12 need 3–10, and $-\omega_{11}$ needs thousands (its
  chain passes through the $a$- and $z$-dependent rows).
  With affine duals and quadratic residual, $-\omega_{11}$ has ratio $0.84+0.92$ on the
  whole box and the residual falls fourfold per trisection, so roughly 64–100 cells;
  total well under $10^3$ cells and minutes of exact arithmetic.
- **If capture can bound $b\le1/40$**, $r=1/4000$ passes with ratio about $0.95$. The
  route review’s stop condition ($10^{-4}$) is not triggered.

## Open Questions

1. **Radius enlargement.** The ratio test is first-order with a worst-case remainder;
   its radius scales like $1/\sum\lambda_i$ and cannot exceed about $2.4\times10^{-4}$
   over the physical domain.
   A second stage that proves every feasible configuration in a larger box lies in the
   certified rectangle (interval branch-and-bound on the retained system along
   $\omega_{11}-\omega_{12}$ and $\omega_{16}$) is a separate instrument.
2. **The slider box in $b$.** $b$ is the only parameter that costs radius.
   Its physical range is $[0,T]\approx[0,0.071]$ with square 6 present; the capture step
   must deliver the bound, since the 16-square system alone does not limit $b$ (13 can
   retreat along $-v$ into 6’s place).
3. **Exact affine duals.** Requiring $\mu_k^{\mathsf T}A_l=0$ for all $k,l$ (identity
   exact in $w$, no cells) was infeasible in the float LP for every coordinate tried; I
   did not determine whether this is structural or a solver artefact.
   The quadratic-residual version is feasible for all 90.
4. **Frame constants.** $u,v$ at the exact root are algebraic; the capture step works
   with rational enclosures of them, and the $10^{-12}$ discrepancy must be charged to
   its radius, not to $r$.
5. **Reuse.** The same recipe (translation sliders, moving base point, affine $A_N(w)$)
   applies to any reported endpoint with sliders (n18, n19, n26, n29); the only
   endpoint-specific inputs are the roster, the slider parametrisation and the $\tau$
   branches.

## Evidence Status

| Kind | Items |
| --- | --- |
| Verified by exact computation (scratch scripts, root midpoint) | Kernel equals the six slider directions; $A_N$ rank 45; stress vanishes on the non-slider columns; row builder agrees with `check_n17_core_stress.common_rows`; affine dependence on $a$, $b$; the $\tau_{13,14}$ sign change; Lemma 2 coefficients |
| Double precision only | All ratios, dual sums, cell counts, unavailability margins over $B_W$, slider-domain gaps |
| Derived by hand | Theorem, Lemmas 1–6, the second-order checklist, the constants in argument (b) |
| Taken on trust | H255–H257 certificates; the n11 curvature formula and saturation argument |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
