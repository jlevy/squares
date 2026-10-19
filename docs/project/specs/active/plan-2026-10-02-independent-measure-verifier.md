# Plan: An Independent, Fast Verifier for Measure-Capture Certificates

**Date:** 2026-10-02

**Author:** Claude (agent), lane W1 of `think-gpe0`, for the repository owner

**Status:** Active.
The clean-room verifier and its complete census are on main (PR #332,
fa5133b49: 149 of 149 verified); slice 4, the independence-record audit and confirming
evidence entries, remains open under think-3ok2.

**Workflow:** W7 `pipeline-improvement`: a new verifier capability with controls, an
evidence limit and a cost receipt, and no scientific verdict of its own

**Beads:** epic `think-gpe0`, under the effort `think-20pp`; the slice beads are listed
in [Slices, Lanes and Beads](#5-slices-lanes-and-beads).
The work ships as a pull request stacked on #298, tracked as `think-tatg`.

**This document is an implementer input.** It states the mathematics, the certificate
formats and the soundness obligations, and it quotes and paraphrases no author’s
checker. Two companion artifacts carry what was learned by building and profiling the
authors’ checkers, and the implementer lanes do not read them: the
[profile research note](../../research/research-2026-10-02-author-checker-profile.md)
and the
[profiling tool](../../../../packing/benchmarks/profile_author_measure_checkers.py) with
its `attribution/` outputs.
The timings that implementers may read are in
[`timings.json`](../../../../packing/benchmarks/results/author-checker-profile-2026-10-02/timings.json).

## Summary

Every external lower-bound certificate of the measure-capture kind that this repository
has replayed was replayed with its author’s own checker, pinned by digest and run byte
for byte: Tokoharu’s rectangle-density checker, wand125’s mixed and linear checkers, and
Evan Daniel’s continuous-angle checker.
That establishes reproducibility with one implementation each.
This plan specifies a second implementation, written in a clean room from the
mathematics alone, and asks that it be much faster than the first.

Under [`epistemics.md`](../../../../epistemics.md#confirmation), a second implementation
does not change a result’s confirmation rung.
`C4` is `C3` plus two retained adversarial AI reviews and a human oversight record, and
“two independently written implementations using the same method, or two different
methods, do not change the rung”.
What this work adds is an attribute the register shows beside the rung: a confirming
evidence entry with `relationship_to_generator: independent-implementation`, naming the
new verifier in the `verifiers` registry field, with an independence record that lets
anyone audit the claim of independence.

The baseline profile measured the authors’ checkers on this host at 0.2 to 0.5 ms of CPU
per centre box, while on the same certificates a box at the scale of the leaves has only
20 to 52 pieces that are neither certainly inside nor certainly outside every core, out
of 1,832 to 9,872. A box whose work is proportional to that count, at on the order of
100 ns per piece in binary64 enclosures, costs a few microseconds.
That gap, and nothing cleverer, is why a speedup of one to two orders of magnitude per
core is plausible.

## Goals

- A verifier, written without reading any author’s checker, that decides every
  certificate family below: rectangle densities on the 201-direction net (Tokoharu’s and
  wand125’s rectangle certificates), wand125’s mixed rectangle-and-point measures and
  linear point-segment-rectangle measures on the same net, and Daniel’s format of points
  and axis-parallel segments at every angle (the certificates `zmx2` decides).
- Exact admission of every certificate from its files, and outward-rounded or exact
  arithmetic on every inequality it certifies.
- Per-core speed at least thirty times the authors’ checkers on every family, measured
  on one host by the same timing method as the baseline.
- An independence record, produced by a tool, that names every input each implementer
  lane read, so that the claim `independent-implementation` can be audited.
- Confirming evidence entries for every certificate already replayed here, after two
  adversarial reviews.

## Non-Goals

- No new bound, and no certificate that has not already been replayed here, is in scope
  for acceptance. Reported-but-unreplayed certificates are stretch targets.
- No change to any rung by this work alone, and no human oversight record: that is the
  owner’s.
- No formal proof. The verifier’s lemmas are proved on paper here and reviewed; a Lean
  formalization is a later, separate question.
- Polygons of uniform density (allowed by Daniel’s format, used by no certificate here)
  and non-axis-parallel segments in the continuous-angle family are refused, not
  supported.

## Background

| Family | Author’s checker | Statement checked | Atoms | Replayed here |
| --- | --- | --- | --- | --- |
| T: rectangle density | Tokoharu | Every core of side $B$ at each of 201 net directions captures $\ge \Gamma$ | Uniform rectangles | 3 Tokoharu and 24 wand125 certificates |
| M: mixed | wand125 | The same, at $\Gamma = 1$, on per-bin centre domains | Uniform rectangles (points allowed, none present) | $n = 76$ |
| L: linear | wand125 | The same, at $\Gamma = 1$ | Points, segments of any direction, uniform rectangles | $n = 101$ |
| D: continuous angle | Daniel | Every closed unit square at every angle captures $\ge 1$ | Points, axis-parallel segments | $n = 13, 21, 32, 45, 59, 60, 77$ |

The repository already has an exact, source-independent verifier for family T,
[`sqpack.rectangle_density`](../../../../packing/src/sqpack/rectangle_density.py), with
a Rust exact-area kernel in [`sqverify_exact`](../../../../packing/sqverify_exact/). It
is exact-rational everywhere, has never completed an external certificate, and
[the performance research of 30 September](../../research/research-2026-09-30-exact-arithmetic-verifier-performance.md)
measured it slow: 1,000 nodes of one direction in 13 seconds.
The baseline below puts its cost per box at about two orders of magnitude above the
authors’ outward-rounded checker’s. This plan keeps that exact path as the reference
oracle and the fallback, and puts the fast path in binary64 enclosures.

## 1. Mathematical Specification

Everything in this section is stated so that an implementer can work from it alone.
Each lemma ends with its **soundness obligation**: the property the implementation must
establish, by exact arithmetic or by a certified enclosure, for its use of the lemma to
be sound. A failed obligation may cost completeness (a box that does not close); it must
never produce a certificate.

### 1.1 The Statement and Its Conventions

$s(n)$ is the least side of a closed square container holding $n$ closed unit squares
with pairwise disjoint interiors, each freely translated and rotated; contact is
allowed. A **pose** is a centre $c \in \mathbb R^2$ and an angle $\theta$, and
$Q(c, \theta) = c + R_\theta [-\tfrac12, \tfrac12]^2$ is the closed unit square at that
pose, with $R_\theta$ the rotation by $\theta$. Since
$Q(c, \theta + \pi/2) = Q(c, \theta)$, $\theta \in [0, \pi/2)$ is every pose.
The container is $K = [0, L]^2$.

For a side $b \in (0, 1)$, the **core** $C_b(c, \theta) = c + R_\theta [-b/2, b/2]^2$ is
the closed square of side $b$ concentric with $Q(c, \theta)$.

A certificate is a finite nonnegative Borel measure $\mu$ on $K$, built from atoms
(§1.2), a threshold $\Gamma \ge 1$, a count $n$ and a side $L$, with total mass
$M = \mu(K) < n$. It claims that every core of a stated kind captures at least $\Gamma$.
The conclusion it supports is $s(n) \ge L$. For the net families, whose cores lie
strictly inside the squares, it excludes side $L$ itself, and compactness gives
$s(n) > L$; for family D it does not, and $s(59) = 8$ is attained.

### 1.2 Measures and Atoms

All coordinates and masses are exact rationals.

- **Point** $p$ with mass $w$: $w\,\delta_p$. A point on the boundary of a closed set
  belongs to it.
- **Segment** $\sigma = \lbrace P_0 + \lambda (P_1 - P_0) : \lambda \in [0, 1]\rbrace$,
  $P_0 \ne P_1$, with mass $w$ spread uniformly by length.
  For a convex closed set $C$, its contribution is
  $w \cdot |\lbrace \lambda \in [0,1] : P(\lambda) \in C\rbrace|$, the parametric
  fraction of the closed intersection.
  A segment lying along an edge of $C$ counts in full; a segment meeting $C$ in one
  point counts nothing.
- **Uniform rectangle** $R = [a, d] \times [b, e]$, $a < d$, $b < e$, with density
  $\rho \ge 0$: its contribution to a measurable set $C$ is $\rho\,|R \cap C|$ (area).
  Boundaries have area zero.

**$D_4$ expansion.** The symmetry group $D_4$ of $K$ is generated by
$\sigma_x : (x, y) \mapsto (L - x, y)$ and $\tau : (x, y) \mapsto (y, x)$. Where a
format lists an orbit representative with mass $m$, the measure holds all eight images
$g(\text{representative})$, $g \in D_4$, each with mass $m/8$, coincident images
included (a rectangle image of mass $m/8$ has density $m / (8 |R|)$). The expanded
measure is $D_4$-invariant whatever the representatives are, and its total is $\sum m$.

### 1.3 The Counting Lemma

**Lemma K.** Let $\mu$ be a finite nonnegative Borel measure with $\mu(K) \le M$, and
$\Gamma > 0$. Suppose that in every closed unit square $Q \subseteq K$ one can choose a
closed set $C(Q) \subseteq \operatorname{int} Q$ with $\mu(C(Q)) \ge \Gamma$. Then $K$
holds at most $M / \Gamma$ unit squares with disjoint interiors.

*Proof.* The sets $C(Q_i)$ lie in pairwise disjoint open interiors, so they are pairwise
disjoint, and $n\Gamma \le \sum_i \mu(C(Q_i)) = \mu(\bigcup_i C(Q_i)) \le M$. ∎

The net families T, M and L use cores $C(Q)$ of side $B$ at a nearby net angle (§1.5).
Family D uses a scaling instead (§1.7): a packing in a side $L' < L$, scaled by
$L / L' > 1$, gives squares of side greater than one in $K$, and their concentric closed
unit squares are the disjoint sets.

**Obligation K.** Admission must establish, exactly: every mass is nonnegative; $M$, the
exact sum of all masses after expansion, satisfies $M < n$; $\Gamma \ge 1$; and the
measure the checks run on is the measure whose mass is $M$.

### 1.4 Certificate Formats

Every number in a certificate file is read as an exact rational.
A JSON number token is read from its decimal text, never through binary floating point:
`4.8975` is $48975/10000$. A JSON string holds a decimal or a fraction `p/q`. Duplicate
JSON keys are refused.
Files stored here as `.gz` are deterministic gzip of the upstream bytes;
[`devtools/retained_data.py`](../../../../packing/devtools/retained_data.py) reads them.

| Format | Files | Fields used | Expansion | $\Gamma$ | Centre domain |
| --- | --- | --- | --- | --- | --- |
| T | `certified_candidate.json` | `L`, `B`, `rectangles` ($[x_0, y_0, x_1, y_1]$ rows), `weights` (one per row; zero allowed), `coverage_lower_bound_exact`; $n$ from the case name or the register when the file has no `n` | Each row with positive weight $w$ is an orbit representative of mass $w$ | `coverage_lower_bound_exact`, $10001/10000$ in every file here | Tokoharu’s, §1.5 |
| M | `candidate.json` | `n`, `L`, `B`, `rectangles` (objects with `rectangle` and `mass`), `points`, `total_mass` | Each rectangle is an orbit representative; a nonempty `points` list is refused (none occurs) | $1$ | Per-bin, §1.5 |
| L | `candidate.json`, `schema` `point_line_rectangle_v1` | `n`, `L`, `B`, `net` (`step` $= 83/40000$, `last` $= 200$, else refuse), `primitives` (`kind` in `point`, `segment`, `rectangle`; `geometry` of 2, 4, 4 numbers; `mass`), `total_mass` | Every primitive is an orbit representative | $1$ | Tokoharu’s, §1.5 |
| D | `*_mixed_cover_*.txt`, header `mixed 1` | as the format statement: $s$, $D$, $W$, points `X Y w`, segments `X0 Y0 X1 Y1 w`, polygons (refused if any) | None: the file lists the whole measure | $1$ | All poses, §1.7 |
| P | `*_closed_cover_*.txt` (no header word) | $s$, $D$, $W$, points | None | $1$ | All poses, §1.7 |

Formats D and P are documented in the retained format statements
([points](../../../../packing/resources/web/evand-square-packing-2026-09-26/square-packing/s12/certificates/FORMAT.md),
[mixed](../../../../packing/resources/web/evand-square-packing-2026-09-28/square-packing/s12/certificates/s21/FORMAT.md)),
which are implementer inputs.

**Admission obligations.** Refuse, before any geometry: a malformed file; a negative
mass; a rectangle without positive area, a segment of length zero; a piece outside
$[0, L]^2$; `total_mass` (where present) different from the exact sum; $M \ge n$;
$0 < B < 1$ and $L > 1$ failing; in format D a segment that is not axis-parallel or any
polygon. In format T the rectangles of positive weight also lie strictly inside
$(\varepsilon, L - \varepsilon)^2$ with $\varepsilon = 1/20000$, which the format’s
optional smoothing lemma needs and the bound does not; check it and report it, but it is
not a premise of §1.5.

### 1.5 The Net-and-Shrink Argument (Families T, M, L)

**The net.** $D = 83/40000$, $t_r = rD$ for $r = 0, \dots, 200$,
$\theta_r = 2 \arctan t_r$, and the exact rationals
$c_r = (1 - t_r^2)/(1 + t_r^2) = \cos\theta_r$, $s_r = 2t_r/(1 + t_r^2) = \sin\theta_r$.
The core side is $B = 9977/10000$ in every certificate here; read it from the file.

**Lemma N1 (reach).** If $t_{200}^2 + 2t_{200} - 1 > 0$ (here $89/40000$), then
$t_{200} > \tan(\pi/8)$, and every half-angle tangent $t \in [0, \tan(\pi/8)]$ has an
index $r$ with $|t - t_r| \le D/2$.

**Lemma N2 (half-angle).** For $t, t_r \ge 0$ with $\theta = 2\arctan t$,
$\tan(|\theta - \theta_r|/2) = |t - t_r| / (1 + t t_r) \le |t - t_r|$.

**Lemma N3 (projection width).** With $\delta = |\theta - \theta_r|$ and
$z = \tan(\delta/2)$, $\cos\delta + \sin\delta = (1 + 2z - z^2)/(1 + z^2) \le 1 + 2z$,
because $(1 + 2z)(1 + z^2) - (1 + 2z - z^2) = 2z^2 + 2z^3 \ge 0$.

**Lemma N4 (strict containment).** If $B(1 + D) < 1$ (here $399908091/400000000$), then
for every $\theta \in [0, \pi/4]$ and any $r$ with $|t - t_r| \le D/2$, the closed core
$C_B(c, \theta_r)$ lies in the open interior of $Q(c, \theta)$. *Proof.* In the frame of
$Q$, the core is a square of side $B$ turned by $\delta$; its half-extent along each
axis of $Q$ is $\tfrac B2(\cos\delta + \sin\delta) \le \tfrac B2(1 + D) < \tfrac12$ by
N2 and N3. ∎

**Lemma N5 (orientation fold).** If $\mu$ is invariant under a reflection of $K$ that
maps orientation $\theta$ to $\pi/2 - \theta$ (the diagonal $\tau$, or $\sigma_x$, which
maps it to $-\theta \equiv \pi/2 - \theta$), then statements for cores at the angles
$+\theta_r$ cover unit squares at every orientation: a square at
$\theta \in (\pi/4, \pi/2)$ is the image of a square at $\pi/2 - \theta \in (0, \pi/4)$,
whose core maps back to a core strictly inside the original with the same measure.

**Lemma N6 (quadrant fold).** If $\mu$ is invariant under the quarter turn about
$(L/2, L/2)$, which maps the core at $\theta_r$ centred at $c$ to the core at
$\theta_r + \pi/2$, the same set, centred at the image of $c$, then coverage on the
closed quadrant $[L/2, L/2 + E]^2$ implies coverage on $[L/2 - E, L/2 + E]^2$.

N5 and N6 need $D_4$ invariance, which the expansion of §1.2 provides for formats T, M
and L. An implementation that admits a measure without expansion must check invariance
exactly, as a measure: aggregated point masses, merged densities.

**Centre domains.** At index $r$ the claim is checked on the closed quadrant
$\Omega_r = [L/2, L/2 + E_r]^2$, with:

- **Tokoharu’s domain** (formats T and L): $E_r = (L - B(c_r + s_r))/2$. The core at
  $\theta_r$ lies in $K$ exactly when its centre is in
  $[\tfrac B2(c_r + s_r), L - \tfrac B2(c_r + s_r)]^2$, since its extreme coordinates
  are attained at vertices.
- **The per-bin domain** (format M): $E_r = L/2 - \rho(a_r)$ with
  $a_r = \max(0, t_r - D/2)$ and $\rho(a) = (1 + 2a - a^2)/(2(1 + a^2))$, the half-width
  of a unit square at half-angle tangent $a$. Every unit square in $K$ whose orientation
  is assigned to node $r$ (half-angle in $[a_r, t_r + D/2] \cap [0, \tan(\pi/8)]$) has
  its centre in $[\rho(a_r), L - \rho(a_r)]^2$, because $\rho$ increases on
  $[0, \tan(\pi/8)]$. Centres outside it carry no core that the counting lemma uses.

**Theorem N.** Suppose admission (Obligation K) holds, N1 and N4 hold, the measure is
$D_4$-invariant, and for every $r \in \lbrace 0, \dots, 200\rbrace$ and every
$c \in \Omega_r$, $\mu(C_B(c, \theta_r)) \ge \Gamma$. Then $s(n) \ge L$. *Proof.* Each
unit square of a packing has an orientation folded to $[0, \pi/4]$ (N5), a node $r$
within $D/2$ (N1), and a core at $\theta_r$ strictly inside it (N4) whose centre lies,
after the quarter-turn fold (N6), in $\Omega_r$. Lemma K. ∎

**Obligations N.** Check N1, N4 and $E_r > 0$ for all 201 indices exactly.
Check every directional statement on its whole closed domain, for all 201 indices, with
no index skipped and none counted twice.

### 1.6 Lower Bounds on a Centre Box (Net Mode)

Fix $r$ and write $C(c) = C_B(c, \theta_r)$, $\gamma = c_r$, $\varsigma = s_r$ (both
nonnegative). A **centre box** is a closed rectangle $X = [x_0, x_1] \times [y_0, y_1]$
with midpoint $c^\ast$ and half-widths $h_x, h_y$. In the core’s frame, a point $p$ has
local coordinates $u_p(c) = \gamma(p_x - c_x) + \varsigma(p_y - c_y)$ and
$v_p(c) = -\varsigma(p_x - c_x) + \gamma(p_y - c_y)$, and $p \in C(c)$ iff
$|u_p(c)| \le B/2$ and $|v_p(c)| \le B/2$. As $c$ ranges over $X$,
$u_p(c) - u_p(c^\ast)$ ranges over $[-e_u, e_u]$ and $v_p(c) - v_p(c^\ast)$ over
$[-e_v, e_v]$, exactly, with $e_u = \gamma h_x + \varsigma h_y$ and
$e_v = \varsigma h_x + \gamma h_y$.

**Branch and bound.** Each domain $\Omega_r$ is covered by a finite tree of closed
boxes, each split into closed halves that cover it.
A leaf is **certified** when a lower bound $\ell(X) \le \inf_{c \in X} \mu(C(c))$
satisfies $\ell(X) \ge \Gamma$. The direction is certified when every leaf is.
Work limits and depth floors are the implementer’s; reaching one leaves the direction
**unresolved**, never certified.

**B0 (combination).** If $\mu = \sum_a \mu_a$ with each $\mu_a \ge 0$ and
$\ell_a(X) \le \inf_{c \in X} \mu_a(C(c))$, then $\ell(X) = \sum_a \ell_a(X)$ is a valid
lower bound (a sum of infima is at most the infimum of the sum).
*Obligation:* each atom counted in exactly one term; the sum rounded down if inexact.

**B1 (classification and inheritance).** Call an atom *inside* on $X$ if its support
lies in $C(c)$ for every $c \in X$ (it then contributes its full mass), and *outside* if
$\mu_a(C(c)) = 0$ for every $c \in X$ (it contributes nothing).
If an atom is inside (outside) on $X$, it is inside (outside) on every sub-box of $X$,
so children inherit both classes and only the remaining, **straddling** atoms need work.
*Obligation:* “inside” proved for every $c \in X$, e.g. every extreme point $q$ of the
support has $|u_q(c^\ast)| + e_u \le B/2$ and $|v_q(c^\ast)| + e_v \le B/2$; “outside”
proved as zero measure, not as disjoint interiors: a point on a core’s boundary is
inside it, and at $\theta_0 = 0$ an axis-parallel segment can lie along a core edge and
count in full. A separating line with a strict gap for every $c \in X$ suffices for
points; a separating line with a non-strict gap suffices for rectangles and for segments
that are not parallel to it.

**B2 (point).** If $|u_p(c^\ast)| + e_u \le B/2$ and $|v_p(c^\ast)| + e_v \le B/2$, then
$p \in C(c)$ for every $c \in X$ and the point contributes $w$; otherwise use $0$.
Equivalently, test the four corners of $X$, since $u_p$ and $v_p$ are affine in $c$.
*Obligation:* the inequalities certified for every $c \in X$, exactly or with
enclosures.

**B3 (segment by convexity).** Let
$\Lambda(X) = \lbrace \lambda \in [0, 1] : P(\lambda) \in C(c) \ \forall c \in X\rbrace$.
It is a closed interval:
$\Lambda(X) = [0,1] \cap \lbrace \lambda : |u_{P(\lambda)}(c^\ast)| \le B/2 - e_u\rbrace \cap \lbrace \lambda : |v_{P(\lambda)}(c^\ast)| \le B/2 - e_v\rbrace$,
an intersection of intervals because $u$ and $v$ are affine in $\lambda$. The segment
contributes at least $w\,|\Lambda(X)|$, and at least $w(\lambda_1 - \lambda_0)$ for any
$[\lambda_0, \lambda_1] \subseteq \Lambda(X)$: if $P(\lambda_0)$ and $P(\lambda_1)$ lie
in the convex set $C(c)$, so does every point between them, and uniform mass by length
is uniform in $\lambda$. *Obligation:* either compute $\Lambda(X)$ exactly, or choose
$\lambda_0 \le \lambda_1$ by any means and prove both endpoints inside every core of
$X$; charge a certified lower bound on $w(\lambda_1 - \lambda_0)$. Segments of any
direction are covered.

**B4 (uniform rectangle).** For a rectangle $R = [a, d] \times [b, e]$ with density
$\rho$, let $f_R(c) = \rho\,|R \cap C(c)|$ and let $F$ be the sum of $f_R$ over the
straddling rectangles.
Any of the following is a valid lower bound on $\inf_X F$, and so is their maximum.

- **(a) Fundamental theorem, first order.** $F$ is Lipschitz.
  Where its partial derivatives exist,
  $\partial_x f_R(c) = \rho\,(\ell_{\text{left}}(c) - \ell_{\text{right}}(c))$ and
  $\partial_y f_R(c) = \rho\,(\ell_{\text{bottom}}(c) - \ell_{\text{top}}(c))$, where
  $\ell_{\text{left}}(c)$ is the length of the edge $\lbrace a\rbrace \times [b, e]$
  inside $C(c)$, and so on.
  In one dimension, $x \mapsto |[a, d] \cap [x - B/2, x + B/2]|$ has derivative
  $\mathbf 1[a \in \text{core}] - \mathbf 1[d \in \text{core}]$ away from its
  breakpoints. Integrating along the two axis-parallel segments from $c^\ast$ to
  $(c_x, c^\ast_y)$ to $c$, which lie in $X$, gives, for every $c \in X$,
  $$
  F(c) \ \ge\ F(c^\ast) - h_x G_x - h_y G_y,\qquad
  G_x \ge \sup_{c' \in X} \Big|\sum_R \rho_R(\ell_{\text{left}} - \ell_{\text{right}})(c')\Big|,
  $$
  and likewise $G_y$. The bound holds across changes in the intersection’s
  combinatorics; no second derivative is used.
  *Obligation:* a certified lower bound on $F(c^\ast)$ (for an enclosed $c^\ast$, one
  valid at every centre of the enclosure: an exact clip, or a polygon proved inside both
  $R$ and every such core), and certified upper bounds $G_x, G_y$ on the sup of the
  derivative sums over the whole box (each chord length enclosed over $X$; cancellation
  inside the sum is allowed).
- **(b) Common core.** The set
  $K(X) = c^\ast + R_{\theta_r}\big([-(B/2 - e_u), B/2 - e_u] \times [-(B/2 - e_v), B/2 - e_v]\big)$,
  when both half-sides are positive, lies in $C(c)$ for every $c \in X$, so
  $F(c) \ge \sum_R \rho_R |R \cap K(X)|$. This is the bound `sqpack.rectangle_density`
  uses as `common-core`. *Obligation:* the area of each $R \cap K(X)$ bounded below.
- **(c) Corner minimum.** For convex $R$ and $C_0$, $c \mapsto |R \cap (C_0 + c)|^{1/2}$
  is concave on the convex set where the intersection has positive area
  (Brunn–Minkowski). So if the overlap is positive at all four corners of $X$, its
  minimum over $X$ is at least the least corner overlap; otherwise $0$ bounds it.
  *Obligation:* corner areas bounded below; the positivity test exact or certified.

**B5 (the axis direction, rectangles only).** At $r = 0$ the core is axis-parallel and,
for a measure of rectangles alone,
$F(c) = \sum_R \rho_R\,\lambda^x_R(c_x)\,\lambda^y_R(c_y)$ with
$\lambda^x_R(x) = |[a, d] \cap [x - B/2, x + B/2]|$, piecewise linear with breakpoints
at $a \pm B/2$ and $d \pm B/2$. On each cell of the grid formed by all breakpoints
inside the domain interval and the two domain ends, $F$ is bilinear, so its minimum over
the cell is at a corner, and the minimum over $\Omega_0$ is the minimum over the grid
vertices. *Obligation:* the grid contains every breakpoint of every image inside the
domain, on both axes; every vertex value is certified $\ge \Gamma$. With points or
segments present, $F$ is not bilinear and a point’s capture is only upper
semicontinuous: use B0 to B4 with the axis-parallel core instead.

### 1.7 The Continuous-Angle Argument (Family D)

**Statement.** Formats D and P assert that every closed unit square
$Q \subseteq [0, s]^2$, at every centre and angle, has $\mu(Q) \ge 1$. With $M < n$ this
gives $s(n) \ge s$ by the scaling form of Lemma K (§1.3). There is no net and no shrink:
the margin in the scale direction may be zero, so the comparison with $1$ must be exact
or certified.

**Poses and admissibility.** Use $u = \tan(\theta/2)$, so
$C = \cos\theta = (1 - u^2)/(1 + u^2)$ and $S = \sin\theta = 2u/(1 + u^2)$ are rational
in $u$. Let $w(u) = C + S = (1 + 2u - u^2)/(1 + u^2)$. The pose $(c, u)$ is
**admissible**, $Q \subseteq [0, s]^2$, iff $w/2 \le c_x, c_y \le s - w/2$. Inadmissible
poses are exempt.

**Regions.**

- *$D_4$ mode.* If $\mu$ is invariant, as a measure (point masses aggregated by
  coordinate, line densities merged), under $x \mapsto s - x$ and
  $(x, y) \mapsto (y, x)$, then every pose is equivalent to one with $c \in [0, s/2]^2$
  and $\theta \in [0, \pi/4]$, and $u \in [0, \tfrac12]$ contains $\tan(\pi/8)$. Region:
  $[0, s/2]^2 \times [0, \tfrac12]$.
- *Full mode*, no symmetry assumed: all centres with $u \in [0, \tfrac12]$ for $\mu$,
  and the same for $\mu$ reflected by $y \mapsto s - y$. The reflection maps
  $Q(c, \theta)$ to a square at $-\theta \equiv \pi/2 - \theta$, so the second pass
  covers $\theta \in [36.87°, 90°]$ and the two cover every pose.

*Obligation:* in $D_4$ mode, check invariance exactly as a measure and refuse otherwise.
Full mode needs no check and is preferred wherever the cost allows.

**Boxes.** A pose box $\mathcal B = [x_0, x_1] \times [y_0, y_1] \times [u_0, u_1]$,
closed; splits into closed halves.
**Main property:** a bound $L(\mathcal B) \le \mu(Q(c, u))$ holds at every admissible
pose of $\mathcal B$. A box is a leaf when $L(\mathcal B) \ge 1$ or when it has no
admissible pose; the region is certified when every root’s tree has only such leaves.

**Lemma E (empty boxes).** $w'(u) \propto 2 - 4u - 2u^2$, so $w$ increases on
$[0, \sqrt2 - 1]$ and decreases after; on $[u_0, u_1]$,
$w \ge w_{\min} = \min(w(u_0), w(u_1))$. If $x_1 < w_{\min}/2$, or
$x_0 > s - w_{\min}/2$, or the same for $y$, no pose of $\mathcal B$ is admissible.

**Lemma P (points).** With $a = p_x - c_x$ and $b = p_y - c_y$, $p \in Q(c, u)$ iff all
four of
$$
\begin{aligned}
G_0 &= (-2a - 1)u^2 + 4bu + (2a - 1) \le 0, &
G_1 &= (2a - 1)u^2 - 4bu + (-2a - 1) \le 0,\\
G_2 &= (-2b - 1)u^2 - 4au + (2b - 1) \le 0, &
G_3 &= (2b - 1)u^2 + 4au + (-2b - 1) \le 0,
\end{aligned}
$$
which are $X \le \tfrac12$, $X \ge -\tfrac12$, $Y \le \tfrac12$, $Y \ge -\tfrac12$ for
$(X, Y) = R_{-\theta}(p - c)$, multiplied by $2(1 + u^2) > 0$. Each $G_k$ is affine in
$c$ for fixed $u$, so its maximum over the box is at a corner of
$[x_0, x_1] \times [y_0, y_1]$; at a corner it is a quadratic in $u$, whose maximum on
$[u_0, u_1]$ is at an end or at an interior vertex.
A point with all four maxima $\le 0$ is in $Q$ at every pose of the box.
*Obligation:* decide the four maxima exactly (integer or rational arithmetic) or with
certified upper bounds; count the point only if all four are proved $\le 0$.

**Chords of a vertical line.** For $0 < \theta < \pi/2$, the line $x = \ell$ and
$d = c_x - \ell$, the set $\lbrace y : (\ell, y) \in Q\rbrace$ is
$[c_y + \max(f_1, g_1),\ c_y + \min(f_2, g_2)]$ (empty if the ends cross), with
$$
f_1 = \frac{dC - \tfrac12}{S} = \frac{d - \tfrac12}{2u} - \frac{(d + \tfrac12)u}{2},\quad
f_2 = \frac{dC + \tfrac12}{S} = \frac{d + \tfrac12}{2u} + \frac{(\tfrac12 - d)u}{2},\quad
g_1 = \frac{-dS - \tfrac12}{C},\quad g_2 = \frac{-dS + \tfrac12}{C}.
$$
($f$ from $|X| \le \tfrac12$, $g$ from $|Y| \le \tfrac12$, with $S, C > 0$.) Each is
affine in $d$ for fixed $u$; enclosures over a box follow from monotonicity and the
critical points of $\alpha/u + \beta u$ and of $-d\tan\theta \pm \tfrac12\sec\theta$ in
$u$.

**Line measures.** A line $x = \ell$ carries $\nu_\ell$: the uniform densities of the
segments lying on it (overlapping segments add), with continuous, nondecreasing,
piecewise-linear cumulative
$F_\ell(y) = \nu_\ell^{\text{seg}}(\lbrace \ell\rbrace \times (-\infty, y])$, plus the
**atoms**: points on the line assigned to it.
Each point is assigned to at most one line or to none (an ordinary point).
The assignment is free: soundness needs only that the parts $\mu_{\text{ord}}$ and
$\nu_\ell$ are nonnegative measures summing to $\mu$, which holds because a vertical and
a horizontal line meet in a point, where segment densities put no mass.

**Lemma S (one line).** If, at every pose of the box with $u > 0$, the chord contains
$[y_{\text{lo}}, y_{\text{hi}}]$, then
$\nu^{\text{seg}}_\ell(Q) \ge (F_\ell(y_{\text{hi}}) - F_\ell(y_{\text{lo}}))^+$. An
atom counts if all four of its conditions (Lemma P) are proved on the box.
*Obligation:* $y_{\text{lo}} \ge \sup (c_y + \max(f_1, g_1))$ and
$y_{\text{hi}} \le \inf (c_y + \min(f_2, g_2))$ over the box, certified.

**Lemma Z (the pair at unit spacing).** For lines $a: x = \ell$ and $b: x = \ell + 1$,
$d_b = d_a - 1$ and
$$
f_2(d - 1, u) = \frac{(d - 1)C + \tfrac12}{S} = f_1(d, u) + \frac{1 - C}{S} = f_1(d, u) + u .
$$
So with $\zeta = c_y + f_1(d_a, u)$, the lower $X$-end of $a$’s chord, the upper $X$-end
of $b$’s chord is exactly $\zeta + u \ge \zeta + u_0$. For every pose of the box,
$$
\nu_a(Q) + \nu_b(Q) \ \ge\ \Phi(\zeta) =
\big[F_a(h_a) - F_a(\max(\zeta, l_a))\big]^+ +
\big[F_b(\min(\zeta + u_0, h_b)) - F_b(l_b)\big]^+ + A_a(\zeta) + A_b(\zeta),
$$
where $l_a$ bounds $c_y + g_1(d_a)$ above, $h_a$ bounds $c_y + \min(f_2, g_2)(d_a)$
below, $l_b$ bounds $c_y + \max(f_1, g_1)(d_b)$ above and $h_b$ bounds $c_y + g_2(d_b)$
below, all over the box.
The upper $X$-end of $b$ may be tightened to
$\min(\max(\zeta + u_0, \underline{H}_b), h_b)$ with $\underline H_b$ a lower bound of
$c_y + f_2(d_b)$ over the box.
$A_a(\zeta)$ is the mass of $a$’s atoms whose other three conditions are proved on the
box and whose height is $\ge \zeta$; $A_b(\zeta)$ of $b$’s atoms with the other three
proved and height $\le \zeta + u_0$; atoms with all four proved count always.
Hence $\nu_a(Q) + \nu_b(Q) \ge \inf_{z \in Z} \Phi(z)$ for any $Z$ containing the range
of $\zeta$ over the box, which may be unbounded.
$\Phi$ is piecewise linear in $z$ with breakpoints among $l_a$, $h_a$, the breakpoints
of $F_a$, and $h_b - u_0$, $l_b - u_0$ (and $\underline H_b - u_0$ when the tightening
is used), the breakpoints of $F_b$ shifted by $-u_0$, plus jumps at the atom heights:
$A_a$ is left-continuous and nonincreasing, $A_b$ right-continuous and nondecreasing.
Its infimum over an interval is the least of its one-sided limits at those candidates
and at the interval’s ends, and of its constant tails.
*Obligation:* the four end bounds and the range of $\zeta$ certified over the box; the
infimum computed exactly over the candidates, or bounded below with both one-sided
limits at every jump.
This lemma is what closes the boxes near $\theta = 0^+$, where $\zeta$ sweeps the whole
line and any bound that treats the two lines separately is zero.

**Lemma W (walls at distance one).** If the left wall is $x = 0$ and $\ell = 1$, then at
every admissible pose with $u > 0$, $c_y + f_2(d) \ge c_y + q(u)$, where
$q(u) = (1 - u^2 + 2u^3)/(2(1 + u^2))$. *Proof.* $\partial f_2/\partial d = C/S > 0$;
admissibility gives $d \ge w/2 - 1$; and
$f_2(w/2 - 1) = ((1 - C)^2 + SC)/(2S) = u(1 - C)/2 + C/2 = q(u)$. ∎ By the mirror
computation, if $\ell = s - 1$ then $c_y + f_1(d) \le c_y - q(u)$. On $[u_0, u_1]$,
$q(u) \ge (1 - u_1^2 + 2u_0^3)/(2(1 + u_1^2))$. *Obligation:* used only for lines at
distance exactly one from a wall, and only at admissible poses (the box may contain
inadmissible ones; the bound need not hold there).

**Lemma H ($\theta = 0$).** A box with $u_0 = 0$ contains axis-parallel poses, where the
chord of $x = \ell$ is $[c_y - \tfrac12, c_y + \tfrac12]$ if $|d| \le \tfrac12$ and
empty otherwise, and segments on the square’s edges count in full.
*Obligation:* the box’s bound must hold at its admissible poses with $u = 0$ as well,
not only in the limit $u \to 0^+$. The chord functions $f_1, f_2$ are unbounded as
$u \to 0^+$, so enclosures over $[0, u_1]$ must say what they do there, and the
implementer must write out and test its own argument that every single-line and pair
bound it computes on such a box is at most the true mass at every admissible pose with
$u = 0$.

**Lemma T (horizontal lines).** The rotation $(x, y) \mapsto (-y, x)$ maps
$Q(c, \theta)$ to $Q(c', \theta)$ (the unit square is invariant under a quarter turn),
the container to $[-s, 0] \times [0, s]$ with admissibility preserved, and horizontal
lines to vertical ones.
Every vertical-line lemma applies there.

**Lemma DP (partition).** For any partition of the vertical lines into singletons and
pairs at distance exactly one, and likewise for the horizontal lines,
$\mu(Q) \ge P(\mathcal B) + \sum_{\text{groups}} (\text{group bound})$, where
$P(\mathcal B)$ is the mass of the ordinary points proved inside.
The best partition along each chain $\ell, \ell + 1, \ell + 2, \dots$ is a dynamic
programme; any partition is sound.

### 1.8 Arithmetic Contract

- Admission, expansion, mass sums, net identities, domains and every comparison that
  decides a refusal are exact.
- Every inequality that certifies a box uses exact arithmetic or an **enclosure**: an
  interval $[\underline v, \overline v]$ that contains the exact real value, produced by
  IEEE 754 binary64 operations in round-to-nearest followed by a one-ulp widening in the
  safe direction, by error-free transformations, or by integer or fixed-point arithmetic
  with checked overflow.
- Each input rational enters through a certified enclosure: exact when it is a binary64,
  otherwise two adjacent binary64 values proved by an exact comparison to straddle it.
- No contraction into fused multiply-add except where an exact FMA is intended, no
  reassociation, no fast-math, no flush-to-zero, and the default rounding mode.
  Rust satisfies this by default; a C or C++ build would need the flags stated.
- A NaN, an infinity, or an overflow on the certification path is a refusal or an
  unresolved box, never a certificate.
- The final test compares the lower end of $\ell$ with $\Gamma$: $\Gamma = 1$ is exact
  in binary64; $10001/10000$ is not, and is compared through an upward enclosure.
- **Differential obligation.** The exact path,
  [`sqpack.rectangle_density`](../../../../packing/src/sqpack/rectangle_density.py) for
  rectangle areas or the implementation’s own exact mode, evaluates the same lower-bound
  expression on a sample of boxes from every family; every float enclosure must contain
  the exact value of the expression it encloses.

### 1.9 Verdicts, Refusals and Reports

Per direction (net mode) or per root (continuous mode), the verdict is `CERTIFIED`,
`UNRESOLVED` (with the open boxes listed exactly) or, for the whole certificate,
`REFUSED` at admission.
A certificate passes only when admission holds and every direction or every root of the
region is certified.
Exit status is nonzero otherwise.
An optional witness search at unresolved boxes may report an exact pose whose exact
capture is below $\Gamma$: that is a refutation of the claim at that pose, the strongest
kind of failure report.
Each run writes a JSON report: input digests, format, $n$, $L$, $\Gamma$, mode, and per
direction or root the verdict, nodes, leaves, least certified leaf bound, CPU and wall
seconds; and the implementation’s source digest and build flags.

## 2. Clean-Room Protocol

The claim `independent-implementation` is a claim about what the implementers read.
This protocol fixes that in advance and makes it auditable.

### 2.1 Roles

| Role | Who | May read | Produces |
| --- | --- | --- | --- |
| Spec author | Lane W1 (this slice) | Everything, including the authors’ sources, which it built and profiled | This specification, `timings.json`, the dirty-side research note |
| Implementer | Lane W2, and any later implementer lane | The allowlist in §2.2 only | The verifier, its tests, its reports |
| Adversarial reviewer | Two reviewers, distinct from W2 and from each other | Everything | Two review documents with verdicts |
| Coordinator | The integrating session | Everything | Integration, beads, the evidence entries; relays nothing code-level to W2 |

Questions from an implementer go to the spec author through the coordinator and come
back as committed amendments to this file, which the spec author writes in the terms of
§1. No snippet, pseudo-code, constant or structure taken from an author’s checker
crosses to the clean side, whether in an amendment, a review comment or a bead
description.

### 2.2 Inputs Allowed to Implementers

1. This specification and its committed amendments.

2. Certificate data: the candidate and cover files, `certificate_metadata.json`,
   `verification_summary.json`, `verified_angles.jsonl`, `certificate.json`,
   `manifest.json`, the packets’ and certificates’ README files for their description of
   the data, and the two retained format statements named in §1.4.

3. [`timings.json`](../../../../packing/benchmarks/results/author-checker-profile-2026-10-02/timings.json)
   of the baseline profile.

4. The repository’s own implementations that are not specific to an author’s checker:
   `sqpack.rectangle_density`, `sqverify_exact`, `devtools/retained_data.py`, and the
   general project guides (`AGENTS.md`, `development.md`, `conventions.md`,
   `epistemics.md`, `operating-rules.md`).

5. The mathematical sections of the reviews, and only these:

| Review | Sections allowed |
| --- | --- |
| [Tokoharu density mathematics](../../reviews/review-2026-09-22-tokoharu-density-mathematics.md) | “Mathematical Reduction”, with “All orientations”, “Continuous centre coverage and symmetry”, “Lower bounds on each centre box” and “Optional smoothing” |
| [wand125 rectangle scaling](../../reviews/review-2026-09-27-wand125-rectangle-scaling.md) | “The Net and the Box Argument at Side 9”, “The Monotone Transfers” |
| [n = 50 mixed verifier](../../reviews/review-2026-09-28-wand125-n50-mixed-verifier.md) | “The Containment Argument in Exact Arithmetic”, with “The per-node centre domain” |
| [T-069 and n = 84, 85](../../reviews/review-2026-10-02-wand125-mixed-rectangle-bounds.md) | “The Argument From Certificate to Bound” |
| [T-068](../../reviews/review-2026-10-02-wand125-rectangle-bounds-t068.md) | “The Argument From Certificate to Bound” |
| [linear certificates and n = 76](../../reviews/review-2026-10-02-wand125-linear-certificates-and-n76.md) | “The Argument From a Linear Measure to the Bound” |
| [s(59) and s(77)](../../reviews/review-2026-10-02-wand125-s59-s77-mixed-covers.md) | §3 “From Certificate to Claim” |
| [s(21) and s(45)](../../reviews/review-2026-09-28-evand-s21-s45-mixed-covers.md) | §3 “The Theorem and Its Architecture” |

### 2.3 Inputs Forbidden to Implementers

- Every author’s program and design note: anything under a packet’s `src/` or `code/`
  directory, every `.cpp`, `.rs` and `.py` file under `packing/resources/web/`, and the
  write-ups of the checkers (`ZMX2.md`, `ZM_MIXED.md`, `ZM_MIXED_AUDIT.md`,
  `LINE_COVER.md`, `S32_EXACT.md`, Tokoharu’s `docs/`), whether retained here or on
  GitHub.
- The repository’s checker-specific wrappers and probes:
  `devtools/audit_tokoharu_density.py`, `devtools/audit_wand125_rectangles.py`,
  `devtools/audit_wand125_point_and_mixed.py`, `devtools/audit_wand125_linear.py`,
  `devtools/replay_evand_zmx2.py`, `devtools/audit_evand_mixed_covers.py`,
  `devtools/tokoharu_density_probe.cpp`,
  `benchmarks/bench_rectangle_verifier_parity.py`.
- The profile’s dirty side: `benchmarks/profile_author_measure_checkers.py`, its test,
  the `attribution/` directory beside `timings.json`, and
  [the profile research note](../../research/research-2026-10-02-author-checker-profile.md).
- Replay receipts and logs under `packing/resources/web/**/receipts/`, which hold the
  checkers’ raw output.
- The review sections not listed in §2.2.

### 2.4 The Independence Record

The record lives at the root of the verifier’s crate as `independence-record.yaml`, and
every evidence entry with `relationship_to_generator: independent-implementation` that
rests on this verifier gives its path as `independence_record`. It holds:

```yaml
kind: independence-record/v1
implementation:
  path: packing/<crate>            # W2's choice
  commits: {first: <sha>, last: <sha>}
spec:
  path: docs/project/specs/active/plan-2026-10-02-independent-measure-verifier.md
  versions_read: [<commit>, ...]   # every committed version an implementer read
lanes:
  - lane: W2
    role: implementer
    sessions: [<session id>, ...]
    harness: <agent harness and version>   # never a model name
    period: {from: <UTC>, to: <UTC>}
    reads:                          # extracted from the session transcripts by the audit tool
      - {path: <repo-relative path>, at: <commit or blob>}
    fetched: [<url>, ...]
    forbidden_hits: []              # must be empty
    declaration: "<one paragraph, in the lane's words>"
  - lane: W1
    role: spec-author
    dirty_inputs: [<summary of what was read and run>]
    clean_outputs: [<this spec>, <timings.json>]
  - lane: <reviewer>
    role: adversarial-reviewer
    review: docs/project/reviews/<file>
shared_components:                  # code the verifier shares with anything else
  - {path: packing/src/sqpack/rectangle_density.py, use: exact reference oracle, written here}
audit: {tool: <devtools path>, ran_at: <UTC>, result: PASS}
```

A tool, not prose, fills `reads`, `fetched` and `forbidden_hits`: it reads each
implementer session’s transcript, extracts every file read, search and fetch, matches
them against §2.3, and fails on any hit.
It runs at the end of every implementer session, while the transcripts exist, and
commits the extracted lists, not the transcripts.
Building it is part of slice 4 below.

## 3. Performance Architecture

### 3.1 The Baseline

Measured by the profiling tool on this host (Intel Xeon at 2.1 GHz, 4 logical CPUs,
shared with other sessions; load average 10 to 15 during the run), one process per
direction, child CPU time from `wait4`. Every complete direction reproduced its recorded
node count, and where recorded its leaves and printed bound.
Full figures are in
[`timings.json`](../../../../packing/benchmarks/results/author-checker-profile-2026-10-02/timings.json).

| Family, certificate | Pieces after expansion | Directions timed | Boxes per direction | CPU per box | CPU per direction |
| --- | ---: | --- | ---: | ---: | ---: |
| T, wand125 `rect_n20_L48975` | 1,832 rectangles | 30, 98, 195 | 34,887 to 89,205 | 297 to 533 µs | 10.4 to 47.5 s |
| M, wand125 `mixed_n76_L894` | 2,536 rectangles | 3, 101, 200 | 108,685 to 246,833 | 227 to 366 µs | 24.6 to 90.4 s |
| L, wand125 `mixed_n101_L1028` | 9,872 (2,664 points, 7,176 segments, 32 rectangles) | 35, 113 | 76,875 to 146,489 | 457 to 467 µs | 35.2 to 68.4 s |

The linear checker’s axis direction, timed over its first 100,000 boxes, costs 397 µs
per box. Cost per box is flat with depth for the linear checker (456 µs over the first
3,000 boxes of direction 35, 449 µs over 30,000) and rises with depth for the mixed one
(49 µs over the first 3,000 boxes of direction 3, 136 µs over 30,000, 227 µs over all of
it). A first run of the same directions an hour earlier agreed within about 5 per cent.

The exact Python path on the same rectangle certificate and direction, capped at 400
boxes, spent 55 ms of CPU per box, about 180 times the outward-rounded checker’s 297 µs
on that direction.
The replay receipts put whole certificates at 3.6 CPU-hours ($n = 76$)
and 7.7 CPU-hours ($n = 101$) here, and the upstream records put `rect_n20_L48975` at
13.1 million boxes and 21 minutes on the author’s machine.

**Locality census.** On a 15 × 15 grid of centres over each timed direction’s domain, a
float diagnostic (no proof authority) counted the pieces that a box of half-width
$E_r/2^9$, the scale of the leaves, can neither prove inside every core nor outside
every core:

| Certificate | Pieces | Straddling at leaf scale, mean (max) | Inside, mean | Near the core’s bounding box, mean |
| --- | ---: | ---: | ---: | ---: |
| `rect_n20_L48975`, direction 30 | 1,832 | 20.0 (73) | 111.1 | 157.8 |
| `mixed_n76_L894`, direction 3 | 2,536 | 52.2 (100) | 18.6 | 71.7 |
| `mixed_n101_L1028`, direction 35 | 9,872 | 25.5 (52) | 95.6 | 153.2 |

### 3.2 What the Baseline Justifies

- **Classification with inheritance and a spatial index (B1): justified.** A leaf-scale
  box has 20 to 52 straddling pieces on these certificates, against 72 to 158 whose
  bounding boxes meet the swept core and 1,832 to 9,872 in all.
  Inheriting the inside mass and the straddling list from parent to child, and finding a
  root’s candidates through a uniform grid over the container with cells about one core
  wide, makes the per-box work proportional to the straddling count and independent of
  the measure’s size. A bounding-box filter alone leaves 1.4 to 8 times more pieces to
  evaluate.
- **Outward-rounded binary64 enclosures for the bulk: justified.** Binary64 enclosures
  already decide these certificates, and the least certified leaf bounds the authors
  record sit between $4 \times 10^{-11}$ (mixed, $n = 90$) and about $2 \times 10^{-7}$
  (`rect_n20_L48975`) above $\Gamma$, while an enclosure of a sum of a few hundred terms
  of order one is about $10^{-13}$ wide.
  Widening by one ulp costs an inline bit operation in Rust (`next_up`, `next_down`);
  widening once per compound expression, where a proved rounding-error bound allows it,
  rather than after every operation, is a further constant factor worth measuring.
- **An exact fallback near the threshold: justified as a safety net, not as a hot
  path.** Use the exact mode only for boxes whose enclosure straddles $\Gamma$ at the
  depth floor, and as the differential oracle of §1.8. The exact path costs two orders
  of magnitude more per box, so it must stay rare.
- **Parallelism over directions and subtrees: neutral for the per-core target.** The 201
  directions are independent, and the authors’ drivers already run them in parallel;
  speed is compared per core.
- **Not justified by the baseline, left to W2’s own measurements:** SIMD or batched
  evaluation of the straddling list (worth measuring once classification makes per-piece
  arithmetic the cost), reuse across neighbouring directions (a warm start can save at
  most the interior nodes, about half of a direction’s boxes), and tighter bounds that
  reduce the node count (B4 (c), second-order terms).
  Each is an experiment for W2’s performance loop with its own baseline.

### 3.3 Where the Speedup Comes From

An estimate from first principles, not from the authors’ code: with inheritance, a box
costs its straddling pieces plus a constant for bookkeeping.
A rectangle’s area bound and its four edge chords in binary64 enclosures are a few
hundred floating-point operations, on the order of 100 ns; a point or a segment is less.
At 20 to 52 straddling pieces a box should cost 2 to 6 µs against the baseline’s 227 to
533 µs, a factor of 40 to 250 per box.
Bound quality, and so the node count, is of the same kind as the authors’ unless W2
improves it. One to two orders of magnitude per core is therefore the plausible range;
the acceptance target is thirty times on every family.
Family M has the least headroom, since its straddling count is the largest and closest
to its near count, so it is the family to watch.
The axis direction of family T is separate: its vertex grid (B5) has millions of
vertices, and evaluating each vertex against only the rectangles whose breakpoints
surround it removes the same factor there.

### 3.4 Recommended Module Boundaries

W2 owns the crate and its layout.
Boundaries that keep the proof-carrying parts small and reviewable: certificate
admission per format (exact); the exact rational core; the enclosure type and its
conversions; net mode (domains, atom bounds B0 to B5, the box tree); continuous mode
(Lemmas E, P, chords, S, Z, W, H, T, DP); reports.
A Python adapter under `devtools/` runs it on the retained certificates and writes
receipts.

## 4. Acceptance

### 4.1 Certificates

The verifier must pass every certificate in the table, from the retained files, with no
direction or root unresolved:

| Evidence entry | Format | Certificates |
| --- | --- | --- |
| `E-tokoharu-density-source-replay` | T | Tokoharu `cert_n11_L381`, `cert_n26_L5508`, `cert_n29_L571` |
| `E-wand125-rectangle-source-replay` | T | `rect_n18_L4695`, `rect_n19_L4815`, `rect_n20_L4895`, `rect_n26_L553`, `rect_n27_L56`, `rect_n30_L5865`, `rect_n31_L592`, `rect_n32_L595`, `rect_n40_L6695`, `rect_n61_L796`, `rect_n75_L889`, `rect_n78_L8955` (packet of 27 September) |
| `E-wand125-rectangle-2026-09-28-source-replay` | T | `rect_n29_L579`, `rect_n38_L654`, `rect_n39_L663`, `rect_n41_L6755`, `rect_n52_L7535`, `rect_n53_L7595`, `rect_n59_L792`, `rect_n67_L8455`, `rect_n69_L8575`, `rect_n71_L8685`, `rect_n86_L9355`, `rect_n95_L98418` |
| `E-n076-wand125-mixed-894-source-replay` | M | `mixed_n76_L894` |
| The $n = 101$ linear replay (`FULL_REPLAY_MATCHES_SHIPPED`, entry pending) | L | `mixed_n101_L1028` |
| `E-n013-evand-casefree-cover-zmx2-replay` | P | `s13_closed_cover_4` |
| `E-n021-evand-mixed-cover-zmx2-replay` | D | `s21_mixed_cover_5` |
| `E-n032-evand-closed-cover-zmx2-replay`, `E-n032-evand-zmx2-full-sym-replay` | P | `s32_closed_cover_6` |
| `E-n045-evand-mixed-cover-zmx2-replay`, `E-n045-wand125-point-cover-source-replay` | D, P | `s45_mixed_cover_7`; wand125 `point_n45_L7` cover |
| `E-n059-wand125-mixed-cover-zmx2-replay` | D | `n59_mixed_cover_8` |
| `E-n060-evand-mixed-cover-zmx2-replay` | D | `s60_mixed_cover_8` |
| `E-n077-wand125-mixed-cover-zmx2-replay` | D | `n77_mixed_cover_9` |

Stretch targets, reported here but not yet replayed: the 34 certificates of `T-068`
(packet of 1 October), the mixed certificates of `T-069` and $n = 84, 85$, and the
linear $n = 83$.

### 4.2 Controls

Every mutation control already retained must be refused, at the same direction or root
region: the rectangle controls of the 1 October packet (every weight scaled by $99/100$,
and the top contributor’s orbit dropped, on `rect_n41_L676` at direction 32), the two
mixed controls on $n = 37$, the two linear controls on $n = 101$, and the controls that
drop the heaviest point or the heaviest segment (for the point cover of $s(32)$, its
heaviest or its second-heaviest point) on $s(32)$, $s(59)$, $s(60)$ and $s(77)$. The
mutated inputs are data; the evidence lane regenerates them as files the implementer may
read.
In addition, the verifier must refuse: a measure with $M \ge n$; a $D_4$-mode cover
whose invariance is broken by one point; a certificate whose threshold is raised above
its true minimum at one direction; and a box-level fault injection that flips one inside
classification. Each refusal of a mutation must come with an unresolved box containing,
or an exact witness at, a pose whose exact capture is below $\Gamma$. The differential
tests of §1.8 cover, for rectangles, the axis direction, the first nonzero direction,
intermediate ones and the last; and separation, tangency, near tangency, containment and
partial overlap of a rectangle with a core.

### 4.3 Agreement With the Authors’ Checkers

Verdicts must agree on every direction and root.
Node counts are reported side by side and are not required to match, since the traversal
and bounds are W2’s; a ratio outside $[0.1, 10]$ on a direction is investigated and
explained in the receipt.
On each certificate’s least-bound direction, the exact capture at the centre of the
verifier’s least-bound leaf is evaluated by the exact path and must be at least
$\Gamma$. For every control, the verifier’s open boxes must contain the author’s witness
pose or yield an exact witness of its own.

### 4.4 Review and Evidence

Two adversarial reviews by distinct reviewers, neither of them an implementer, read this
specification, the implementation and, as they choose, the authors’ checkers, and record
verdicts in `docs/project/reviews/`. After both accept, each certificate family gets a
confirming evidence entry: `method: interval-certified` (or `exact-algebraic` for an
exact run), `origin: replayed-here`, `performed_by: repository`,
`relationship_to_generator: independent-implementation`, `verifiers` listing the new
verifier’s registry id, `independence_record` giving the path of the record of §2.4, a
replay command from the repository, a `limitations` statement, and a control path.
No rung moves by these entries alone: the register shows the independent implementation
as an attribute beside the rung, and `C4` still needs adversarial reviews of each claim
and the owner’s oversight record.

### 4.5 Performance

For each family, the receipt reports the verifier’s CPU per box and per direction beside
the baseline’s, on one host with the load recorded, and the whole acceptance suite’s
cost. The target is thirty times per core on every family.
Missing it does not block the evidence entries; it reopens the performance loop.

## 5. Slices, Lanes and Beads

Lanes are disjoint in deliverables and files (`OR-6`). W2’s lane is the implementation
and its performance loop, under `think-gpe0`, and owns the crate; the slices below do
not duplicate it.

| Slice | Bead | Lane | Deliverable | Files owned | Exit |
| --- | --- | --- | --- | --- | --- |
| 1. Specification and clean-room protocol | `think-s333` | W1 | This document | `docs/project/specs/active/plan-2026-10-02-independent-measure-verifier.md` | Committed; W2 reading it |
| 2. Baseline profile of the authors’ checkers | `think-fcxx` | W1 | The profiling tool, `timings.json`, the attribution and the research note | `packing/benchmarks/profile_author_measure_checkers.py`, its test, `packing/benchmarks/results/author-checker-profile-2026-10-02/`, `docs/project/research/research-2026-10-02-author-checker-profile.md` | Committed |
| — Implementation and performance loop | W2’s bead | W2 | The verifier, its tests and reports | The crate, its adapter | Passes §4.1 and §4.2 |
| 3. Adversarial review | `think-r07y` | Two reviewers | Two reviews with verdicts; findings as beads | `docs/project/reviews/review-…-independent-measure-verifier-*.md` | Both accept, or findings fixed and re-reviewed |
| 4. Evidence recording | `think-3ok2` | Coordinator | The independence-record audit tool, the record, the control inputs, the replay receipts, the evidence entries | `packing/devtools/` audit tool and its test, the record, receipts, `packing/frontier/evidence.yaml` | Entries recorded; register check passes |

Slice 3 starts when W2 declares the implementation complete for a family; slice 4’s
audit tool can be built now and must run at the end of each W2 session.

## 6. Open Questions

- Whether full mode is affordable for every family-D cover, or $D_4$ mode with its exact
  invariance check is used for some (the authors ran both for most covers).
- Whether to verify format T at its declared $\Gamma = 10001/10000$ or at $\Gamma = 1$,
  which the bound needs.
  The default is the declared threshold, so that verdicts compare with the authors’; a
  run at $\Gamma = 1$ is a cheaper second receipt.
- The `verifiers` registry and the `independence_record` field are being added by
  another lane; this plan uses the names the coordinator gave, beside the existing
  `relationship_to_generator` and `performed_by`.

## References

- [`epistemics.md`, Confirmation](../../../../epistemics.md#confirmation)
- [Exact arithmetic and verifier performance, 30 September](../../research/research-2026-09-30-exact-arithmetic-verifier-performance.md)
- [Native rectangle verification plan](plan-2026-09-29-native-rectangle-verification.md)
- The reviews named in §2.2.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
