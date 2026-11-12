# Doğa Özden’s s(269) Certificate at fdab2c0

This packet retains
[kenaznia-doga/s269-upper-bound-16899469076](https://github.com/kenaznia-doga/s269-upper-bound-16899469076/tree/fdab2c0073ea91701d0d8429663faa6e5c7f831f)
at `fdab2c0073ea91701d0d8429663faa6e5c7f831f` (committed 2026-11-11T23:34:47Z), the
repository’s one commit, which [issue #962](https://github.com/jlevy/squares/issues/962)
names 17 seconds later.
Doğa Özden’s AI agent, which uses the account kenaznia-doga, prepared and posted both on
his behalf, and six seconds after the issue it pointed to it from his earlier issue at
this count
([#947, comment](https://github.com/jlevy/squares/issues/947#issuecomment-6809799112)).

## What the Source Claims

- `n-269-candidate.yaml`, a `packing.squares:Witness/v2` file (corners, rational
  scalars, 269 squares), bounds s(269) by its exact side, a fraction whose denominator
  has 217 places and whose 16-place ceiling is 16.8994690758550466. #962 prints its
  12-place ceiling, 16.899469075856, and says it is 1.526e-03 below the record, T-290,
  the author’s own #947 certificate, which it calls a further improvement of that
  record. The issue and README also print the exact side as 16.8994690758550465, the side
  truncated at 16 places, 2.72 × 10⁻¹⁷ below it.
  It claims an upper bound only: no KKT, local-optimality, rigidity or global-optimality
  claim.
- The exact coordinates were made by this repository’s own `packing-witness promote
  --strategy robust-rational` at `0af33d85` from the lab’s decimal pose,
  `n-269-decimal-pose.yaml`, which the witness’s `source.path` names, with
  `center_dilation: '1'` and no dilation.
  The issue says the pair margins of about 2 × 10⁻¹³ are the decimal pose’s own, left by
  the final binary64 repair scaling of Evan Daniel’s quench (about 10⁻¹³ relative), that
  only the squares that set the left wall, the bottom wall and the side touch them
  exactly, and that other squares near a wall clear it by up to about 10⁻¹². Measured
  here, 11 squares touch a wall exactly: square 103 at the bottom, square 155 at the
  top, which sets the side, and nine squares, 158 and 160 to 167, that share the least x
  and so set the left wall.
  Of the other square–wall clearances, 25 are below 10⁻¹² and at most 1.53 × 10⁻¹⁵, and
  25 lie between 9.7 × 10⁻⁸ and 7.1 × 10⁻⁴.
- `n269-witness.json` is the same file as JSON. `packing-witness-verify.txt` is the
  author’s run of this repository’s `packing-witness verify` at `0af33d85` (VERIFIED,
  36,046 pairs); `sqcheck-output.txt` is the author’s run of `verifier/sqcheck.py`, an
  exact checker the source says was written separately from this repository’s code
  (VALID, exact rational, the exact side rounded up).
  The issue says the two share only the unit-square, wall and non-overlap definitions,
  that `packing-witness verify` is not independent of how the coordinates were rounded,
  and that `sqcheck.py` certified the decimal pose in interval arithmetic at its own
  side before promotion.
  Those statements are the author’s; no source program ran here.
- The issue says the packing was found by an AI-run band-design search, new for this
  filing, the one #954 and #960 described at 179 and 237: tilted squares from registry
  or own packings of the same family laid along the diagonal as a seed band; simulated
  annealing in a reduced model in which the tilted squares move freely and the
  axis-parallel squares sit on the two wall-anchored staircase lattices, present or
  absent, with the overlap of the squares that must be kept as energy; then a quench
  with Evan Daniel’s ALM+SLP code from
  [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT,
  at `bb4cc78e`). The band is built from tilted squares of three clusters: the second
  cluster of the registry’s n = 207 packing (`207b`), the cluster of the registry’s n =
  70 packing (`70a`; Ryan Xu, improved by Evan Daniel and PingYou Ltd) and the first
  cluster of the lab’s own n = 179 band packing of #954 (`179ha`), each reflected in the
  main diagonal of its box (symmetry 2; shifts (0, 0), (0, 0) and (3, 3)) and rotated to
  a lean of 2.55 degrees, 45 tilted squares at band parameter 0.899; annealed at that
  side (2 × 10⁷ moves, energy 0.0719) and quenched once to 16.899469084224, then kicked
  (sigma 0.0031) and quenched to 16.899469075879 18 seconds later in the same job, then
  kicked again (sigma 0.0296) and quenched, 3 seconds after that, to the filed side.
  The issue counts 46 tilted squares against the record’s 100, 16 of them at −42.88
  degrees, and says it is not one clean band.
  Against the registry packing, matched by assignment up to the square’s symmetries, it
  reports 262 of 269 centres beyond 1e-3, 124 beyond 0.05 (largest 1.456), 116 squares
  re-tilted beyond 1 degree (largest 44.77), and 46 squares tilted beyond 0.5 degree
  against the record’s 100.
- The issue describes the record, T-290, in two ways: in its claim paragraph as “built
  from Nate Chaoweeraprasit’s packing (itsnaka) improved by Evan Daniel and PingYou
  Ltd”, and in its lineage paragraph as found by transplanting Evan Daniel’s n = 304
  packing. The register records T-290 as the second: a strip cut of Evan Daniel’s 304,
  below T-174, Nate Chaoweeraprasit’s packing as Evan Daniel and PingYou Ltd improved
  it, which was the house before it.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the whole tree, 11 files: 7 retained under [source/](source/) and 4 pinned
by digest.

| File | Bytes |
| --- | --- |
| `LICENSE.md` | 1,484 |
| `README.md` | 7,213 |
| `n-269-candidate.yaml` | 611,228 |
| `n-269-decimal-pose.yaml` | 27,608, the decimal pose the witness was promoted from |
| `n269-witness.json` | 602,860, the same packing as JSON, which the reader holds equal to the YAML |
| `packing-witness-verify.txt` | 617 |
| `sqcheck-output.txt` | 101 |
| `LICENSE-evand-square-packing.txt` | 1,068, pinned against the identical copy of Evan Daniel’s MIT notice the [evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains |
| `records/n-269-candidate-diff.png` | 304,992, pinned by digest: a raster comparison that decides nothing |
| `verifier/README.md` | 3,441, pinned against the identical copy the [3 November s299 packet](../ozden-s299-upper-bound-2026-11-03/README.md) retains |
| `verifier/sqcheck.py` | 17,654, pinned against the identical copy the [9 November s232 packet](../ozden-s232-upper-bound-2026-11-09/README.md) retains, never executed here |

The SHA-256s the issue states for `n-269-candidate.yaml` and the README states for it
and for `n269-witness.json` are the files’.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is about 1.4 megabytes in a checkout and far less as Git stores it, so it is
kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `75cce00b6` on 12
November 2026):

- **269:** exact side 16.8994690758550466 rounded up at 16 places, below the case’s
  house (T-290, Doğa Özden’s own certificate of #947) by 1.526e-03, as the issue states,
  and below T-174, the house before it, by 2.045e-03. No register bound is pending
  adoption at 269.

## Report Order

The
[ledger of 12 November for this lane](../../../campaign/issue-intake/upper-bounds-962-20261112/README.md)
walks every report at 269 in the order it reached this repository, from a start frozen
at `main` `75cce00b6`, and records this packet’s claim at 269. The best public Kaggle
per-puzzle packing the issue quotes at 269, 16.901513582205 (kirilltym), is above this.
The issue also quotes, and states first, a side-only Kaggle leaderboard entry at 269,
16.889730079125 (team elegans, 5 November), 9.74e-3 below this side.
It is unpublished and states no packing, so it is no report and is recorded as context
only.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-290’s packing, T-174’s,
the house witness and the regularized view, and wrote
[measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **269:** no symmetry of the box pairs it one to one with T-290’s packing by nearest
  centres. The optimal assignment, under the best of the box’s eight symmetries, moves
  every square beyond 10⁻⁶, 230 beyond 10⁻³, 134 beyond 0.01 and 115 beyond 0.1 (largest
  1.12355), and turns 149 squares by more than 10⁻⁶ radians, by up to 44.77 degrees;
  aligned by box centres, 116 squares turn by more than a degree, as the issue says.
  Tilted beyond a degree: 45 here, 39.53 to 44.77 degrees from upright, 22 turned one
  way and 23 the other, with one more at 0.55 degrees, so 46 beyond half a degree, as
  the issue says, 16 of them within 0.01 degrees of −42.88; T-290’s 100, 18.70 to 36.11
  degrees, all turned one way.
  The house witness, as it stood before this adoption, measures the same, and its
  regularized view, a drawing of T-290’s packing at its side, the same but for 112
  squares beyond a tenth.
  So it is a new arrangement relative to T-290’s packing, not a further arrangement of
  it.
- **Against T-174**, the house before T-290, it is new as well: no symmetry pairs
  nearest centres one to one, and the optimal assignment moves 65 squares beyond a tenth
  (largest 0.928203); aligned by box centres, 70 squares turn by more than a degree.
  T-174 has 49 squares tilted beyond a degree, 33.99 to 44.87 degrees, 25 one way and 24
  the other.
- The issue’s own counts (262 of 269 beyond 10⁻³, 124 beyond 0.05, largest 1.456) are
  not those of the optimal assignment or of box-centred alignment, which give 230 and
  249 beyond 10⁻³ and a largest move of 1.12355 and 1.12358. All five of the issue’s
  counts, 116 re-tilted beyond a degree and the largest turn of 44.77 degrees among
  them, hold, as the review measured, with T-290 reflected left to right, set against
  the lower-right corner of the new box and paired by least summed move, one of the 80
  placements and assignments it tried; the issue names neither the symmetry nor the
  anchoring (F6).

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 216,276 pair decisions, 59.25 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 2.034e-13. `check --replay` decided the three jobs again.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
10⁻³⁰ past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)), with the
expected verdicts stated before it ran.
It lowered the side by the least far-wall clearance, closed the least-gap pair (squares
10 and 13) by its gap, and moved every square toward the nearer near wall by its least
clearance: both routes accepted each at contact with margin 0 and refused each past it.
It enlarged one square to its pair and one to its wall: both routes refused the first at
contact for its shape alone and accepted the second, square 103, which already touches
its wall and so grew by 0, at contact; both refused each 10⁻³⁰ past it for the overlap
or the wall as well.
Both refused a duplicated square.
All 11 were as stated in advance.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read the witness through the `witness-corners`
reader. The first route is the `packing-witness verify` the author ran on the same file,
so on that route the replay is reproduced with the producer’s code; the second shares no
verification code with it.
Neither is independent of this repository’s `packing-witness
promote`, which made the coordinates.
The source’s own `sqcheck.py` was not run.

## The Gain Against Padding

T-290’s certificate at 269, contracted uniformly about the origin to first contact and
boxed, loses 3.238 × 10⁻¹² of its side (1 − λ\* = 2.036 × 10⁻¹³, the binding pair
squares 119 and 202). The gain this certificate states, 1.526e-03, is 4.71 × 10⁸ times
that margin, so none of it is T-290’s padding; the owner’s open question about gains
inside a padding margin (RV-3, think-ruu2) does not reach it, and the entry is not held
at V0/C1 as T-285 and T-286 were.
T-174’s certificate has no padding to measure (1 − λ\* = 0, a pair already touching), as
T-290’s packet found.
This certificate’s own margin, measured the same way, is 3.234 × 10⁻¹² (1 − λ\* = 2.034
× 10⁻¹³, the binding pair squares 10 and 13, the least-gap pair); contracted, it would
be a square of side 16.89946907585181, which nobody reported and which is not registered
(RV-3). `devtools.contraction_margin` wrote the two receipts,
[measure/contraction-n269.json](measure/contraction-n269.json) and
[measure/contraction-n269-own.json](measure/contraction-n269-own.json), each contracted
packing decided on both maintained routes.

## The L Step

`devtools.l_step_scan`, with this side stood in for 269’s ceiling, finds the same L-step
and monotonicity consequences as on `main`: this bound carries to no other count
([measure/l-step-scan.json](measure/l-step-scan.json)).

## Stage 4 Review and Adoption

The stage 4 mathematical review of 12 November 2026
([review-2026-11-12-ozden-962.md](../../../../docs/project/reviews/review-2026-11-12-ozden-962.md)),
written in a separate lane (L117) blind to this one throughout, accepts the certificate
with 12 findings, all notes, none blocking, and scores it S3. Its clean-room checker
decides every square, wall and pair by separating axes in Python integers and by the
convex hull of vertices and edge crossings in GMP rationals, with 20 controls stated
before they ran, and accepts the same squares in the box of the claim’s own side,
16.899469075856, and refuses them in the box of its 12-place floor (F3). Of the 20
controls, 19 came out as stated; the twentieth, G2, refused the file as stated, but its
method B read the right wall of a square moved 13.48 beyond it as apart, a limit of the
review’s own checker that bears on no square of the certificate (F2). Its programs and
receipts are kept in the review-only directory beside this packet,
[ozden-s269-962-review-2026-11-12](../ozden-s269-962-review-2026-11-12/README.md).
Read against this packet’s receipts once both were done, its least pair margin is the
replay’s exactly, its contraction receipts for T-290 and for the certificate itself
equal [measure/contraction-n269.json](measure/contraction-n269.json) and
[measure/contraction-n269-own.json](measure/contraction-n269-own.json) in margin,
factor, binding pair and contracted side, and its identity measurement against T-290 and
T-174 equals [measure/identity.json](measure/identity.json) under nearest centres, the
optimal assignment and box-centred alignment, as do the tilt counts.

The review finds the issue’s arithmetic right (F4): the claim is the side’s 12-place
ceiling, the gain and the distance above the Kaggle entry are as printed, and “our exact
side 16.8994690758550465” is the side’s 16-place floor.
The pair margins are the pose’s own, 2.03 to 2.09 × 10⁻¹³ of the centres’ separation,
median 2.06 × 10⁻¹³, about twice “about 1e-13 relative” (F5). The issue’s lineage counts
hold with T-290 reflected left to right, set against the lower-right corner and paired
by least summed move (F6, above).
The claim paragraph’s “built from Nate Chaoweeraprasit’s packing” misdescribes T-290,
which the record and the issue’s own lineage paragraph give as a strip cut of Evan
Daniel’s 304 (F7). The certificate’s own squares, contracted by 1 − 2.034 × 10⁻¹³, are
accepted at side 16.89946907585181, a side only RV-3 could register, and it is not
registered (F8). The contact statement holds with eleven contacts, and square 140 clears
the right wall by 9.7 × 10⁻⁸, beyond “up to about 1e-12” (F12). The witness’s
`softschema.schema` names `witness.schema.yaml`, which resolves to no file in the
author’s repository, and its `certificate.replay` names the file but not where to run
it, as at #947 and #959; the adopted witness carries this repository’s own, and a
`sqpack` replay is the author’s first check run again (F11). The issue’s search for
competing claims is dated the minute it was opened, and the dating is consistent.

The issue names the registry’s 207 and 70 among the band’s sources; both witnesses come
from PingYou Ltd’s PR 574 algebraic supplement, a release with no licence file, kept
here in the derived-only form.
Whether a seed taken from them needs a notice of its own is the owner’s open decision on
`think-71uq` (F10; the review named `think-mdxq`, which closed on 4 November).
It is noted here, not decided.

Its six questions for the author, informational and holding nothing open:

1. The margins and the pose’s side both point to a repair scaling of about 2 × 10⁻¹³, as
   at #947 and #959. Was it that, rather than 10⁻¹³ (F5)?
2. The lineage counts reproduce with T-290 reflected left to right and set against the
   lower-right corner of the new box, under the assignment of least summed move.
   Is that the tool’s convention, and would the issue name it (F6)?
3. Would the author correct the claim paragraph’s “built from Nate Chaoweeraprasit’s
   packing (itsnaka) improved by Evan Daniel and PingYou Ltd”, since the record and the
   issue’s own lineage paragraph have T-290 from a strip cut of Evan Daniel’s 304 (F7)?
4. The squares, contracted uniformly by 1 − 2.034 × 10⁻¹³, are accepted exactly at side
   16.89946907585181. Would the lab promote with a contraction (`center_dilation` below
   1)? Whether the record registers a side inside the repair dilation is its owner’s
   question (RV-3, F8).
5. Will the band-design search and its seed band be published, and did `207b` and `70a`
   come from the registry’s witnesses, PingYou Ltd’s PR 574 release, or other published
   coordinates (F10)?
6. Would the author point `softschema.schema` at a file that resolves in his repository,
   and say in the replay line where to run it (F11)?

The case adopted the certificate as its house on 12 November 2026 under the house rule,
as T-296, in place of T-290, which keeps its certificate as history, with Doğa Özden the
packing’s finder; the band’s source packings credited as the search’s seed, PingYou
Ltd’s n = 207 packing, Ryan Xu’s n = 70 packing as Evan Daniel and PingYou Ltd improved
it, and his own n = 179 packing (T-291); Evan Daniel credited for the optimizer; and
T-290, his own packing from a strip cut of Evan Daniel’s 304, as the record it improves
(the review’s F9). Both strong generators ran on the new witness
([the runs](../../../cases/regularized_drawings/think-s418-2026-11-12/README.md)), and
the selection, measured against this witness’s drawing, draws grid-slack’s 1-degree
view: light, uneven and near-axis squares, angle classes and hues 17, 52, 29, 54 and 19
against 1, 3, 0, 24 and 19, and full shared sides 651 and 826 against 836 and 854. Evan
Daniel’s driver refused its same-side view; his certified KKT solve lies 3.39 × 10⁻¹²
below the side, 1.05 of the certificate’s own contraction margin (3.234 × 10⁻¹²), held
at row 3 as a register candidate and not admitted, as at 156, 172, 179, 180, 199, 268,
269 for T-290 and 270 (RV-3). The rigidity block, derived again on the new witness,
stays not rigid: 217 of its 269 squares translate, against 195 of T-290’s.

## What Is Not Established

- **Human oversight.** One AI review is retained; no human oversight record.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **The lineage** the source states, beyond what the measurement above shows.

## Credit and Licence

The packing is Doğa Özden’s, found by his lab’s band-design search from tilted squares
of three packings: the registry’s n = 207 packing, PingYou Ltd’s; the registry’s n = 70
packing, Ryan Xu’s, as Evan Daniel and PingYou Ltd improved it; and his own n = 179
packing of #954 (T-291). The case record credits Özden as the finder, the three
packings’ holders as the band’s sources, Evan Daniel for the local optimizer and T-290,
his own, as the record it improves (the review’s F9). The issue asks that the
improvement be credited to Özden, the band’s source packings and the current record to
their holders as the registry lists them, and the local optimizer to Evan Daniel.
The record at 269 before this adoption was T-290, Doğa Özden’s own packing from a strip
cut of Evan Daniel’s n = 304 packing.
The issue says the search and its code were written and run by AI agents throughout and
that the checks were run by code that did not produce the packing; it says the issue and
repository were prepared and posted by his AI agent, and that Özden directed the work.
The source starts from this repository’s registry packings and makes its exact
coordinates with this repository’s promotion tool, so its lineage builds on this
project. The bibliography key is **[Özden s269 issue 962 2026-11-11]**.

The witness, the JSON, the decimal pose, the checker outputs, the README and the diff
image are published under CC BY 4.0, and `verifier/sqcheck.py` under the MIT licence,
copyright (c) 2026 Doğa Özden, as [source/LICENSE.md](source/LICENSE.md) states; it is
byte-identical to the `LICENSE.md` the lab added to its s299, s204 and s94 repositories
on 4 November 2026 and announced on #890
([comment](https://github.com/jlevy/squares/issues/890#issuecomment-6637821113)). The
diff image is pinned by digest only.
The source carries Evan Daniel’s MIT notice as `LICENSE-evand-square-packing.txt`, for
his quench code, byte-identical to the `LICENSE` the
[evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains, and
pinned against it.

## Commands

From `packing/`, with the project interpreter.
The identity measurement reads the house witness and its regularized view as they stood
at main 75cce00b6, before this adoption replaced them, so it reproduces there; the
contraction margins read the packets and reproduce anywhere
`devtools.contraction_margin` is:

```bash
python -m devtools.acquire_source ozden-s269-issue962-2026-11-11 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s269-issue962-2026-11-11 --check
python -m devtools.upper_bound_reports ozden-s269-issue962-2026-11-11 check-claims --write
python -m devtools.upper_bound_reports ozden-s269-issue962-2026-11-11 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ozden-s269-issue962-2026-11-11 check --replay
python -m devtools.upper_bound_reports ozden-s269-issue962-2026-11-11 sharp-controls
python -m devtools.measure_identity --n 269 'OZDEN=packet:ozden-s269-issue962-2026-11-11' \
  'T-290=packet:ozden-s269-upper-bound-2026-11-11' 'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-269-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-269.yaml' \
  --out resources/web/ozden-s269-issue962-2026-11-11/measure/identity.json
python -m devtools.contraction_margin --n 269 'T-290=packet:ozden-s269-upper-bound-2026-11-11' \
  --against 'ozden-962=packet:ozden-s269-issue962-2026-11-11' \
  --out resources/web/ozden-s269-issue962-2026-11-11/measure/contraction-n269.json
python -m devtools.contraction_margin --n 269 'ozden-962=packet:ozden-s269-issue962-2026-11-11' \
  --out resources/web/ozden-s269-issue962-2026-11-11/measure/contraction-n269-own.json
python -m devtools.l_step_scan --with 269=S269 \
  --out resources/web/ozden-s269-issue962-2026-11-11/measure/l-step-scan.json
```

In the last command `S269` is the `exact_side` in the packet’s claim record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
