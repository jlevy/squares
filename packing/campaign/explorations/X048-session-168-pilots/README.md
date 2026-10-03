# X-048 Session 168 Pilots: Receipts

Session 168 ran BC-418, the coordinating entry after Session 167. Its sub-pattern
selector lane built H-267’s heuristic selector as a retained tool, and its kernel lane
ran the adapted n11 prover on the first flagged patterns; their outputs are kept here.

These are **planning evidence, not admitted results**. The selector proposes forbidden
sub-patterns and certifies none, and the kernel has not yet closed one.
Until an independent prover certifies a pattern infeasible, nothing it flags excludes a
case.

## H-267: The Sub-Pattern Selector

`devtools/select_n17_sub_patterns.py` (SHA-256 `a40f34fb…`), built by lane S1, Opus at
extra-high effort, runs on the unique-state cover `ring-3-voronoi-8-tabbed-unique` at
cap $1169/250$. It enumerates the sub-patterns of $k$ occupied cells that are connected
in the cells’ interaction graph, up to D4. For each one it searches hard for a feasible
placement: unit squares with centres in their cells, any orientations, inside the
container, pairwise disjoint.
It flags a pattern only when every attempt leaves positive penetration, including a deep
second stage. An exact consumer then counts the D4 orbits that contain no flagged
pattern.

| Receipt | What it holds |
| --- | --- |
| `receipts/selector-arity6-seed1.json` | The run to arity 6 with seed 1, its controls and survivor counts, and the certification priority |
| `receipts/selector-arity6-seed1.log` | Its progress log, 264 s on two workers |
| `receipts/selector-seed-study.json` | The three flagged classes re-searched under seeds 1 to 4 |
| `receipts/selector-arity7-seed1.json` | The run to arity 7 with seed 1 at commit d674e665, 2,028 s on two workers: 44 flagged classes (3 at arity 6, 41 at arity 7) and the certification priority |
| `receipts/selector-arity7-seed2.json` | The same run with seed 2 on one worker, 3,498 s; see the provenance note below |
| `receipts/selector-arity7-seed2.log` | Its progress log |
| `receipts/selector-arity7-seed1.log` | Its progress log |
| `receipts/selector-lane-f-retest.json` | The bulk-exclusion lane’s exploratory arity-5 flags re-searched on its own design |

The findings:

- **Nothing is flagged at arity 5 or below.** All 6,589 connected classes are placed.
  This corrects the bulk-exclusion design review’s exploratory proxy, whose 10 arity-5
  flags (and 11,939 orbits) were false: on that lane’s own design this search places all
  of them.
- **Three classes are flagged at arity 6,** all crowds of interior cells, with best
  penetrations of $1.49\times10^{-2}$, $5.6\times10^{-3}$ and $2.0\times10^{-3}$, stable
  across four seeds. If all three are certified, 185,424 states and 23,354 orbits
  survive. That is still above H-267’s threshold of $10^4$, so arity 7 (43,086 connected
  classes) is needed.
- **Arity 7 reaches the threshold, heuristically.** 41 more classes are flagged, 44 in
  all, with best penetrations from $6.2\times10^{-5}$ to $2.3\times10^{-2}$. If all are
  certified, 40,016 states and **5,084 orbits** survive, below H-267’s $10^4$. The
  thinnest flags are the likeliest to be false, and the top-priority class is now a
  west-wall column plus two interior cells.
- **The flags are stable under a second seed.** Seed 2 flags exactly the same 44
  classes, with best penetrations within 5% of seed 1’s, and the same survivors at every
  arity. The seed-2 run imported the committed selector (`a40f34fb…`) at launch; its
  receipt’s `module_sha256` names `d33762ab…`, a later working-tree edit by another
  lane, because the selector hashes its file when it writes the receipt rather than when
  it imports it. The selector now hashes its bytes at import (`f17a1dbb…`).
- **The endpoint survives at every arity.** Its own sub-pattern classes are witnessed at
  its pose to penetration $7\times10^{-16}$ and are never flagged.
- **One false flag can remove half the census.** Before the deep stage was added, two
  classes were flagged that other seeds placed, and one of them alone excluded 171,604
  states. The prover is load-bearing.

Reproduce, from `packing/`:
`uv run --frozen --all-extras --group dev python -m devtools.select_n17_sub_patterns --max-arity 6 --seed 1 --workers 2 --output FILE`.

### Arity 8, a Priority Subset

Lane S2, Opus, added `--restrict-to-survivors K`: from arity `K` on, a class is tested
only if it lies in a state that survives every lower flag.
That is exact for the consumer, because the surviving set is closed under D4 and a
tested class sees the same warm starts and seed either way.
It also added `--count-only` and `--max-missing-pairs`, a priority subset that is not
exact and records what it defers.
It also fixed the digest defect above: the selector now hashes the bytes it imports.

| Receipt | What it holds |
| --- | --- |
| `receipts/selector-count-arity8-under-arity7-flags.json` | Class counts at arity 8 without search |
| `receipts/selector-arity8-seed1-restricted.json` | Seed 1 to arity 8, restricted, classes with at most two non-interacting pairs: 7,341 s on one worker |
| `receipts/selector-arity8-seed1-restricted.log` | Its progress log |
| `receipts/selector-arity8-ran-to-committed.diff` | The run imported `d33762ab…`; reverse-applying this diff to the committed selector reproduces those bytes |

- **Restriction saves almost nothing at arity 8.** 91,133 of the 92,065 connected
  8-classes still lie in a surviving state.
- **The priority subset adds 46 flags.** 7,790 classes were searched and 83,343
  deferred. Best penetrations run from $6.2\times10^{-5}$ to $2.7\times10^{-2}$, with six
  below $10^{-3}$. Arity 7 and below reproduce bit-identically.
- **If all 90 flags at arity 8 or below are certified, 17,636 states and 2,256 orbits
  survive,** down from 5,084. This is an upper bound for a full arity-8 sweep.
- **The value is in the head.** In greedy order the top arity-8 class removes 1,163
  orbits, the top five 2,293 (81%), and the last twelve nothing once the first 34 are
  in. The top class is corner-SW, corner-NW, side-S0, side-W0, side-W1, side-W2,
  interior-SW and interior-NW, with penetration $3.5\times10^{-3}$.

## The Kernel on Flagged Patterns

Lane K2, Opus at extra-high effort, extended `sqpack.hull_kernel` with a sequential
grammar (refinement, revisits, derived closures, stall reporting) and a producer.
It ran them on three arity-6 flags and one arity-7 flag through
`devtools/check_n17_subpattern.py` (SHA-256 `893b5206…`). The producer proposes rows
over uniform angle bins; the checker certifies exactly what it emits, so a certified
stall is a sound statement that these rows exclude nothing.

| Receipt | Pattern | Bins | Outcome | Wall |
| --- | --- | ---: | --- | ---: |
| `receipts/kernel-A-bins16.json` | A: interior-{SW,NW,W,S,N,SE}, penetration $1.49\times10^{-2}$ | 16 | round cap at 4 rounds, still changing slowly | 35.6 s |
| `receipts/kernel-B-bins16.json` | B: side-S1, side-W1, interior-{NW,W,S,SE} | 16 | stall | 6.4 s |
| `receipts/kernel-C-bins16.json` | C: interior-{NW,W,S,N,E,SE} | 16 | stall | 7.4 s |
| `receipts/kernel-W7-bins64.json` | W7: the top arity-7 flag, the west-wall column with side-N0, interior-SW and interior-W | 64 | round cap at 6 rounds, still contracting | 990 s |
| `receipts/kernel-endpoint6-bins64.json` | Control: six cells of the endpoint’s own state | 64 | stall, as required | 15.6 s |

Nothing is excluded yet.
The obstacle is reach, not splitting: the axis interior cells have least enclosing
radius about $0.52$, so they own no point from the cell alone, and most of B’s and C’s
cells never own anything.
W7 is the lead: at 64 bins its west-wall owners grew hulls of 32 to 66 vertices and
shrank to $0.57\times0.36$ and $0.85\times0.20$ before the round cap.
The levers are collision regions from partner pose covers, which reach owners with empty
hulls; a bounded compression that holds step cost flat; and finer bins for A, whose
64-bin producer run eliminated rows that 16 bins did not.
A two-cell closure control certifies, and the n11 mask-0 and case-2095 replays are
unchanged and exact on the same kernel.

Reproduce, from `packing/`:
`uv run --frozen --all-extras --group dev python -m devtools.check_n17_subpattern --pattern W7 --bins 64 --max-rounds 6 --output FILE`.

### With Collision Regions

The second kernel slice wired collision regions into the sequential grammar.
A partner’s complete pose cover is admitted row for row, and every region is verified
exactly before it joins a cover.
It also caps owned hulls at 16 vertices, and adds a producer time cap whose partial node
is certified as a stall.
The tool’s SHA-256 is now `3b9e9264…`. A fast test closes a two-cell pattern through
collision alone, where neither owner holds a point and nothing closes without collision.

| Receipt | Pattern | Bins | Outcome | Wall |
| --- | --- | ---: | --- | ---: |
| `receipts/kernel-collision-A-bins32.json` | A | 32 | time cap after round 5, still contracting | 404 s |
| `receipts/kernel-collision-W7-bins32.json` | W7 | 32 | time cap after round 7, contraction mostly over by round 4 | 1,016 s |
| `receipts/kernel-collision-B-bins16.json` | B | 16 | stall, round 1 equals round 0 | 45 s |
| `receipts/kernel-collision-endpoint6-bins64.json` | Control | 64 | stall, as required | 573 s |

Collision reaches A’s blind owner: interior-N now owns points.
A contracts hard at 32 bins.
interior-W falls from 32 live rows to 12, and its residual from $0.78\times0.35$ to
$0.66\times0.23$. interior-NW falls to 16 rows and $0.59\times0.13$, and interior-SE to
23 rows and $0.20\times0.59$. It is the likeliest first closure, if run without the time
cap.
W7 at 32 bins with capped hulls contracts less than the uncapped 64-bin run did, and
side-N0 never moves.
The two changes are confounded.
B does not move: four of its six owners never own a point.
Collision cost now dominates, and exact plane construction is most of it.

### The First Closure, Not Yet Admitted

The third slice made collision 2.4 to 3.2 times cheaper in the producer only.
It builds the facets of $Q_r-Q_i$ by edge merge, caches each partner row once per step
and verifies by integer cross-multiplication.
On W7’s round-0 rows it brought side-W0 from 38.9 s to 14.5 s, with the same 421
collision regions. The checker is unchanged.

| Receipt | Pattern | Bins | Outcome | Wall |
| --- | --- | ---: | --- | ---: |
| `receipts/kernel-collision-A-bins32-to-stall.json` | A | 32 | true stall: round 8 equals round 7 | 609 s |
| `receipts/kernel-closure-W7-bins64.json` | W7 | 64 | **closed**: every parent pose of side-N0 forbidden at step 57 | 1,513 s |
| `receipts/kernel-closure-endpoint6-bins64.json` | Control | 64 | stall, as required | 171 s |
| `receipts/kernel-collision-cost-before.json`, `…-after.json` | W7 round 0 | 64 | per-step producer cost before and after | — |

**W7 closes under the kernel’s checker.** Its west wall pins first: side-W2 goes from 64
live rows to 12 and from $0.91\times0.71$ to $0.11\times0.05$, side-W1 to 20 rows and
$0.16\times0.12$. side-N0 owns points from round 4, then loses every row by collision
against side-W2’s nearly pinned cover.
The transfer excludes 133,152 states and 16,701 D4 orbits, the same state count the
selector predicted for the class.
Every checker module is byte-identical to `214601ac`; only the producer differs.

The closure is not admitted, and nothing in the census uses it yet.
Four things must come first:
- The seed and node objects were not saved; the receipt holds their SHA-256 (node
  `2d516d00…`, seed `8949a798…`). A re-run must reproduce them and save them, and a
  fresh process must re-check them.
- The new grammar has only its builder’s soundness argument: partner covers from the
  hull of each accepted row’s residual vertices, collision regions, replace-mode owned
  hulls and empty seed groups.
  It needs an independent review.
- The endpoint control above never contracts, so it is weak.
  The decisive falsifier is the endpoint’s own west-wall arity-7 sub-pattern at the same
  settings. It must not close.
- A second certifier on W7, the interval branch-and-bound pilot.

A plateaus at 32 bins and needs 64 bins or row splitting.

### Reproduction, Saved Certificate and Falsifiers

The fourth slice met three of those conditions, from a worktree at `fe152c30`. The
independent review was running alongside it.

| Receipt | What it shows | Wall |
| --- | --- | ---: |
| `receipts/kernel-closure-W7-reproduce.json` | W7 re-run with `--save-objects`: the same node `2d516d00…` and seed `8949a798…`, the same closure and transfer | 29.7 min |
| `receipts/kernel-closure-W7-check-saved.json` | `--check-saved` on the saved objects in a fresh process: `PASS_SAVED_CLOSED`, the producer never imported, every cover re-proved by the reference all-pairs sweep rather than the indexed one | 27.3 min |
| `receipts/kernel-falsifier-endpoint7.json` | The endpoint’s own west-wall arity-7 sub-pattern (its squares 1, 2, 3, 4, 9, 10, 11) at W7’s settings: certified stall | 4.2 min |
| `receipts/kernel-falsifier-W7-minus-N0.json` | W7 without side-N0, which the selector places: certified true stall. Its rows match W7’s through round 3, then plateau | 28.3 min |

The certificate is in `certificates/W7/`: the gzipped seed and node, each named by the
SHA-256 of its decompressed canonical JSON, and a `README.txt` giving the format for an
independent reader. The sharper falsifier is the useful one.
It runs the same cascade as W7, so it exercises the collision path that closes W7, and
without side-N0 it plateaus with side-W2 at 48 live rows rather than 12.

### The Next Three Arity-7 Classes

At W7’s settings, the kernel closes none of the next three classes in priority order.

| Receipt | Class | Outcome | Wall |
| --- | --- | --- | ---: |
| `receipts/kernel-stall-NW7-bins64.json` | NW7: side-N0, side-N1, side-W2, interior-SW, interior-NW, interior-W, interior-S (penetration $6.3\times10^{-5}$) | certified true stall at round 9; five owners end in residual boxes under 0.35 a side | 20.4 min |
| `receipts/kernel-incomplete-P4-bins64.log` | P4: corner-SW, side-N0, side-W0, side-W1, interior-SW, interior-NW, interior-W | incomplete: the checker ran out of the 30-minute ceiling; the producer’s live rows stopped changing at round 4 | 30.0 min |
| `receipts/kernel-stall-P5-bins64.json` | P5: corner-SW, side-S0, side-W0, side-W2, interior-SW, interior-NW, interior-W | certified true stall at round 9 | 18.1 min |

NW7 pins its interior owners to near-points without closing, which fits the suspicion
that its thin flag is false.
Its final boxes can seed a placement search to decide that.
The devtool now saves the seed and node before checking, so a run cut off by the ceiling
can be finished with `--check-saved`.

## An Independent Certifier: Interval Branch and Bound

Lane P2, Opus, built `devtools/pilot_n17_subpattern_bb.py`, which shares no code with
the kernel or the selector beyond the cover’s exact cell polygons.
It branches on the angles and decides the centres of each angle box by one LP over the
exact cell rows, outward wall bounds and per-pair cuts.
HiGHS only proposes multipliers: every pruning step is a dual bound evaluated with
outward rounding, and sin and cos are enclosed by interval arithmetic.

| Receipt | Pattern | Outcome | Wall |
| --- | --- | --- | ---: |
| `receipts/bb-A-certified.json` | A | **certified infeasible**: 41,598 nodes, 21,215 leaves, depth 31, no Farkas failure | 569 s |
| `receipts/bb-control-endpoint-{west,north,east}.json` | Three endpoint sub-patterns | not certified; the witness path follows the endpoint’s pose to the resolution floor | 90 s each |
| `receipts/bb-control-placed.json` | A class the selector placed | not certified; witness path passes | 90 s |
| `receipts/bb-target-a7-0-W7-30min.json` | W7 | unresolved at 30 min, 0.4% of the tree closed | 1,800 s |
| `receipts/bb-target-a6-{1-B,2-C}.json`, `bb-target-a7-{0,1,3,4,5}.json` | Other flags | unresolved at 10 min | 600 s each |

The A receipt is a reproduction from a worktree at `0bc6a03b` with the certificate
writer added. It imported the tool bytes this commit holds (`f8da95e8…`), and
`bb-A-certified-imports.json` lists the digest of every module it imported.
It matches the first run node for node.
The controls and the 10-minute targets ran on an intermediate revision (`afe96ca8…`),
and the W7 run on `7b77c4fd…`. They certify nothing and are planning evidence only.

The saved certificate is 53 MB in 84 gzipped chunks: every node’s boxes, cut rows,
Farkas multipliers and bound certificates in exact rationals, with a format README. P2’s
own exact re-check passes all 4,504 Farkas closures, 639,609 bound certificates and
324,934 cuts. It is held outside the repository until the independent review decides
admission; the run is deterministic and regenerates it from these bytes.

The two provers complement each other.
The kernel closes W7 and stalls on A, and the branch and bound closes A and does not
finish W7. A’s margin is large and its squares are interior; W7’s is a wall chain.

## The Capture Pilot

Lane C1, Opus, built `devtools/pilot_n17_capture.py` (SHA-256 `e22ca457…`). It runs the
kernel’s certified rounds on the endpoint’s own occupancy state, at the capture cap
$U' = 935106018721/200000000000$, $4.49\times10^{-13}$ above $S^\ast$, in the
composition review’s frame.
Square 6 stays coarse, and every update is checked by the sequential grammar before the
next. The capture feasibility review’s falsifier is a contraction factor $g>0.95$ at the
$10^{-3}$ scale, or more than 16 splits.

| Receipt | Run | Outcome |
| --- | --- | --- |
| `receipts/capture-main-box1024.json` | Each owner’s cell cut to its guard polygon widened by $\rho = 1/1024$, 32 bins, 224 updates | position $g = 1.000$ for every owner over 14 rounds; turns contract to 0.002–0.042 rad, then stall |
| `receipts/capture-main-box64.json` | The same at $\rho = 1/64$, 240 updates | position $g = 1.000$; turns stall at 0.035–0.26 rad |
| `receipts/capture-control-U-box1024.json` | The $\rho = 1/1024$ box at the exclusion cap $U = 1169/250$ | positions identical to $U'$; only the angles differ |
| `receipts/capture-replay-box1024.json` | The saved $\rho = 1/1024$ node replayed whole | `PASS_REPLAYED`, 224 steps |
| `receipts/capture-try-b32-g64.json`, `capture-control-U-b32-g64.json` | The cell seed itself, on an earlier revision (`98d98482…`) | nothing contracts: all 544 rows stay live, and 13 of 17 owners own no point |

**The falsifier is met.** No run brings any position coordinate below its starting
radius, so the first round under $10^{-2}$, $10^{-3}$, $3\times10^{-4}$ and
$2\times10^{-4}$ is never.
Starting from the cells, roughly 190 position splits would be needed before boxes even
reach $1/64$, against the falsifier’s 16. The endpoint control holds after all 1,197
certified updates.

Lane C1’s reading was that pairwise propagation reaches the box as its fixpoint, so the
architecture is wrong for n17 capture.
The
[independent review](../../../../docs/project/reviews/review-2026-10-02-n17-capture-after-pilot.md)
finds the result producer-limited instead.
In a first-order model of the best any pairwise ownership induction can do, there is no
fixpoint above zero for n17 or n11. With the pilot’s cap of 24 live rows per owner,
positions stay at the box for 23 rounds, and the pilot ran 14. With 96 rows they
contract from round 12 at $g\approx0.70$; calibrated against n11’s record, the real
kernel would sit near $g\approx0.9$. The review specifies a second pilot with the
live-row cap lifted, a sharper core and an n11 contraction control, and its own
falsifier.

## The Residue Survey

Lane Q1, Opus, built `devtools/survey_n17_residue.py` (SHA-256 `824c5335…`). It samples
the orbits that survive the 90 selector flags, stratified by corner and interior counts
and by Hamming distance from the endpoint’s state, and weighted toward the endpoint.
For each one it searches for a full 17-square placement at $U$, then shrinks the state
by deletion to a minimal failing sub-pattern.

| Receipt | What it holds |
| --- | --- |
| `receipts/residue-survey-calibration.json` | The positive control: the endpoint’s state placed blind, 3 of 6 seeds in one round and 6 of 6 by round 5, at penetration exactly 0 |
| `receipts/residue-survey-arity8-seed1.json` | The 45-state sample (44 random plus the control), merged from a run of 15 states and a resumed run of 30 on the same tool bytes |
| `receipts/residue-survey-resume.py.txt` | The script that resumed the run, checked the tool digest and the draw, and merged |

- **No sampled state other than the endpoint’s fits at $U$.** That includes 9 distinct
  states at distance 2. The best full-state penetration is $9.1\times10^{-3}$, and 43 of
  44 exceed $10^{-2}$. The 95% upper bound is about 27 of the 95 distance-2 orbits, and
  about 148 of all 2,256, feasible at $U$.
- **What kills each state is large and new.** Of 21 reductions, 19 are confirmed: arity
  8 to 15, median 11, best penetrations $3.8\times10^{-4}$ to $1.6\times10^{-2}$. Every
  one is a new class, and no class recurs.
  Together, if certified, the 19 would take the projected 2,256 orbits to 987. The top
  one is an arity-8 north-wall crowd the arity-8 priority subset deferred, which alone
  removes 539 orbits.
- **The selector’s search is too short for full states.** Its descent stops at 600
  iterations and polishes only below $10^{-4}$, so on the endpoint’s state it stalls at
  about $2\times10^{-3}$. One long descent from its best pose places it exactly.
  Its flags between $10^{-4}$ and $10^{-2}$ never had that descent, so some may be
  false.
- Two reductions overshot: their confirmation search placed them.
  The receipt’s `found_classes` still counts them, and the confirmed-only figures above
  do not. “Minimal” means irreducible under deletion, not smallest.

## The Local Theorem at a Larger Radius

Lane L1 built `devtools/check_n17_local_radius.py`, which runs the H-261 recipe at a
per-coordinate radius vector and H-268’s slide coverage at a chosen radius, calling both
checkers’ functions unchanged.
The [review](../../../../docs/project/reviews/review-2026-10-03-n17-local-radius.md)
reads the receipts. Each is reproduced from `packing/` by
`python -m devtools.check_n17_local_radius` with the arguments below, writing to
`receipts/local-radius/`; $B_c$ is `--box 0 4/25 -1/128 11/100 -13/200 1/30`.

| Receipt | Arguments | Outcome |
| --- | --- | --- |
| `scan-uniform.json` | `scan` | the ratio is linear in a uniform radius, $-\omega_{11}$ binding; the uniform limit lies between $1/4630$ and $1/4391$ |
| `shape-bwprime-1024.json`, `ratio-bwprime-1024.json` and its certificates | `shape --floor 1/1024`, then `ratio --radii` on it | exact pass on $B_W'$ with every coordinate at least $1/1024$, worst $0.999973$ |
| `shape-bwprime-896.json`, `shape-bwprime-512.json` | `shape --floor 1/896` (`1/512`) `--theta 1` | no vector settles |
| `slide-11-2048.json` | `slide --radius 11/2048 --thresholds 2/5 -1/10 3/20 --tight 6/25 -1/10 3/20` | passes, but $b$ reaches $0.143$, outside $B_W'$, so the $B_W'$ vector does not compose |
| `slide-9-2048.json` | `slide --radius 9/2048 --thresholds 2/5 -1/10 3/20 --tight 4/25 -13/200 11/100` | passes; the certified box lies in $B_c$ |
| `shape-composition-1216.json`, `ratio-composition-1216.json` and its certificates | `shape --floor 1/1216` on $B_c$, then `ratio` | exact pass, every coordinate at least $1/1216$, worst $0.999317$ |
| `shape-composition-1152.json` | `shape --floor 1/1152` on $B_c$ | settles with $\omega_{11}$ above the slide radius, so it does not compose |
| `shape-composition-capture.json`, `ratio-composition-capture.json` and its certificates | `shape --floor 1/1024 --position-share 1/3` on $B_c$, then `ratio` | exact pass, every angle at least $1/1024$ and every position at least $1/3072$, worst $0.999368$ |
| `bounds-*.json` | `bounds` at $1/5000$ and at the $B_W'$ vector | a finer curvature lemma would gain about a factor of two |

The slide receipt’s `margins`, `declared_box` and `inside_declared_box` fields compare
with $B_W$, the slide module’s constant, and are not what the composition uses.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
