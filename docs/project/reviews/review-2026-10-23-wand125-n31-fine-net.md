# wand125’s Fine-Net Certificate for $s(31) \ge 2391/400$: Mathematical Review

2026-10-23. Reviewer: Claude (Anthropic), strongest tier (`tbd-strong-max`), maximum
reasoning. Bead `think-oc25`, the stage 4 mathematical review lane of the import
`think-wop1`, prompted separately from the records lane that retained and registered the
result and sharing none of its context beyond the brief and the committed record.
Scope: the certificate `mixed_n31_L59775` of wand125/square-packing at `23e3186`, and
T-232, the entry the records branch registers for it
(`claude/intake-2026-10-23-lower-bounds` at `7b90d47d2`). This review registers nothing
and moves no bound.

## Summary for the Author

**Verdict: accept.** The argument from the certificate to the claim is correct and
complete: if 31 unit squares fitted in the closed square of side $L = 2391/400$, their
cores would be 31 disjoint sets of measure at least one each, against a total mass of
$3099999/100000$. Every hypothesis the argument needs holds in exact arithmetic, and the
declared net reaches every orientation with the stated margin.
The certificate in fact proves the strict inequality $s(31) > 2391/400$.

The one condition that needs a large computation is the capture: at each of the 2,073
net directions, every admissible core must hold mass at least one.
This review decided it again, with a checker written for this review from the
mathematics and the certificate format alone, in exact integer arithmetic, at a
stratified sample of 122 directions (including the axis direction, the two smallest
angles, the last two directions, and the twelve directions where your run’s certified
bound was tightest).
Every one of them verified, the least capture found being 1.000116 at direction 1841.
That is a sample: it decides those directions and nothing about the other 1,951. The
complete replay over all 2,073 directions is the records lane’s, running now with this
repository’s reviewed `sqverify-fast`. Mutants of the certificate (every mass scaled by
$99/100$, the heaviest row removed, and every mass scaled by 0.999784 so that one pose
at direction 1841 falls just below one) were all refused, each with an exact witness.

There is no blocking or major finding.
Three minor findings concern your bundle’s prose and manifest, not the mathematics: the
README names a control file that does not exist (M-1), `files-sha256.json` gives the
digest of an earlier README (M-2), and the check2 receipt calls the check independent
where it is independent of your search but is this repository’s verifier with one change
(M-3). The notes and the questions at the end are about margins, the control and the
price of the check.

## The Claim and What Was Read

**The claim.** No packing of 31 closed unit squares with pairwise disjoint interiors
fits in the closed square $[0, L]^2$, $L = 2391/400 = 5.9775$. Hence $s(31) \ge L$. The
record’s lower lanes at $n = 31$ stand at $2381/400$ (T-068 reported, T-074 verified);
the claim is above them by $1/40$, and above jlevy/squares#446’s unadopted $597/100$ by
$3/400$. The upper bound is $6$, so the gap would narrow from $19/400$ to $9/400$.

**The certificate.** `candidate.json` (148,514 bytes, SHA-256 `4a7df269…be3b`), retained
gzip-compressed in the packet `packing/resources/web/wand125-fine-net-n31-2026-10-11/`:
536 axis-parallel rectangles with positive masses summing exactly to $3099999/100000$,
no points, core side $B = 4999/5000$, and the declared net `proof_net = {step: 1/5002,
last: 2072}`. Each rectangle’s mass is spread uniformly, one eighth on each of its
images under the symmetry group $D_4$ of the container.

**Read, as data.** The packet’s README, acquisition and retention records, the retained
candidate, `bundle.json`, `ASSET.json`, `files-sha256.json` and the source’s README; the
check2 receipt, control summary, run log and control log; the pre-publication receipt;
the lane’s premises and diagnostic-sample receipts; the source’s `SPEC.md`
(byte-identical to the copy the 6 October check2 packet retains); T-232 with its
evidence entry `E-wand125-fine-net-n31-59775-report`, and the changes to `n-031.md` on
the branch.
**Read, as method.** `result-import.md` stage 4 and “Label the PR and Prepare
News”; `epistemics.md` on confirmation, independence, review records and significance;
the
[declared-net soundness review](review-2026-10-06-sqverify-fast-declared-net-soundness.md)
of the maintained crate and its
[fix check](review-2026-10-06-sqverify-fast-declared-net-fix-check.md), of 6 October;
and, of other results on this route, the
[n68](review-2026-10-19-n68-fine-net-mathematics.md) and
[n84/n85](review-2026-10-19-n84-n85-fine-net-mathematics.md) reviews of 19 October and
the opening of the
[review of ten check2 certificates](review-2026-10-06-wand125-check2-ten-certificates.md)
of 6 October. **Not read.** The source’s adapted crate
`sqverify-proof-net-fe12e036c.tar.gz` (pinned, unopened), the sealed inner bundle, this
repository’s `packing/sqverify_fast/` source and its `SOUNDNESS.md`, any program of
`packing/devtools/`, and the programs of the 14 October fine-net review.
No earlier review of this certificate exists (see [Earlier Reviews](#earlier-reviews)).

## The Argument, Re-Derived

Write $D = 1/5002$, $t_j = jD$ for $j = 0, \ldots, 2072$, $\theta_j = 2\arctan t_j$,
$b = B/2$, and $r(t) = (1 + 2t - t^2)/(2(1 + t^2))$, which is
$(\cos\varphi + \sin\varphi)/2$ for $\varphi = 2\arctan t$. Let $\mu$ be the
certificate’s measure and $Q_j(c)$ the closed square of side $B$, centre $c$ and angle
$\theta_j$.

1. **Fold.** A unit square’s orientation is defined modulo $\pi/2$, and a reflection of
   the container maps orientation $\varphi$ to $-\varphi$. So each square $S$ of a
   packing has an image $gS$, $g \in D_4$, with orientation $\varphi \in [0, \pi/4]$,
   half-angle tangent $t \in [0, \tan(\pi/8)]$. The fold is applied square by square; no
   single symmetry needs to fold the whole packing.
2. **Bins.** The bins $[t_j - D/2, t_j + D/2]$ abut and cover $[0, (2072 + 1/2)D]$,
   which contains $[0, \tan(\pi/8)]$ because $t_{2072} = 1036/2501$ satisfies
   $t^2 + 2t - 1 = 367/6255001 > 0$. Choose $j$ with $|t - t_j| \le D/2$.
3. **Containment.** The relative turn $\delta$ between $gS$ and $\theta_j$ has
   $z = \tan(|\delta|/2) = |t - t_j|/(1 + t t_j) \le D/2$. The concentric square of side
   $B$ turned by $\delta$ lies strictly inside the unit square if and only if
   $B(\cos\delta + \sin|\delta|) < 1$, and
   $\cos\delta + \sin|\delta| = (1 - z^2 + 2z)/(1 + z^2) \le 1 + 2z \le 1 + D$, while
   $B(1 + D) = 25009997/25010000 < 1$. Checked exactly at both ends of every bin, the
   largest extent is $500400014977/500400085000$, at the upper end of bin 0.
4. **Centre domain.** $gS \subset [0, L]^2$ puts its centre in $[r(t), L - r(t)]^2$.
   Since $r'(t)$ has the sign of $1 - 2t - t^2$, positive below $\tan(\pi/8)$, every
   square of bin $j$ has its centre in $C_j = [r(a_j), L - r(a_j)]^2$,
   $a_j = \max(0, t_j - D/2)$. Every $a_j$ lies below $\tan(\pi/8)$ (the last bin’s
   lower end gives $-22423/100080016 < 0$).
5. **Capture.** The certificate asserts that $\mu(Q_j(c)) \ge 1$ for every $j$ and every
   $c \in C_j$. Then $g^{-1}Q_j(c)$, with $c$ the centre of $gS$, is a closed square
   strictly inside $S$, and its measure is $\mu(Q_j(c)) \ge 1$ because $\mu$ is
   $D_4$-invariant.
6. **Count.** The cores of distinct squares lie in their disjoint open interiors, so
   they are disjoint. Every mass is positive, so
   $31 \le \sum_S \mu(\text{core}(S)) \le \mu(\mathbb{R}^2) = 3099999/100000 < 31$, a
   contradiction. No packing of 31 unit squares fits at side $L$, and since a packing
   that fits at a smaller side fits at $L$, $s(31) > L$.

**The quarter turn.** At a fixed direction the rotation by $\pi/2$ about the container’s
centre maps $Q_j(c)$ to $Q_j$ at the rotated centre (a square is invariant under a
quarter turn about its own centre) and preserves $\mu$, and the four images of the
quadrant $[L/2, L - r(a_j)]^2$ tile $C_j$. So step 5 needs only the quadrant.
The maintained crate decides the quadrant, by the 19 October reviews, and so does this
review’s checker.

**What the net covers.** Every orientation, by steps 1 and 2; every position, by step 4;
hence every square of every packing.
The exclusion is uniform, square by square, with no case split over configurations,
which is why one measure suffices and why the only computation is the capture at 2,073
directions.

**The measure.** “Mixed” is the format’s name (rectangles, points and segments); this
certificate uses rectangles only.
The 536 rows expand to 4,288 images, of which 4,244 are distinct after coincident images
merge (their densities add); the merged measure is exactly $D_4$-invariant and
integrates exactly to the listed mass.
It is strongly concentrated: 260 of the 536 rows are strips about $1/1000$ thick, 216 of
them within $0.03$ of a line at distance 1, 2 or 3 from a wall, and those carry 20.5 of
the 31 units of mass.
The densest row is a $1.011 \times 1.002$ thousandths square of mass $0.391$ at
$(0.9988, 0.9988)$, density $386{,}421$ (an image density of $48{,}303$). So the capture
is far from smooth: moving a core by a thousandth can move a large mass in or out.

**The arithmetic.** The source’s check and the maintained route decide admission and
premises in exact rationals and the capture by interval branch and bound with outward
binary64 rounding over centre boxes, with an exact-event vertex sweep at direction 0
(per the source’s `SPEC.md` section 5 and the reviews cited above; this review did not
read the crate). This review’s checker decides everything in exact integers (below).

## Hypotheses Each Checker Assumes

| Hypothesis | Where it enters | Status here |
| --- | --- | --- |
| H1. The format’s meaning: rows `[x0, y0, x1, y1]`, mass spread one eighth per $D_4$ image, densities adding | every checker | read from `SPEC.md` §2; the expansion here is written from it |
| H2. Every mass nonnegative | step 6 | holds: all 536 positive |
| H3. $M < n$ with threshold one | step 6 | holds: $31 - M = 1/100000$ |
| H4. $B(1 + D) < 1$ and $t_{2072}$ past $\tan(\pi/8)$ | steps 2, 3 | hold, margins above |
| H5. The per-bin domain, from $a_j$ and the monotonicity of $r$ | step 4 | holds at every node |
| H6. $D_4$-invariance of $\mu$, for the fold and the quarter turn | steps 1, 5 | holds exactly on the merged expansion |
| H7. The capture at every centre of every direction’s quadrant | step 5 | the computation; decided here at a sample, at all 2,073 by the lane’s census |
| H8. Closed cores strictly inside open squares | step 6 | holds by step 3; no point masses, so nothing rests on boundaries |
| H9. The maintained route’s implementation conditions: $t_{\max} \le 1/2$, the tangent form $B(1 + D/(1 - D^2/4)) < 1$, the densest row’s mass over area (eight times its image density) at most $2^{32}$ | the crate’s frame bounds, not the mathematics | hold: $1036/2501$; $500400014977/500400075000$; $386{,}421$ |

## This Review’s Checker

The programs are in the packet’s
[`review/review-2026-10-23/`](../../../packing/resources/web/wand125-fine-net-n31-2026-10-11/review/review-2026-10-23/README.md),
with what each printed.

**Premises (`premises.py`, exact).** The decompressed candidate’s SHA-256 is the pin;
$n$, $L$, $B$ and the net are the claim’s; all 536 rows lie in $[0, L]^2$ with
$x_0 < x_1$, $y_0 < y_1$ and positive mass, and every coordinate is a multiple of
$10^{-17}$. The masses sum exactly to $3099999/100000 = 31 - 1/100000$. The merged
expansion has 4,244 rows, integrates exactly to the same mass, and is invariant under
all eight symmetries.
Lemma N0’s premises: $B(1 + D) = 25009997/25010000$ (margin $3/25010000$);
$t_{2072}^2 + 2t_{2072} - 1 = 367/6255001$; the last bin’s lower end gives
$-22423/100080016$; $t_{2072} = 1036/2501 \le 1/2$; the tangent form is
$500400014977/500400075000 < 1$. The narrowest per-bin domain is
$42801606283/9379557200 \approx 4.563$ wide.
Status `PREMISES_HOLD`.

**The net (`net.py`, exact).** The 2,073 bins abut, bin 0 starts at 0, and the last
reaches past $\tan(\pi/8)$. The core is strictly inside the square at both ends of every
bin, computed with the exact $z$ there; the largest extent is
$500400014977/500400085000$, a margin of
$70023/500400085000 \approx 1.4 \times 10^{-7}$, at the upper end of bin 0, and the
uniform bound $B(1 + 2z) \le B(1 + D)$ holds at every end.
Every $a_j$ lies where $r$ increases, and at every node the four quarter-turn images of
the quadrant tile the domain.
Status `NET_COVERS`.

**The capture (`capture.py`).** For a cell $P$ of centres (an axis-parallel box with
centre $p_0$ and half-widths $h_x, h_y$), put $\eta_u = h_x\cos\theta + h_y\sin\theta$,
$\eta_v = h_x\sin\theta + h_y\cos\theta$, and work in the frame
$(\sigma, \omega) = (u \cdot q, v \cdot q)$ with $u = (\cos\theta, \sin\theta)$,
$v = (-\sin\theta, \cos\theta)$. The kernel
$K = [\sigma_0 \pm (b - \eta_u)] \times [\omega_0 \pm (b - \eta_v)]$ is the intersection
of all cores over the cell.
For $p \in P$ the core $Q(p)$ also contains four slabs outside $K$ and disjoint from it
and from each other: on the $+u$ side the slab of width $\eta_u + u \cdot (p - p_0)$ and
the kernel’s $\omega$-extent, on the $-u$ side the one of width
$\eta_u - u \cdot (p - p_0)$, and the same along $\pm v$. The two $u$-widths sum to
$2\eta_u$. The measure of a slab is the integral of the line density across it; the line
density is a sum over rectangles of density times chord, and a chord of a convex set is
concave in its offset on its support (Brunn–Minkowski in one dimension), so on the slab
it is at least the smaller of its values on the slab’s two extreme lines.
Hence, for every $p \in P$,

$$\mu(Q(p)) \ge \mu(K) + 2\eta_u \min(\Lambda_{+u}, \Lambda_{-u}) + 2\eta_v \min(\Lambda_{+v}, \Lambda_{-v}),$$

where $\Lambda_{\pm u}$ sums, over rectangles, density times the smaller chord on the
two extreme lines of the slab.
Unlike the kernel bound alone, this is exact to first order in the cell’s size, so far
fewer cells are needed: 2,842,868 nodes over the sample, against 46,696,377 in the
source’s run at the same oblique directions.

A float64 pass chooses the cells.
Each leaf it accepts is decided again in exact integer arithmetic: the grid is
$1/(10^{17} \cdot 2^{61})$, on which every coordinate of the measure is an integer;
$\cos\theta_j = C/E$ and $\sin\theta_j = S/E$ with integers $C^2 + S^2 = E^2$; the area
of a rotated box against a rectangle is a signed sum of sixteen corner terms with no
division, and a chord is a min–max of integers.
Densities are rounded down to multiples of $2^{-64}$ and the quadrant’s upper end is
rounded up, both of which can only make the decision harder.
Every rectangle near a leaf is gathered from an exact bucket index and classified
exactly. The leaves are checked to be exactly the leaves of one bisection tree of the
quadrant. The verdict rests on the exact pass alone.
`geometry_selftest.py` holds the integer formulas to brute-force clipping in Fractions
at nine directions (0, 1, 2, 7, 296, 1036, 1777, 2071 and 2072): 18,000 random and
adversarial cases for each of the area and the two chords, with thin rectangles,
near-parallel edges and box centres on rectangle corners among them, and 3,570 of the
areas partial. All agree exactly.

**The sample.** `sample_plan.py` fixed it before any direction ran: the directions 1 to
2072 in 96 strata of about 21.6, one drawn uniformly from each by a generator seeded
from the candidate’s SHA-256 (its first 16 hex digits, `4a7df269037a6449`, as an
integer), and 28 named directions: 0, 1, 2, 1036, 2071 and 2072, the six of the lane’s
diagnostic, the source’s twelve tightest and its four heaviest.
Two named directions (1776 and 1820) were also drawn, so the sample is 122 directions,
5.9% of the net.

Every one of the 122 is `VERIFIED`. Each partition holds, and every leaf the float pass
accepted was certified exactly at the first attempt; none needed splitting again.
The checker took 2,842,868 nodes and 1,421,495 leaves over the sample, a median of 23
times fewer nodes per oblique direction than the source’s run, and 1,909.7 CPU-seconds:
a median of 13.7 s, and 257 s for the three smallest angles 0, 1 and 2 together, where
near-parallel edges make the bound work hardest.

| Direction | Why named | Nodes here | Nodes at the source | Least capture found |
| ---: | --- | ---: | ---: | ---: |
| 0 | the axis | 333,413 | (a vertex sweep of 11,778,624 vertices) | 1.0014685 |
| 1 | smallest angle | 167,741 | 191,001 | 1.0014859 |
| 296 | lane’s diagnostic | 14,329 | 258,339 | 1.0013765 |
| 676 | source’s tightest | 13,753 | 356,707 | 1.0010028 |
| 1036 | middle | 16,539 | 400,703 | 1.0010123 |
| 1820 | source’s tightest, also drawn | 21,361 | 484,833 | 1.0002510 |
| 1841 | drawn | 21,485 | 489,859 | 1.0001161 |
| 1851 | source’s tightest | 21,507 | 492,057 | 1.0001508 |
| 2069 | source’s heaviest | 22,829 | 516,671 | 1.0007357 |
| 2072 | last | 22,895 | 514,531 | 1.0007467 |

The least certified leaf bound was $1 + 1.0 \times 10^{-9}$ (direction 1519), which only
says where the branch and bound stopped.
The least capture found is the exact capture, by the second method, at the leaf centre
of least float capture, so it bounds that direction’s true minimum from above.
Over the sample it runs from 1.000116 (direction 1841, centre near $(3.7040, 3.5774)$)
to 1.00215 (direction 133), with median 1.00096. 69 of the 122 are below 1.001 and five
below 1.0005 (1841, 1851, 1820, 1861 and 573).

**Controls.** A checker that accepts the certificate must refuse what is false.

- Every mass scaled by $99/100$: `REFUTED` at directions 0, 1, 676, 1036 and 2072, each
  with an exact witness inside the domain (captures 0.99486, 0.99487, 0.99823, 0.99483
  and 0.99342).
- The heaviest row (row 33, mass 1.3749, the strip
  $[0.6574, 0.9200] \times [0.99878, 0.99979]$) and its seven images removed: `REFUTED`
  at directions 1, 1036 and 2072 (0.663, 0.779 and 0.743).
- The sharp control: every mass scaled by $499891977421/500000000000 \approx 0.999784$,
  so that the capture at direction 1841’s least-capture pose is at most $1 - 10^{-4}$:
  `REFUTED` at 1841 after 21,337 nodes, with an exact witness of capture 0.9999947 near
  $(3.7041, 3.5765)$.

So the checker separates the certificate from a measure $2.2 \times 10^{-4}$ lighter at
its tightest sampled direction.
And `bound_selftest.py` holds the cell bound itself to the second method: at 24 random
cells at directions 0, 1, 296 and 2072, the exact bound never exceeds the exact capture
at any of seven points of its cell.
Where the bound is tight it comes within $7 \times 10^{-22}$ of the capture, which is
the rounding of the densities.

**The source’s logs at single poses (`source_log_points.py`).** Status `CONSISTENT`.

- **The axis row.** Its logged argmin $(70013/20000, 70013/20000)$ has exact capture
  1.0012987505, at least the row’s certified 1.0012987504. Scaled by $197/200$ it is
  0.98627927, so the control’s axis refusal, logged by the sweep’s value and with no
  exact flag, is genuine.
- **The twelve tightest rows.** At two points of each least-bound box, the exact
  captures are 1.0021 to 1.0857, each at least its row’s bound.
  A bound of $1 + 2 \times 10^{-11}$ over a box whose captures exceed 1.002 is where the
  branch and bound stopped, not a sign of tightness.
- **The 31 oblique control witnesses.** Each lies in its per-bin domain.
  Each scaled capture equals the log’s exact rational digit for digit and lies between
  0.98786 and 0.99999999993, and each unscaled capture is at least one (1.0029 to
  1.0152).

## Trust Boundaries and What the Checkers Share

Three checkers bear on the claim.

- **The source’s check** (`V-wand125-sqverify-proof-net`, build source `ab6e33e1…`,
  binary `ec04d332…`): this repository’s `sqverify_fast` adapted by the source to read a
  declared net, at fe12e036c. It trusts that adaptation, which no review here has read
  (the 6 October review accepted `d97758bb…`, this repository’s own declared-net build,
  not the source’s), rustc 1.98.0, binary64 directed rounding as the crate does it, and
  the truth of its receipts: no third party watched either complete run.
  It decides all 2,073 directions, twice by the author’s account, and refuses the
  197/200 mutant at 32 directions.
- **The maintained route** (`V-sqverify-fast`, `d97758bb…`, the records lane’s census
  now running): the reviewed crate, its outward-rounded interval branch and bound and
  axis sweep, the compiler and the hardware, and the census driver’s admission and
  control logic. When the census completes it decides all 2,073 directions and the
  whole-net controls. It shares with the source’s check the whole crate except the
  declared-net reader, so its agreement with the source is close to a reproduction, as
  the registry already says.
  The lane’s eight-direction diagnostic found the reviewed build and the source’s
  adaptation taking the same node counts to the same least bounds, which is what that
  sharing predicts.
- **This review’s checker** (`capture.py` with `n31_geometry`, `n31_exact` and
  `n31_brute`): CPython 3.14.7’s integers and `fractions`, its own reading of the
  format, the cell bound proved above, the sixteen-term area and chord formulas (derived
  here, and held to brute-force clipping on 18,000 cases each), the exactness of its
  bucket index, and the partition check.
  numpy enters only the float pass, which decides nothing.
  It decides the 122 directions of the sample.

What any two share:

- **Code.** The source’s check and the maintained route share the crate.
  This review’s checker shares no code with either: it was written from the mathematics
  and the format, before its authors had read any of their code, and it imports nothing
  of either.
- **Mathematics and format.** All three follow the same reduction (lemma N0’s fold, bins
  and per-bin domain, and the quarter-turn quadrant) and the same reading of the format
  (`SPEC.md` section 2: corners `[x0, y0, x1, y1]`, mass split evenly over the $D_4$
  images). A misreading shared by all three would not be caught by any of them.
  Two things here bear on that: the reduction is re-derived above from first principles,
  and this review’s evaluator reproduces the source checker’s logged exact control
  captures digit for digit (all 31 oblique witnesses), which a different reading of the
  corners or the split could not do.
- **Authorship.** The source’s commit names Claude as co-author; this review’s programs
  were written by a Claude agent.
  The overlap is at the system family, with separate prompts and separate code.

## Findings

No finding is blocking or major.
Paths are the source’s, at `23e3186`, under
`problems/square-lower-bounds/certificates/mixed_n31_L59775/` (retained in the packet’s
`square-packing/` and `release/` trees).

**M-1 — minor. `README.md` line 15 names a control log that does not exist.** It lists
`check2/control.json, check2/control.jsonl.gz`; the log in the release asset is
`check2/control-197_200.jsonl.gz`. A reader following the README cannot find the file.

**M-2 — minor. `files-sha256.json` line 2 gives the README’s sealed digest.** It lists
`README.md` as `3e302ff4…`, the edition inside the sealed bundle; the published
`README.md` is `6dbab236…`, because the pre-publication paragraph (line 54) was added
after the manifest.
So the published directory’s manifest does not verify its own README.
Every other digest matches (the custody check above).

**M-3 — minor. `check2/receipt.json` line 90 calls the check “an independent
second-system check”.** It is independent of the search code, as the line goes on to
say, but the verifier is this repository’s `sqverify_fast` with one change (line 89). A
reader of the receipt alone could take it for a second implementation beside
jlevy/squares’ verifier.
It is not, which is why a replay here with `sqverify-fast` is recorded as sharing the
producer’s components.
The README’s line 12 has the same word.

**N-1 — note. The certificate proves the strict bound.** No packing fits at side exactly
$L$ (`README.md` line 3), so $s(31) > 2391/400$; line 5 and the record state $\ge$,
which is what a lower-bound entry means.
Nothing to change.

**N-2 — note. The source’s control is sampled and 1.5% below the threshold.**
`check2/control.json` scales every mass by $197/200$ at 32 directions.
Its 31 oblique refusals carry exact witnesses, and its axis refusal is the sweep’s value
with no exact flag; this review evaluated all 32 exactly, and every refusal is genuine
(the logged poses, above).
Such a control shows that the check is not vacuous.
It does not show sharpness, and it is not the whole-net control (the $99/100$ mutant at
every direction) the route requires, which the records lane’s census runs.

**N-3 — note. The source’s two complete runs are of an unreviewed build.** Their build
source `ab6e33e1…` is the source’s adaptation, pinned and unopened here.
Only the census with the reviewed `d97758bb…` can carry a rung, as the entry already
says.

**N-4 — note.
The margins are wider than the logs suggest.** The source’s least certified
bounds go down to $1 + 2.3 \times 10^{-11}$ (direction 676). That is where its branch
and bound stopped, not how tight the certificate is: this review found least captures
(exact, at a leaf centre) from 1.000116 to 1.00215 over the sample, with median 1.00096,
and 1.0010 at direction 676. The real slack is about $1.2 \times 10^{-4}$ at the
tightest sampled direction (1841), below $5 \times 10^{-4}$ at five of the 122, and
about a thousandth at a typical one; directions 1820 to 1861 are the tightest region the
sample found.

**N-5 — note. `README.md` lines 48–49 compare CPU-hours with wall time.** They set the
earlier bundles’ “about 24 CPU hours per certificate” beside “minutes per certificate”
for the second-system check.
This check took 21,625 direction CPU-seconds, about six CPU-hours, which is 36 minutes
of wall only at 12 threads (`check2/receipt.json`), and 7,277 s on the pre-publication
machine. A replay’s price is its CPU.

**R-1 — note, for the records branch.
The entry’s pending-review clauses.** In the entry the records branch registers (T-232),
the `next_rung`, `unfinished_confirmations` and `notes`, and in the reported evidence
entry the `limitations`, say that a review that reads this certificate is pending.
Once this review is mapped they should say it is retained, and the entry derives `C1`
(`record-changes.md`). The claim, the composition and `n-031.md` are otherwise accurate
in every number checked: the mass and its gap, the net’s premises and margins, the gains
of $1/40$ and $3/400$, the interval $2381/400 \le s(31) \le 6$ of width $19/400$, and
the diagnostic’s eight directions.

## Questions for the Author

1. Would you correct the control file’s name in the README (M-1) and either regenerate
   `files-sha256.json` after the pre-publication paragraph or say that it describes the
   sealed bundle (M-2)?
2. Could the check2 receipt say that it is independent of the search and is
   jlevy/squares’ `sqverify_fast` with the declared-net change (M-3), so that no reader
   counts it as a second implementation beside this repository’s verifier?
3. Your search must have aimed at some least capture over the net.
   This review finds as little as $1.2 \times 10^{-4}$ of slack, at direction 1841
   (N-4). Is that the margin the search targeted, and is the least capture over all
   2,073 directions recorded anywhere?
4. How many threads did the pre-publication run use?
   Its receipt gives 7,277 s and no thread count.
5. Would you consider a control closer to the threshold, for instance every mass scaled
   to just below one over the least capture found, or the $99/100$ mutant at every
   direction, as this repository’s route runs?
   The $197/200$ control at 32 directions shows the check is not vacuous but says little
   about where the certificate is tight (N-2).

## Rungs and Significance

**Now.** The entry is `V0/C0`. With this review recorded as the `external_review` of the
reported entry (state `informally-verified`) and listed in the entry’s `reviews`
(`kind: adversarial`, verdict `accepted`), the entry derives `V0/C1`: a read of a
recorded claim.
This review’s sample is evidence of its own, cited by the case record and
not by the entry, because a sample sets no rung.

**Once the census and its controls pass.** A complete `sqverify-fast` capture at all
2,073 directions from the retained candidate, with a `CONTROLS_REFUSED` receipt for the
whole-net controls (the $99/100$ mutant at every direction, FC-1, each coverage refusal
an in-domain pose checked apart from the crate), registered as replay evidence
(`replayed-here`, interval-certified, passing, with its control path), supports `V3/C3`.
Every item of the 6 October checklist that concerns the file, the premises and the
mathematics holds for this certificate (items 1, 3 and 7: format M with no points,
`proof_net` with exactly `step` and `last`, no top-level `net` key, the densest row
$386{,}421 \le 2^{32}$, lemma N0’s (a) to (e) in exact arithmetic apart from the crate,
and this review). Items 2, 4, 5, 6 and 8 concern the census’s receipts and words.
The confirmation would read *confirmed, re-implemented sharing the producer’s
components* (the crate), with beside it: *sampled, 122 of 2,073 net directions,
independently re-implemented (clean-room), by a Claude agent, a system family the
producer also used*. `V4/C4` would further need a second adversarial AI review by a
distinct reviewer and a human oversight record.

**Significance: S3, confirmed.** The result, if correct, is the strongest lower bound on
record at $n = 31$, $1/40$ above the standing lanes, and it more than halves the gap to
the upper bound. It uses the certificate kind and the declared net of T-132, T-142 and
T-143, with no new technique, so it is a substantive case result (S3), as those are; not
a reusable technique or bound family (S4), and $n = 31$ is not a central open case (S5).
The PR label is `S3`. No News item is owed; an optional draft is in `record-changes.md`.

## Reproduction

Every program ran with `packing/.venv/bin/python3 -I` (CPython 3.14.7, numpy 2.5.2) at
`nice -n 19`, one process at a time, on the shared four-core Linux host whose load
average stood between 9 and 39. The commands, from the programs’ directory, are in its
[README](../../../packing/resources/web/wand125-fine-net-n31-2026-10-11/review/review-2026-10-23/README.md#how-to-run-them),
and every output is under its `outputs/`. CPU, by program:

| Run | CPU-seconds |
| --- | ---: |
| `premises.py`, `net.py`, `geometry_selftest.py`, `sample_plan.py` | 3.3 |
| `capture.py`, the sample: 122 directions in two invocations | 1,909.7, and at most 9 more for direction 319’s lost first attempt |
| `capture.py`, the nine mutant runs | 10.6 |
| `source_log_points.py` | 3.2 |
| `bound_selftest.py` | 10.6 |
| Development trials of earlier drafts of `capture.py` (11 runs, deciding nothing, not retained) | about 330 |
| Total | about 2,270 (0.63 CPU-hours) |

The custody checks used `sha256sum`, `git ls-tree` and `gh api` against
wand125/square-packing at the pin: the four retained documents’ Git blobs equal the
commit’s, the release asset (id 629390758) is 631,670 bytes with SHA-256
`50b1cf3f…0a58`, and its six data members equal the packet’s copies.
The two pinned archives in it were streamed to a digest without being unpacked
(`e495f9bf…` and `b88c5003…`, as pinned), and the download was deleted.
No tracked file changed in any worktree; `git status` of the reference checkout is
clean.

## Earlier Reviews

No earlier review of this certificate exists.
The only documents under `docs/project/reviews/` that name it are two tracker
dispositions of 13 October (`review-2026-10-13-owner-decisions-applied.json` and
`-n17.json`), which keep the import’s bead open and do not read the certificate; they
were read after the findings above were written.
The reviews this one read first are of other results and of the maintained crate, and
are listed under [What Was Read](#the-claim-and-what-was-read).
On this route, the 6 October review of ten check2 certificates (T-102 to T-111, which
include the first certificates on this 1/5002 net) reached the same reading of lemma N0
and the per-bin domain; this review re-derived both without relying on it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
