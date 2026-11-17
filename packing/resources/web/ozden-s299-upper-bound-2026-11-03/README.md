# Doğa Özden’s s(299) Certificate at 6486ead

This packet retains
[kenaznia-doga/s299-upper-bound](https://github.com/kenaznia-doga/s299-upper-bound/tree/6486ead9be5e3348f64ad39aecc1950f22910de4)
at `6486ead9be5e3348f64ad39aecc1950f22910de4` (committed 2026-11-03T18:57:22Z), the
repository’s one commit, which [issue #893](https://github.com/jlevy/squares/issues/893)
names 20 seconds later.
Doğa Özden’s AI agent, which uses the account kenaznia-doga, prepared and posted both on
his behalf.

## What the Source Claims

- `n-299-candidate.yaml`, a `packing.squares:Witness/v2` file (centre-basis, rational
  scalars, 299 squares), states s(299) ≤ 3560247706795812422293947620670679551/(2 ·
  10³⁵), which is 17.8012385339790622 rounded up at 16 places and 17.801238533980 at 12,
  and which the issue says is 1.54 × 10⁻⁸ below the record, Evan Daniel’s certificate of
  his update to issue #824 (T-258). It claims an upper bound only: no KKT,
  local-optimality, rigidity or global-optimality claim.
- The issue’s title and claim print the side as 17.801238533979, “rounded up at 12
  places”. That print is 6.21 × 10⁻¹⁴ **below** the exact side, which rounds up at 12
  places to 17.801238533980, so the print alone does not bound s(299). The issue also
  states the exact fraction, and the record holds that.
- `n299-refill2-t000173.json` is the lab’s export of the same squares.
  `packing-witness-verify.txt` is the author’s run of this repository’s
  `packing-witness verify` (VERIFIED, 44,551 pairs); `sqcheck-output.txt` and
  `sqcheck-output.json` are the author’s run of `verifier/sqcheck.py`, an exact checker
  the source says was written separately from this repository’s code (VALID, least pair
  margin about 1.0 × 10⁻²², walls touching).
  Those statements are the author’s; no source program ran here.
- The packing starts from the registry’s 299 as malyshevdanil’s Living Atlas on Kaggle
  carries it: about 250 of the 299 squares lie within 0.05 of it, the lower-right tilted
  corner is rebuilt, one square is re-tilted by 14.9°, the tilted set has 85 squares
  against 87, and the right-edge column is slid by about 0.5.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the whole tree, 9 files: 8 retained under [source/](source/) and 1 pinned
by digest.

| File | Bytes |
| --- | --- |
| `README.md` | 2,851 |
| `n-299-candidate.yaml` | 73,526 |
| `n299-refill2-t000173.json` | 85,033, stored as gzip (below) |
| `packing-witness-verify.txt` | 255 |
| `sqcheck-output.json` | 326 |
| `sqcheck-output.txt` | 82 |
| `verifier/README.md` | 3,441 |
| `verifier/sqcheck.py` | 17,047 |
| `records/n-299-candidate-diff.png` | 256,123, pinned by digest: a raster comparison that decides nothing |

The SHA-256s the issue and the source’s README state for `n-299-candidate.yaml`
(`2976d67f…76e0`) and `n299-refill2-t000173.json` (`4fac4ed1…b797`) are the files’.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is well under a megabyte, so it is kept in Git.

[licence/LICENSE.md](licence/LICENSE.md) is the one file kept from a later commit. The
lab added it at `0c61a5555d8dd9ec05019d4fd72672f5f502cf97` (committed
2026-11-04T17:48:56Z), the pin’s one successor, which adds that file and changes nothing
else: its tree is the pin’s with `LICENSE.md` added, so every file retained or pinned
here is unchanged under the licence. It is kept byte for byte, 1,484 bytes, Git blob
`9803370f8c382515d3769896adb8d04b201aebd6`, SHA-256
`5b8e14499bddd521ce875b7b1b30da6f7ea215f3c44e15cfabce3a493f18da4c`, and outside
`source/`, since the packet stays pinned at `6486ead`. The copies the lab added to its
s94 and s204 repositories the same minute are byte-identical.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `ca3a171bb` on 4 November
2026):

- **299:** exact side 17.8012385339790622…, below the case’s house (T-258, Evan Daniel,
  after Chris Deotte) by 1.54 × 10⁻⁸; no register bound pending adoption below the
  house.

## Report Order

The
[ledger of 4 November for this pass](../../../campaign/issue-intake/upper-bounds-893-895-20261104/README.md)
walks every report at 204, 260 and 299 in the order it reached this repository, from
starts frozen at `main` `ca3a171bb`, and records this packet’s claim at 299. The Kaggle
sources the issue names are no report: the dataset
kmmmvs/squares-in-squares-best-packings holds 299 at 17.801238553, above the house, and
the per-puzzle leaderboard’s side-only entries near 17.798 and 17.794 state no packing.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-258’s packing and wrote
[measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **299:** one to one with T-258’s packing under the identity by nearest centres; the
  optimal assignment moves 12 squares beyond 0.1 and 119 beyond 0.01 (largest 0.501947)
  and turns 71 squares by more than 10⁻⁶ radians, by up to 14.9 degrees.
  Tilted beyond 1 degree: this packing 85, T-258 87, all turned one way.
  So it is a further arrangement of T-258’s packing, one to one with it, and not a new
  arrangement.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 267,306 pair decisions, 31.0 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and the least pair gap is
99991899999991/10³⁶ = 9.9991899999991 × 10⁻²³, as the author’s `sqcheck` reports.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
1e-30 past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)). It lowered
the side by the least far-wall clearance, closed the least-gap pair by its gap, and
moved every square toward the nearer near wall by its least clearance: both routes
accepted each at contact with margin 0 and refused each past it.
It enlarged one square to its pair and one to its wall: both routes refused the first
at contact for its shape alone and accepted the second, already touching its wall and
so grown by zero, at contact; both refused each 1e-30 past it for the overlap or the
wall as well.
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
  the case adopted it at 299 that day; its programs and receipts are in
  [review/review-2026-11-04/](review/review-2026-11-04/README.md). No human oversight record is retained.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **The lineage** the source states, beyond what the measurement above shows.

## Credit and Licence

The packing is Doğa Özden’s, found from Evan Daniel’s packing at 299, after Chris
Deotte; the issue asks that the improvement be credited to Özden and the base packing to
its holders as the record lists them.
The search was AI-assisted (GPT-based agents plus local optimisation), the checks were
run by code that did not produce the packing, and the issue and repository were prepared
and posted by his AI agent; Özden directed the work.
The bibliography key is **[Özden s299 upper bound 2026-11-03]**.

The witness, the export, the checker outputs, the READMEs and the diff image are
published under CC BY 4.0, and `verifier/sqcheck.py` under the MIT licence, copyright
(c) 2026 Doğa Özden, as [licence/LICENSE.md](licence/LICENSE.md) states; it asks that
credit go to Doğa Özden, with the prior work the README cites. The lab announced the
choice on #890
([comment](https://github.com/jlevy/squares/issues/890#issuecomment-6637821113),
2026-11-04T17:49:05Z), answering the question of #893’s closing comment that
**think-mdxq** followed up. Until then every file retained under [source/](source/)
rested on the presumption of permission that an author’s own submission to this
repository carries (the owner, 24 October 2026, think-cnn7). The diff image is pinned by
digest only.
The [ozden-s204-upper-bound-2026-11-03](../ozden-s204-upper-bound-2026-11-03/README.md)
packet retains no `verifier/` of its own: it pins its byte-identical
`verifier/README.md` and `verifier/sqcheck.py` `identical_to` this packet’s copies, and
its own repository’s byte-identical `LICENSE.md` licenses them the same way.
The packing modifies Evan Daniel’s MIT-licensed certificate, whose notice the
[evand-n299-update-2026-10-29](../evand-n299-update-2026-10-29/README.md) packet
retains; the source carries no copy of that notice.

## Compressed Files

One upstream file of more than 1,000 lines, the lab’s JSON export, is stored as
deterministic gzip made by `gzip -9n`, with no file name or timestamp in the header.
The table gives the Git blob and SHA-256 of the decompressed bytes, and
`python -m devtools.retained_data check PACKET` re-derives every row.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `source/n299-refill2-t000173.json.gz` | upstream | `31bfb75709e499f3e44509bce80769ff0386569a` | `4fac4ed1b75eb0890935691045a0b395af2a762f8130bcd83cd4b3b83f0bb797` |

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source ozden-s299-upper-bound-2026-11-03 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s299-upper-bound-2026-11-03 --check
python -m devtools.upper_bound_reports ozden-s299-upper-bound-2026-11-03 check-claims --write
python -m devtools.upper_bound_reports ozden-s299-upper-bound-2026-11-03 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ozden-s299-upper-bound-2026-11-03 check --replay
python -m devtools.upper_bound_reports ozden-s299-upper-bound-2026-11-03 sharp-controls
python -m devtools.measure_identity --n 299 'OZDEN=packet:ozden-s299-upper-bound-2026-11-03' \
  'T-258=packet:evand-n299-update-2026-10-29' \
  --out resources/web/ozden-s299-upper-bound-2026-11-03/measure/identity.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
