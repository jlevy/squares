# Doğa Özden’s s(204) Certificate at d4b8b05

This packet retains
[kenaznia-doga/s204-upper-bound](https://github.com/kenaznia-doga/s204-upper-bound/tree/d4b8b05c45e3be464476c94712a4dbc063009875)
at `d4b8b05c45e3be464476c94712a4dbc063009875` (committed 2026-11-03T22:35:57Z), the
repository’s one commit, which [issue #894](https://github.com/jlevy/squares/issues/894)
names 16 seconds later.
Doğa Özden’s AI agent, which uses the account kenaznia-doga, prepared and posted both on
his behalf.

## What the Source Claims

- `n-204-candidate.yaml`, a `packing.squares:Witness/v2` file (centre-basis, rational
  scalars, 204 squares), states s(204) ≤ 7403810497792604009019579959/(5 · 10²⁶) =
  14.807620995585208…, printed 14.807620995586 rounded up at 12 places, which the issue
  says is 6.48 × 10⁻⁶ below the record, Evan Daniel’s #845 certificate (T-257). It
  claims an upper bound only: no KKT, local-optimality, rigidity or global-optimality
  claim.
- `n204-witness.json` holds the same squares as plain JSON. `packing-witness-verify.txt`
  is the author’s run of this repository’s `packing-witness verify` at `e6e8d577`
  (VERIFIED, 20,706 pairs); `sqcheck-output.txt` is the author’s run of
  `verifier/sqcheck.py`, an exact checker the source says was written separately from
  this repository’s code (VALID, exact rational).
  Those statements are the author’s; no source program ran here.
- The packing starts from the registry’s 204, whose lineage Daniel states starts at
  Daniil Ostashev’s s(176) packing (#575): 24 squares move by more than 0.05, 14 are
  re-tilted by more than 1° (largest 25.6°), and the tilted set has 76 squares against
  79\.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the whole tree, 8 files: 5 retained under [source/](source/) and 3 pinned
by digest.

| File | Bytes |
| --- | --- |
| `README.md` | 2,350 |
| `n-204-candidate.yaml` | 43,179 |
| `n204-witness.json` | 40,159 |
| `packing-witness-verify.txt` | 237 |
| `sqcheck-output.txt` | 74 |
| `records/n-204-candidate-diff.png` | 352,144, pinned by digest: a raster comparison that decides nothing |
| `verifier/README.md` | 3,441, pinned against the identical copy the [s299 packet](../ozden-s299-upper-bound-2026-11-03/README.md) retains |
| `verifier/sqcheck.py` | 17,047, pinned the same way, never executed here |

The SHA-256s the issue and the source’s README state for `n-204-candidate.yaml`
(`e3c8c7eb…eeb8`) and `n204-witness.json` (`613c0a66…af45`) are the files’.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The two pinned copies are the s299 packet’s, under the same licence.
The packet is well under a megabyte, so it is kept in Git.

[licence/LICENSE.md](licence/LICENSE.md) is the one file kept from a later commit. The
lab added it at `06b0bf99fda02c9521e21fdd7b970fb6d0cb44ef` (committed
2026-11-04T17:48:57Z), the pin’s one successor, which adds that file and changes nothing
else: its tree is the pin’s with `LICENSE.md` added, so every file retained or pinned
here is unchanged under the licence. It is kept byte for byte, 1,484 bytes, Git blob
`9803370f8c382515d3769896adb8d04b201aebd6`, SHA-256
`5b8e14499bddd521ce875b7b1b30da6f7ea215f3c44e15cfabce3a493f18da4c`, and outside
`source/`, since the packet stays pinned at `d4b8b05`. The copies the lab added to its
s94 and s299 repositories the same minute are byte-identical.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `ca3a171bb` on 4 November
2026):

- **204:** exact side 14.8076209955852081…, below the case’s house (T-257, Evan Daniel,
  from a search seeded with Daniil Ostashev’s n = 176 packing) by 6.48 × 10⁻⁶; no
  register bound pending adoption below the house.

## Report Order

The
[ledger of 4 November for this pass](../../../campaign/issue-intake/upper-bounds-893-895-20261104/README.md)
walks every report at 204, 260 and 299 in the order it reached this repository, from
starts frozen at `main` `ca3a171bb`, and records this packet’s claim at 204. The tie
that think-pg1y records at 204, between Mykhailo Polkovskyi’s certificate of 23 October
and T-231, lies above T-257 and does not reach this claim.
The Kaggle sources the issue names are no report: the dataset
kmmmvs/squares-in-squares-best-packings holds 204 at 14.807627474, above the house, and
the per-puzzle leaderboard’s side-only 14.803489183116 (Cats and boxes, 27 October
2026), which #845 quoted, states no packing.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-257’s packing and wrote
[measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **204:** one to one with T-257’s packing under the identity by nearest centres; the
  optimal assignment moves 6 squares beyond 0.1 and 81 beyond 0.01 (largest 0.18968) and
  turns 87 squares by more than 10⁻⁶ radians, 14 of them by more than 1 degree and by
  up to 25.58 degrees.
  Tilted beyond 1 degree: this packing 76, T-257 79, none reversed.
  So it is a further arrangement of T-257’s packing, one to one with it, and not a new
  arrangement.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 124,236 pair decisions, 14.4 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Every wall clears by at least 9.99 × 10⁻¹⁸ and every pair by at least 9.99 × 10⁻¹⁸.

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
and the separating-axis method, and read the witness through the `witness-center-basis`
reader. The first route is the `packing-witness verify` the author ran, so on that
route the replay is reproduced with the producer’s code; the second shares with it only
this repository’s centre-basis reader and is independently re-implemented (F6 and F9 of
the stage 4 review).
The source’s own `sqcheck.py` was not run.

## What Is Not Established

- **Human oversight.** The stage 4 mathematical review of 4 November 2026
  ([review-2026-11-04-ozden-893-894-299-204.md](../../../../docs/project/reviews/review-2026-11-04-ozden-893-894-299-204.md)),
  by a strong-tier lane sharing no context with this one, accepted the certificate and
  the case adopted it at 204 that day; its programs and receipts are in
  the 299 packet’s and, at 204, [review/review-2026-11-04/](review/review-2026-11-04/README.md). No human oversight record is retained.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **The lineage** the source states, beyond what the measurement above shows.

## Credit and Licence

The packing is Doğa Özden’s, started from Evan Daniel’s packing at 204, from his search
seeded with Daniil Ostashev’s s(176); the issue asks that the improvement be credited to
Özden and the base packing to its holders as the record lists them.
The search was AI-assisted, the checks were run by code that did not produce the
packing, and the issue and repository were prepared and posted by his AI agent; Özden
directed the work. The bibliography key is **[Özden s204 upper bound 2026-11-03]**.

The witness, the JSON, the checker outputs, the READMEs and the diff image are
published under CC BY 4.0, and `verifier/sqcheck.py` under the MIT licence, copyright
(c) 2026 Doğa Özden, as [licence/LICENSE.md](licence/LICENSE.md) states; it asks that
credit go to Doğa Özden, with the prior work the README cites. The lab announced the
choice on #890
([comment](https://github.com/jlevy/squares/issues/890#issuecomment-6637821113),
2026-11-04T17:49:05Z), answering the question of #894’s closing comment that
**think-mdxq** followed up. Until then every file retained under [source/](source/)
rested on the presumption of permission that an author’s own submission to this
repository carries (the owner, 24 October 2026, think-cnn7). The diff image is pinned by
digest only. `verifier/README.md` and `verifier/sqcheck.py` are not retained here: they
are pinned `identical_to` the byte-identical copies the
[ozden-s299-upper-bound-2026-11-03](../ozden-s299-upper-bound-2026-11-03/README.md)
packet retains, under the same licence.
The packing modifies Evan Daniel’s MIT-licensed certificate, whose notice the
[evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains; the
source carries no copy of that notice.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source ozden-s204-upper-bound-2026-11-03 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s204-upper-bound-2026-11-03 --check
python -m devtools.upper_bound_reports ozden-s204-upper-bound-2026-11-03 check-claims --write
python -m devtools.upper_bound_reports ozden-s204-upper-bound-2026-11-03 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ozden-s204-upper-bound-2026-11-03 check --replay
python -m devtools.upper_bound_reports ozden-s204-upper-bound-2026-11-03 sharp-controls
python -m devtools.measure_identity --n 204 'OZDEN=packet:ozden-s204-upper-bound-2026-11-03' \
  'T-257=packet:evand-issue845-2026-10-29' \
  --out resources/web/ozden-s204-upper-bound-2026-11-03/measure/identity.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
