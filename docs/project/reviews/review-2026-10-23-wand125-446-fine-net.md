# wand125’s Fine-Net Lower Bounds of #446 at n = 19, 20, 26 and 27: Mathematical Review

2026-10-23. Reviewer: Claude (Anthropic), `tbd-strong-max` tier at maximum reasoning,
the stage 4 mathematical review lane `c-review-t233-math` of the 23 October intake pass
(bead `think-bwis`), prompted separately from the records lane that registered the entry
and sharing none of its context beyond the brief and the committed record.
Workflow:
[result-import.md, stage 4](../../../packing/campaign/result-import.md#stage-4-validate),
“The review”. Scope: the four certificates of T-233, the entry the records branch
`claude/intake-2026-10-23-lower-bounds` registers (head `5690db065`, not yet on `main`),
read from that branch without checking it out.
This review registers nothing, moves no bound and publishes nothing; the records lane
commits it.

## Summary for the Author

**Decision: accept all four certificates.** For `mixed_n19_L48275`, `mixed_n20_L49125`,
`mixed_n26_L5555` and `mixed_n27_L5655` the argument from the certificate to the claim
is correct and complete, and every hypothesis it needs holds in exact arithmetic.
If $n$ unit squares fitted in the closed square of side $L$, their cores at the declared
net’s angles would be $n$ disjoint sets of measure at least one each, against a total
mass of $n - 1/100000$. Each certificate in fact proves the strict bound $s(n) > L$.

The one condition that needs a large computation, that at each of the 2,073 net
directions every core captures mass at least one wherever its centre may lie, rests on
your two complete runs of `sqverify-proof-net`. This review read them as data and did
not repeat them. What it could decide cheaply, it decided with programs of its own that
share no code with yours or with this repository’s verifier:

- every exact premise, at all four counts, and the net’s reach over every orientation;
- direction 0 of each net, completely, by a vertex argument of its own; the least
  capture and its vertex are the ones your sweep logs;
- the exact capture at your 124 oblique control witnesses, equal to your logged
  fractions;
- the exact capture at the centre of every direction’s least-bound box (8,288 poses) and
  at the end of an independent search at 32 directions of each net (2,176 poses): every
  value is at least 1, and at least your certified bound.

The least capture found is $1.0003$, at n = 26, so the certificates keep a few
ten-thousandths of slack where your certified bounds stop just above 1. There is no
blocking or major finding.
Three minor findings are for this record: the credit line, the scope of the read, and
the replay’s price. The notes for you concern the README’s control filename, the
soundness document beside the verifier archive, and the upstream commit the bundle
names, which jlevy/squares does not hold; by file digest, your archive is this
repository’s reviewed crate with `certificate.rs`, its tests and two documents changed.
Questions are at the end.

The values stand as reported (`V0`), and with this review as the read, `C1`. A complete
replay here with the reviewed `sqverify-fast` and whole-net controls, priced at 10.5 to
19.2 CPU-hours for the four, would carry each count to `V3/C3`.

## The Claims

Each certificate is a format M rectangle measure in D4 orbits, with no point or segment,
on the net it declares, `proof_net {"step": "1/5002", "last": 2072}`, at core side
$B = 4999/5000$, and of total mass $M = n - 1/100000$.

| n | Certificate | Claim | Rows | Distinct images | Pinned at | Asset SHA-256 | Gain over the case |
| ---: | --- | --- | ---: | ---: | --- | --- | --- |
| 19 | `mixed_n19_L48275` | $s(19) \ge 1931/400 = 4.8275$ | 347 | 2,776 | `61e37d5` | `9d1aea51…8ccb` | $1/400$ over T-103 |
| 20 | `mixed_n20_L49125` | $s(20) \ge 393/80 = 4.9125$ | 471 | 3,768 | `61e37d5` | `0ccc62a0…fb76` | $3/400$ over T-104 |
| 26 | `mixed_n26_L5555` | $s(26) \ge 1111/200 = 5.555$ | 615 | 4,916 | `61e37d5` | `ae4dc5e8…1074` | $1/100$ over T-105 |
| 27 | `mixed_n27_L5655` | $s(27) \ge 1131/200 = 5.655$ | 714 | 5,696 | `bf85d6b` | `4f1b449a…59cf` | $23/2000$ over T-106 |

The n = 27 certificate is the author’s follow-up of 8 October on the issue; it
supersedes the issue’s $2261/400$, which is not reviewed here.
At n = 26 the 4,920 images make 4,916 distinct rectangles and at n = 27 the 5,712 make
5,696, coincident images merging by adding their densities; at n = 19 and 20 no two
coincide. Each side is below the case’s upper bound on `main` ($3 + 4\sqrt2/3$, $5$,
$7/2 + 3\sqrt2/2$ and $5 + \sqrt2/2$). The retained data are the release packet
[`wand125-fine-net-lower-bounds-446-release-2026-10-08`](../../../packing/resources/web/wand125-fine-net-lower-bounds-446-release-2026-10-08/README.md),
whose candidates this review read from the branch as data.

## The Argument, Re-Derived

**The measure.** Write each row as $R_j = [x_1, x_2] \times [y_1, y_2]$ with mass
$m_j \ge 0$; the field order is `[x1, y1, x2, y2]`, as the source’s `SPEC.md` §2 says.
Each of the eight images $S(R_j)$, $S$ in the symmetry group $D_4$ of $K = [0, L]^2$,
carries $m_j/8$ uniformly:

$$
g = \sum_j \frac{m_j}{8\,|R_j|} \sum_{S \in D_4} \mathbf 1_{S(R_j)} .
$$

So $g \ge 0$, $g$ is $D_4$-invariant, and $\int g = \sum_j m_j = M$. The field order was
not assumed: the other reading gives rectangles of no positive area at 5 to 19 rows of
each file, and this review’s exact capture reproduces the source’s own exact capture
values only under this reading (Controls, below).

**The net (N1).** The nodes are $t_r = r/5002$, $r = 0, \dots, 2072$, at angles
$\theta_r = 2\arctan t_r$, with $\cos\theta_r = (1 - t_r^2)/(1 + t_r^2)$ and
$\sin\theta_r = 2t_r/(1 + t_r^2)$, both rational.
The last tangent is $t_{2072} = 1036/2501$, and
$t_{2072}^2 + 2t_{2072} - 1 = 367/6255001$ is positive, so
$t_{2072} > \sqrt2 - 1 = \tan(\pi/8)$. The bins $[t_r - D/2, t_r + D/2]$, $D = 1/5002$,
are contiguous from $-D/2$ and so cover $[0, \tan(\pi/8)]$. The last bin is needed: its
lower end $4143/10004$ gives $-22423/100080016 < 0$, so $\tan(\pi/8)$ lies in it.

**The fold (N2).** A unit square’s angle is defined modulo $\pi/2$. For each square
separately, a reflection in $D_4$ maps it to a square of angle $\varphi \in [0, \pi/4]$
in $K$; because $g$ is invariant, a core proved for the image pulls back to a core of
the same measure strictly inside the original square.
The fold is per square and needs no single reflection of the whole packing.
With $u = \tan(\varphi/2) \in [0, \tan(\pi/8)]$ and a node with $|u - t_r| \le D/2$, the
relative turn has $z = \tan(\delta/2) = |u - t_r|/(1 + u t_r) \le D/2$, since
$u, t_r \ge 0$.

**The shrink (N3).** The concentric square of side $B$ at angle $\theta_r$, seen in the
unit square’s frame, is turned by $\delta$, and its extent along each of the unit
square’s axes is $B(1 + 2z - z^2)/(1 + z^2)$. That function increases on
$[0, \sqrt2 - 1]$ (its derivative is $2(1 - 2z - z^2)/(1 + z^2)^2$), so its largest
value on the bin is at $z = D/2$:
$B(1 + D - D^2/4)/(1 + D^2/4) = 500400014977/500400085000 < 1$. The weaker form the
checkers test is $B(1 + D) = 25009997/25010000 < 1$, margin $3/25010000$, and the
tangent form is $B(1 + D/(1 - D^2/4)) = 500400014977/500400075000 < 1$. So every core
lies in the open unit square, with a clearance of $6.997 \times 10^{-8}$ per edge at a
bin’s end, which is what makes the cores of two packed squares disjoint even where the
squares touch. The shrink is tight: the core is $0.9998$ of the square, against $0.9977$
on the standard net, and that is what the finer net buys.

**The per-bin domain (lemma D) and the quarter turn (C1).** A unit square at
$u \in [a_r, t_r + D/2] \cap [0, \tan(\pi/8)]$, $a_r = \max(0, t_r - D/2)$, has
half-width $\rho(u) = (\cos\varphi + \sin\varphi)/2 = (1 + 2u - u^2)/(2(1 + u^2))$,
which is the extent function above halved and so increases there; its centre therefore
lies in $[\rho(a_r), L - \rho(a_r)]^2$. A quarter turn about $(L/2, L/2)$ preserves $g$
and maps the core at $\theta_r$ to the core at $\theta_r + \pi/2$, the same square, so
the capture is invariant and the quadrant $\Omega_r = [L/2, U_r]^2$,
$U_r = L - \rho(a_r)$, suffices.
A reflection reverses the angle and is not used for this reduction.
Every $\Omega_r$ is nonempty (its least width is $1.7066$ at n = 19), and at its far
corner the core at $\theta_r$ still lies in $K$, by at least $1.0994 \times 10^{-7}$
(node 1).

**Counting (N4).** If $n$ unit squares packed in $K$, each would hold a closed core of
measure at least $1$ in its open interior; the cores are pairwise disjoint, so
$n \le \sum_i \int_{Q_i} g \le M = n - 1/100000$, a contradiction.
Hence no packing of side $L$ exists, and by compactness $s(n) > L$; the claims state
$\ge$.

**So covering the net proves the bound** when, for every $r = 0, \dots, 2072$ and every
centre $c \in \Omega_r$, the closed core $C_B(c, \theta_r)$ satisfies
$\int_{C_B(c, \theta_r)} g \ge 1$. Everything else above is exact arithmetic on the
file, which this review recomputed.
That coverage statement, 2,073 two-dimensional minimisation claims per certificate,
whose least certified margins in the source’s runs are $1.5 \times 10^{-11}$ to
$1.4 \times 10^{-10}$, is the whole computational content, and only a complete run of an
interval checker decides it.

**What the deciding checker assumes.** The source decided coverage with
`sqverify-proof-net`, its adaptation of this repository’s `sqverify_fast` at a commit it
names as `fe12e036c` (build source digest `ab6e33e1…`). As its `SPEC.md` §3 to §5
describes it, and as this repository’s
[`SOUNDNESS.md`](../../../packing/sqverify_fast/SOUNDNESS.md) proves for the maintained
crate, whose kernel files the source’s archive holds byte for byte (F-8), the decision
assumes:

- exact admission: rationals read exactly, the measure expanded and its total equal to
  $M$, lemma N0’s premises (a) to (e) on the declared net;
- at $r = 0$, an exact-event vertex sweep (lemmas A1, A2): the capture is bilinear on
  the cells of the event grid, so its least value is at a vertex;
- at $r \ge 1$, interval branch and bound over boxes of centres covering a superset of
  $\Omega_r$: inside and outside rectangles by the triangle inequality with a slack of
  $10^{-9}$ (R1, F2), a trapezoid lower bound on each straddling rectangle’s area (R2),
  and a mean-value penalty from enclosed partial derivatives (R3 to R5); a box is
  accepted when the downward-rounded bound is at least the threshold;
- binary64 arithmetic with directed steps of $|x|2^{-52} + 2^{-1074}$ per operation
  (I1), exact enclosures of rationals (I2), and admission caps that keep every
  intermediate finite (F3);
- that the compiled program on its machine computed what its source says, and that the
  logs are the run’s.

The census route this repository would replay with is the maintained crate, source
`d97758bb…`, whose soundness, declared-net change and controls were reviewed on 3 and 6
October; it shares all of this with the source’s checker apart from the declared-net
reader.

## What This Review Ran

Every program is this lane’s own, in
[`review/review-2026-10-23/programs/`](../../../packing/resources/web/wand125-fine-net-lower-bounds-446-release-2026-10-08/review/review-2026-10-23/README.md)
of the release packet, and each wrote one receipt under `outputs/`. They use Python
3.14.7 (`fractions`, `hashlib`, `json`, `zlib`) and, for the float search and one matrix
product, numpy 2.5.2 on OpenBLAS 0.3.34 at one thread.
They import nothing from this repository, the source or the maintained route.
None of the source’s programs ran.

| Program | Decides | Result | CPU (s) |
| --- | --- | --- | ---: |
| `premises.py` | premises | `ALL_PREMISES_HOLD` at all four | 1.1 |
| `custody.py` | premises | `ALL_CUSTODY_HOLDS` | 0.1 |
| `crate_identity.py` | premises, by digest | 16 of 20 archived files identical at `e020eb1e2` | under 1 |
| `net_cover.py` | premises | `NET_COVERS`, 10,363 orientations | 1.0 |
| `geometry_selftest.py` | nothing (a test) | `PASS`, 18 of 18 fixtures | 0.9 |
| `receipts_check.py` | poses | `ALL_CONSISTENT` | 61.6 |
| `axis_decide.py` | direction 0, completely | `AXIS_DIRECTION_DECIDED` at all four | 16.3 |
| `direction_sample.py` | poses | `NO_COUNTEREXAMPLE_IN_SAMPLE`, 128 directions | 471.4 |
| `controls.py` | nothing (a test) | `EVERY_CONTROL_REFUSED` | 25.8 |

The final runs took 579 CPU-seconds; with the trial runs, about 12 CPU-minutes in all,
against the brief’s ceiling of two CPU-hours.

**Premises.** `premises.py` read each candidate strictly (one gzip member, no float
token, no duplicate key, every number a decimal or `p/q`) and recomputed: the stored and
decompressed SHA-256 against the retention record and both receipts; $n$, $L$ equal to
the register’s side, $B = 4999/5000$, the net, no points; the field order; every mass
positive, the listed total equal to `total_mass` $= n - 1/100000 < n$, and the expansion
integrating back to it; lemma N0 (a) to (e), the sharp extent, the last bin, every
domain nonempty, the core inside $K$ at every domain corner; F3’s caps (eight times the
densest row is $2.6 \times 10^6$ to $5.7 \times 10^6$, far below $2^{32}$). All hold at
all four counts, and so does every premise the source’s summary prints, including its
counts of distinct images.
The source’s `candidate_digest` is the SHA-256 of the candidate as JSON with sorted keys
and compact separators; this review reproduced it at all four.
`custody.py` re-derived every retained member’s digest from its bytes, the asset digests
against the source’s `ASSET.json` and the 8 October packet, and the documents against
the subtree manifest.
All hold; the source’s sealed inventory differs from the retained files only in
`README.md`, as the lane recorded.

**The net, by geometry.** `net_cover.py` did not use the closed forms.
At every node and five rational tangents in its bin (both ends, both quarter points, the
node) it built the unit square and the core in exact rationals and checked every core
vertex strictly inside the unit square, $|z| \le D/2$, and $\rho(u) \ge \rho(a_r)$:
10,363 orientations, no failure, least clearance $6.9967 \times 10^{-8}$ at the end of
bin 0, equal to the sharp extent’s margin.

**Direction 0, decided.** `axis_decide.py` decides the axis direction of each
certificate completely and by itself.
Every coordinate’s denominator divides $Q = 10^{17}$, so the events $x_1 \pm h$,
$x_2 \pm h$ in $[L/2, L - 1/2]$ and the overlap lengths $o_k$, $p_k$ at them are exact
`int64` multiples of $1/Q$. The capture at every grid vertex is one matrix product in
binary64 over nonnegative terms, rounded inputs and densities rounded down, so the true
value is at least the computed one divided by $(1 + \gamma_K)(1 + 2^{-53})^3$ in any
summation order; the comparison with $1$ is exact.
The least value over the closed quadrant is at a vertex, by the bilinearity argument
above, which this review proved for itself.

| n | Events | Vertices | Rigorous least capture | Exact at the least vertex | Least vertex |
| ---: | ---: | ---: | --- | --- | --- |
| 19 | 2,272 | 5,161,984 | $1.0015172217253$ | $1.0015172217257$ | $(3.3278000117622, 3.3278000117622)$ |
| 20 | 3,132 | 9,809,424 | $1.0010018543801$ | $1.0010018543805$ | $(3.4128000000674, 3.4128000000674)$ |
| 26 | 4,020 | 16,160,400 | $1.0009906901489$ | $1.0009906901495$ | $(3.4992363535086, 5.055)$ |
| 27 | 4,743 | 22,496,049 | $1.0009178105187$ | $1.0009178105193$ | $(3.1555000876186, 3.9308719988476)$ |

Each event count and vertex count equals the one the source’s sweep logs, and each least
vertex is the source’s logged argmin to the last digit; the source’s certified bound
sits $1.7 \times 10^{-10}$ to $3.3 \times 10^{-9}$ below the exact value, as an
outward-rounded sweep should.
The 64 smallest vertices were evaluated again in fractions, and the least one a third
time by the clipping geometry; all agree.
So index 0 of each certificate is decided by an implementation that shares nothing with
the source: 1 of 2,073 directions per count.

**The source’s logs, read as data.** `receipts_check.py` found each run log complete:
2,073 rows, indices 0 to 2072 once each, every one `verified` at threshold 1 with a
bound of at least 1, the sweep at index 0 and branch and bound elsewhere, every rotated
search tree complete (nodes $= 2 \times$ leaves $- 1$), node and CPU totals equal to the
summary, the summary `VERIFIED` with no refusal, its input digest the candidate’s. At
every rotated direction the exact capture at the centre of the source’s least-bound box
is at least 1 and at least that box’s certified bound: 8,288 poses, none below.

| n | Threads | Direction CPU (s) | Nodes | Least certified margin (r) | Least exact margin at those centres (r) |
| ---: | ---: | ---: | ---: | --- | --- |
| 19 | 6 | 3,583.9 | 377,472,588 | $1.41 \times 10^{-10}$ (1342) | $7.45 \times 10^{-4}$ (686) |
| 20 | 12 | 8,352.8 | 410,012,470 | $1.23 \times 10^{-10}$ (2028) | $7.24 \times 10^{-4}$ (361) |
| 26 | 12 | 8,157.8 | 663,387,112 | $3.41 \times 10^{-11}$ (905) | $3.38 \times 10^{-4}$ (1349) |
| 27 | 12 | 12,675.8 | 648,972,154 | $1.49 \times 10^{-11}$ (1801) | $6.41 \times 10^{-4}$ (1056) |

The control logs scale every mass by $197/200$ at 32 directions spread evenly over the
net ($\mathrm{round}(k \cdot 2072/31)$). At each of the 31 rotated ones the source’s
`exact_coverage`, a rational with a denominator of up to about 300 digits, equals this
review’s exact capture at the witness pose times $197/200$ as fractions: 124 of 124
across the four counts.
That is two separately written exact evaluators agreeing on the measure, the angle
$2\arctan(r/5002)$, the core and the scaling.
At index 0, where the source’s sweep reports a refusal without a witness flag, this
review’s exact capture at the logged argmin times $197/200$ is $0.9865$, $0.9860$,
$0.9860$ and $0.9859$; so all 32 refusals of each control have an exact witness below 1.
Every witness lies in its per-bin quadrant.

**A stratified sample of rotated directions.** `direction_sample.py` searched for the
least capture at 32 rotated directions of each certificate: index 1, the last index, the
source’s least-certified direction, the direction whose least-bound centre had the least
exact capture above, and one seeded index in each of 28 equal strata.
The search is its own: a $49 \times 49$ grid over $\Omega_r$ and a compass search from
the best point of each of 16 blocks; one more search starts at the source’s least-bound
box and is reported apart.
Every end point was evaluated exactly.
This decides nothing between the points it evaluates; it can only find a counterexample,
or a value below the source’s certified bound, and it found neither.

| n | Directions | Exact points | Least found (r) | Least from independent starts (r) | Median least per direction | Least gap above the source’s bound | 99/100 witness |
| ---: | ---: | ---: | --- | --- | --- | --- | ---: |
| 19 | 32 | 544 | $1.000676$ (686) | $1.000863$ (940) | $1.001535$ | $6.8 \times 10^{-4}$ | 32 of 32 |
| 20 | 32 | 544 | $1.000651$ (1041) | $1.000651$ (1041) | $1.000925$ | $6.5 \times 10^{-4}$ | 32 of 32 |
| 26 | 32 | 544 | $1.000308$ (1349) | $1.000332$ (1358) | $1.001035$ | $3.1 \times 10^{-4}$ | 32 of 32 |
| 27 | 32 | 544 | $1.000495$ (1830) | $1.000495$ (1830) | $1.000901$ | $4.9 \times 10^{-4}$ | 32 of 32 |

Every exact value is at least 1 and at least the source’s certified bound at its
direction. The start at the source’s box went lower than every independent start at 6 of
the 128 directions, so the independent search is the heuristic it claims to be, and its
values are upper bounds on each direction’s least capture.
The least values lie $3 \times 10^{-4}$ to $1.7 \times 10^{-3}$ above 1, against
certified bounds of about $1 + 10^{-7}$: the certified margins are where the source’s
branch and bound stopped, not what the certificates have.
Under the 99/100 mutant, every sampled direction has an exact witness $0.83$ to $0.97$
percent below the threshold.
The search made 1,177,612 float evaluations.

**Controls on this review’s checker.** `controls.py` mutated in-memory copies and
recorded what each check did:

- the strict reader refused a duplicate key, a float token, a negative mass and a second
  gzip member;
- the premises refused a total mass of exactly $n$, a step of $1/4999$ (so
  $B(1 + D) = 1$) and a last index of 2071 (the net stops short of $\tan(\pi/8)$);
- the axis decision decided none of the 99/100 mutants: their rigorous least captures
  are $0.99150$, $0.99099$, $0.99098$ and $0.99091$;
- at the 31 rotated control witnesses of n = 19, the right conventions reproduce all 31
  of the source’s fractions, and each wrong one reproduces none: the other field order,
  the standard net’s step $83/40000$ (the failure mode of DR-1 of the 6 October review),
  half the declared step, and the rows without their $D_4$ images;
- the 99/100 mutant’s exact capture is below 1 at the least point of all 32 sampled
  directions of n = 19.

## Trust Boundaries and What the Checkers Share

| Checker | Decides | Trusts |
| --- | --- | --- |
| The source’s `sqverify-proof-net` (`fe12e036c`, source digest `ab6e33e1…`) | Coverage at all 2,073 directions, twice (check2 run and pre-publication run) | This repository’s reviewed kernel (16 of 20 files byte-identical at `e020eb1e2`) and its own `certificate.rs`, which nobody here has read; rustc 1.98.0 on x86_64; its machines; that the logs are the runs’ |
| The maintained `sqverify-fast` (source `d97758bb…`), for the replay | Coverage at all 2,073 directions, with whole-net controls, once run | The reviewed crate, census driver and controls; rustc 1.98.0; this host |
| This review’s programs | Every exact premise; direction 0 completely; the capture at the 8,288 least-bound centres, the 8 axis argmins, the 124 oblique control witnesses and the sample’s search ends | CPython 3.14.7’s `fractions`; IEEE binary64 in OpenBLAS `dgemm` under the stated bound; its own code |

The source’s checker and the maintained crate share the whole crate apart from the
declared-net reader, so a replay with the maintained crate is a re-implementation
sharing the producer’s components, as T-205 to T-207 are.
This review’s programs share no code with either.
All three share the mathematics (N1 to N4, lemma D, C1) and the reading of the format
(the $D_4$ average, `[x1, y1, x2, y2]`, a row’s mass its whole mass); the reading is
confirmed against the source’s own exact values, and the mathematics was re-derived
above. An error in that shared mathematics would pass all three; none was found.
Authorship overlaps at the level of the system family: the source’s commits `7400660`,
`61e37d5` and `bf85d6b` carry `Co-Authored-By` trailers naming Claude, the crate the
source adapted was written by a Claude agent of this project (lane W2), and this review
is a Claude agent with its own prompt and its own files.

## Findings

No finding is blocking or major for any of the four certificates.
The mathematics holds, the files are what they say, and nothing this review evaluated
contradicts the source’s runs.

Grades: blocking, major, minor, note.
Line numbers are of the files at the records branch’s head `5690db065`, or of the
retained source files named.

**F-1 (minor, record): the credit differs from every other entry of this family.**
T-233’s claim ends “Hiroaki Hosono after Levy” at line 32122 of
`packing/frontier/results.yaml`, and its register row says “Hosono after Levy” at line
109 of `packing/frontier/RESULTS.md`. Both come from the bibliography entry
`[wand125 fine-net lower bounds 2026-10-08]` (`packing/resources/bibliography.yaml`,
line 1579, `credit: Hosono after Levy`), the only Hosono entry with that credit.
Every other register entry for these check2 measures credits “Hiroaki Hosono after
Tokoharu and Levy”: T-103 to T-106, T-132, T-142, T-143 and T-205. The source credits
code and formats to Evan Daniel, Tokoharu and jlevy/squares (the release packet README,
“Sources and Notices”). Align the bibliography entry’s credit and the claim’s credit
line with the family’s, or record why this report differs.

**F-2 (minor, record): a read recorded on the seven-count report entry would overstate
its scope.** `E-wand125-fine-net-lower-bounds-446-report`
(`packing/frontier/evidence.yaml`, line 28934) covers n = 19, 20, 26, 27 (the superseded
$2261/400$), 28, 29 and 31. This review read three of those certificates.
Record its `external_review` with the scope in the note (“read for n = 19, 20 and 26
only”), or give T-233 a reported entry of its own for those three counts, as the n = 27
follow-up already has (`E-wand125-fine-net-n27-5655-followup-report`, line 29127).

**F-3 (minor, record): the replay price applies one ratio to runs of different settings
and prices the controls at the capture’s full cost.** T-233’s
`unfinished_confirmations.estimated_cost` (`packing/frontier/results.yaml`, lines 32190
to 32200) doubles each count’s direction CPU and scales it by the n = 31 sample’s 0.689.
The source’s n = 19 run used 6 threads and the other three 12, at 9.5 against 12 to 20
µs per node, and controls have cost 8 to 40 percent of the capture.
The ceiling of 18.21 CPU-hours stands.
The per-count figures are better stated as in
[The Price of a Full Replay](#the-price-of-a-full-replay), and an eight-direction sample
of each certificate would settle them.

**F-4 (note, record): two overlong lines.** The inserted “(the 99/100 mutant at every
direction, FC-1)” leaves `next_rung` and `unfinished_confirmations.what` of T-233
(`packing/frontier/results.yaml`, lines 32178 and 32185) with a line far longer than its
neighbours. Reflow when next edited.

**F-5 (note, record): wording.** The claim says the source reports “every such core
capturing mass at least one”; what is checked is every core at a net angle centred in
that angle’s per-bin domain, as the bundles’ README says (“all centres in
$[r(a_j), L - r(a_j)]^2$”). Separately, the 8 October catalogue on `main`
(`packing/resources/web/wand125-fine-net-lower-bounds-2026-10-08/reported-catalogue.json`,
`independent_review` and `standing_results`) has run-together words (“percase”,
“source20file”, “T-102 throughT-111,FN1original”); that is outside this branch’s change.

**F-6 (note, author): the README names the wrong control file.** Line 15 of each
bundle’s `README.md` lists `check2/control.jsonl.gz`; the asset holds
`check2/control-197_200.jsonl.gz`. The same correction was asked for the 16 October
bundles on 19 October.

**F-7 (note, author): the soundness document beside the archive predates the declared
net.** Each bundle’s `check2/src/SOUNDNESS.md` (33,225 bytes, SHA-256 `16f1e679…`) is
this repository’s file at `b2c98e3bd` of 3 October, before lemma N0 was added on 5
October (`f007d7afd`); its line 19 gives the net as “here $83/40000$ and $201$”. The
bundled `SPEC.md` says at line 72 that the lemmas “are stated for a general step D”. The
proofs are symbolic in $D$, and `SPEC.md` §4 states the net lemma for the declared step
correctly, so nothing in the mathematics is wrong.
But the soundness document a reader finds beside the archive does not state premises (a)
to (e), which the checker relies on.
The archive’s own `SOUNDNESS.md` is a different file, 870 bytes longer (SHA-256
`8e7a6180…`, from the 8 October manifest), which no commit of this repository holds and
this record has not read.
Put the archive’s copy beside it, or quote lemma N0 in `SPEC.md`.

**F-8 (note, author and record): the adapted crate is the reviewed one with one file
changed, and its base cannot be named publicly.** Each bundle’s
`check2/src/UPSTREAM_COMMIT` names `42534d959d668c5e03839dc87f9e628fa4fc2d83`, which
jlevy/squares does not hold (GitHub commits API, 23 October: HTTP 422, “No commit
found”); the branch commit `fe12e036c` did not resolve on 8 October either.
By content it is identifiable: `crate_identity.py` compared the 8 October manifest’s
digests of the archive’s 20 files with this repository’s `packing/sqverify_fast`, and 16
are byte-identical at `e020eb1e2`, the source (`7c49cf79…`) the 3 October soundness
reviews and the route review accepted.
The kernel is all among them (`axis.rs`, `exact.rs`, `interval.rs`, `lib.rs`, `main.rs`,
`oracle.rs`, `rotated.rs`, `build.rs` and the lockfile).
The four that differ are `src/certificate.rs` (31,964 bytes against 30,446),
`tests/adversarial.rs`, `README.md` and `SOUNDNESS.md`, as `SPEC.md` §5 says (“one
change”). So the code the source’s two runs rest on that nobody here has read is that
one change to `certificate.rs`, the declared-net reader; the archive is pinned by digest
and was not opened. That is why the runs stand at `V0`, and why the census replay with
the maintained crate, whose own declared-net reader was reviewed, is the step that
counts. It is not a defect of any certificate.

**F-9 (note): the whole-net control should refuse everywhere.** The source’s control
samples 32 directions; the route needs the 99/100 mutant at all 2,073. At every
direction this review sampled, the least capture found was below $100/99$, so that
mutant has an exact witness 0.83 to 0.97 percent below threshold there.
Expect a census control with no verified mutant direction, unlike n = 68’s four; it
still has to run.

## Questions for the Author

1. Does the adapted `certificate.rs` at `fe12e036c` refuse a declared net that fails any
   of lemma N0’s (a) to (e), and does its per-bin `domain_upper` read the declared step?
   Your `SPEC.md` §5 says so; this record has not read the archive.
2. Could the bundle’s `UPSTREAM_COMMIT` name a public commit of jlevy/squares?
   `42534d95…` does not resolve there, nor does `fe12e036c`. By content the archive is
   `e020eb1e2` with four files changed (F-8); a published diff of `certificate.rs`
   against that commit would let a reader see the whole change.
3. Would you correct the README’s control filename (`check2/control.jsonl.gz`, the file
   is `check2/control-197_200.jsonl.gz`), as asked for the 16 October bundles?
4. The n = 19 check2 run used 6 threads and the others 12. Were the 12-thread runs on 12
   physical cores, or on 6 with two threads each?
   The per-node CPU of the four runs differs by a factor of two, which matters for
   pricing the replay here.

## Rungs and Significance

**Now.** Each count stands as the source reports it: `V0`, since both cited evidence
entries are reported with no replay.
Recorded as an `external_review` on those entries (scoped as F-2 says), this review is a
qualifying read, which supports `C1` at every count, as T-176 to T-178 hold it.
Its own runs are a sample (direction 0 of 2,073 decided, and poses) and derive no rung;
they belong in the case records.

**After a complete replay.** A maintained census at all 2,073 directions of each
retained candidate, with its whole-net control receipt (the 99/100 mutant at every
direction), held to the 6 October checklist, would support `V3/C3` at that count,
confirmed, re-implemented sharing the producer’s components.
This review is the review that reads the certificate which that checklist’s item 7 asks
for, for all four. The entry takes the least rung of its four counts.
`V4/C4` would need a second accepting adversarial review by a distinct reviewer and a
human oversight record.

**Significance.** Confirm the draft’s S3, for the entry and at each count.
No case’s verified lower bound moves now: the case records keep T-103 to T-106 in both
lower lanes until a replay.
Once replayed, each value raises its case’s verified and reported lower lanes:

| n | Lower lanes now | After a replay | Gain | Gap to the upper bound, now and after | Score |
| ---: | --- | --- | --- | --- | --- |
| 19 | $193/40$ (T-103) | $1931/400$ | $1/400$ | $0.0606$ to $0.0581$ | S3 |
| 20 | $981/200$ (T-104) | $393/80$ | $3/400$ | $0.0950$ to $0.0875$ | S3 |
| 26 | $1109/200$ (T-105) | $1111/200$ | $1/100$ | $0.0763$ to $0.0663$ | S3 |
| 27 | $11287/2000$ (T-106) | $1131/200$ | $23/2000$ | $0.0636$ to $0.0521$ | S3 |

Each is a step by the certificate kind and declared net of T-142, with no new technique,
as T-103 to T-106 were scored; none establishes an open case or a reusable method, so
none is S4 or S5, and no News entry is owed.
At n = 19 the record also holds Fitzharding’s reported Lean proof that
$s(19) = 3 + 4\sqrt2/3$ (T-194, read here on 16 October, not built), which would
supersede any lower bound if it is adopted; that does not change the score.

## The Price of a Full Replay

The census route costs the capture at every direction plus the whole-net controls.
The records lane priced it at twice the source’s direction CPU, scaled by the ratio of
0.689 that an eight-direction n = 31 sample on this host measured: 12.54 CPU-hours, or
18.21 at the source’s own CPU. Two things suggest a different split, though not a lower
ceiling:

- The controls have cost 8 to 40 percent of the capture, not 100: 160 and 108
  CPU-seconds against 1,396 and 1,415 at n = 84 and 85, 347 against 857 at n = 68. The
  sample above found a 99/100 witness 0.83 to 0.97 percent below threshold at every
  direction it ran, so these controls should refuse early everywhere.
- The source’s direction CPU mixes a 6-thread run (n = 19, 9.5 µs per node) with
  12-thread runs (12 to 20 µs per node), so one ratio does not carry across the four.
  By nodes at the 18.6 µs per node the n = 31 sample measured here, the captures are
  1.95, 2.12, 3.43 and 3.36 CPU-hours.

| n | Nodes | Capture, by the ratio (CPU-h) | Capture, by nodes (CPU-h) | Lane’s total (CPU-h) | This review’s range (CPU-h) |
| ---: | ---: | ---: | ---: | --- | --- |
| 19 | 377,472,588 | 0.69 | 1.95 | 1.37 to 1.99 | 1.4 to 2.7 |
| 20 | 410,012,470 | 1.60 | 2.12 | 3.20 to 4.64 | 2.3 to 4.6 |
| 26 | 663,387,112 | 1.56 | 3.43 | 3.12 to 4.53 | 3.1 to 4.8 |
| 27 | 648,972,154 | 2.43 | 3.36 | 4.85 to 7.04 | 3.7 to 7.0 |
| All | 2,099,844,324 | 6.27 | 10.87 | 12.54 to 18.21 | 10.5 to 19.2 |

The range takes, per count, the lower of the lane’s figure and the node-based capture
times 1.1, and the higher of the lane’s figure and the node-based capture times 1.4. An
eight-direction sample of each certificate with the maintained binary, about a
CPU-minute each, would narrow it before the four are scheduled.
At two workers the wall time is about half the CPU time on an idle host; this host’s
load was 17 to 37 on 4 cores during this review.

## Comparison With Other Reviews

**Earlier reviews of these four certificates.** None exists.
After the findings above were written, this lane searched `docs/project/reviews/` on
`main` and on the branch for the four certificate names, their sides and #446. Only
tracker records and audits name the issue
(`review-2026-10-11-final-asymptotic-and-grading.md`, line 496;
`review-2026-10-18-intake-audit.md`, line 210; eight bead-reconciliation and
owner-decision JSON files of 10 to 13 October, which dispose of beads); none reads a
certificate. The 8 October intake’s premise acceptance is recorded in the facts packet’s
catalogue, not in a review document: “the maintained `measure()`/`declared_net()`
premises accepted for all seven complete rational candidates”.
This review’s premises agree with it and with the records lane’s four
`receipts/premises-n*.json` (`EXACT_PREMISES_HOLD`, the same facts), which use the
maintained readers that this review did not read.

**The review of the n = 31 certificate on the same net.** A separate lane reviews
`mixed_n31_L59775`, which the records branch also registers.
Its document was read in draft, after the findings above were written.
The two reviews share:

- **The net.** The same exact facts, computed apart: $B(1 + D) = 25009997/25010000$,
  $367/6255001$, $-22423/100080016$ at the last bin’s lower end, the tangent form
  $500400014977/500400075000$, and the largest extent $500400014977/500400085000$ at the
  upper end of bin 0.
- **The method.** The same reduction (the fold square by square, the bins, the per-bin
  domain, the quarter-turn quadrant) and the same reading of the format, which each
  review confirmed against the source’s logged exact control captures.
  Both find the margins about a thousandth where the source’s certified bounds stop near
  $1 + 10^{-11}$, and both find the source’s run to rest on its unread adaptation of the
  crate.
- **The notes for the author.** Its M-1 is F-6 here; its M-2, the sealed `README.md`
  digest in `files-sha256.json`, holds for these four bundles too (`custody.py` lists
  `README.md` as the only difference), and this review left it unraised because the lane
  had disclosed it. Its M-3, that the receipt calls the check “independent”, is in this
  review’s trust section rather than its findings.
  Its R-1, the pending-review clauses, is section 5 of this review’s record changes.

They differ in what they decide.
The n = 31 review decides whole rotated directions of its sample, by an exact integer
branch and bound with a kernel-and-slab bound.
This review decides only direction 0 completely and evaluates poses at its rotated
directions, and it checks the source’s logs at every direction.
Its `crate_identity.py` also locates the unreviewed code in the archive, the one changed
`certificate.rs`, which bears on both reviews’ trust boundaries.

## Reproduction

From the repository root, with the project interpreter and one BLAS thread:

```bash
PKT=packing/resources/web/wand125-fine-net-lower-bounds-446-release-2026-10-08
R=$PKT/review/review-2026-10-23
FACTS=packing/resources/web/wand125-fine-net-lower-bounds-2026-10-08
export OPENBLAS_NUM_THREADS=1
packing/.venv/bin/python3 -I $R/programs/premises.py --packet $PKT --out $R/outputs/premises.json
packing/.venv/bin/python3 -I $R/programs/custody.py --packet $PKT --facts $FACTS --out $R/outputs/custody.json
packing/.venv/bin/python3 -I $R/programs/crate_identity.py --manifest $FACTS/source-manifest.json \
  --repo . --commit e020eb1e2 --commit 910b6b12c --out $R/outputs/crate-identity.json
packing/.venv/bin/python3 -I $R/programs/net_cover.py --out $R/outputs/net-cover.json
packing/.venv/bin/python3 -I $R/programs/geometry_selftest.py --packet $PKT --out $R/outputs/geometry-selftest.json
packing/.venv/bin/python3 -I $R/programs/receipts_check.py --packet $PKT --out $R/outputs/receipts-check.json
packing/.venv/bin/python3 -I $R/programs/axis_decide.py --packet $PKT --out $R/outputs/axis-decision.json
packing/.venv/bin/python3 -I $R/programs/direction_sample.py --packet $PKT \
  --receipts $R/outputs/receipts-check.json --out $R/outputs/direction-sample.json
packing/.venv/bin/python3 -I $R/programs/controls.py --packet $PKT \
  --sample $R/outputs/direction-sample.json --scratch "${TMPDIR:-/tmp}" --out $R/outputs/controls.json
```

Each exits 0 on the retained packet and prints its verdict.
The packet’s
[README](../../../packing/resources/web/wand125-fine-net-lower-bounds-446-release-2026-10-08/review/review-2026-10-23/README.md)
lists what each printed, its CPU, and what failed along the way.

## What This Review Read

Read: the brief; `packing/campaign/result-import.md` stage 4 and “Label the PR and
Prepare News”, and `epistemics.md` (rungs, independence, review records), both from the
branch; the 19 October n = 68 and n = 84/85 reviews, and the 6 October declared-net
soundness review’s scope, §1, §7, findings and checklist; this repository’s
`packing/sqverify_fast/README.md` and `SOUNDNESS.md` (to “Tests That Hold the Lemmas”),
its 3 October `SOUNDNESS.md` opening at `b2c98e3bd`, and §1.1 to §1.5 of the measure
verifier’s specification; the source’s `SPEC.md` and `UPSTREAM_COMMIT` (the copies the 6
October check2 packet retains, byte-identical to these bundles’); the retained files of
the release packet and the 8 October facts packet, as data (the acquisition records and
premises receipts in part); T-233, its two evidence entries, the case records’ lower
lanes and blockers, the branch’s other changes to the register; the register entries
T-103 to T-106, T-132, T-142, T-143, T-178 and T-205, the n = 37 report entry and the n
= 68 review’s evidence entries, and the verifier registry’s entries for the 14 October
review’s programs; the head of `packing/sqverify_fast/independence-record.yaml`, for
authorship; the records lane’s n = 31 timing receipt; beads `think-eth9` and
`think-bwis`; issue #446 and its replies; the three source commits’ messages.
After the findings were written: the tracker files that name #446, and the n = 31
review’s draft.

Not read: any code of the source (its adapted crate archive is not retained, and
`fine_net_check.sh` was not opened), this repository’s `sqverify_fast` source, the
census driver, `devtools/fine_net_followup.py`, `devtools/audit_wand125_declared_net.py`
and `devtools/check_sqverify_fast.py`; any earlier review of these four claims before
this review’s findings were written; the n = 31 review’s output before the same point.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
