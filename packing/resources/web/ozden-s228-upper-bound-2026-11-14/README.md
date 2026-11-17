# Doğa Özden’s s(228) Certificate at 8bebf3f

This packet retains
[kenaznia-doga/s228-upper-bound](https://github.com/kenaznia-doga/s228-upper-bound/tree/8bebf3f78ef50baa0b47341a836b5e45717c49cc)
at `8bebf3f78ef50baa0b47341a836b5e45717c49cc` (committed 2026-11-14T18:33:59Z), the
repository’s one commit, which [issue #983](https://github.com/jlevy/squares/issues/983)
names 36 seconds later.
Doğa Özden’s AI agent, which uses the account kenaznia-doga, prepared and posted both on
his behalf. The account’s latest issues before it, #947, #962 and #967 at 269, #954 and
#959 at 179 and #960 at 237, of 11 and 12 November, are closed, and none is at 228; no
comment on them points to this one, and #983 had no comment when this packet was written.
The intake label was added at 18:57:20Z.

## What the Source Claims

- `n-228-candidate.yaml`, a `packing.squares:Witness/v2` file (corners, rational
  scalars, 228 squares), bounds s(228) by its exact side, a fraction whose 16-place
  ceiling is 15.6008017348117539. #983 prints its 12-place ceiling, 15.600801734812, and
  says it is 0.00379974091792048 below the record, T-174, Francisco Couzo’s packing as
  PingYou Ltd improved it (relative 2.435 × 10⁻⁴).
  The issue and README also print the exact side to 43 places before an ellipsis,
  15.6008017348117538028514559173910014808630264, the side rounded up there, and
  `sqcheck-228.txt` prints it rounded up at 15 places, 15.600801734811754.
  It claims an upper bound only: no optimality, KKT or rigidity claim.
- The exact coordinates were made by this repository’s own `packing-witness promote
  --strategy robust-rational` at `fa980f8e` from the lab’s decimal pose,
  `n-228-decimal-pose.yaml`, which the witness’s `source.path` names, with
  `center_dilation: '1'` and no dilation.
  The issue says the decimal pose was certified in interval arithmetic by `sqcheck.py` at
  its own side, with pair margins of at least 2.02 × 10⁻¹³ and wall margins of at least
  1.01 × 10⁻¹³, and that translating the least corner coordinates to zero and taking the
  greatest corner extent as the side lowered the pose’s side by 2.04 × 10⁻¹³, which it
  calls normalization and not part of the 0.0038 gain.
  `checks/promote.json` states that change of side exactly, −2.042 × 10⁻¹³.
- `n228-witness.json` is the same witness as JSON. `verify-228.txt` is the author’s
  unmodified run of this repository’s `packing-witness verify` at `fa980f8e` (VERIFIED,
  exact-algebraic over Q, 25,878 pairs), and `checks/registry.json` reports the same
  run’s least best pair gap, exactly 101/500000000000000, and least wall clearance, 0.
  `sqcheck-228.txt` is the author’s run of `verifier/sqcheck.py`, an exact checker the
  source says was implemented separately (VALID, exact rational); `checks/exact.json` and
  `checks/interval.json` are its JSON reports on the exact witness and on the decimal
  pose. The issue says promotion shares code with `packing-witness verify` and that
  `sqcheck.py` is separate.
  Those statements are the author’s; no source program ran here.
- The issue says the packing is an original AI-run column-band proposal design (the lab’s
  Sol near1 director, gpt-6.1-sol), not a donor or transplant start or a public recovery:
  axis-parallel squares occupy two wall-anchored staircase or corner domains, tilted
  stacks span a diagonal band, and a finite-memory dynamic programme over the columns
  generates proposals, with no global count optimality asserted for arbitrary-angle
  junctions. Full emitted-count and far-overlap audits precede one quench with Evan
  Daniel’s ALM+SLP fq optimizer from
  [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT,
  built from `bb4cc78e`), and no random kicks were used for this hit.
  `hit-n228-114-0.txt` is the filed hit, of kind design, from the proposal f = 0.596543,
  delta 1 degree, tolerance 0.03, count 228, 48 tilted squares, column offset 0.026742,
  variant 1 and corner layout `t:4,4`, final decimal side 15.60080173481195764 at 121
  seconds of search; `hit-n228-114-0.json` records that metadata.
  The README says these are proposal parameters, not a claim that the quenched squares
  keep that angle, and that an independently harvested copy of the hit file has the
  SHA-256 18dad468…f2bfe5, which is the retained file’s.
- Against the registry packing, matched up to the square’s eight symmetries, the issue
  reports all 228 centres moved beyond 0.001, 93 beyond 0.05 (largest 0.940), and 59
  squares re-tilted beyond 1 degree; it counts 50 squares tilted beyond 0.5 degree
  against the record’s 51.
- **The leaderboard, disclosed first.** The issue opens by saying this packing does not
  beat the cached Kaggle per-puzzle side-only entry at 228, 15.596043116646 (square1000,
  29 October, from a cache of 9 November 20:52 UTC), 0.004758618166 below this side, and
  that the entry supplies no packing it can verify.
  It quotes the best public Kaggle packing it found at 228, 15.604601475744 (kirilltym,
  data of 11 November), above this side by 3.80 × 10⁻³, and says that open issues #593,
  #375, #419 and #405 and the open pull requests hold no lower packing at 228.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the whole tree, 18 files: 13 retained under [source/](source/) and 5 pinned
by digest.

| File | Bytes |
| --- | --- |
| `LICENSE.md` | 1,484 |
| `README.md` | 5,302 |
| `checks/exact.json`, `checks/interval.json`, `checks/promote.json`, `checks/registry.json` | 311, 357, 1,468 and 961 |
| `hit-n228-114-0.json` | 378 |
| `hit-n228-114-0.txt` | 13,597, the search’s pose as it was filed |
| `n-228-candidate.yaml` | 623,114 |
| `n-228-decimal-pose.yaml` | 23,416, the decimal pose the witness was promoted from |
| `n228-witness.json` | 667,353, stored compressed, the same packing as JSON, which the reader holds equal to the YAML |
| `sqcheck-228.txt` | 101 |
| `verify-228.txt` | 621 |
| `LICENSE-evand-square-packing.txt` | 1,068, pinned against the identical copy of Evan Daniel’s MIT notice the [evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains |
| `records/n-228-candidate-diff.png` | 265,611, pinned by digest: a raster comparison that decides nothing |
| `records/n-228-candidate-diff.svg` | 76,066, pinned by digest: the same comparison drawn as vectors |
| `verifier/README.md` | 3,441, pinned against the identical copy the [3 November s299 packet](../ozden-s299-upper-bound-2026-11-03/README.md) retains |
| `verifier/sqcheck.py` | 17,654, pinned against the identical copy the [9 November s232 packet](../ozden-s232-upper-bound-2026-11-09/README.md) retains, never executed here |

The SHA-256 the issue and README state for `n-228-candidate.yaml` is the file’s.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is about a megabyte in a checkout and far less as Git stores it, so it is kept
in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `fa980f8e7` on 14
November 2026):

- **228:** exact side 15.6008017348117539 rounded up at 16 places, below the case’s
  house (T-174, Francisco Couzo’s packing as PingYou Ltd improved it) by 3.7997409179 ×
  10⁻³, the 0.00379974091792048 the issue states.
  No register bound is pending adoption at 228.

## Report Order

The
[ledger of 14 November for this lane](../../../campaign/issue-intake/upper-bounds-983-20261114/README.md)
walks every report at 228 in the order it reached this repository, from a start frozen
at `main` `fa980f8e7`, and records this packet’s claim at 228 as a new packing, as the
issue calls it. The best public Kaggle per-puzzle packing the issue quotes at 228,
15.604601475744 (kirilltym), is above this, by 3.80 × 10⁻³. The side-only Kaggle
leaderboard entry the issue states first, 15.596043116646 (square1000), lies 4.76 ×
10⁻³ below this side, as the issue says; it is unpublished and states no packing, so it
is no report and is recorded as context only.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-174’s packing, the house
witness and the regularized view, and wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **Against T-174**, the house: no symmetry of the box pairs it one to one with T-174’s
  packing by nearest centres.
  The optimal assignment, best under symmetry 7, moves every square beyond 10⁻³, 108
  beyond 0.01 and 75 beyond 0.1 (largest 0.940075), and turns 74 squares by more than
  10⁻⁶ radians, by up to 42.93 degrees; aligned by box centres, 59 squares turn by more
  than a degree and 36 tilts reverse.
  Tilted beyond a degree: 48 here, at 41.02 to 43.03 degrees, all one way, against
  T-174’s 51, at 38.43 to 42.93 degrees, 45 one way and 6 the other.
  Two of the 89 squares within a degree of upright here turn by more than half a degree,
  0.67 and 0.96, so 50 are tilted beyond half a degree, as the issue counts, against
  T-174’s 51.
  The house witness and its regularized view measure as T-174.
  So it is a new arrangement relative to T-174’s packing, not a further arrangement of it.
- The issue’s own counts hold where the measurement bins them: every centre beyond
  0.001, the largest move 0.940 and 59 squares re-tilted beyond a degree, the last under
  box-centred alignment. The 93 beyond 0.05 falls between the assignment’s 108 beyond
  0.01 and 75 beyond 0.1, a bin the receipt does not keep.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 155,268 pair decisions, 41.55 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 101/500000000000000, 2.02 × 10⁻¹³, the gap the author’s verify run reports.
`check --replay` decided the three jobs again.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
10⁻³⁰ past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)), with the
expected verdicts of the gross and sharp controls stated before either ran (SHA-256
`c56e906d5797db868db3d11a53ddc1badb0ecaa52f36db574b1678f10746a23f`, at 19:04:20Z on 14
November, recorded on the bead).
It lowered the side by the least far-wall clearance, 0, closed the least-gap pair
(squares 118 and 119) by its gap, and moved every square toward the nearer near wall by
its least clearance, 0: both routes accepted each at contact with margin 0 and refused
each past it.
It enlarged one square to its pair and one to its wall: both routes refused the first,
square 119, at contact for its shape alone and accepted the second, square 63, which
already touches its wall and so grew by 0, at contact; both refused each 10⁻³⁰ past it
for the overlap or the wall as well.
Both refused a duplicated square.
All 11 were as stated in advance.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read the witness through the `witness-corners`
reader. The first route is the `packing-witness verify` the author ran on the same file,
so on that route the replay is reproduced with the producer’s code; the second shares no
verification code with it.
Neither is independent of this repository’s `packing-witness promote`, which made the
coordinates. The source’s own `sqcheck.py` was not run.

## The Gain Against Padding

T-174’s certificate at 228, contracted uniformly about the origin to first contact and
boxed, loses nothing: its binding pair, squares 201 and 227, already touches (λ\* = 1).
So the whole gain this certificate states, 3.7997 × 10⁻³, lies outside the house’s
padding; the owner’s open question about gains inside a padding margin (RV-3,
think-ruu2) does not reach it, and the entry is not held at V0/C1 as T-285 and T-286
were.
This certificate’s own margin, measured the same way, is 2.949 × 10⁻¹² (1 − λ\* =
101/500000000000101, about 2.02 × 10⁻¹³, the binding pair squares 118 and 119, the
least-gap pair); contracted, it would be a square of side 15.6008017348088045 rounded
up, which nobody reported and which is not registered (RV-3).
The gain is 1.29 × 10⁹ times that margin.
`devtools.contraction_margin` wrote the two receipts,
[measure/contraction-n228.json](measure/contraction-n228.json) and
[measure/contraction-n228-own.json](measure/contraction-n228-own.json), each contracted
packing decided on both maintained routes.

## The L Step

`devtools.l_step_scan`, with this side stood in for 228’s ceiling, finds the same L-step
and monotonicity consequences as on `main`: this bound carries to no other count
([measure/l-step-scan.json](measure/l-step-scan.json)).

## Stage 4 Review and Adoption

The stage 4 mathematical review of 14 November 2026
([review-2026-11-14-ozden-983.md](../../../../docs/project/reviews/review-2026-11-14-ozden-983.md)),
written in a separate lane (L159) blind to this one throughout, accepts the certificate
with nine findings, all notes, none blocking, and scores it S3. Its clean-room checker
decides every square, wall and pair by separating axes in Python integers and by exact
Sutherland–Hodgman clipping in GMP rationals, with 20 controls stated before they ran,
all 20 as stated, and accepts the same squares in the box of the claim’s own side,
15.600801734812, and refuses them in the box of its 12-place floor (F3). Its programs
and receipts are kept in the review-only directory beside this packet,
[ozden-s228-983-review-2026-11-14](../ozden-s228-983-review-2026-11-14/README.md).

This lane recorded its replay, controls and measurements in its intake commit
(`1cc92c9dc`, 19:15Z) and registered T-300 (`07cf0d714`, 19:20Z) before it read the
review. It read the review’s frozen findings (`c2ed4e00c`, 19:23Z) at about 19:25Z and
began the adoption on their accepted verdict, its regularization runs from 19:27Z, while
the review’s later checks ran; it merged the review’s final head (`fcdfe8086`, 19:41Z)
once the coordinator reported it landed.
Read against this packet’s receipts once both were done, the review’s least pair margin
(101/500000000000000, squares 118 and 119 and six more pairs) is the replay’s exactly,
and square 63, the square the sharp controls grew at its wall, is one of its three wall
contacts (63 at the left, 167 at the bottom, 213 at the top).
Its contraction receipts for T-174 and for this certificate equal
[measure/contraction-n228.json](measure/contraction-n228.json) and
[measure/contraction-n228-own.json](measure/contraction-n228-own.json) in margin, factor,
binding pair and contracted side, and its identity measurement against T-174 equals
[measure/identity.json](measure/identity.json) under nearest centres, the optimal
assignment and box-centred alignment, as do the tilt counts.
No disagreement.

The review finds the issue’s arithmetic right (F4): the claim is the side’s 12-place
ceiling and the gain the exact gap’s 17-place floor, relative to T-174’s side; the
43-place exact side is rounded up and followed by an ellipsis that reads as a truncation.
T-174 has no contraction margin, so RV-3 does not reach the gain, and the certificate’s
own contracted side, 15.6008017348088, is a side only RV-3 could register (F5).
The issue’s lineage counts hold, all four, with T-174 transposed and set against the
lower-left corner of the new box under either assignment, a convention the issue does
not name; under the placement of least total move 52 upright squares stay within 10⁻³ of
T-174’s (F6). It is a new arrangement relative to T-174 and to T-128, T-098, T-092 and
T-056, every other registered packing at 228 (F7).
The reports under `checks/` name the promoted witness `W-colband-n228-sol1114-rational`
from `W-colband-n228-sol1114`, where the retained certificate is `W-candidate-n228` from
`W-colband-near1-n228`; they agree with it in side, pairs, least gap and wall clearance
(F8). The witness’s `softschema.schema` resolves to no file in the author’s repository
and its `certificate.replay` names no directory, as at #967; the adopted witness carries
this repository’s own (F9). The side is not s(m) + k for any registry value below 228
and integer k up to 16 within 10⁻⁹; the nearest is s(37) + 9, 2.18 × 10⁻³ away.

Its six questions for the author, informational and holding nothing open:

1. The lineage counts reproduce with T-174 transposed in the new box and set against its
   lower-left corner. Is that the tool’s convention, and would the issue name it (F6)?
2. Was the retained `W-candidate-n228` made from the reports’ witness by changing its ids
   alone (F8)?
3. Would the author print the 43-place side’s floor, or drop the ellipsis (F4)?
4. Will the column-band designer and its dynamic programme be published, and is the
   proposal’s `nt = 48` the band’s 48 squares?
5. Would the author point `softschema.schema` at a file that resolves in his repository,
   and say in the replay line where to run it (F9)?
6. Would the lab promote with a contraction (`center_dilation` below 1), knowing that
   whether the record registers a side inside the certificate’s own padding is its
   owner’s question (RV-3, F5)?

The case adopted the certificate as its house in the pass of 14 November 2026 under the
house rule, as T-300, in place of T-174, which keeps its certificate as history, with
Doğa Özden the finder of a new arrangement below Francisco Couzo’s packing as PingYou
Ltd improved it, and Evan Daniel credited for the optimizer, as the issue asks (F7).
228 joins the day’s pass beside 297, whose archive takes a row for each count.
Both strong generators ran on the new witness
([the runs](../../../cases/regularized_drawings/think-14i2-2026-11-14/README.md)), and
the selection, measured against the axis tool’s drawing of this witness, draws
grid-slack’s 1-degree view: light, uneven and near-axis squares, angle classes and hues
35, 78, 12, 30 and 19 against 0, 4, 0, 16 and 16, and full shared sides 475 and 577
against 672 and 680. Evan Daniel’s driver drew a same-side view that its row 7 holds for
review; his certified KKT solve lies 3.01 × 10⁻¹² below the side, 1.02 of the
certificate’s own contraction margin (2.949 × 10⁻¹²), held at row 3 as a register
candidate and not admitted, as at 156, 172, 179, 180, 199, 268, 269 and 270 (RV-3).
The rigidity block, derived again on the new witness, stays not rigid: 123 of its 228
squares translate, against 18 of T-174’s.

## What Is Not Established

- **Human oversight.** One AI review is retained; no human oversight record.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **The lineage** the source states, beyond what the measurement above shows.

## Credit and Licence

The packing is Doğa Özden’s, found by his lab’s column-band proposal designer, which the
issue says took no donor packing, and quenched with Evan Daniel’s optimizer.
The issue asks that Özden be recorded as the finder of this new arrangement, that the
old record stay credited to Francisco Couzo and PingYou Ltd, and that Evan Daniel be
credited for the optimizer.
The record at 228 before this import was T-174, PingYou Ltd’s refinement of Francisco
Couzo’s refinement of his own packing.
The issue says the search, checks and filing were AI-assisted throughout and that the
issue and repository were prepared and posted on his behalf by his AI agent.
The source makes its exact coordinates with this repository’s promotion tool, so its
lineage builds on this project.
The bibliography key is **[Özden s228 upper bound 2026-11-14]**.

The witness, the JSON, the decimal pose, the hit file and its metadata, the check
reports and outputs, the README and the two comparison figures are published under CC
BY 4.0, and `verifier/sqcheck.py` under the MIT licence, copyright (c) 2026 Doğa Özden, as
[source/LICENSE.md](source/LICENSE.md) states; it is byte-identical to the `LICENSE.md`
the lab added to its s299, s204 and s94 repositories on 4 November 2026 and announced on
#890 ([comment](https://github.com/jlevy/squares/issues/890#issuecomment-6637821113)),
and to the one #967’s repository carries.
The comparison figures are pinned by digest only.
The source carries Evan Daniel’s MIT notice as `LICENSE-evand-square-packing.txt`, for
his quench code, byte-identical to the `LICENSE` the
[evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains, and
pinned against it.

## Commands

From `packing/`, with the project interpreter.
The identity measurement reads the house witness and its regularized view as they stood
at main fa980f8e7, before any adoption replaced them, so it reproduces there; the
contraction margins read the packets and reproduce anywhere
`devtools.contraction_margin` is:

```bash
python -m devtools.acquire_source ozden-s228-upper-bound-2026-11-14 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s228-upper-bound-2026-11-14 --check
python -m devtools.upper_bound_reports ozden-s228-upper-bound-2026-11-14 check-claims --write
python -m devtools.upper_bound_reports ozden-s228-upper-bound-2026-11-14 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ozden-s228-upper-bound-2026-11-14 check --replay
python -m devtools.upper_bound_reports ozden-s228-upper-bound-2026-11-14 sharp-controls
python -m devtools.measure_identity --n 228 'OZDEN=packet:ozden-s228-upper-bound-2026-11-14' \
  'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  'regularized=witness-corners:atlas/known-best/regularized/n-228-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-228.yaml' \
  --out resources/web/ozden-s228-upper-bound-2026-11-14/measure/identity.json
python -m devtools.contraction_margin --n 228 'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  --against 'ozden-983=packet:ozden-s228-upper-bound-2026-11-14' \
  --out resources/web/ozden-s228-upper-bound-2026-11-14/measure/contraction-n228.json
python -m devtools.contraction_margin --n 228 'ozden-983=packet:ozden-s228-upper-bound-2026-11-14' \
  --out resources/web/ozden-s228-upper-bound-2026-11-14/measure/contraction-n228-own.json
python -m devtools.l_step_scan --with 228=S228 \
  --out resources/web/ozden-s228-upper-bound-2026-11-14/measure/l-step-scan.json
```

In the last command `S228` is the `exact_side` in the packet’s claim record.

## Compressed Files

| Stored file | Origin | Git blob of stored file | SHA-256 of decompressed source |
| --- | --- | --- | --- |
| `source/n228-witness.json.gz` | upstream | `6f1da4b17f0f6864b0e26688833905e3a741107a` | `2d4066b6962e8131e3d8e37b2fbf3d36816543c139b6e0cfb5d5602ac1274ebb` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
