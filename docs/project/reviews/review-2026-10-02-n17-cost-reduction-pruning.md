---
title: n17 Cost Reduction by Pruning
date: 2026-10-02
status: planning-review
---
# n17 Cost Reduction by Pruning

**Session:** 168, BC-418, lane F1. **Baseline:** `c045e43f`, with W7 and A admitted
under exp-249 and the [residue process review](review-2026-10-02-n17-residue-process.md)
costing the global half at $4\times10^{3}$ to $4\times10^{4}$ CPU-hours.
**Question:** which sound changes to *how many* certificates the global half needs, and
*how large* each one is, could keep it at hundreds of CPU-hours, and how do they
compose? Lane F2 covers raw performance engineering (compiled backends, faster sweeps);
this review does not, and says where a lever borders on it.

This review changes no bound, verdict or frontier field.
Its computations are read-only and run on one worker in the session scratchpad
(`lanes/f1/`: `residue_structure.py`, `shell_structure.py`, `conditioned_tests.py`,
`coverage_queue.py`, `coverage_queue_mp.py`, their logs and JSON outputs, one kernel
receipt and one branch-and-bound estimate), outside the record for the usual reason.
They use the retained selector’s exact consumer and its float search, the retained
kernel tool and the retained branch-and-bound pilot; every float verdict below is a
search result, never a margin, and every count conditional on a flag is a projection.

## Summary

- **The cost is a product, and the count is the factor the record has not yet
  optimised.** The revised model is several hundred to about a thousand sub-pattern
  certificates of arity 8 to 15 at 2 to 9 CPU-hours each, plus a per-state tail at 5 to
  15 CPU-hours each. Every certificate so far was chosen either by the selector’s
  bottom-up sweep (compact classes, by arity) or by the survey’s deletion-minimal shrink
  of one state; neither chooses for the number of residue orbits a certificate removes.
- **The residue is the endpoint’s Hamming neighbourhood, and that is what makes it
  coverable.** Under the 90 flags, 2,256 orbits survive; 95 are one square away from an
  endpoint image, 810 two, 920 three.
  Every one enters at least one of the endpoint’s seven empty cells: side-W1 in 1,129
  orbits, interior-NE in 1,118, interior-SE in 1,097, interior-NW in 966, side-E2 in
  840, interior-SW in 790, interior-S in 323. The flags already cover 11 of the 17
  one-square moves into interior-NW or interior-NE and none of the 17 into side-E2,
  interior-SE or interior-SW. A certificate that contains an entered cell and avoids a
  state’s left cells excludes that state; the residue is a covering problem over
  (entered, left) pairs, and the distance-2 shell alone is covered by six arity-8
  classes if those six are infeasible.
- **Coverage alone is the wrong queue key; locality must be combined with it.** 77,356
  connected arity-8 classes occur in a residue state and lie in no endpoint image, of
  which the priority subset tested 7,790; the best-case greedy cover is nine if all were
  infeasible. But the 488 highest-coverage candidates, spread over three or four walls,
  were all placed by the selector’s search in a median of one attempt and 0.16 s each.
  Infeasibility lives in compact crowds, which by locality have middling coverage.
  The two locality-filtered queues (arity 8 at three to five missing pairs; arity 9 at
  at most two, which no sweep has touched) are reported in section 2.6.
- **Two sharing ideas are dead on the cheap probe.** A certificate with one owner’s
  domain fattened to the hull of its cell and a neighbour is placed within ten attempts
  for every one of nine variants of three flagged classes: a cell’s width is a hundred
  times the $4\times10^{-3}$ to $10^{-2}$ margins.
  Conditioning one wall square’s angle to any of four bands does not make an arity-6 or
  arity-7 north-wall pattern unplaceable in sixteen searches, so angle conditioning does
  not substitute for a cell at low arity.
- **The size levers are a second-order core at 16 to 32 rows and a Taylor relaxation for
  the branch and bound.** The envelope core loses half the row’s half-width per core in
  every direction, $1.2\times10^{-2}$ per link at 64 rows, which is the size of the
  margins and why 64 rows were needed; an octagon core loses the square of that.
  A node’s size and its verification time scale with rows times partner rows, so 16 to
  32 rows are a four- to sixteen-fold cut in both, measurable by re-running W7. The
  branch and bound’s interval coefficients lose first order on corner-to-edge rows and
  resolve boxes to about a twentieth of the margin; the Taylor form the capture review
  specified resolves to the square root, about 35 times coarser per angle dimension.
- **The plan reaches about $10^{3}$ CPU-hours on count and size alone, and hundreds only
  with a short tail or with lane F2’s backend.** Sweep the residue’s arity 8 to 10
  universe in float (about 35 CPU-hours), certify in marginal-coverage order with the
  size levers, and leave a per-state tail whose count is the one number that decides the
  outcome. Its falsifier is a sweep whose flags cover less than half of the residue.
  The two measurements that decide it, the sweep and the W7 re-run at 32 rows, cost a
  CPU-day and an hour.

## 1. What Sets the Cost

The revised cost model of the residue process review, section “The cost model, revised”,
has four terms, and this review treats each as count times size times rate:

| Term | Count | Unit size and cost today | Where chosen |
| --- | ---: | --- | --- |
| The 90 selector flags, 2 certified | 88 | kernel 0.3–0.5 h or branch and bound 0.15 h to over 100 h, plus verifier 0.4–1.5 h | the selector’s bottom-up sweep, compact classes first |
| Q1’s new classes, arity 8 to 15 | several hundred to about 1,000 | 2–9 h with verification | the survey’s deletion-minimal shrink of each sampled state |
| Per-state tail | what the above leaves | 5–15 h; two K2 runs stall at 0.7 h with no contraction | one node per orbit |
| Near-endpoint at $U'$ | 0–150 | 10–50 h | Q1’s feasibility search, now empty |

The rate (CPU-seconds per row, per facet inequality, per LP) is lane F2’s. The size
(rows per owner, partner rows per step, nodes per tree) and the count (how many
certificates, each removing how many orbits) are this review’s, and the record shows
neither has been chosen for cost yet: the sweep’s order is arity then missing pairs,
which is a proxy for infeasibility, not for orbits removed; and the survey’s shrink
deletes the least-involved cell until deletion places the rest, which finds an
irreducible pattern of the state, not the one that covers most of the residue.
The survey said as much (“minimal means irreducible under deletion, not smallest”), and
its 19 confirmed classes remove 4 to 539 orbits each, median about 40.

Two arithmetic facts frame everything below.
First, a sub-pattern certificate of arity $k$ transfers to every state containing an
image of it, so the orbits it removes fall steeply with $k$: among the residue, the
best-covering arity-8 subset of a sampled state covers about 1,100 to 1,250 orbits, the
best arity-11 about 440 to 470, the best arity-14 about 70 and the best arity-15 about
26 (section 2.3). Second, every certificate is paid for twice, by its producer and by
the standing verifier that re-derives it in full, so a size lever counts in both and
again in every re-verification after a checker change.

## 2. The Residue, Measured Here

All figures in this section are planning evidence from the scratchpad scripts, computed
with the selector’s exact consumer on the 90 flags (2,256 orbits) and checked against
the survey where the two overlap: the north-wall class’s coverage comes out at 539, the
survey’s number.

### 2.1 Shape

| Property | Orbits of 2,256 |
| --- | ---: |
| Hamming distance to the nearest endpoint image 2 / 4 / 6 / 8 / 10 / 12 | 95 / 810 / 920 / 363 / 66 / 1 |
| Full walls (corner, three side cells, corner) 0 / 1 / 2 / 3 / 4 | 440 / 1,172 / 578 / 64 / 2 |
| Walls with at least four of five cells, 1 / 2 / 3 / 4 | 6 / 228 / 1,092 / 930 |
| Interior cells 1 / 2 / 3 / 4 / 5 / 6 | 2 / 43 / 400 / 1,301 / 496 / 14 |
| Corner cells 1 / 2 / 3 / 4 | 15 / 205 / 880 / 1,156 |

Ninety per cent of the residue has three or four walls at four cells or more, and 80%
has at least one full wall.
The endpoint has two full walls (south and north) and two at four of five.

### 2.2 Entered and Left Cells

Read each residue state against its nearest endpoint image and map through the symmetry
that takes that image to the endpoint’s own labelling.

| Entered (one of the endpoint’s seven empty cells) | Orbits | Left (one of its seventeen) | Orbits |
| --- | ---: | --- | ---: |
| side-W1 | 1,129 | interior-N | 746 |
| interior-NE | 1,118 | interior-E | 700 |
| interior-SE | 1,097 | interior-W | 560 |
| interior-NW | 966 | side-N2 | 501 |
| side-E2 | 840 | side-N0 | 428 |
| interior-SW | 790 | corner-NE | 389 |
| interior-S | 323 | the other eleven | 145–342 each |

The distance-2 shell is 95 (entered, left) pairs: 17 of 17 survive for side-E2,
interior-SE and interior-SW, 16 of 17 for side-W1 and interior-S, and 6 of 17 for
interior-NW and interior-NE. So the selector’s 90 flags, all compact crowds, bite on the
two interior cells nearest the north-west and north-east corners and not at all on the
three cells that complete a wall or sit in the south-east and south-west.

**What this means for the count.** A certificate $P$ with entered part $P\setminus E$
and endpoint part $P\cap E$ excludes the state $E-A+B$ exactly when
$P\setminus E\subseteq
B$ and $P\cap E$ avoids $A$. For the distance-2 shell with entered cell $b$ that is one
certificate for each way of avoiding the left cell, and three arity-8 certificates with
pairwise disjoint endpoint parts would clear all 17. The best-case greedy cover of the
shell by arity-8 classes of its own states is six (marginals 43, 34, 11, 4, 2, 1), by
arity-9 classes [SHELL9], and the distance-4 shell of 905 orbits [SHELL4]. These are
upper bounds on usefulness, not predictions: they say the residue is combinatorially
coverable by few patterns, and leave open which of those patterns are infeasible.

### 2.3 Found Against Best Coverage

For each surveyed state with a confirmed minimal class, the coverage of that class
against the best coverage of any connected subset of the same state, of the same or
lower arity, that lies in no endpoint image (a subset of an endpoint image is placeable
by the endpoint’s own pose and is excluded from the count):

| State (survey index) | Distance | Found arity, coverage | Best coverage at arity 8 / 9 / 10 / 11 | At the found arity |
| ---: | ---: | --- | --- | ---: |
| 2 | 4 | 10, 148 | 1,115 / 914 / 655 / — | 655 |
| 22 | 4 | 11, 80 | 1,200 / 917 / 654 / 437 | 437 |
| 25 | 8 | 11, 160 | 1,248 / 1,013 / 757 / 474 | 474 |
| all 19 | — | median about 40 | — | 3 to 9 times the found coverage |

The ceiling is four to nine times the found coverage at the found arity, and far more at
arity 8. The qualification that matters: every arity-7 subset of every residue state was
placed by the selector’s complete arity-7 sweep, and the 488 highest-coverage arity-8
candidates are placed in a median of one attempt (section 2.5). Coverage is
anti-correlated with infeasibility, because a pattern contained in many residue states
is a typical pattern, and typical patterns are feasible.
The useful candidates are the compact crowds that happen to have the largest coverage
among crowds, which the survey’s north-wall class (arity 8, four missing pairs, 539
orbits) exemplifies and the priority subset’s rule of at most two missing pairs
deferred.

### 2.4 The Candidate Universe

Connected classes that occur in some residue state and lie in no endpoint image, with
their residue coverage, and the greedy set cover of the residue if every one were
infeasible:

| Arity | Classes | Of them, tested by a sweep | Coverage: max / median / at least 100 | Greedy cover, all infeasible | Picks to 90% |
| ---: | ---: | ---: | --- | ---: | ---: |
| 8 | 77,356 | about 7,000 (the priority subset, at most two missing pairs) | 1,251 / 342 / 67,158 | 9 | 3 |
| 9 | 142,115 | none | 1,065 / 205 / 105,014 | 12 | 5 |
| 10 | [UNIV10] | none | [UNIV10] | [UNIV10] | [UNIV10] |
| 11 | [UNIV11] | none | [UNIV11] | [UNIV11] | [UNIV11] |

By missing pairs at arity 8, the compact end of the universe is 797 classes with none,
2,174 with one, 4,582 with two (the priority subset’s range), 6,675 with three, 9,007
with four and 10,260 with five; at arity 9 it is 256, 1,050 and 2,983 with none, one and
two.
The sweep that tests them is cheap: a placed class costs the selector’s search about
0.16 s on this machine (section 2.5), so the untested arity-8 universe is about three
CPU-hours of first-stage search plus the deep stage for whatever is flagged, and arity 9
about six.

### 2.5 Fat Domains and Angle Bands

Two sharing ideas, probed with the selector’s search under a reduced deep budget (12
starts, 24 hops, 64 and 64 deep attempts, finish), on the north-wall class (arity 8,
confirmed by the survey at $4.1\times10^{-3}$), W7 (admitted) and the top arity-8 flag
(corner-SW, corner-NW, side-S0, side-W0, side-W1, side-W2, interior-SW, interior-NW, at
$3.5\times10^{-3}$):

| Probe | Baseline | Variants | Outcome |
| --- | --- | --- | --- |
| One owner’s domain replaced by the convex hull of its cell and a neighbouring cell | all three unplaced at 165 attempts, penetrations $4.2\times10^{-3}$, $1.1\times10^{-2}$, $3.5\times10^{-3}$ | nine (interior cells fattened toward the centre or sideways, side cells along the wall) | all nine placed, in 1 to 10 attempts, 0.1 to 1.5 s |
| One wall square’s angle confined to a band (axis $[0,0.12]$, mid $[0.12,0.55]$, tilted $[0.55,1.02]$, steep $[1.02,\pi/2]$ rad) | the north wall plus side-W2 and side-E2 (arity 7), the north wall plus interior-NW (arity 6) and a sampled state’s best arity-8 subset, all placed | sixteen (side-N1 and side-N0 banded) | all placed, in 1 to 6 attempts |

The first result is the one to remember: a cell is about $0.7$ wide and the margins are
$10^{-2}$, so any domain that is a union of cells is placeable, and a certificate can
share across cells only through what the kernel already does, the transfer by
containment and symmetry.
The second says angle conditioning does not lower the arity of a wall crowd by one; it
leaves open joint conditioning on two or three angles at arity 8 to 10, which was not
probed.

### 2.6 The Coverage Queues

The selector’s `recheck_flag` (sub-pattern witnesses first, then the class with warm
starts) run under a screen budget (12, 24, 48, 48, finish) and, for a class the screen
cannot place, the selector’s full budget, over candidates ordered by residue coverage:

| Queue | Candidates screened | Flagged | Search cost | Coverage range |
| --- | ---: | ---: | ---: | --- |
| Arity 8, pure coverage order (missing pairs 5 to 14) | 488 | 0 | 80 s | 1,251 to 1,041 |
| Arity 8, three to five missing pairs, by coverage | [Q8] | [Q8] | [Q8] | [Q8] |
| Arity 9, at most two missing pairs, by coverage | [Q9] | [Q9] | [Q9] | [Q9] |

[Q8Q9-READING]

### 2.7 Two Prover Measurements

**A feasible wall prefix under the kernel.** The full west wall (corner-SW, side-W0,
side-W1, side-W2, corner-NW), which the selector places, run through
`check_n17_subpattern` at 64 rows for six rounds: [WALL]. This bears on the
shared-prefix idea of section 4: a parent node on a pattern common to many residue
states is worth building only if the kernel contracts it while it is still feasible.

**The branch and bound past arity 6.** Knuth’s estimator (`--estimate 150`) on the
north-wall class, arity 8 at $4.1\times10^{-3}$: [BB]. For A (arity 6,
$8.8\times10^{-3}$) the same estimator gave $2\times10^{4}$ to $1.2\times10^{5}$ nodes
against 41,598 actual.

## 3. Ideas That Cut the Count

Each idea: what it claims, why it is sound, the cheap measurement, the factor, and how
it composes.

### 3.1 Sweep the Residue’s Universe at Arity 8 to 10, Exactly Restricted

**Claim.** Test, in float, every connected class of arity 8, 9 and 10 that occurs in a
residue state and lies in no endpoint image, rather than the compact priority subset.

**Soundness.** The sweep certifies nothing; a flag is a candidate for the prover.
The restriction to classes occurring in a surviving state is exact for the consumer
(X048 README, “Arity 8, a Priority Subset”), because a class occurring in no surviving
state removes nothing whatever its verdict.
Excluding subsets of endpoint images is exact because the endpoint’s pose places them.

**Measurement.** It is the sweep itself: 77,356 arity-8 classes less the 7,790 tested,
142,115 at arity 9, [UNIV10] at arity 10, at about 0.16 s per placed class and the
selector’s deep budget per flag.
About 35 CPU-hours in all, a day on a few workers, and the output is exact: the set of
float-infeasible classes of arity at most 10 in the residue with their coverages, from
which the greedy cover is computed in seconds.

**Factor.** The survey found one such class in 44 states that the priority rule had
deferred, and it removes 539 orbits, a quarter of the residue, on its own.
Of the survey’s 21 shrinks, 8 ended at arity 8 to 10 by a deletion order that does not
seek the smallest; so at least a third of residue states, and likely more, have an
arity-at-most-10 certificate.
The count of certificates this replaces is the count of tail states it removes, each a 5
to 15 CPU-hour node today.

**Composition.** It is the input to 3.2 and the gate of the plan: its flags’ greedy
cover of the residue is the number that prices everything after it.

### 3.2 Certify in Marginal-Coverage Order, With a Stop Rule and Structural Routing

**Claim.** Order the admitted queue by orbits removed per expected CPU-hour, recomputed
after each admission (the residue process review’s section 5.2, applied to the sweep’s
output rather than the survey’s), and stop a level when the marginal coverage of its
best remaining class times the per-state cost falls below the class’s certificate cost.

**Soundness.** The order changes nothing about any certificate; the consumer’s union is
the same set whatever the order.
The stop rule is a cost rule, not a soundness rule.

**Measurement.** The hit rate of the queues in section 2.6, and the greedy cover of the
sweep’s flags.

**Factor.** The survey’s 19 classes take 2,256 to 987 at 67 orbits per certificate,
size-biased. A greedy cover over the full flag set removes more per certificate at the
head and the same at the tail; the stop rule matters little, since a per-state node
costs 5 to 15 CPU-hours and a class certificate 2 to 9, so any class with a marginal of
two or more orbits is worth certifying.
The factor is in the head: whether a few dozen classes take the residue below a few
hundred orbits.

**Composition.** Routing by structure (kernel for wall-anchored, branch and bound for
interior crowds) is unchanged; the near-endpoint families of section 2.2 (side-W1 and
side-E2 complete a wall; interior-SE and interior-SW sit in the empty south corners) are
where the head should be sought first, since those entered cells are the ones the 90
flags do not touch.

### 3.3 Angle-Conditioned Certificates for the Tail

**Claim.** A certificate for a pattern $G$ with owner $i$’s half-angle confined to a
closed interval $[a,b]$ is the kernel’s existing `half_angle` branch predicate (kernel
spec, section 1.4); a state is excluded once admitted conditional certificates on one
owner cover $[0,1]$.

**Soundness.** Each conditional certificate is a child node of n11’s grammar; the
disjunction over a closed partition of the chart is exhaustive.
The consumer needs a new rule: per state, per owner, the union of admitted intervals
must be $[0,1]$, by exact interval arithmetic on rationals.

**Measurement.** Section 2.5 probed one owner at arity 6 and 7 and found nothing.
The next probe is joint bands on two or three squares of a tail state’s minimal class,
at arity 8 to 10, a few CPU-minutes per state.

**Factor.** Unknown; the cheap probe is negative.
It stays as the reserve for tail states whose minimal class is arity 11 or more, where
lowering the arity by three would raise coverage from tens to hundreds.

**Composition.** It multiplies the certificate count by the number of bands and divides
the arity; it is worth it only where the band count is two or three and the coverage
gain is tenfold.

### 3.4 Fewer Cells

**Claim.** A D4-symmetric capacity-one cover with 23 cells has
$\binom{23}{17}=100{,}947$ states, 3.4 times fewer than 24 cells; with 22,
$\binom{22}{17}=26{,}334$, 13 times fewer.

**Soundness.** Any capacity-one cover with the family in one state is admissible; the
bulk-exclusion review’s cover search found 24 and did not report trying 23.

**Measurement.** The cover design search re-run for seven interior cells (and six), with
the exact checker; a day.
The falsifier of H-F1 applies: no such cover holds the family in one state with margin.

**Factor.** Unclear in sign for the residue: larger cells raise the arity at which
crowds become infeasible, so a smaller census can leave a residue that is harder per
state. Not on the plan’s path; recorded because it is the only lever on the census
itself.

### 3.5 Ideas That Do Not Cut the Count

- **Lower cap.** The census cap sits $4.7\times10^{-4}$ above $S^{\ast}$ and every
  sampled residue state is infeasible by $9.1\times10^{-3}$ or more; a wall-anchored
  pattern gains at most the cap difference in margin, five per cent, and an interior
  crowd nothing. The ladder keeps its two uses from the residue process review and is not
  a count lever.
- **Symmetry beyond D4.** The container has none, and the transfer rule (containment
  plus the eight images) is already the whole of what a certificate on closed cells
  implies. Cell-inclusion dominance is empty on this cover, which has overlaps but no
  cell inside another.
- **Several covers.** A packing realises a state in each cover, so excluding a packing
  needs a certificate in one of them, and the joint states are the states of the
  intersection cover, a refinement with more cells.
  That is the kernel’s row refinement by another name, inside a leaf, not a bulk lever.
- **Dominance between states.** Removing a square from a state adds freedom, so an
  exclusion never transfers to a state with fewer of its cells; containment is the only
  monotone direction, and it is in use.
- **Fat domains.** Dead, section 2.5.

## 4. Ideas That Cut the Size

### 4.1 A Second-Order Core at 16 to 32 Rows

**Claim.** Replace the producer’s envelope core (the axis square of side
$(B-\text{slack})/\text{factor}$ at the row’s midpoint angle, `counting.row_envelope`)
by the intersection of the two end-angle squares, as the capture review specified for
the capture producer (section 5, item 2), and run exclusions at 16 or 32 rows.

**Soundness.** The octagon lies strictly inside both end squares and, by convexity of
the support function in the angle, inside every square between; it is still passed
through `strict_core`, so the checker is unchanged.
Fewer rows change only the producer’s proposals.

**Why it is a size lever.** A row of half-width $\delta$ in angle has envelope side
$1/(\cos\delta+\sin\delta)\approx1-\delta$, so each core loses $\delta/2$ in every
direction and a collision link uses two cores: $1.2\times10^{-2}$ at 64 rows over the
quarter turn, which is the size of the margins ($3.5\times10^{-3}$ to $10^{-2}$) and the
reason A plateaued at 32 rows and needed 64. The octagon’s loss is second order, about
$\delta^2/2$: $7\times10^{-5}$ at 64 rows, $3\times10^{-4}$ at 32, $1.2\times10^{-3}$ at
16\. A node’s step cost, its saved size (W7: 3,712 rows, 19,282 partner cover rows,
7,752 collision regions, 16 MB) and its verification (75 minutes for W7, all of it rows
times partner rows times facets) scale with rows squared, so 32 rows is a fourfold cut
and 16 rows sixteenfold, before any compiled backend.

**Measurement.** Re-run W7 at 32 and 16 rows with the octagon core; record closure,
steps, rows, regions and verifier time.
An hour on one worker at 32 rows.
Falsifier: W7 does not close at 32 rows with the octagon, which would mean the loss that
needs 64 rows is not the core’s but the one-sided row bounds’.

**Composition.** Multiplies with every count lever and with F2’s rate; it is the one
lever that lowers the per-state tail’s unit cost without touching the arithmetic.
The capture pilot 2 needs the same core, so the build is shared.

### 4.2 The Taylor Relaxation for the Branch and Bound

**Claim.** Linearise each pair row’s support at the box centre so the loss is the
second-order remainder, as the capture review’s route (b) specifies, instead of the
interval coefficients’ first-order loss on the eleven corner-to-edge rows.

**Soundness.** The same Farkas closures with outward rounding; the remainder is bounded
by interval arithmetic on the second derivative.
The review calls it a few days of build on the existing tool.

**Why it is a size lever.** With first-order loss about $20\rho$ against a margin $m$, a
box closes at $\rho\lesssim m/20$; with second-order loss about $33\rho^2$, at
$\rho\lesssim\sqrt{m/33}$. At $m=10^{-2}$ that is $5\times10^{-4}$ against
$1.7\times10^{-2}$, 35 times coarser per angle dimension, and the tree is what the
certificate is (A: 41,598 nodes, 53 MB, 26 minutes to verify).

**Measurement.** `--estimate` on A and W7 after the swap; minutes.
[BB-COMPOSE]

**Composition.** It is the branch and bound’s analogue of 4.1 and applies to the
interior crowds the kernel stalls on.

### 4.3 Counting Packets for Wall Crowds, After a Prefix

**Claim.** n11’s 59 fields were counting packets (mode B): a majority feature that two
charged cells are each forced to capture, proved per cell per row with no pairwise
collision regions, so a certificate is linear in cells times rows (the 46 n11 packets
replay with 18,855 rows in all).
The residue’s dominant entered cells complete a wall (side-W1, side-E2), and wall crowds
are mode B’s shape.

**Soundness.** The checker exists (`sqpack/hull_kernel/counting.py`, the mask-0 replay);
a packet is admitted only for a unit-weight feature with required owners whose owned
points are proved.

**The obstacle, measured from the record.** n11’s required owners owned points from
their cells alone; n17’s side cells, $0.911$ deep and $0.705$ wide, own nothing from the
cell (every side cell has zero seed points in every receipt), and only corners and some
interior cells do. A packet for the north-wall crowd therefore needs side-W2 and side-E2
pinned first, which is a mode-A contraction: the W7 closure pins side-W2 to
$0.11\times0.05$ by round 4. So mode B here is a hybrid: a stalled mode-A prefix on the
wall supplies the owned points, and the packet closes.
That is new grammar (a packet whose required owners cite a node’s final hulls) and a
producer with no n17 precedent.

**Measurement.** Hand-build one packet for the north-wall crowd from the W7-style
prefix, replay it through the counting checker; a day.
Falsifier: no feature with two forced captures exists at the margins the prefix leaves.

**Factor.** For the classes it fits, a certificate of seconds in place of hours, and a
verification of seconds.
The fraction of the residue it fits is bounded by the wall families: 1,969 of 2,256
orbits enter side-W1 or side-E2, with overlaps.

### 4.4 Size Levers That Do Not Pay

- **Minimal owner sets.** A certificate should cite only owners that own or collide; W7
  already is minimal, since removing any cell makes it placeable.
  Nothing further.
- **Sampled verification.** The admission rule is a full re-derivation, and the
  branch-and-bound review showed why: the witness-path controls caught four of sixteen
  mutants and the full check every one.
  Size, not sampling, is the lever on verification.

## 5. Unit Levers Short of Compiling

Two producer-policy changes alter what a node is rather than how fast a row is checked;
they border on lane F2 and are listed, not planned.

- **Shared prefixes.** A stalled node on a pattern common to many residue states (a full
  wall, two walls) is a sound outer bound for those owners in every superset state, so a
  child that adds owners and starts from the parent’s final state is sound by the
  kernel’s invariant. This is new grammar (a child that adds owners; n11’s children add a
  predicate) and pays only if feasible prefixes contract.
  Section 2.7’s wall run says [WALL-SHORT].
- **Sub-cell seeds.** A side cell split along its long axis gives two half-cells of
  diameter below one that own points from the seed; the split is n11’s centre halfplane
  predicate, existing grammar, at the cost of two children per split owner.
  It attacks the reach problem (B: four of six owners never own a point; the K2 states:
  11 and 14 of 17) that the margin does not.
  Unmeasured here.

## 6. The Ranked Plan

| Rank | Step | Cost | Removes or saves | Assumption | Falsifier |
| ---: | --- | ---: | --- | --- | --- |
| 1 | Re-run W7 at 32 and 16 rows with the octagon core (4.1) | 1–2 CPU-hours | a 4- to 16-fold cut in every kernel certificate’s size and verification | the envelope core’s loss is what needs 64 rows | W7 fails to close at 32 rows with the octagon |
| 2 | Sweep the residue’s arity 8 to 10 universe, exactly restricted (3.1) | about 35 CPU-hours of float search | the full flag set with coverages; the greedy cover’s size | at least a third of residue states have an arity-at-most-10 certificate | the flags’ greedy cover removes less than half of the 2,256 |
| 3 | Certify the sweep’s flags and the 88 remaining selector flags in marginal-coverage order, routed by structure, at the rows step 1 allows (3.2) | 40–120 class certificates at 0.5–3 h each: 20–360 CPU-hours | the residue to a few hundred orbits | hit rate and coverage of the sweep; the prover closes arity 8 to 10 as it closed 6 and 7 | more than half of the flags of arity 8 to 10 stall under both provers at the rows that closed W7 and A |
| 4 | Taylor relaxation for the branch and bound, then its estimates on the stalled interior classes (4.2) | days of build, then minutes | the interior crowds the kernel stalls on | the capture review’s loss model | estimates above $10^{6}$ nodes at arity 8 |
| 5 | The tail: per-state or minimal-class nodes at the smaller size, with sub-cell seeds where owners own nothing (5) | the tail count times 1–5 CPU-hours | the rest | tail count at most about 200 | the tail exceeds 300 orbits, or nodes still stall at 2 CPU-hours |
| 6 | Mode B after a wall prefix for the wall families (4.3), if step 5’s unit cost stays above 2 CPU-hours | a day of build, then seconds per packet | the side-W1 and side-E2 families | a forced double capture exists | none found on the north-wall crowd |

**The arithmetic.** With steps 1 to 3 and a tail of 200 orbits at 2 CPU-hours: 90 flags
at 0.5 to 3 hours (50 to 250), the sweep (35), 40 to 120 class certificates (20 to 360),
the tail (400), the capture (100 to 400, unchanged from the capture review): about 600
to 1,450 CPU-hours.
With a tail of 100 orbits and the lower unit costs, about 400 to 800.
Without step 1 the class and tail terms are four to sixteen times larger and the total
is back at $2\times10^{3}$ to $10^{4}$. So the count and size levers alone take the
model from $4\times10^{3}$ to $4\times10^{4}$ down to about $10^{3}$, a four- to
forty-fold cut, and hundreds is reached only when the tail is short (step 2’s
measurement decides this) or when lane F2’s rate gain multiplies in; the two compose
multiplicatively, since every term here is count times size times rate.

**What the plan rests on, and what ends it.**

1. *Residue states have small certificates.* Falsified if step 2’s flags cover less than
   half of the residue; the tail is then over a thousand orbits and the global half is a
   per-state job whose price is F2’s to set.
2. *The rows can be cut.* Falsified if W7 needs 64 rows with the octagon core.
3. *The provers scale one arity level.* Falsified if the arity-8 to 10 flags stall at
   W7’s and A’s settings; the branch and bound’s Knuth estimate on the north-wall crowd
   (section 2.7) is the first reading.
4. *Coverage-ordered certification is not fooled by false flags.* The selector’s finish
   stage and the batch controls of the residue process review stand; a high-coverage
   flag that is false costs one failed certification, and the review-by- weight rule
   reads every certificate removing more than one per cent of the census.

## Evidence Status

| Kind | Items |
| --- | --- |
| Measured from the record | the cost model’s terms; the survey’s 19 classes and their coverages; W7’s and A’s sizes and verification times; the seed points per cell in every receipt; the K2 stalls; the envelope core’s loss formula (capture review) |
| Measured here, planning evidence | the residue’s shape, entered and left cells, the distance-2 shell; found against best coverage; the candidate universe and its greedy covers; the pure-coverage queue; the fat-domain and angle-band probes; the locality queues; the wall-prefix stall; the branch-and-bound estimate |
| Derived here, needing review | the covering-design reading of the residue; the second-order core’s loss and the rows-squared scaling of size and verification; the conditional-certificate consumer rule; the mode-B hybrid’s need for a prefix |
| Estimated | every cost figure in section 6; the 35 CPU-hour sweep; the tail count |
| Conjecture | that a third or more of residue states have an arity-at-most-10 certificate; that the provers close arity 8 to 10 as they closed 6 and 7 |

## Addendum, 2026-10-03: What the Ranked Plan’s First Steps Found

The lanes that took up this plan corrected two of its derivations and settled two ranks,
both against the plan.

**The second-order core in section 4.1 needs a scale factor.** Lane K2 found that the
intersection of a row’s two end-angle squares is not inside every intermediate square.
A point in the mid-angle direction escapes by about $h(1/\cos(\Delta/2)-1)$, where
$\Delta$ is the row’s angular width.
For a point $p$ inside both end squares,
$p\cdot u_\theta \le h\cos(\theta-\mathrm{mid})/\cos(\Delta/2)$, so scaling the octagon
by $\cos(\Delta/2)$ is enough (lane C1’s derivation).
K2’s committed core (`d97187d52`) uses $\cos^2(\Delta/2)=(1+\cos\Delta)/2$, which is
rational in the half-angle chart.
The exact $\cos(\Delta/2)$ is generally irrational there.
The loss stays second order.
The smallest support over each row’s end and middle directions is 0.4981 at 16 bins,
against the envelope core’s 0.4924 at 64. The exact factor would give 0.4990, and a
rational bound $\max(\cos^2, 1-D^2/8)$ with $D\ge\Delta$ would recover nearly all of it.
Soundness never rests on the factor: the checker’s `strict_core` re-proves in exact
arithmetic that every core vertex lies strictly inside the square at every turn of the
closed row interval, and the independent verifier repeats that obligation.
A factor that is too large makes a certificate fail to check; it cannot certify a false
exclusion.

**The size lever is linear in rows, not quadratic.** Lane F2’s
[performance review](review-2026-10-02-n17-cost-reduction-performance.md) measured the
32-bin and 64-bin receipts.
The row sweep is linear in rows, and only the collision share is quadratic: 11 per cent
of the checker and about a sixth of the verifier.
Halving rows therefore roughly halves a node; it does not quarter it.

**Rank 4 is settled: its falsifier is met.** Lane P2 built the Taylor relaxation with
exact verifier support (`ff5471e89`). Knuth estimates on the arity-8 classes I8 and N8
stay above $10^{6}$ nodes in every form tried: interval, Taylor, a coupled McCormick
form, and pre-split centre boxes.
P2’s diagnosis is that 80 to 85 per cent of the closable open nodes are held by the
range of each pair’s separating normal over the angle box.
That is a per-pair disjunction, and no relaxation of the trigonometric coefficients
removes it. The branch and bound therefore stays at arity seven and below, and interior
crowds at arity eight go to the kernel.
The receipts are in
[`receipts/bb-rank4/`](../../../packing/campaign/explorations/X048-session-168-pilots/receipts/bb-rank4/).

**Rank 1 is settled: its falsifier fired.** W7 at 32 bins with the octagon core does not
close. The producer reached a fixed point after 11 rounds and stopped by itself: 77
steps, 2,464 rows, 1,052 s. The result is a certified stall
([receipt](../../../packing/campaign/explorations/X048-session-168-pilots/receipts/kernel-octagon-W7-bins32.json)).
The octagon contracts much further than the envelope core did at 32 bins.
Corner-SW and the three west sides fall to between 10 and 17 live rows of 32. But no row
of side-N0, interior-SW or interior-W ever dies, and side-N0’s residual box freezes from
round 6 at $0.590\times0.911$. At 64 bins all of side-N0’s rows died in one step.
Lane K2’s reading is that the octagon removes a coarse row’s core loss but not its
domain loss. A row’s residual, and the partner cover built from it, is the union over
every angle in the row, and halving the bins doubles that sweep.
So core size was not what kept W7 open at 32 bins, and the four- to sixteen-fold size
cut this plan assumed is not available this way.
Kernel certificates stay at 64 bins.
Adaptive rows, bisected in angle only where a residual or partner cover is wide, are the
untested form of the lever.

**What this does to the arithmetic.** Without rank 1, section 6 puts the class and tail
terms back at four to sixteen times its lower figures.
Lane F2’s rate levers multiply in: the verifier rewrite measured 17.6 times on W7, and
the producer and checker levers are estimated at 2 to 3 times.
The total therefore rests on count and rate.
Rank 2 decides the count.

**Rank 2 is running.** Lane S2’s sweep tool (`16ea38d81`) reproduces this review’s
universe counts at arity 8 and 9. Its first 3,000 classes, the highest-coverage arity-8
classes of the first queue, gave one flag: a south-wall crowd that removes 539 of the
2,264 residue orbits by itself.
That class is next for the kernel, at 64 bins.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
