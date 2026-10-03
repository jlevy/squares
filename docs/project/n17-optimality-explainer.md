---
title: The n = 17 Optimality Proof, Explained
date: 2026-10-02
status: active
---
# The n = 17 Optimality Proof, Explained

**Audience:** a careful reader who has read the [tutorial](../../TUTORIAL.md), in
particular
[§9, How an Optimality Proof Is Built](../../TUTORIAL.md#9-how-an-optimality-proof-is-built),
and wants the $n = 17$ case itself: its numbers, its records and its status.

**Owns:** the account of the proof in progress, as of 2026-10-02. Every number below is
taken from a linked record, and each claim is labelled by its evidential status:
*proved* (an exact argument, machine-checked and reviewed), *verified* (an exact or
outward-interval computation with a replay and a review), *projected* (an exact
consequence of something not yet admitted), *heuristic* (a search result that certifies
nothing), or *modelled* (an estimate).
Where this document and a record differ, the record is right.

**Does not own:** the case’s bounds, which [`n-017.md`](../../packing/frontier/n-017.md)
and the [results register](../../packing/frontier/RESULTS.md) hold, or the general
machinery, which the tutorial explains and this document only names.

## The Bracket

| Bound | Value | Who, when | Status |
| --- | --- | --- | --- |
| Best known packing | $S^{\ast} = 4.67553009360455\ldots$ | John Bidwell, 1998, building on Hämäläinen’s 1980 packing | verified: a rational ceiling $4.6755300936045509516342148538535054$ certified here ([T-065](../../packing/frontier/RESULTS.md)) |
| Its side as an algebraic number | the root of the catalogue’s degree-18 polynomial | this project, [exp-245](../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-245-h265-n17-catalogue-polynomial.md), 2026-10-02 | proved: the polynomial is irreducible and the certified side is its root ([H-265](../../packing/campaign/hypotheses/H-265-n17-catalogue-polynomial-identity.md)) |
| Best lower bound | $s(17) > 116511/25000 = 4.66044$ | Guzhou0806 / N17 project, R068, 28 September 2026, continuing Kleddamag’s charge | verified at `V3/C3`: both source checkers replayed here in full ([T-043](../../packing/frontier/RESULTS.md)) |
| Gap | $0.01509$ |  | **open** |

The known packing has ten axis-aligned squares, six tilted by about $39.80^{\circ}$ and
one by about $-36.62^{\circ}$: three orientation classes, the first case with more than
two. It is not rigid.
Square 6 is free in its hole, and squares 5, 11 and 13 slide without changing the side,
so the object to be proved optimal is a **family**, not a pose.

The frontier page and the register still carry the wording from before exp-245
identified the side with the catalogue polynomial; their update is tracked separately.

## The Three Parts

The proof follows the shape that settled $n = 11$
([T-060](../../packing/frontier/RESULTS.md)); the tutorial’s
[Three parts](../../TUTORIAL.md#three-parts) says why a counting certificate cannot do
it.

| Part | What it must show for $n = 17$ | Status on 2026-10-02 |
| --- | --- | --- |
| Local half | Every packing of side at most $S^{\ast}$ in the known occupancy state, with its 45 non-slider coordinates within $1/5000$ of the family’s, lies on the family and has side $S^{\ast}$ | **proved**, as the capture-target theorem below |
| Global half | Every packing of side at most $S^{\ast}$ lies in one of 346,104 occupancy states, and every state but the known one is impossible | the census is **verified**; two sub-pattern certificates are **verified and admitted** ([exp-249](../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-249-h267-n17-first-certified-sub-patterns.md)); the rest is open |
| Capture | Every packing in the known state at the capture cap lies within $1/5000$ of the family | a pilot is running and has not reported |

## The Cap

The exclusions run at $U = 1169/250 = 4.676$, which is $4.7 \times 10^{-4}$ above
$S^{\ast}$. The known family occupies its state at that cap with a margin of $0.002112$,
against a container slack of $0.00047$, so no translation the cap allows moves it across
a seam (verified,
[exp-247](../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-247-h266-n17-unique-state-cover.md)).

Capture cannot run at that cap.
Near the family the side rises at only $\kappa_\infty = 1/175.8$ per unit of
displacement in the softest direction, so at $U$ a packing can move about $0.08$ along
it, and about $0.02$ in the stiff directions, with side still at most $U$. Those are
packings of side above $S^{\ast}$, and the local radius is $1/5000$. The capture
therefore runs at a second cap $U'$, the upper end of a rational enclosure of $S^{\ast}$
from the root box, with $0 < U' - S^{\ast} \le 10^{-12}$, keeping the cells in the $U$
frame and centring only the wall bounds; there the first-order feasible set has radius
about $2 \times 10^{-10}$ (modelled,
[kernel adaptation specification, section 4.1](reviews/review-2026-10-02-n17-kernel-adaptation-spec.md)).

## The 24-Cell Cover

The cover is `ring-3-voronoi-8-tabbed-unique`, checked by
[`check_n17_capacity_one_cover.py`](../../packing/devtools/check_n17_capacity_one_cover.py)
and recomputed in separate code by an
[independent review](reviews/review-2026-10-02-n17-unique-state-cover.md)
([H-266](../../packing/campaign/hypotheses/H-266-n17-minimal-capacity-one-cover.md),
[exp-246](../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-246-h266-n17-capacity-one-cover.md),
[exp-247](../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-247-h266-n17-unique-state-cover.md)).
The tutorial’s
[centre box and capacity-one covers](../../TUTORIAL.md#the-centre-box-and-capacity-one-covers)
explains each argument in the table.

| Cells | Count | Shape | Capacity argument | Exact margin |
| --- | ---: | --- | --- | ---: |
| Corners | 4 | squares of side $79/100$ | depth-width wall lemma, one wall | $\max G = -0.0115$ |
| Outer wall cells | 8 | depth $911/1000$, width $529/750$ | depth-width wall lemma | $\max G = -0.00353$ |
| Middle wall cells | 4 | depth $93/100$, width $257/375$ | depth-width wall lemma | $\max G = -0.00348$ |
| Interior | 8 | Voronoi cells of eight rational sites, cut and tabbed | diameter below $1$ | diameter at most $0.9696$ |

Everything in the table is verified: coverage by an exact sweep and by an area count
with overlaps subtracted (the union’s area is exactly $(U - 1)^2 = 844561/62500$), and
the wall lemma is proved and sharp
([lemma review](reviews/review-2026-10-02-n17-depth-width-wall-lemma.md)).

The census it gives:

| Quantity | Value | How |
| --- | ---: | --- |
| Occupancy states | $\binom{24}{17} = 346{,}104$ | every 17-subset of the cells |
| States fixed by each reflection | 660 | counted as unions of whole cycles |
| States fixed by a rotation | 0 |  |
| $D_4$ orbits | $(346{,}104 + 4 \times 660)/8 = 43{,}593$ | Burnside, and brute force agreeing |
| The family’s state | corner-SW, corner-NW, corner-SE, corner-NE, side-S0, side-S1, side-S2, side-N0, side-N1, side-N2, side-W0, side-W2, side-E0, side-E1, interior-W, interior-N, interior-E | unique, least margin $0.002112$ (square 13 against the middle south cell’s top) |
| Empty cells in that state | side-W1, side-E2, interior-SW, interior-NW, interior-S, interior-SE, interior-NE |  |

An earlier tabbed design of the same cover left the family in two states, because square
13 sat $0.0023$ inside an overlapping wall cell; the middle wall cells were deepened and
narrowed to make the state unique (exp-246, then exp-247).

## The Local Half

Three records compose into the theorem capture must reach.
The tutorial’s
[local minimum modulo sliders](../../TUTORIAL.md#a-local-minimum-modulo-sliders)
explains the mechanism.

**H-258, the stress** (proved,
[exp-242](../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-242-h258-n17-core-stress.md)).
Nonnegative weights on 58 contact and wall rows, 52 of them strictly positive and six
exactly zero, whose weighted sum of row gradients is exactly the side’s, as
rational-function identities at the root.
It is first-order stationarity of the complete local model in both corner branches, and
nothing more.

**H-261, the local minimum modulo sliders** (verified on a declared box,
[exp-244](../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-244-h261-n17-local-minimum.md)).
The slides are $a \ge 0$ for square 5 along the bottom wall, and $b$ and $z$ for squares
11 and 13 along the tilted block’s axis; square 6 is dropped.
The kernel of the 52 positive rows is exactly the six slider directions; for each of the
90 signed non-slider coordinate directions an exact nonnegative dual is certified; and
the ratio test passes at $r = 1/5000$ on 93 cells of the slider box
$B_W = [0, \tfrac14] \times [0, \tfrac1{12}] \times [-\tfrac18, \tfrac1{16}]$, worst
ratio $0.925818$ for the rotation of square 11. The duals are affine in the slides
because the base point moves with them
([recipe review](reviews/review-2026-10-02-n17-local-theorem-recipe.md)). An independent
review reproduced every curvature constant and option margin.

H-261 stays **unresolved as worded**. Its claim lets the sliders range over everything
physically feasible, and the
[composition review](reviews/review-2026-10-02-n17-local-half-composition.md) exhibits a
packing meeting every premise outside the box: the family with squares 5 and 6
exchanged, valid at side exactly $S^{\ast}$ for every $a \in [1, 1.0742]$. Narrowing the
claim after the result would be a retune, so the hypothesis keeps its verdict and the
usable theorem carries a state premise instead.

**H-268, the slide coverage** (verified,
[exp-248](../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-248-h268-n17-local-half-composition.md)).
With square 6 confined to its cover cell and the other squares within $r$ of the family,
exact separating-axis bounds give:

| Slide | Certified range | Why not tighter |
| --- | --- | --- |
| $a$ | $[0, 23/200]$ | square 6 sits between squares 5 and 13 |
| $b$ | $[b^{\ast}, 37/500]$, $b^{\ast} = -1.685\thinspace r$ | the 9/11 contact, which the local theorem drops, lets square 11 move toward square 9 by $1.685\thinspace r$ |
| $z$ | $[-49/1000, 0.0241]$ | the 11/13 contact above, square 6 below |

The $b$ floor falls just below $B_W$, so the local theorem was re-run over the widened
box
$B_W' = [0, \tfrac14] \times [-\tfrac1{2500}, \tfrac1{12}] \times [-\tfrac18, \tfrac1{16}]$,
worst ratio $0.925931$.

**The capture-target theorem** (proved, as the composition of the three).
Take a packing of 17 unit squares of side $S \le S^{\ast}$, placed in the cover frame
with its lower-left corner at the family’s, which sits at $(\sigma, \sigma)$ with
$\sigma = (U - S^{\ast})/2$. If its occupancy state is the family’s, which labels its
squares, and its 45 non-slider coordinates are each within $1/5000$ of the family’s,
angles taken modulo a quarter turn, then its slides lie in $B_W'$, its sixteen squares
other than 6 lie exactly on the family, and $S = S^{\ast}$.

## The Global Half

### The census and the selector

On the cover there are 43,593 orbits to exclude or capture.
The engine is sub-pattern exclusion by containment, as the tutorial’s
[sub-pattern exclusion](../../TUTORIAL.md#sub-pattern-exclusion-by-containment) and
[selection versus certification](../../TUTORIAL.md#selection-versus-certification)
describe. The selector
([`select_n17_sub_patterns.py`](../../packing/devtools/select_n17_sub_patterns.py))
proposes candidates and certifies nothing
([H-267](../../packing/campaign/hypotheses/H-267-n17-isolated-sub-pattern-residue.md),
[receipts](../../packing/campaign/explorations/X048-session-168-pilots/README.md)).
Everything in this table is heuristic.

| Arity | Connected classes | Flagged | Orbits left if all flags proved |
| ---: | ---: | ---: | ---: |
| 3 to 5 | 6,589 | 0 | 43,593 |
| 6 | 17,052 | 3, all crowds of interior cells | 23,354 |
| 7 | 43,086 | 41 more, 44 in all | 5,084 |
| 8, priority subset only | 7,790 searched of 92,065 | 46 more, 90 in all | 2,256 |

A second seed flagged exactly the same 44 classes at arities six and seven.
The family’s own sub-patterns are witnessed at its pose and never flagged.
The thinnest flags, with best penetrations near $6 \times 10^{-5}$, are the likeliest to
be false; before the selector’s deep stage was added, two flags that other seeds placed
would together have removed half the census.
The arity-five line corrects an earlier exploratory count that had flagged ten classes.

### The two provers

The tutorial’s [certificates](../../TUTORIAL.md#what-makes-a-certificate-admissible)
explains both engines and the admission rules.

| Prover | Tool | Adapted from | What it emits |
| --- | --- | --- | --- |
| Ownership-induction kernel | [`check_n17_subpattern.py`](../../packing/devtools/check_n17_subpattern.py) on `sqpack.hull_kernel` | the $n = 11$ proof’s kernel, with the 24 physical cells in place of 16 normalised ones, $D_4$ transfer in place of the half-turn, and the wall lemma in place of a diameter assertion ([specification](reviews/review-2026-10-02-n17-kernel-adaptation-spec.md)) | a seed and a node, each named by the hash of its canonical bytes |
| Interval branch and bound | [`pilot_n17_subpattern_bb.py`](../../packing/devtools/pilot_n17_subpattern_bb.py) | nothing: it shares only the cells | every node’s boxes, cuts, multipliers and bounds in exact rationals |

### The first two certificates

Both were admitted on 2026-10-02 in
[exp-249](../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-249-h267-n17-first-certified-sub-patterns.md),
after clean runs from a committed tree bound each certificate to the bytes that produced
it. The live source is the ledger,
[`certified-sub-patterns.yaml`](../../packing/campaign/explorations/X048-session-168-pilots/certified-sub-patterns.yaml),
read by [`census_n17_certified.py`](../../packing/devtools/census_n17_certified.py),
which counts only admitted entries.

|  | W7 | A |
| --- | --- | --- |
| Cells | corner-SW, side-N0, side-W0, side-W1, side-W2, interior-SW, interior-W | interior-SW, interior-NW, interior-W, interior-S, interior-N, interior-SE |
| Prover | kernel, 64 rows per owner | branch and bound |
| How it closed | 58 steps; the west wall pins first, then side-N0 loses every row to collision against side-W2’s nearly pinned cover | 41,598 nodes, 21,215 closed leaves, depth 31, no Farkas failure |
| Wall time | 1,513 s | 569 s |
| Excludes | 133,152 states, 16,701 orbits | 110,448 states, 13,897 orbits |
| Fresh-process re-check | saved seed and node re-certified with the producer never imported, 27.3 min | the saved certificate, 53 MB in 84 chunks, re-checked by its author’s own exact verifier |
| Independent verification | a verifier importing nothing from the kernel re-proved the seed, the hull chain, all 19,282 partner cover rows and all 3,712 rows (3,324 in full, 388 empty), with 7,752 collision regions by 30,952,184 exact facet inequalities, in 75 min | all 41,598 nodes in exact rationals, all 378 trigonometric enclosures, the tree’s coverage of the root and every piece and pair split, in 26 min |
| Mutation suite | 25 of 26 unsound objects refused; the 26th ends unproved and excludes nothing | the certificate check rejects every one of twelve mutants that produced an invalid record, and all nine doctored certificates |
| Falsifier controls | W7 minus side-N0, W7 minus interior-W, and the family’s own west-wall arity-7 pattern all stall | the family’s west, north and east sub-patterns and a placed class are not certified |
| Review | [no blocking defect](reviews/review-2026-10-02-n17-w7-closure.md); admitted once the saved objects were bound to a committed tool, the full re-check retained and the controls recorded | [no blocking defect](reviews/review-2026-10-02-n17-branch-and-bound-certifier.md); admitted once the committed receipt and manifest were bound and the re-check retained; the claim rests on the certificate check, not the controls |
| The other prover | the branch and bound had closed 0.4% of W7’s tree after 30 minutes | the kernel stalls on A at 32 rows per owner |

With both admitted, the certified census is 139,976 states and 17,690 orbits.
[exp-250](../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-250-h267-n17-standing-verifier-admissions.md)
then admitted two more kernel certificates on the standing verifier’s full pass: flag 3,
an arity-9 class named SW9, and N1, a whole 17-cell residue state.
The certified census is now 126,168 states and 15,953 orbits.
The family’s state contains no image of any admitted pattern.

## Capture and Its Pilot

Capture must show that every packing in the known state at the cap $U'$ lies within
$1/5000$ of the family, in the frame and angle chart the local theorem uses; the
tutorial’s [capture](../../TUTORIAL.md#capture) explains the engine.
The composition review lists three obligations: read the occupancy state with the
packing’s lower-left corner at $(\sigma, \sigma)$, since the two other natural
embeddings are offset from the local theorem’s frame by more than $r$; contract to
$1/5000$ at $U'$; and charge the rational enclosure of the tilted block’s axis, an
algebraic direction, to the capture radius rather than to $r$.

The [capture costing](reviews/review-2026-10-02-n17-capture-feasibility.md) models the
cost at 100 to 400 CPU-hours for 8 to 32 leaves at a radius of $3 \times 10^{-4}$, each
factor uncertain by about three times, and names the falsifier: a contraction factor
$g > 0.95$ at the $10^{-3}$ scale, or more than 16 splits before reaching it, means the
$n = 11$ architecture is the wrong engine for $n = 17$ whatever the radius.
The slope $\kappa_\infty$ is nine times smaller than at $n = 11$, which is the reason to
expect slower contraction; only a pilot measures it.

The pilot, `devtools/pilot_n17_capture.py`, runs the family’s own state at $U'$ with
sixteen contracting owners and square 6 coarse, refines angle rows by bisection, and
checks after every certified update that the family’s exact pose still lies in some live
row of every owner. A companion run at $U$ must *fail* to contract below the first-order
feasible set, as a check that the two-cap distinction is real.

The first pilot met that falsifier: over 14 rounds from a box of radius $1/1024$, no
position contracted ($g = 1.000$). An
[independent review](reviews/review-2026-10-02-n17-capture-after-pilot.md) found the
result limited by the producer, not the architecture.
In a model of the best pairwise induction, positions contract only once each owner’s
widest live row is about a tenth of its position extent, and the pilot’s cap of 24 live
rows kept that ratio between a quarter and one.
Calibrated by $n = 11$, the model predicts $g \approx 0.91$. The review sharpened the
falsifier: if every owner’s widest row is under a twentieth of its position extent for
three rounds and no two-sided extent falls by ten percent, the architecture is wrong.
The second pilot raised the cap.
Its $n = 11$ control reproduced the recorded contraction ($g \approx 0.80$ against
$0.84$). At 128 rows no $n = 17$ position contracted, but the widest-row ratio stalled
at a fifth on side-N2, so the falsifier could be neither met nor cleared.
At 256 rows, 15 of the 16 owners were under a tenth by round 10, where the model says
positions should begin to move, but side-N2 held at 0.1002, and over 13 rounds no
two-sided position extent moved off the box.
The [capture scorer](../../packing/devtools/score_n17_capture.py) reads the falsifier as
undecided at that cap: side-N2 needs two more bisections, about 528 rows, to pass a
twentieth. A run at 576 rows resumed from round 13 (modelled at about 2.8 hours a round,
14 hours to read the falsifier); rows allotted per owner by need would take about 5.6
hours, but the pilot does not allot them yet (measured to round 13; not yet decided).

The target itself is larger than $1/5000$ per coordinate.
Following $n = 11$'s two-radius result, a
[radius review](reviews/review-2026-10-03-n17-local-radius.md) found that a uniform
radius cannot pass much beyond $1/4630$. A per-coordinate vector does compose with the
slide coverage on a box $B_c$: every coordinate at least $1/1216$, $\omega_{11}$ at
$85/16$ of that, worst ratio $0.999317$, exact.
That makes capture’s target four to five times larger and the angle rows it needs about
two bisections coarser.
It is held as a component, not yet a hypothesis, until a pilot adopts it.
The $1/1024$ pilot box is not inside it, so capture must still contract every angle two
to 33 times.

## Approaches Tried and Set Aside

| Approach | What it was | Why it was set aside | Record |
| --- | --- | --- | --- |
| The H-259 grid | A $5 \times 5$ grid of closed cells over the centre box: sixteen wall cells of capacity one and nine interior cells of capacity two | It counted like a 30-cell cover: 161,100,756 states and 20,155,518 orbits, 7,703,312 after two free cuts, and the family straddled a seam. No per-case engine recovers from a census that size | [mixed-capacity review](reviews/review-2026-10-01-n17-mixed-capacity-cover.md), [H-259](../../packing/campaign/hypotheses/H-259-n17-mixed-capacity-cover.md), [H-260](../../packing/campaign/hypotheses/H-260-n17-closed-cell-symmetry.md) |
| Charge floors, H-262 | Use the R068 lower-bound charge at the cap to put a minimum charge on each grid cell, and exclude states whose floors exceed the budget | R068’s charge collapses at the cap: its sites are spaced for its own slightly larger cores, the smaller square slips between them, and every orbit survives. A ceiling theorem then showed that any single $D_4$-symmetric linear floor vector, from any charge, leaves at least 30,966 orbits, so the hypothesis could not be confirmed; asymmetric and nonlinear floors escape the theorem and are untested | [exp-243](../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-243-h262-n17-charge-floor-pilot.md), [pilot review](reviews/review-2026-10-02-n17-charge-floor-pilot.md) |
| The widened projection theorem | Widen the conditional projection theorem to an angle box of radius about $10^{-2}$, so that capture need only reach the region where the contact features are forced | Scoped as plausible, with the instrument an interval certificate of dual sheets over seven backbone angles; not built. It stays nested inside H-261 as the fallback if capture stalls in angle directions | [scope review](reviews/review-2026-10-02-n17-widened-projection-scope.md) |

## What Costs Time

Every prover works in exact rational arithmetic in Python, and every clip and hull
multiplies denominators; the tutorial’s
[exact arithmetic](../../TUTORIAL.md#why-exact-arithmetic-dominates-the-cost) says why
that is not optional.

| Item | Cost | Where the time goes |
| --- | ---: | --- |
| W7 closure, kernel | 1,513 s | collision regions; exact plane construction is most of it. Building facets by edge merge cut one owner’s first-round rows from 38.9 to 14.5 s with the same 421 regions |
| W7 reproduction with saved objects | 29.7 min | producer 838 s, checker 930 s |
| W7 fresh-process re-check | 27.3 min | every cover re-proved by the reference all-pairs sweep |
| W7 independent verification | about 7 min for 270 rows; about 90 min on one core for all 3,712 rows | exact hulls, clips, Minkowski differences and area subtraction in separate code |
| A certification, branch and bound | 569 s for 41,598 nodes, about 14 ms a node | the node count, which multiplies as a pattern’s margin shrinks; W7, whose best found placement violates by $9 \times 10^{-3}$, had 0.4% of its tree closed after 30 min |
| The selector to arity 7 | 2,028 s on two workers | penalty descent over 43,086 classes |

Each flagged class is an independent job, so the 44 run in parallel without
coordination. A compiled evaluator for the branch and bound’s per-node bounds is the
obvious speed-up; it is unbuilt and its gain unmeasured.

## What Remains

Stated without a forecast, because none is on record.

1. **Certify or refute the remaining flags.** W7, A and SW9 are admitted, and 88 flagged
   classes have no certificate.
   Uniform rows stalled on several.
   Adaptive rows closed flag 3 (SW9) but stalled on flag 2 at their cap of 1,152 rows:
   the cap was spent by round 4, the live rows fell from 1,152 to 794 by round 18 and
   then stopped, and three of the nine owners never lost a row.
   A flag the prover cannot close is either a false flag, in which case the search
   resumes, or a stall of the engine on a true pattern, which needs finer rows,
   splitting or the other prover.
2. **A method for the residue.** 15,953 certified orbits remain, and at most 5,084 if
   every flag of arity seven proves; each is a state that no small pattern excludes and
   that must be excluded on its own, as $n = 11$ excluded 276 cases at about 636
   CPU-seconds each. The kernel has excluded one such state, N1, in 3,723 s, but the
   $n = 17$ per-state method and its price are not established; the
   [residue process review](reviews/review-2026-10-02-n17-residue-process.md) plans one.
3. **Capture.** At 256 rows the review’s falsifier cannot be read; the 576-row run
   resumed from round 13 decides whether the architecture holds.
   If it holds, the per-coordinate target above is the next pilot’s goal, registered as
   a hypothesis with its vector and box frozen.
   If it fails, the widened projection theorem is the fallback.
4. **Independent review of everything.** Each piece so far carries one review.
   The composition of the census, the certificates, the consumer and the capture into
   one argument has not been written down, let alone reviewed, and T-060’s rungs show
   what further assurance costs even then.
5. **Certificates that fit in memory.** Adaptive rows close classes that uniform rows
   could not, but flag 2’s node reached 931 MB of JSON. The producer’s own check of it
   reached 8.6 GB and was killed; the standalone check of the saved objects peaked at
   about 4.3 GB and took 3,714 s. A streamed or compact certificate format, or a
   compiled checker, has to come before adaptive rows are used at scale or their cap is
   raised.
6. **Admission at the corrected verifier.** After $n = 11$'s finding C2, the kernel
   verifier’s point and segment covers were made exact (318c28c42). The defect never ran
   on W7, SW9 or N1. New admissions should be verified at that revision or later.

If the proof were completed, the result would be apparently novel in the sense the
tutorial’s [§8](../../TUTORIAL.md#8-what-is-known-and-what-is-not) defines: new to the
best of this project’s knowledge from the archived corpus, an assessment of the search
done rather than an assertion of priority.
An outside group, Guzhou0806 / N17 project continuing Kleddamag’s work, publishes
$n = 17$ lower-bound results and holds the bracket’s lower end.

## Evidence Status

| Status | Items |
| --- | --- |
| Proved | The depth-width wall lemma; the identity of the certified side with the catalogue polynomial; the stress; the capture-target theorem as the composition of exp-244, exp-248 and exp-247 |
| Verified | The rational ceiling on the side; the R068 lower bound at `V3/C3`; the cover’s coverage, capacities, $D_4$ invariance, Burnside count and unique family state; the local minimum over $B_W'$ at $r = 1/5000$; the slide bounds |
| Admitted | The W7 and A certificates, each re-proved in full by an independent verifier ([exp-249](../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-249-h267-n17-first-certified-sub-patterns.md)); the SW9 and N1 kernel certificates, each re-proved in full by the standing verifier; and the certified census of 15,953 orbits ([exp-250](../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-250-h267-n17-standing-verifier-admissions.md)) |
| Projected | Nothing at present beyond the heuristic lines below |
| Heuristic | Every selector flag, every best-penetration figure, and every orbit count conditional on flags proving |
| Modelled | The feasible-set radii at the two caps; the capture cost table and its falsifier thresholds |
| Not started or not reported | The capture pilot’s result; a per-state method for the residue; the composed proof and its review |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
