# Doğa Özden’s Second s(179) Certificate at 6ab3cfe

This packet retains
[kenaznia-doga/s179-upper-bound-13880960371](https://github.com/kenaznia-doga/s179-upper-bound-13880960371/tree/6ab3cfe60db4d081092bed3b6bbb44c76b067230)
at `6ab3cfe60db4d081092bed3b6bbb44c76b067230` (committed 2026-11-11T21:18:12Z), the
repository’s one commit, which [issue #959](https://github.com/jlevy/squares/issues/959)
names 12 seconds later. Doğa Özden’s AI agent, which uses the account kenaznia-doga,
prepared and posted both on his behalf. Five seconds after the issue, at 21:18:29Z, the
same account commented on #954
([issuecomment-6807260149](https://github.com/jlevy/squares/issues/954#issuecomment-6807260149))
that #959 supersedes it, and asked that #959 be adopted in place of #954. #954 is T-291,
the house at 179 from 11 November 2026 until this certificate’s adoption on 12 November,
retained in the
[ozden-s179-upper-bound-2026-11-11](../ozden-s179-upper-bound-2026-11-11/README.md)
packet; it stays a verified bound.

## What the Source Claims

- `n-179-candidate.yaml`, a `packing.squares:Witness/v2` file (corners, rational scalars,
  179 squares), bounds s(179) by its exact side, a fraction whose denominator has 219
  places and whose 16-place ceiling is 13.8809603715582251. #959 prints its 12-place
  ceiling, 13.880960371559, and says it is 2.835e-03 below T-174 (Nate Chaoweeraprasit’s
  packing, improved by Siddharth Gupta and PingYou Ltd) and 4.068e-4 below the author’s
  own #954, from the same method on a later batch. It claims an upper bound only: no KKT,
  local-optimality, rigidity or global-optimality claim.
- The exact coordinates were made by this repository’s own `packing-witness promote
  --strategy robust-rational` at `c8448724` from the lab’s decimal pose,
  `n-179-decimal-pose.yaml`, which the witness’s `source.path` names, with
  `center_dilation: '1'` and no dilation. The issue says the pair margins of about
  2 × 10⁻¹³ are the decimal pose’s own, left by the final binary64 repair scaling of Evan
  Daniel’s quench, that only the squares that set the left wall, the bottom wall and the
  side touch them exactly, and that other squares near a wall clear it by up to about
  10⁻¹².
- `n179-witness.json` is the same file as JSON. `packing-witness-verify.txt` is the
  author’s run of this repository’s `packing-witness verify` at `c8448724` (VERIFIED,
  15,931 pairs); `sqcheck-output.txt` is the author’s run of `verifier/sqcheck.py`, an
  exact checker the source says was written separately from this repository’s code
  (VALID, exact rational, the exact side rounded up). Those statements are the author’s;
  no source program ran here.
- The issue says the packing came from a later batch of #954’s band-design scan: the
  tilted squares of the registry’s n = 70 packing (Ryan Xu, improved by Evan Daniel and
  PingYou Ltd; side 8.880960371555579595), a two-row band of 20 squares at −40.7505
  degrees, laid where x + y ≤ 16 with a copy shifted by (5, 5) where x + y > 16, 35
  tilted squares; mutated (band parameter 4.4245 where #954’s seed has 4.2495), annealed
  at side 13.88105 in a reduced model with the axis-parallel squares on the two
  wall-anchored staircase lattices, then quenched once with Evan Daniel’s ALM+SLP code
  ([evand/square-packing](https://github.com/evand/square-packing) `search/packer`, MIT,
  at `bb4cc78e`). Two further jobs of the batch reach the same side, to 1.5e-13, one from
  a different band (`179ha`/`207a`, shifted by (−1, −1)). It says the side is 2.64e-12
  above side(70) + 5 = 13.880960371555579595, and that the lab has not shown the packing
  is that construction.
- Against T-174, matched by assignment up to the square’s symmetries, the issue reports
  143 of 179 centres beyond 1e-3, 48 beyond 0.05 (largest 0.889), 43 squares re-tilted
  beyond 1 degree (largest 44.36), and 36 squares tilted beyond 0.5 degree against the
  record’s 35. It does not measure the packing against #954’s.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the whole tree, 11 files: 7 retained under
[source/](source/) and 4 pinned by digest.

| File | Bytes |
| --- | --- |
| `LICENSE.md` | 1,484, byte-identical to the copy the 954 packet retains |
| `README.md` | 7,072 |
| `n-179-candidate.yaml` | 533,889 |
| `n-179-decimal-pose.yaml` | 19,394, the decimal pose the witness was promoted from |
| `n179-witness.json` | 528,381, the same packing as JSON, which the reader holds equal to the YAML |
| `packing-witness-verify.txt` | 621 |
| `sqcheck-output.txt` | 101 |
| `LICENSE-evand-square-packing.txt` | 1,068, pinned against the identical copy of Evan Daniel’s MIT notice the [evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains |
| `records/n-179-candidate-diff.png` | 237,546, pinned by digest: a raster comparison that decides nothing |
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
(`devtools.upper_bound_reports check-claims`, read from `main` `b5b12c206` on 11 November
2026):

- **179:** exact side 13.8809603715582251 rounded up at 16 places, below the case’s house
  (T-291, the author’s own #954, adopted that day) by 4.068e-04. No register bound is
  pending adoption at 179. It is 2.835e-03 below T-174, the house before T-291, as the
  issue states.

## Report Order

The [ledger of 11 November for this lane](../../../campaign/issue-intake/upper-bounds-959-20261111/README.md)
walks every report at 179 in the order it reached this repository, from a start frozen at
`main` `b5b12c206`, and records this packet’s claim at 179.
The best public Kaggle per-puzzle packing the issue quotes at 179, 13.883795490524
(kirilltym), is above this. The issue also quotes, and states first, a side-only Kaggle
leaderboard entry at 179, 13.880960371556 (team Nevska, 7 November), 2.2e-12 below this
side, which the stage 4 review of #954 found to be exactly the registry’s s(70) + 5 at 12
places. It is unpublished and states no packing, so it is no report and is recorded as
context only.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-291’s packing, T-174’s,
the house witness and its regularized view, and wrote
[measure/identity.json](measure/identity.json). A measurement for credit; it decides
nothing.

- **Against T-291:** nearest centres pair the two one to one under the identity of the
  box. The optimal assignment moves 3 squares beyond 0.1, 31 beyond 0.01 and 85 beyond
  10⁻³ (largest 0.218429) and turns 44 squares by more than 10⁻⁶ radians, by up to 27.79
  degrees; with the boxes centred, 5 turn by more than a degree. Tilted beyond a degree:
  35 here, 37.7 to 40.75 degrees from upright, all turned the same way; T-291’s 36, 27.3
  to 41.4 degrees. The house witness and the regularized view, as they stood at
  `b5b12c206`, measure the same. So it is a further arrangement of T-291’s packing, by
  the same finder, not a new one.
- **Against T-174:** no symmetry pairs it one to one; the optimal assignment moves 46
  squares beyond 0.1 (largest 0.885863), and with the boxes centred 43 turn by more than a
  degree and the largest move is 0.886996, as the issue’s 43 and 0.889 say.

## The 70 and s(70) + 5

`devtools.measure_core` placed the registry’s n = 70 packing (Ryan Xu, improved by Evan
Daniel and PingYou Ltd; the house witness `W-known-best-n070`, a number-field witness
projected at 50 digits) in this packing’s box, and wrote
[measure/core-n070.json](measure/core-n070.json). A measurement for credit; it decides
nothing.

- **The side.** This side less s(70) is 5 + 2.645427e-12, so it lies 2.645e-12 above
  s(70) + 5, 1.906e-13 of itself, as the issue says. That is about the certificate’s own
  padding: contracted uniformly to first contact (below), it loses 2.566e-12 and lands
  7.9e-14 above s(70) + 5.
- **Not a core and a border.** A border of unit squares five wide round the 70, by five L
  steps, holds 70 + 105 = 175 squares at s(70) + 5, four short of 179. Set flush in any
  corner of the box under any of the eight symmetries, the 70 meets at most 48 of its 70
  squares within 10⁻⁹ (upper right, identity) and 64 within 0.1; never all 70.
- **A spliced band.** Laid along the main diagonal at shifts (0, 0) to (5, 5) under the
  identity of the 70 box, the 70 lies within 10⁻⁹ of 99 of this packing’s 179 squares,
  and of 15 of its 35 tilted ones, 7 at (0, 0) and 8 at (5, 5); 29 of the 35 lie within
  0.05. Under each of the other seven symmetries no tilted square lies within 0.01. So
  the packing keeps both ends of the 70’s band, to 10⁻⁹, where the issue’s seed puts
  them, with the band between them re-laid, and its side is s(70) + 5 but for its
  padding. For credit: it is not the 70 with a border, a construction the 70’s holders
  would be credited with, but a band the lab re-laid from the 70’s, as T-291’s is, now
  measured to keep the 70’s band ends exactly in place. Whether s(179) ≤ s(70) + 5 holds
  exactly, by a construction from the 70’s exact coordinates, is not shown here.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 95,586 pair decisions, 39.82 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 1.99e-13. `check --replay` decided the three jobs again.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
10⁻³⁰ past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)), with the
expected verdicts stated before it ran (the lane’s plan, SHA-256
`28ab9fb229aa190a30bfb2cd093cec9ecc0e71958797242e7bf4a657de45935b`, 22:23:56Z). It
lowered the side by the least far-wall clearance, 0, closed the least-gap pair (squares
104 and 105) by its gap, 1.99e-13, and moved every square toward the nearer near wall by
its least clearance, 0: both routes accepted each at contact with margin 0 and refused
each past it. It enlarged one square to its pair and one to its wall: both routes refused
the first at contact for its shape alone and accepted the second, square 67, which
already touches its wall and so grew by 0, at contact; both refused each 10⁻³⁰ past it
for the overlap or the wall as well. Both refused a duplicated square. All 11 rows are as
the plan states.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read the witness through the `witness-corners`
reader. The first route is the `packing-witness verify` the author ran on the same file,
so on that route the replay is reproduced with the producer’s code; the second shares no
verification code with it. Neither is independent of this repository’s `packing-witness
promote`, which made the coordinates. The source’s own `sqcheck.py` was not run.

## The Gain Against Padding

T-291’s certificate at 179, contracted uniformly about the origin to first contact and
boxed, loses 2.616e-12 of its side (1 − λ\* = 2.030834e-13, squares 14 and 15 the
binding pair). The gain this certificate states over it, 4.068e-04, is 1.555 × 10⁸ times
that margin, so none of it is T-291’s padding, and the owner’s open question about gains
inside a padding margin (RV-3, think-ruu2) does not reach it: the entry is not held at
V0/C1. This certificate’s own margin, measured the same way, is 2.566e-12 (1 − λ\* =
1.992233e-13, the binding pair the least-gap pair of the replay, squares 104 and 105).
`devtools.contraction_margin` wrote both receipts,
[measure/contraction-n179.json](measure/contraction-n179.json) and
[measure/contraction-n179-own.json](measure/contraction-n179-own.json), each contracted
packing decided on both maintained routes.

## The L Step

`devtools.l_step_scan`, with this side stood in for 179’s ceiling, finds the same L-step
and monotonicity consequences as on `main`: this bound carries to no other count
([measure/l-step-scan.json](measure/l-step-scan.json)).

## Stage 4 Review and Adoption

The stage 4 mathematical review of 11 November 2026,
[review-2026-11-12-ozden-959.md](../../../../docs/project/reviews/review-2026-11-12-ozden-959.md)
(lane L108), was written in a separate lane blind to this one until its findings were
frozen, and keeps its programs and receipts in the review-only directory
[ozden-s179-959-review-2026-11-12](../ozden-s179-959-review-2026-11-12/README.md). It
accepts the certificate, every one of its 13 findings a note. Its clean-room checker,
frozen at 22:03:30Z, decided every square, wall and pair by separating axes in GMP
rationals and by exact clipping in Python fractions, and its 19 controls, stated
beforehand, came out as stated; the squares are accepted in the box of the claim’s own
side, 13.880960371559 (F3). The case adopted the certificate at 179 on 12 November, in place
of T-291, with both strong generators’ regularization of the new house.

Where the review and this lane measured the same thing, they agree:

| Quantity | This lane | The review |
| --- | --- | --- |
| Gain on T-291 | 4.068e-04 | 4.06788552e-4 |
| Least pair gap | 1.99e-13, squares 104 and 105 | 1.99223328482862e-13, squares 104 and 105 |
| Wall contacts | the left, bottom and far walls touched exactly; square 67 at its wall | squares 67 bottom, 123 left, 162 top |
| T-291’s contraction margin | 2.616e-12, pair 14 and 15 | 2.616e-12, pair 14 and 15 |
| Identity against T-291 | one to one under the identity; 3 beyond 0.1, largest 0.218429; 5 turned beyond a degree | one to one at every anchor; 9 beyond 0.05, 3 beyond 0.1, largest 0.2181; 5 turned beyond a degree |
| Tilted squares | 35 beyond a degree, against T-291’s 36 | 36 beyond half a degree, against T-291’s 37 (square 42 at +0.53 degrees) |
| Side less s(70) + 5 | 2.645427e-12 | 2.6454e-12 |
| Contracted to first contact | 1 − λ\* = 1.992233e-13, side s(70) + 5 + 7.9e-14 | accepted at 1 − 1.99e-13, side s(70) + 5 + 8.2e-14; refused at 1 − 2e-13 |
| The 70 at a corner | at most 48 of 70 within 10⁻⁹ (upper right), 34 at the lower left | at most 48 (upper right), 34 at the lower left |
| The 70’s band ends | 7 at (0, 0) and 8 at (5, 5) within 10⁻⁹, identity only | 7 and 8 within 10⁻¹¹ |

The review adds what this lane did not measure: 26 of the 36 tilted squares sit at the 70
band’s angle, −40.750530446306 degrees, to 10⁻⁹ degrees; 103 upright squares lie on unit
lattices anchored at two walls; the 207 placed at the lower left matches 106 squares;
and the seed as the issue states it has 34 squares, not 35 (F9). Its F10 measures the
contracted side, 13.88096037155566185, 3.4e-13 below the leaderboard’s 13.880960371556:
a side inside the certificate’s own dilation is the owner’s open question RV-3
(think-ruu2), so it is noted and not registered. Its F11 names `think-mdxq` for the
band’s licence; that bead closed on 4 November, and the owner’s decision is
`think-71uq`.

The review’s questions for the author, which hold no rung:

1. Would the lab promote the pose with a contraction (`center_dilation` below 1)?
   Whether the record registers a side inside the repair dilation is its owner’s
   question.
2. Is there an exact construction at side s(70) + 5, as the registry’s 207 is at
   s(70) + 6? It would be scored on its own.
3. Was the repair scaling about 2 × 10⁻¹³ rather than 10⁻¹³ (F6)?
4. Do the lineage counts use T-174 reflected top to bottom and set against the
   upper-left corner, and would the issue name that convention (F7)?
5. Would the issue correct “our exact side 13.880960371558224”, the side’s binary64
   value, and the side’s 12-place fractional part, 0.880960371558 rather than
   0.880960371556 (F5)?
6. The seed as stated has 34 squares by their centres, not 35: which square does the
   35th count?
7. The issue dates its search for other claims 13:30 PST, after it was opened at 13:18
   PST: which time is right (F13)?
8. Did the seed take the 70 band from the registry’s witness or from Ryan Xu’s or Evan
   Daniel’s published coordinates, and will the band-design search be published?

## What Is Not Established

- **Human oversight.** No human oversight record.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **s(179) ≤ s(70) + 5 exactly.** The side is 2.645e-12 above it, and no construction
  from the 70’s exact coordinates is checked here.
- **The lineage** the source states, beyond what the measurements above show.

## Credit and Licence

The packing is Doğa Özden’s, a further arrangement of his own #954 packing (T-291), found
by his lab’s band-design search from the tilted squares of the registry’s n = 70 packing
(Ryan Xu, improved by Evan Daniel and PingYou Ltd). The issue asks that the improvement
be credited to Özden, the band’s source packing and the current record to their holders
as the registry lists them, and the local optimizer to Evan Daniel. The issue says the
search and its code were written and run by AI agents throughout and that the checks were
run by code that did not produce the packing; it says the issue and repository were
prepared and posted by his AI agent, and that Özden directed the work. The source starts
from this repository’s registry packings and makes its exact coordinates with this
repository’s promotion tool, so its lineage builds on this project. The bibliography key
is **[Özden s179 issue 959 2026-11-11]**.

The witness, the JSON, the decimal pose, the checker outputs, the README and the diff
image are published under CC BY 4.0, and `verifier/sqcheck.py` under the MIT licence,
copyright (c) 2026 Doğa Özden, as [source/LICENSE.md](source/LICENSE.md) states; it is
byte-identical to the `LICENSE.md` of the lab’s #954 repository and to the one it added
to its s299, s204 and s94 repositories on 4 November 2026 and announced on #890
([comment](https://github.com/jlevy/squares/issues/890#issuecomment-6637821113)).
The diff image is pinned by digest only. The source carries Evan Daniel’s MIT notice as
`LICENSE-evand-square-packing.txt`, for his quench code, byte-identical to the `LICENSE`
the [evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains,
and pinned against it. The registry’s 70, the band’s source, comes from PingYou Ltd’s PR
574 algebraic supplement, which has no licence file; whether a seed taken from it needs a
notice of its own is the owner’s decision on think-71uq, as for #954, noted here and not
decided.

## Commands

From `packing/`, with the project interpreter. The identity measurement reads the house
witness and its regularized view as they stood at main b5b12c206, before an adoption
replaces them, so it reproduces there; the other measurements read packets and the 70’s
house witness, and reproduce anywhere their tools are:

```bash
python -m devtools.acquire_source ozden-s179-issue959-2026-11-11 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s179-issue959-2026-11-11 --check
python -m devtools.upper_bound_reports ozden-s179-issue959-2026-11-11 check-claims --write
python -m devtools.upper_bound_reports ozden-s179-issue959-2026-11-11 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ozden-s179-issue959-2026-11-11 check --replay
python -m devtools.upper_bound_reports ozden-s179-issue959-2026-11-11 sharp-controls
python -m devtools.measure_identity --n 179 'OZDEN-959=packet:ozden-s179-issue959-2026-11-11' \
  'T-291=packet:ozden-s179-upper-bound-2026-11-11' \
  'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-179-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-179.yaml' \
  --out resources/web/ozden-s179-issue959-2026-11-11/measure/identity.json
python -m devtools.measure_core --n 179 '#959=packet:ozden-s179-issue959-2026-11-11' \
  --m 70 witnesses/known-best/n-070.yaml \
  --out resources/web/ozden-s179-issue959-2026-11-11/measure/core-n070.json
python -m devtools.contraction_margin --n 179 'T-291=packet:ozden-s179-upper-bound-2026-11-11' \
  --against 'ozden-959=packet:ozden-s179-issue959-2026-11-11' \
  --out resources/web/ozden-s179-issue959-2026-11-11/measure/contraction-n179.json
python -m devtools.contraction_margin --n 179 'ozden-959=packet:ozden-s179-issue959-2026-11-11' \
  --out resources/web/ozden-s179-issue959-2026-11-11/measure/contraction-n179-own.json
python -m devtools.l_step_scan --with 179=S179 \
  --out resources/web/ozden-s179-issue959-2026-11-11/measure/l-step-scan.json
```

In the last command `S179` is the `exact_side` in the packet’s claim record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
