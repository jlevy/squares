# Guzhou0806’s `s(40) > 3359/500`: Review of the New-Support Density on the Continuous-Pose Kernel

**Verdict: no blocking defect in the mathematics, in the density or in the replay.** The
argument from Guzhou0806’s new rectangle density to the strict bound
$s(40) > 3359/500 = 6.718$ is `T-145`’s argument with three parameters changed and the
measure replaced, and it is correct as `PROOF.md` states it: every exact premise holds,
and every number in it was recomputed here in exact rationals with code written for this
review, apart from the first-party audit’s. The two kernels that carry the proof are
byte for byte the ones the
[10 October review](review-2026-10-10-guzhou-n40-continuous-pose-bound.md) read line by
line and the [11 October final review](review-2026-10-11-final-lower-bounds.md) read
again; nothing in the kernel code depends on the density beyond the terms it reads.
What is new, and what this review and the replay decided, is the density: 685 positive
D4 rectangle orbits, 522 of them rows of wand125’s `rect_n40_L67` pool and 163 generated
outside it, with every weight new, of mass $3999/100$; and whether the same kernels, on
this measure, at the smaller side $B = 3350/3359$ and the smaller axis side
$A = 249329659/250000000$, close the cover.
They do: both kernels were rebuilt here into the byte-identical binaries of the
release’s CI run, the axis certificate and all 43 slabs reproduced the release’s two
receipts field for field apart from timing, the kernels refused every synthetic density
whose least capture is below the threshold and the release’s own `exact.py` refused the
mutated axis side, and this repository’s `sqverify-fast` decided the near-axis statement
a second way on the new density and verified the 401-direction nodal statement at the
new side, a necessary condition the claim passed.
The release’s two dual programs for its separate negative result ran and agreed with
both receipts; that result bears on no register value.

Eight findings are recorded, none blocking for the claim.
GN-4 says what the evidence is: the continuous cover is decided by the producer’s kernel
and by nothing else here, so the confirmation is *reproduced with the producer’s code*,
exactly as `T-145`’s; GC-4 of the 10 October review stands, and wand125’s now published
continuous-angle verifier (GN-7) is the first candidate for a code-distinct decision,
not yet reviewed or retained.
The draft significance `S3` is kept, on the precedent of `T-099`, `T-100` and `T-145`:
the strongest lower bound on record at $n = 40$, by a reweighted and extended density on
an existing technique.

This is stage 4 of the import of Guzhou0806’s 11 October follow-up on issue 485
(`think-tln9`), written on 2026-10-12 by an AI agent (Claude, at the highest reasoning
effort), the lane that ran the complete replay and extended the first-party audit for
it; it was prompted separately from the lane that wrote the audit’s finite checks and
the packet (lane E of the 2026-10-11 intake pass), whose work it judges, and from the
three reviews of pull request 512 that read that work.
It registers nothing and moves no bound; the register entry is `T-NNN`, to be assigned,
and `T-145` keeps its claim.

## Scope and Evidence

The subject is the claim of Guzhou0806’s comment of 2026-10-11T07:39:30Z on
[jlevy/squares#485](https://github.com/jlevy/squares/issues/485#issuecomment-6106761997):
source [Guzhou0806/n40-square-packing](https://github.com/Guzhou0806/n40-square-packing)
at `6a65957e6c5c51cdf267917d882dab7f5b4928dd`, committed 2026-10-11T07:12:04Z, a child
of the `T-145` pin `71c97d07`, which the tag `n40-new-supports-6718-20261011` names;
release ZIP `n40-6718.zip`, 196,420 bytes, SHA-256
`e6e495901b2bfb590a4154ad5cc296b72dff785c9fda5e9b40ef0711158e3b3f`, published
2026-10-11T07:39:20Z from GitHub Actions run 38120568498 (`success`, `head_sha`
`6a65957e`, 07:12:07Z to 07:38:58Z). Everything was read from the retained packet
[`guzhou-n40-new-supports-2026-10-11/`](../../../packing/resources/web/guzhou-n40-new-supports-2026-10-11/README.md),
whose `acquire_source --check` reports `PACKET_MATCHES_ITS_CONTRACT`.

**Read in full.** The comment and wand125’s review comment of 2026-10-11T17:14:50Z as
edited 2026-10-12T02:19:26Z; the packet README and its three stage 2 receipts; of the
release, `README.md`, `PROOF.md`, `VERIFICATION.md`, `REPRODUCIBILITY.md`, `SOURCES.md`,
`OBSTRUCTION.md`, `certificate/parameters.json`, `verifier/run.py`,
`obstruction/run.py`, both receipts (`results/` in the tree and in the ZIP, as data) and
the parts of `verifier/continuous_pose.cpp` that read the input and the threshold (lines
44 and 163 to 168; the kernel is byte for byte `T-145`’s, `da06206b…`, whose two earlier
reviews read all of it); this repository’s `T-145` entry and its four evidence entries,
the 10 October review and its replay contract, the 11 October final review’s `T-145`
section, the three reviews of pull request 512 (A, B and C), `epistemics.md`,
`devtools.audit_continuous_pose` and `devtools.audit_n40_new_supports` with their tests.

**Not opened.** `verifier/exact.py` beyond a search for the string `axis_side`, which
control G needs (one line, as `T-145`’s replay found it in its copy);
`verifier/audit.py`; `obstruction/check.py` and `obstruction/check.cpp` beyond the
latter’s includes; the release’s `tests/`; the log of run 38120568498 (only its
conclusion, head and times, from the retained API record); wand125’s continuous-angle
verifier.

**Ran.** On a 4-core x86-64 Linux container shared with other work, at a one-minute load
average between 7.6 and 27.0, with at most two worker processes, and every script of
this review under `python3 -I` with the standard library only.

| # | Command | Result |
| --- | --- | --- |
| 1 | `review_checks.py`: the density’s orbit facts, D4 expansion and mass, and the scalar chain, in exact rationals apart from the audit | candidate `984fcd3a…`, pool `71011d03…`; 685 sites, 522 inherited each equal to its pool row with no index twice, 163 generated in none of the pool’s D4 orbits, 685 distinct orbits, every box proper in $K$, every weight positive, mass $3999/100$; 5,424 distinct terms of integral $M$; $X = L/B = 3359/500$, the raise $217911/99764500$; $40\tau - M = 1/500$; $T^2 + 2T - 1 = 89/40000$; $B - AW(\varepsilon) = 424025836324581/839750000000839750000000 > 0$; 44 endpoints; $\mathrm{up}(\mathrm{fl}(\tau)) - \tau = 1.33 \times 10^{-16}$; the receipts’ least leaf bound and axis minimum above $\tau$ |
| 2 | `audit_n40_new_supports check --output` | `FINITE_STEPS_HOLD`, 68 checks, 7 controls refused; byte-identical to the packet’s `receipts/finite-audit.json` |
| 3 | `audit_n40_new_supports check-axis --output` | `AXIS_STAGE_HOLDS`; byte-identical to `receipts/axis-check.json` |
| 4 | `audit_n40_new_supports run-replay --workers 2` (builds, axis, slabs) | pose binary `69bc9e64…`, axis binary `19288b2f…`, the CI run’s; axis `AXIS_COVERAGE_PROVED`, every field both receipts’; 43 of 43 slabs `verified`, every non-timing field both receipts’; 5,242.6 CPU-seconds, 12,629 s of wall time |
| 5 | the same, stage `controls` | A: synthetic-negative exit 3 at 83 nodes, limited-budget exit 3 at 1, synthetic-positive verified at 117; B: exit 3 at 92, 87 and 89 nodes; C: all 14 exit 3, the two on [410000,415000] by the 1,500,000-node budget, the rest at the width floor; D: all five exit 3, four by the budget; E: all 14 cuts verified, the largest at 251,857 nodes, the gap verified at 140,819; F: exits 0, -6, -6, 1, 1; H: 1/2 proved, 62593/62500 refused (exit 2), 500743/500000 proved; 72.5 CPU-seconds in all |
| 6 | `cargo build --release --locked -j 1` of `sqverify_fast` (source `d97758bb…`, reviewed), then the same, stage `crate` | the axis at side $A$: `verified`, 10,929,636 vertices, least certified $1.0016868361671276$, the axis stage’s value again; the 401-direction net at side $B$: VERIFIED, 401 of 401 directions, no direction refused, 35,375,590 boxes, least certified 1.000000000310131 at r = 398; 1,782.6 s of wall time and 720.9 CPU-seconds at two threads |
| 7 | the same, stage `release-g` | the release’s `scalar()` on the unchanged copy returns both receipts’ scalar block; with `axis_side` one step of $1/250000000$ larger it refuses `NEAR_AXIS_CONTAINMENT` |
| 8 | the same, stage `duals` (Boost 1.83 headers installed for it) | `EXACT_DUAL_CODE_DISTINCT_CHECKED`, column 201, slack `66062736801751370160`, every non-timing field both receipts’; 703.0 s; the dual binary `d5ecc193a842c21e86281c7facdc4f92a70cec92a28f5f7e002ed5d3a77cf51c`, byte for byte the CI run’s |
| 9 | `audit_n40_new_supports check-replay --output` | `REPLAY_HOLDS`, 70 checks; retained as `receipts/replay-check.json` |
| 10 | the review’s own refusal control: the density with every weight scaled by $985/1000$ (mass $787803/20000$), written as a crate input at side $B$ on the standard net and as the kernel’s pose input; `sqverify-fast --directions 0 --threshold 1` on the first, and the replay’s pose binary on slabs 0 and 1 of the second at `4999 5000 1500000` | the crate: `refused` at direction 0 by the exact axis-vertex sweep over 10,929,636 vertices, least certified $0.9866748\ldots$ at $(174813950953527470221/(3359 \cdot 10^{16}),\ 208303/33590)$, exit 1; the kernel: `unresolved`, exit 3, on both slabs at the width floor after 56 nodes and 40 angle splits, its centre bound $0.98648$ at the same corner of the centre domain; every checker that accepted the original refused the scaled copy |
| 11 | `pytest tests/test_audit_n40_new_supports.py tests/test_audit_continuous_pose.py`; `audit_continuous_pose check-replay` | 134 passed: the n40 file’s 117, of which 18 are new for the replay, and `T-145`’s 17, of which one is new for the resumable slab stage; `T-145`’s `replay-check.json` regenerates byte for byte through the shared runner and judge |

What failed along the way: the first slab run was stopped from outside by the session’s
two-hour limit on a background command after 38 of the 43 slabs had finished, at a load
average near 19, with every finished row still in memory; the runner was changed to
write each slab’s row as it finishes and to keep, on a later run in the same directory,
a row that names the same binary, input and arguments (a test holds it to that), and the
stage ran again from the start.
The receipt’s 43 rows are from two runs of that stage, the second of which kept the
first’s 32 finished rows after the same two-hour limit stopped the first at a load
average above 20; each row carries its own start time, wall and CPU time, and the
stage’s 12,629 s of wall time span both.
Where the price was wrong: the stage 1 price, 2,604 to 2,626 CPU-seconds for the slabs,
was half the measured cost.
The slabs took 5,242.6 CPU-seconds, 1.97 times the local receipt’s 2,655.3 and within
0.3% of the CI receipt’s 5,229.5, with the same ratio slab for slab, where `T-145`’s
replay on this host had taken 0.98 of its local receipt at a load average of 3 to 14.
The difference is the host: for this whole stage the one-minute load average was 7.6 to
27.0 on four cores, and a CPU-second on a core shared that heavily does about half the
work. The work is the receipts’, not more; the calibration assumed the earlier host
conditions (GN-3).

## The Claim

Let $s(40)$ be the least side of a square that holds forty closed unit squares with
pairwise disjoint interiors, any rotations, boundary contacts allowed.
The release claims

$$
s(40) > X = \frac{3359}{500} = 6.718,
$$

an increase of exactly $217911/99764500 = 0.0021842539\ldots$ over `T-145`’s
$1340000/199529$, from a new certificate.
It is not a packing, an optimality claim or a priority claim; the release says so, and
says wand125’s review of the earlier $6.70854$ covers neither this density nor the
kernel. Nobody else holds the value: the register’s strongest lower bound at $n = 40$ is
`T-145`’s, and no pending report is at $n = 40$.

## The Argument From Certificate to Bound

Notation, all exact rationals: $L = 67/10$, $K = [0, L]^2$, $B = 3350/3359$,
$M = 3999/100$, $\tau = 4999/5000$, $A = 249329659/250000000$, $\varepsilon = 10^{-6}$,
$T = 83/200$, $X = L/B$; for $t = \tan(\theta/2)$, $c = (1 - t^2)/(1 + t^2)$,
$s = 2t/(1 + t^2)$, $W = c + s$, $E(t) = L/2 - BW(t)/2$. Against `T-145`: $B$ falls from
$199529/200000 = 0.997645$ to $0.9973206\ldots$, $A$ from $997643/10^6$ to
$0.9973186\ldots$, and $\tau$, $M$, $\varepsilon$, $T$, the 43 slabs and the budget are
unchanged.

**1. The density.** `certificate/certified_candidate.json` lists 685 sites, each a box
$R$ in $K$ with a weight $w$, a kind, and for the inherited ones the index of its row in
wand125’s pool. The measure is $w/(8|R|)$ on each of the eight images of $R$ under the
symmetries of $K$, multiplicities kept, overlaps added (`PROOF.md` §1): a bounded,
nonnegative, $D_4$-invariant density $g$ with $\int_K g = \sum w = M$. Recomputed here
(item 1): 522 inherited boxes equal to their pool rows exactly, no row twice (427 of
those rows carried positive weight in `rect_n40_L67`, 95 were among its zero-weight
candidates); 163 generated boxes D4-equivalent to none of the pool’s 2,526 rectangles;
685 distinct orbits; every box proper and in $K$; every weight positive; 5,480 terms,
5,424 distinct rectangles once merged, the multiset invariant under each of the eight
maps; integral $M$. The provenance of the inherited rows and the novelty of the
generated ones are facts about the file, checked because the release states them; the
proof needs only $g \ge 0$, $g$ bounded, $\int g = M$ and the invariance, which hold for
any such file. How the weights and the new supports were found (the release says a dual
pricing and a rationalization) is outside every check and needs no review: the density
is what it is. Correct.

**2. The reduction** is `T-145`’s, unchanged (items 2 of the 10 October review): the
diagonal reflection folds the angle into $[0, \pi/4]$, the quarter-turns about the
centre of $K$ carry the centre into the closed northeast quadrant with the orientation
kept modulo $\pi/2$, one square at a time; $t \in [0, \sqrt2 - 1]$ and $T$ exceeds
$\sqrt2 - 1$ since $T^2 + 2T - 1 = 89/40000 > 0$; the legal centres at $\theta$ are
$[BW/2, L - BW/2]^2$, parametrised by $(u, v) \in [0, 1]^2$ with $E > 0$ because
$L > B \cdot 1414213562373096/10^{15}$, that bound’s square exceeding 2 (recomputed at
the new $B$). Correct.

**3 to 7. The interval kernel** is `T-145`’s, byte for byte (`da06206b…`, the manifest
of both packets): the enclosures of $c$, $s$ and $W$, whole-box containment and
exclusion by projection on the square’s normals, the concave-section trapezoid bound at
the box’s centre, the translation-derivative extension over the centre box, the dyadic
subdivision and the exit codes, all re-derived by the 10 October review and again by the
11 October final review, which this review does not repeat.
What this review checked is that nothing in the kernel depends on the density or the
parameters beyond what it reads: `readI` (line 44) reads each value as a pair through
`stod`, which accepts the hexadecimal pair this release writes for $B$ where `T-145`’s
wrote a decimal one, and asserts the pair finite and ordered; `main` (lines 163 to 168)
takes the slab, the denominator, the threshold as `tn/td` with both below $10^8$, and
the budget, accepts a leaf only at $\mathrm{up}(\mathrm{fl}(tn/td))$, and reads
`certificate_input.txt` from the working directory.
The 5,480 terms are read into a vector; no array bound, screen or heuristic is sized to
`T-145`’s 3,840. The receipts: 60,500,889 nodes, 30,250,466 leaves, 13,812,428 angle
bisections, the largest slab 6,072,313 nodes (slab 1,
$t \in [5 \times 10^{-4}, 10^{-2}]$, as for `T-145`), the least leaf bound
$9005397816695287/2^{53} = 0.99980000020\ldots$ at slab 40, $2.0 \times 10^{-10}$ above
$\tau$, which is where subdivision stopped and says nothing about the true minimum.
Correct, by the earlier reviews and the replay (below).

**8. The near-axis patch** at the new $A$. For $t \in [0, \varepsilon]$, $W$ increases
($W' > 0$ where $1 - 2t - t^2 > 0$), so $AW(t) \le AW(\varepsilon) \le B$, recomputed:
$B - AW(\varepsilon) = 424025836324581/839750000000839750000000 =
5.05 \times 10^{-10} > 0$, `PROOF.md` §6’s value.
The horizontal side-$A$ square concentric with a legal side-$B$ square at angle $\theta$
lies inside it and inside $K$, and $g \ge 0$ gives $\int_{Q_B} g \ge \int_{Q_A} g$. The
axis kernel decides $\int_{Q_A} g_- \ge \tau$ for every legal horizontal side-$A$ square
on the dominated measure $g_-$: supports moved inward to the $10^{-9}$ grid, densities
floored, 5,480 rows, none dropped, $\int g_- = M - 2.57 \times 10^{-6}$, quarter-turn
invariant (the audit; item 2). The capture is bilinear on each cell of the
$3293 \times 3293$ grid of breakpoints, so its minimum is at a vertex; the integer
evaluation is bounded by $627444222088298915573283512797161984 < 2^{125}$; the minimum
$1001486431423867090847280653/10^{27} = 1.0014864\ldots$ at
$(3.490012394, 6.201340682)$, a grid vertex, is $1.69 \times 10^{-3}$ above $\tau$, and
the audit evaluated the dominated measure’s capture there again in integers and got the
same value; the density’s own capture there is $1.0014865\ldots$. The crate’s exact
sweep on $g$ itself at side $A$ found its least capture $1.0016868\ldots$ over
10,929,636 vertices (threshold 1 on the density scaled by $5000/4999$; GC-4). Correct,
with a margin a thousand times `T-145`’s (GN-1): the new density is far from tight on
the axis, and tight somewhere in the slabs.

**9. Counting and the endpoint.** Every legal side-$B$ square captures at least $\tau$;
forty with disjoint interiors capture at most $M$; $40\tau - M = 1/500 > 0$. A packing
at side exactly $X$ scales by $B = L/X$ into forty side-$B$ squares in $K$: refused.
The feasible set is compact, so the least side is attained, hence $s(40) > X$. Correct,
as in the `T-133` and `T-145` reviews.

**What changed and what it cost.** The whole raise comes from the density: `T-145` spent
its margin on the smaller side, this release keeps $\tau$ and $M$ and finds a measure
that the smaller square still captures.
The kernel’s least leaf bound sits at the same $2 \times 10^{-10}$ above $\tau$ as
before, where subdivision stops; the slabs’ node count fell by 2.2% and the axis margin
rose by three orders of magnitude.
The 401-direction run of `sqverify-fast` at side $B$ (item 6) gives the least certified
nodal capture $1.000000000310131$ at $r = 398$ (and, at $r = 0$ by the exact vertex
sweep at side $B$, $1.0017003\ldots$, the horizontal minimum on the scaled density),
which bounds the claim’s true slack from above at those directions.

## Hypotheses Each Checker Assumes

The continuous kernel (`continuous_pose.cpp`, items 4 and 5):

1. The input is the retained measure: the first-party audit regenerates the pose input
   from the retained candidate, term for term the D4 expansion in the release’s order,
   each of its 27,402 numbers bracketed by a binary64 pair, to the digest `6c64a2d2…`
   that every slab row and both admission blocks of both receipts name, and the replay
   ran the kernel on that file.
   Discharged here, item 2, and refused by the audit’s control D3 (a mass-preserving
   reweighting fails both input digests).
2. The geometric lemmas of the 10 October review, items 2 to 7; re-derived there and in
   the 11 October final review, unchanged, and independent of the density.
3. IEEE-754 binary64 with round-to-nearest and subnormals, SSE2 evaluation, no fused
   multiply-add, and GCC honouring `-fno-fast-math -ffp-contract=off` at `-O3`; asserted
   at start-up where the program can (controls F), refused at compile time where it can,
   and trusted for the rest.
4. All 43 slabs finish `verified` within the 30,000,000-node budget: the receipts show
   it, and the complete run here (item 4) reproduced every count.

The axis kernel (`axis_integer_grid.cpp`, item 4):

5. Exact integer arithmetic within the guarded bound, the bilinear-cell lemma and the
   hinge expansion; re-derived by the 10 October review, and the minimum reproduced here
   by the audit’s direct evaluation on the same measure and bounded from below by the
   crate on $g$ itself.
   This release builds the axis kernel with the pose kernel’s flags (`-O3
   -fno-fast-math -ffp-contract=off` in place of `-O2`); the kernel is integer code, and
   the build here reproduced the CI run’s binary `19288b2f…` and the same output.

The finite checks (`devtools.audit_n40_new_supports`, written apart from `exact.py`;
`review_checks.py` here, written apart from both):

6. JSON decimals are their literal values, read as fractions; Python integers and
   `Fraction` are exact.
   Trusted.
7. The scalar chain: $X = L/B$, $40\tau - M = 1/500$, $T^2 + 2T - 1 > 0$,
   $(1414213562373096/10^{15})^2 > 2$, $L > B \cdot 1414213562373096/10^{15}$,
   $A \le B$, $W$ increasing on $[0, \varepsilon]$, $AW(\varepsilon) \le B$, the 44
   endpoints partitioning $[10^{-6}, 83/200]$, $\mathrm{up}(\mathrm{fl}(\tau)) \ge \tau$
   with `tn`, `td` inside the kernel’s bounds, the receipts’ least leaf bound at least
   that threshold, and the axis minimum at least $\lceil 10^{27}\tau \rceil$; every one
   holds (items 1 and 2).

The crate (`sqverify-fast`, item 6): its exact-event axis sweep and its rotated branch
and bound at a fixed direction, as the 3 and 6 October soundness reviews accepted them;
the scaling by $5000/4999$ turns capture $\ge \tau$ into capture $\ge 1$ exactly.

The prose (`PROOF.md`): §1 (the density), §6 (the patch) and §7 (the counting) are
re-derived above; §2 to §5 state `T-145`’s lemmas in the same words, and nothing in the
proof is assumed that the code does not implement.
`VERIFICATION.md` says what the release’s label means (`REPLAYED_SAME_KERNEL`: the same
kernel on two compilers) and that the claim has no external independent review, which
was true when it was written.

## Trust Boundaries and What the Checkers Share

The continuous cover is decided by the release’s own kernel and by nothing else here.
The replay rebuilt it from the retained, reviewed source into the CI run’s binary and
ran it on the input derived here; that is *reproduced with the producer’s code*, and it
is what the kernel-replay evidence entry must say.
The kernel shares no code with `sqverify-fast`, Tokoharu’s `verify.cpp` or wand125’s
checkers; the release says its translation-derivative structure follows Tokoharu and its
concave sections draw on this repository’s crate.
It shares with every verifier of this certificate the measure, its $D_4$ expansion, the
container and the counting; a defect in that mathematics would reach all of them.

The near-axis statement is decided twice: by the release’s integer axis kernel, rebuilt
and re-run here on the dominated measure (*reproduced with the producer’s code*), and by
`sqverify-fast`’s exact axis-vertex sweep on the density itself, undominated, with code
that shares nothing with the axis kernel (*independently decided*; the crate was
reviewed on 3 and 6 October and is this repository’s own).
The finite steps are decided by `devtools.audit_n40_new_supports`, a first-party tool
written without opening `exact.py` (its docstring is the read log; this review searched
`exact.py` for one string, after the finite checks were written and unchanged), which
shares with `exact.py` the definition of the density, its expansion, the kernels’ input
order, the enclosure rule and the inward rounding, and no code (*independently
decided*); and again by this review’s own script, written apart from both.
The 401-direction nodal statement at side $B$ is decided by `sqverify-fast` alone; it is
a necessary condition of the claim and not the claim.

The release’s two dual programs decide `OBSTRUCTION.md`’s negative result, a statement
about the original support family at $168/25$ that bears on no bound; the replay ran
them as the release runs them, with the producer’s code, and nothing here decided that
result a second way.

wand125’s comment reports a fresh run of the release’s entry point and a verifier of
their own; it publishes summary numbers and, since its edit of 2026-10-12T02:19Z, a pin
of that verifier’s source (GN-7), and no receipt; it is a third party’s report and
confirms nothing here.

## What the Replay Decided and How It Was Checked

The replay ran the 10 October review’s contract at the new parameters, through
`devtools.audit_continuous_pose`’s runner and judge parametrised by this release
(`Replay`), which keeps `T-145`’s judgement byte for byte (item 11), with the contract’s
totals from both of this release’s receipts, its control H thresholds either side of
this release’s axis minimum, its control G mutant in this release’s `exact.py`, and a
stage of its own for the dual programs.
`check-replay` judges the retained receipts and must print `REPLAY_HOLDS`; its output is
retained as `receipts/replay-check.json`, and the tests hold it to that file and refuse
a changed slab, a changed least bound, an accepted control, an admitted axis threshold,
a crate run with other values, an admitted control G and a dual that disagrees.

| Contract | Here |
| --- | --- |
| **1.** the derived inputs, `6c64a2d2…` (pose) and `10dd46b0…` (axis) | regenerated; the digests both receipts name |
| **2.** the builds from the tree’s directory with the release’s flags, the axis kernel now at the pose kernel’s flags | `g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`: pose `69bc9e64…` and axis `19288b2f…`, byte for byte the CI run’s; the rounding harness `81f15ab0…` |
| **3.** the axis run: `AXIS_COVERAGE_PROVED`, $3293^2$ vertices, minimum `1001486431423867090847280653` at scale $10^{27}$, minimiser `3490012394, 6201340682`, `direct_sum_matches` | the same, every field equal to both receipts’, exit 0, 7.0 s |
| **3.** `sqverify-fast` at side $A$, direction 0, on the 685 rows scaled by $5000/4999$ | `verified`, `axis-vertex-sweep`, 10,929,636 vertices, least certified $1.0016868361671276$, the axis stage’s decision of 11 October again |
| **4.** the 43 slabs, `continuous PL PH 1000000 4999 5000 30000000`, each `verified`, every non-timing field equal to both receipts’ | all 43, against the local and the CI receipt; 60,500,889 nodes, 30,250,466 leaves, 13,812,428 angle splits, least `lower_bound` $9005397816695287/2^{53}$ at slab 40; every slab’s nodes $= 2\,\text{leaves} - 1$; 5,242.6 CPU-seconds and 12,629 s of wall time on two workers at a load average of 7.6 to 27.0 (slab 0 took 68.6, slab 1 322.1 and slab 42 134.0 CPU-seconds, against the local receipt’s 32.8, 158.6 and 66.0 and the CI receipt’s 67.6, 327.3 and 104.6) |
| **5.** controls A to F and H, and G on the release’s `exact.py` | every one as the contract states it: A exit 3 at 83 and 1 nodes with the positive control verified at 117; B exit 3 at 92, 87 and 89 nodes; C all 14 exit 3 (the two on `[410000,415000]` by the budget); D all five exit 3 (four by the budget); E all 14 cuts `verified`, the largest at 251,857 nodes, and the gap at 140,819; F the rounding harness `PASSED` on 1,000,008 values, the wrong-rounding and flush-to-zero runs exit $-6$, both compilations refused by the kernel’s `#error`; G the release’s `exact.py` returns both receipts’ scalar block unchanged and refuses `NEAR_AXIS_CONTAINMENT` with $A$ one step larger; H the axis kernel refuses $62593/62500$ (exit 2) and proves $500743/500000$ and $1/2$ |
| **6.** `sqverify-fast` on the same rows at side $B$, `D` $83/80000$, 401 directions, two threads | `VERIFIED`, 401 of 401, no direction refused, 35,375,590 boxes, least certified 1.000000000310131 at $r = 398$; at $r = 0$, the exact axis-vertex sweep at side $B$, least 1.001700339663363; 1,782.6 s of wall time and 720.9 CPU-seconds at two threads under the shared load |
| the duals (no contract item; the release’s own entry point) | `obstruction/run.py` on a scratch copy of the retained tree with the pinned pool restored: Python `Fraction` and C++ Boost programs both `EXACT_FAMILY_OBSTRUCTION`, column 201, score $24998348431654956215746/1000000000003000000000000$, slack `66062736801751370160`, the false one-pose dual refused (exit 2); 703.0 s; binary `d5ecc193a842c21e86281c7facdc4f92a70cec92a28f5f7e002ed5d3a77cf51c`, byte for byte the CI run’s |

Every control gave the exit the contract states: the 36 kernel runs of A to E, the five
of F, the two of G on the release’s own `exact.py` and the three of H, 72.5 CPU-seconds
in all for the kernel runs; the E caps held with 8,143 and 181 nodes to spare (GN-5). A
budget exit is `unresolved`, never an acceptance (GC-5), and the replay kept the full
30,000,000 nodes per slab.

A control of this review’s own design on the real density (item 10): every weight scaled
by $985/1000$ keeps every orbit fact but the mass, which falls to $787803/20000$, and
makes every capture $985/1000$ of the original’s. `sqverify-fast` at direction 0 and
side $B$ refused it with an exact witness: the horizontal square centred at
$(5.2043\ldots, 6.2013\ldots)$, on the top edge of the centre domain, captures
$0.98667\ldots$ of the copy scaled by $5000/4999$, below 1, so the scaled density
captures $0.98647\ldots$ there, below $\tau$. The kernel on slabs 0 and 1 refused within
56 nodes at the width floor, its centre bound $0.98648$ at $(u, v) = (0.9998, 0.97)$ and
$(0.999, 0.992)$, the same corner; a width-floor or budget exit is `unresolved`, never
an acceptance. Nothing of this is retained as a receipt: the commands and outputs are in
the review’s scratch directory, and the control costs seconds, so it belongs in the
audit’s next contract.

What the complete replay gives and does not give is `T-145`’s: the continuous cover
reproduced with the producer’s kernel from reviewed source, deterministic across the
three compilers seen (GCC 15.2 and 13.3 in the receipts, 13.3 here); the axis statement
decided twice; the finite steps decided again by other code; and the nodal statement at
401 directions as a consistency check.
No second method decides the continuous cover.

## Findings

### GN-1 — Non-blocking, robustness: the near-axis containment margin is $5 \times 10^{-10}$

$B - AW(\varepsilon) = 5.05 \times 10^{-10}$, ten times thinner than `T-145`’s
$4.72 \times 10^{-9}$, because $A$ was chosen as close to $B/W(\varepsilon)$ as the
denominator $250000000$ allows; one step of $1/250000000$ in $A$ breaks it (the audit’s
control G, which the release’s own `exact.py` also refuses, item 7). The other margins
are wide: the axis minimum is $1.69 \times 10^{-3}$ above $\tau$ on $g_-$ and the
crate’s least capture at side $A$ is $1.69 \times 10^{-3}$ above on $g$, against
`T-145`’s $3.6 \times 10^{-6}$. The chain is sound only in exact rationals, as before: a
replay must not round, and any decimal restatement of $A$ or $\varepsilon$ is a
different claim.

### GN-2 — Non-blocking, record: the ZIP is not the pinned tree, and the pose binaries are `T-145`’s

As with `T-133` and `T-145` (GC-3): the tree’s `results/` holds the producer’s local run
(`source_commit` null, GCC 15.2.0, Python 3.14.4, 858.95 s at four workers, pose binary
`a5dcfa3e…`, axis `a3a82b57…`), the ZIP’s the GitHub Actions run (`6a65957e…`, GCC
13.3.0, Python 3.12.3, 1,587.30 s, pose `69bc9e64…`, axis `19288b2f…`); `SHA256SUMS`
differs in those four lines.
Both are retained and named.
The pose binaries are `T-145`’s, since the kernel source and the flags are unchanged;
the axis binaries are new only because `run.py` now builds that source at `-O3` with the
pose kernel’s flags.
The build here reproduced both CI binaries.

### GN-3 — Non-blocking, record: the audit’s price was half the measured cost, by the host’s load

Stage 1 priced the slabs at 2,604 to 2,626 CPU-seconds from both receipts scaled by
`T-145`’s replay here; the replay took 5,242.6 CPU-seconds.
Slab for slab the CPU-seconds here are 1.97 times the local receipt’s and equal to the
CI receipt’s within 0.3% (slabs 0, 1 and 42: 68.6, 322.1 and 134.0 against 32.8, 158.6,
66.0 and 67.6, 327.3, 104.6), where the calibration run, `T-145`’s replay, took 0.98 of
its local receipt at a load average of 3 to 14. A CPU-second on a core shared by five or
six runnable processes does about half the work, so the price understated the cost on
this host by a factor of two and the work by nothing; the records lane should record the
measured figure and say why it differs.
The wall time, 12,629 s at two workers, is 3.5 hours against the 22 minutes priced,
across two runs of the stage, the first stopped by the session’s two-hour limit on a
background command; the host was shared at a load average up to 27.0 on four cores.

### GN-4 — Non-blocking, first-party tooling: nothing here decides the continuous cover

GC-4 of the 10 October review stands unchanged: `sqverify-fast` decides the axis
statements and the 401-direction nodal statement, and the continuous cover is decided by
the producer’s kernel alone.
The confirmation of this claim is therefore *reproduced with the producer’s code*, as
`T-145`’s is, and the register entry’s claim, composition and case-record sentences must
say so with those words.
A first-party interval kernel with the angle as an interval dimension remains the W7
slice the 10 October review specified; wand125’s verifier (GN-7) is now a second
candidate, external.

### GN-5 — Non-blocking, confirmed: the kernel contract holds at the new parameters without re-tuning

The synthetic controls B to E are defined from $B$ and $\tau$ in closed form, so they
moved with the side; every one of the 36 kernel runs gave the exit the contract states,
the E cuts closed within 251,857 nodes against the cap of 260,000 and the E gap within
140,819 against 141,000, and the C and D refusals that reached the 1,500,000-node budget
are the ones that did for `T-145` (the two cuts on `[410000,415000]` and four of the
five gaps). Control H’s refusing threshold is this release’s: $62593/62500 = 1.001488$,
just above the minimum $1.0014864\ldots$ (the kernel admits numerators and denominators
to $10^6$, so $1001487/10^6$ stops at its input bounds), beside $1.001486$ proved and
the contract’s $1/2$, which is below the minimum and proved, as `T-145`’s replay found.
A budget exit is `unresolved`, never an acceptance (GC-5), and the replay kept the full
30,000,000 nodes per slab.

### GN-6 — Non-blocking, scope: `OBSTRUCTION.md` is a statement about a family, replayed and not registered

The release’s negative result, that no nonnegative weighting of the 2,526 original
uniform orbits gives a uniform per-square charging contradiction at $X \ge 168/25$, was
reproduced here with both of the release’s programs (item 8) and agrees with both
receipts to the last digit.
It is not an upper bound on $s(40)$, not a lower-bound proof at $6.72$, and says nothing
about densities with new supports, as the release says; it is retained with the release,
mapped as a non-registered request (`s40-support-family-obstruction`), and bears on no
register value. Nothing here decided it a second way, and this review did not read its
two programs.

### GN-7 — Non-blocking, record: wand125’s continuous-angle verifier is now published, and a replay of it would change the confirmation’s mark and nothing in the rung

wand125’s comment, edited 2026-10-12T02:19:26Z after stage 1 read it, now pins the
verifier’s source: `wand125/square-packing` at
`f30cc2cf345a3a3f6af778925f354d9ec979868b`, `tools/sqverify_continuous`, version v3,
`source_sha256` `1266a8b9…`. The record’s read of that commit is bead `think-xzob`
(2026-10-12), which this review relies on and does not repeat: the tool is this
repository’s `sqverify_fast` crate with a continuous-angle mode added (`src/slab.rs`,
786 lines, and a run function in `main.rs`), whose `interval.rs`, `axis.rs`, `exact.rs`,
`oracle.rs` and `rotated.rs` are byte for byte this repository’s and whose
`certificate.rs` is wand125’s own `proof_net` admission, without the declared-net
review’s fixes; its method is `T-145`’s in outline (branch and bound over $(u, v, t)$,
monotone angle enclosures, a concave-section trapezoid bound, interval-only
classification, translation derivatives, an exact axis patch near $t = 0$), with 86 root
ranges, no floating screen and $\varepsilon = 10^{-7}$. On this density it reports
`VERIFIED`, 86 of 86 roots, 118,717,888 nodes, least certified $0.99980000000759$, 1,130
s at six threads in the comment and 1,355 s in its README; its controls (every weight
$\times 985/1000$; $B = 3348/3359$) refused.
It is a third party’s report: no run directory, receipt or binary digest is published,
and nothing here has read its source.
Nothing new was run for it here.

What a replay of it here would change, judged by `epistemics.md`:

- **The relation, and the confirmation’s mark.** Its entry would be
  `independent-implementation` with respect to the producer’s kernel: no file shared
  with `continuous_pose.cpp`, written from the mathematics and the certificate format;
  not clean-room, since its author read that kernel during the `T-145` review, which its
  `independence_record` must say.
  With respect to this repository’s first-party route it is `shared-components` (the
  interval arithmetic, admission, D4 expansion, exact axis sweep and exact oracle, each
  named). The continuous cover, the one part of this claim decided today only by the
  producer’s code, would then take the relation furthest from the producer among its
  deciders, `independent-implementation`; the near-axis statement (the crate) and the
  finite steps (the audit) already have one; so the result would take *confirmed,
  independently re-implemented* in place of *confirmed, reproduced with the producer’s
  code*. That is the whole change.
- **The rungs.** None.
  `C3`’s predicate is met today by the kernel replay (below), and “two independently
  written implementations using the same method, or two different methods, do not change
  the rung”; `V3` likewise.
  `V4`/`C4` need two retained adversarial reviews and a human oversight record, which a
  replay is not.
- **The attributes beside the rung.** The count of distinct machine methods stays at
  one: independent code, not an independent method, as the comment and `PROVENANCE.md`
  say. Should wand125 publish a run directory and receipts at the pin, an
  `independently-external` entry (a third party’s own replay, retained here) would show
  as a third party’s retained replay beside the rung, again without moving it.
- **What it needs first.** Retention at `f30cc2c`; a mapped soundness review of
  `slab.rs`, the run function and `certificate.rs` against its lemmas C1 to C6, with the
  10 October review of the C++ kernel as its model; a build at the pinned source digest;
  then the replay at one thread, about 2.3 CPU-hours for this density by its README (4.4
  for both $n = 40$ claims with controls), which `think-xzob` prices and which waits for
  an owner budget. Until then the comment confirms nothing here, and the record’s
  sentence that the mode is unpublished should be restated as published and unretained.

### GN-8 — Non-blocking, scope of the controls: what was and was not run

The release’s `tests/test_kernel.py` (the 160-case finite oracle) and
`tests/test_admission.py` were not run here; `T-145`’s review ran the oracle by hand and
its replay did not.
They are regression controls (GC-8). The replay ran the release’s own
synthetic, budget, rounding, flush-to-zero and compilation controls, the review’s
closed-form controls B to E, G on the release’s `exact.py` and H on the axis kernel, and
the audit refuses seven finite mutants.
The reviewer’s own control is item 10: the real density with every weight scaled by
$985/1000$, which every checker that accepted the original must refuse.

## Where the Comment, the Release and the Record Differ

- The comment, the release, both receipts and wand125’s comment agree at every number
  read here: $X$, the raise, $B$, $M$, $\tau$, $A$, $\varepsilon$, $T$, the counting
  margin, 685 orbits (522 and 163), the mass, 43 slabs, 60,500,889 nodes, 30,250,466
  leaves, 13,812,428 bisections, the least bound, the axis minimum and its $3293^2$
  vertices, 858.95 s and 1,587.30 s at four workers, wand125’s 1,552 s at six, the three
  digests, and the dual’s column, score and slack.
- The comment says the ZIP “contains the separate CI receipt”; it contains it in place
  of the tree’s (GN-2), as both earlier releases did.
- Stage 1 read wand125’s comment before its edit; the record’s sentence that the
  continuous-angle mode is unpublished is out of date (GN-7) and the records lane should
  restate it.
- The release says the claim has “no external independent geometry review”; this review
  and wand125’s are the first two, both AI-assisted, neither a human oversight record.
- The packet README’s “not run here” list (the 43 slabs, the controls, the tests, the
  duals) is answered by this replay except for the release’s tests (GN-8); the records
  lane updates it with the receipts.

## Significance

`T-145` was scored `S3` as the strongest lower bound on record at $n = 40$, by a
technique new to the record, and the 11 October final review kept `S3` on comparison
with `T-095`, `T-099`, `T-100` and `T-102` to `T-111` (single-count certificate raises,
all `S3`) and the `S4` set (repairs of published values, bound families, optimality
proofs), with the note that the kernel’s reuse at a second count would make it a bound
family and an `S4` question.
This claim raises $n = 40$ by a further $0.00218$ with no new technique: the same two
kernels, the same slabs and threshold, on a density with 163 new supports and new
weights, found by a dual pricing the release does not ask to be reviewed.
It is a single-count raise on an existing technique, the strongest lower bound on record
at $n = 40$ once registered, and the reuse is at the same count, so it is not the bound
family the final review had in mind.
`S3` on the precedent of `T-099`, `T-100` and `T-145`; the score is the registering
lane’s.

## The Rungs the Evidence Supports

By [`epistemics.md`](../../../epistemics.md), the checker derives `V3` from evidence
that is exact-algebraic or interval-certified, of any origin, with a certificate, a
replay command and a passing replay status.
The kernel-replay entry this review supports has all four: method `interval-certified`,
the certificate `certificate/certified_candidate.json.gz`, the replay command
`audit_n40_new_supports run-replay` then `check-replay` printing `REPLAY_HOLDS`, and
`replay_status: passed` with its receipts retained.
**`V3`.**

`C3` needs confirming-origin evidence (`replayed-here`, `audited-here` or
`independently-external`) that is exact-algebraic or interval-certified, with a
certificate, a replay command and a passing replay, and at least one named control path.
The kernel replay is `replayed-here`, interval-certified, with the certificate, the
command and `passed`, and its controls are retained (`receipts/controls.jsonl.gz`,
`receipts/control-G-release.json`, `tests/test_audit_n40_new_supports.py`); the finite
audit and the crate’s axis decision are `audited-here`, exact-algebraic, with their own
commands and passing status.
The predicate is met exactly.
**`C3`**, confirmed, reproduced with the producer’s code (the relation closest to the
producer among the entries that decide the bound; the near-axis and finite entries are
independently decided and stand beside it).

`V4` and `C4` need two retained adversarial AI reviews by distinct reviewers whose
latest verdict accepts the claim, and a retained human oversight record.
This review is one; the 11 October final review covers `T-145`’s kernel and density, not
this density, and does not count for this claim; wand125’s review is a comment, not a
retained review record.
**Not `V4`/`C4`.**

What remains, and what each remaining step would change: a second adversarial AI review
by a distinct reviewer and a human oversight record would take the claim to `V4`/`C4`,
neither of which a replay supplies.
A replay of wand125’s `sqverify_continuous` here, after its soundness review and on a
budget the owner sets (`think-xzob`), would move the confirmation’s mark from
*reproduced with the producer’s code* to *independently re-implemented*, because the
continuous cover would then have a decider whose relation to the producer’s kernel is
`independent-implementation` (with an independence record that says its author read the
kernel), and would leave `V3`/`C3` where they are; the method-distinct count beside the
rung would stay at one, since it is the same method in independent code (GN-7). A
first-party interval kernel with the angle as an interval dimension (GN-4) would do the
same for the mark with a clean-room record, and no more for the rung.
A retained run directory from wand125 at the pin would add a third party’s retained
replay beside the rung, `independently-external`, without moving it.

## Disposition

No finding blocks registration at `V3`/`C3` with the replay evidence.
GN-2, GN-3 and GN-7 are record obligations for the records lane: retain both receipts
and name them (done in the packet), record the measured price, and restate wand125’s
verifier as published and unretained; GN-4 fixes the wording of the confirmation; GN-5,
GN-6 and GN-8 record what was checked; GN-1 is a note for the author and the replayer.
The reviewer’s own checks are evidence and not a rung: what was proved here is the
density’s admissibility (nonnegative, bounded, invariant, of mass $M$), the near-axis
containment at the new $A$ and the counting at the new $X$, on `T-145`’s lemmas; what
was checked by computation here is every finite quantity, both derived inputs’ identity,
both CI binaries’ identity, all 43 slabs and the axis certificate with the producer’s
kernels, the axis statement by the crate, the 401-direction nodal statement, a refusal
control of this review’s own on the real density scaled by $985/1000$ (the crate with an
exact witness, the kernel on two slabs), the contract’s controls, and the release’s
duals; what no first-party route decides is the continuous cover (GN-4).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
