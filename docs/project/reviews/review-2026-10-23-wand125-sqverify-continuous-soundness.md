# Soundness Review: wand125’s `sqverify_continuous`, v3 and v4

Reviewed 2026-10-23 from the two packets retained that day,
[`wand125-sqverify-continuous-v4-2026-10-12`](../../../packing/resources/web/wand125-sqverify-continuous-v4-2026-10-12/README.md)
(the tree at `d4a1981`) and
[`wand125-sqverify-continuous-v3-2026-10-12`](../../../packing/resources/web/wand125-sqverify-continuous-v3-2026-10-12/README.md)
(the tree at `f30cc2c`), by an AI agent: Claude (Anthropic), the stage 4 validation lane
`c-review-sqvc-1023` of the 23 October 2026 intake pass (think-xzob, epic think-ezt8),
tier `tbd-strong-max`, maximum reasoning, prompted separately from the lanes that
imported T-145, T-157 and T-192 and from the reviews of those results.
The lane worked in a worktree of its own and read the source as data.
The only programs it ran that it did not write are the verifier itself, built from the
retained source, and the verifier’s own test suite: about 7 CPU-minutes in all, under
the 2 CPU-hour ceiling its brief set, and no complete run of any claim.
Everything else it ran it wrote; the programs and their receipts are in the v4 packet’s
[`review/`](../../../packing/resources/web/wand125-sqverify-continuous-v4-2026-10-12/review/README.md).
Nothing was posted and the author was not contacted.

What it saw before writing §§1 to 9: the bead think-xzob’s description, the brief, the
register entries of T-145, T-157 and T-192 (their claims, compositions, next steps and
the `scope` lines of their `reviews` items), the registry entries of the release’s two
kernels, of this verifier and of `contpose_check3`, the `external_review` notes of
`E-n040-guzhou-continuous-pose-report` and `E-n040-guzhou-new-supports-report` (which
name the earlier reviews’ findings GC-1 to GC-8 and GN-1 to GN-8 by title), the n = 28
packet’s README, and the opening of the 14 October review of wand125’s fine-net bounds,
which says that review read the same 34 lines of `certificate.rs` (§3.8). It did not
open Guzhou0806’s `continuous_pose.cpp` or any earlier review document until those
sections were written; §10 compares them.

## Summary for the Author

`sqverify-fast --continuous` claims that every closed square of side $B$ in
$K = [0, L]^2$, at every centre and every angle, captures at least $\tau$ of a
D4-symmetrized rectangle density, checks $n\tau > M$ exactly, and concludes
$s(n) > L/B$. This review re-derived the argument, lemmas C1 to C6 of `CONTINUOUS.md`
and the counting step, from the source, and read every line of `src/slab.rs`, the
continuous path of `src/main.rs` and the admission in `src/certificate.rs` it depends
on, against this repository’s copies of the modules the mode reuses.
**No step is false, and no finding is blocking or major.** The bound each box accepts is
a valid lower bound on the capture at every pose of the box, every coordinate of the
search is covered, and acceptance compares a downward bound with the upward enclosure of
$\tau$.

Beyond reading, it checked the code three ways, all with programs it wrote.
A Python transcription of the box bound, held to an exact rational oracle of its own on
adversarial boxes and rectangles, found no failure in 3.4 million checks at 17,280
sampled poses, and it detects 9 of 10 deliberate errors put into the transcription
(§8.1). The build reproduces the binary the 15 October import built (`31936c4d…`), and
the crate’s 36 tests pass.
And v4, run here on the source’s own controls, reproduces the source’s v3 rows node for
node (7,714, 5,979 and 12,364,148 nodes) and the n = 28 control log root by root, with
every refusal witness re-evaluated here in exact arithmetic (§8.2).

Two findings are minor.
`--resume` counts root lines taken from a file whose key anyone can compute (SC-1), so a
replay here must not resume from any output but its own; and the y-derivative enclosure
has no test, though the x one does and the two take different code paths (SC-2). The
rest are notes, among them two facts the record needed: T-192’s certificate is format M
and declares the standard net as `proof_net`, so its admission does pass through your
`proof_net` branch, which is inert for this mode (SC-8); and your n = 40 runs publish no
receipt, so they are a report until a replay here (SC-11).

For the record: the mode is independent code with the same method as Guzhou0806’s
kernel, and it shares this repository’s interval, exact, axis and oracle modules byte
for byte. A complete replay here would make T-145’s and T-157’s continuous cover
independently re-implemented after reading the producer’s code, and change no rung; for
T-192 it is route A, reproduced with the producer’s code.
Neither replay has run (§9).

## 1. The Claim and the Results It Bears On

**The mode’s theorem.** Let $\mu$ be the certificate’s measure: each positive row’s
weight spread uniformly over its eight images under the symmetries of $K$, so that $\mu$
is $D_4$-invariant, absolutely continuous and of total mass $M$. Let $0 < A \le B$,
$0 < \varepsilon < T \le 1/2$ with $T^2 + 2T - 1 > 0$ and
$\varepsilon^2 + 2\varepsilon - 1 < 0$, $L^2 > 2B^2$, $A\,W(\varepsilon) \le B$ and
$n\tau > M$, all exact.
If every root range of $t = \tan(\theta/2)$ in $[\varepsilon, T]$ is verified and the
axis patch is verified, then every closed square of side $B$ in $K$ captures
$\mu(P) \ge \tau$, and so $s(n) > L/B$.

| Result | Certificate | $B$ | $\tau$ | $X = L/B$ | Role of this mode | Version the source ran |
| --- | --- | --- | --- | --- | --- | --- |
| T-145 | Hosono’s rect_n40_L67 (480 orbits, $M = 3999/100$) | $199529/200000$ | $4999/5000$ | $1340000/199529$ | a second route beside the producer’s kernel | v3, reported VERIFIED, no receipt |
| T-157 | Guzhou0806’s 685-orbit density ($M = 3999/100$) | $3350/3359$ | $4999/5000$ | $3359/500$ | the same | v3, reported VERIFIED, no receipt |
| T-192 | continuous_n28_L5745 (884 orbits, $M = 2799999/100000$) | $499/500$ | $1$ | $1149/200$ | route A, the producer’s own checker | v4, VERIFIED, log in the release asset |

## 2. Custody: What Was Read, Built and Run

The two revisions are the only commits that touch `tools/sqverify_continuous`, both on
12 October 2026: `f30cc2cf345a3a3f6af778925f354d9ec979868b` (01:00:19Z, v3) and its
child `d4a19815e2b0cca5faa562f00c7a80b93d3402ef` (01:29:29Z, v4). The v4 tree (Git tree
`2734b434…`) is unchanged at `8530baf`, the n = 28 pin, and at the head `e48de243` read
on 23 October. This review’s
[custody receipt](../../../packing/resources/web/wand125-sqverify-continuous-v4-2026-10-12/review/receipts/custody.json)
records the following, each measured rather than taken from the source:

- **Source digests by `build.rs`’s rule**: v3 `1266a8b9…1f33`, v4 `619b3c00…c7f5`, the
  values `PROVENANCE.md` prints and every summary embeds.
- **What changed from v3 to v4**: `CONTINUOUS.md`, `src/main.rs`, `src/slab.rs` and
  `src/slab_tests.rs`. In `slab.rs` only `Params` and `run` changed, and `run_key` and
  `inherited` were added; `run_root` and every function it calls are the same text.
- **The patch**: `patches/continuous.diff` applied to wand125’s
  `tools/fine_net_verifier/sqverify_fast` reproduces the crate byte for byte at both
  revisions, and the five files `PROVENANCE.md` lists are the only ones that differ.
- **Against this repository’s `packing/sqverify_fast`**: `axis.rs`, `exact.rs`,
  `interval.rs`, `oracle.rs` and `rotated.rs` have the same Git blobs at `dee22b88`,
  `910b6b12c` and `origin/main`; `certificate.rs` (`1bbefbd8`) differs from all three
  (§3.8); `lib.rs` and `main.rs` differ from their `dee22b88` copies by the mode alone.
- **The n = 28 asset**: `check1/src/sqverify_continuous_v4.tgz` (`72086975…`) unpacks to
  the `d4a1981` tree byte for byte; the asset itself matched its pin (912,977 bytes,
  `d7249d0d…`) when fetched to scratch.

**Build.** `cargo build --release --locked` with rustc 1.98.0, the toolchain the crate
pins, gave the binary
`31936c4dcfac398b729990f51820fd5a5b70e23a2e809b71de1ca5864e6de618`, the digest the 15
October import recorded for its own build (34 CPU-seconds).
`cargo test --release --locked` passed 17 unit tests (the four slab tests among them)
and 19 adversarial tests (85 CPU-seconds).

**Runs of the verifier**, every one small: three toy runs on a uniform density, the
source’s three n = 40 controls on candidates this review built from this repository’s
copies of the densities, and the n = 28 control from the asset; 275 CPU-seconds in all
(§8.2).

## 3. The Argument, Re-derived

Line numbers are v4’s. In `slab.rs`, a v3 line from 74 to 672 is the v4 line minus 4.
The code is read as written; the soundness of the reused modules is the 3 October
reviews’ (lemmas I1, F3, A1 and A2 of `SOUNDNESS.md`), and §4 says what that leaves
trusted.

### 3.0 The Counting Step and the Endpoint

Suppose $n$ unit squares with disjoint interiors fit in a square of side $L/B$. Scaling
by $B$ gives $n$ closed squares $P_i$ of side $B$ in $K$ with disjoint interiors.
Each captures $\mu(P_i) \ge \tau$, and since $\mu$ is absolutely continuous their
boundaries are null, so $n\tau \le \sum_i \mu(P_i) \le \mu(K) \le M$, against
$n\tau > M$. Points and segments of a format L file are dropped from the capture and
kept in $M$; dropping nonnegative mass only lowers each $\mu(P_i)$, so the inequality
survives. $s(n)$ is attained, so a packing in side exactly $L/B$ would also fit, and the
bound is strict.

Hypotheses and where they are established: $n\tau > M$ in exact rationals
(`slab.rs:115`); $M$ is the exact sum of every weight, points and segments included, and
`total_mass`, when present, must equal it (`certificate.rs:652`, `714–718`); weights are
nonnegative (`649`); $0 < M < n$ (`719–723`). The summary prints the claim $s(n) > L/B$
only when the status is `VERIFIED` (`slab.rs:854`).

### 3.1 C1: Reduction by Symmetry

**Statement.** It suffices to check $\theta \in [0, \pi/4]$, i.e.
$t \in [0, \tan(\pi/8)]$, and centres $x = L/2 + uE(t)$, $y = L/2 + vE(t)$ with
$(u, v) \in [0, 1]^2$, where $c = (1 - t^2)/(1 + t^2)$, $s = 2t/(1 + t^2)$, $W = c + s$
and $E(t) = L/2 - (B/2)W(t)$.

**Derivation.** A square’s angle matters modulo $\pi/2$. The reflection
$x \mapsto L - x$ maps axes $(\cos\theta, \sin\theta)$ to
$(\cos(\pi - \theta), \sin(\pi - \theta))$, so angle $\theta$ to $-\theta$ modulo
$\pi/2$; this brings every angle to $[0, \pi/4]$. A quarter turn about $(L/2, L/2)$ adds
$\pi/2$ to the angle, which changes nothing, and some power of it carries any centre
into the closed quadrant $x, y \ge L/2$. Both maps preserve $K$, and $\mu$ is invariant
under all eight symmetries, so captures are equal.
At $\theta \in [0, \pi/2]$ the square’s bounding box has half-side $(B/2)W$, so the
square lies in $K$ exactly when $|x - L/2|, |y - L/2| \le E(t)$. $W \le \sqrt 2$ and
$L^2 > 2B^2$ give $E > 0$ at every angle.

**In the code.** $D_4$ invariance: `d4_images` lists the eight images
(`certificate.rs:427–448`), and each row’s weight is split into eight shares, each image
receiving one, with coinciding images merged by exact key (`656–673`); the multiset of
images of a row is invariant under every symmetry, so the sum is.
$L^2 > 2B^2$: `slab.rs:97`. The search covers $t \in [\varepsilon, T]$ with
$T > \tan(\pi/8)$ (`slab.rs:103`); the part above $\tan(\pi/8)$ is redundant and only
costs time.

### 3.2 C2: Angle Enclosures

**Statement.** For a box $t \in [t_a, t_b] \subset [0, 1/2]$, `angles` returns intervals
$C \ni c(t)$, $S \ni s(t)$ and $\mathcal W \ni W(t)$ for every $t$ of the box.

**Derivation.** On $[0, 1]$, $c$ decreases and $s$ increases.
$W'(t) = -2(t^2 + 2t - 1)/(1 + t^2)^2$, so $W$ increases up to $\sqrt 2 - 1$ and
decreases after; its minimum over an interval is at an end, and its maximum is at the
end nearer $\sqrt 2 - 1$ when the interval lies on one side of it, and
$W(\sqrt 2 - 1) = \sqrt 2$ otherwise.

**In the code** (`slab.rs:165–201`). $c$: lower end $c(t_b)$ from a downward numerator
$1 - t_b^2$ over an upward denominator, upper end $c(t_a)$ the reverse (`168–169`); both
numerators are positive for $t \le 1/2$, so the quotient of a lower numerator and an
upper denominator is a lower bound.
$s$: `170–171`, the same.
$W$: lower end the smaller of the two directed end values (`184`); upper end chosen by
directed tests of the sign of $t^2 + 2t - 1$ at each end (`186–195`), with `up(SQRT_2)`
above $\sqrt 2$ when the box contains $\sqrt 2 - 1$ or the tests cannot decide.
The directed steps are lemma I1’s (`interval.rs:44–95`), which bound every rounded
operation’s exact result.
The clamps at zero (`197–198`) are harmless: $c, s \ge 0$ on the range.
The root ends are enclosed outward and may exceed $1/2$ by one unit in the last place
(`run_root`, `556–557`); the monotonicity used holds on $[0, 1]$, so that is covered.

**Derived quantities** (`pose`, `236–265`). $E$ is enclosed by $e_{lo} = L/2 - hW$ with
$W$’s upper end and $e_{hi}$ with its lower end (`238–239`), and the box is refused
unless $e_{lo} > 0$, a NaN included (`241–243`); the error goes to the caller as “empty
centre domain”, which fails the run (`585–587`, `820–833`). For $u \ge 0$, $L/2 + uE(t)$
lies in $[L/2 + u_l e_{lo}, L/2 + u_h e_{hi}]$ (`244–249`), and the same with $u = u_0$
for the path centre $x_m(t) = L/2 + u_0E(t)$. For any $u \in [u_l, u_h]$,
$|u - u_0| \le \max(u_h - u_0, u_0 - u_l)$, so $|x - x_m(t)| \le du\,E(t) \le dx$
(`252–253`, `262–263`). The bounding box half-side is at most `ext`
$= h_{hi}\mathcal W_{hi}$ (`257`).

### 3.3 C4: Classification

**Statement.** A rectangle $R$ is *inside* every square of the box when, along both of
the square’s axes $(c, s)$ and $(-s, c)$, the largest possible distance between the
centres plus $R$’s half-extent along that axis is at most $h_{lo}$; it is *outside*
every square when it is separated from the bounding box along $x$ or $y$, or when along
one axis the smallest possible distance minus $R$’s half-extent is at least $h_{hi}$.

**Derivation.** The square is the intersection of two slabs
$\{|\langle z - p, (c, s)\rangle| \le h\}$ and
$\{|\langle z - p, (-s, c)\rangle| \le h\}$. $R$’s projection on the axis $(c, s)$ is
the interval of centre $\langle m - p, (c, s)\rangle$ and half-width $|c|h_x + |s|h_y$,
and on $(-s, c)$ of half-width $|s|h_x + |c|h_y$. $R$ lies in a slab iff its projection
lies in $[-h, h]$, and lies in the square iff it lies in both.
If one projection misses $(-h, h)$, the intersection has no interior; so does a
separation from the bounding box.
Inside means the whole mass is captured; outside, none.

**In the code** (`slab.rs:288–316`). Every test is an interval comparison over
$X \times Y \times C \times S$ with outward steps (`298–308`), the inside test with
$h_{lo}$ (`309`) and the outside tests with $h_{hi}$ and `ext` (`290–296`, `312`).
Treating $c$ and $s$ as independent intervals, without $c^2 + s^2 = 1$, only enlarges
the set tested. The rectangle’s binary64 approximations (`Rect.mx` and the like, lemma
F2’s) are not used: `slab.rs` reads only the enclosures.
A child box’s poses are a subset of its parent’s, so it may keep the parent’s inside
mass and boundary list (`649–650`).

### 3.4 C3: The Bound at the Path Centre, for Every Angle of the Box

**Statement.** For a boundary rectangle $R$, `area_lo` is at most
$|R \cap Q(x_m(t), y_m(t), t)|$ for every $t$ of the box.

**Derivation.** Work relative to the path centre.
The *inner rectangle* $I = [\xi_1, \xi_2] \times [b, e]$, with
$\xi_1 = x_{1,hi} - X_{m,lo}$, $\xi_2 = x_{2,lo} - X_{m,hi}$, $b = y_{1,hi} - Y_{m,lo}$,
$e = y_{2,lo} - Y_{m,hi}$, each rounded inward, lies in $R - (x_m(t), y_m(t))$ for every
$t$, since $x_m(t) \in X_m$ and $y_m(t) \in Y_m$. So the capture is at least
$|I \cap Q_0(t)|$, $Q_0(t)$ the square at the origin.
At fixed $t$ (with $s, c > 0$), the section of $Q_0$ over the line $\xi$, clipped to
$[b, e]$, has length
$\sigma(\xi) = \min(e, (h - c\xi)/s, (h + s\xi)/c) - \max(b, (-h - c\xi)/s, (s\xi - h)/c)$
(solve $|c\xi + s\eta| \le h$ and $|{-s\xi} + c\eta| \le h$ for $\eta$), a minimum of
affine functions minus a maximum of affine functions, so concave in $\xi$; and
$|I \cap Q_0| = \int_{\xi_1}^{\xi_2} \max(0, \sigma)$. On any segment $[a, a']$,
concavity gives $\int \sigma \ge (\sigma(a) + \sigma(a'))(a' - a)/2$, and
$\int \max(0, \sigma) \ge \max(0, \int\sigma)$. Any lower bounds of $\sigma(a)$ and
$\sigma(a')$ may replace them, and when their sum is positive a lower bound of the width
may replace the width.
Summing over a partition of $[\xi_1, \xi_2]$ gives a lower bound, whatever the
partition.

**In the code.** The inner rectangle with inward steps, and zero when it is empty or NaN
(`slab.rs:394–400`). `section_lo` (`362–370`) bounds each quotient below over all
$c \in C$, $s \in S$, $h \ge h_{lo}$: the numerator’s bound uses $c$’s or $s$’s upper or
lower end by the sign of $\xi$ (`kx_up`, `kx_dn`, `340–356`), and the division by the
denominator’s upper or lower end by the sign of that bound (`quot_lo`, `quot_hi`,
`320–336`). Each term increases with $h$ on the top side and decreases on the bottom
side, so $h_{lo}$ is the right end.
The knots are $\xi_1$, $\xi_2$ and estimated breakpoints at the two corner angles
$(C_{lo}, S_{hi})$ and $(C_{hi}, S_{lo})$, kept only strictly inside (`402–417`); they
only affect accuracy.
Each segment adds `dn(mul_dn(sum, width) * 0.5)` when the downward sum is positive and
the downward width is positive (`418–431`). $s_{lo} > 0$ at every $t \ge \varepsilon$,
so no quotient divides by zero for an admitted input.

### 3.5 C5: From the Path Centre to the Box

**Statement.** For every pose $(x, y, t)$ of the box,
$F(x, y, t) \ge F(x_m(t), y_m(t), t) - dx\,|G_x| - dy\,|G_y|$, where $F$ is the capture
and $G_x$, $G_y$ enclose its partial derivatives over $X \times Y$ at the box’s angles.

**Derivation.** At fixed $t$, $|R \cap Q(x, y)|$ is Lipschitz in the centre, and its
derivative in $x$, where it exists, is $\ell(x_1) - \ell(x_2)$, $\ell(z)$ the length of
the square’s chord on the line $\{x = z\}$ clipped to $[y_1, y_2]$ (move the rectangle
instead of the square and differentiate its indicator); for the $y$ derivative, the
chords on the lines $y = y_1$ and $y = y_2$ clipped to $[x_1, x_2]$, whose bounds are
the section formula with $c$ and $s$ exchanged.
The path $(x_m, y_m) \to (x, y_m) \to (x, y)$ stays in $X \times Y$ at the same $t$, so
the fundamental theorem of calculus along it gives the inequality with
$|G_x| = \max|\cdot|$ of the enclosure.
A rectangle inside or outside for the whole box has constant capture along the path and
contributes no derivative.

**In the code.** `chord` (`slab.rs:444–451`) encloses $\ell$ by the same section
formulas in interval arithmetic over $X \times Y \times C \times S$, with `over`
dividing by an interval of positive reciprocal ends (`436–438`); `gradient` (`454–483`)
takes the left minus the right chord for $x$ and the bottom minus the top chord with
$(s, c)$ for $y$, skips an edge whose line cannot reach any square of the box, and
scales by the density.
`bound` sums the enclosures over the boundary rectangles only and takes
`mul_up(dx, gx.mag())` (`518–535`).

### 3.6 Acceptance and the Cover of the Search

A box’s bound is `sub_dn(sub_dn(add_dn(base, f), lx), ly)` (`slab.rs:599`), `base` the
inside mass (`593`), `f` the boundary rectangles’ path-centre bounds times the lower end
of their density (`524–527`). A non-finite bound or loss refuses the root (`600–604`). A
box is accepted only when the bound is at least `thr`, the upper end of $\tau$’s
binary64 enclosure (`605`, `753`), so a box’s acceptance implies $F \ge \tau$ at all its
poses. Otherwise the box stops the root with a refusal at the node budget or below
resolution (`610–631`), or is split at a binary64 midpoint of $u$, $v$ or $t$ into two
closed children that cover it (`636–667`); the split rule only orders the work.
A root is verified only when its stack empties (`669`), every box popped being accepted,
refused or split.

The roots are $[\varepsilon, k_1], \dots, [k_m, T]$ with the cuts strictly increasing in
$(\varepsilon, T)$ (`118–127`); each root’s box starts at $u, v \in [0, 1]$ and at $t$
from the largest binary64 value at most $k_i$ to the smallest at least $k_{i+1}$, by
exact comparison (`556–569`; `exact.rs:117–147`). The default cuts give 86 roots
(`main.rs:168–185`); this review’s
[premises receipt](../../../packing/resources/web/wand125-sqverify-continuous-v4-2026-10-12/review/receipts/premises.json)
computes them, their enclosures and their overlaps again.
The summary is `VERIFIED` only when no `--roots` restriction was given, there is exactly
one line per root, each verified, and the axis patch is verified (`838–844`); v3
required one search result per root, each verified (v3 `762–763`), which is the same set
of outcomes without `--resume`.

### 3.7 C6: Near the Axis

**Statement.** For $t \in [0, \varepsilon]$, every legal side-$B$ square contains the
concentric axis-aligned square of side $A$, which lies in $K$, so the axis sweep of side
$A$ over $[L/2, L - A/2]^2$ bounds every such pose.

**Derivation.** $\varepsilon < \sqrt 2 - 1$, so $W$ increases on $[0, \varepsilon]$ and
$W(t) \le W(\varepsilon)$. A corner $(\pm A/2, \pm A/2)$ of the axis square projects on
$(c, s)$ and on $(-s, c)$ to at most $(A/2)(c + s) \le (A/2)W(\varepsilon) \le B/2$, so
the four corners, and by convexity the square, lie in the side-$B$ square.
Since $W \ge 1$ on $[0, 1/2]$ and $A \le B$, $L/2 - (B/2)W(t) \le L/2 - A/2$, so the
side-$B$ centre domain’s north-east quadrant lies in $[L/2, L - A/2]^2$. $\mu \ge 0$
gives $\mu(P_B) \ge \mu(Q_A)$. Lemma A1 (the capture is bilinear on each cell of the
event grid, so its minimum is at a vertex) and A2 (the sweep) are the upstream lemmas.

**In the code.** The premises $0 < A \le B$, $\varepsilon^2 + 2\varepsilon - 1 < 0$ and
$A\,W(\varepsilon) \le B$ are exact (`slab.rs:93`, `108`, `111–114`). The patch copies
the certificate with `core` set to $A$ and calls `axis::verify_axis` with `upper`
$= L - A/2$ and the same `thr` (`750–755`); `verify_axis` takes $h = $ `core`$/2$ and
the lower end $L/2$ (`axis.rs:72–73`) and accepts when every vertex’s outward-rounded
lower bound reaches `thr` (`199`). Its events are exact rationals and its values are
outward-rounded intervals, which is what “exact event sweep” means here.
It reads only rectangles, which is sound for format L as in §3.0. The default $A$ is
$\lfloor 10^9 B/W(\varepsilon)\rfloor/10^9$ (`main.rs:159–167`); the margins
$B - A\,W(\varepsilon)$ are $4.7 \times 10^{-10}$ (T-145), $6.8 \times 10^{-10}$ (T-157)
and $4.0 \times 10^{-10}$ (T-192), positive in exact rationals.

### 3.8 Admission, and What the Mode Reads from It

The continuous path calls the crate’s `admit` and nothing of the net search
(`main.rs:322–326`); `slab.rs` uses `Certificate`, `Rect`, `enclose`, `of_f64`, the
interval steps, `axis::verify_axis` and, for refusal witnesses only, `oracle::coverage`.
From the admitted certificate it reads $n$, $L$, the exact mass, the merged images’
enclosures (`rects`: edges, density, mass) and their exact data (`exact`, for the axis
sweep and the witness).

wand125’s `certificate.rs` (`1bbefbd8`) is this repository’s `dee22b88` copy
(`657ef08f`, the source the 3 October reviews accepted at `4ddf37d9c`) plus one block,
`certificate.rs:557–582` and `611–621`: a format M file may declare `proof_net`
`{step, last}`, which then sets the net’s step and count and is held to the net
premises. That block differs from this repository’s declared-net admission: `f007d7afd`
also accepts an optional `count` and refuses any other field, and `910b6b12c`, with the
5 October review’s fixes, also refuses a format L `net` block in a T or M file (DN-5);
wand125’s accepts exactly `{step, last}` and does not refuse a stray `net` block.
For this mode the difference is inert.
The branch sets only `step` and `angle_count`, which `slab.rs` never reads; its checks
can only refuse; and every line that turns rows into the measure (`sources`, `199–277`;
the expansion and mass, `632–783`) is the reviewed one.
A format T candidate never enters the branch, so the n = 40 candidates are admitted by
exactly the reviewed code.
T-192’s candidate does enter it (SC-8): it is format M, its rows are `{rectangle, mass}`
with an empty `points` list, and it declares `proof_net: {step: 83/40000, last: 200}`,
the standard net. The admitted measure is the one the reviewed admission would build.
One more property of admission matters to the mode only as friction: the candidate’s own
`B` field must pass the net premises (`588–608`, `626–631`), although the mode’s core is
`--core`. T-192’s candidate carries `B = 9977/10000` for that reason (SC-10).

### 3.9 v3 Against v4

The search is the same text in both versions (§2). The difference is the output and
`--resume`: v4 prints each root line as the root ends, keys every line with `run_key`,
and may take over verified root lines of an earlier run (`slab.rs:674–725`, `788–795`).
With no `--resume`, the two versions accept and refuse the same inputs, and the source’s
v3 rows reproduce on v4 node for node (§8.2).

## 4. Trust Boundary

What a `VERIFIED` summary of this mode rests on, beyond the lemmas of §3:

- **Its own new code**: `slab.rs` and `main.rs`’s `run_continuous`, read line by line
  here and by no other review.
- **Reused code**: `interval.rs` (lemma I1 and F3’s NaN rule), `exact.rs` (exact parsing
  and tight enclosure), `axis.rs` (A1, A2), `oracle.rs` (witnesses only), and the
  admission of `certificate.rs`; all but the `proof_net` block are byte for byte this
  repository’s crate, reviewed on 3 October and not reviewed again here beyond what
  `slab.rs` uses.
- **Binary64 arithmetic**: IEEE 754 operations correctly rounded to nearest, which the
  directed steps assume; no fused multiply-add (Rust does not contract, and the x86-64
  target uses SSE2); the default rounding mode with subnormals kept, which nothing in
  the program changes and nothing checks (SC-12). Overflow and NaN are refused, never
  accepted (`slab.rs:600–604`; the one place a NaN is dropped instead is SC-5).
- **Exact arithmetic**: `num-bigint` 0.4.6 and `num-rational` 0.4.2 for every premise,
  the admission, the axis events and the witnesses; `serde_json` 1.0.151 with
  `arbitrary_precision`, so a JSON number reaches `parse_rational` as its literal text.
- **The build**: rustc 1.98.0 and the locked dependency set; the binary here is
  `31936c4d…`. Nothing is formally verified.
- **Custody of receipts**: with `--resume`, the earlier output file (SC-1).

What it does not rest on: the knots, the split rule and the node order (accuracy and
time only), the refusal witness (a diagnostic, SC-6), the rectangle approximations of
lemma F2 (unused), and the net, which the mode never reads.

## 5. What It Shares

**With this repository’s `sqverify-fast` (V-sqverify-fast).** The interval arithmetic,
the exact parsing and enclosure, the admission and $D_4$ expansion (as §3.8 qualifies),
the exact axis sweep and the oracle, byte for byte.
So a decision by this mode is re-implemented sharing those components with
V-sqverify-fast, and an error in one of them is an error both would make.

**With the routes this record maintains for T-145 and T-157.**

- The producer’s kernel `continuous_pose.cpp` (the replayed cover,
  `E-n040-guzhou-continuous-pose-kernel-replay` and
  `E-n040-guzhou-new-supports-kernel-replay`): no code in common (Rust against C++, and
  no file of the release in the source).
  The method is the same: a branch and bound over $(u, v, t)$ on the same centre
  parametrization, concave sections, translation derivatives and an axis patch near
  $t = 0$, and the author read that kernel while reviewing T-145 before writing this
  mode (`PROVENANCE.md:38–48`). Independent code, not an independent method; §10 records
  what reading the kernel afterwards added.
- The release’s axis kernel `axis_integer_grid.cpp`: no code in common; a different side
  ($A = 77941/78125$ here against $997643/1000000$ there for T-145) and a different
  $\varepsilon$ ($10^{-7}$ against $10^{-6}$).
- This repository’s `crate-axis` evidence (`sqverify-fast`’s axis sweep on the density):
  the same `axis.rs`. This mode’s near-axis decision is that component again, at another
  side, not a second implementation of it.
- `devtools.audit_continuous_pose` (the finite audit): no code in common.

**With the producer’s other tools, for T-192.** This mode is the producer’s own checker
there. The producer’s second program, `contpose_check3`, shares no code with it and runs
Guzhou0806’s kernels; both are by the same author, who names Claude and Codex as
assistants.
The crate under the mode is wand125’s `tools/fine_net_verifier/sqverify_fast`
with five files changed, so its admission is that verifier’s admission.

**Authorship.** The commit that adds the mode names Claude as co-author; this review is
also Claude. That is an overlap of system family between the checker and its reviewer,
which separate prompts and separate code do not remove.

## 6. Findings

| Id | Grade | Where | Finding |
| --- | --- | --- | --- |
| SC-1 | minor | `slab.rs:676–725`, `788–795`, `838–844` | `--resume` counts verified root lines from any file whose `run_key` matches, and the key is a public digest |
| SC-2 | minor | `slab_tests.rs:196–207`; `slab.rs:469–478` | the y-derivative enclosure is untested, and its code path differs from the x one |
| SC-3 | note | `slab.rs:106–107` | the comment says $\varepsilon < 1/3$; the test is $\varepsilon < \sqrt 2 - 1$ |
| SC-4 | note | `README.md:214–221` | “three property tests” for four tests checking six things |
| SC-5 | note | `slab.rs:425`, `525` | a NaN area is dropped, not refused, against the crate’s F3 rule |
| SC-6 | note | `slab.rs:612–627` | the refusal witness pose is computed in binary64 and need not be legal |
| SC-7 | note | `slab.rs:537–546`; `oracle.rs:167–183` | for a format L file the witness counts points and segments that the search drops |
| SC-8 | note | `certificate.rs:557–582`, `611–621` | T-192’s candidate passes through the `proof_net` branch, which is inert for this mode |
| SC-9 | note | `README.md:193–199` | “REFUSED (86/86 roots)” counts refusals; at B = 3348/3359 two of them are refutations |
| SC-10 | note | `README.md:116–119`; `examples/n40/run.sh:15`; `certificate.rs:588–608` | budgets and the candidate’s `B` field in the examples differ from the documented defaults |
| SC-11 | note | `README.md:191–202` | the n = 40 runs publish no receipt |
| SC-12 | note | `interval.rs:44–53`; `main.rs:308–317` | the directed steps assume round-to-nearest with subnormals kept, which the program never checks (found in §10) |

**SC-1 (minor).** `run_key` (`slab.rs:676–697`) is a SHA-256 of the input digest, the
build’s source digest and the parameters, all public.
`inherited` (`701–725`) takes over any verified root line carrying it, and the
taken-over lines count toward `VERIFIED` exactly as searched ones (`788–795`,
`838–844`). So the summary of a resumed run is as trustworthy as the file it resumed
from, which `README.md:165–166` says; the summary records `inherited_roots` and
`resumed_from`, which is what makes it auditable.
The n = 28 summary shows `inherited_roots: 0` and `resumed_from: null`. The search is
unaffected.
For the record: a replay here counts only a run with `inherited_roots: 0`, or
one resumed from its own earlier output with both files kept.
Suggested for the source: print a warning line, or a status other than `VERIFIED`, when
any root was inherited.

**SC-2 (minor).** `box_bounds_hold_at_sampled_poses` checks the $x$ component of
`gradient` against an exact difference quotient (`slab_tests.rs:196–207`) and never the
$y$ component. The $y$ chords call `chord` with $(s, c)$ in place of $(c, s)$
(`slab.rs:469–478`), so an error in that exchange would not be caught.
`README.md:219` and `CONTINUOUS.md:124` describe the test as checking “the derivative
enclosure”. This review re-derived the exchanged formula (§3.5) and its probe checks the
$y$ component against one-sided exact quotients in both directions: no failure (§8.1).
Suggested: the same assertion for `gy`.

**SC-3 (note).** `slab.rs:106–107` reads “eps lies there because eps < 1/3 is checked as
eps^2 + 2 eps - 1 < 0”; the condition is $\varepsilon < \sqrt 2 - 1$, which is what C6
needs. The code is right.

**SC-4 (note).** `README.md:214` says the mode adds three property tests;
`slab_tests.rs` at v4 has four tests, the resume test being the fourth, and the six
bullets that follow list checks, not tests.

**SC-5 (note).** When a segment’s sum is NaN, `area_lo` adds it so that the rectangle’s
area becomes NaN (`slab.rs:425–426`), and `bound` then skips the rectangle because
`a > 0.0` is false (`525`). Dropping a nonnegative term is sound, but it does not
refuse, which the crate’s rule F3 and the mode’s own non-finite check (`600–604`)
otherwise do. No NaN can arise for an admitted input at $t \ge \varepsilon$
($S_{lo} > 0$, finite magnitudes).
Suggested: let a NaN area reach `lower`.

**SC-6 (note).** The witness pose is $x = L/2_{lo} + u_0 e$ with $e$ a binary64 value
near $E(t_m)$ (`slab.rs:617–619`), so the pose can lie outside the centre domain by
about one unit in the last place; `README.md:141–144` asks the reader to check legality.
Every witness of the runs here, 516 of them, is a legal pose (§8.2).

**SC-7 (note).** `exact_capture` uses `oracle::coverage`, which adds point and segment
masses (`oracle.rs:167–183`), while the search and the patch drop them.
For a format L file `exact_below_threshold` can then be false at a pose where the mode’s
own capture is below $\tau$. It changes no verdict.

**SC-8 (note).** The bead asked whether the continuous path reaches any `proof_net`
code. For T-192 it does: the candidate is format M and declares the standard net as
`proof_net`, so admission runs `certificate.rs:563–582` and `613–621`. §3.8 shows the
branch is inert for this mode and the measure is the reviewed admission’s; the n = 40
candidates are format T and never enter it.

**SC-9 (note).** The README’s row `c6718_B3348`, “REFUSED (86/86 roots)”, is accurate as
a count of refusals.
Run here, 84 of the 86 roots stop below resolution at poses whose exact capture is above
$\tau$ by about $2.5 \times 10^{-11}$, at the edge of the region where the claim fails,
and 2 stop at poses that refute it (least capture $0.99856\ldots$). The README’s column
“least exact capture at a refused pose” is the right measure; a reader should not take
86 refutations from the status.

**SC-10 (note).** The examples pass `--max-nodes 30000000` (`examples/n40/run.sh:15`),
the README’s default is 50,000,000 (`README.md:118`), and `run_key` includes the budget
(`slab.rs:689`). A verified root’s node count does not depend on the budget, so the
README’s counts compare with any run that verifies; the key only matches the examples’
own budget. Separately, a candidate must carry a `B` that passes the net premises of
admission even though the mode uses `--core` (`certificate.rs:588–608`, `626–631`); the
n = 28 file carries `B = 9977/10000` beside a core of $499/500$. Fail-closed, and easy
to misread.

**SC-11 (note).** The n = 40 table (`README.md:191–202`) reports the runs’ totals at v3
and publishes no run log or summary, unlike the n = 28 release.
A third party’s run counts here only from its retained receipts, so these runs stand as
a report until a replay here.
Suggested: publish `c6715.jsonl` and `c6718.jsonl` as the n = 28 release does.

**SC-12 (note, from the comparison of §10).** The directed steps add
$|x|\,2^{-52} + 2^{-1074}$ (`interval.rs:44–53`), which bounds the rounding error only
under round-to-nearest with subnormal results kept: a flush-to-zero or
denormals-are-zero mode would make the added $2^{-1074}$ vanish near the subnormal
range. Nothing in the Rust program changes the floating-point environment, and a Rust
program starts in round-to-nearest with subnormals on x86-64, so this is a trust
assumption rather than a defect; the producer’s kernel asserts both at startup
(`continuous_pose.cpp:158–162`), and the mode does not.
Suggested: the same check at the start of `main` (`main.rs:308–317`).

## 7. Questions for the Author

1. Would you publish the n = 40 run outputs (SC-11)? They would let this record compare
   a replay root by root, as it can at n = 28.
2. Would you add the `gy` assertion to `box_bounds_hold_at_sampled_poses` (SC-2)?
3. For `--resume`, would you mark a summary with inherited roots in its status, or
   refuse a resume across machines unless asked (SC-1)?
4. Could `--continuous` skip the net premises of admission, or take the core from the
   file, so that a candidate need not carry a net-legal `B` (SC-10)?
5. Would you assert round-to-nearest and subnormals at startup, as the T-145 kernel does
   (SC-12)?

## 8. The Checks Run Here

### 8.1 The Box Bound Against an Exact Oracle

[`bounds_probe.py`](../../../packing/resources/web/wand125-sqverify-continuous-v4-2026-10-12/review/programs/bounds_probe.py)
transcribes `angles`, `pose`, `classify`, `section_lo`, `area_lo`, `chord`, `gradient`
and `bound` from this review’s reading of `slab.rs` and `interval.rs`; Python’s floats
are the same binary64 operations, so each step computes what the Rust computes.
Its oracle is its own: the area of a rectangle clipped by a rotated square, by exact
Sutherland–Hodgman clipping in rationals, with $c$ and $s$ the exact rational rotation
of a rational $t$. At poses sampled in each box, the box’s corners and edges included,
it checks C2’s enclosures of $c$, $s$, $W$ and $E$ and of the centres, C4’s verdicts,
C3’s bound at the path centre, C5’s gradient enclosure along $x$ and along $y$ against
one-sided exact difference quotients, and the whole-box bound against the exact capture.
The instances are adversarial: rectangles at the edges and corners of the box’s middle
square, thin, tiny, large or on the container’s edge with the square pushed against it;
boxes straddling $t = \sqrt 2 - 1$, at $t$ near $10^{-7}$ and near $83/200$, and deep
ones; three parameter families, one of them $L = 3/2$, $B = 1$, where the centre domain
near $\pi/4$ is tiny; and boxes on the c6715 density itself.

Three runs with three seeds took 1,020 boxes each: 300 in each of the three adversarial
families ($L = 67/10$ with $B = 199529/200000$; $L = 3/2$ with $B = 1$; and
$L = 573351/100000$ with $B = 499/500$) and 120 on the c6715 density.
In all, 3,060 boxes and 17,280 sampled poses gave **3,386,054 checks and no failure**:
17,280 each of the enclosures of $c$, $s$ and $W$, of $E$, of the centres, of $dx$ and
$dy$, and of the whole-box bound; 120,615 inside and 1,888,365 outside verdicts; 304,401
path-centre area bounds; and 493,625 $x$-gradient and 492,648 $y$-gradient quotients.
The suite took 623 CPU-seconds
([receipt](../../../packing/resources/web/wand125-sqverify-continuous-v4-2026-10-12/review/receipts/probe-suite.json)).

**What the probe can see.** Each of ten deliberate errors was put into the transcription
in turn and the probe run on 150 adversarial boxes:

| Mutation | Detected by |
| --- | --- |
| the area bound $\times 1.0005$ (the source’s own mutation) | 5,209 C3 and 462 whole-box failures |
| a section term $\times 1.001$ (the source’s) | 1,920 C3 and 188 whole-box failures |
| the gradient halved (the source’s) | 5,853 $x$, 5,764 $y$ and 132 whole-box failures |
| $dx$ halved (the source’s “dx shrunk”) | 828 C5 and 132 whole-box failures |
| the inside test loosened by 1% (the source’s) | 216 C4 and 6 whole-box failures |
| the outside test loosened by 2% (the source’s) | 417 C4 failures |
| $W$’s upper end always taken at $t_b$, ignoring the maximum at $\sqrt 2 - 1$ | 153 C2 failures |
| the inner rectangle taken from the wrong end of $X_m$ | 37 C3 failures |
| the wrong branch of `kx_up` for $\xi < 0$ | 18 C3 failures |
| the midpoint rule in place of the trapezoid | none |

The midpoint rule over-estimates a concave integral, but with knots at the breakpoints
of both end angles the section is linear between knots up to second order in the angle
width, which the first-order slack of the $(C, S)$ box hides; at the boxes the search
uses, the mutation is not detectable this way, and the probe claims nothing for it.
The other nine show the probe would see an error of each of those kinds.
Its limit is the one every transcription has: a misreading shared by `slab.rs` and this
review’s transcription of it would pass, and the review’s reading (§3) is what stands
against that.

### 8.2 The Verifier on Toy Instances and on the Source’s Controls

Every run used the binary `31936c4d…` at two threads, and each output was judged by
[`judge_run.py`](../../../packing/resources/web/wand125-sqverify-continuous-v4-2026-10-12/review/programs/judge_run.py),
which holds the premises line to this review’s exact values, every root line to its cut
and to `nodes = 2 leaves - 1` when verified, the summary to its lines, and every refusal
witness to an exact re-evaluation: the pose read as the rationals of its binary64
values, its legality decided exactly, and its capture computed with the oracle of §8.1
and compared with the run’s `exact_capture`.

| Run | Status here | Nodes | Axis patch minimum | Witnesses that refute | CPU-s | Agrees with |
| --- | --- | --- | --- | --- | --- | --- |
| uniform toy, $\tau = 4/5$ | `VERIFIED`, 86 roots | 2,132 | 0.8099997 | none (verified) | 0.0 | the exact answer $B^2 = 81/100$ |
| uniform toy, $\tau = 81/100$ | `REFUSED` | 3,767 | 0.8099997 | 0 of 86 (capture exactly $\tau$) | 0.0 | the exact answer |
| uniform toy, $\tau = 41/50$ | `REFUSED` | 3,767 | 0.8099997 | 86 of 86 at $81/100$ | 0.0 | the exact answer |
| c6715, every weight × 985/1000 | `REFUSED` | 7,714 | 0.98488 | 86 of 86, least 0.98711 | 1.5 | README v3 row, every figure |
| c6718, every weight × 985/1000 | `REFUSED` | 5,979 | 0.98648 | 86 of 86, least 0.98648 | 1.9 | README v3 row, every figure |
| c6718 at $B = 3348/3359$ | `REFUSED` | 12,364,148 | 0.98421 | 2 of 86, least 0.99856 (SC-9) | 266 | README v3 row, every figure |
| n = 28, every mass × 985/1000 | `REFUSED` | 5,478 | 0.98599 | 86 of 86, least 0.98599 | 3.7 | the source’s `control.jsonl`, root by root, and its `run_key` |

The uniform toy is one rectangle covering $K = [0, 3]^2$ with density 1 at $B = 9/10$,
where every legal square captures exactly $81/100$: the mode verifies just below that,
refuses at it without claiming a refutation, and refutes just above it, as §3 predicts.
The n = 40 candidates were built by
[`candidates.py`](../../../packing/resources/web/wand125-sqverify-continuous-v4-2026-10-12/review/programs/candidates.py)
from this repository’s copies of the two densities, held to the SHA-256 values
`prepare.py` pins, in `prepare.py`’s row order; that the node counts match the README to
the last node shows the same measure in the same order, and v4’s search equal to v3’s on
it. At n = 28 the control run here equals the source’s log in every root’s verdict, node
count, witness pose and exact capture, and in the axis patch.

### 8.3 Exact Premises

[`premises.py`](../../../packing/resources/web/wand125-sqverify-continuous-v4-2026-10-12/review/programs/premises.py)
decides every premise of §§3.0 to 3.7 for the four parameter sets, and
[`candidates.py`](../../../packing/resources/web/wand125-sqverify-continuous-v4-2026-10-12/review/programs/candidates.py)
the certificates’ facts, all in exact rationals:

| Parameters | $X = L/B$ | $n\tau - M$ | $A$ (default) | $B - A\,W(10^{-7})$ |
| --- | --- | --- | --- | --- |
| T-145, c6715 | $1340000/199529$ | $1/500$ | $77941/78125$ | $235529976449/500000000000005000000$ |
| T-157, c6718 | $3359/500$ | $1/500$ | $997320431/10^9$ | $227120145419327729/335900000000003359000000000$ |
| control, c6718 at $3348/3359$ | $225053/33480$ | $1/500$ | $124590627/125000000$ | $20702515139916093/41987500000000419875000000$ |
| T-192, n = 28 | $1149/200$ | $1/100000$ | $4989999/5000000$ | $200029979999/500000000000005000000$ |

In each, $L^2 > 2B^2$, $T^2 + 2T - 1 = 89/40000 > 0$,
$\varepsilon^2 + 2\varepsilon - 1 < 0$, $0 < A \le B$, and the 86 default roots increase
strictly from $\varepsilon$ to $T$ with outward enclosures that cover and overlap.
The `run_key` recomputed from T-192’s parameters, its candidate digest, the v4 source
digest and the budget $2 \times 10^8$ equals the key in the source’s `summary.json` and
`control-summary.json`, and every premise those summaries print equals the value here.
The densities: c6715 has 480 positive orbits of mass $3999/100$ and 3,792 distinct
images; c6718 has 685 orbits, 522 inherited rows each equal to its pool row with no
index twice and 163 generated in no pool orbit, mass $3999/100$, 5,424 images; T-192’s
candidate has 884 positive rows inside $K$, mass $2799999/100000$ equal to its
`total_mass`, 7,068 images (the `expanded_rectangles` its summary prints), and its
control is it with every mass times $985/1000$, row by row.

## 9. For the Record

**What the review supports.** For T-192, the argument from this certificate to the
claim, through route A’s checker, with its premises and its control, read and found
without a blocking defect: the qualifying read that `C1` describes, recorded as the
`external_review` of `E-wand125-continuous-n28-5745-report`. For T-145 and T-157, the
soundness of a second route whose runs are reported, recorded on two reported entries of
the source’s n = 40 runs (`E-n040-wand125-sqverify-continuous-6715-report` and
`-6718-report`). With those records, `devtools.check_results` derives `C1` for T-192,
from `C0`, and leaves every other rung where it was: no complete run of the mode has
been replayed here, so no `V` rung and no `C` rung above `C1` can rest on it.
For T-157 this review is the second retained adversarial AI review, so `V4` and `C4`
there now wait only on a human oversight record; it decided the density and the argument
again through the second checker, and the kernel’s code was read by T-145’s two reviews,
which an overseer should weigh.

*Note of 23 October 2026, after review A of jlevy/squares#752:* the record does not
adopt the last sentence above.
It does not count this review toward T-157’s rung 4, since the review decided no part of
T-157’s continuous cover and read neither of its kernels, and it lists the review among
T-192’s reviews only, citing it from T-145 and T-157, until a replay here (think-flxm)
makes the mode a deciding route for them.

**What is owed.**

- **T-192, route A** (think-0arj): the complete v4 run over 86 roots at two threads,
  priced at 13.3 CPU-hours (high 16) from the 15 October sample, with the published
  control (4 CPU-seconds here) and a counted oblique control.
  Its bead holds the commands; §11 gives the judge’s conditions.
  It would reach `C3` reproduced with the producer’s code.
- **T-145 and T-157, the second route**: the complete v4 runs of c6715 and c6718 on the
  candidates `candidates.py` builds, priced from the source’s walls at about 2.4 and 2.8
  CPU-hours here (six threads times the wall, times the ratio 1.23 the n = 28 sample
  measured), and from this host’s rate on the B = 3348/3359 control (about 46,000 nodes
  a CPU-second) at about 0.7 CPU-hours each; with the mass controls (seconds) and a
  counted oblique control.
  They would move the continuous cover’s mark to independently re-implemented after
  reading the producer’s code, and no rung.

## 10. Comparison with Earlier Reviews

This section was written after §§1 to 9, from the 10 October review of T-145’s kernel
(the argument, the trust boundaries and GC-1 to GC-8), the 12 October review of T-157
(its headings and GN-7), the passage of the 14 October review of wand125’s fine-net
bounds on `certificate.rs`, and Guzhou0806’s `continuous_pose.cpp`, read for the first
time here. The 11 October final review of T-145 predates the mode and was not read.

**Against the 10 October review and the kernel it read.** The two arguments are the
same, lemma for lemma: that review’s items 2 to 9 are C1 to C6 and the counting, and
nothing in either derivation contradicts the other.
The implementations differ where the mode’s README says they do, and in one more place:

- *Directed rounding.* The kernel steps each result one neighbour by integer arithmetic
  on its encoding and asserts round-to-nearest and no flush-to-zero at startup
  (`continuous_pose.cpp:28–35`, `158–162`); the mode adds $|x|\,2^{-52} + 2^{-1074}$
  (lemma I1) and asserts nothing, which is SC-12.
- *Classification.* The kernel screens in floating point with a $10^{-10}$ tolerance and
  decides by intervals (GC-6); the mode has no screen.
- *The section bound.* The kernel evaluates each term in interval arithmetic
  (`continuous_pose.cpp:52–58`); the mode bounds each by the sign of its numerator.
  Both are valid lower bounds over the box.
- *Knots and the trapezoid.* The twelve knot expressions are the same expressions in the
  same order (`continuous_pose.cpp:65–67`, `slab.rs:374–389`), the kernel’s at the box’s
  mid angle and the mode’s at both corner angles, and the trapezoid accumulation has the
  same form (`continuous_pose.cpp:72–76`, `slab.rs:418–430`). That is the visible trace
  of the author’s reading of the kernel, which `PROVENANCE.md` declares.
  Knots set accuracy only, and §3.4 re-derives the trapezoid bound for any knots, so
  this shared structure carries no shared error this review can find; it is why the mode
  is independent code written after reading the producer’s, and not clean-room.
- *NaN.* GC-7 found the kernel’s `min_element` dropping a NaN; SC-5 finds the mode
  dropping a NaN area.
  Both are sound and both depart from their own rule.
- *The near-axis patch.* The kernel’s axis certificate is an int128 sweep of a dominated
  measure at $\varepsilon = 10^{-6}$ and side $997643/10^6$, margin $3.6 \times 10^{-6}$
  on that measure (GC-1); the mode’s is the crate’s exact-event sweep of the density
  itself at $\varepsilon = 10^{-7}$ and side $77941/78125$. GC-1’s point carries over:
  the containment margins here, $4 \times 10^{-10}$ to $7 \times 10^{-10}$, hold in
  exact rationals only, which is how the mode checks them.
- *The budget* (GC-5). In both, a verified slab’s or root’s node count does not depend
  on the budget; the mode’s `run_key` binds the budget anyway (SC-10).

GC-4 specified a first-party kernel with the angle as an interval dimension on this
repository’s crate. The mode is that design written outside the project: it keeps the
crate and adds the angle, as GC-4 described, with a section bound of its own rather than
the crate’s rotated branch and bound.

**Against GN-7 of the 12 October review.** GN-7, written before anyone here read the
source, said a replay would make the relation `independent-implementation` against the
producer’s kernel, not clean-room, and `shared-components` against this repository’s
route, and move no rung.
This review agrees, with two refinements.
The mark the result would take is *independently re-implemented after reading the
producer’s code*, the ladder’s not-clean-room level, rather than plain *independently
re-implemented*. And the near-axis part of a replay would not be a second implementation
of anything: it is the same `axis.rs` that `E-n040-guzhou-new-supports-crate-axis`
already runs.
GN-7’s price, about 2.3 CPU-hours for c6718 from the README’s wall, is near
this review’s high end of 2.8; this host’s rate on the B = 3348/3359 control puts it
near 0.7.

**Against the 14 October review.** That review read a 34-line `proof_net` hunk in an
archived copy of wand125’s nested fine-net crate and described it as lacking, among
other things, a refusal of `proof_net` outside format M. The copy retained here has that
refusal (`certificate.rs:613–615`). The archive that review read is not retained, so
whether the two copies differ, or that sentence is wrong, cannot be settled here;
neither review’s conclusion depends on it, since this mode never reads the net.

**Against the bead.** think-xzob’s read of 12 October said the declared-net review’s
fixes DN-2, DN-4 to DN-6 and DN-9 are not in this `certificate.rs`. Of those, only DN-5
changed `certificate.rs` (a `net` block refused outside format L); DN-2 is in a Python
audit and the rest in documents and tests (§3.8).

## 11. For Whoever Replays It

The judge of a replay holds, beyond the stage 4 runbook: the build’s `source_sha256` is
`619b3c00…c7f5`; the summary’s `inherited_roots` is 0, or the resumed file is the
replay’s own and is kept (SC-1); every root line’s index and `t` are the default cuts’;
every verified root has `nodes = 2 leaves - 1` and a least bound at least $\tau$; the
axis patch is verified at the default $A$; and every counted control’s refusal is at a
legal pose whose capture, computed apart from the crate, is below $\tau$ (SC-6, SC-9).
`judge_run.py` does each of these.
The source’s mass controls fail everywhere by about 1.5%: run here, each is refused at
the axis patch and at every root within a few dozen boxes, at legal poses whose exact
captures are below $\tau$. That is a coarse test of the oblique search.
A counted control should keep the axis patch and fail only at an oblique root, so that
its refusal tests the oblique bound where it is tight.
(The n = 28 packet’s README said the source’s control “is refused at the axis patch
alone … and never reaches the oblique search”; for this program that is not so, as its
own table and the run here show, and the sentence fits the second program,
`contpose_check3`; the change that records this review corrects the README.)

## What This Review Does Not Establish

No complete run of the mode on any claim, and so no decision of any continuous cover; no
review of Guzhou0806’s kernels or of the producer’s second program, `contpose_check3`;
no new review of the modules shared with this repository’s crate beyond what `slab.rs`
uses; no formal verification; no human oversight; and no change of any bound, rung or
significance by itself.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
