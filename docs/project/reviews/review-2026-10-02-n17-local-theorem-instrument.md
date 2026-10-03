---
title: n17 Local Theorem Modulo Sliders — Independent Review of the H-261 Instrument
date: 2026-10-02
status: planning-review
---
# n17 Local Theorem Modulo Sliders — Independent Review of the H-261 Instrument

**Session:** 167 (BC-406), lane A2-review (second pass).
**Reviewed:**
[H-261](../../../packing/campaign/hypotheses/H-261-n17-local-minimum-modulo-sliders.md)
(frozen criterion), the [recipe review](review-2026-10-02-n17-local-theorem-recipe.md)
(theorem, Lemmas 1–6, items C1–C12), `packing/devtools/check_n17_local_minimum.py` at
`af930710` and the builder’s follow-up `e91bd859` (C1 binding, C11 stress along the
family, the restored 9/11 control), its tests, and the lane A2b2 receipt
`local-minimum-ratio-target.json` with `local-minimum-ratio-certificates.json` (uniform
$r=1/5000$ over $B_W=[0,\tfrac14]\times[0,\tfrac1{12}]\times[-\tfrac18,\tfrac1{16}]$ in
$(a,b,z)$, 90 directions on 93 cells, worst ratio $0.925818$ at $-\omega_{11}$).
**Recomputation:**
[`recompute.py.txt`](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-244-n17-local-minimum/audit/recompute.py.txt),
output `recompute-output.json` and log `recompute.log`, retained under exp-244’s
`audit/` with a `.txt` suffix as earlier independent reviews were; it imports nothing
from the instrument.

## Verdict

**No blocking defect in the mathematics, the instrument or the certificates.** Every
check I could make independently reproduces the receipt.
Two record-level items must be settled before H-261 is accepted, and both are about
scope rather than correctness: the claim says “slider coordinates anywhere in the
physical slider domain”, but what is certified is the declared box $B_W$, which does not
cover the physical domain in $a$ and $z$ when square 6 is free; and the frozen criterion
names 135 unavailable alternatives where the instrument legitimately checks 125. The
receipt itself is planning evidence from a scratch lane; acceptance needs the same run
recorded as an experiment at the committed engine.

## The Theorem and Its Lemmas

The composition is sound.
It runs: rows as nonnegative combinations of elementary gaps (Lemma 1, 2), tightness
along the family (Lemma 3), the affine $A_N(w)$ (Lemma 3, C4), per-cell nonnegative
affine duals with a residual (Lemma 4, C8), curvature constants (C7), the ratio test
(Lemma 5, C9), and the conclusion $h=0$ on each cell, hence $x=x^\ast(w(x))$ on the
product neighbourhood, hence by spanning (C10) no side below $S^\ast$ lands there.

- **Lemma 2.** I re-derived the four elementary corner gaps of a parallel face with
  owner $i$ and owner $j$ from
  $g=\sigma\,n(\omega_o)\cdot(c_p+R(\omega_p)q-c_o)-\tfrac12$: with $\tau\ge0$,
  $E_+=a_-$ is an elementary gap of owner $i$ and equals $(1-\tau)b_++\tau b_-$;
  $E_-=b_-$ is an elementary gap of owner $j$ and equals $(1-\tau)a_++\tau a_-$. With
  $\tau<0$ the roles swap ($E_-=a_+$, $E_+=b_+$) and the convex weights are
  $(1-|\tau|,|\tau|)$. The lemma’s displayed formula labels $b_\pm$ oppositely to
  $a_\pm$; that is a naming convention, the content is right.
  Since nonoverlap forces one owner’s *two* tight gaps to be nonnegative nonlinearly and
  each $E$ row is either that owner’s elementary gap or a convex combination of them,
  $E_\pm(h)\ge-\max K\,\theta^2/2$ with $\theta$ the saturation parameter.
  The constructive check in `recompute.py` finds, at the box centre where
  $\tau_{5,7}=-1/8$, exactly two rows per face admitting a convex representation, and
  they are the instrument’s rows.
  The sign branch is essential: with the wrong $k$ the weight $1-\tau$ exceeds one and
  the lower bound fails; C3 proves each branch over $B_W$ and the control refuses a
  flipped one.
- **Lemma 1 and the dropped items.** Dropping square 6, the $2/3$ corner, $9/11$, the
  $5$-right and $6$-bottom walls, the non-contact pairs and inactive walls removes
  constraints from a necessary system and cannot exclude a feasible packing; the
  theorem’s conclusion is exact equality of the 45 coordinates, so nothing is lost.
  The zero-weight rows *must* be dropped: at $a>0$ or $b>0$ they carry slack ($a$, $b$)
  at the base point, and a dual using them would turn the saturation inequality into one
  with a constant and no contradiction.
  The retained corner of a nonparallel contact stays the minimiser along the family
  because every slide is tangent to the owning face, so all four corner gaps of that
  feature are unchanged (C2’s margin invariance covers this).
- **Side and slider columns.** The container is fixed at $S^\ast$, so $\sigma\equiv0$ in
  every gap function and the side column is simply absent; $h_W=0$ by the choice of base
  point $w=w(x)$, so the slider columns multiply nothing.
  The point-mode LP with $\sigma$ free is a different object and is not used by the
  ratio test.
- **Lemma 6.** Orientation lives in $\mathbb R/(\pi/2)\mathbb Z$; with
  $r=1/5000\ll\pi/4$ the H254 lift within $r$ is unique and the eight owner-axis options
  and four corners per option are permuted, not changed, by a quarter turn.
  The chart is correct.
  Its consequence for capture is stated correctly in the recipe: a square geometrically
  within $r$ but labelled a quarter turn off is *not* in the neighbourhood until
  relabelled.
- **Equality only on the family.** The theorem gives $x_N=x_N^\ast$ and $w(x)\in B_W$,
  i.e. $x=x^\ast(w(x))$ with square 6 unconstrained.
  For $w$ where $x^\ast(w)$ is itself infeasible (my scan finds $z>0.0235$ overlaps
  $11/13$) the statement is vacuous there, which is harmless.
- **Assumed, not certified here:** tightness of the 27 identity options and 13 anchors
  at $x^\ast(0)$ at the exact root (H-257, accepted); the two closing contacts’
  residuals at the midpoint ($10^{-60}$) vanish at the root by H255; the frame $u$ of
  the 45 coordinates is the exact root’s, so capture must charge the rational-enclosure
  discrepancy to its own radius (recipe open question 4); the kernel claim at the exact
  root is argued (C8 residual below one plus H-258’s exact stress gives rank 46) rather
  than checked there; C11’s numerator affinity rests on eleven exact points and a
  structural argument, not a symbolic proof.

## The Ratio Test

The checked inequality $M_j<2(r_j-\varepsilon_jR)$ is Lemma 5 and n11’s argument
verbatim. With $\lambda\ge0$, $\lambda^{\mathsf T}A_N(w)=-se_j^{\mathsf T}+\rho$,
$\lVert\rho\rVert_1\le\varepsilon_j$, and $A_ih\ge-K_i\theta^2/2$:
$s\,h_j\le\theta^2M_j/2+\varepsilon_j\theta R$; at the saturating coordinate with
$s=\operatorname{sign}h_j$ this reads
$r_j\le\theta M_j/2+\varepsilon_jR\le M_j/2+\varepsilon_jR$, the contradiction.
The factor 2 is right; $R=\max_kr_k$ bounds $\lVert h\rVert_\infty/\theta$; $M_j$ and
the vertex minimum of $\lambda(w)$ are exact at the eight vertices, which suffices
because $\lambda(w)$ is affine.
The residual expansion in `evaluate_dual` ($r_0$, the three $r_k$, the nine $q_{kl}$
with the cell half-widths) is the exact expansion of $\lambda(w)^{\mathsf T}A(w)+se_j$
about the cell centre.

**Curvature.** I re-derived n11’s bound: for
$g=n(\omega_o)\cdot(c_p-c_o)+n(\omega_o)\cdot R(\omega_p)q-\tfrac12$ the Hessian
quadratic form is bounded by
$|c_p-c_o|\,w_o^2+2|\delta c_p-\delta c_o|\,w_o+|q|(w_o+w_p)^2$ with $|q|=1/\sqrt2$, and
$|c_p-c_o|$ must be taken along the Taylor segment, which is
$D_{op}=\max_{\rm vertices}|\Delta(w)|+\rho$ since $|\Delta|^2$ is convex in $w$. The
instrument does exactly this (`curvature_audit`:
`separation = sqrt_upper(squared) + rho`), takes the root-box upper end of $|\Delta|^2$,
and gives face rows the larger owner’s bound as Lemma 2 requires.
`sqrt_upper` is sound (checked $u^2\ge v$) and $0.7071068>1/\sqrt2$. My own constants,
computed from my own rows and position boxes, reproduce all 27 pair constants and the
wall constant to every printed digit; for example $K_{14\to7}=3.9145801\times10^{-7}$,
$K_{5/7}=3.3327147\times10^{-7}$, $K_{11/12}=3.4649192\times10^{-7}$.

## Exactness

- The certificates are dyadic rationals ($2^{-44}$ grid) proposed by HiGHS and verified
  only by exact `Fraction` arithmetic in `evaluate_dual`; `replay_certificates` re-reads
  them from JSON with no LP and must reproduce the worst ratio (check
  `c8_c9_replayed_from_certificates`). Tampered certificates are refused (tests).
- The cell partition is an exact tiling: containment, pairwise disjoint interiors and
  volume sum equal to the box volume, all rational; closed cells with full measure cover
  the closed box.
- Vertex nonnegativity of an affine $\lambda(w)$ on a box is sufficient.
- The root-box residual is folded in correctly: by the symbolic C4 the slopes $A_k$ are
  free of $(t,\beta)$, so $A^\ast(w)-A_{\rm mid}(w)$ is constant in $w$ and bounded
  entrywise at $w=0$; $\lVert\lambda^{\mathsf T}D\rVert_1\le\sum_i\lambda_id_i$ with
  $d_i$ the row sums, maximised at a vertex.
  The lifts use the interval frame $u^\ast$, as the theorem at the root requires.
- **Independent replay of $-\omega_{11}$.** From my own row construction (elementary
  gaps built from the H-254 chart and the accepted H-256 layout, corners chosen by exact
  minimisation, $E_\pm$ by Lemma 2) I verified all four serialised cells exactly: vertex
  minimum $10^{-6}$ on each; $\varepsilon=0.05270,\,0.05565,\,0.05909,\,0.06315$;
  $M=3.46943\times10^{-4}$; ratios $0.91561,\,0.91847,\,0.92183,\,0.92582$, all below
  one. With the root-box term at zero my worst ratio equals the receipt’s exact fraction
  to $1.06\times10^{-18}$; the difference is the root-box term.
  My own enclosure of the rows over the H255 box, in `mpmath` interval arithmetic at 320
  bits (independent of `Dyadic`), gives a largest row deviation of $3.59\times10^{-21}$
  against the instrument’s $3.80\times10^{-21}$ and a root-box residual of
  $9.3\times10^{-19}$ per cell.
  My rows at $w=0$ equal the H-258 producer’s 52 rows exactly (the roster cross-check:
  25 wall, 16 face, 11 nonparallel, in the derivation’s order), and my $A_N(w)$ is
  affine with the stated support on six random rational points of $B_W$.
- **C6 independently.** My own enumeration gives 168 options, 33 identities, 125
  unavailable on the 19 retained pairs, all 125 Taylor margins negative at every vertex,
  least negative $-0.055273$ ($14/17$, owner 17), $-0.055278$ ($7/14$), $-0.069917$
  ($12/16$), $-0.093628$ ($3/11$ at $b=1/12$): the receipt’s values.

## The Criterion Versus the Recipe

| Criterion item | Status | Note |
| --- | --- | --- |
| Kernel of the 52 positive rows exactly the slider span, dimension 6 | **Met** | Exact at the midpoint (point mode); at the eight vertices of $B_W$ by annihilation plus rank 46 mod $p$ (C11) |
| Exact nonnegative duals for all 90 signed directions | **Met** on $B_W$ | Affine per cell, vertex-nonnegative, residual exact, root box folded in |
| Curvature bounds by the n11 recipe | **Met** | Reproduced independently |
| Taylor checks that the 135 unavailable alternatives stay negative | **Met as 125; deviation to record** | The ten others belong to $2/3$ and $9/11$, dropped by Lemma 1; no constraint on those pairs is used, so no check is owed. The point receipt still shows all 135 negative at $x^\ast(0)$ |
| Stress and duals nonnegative uniformly over the slider domain | **Met on $B_W$; not on the physical domain** | C11 (e91bd859): the H-258 stress rebalanced through the $5$-bottom and $7$-right wall moments, least weight $0.0042558$, zeros exact; the duals by C8. See scope below |
| Ratio test at one declared rational radius | **Met** | $r=1/5000$ uniform, worst $0.925818<1$; the stronger form with residual |
| Synthetic controls | **Met** | C12: flipped branch, perturbed slope, negative vertex, radius $3/5000$ (ratio $2.78$), largest corner, restored $9/11$ not slide-invariant, and n11’s focused receipt reproducing $0.676505208203$ at branch 12, coordinate 6, sign $-1$ exactly |
| Independent review of the composition | **This document** | Angle chart and product form found sound |
| H-258 accepted | Met | exp-242 |
| Every item exact or outward | **Met** with the stated trusts | H-257 tightness at $x^\ast(0)$; Lemmas 1–6 as hand proofs, now read |

On C11’s rebalancing: moving weight between $W_-$ and $W_+$ of one wall changes only
that square’s angle column (the two rows share translational and side entries), so
absorbing the $-f a/2$ shift of the $5/7$ torque there is a legitimate stress as long as
both wall weights stay nonnegative, which the vertex check shows.
The identity is exact at eleven points and the numerators are affine on structural
grounds; for a consistency witness that is adequate.
It is not load-bearing: the theorem uses the 90 duals only.

## Scope of a Pass

A pass proves: every feasible configuration of the 16 squares other than 6 in the fixed
container $[0,S^\ast]^2$, at the exact H255 root, whose 45 non-slider coordinates (the
H254 lift of each angle in radians; $\eta_5,\omega_5$ for square 5;
$u^\ast\!\cdot\delta r,\ \omega$ for squares 11 and 13; $\xi,\eta,\omega$ for the other
thirteen) are each within $1/5000$ of the endpoint’s, and whose slider parameters
satisfy $a=-\delta\xi_5\in[0,\tfrac14]$,
$b=-v^\ast\!\cdot\delta r_{11}\in[0,\tfrac1{12}]$,
$z=v^\ast\!\cdot\delta r_{13}\in[-\tfrac18,\tfrac1{16}]$, equals $x^\ast(w)$; the family
touches all four walls, so no packing of side below $S^\ast$ embeds there, and a packing
of side $S^\ast$ there lies on the family.
Square 6 is unconstrained.

**Does $B_W$ cover the physical slider domain?** Not in $a$ and $z$. A float
separating-axis scan of $x^\ast(w)$ along one axis at a time (`recompute.py`, step
$1/2000$): $b$ reaches $0.0235$ before $11/13$ overlaps, with or without square 6, so
$b\le1/12$ covers it.
$z$ reaches $+0.0235$ ($11/13$) and, with 6 at its centroid, $-0.0235$ ($6/13$); with 6
absent, $-0.9165$ (13 reaches the bottom wall), far beyond $-1/8$. $a$ reaches $0.037$
against 6 at its centroid but $1.074$ with 6 absent ($5/13$), beyond $1/4$. Since 6 is
free in the theorem, the physical domain of the family includes $a>1/4$ and $z<-1/8$.
For capture this means: the product neighbourhood is a *premise*, and capture must
deliver $a\le1/4$ and $z\ge-1/8$ (the $b$ bound is free), or $B_W$ must be widened
before the capture step is designed.
Widening in $a$ is cheap ($a$ enters only the $5/7$ rows, $\tau_{5,7}=-a$ stays in the
branch for $a<1$); widening in $z$ costs radius as $\tau_{13,14}$ grows and ends at
$z\approx-0.79$ where the $13/14$ face degenerates.
The H-261 claim as registered (“anywhere in the physical slider domain”) is therefore
wider than what is certified and must be re-scoped to the declared box at acceptance.

## Blocking Defects

None in the instrument, its certificates or the lemmas.

Blocking for acceptance of the claim *as worded*: the slider-domain scope above.
The record must either narrow H-261 to $B_W$ with the capture obligation stated, or the
box must be widened and re-run.

## Notes

1. Record the $135\to125$ deviation from the frozen criterion with its reason.
2. Lemma 2’s $b_\pm$ labels are swapped relative to $a_\pm$ in the displayed formula.
3. The receipt is planning evidence (its own scope string says so) from an uncommitted
   lane run; acceptance needs an experiment record at `e91bd859` with the fresh
   receipt’s 14 checks and both certificate files bound by digest.
4. `H-261.instrument_ready` is still `false`; it should flip with that record.
5. The kernel statement in the claim is certified at the midpoint and the vertices mod
   $p$, and argued at the exact root; say so in the acceptance text.
6. The $+z$ half of $B_W$ above $0.0235$ and most of $a\in(0.037,\tfrac14]$ with 6
   present are physically empty; harmless, but the box is not tight.
7. The exploratory “$-\omega_{11}$ needs thousands of cells” estimate in the recipe
   turned out to be 4 cells with affine duals; 77 directions needed none of the
   quadratic residual (constant duals), matching the recipe’s expectation.
8. My recomputation needed three of its own fixes (the Lemma 2 pattern must be fixed
   away from $\tau_{5,7}=0$; wall rows must keep the $W_-,W_+$ order; the interval
   context precision), none of which touched the instrument; the log shows them.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
