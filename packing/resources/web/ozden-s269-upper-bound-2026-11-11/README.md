# Doğa Özden’s s(269) Certificate at 6f93b07

This packet retains
[kenaznia-doga/s269-upper-bound](https://github.com/kenaznia-doga/s269-upper-bound/tree/6f93b07eac91e5f7b299c9a6420041d9a695a478)
at `6f93b07eac91e5f7b299c9a6420041d9a695a478` (committed 2026-11-11T03:34:54Z), the
repository’s one commit, which [issue #947](https://github.com/jlevy/squares/issues/947)
names 13 seconds later. Doğa Özden’s AI agent, which uses the account kenaznia-doga,
prepared and posted both on his behalf.

## What the Source Claims

- `n-269-candidate.yaml`, a `packing.squares:Witness/v2` file (corners, rational scalars,
  269 squares), bounds s(269) by its exact side, a fraction whose denominator has
  215 places and whose 16-place ceiling is 16.9009945799513249. #947 prints its 12-place
  ceiling, 16.900994579952, and says it is 5.190e-04 below the record, Nate Chaoweeraprasit's SQUISH packing, improved by Evan Daniel and PingYou Ltd
  (T-174). It claims an upper bound only: no KKT, local-optimality, rigidity or
  global-optimality claim.
- The exact coordinates were made by this repository’s own `packing-witness promote
  --strategy robust-rational` at `f54ad104` from the lab’s decimal pose,
  `n-269-decimal-pose.yaml`, which the witness’s `source.path` names, with
  `center_dilation: '1'` and no dilation. The issue says the pair margins of about
  2 × 10⁻¹³ are the decimal pose’s own, left by the final binary64 repair scaling of
  Evan Daniel’s quench, that only the squares that set the left wall, the bottom wall
  and the side touch them exactly, and that other squares near a wall clear it by up to
  about 10⁻¹².
- `n269-witness.json` is the same file as JSON. `packing-witness-verify.txt` is the
  author’s run of this repository’s `packing-witness verify` at `f54ad104` (VERIFIED,
  36,046 pairs); `sqcheck-output.txt` is the author’s run of `verifier/sqcheck.py`, an
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
  registry’s 304 (Evan Daniel; side 17.920944093340243; [Daniel issue 914 2026-11-05]),
  seed type Cm, a horizontal and a vertical unit-wide strip cut out and closed up at a random position, one of the most crowded squares deleted to reach 269 (the issue says the sibling seed type Lm, an L cut from the same donor, reached the same final packing), then quenched; the hit came from the basin-hopping stage
  (chain 0, trials 204, 205 and 212, the last the witness filed, move crot). Against the registry packing, matched by assignment up to the square’s
  symmetries, it reports 237 of 269 centres beyond 1e-3, 117 beyond 0.05 (largest 1.103), 109 squares re-tilted beyond 1 degree (largest 43.52), 100 squares tilted beyond 0.5 degree against the record's 49.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the whole tree, 11 files: 7 retained under
[source/](source/) and 4 pinned by digest.

| File | Bytes |
| --- | --- |
| `LICENSE.md` | 1,484 |
| `README.md` | 5,572 |
| `n-269-candidate.yaml` | 828,609 |
| `n-269-decimal-pose.yaml` | 30,005, the decimal pose the witness was promoted from |
| `n269-witness.json` | 820,311, the same packing as JSON, which the reader holds equal to the YAML |
| `packing-witness-verify.txt` | 613 |
| `sqcheck-output.txt` | 101 |
| `LICENSE-evand-square-packing.txt` | 1,068, pinned against the identical copy of Evan Daniel’s MIT notice the [evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains |
| `records/n-269-candidate-diff.png` | 316,521, pinned by digest: a raster comparison that decides nothing |
| `verifier/README.md` | 3,441, pinned against the identical copy the [3 November s299 packet](../ozden-s299-upper-bound-2026-11-03/README.md) retains |
| `verifier/sqcheck.py` | 17,654, pinned against the identical copy the [9 November s232 packet](../ozden-s232-upper-bound-2026-11-09/README.md) retains, never executed here |

The SHA-256s the issue states for `n-269-candidate.yaml` and the README states for it and
for `n269-witness.json` are the files’.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is under two megabytes in a checkout and far less as Git stores it, so it is
kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `f54ad1048` on 11 November
2026):

- **269:** exact side 16.9009945799513249 rounded up at 16 places, below the case’s house
  (T-174, Nate Chaoweeraprasit's SQUISH packing) by 5.190e-04, as the issue states.

## Report Order

The [ledger of 11 November for this lane](../../../campaign/issue-intake/upper-bounds-943-947-20261111/README.md) walks every report at 269 in the
order it reached this repository, from starts frozen at `main` `f54ad1048`, and records
this packet’s claim at 269. The best public Kaggle per-puzzle packing the issue quotes at
269, 16.901513582205 (kirilltym), is above this. The issue also quotes a side-only Kaggle leaderboard entry at 269, 16.889730079125 (team elegans, 5 November), which the issue states first and says is 1.126e-2 below this side; it states no packing, so it is no report.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-174’s packing, the
house witness and the regularized view, and wrote [measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **269:** no symmetry of the box pairs it one to one with T-174’s packing by
  nearest centres. The optimal assignment, under the best of the box’s eight symmetries,
  moves 112 squares beyond 0.1 and 134 beyond 0.01
  (largest 1.10268) and turns 120 squares by more than 10⁻⁶
  radians, by up to 43.52 degrees. Tilted beyond 1 degree: this packing
  100, all turned the same way;
  T-174 49, 25 turned one way and 24 the other. The house witness
  measures the same, and against the regularized view the assignment moves
  112 squares beyond 0.1. So it is not a further arrangement of
  T-174’s packing; the issue names another count’s packing, the registry’s 304, as
  its seed, which this measurement does not reach. The issue’s own counts against the house (237 centres beyond 1e-3, 109 squares re-tilted beyond a degree, largest move 1.103) are this measurement’s.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 216,276 pair decisions, 95.39 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 2.03e-13. `check --replay` decided the three jobs again.

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

T-174’s certificate, contracted uniformly about the origin to first contact and
boxed, loses 0.000e+00 of side (1 − λ\* = 0.000000e+00); the gain this certificate
states, 5.190e-04, is the house certificate has no padding to measure: a pair already touches, so no share of it worth stating is the
house’s padding, and the owner’s open question about gains inside a padding margin (RV-3,
think-ruu2) does not reach it. This certificate’s own margin, measured the same way, is
3.238e-12 (1 − λ\* = 2.036494e-13, the binding pair the least-gap pair of the replay).
`devtools.contraction_margin` wrote both receipts,
[measure/contraction-n269.json](measure/contraction-n269.json) and
[measure/contraction-n269-own.json](measure/contraction-n269-own.json), each contracted
packing decided on both maintained routes.

## The L Step

`devtools.l_step_scan`, with this side and the lane’s other three stood in for their
ceilings, finds the same L-step and monotonicity consequences as on `main`: this bound
carries to no other count
([the receipt in the s156 packet](../ozden-s156-upper-bound-2026-11-10/measure/l-step-scan.json)).

## Stage 4 Review and Adoption

The stage 4 mathematical review is written in a separate lane, blind to this one, and is
not yet mapped. The case’s verified lane and the adoption of this certificate as the
house at 269 in place of T-174 wait on its acceptance (the house rule), with both strong
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
The bibliography key is **[Özden s269 upper bound 2026-11-11]**.

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
python -m devtools.acquire_source ozden-s269-upper-bound-2026-11-11 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s269-upper-bound-2026-11-11 --check
python -m devtools.upper_bound_reports ozden-s269-upper-bound-2026-11-11 check-claims --write
python -m devtools.upper_bound_reports ozden-s269-upper-bound-2026-11-11 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ozden-s269-upper-bound-2026-11-11 check --replay
python -m devtools.upper_bound_reports ozden-s269-upper-bound-2026-11-11 sharp-controls
python -m devtools.measure_identity --n 269 'OZDEN=packet:ozden-s269-upper-bound-2026-11-11' \
  'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  'regularized=witness-corners:atlas/known-best/regularized/n-269-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-269.yaml' \
  --out resources/web/ozden-s269-upper-bound-2026-11-11/measure/identity.json
python -m devtools.contraction_margin --n 269 'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  --against 'ozden-947=packet:ozden-s269-upper-bound-2026-11-11' \
  --out resources/web/ozden-s269-upper-bound-2026-11-11/measure/contraction-n269.json
python -m devtools.contraction_margin --n 269 'ozden-947=packet:ozden-s269-upper-bound-2026-11-11' \
  --out resources/web/ozden-s269-upper-bound-2026-11-11/measure/contraction-n269-own.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
