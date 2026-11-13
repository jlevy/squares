# Joost de Winter’s s(157) Certificate at 6617869

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/6617869a3491b5872c6ecdff55db05cbee57d516)
at `6617869a3491b5872c6ecdff55db05cbee57d516` (committed 2026-11-11T20:52:23Z), the head
of `main` when it was read at 20:58Z, which
[issue #958](https://github.com/jlevy/squares/issues/958) names. The issue was opened at
20:56:18Z, and the lane first read the folder as a publication in a watched repository
before it saw the issue.

The folder `n157/` first appeared at `a491dad` (20:49:44Z) with `n132/`, whose packet is
[de-winter-s132-upper-bound-2026-11-11](../de-winter-s132-upper-bound-2026-11-11/README.md)
and tells the history of both commits. `6617869` changes only the READMEs and checksums,
so the certificate’s bytes are `a491dad`’s. The push time is not read, and the issue
dates the claim, since no other report reached 157 in between.

Intake lane L104 (think-bcfs) retained it, replayed it and registered it on 11 November
2026 as **T-293**. The blind stage 4 review of lane L105 accepted it the same day, so it
is at V3/C3, and the case adopted it as its house in place of the grid under the house rule.

## What the Source Claims

- `n157/n157_witness.yaml` states 157 unit squares by centre and the unit direction of one
  edge, every number an exact rational, in the same envelope-free Witness/v2 object as the
  s132 packet’s. `n157/n157_exact.json` states the same packing as rows.
- **The side.** The root README rounds it up at 12 places, 12.993302611344, which the
  packet admits; `n157/README.md` cuts it at 50,
  12.99330261134322364133727935496577166311874424252458…, and calls it below the 13 × 13
  grid’s 13 by 0.0067.
- **The construction.** A pinwheel: a central block of tilted squares with four arms,
  surrounded by four blocks of axis-aligned squares, 61 tilted, at four distinct angles
  between 24.0 and 27.6 degrees, and 96 axis-aligned. It is derived in two steps from the
  public 109-square packing of `Samanyu-dev/squares_in_squares` (`53551d7`,
  `best_fit_101_500.csv`, side 10.949289581). Each step cuts the packing along one
  horizontal and one vertical line, moves the parts about one unit apart, fills each gap
  with one layer of squares that continues the local lattice and re-optimizes every
  square. The first step gives the packing of 132; the second gives this one.
- **Credit.** “Credit for the pinwheel arrangement at n = 109 belongs to Samanyu-dev.”
- **The local optimum.** IPOPT, then the contact equations solved to 250 digits: all 2,024
  hold to 10⁻²⁴⁷ and every other gap stays open, and the certificate’s side is 1.4 × 10⁻⁵⁹
  above that solution. Non-negative contact forces in balance exist (in floating point),
  and 297 perturbation trials found no smaller side. Local optimality has no formal proof,
  and no minimal polynomial of degree 16 or less was found.
- **The Kaggle caveat.** The per-puzzle leaderboard lists sides without packings; the
  author has not seen its values at 157, so an unpublished packing with a smaller side may
  exist.
- **The checker.** `verify_exact.py`, byte-identical to `n132/`’s, was not run here, nor
  were the floating-point and Shapely checks the issue says agree.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json). The scope is the licence, the
root README and the whole of `n157/`, 8 files: 4 retained under [source/](source/) and 4
pinned by digest. `LICENSE` is pinned against the byte-identical copy of the
[227, 229 and 260 packet](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md), the
root README and `verify_exact.py` against the s132 packet’s copies, and the figure by its
digest. `n157/SHA256SUMS` states the digests of the five other files of `n157/`, and they
match.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `c8448724e`. The certificate is 6.6973887 × 10⁻³ below the grid’s 13, which the case
holds in both lanes, and it is the first packing of 157 squares below the grid on record.
The
[ledger of 11 November](../../../campaign/issue-intake/upper-bounds-de-winter-132-157-20261111/README.md)
records it as a new packing, the only report at 157.

Since 157 = 13² − 13 + 1, the record now shows s(k² − k + 1) < k at k = 13. Kevin Fang’s
Theorem 1 (T-163) gives it for every k ≥ 15, and Evan Daniel’s 183 (T-220) at k = 14; 111
and 133 (k = 11 and 12) stay at their grids.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes: 3 jobs, all 12,246 pairs a job
and route, 78.4 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes. Squares touch the walls
exactly, and every pair clears by at least 9.99 × 10⁻⁶¹.

`sharp-controls` ([receipts/sharp-controls.json](receipts/sharp-controls.json)) behaved as
the module predicts on both routes:

- **Wall, pair and near-wall.** The box lowered by 0, the tightest pair (square 101 against
  88) closed by its gap of 10⁻⁶⁰, and every square moved to its near wall: each is accepted
  at exact contact and refused 1e-30 past it.
- **Enlarged to a pair.** Square 101, enlarged against 88, is refused at contact for its
  shape alone.
- **Enlarged to a wall.** Square 109 already touches its wall; grown by 0 it is accepted,
  and refused 1e-30 past for the wall and the overlap.
- **Duplicate.** A duplicated square is refused.

## Pose by Pose and Padding

- **Against the grid.** [measure/identity.json](measure/identity.json) reads the house
  witness, `witnesses/known-best/n-157.yaml`, through the corner reader, which accepts the
  schema path the house witnesses state from this lane on. No symmetry of the box pairs
  the certificate one to one with the grid’s squares by nearest centres. The optimal
  assignment moves 100 squares beyond a tenth (largest 1.409) and turns 61, every one by
  24.0 to 27.5 degrees, all the same way.
- **The grid’s margin** is 0, its squares touching
  ([contraction-n157.json](measure/contraction-n157.json)), so the whole gain of
  6.697 × 10⁻³ lies outside any padding. A packing below the grid is no re-certification
  of it, and RV-3 (think-ruu2) does not reach it.
- **Its own margin** is 1.349 × 10⁻⁵⁹ (1 − λ\* = 10⁻⁶⁰;
  [contraction-n157-own.json](measure/contraction-n157-own.json)), about the 1.4 × 10⁻⁵⁹
  the README states.
- **The L step.** The scan in the s132 packet stands both sides in. From 157 the step lands
  at 182 at 13.993…, above 182’s 13.971…, and 184’s L-extension of the grid at 157 lapses.
  The bound carries to no other count.

## The Register

T-293 records the claim at V3/C3, S3, the same score as T-057 at 211 and T-220 at 183, as
the stage 4 review confirmed. The case adopted it as its house on 11 November 2026 under
the house rule, in place of the grid, and withdrew its conjectured integer optimum. Both
strong generators ran on the new witness
([the runs](../../../cases/regularized_drawings/think-bcfs-2026-11-11/README.md)): the
picture is grid-slack’s 0.5-degree view, and Evan Daniel’s solve lies above the side,
held.

## Stage 4 Review

The stage 4 review of 11 November 2026
([review-2026-11-11-dewinter-132-157.md](../../../../docs/project/reviews/review-2026-11-11-dewinter-132-157.md), lane L105) accepts this certificate with
the 132’s; all 14 findings are notes. The s132 packet’s README gives the review in full.

- **Feasibility.** Its clean-room checker decides both files, every square, wall and all
  12,246 pairs, by two exact methods. It finds one exact wall contact (square 109, right),
  the least positive wall clearance 1.01 × 10⁻²⁴⁸ (square 136, right), no pair touching,
  and the least pair margin 10⁻⁶⁰ less about 10⁻²⁴⁷, at squares 88 and 101. Its 16
  controls came out as stated, among them the squares accepted in the box of side
  12.993302611344 itself.
- **The construction (F11).** Measured from the author’s 132: under one symmetry (one
  quarter turn), the 132 cut at about x = 8.33 and y = 8.32 and its four parts moved about
  one unit apart pairs every one of its squares with a square here within 0.126. The 25
  squares left over are 17 axis-aligned squares at the cuts and 8 tilted ones.
- **Notes for the author.** 1.3493 × 10⁻⁵⁹ above the scaled-back configuration, the
  stated 1.4 × 10⁻⁵⁹ rounded up (F8); 2,048 corner incidences against 2,024 equations
  (F9); the YAML’s schema deviations (F10).
- **F14.** At adoption the case’s `conjectured_optimum: integer` and its prose that nothing
  beats the grid are retired, as at 183 and 211.

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

## The Author’s Answers

Joost de Winter answered the six questions on 12 November 2026
([issuecomment-6818738203](https://github.com/jlevy/squares/issues/958#issuecomment-6818738203),
08:31:55Z); the
[s132 packet](../de-winter-s132-upper-bound-2026-11-11/README.md#the-authors-answers)
records them in full. At 157:

- **The margin (F8).** The stated 1.4 × 10⁻⁵⁹ is the measured 1.3493 × 10⁻⁵⁹ rounded up.
- **The count (F9).** The 2,024 are the equations his solver used, counted on edge lines
  within 10⁻⁶ in the binary64 solution, not on edge segments within 10⁻⁵⁰.
- **The witness (F10).** `57de046` adds the header, the claim block and the lowercase
  id, with the squares and the side unchanged; the
  [method packet](../de-winter-method-132-157-2026-11-12/README.md) retains it, and this
  packet stays at `6617869`.
- **The cuts (F11).** His second step cut the 132 at x = 9.71, y = 3.33, which he reads
  as the review’s cuts, since, he says, the packings have fourfold symmetry and a cut can
  sit anywhere inside an axis-aligned block. He says the squares added were copies of the
  12 + 13 that bordered the cuts, matching in number the 25 the review found left unpaired.
- **The method.** Published in `57de046`, retained in the method packet and not run
  here, so the byte-for-byte reproduction from the seed is the author’s claim, unchecked.
- **The seed’s licence (F12).** He has not contacted Samanyu-dev; it stays the owner’s
  question on think-71uq.

## What Is Not Established

- **The 250-digit solution as a local optimum**, and any optimality: not replayed here.
- **Samanyu-dev’s 109**: not retained here; the review measured both growth steps (F11),
  which decide nothing about the bound.
- **Human oversight**: no record is retained.

## Credit and Licence

The packing is Joost de Winter’s, after Samanyu-dev’s pinwheel at 109, which the source
credits; it continues his own 132. The README says the work was produced with Claude Fable
5.2 (Anthropic) under his direction. The lineage is independent of this project. The
bibliography key is **[de Winter s157 upper bound 2026-11-11]**. Everything here is
published under the MIT licence, copyright (c) 2026 Joost de Winter, by `LICENSE` at the
pin.

## Commands

From `packing/`, with the project interpreter:

```bash
P=de-winter-s157-upper-bound-2026-11-11
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 157 "DEWINTER=packet:$P" \
  'grid=witness-corners:witnesses/known-best/n-157.yaml' \
  --out resources/web/$P/measure/identity.json
python -m devtools.contraction_margin --n 157 'grid=witness-corners:witnesses/known-best/n-157.yaml' \
  --against "dewinter-157=packet:$P" --out resources/web/$P/measure/contraction-n157.json
python -m devtools.contraction_margin --n 157 "dewinter-157=packet:$P" \
  --out resources/web/$P/measure/contraction-n157-own.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
