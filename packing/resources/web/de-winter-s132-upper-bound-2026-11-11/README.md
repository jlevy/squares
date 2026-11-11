# Joost de Winter’s s(132) Certificate at 6617869

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/6617869a3491b5872c6ecdff55db05cbee57d516)
at `6617869a3491b5872c6ecdff55db05cbee57d516` (committed 2026-11-11T20:52:23Z), the head
of `main` when it was read at 20:58Z, which
[issue #958](https://github.com/jlevy/squares/issues/958) names. The issue was opened at
20:56:18Z, and the lane first read the folder as a publication in a watched repository
before it saw the issue.

The folder `n132/` first appeared at `a491dad` (20:49:44Z) with `n157/`, whose packet is
[de-winter-s157-upper-bound-2026-11-11](../de-winter-s157-upper-bound-2026-11-11/README.md).
`6617869` changes only the two folders’ READMEs and checksums and the root README, naming
Claude Fable 5.2 in the AI statements, so the certificate’s bytes are `a491dad`’s.
GitHub’s activity log was not readable from this session, so the push time of `a491dad`
is not read. By the owner’s rule of 14 October 2026 the folder would be a report from that
commit if its push came first, but no other report reached 132 or 157 in the 6 minutes 34
seconds before the issue, so the ledger dates both claims by the issue, with the first
commit kept, and the verdicts are the same either way.
The commit before them, `501cb8d` (19:41:30Z), corrects the READMEs of `above324/` and
`above324_refined/`; it is outside this scope and read in
[campaign/intake-watch.yaml](../../../campaign/intake-watch.yaml).

Intake lane L104 (think-bcfs) retained it, replayed it and registered it on 11 November
2026 as **T-292**. The blind stage 4 review of lane L105 accepted it the same day, so it
is at V3/C3, and the case adopted it as its house in place of T-174 under the house rule.

## What the Source Claims

- `n132/n132_witness.yaml` states 132 unit squares by centre and the unit direction of one
  edge, every number an exact rational. Like the s172 packet’s witness, it follows
  Witness/v2’s `witness` object without the schema’s envelope. `n132/n132_exact.json`
  states the same packing as `[center_x, center_y, cos, sin]` rows with the side.
- **The side.** The root README rounds it up at 12 places, 11.976048383604, which the
  packet admits; `n132/README.md` cuts it at 50,
  11.97604838360340752372871695271367782454646197183552…, and compares it with the
  record’s 11.9856801988458088, an improvement of 0.0096.
- **The construction.** A pinwheel: a central block of tilted squares with four arms,
  surrounded by four blocks of axis-aligned squares, 54 tilted and 78 axis-aligned. It is
  derived from the public 109-square packing of `Samanyu-dev/squares_in_squares` (commit
  `53551d7`, `best_fit_101_500.csv`, side 10.949289581), which that repository’s README
  reports as a result of its own stretch and quench chains. The packing of 109 was cut
  along one horizontal and one vertical line, the parts moved about one unit apart, each
  gap filled with one layer of squares that continues the local lattice, and every square
  re-optimized. The same step applied to this packing gives the packing of 157.
- **Credit.** “Credit for the pinwheel arrangement at n = 109 belongs to Samanyu-dev.”
- **The local optimum.** IPOPT optimized every square together, and the contact equations
  were then solved to 250 digits. All 1,407 contact equations hold to 10⁻²⁶⁹ and every
  other gap stays open. The certificate’s side is 1.3 × 10⁻⁵⁹ above that solution.
  Non-negative contact forces in balance exist (in floating point), and 324 perturbation
  trials, each re-optimized, found no smaller side. Local optimality has no formal proof,
  and a search for a minimal polynomial of the side up to degree 16 found none.
- **The Kaggle caveat.** The competition “Squares in Squares” has a per-puzzle leaderboard
  that lists sides without packings. The author has not seen its values at 132, so an
  unpublished packing with a smaller side may exist.
- **The checker.** `verify_exact.py`, Python’s standard library only, is the folder’s one
  exact checker. It was not run here. The issue says it is the checker used for #946 without its
  polynomial test, and that a floating-point separating-axis test and a union-area test
  with Shapely, separate code outside the repository, agree. None of them ran here.
- **The issue on 109.** The issue says Samanyu-dev’s 109, side 10.949289581, is below the
  register’s 10.949747468 at 109, makes no claim there, and names its own contribution as
  the two growth steps and the optimization.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the licence, the root README and the whole of `n132/`,
8 files: 6 retained under [source/](source/) and 2 pinned by digest (`LICENSE`, against the
byte-identical copy the
[227, 229 and 260 packet](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md)
retains, and the figure). `n132/SHA256SUMS` states the digests of the five other files of
`n132/`, and they match. The s157 packet pins its root README and `verify_exact.py`
against this packet’s copies.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `c8448724e`. The certificate is 9.6318152 × 10⁻³ below T-174, the house (Evan
Daniel’s packing, improved by PingYou Ltd). The
[ledger of 11 November](../../../campaign/issue-intake/upper-bounds-de-winter-132-157-20261111/README.md)
records it as a new packing, the only report at 132.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, through the centre-basis reader
written for #939’s files: 3 jobs, all 8,646 pairs a job and route, 54.6 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes. Squares touch the walls
exactly, and every pair clears by at least 9.99 × 10⁻⁶¹.

`sharp-controls` took it to exact contact and 1e-30 past it on both routes
([receipts/sharp-controls.json](receipts/sharp-controls.json)), and every control behaved
as the module predicts:

- **Wall, pair and near-wall.** The box lowered to the extent (by 0), the tightest pair
  (square 119 against 14) closed by its gap of 10⁻⁶⁰, and every square moved to its near
  wall: each is accepted at exact contact and refused 1e-30 past it.
- **Enlarged to a pair.** Square 119, enlarged against 14, is refused at contact for its
  shape alone.
- **Enlarged to a wall.** Square 17 already touches its wall; grown by 0 it is accepted, and
  refused 1e-30 past for the wall and the overlap.
- **Duplicate.** A duplicated square is refused.

## Pose by Pose and Padding

`devtools.measure_identity` wrote [measure/identity.json](measure/identity.json), and
`devtools.contraction_margin` the `contraction-*.json` receipts under [measure/](measure/):

- **Against T-174.** No symmetry of the box pairs it one to one with T-174’s packing by
  nearest centres, and the house witness and its regularized view measure the same. The
  optimal assignment of least summed squared move moves 84 squares beyond a tenth and 91
  beyond a hundredth (largest 0.986), and turns 78, by up to 40.42 degrees. It is a new
  arrangement relative to T-174’s packing.
- **Its tilts.** 54 squares turn: 53 by 23.6 to 31.4 degrees, all the same way, and one by
  0.22 degrees. T-174 has 39, 18 turned one way and 21 the other.
- **T-174’s margin** is 0, its pair 87 and 88 already touching, so the whole gain of
  9.632 × 10⁻³ lies outside the predecessor’s padding
  ([contraction-n132.json](measure/contraction-n132.json)). RV-3 (think-ruu2) does not
  reach it.
- **Its own margin** is 1.248 × 10⁻⁵⁹ (1 − λ\* = 10⁻⁶⁰;
  [contraction-n132-own.json](measure/contraction-n132-own.json)), about the 1.3 × 10⁻⁵⁹
  the README states.

## The L Step

[measure/l-step-scan.json](measure/l-step-scan.json) is `devtools.l_step_scan` with this
side and the s157 packet’s stood in. From 132 the L step lands at 155 at the side plus one,
12.976…, above 155’s 12.952…, and from 157 at 182 at 13.993…, above 182’s 13.971…. The
scan finds every consequence main finds but one: 184’s L-extension of the grid at 157
lapses, its ceiling the grid’s 14 either way. Neither bound carries to another count.

## The Register

T-292 records the claim at V3/C3 on the replay, S3 as a draft for the stage 4 review. The
case record is not touched: the house rule adopts it once the review is mapped with an
accepted verdict, with both strong generators’ regularization of the new house and its
flip in the same change.

## Stage 4 Review

The stage 4 review of 11 November 2026
([review-2026-11-11-dewinter-132-157.md](../../../../docs/project/reviews/review-2026-11-11-dewinter-132-157.md), lane L105, under think-bcfs), written in
a separate lane blind to this one until its findings were frozen, accepts both
certificates; all 14 findings are notes. Its programs and receipts are in the review-only
directory [dewinter-132-157-review-2026-11-11](../dewinter-132-157-review-2026-11-11/README.md).

- **Feasibility.** Its clean-room checker decides both files, every square, wall and all
  8,646 pairs, by separating axes in `Fraction` and by exact clipped areas in
  `gmpy2.mpq`. It finds 20 exact wall contacts (ten at the right wall, ten at the top), the
  least positive wall clearance exactly 1.5 × 10⁻⁶⁰ (left and bottom), no pair touching,
  and the least pair margin 10⁻⁶⁰ less about 10⁻²⁵⁰, at squares 14 and 119. Its 16
  controls, stated beforehand, came out as stated, among them the squares accepted in the
  box of side 11.976048383604 itself (F5); the JSON and the YAML are one packing (F3).
- **Against this lane.** Its comparison printed `LANE_EQUALS_REVIEW` on 51 comparisons.
- **The construction (F11).** Measured from Samanyu-dev’s 109 at `53551d7`: under one
  symmetry (three quarter turns), the seed cut at about x = 3.58 and y = 7.37 and its four
  parts moved about one unit apart pairs every seed square with a square here within
  0.129. The 23 squares left over are 15 axis-aligned squares in the rows and columns at
  the cuts and 8 tilted ones. The seed is 4.58 × 10⁻⁴ below the record at 109,
  6 + (7/2)√2; #958 makes no claim there, and the seed’s repository is not watched or
  retained, so it is context and not a report here.
- **Notes for the author.** The side lies 1.2476 × 10⁻⁵⁹ above the configuration scaled
  back by 1 + 10⁻⁶⁰, the README’s 1.3 × 10⁻⁵⁹ rounded up (F8). Corner incidences within
  10⁻⁵⁰ number 1,423 against the README’s 1,407 equations (F9). The YAML is not a valid
  Witness/v2 file as this repository’s schema defines it (F10); it equals the JSON, and the
  record writes its own witness.
- **The seed’s licence (F12).** The seed’s repository has no licence file, only its
  README’s “MIT-style” sentence. That question is the owner’s on think-71uq, under
  think-gtmb, and decides nothing here.
- **F14.** At adoption the case’s credit fields are derived again for a new arrangement.

## Questions for the Author

The stage 4 review’s six questions, informational, holding nothing open:

1. The certificate reads as the solution scaled by 1 + 10⁻⁶⁰ and translated by 10⁻⁶⁰,
   which puts the sides 1.2476 and 1.3493 × 10⁻⁵⁹ above it. Were the stated 1.3 and
   1.4 × 10⁻⁵⁹ rounded up, or measured another way?
2. How are the 1,407 and 2,024 contact equations counted? A count of corners on edge
   segments and walls within 10⁻⁵⁰ gives 1,423 and 2,048.
3. Would the YAML carry the `softschema` header, a `claim` block and a lowercase id, so
   that it validates as a Witness/v2 file?
4. The cuts measure at about x = 3.58, y = 7.37 in the 109 packing turned three quarter
   turns, and at x = 8.33, y = 8.32 in the 132 packing turned one quarter turn. Are those
   the author’s cuts, and which squares were added in each gap?
5. Will the growth step’s code, the IPOPT model, the 250-digit solutions and the binary64
   and Shapely checks be published?
6. Samanyu-dev’s repository has no licence file. Did its author agree to the 109 packing
   being built on, and does “MIT-style” cover the packing data as well as the code?

## What Is Not Established

- **The 250-digit solution as a local optimum**, and any optimality: not replayed here.
- **Samanyu-dev’s 109**: not retained here; the review measured the growth step from it
  (F11), which decides nothing about the bound.
- **Human oversight**: no record is retained.

## Credit and Licence

The packing is Joost de Winter’s, after Samanyu-dev’s pinwheel at 109, which the source
credits. The README says the derivation, optimization, high-precision solution, rational
certificate, checking and figure were produced with Claude Fable 5.2 (Anthropic) under his
direction; `a491dad` said Claude (Anthropic). The source builds on no certificate or data
of this project, so the lineage is independent. The bibliography key is
**[de Winter s132 upper bound 2026-11-11]**.

Everything here is published under the MIT licence, copyright (c) 2026 Joost de Winter, by
`LICENSE` at the pin, which the root README says covers all files.

## Commands

From `packing/`, with the project interpreter. The identity measurement reads the house
witness and its regularized view as they stand at main `c8448724e`; the contraction margins
read the packets:

```bash
P=de-winter-s132-upper-bound-2026-11-11
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 132 "DEWINTER=packet:$P" \
  'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  'regularized=witness-corners:atlas/known-best/regularized/n-132-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-132.yaml' \
  --out resources/web/$P/measure/identity.json
python -m devtools.contraction_margin --n 132 'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  --against "dewinter-132=packet:$P" --out resources/web/$P/measure/contraction-n132.json
python -m devtools.contraction_margin --n 132 "dewinter-132=packet:$P" \
  --out resources/web/$P/measure/contraction-n132-own.json
python -m devtools.l_step_scan --with 132=S132 --with 157=S157 \
  --out resources/web/$P/measure/l-step-scan.json
```

In the last command each `S` is that count’s `exact_side` in its packet’s claim record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
