# Mathematical Review: wand125’s Closed-Form Lower Bound s(N) ≥ a(N) for Every Non-Square N ≥ 49

Reviewed 2026-10-14 from the packet
[`packing/resources/web/wand125-closed-form-2026-10-14/`](../../../packing/resources/web/wand125-closed-form-2026-10-14/README.md),
which retains `problems/closed-form` of
[wand125/square-packing](https://github.com/wand125/square-packing/tree/9a28a84bd55dc124bfa2919bb6c4fb504dda3149/problems/closed-form)
at the pin `9a28a84` (release `closed-form-v1`, committed 2026-10-13 in `eb0fd19`), by
an AI agent: the mathematical review lane of the import (bead think-tsox), Fable at the
strong tier with max reasoning, in a worktree of its own.
The lane read the source as data and executed none of its programs except the ones the
brief allows and the intake lane had already read and run, the structure script
`validate_family.py` on one family; every other computation below is the lane’s own
code, kept under the packet’s
[`review/`](../../../packing/resources/web/wand125-closed-form-2026-10-14/review/README.md)
directory and run with the project interpreter.
No earlier review of this result exists, and none was read.
Nothing was posted anywhere and the author was not contacted.

This review registers nothing and moves no bound.
It is not a human oversight record.

## Summary for the Author

The theorem is that for every non-square integer $N \ge 49$, with
$k = \lfloor\sqrt N\rfloor$,
$s(N) \ge a(N) = k + \sup\{\delta \in (0,1] : (k+\delta)^2 - 4S^*(\delta) < N\}$, where
$S^*(\delta)$ is the largest of 34 certified savings $\alpha_i\delta + \beta_i$ over the
intervals of $\delta$ that contain it.
The lane re-derived the whole argument from the certificate to the claim: the measure
principle and the scaling that avoids double counting; the total-mass identity
$a^2 - 4S(\delta)$, which it reduced to two affine identities (in $k$ and in $\delta$)
that the structure check decides at $k = 7, 8, 9$ and both endpoints; the C4 arrangement
and the four-step localization of §2.3, whose numerical inequalities it decided exactly;
the families, poses and regions; every leaf lemma of §5 (the core and outer polygons,
the two-edge and one-sided edge lemmas, Lemma B3′ and the completeness of its contact
planes, the concavity and tangent lemmas, the CORE1 corner argument, and the
Brunn–Minkowski step behind B4U); the tiling and the product grid; and the
upper-semicontinuity closure at $u = 0$. It read `replay4d` and `seam4d_core` against §5
and found the dispatch, the guards, the root isolation and the sign test faithful to the
specification, and the three places the intake flagged sound: the modular gcd shortcut
is one-directional and correct, the `B3_PLAIN_RF` switch changes the route to the same
reduced form and nothing that is decided, and the omission of `b3d_sort.rs` from the
printed source hash is a provenance gap, not a mathematical one.

Nothing read is false, and no finding is blocking or major.
The findings are minor and notes: a structure receipt that names an unpublished revision
of its own script; a source hash that leaves out a file the checker compiles in; an
arithmetic switch whose setting no receipt records; a sentence of §2.3 that credits the
window identity for the right region where the wall-period check carries it; and small
wording points. Every one is listed with its file and line in §6, with questions in §7.

What the lane tested independently, with code kept in the packet: $a(N)$ from the
definition alone at all 3,498 non-square counts to 3,600, equal at thirty places to the
source’s `a_of_n.py` and to the intake evaluation; $a(N)$ against every bound of the 264
case records from 49 to 324, above no upper bound, equal to the known values $m$ at
$m^2 - 1, m^2 - 2, m^2 - 3$ and below $m$ at $m^2 - 4$; the 29 inequalities of the
localization; the arithmetic and digest chain of the source’s replay receipt, in which
the 158 pieces of the 25 cut records tile their regions and the published files are the
replayed ones by digest; and, on one of the 34 released intervals, interval 20
($[93/200, 47/100]$; the assets of intervals 7 and 34 were fetched too, but their runs
were stopped before their receipts were written), the family structure recomputed from
scratch, the global measure built here for $k = 7, 8, 11$ and compared with the local
family on the window, the product grid and the tiling of its four region records, and
the mass of the global measure on closed unit squares at 1,345 exactly computed poses,
random, delicate and found by descent, never below 1.

**Verdict: accepted as mathematics, reported as evidence.** The argument is correct as
specified, and the published checker implements the specification where the lane read
it. What establishes the theorem is the acceptance of all 187,183,108 leaves of the 136
records by `replay4d`, which the source reports (4,294 CPU-hours) and which has not been
reproduced here; until a complete replay runs, the bound stands as the source’s report,
read and found sound.
The sample checks of this lane decide nothing: they could have refuted the claim and did
not.

## 0. What Was Read, Run and Not Reached

Paths are relative to `packing/resources/web/wand125-closed-form-2026-10-14/`, and `CF/`
stands for `square-packing/problems/closed-form/`.

**Read in full.** `CF/SPEC.md` (687 lines), `CF/README.md`, `CF/INTERVALS.md`,
`CF/intervals.json` (decompressed), `CF/a_of_n.py`, `CF/structure/validate_family.py`
and `structure_all.py`, `CF/checker/replay4d/src/main.rs` and `sha256.rs`,
`CF/checker/seam4d_core/src/lib.rs`, `fast.rs`, `replay.rs`, `b3d.rs` (2,617 lines) and
`b3d_sort.rs`, `CF/checker/seam4d_core/tests/w0.rs`, `CF/checker/replay_all.py`,
`CF/receipts/replay.json` (decompressed), `structure.json`, `families.json` and
`published_checker.json`, `CF/ASSET.json`; the packet’s `README.md`, `register-plan.md`,
`acquisition/`, `receipts/` and `evaluation/` (the README and `closed_form_bounds.py`,
934 lines).

**Fetched for this review, into scratch, and checked against `ASSET.json` and each
archive’s `SHA256SUMS`.** The release assets `interval_0.465_0.47.tar.gz` (interval 20,
4,418,084 bytes), `interval_0.38_0.4.tar.gz` (interval 7, 10,690,117 bytes) and
`interval_0.99_1.tar.gz` (interval 34, 7,241,272 bytes): six families and twelve region
records. They stay in scratch; nothing of them is proposed for retention.
The probe of §4 ran to completion on interval 20 only; on intervals 7 and 34 it was
stopped, to stay inside the lane’s CPU budget, before a receipt was written, after an
earlier run on interval 7 had passed every structure check and reproduced the example
savings of SPEC.md §3.2 (0.589900810970916 and 0.624200093890916).

**Run.** The five programs of §4, all the lane’s own.
Of the source’s programs, `validate_family.py` was run once on interval 20’s families to
compare its decomposition with the lane’s while a bug in the lane’s own clipping was
found; the intake lane had read and run it before.

**Not reached.** No record was replayed and `replay4d` was not built: the certificate’s
acceptance rests on the source’s receipts.
Thirty-one of the 34 released intervals were not downloaded.
The site write-up and its table were not re-read beyond the intake’s digest check.
The Rust code was read, not executed, and the lane did not transliterate `b3d_sort.rs`
to test it.

## 1. The Claim, Exactly

Let $s(N)$ be the least side of a square that holds $N$ closed unit squares with
pairwise disjoint interiors, any positions and orientations.
Fix a non-square integer $N \ge 49$ and put $k = \lfloor\sqrt N\rfloor \ge 7$, so that
$k^2 < N < (k+1)^2$. The 34 intervals $I_1, \dots, I_{34}$ of `intervals.json` cover
$(0, 1]$; each is closed on the right, and $I_1 = (0, 1/50]$, $I_8 = (2/5, 81/200]$ and
$I_{34} = (99/100, 1]$ are open on the left, the rest closed.
Each carries exact rationals $\alpha_i, \beta_i$ and the certified line
$S_i(\delta) = \alpha_i\delta + \beta_i$. For $\delta \in (0,1]$ let $S^*(\delta)$ be
the largest $S_i(\delta)$ over the $i$ with $\delta \in I_i$.

**Theorem (SPEC.md §1.1, lines 17–19).** If $\delta \in (0,1]$ satisfies
$(k+\delta)^2 - 4S^*(\delta) < N$ then $s(N) \ge k + \delta$. Consequently
$s(N) \ge a(N) := k + \sup\{\delta \in (0,1] : (k+\delta)^2 - 4S^*(\delta) < N\}$.

Hypotheses, all of them: $N$ an integer, $N \ge 49$, $N$ not a square;
$k = \lfloor\sqrt N\rfloor$ (so the theorem is applied with the container side
$k + \delta \le k + 1$, and the case $\delta = 1$ is the side $k + 1$ treated with this
$k$, not with $k + 1$); the 34 lines with their exact coefficients; the open and closed
endpoints as declared.
The set in the supremum is never empty, since $\beta_1 = 0$ makes
$(k+\delta)^2 - 4\alpha_1\delta \to k^2 < N$ as $\delta \to 0^+$; the specification does
not say so, and the “consequently” needs it (note N9). The closed form (§1.1, lines
21–29) follows because each $T_i(\delta) = (k+\delta)^2 - 4(\alpha_i\delta + \beta_i)$
has derivative $2(k+\delta) - 4\alpha_i \ge 14 - 4 \cdot 1.7496 > 0$ (program 3 confirms
$\max_i \alpha_i = 1.7495351\ldots$), so on each interval the admissible $\delta$ form
an initial segment and $a(N)$ is the largest of $\min(a_i(N), k + d_1^{(i)})$ over the
intervals whose root
$a_i(N) = 2\alpha_i + \sqrt{4\alpha_i^2 + N + 4\beta_i - 4\alpha_i k}$ exceeds
$k + d_0^{(i)}$, the positive root being the relevant one since the vertex
$2\alpha_i < 4 < k$.

Each interval’s certificate is a family: finitely many axis-parallel segments with
masses (`F` fixed, `T` translating by $\delta$, `V` of variable length with fixed
density), from which §2.1 builds, for every $k \ge 7$ and $\delta \in I_i$, a
C4-symmetric measure $\mu_{k,\delta}$ on $[0, k+\delta]^2$. The certificate claims two
things of it: total mass $(k+\delta)^2 - 4S(\delta)$ with $S(\delta) = S_i(\delta)$ on
$I_i$, and $\mu_{k,\delta}(Q) \ge 1$ for every closed unit square
$Q \subset [0, k+\delta]^2$.

## 2. From the Certificate to the Claim

### 2.1 The measure principle (§1.2, lines 44–48)

If $\mu$ is a finite nonnegative measure on $[0,a]^2$ with $\mu(Q) \ge 1$ for every
closed unit square $Q \subseteq [0,a]^2$ and $\mu([0,a]^2) < N$, then $s(N) \ge a$.
Suppose $N$ unit squares pack a container of side $b < a$. Scale by $a/b > 1$: the
images are squares of side $a/b > 1$ in $[0,a]^2$ with disjoint interiors; the closed
unit square concentric and parallel to each image lies in that image’s interior, so the
$N$ closed unit squares are pairwise disjoint and inside $[0,a]^2$, whence
$\mu([0,a]^2) \ge \sum \mu(Q_j) \ge N$, a contradiction.
This is correct, and the scaling is what makes the singular segment measure safe on
shared edges: the unit squares are disjoint as closed sets, so no segment is counted
twice. The conclusion $s(N) \ge a$ is the statement that no packing has side below $a$,
which is what the theorem claims.

### 2.2 Total mass (§1.3, lines 50–62) and what the structure check decides

With $W = 2+\delta$, $R = 2$, $\alpha = 9/5$ and the corner $C = [0,W] \times [0,R]$,
$\operatorname{area}(C \setminus U) = 2(2+\delta) - (2+\delta - 9/5)(2 - 9/5) = 99/25 + 9\delta/5$.
Each wall carries $k - 4$ periods of mass $9/5$ and the terminal line of mass $m_v$,
each corner the mass $M_C(\delta)$, and the middle is Lebesgue measure on
$[9/5, a - 9/5]^2$. Then
$\mu([0,a]^2) = (a - 18/5)^2 + 4[(k-4)\,9/5 + M_C(\delta) + m_v]$, and with
$S(\delta) = 99/25 + 9\delta/5 - M_C(\delta) - m_v$ one checks
$a^2 - 4S(\delta) - (a - 18/5)^2 = 36a/5 - 324/25 - 4S(\delta) = 36k/5 - 144/5 + 4M_C + 4m_v$,
which is the bracket.
The lane re-derived this and reduced the identity to two affine ones.
In $k$ the two sides are affine with slopes $4 \cdot 9/5$ and $36/5$, equal exactly when
the period mass is $9/5$, which `validate_family.py` requires (line 217); in $\delta$
both sides are affine because every `V` row has $x_l \le 2 + d_0$ (line 68), so its mass
$\rho(2+\delta-x_l)$ is affine and nonnegative on the interval, and `F`, `T` and the
walls carry constant mass.
So the endpoint checks at $k = 7, 8, 9$ (`validate_family.py` lines 337–344, which build
the measure and compare `mass(ss) + (a − 2α)² == a² − 4S`) establish the identity for
every $k \ge 7$ and every $\delta \in [d_0, d_1]$. `structure_all.py` (lines 57–60) then
requires the certified line to be exactly the line through the recomputed $S(d_0)$ and
$S(d_1)$, so $S_i = S$ on $I_i$; §1.1’s “concave and piecewise affine, the chord is a
lower bound” is weaker than what is checked (note N6). Nonnegativity of every row (line
66), axis alignment (line 72) and the reflection, transposition and corner-separation
identities (lines 205–226) complete what the global construction needs to be a
nonnegative measure of the stated mass.

### 2.3 The C4 arrangement and the localization (§2.1–2.3, lines 66–116)

The global measure is one corner, $k - 4$ bottom-wall periods and the terminal line,
rotated by $\rho(x,y) = (a - y, x)$ four times, plus Lebesgue measure on
$U = [9/5, a-9/5]^2$. The lane reconstructed what the left wall looks like near the
origin: it is $\rho^3$ of the top-left corner’s bottom wall, so its periods run upward
from $y = 2$ with the terminal line of that wall at $y = 2$ and the reflected period
above it; the family model’s reflection symmetry (`validate_family.py` line 213) is what
makes that wall read as whole periods with phase 0 at the bottom, and the local `F`
stores exactly that (lines 214–216). `build()` (lines 264–273) is the definition of
$\mu_{k,\delta}$ as far as the proof is concerned, and checks 4a–4c decide, at
$k = 7, 8, 9$ and both endpoints, the mass identity, support inside the container, C4
invariance, equality with the local family on $[0, 24/5]^2$ as a segment measure,
equality of the $k = 7$ and $k = 9$ windows, that periods $n \ge 1$ of the built wall
are the profile, and that the terminal line has phase 0. For $k \ge 10$ the window
content is the same by construction (the three lowest periods of each wall, the corner,
and $U$ cut at $24/5 \le a - 9/5$), which is the “integer shifts” remark of §2.3 (2);
the lane’s program 4 rebuilt the measure for $k = 11$ and found the window identity and
the mass identity hold there too.

The localization, re-derived (the 29 inequalities it uses are decided exactly by program
3):

1. **Rotation.** $\rho$ preserves $\mu$, so a square with centre $z$ may be taken with
   $z \in [0, a/2]^2$.
2. **Global = local on $[0, a/2 + r]^2$**, $r = 7072/10000 > \sqrt2/2$. The lower-right
   corner has $x \ge a - 2$, the top-left corner $y \ge a - W$, the far edges of $U$ are
   at $a - 9/5$, and the terminal line is at $a - 2$; all exceed $a/2 + r$ because
   $a > 2W + 2r$, which at the worst case $k = 7$, $\delta = 1$ has margin $183/625$.
   This is where $k \ge 7$ enters: $k = 6$ fails for $\delta > 2 - \sqrt2$ (the
   specification’s “0.586”, note N7).
3. **Periodic shifts.** If $z_y \ge 2.71$, the square lies above $y = 2$ and meets only
   the left wall and $U$; shifting it by an integer to $z_y \in [2.71, 3.71]$ keeps it
   strictly inside $(2, a - W)$ where the wall is exactly periodic with period 1 and
   inside the $y$-range of $U$, so the mass is unchanged; then either $z_x \ge 9/5 + r$
   and the square sits in $U$ with mass 1, or $z_x < 9/5 + r \le 2.51 + d_1$ and the
   centre is in the left, straddle or top region.
   If $z_y < 2.71$ and $z_x > W + r$, the square lies right of $x = W$ and meets only
   the bottom wall and $U$; the shift to $z_x - \delta \in [2.71, 3.71]$ lands in the
   right region. The remainders of both steps, $z_y \in (2.7072, 2.71)$ and
   $z_x - \delta \in (2.7072, 2.71)$, are inside the straddle and right regions
   respectively.
4. **The four regions** cover $[0, 3.8 + \delta] \times [0, 3.8]$ in original
   coordinates for every $\delta \in [d_0, d_1]$, because the straddle and top regions
   reach $2.51 + d_1 \ge 2.51 + \delta$, where the shifted right region begins;
   `structure_all.py` (lines 61–64) requires exactly these bounds.
   Squares of the left, straddle and top regions stay inside $[0, 24/5]^2$, where global
   = local was decided.
   Squares of the right region do not: in original coordinates they reach
   $x = 4.5072 + \delta$, beyond $24/5$ for $\delta > 0.2928$. What identifies the
   global measure with the right-side family there is route (b) of §2.3 (2): those
   squares lie inside the first three bottom-wall periods ($4.5072 < 5$, so they reach
   neither the terminal line nor the lower-right corner even at $k = 7$), right of the
   left wall ($2.51 - r > 9/5$), and below $a - 9/5$; the periods are the profile by
   check 4c, the right-side family is `T` row for row (line 303), and dropping `F`, `V`
   and the part of $U$ left of $x' = 9/5$ only lowers the mass (§3.3). The proof is
   complete; the sentence of §2.3 (2) that credits the window identity for all four
   regions is the one presentation point the lane would change (finding F4).

### 2.4 Families, poses and regions (§3–4)

The family format, the saving extraction and the right-side and X/Y variants were read
against the code: `load_family_text` (`lib.rs` 640–701), `derive_family_text`
(`replay.rs` 7–31), the structure script’s `decompose` and `saving`. Poses are
parametrized by $u = \tan(\theta/2)$ with $c, s$ rational, the four normals and vertices
as in §4.1, half-width $w(u) = (|c| + |s|)/2$, and the admissible centres
$z_x, z_y \ge w(u)$ (the upper constraints at $20 - w$ are inactive in every region).
The $u$-range $[-13/32, 7/16]$ covers a quarter turn since
$13/32 + 7/16 + 91/512 = 523/512 \ge 1$ is $\tan(\theta_a/2 + \theta_b/2) \ge 1$, and a
quarter turn is enough because the square has fourfold symmetry; `replay4d` decides this
per record (`main.rs` 52–54). The region bounds, the pitch $1/10$ and the $u$ cuts at
$j/32$ ($u = 0$ a cut, never interior) are as §4.2–4.4 say; the lane verified the
product grids of twelve records (§4).

### 2.5 The leaf tests (§5)

Each lemma was re-derived; the lane records here what each one needs.

- **EMPTY, CORE** (`fast.rs` 370–432, `lib.rs` 476–526). The angular core $P$ is the
  intersection of the endpoint half-planes and the chord half-planes, shrunk by the
  support function of the centre box; the core lemma (an intermediate normal is a
  positive combination of an endpoint normal and the chord normal, and the bound
  $\cos(t)/2 \le 1/2$) puts $P$ inside every square of the box.
  $P_T = (P - e_0e_x) \cap (P - e_1e_x) \subseteq P - \delta e_x$ by convexity, $V$ only
  lengthens so $V(e_0)$ is least, and
  $L_U = \max(\operatorname{area}(P \cap U), 1 - \operatorname{area}(O) + \operatorname{area}(O \cap U))$
  bounds $\operatorname{area}(Q \cap U)$ from below because $P \subseteq Q \subseteq O$.
  The Cyrus–Beck clipping and the cell prefilter are exact and never skip a segment that
  meets the polygon.
- **EDGE, EX, EY** (§5.5–5.6, `replay.rs` 63–149). With $z_x \ge \alpha$ the vertical
  cross-section of $Q$ is nondecreasing up to the centre, so the area lost left of
  $x = \alpha$ is at most $h_X\ell(\alpha)$, which a density $\ge \rho_X \ge h_X$ on the
  chord repays; the two losses are overestimated separately, which is safe.
  $D_Y$ is the essential infimum of a sum of indicators in $(x, x - \delta)$; the lane
  checked that the cuts in $x$ at the `T` endpoints $+e_0$, $+e_1$ and at $2 + e_0$,
  $2 + e_1$ make the set of pieces that the sliding window meets constant on each strip,
  so the midpoint evaluation is the exact minimum.
  For EX/EY the side condition is taken on the original family and the base test on the
  variant, whose $U$ is a half-plane, exactly as §5.6 proves.
- **B3D** (§5.3–5.4, `b3d.rs` 1611–1882). For $u \ne 0$ no square edge is parallel to an
  axis, so clipped lengths are continuous and affine on the cells of the arrangement
  whose planes are: a support line meeting a vertex, a density breakpoint meeting an
  edge, the `V` line and its two endpoints, the box faces and the admissibility faces,
  with $\gamma = -l_x$ or $-n_x$ for everything that moves with $\delta$. The lane
  checked the table against the code (lines 1688–1729) and that no other event changes
  the formula: breakpoints are taken where the summed density changes (lines 1264–1274),
  which is exactly where the clipped mass is not affine.
  A plane is pruned only when its sign polynomial is root-free and of one strict sign at
  all eight box corners (lines 1738–1764), so it misses the box for every $u$. Vertices
  are triple intersections; membership uses the ten sign polynomials with $\ge 0$ at a
  sample of each root-free component (lines 1812–1843); `check_value3` evaluates the
  mass symbolically with every comparison guarded, splits at guard roots, and proves
  $(N - \tau D)D \ge 0$ by `nonneg_open` (lines 1539–1593).
- **`nonneg_open`** (lines 1115–1155). The root-free shortcut is a Cauchy-type bound on
  the shifted polynomial and sound; otherwise Yun’s square-free decomposition isolates
  the product of odd-multiplicity factors, any root strictly inside $(A, B)$ rejects,
  and the final sign is taken at a non-root, resampled past even roots.
  Sturm counting is on square-free polynomials throughout, counts roots in $(l, r]$, and
  `roots_open` removes a root at the right end; algebraic endpoints are isolating
  intervals refined on demand, with equality decided through the gcd.
- **B3U, B3T** (§5.7–5.8). For $z_x \ge \alpha$ the lost area
  $g(z_x) = \int_{-\infty}^{\alpha - z_x}\ell$ is convex
  ($g'' = \ell'(\alpha - z_x) \ge 0$ since $\ell$ is nondecreasing on $t \le 0$), so
  $1 - g$ is concave and a concave-plus-affine function on a cell is least at a vertex;
  the two-cut guard $x_0 + y_0 - D_{\mathrm{diag}} \ge 2\alpha$ is exactly
  $\min_{q \in Q}(q_x + q_y) \ge 2\alpha$, since the support of the unit square in the
  direction $(1,1)/\sqrt2$ is $\max(|c|,|s|)/\sqrt2$, so the two cut-off parts are
  disjoint and the quadrant area is $(1 - g_x) + (1 - g_y) - 1$; the `xyh` kinds use
  inclusion–exclusion without the guard.
  For $z_x \le \alpha$ the kept area is convex and lies above its tangent at the box
  midpoint, and the tangent’s slope is the chord length there, which `tangent_term`
  computes as the mass of a density-1 segment (lines 1406–1419).
- **CORE1** (§5.9, lines 2026–2207). For a fixed segment the clipped parameter width is
  $\min(1, \min_i r_i) - \max(0, \max_j r_j)$ with each $r$ affine in the centre (and in
  $\delta$ for `T`), hence concave; for a `V` row the physical clipped length is
  $\min(2+\delta, \min_i e_i) - \max(x_l, \max_j e_j)$ with the $e_i$ independent of
  $\delta$, hence concave in $(z, \delta)$ jointly, and the code’s
  $(t_1 - t_0)\rho(2 + p_\delta - x_l)$ at a corner is exactly that value (lines
  2067–2078). A segment kept only when its width is nonnegative at all eight corners is
  then nonnegative on the whole box, and dropped segments only lower the bound.
  The $U$ terms are concave or affine under the stated hypotheses, so the eight corners
  decide the box; the whole box is admissible by the domain guard (lines 2117–2121).
- **B4U** (§5.11, lines 2306–2525). On a cell the polygon area $g$ is quadratic and
  $\sqrt g$ is concave by Brunn–Minkowski, so $\operatorname{Hess} g$ has at most one
  positive eigenvalue and the minimum of $f = M + g$ over the cell is at a vertex or at
  an interior critical point of an edge, which `edge_runner3` tests on every pair of
  consecutive admissible points along every pair of planes; the chain of components
  covers the $u$-interval from the frontier with the reference `nonneg_open`. The sort
  of the points along an edge is `b3d_sort.rs`, compiled in by `#[path]` (lines
  2450–2454), the one place the lane did not verify (finding F2).
- **Dispatch and failure.** `replay.rs` 167–287 matches exact kind strings, rejects
  $u_0 < 0 < u_1$ for every vertex-type test, and a panic in a leaf is caught and
  counted as a failure (`main.rs` 137); there is no fallback to another kind.

### 2.6 The tiling, the product grid and $u = 0$ (§6)

`tiles` (`main.rs` 24–42) reconstructs a midpoint bisection in the order
$u, \delta, x, y$ and accepts only when every terminal box equals a leaf; equality of
volumes alone is not accepted, and duplicates or displaced leaves fail (its test, lines
180–189). `domain` (lines 47–63) extracts the four interval sets, requires each to
partition the region’s bounds, the $u$-range and $[d_0, d_1]$, requires the root set to
have the product cardinality with no duplicates (equal cardinality suffices because each
root belongs to the product by construction), and forbids $u = 0$ inside any root.
The lane re-decided the product grid for twelve records with its own code and the tiling
by a different route, volume plus pairwise disjointness (§4). At $u = 0$ and on every
box boundary the mass of a closed square is upper semicontinuous in the pose (the upper
limit of indicators of closed sets converging in the Hausdorff sense is at most the
indicator of the limit), so $\mu(Q) \ge 1$ on a dense open set of poses gives it
everywhere, which closes $u = 0$, the guard roots, the determinant roots and the box
faces at once (§6.3).

### 2.7 Acceptance, and how 136 records and 68 families cover every $N$

The acceptance order (§7.1) is: format and nonnegativity, the wall and corner identities
and the savings (`validate_family.py`); the certified line through the endpoint savings
and the region bounds (`structure_all.py`); the product grid, tiling, leaf kinds and
$u = 0$ rule, and every leaf (`replay4d`); the union of regions and the reduction to the
global measure (§2.3, prose plus checks 4a–4c); the interval coverage of $(0,1]$
(`intervals.json`, decided here by program 1). Put together: for each $i$, the family of
$I_i$ gives, for every $k \ge 7$ and $\delta \in I_i$, a measure of mass
$(k+\delta)^2 - 4S_i(\delta)$ with $\mu(Q) \ge 1$ on every closed unit square, so by
§2.1 $s(N) \ge k + \delta$ whenever $(k+\delta)^2 - 4S_i(\delta) < N$. Since every
$\delta \in (0,1]$ lies in some $I_i$ and $S^*(\delta)$ is the largest $S_i(\delta)$
over those, the theorem follows for every non-square $N \ge 49$ at once; no $N$ is
treated individually, and the only use of $N$ is through
$k = \lfloor\sqrt N\rfloor \ge 7$. The open-left intervals cost nothing: the supremum is
the same whether or not $d_0$ belongs to the interval, and the shared endpoints $2/5$
and $99/100$ belong to the interval on their left.

### 2.8 What the checkers assume, and what is asserted but not checked

Hypotheses `replay4d` takes from outside itself: that the family is structurally what
§2–3 say (it drops rows of weight $\le 0$ instead of rejecting them, `lib.rs` 316–322
and 703–710, so nonnegativity is the structure check’s), that `UA = 9/5` and the
standard quadrant are in force (the concavity, tangent and edge lemmas need them, and
the published families carry no `U` field, which `validate_family.py` line 58 refuses),
that the region bounds on its command line are the ones §2.3 (4) requires
(`replay_all.py` passes them from `intervals.json`, and `structure_all.py` checks them),
that the window constant 20 is inactive, and that the mathematics of §5 is right.
It trusts nothing in a record but the boxes and the kind strings.
`validate_family.py` assumes the localization inequalities (its own last line says so),
the correctness of the periodic-shift argument, and that its `build()` is the measure
the proof means.

Steps the source asserts in prose and no program of its own checks, each decided or
re-derived here: the measure principle; the reduction of the mass identity to the
endpoint checks (affineness in $k$ and $\delta$); the inequalities of §2.3 (program 3);
the periodic-shift argument of step (3); the coverage of the remaining centres by the
four regions (program 3); the window content for $k \ge 10$ (re-derived, and rebuilt at
$k = 11$ by program 4); the core lemma, Lemma B3′ and its contact table, the edge,
concavity and tangent lemmas, the CORE1 concavity, and the B4 eigenvalue argument; upper
semicontinuity at $u = 0$; the quarter-turn sufficiency; and the coverage of $(0, 1]$ by
the intervals (program 1). Steps checked by the source’s programs that the lane did not
reproduce: every leaf of every record, the tiling of every root, and the structure of 62
of the 68 families (the intake lane ran the source’s structure check on all 68; the lane
re-derived interval 20’s two with its own code).

## 3. Trust Boundaries

| Checker | Decides | Trusts | Shares with |
| --- | --- | --- | --- |
| `replay4d` with `seam4d_core` (Rust, exact GMP rationals and real algebraic numbers) | For one record: the product grid, the tiling of each root, the $u = 0$ rules, and every leaf by its named test against the family it is given | The family’s structure and nonnegativity; the region bounds; the mathematics of §5; its own 2,617-line arithmetic, of which the lane read the whole and verified the sound direction of every shortcut it found | `seam4d_core` is the producer’s own leaf evaluator (README lines 100–102): the replay is the producer’s code re-run; `b3d_sort.rs` is a port of CPython’s sort |
| `structure/validate_family.py` via `structure_all.py` (Python, exact) | The family format, nonnegativity, wall and corner identities, the saving at both ends, the mass identity and local agreement at $k = 7, 8, 9$, the right-side derivation; the line through the endpoint savings; the region bounds | The localization inequalities and the periodic-shift argument; that endpoint identities extend (true by affineness) | Nothing with `replay4d`; both read the same family bytes and `intervals.json` |
| `a_of_n.py` (Python, exact comparisons by integer square roots) | What the theorem implies at a count, from `intervals.json` | The theorem; the closed form of §1.1 | Nothing but `intervals.json` |
| `evaluation/closed_form_bounds.py` (this project, intake lane) | The same, by two routes, against the case records | The theorem; the packet manifest’s digests | `intervals.json` and the case records; written after reading `a_of_n.py`, in a file of its own |
| The five programs of §4 (this lane) | What each says in §4; a sample of the claim on three intervals | The theorem’s statement and SPEC.md’s definitions; the packet manifest; `ASSET.json` | Nothing of the source’s code; the same bytes |

What any two share: the family bytes, `intervals.json` and the release assets; the
mathematics of SPEC.md, which every checker, the source’s and this lane’s, takes as
specification; and, for the two Python evaluators and this lane’s programs, the same
system family as the source’s commit names as co-author.
No deciding program of the certificate exists outside the producer’s code base.

## 4. What the Lane Tested

All programs are under `review/`, documented in its
[README](../../../packing/resources/web/wand125-closed-form-2026-10-14/review/README.md),
run with Python 3.14.7 (`python -I`) on one worker of a four-core host shared with other
agents, and their receipts are under `review/outputs/`.

| Program | Reads | Decides | Printed |
| --- | --- | --- | --- |
| `a_of_n_by_definition.py` | `intervals.json` (digest-checked), the retained `a_of_n.py` output, the intake receipt | $a(N)$ for 3,498 non-square $N \le 3600$ from the supremum alone, by bisection on each interval and exact separation of the candidates, with no closed form and no square root; the interval facts | Every 30-place value of the source’s `a_of_n.py` and of the intake evaluation satisfies $v \le a(N) < v + 10^{-30}$; the attaining interval agrees at all 3,498; 234 counts hit a cap $k + d_1$; the intervals cover $(0,1]$, no $j/5$ is interior, $\max\alpha_i < 1.7496$, the least margin over $\delta/2$ at $\delta \ge 1/50$ is $0.0226439\ldots$ on $I_2$, $S^*(1) = 0.8528498\ldots > 3/4$; 10 s |
| `record_consistency.py` | the enclosures above, the front matter of `n-049.md` to `n-324.md` | $a(N)$ against the four lanes of 264 case records, and the known values | Above no upper bound; equal to the verified upper bound at the 33 proved counts $m^2 - 1, m^2 - 2, m^2 - 3$, $m = 8..18$, where $a(N) = m$ exactly; below $m$ at the eleven $m^2 - 4$; above the reported lower bound at 156 and the verified one at 189, equal at 33, below at 75 and 42, the intake’s counts; $a(N) \le k + 1$ everywhere and nondecreasing in $N$; 2 s |
| `localization_checks.py` | `intervals.json` | The 29 inequalities of §2.3, §4.1 and §5.1 listed in its docstring, exactly | All 29 hold; the worst margin of $a/2 + r < a - W$ is $183/625$ at $k = 7$, $\delta = 1$; $k = 6$ holds at $\delta = 0.585$ and fails at $0.586$; under 1 s |
| `replay_receipt_pieces.py` | `receipts/replay.json`, `families.json`, `published_checker.json`, `intervals.json`, all digest-checked | The internal arithmetic of the source’s replay receipt and its digest chain to the published files | The 158 pieces of the 25 cut records tile their regions, their roots and line-hash sums add up, 269 runs and 4,294.08 CPU-hours add up, every record digest in the receipt is the published record’s, every family digest is `families.json`’s old digest whose new digest is `intervals.json`’s, and the published build’s eight runs name the published digests with matching counts and kinds; under 1 s |
| `family_probe.py` | interval 20’s unpacked asset in scratch, `intervals.json` | For that interval: the family structure and savings from SPEC.md with its own decomposition; the global measure built here for $k = 7, 8, 11$ at four $\delta$; the product grid, counts and kinds of its four records, the volume of every root and the pairwise disjointness of the leaves of every top root and 200 roots of each other record; the exact mass of the global measure at 1,345 admissible poses | Every structure check passed: period mass $9/5$, reflection symmetry, six repeated periods on each wall, nonnegative corner remainders in place, $S(d_0) = 0.48018551\ldots$ and $S(d_1) = 0.47919140\ldots$ equal to the stored values and to the certified line, above $\delta/2$; the right-side family is `T` row for row; all twelve global builds pass the mass identity, the support and the window identity (1,056 to 1,460 segments); the records have 10,584, 17,442, 4,158 and 13,338 roots over grids of $14 \times 28$, $17 \times 38$, $14 \times 11$ and $13 \times 38$ cells by 27 $u$-pieces and one $\delta$-piece, 832,232 leaves of the published kinds and counts, every root tiled; the least exact mass over 1,345 poses is exactly 1, at a random pose with $k = 7$; the local family’s mass equalled the global one at all 679 poses in the left, straddle and top regions, and the right-side family’s mass never exceeded the global one at 348 poses in the right region; 174 s. `FAMILY PROBE OK` |

The probe was not completed on intervals 7 and 34, so nothing is recorded for them; the
receipt of interval 20 is `review/outputs/probe-20.json`.

## 5. The Three Places the Intake Flagged, and the Digest Mismatch

**`B3_PLAIN_RF`** (`b3d.rs` 499–505, used at 558–670). The variable selects, for
rational-function addition, multiplication and division, between Henrici’s route (cancel
$\gcd(d_1, d_2)$ first, then $\gcd(n, g)$; for products cancel $\gcd(n_1, d_2)$ and
$\gcd(n_2, d_1)$) and the plain route (form the product or sum, reduce by the full gcd).
The lane verified the identities the fast route relies on: for reduced inputs with monic
denominators, $\gcd(n_1 d_2/g \pm n_2 d_1/g,\ d_1 d_2/g) = \gcd(n, g)$ and
$\gcd(n_1 n_2, d_1 d_2) = \gcd(n_1, d_2)\gcd(n_2, d_1)$, so both routes return the
unique reduced form with monic denominator.
Only the value and the guard polynomial $n \cdot d$ enter any decision, and an unreduced
guard would only add roots to split at.
Soundness does not depend on the setting.
What depends on it is reproducibility of the trace, and no receipt records which setting
ran (F3).

**The gcd shortcut** (`b3d.rs` 411–495). `modp_coprime` reduces both integer polynomials
modulo one of three primes near $2^{31}$ that divides neither leading coefficient,
computes the modular gcd, and returns “coprime” when its degree is 0. This is sound: if
$h = \gcd(a, b)$ over $\mathbb{Q}$ had positive degree, its primitive integer form
divides $a$ and $b$ in $\mathbb{Z}[x]$ (Gauss), its leading coefficient divides
$\operatorname{lc}(a)$, so $h \bmod p$ keeps its degree and divides the modular gcd,
which then has positive degree.
A prime that divides a leading coefficient returns `None` and the next prime is tried;
three failures fall back to the primitive Euclidean sequence.
The shortcut can only say “coprime” when it is true; it never reports a false common
factor, and under-reduction never arises.
The 64-bit arithmetic is within range ($p < 2^{31}$, products below $2^{62}$).

**`b3d_sort.rs` outside the source hash** (`main.rs` 64–78, SPEC.md §9.4 line 641). The
file is compiled into `seam4d_core` (`b3d.rs` 2450–2451) and is the comparison sort of
the points along an arrangement edge in the B4U edge stage (line 2428); the edge stage
takes consecutive pairs of the sorted list, so an incorrect order could skip an edge
segment. The printed source hash, and therefore the receipt’s `306ad4b5…` for the full
replay and `92002e0e…` for the published build, does not identify this file; the packet
manifest pins the published one (`23be1db0…`). The exposure is the 113 B4U leaves of 187
million, all in left regions, and the file is a line-by-line port of CPython’s powersort
with the comparator made fallible so that guard recording follows Python’s order.
The lane did not transliterate and test it; it recommends including the file in the hash
and verifying the output order with the same guarded comparator after the sort, which
can only add guards (F2).

**The `validate_family.py` digest.** `receipts/structure.json` line 4 names
`fdd61866ca18…`; the published script is `22e55f17f29a…`, and the upstream history of
the file is the single commit `eb0fd19` (checked read-only on GitHub), so the revision
the receipt names was never published.
The published script passed on all 68 families here (the intake’s run, receipts under
`receipts/structure-check/`, with the same 680 checks and the same results as the
source’s receipt), so the discrepancy is one of provenance: the author ran an earlier
revision, edited the script before committing, and did not rerun (F1).

## 6. Findings

Graded blocking, major, minor or note; none is blocking or major.

- **F1, minor.** `CF/receipts/structure.json` line 4 names `validate_family.py` by a
  digest (`fdd61866…`) that is not the published file’s (`22e55f17…`), and the file has
  one upstream commit, so the receipt’s script cannot be recovered.
  The published script was run here on all 68 families with identical results.
  Rerun `structure_all.py` with the published script and republish the receipt.
- **F2, minor.** `CF/checker/replay4d/src/main.rs` 64–78 and SPEC.md line 641: the
  source hash omits `seam4d_core/src/b3d_sort.rs`, which `b3d.rs` 2450–2451 compiles in
  and whose correctness the B4U edge stage (2426–2445) needs.
  Include it in the hash; add a post-sort order check with the guarded comparator.
- **F3, minor.** `CF/checker/seam4d_core/src/b3d.rs` 499–505: `B3_PLAIN_RF` selects the
  arithmetic route from the environment and the summary JSON (`main.rs` 162–164) does
  not record it. Record the setting in the summary, or remove the switch from the
  published checker.
- **F4, minor (presentation).** SPEC.md §2.3 (2), line 101, says every checked square
  stays inside $[0, 24/5]^2$ in local coordinates; in original coordinates the right
  region’s squares reach $x = 4.5072 + \delta$, so the identification there rests on
  route (b), the wall-period and terminal checks 4c of `validate_family.py` 349–364,
  which do hold. Say which route carries the right region.
- **N5, note.** SPEC.md §1.1 line 31: “concave and piecewise affine … the chord is a
  lower bound”. $S$ is affine on each interval (every `V` row has $x_l \le 2 + d_0$) and
  `structure_all.py` 57–60 requires the certified line to equal it; the weaker sentence
  invites a reader to look for a concavity argument that is not needed.
- **N6, note.** SPEC.md §2.3 (5)(i), line 116: “$k = 6$ fails when $\delta > 0.586$”;
  the threshold is $2 - \sqrt2 = 0.5858\ldots$, or $2(1 - r) = 0.5856$ with the bound
  $r = 7072/10000$ the proof uses.
- **N7, note.** `CF/checker/seam4d_core/src/lib.rs` 316–322 and 703–710: rows of weight
  $\le 0$ are dropped, not rejected, as README lines 93–95 say.
  The identification of the replayed measure with the one whose mass §1.3 computes
  therefore rests on the nonnegativity check of `validate_family.py` line 66; a checker
  that rejects such rows would remove the dependence.
- **N8, note.** SPEC.md §1.1 lines 17–19: the “consequently” needs the supremum’s set to
  be nonempty, which holds because $\beta_1 = 0$ and $k^2 < N$; worth one clause.
- **N9, note.** `CF/receipts/replay.json`: the family digests are those of the
  pre-cleanup families; `families.json` maps them to the published ones and says the
  difference is two unread keys, which the lane could not verify without the old files
  (the chain of digests is consistent, program 4). The published build’s replay of
  intervals 1 and 34 with the published families is the only replay of published family
  bytes.
- **N10, note.** `CF/README.md` lines 110–115 and `replay.json`: 25 of the 136 records
  were replayed as 158 pieces over sub-boxes; the receipt records each piece’s bounds
  and the lane verified they tile the regions, so each centre of those regions is
  covered by a replayed piece, which is what the theorem needs; the product-grid check
  ran per piece, and the uncut published record as a whole was checked only for
  intervals 1 and 34.
- **N11, note.** `CF/a_of_n.py` 54–66: `greater()` separates two roots by refining to
  $10^{4000}$ and raises otherwise; the lane’s program separates exactly and found no
  tie at any count to 3,600.

## 7. Questions for the Author

1. Which revision of `validate_family.py` produced `receipts/structure.json`, and what
   changed before publication?
   Would you rerun it and republish the receipt (F1)?
2. Why is `b3d_sort.rs` outside the source hash?
   Would you include it, and add an order check after the sort (F2)?
3. Under which setting of `B3_PLAIN_RF` did the full replay and the published-build
   replay run, and would you record the setting in the summary JSON (F3)?
4. For the right region, is route (b) of §2.3 (2), the wall-period and terminal checks,
   the intended justification of global = local (F4)?
5. Do the families used for the full replay survive anywhere public, so that
   `families.json`’s statement (two unread keys removed) can be verified from bytes?
6. Were the 158 pieces of the cut records produced by cutting the published records
   along grid lines, and is the cutting tool available?
   The receipt lets a reader verify the tiling and the root counts, not the lines.
7. Is a checker of the leaf tests that shares nothing with the search tools planned?
   The source says one would be welcome; §3 of this review is written to help a second
   implementer, and the lane would start from the contact table of §5.3 and
   `nonneg_open`.

## 8. What the Rung Table Can Say

The result is reported: the evidence the records lane will cite is the source’s public
claim with its own receipts, `assurance: reported`, `replay_status: not-attempted`.

- **V stays `V0`** on this review.
  `V3` needs an evidence entry with a certificate, a replay command and a passing replay
  status; the source’s receipts are the producer’s statement, and no replay has run
  here. A complete replay of the 136 records by `replay4d`, from the retained crates with
  the locked `Cargo.lock`, is what moves it (4,294 CPU-hours by the source’s receipt,
  about 67 hours on 64 dedicated cores).
- **C moves from `C0` to `C1`** when this review is recorded as the entry’s
  `external_review` with the state `informally-verified`: a qualifying read that found
  no defect blocking the claim.
  `C3` needs the complete replay; `C4` needs a second adversarial review by a distinct
  reviewer and a human oversight record.
- **What a replay here would be.** Reproduced with the producer’s code
  (`same-implementation`), since `seam4d_core` is the search tools’ leaf evaluator; it
  rules out a lost, altered or machine-dependent result and nothing in the code.
  An independently written checker of the leaf tests would be the second route beside
  the rung; none exists.
- **The sample checks of §4 set no rung.** They are recorded so that a reader knows the
  claim survived an independent attempt to refute it at a few thousand poses and on
  three of 34 families, and that the closed form, the localization and the receipt
  arithmetic are right.

The verified lane of the 189 case records that $a(N)$ exceeds should not move on this
review alone; the reported lane may take $a(N)$ as the register plan proposes.

## 9. Proposed Verifier Entries

For `packing/frontier/verifiers.yaml`, written here and not applied; the records lane
takes them with the review.
All five are first-party, written by this lane after reading the mathematics, the proof
text, the specification, the certificate format and the producer’s code, in files that
import none of it, with the system family the source’s commit also names.

```yaml
- id: V-closed-form-review-a-by-definition
  program: review/a_of_n_by_definition.py
  author: Squares Project (Levy)
  provenance: first-party
  language: [Python]
  methods: [exact-algebraic]
  role: premises
  summary: >-
    Encloses a(N) from the supremum of SPEC.md section 1.1 alone, by exact bisection on
    each interval and exact separation of the candidates, at every non-square count to
    3600, and decides the interval facts the corollaries use; compares the 30-place values
    of the source's a_of_n.py and of the intake evaluation.
  source:
  - packing/resources/web/wand125-closed-form-2026-10-14/review/a_of_n_by_definition.py
  versions:
  - {sha256: 6e7ed56592d13c25446f6bd76d1634b9532fef5ec0ca8acb2a8ebaa135bb0ad1}
  independence_record: packing/resources/web/wand125-closed-form-2026-10-14/review/README.md
  independence:
    read: [mathematics, proof-text, specification, certificate-format, producer-code, producer-output]
    clean_room: false
    shares: []
    written_by:
    - kind: ai
      system: Claude (Anthropic)
      setting: the mathematical review lane of the wand125-cf import (think-tsox), strong tier, max reasoning
    overlaps_producer:
      extent: system-family
      separate_prompt: true
      separate_code: true
      note: >-
        The source's commit names Claude Opus 5.5 as co-author. Written by a Claude agent
        in a lane prompted separately from the source and from the intake lane, in a file
        of its own that imports none of the source; its author had read SPEC.md, README.md,
        a_of_n.py and the checker first.
  note: It decides what the theorem implies at a count and nothing about the certificate.
- id: V-closed-form-review-record-consistency
  program: review/record_consistency.py
  author: Squares Project (Levy)
  provenance: first-party
  language: [Python]
  methods: [exact-algebraic]
  role: premises
  summary: >-
    Compares the enclosures of a(N) with the four lanes of the case records n = 49..324
    and with the known values at m^2 - 1, -2, -3 and -4: a lower bound above a recorded
    upper bound, or above a known value, would refute the claim.
  source:
  - packing/resources/web/wand125-closed-form-2026-10-14/review/record_consistency.py
  versions:
  - {sha256: a0fc92993452d20da1b9f36e3890c39acf3cce54f7e6598b4b6887266562a0ae}
  independence_record: packing/resources/web/wand125-closed-form-2026-10-14/review/README.md
  independence:
    read: [mathematics, proof-text, specification, producer-output]
    clean_room: false
    shares: []
    written_by:
    - kind: ai
      system: Claude (Anthropic)
      setting: the mathematical review lane of the wand125-cf import (think-tsox), strong tier, max reasoning
    overlaps_producer:
      extent: system-family
      separate_prompt: true
      separate_code: true
      note: As above; it reads the case records through PyYAML and the enclosures of the first program.
  note: A consistency check that can refute and cannot establish.
- id: V-closed-form-review-localization
  program: review/localization_checks.py
  author: Squares Project (Levy)
  provenance: first-party
  language: [Python]
  methods: [exact-algebraic]
  role: premises
  summary: >-
    Decides exactly the 29 numerical inequalities that SPEC.md sections 2.3, 4.1 and 5.1
    assert in prose and no program of the source checks: corner and edge reach for
    k >= 7, the periodic-shift ranges, the window containment of the checked regions, the
    coverage of [0, 3.8 + delta] x [0, 3.8] by the four regions, the quarter-turn
    condition on the u-range, the half-width bound, the window premise and the slopes.
  source:
  - packing/resources/web/wand125-closed-form-2026-10-14/review/localization_checks.py
  versions:
  - {sha256: b3bbe6413b6e3dae0ab2a0cf1a2eb3c04cb4ff0c0c41e8baf04623ab96c4894a}
  independence_record: packing/resources/web/wand125-closed-form-2026-10-14/review/README.md
  independence:
    read: [mathematics, proof-text, specification]
    clean_room: false
    shares: []
    written_by:
    - kind: ai
      system: Claude (Anthropic)
      setting: the mathematical review lane of the wand125-cf import (think-tsox), strong tier, max reasoning
    overlaps_producer:
      extent: system-family
      separate_prompt: true
      separate_code: true
      note: As above; the inequalities are the specification's, decided from its constants.
  note: These are premises of the proof that the structure check leaves to the specification.
- id: V-closed-form-review-replay-receipt
  program: review/replay_receipt_pieces.py
  author: Squares Project (Levy)
  provenance: first-party
  language: [Python]
  methods: [exact-algebraic]
  role: premises
  summary: >-
    Checks the source's replay receipt against itself and the published files: the 158
    pieces of the 25 cut records tile their regions, root counts and line-hash sums add
    up, run and CPU-hour totals add up, and every record and family digest chains to
    intervals.json through families.json and the published-build receipt.
  source:
  - packing/resources/web/wand125-closed-form-2026-10-14/review/replay_receipt_pieces.py
  versions:
  - {sha256: 3da9b960c45e589150cdc42407683744dd6eb42ebcadbf931da48ee0a5156c96}
  independence_record: packing/resources/web/wand125-closed-form-2026-10-14/review/README.md
  independence:
    read: [specification, certificate-format, producer-output]
    clean_room: false
    shares: []
    written_by:
    - kind: ai
      system: Claude (Anthropic)
      setting: the mathematical review lane of the wand125-cf import (think-tsox), strong tier, max reasoning
    overlaps_producer:
      extent: system-family
      separate_prompt: true
      separate_code: true
      note: As above.
  note: A receipt is the author's statement; this decides only that it is consistent and names the published files.
- id: V-closed-form-review-family-probe
  program: review/family_probe.py
  author: Squares Project (Levy)
  provenance: first-party
  language: [Python]
  methods: [exact-algebraic]
  role: premises
  summary: >-
    For one released interval: re-derives the family's structure and savings from
    SPEC.md with code of its own, builds the global measure for several k and delta and
    decides the mass identity, the support and the window identity, re-decides the product
    grid and the tiling of the four region records by volume and pairwise disjointness,
    and computes the mass of the global measure on closed unit squares exactly at random,
    delicate and descent-found poses, which must be at least 1.
  source:
  - packing/resources/web/wand125-closed-form-2026-10-14/review/family_probe.py
  versions:
  - {sha256: bb7a9d1df6d971964752e673230f088755792edced0dff7f6c571974863398b6}
  independence_record: packing/resources/web/wand125-closed-form-2026-10-14/review/README.md
  independence:
    read: [mathematics, proof-text, specification, certificate-format, producer-code, producer-output]
    clean_room: false
    shares: []
    written_by:
    - kind: ai
      system: Claude (Anthropic)
      setting: the mathematical review lane of the wand125-cf import (think-tsox), strong tier, max reasoning
    overlaps_producer:
      extent: system-family
      separate_prompt: true
      separate_code: true
      note: >-
        As above. Its author read validate_family.py and the checker before writing it, and
        ran validate_family.py once on one family to compare decompositions while fixing a
        clipping bug of its own; the structure and savings code is written from SPEC.md
        sections 2.1 and 3.2 and shares no line with the source.
  note: >-
    A sample: it ran to completion on interval 20 of 34, with 1,345 poses, and its runs on
    intervals 7 and 34 were stopped before a receipt was written. It decides the structure
    of interval 20's two families and the grids of its four records fully, the tiling of
    its top record fully and of the other three on 200 roots each, and the claim itself
    only at the poses it visited.
```

## 10. Comparison With Earlier Reviews

No earlier review of this result exists in the record or was found; the intake README
and the register plan were read, as the brief directs, and are not reviews.
Nothing was seen first that this review had to disclose.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
