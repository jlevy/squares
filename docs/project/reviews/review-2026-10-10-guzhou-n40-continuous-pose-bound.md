# Guzhou0806’s `s(40) > 1340000/199529`: Review of the Continuous-Pose Kernel on wand125’s `rect_n40_L67`

**Verdict: no blocking defect in the mathematics or in the kernel.** The argument from
wand125’s rectangle density to the strict bound
$s(40) > 1340000/199529 = 6.7158157\ldots$ is correct as `PROOF.md` states it, every
exact premise it states holds, and every number in it was recomputed here in exact
rationals with code written for this review.
The step that carries the proof is new to this record: a 195-line C++ kernel that covers
the three-dimensional pose domain, centre and half-angle tangent together, by interval
branch and bound, in 43 closed slabs over $t = \tan(\theta/2) \in [10^{-6}, 83/200]$,
with a separate exact certificate for horizontal squares that covers
$t \in [0, 10^{-6}]$ by containment.
The kernel was read line by line against the lemmas it rests on, built here into the
byte-identical binary of the release’s CI run, run 98 times on synthetic densities whose
least capture is known in closed form, where it refused every threshold above the true
minimum and never accepted one, and replayed on three of the 43 slabs, which reproduced
the release’s receipts field for field.
The near-axis certificate was decided a second way with this repository’s
`sqverify-fast` on the original density, and the same crate verified the nodal statement
at the new parameters at all 401 directions of the finer net, a necessary condition the
claim passed. The bound stands as the source’s report until the records lane’s complete
replay passes; this review names what that replay must show, and what no first-party
route decides.

Eight findings are recorded, none blocking for the claim.
One, GC-4, says where the first-party tooling stops: `sqverify-fast` refuses a threshold
below one, so every nodal cross-check here ran on the density scaled by $5000/4999$, and
nothing in this repository decides the continuous cover itself; a first-party kernel is
a W7 slice, and this review is its specification.
The draft significance `S3` is suggested by the precedent of `T-133`, with the note that
the technique is new to this record and makes the net, the transfer and the density peak
unnecessary.

This is the mathematical lane of the stage 4 import of the issue 485 follow-up
(`think-xms6`), written on 2026-10-10 by an AI agent (Claude, model Fable 5.1, maximum
thinking effort), prompted separately from the records lane, before any complete replay
here and before retention.
It registers nothing and moves no bound; the register entry is `T-NNN`, to be assigned,
and `T-133` keeps its claim.

## Scope and Evidence

The subject is the claim of Guzhou0806’s comment of 2026-10-10T14:50Z on
[jlevy/squares#485](https://github.com/jlevy/squares/issues/485#issuecomment-6098734391):
source [Guzhou0806/n40-square-packing](https://github.com/Guzhou0806/n40-square-packing)
at `71c97d07553d7d5ff5c5c82f0c9d1c75a150a4e3`, committed 2026-10-10T14:30:28Z, a
descendant of the `T-133` pin `e5abeb4d`, which the tag
`n40-continuous-1340000-199529-20261010` names; release ZIP
`n40-continuous-1340000-199529.zip`, 129,976 bytes, SHA-256
`78d693ae5bd08cc3065348c6593c2bec36412bebe48eb2f744786dc115bba26f`, published
2026-10-10T14:49:22Z from GitHub Actions run 38059878931 (`success`, `head_sha`
`71c97d07`, 14:30:32Z to 14:47:05Z).

**Read in full.** The comment, the release notes, the tree’s 28 files: `README.md`,
`PROOF.md`, `VERIFICATION.md`, `REPRODUCIBILITY.md`, `SOURCES.md`,
`certificate/parameters.json`, `verifier/continuous_pose.cpp`,
`verifier/axis_integer_grid.cpp`, `verifier/exact.py`, `verifier/run.py`,
`verifier/audit.py`, `tests/kernel_harness.cpp`, `tests/rounding_harness.cpp`,
`tests/oracle.py`, `tests/test_kernel.py`, `tests/test_admission.py`, the workflow,
`results/verification.json`, `results/slabs.jsonl` and `results/axis.json`, in both the
tree at the pin and the ZIP; this repository’s `T-133` entry, the
[10 October review of T-133](review-2026-10-10-guzhou-n40-clipped-corner-bound.md),
`result-import.md` (stage 1), `sqverify_fast/src/main.rs` (the flags) and
`certificate.rs` (`admit`, the format T metadata net and the threshold), and
`sqpack.rectangle_density` (`coverage_at_point`, `exact_intersection_area`).

**Not opened.** The log of run 38059878931; only its conclusion, head and times were
read through the API. No checker of wand125’s or Tokoharu’s.

**Ran.** Everything in a scratch directory outside the tree, with the two untrusted
downloads in directories of their own, every script written here under `python3 -I`
(3.13, standard library only) except the release’s own oracle test, and nothing from the
downloads imported except that test’s three files, read in full first; at most two
processes at a time.
Scripts: `exact_checks.py`, `capture.py`, `synthetic_tests.py` (three parts),
`capture_search.cpp`, `confirm_poses.py`, `confirm_argmins.py`, `make_crate_inputs.py`,
`receipts_summary.py`, `net401_summary.py`, `replay_slabs.sh`.

| # | Command | Result |
| --- | --- | --- |
| 1 | `gh release download`, `sha256sum`; `gh api` on the comment, release, tag and run | the ZIP’s digest and size are the comment’s; tag → `71c97d07`; run `success` on that commit |
| 2 | `git clone`, `checkout --detach 71c97d07` | 28 files; `e5abeb4d` is an ancestor |
| 3 | `diff -r` ZIP against tree; `sha256sum -c SHA256SUMS` in both | identical except `results/verification.json`, `results/slabs.jsonl`, `results/axis.json` and `SHA256SUMS` (GC-3); all 27 listed digests hold in each |
| 4 | `sha256sum certificate/certified_candidate.json` against the retained `rect_n40_L67` | `71011d03…` both: the density is the retained one, byte for byte |
| 5 | `exact_checks.py`: the D4 expansion from the eight maps on points, both kernel inputs regenerated, every enclosure checked, every scalar below | 480 rows, 3,840 terms, 3,792 distinct, invariant under all eight maps; pose input SHA-256 `ccf7b68a…` and axis input `d57e8bb2…`, the release’s constants; every line of the scalar table holds |
| 6 | `g++ 13.3.0` with the release’s flags, from the tree’s directory | pose binary `69bc9e64…` and axis binary `cccecb9a…`: byte for byte the CI run’s; from an absolute path the pose binary differs (`__FILE__` in `assert`) |
| 7 | `rounding_harness`: 1,000,008 inputs | `PASSED`, as both receipts |
| 8 | the kernel on slabs 0, 42 and 1 (`[1,500]`, `[410000,415000]`, `[500,10000]`) | nodes, leaves, bounds, classification counts, depth and angle splits identical to both receipts; 21.3 s, 57.7 s, 86.9 s against the receipts’ 22.1, 55.6, 87.5 |
| 9 | 98 kernel runs on synthetic densities with closed-form least capture (below) | 53 refusals, every one where the true minimum lay below $\tau$; 28 acceptances, every one where it lay above; 17 budget exhaustions, never an acceptance; no false acceptance |
| 10 | the release’s `tests/test_kernel.py` | `PASSED_FINITE_ORACLE_TESTS`, 160 cases, 4,014 poses, 3,568 areas, stdout digest `9b95b293…` as the local receipt |
| 11 | `confirm_poses.py`: the review’s exact clipper on the dominated integer measure at the axis minimiser | $249950896232809301864786207/25 \cdot 10^{25}$ exactly, the axis kernel’s value |
| 12 | `sqverify-fast` (`567a0fd5…`, the reviewed build) at direction 0, side $A$, density $\times 5000/4999$, threshold 1 | `verified`, least certified $1.0000037044548487$ over 4,897,369 vertices, argmin $(2103865688632621/5 \cdot 10^{14},\ 12402357/2 \cdot 10^6)$; exact capture there $0.9998037038\ldots$ |
| 13 | the same at side $B$, direction 0 | `verified`, least certified $1.000091413240477$; exact capture at its argmin $0.9998913951\ldots$ |
| 14 | the same at side $B$, all 401 directions of the $83/80000$ net, two threads | `VERIFIED`, 401 of 401, least certified $1.000000000357051$ at $r = 289$, 32,763,798 boxes, 171 s |
| 15 | `capture_search` (float, grid up to $100^3$ and $4000 \times 2 \times 11$, coordinate descent) | least found $0.9999908$ at $t = 0$ on the top edge; a rugged landscape (two dips $3 \times 10^{-4}$ apart in $x$), so the exact sweeps of items 12 and 13 are what decide the axis minima |

What failed along the way: the review’s first closed form for the cut cases used the
triangle regime where the strip regime applied, which mislabelled two correct
acceptances in slab 0, and one gap case was labelled with the wrong expectation; both
were errors in the review’s tests, found and corrected, and the counts above are from
the corrected runs.
Several commands were refused by the session’s sandbox and moved into
script files. Nothing the brief asked for went unestablished.

## The Claim

Let $s(40)$ be the least side of a square that holds forty closed unit squares with
pairwise disjoint interiors, any rotations, boundary contacts allowed.
The release claims

$$
s(40) > X = \frac{1340000}{199529} = 6.715815746082023\ldots,
$$

an increase of exactly $72586117/9976450000 = 0.0072757\ldots$ over `T-133`’s
$335427/50000$, from the same certificate.
It is not a packing, an optimality claim or a priority claim; the release says so, and
says that wand125’s review on the issue covers $6.70854$ only.
The density is wand125’s `rect_n40_L67`, unchanged: the retained
`certified_candidate.json` of the 2026-10-01 packet decompresses to the SHA-256
`71011d03…` the release pins (item 4), so this is a second extension of a certificate
the record already holds, not a new density.
Nobody else holds the value; the register’s strongest lower bound at $n = 40$ is
`T-133`’s.

## The Argument From Certificate to Bound

Notation, all exact rationals: $L = 67/10$, $K = [0, L]^2$, $B = 199529/200000$,
$M = 3999/100$, $\tau = 4999/5000$, $A = 997643/10^6$, $\varepsilon = 10^{-6}$,
$T = 83/200$, $X = L/B$; for $t = \tan(\theta/2)$, $c = (1 - t^2)/(1 + t^2)$,
$s = 2t/(1 + t^2)$, $W = c + s$, $E(t) = L/2 - BW(t)/2$.

**1. The density.** The 480 positive-weight rows expand through the eight symmetries of
$K$ with density $w/(8|R|)$ per image into 3,840 terms, a $D_4$-invariant $g \ge 0$ with
$\int g = M$. Recomputed here (item 5) from the eight maps on points: 480 rows, 3,840
terms, 3,792 distinct, the multiset invariant under each map, $\int g = M$ from the
terms. The kernel’s input is these 3,840 terms, unmerged, each coordinate and density as
a pair of binary64 hexadecimal floats that bracket the rational, $L$ likewise and $B$ as
17-digit decimals; regenerated here with enclosures computed independently, its SHA-256
is `ccf7b68a…`, the constant `exact.py` binds the receipts to, and every one of the
19,202 enclosures in the file brackets its rational.
So the measure the kernel decided is the retained certificate’s, and nothing else.

**2. The reduction.** Each square’s capture is invariant under the eight symmetries of
$K$. The diagonal reflection sends an orientation $\alpha$ to $\pi/2 - \alpha$ (modulo
$\pi/2$), so every square’s capture equals that of a square at some $\theta \in [0,
\pi/4]$; the quarter-turns about the centre of $K$ preserve the orientation modulo
$\pi/2$ and carry the centre into the closed northeast quadrant.
`PROOF.md` is right to use only quarter-turns for the centre: the axis reflections also
flip the orientation.
One square at a time, with no claim that the transformed squares pack.
With $\theta \in [0, \pi/4]$, $t \in [0, \sqrt2 - 1]$, and $T = 83/200$ exceeds
$\sqrt2 - 1$ because $T^2 + 2T - 1 = 89/40000 > 0$. The legal centres of a side-$B$
square at $\theta$ are $[BW/2, L - BW/2]^2$ (its bounding box inside $K$); in the
quadrant, $x = L/2 + uE(t)$, $y = L/2 + vE(t)$ with $(u, v) \in [0, 1]^2$, and $E > 0$
since $L > B\sqrt2$. The domain to cover is $[0,1]^2 \times [0, \sqrt2 - 1]$ in
$(u, v, t)$, closed; the slabs cover $t \in [10^{-6}, 83/200]$ and the patch covers
$t \in [0, 10^{-6}]$, meeting at the point.
Correct.

**3. The interval kernel.** Each node is a box $[u \pm d_u] \times [v \pm d_v] \times
[w \pm d_w]$ of dyadic coordinates, $t = t_0 + (t_1 - t_0)\,w$ for the slab
$[t_0, t_1]$, the root $[0,1]^3$. For the box, `direction` encloses $c$, $s$ and $W$:
$c$ decreases and $s$ increases on $(0, 1/2]$, so their values at the endpoints bracket
them; $W$ increases to $t = \sqrt2 - 1$ and decreases after, since
$W' = -2(t^2 + 2t - 1)/(1 + t^2)^2$, so its endpoint values bracket it unless the
critical point may lie inside, in which case the upper bound is
$1414213562373096/10^{15}$, whose square exceeds 2 (recomputed), and the lower bound is
still an endpoint value because $W$ is unimodal.
Correct, and the asserted range $0 < t \le 1/2$ holds in every slab.
From these, $E$, the centre $(x_c, y_c)$ at $(u, v)$ and the ranges $X, Y$ of the whole
box are intervals, all outward.

Every interval operation first rounds to nearest and then steps each endpoint one
representable neighbour outward by integer arithmetic on the IEEE encoding, with zero,
infinity and NaN handled apart; under round-to-nearest the true result of a basic
operation lies between the neighbours of its rounded value, so each operation encloses,
products take the four endpoint products, and division asserts a denominator interval
not containing zero (here $s \ge s(10^{-6}) > 0$ and $c \ge 3/5$). The stepping was
checked against `nextafter` on 1,000,008 inputs (item 7), which shows the stepping and
nothing about enclosure; enclosure follows from round-to-nearest, which `main` asserts,
and from the absence of flush-to-zero and denormals-are-zero, which it asserts on the
MXCSR. The build forbids `NDEBUG` and `__FAST_MATH__` by `#error`, passes
`-fno-fast-math -ffp-contract=off`, and x86-64 evaluates in SSE2 without excess
precision; so no fused multiply-add and no x87 rounding enters.
Compared with `-O3` under GCC 13.3 and 15.2, the release’s two runs and the three slabs
replayed here agree in every count, which is what determinism under those flags
predicts.

**4. Whole-box classification.** For each still-active rectangle, a floating screen
proposes containment or exclusion, and only an interval test decides: the rectangle’s
centre offset projected on the square’s two normals, $U = |c\,r_x + s\,r_y|$,
$V = |{-s}\,r_x + c\,r_y|$, and its projected half-widths $W_U = c h_x + s h_y$,
$W_V = s h_x + c h_y$, over the whole box; it is inside the square for every pose in the
box when $(U + W_U)^{\uparrow} \le (B/2)^{\downarrow}$ on both axes, and then its full
mass $(\rho |R|)^{\downarrow}$ joins the constant term; it is outside for every pose
when $(U - W_U)^{\downarrow} \ge (B/2)^{\uparrow}$ on either axis, a separating axis,
and then it is dropped.
A rectangle outside the square’s bounding-box range over the whole box is dropped first.
Children inherit the constant and the active list, and their parameter sets lie inside
the parent’s, so the invariant holds by induction.
Correct, and the $10^{-10}$ tolerances in the screen decide nothing (GC-6).

**5. The centre integral.** At the box’s centre parameters $(u, v)$ the centre
$(x_c(\theta), y_c(\theta))$ still varies with $\theta$; `area_lower` takes the relative
inner rectangle $[a^{\uparrow} - x_c^{\downarrow},\ d^{\downarrow} -
x_c^{\uparrow}] \times [\ldots]$, inside the true one for every $\theta$ of the box, and
bounds $\int \max(0, \tilde f)$ over it, where $\tilde f(\xi) = \min(e', (h - c\xi)/s,
(h + s\xi)/c) - \max(b', (-h - c\xi)/s, (-h + s\xi)/c)$ is the clipped vertical section
of the square at relative abscissa $\xi$: the lower envelope of affine functions less
the upper envelope, hence concave, so on each segment between consecutive knots the
chord lies below it, and $\int \max(0, \tilde f) \ge \max(0, \int \text{chord})$. The
knots are floating heuristics and only their sorted positions matter; each chord
endpoint is the interval lower bound of $\tilde f$ over the box’s $c, s$ and $h$,
computed with the correlated numerators subtracted before division, so the bound holds
at every angle of the box without sampling it.
Each segment’s contribution is the trapezoid when positive and zero otherwise, all
rounded down. Correct, and missing or spurious knots lose sharpness only, as `PROOF.md`
says. The capture at the centre is then $f_0 = \sum \rho^{\downarrow}\,
\text{area\_lower}$, a lower bound for every $\theta$ in the box.

**6. From the centre to the box.** With $F(x, y, \theta)$ the capture from the active
rectangles, $\partial F/\partial x = \sum_r \rho_r (\ell_r(a_r) - \ell_r(d_r))$ where
$\ell_r(\xi)$ is the vertical section of the square at the line $x = \xi$ clipped to
$[b_r, e_r]$, by Leibniz on $\int_{a - x}^{d - x}\ell\,d\xi$; `slice_correlated`
encloses each section over the whole box (centre ranges $X, Y$, edge intervals,
$c, s, h$), the $y$-derivative by the same function with $c$ and $s$ exchanged, which is
the right formula for horizontal sections (re-derived).
$F$ is Lipschitz in the centre, so at fixed $\theta$,
$F(x', y', \theta) \ge F(x_c, y_c, \theta) - |x' - x_c|\,G_x - |y' - y_c|\,G_y$ along an
L-shaped path in the convex centre box, with $G_x = |f_x|^{\uparrow}$ and
$|x' - x_c| = |u' - u|\,E(\theta) \le d_u E^{\uparrow}$. Hence every pose in the box
captures at least $\text{base} + f_0 - d_u E^{\uparrow} G_x - d_v E^{\uparrow} G_y$,
rounded down at each step, and a box closes only when this reaches
$\tau^{\uparrow} = \mathrm{up}(\mathrm{fl}(4999/5000)) = \tau + 1.33 \times 10^{-16}$.
Rectangles dropped in item 4 contribute nothing to $F$ anywhere in the box, so nothing
to its derivatives. Correct.

**7. Subdivision and termination.** An unclosed box is bisected in one normalised
coordinate, chosen by a heuristic that compares the angle loss against the two
translation terms; the children are closed and cover the parent exactly, and every
coordinate stays a multiple of $2^{-41}$, exactly representable (recomputed: $d \ge
2^{-40}$ is checked before a split).
The run ends `verified` only when the stack is empty; a half-width below $2^{-40}$ or
the node budget exits 3 with `unresolved`, and `exact.py` refuses anything but
`verified` with `nodes = 2\,\text{leaves} - 1`. So an accepted slab is a finite closed
cover of $[0,1]^3$ by boxes each of which the bound of item 6 closed.
The receipts: 61,860,927 nodes, 30,930,485 leaves, 14,096,668 angle bisections, greatest
depth 54 (slab 0), the largest slab 6,319,087 nodes (slab 1,
$t \in [5 \times 10^{-4}, 10^{-2}]$), the least leaf bound
$2251349454150741/2^{51} = 0.99980000019\ldots$, $1.9 \times 10^{-10}$ above $\tau$,
which is where subdivision stopped and says nothing about the true minimum (item 15).

**8. The near-axis patch.** For $t \in [0, \varepsilon]$, $W$ increases, so
$AW(t) \le AW(\varepsilon) \le B$, recomputed: $B - AW(\varepsilon) =
589499411/125000000000125000 = 4.72 \times 10^{-9} > 0$. The horizontal side-$A$ square
concentric with a legal side-$B$ square at angle $\theta$ lies inside it, because its
corners project on each normal to at most $AW/2 \le B/2$, and inside $K$ because
$A \le BW$; $g \ge 0$ gives $\int_{Q_B} g \ge \int_{Q_A} g$. The axis kernel decides
$\int_{Q_A} g_- \ge \tau$ for every legal horizontal side-$A$ square, where $g_-$ is the
dominated measure: supports moved inward to the $10^{-9}$ grid, densities floored to
$10^{-9}$, so $g_- \le g$ pointwise and $\int g_- = M - 4.1 \times 10^{-6}$ (recomputed,
3,840 rows, none dropped; its quarter-turn invariance, which the quadrant reduction for
$g_-$ needs, checked).
The capture of a horizontal square is bilinear on each cell of the grid of the 2,213
breakpoints $\{a, d\} \pm A/2$ per axis inside $[L/2, L - A/2]$, so its minimum is at
one of the $2213^2 = 4{,}897{,}369$ vertices; the kernel writes each rectangle as
sixteen signed hinge products, accumulates coefficient prefix sums and evaluates every
vertex in signed 128-bit integers at scale $10^{27}$, with every accumulation and
evaluation bounded by $16 \sum w\,(l + l + A/2)^2 =
3.84 \times 10^{35} < 2^{125}$ (recomputed; the four evaluation terms sum below
$2^{127}$), and the threshold compared as $\text{minimum} \ge \lceil 10^{27}\tau \rceil$
without multiplying the minimum.
The minimum, $249950896232809301864786207/(25 \cdot 10^{25}) = 0.99980358493\ldots$ at
$(4.207731377, L - A/2)$, was reproduced here exactly by the review’s clipper on $g_-$
at that centre (item 11), and the crate’s exact vertex sweep on $g$ itself at side $A$
found its minimum at the same breakpoint, $0.99980370\ldots$ (item 12). The margin is
$3.58 \times 10^{-6}$ on $g_-$ and $3.70 \times 10^{-6}$ on $g$ (GC-1). Correct.

**9. Counting and the endpoint.** Every legal side-$B$ square captures at least $\tau$;
forty with disjoint interiors capture at most $\int_K g = M$ since $g$ is absolutely
continuous; $40\tau - M = 1/500 > 0$. A packing of forty unit squares in a square of
side exactly $X$ scales by $B = L/X$ to forty side-$B$ squares in $K$: refused.
With sides in $[1, 7]$, centres in $[0, 7]^2$ and angles in $[0, \pi/2]$ the feasible
set is compact and nonempty, so the least side is attained, and attainment at
$s(40) \le X$ would give a packing in a container of side exactly $X$. Hence
$s(40) > X$. Correct, as in the `T-133` review.

**What the new kernel changes.** `T-133` needed a 401-direction net, a concentric
reference at a neighbouring node, the clipped-corner area bound and the density’s
essential supremum, and lost $3.1 \times 10^{-4}$ of capture to the transfer; this
argument has no net, no transfer and no peak, and spends the whole margin on the smaller
side: $B$ falls from $9977/10000$ to $199529/200000$ and $\tau$ from $10001/10000$ to
$4999/5000$. The exact minimum over horizontal side-$B$ squares is $0.99989140\ldots$
(item 13), $9.1 \times 10^{-5}$ above $\tau$, and no pose found by search captures less
(item 15); the slack of the whole claim is of that order, concentrated near the axis on
the container’s edges.

## Hypotheses Each Checker Assumes

The continuous kernel (`continuous_pose.cpp`, items 6 to 9):

1. The input is the retained measure: `exact.py` regenerates it from the density file
   whose digest it checks, binds the bytes by digest, and `run.py` re-checks the file
   the kernel read; discharged here by item 5.
2. The geometric lemmas of items 2 to 7: the reduction, the monotonicity of $c$, $s$ and
   $W$, the concavity of the section, the derivative formula, the Lipschitz extension
   and the dyadic subdivision.
   Re-derived above; nothing beyond measure theory and plane geometry is used.
3. IEEE-754 binary64 with round-to-nearest and subnormals, SSE2 evaluation, no fused
   multiply-add, and GCC honouring `-fno-fast-math -ffp-contract=off` at `-O3`; asserted
   at start-up where the program can, refused at compile time where it can, and trusted
   for the rest.
4. All 43 slabs finish `verified` within budget: the receipts show it, three slabs
   reproduced here, and the complete run is the records lane’s.

The axis kernel (`axis_integer_grid.cpp`, item 8):

5. Exact integer arithmetic within the guarded bound, the bilinear-cell lemma and the
   hinge expansion; re-derived, and the reported minimum reproduced here by another
   method on the same measure and by the crate on the original.

The finite checks (`exact.py`; `exact_checks.py` here, written apart from it):

6. JSON decimals are their literal values, read as fractions; Python integers and
   `Fraction` are exact.
   Trusted.
7. The scalar chain: $X = L/B$, $40\tau - M = 1/500$, $T^2 + 2T - 1 > 0$,
   $(1414213562373096/10^{15})^2 > 2$, $L > B \cdot 1414213562373096/10^{15}$,
   $A \le B$, $AW(\varepsilon) \le B$, the 44 endpoints partition $[10^{-6}, 83/200]$,
   the axis minimum and both receipts’ `coverage` and `axis` blocks; every one holds
   (item 5).

The prose (`PROOF.md`): items 2, 8 and 9 re-derived; §6 and §7 state the lemmas the code
uses, and nothing in the proof is assumed that the code does not implement.
`audit.py --check` reads receipts and decides nothing about coverage, as the release
says.

## Trust Boundaries and What the Checkers Share

The continuous kernel is the release’s own; it shares no code with `sqverify-fast`, with
Tokoharu’s `verify.cpp` or with wand125’s checkers, and the release says its
translation-derivative structure follows Tokoharu and its concave-section bound was
informed by this repository’s crate.
It shares with every verifier of this certificate the measure, its $D_4$ expansion, the
container and the counting; a defect in that mathematics would reach all of them.
Within the release, the axis kernel shares nothing with the continuous one but the
measure, and `oracle.py` is a third, exact, finite implementation used only for
regression. The release’s label `REPLAYED_SAME_KERNEL` is exact: its two runs are the
same kernel on two compilers.

Independent of all of them here: the review’s exact clipper (`capture.py`), which shares
no code with the release or with `sqpack`, reproduced the axis minimum and evaluated
every pose the search proposed; and `sqverify-fast`, reviewed on 3 and 6 October,
decided the axis statements and the 401-direction nodal statement on the original
density at the new parameters.
Neither decides the continuous cover.

## Findings

### GC-1 — Non-blocking, robustness: the margin is $3.6 \times 10^{-6}$ at the axis

The near-axis patch holds with $\int_{Q_A} g_- - \tau = 896232809301864786207/(25 \cdot
10^{25}) = 3.58 \times 10^{-6}$ at $(4.207731377, L - A/2)$, and the continuous domain’s
tightest face is the axis, where the least horizontal side-$B$ capture is
$9.1 \times 10^{-5}$ above $\tau$ at $(4.2077324\ldots, L - B/2)$: the
$2 \times 10^{-6}$ of side between $B$ and $A$ costs $9 \times 10^{-5}$ of capture there
(items 12, 13), because the square’s boundary runs along dense strips of the measure.
The chain is sound only in exact rationals and outward intervals, which the release and
this review use; a replay must not round, and any decimal restatement of $A$ or
$\varepsilon$ is a different claim.

### GC-2 — Non-blocking, code: the kernel’s `main` has no `return`

`continuous_pose.cpp` ends `main` without a return; as `main` that is a conforming
`return 0`, and both receipts and item 8 show exit 0. The two harnesses rename it
(`#define main pose_entry`, `continuous_entry`), after which the renamed function
returns nothing on the `verified` path, which is undefined behaviour; neither harness
reaches that path (`kernel_harness` never calls it; `rounding_harness` runs it with a
budget of one node and expects exit 3). A `return 0;` costs nothing and belongs in the
author’s next release.

### GC-3 — Non-blocking, record: the release ZIP is not the pinned tree

As with `T-133`: the tree’s `results/` holds the local run (`source_commit` null,
binaries `a5dcfa3e…` and `051e306d…`, GCC 15.2.0, Python 3.14.4, 510.96 s), the ZIP’s
the GitHub Actions run (`source_commit` `71c97d07…`, binaries `69bc9e64…` and
`cccecb9a…`, GCC 13.3.0, Python 3.12.3, 983.95 s); `SHA256SUMS` differs in those three
lines, and `audit.py --package` writes it so.
Every non-timing field of the 43 slab outputs and the axis output is identical between
the two, and the comment describes the ZIP correctly.
The packet should retain both receipts and say which is which; the ZIP’s binaries are
the ones a build on this host reproduces (item 6).

### GC-4 — Non-blocking, first-party tooling: nothing here decides the continuous cover

`sqverify-fast` refuses a threshold below one, so the nodal statements at
$\tau = 4999/5000$ reached it only as “capture $\ge 1$” of the density scaled by
$5000/4999$ (mass $199950/4999 < 40$, admitted as format T with the metadata net); that
is the same statement, exactly, and the contract below is written that way.
The crate decides the axis statements (items 12, 13) and the 401-direction statement
(item 14), which is a necessary condition of the claim and not the claim.
A first-party decision of the continuous cover needs an interval kernel with the angle
as an interval dimension: the crate’s rotated branch and bound at a fixed direction,
plus the enclosures of $c$, $s$ and $W$ of item 3, the $t$-dependent centre domain, and
either the section–derivative bound of items 5 and 6 or a bound of its own; the 195
lines read here are its specification, and this is a W7 slice with a budget the owner
sets.

### GC-5 — Non-blocking, sharpness: the budget is part of the contract

On synthetic densities (item 9) the kernel refused every threshold above the true
minimum, by $10^{-12}$ relative and more, exiting `unresolved` at the width floor or at
the budget, and it never accepted one.
What it can close depends on the density: the cut densities with a margin of $10^{-4}$
relative closed in at most 252,000 nodes, the right cut on slab `[200000,210000]` closed
at $10^{-6}$ in 1.3 million, the uniform density on $K$ exhausted 3 million nodes at
$10^{-6}$ and $10^{-9}$ on three slabs, and the gap density closed within 1.5 million
nodes only on slab `[400000,410000]`, at $1.2 \times 10^{-4}$ and above; a rectangle
larger than the square, or an edge through the square’s middle, makes the angle
enclosure or the derivative term cost more than the margin until the box is small.
This is why the real run splits the angle 14 million times and why slab 1 needs 6.3
million nodes; a replay must keep the full budget of 30,000,000 nodes per slab, and a
budget exit is `unresolved`, never an acceptance (checked: exit 3 at every exhaustion).

### GC-6 — Non-blocking, confirmed: no floating heuristic decides acceptance

The $10^{-10}$ screens in `classify`, the midpoint directions in `set_frame`, the knots
in `area_lower`, the angle-loss estimate that picks the split and `mid()` everywhere
were each traced: they choose what to attempt or where to split, and every acceptance,
containment and exclusion is an interval comparison with outward rounding.
`PROOF.md` §5 and §7 say so, and the code agrees.

### GC-7 — Non-blocking, robustness: NaN is not propagated through `min_element` and `std::min`

A NaN in the second argument of `std::min` or after the first element of `min_element`
is dropped rather than propagated, so an overflow in an intermediate product could in
principle lose its infinity before the final `isfinite` assertion.
It cannot arise on this input: every coordinate is bounded by $L < 10$, every density by
the essential supremum $2818.72$ of the `T-133` review, and every divisor by
$s \ge 2 \times 10^{-6}$ and $c \ge 3/5$, so no intermediate exceeds $10^{9}$ in
magnitude. A note for the author; not a defect of the proof.

### GC-8 — Non-blocking, scope of the controls: what the release’s tests show

The 1,000,008-input test shows the bit stepping equals `nextafter`, not that the
arithmetic encloses; the 160 oracle cases show the per-box bound lies below the exact
capture at 4,014 sampled poses, not that it does everywhere; the wrong-rounding, FTZ,
`NDEBUG` and fast-math controls show the guards fire; the synthetic and budget controls
show `unresolved` is an exit.
They are regression controls, as `VERIFICATION.md` says, and the review’s 98 closed-form
cases are of the same kind, finer and adversarial; none is a second decision of the
cover.

## The Replay Contract

What the records lane must run, and what each run must show, for the status to move from
reported. Every number is from the release’s receipts and was reproduced here where the
row says so.

**0. Retention.** The tree at `71c97d07` (28 files, `SHA256SUMS` holding) and the ZIP
`78d693ae…` with its CI receipts, both receipts named for what they are (GC-3); the
comment cited as text.
The density is already retained in the 2026-10-01 packet and the earlier release in the
`T-133` packet.

**1. The derived inputs,** regenerated first-party from the retained
`rect_n40_L67/certified_candidate.json.gz` (OR-1: `exact_checks.py` is the measurement;
the tool belongs in `devtools`): the pose input, `L` as a hexadecimal pair, `B` as a
17-digit decimal pair, `3840`, then the 3,840 terms in the release’s order (per row:
transpose in `(no, yes)`, then $x$-flip, then $y$-flip), each of the five values as a
hexadecimal pair that brackets its rational; and the axis input, header
`6700000000 997643000 1000000000 1000000000 4999 5000 3840` then the 3,840
inward-rounded integer rows in quarter-turn order.
Their SHA-256 must be `ccf7b68aa89fdcfcf0d78ac135cfa24e4a73b822eb412b2aac46e9c49e2b9925`
and `d57e8bb267dc1a17d57fa0f17f662bf552b6aef46427a0eb9308ae16539ed1cb`; the digests, not
the construction, bind them to the receipts.

**2. The builds,** from the tree’s directory with the release’s flags:

```text
g++ -O3 -std=c++17 -fno-fast-math -ffp-contract=off verifier/continuous_pose.cpp -o continuous
g++ -O2 -std=c++17 verifier/axis_integer_grid.cpp -o axis
```

On Ubuntu 24.04’s GCC 13.3.0 the binaries are
`69bc9e6485102d3636db5377884ba6304f749be94d6ca913d82d80108f1ed4ab` and
`cccecb9ab1ca0ecd88b0994c04ebf7965cf0982b7e400966702da6f7e893265c`, the ZIP receipts’;
another compiler gives other digests and, on this evidence, the same counts.

**3. The axis run,** `axis axis-input.txt`: `AXIS_COVERAGE_PROVED`, 2,213 nodes on each
axis, `minimum_numerator` `999803584931237207459144828`, scale $10^{27}$, minimiser
`4207731377, 6201178500`, `direct_sum_matches`, evaluation bound
`384178892657373682994447839008000000`; under a second.
Beside it, the first-party decision:
`sqverify-fast --candidate axis-A.json --n 40 --side 67/10 --directions 0
--threshold 1 --threads 1 --confirm` on the 480 rows with weights $\times 5000/4999$,
`B` `997643/1000000` and the standard net in metadata (input `379193ff…`): `verified`,
`axis-vertex-sweep`, 4,897,369 vertices, least certified $1.0000037044548487$
(reproduced here).

**4. The 43 slabs,** each `continuous PL PH 1000000 4999 5000 30000000` in a directory
holding `certificate_input.txt`, for the consecutive pairs of
`1, 500, 10000, 20000, …, 410000, 415000`: every slab `verified`, exit 0, and every
non-timing field of its output equal to `results/slabs.jsonl`: in all 61,860,927 nodes,
30,930,485 leaves, 14,096,668 angle splits, least `lower_bound` $0.99980000019017234$ at
slab 1. Price on this host, measured on slabs 0, 42 and 1 at the receipts’ speed: 1,892
CPU-seconds, about 32 minutes on one worker, 16 on two, and the source’s 511 s on four;
the release’s `verifier/run.py --output DIR --workers W` runs them with the fourteen
control stages and writes the same receipts.

**5. Controls,** each of which must refuse:

| Control | Expected |
| --- | --- |
| A. the release’s `synthetic-negative` (uniform density $1/2$) and `limited-budget` (budget 1) | exit 3, `unresolved` (both receipts; reproduced here through item 9) |
| B. uniform density $\rho = \tau(1 - 10^{-9})/B^2$ on $K$, any slab | exit 3 within 100 nodes (reproduced here, three slabs) |
| C. density $\rho$ on $[0, L] \times [0, L - h]$ with $\rho = \tau(1 - 10^{-9})/(B^2 - \text{cut}(t_0))$, the cut $h^2/\sin 2\theta$ or $(B/\cos\theta)(h - B\sin\theta/2)$ at the slab’s left endpoint, e.g. $h = 1/100$ on slab `[500,10000]` | exit 3 (reproduced here, seven slab–depth pairs, both regimes, top and right cuts) |
| D. density $\rho$ off a gap $[0, L] \times [L/2 \pm 1/200]$ with $\rho = \tau(1 - 10^{-9})/(B^2 - B/(100 \cos\theta_1))$, the minimum at the slab’s right endpoint | exit 3 (reproduced here, five slabs) |
| E. C’s densities at $\tau(1 + 10^{-4})$; D’s at $\tau(1 + 3.4 \times 10^{-4})$ on slab `[400000,410000]` | `verified`, exit 0, within 260,000 and 141,000 nodes (reproduced here) |
| F. `wrong-rounding`, `ftz`, `reject-ndebug`, `reject-fastmath` | exit $-6$, $-6$, 1, 1 (both receipts; not run here) |
| G. $A$ replaced by $997644/10^6$ | `exact.py` refuses `NEAR_AXIS_CONTAINMENT`, since $AW(\varepsilon) - B$ would be $10^{-6}$ against a margin of $4.7 \times 10^{-9}$ (not run here) |
| H. $\tau = 1/2$ in the axis header | `AXIS_TEST_REFUSED`, exit 2 (not run here) |

**6. The necessary condition,** `sqverify-fast` on the same scaled rows with `B`
`199529/200000`, `D` `83/80000`, `angle_count` 401 (input `94c3ab2e…`), all directions,
threshold 1: `VERIFIED`, 401 of 401, least certified $1.000000000357051$ at $r = 289$,
32,763,798 boxes, about three minutes at two threads (reproduced here).
A refusal anywhere would refute the claim; a pass does not decide it.

What a complete replay here does and does not give: the continuous cover reproduced with
the producer’s kernel from reviewed source, deterministic across the compilers seen so
far; the axis statement decided twice, once by the producer’s integer kernel and once by
this repository’s crate on the original density; the finite steps decided again by other
code; and the nodal statement at 401 directions as a consistency check.
No second method decides the continuous cover (GC-4).

## Where the Comment, the Release and the Record Differ

- The comment, the release and the receipts agree at every number read here: $X$, the
  raise, $B$, $M$, $\tau$, $A$, $\varepsilon$, $T$, the counting margin, the axis
  minimum and its $2213^2$ vertices, 43 slabs, 61,860,927 nodes, 510.96 s and 983.95 s,
  four workers, the three digests.
- The comment says the ZIP “contains the separate CI receipt”; it contains it in place
  of the tree’s (GC-3), as the earlier release did.
- The comment’s controls (“seven admission-test groups with 29 invalid receipt variants,
  160 finite exact-polygon cases, both IEEE neighbour directions at 1,000,008 inputs”)
  are what the code runs; the counts match `test_admission.py` (19 slab and 10 axis
  variants) and the oracle receipt.
- The release says the kernel “is not a wholly independently sourced second complete
  verifier”, and this review agrees; it is the only verifier of this claim.

## Significance

`T-133` raised $n = 40$ by $0.00854$ with a technique new to the record and was scored
`S3` on the precedent of `T-099`. This claim raises it by a further $0.00728$ on the
same certificate with a second technique new to the record, an interval cover of the
continuous pose domain that dispenses with the net, the transfer and the peak, and that
applies as it stands to every format T certificate the record holds, with the side and
threshold as the only parameters.
`S3` is suggested on that precedent, with the technique noted; the score is the
registering lane’s.

## Disposition

No finding blocks registration as reported or, once the contract’s runs pass, the replay
evidence. GC-3 and GC-4 are retention and wording obligations for the records lane, and
GC-4 names the W7 slice; GC-1, GC-2 and GC-7 are notes for the author, of which GC-2 is
worth a sentence in the reply; GC-5, GC-6 and GC-8 record what was checked.
The reviewer’s own checks are evidence and not a rung: what was proved here is the
reduction, the lemmas the kernel rests on, the patch and the endpoint; what was checked
by computation here is every finite quantity, both derived inputs’ identity, the CI
binaries’ identity, three of 43 slabs, the axis minimum by two other methods, 98
adversarial kernel runs, the release’s oracle test and the 401-direction nodal
statement; what the source reports and this review did not run is the complete 43-slab
run, which its two receipts and its CI run report.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
