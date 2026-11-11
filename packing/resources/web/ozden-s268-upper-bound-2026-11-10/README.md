# Doğa Özden’s s(268) Certificate at b027aba

This packet retains
[kenaznia-doga/s268-upper-bound-16872029849](https://github.com/kenaznia-doga/s268-upper-bound-16872029849/tree/b027aba9280d453ea075bd9b80694a5345257f4e)
at `b027aba9280d453ea075bd9b80694a5345257f4e` (committed 2026-11-10T15:27:50Z), the
repository’s one commit, which [issue #945](https://github.com/jlevy/squares/issues/945)
names 52 seconds later. Doğa Özden’s AI agent, which uses the account kenaznia-doga,
prepared and posted both on his behalf.

## What the Source Claims

- `n-268-candidate.yaml`, a `packing.squares:Witness/v2` file (corners, rational scalars,
  268 squares), bounds s(268) by its exact side, a fraction whose denominator has
  222 places and whose 16-place ceiling is 16.8720298490844502. #945 prints its 12-place
  ceiling, 16.872029849085, and says it is 4.400e-04 below the record, Evan Daniel's packing as Doğa Özden improved it (#928)
  (T-276). It claims an upper bound only: no KKT, local-optimality, rigidity or
  global-optimality claim.
- The exact coordinates were made by this repository’s own `packing-witness promote
  --strategy robust-rational` at `f54ad104` from the lab’s decimal pose,
  `n-268-decimal-pose.yaml`, which the witness’s `source.path` names, with
  `center_dilation: '1'` and no dilation. The issue says the pair margins of about
  2 × 10⁻¹³ are the decimal pose’s own, left by the final binary64 repair scaling of
  Evan Daniel’s quench, that only the squares that set the left wall, the bottom wall
  and the side touch them exactly, and that other squares near a wall clear it by up to
  about 10⁻¹².
- `n268-witness.json` is the same file as JSON. `packing-witness-verify.txt` is the
  author’s run of this repository’s `packing-witness verify` at `f54ad104` (VERIFIED,
  35,778 pairs); `sqcheck-output.txt` is the author’s run of `verifier/sqcheck.py`, an
  exact checker the source says was written separately from this repository’s code
  (VALID, exact rational, the exact side rounded up). The issue says the two share only
  the unit-square, wall and non-overlap definitions, that `packing-witness verify` is not
  independent of how the coordinates were rounded, and that `sqcheck.py` certified the
  decimal pose in interval arithmetic at its own side before promotion.
  Those statements are the author’s; no source program ran here.
- The issue says the packing was found by AI-run transplant search: seeds built from
  neighbouring counts’ registry packings, quenched with Evan Daniel’s ALM+SLP code from
  [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT,
  at `bb4cc78e`), then basin hopping over the quench’s local minima. Its seed was the
  registry’s 302 (PingYou Ltd, improved by Francisco Couzo, Mishapolk and Evan Daniel; side 17.870013850404464; [Daniel exact current records 2026-10-16]),
  seed type C+1, a horizontal and a vertical unit-wide strip cut out and closed up, the count then fixed to 268, then quenched; the hit came from the basin-hopping stage
  (chain 1, trial 218, move aswap). Against the registry packing, matched by assignment up to the square’s
  symmetries, it reports 230 of 268 centres beyond 1e-3, 130 beyond 0.05 (largest 1.041), 111 squares re-tilted beyond 1 degree (largest 43.99), 43 squares tilted beyond 0.5 degree against the record's 99.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the whole tree, 11 files: 7 retained under
[source/](source/) and 4 pinned by digest.

| File | Bytes |
| --- | --- |
| `LICENSE.md` | 1,484 |
| `README.md` | 5,362 |
| `n-268-candidate.yaml` | 863,734 |
| `n-268-decimal-pose.yaml` | 29,352, the decimal pose the witness was promoted from |
| `n268-witness.json` | 855,465, the same packing as JSON, which the reader holds equal to the YAML |
| `packing-witness-verify.txt` | 627 |
| `sqcheck-output.txt` | 101 |
| `LICENSE-evand-square-packing.txt` | 1,068, pinned against the identical copy of Evan Daniel’s MIT notice the [evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains |
| `records/n-268-candidate-diff.png` | 296,695, pinned by digest: a raster comparison that decides nothing |
| `verifier/README.md` | 3,441, pinned against the identical copy the [3 November s299 packet](../ozden-s299-upper-bound-2026-11-03/README.md) retains |
| `verifier/sqcheck.py` | 17,654, pinned against the identical copy the [9 November s232 packet](../ozden-s232-upper-bound-2026-11-09/README.md) retains, never executed here |

The SHA-256s the issue states for `n-268-candidate.yaml` and the README states for it and
for `n268-witness.json` are the files’.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is under two megabytes in a checkout and far less as Git stores it, so it is
kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `f54ad1048` on 11 November
2026):

- **268:** exact side 16.8720298490844502 rounded up at 16 places, below the case’s house
  (T-276, the author's own #928 packing) by 4.400e-04, as the issue states.

## Report Order

The [ledger of 11 November for this lane](../../../campaign/issue-intake/upper-bounds-943-947-20261111/README.md) walks every report at 268 in the
order it reached this repository, from starts frozen at `main` `f54ad1048`, and records
this packet’s claim at 268. The best public Kaggle per-puzzle packing the issue quotes at
268, 16.874361715873 (ntumlnoob), is above this. The issue also quotes a side-only Kaggle leaderboard entry at 268, 16.871868135138 (team Cats and boxes, 28 October), which the issue states first and says is 1.617e-4 below this side; it states no packing, so it is no report.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-276’s packing, the
house witness and the regularized view, and wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **268:** no symmetry of the box pairs it one to one with T-276’s packing by
  nearest centres. The optimal assignment, under the best of the box’s eight symmetries,
  moves 125 squares beyond 0.1 and 151 beyond 0.01
  (largest 1.04105) and turns 156 squares by more than 10⁻⁶
  radians, by up to 43.99 degrees. Tilted beyond 1 degree: this packing
  43, 17 turned one way and 26 the other;
  T-276 99, all turned the same way. The house witness
  measures the same, and against the regularized view the assignment moves
  118 squares beyond 0.1. So it is not a further arrangement of
  T-276’s packing; the issue names another count’s packing, the registry’s 302, as
  its seed, which this measurement does not reach. The issue’s own counts against the house (230 centres beyond 1e-3, 111 squares re-tilted beyond a degree, largest move 1.041) are this measurement’s.

Its side is 3.27 × 10⁻¹² above 16.872029849081179973, which is 16 plus the first 18 decimal places that the exact sides of Evan Daniel’s certificates at 129, 153 and 302 share (T-145), and contracted to first contact (below) it is 6.6 × 10⁻¹⁴ above it. The issue names the registry’s 302 as its seed. Whether the packing shares the structure of those certificates is not measured here.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 214,668 pair decisions, 80.57 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 2.01e-13. `check --replay` decided the three jobs again.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
10⁻³⁰ past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)), with the
expected verdicts stated before it ran. It lowered the side by the least far-wall
clearance, closed the least-gap pair by its gap, and moved every square toward the
nearer near wall by its least clearance: both routes accepted each at contact with
margin 0 and refused each past it.
It enlarged one square to its pair and one to its wall: both routes refused the first at
contact for its shape alone and accepted the second, which already touches its wall and
so grew by 0, at contact; both refused each 10⁻³⁰ past it for the overlap or the wall as
well. Both refused a duplicated square.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read the witness through the `witness-corners`
reader. The first route is the `packing-witness verify` the author ran on the same file,
so on that route the replay is reproduced with the producer’s code; the second shares no
verification code with it. Neither is independent of this repository’s `packing-witness
promote`, which made the coordinates. The source’s own `sqcheck.py` was not run.

## The Gain Against Padding

T-276’s certificate, contracted uniformly about the origin to first contact and
boxed, loses 3.193e-12 of side (1 − λ\* = 2.012182e-13); the gain this certificate
states, 4.400e-04, is about 1.4e08 times that margin, so no share of it worth stating is the
house’s padding, and the owner’s open question about gains inside a padding margin (RV-3,
think-ruu2) does not reach it. This certificate’s own margin, measured the same way, is
3.204e-12 (1 − λ\* = 2.018950e-13, the binding pair the least-gap pair of the replay).
`devtools.contraction_margin` wrote both receipts,
[measure/contraction-n268.json](measure/contraction-n268.json) and
[measure/contraction-n268-own.json](measure/contraction-n268-own.json), each contracted
packing decided on both maintained routes.

## The L Step

`devtools.l_step_scan`, with this side and the lane’s other three stood in for their
ceilings, finds the same L-step and monotonicity consequences as on `main`: this bound
carries to no other count
([the receipt in the s156 packet](../ozden-s156-upper-bound-2026-11-10/measure/l-step-scan.json)).

## Stage 4 Review and Adoption

The stage 4 mathematical review is written in a separate lane, blind to this one, and is
not yet mapped. The case’s verified lane and the adoption of this certificate as the
house at 268 in place of T-276 wait on its acceptance (the house rule), with both strong
generators’ regularization of the new house in the same change.

## What Is Not Established

- **Human oversight.** No review is mapped yet; no human oversight record.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **The lineage** the source states, beyond what the measurement above shows.

## Credit and Licence

The packing is Doğa Özden’s; the issue asks that the improvement be credited to Özden,
the seed packing and the current record to their holders as the registry lists them, and
the local optimizer to Evan Daniel.
The issue says the search and its code were written and run by AI agents throughout and
that the checks were run by code that did not produce the packing; it says the issue and
repository were prepared and posted by his AI agent, and that Özden directed the work.
The source starts from this repository’s registry packings and makes its exact
coordinates with this repository’s promotion tool, so its lineage builds on this project.
The bibliography key is **[Özden s268 upper bound 2026-11-10]**.

The witness, the JSON, the decimal pose, the checker outputs, the README and the diff
image are published under CC BY 4.0, and `verifier/sqcheck.py` under the MIT licence,
copyright (c) 2026 Doğa Özden, as [source/LICENSE.md](source/LICENSE.md) states; it is
byte-identical to the `LICENSE.md` the lab added to its s299, s204 and s94 repositories
on 4 November 2026 and announced on #890
([comment](https://github.com/jlevy/squares/issues/890#issuecomment-6637821113)).
The diff image is pinned by digest only. The source carries Evan Daniel’s MIT notice as
`LICENSE-evand-square-packing.txt`, for his quench code and the certificates his
packings come from, byte-identical to the `LICENSE` the
[evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains, and
pinned against it.

## Commands

From `packing/`, with the project interpreter. The identity measurement reads the house
witness and its regularized view as they stand at main f54ad1048, so it reproduces there
until an adoption replaces them; the contraction margins read the packets and reproduce
anywhere `devtools.contraction_margin` is:

```bash
python -m devtools.acquire_source ozden-s268-upper-bound-2026-11-10 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s268-upper-bound-2026-11-10 --check
python -m devtools.upper_bound_reports ozden-s268-upper-bound-2026-11-10 check-claims --write
python -m devtools.upper_bound_reports ozden-s268-upper-bound-2026-11-10 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ozden-s268-upper-bound-2026-11-10 check --replay
python -m devtools.upper_bound_reports ozden-s268-upper-bound-2026-11-10 sharp-controls
python -m devtools.measure_identity --n 268 'OZDEN=packet:ozden-s268-upper-bound-2026-11-10' \
  'T-276=packet:ozden-s268-upper-bound-2026-11-09' \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-268-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-268.yaml' \
  --out resources/web/ozden-s268-upper-bound-2026-11-10/measure/identity.json
python -m devtools.contraction_margin --n 268 'T-276=packet:ozden-s268-upper-bound-2026-11-09' \
  --against 'ozden-945=packet:ozden-s268-upper-bound-2026-11-10' \
  --out resources/web/ozden-s268-upper-bound-2026-11-10/measure/contraction-n268.json
python -m devtools.contraction_margin --n 268 'ozden-945=packet:ozden-s268-upper-bound-2026-11-10' \
  --out resources/web/ozden-s268-upper-bound-2026-11-10/measure/contraction-n268-own.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
