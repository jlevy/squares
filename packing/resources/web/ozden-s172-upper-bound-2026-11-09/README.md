# Doğa Özden’s s(172) Certificate at 2ce1f7c

This packet retains
[kenaznia-doga/s172-upper-bound](https://github.com/kenaznia-doga/s172-upper-bound/tree/2ce1f7c7621859437e0bcc1f9ad2b00822b2c605)
at `2ce1f7c7621859437e0bcc1f9ad2b00822b2c605` (committed 2026-11-09T15:28:22Z), the
repository’s one commit, which [issue #935](https://github.com/jlevy/squares/issues/935)
names 26 seconds later. Doğa Özden’s AI agent, which uses the account kenaznia-doga,
prepared and posted both on his behalf.

## What the Source Claims

- `n-172-candidate.yaml`, a `packing.squares:Witness/v2` file (corners, rational scalars,
  172 squares), bounds s(172) by its exact side, a fraction of about 90 digits whose
  16-place ceiling is 13.6146898532862152. #935 prints its 12-place ceiling,
  13.614689853287, and says it is 3.246e-03 below the record, Evan Daniel’s packing
  (T-257, #845). It claims an upper bound only: no KKT, local-optimality, rigidity or
  global-optimality claim.
- The exact coordinates were made by this repository’s own `packing-witness promote
  --strategy robust-rational` at `ef1af493` from the lab’s decimal pose,
  `n-172-decimal-pose.yaml`, which the witness’s `source.path` names, with
  `center_dilation: '1'` and no dilation. The issue says the pair margins of about
  2 × 10⁻¹³ are the decimal pose’s own, left by the final binary64 repair scaling of
  Evan Daniel’s quench, that only the squares that set the left wall, the bottom wall
  and the side touch them exactly, and that other squares near a wall clear it by up to
  about 10⁻¹². Measured by the stage 4 review, exactly three squares touch a wall (left
  46, bottom 85, right 161); the other squares within 10⁻¹² of a wall clear it by
  2.8 × 10⁻¹⁷ to 7.0 × 10⁻¹⁵, and square 151 clears the top by 6.0 × 10⁻⁵, beyond “up
  to about 1e-12” (its F4). The pair margins are 2.0 to 3.3 × 10⁻¹³ of the centres’
  separation, about twice the issue’s “about 1e-13 relative” (F5).
- `n172-witness.json` is the same file as JSON. `packing-witness-verify.txt` is the
  author’s run of this repository’s `packing-witness verify` at `ef1af493` (VERIFIED,
  14,706 pairs); `sqcheck-output.txt` is the author’s run of `verifier/sqcheck.py`, an
  exact checker the source says was written separately from this repository’s code
  (VALID, exact rational, the exact side rounded up). The issue says the two share only
  the unit-square, wall and non-overlap definitions, that `packing-witness verify` is not
  independent of how the coordinates were rounded, and that `sqcheck.py` certified the
  decimal pose in interval arithmetic at its own side before promotion.
  Those statements are the author’s; no source program ran here.
- The packing starts from the registry’s 172 (Evan Daniel (found_by); T-257, #845),
  taken from this repository’s regularized known-best atlas, and was found by basin
  hopping (kick, rotate, swap and reinsert moves) over local minima computed by Evan
  Daniel’s ALM+SLP quench from [evand/square-packing](https://github.com/evand/square-packing)
  (`search/packer`, MIT, at `bb4cc78e`), built unmodified into the lab’s search.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the whole tree, 11 files: 7 retained under
[source/](source/) and 4 pinned by digest.

| File | Bytes |
| --- | --- |
| `LICENSE.md` | 1,484 |
| `README.md` | 4,400 |
| `n-172-candidate.yaml` | 520,850 |
| `n-172-decimal-pose.yaml` | 19,503, the decimal pose the witness was promoted from |
| `n172-witness.json` | 515,559, the same packing as JSON, which the reader holds equal to the YAML |
| `packing-witness-verify.txt` | 362 |
| `sqcheck-output.txt` | 101 |
| `LICENSE-evand-square-packing.txt` | 1,068, pinned against the identical copy of Evan Daniel’s MIT notice the [evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains |
| `records/n-172-candidate-diff.png` | 251,971, pinned by digest: a raster comparison that decides nothing |
| `verifier/README.md` | 3,441, pinned against the identical copy the [3 November s299 packet](../ozden-s299-upper-bound-2026-11-03/README.md) retains |
| `verifier/sqcheck.py` | 17,654, pinned against the identical copy the [9 November s232 packet](../ozden-s232-upper-bound-2026-11-09/README.md) retains, never executed here |

The SHA-256s the issue states for `n-172-candidate.yaml` (`0df5ae79…b2af`) and the README
states for it and for `n172-witness.json` (`311a8333…a2bf`) are the files’.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is about one megabyte in a checkout and far less as Git stores it, so it is
kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `ef1af4933` on 9 November
2026):

- **172:** exact side 13.6146898532862152 rounded up at 16 places, below the case’s
  house (T-257, Evan Daniel) by 3.246e-03, as the issue states; no register bound pending
  adoption below the house.

## Report Order

The
[ledger of 9 November for this lane](../../../campaign/issue-intake/upper-bounds-935-936-20261109/README.md)
walks every report at 172 and 270 in the order it reached this repository, from starts
frozen at `main` `ef1af4933`, and records this packet’s claim at 172. The best public
Kaggle per-puzzle side the issue quotes at 172, 13.617935700905 (jazivxt), is above this
and states no packing.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-257’s packing, the house
witness and the regularized view, and wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **172:** no symmetry pairs it one to one with T-257’s packing by nearest centres, which
  miss by one shared centre (squares 14 and 18 both lie nearest house square 14); the
  optimal assignment, under the identity, moves 15 squares beyond 0.1 and 69 beyond 0.01
  (largest 0.668426) and turns 58 squares by more than 10⁻⁶ radians, 15 of them by more
  than 1 degree. In a block turned about 45 degrees, ten squares move by up to 0.6 and
  turn by about a degree, three upright squares take the block’s tilt (the largest turn,
  44.61 degrees) and two of its squares straighten (the review’s F6).
  Tilted beyond 1 degree: 49 in each packing, 44 and 45 of them within a degree of 45
  degrees, where the sign of a tilt is a convention; the nine squares whose angles cross
  45 degrees turn by 0.8 to 1.2 degrees, so no tilt reverses (F15, which corrects this
  section’s first draft). The house witness measures the same, and against the
  regularized view the source says it started from, the assignment moves 15 squares
  beyond 0.1 and 65 beyond 0.01. So it is a further arrangement of T-257’s packing,
  though not one to one with it by nearest centres. The issue’s own counts (168 centres
  beyond 10⁻³, 15 squares re-tilted beyond 1 degree, largest move 0.668) are against the
  house witness, and agree with these (F7).

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 88,236 pair decisions, 38.05 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 2.008e-13.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
1e-30 past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)). It lowered
the side by the least far-wall clearance, closed the least-gap pair by its gap, and moved
every square toward the nearer near wall by its least clearance: both routes accepted
each at contact with margin 0 and refused each past it.
It enlarged one square to its pair and one to its wall: both routes refused the first at
contact for its shape alone and accepted the second, already touching its wall, at
contact; both refused each 1e-30 past it for the overlap or the wall as well.
Both refused a duplicated square.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read the witness through the `witness-corners`
reader. The first route is the `packing-witness verify` the author ran on the same file,
so on that route the replay is reproduced with the producer’s code; the second shares no
verification code with it. Neither is independent of this repository’s `packing-witness
promote`, which made the coordinates. The source’s own `sqcheck.py` was not run.

## The Gain Against Padding

T-257’s certificate carries padding of its own: contracted uniformly about the origin to
first contact and boxed, its packing loses 1.36 × 10⁻¹⁹ of side (1 − λ\* = 10⁻²⁰).
The gain this certificate states, 3.246 × 10⁻³, is about 2.4 × 10¹⁶ times that margin,
so no share of it worth stating is the house’s padding. This certificate’s own margin,
measured the same way, is 2.53 × 10⁻¹² (1 − λ\* = 2.008 × 10⁻¹³, the binding pair the
least-gap pair of the replay). `devtools.contraction_margin` wrote both receipts,
[measure/contraction-n172.json](measure/contraction-n172.json) and
[measure/contraction-n172-own.json](measure/contraction-n172-own.json), each contracted
packing decided on both maintained routes. The review measured the same margins with its
own programs ([houses.json](review/review-2026-11-09/out/houses.json),
[compare-lane.json](review/review-2026-11-09/out/compare-lane.json)), so the owner’s question about gains
inside a padding margin does not reach this one (its F9).

## Stage 4 Review and Adoption

The stage 4 mathematical review of 9 November 2026
([review-2026-11-09-ozden-935-936.md](../../../../docs/project/reviews/review-2026-11-09-ozden-935-936.md)),
written in a separate lane (L72, think-qqyg) blind to this one until its findings were
frozen, accepts the certificate with findings, none blocking or major, and scores it S3.
Its clean-room checker decides every square, wall and pair by separating axes in
`Fraction` and by exact clipped areas in GMP rationals, with 23 controls stated before
they ran; its programs, its shared receipts and this count’s are kept in
[review/review-2026-11-09/](review/review-2026-11-09/README.md). F15 (minor) corrected
this README’s and the register’s first reading of the tilts near 45 degrees; F4, F5, F12
and F13 are notes for the author: the wall sentence, the size of the margins, the decimal
pose’s schema path on the author’s machine, and a `certificate.replay` with no working
directory. The case adopted the certificate as its house on 9 November 2026 under the
house rule, as T-282, in place of T-257.

## What Is Not Established

- **Human oversight.** One AI review is retained; no human oversight record.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **The lineage** the source states, beyond what the measurement above shows.

## Credit and Licence

The packing is Doğa Özden’s, found from the registry’s 172 (Evan Daniel (found_by);
T-257, #845); the issue asks that the improvement be credited to Özden, the base packing
to its holders as the record lists them, and the local optimizer to Evan Daniel.
The issue says the search and its code were written and run by AI agents throughout and
that the checks were run by code that did not produce the packing; the issue and
repository were prepared and posted by his AI agent, and Özden directed the work.
The source starts from this repository’s regularized atlas and makes its exact
coordinates with this repository’s promotion tool, so its lineage builds on this project.
The bibliography key is **[Özden s172 upper bound 2026-11-09]**.

The witness, the JSON, the decimal pose, the checker outputs, the README and the diff
image are published under CC BY 4.0, and `verifier/sqcheck.py` under the MIT licence,
copyright (c) 2026 Doğa Özden, as [source/LICENSE.md](source/LICENSE.md) states; it is
byte-identical to the `LICENSE.md` the lab added to its s299, s204 and s94 repositories
on 4 November 2026 and announced on #890
([comment](https://github.com/jlevy/squares/issues/890#issuecomment-6637821113)).
The diff image is pinned by digest only. The packing modifies Evan Daniel’s MIT-licensed
certificate, and the source carries his MIT notice as `LICENSE-evand-square-packing.txt`,
byte-identical to the `LICENSE` the
[evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains, and
pinned against it.

## Commands

From `packing/`, with the project interpreter. The identity measurement reads the house
witness and its regularized view as they stood at main ef1af4933, before this adoption
replaced them, so it reproduces there; the contraction margins read the packets and
reproduce anywhere `devtools.contraction_margin` is (main 20f844dbf on):

```bash
python -m devtools.acquire_source ozden-s172-upper-bound-2026-11-09 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s172-upper-bound-2026-11-09 --check
python -m devtools.upper_bound_reports ozden-s172-upper-bound-2026-11-09 check-claims --write
python -m devtools.upper_bound_reports ozden-s172-upper-bound-2026-11-09 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ozden-s172-upper-bound-2026-11-09 check --replay
python -m devtools.upper_bound_reports ozden-s172-upper-bound-2026-11-09 sharp-controls
python -m devtools.measure_identity --n 172 'OZDEN=packet:ozden-s172-upper-bound-2026-11-09' \
  'T-257=packet:evand-issue845-2026-10-29' \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-172-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-172.yaml' \
  --out resources/web/ozden-s172-upper-bound-2026-11-09/measure/identity.json
python -m devtools.contraction_margin --n 172 'T-257=packet:evand-issue845-2026-10-29' \
  --against 'T-282=packet:ozden-s172-upper-bound-2026-11-09' \
  --out resources/web/ozden-s172-upper-bound-2026-11-09/measure/contraction-n172.json
python -m devtools.contraction_margin --n 172 'T-282=packet:ozden-s172-upper-bound-2026-11-09' \
  --out resources/web/ozden-s172-upper-bound-2026-11-09/measure/contraction-n172-own.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
