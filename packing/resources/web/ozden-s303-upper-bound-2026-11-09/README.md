# Doğa Özden’s s(303) Certificate at b43ca09

This packet retains
[kenaznia-doga/s303-upper-bound](https://github.com/kenaznia-doga/s303-upper-bound/tree/b43ca090fc2ff5e750fecc71d8514298fe164514)
at `b43ca090fc2ff5e750fecc71d8514298fe164514` (committed 2026-11-09T06:03:05Z), the repository’s one commit, which
[issue #930](https://github.com/jlevy/squares/issues/930) names 42 seconds
later. Doğa Özden’s AI agent, which uses the account kenaznia-doga, prepared and posted both
on his behalf.

## What the Source Claims

- `n-303-candidate.yaml`, a `packing.squares:Witness/v2` file (corners, rational scalars, 303
  squares), bounds s(303) by its exact side, a fraction of more than 150 digits whose
  16-place ceiling is 17.9017892731564904. #930 prints its 12-place ceiling, 17.901789273157, and says
  it is 4.348e-05 below the record, Evan Daniel’s packing built by his fault-line composer after Chris Deotte’s multi-gadget fault DP (T-272, #914). It claims an upper bound only: no KKT, local-optimality,
  rigidity or global-optimality claim.
- The exact coordinates were made by this repository’s own `packing-witness promote
  --strategy robust-rational` at `19b354a5` from the lab’s decimal pose: pairs are separated
  by at least about 2 × 10⁻¹³, and squares at the walls touch them exactly. Measured by the
  stage 4 review, exactly three squares touch a wall, at the left, the bottom and the far
  wall that sets the side, and the other 31 square–wall pairs within 10⁻¹² sit
  1.05 × 10⁻¹⁶ to 10⁻¹² inside (its F4).
- `n303-witness.json` is the same file as JSON. `packing-witness-verify.txt` is the author’s run
  of this repository’s `packing-witness verify` at `19b354a5` (VERIFIED, 45,753 pairs);
  `sqcheck-output.txt` is the author’s run of `verifier/sqcheck.py`, an exact checker the
  source says was written separately from this repository’s code (VALID, exact rational,
  the exact side rounded up). The issue says the two share only the unit-square, wall and
  non-overlap definitions, and that `packing-witness verify` is not independent of how the
  coordinates were rounded. Those statements are the author’s; no source program ran here.
- The packing starts from the registry’s 303 (Evan Daniel (found_by), after Chris Deotte; T-272, #914), taken from this
  repository’s regularized known-best atlas, and was found by basin hopping over local
  minima computed by Evan Daniel’s ALM+SLP quench from
  [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT, at
  `bb4cc78e`), compiled into the lab’s search.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the whole tree, 9 files: 6 retained under
[source/](source/) and 3 pinned by digest.

| File | Bytes |
| --- | --- |
| `LICENSE.md` | 1,484 |
| `README.md` | 3,633 |
| `n-303-candidate.yaml` | 878,216 |
| `n303-witness.json` | 868,864, the same packing as JSON, which the reader holds equal to the YAML |
| `packing-witness-verify.txt` | 505 |
| `sqcheck-output.txt` | 101 |
| `records/n-303-candidate-diff.png` | 325,709, pinned by digest: a raster comparison that decides nothing |
| `verifier/README.md` | 3,441, pinned against the identical copy the [3 November s299 packet](../ozden-s299-upper-bound-2026-11-03/README.md) retains |
| `verifier/sqcheck.py` | 17,654, pinned against the identical copy the [s232 packet](../ozden-s232-upper-bound-2026-11-09/README.md) retains, never executed here |

The SHA-256s the issue states for `n-303-candidate.yaml` (`9cbeb7a8…2f3e`)
and the README states for it and for `n303-witness.json` (`0fd9f9dc…c3a2`)
are the files’. [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is
the full manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is under two megabytes in a checkout and far less as Git stores it, so it is
kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `19b354a5c` on 9 November
2026):

- **303:** exact side 17.9017892731564904 rounded up at 16 places, below the case’s house (T-272, Evan Daniel, after Chris Deotte) by
  4.348e-05, as the issue states; no register bound pending adoption below the
  house.

## Report Order

The
[ledger of 9 November for this pass](../../../campaign/issue-intake/upper-bounds-927-931-20261109/README.md)
walks every report at 232, 268, 299, 303 and 307 in the order it reached this repository,
from starts frozen at `main` `19b354a5c`, and records this packet’s claim at 303. The best
public Kaggle per-puzzle side the issue quotes at 303, 17.906978233799 (ntumlnoob), is above this and
states no packing.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-272’s packing, the
house witness and the regularized view, and wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **303:** one to one with T-272’s packing under the identity by nearest centres; the optimal assignment moves 5 squares beyond 0.1 and 105 beyond 0.01 (largest 0.22746) and turns 151 squares by more than 10⁻⁶ radians, 14 of them by more than 1 degree and by up to 19.02 degrees. Tilted beyond 1 degree: this packing 111, T-272 112, all turned one way. The house witness measures the same, and against the regularized view the source says it started from, the assignment moves 3 squares beyond 0.1 and 100 beyond 0.01. So it is a further arrangement of T-272’s packing, one to one with it, and not a new arrangement.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 274,518 pair decisions, 113.28 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Three squares touch the box, a least wall clearance of exactly 0, and every pair clears
by at least 2.013e-13.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
1e-30 past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)). It lowered
the side by the least far-wall clearance, closed the least-gap pair by its gap, and
moved every square toward the nearer near wall by its least clearance: both routes
accepted each at contact with margin 0 and refused each past it.
It enlarged one square to its pair and one to its wall: both routes refused each at
contact for its shape alone and 1e-30 past it for the overlap or the wall as well.
Both refused a duplicated square.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read the witness through the `witness-corners`
reader. The first route is the `packing-witness verify` the author ran on the same file,
so on that route the replay is reproduced with the producer’s code; the second shares no
verification code with it. Neither is independent of this repository’s `packing-witness
promote`, which made the coordinates and itself ran `sqpack`’s exact `verify_packing` on
them before writing them (the review’s F10). The source’s own `sqcheck.py` was not run.

## Stage 4 Review and Adoption

The stage 4 mathematical review of 9 November 2026
([review-2026-11-09-ozden-927-931-five.md](../../../../docs/project/reviews/review-2026-11-09-ozden-927-931-five.md)),
written in a separate lane blind to this one until its findings were frozen, accepts the
certificate with findings, none blocking or major, and scores it S3. Its clean-room
checker decides every square, wall and pair by separating axes in `Fraction` and by
exact clipped areas in GMP rationals, with controls stated before they ran; its
programs are kept once in the
[s232 packet’s review directory](../ozden-s232-upper-bound-2026-11-09/review/review-2026-11-09/README.md),
and this count’s receipts in [review/review-2026-11-09/out/](review/review-2026-11-09/out/).
The case adopted the certificate as its house on 9 November 2026 under the house rule,
as T-278, in place of T-272.

## What Is Not Established

- **Human oversight.** One AI review is retained; no human oversight record.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **The lineage** the source states, beyond what the measurement above shows.

## Credit and Licence

The packing is Doğa Özden’s, found from the registry’s 303 (Evan Daniel (found_by), after Chris Deotte; T-272, #914); the issue
asks that the improvement be credited to Özden, the base packing to its holders as the
record lists them, and the local optimizer to Evan Daniel.
The search was AI-assisted throughout, the checks were run by code that did not produce
the packing, and the issue and repository were prepared and posted by his AI agent; Özden
directed the work. The source starts from this repository’s regularized atlas and makes
its exact coordinates with this repository’s promotion tool, so its lineage builds on
this project. The bibliography key is **[Özden s303 upper bound 2026-11-09]**.

The witness, the JSON, the checker outputs, the README and the diff image are published
under CC BY 4.0, and `verifier/sqcheck.py` under the MIT licence, copyright (c) 2026 Doğa
Özden, as [source/LICENSE.md](source/LICENSE.md) states; it is byte-identical to the
`LICENSE.md` the lab added to its s299, s204 and s94 repositories on 4 November 2026 and
announced on #890
([comment](https://github.com/jlevy/squares/issues/890#issuecomment-6637821113)).
The diff image is pinned by digest only. The packing modifies Evan Daniel’s MIT-licensed certificate, whose notice the [evand-issue914-2026-11-05](../evand-issue914-2026-11-05/README.md) packet retains; the source carries no copy of that notice.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source ozden-s303-upper-bound-2026-11-09 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s303-upper-bound-2026-11-09 --check
python -m devtools.upper_bound_reports ozden-s303-upper-bound-2026-11-09 check-claims --write
python -m devtools.upper_bound_reports ozden-s303-upper-bound-2026-11-09 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ozden-s303-upper-bound-2026-11-09 check --replay
python -m devtools.upper_bound_reports ozden-s303-upper-bound-2026-11-09 sharp-controls
python -m devtools.measure_identity --n 303 'OZDEN=packet:ozden-s303-upper-bound-2026-11-09' \
  'T-272=packet:evand-issue914-2026-11-05' \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-303-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-303.yaml' \
  --out resources/web/ozden-s303-upper-bound-2026-11-09/measure/identity.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
