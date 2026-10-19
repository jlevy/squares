# Final Review of PR 487’s Lower Bounds: `T-133` and `T-145` at `n = 40`, and the Reported `T-132`, `T-142`, `T-143` and `T-144`

**Verdict: no blocking defect.** Both verified lower bounds at $n = 40$ are correct as
registered: Guzhou0806’s clipped-corner transfer on a 401-direction net proves the
strict bound $s(40) > 335427/50000$ (`T-133`), and his continuous-pose interval kernel
on the same density proves the strict bound $s(40) > 1340000/199529$ (`T-145`), which
supersedes it on both lanes of `n-040.md`. Each argument was re-derived here from first
principles, every finite quantity was recomputed in exact rationals with code written
for this review, the four first-party audits were run again and reproduced their
retained receipts byte for byte, both C++ kernels were rebuilt from the retained source
into the CI run’s binaries and two of the 43 slabs and the axis certificate were
replayed, the reviewed `sqverify-fast` build was rebuilt and reproduced the nodal rows
at the tightest directions, and a refusal control of this review’s own design, on the
real density with an exact witness below the threshold, was refused.
The four reported results `T-132`, `T-142`, `T-143` and `T-144` state their sources’
claims exactly and no stronger, their `V0`/`C0` rungs and `S3` scores are the rubric’s,
their unfinished confirmations are priced as the retained samples price them, and no
case record adopts them.
Six findings are recorded, all non-blocking: record wording and bookkeeping, with the
exact fixes below.

This is lane F1 of the final adversarial mathematical review of PR 487, written on
2026-10-11 by an AI agent (Claude, at maximum reasoning effort), prompted separately
from the import, replay and stage 4 review lanes, with no shared context.
It registers nothing and moves no bound.
For `T-133` and `T-145` it is the second adversarial AI review by a distinct reviewer;
it is not a human oversight record.
Its read of `T-132`, `T-142`, `T-143` and `T-144` covers the record and the intake’s
retained receipts, not the certificates themselves, which are kept outside Git, so it is
not a `C1` read of those four.

## Scope and Evidence

**Claims covered.** `T-133` ($s(40) > 335427/50000$, and the weaker full-core
$s(40) > 67000\sqrt{6400006889}/798988091$), `T-145` ($s(40) > 1340000/199529$), `T-132`
($s(29) \ge 291/50$, reported), `T-142` ($s(28) \ge 2297/400$, reported), `T-143`
($s(30) \ge 2357/400$, reported) and `T-144` ($s(n) \ge 563/50$ for
$n = 122, \ldots, 126$, reported), at `aeb8a7219` on `claude/determined-rubin-yjfy2a`.

**Read in full.** The six register entries and the eleven evidence entries they cite
(`packing/frontier/results.yaml`, `evidence.yaml`); the case records `n-040.md`,
`n-029.md`, `n-028.md`, `n-030.md` and `n-122.md` to `n-127.md`, and the PR’s diff of
`n-0*.md` and `evidence.yaml`; both packets under `packing/resources/web/guzhou-n40-*`
with their READMEs, the two `PROOF.md`, `parameters.json`, both release receipts and
every retained receipt; `verifier/continuous_pose.cpp` and
`verifier/axis_integer_grid.cpp` line by line; the two first-party checkers
`devtools/audit_clipped_corner_transfer.py` and `devtools/audit_continuous_pose.py` in
full with their tests; the releases’ `finite.py` and `exact.py`, read after the
re-derivation was written, as data; the three wand125 packets with their follow-up
records, premises and sample receipts, and `devtools/fine_net_followup.py`’s contract;
`certificate.rs` (`admit`, `domain_upper`, `direction`) and `SOUNDNESS.md` (The Claim,
Reduction of Centres, Direction $r = 0$); the two stage 4 reviews of 10 October;
`epistemics.md`; `results.schema.yaml` and `check_results.py` for
`unfinished_confirmations`; and the beads `think-r333`, `think-i85v` and `think-nd7g`.

**Not opened.** No certificate of wand125’s (the assets stay outside Git), no checker of
wand125’s or Tokoharu’s, no GitHub Actions log, and nothing on the network.

**Ran.** From `packing/` with the project interpreter, scripts under `python3 -I` in a
scratch directory, at most two processes at a time; about five CPU-minutes in all, and
none of the deferred CPU-hour replays of `T-132`, `T-142`, `T-143` or `T-144`.

| # | What | Result |
| --- | --- | --- |
| 1 | `audit_clipped_corner_transfer check --output` | `FINITE_STEPS_HOLD`, 61 checks, controls E–H refused; output byte-identical to the packet’s `receipts/finite-audit.json`; 1.2 CPU-s |
| 2 | `audit_continuous_pose check --output` | `FINITE_STEPS_HOLD`, 61 checks, controls G–G4 refused; byte-identical to `receipts/finite-audit.json`; 1.1 CPU-s |
| 3 | `audit_clipped_corner_transfer check-replay --rank --output` | `REPLAY_HOLDS`, 22 checks, all 400 oblique leaf centres weighed again; byte-identical to `receipts/replay-check.json`; 13.4 CPU-s |
| 4 | `audit_continuous_pose check-replay --output` | `REPLAY_HOLDS`, 65 checks; byte-identical to `receipts/replay-check.json`; 0.4 CPU-s |
| 5 | `rederive.py`, this review’s exact re-derivation (below) | every check holds; 3.1 CPU-s |
| 6 | `g++ 13.3.0` with the release’s flags on the retained kernel sources, from a scratch copy at the upstream paths | `continuous` `69bc9e64…`, `axis` `cccecb9a…`, `rounding` `81f15ab0…`: byte for byte the CI run’s and the packet’s |
| 7 | `axis axis-input.txt` on the input regenerated by `derive` (`d57e8bb2…`) | `AXIS_COVERAGE_PROVED`, minimum `999803584931237207459144828`, minimiser `4207731377, 6201178500`, every field the receipts’; 0.16 CPU-s |
| 8 | `rounding` | `PASSED`, 1,000,008 values |
| 9 | the kernel on slabs 0 and 42, `continuous 1 500 1000000 4999 5000 30000000` and `410000 415000 …` | `verified`, 1,192,309 and 1,428,947 nodes, 596,155 and 714,474 leaves, least bounds `0.999800003966137` and `0.99980000269020575`, depths 54 and 31: every non-timing field the receipts’; 27.1 and 74.3 CPU-s |
| 10 | contract controls B-uniform-1-500, C-cut-right-1-500-h2000, D-gap-1-500, E-cut-right-1-500-h2000 on that build | exit 3 at 92, 9,946 and 29,504 nodes; `verified` at 40,959: as the packet’s receipts |
| 11 | this review’s refusal control: the real density, slab 0, threshold $99994/10^5$, budget 3,000,000, with a witness pose at $t = 10^{-6}$ whose exact capture is $0.9999383$ (item 15) | `unresolved`, exit 3, at the width floor after 538,182 nodes; the box it stopped at is the witness’s region ($u = 0.3008$, $v = 1$); 10.1 CPU-s |
| 12 | the same at $9999/10^4$ and $99985/10^5$ (the exact axis minimum $0.9998914$ lies at $t = 0$, outside the slab) and $99993/10^5$ | `verified` at both lower thresholds within 1.3 million nodes; `unresolved` at $99993/10^5$; 29, 28 and 24 CPU-s |
| 13 | `cargo build --release --locked -j 1` at rustc 1.98.0; `sqverify_fast_census --source-digest` | binary `567a0fd5…`, the reviewed build; source `d97758bb…`, reviewed for declared nets (`910b6b12c`); 22 CPU-s |
| 14 | the crate on the inputs `derive` wrote: `axis-A.json` at direction 0; `net401-B.json` at 0, 289, 400; the `T-133` `derived-401.json` (`49f696a4…`) at 0, 73, 220, 400 at threshold $10001/10000$; control A (weights $\times 99/100$) at 73, 220 | `verified` with least certified $1.0000037044548487$ over 4,897,369 vertices; $1.000091413240477$, $1.000000000357051$, $1.000000048836833$; $1.0012141064171602$ over 4,879,681 vertices, $1.000100000471634$, $1.0001004698611937$, $1.0001000437006502$ with 52,597, 84,159 and 144,685 boxes; control A `REFUSED` at both with exact witnesses: every value the receipts’; 7 CPU-s |
| 15 | `clipper.py`, this review’s exact rational capture of a rotated square against the expanded density (Sutherland–Hodgman, shoelace), at the axis minimisers, at the `T-133` least-bound box centres for $r = 1, 73, 220, 400$, at the control point and both control-A witnesses, at 24 poses with $t \in \{10^{-6}, 10^{-5}, 1/2000\}$ near the axis minimiser, and at the kernel’s two unresolved box centres of items 11 and 12 | equal, as rationals, to the crate’s exact probes at the control point ($1.0013165657619967$) and both witnesses ($0.9993227551$, $0.9992277156$); at least the crate’s certified bound at each of those four least-bound boxes; $0.9998037043$ at the axis kernel’s minimiser (side $A$); $0.9999383$ to $1.00014$ at $t = 10^{-6}$ near $x = 4.20773$ on the top edge; at the kernel’s hardest boxes the exact capture exceeds its centre lower bound by $6 \times 10^{-11}$ |
| 16 | `pytest` on `test_audit_clipped_corner_transfer.py`, `test_audit_continuous_pose.py`, `test_fine_net_followup.py`, `test_results_register.py`; `devtools.check_results` | 136 passed, 64 CPU-s; 146 results pass every structural check, 11 recorded, 2 reviewed, 132 confirmed, 1 incomplete |

What failed along the way: this review’s first kernel control (item 12, $9999/10^4$ on
slab 0) was built on the exact axis minimum, which lies at $t = 0$ and outside the slab;
the kernel’s acceptance there was consistent, not a defect, and item 11 replaced it with
a witness inside the slab.
Nothing the brief asked for went unestablished.

## `T-133`: The Clipped-Corner Transfer, Re-derived

Notation, all exact: $L = 67/10$, $K = [0, L]^2$, $B = 9977/10000$, $M = 3999/100$,
$D = 83/80000$, $\theta_j = 2\arctan(jD)$ for $j = 0, \ldots, 400$,
$\tau = 10001/10000$, $X = 335427/50000$, $q = L/X = 335000/335427$,
$h = 514946944479/10^{15}$, $H = 2818711359413/10^9$.

**The density.** The 480 positive rows of the retained `rect_n40_L67` (SHA-256
`71011d03…`), read with every decimal exact, expand through the eight symmetries of $K$,
which this review generated as the matrices of the quarter turn and the diagonal
reflection about $(L/2, L/2)$, into 3,840 terms of density $w/(8|R|)$, 3,792 distinct
rectangles after merging, a measure $g \ge 0$ invariant under each of the eight maps
with $\int g = M$ (item 5). The derived 401-direction input written from the contract’s
description alone has SHA-256 `49f696a4…`, the input both release receipts and the
packet’s replay name.

**The nodal statement.** For every $j$ and every centre $c$ with the closed side-$B$
square $Q_j(c)$ at angle $\theta_j$ inside $K$, that is $c \in [a_j, L - a_j]^2$ with
$a_j = B(\cos\theta_j + \sin\theta_j)/2$, $\int_{Q_j(c)} g \ge \tau$. This is what
`sqverify-fast` decides for a format T file whose metadata sets the net: `admit` reads
`certificate.D` and `angle_count`, checks in exact rationals that $D > 0$,
$2 \le N_\theta \le 2^{16}$, $B(1 + D) = 798988091/800000000 < 1$, that the last tangent
$83/200$ satisfies $t^2 + 2t - 1 = 89/40000 > 0$ and $t \le 1/2$, and $L^2 \ge 2B^2$;
`domain_upper` with `Domain::Tokoharu` is $L - B(c + s)/2$, so the quadrant it covers,
with lemma C1’s quarter turns, is the whole legal domain.
The crate’s theorem, lemmas N1 to N4, is not used by the transfer beyond the
per-direction coverage statement; what the transfer needs is only that every row says
every legal centre at $\theta_j$ captures at least $\tau$, which the 401 `verified` rows
say. The packet’s complete run, four directions reproduced here on the reviewed build
(item 14) and the exact capture at the four least-bound box centres above the crate’s
bound (item 15) are what this review checked of it; the crate’s own soundness rests on
the reviews of 3 and 6 October and is trusted here.

**The fold.** A unit parent $P$ at orientation $\alpha$ modulo $\pi/2$: the diagonal
reflection $\sigma$ of $K$ sends $\alpha$ to $\pi/2 - \alpha$ and $g$ to itself, so
$\int_P g = \int_{\sigma P} g$ and each parent’s integral may be bounded with
$\alpha \in [0, \pi/4]$, one parent at a time, with no claim that the reflected parents
pack. Since $\theta_{400} > \pi/4$, $\alpha \in [\theta_j, \theta_{j+1}]$ for some
$j \le 399$, and $\theta_{j+1} - \theta_j = 2\arctan(D/(1 + j(j+1)D^2)) \le 2\arctan D$
(checked for every $j$).

**The case split.** With $\delta_0 = 2\arctan h$ and $\beta = 2\arctan b$,
$b = (D - h)/(1 + Dh)$, so that $\beta = 2\arctan D - \delta_0$:

- If $\theta_{j+1} - \alpha \le \delta_0$, the concentric side-$B$ square $R$ at
  $\theta_{j+1}$ lies inside $P$: its corners project on $P$’s axes to
  $B(\cos\delta + \sin\delta)/2 \le B(\cos\delta_0 + \sin\delta_0)/2 \le q/2$, since
  $\cos + \sin$ increases on $[0, \pi/4]$ and $B(\cos\delta_0 + \sin\delta_0) \le q$
  holds in exact rationals with slack $1.63 \times 10^{-15}$ (item 5). So $R$ is legal
  and $\int_P g \ge \int_R g \ge \tau$. That $\theta_{400}$ exceeds $\pi/4$ is harmless:
  containment is relative to $P$.
- Otherwise $\delta = \alpha - \theta_j < \beta$ and $R$ is the concentric side-$B$
  square at $\theta_j$. It is legal because $\theta_j \le \alpha \le \pi/4$ and
  $B \le q$ give $R$ an axis-aligned bounding box inside $P$’s, which lies in $K$ with
  $P$. Then
  $\int_P g \ge \int_R g - \int_{R \setminus P} g \ge \tau - H|R \setminus P|$, using
  $g \le H$ almost everywhere.

**The clipped corners.** In $P$’s frame, $R$’s corner beyond the right side of $P$ is at
distance $e/2$ past it, $e = B(c + s) - q$ with $c = \cos\delta$, $s = \sin\delta$, and
$R$ lies in the cone at that corner spanned by its two edges, whose directions descend
in $x$ at rates $c$ and $s$ per unit length.
The cone’s part beyond the side is the right triangle with legs $e/(2c)$ and $e/(2s)$,
area $e^2/(8cs)$; four sides and subadditivity give $|R \setminus P| \le e^2/(2cs)$,
whatever the pieces’ shapes.
With $z = c + s$ and $a = q/B \ge 1$ the bound is $B^2(z - a)^2/(z^2 - 1)$, with
derivative $2(z - a)(az - 1)/(z^2 - 1)^2 \ge 0$ for $z \ge a$ (checked on 2,000 points
of $[1, \sqrt2]$), zero below $a$, and $z$ increases with $\delta$ on $[0, \pi/4]$; so
the loss over $\delta < \beta \le \pi/4$ is at most its value $A$ at $\beta$:
$b = 41804244441680000/80000042740596391757$, $e = 1.516 \times 10^{-5}$,
$A = 1.0997 \times 10^{-7}$, $HA = 3.0996 \times 10^{-4}$.

**The density peak.** By this review’s own sweep, over the open $x$-intervals between
consecutive distinct abscissae and, within each, the open $y$-intervals between the
active rectangles’ events, $\operatorname{ess\,sup} g =
744157113224753949201233200959491557948628550000000000000000000000000000000/
264006142643866310314006500845084529851262768737056316088338267454599309 =
2818.711359411784\ldots$, attained on the cell at $(0.87567\ldots, 2.71306\ldots)$,
$1.215 \times 10^{-9}$ below $H$; with every merged density rounded up to a multiple of
$10^{-9}$ the same sweep returns $H$ exactly.
Cell boundaries have measure zero.

**Counting and the endpoint.** $\chi = \tau - HA = 0.99979003557\ldots \ge
99979/100000$, and $40 \cdot 99979/100000 - M = 1/625 > 0$. Forty parents with disjoint
interiors capture at most $\int_K g = M$ since $g$ is absolutely continuous, so no forty
squares of side $q$ pack in $K$, that is, none of side one in a square of side exactly
$X$. The feasible set of forty-square packings with side in $[1, 7]$ is compact and
nonempty, so the least side is attained; attainment at $s(40) \le X$ would give a
packing in a container of side $X$. Hence $s(40) > X$, strict, exactly the claim.
The next grid side $335428/50000$ fails at every admissible $h$ (margin at most
$-0.00998$, by exact bisection), and the standard 201 net gives $\chi < 0$: the finer
net is what the bound needs.

**The full-core bound.** A parent of side $\gamma = B(1 + D)/\sqrt{1 + D^2}$ contains a
legal concentric reference at the nearest node, whose error is at most $\arctan D$, and
$40\tau - M = 7/500 > 0$; $(L/\gamma)^2 = 28729630924721000000/638381969559824281 =
(67000/798988091)^2 \cdot 6400006889$, between $6.70848908^2$ and $6.70848909^2$.
Correct, from the nodal statement alone.

## `T-145`: The Continuous-Pose Kernel, Re-derived

Notation: $B = 199529/200000$, $\tau = 4999/5000$, $A = 997643/10^6$,
$\varepsilon = 10^{-6}$, $T = 83/200$, $X = L/B = 1340000/199529$, $t = \tan(\theta/2)$,
$c = (1 - t^2)/(1 + t^2)$, $s = 2t/(1 + t^2)$, $W = c + s$, $E(t) = L/2 - BW/2$.

**The reduction.** The diagonal reflection folds the angle into $[0, \pi/4]$; the
quarter turns about $(L/2, L/2)$ preserve the angle modulo $\pi/2$ and carry the centre,
whose legal set $[BW/2, L - BW/2]^2$ is symmetric about $L/2$, into the closed northeast
quadrant $x = L/2 + uE$, $y = L/2 + vE$, $(u, v) \in [0, 1]^2$; $E > 0$ since
$L > B \cdot 1414213562373096/10^{15}$ and that bound’s square exceeds 2. Each is a
statement about one square’s capture, with no claim that transformed squares pack.
$T > \sqrt2 - 1$ because $T^2 + 2T - 1 = 89/40000 > 0$, so the 43 closed slabs over
$[\varepsilon, T]$, whose 44 endpoints partition it, reach past $\pi/4$.

**The kernel** (`continuous_pose.cpp`, 195 lines, read in full).
Every interval operation rounds to nearest and steps each endpoint one representable
neighbour outward by integer arithmetic on the encoding, with zero, infinities and NaN
apart; under round-to-nearest the exact result lies between the neighbours of the
rounded one, so each operation encloses, products take the four endpoint products, and
division asserts a denominator interval away from zero ($s \ge s(10^{-6}) > 0$,
$c \ge 3/5$). `direction` encloses $c$ (decreasing), $s$ (increasing) and $W$ (unimodal,
critical at $\sqrt2 - 1$) over the box’s $t$-range, with the rational upper bound above
$\sqrt2$ whenever the critical point may lie inside.
`classify` keeps a rectangle’s full mass only when $U + W_U \le B/2$ and
$V + W_V \le B/2$ hold as intervals over the whole box, $U, V$ the projections of the
centre offset on the square’s normals and $W_U, W_V$ the rectangle’s projected
half-widths, and drops it only when a separating axis holds throughout; the $10^{-10}$
screens choose what to attempt.
`area_lower` takes the inner rectangle of the relative coordinates, valid for every
centre the box’s $\theta$-range gives, and bounds the intersection area from below by
trapezoids under the clipped vertical section $f(\xi) = \min(e, (h - c\xi)/s,
(h + s\xi)/c) - \max(b, (-h - c\xi)/s, (-h + s\xi)/c)$, concave as a lower envelope of
affine functions less an upper envelope, whose values at the knots are interval lower
bounds over the box’s $c, s, h$; the knots are heuristic and only their order matters.
`slice_correlated` encloses the section at a rectangle’s edge over the box’s centre
ranges, so $\partial F/\partial x = \sum_r \rho_r(\ell_r(a_r) - \ell_r(d_r))$ by the
Leibniz rule, and the $y$-derivative by the same with $c$ and $s$ exchanged, which this
review re-derived from the square’s two slab inequalities.
$F$ is Lipschitz in the centre, so along an L-shaped path inside the centre box every
pose captures at least $\text{base} + f_0 - d_uE^{\uparrow}G_x - d_vE^{\uparrow}G_y$,
each step rounded down.
A box closes only when that reaches $\mathrm{up}(\mathrm{fl}(4999/5000))$, which exceeds
$\tau$ by $1.33 \times 10^{-16}$ (recomputed: `0x1.ffe5c91d14e3dp-1`); an unclosed box
is bisected in one dyadic coordinate, children cover the parent exactly, and `verified`
is printed only on an empty stack, a half-width below $2^{-40}$ or the budget exiting 3.
The build refuses `NDEBUG` and `__FAST_MATH__`, asserts round-to-nearest and a clear
MXCSR, and is compiled with `-fno-fast-math
-ffp-contract=off`; the receipts and this review’s rebuild agree in every count across
GCC 13.3 and 15.2.

**The near-axis patch.** $W$ increases on $[0, \varepsilon]$ since
$\varepsilon^2 + 2\varepsilon - 1 < 0$, and $B - AW(\varepsilon) =
589499411/125000000000125000 > 0$, so every legal side-$B$ square at $t \le \varepsilon$
contains the concentric horizontal side-$A$ square, which lies in $K$ with it, and
$g \ge 0$ gives $\int_{Q_B} g \ge \int_{Q_A} g \ge \int_{Q_A} g_-$ for the dominated
measure $g_-$: supports moved inward to the $10^{-9}$ grid and densities floored,
regenerated here in quarter-turn order with SHA-256 `d57e8bb2…`, the receipts’ input,
3,840 rows, none dropped, quarter-turn invariant, of mass $M - 4.1 \times 10^{-6}$. A
horizontal square’s capture is a sum of products of trapezoids in $x$ and $y$, each a
sum of four hinges at $a \mp A/2$, $d \mp A/2$, hence bilinear on the cells of the
$2213 \times 2213$ grid of breakpoints in $[L/2, L - A/2]$ (recomputed) and least at a
vertex; the kernel’s sixteen signed hinge products with two-dimensional prefix sums,
evaluated in signed 128-bit integers at scale $10^{27}$, are that expansion, each
accumulated and evaluated quantity bounded by
$16\sum w(2l + A/2)^2 = 384178892657373682994447839008000000 < 2^{125}$ and the four
evaluation terms below $2^{127}$ (recomputed), with the threshold compared as
$\text{minimum} \ge \lceil 10^{27}\tau\rceil$. The reported minimum
$249950896232809301864786207/(25 \cdot 10^{25})$ at $(4.207731377, L - A/2)$ was
reproduced here by direct integer summation of $g_-$ (item 5) and, on $g$ itself, by
this review’s clipper ($0.9998037043$, item 15) and the crate’s exact sweep (item 14);
the margin is $3.58 \times 10^{-6}$.

**Counting and the endpoint.** $40\tau - M = 1/500 > 0$; a packing at side exactly $X$
scaled by $B$ is forty side-$B$ squares in $K$, refused; compactness and attainment make
the bound strict, as for `T-133`. $X - 335427/50000 = 72586117/9976450000$.

**What the slab replay establishes.** Both receipts and the packet’s replay show all 43
slabs `verified` with $\text{nodes} = 2\,\text{leaves} - 1$, 61,860,927 nodes in all,
and a least leaf bound $2251349454150741/2^{51}$ above the kernel’s threshold; this
review reproduced slabs 0 and 42 exactly (item 9). The pose input regenerated here from
the contract’s description, with binary64 brackets computed independently, has SHA-256
`ccf7b68a…`, the receipts’ input, and its 3,840 terms are the D4 expansion.

## Hypotheses Each Checker Assumes, and What Discharges Them

| Hypothesis | Discharged by |
| --- | --- |
| The inputs are the retained density: the 401-direction file, the pose input and the axis input | regenerated here from the retained candidate by code written for this review and equal in SHA-256 to the inputs the receipts name (items 5, 14); the first-party audits bind the same digests (items 1, 2) |
| The crate decides the nodal statement at 401 directions on Tokoharu’s domain | admission read; four directions reproduced on the reviewed build; the packet’s complete run; the crate’s lemmas on the 3 and 6 October reviews (trusted) |
| The kernel’s lemmas: enclosures, classification, concave section, derivative formula, Lipschitz extension, dyadic cover, threshold | re-derived above; exact captures above the kernel’s centre bounds at its hardest boxes and above the crate’s bounds at its tightest boxes (item 15); refusal of a density with an exact witness below the threshold (item 11) |
| IEEE-754 binary64, round-to-nearest, no FMA, no flush-to-zero, GCC honouring the flags | asserted or refused by the kernel where it can; the rebuilt binaries are the CI run’s; trusted beyond that |
| Exact 128-bit integer arithmetic within the guard | the guard recomputed; the minimum reproduced by two other methods |
| $g \le H$ almost everywhere | the essential supremum recomputed by a third method |
| The transfer, the fold, the legality of both references, the cone bound and its monotonicity, the near-axis containment, the counting, attainment | re-derived above |
| JSON decimals are exact, Python integers and `Fraction` exact, CPython division rounds to nearest | trusted |

## Trust Boundaries

`sqverify-fast` is the code the clipped-corner release itself ran, so the packet’s nodal
replay and this review’s four directions reproduce the producer’s decision with the
producer’s code, as `T-133`’s composition says; it is independent of wand125’s and
Tokoharu’s checkers, which decided the base certificate at 201 directions.
The continuous kernel is the release’s own and the only decider of the continuous cover;
the packet’s replay and this review’s two slabs reproduce it with the producer’s code,
as `T-145`’s composition says.
Independent of all of them here: this review’s expansion, peak sweep, chain and clipper,
which share no code with the releases, the crate, `sqpack` or the first-party audits,
and agree with every exact value they were compared with.
The first-party audits share with the releases’ finite checks only the definitions.
Nothing in this repository decides the continuous cover by a second method (GC-4 of the
stage 4 review stands), and nothing here read wand125’s four certificates.

## The Reported Results `T-132`, `T-142`, `T-143`, `T-144`

**Stated as certified.** Each claim is the source’s, non-strict as the source states it:
$s(29) \ge 291/50$, $s(28) \ge 2297/400$, $s(30) \ge 2357/400$, $s(122) \ge 563/50$. The
differences stated are exact: $291/50 - 581/100 = 1/100$, $- 1163/200 = 1/200$,
$- 2327/400 = 1/400$; $2297/400 - 1147/200 = 3/400$, $- 287/50 = 1/400$;
$2357/400 - 11767/2000 = 9/1000$; $563/50 - 11.22928087555\ldots = 0.0307191\ldots$,
above Nagamochi’s $1 + \sqrt{105} = 11.24695\ldots$ at 126 and the Karakuş strip values
$11.0475$ to $11.2355$ at 122 to 126, while 127 holds $11.2956$ and $11.2819$.

**The premises the record states.** With core $4999/5000$ and step $1/5002$,
$B(1 + D) = 25009997/25010000 < 1$, and the last tangent $1036/2501$ satisfies
$t^2 + 2t - 1 = 367/6255001 > 0$, so the nearest node to any angle in $[0, \pi/4]$ is
within $\arctan D$ and the concentric core lies strictly inside the unit square: the
sentence each claim states is right, and it is lemma N0’s premise, not the coverage.
The sample receipts show the crate admitted each candidate as format M on its
`proof_net` with the per-bin domain at threshold one, and verified the eight directions
with the source’s node counts and least certified bounds; a diagnostic, as recorded.

**The derivation of 123 to 126 from 122.** Two valid routes, both in the record: the
claim’s, that a packing of $N \ge 123$ unit squares contains one of 122, so
$s(N) \ge s(122)$; and the composition’s, that the measure’s mass $12199999/100000$ is
below every $N \ge 122$ and the count enters the certificate only through the mass, so
$N$ squares capturing at least one each exceed it directly.

**Rungs, prices and adoption.** `V0` because the cited entries are the sources’ claims
with `replay_status: not-attempted`; `C0` because no entry carries an `external_review`
and no replay has run.
The `unfinished_confirmations` items name `C3`, link the beads, and price the work as
the retained samples price it: $4.302$, $3.282$, $4.492$ and $11.236$ CPU-hours from
`receipts/sample-diagnostic*.json` and `linear-sample-diagnostic.json`, with `T-144`’s
upper end 23 from the author’s 7 h 41 min at three workers; each basis sentence matches
its receipt. The beads’ 11 October prep notes revise the first three upward (F1-3).
`n-029.md` cites the new evidence and adds a `source-evidence` blocker while keeping
`T-108`’s $581/100$ on both lanes; `n-028.md`, `n-030.md` and `n-122.md` to `n-126.md`
are unchanged and adopt nothing (F1-4). `S3` on all four follows the rubric: the score
is of the claim, a reported and a confirmed result take the same score, and the nearest
entries, `T-102` to `T-111` and `T-080`, are `S3`.

## Findings

### F1-1 — Non-blocking, record: `T-133`’s notes state a move that `T-145` superseded the same day

`packing/frontier/results.yaml`, `T-133.notes`, line 13717 at `aeb8a7219`: “n = 40’s
reported and verified lower bounds move from T-068’s 67/10, which the case record keeps
as history, to 335427/50000.” Both lanes of `n-040.md` cite `T-145`, and the rendered
register reads “superseded by T-145”, but a reader of the entry alone takes
$335427/50000$ for the case’s current bound.
Fix: replace the sentence with “n = 40’s reported and verified lower bounds moved from
T-068’s 67/10 to 335427/50000 at registration, and T-145, registered the same day on the
same density, raised both lanes to 1340000/199529; the case record keeps this entry as
history.”

### F1-2 — Non-blocking, record: the significance of `T-133` and `T-145` is still a draft

`T-133.significance.by` (line 13641) and `T-145.significance.by` (line 15244), both at
`aeb8a7219`, name the registering lane as a draft; the rubric says the lane that reviews
the mathematics compares the score with the nearest entries, keeps or changes it, and
`by` then names that review.
This review compared both with `T-095`, `T-099`, `T-100`, `T-102` to `T-111`
(single-count certificate raises, all `S3`) and with the `S4` entries, which are repairs
of published values, multi-count bound families and optimality proofs, and keeps `S3`
for both, with the note that `T-145`’s kernel is a reusable technique whose reuse at a
second count would make it a bound family and an `S4` question.
Fix, on both: set `scored: '2026-10-11'` and `by: the 11 October final review
(docs/project/reviews/review-2026-10-11-final-lower-bounds.md)`. The drafts on `T-132`,
`T-142`, `T-143` and `T-144` may stay drafts until the stage 4 review that reads their
certificates, or take the same `by`; this review keeps `S3` on all four.

### F1-3 — Non-blocking, record: three prices have been revised in the beads since they were recorded

`T-132`, `T-142` and `T-143` record `estimated_cost.cpu_hours` 4.3, 3.28 and 4.49,
priced on 2026-10-10 from the retained eight-direction samples, which is what their
`basis` says. The prep-lane notes of 2026-10-11 in `think-r333` and `think-i85v` revise
them to about 5.5, 4.5 and 6.1 CPU-hours from two-direction smokes at a higher CPU
ratio, and `think-nd7g` revises `T-144` to 14.6, inside its recorded upper end of 23;
the smoke receipts are in scratch only.
The checker accepts a price dated no later than `last_reviewed`, 2026-10-11. Fix: add
`cpu_hours_high: 5.5`, `4.5` and `6.1` to the three items, with a sentence appended to
each `basis`: “The prep lane’s smoke of 11 October (two directions, think-r333 /
think-i85v) revised the price upward to the upper end; its receipts are not retained.”
Separately, `think-i85v` records that `T-142`’s whole-net control is held: at the axis
direction the $99/100$ mutant’s exact capture sits $2.15 \times 10^{-9}$ above the
vertex sweep’s certified bound, beyond the census’s `AXIS_ROUNDING` of $10^{-9}$, so the
control as the census writes it would report `CONTROL_FAILED` although the refusal is
sound. That is a tooling tolerance on an unmerged branch and an owner question;
`T-142.next_rung` may say so in one clause when that branch lands.

### F1-4 — Non-blocking, record: the case records treat the four reported results unevenly

`n-029.md` lists `E-wand125-fine-net-n29-582-followup-report` in its evidence, adds a
`source-evidence` blocker and a resource for the packet; `n-028.md` lists the weaker 8
October report `E-wand125-fine-net-lower-bounds-446-report` ($287/50$) with a blocker
but not `E-wand125-fine-net-n28-57425-report` ($2297/400$); `n-030.md` and `n-122.md` to
`n-126.md` list nothing of `E-wand125-fine-net-n30-58925-report` or
`E-wand125-linear-n122-1126-report`. None adopts a bound, which is right.
Fix, for consistency with `n-029.md`: add the evidence id, a `source-evidence` blocker
worded as `n-029.md`’s (“The 2297/400 report awaits a complete maintained capture,
whole-net controls and a review that reads it; an eight-direction sample is
diagnostic.”, and the like at 30 and 122 to 126 with “a two-angle sample”), and the
packet’s resource key to each of `n-028.md`, `n-030.md` and `n-122.md` to `n-126.md`; or
state in each result’s `notes` why its case stays silent.

### F1-5 — Non-blocking, wording: `T-143` names its review without the checklist

`T-143.next_rung` and its `unfinished_confirmations[0].what` end at “a review that reads
this certificate”, where `T-132`’s and `T-142`’s add “by the checklist of the 6 October
declared-net soundness review”; the review the three need is the same.
Fix: append the phrase to both fields of `T-143`. A smaller nit of the same kind:
`E-n040-guzhou-clipped-corner-sqverify-fast-replay.proof.assumptions[1]` says “Every
angle and legal centre is covered by the 401-direction net”, which is lemma N0’s net
premise; the net covers angles to within half a gap and the transfer carries the rest.
“Every legal centre at each of the 401 net directions is covered, and lemma N0’s net
premises … hold” says it exactly.

### F1-6 — Non-blocking, confirmed: what the kernel’s controls show, and a control that closes the gap

The contract’s refusal controls B, C and D refuse by `unresolved`, which a kernel that
never closed a box would also return; the positive controls E and the real run show that
it closes. This review added the missing kind: on the real density, slab 0 at threshold
$99994/10^5$, with a pose inside the slab whose exact capture by independent code is
$0.9999383$, the kernel refused, and stopped at the box holding that pose; at its two
hardest boxes the exact capture at the centre exceeds the kernel’s centre lower bound by
$6 \times 10^{-11}$, so the per-box bound is sound and nearly sharp there.
No change to the record; the stage 4 review’s GC-5 and GC-8 stand as written.

## Where the Record and the Sources Differ

At every number read here the register, the evidence, the packets, the receipts and the
releases agree: both bounds, the raise, $B$, $M$, $D$, $\tau$, $h$, $H$, $99979/100000$,
$1/625$, $1/500$, $A$, $\varepsilon$, $T$, the axis minimum and its $2213^2$ vertices,
43 slabs and 61,860,927 nodes, 401 of 401 and 32,970,910 boxes, and every digest.
`E-n040-guzhou-continuous-pose-kernel-replay` gives the slab replay’s load average as 3
to 14 and the packet README’s whole run as 3.0 to 18.0; both are true of what each
describes (the slab receipts span 2.98 to 14.03).

## Significance

`S3` on all six, as registered, by the comparison in F1-2.

## Verdicts

| Result | Verdict | Grounds |
| --- | --- | --- |
| `T-133` | accepted | the argument re-derived; every finite value recomputed; the nodal rows reproduced at four directions and the complete run’s receipts judged again; `V3`/`C3` as the evidence derives them; findings F1-1, F1-2, F1-5 are wording |
| `T-145` | accepted | the kernel’s lemmas re-derived and the kernel read line by line; the binaries rebuilt; two slabs and the axis replayed; the hardest boxes and a refusal control checked by independent code; `V3`/`C3` as the evidence derives them; it supersedes `T-133` on both lanes of `n-040.md`, as the renderer derives |
| `T-132`, `T-142`, `T-143` | accepted as recorded (`V0`/`C0`, reported) | claims as the sources state them; premises as the samples show them; prices as the retained samples price them (F1-3); no case adopts them (F1-4) |
| `T-144` | accepted as recorded (`V0`/`C0`, reported) | the same, with the derivation of 123 to 126 from 122 valid by either route the record gives |

## Disposition

No finding blocks the merge.
F1-1 to F1-5 are one-line record fixes for the coordinator; F1-6 records what was
checked. For `T-133` and `T-145` this review is a second accepted adversarial AI review
by a separately prompted lane with no shared context, and the coordinator may cite it in
each entry’s `reviews` once it is mapped in `docs/project/document-map.yaml` as a
retained review; `V4`/`C4` would then still need a human oversight record on each.
The reviewer’s own checks are evidence and not a rung: what was proved here is each
argument from certificate to bound; what was checked by computation is every finite
quantity, every derived input’s identity, the CI binaries’ identity, two of 43 slabs and
the axis certificate, four of 401 directions, the exact captures at the tightest and
hardest boxes, and the first-party audits’ receipts; what the packets report and this
review did not run is the other 41 slabs and the other 397 directions, each of which the
retained receipts show and the first-party judges hold.
The CPU-hour replays of the four reported results were not started, as the owner
deferred them.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
