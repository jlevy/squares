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
  about 10⁻¹².
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

- **172:** no symmetry pairs it one to one with T-257’s packing by nearest centres; the
  optimal assignment, under the identity, moves 15 squares beyond 0.1 and 69 beyond 0.01
  (largest 0.668426) and turns 58 squares by more than 10⁻⁶ radians, 15 of them by more
  than 1 degree and by up to 44.61 degrees, 9 of them to the other side of upright.
  Tilted beyond 1 degree: this packing 49, 36 turned one way and 13 the other; T-257 49,
  25 and 24. The house witness measures the same, and against the regularized view the
  source says it started from, the assignment moves 15 squares beyond 0.1 and 65 beyond
  0.01. So it is a further arrangement of T-257’s packing, though not one to one with it
  by nearest centres. The issue’s own counts (168 centres beyond 10⁻³, 15 squares
  re-tilted beyond 1 degree, largest move 0.668) agree with these.

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
least-gap pair of the replay). The measurement is `contraction_margin`’s, from the
module PR #934 adds; its receipts are not yet retained here.

## What Is Not Established

- **The stage 4 review.** A separate lane (L72, think-qqyg), blind to this one, reviews
  the certificate; until its review is mapped the case keeps its house, T-257, and the
  register entry T-282 stands at V3/C3 on this replay alone.
- **Human oversight.** No human oversight record is retained.
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
witness and its regularized view as they stand at main ef1af4933, before any adoption
replaces them, so it reproduces there:

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
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
