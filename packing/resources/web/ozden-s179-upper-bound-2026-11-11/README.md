# Doğa Özden’s s(179) Certificate at bd262d8

This packet retains
[kenaznia-doga/s179-upper-bound](https://github.com/kenaznia-doga/s179-upper-bound/tree/bd262d8ba2966000e827547597fe6da24d0e118c)
at `bd262d8ba2966000e827547597fe6da24d0e118c` (committed 2026-11-11T18:27:50Z), the
repository’s one commit, which [issue #954](https://github.com/jlevy/squares/issues/954)
names 24 seconds later. Doğa Özden’s AI agent, which uses the account kenaznia-doga,
prepared and posted both on his behalf.

## What the Source Claims

- `n-179-candidate.yaml`, a `packing.squares:Witness/v2` file (corners, rational scalars,
  179 squares), bounds s(179) by its exact side, a fraction whose denominator has 158
  places and whose 16-place ceiling is 13.8813671601098758. #954 prints its 12-place
  ceiling, 13.881367160110, and says it is 2.428e-03 below the record, Nate
  Chaoweeraprasit’s packing (itsnaka), improved by Siddharth Gupta and PingYou Ltd
  (T-174). It claims an upper bound only: no KKT, local-optimality, rigidity or
  global-optimality claim.
- The exact coordinates were made by this repository’s own `packing-witness promote
  --strategy robust-rational` at `591644a9` from the lab’s decimal pose,
  `n-179-decimal-pose.yaml`, which the witness’s `source.path` names, with
  `center_dilation: '1'` and no dilation. The issue says the pair margins of about
  2 × 10⁻¹³ are the decimal pose’s own, left by the final binary64 repair scaling of
  Evan Daniel’s quench, that only the squares that set the left wall, the bottom wall
  and the side touch them exactly, and that other squares near a wall clear it by up to
  about 10⁻¹². Measured by the review, exactly three squares touch a wall (123 at the left,
  39 at the bottom and 117 at the right), as the issue says; the other 36 square–wall
  clearances below 10⁻¹² are at most 4.29 × 10⁻¹⁴, and eight square–wall pairs lie between
  6.84 × 10⁻⁵ and 7.21 × 10⁻⁴ from a wall, which the issue’s “near a wall” does not cover.
  The certificate is the decimal pose translated by about 1.04 × 10⁻¹³ toward the corner,
  every centre equal to the pose’s to 1.8 × 10⁻³⁷, so the pair margins are the pose’s own,
  as the issue says; they lie between 2.03 and 4.08 × 10⁻¹³ of the centres’ separation along
  the binding axis, median 2.17 × 10⁻¹³, about twice the issue’s “about 1e-13 relative”
  (F5).
- `n179-witness.json` is the same file as JSON. `packing-witness-verify.txt` is the
  author’s run of this repository’s `packing-witness verify` at `591644a9` (VERIFIED,
  15,931 pairs); `sqcheck-output.txt` is the author’s run of `verifier/sqcheck.py`, an
  exact checker the source says was written separately from this repository’s code
  (VALID, exact rational, the exact side rounded up). The issue says the two share only
  the unit-square, wall and non-overlap definitions, that `packing-witness verify` is not
  independent of how the coordinates were rounded, and that `sqcheck.py` certified the
  decimal pose in interval arithmetic at its own side before promotion.
  Those statements are the author’s; no source program ran here.
- The issue says the packing was found by an AI-run band-design search, new for this
  filing: tilted squares from a registry packing of the same family laid along the
  diagonal as a seed band; simulated annealing in a reduced model in which the tilted
  squares move freely and the axis-parallel squares sit on the two wall-anchored
  staircase lattices, present or absent, with the overlap of the squares that must be
  kept as energy; then one quench with Evan Daniel’s ALM+SLP code from
  [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT,
  at `bb4cc78e`). The band is built from the tilted squares of the registry’s n = 70
  packing (Ryan Xu, improved by Evan Daniel and PingYou Ltd; side 8.880960371555579595),
  a two-row band of 20 squares at −40.7505 degrees along the diagonal; the registry’s
  n = 207 packing (PingYou Ltd) is two such bands, mirrored, which the review measures at
  19 squares each, not 20 (F7). Its seed, `M_55_16_36`, is
  that band where x + y ≤ 16 and a second copy shifted by (5, 5) where x + y > 16,
  overlapping squares dropped and random adjacent squares added up to 36 tilted squares,
  annealed at side 13.8812 and then quenched; two other seeds of the same scan quench to
  the same side. The issue describes the result as one straight band of 35 squares from
  corner to corner, where the record’s band is wavy and lies on the other diagonal.
  Against the registry packing, matched by assignment up to the square’s symmetries, it
  reports 146 of 179 centres beyond 1e-3, 54 beyond 0.05 (largest 0.886), 44 squares
  re-tilted beyond 1 degree (largest 44.36), and 37 squares tilted beyond 0.5 degree
  against the record’s 35. The review reproduces every one of those counts with the house
  reflected top to bottom and set against the upper-left corner of the new box, an
  anchoring the issue does not name (F6).

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the whole tree, 11 files: 7 retained under
[source/](source/) and 4 pinned by digest.

| File | Bytes |
| --- | --- |
| `LICENSE.md` | 1,484 |
| `README.md` | 6,539 |
| `n-179-candidate.yaml` | 527,207 |
| `n-179-decimal-pose.yaml` | 19,415, the decimal pose the witness was promoted from |
| `n179-witness.json` | 521,699, the same packing as JSON, which the reader holds equal to the YAML |
| `packing-witness-verify.txt` | 499 |
| `sqcheck-output.txt` | 101 |
| `LICENSE-evand-square-packing.txt` | 1,068, pinned against the identical copy of Evan Daniel’s MIT notice the [evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains |
| `records/n-179-candidate-diff.png` | 241,795, pinned by digest: a raster comparison that decides nothing |
| `verifier/README.md` | 3,441, pinned against the identical copy the [3 November s299 packet](../ozden-s299-upper-bound-2026-11-03/README.md) retains |
| `verifier/sqcheck.py` | 17,654, pinned against the identical copy the [9 November s232 packet](../ozden-s232-upper-bound-2026-11-09/README.md) retains, never executed here |

The SHA-256s the issue states for `n-179-candidate.yaml` and the README states for it and
for `n179-witness.json` are the files’.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is about a megabyte in a checkout and far less as Git stores it, so it is kept
in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `c8448724e` on 11 November
2026):

- **179:** exact side 13.8813671601098758 rounded up at 16 places, below the case’s house
  (T-174, Nate Chaoweeraprasit’s packing) by 2.428e-03, as the issue states. No register
  bound is pending adoption at 179.

## Report Order

The [ledger of 11 November for this lane](../../../campaign/issue-intake/upper-bounds-954-20261111/README.md)
walks every report at 179 in the order it reached this repository, from a start frozen at
`main` `c8448724e`, and records this packet’s claim at 179.
The best public Kaggle per-puzzle packing the issue quotes at 179, 13.883795490524
(kirilltym), is above this. The issue also quotes, and states first, a side-only Kaggle
leaderboard entry at 179, 13.880960371556 (team Nevska, 7 November), 4.07e-4 below this
side, whose fractional part is that of the registry’s n = 70 and n = 207 sides. It is
unpublished and states no packing, so it is no report and is recorded as context only.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-174’s packing, the house
witness and the regularized view, and wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **179:** no symmetry of the box pairs it one to one with T-174’s packing by nearest
  centres. The optimal assignment, under the best of the box’s eight symmetries, moves 47
  squares beyond 0.1 and 60 beyond 0.01 (largest 0.885496) and turns 58 squares by more
  than 10⁻⁶ radians, by up to 44.36 degrees, under the assignment of least summed squared
  move; aligned by box centres, 44 squares turn by more than a degree, as the issue says.
  Tilted beyond a degree: 36 here, 27.3 to 41.4 degrees from upright, all turned the same
  way; T-174’s 35, 41.2 to 44.4 degrees, near the diagonal, where no split by sign is
  given. The house witness and the regularized view measure the same. So it is a new
  arrangement relative to T-174’s packing, not a further arrangement of it, as the review
  finds (F9). Anchored at the lower-left corner, as here, or at the centres, every square
  moves beyond 10⁻³, since the sides differ by 2.4 × 10⁻³; the issue’s 146 beyond 10⁻³
  holds with the house reflected top to bottom and set against the upper-left corner (F6).
- **The seed.** The seed the issue states, the 70 band where x + y ≤ 16 and its copy
  shifted by (5, 5) where x + y > 16, lies within 0.05 of 28 of the 37 squares tilted here
  beyond half a degree (31 within 0.1, 33 within 0.25), each turned by less than a degree,
  under the identity of the 70 box and under none of its other seven symmetries; the review
  reads that as strong support for the stated seed (F8). The new band runs corner to corner
  along the main diagonal; T-174’s tilted squares lie along the other.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 95,586 pair decisions, 40.27 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 2.03e-13. `check --replay` decided the three jobs again.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
10⁻³⁰ past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)), with the
expected verdicts stated before it ran. It lowered the side by the least far-wall
clearance, closed the least-gap pair (squares 14 and 15) by its gap, and moved every
square toward the nearer near wall by its least clearance: both routes accepted each at
contact with margin 0 and refused each past it.
It enlarged one square to its pair and one to its wall: both routes refused the first at
contact for its shape alone and accepted the second, square 39, which already touches its
wall and so grew by 0, at contact; both refused each 10⁻³⁰ past it for the overlap or the
wall as well. Both refused a duplicated square.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read the witness through the `witness-corners`
reader. The first route is the `packing-witness verify` the author ran on the same file,
so on that route the replay is reproduced with the producer’s code; the second shares no
verification code with it. Neither is independent of this repository’s `packing-witness
promote`, which made the coordinates. The source’s own `sqcheck.py` was not run.

## The Gain Against Padding

T-174’s certificate at 179, contracted uniformly about the origin to first contact and
boxed, loses no side at all (1 − λ\* = 0): squares 119 and 122 already touch, so it has
no padding to measure, and none of the gain this certificate states, 2.428e-03, is the
house’s padding. The owner’s open question about gains inside a padding margin (RV-3,
think-ruu2) does not reach it, so the entry is not held at V0/C1 as T-285 and T-286 were.
This certificate’s own margin, measured the same way, is 2.616e-12 (1 − λ\* =
2.030834e-13, the binding pair the least-gap pair of the replay, squares 14 and 15).
`devtools.contraction_margin` wrote both receipts,
[measure/contraction-n179.json](measure/contraction-n179.json) and
[measure/contraction-n179-own.json](measure/contraction-n179-own.json), each contracted
packing decided on both maintained routes. The review decided T-174’s witness with its own
checker and found the same touching pair: the gain lies inside no padding margin and is no
re-certification of the house, so RV-3 does not reach it.

## The L Step

`devtools.l_step_scan`, with this side stood in for 179’s ceiling, finds the same L-step
and monotonicity consequences as on `main`: this bound carries to no other count
([measure/l-step-scan.json](measure/l-step-scan.json)).

## Stage 4 Review and Adoption

The stage 4 mathematical review of 11 November 2026
([review-2026-11-11-ozden-954.md](../../../../docs/project/reviews/review-2026-11-11-ozden-954.md)),
written in a separate lane (L101) blind to this one until its findings were frozen,
accepts the certificate with findings, all notes, none blocking, and scores it S3. Its
clean-room checker decides every square, wall and pair by separating axes in `Fraction`
and by exact clipped areas in GMP rationals, with 17 controls stated before they ran, and
accepts the same squares in the box of the claim’s own side, 13.881367160110 (F3); its
programs and receipts are kept in the review-only directory beside this packet,
[ozden-s179-review-2026-11-11](../ozden-s179-review-2026-11-11/README.md). Its comparison
with this packet’s receipts printed `LANE_EQUALS_REVIEW` on 24 comparisons.
The witness’s `softschema.schema` names `witness.schema.yaml`, which resolves to no file in
the author’s repository, and its `certificate.replay` names the file but not where to run
it, unlike the README’s rerun (F11); the adopted witness carries this repository’s own.
Both are notes for the author.

The band’s geometry is the registry’s 70 witness, which comes from PingYou Ltd’s PR 574
algebraic supplement, a release with no licence file, kept here in the derived-only form.
Whether a seed taken from it needs a notice of its own is, in the review’s words,
`think-mdxq`’s question (F10), as the 9 November reviews put their upstream starts; that
bead closed on 4 November with the lab’s own licence answer. It is noted here, not
decided.

Its questions for the author, informational and holding nothing open:

1. Was the final repair scaling about 2 × 10⁻¹³ rather than 10⁻¹³, since the margins are
   2.03 to 4.08 × 10⁻¹³ of the centres’ separation (F5)?
2. Do the lineage counts use the house reflected top to bottom and set against the
   upper-left corner, and would the issue name that convention (F6)?
3. Does “two such bands” at 207 mean the 70 band cut where the two meet, since each has 19
   tilted squares (F7)?
4. Did the seed take the 70 band from the registry’s witness (PingYou Ltd’s algebraic
   certificate) or from Ryan Xu’s or Evan Daniel’s published coordinates?
5. Which replay is intended, `certificate.replay` or the README’s rerun, and from which
   directory, and would the schema path name this repository’s file (F11)?
6. Will the band-design search and its seeds be published? The record scores a reusable
   technique on its own.

The case adopted the certificate as its house on 11 November 2026 under the house rule,
as T-291, in place of T-174, which keeps its certificate as history, with Doğa Özden the
packing’s finder, the band of Ryan Xu’s n = 70 packing, as Evan Daniel and PingYou Ltd
improved it, credited as the search’s seed, and T-174’s packing as the record it improves
(the review’s F9). Both strong generators ran on the new witness
([the runs](../../../cases/regularized_drawings/think-f65n-2026-11-11/README.md)), and the
selection, measured against this witness’s drawing, draws Evan Daniel’s same-side view:
light, uneven and near-axis squares, angle classes and hues 7, 20, 5, 19 and 19 against
0, 0, 0, 5 and 5, and full shared sides 475 and 505 against 550 and 550. His certified KKT
solve lies 2.78 × 10⁻¹² below the side, about the certificate’s own contraction margin
(2.62 × 10⁻¹²), held at row 3 as a register candidate and not admitted, as at 156, 172,
180, 199, 268, 269 and 270 (RV-3). The rigidity block, derived again on the new witness,
stays not rigid: 74 of its 179 squares translate, against 7 of T-174’s.

## What Is Not Established

- **Human oversight.** One AI review is retained; no human oversight record.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **The lineage** the source states, beyond what the measurement above shows.

## Credit and Licence

The packing is Doğa Özden’s, found by his lab’s band-design search from the tilted squares
of the registry’s n = 70 packing (Ryan Xu, improved by Evan Daniel and PingYou Ltd). The
case record credits Özden as the finder, the 70 packing’s holders as the band’s source and
T-174’s holders as the record it improves (the review’s F9). The issue asks that the improvement be credited to Özden, the band’s source packing and the
current record to their holders as the registry lists them, and the local optimizer to
Evan Daniel. The issue says the search and its code were written and run by AI agents
throughout and that the checks were run by code that did not produce the packing; it says
the issue and repository were prepared and posted by his AI agent, and that Özden
directed the work. The source starts from this repository’s registry packings and makes
its exact coordinates with this repository’s promotion tool, so its lineage builds on
this project. The bibliography key is **[Özden s179 upper bound 2026-11-11]**.

The witness, the JSON, the decimal pose, the checker outputs, the README and the diff
image are published under CC BY 4.0, and `verifier/sqcheck.py` under the MIT licence,
copyright (c) 2026 Doğa Özden, as [source/LICENSE.md](source/LICENSE.md) states; it is
byte-identical to the `LICENSE.md` the lab added to its s299, s204 and s94 repositories
on 4 November 2026 and announced on #890
([comment](https://github.com/jlevy/squares/issues/890#issuecomment-6637821113)).
The diff image is pinned by digest only. The source carries Evan Daniel’s MIT notice as
`LICENSE-evand-square-packing.txt`, for his quench code, byte-identical to the `LICENSE`
the [evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains,
and pinned against it.

## Commands

From `packing/`, with the project interpreter. The identity measurement reads the house
witness and its regularized view as they stood at main c8448724e, before this adoption
replaced them, so it reproduces there; the contraction margins read the packets and
reproduce anywhere `devtools.contraction_margin` is:

```bash
python -m devtools.acquire_source ozden-s179-upper-bound-2026-11-11 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s179-upper-bound-2026-11-11 --check
python -m devtools.upper_bound_reports ozden-s179-upper-bound-2026-11-11 check-claims --write
python -m devtools.upper_bound_reports ozden-s179-upper-bound-2026-11-11 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ozden-s179-upper-bound-2026-11-11 check --replay
python -m devtools.upper_bound_reports ozden-s179-upper-bound-2026-11-11 sharp-controls
python -m devtools.measure_identity --n 179 'OZDEN=packet:ozden-s179-upper-bound-2026-11-11' \
  'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  'regularized=witness-corners:atlas/known-best/regularized/n-179-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-179.yaml' \
  --out resources/web/ozden-s179-upper-bound-2026-11-11/measure/identity.json
python -m devtools.contraction_margin --n 179 'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  --against 'ozden-954=packet:ozden-s179-upper-bound-2026-11-11' \
  --out resources/web/ozden-s179-upper-bound-2026-11-11/measure/contraction-n179.json
python -m devtools.contraction_margin --n 179 'ozden-954=packet:ozden-s179-upper-bound-2026-11-11' \
  --out resources/web/ozden-s179-upper-bound-2026-11-11/measure/contraction-n179-own.json
python -m devtools.l_step_scan --with 179=S179 \
  --out resources/web/ozden-s179-upper-bound-2026-11-11/measure/l-step-scan.json
```

In the last command `S179` is the `exact_side` in the packet’s claim record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
