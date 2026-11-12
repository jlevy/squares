# Doğa Özden’s s(237) Certificate at 13c4b23

This packet retains
[kenaznia-doga/s237-upper-bound](https://github.com/kenaznia-doga/s237-upper-bound/tree/13c4b231bb16437a6ee3751e75113ef95113b235)
at `13c4b231bb16437a6ee3751e75113ef95113b235` (committed 2026-11-11T21:37:37Z), the
repository’s one commit, which [issue #960](https://github.com/jlevy/squares/issues/960)
names 13 seconds later. Doğa Özden’s AI agent, which uses the account kenaznia-doga,
prepared and posted both on his behalf.

## What the Source Claims

- `n-237-candidate.yaml`, a `packing.squares:Witness/v2` file (corners, rational scalars,
  237 squares), bounds s(237) by its exact side, a fraction whose denominator has 186
  places and whose 16-place ceiling is 15.8938055805725742. #960 prints its 12-place
  ceiling, 15.893805580573, and says it is 8.798e-03 below the record. It names that
  record T-189, Francisco Couzo’s issue-607 certificate, but prints the side of T-190, his
  15 October certificate of the same packing, 2.40e-11 below T-189, which is the case’s
  house; the gain against T-190 is 8.798e-03, as the issue states. The issue also prints
  the exact side as 15.8938055805725735, 6.55 × 10⁻¹⁶ below it: the side’s binary64
  rounding printed to 16 places, as the review finds, which bounds nothing (F5). It claims
  an upper bound only: no KKT, local-optimality, rigidity or global-optimality claim.
- The exact coordinates were made by this repository’s own `packing-witness promote
  --strategy robust-rational` at `c8448724` from the lab’s decimal pose,
  `n-237-decimal-pose.yaml`, which the witness’s `source.path` names, with
  `center_dilation: '1'` and no dilation. The issue says the pair margins of about
  2 × 10⁻¹³ are the decimal pose’s own, left by the final binary64 repair scaling of
  Evan Daniel’s quench (about 10⁻¹³ relative), that only the squares that set the left
  wall, the bottom wall and the side touch them exactly, and that other squares near a wall
  clear it by up to about 10⁻¹². The decimal pose’s side is 2.07 × 10⁻¹³ above the
  certificate’s. Measured by the review, exactly three squares touch a wall (67 at the
  bottom, 152 at the left and 236 at the top), as the issue says; the other 19
  square–wall clearances below 10⁻¹² are at most 1.20 × 10⁻¹³, and 35 lie between
  1.91 × 10⁻⁵ and 6.40 × 10⁻⁴. The certificate is the decimal pose translated by about
  1.1 × 10⁻¹³ toward the corner, every centre equal to the pose’s to 4.7 × 10⁻³⁸, so the
  pair margins are the pose’s own, as the issue says; they lie between 2.01 and
  5.70 × 10⁻¹³ of the centres’ separation along the binding axis, median 2.38 × 10⁻¹³,
  about twice the issue’s “about 1e-13 relative” (F7).
- `n237-witness.json` is the same file as JSON. `packing-witness-verify.txt` is the
  author’s run of this repository’s `packing-witness verify` at `c8448724` (VERIFIED,
  27,966 pairs); `sqcheck-output.txt` is the author’s run of `verifier/sqcheck.py`, an
  exact checker the source says was written separately from this repository’s code
  (VALID, exact rational, the exact side rounded up). The issue says the two share only
  the unit-square, wall and non-overlap definitions, that `packing-witness verify` is not
  independent of how the coordinates were rounded, and that `sqcheck.py` certified the
  decimal pose in interval arithmetic at its own side before promotion.
  Those statements are the author’s; no source program ran here.
- The issue says the packing was found by an AI-run band-design search, the one #954
  described at 179: tilted squares from a registry packing of the same family laid along
  the diagonal as a seed band; simulated annealing in a reduced model in which the tilted
  squares move freely and the axis-parallel squares sit on the two wall-anchored staircase
  lattices, present or absent, with the overlap of the squares that must be kept as
  energy; then a quench with Evan Daniel’s ALM+SLP code from
  [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT,
  at `bb4cc78e`). The band is built from the tilted squares of the registry’s n = 70
  packing (Ryan Xu, improved by Evan Daniel and PingYou Ltd; side 8.880960371555579595):
  two copies of that packing’s cluster of tilted squares, one reflected in the
  anti-diagonal of its box and placed at the lower left (symmetry 3, shift (0, 0)) and one
  reflected in the main diagonal and shifted by (7, 7) (symmetry 2), both rotated rigidly
  to a lean of 2.0 degrees, which the issue counts as 42 tilted squares; annealed at side
  15.888 (3 × 10⁶ moves, energy 0.113) and quenched to 15.893805580580, then kicked
  (sigma 0.0196) and quenched again, 18 seconds later in the same job, to the filed side.
  The issue describes one straight band of tilted squares from corner to corner, 36 of its
  43 at 42.215 degrees, where the record’s band is curved with 49 tilted squares. Against
  the registry packing, matched by assignment up to the square’s symmetries, it reports
  236 of 237 centres beyond 1e-3, 78 beyond 0.05 (largest 1.202), 73 squares re-tilted
  beyond 1 degree (largest 43.77), and 43 squares tilted beyond 0.5 degree against the
  record’s 49.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the whole tree, 11 files: 7 retained under
[source/](source/) and 4 pinned by digest.

| File | Bytes |
| --- | --- |
| `LICENSE.md` | 1,484 |
| `README.md` | 6,922 |
| `n-237-candidate.yaml` | 695,934 |
| `n-237-decimal-pose.yaml` | 25,800, the decimal pose the witness was promoted from |
| `n237-witness.json` | 688,628, the same packing as JSON, which the reader holds equal to the YAML |
| `packing-witness-verify.txt` | 555 |
| `sqcheck-output.txt` | 101 |
| `LICENSE-evand-square-packing.txt` | 1,068, pinned against the identical copy of Evan Daniel’s MIT notice the [evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains |
| `records/n-237-candidate-diff.png` | 260,280, pinned by digest: a raster comparison that decides nothing |
| `verifier/README.md` | 3,441, pinned against the identical copy the [3 November s299 packet](../ozden-s299-upper-bound-2026-11-03/README.md) retains |
| `verifier/sqcheck.py` | 17,654, pinned against the identical copy the [9 November s232 packet](../ozden-s232-upper-bound-2026-11-09/README.md) retains, never executed here |

The SHA-256s the issue states for `n-237-candidate.yaml` and the README states for it and
for `n237-witness.json` are the files’.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is about 1.4 megabytes in a checkout and far less as Git stores it, so it is
kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `b5b12c206` on 11 November
2026):

- **237:** exact side 15.8938055805725742 rounded up at 16 places, below the case’s house
  (T-190, Francisco Couzo’s certificate of Nate Chaoweeraprasit’s packing, improved by
  Couzo and Mishapolk) by 8.798e-03, as the issue states. It is also below T-253,
  Mykhailo Polkovskyi’s sub-print re-certification of T-190’s packing, 1.59 × 10⁻¹⁹ below
  it and pending adoption (V0/C1, held for think-ikku).

## Report Order

The [ledger of 11 November for this lane](../../../campaign/issue-intake/upper-bounds-960-20261111/README.md)
walks every report at 237 in the order it reached this repository, from a start frozen at
`main` `b5b12c206`, and records this packet’s claim at 237.
The best public Kaggle per-puzzle packing the issue quotes at 237, 15.902603638274
(kirilltym), is above this. The issue also quotes, and states first, a side-only Kaggle
leaderboard entry at 237, 15.893805585209 (team elegans, 5 November), 4.64e-9 above this
side. It is unpublished and states no packing, so it is no report and is recorded as
context only.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-190’s packing, T-189’s, the
house witness and the regularized view, and wrote
[measure/identity.json](measure/identity.json). A measurement for credit; it decides
nothing.

- **237:** no symmetry of the box pairs it one to one with T-190’s packing by nearest
  centres. The optimal assignment, under the best of the box’s eight symmetries, moves
  every square beyond 10⁻³, 111 beyond 0.01 and 72 beyond 0.1 (largest 0.924884), and
  turns 154 squares by more than 10⁻⁶ radians, by up to 43.77 degrees; aligned by box
  centres, 73 squares turn by more than a degree, as the issue says. Tilted beyond a
  degree: 42 here, 42.19 to 44.46 degrees from upright, 38 turned one way and 4 the other,
  with one more at 0.83 degrees, so 43 beyond half a degree, as the issue says; T-190’s
  49, 1.14 to 43.62 degrees. T-189’s packing, T-190’s house witness and its regularized
  view, as they stood before this adoption, measure the same. So it is a new arrangement
  relative to T-190’s packing, not a further arrangement of it. Anchored at the lower-left
  corner or at the centres, every square moves beyond 10⁻³, since the sides differ by
  8.8 × 10⁻³; the issue’s 236 of 237, 78 beyond 0.05 and largest move 1.202 hold, as the
  review measured, with the house turned a half turn, set against the upper-right corner
  of the new box and paired by least summed move, a convention the issue does not name
  (F8). The review finds the band straight, its centres closer to their line than the
  house’s (standard deviation 0.70 against 1.28), with 35 of its tilted squares within
  0.004 degrees of 42.215 and a 36th 0.024 degrees away, so “36 of its 43” holds with
  “share” read loosely.
- **The seed.** The review built the seed the issue states. The first copy of the 70
  band, reflected in the anti-diagonal of its box at the origin, matches: turned by 0.39
  degrees and moved by under 0.05, 19 of its 20 squares lie within 0.1 of a tilted square
  here. The second, reflected in the main diagonal and shifted by (7, 7), does not lie
  where stated: no tilted square here lies within 0.25 of it until it is turned by −1.20
  degrees about the origin and shifted by (−0.45, 0.03), after which 9 of its 20 lie
  within 0.1 and 18 within 0.25. Two copies of the 70 band hold 40 tilted squares, not
  the 42 the issue counts (F9).

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 167,796 pair decisions, 68.10 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 2.04e-13. `check --replay` decided the three jobs again.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
10⁻³⁰ past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)), with the
expected verdicts stated before it ran. It lowered the side by the least far-wall
clearance, closed the least-gap pair (squares 19 and 20) by its gap, and moved every
square toward the nearer near wall by its least clearance: both routes accepted each at
contact with margin 0 and refused each past it.
It enlarged one square to its pair and one to its wall: both routes refused the first at
contact for its shape alone and accepted the second, square 67, which already touches its
wall and so grew by 0, at contact; both refused each 10⁻³⁰ past it for the overlap or the
wall as well. Both refused a duplicated square. All 11 were as stated in advance.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read the witness through the `witness-corners`
reader. The first route is the `packing-witness verify` the author ran on the same file,
so on that route the replay is reproduced with the producer’s code; the second shares no
verification code with it. Neither is independent of this repository’s `packing-witness
promote`, which made the coordinates. The source’s own `sqcheck.py` was not run.

## The Gain Against Padding

T-190’s certificate at 237, contracted uniformly about the origin to first contact and
boxed, loses 1.59 × 10⁻¹⁹ of its side (1 − λ\* = 1.0 × 10⁻²⁰, the binding pair squares 54
and 55). T-189’s, measured the same way, loses 2.39 × 10⁻¹¹ (1 − λ\* = 1.60 × 10⁻¹², the
binding pair squares 74 and 103). The gain this certificate states, 8.798e-03, is
5.5 × 10¹⁶ times T-190’s margin and 3.7 × 10⁸ times T-189’s, so none of it is either
certificate’s padding; the owner’s open question about gains inside a padding margin
(RV-3, think-ruu2) does not reach it, and the entry is not held at V0/C1 as T-285 and
T-286 were. T-253 lies below T-190 by the size of T-190’s padding, as its review found.
This certificate’s own margin, measured the same way, is 2.985e-12 (1 − λ\* =
2.006849e-13, the binding pair squares 36 and 140).
`devtools.contraction_margin` wrote the three receipts,
[measure/contraction-n237.json](measure/contraction-n237.json),
[measure/contraction-n237-t189.json](measure/contraction-n237-t189.json) and
[measure/contraction-n237-own.json](measure/contraction-n237-own.json), each contracted
packing decided on both maintained routes.

## The L Step

`devtools.l_step_scan`, with this side stood in for 237’s ceiling, finds the same L-step
and monotonicity consequences as on `main`: this bound carries to no other count
([measure/l-step-scan.json](measure/l-step-scan.json)).

## Stage 4 Review and Adoption

The stage 4 mathematical review of 11 November 2026
([review-2026-11-11-ozden-960.md](../../../../docs/project/reviews/review-2026-11-11-ozden-960.md)),
written in a separate lane (L109) blind to this one throughout, accepts the certificate
with findings, one minor for the author (F5) and the rest notes, none blocking, and scores
it S3. Its clean-room checker decides every square, wall and pair by separating axes in
`Fraction` and by exact clipped areas in GMP rationals, with 17 controls stated before
they ran, and accepts the same squares in the box of the claim’s own side,
15.893805580573 (F3); its programs and receipts are kept in the review-only directory
beside this packet,
[ozden-s237-review-2026-11-11](../ozden-s237-review-2026-11-11/README.md).
Read against this packet’s receipts once both were done, its least pair margin is the
replay’s exactly, its contraction receipts for T-190 and T-189 equal
[measure/contraction-n237.json](measure/contraction-n237.json) and
[measure/contraction-n237-t189.json](measure/contraction-n237-t189.json) in margin,
factor and binding pair, and its identity measurement against T-190 and T-189 equals
[measure/identity.json](measure/identity.json) under nearest centres, the optimal
assignment and box-centred alignment.

The review corrects the record’s id: the issue names T-189, but the value and fraction it
quotes are T-190’s, the house since 16 October 2026 (F6). The issue dates its search for
competing reports 13:50 PST, which is 21:50Z, twelve minutes after it was opened at
21:37:50Z; either the body was edited or the time is misstated, and nothing in the bound
depends on it (F12). The witness’s `softschema.schema` names `witness.schema.yaml`, which
resolves to no file in the author’s repository, and its `certificate.replay` names the
file but not where to run it, unlike the README’s rerun (F11); the adopted witness carries
this repository’s own. Those are notes for the author.

The issue names the registry’s 70 as the band’s source; that witness comes from PingYou
Ltd’s PR 574 algebraic supplement, a release with no licence file, kept here in the
derived-only form. Whether a seed taken from it needs a notice of its own is the owner’s
open decision on `think-71uq` (F10; the review named `think-mdxq`, which closed on 4
November). It is noted here, not decided.

Its questions for the author, informational and holding nothing open:

1. Was the final repair scaling about 2 × 10⁻¹³ rather than 10⁻¹³, since the margins are
   2.01 to 5.70 × 10⁻¹³ of the centres’ separation, median 2.38 × 10⁻¹³ (F7)?
2. Do the lineage counts use the house turned a half turn, set against the upper-right
   corner of the new box and paired by least summed move, and would the issue name that
   convention (F8)?
3. About which point were the copies “rigidly rotated to a lean of 2.0°”, and what does
   the lean measure, since the second copy as stated lies more than 0.25 from every new
   tilted square (F9)?
4. Two copies of the 70 band hold 40 tilted squares: where do the other two of the “42
   tilted squares at band parameter 2.0” come from (F9)?
5. Did the seed take the 70 band from the registry’s witness (PingYou Ltd’s algebraic
   certificate) or from Ryan Xu’s or Evan Daniel’s published coordinates?
6. Would the author correct the record’s id to T-190, and print the exact side as its
   16-place ceiling, 15.8938055805725742, rather than the binary64 value
   15.8938055805725735 (F5, F6)?
7. Was the body edited after it was opened, or is the search time of 13:50 PST
   misstated (F12)?
8. Will the band-design search and its seeds be published, and which replay is intended,
   `certificate.replay` or the README’s rerun, and from which directory (F11)?

The case adopted the certificate as its house on 12 November 2026 under the house rule,
as T-295, in place of T-190, which keeps its certificate as history, with Doğa Özden the
packing’s finder, two copies of the band of Ryan Xu’s n = 70 packing, as Evan Daniel and
PingYou Ltd improved it, credited as the search’s seed, and T-190’s packing, Nate
Chaoweeraprasit’s as Francisco Couzo and Mishapolk improved it, as the record it improves
(the review’s F10). Both strong generators ran on the new witness
([the runs](../../../cases/regularized_drawings/think-my76-2026-11-11/README.md)), and the
selection, measured against this witness’s drawing, draws Evan Daniel’s same-side view:
light, uneven and near-axis squares, angle classes and hues 33, 68, 68, 75 and 19 against
0, 0, 0, 2 and 2, and full shared sides 331 and 721 against 788 and 788. His certified KKT
solve lies 3.44 × 10⁻¹² below the side, 1.15 of the certificate’s own contraction margin
(2.985 × 10⁻¹²), held at row 3 as a register candidate and not admitted, as at 156, 172,
179, 180, 199, 268, 269 and 270 (RV-3). The rigidity block, derived again on the new
witness, stays not rigid: 206 of its 237 squares translate, against 21 of T-190’s.

## What Is Not Established

- **Human oversight.** One AI review is retained; no human oversight record.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **The lineage** the source states, beyond what the measurement above shows.

## Credit and Licence

The packing is Doğa Özden’s, found by his lab’s band-design search from two copies of the
tilted squares of the registry’s n = 70 packing, Ryan Xu’s, as Evan Daniel and PingYou Ltd
improved it. The case record credits Özden as the finder, the 70 packing’s holders as the
band’s source and T-190’s holders as the record it improves (the review’s F10). The issue
asks that the improvement be credited to Özden, the band’s source packing and
the current record to their holders as the registry lists them, and the local optimizer
to Evan Daniel. The record at 237 is T-190: Nate Chaoweeraprasit’s packing (itsnaka),
improved by Francisco Couzo and Mishapolk (Mykhailo Polkovskyi). The issue says the search
and its code were written and run by AI agents throughout and that the checks were run by
code that did not produce the packing; it says the issue and repository were prepared and
posted by his AI agent, and that Özden directed the work. The source starts from this
repository’s registry packings and makes its exact coordinates with this repository’s
promotion tool, so its lineage builds on this project. The bibliography key is
**[Özden s237 upper bound 2026-11-11]**.

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
witness and its regularized view as they stood at main b5b12c206, before this adoption
replaced them, so it reproduces there; the contraction margins read the packets and
reproduce anywhere `devtools.contraction_margin` is:

```bash
python -m devtools.acquire_source ozden-s237-upper-bound-2026-11-11 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s237-upper-bound-2026-11-11 --check
python -m devtools.upper_bound_reports ozden-s237-upper-bound-2026-11-11 check-claims --write
python -m devtools.upper_bound_reports ozden-s237-upper-bound-2026-11-11 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ozden-s237-upper-bound-2026-11-11 check --replay
python -m devtools.upper_bound_reports ozden-s237-upper-bound-2026-11-11 sharp-controls
python -m devtools.measure_identity --n 237 'OZDEN=packet:ozden-s237-upper-bound-2026-11-11' \
  'T-190=packet:couzo-n237-2026-10-15' 'T-189=packet:couzo-certificates-2026-10-14' \
  'regularized=witness-corners:atlas/known-best/regularized/n-237-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-237.yaml' \
  --out resources/web/ozden-s237-upper-bound-2026-11-11/measure/identity.json
python -m devtools.contraction_margin --n 237 'T-190=packet:couzo-n237-2026-10-15' \
  --against 'ozden-960=packet:ozden-s237-upper-bound-2026-11-11' \
  --out resources/web/ozden-s237-upper-bound-2026-11-11/measure/contraction-n237.json
python -m devtools.contraction_margin --n 237 'T-189=packet:couzo-certificates-2026-10-14' \
  --against 'ozden-960=packet:ozden-s237-upper-bound-2026-11-11' \
  --out resources/web/ozden-s237-upper-bound-2026-11-11/measure/contraction-n237-t189.json
python -m devtools.contraction_margin --n 237 'ozden-960=packet:ozden-s237-upper-bound-2026-11-11' \
  --out resources/web/ozden-s237-upper-bound-2026-11-11/measure/contraction-n237-own.json
python -m devtools.l_step_scan --with 237=S237 \
  --out resources/web/ozden-s237-upper-bound-2026-11-11/measure/l-step-scan.json
```

In the last command `S237` is the `exact_side` in the packet’s claim record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
