# Doğa Özden’s s(180) Certificate at 4cfcb90

This packet retains
[kenaznia-doga/s180-upper-bound](https://github.com/kenaznia-doga/s180-upper-bound/tree/4cfcb9058a5bc5e8e6986bda31c072ccefc3731f)
at `4cfcb9058a5bc5e8e6986bda31c072ccefc3731f` (committed 2026-11-10T15:27:50Z), the
repository’s one commit, which [issue #944](https://github.com/jlevy/squares/issues/944)
names 51 seconds later. Doğa Özden’s AI agent, which uses the account kenaznia-doga,
prepared and posted both on his behalf.

## What the Source Claims

- `n-180-candidate.yaml`, a `packing.squares:Witness/v2` file (corners, rational scalars,
  180 squares), bounds s(180) by its exact side, a fraction whose denominator has
  159 places and whose 16-place ceiling is 13.9156185027900258. #944 prints its 12-place
  ceiling, 13.915618502791, and says it is 1.375e-03 below the record, Nate Chaoweeraprasit's packing, refined by Siddharth Gupta, Francisco Couzo and PingYou Ltd
  (T-174). It claims an upper bound only: no KKT, local-optimality, rigidity or
  global-optimality claim.
- The exact coordinates were made by this repository’s own `packing-witness promote
  --strategy robust-rational` at `f54ad104` from the lab’s decimal pose,
  `n-180-decimal-pose.yaml`, which the witness’s `source.path` names, with
  `center_dilation: '1'` and no dilation. The issue says the pair margins of about
  2 × 10⁻¹³ are the decimal pose’s own, left by the final binary64 repair scaling of
  Evan Daniel’s quench, that only the squares that set the left wall, the bottom wall
  and the side touch them exactly, and that other squares near a wall clear it by up to
  about 10⁻¹². Measured by the review, exactly three squares touch a wall (108 at the left, 132 at the bottom and 48 at the top), as the issue says; square 51 clears the top by 1.2e-12, and 9 square-wall pairs lie between 3.1e-6 and 9.7e-4 from a wall, a range the review gives for the 63 such pairs at 180, 268 and 269 together, which a reader taking "near a wall" for "against a wall" would count (F5). The pair margins are the decimal pose's own, as the issue says, and lie between 2.0e-13 and 9.8e-13 of the centres' separation along the separating axis, median 2.09e-13 here, about twice the issue's "about 1e-13 relative" (F6).
- `n180-witness.json` is the same file as JSON. `packing-witness-verify.txt` is the
  author’s run of this repository’s `packing-witness verify` at `f54ad104` (VERIFIED,
  16,110 pairs); `sqcheck-output.txt` is the author’s run of `verifier/sqcheck.py`, an
  exact checker the source says was written separately from this repository’s code
  (VALID, exact rational, the exact side rounded up). The issue says the two share only
  the unit-square, wall and non-overlap definitions, that `packing-witness verify` is not
  independent of how the coordinates were rounded, and that `sqcheck.py` certified the
  decimal pose in interval arithmetic at its own side before promotion.
  Those statements are the author’s; no source program ran here.
- The issue says the packing was found by AI-run transplant search: seeds built from
  neighbouring counts’ registry packings, quenched with Evan Daniel’s ALM+SLP code from
  [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT,
  at `bb4cc78e`), then basin hopping over the quench’s local minima. Its seed was the
  registry’s 154 (Evan Daniel, improved by Francisco Couzo; side 12.9211009407616806; [Daniel n154 sweep 2026-10-20]),
  seed type L-1, an L of axis-aligned grid squares added along two walls, squares then deleted or inserted to reach 180, then quenched; the hit came from the basin-hopping stage
  (chain 2, trial 1281, move kick). Against the registry packing, matched by assignment up to the square’s
  symmetries, it reports 162 of 180 centres beyond 1e-3, 49 beyond 0.05 (largest 0.91), 49 squares re-tilted beyond 1 degree (largest 44.68), 40 squares tilted beyond 0.5 degree against the record's 44.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the whole tree, 11 files: 7 retained under
[source/](source/) and 4 pinned by digest.

| File | Bytes |
| --- | --- |
| `LICENSE.md` | 1,484 |
| `README.md` | 5,286 |
| `n-180-candidate.yaml` | 544,019 |
| `n-180-decimal-pose.yaml` | 20,300, the decimal pose the witness was promoted from |
| `n180-witness.json` | 538,480, the same packing as JSON, which the reader holds equal to the YAML |
| `packing-witness-verify.txt` | 502 |
| `sqcheck-output.txt` | 101 |
| `LICENSE-evand-square-packing.txt` | 1,068, pinned against the identical copy of Evan Daniel’s MIT notice the [evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains |
| `records/n-180-candidate-diff.png` | 267,177, pinned by digest: a raster comparison that decides nothing |
| `verifier/README.md` | 3,441, pinned against the identical copy the [3 November s299 packet](../ozden-s299-upper-bound-2026-11-03/README.md) retains |
| `verifier/sqcheck.py` | 17,654, pinned against the identical copy the [9 November s232 packet](../ozden-s232-upper-bound-2026-11-09/README.md) retains, never executed here |

The SHA-256s the issue states for `n-180-candidate.yaml` and the README states for it and
for `n180-witness.json` are the files’.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is under two megabytes in a checkout and far less as Git stores it, so it is
kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `f54ad1048` on 11 November
2026):

- **180:** exact side 13.9156185027900258 rounded up at 16 places, below the case’s house
  (T-174, Nate Chaoweeraprasit's packing) by 1.375e-03, as the issue states.

## Report Order

The [ledger of 11 November for this lane](../../../campaign/issue-intake/upper-bounds-943-947-20261111/README.md) walks every report at 180 in the
order it reached this repository, from starts frozen at `main` `f54ad1048`, and records
this packet’s claim at 180. The best public Kaggle per-puzzle packing the issue quotes at
180, 13.916993522491 (kirilltym), is above this. The issue also quotes a side-only Kaggle leaderboard entry at 180, 13.916993522478 (team webmaking, 27 October), which the issue says is the registry's side to 12 places; it states no packing, so it is no report.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-174’s packing, the
house witness and the regularized view, and wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **180:** no symmetry of the box pairs it one to one with T-174’s packing by
  nearest centres. The optimal assignment, under the best of the box’s eight symmetries,
  moves 49 squares beyond 0.1 and 82 beyond 0.01
  (largest 0.921464) and turns 61 squares by more than 10⁻⁶
  radians, by up to 44.68 degrees, under the assignment of least summed
  squared move. Tilted beyond a degree: 40 here, 37.1 to 44.8 degrees from upright; T-174's 44, 26.5 to 44.7 degrees. Near the diagonal the sign of the angle separates orientations only degrees apart, so no split by sign is given (F16). The house witness measures the same, and against the
  regularized view the assignment moves 49 squares beyond 0.1. So it is a new
  arrangement relative to T-174’s packing, not a further arrangement of it (the review’s
  F10). The issue's own counts against the house (162 centres beyond 1e-3, 49 beyond 0.05, the largest move 0.91, 49 squares re-tilted beyond a degree, the largest by 44.68 degrees) reproduce, as the review measured, with lower-left anchoring and the assignment of least summed move; under least summed squared move, which these measurements use, the best symmetry is the transpose and the counts are 163, 54, 0.921 and 50 (F7).
- **The seed.** Modelled as the issue's L-1 extension of the registry's 154 (shifted by (0, -1)), 121 squares match within 0.05 and a degree, 12 of the 40 tilted ones, where the house under the same model matches 127 and 5: the model cannot tell the seed from the house, so the seed is the author's account, consistent with the measure but not shown by it (F8).

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 96,660 pair decisions, 42.39 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 2.00e-13. `check --replay` decided the three jobs again.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
10⁻³⁰ past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)), with the
expected verdicts stated before it ran. It lowered the side by the least far-wall
clearance, closed the least-gap pair by its gap, and moved every square toward the
nearer near wall by its least clearance: both routes accepted each at contact with
margin 0 and refused each past it.
It enlarged one square to its pair and one to its wall: both routes refused the first at
contact for its shape alone and accepted the second, which already touches its wall and
so grew by 0, at contact; both refused each 10⁻³⁰ past it for the overlap or the wall as
well. Both refused a duplicated square.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read the witness through the `witness-corners`
reader. The first route is the `packing-witness verify` the author ran on the same file,
so on that route the replay is reproduced with the producer’s code; the second shares no
verification code with it. Neither is independent of this repository’s `packing-witness
promote`, which made the coordinates. The source’s own `sqcheck.py` was not run.

## The Gain Against Padding

T-174’s certificate, contracted uniformly about the origin to first contact and
boxed, loses 0.000e+00 of side (1 − λ\* = 0.000000e+00); the gain this certificate
states, 1.375e-03, is the house certificate has no padding to measure: a pair already touches, so no share of it worth stating is the
house’s padding, and the owner’s open question about gains inside a padding margin (RV-3,
think-ruu2) does not reach it. This certificate’s own margin, measured the same way, is
2.584e-12 (1 − λ\* = 2.000899e-13, the binding pair the least-gap pair of the replay).
`devtools.contraction_margin` wrote both receipts,
[measure/contraction-n180.json](measure/contraction-n180.json) and
[measure/contraction-n180-own.json](measure/contraction-n180-own.json), each contracted
packing decided on both maintained routes. The review measured the same house margins with its own programs (F9): no gain is near one, and these are not re-certifications of a house, so RV-3 (think-ruu2) does not reach them.

## The L Step

`devtools.l_step_scan`, with this side and the lane’s other three stood in for their
ceilings, finds the same L-step and monotonicity consequences as on `main`: this bound
carries to no other count
([the receipt in the s156 packet](../ozden-s156-upper-bound-2026-11-10/measure/l-step-scan.json)).

## Stage 4 Review and Adoption

The stage 4 mathematical review of 11 November 2026
([review-2026-11-11-ozden-943-947.md](../../../../docs/project/reviews/review-2026-11-11-ozden-943-947.md)),
written in a separate lane (L83, think-x8oc) blind to this one until its findings were
frozen, accepts the certificate with findings, all notes, none blocking, and scores it
S3. Its clean-room checker decides every square, wall and pair by separating axes in
`Fraction` and by exact clipped areas in GMP rationals, with 15 controls stated before
they ran; its programs are kept once in the
[156 packet’s review directory](../ozden-s156-upper-bound-2026-11-10/review/review-2026-11-11/README.md),
and this count’s receipts in [review/review-2026-11-11/out/](review/review-2026-11-11/out/).
The witness's softschema.schema names witness.schema.yaml, which resolves to no file in the author's repository (F12), and its certificate.replay names the file but not where to run it, unlike the README's rerun (F13); the adopted witness carries this repository's own. Both are notes for the author.

Its questions for the author, informational and holding nothing open: how much of the stated seed, the registry's 154, the author expected to remain after 1,281 basin-hopping trials, since the measured relation to it is no closer than to the house (F8); whether the final repair scaling was about 2e-13 rather than 1e-13, since the margins are 2.0e-13 to 9.8e-13 of the centres' separation (F6); which assignment the lineage counts use, least summed move with lower-left anchoring reproducing them all (F7); which replay is intended, certificate.replay or the README's rerun, and from which directory, and whether the schema path could name this repository's file (F12, F13).

The case adopted the certificate as its house on 11 November 2026 under the house rule,
as T-288, in place of T-174, which keeps its certificate as history, with Doğa Özden
the packing’s finder, Evan Daniel’s n = 154 packing as Francisco Couzo improved it credited as the search’s seed and T-174’s
packing as the record it improves (the review’s F10). Both strong generators ran on the new witness ([the runs](../../../cases/regularized_drawings/think-xq4o-2026-11-11/README.md)), and the selection, measured against this witness’s drawing, draws Evan Daniel’s same-side view, from his driver’s run: light, uneven and near-axis squares, angle classes and hues 20, 43, 9, 25 and 19 against 4, 9, 0, 8 and 8, and full shared sides 405 and 477 against 513 and 515. Evan Daniel’s certified KKT solve lies 2.71 × 10⁻¹² below the side, about the certificate’s own contraction margin (2.58 × 10⁻¹²), held at row 3 as a register candidate and not admitted, as at 172, 199 and 270 (RV-3). The rigidity block, derived again on the new witness, stays not rigid: 72 of its 180 squares translate, against 7 of T-174’s.

## What Is Not Established

- **Human oversight.** One AI review is retained; no human oversight record.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **The lineage** the source states, beyond what the measurement above shows.

## Credit and Licence

The packing is Doğa Özden’s, found by his lab’s transplant search from Evan Daniel’s n = 154 packing as Francisco Couzo improved it;
the issue asks that the improvement be credited to Özden, the seed packing and the
current record to their holders as the registry lists them, and the local optimizer to
Evan Daniel. The case record credits Özden as the finder, the seed’s holders as the
search’s start and T-174’s holders as the record it improves (the review’s F10).
The issue says the search and its code were written and run by AI agents throughout and
that the checks were run by code that did not produce the packing; it says the issue and
repository were prepared and posted by his AI agent, and that Özden directed the work.
The source starts from this repository’s registry packings and makes its exact
coordinates with this repository’s promotion tool, so its lineage builds on this project.
The bibliography key is **[Özden s180 upper bound 2026-11-10]**.

The witness, the JSON, the decimal pose, the checker outputs, the README and the diff
image are published under CC BY 4.0, and `verifier/sqcheck.py` under the MIT licence,
copyright (c) 2026 Doğa Özden, as [source/LICENSE.md](source/LICENSE.md) states; it is
byte-identical to the `LICENSE.md` the lab added to its s299, s204 and s94 repositories
on 4 November 2026 and announced on #890
([comment](https://github.com/jlevy/squares/issues/890#issuecomment-6637821113)).
The diff image is pinned by digest only. The source carries Evan Daniel’s MIT notice as
`LICENSE-evand-square-packing.txt`, for his quench code and the certificates his
packings come from, byte-identical to the `LICENSE` the
[evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains, and
pinned against it.

## Commands

From `packing/`, with the project interpreter. The identity measurement reads the house
witness and its regularized view as they stood at main f54ad1048, before this adoption
replaced them, so it reproduces there; the contraction margins read the packets and
reproduce anywhere `devtools.contraction_margin` is:

```bash
python -m devtools.acquire_source ozden-s180-upper-bound-2026-11-10 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s180-upper-bound-2026-11-10 --check
python -m devtools.upper_bound_reports ozden-s180-upper-bound-2026-11-10 check-claims --write
python -m devtools.upper_bound_reports ozden-s180-upper-bound-2026-11-10 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ozden-s180-upper-bound-2026-11-10 check --replay
python -m devtools.upper_bound_reports ozden-s180-upper-bound-2026-11-10 sharp-controls
python -m devtools.measure_identity --n 180 'OZDEN=packet:ozden-s180-upper-bound-2026-11-10' \
  'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  'regularized=witness-corners:atlas/known-best/regularized/n-180-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-180.yaml' \
  --out resources/web/ozden-s180-upper-bound-2026-11-10/measure/identity.json
python -m devtools.contraction_margin --n 180 'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  --against 'ozden-944=packet:ozden-s180-upper-bound-2026-11-10' \
  --out resources/web/ozden-s180-upper-bound-2026-11-10/measure/contraction-n180.json
python -m devtools.contraction_margin --n 180 'ozden-944=packet:ozden-s180-upper-bound-2026-11-10' \
  --out resources/web/ozden-s180-upper-bound-2026-11-10/measure/contraction-n180-own.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
