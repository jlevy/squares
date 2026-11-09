# Doğa Özden’s s(268) Certificate at a40a15d

This packet retains
[kenaznia-doga/s268-upper-bound](https://github.com/kenaznia-doga/s268-upper-bound/tree/a40a15d91081be002805b6eea35e099c9a2656db)
at `a40a15d91081be002805b6eea35e099c9a2656db` (committed 2026-11-09T06:02:49Z), the repository’s one commit, which
[issue #928](https://github.com/jlevy/squares/issues/928) names 57 seconds
later. Doğa Özden’s AI agent, which uses the account kenaznia-doga, prepared and posted both
on his behalf.

## What the Source Claims

- `n-268-candidate.yaml`, a `packing.squares:Witness/v2` file (corners, rational scalars, 268
  squares), states s(268) ≤ 16.8724698978362125… rounded up at 16 places, which #928 prints as
  16.872469897837, the exact side rounded up at 12 places, and says is 2.962e-05 below the
  record, Evan Daniel’s packing built by his fault-line composer after Chris Deotte’s multi-gadget fault DP (T-270, #914). It claims an upper bound only: no KKT, local-optimality,
  rigidity or global-optimality claim.
- The exact coordinates were made by this repository’s own `packing-witness promote
  --strategy robust-rational` at `19b354a5` from the lab’s decimal pose: pairs are separated
  by at least about 2 × 10⁻¹³, and squares at the walls touch them exactly. So the side is a
  fraction of more than 150 digits.
- `n268-witness.json` is the same file as JSON. `packing-witness-verify.txt` is the author’s run
  of this repository’s `packing-witness verify` at `19b354a5` (VERIFIED, 35,778 pairs);
  `sqcheck-output.txt` is the author’s run of `verifier/sqcheck.py`, an exact checker the
  source says was written separately from this repository’s code (VALID, exact rational,
  the exact side rounded up). The issue says the two share only the unit-square, wall and
  non-overlap definitions, and that `packing-witness verify` is not independent of how the
  coordinates were rounded. Those statements are the author’s; no source program ran here.
- The packing starts from the registry’s 268 (Evan Daniel (found_by), after Chris Deotte; T-270, #914), taken from this
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
| `README.md` | 3,629 |
| `n-268-candidate.yaml` | 815,619 |
| `n268-witness.json` | 807,352, the same packing as JSON, which the reader holds equal to the YAML |
| `packing-witness-verify.txt` | 565 |
| `sqcheck-output.txt` | 101 |
| `records/n-268-candidate-diff.png` | 300,300, pinned by digest: a raster comparison that decides nothing |
| `verifier/README.md` | 3,441, pinned against the identical copy the [3 November s299 packet](../ozden-s299-upper-bound-2026-11-03/README.md) retains |
| `verifier/sqcheck.py` | 17,654, pinned against the identical copy the [s232 packet](../ozden-s232-upper-bound-2026-11-09/README.md) retains, never executed here |

The SHA-256s the issue states for `n-268-candidate.yaml` (`74c0e5d4…21b3`)
and the README states for it and for `n268-witness.json` (`fcd07b9f…d180`)
are the files’. [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is
the full manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is under two megabytes in a checkout and far less as Git stores it, so it is
kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `19b354a5c` on 9 November
2026):

- **268:** exact side 16.8724698978362125…, below the case’s house (T-270, Evan Daniel, after Chris Deotte) by
  2.962e-05, as the issue states; no register bound pending adoption below the
  house.

## Report Order

The
[ledger of 9 November for this pass](../../../campaign/issue-intake/upper-bounds-927-931-20261109/README.md)
walks every report at 232, 268, 299, 303 and 307 in the order it reached this repository,
from starts frozen at `main` `19b354a5c`, and records this packet’s claim at 268. The best
public Kaggle per-puzzle side the issue quotes at 268, 16.874361715873 (ntumlnoob), is above this and
states no packing.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-270’s packing, the
house witness and the regularized view, and wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **268:** one to one with T-270’s packing under the identity by nearest centres; the optimal assignment moves 4 squares beyond 0.1 and 61 beyond 0.01 (largest 0.27375) and turns 121 squares by more than 10⁻⁶ radians, 3 of them by more than 1 degree and by up to 2.14 degrees. Tilted beyond 1 degree: this packing 99, T-270 98, all turned one way. The house witness measures the same, and against the regularized view the source says it started from, the assignment moves 7 squares beyond 0.1 and 61 beyond 0.01 (largest 0.396). So it is a further arrangement of T-270’s packing, one to one with it, and not a new arrangement.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 214,668 pair decisions, 93.19 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 2.012e-13.

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
promote`, which made the coordinates. The source’s own `sqcheck.py` was not run.

## What Is Not Established

- **The stage 4 review.** A separate lane (think-rd0p), blind to this one, reviews the
  certificate; until its review is mapped the case keeps its house, T-270, and the
  register entry T-276 stands at V3/C3 on this replay alone.
- **Human oversight.** No human oversight record is retained.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **The lineage** the source states, beyond what the measurement above shows.

## Credit and Licence

The packing is Doğa Özden’s, found from the registry’s 268 (Evan Daniel (found_by), after Chris Deotte; T-270, #914); the issue
asks that the improvement be credited to Özden, the base packing to its holders as the
record lists them, and the local optimizer to Evan Daniel.
The search was AI-assisted throughout, the checks were run by code that did not produce
the packing, and the issue and repository were prepared and posted by his AI agent; Özden
directed the work. The source starts from this repository’s regularized atlas and makes
its exact coordinates with this repository’s promotion tool, so its lineage builds on
this project. The bibliography key is **[Özden s268 upper bound 2026-11-09]**.

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
python -m devtools.acquire_source ozden-s268-upper-bound-2026-11-09 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s268-upper-bound-2026-11-09 --check
python -m devtools.upper_bound_reports ozden-s268-upper-bound-2026-11-09 check-claims --write
python -m devtools.upper_bound_reports ozden-s268-upper-bound-2026-11-09 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ozden-s268-upper-bound-2026-11-09 check --replay
python -m devtools.upper_bound_reports ozden-s268-upper-bound-2026-11-09 sharp-controls
python -m devtools.measure_identity --n 268 'OZDEN=packet:ozden-s268-upper-bound-2026-11-09' \
  'T-270=packet:evand-issue914-2026-11-05' \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-268-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-268.yaml' \
  --out resources/web/ozden-s268-upper-bound-2026-11-09/measure/identity.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
