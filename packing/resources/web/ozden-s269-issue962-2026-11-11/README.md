# Doğa Özden’s s(269) Certificate at fdab2c0

This packet retains
[kenaznia-doga/s269-upper-bound-16899469076](https://github.com/kenaznia-doga/s269-upper-bound-16899469076/tree/fdab2c0073ea91701d0d8429663faa6e5c7f831f)
at `fdab2c0073ea91701d0d8429663faa6e5c7f831f` (committed 2026-11-11T23:34:47Z), the
repository’s one commit, which [issue #962](https://github.com/jlevy/squares/issues/962)
names 17 seconds later.
Doğa Özden’s AI agent, which uses the account kenaznia-doga, prepared and posted both on
his behalf, and six seconds after the issue it pointed to it from his earlier issue at
this count
([#947, comment](https://github.com/jlevy/squares/issues/947#issuecomment-6809799112)).

## What the Source Claims

- `n-269-candidate.yaml`, a `packing.squares:Witness/v2` file (corners, rational
  scalars, 269 squares), bounds s(269) by its exact side, a fraction whose denominator
  has 217 places and whose 16-place ceiling is 16.8994690758550466. #962 prints its
  12-place ceiling, 16.899469075856, and says it is 1.526e-03 below the record, T-290,
  the author’s own #947 certificate, which it calls a further improvement of that
  record. The issue and README also print the exact side as 16.8994690758550465, the side
  truncated at 16 places, 2.72 × 10⁻¹⁷ below it.
  It claims an upper bound only: no KKT, local-optimality, rigidity or global-optimality
  claim.
- The exact coordinates were made by this repository’s own `packing-witness promote
  --strategy robust-rational` at `0af33d85` from the lab’s decimal pose,
  `n-269-decimal-pose.yaml`, which the witness’s `source.path` names, with
  `center_dilation: '1'` and no dilation.
  The issue says the pair margins of about 2 × 10⁻¹³ are the decimal pose’s own, left by
  the final binary64 repair scaling of Evan Daniel’s quench (about 10⁻¹³ relative), that
  only the squares that set the left wall, the bottom wall and the side touch them
  exactly, and that other squares near a wall clear it by up to about 10⁻¹². Measured
  here, 11 squares touch a wall exactly: square 103 at the bottom, square 155 at the
  top, which sets the side, and nine squares, 158 and 160 to 167, that share the least x
  and so set the left wall.
  Of the other square–wall clearances, 25 are below 10⁻¹² and at most 1.53 × 10⁻¹⁵, and
  25 lie between 9.7 × 10⁻⁸ and 7.1 × 10⁻⁴.
- `n269-witness.json` is the same file as JSON. `packing-witness-verify.txt` is the
  author’s run of this repository’s `packing-witness verify` at `0af33d85` (VERIFIED,
  36,046 pairs); `sqcheck-output.txt` is the author’s run of `verifier/sqcheck.py`, an
  exact checker the source says was written separately from this repository’s code
  (VALID, exact rational, the exact side rounded up).
  The issue says the two share only the unit-square, wall and non-overlap definitions,
  that `packing-witness verify` is not independent of how the coordinates were rounded,
  and that `sqcheck.py` certified the decimal pose in interval arithmetic at its own
  side before promotion.
  Those statements are the author’s; no source program ran here.
- The issue says the packing was found by an AI-run band-design search, new for this
  filing, the one #954 and #960 described at 179 and 237: tilted squares from registry
  or own packings of the same family laid along the diagonal as a seed band; simulated
  annealing in a reduced model in which the tilted squares move freely and the
  axis-parallel squares sit on the two wall-anchored staircase lattices, present or
  absent, with the overlap of the squares that must be kept as energy; then a quench
  with Evan Daniel’s ALM+SLP code from
  [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT,
  at `bb4cc78e`). The band is built from tilted squares of three clusters: the second
  cluster of the registry’s n = 207 packing (`207b`), the cluster of the registry’s n =
  70 packing (`70a`; Ryan Xu, improved by Evan Daniel and PingYou Ltd) and the first
  cluster of the lab’s own n = 179 band packing of #954 (`179ha`), each reflected in the
  main diagonal of its box (symmetry 2; shifts (0, 0), (0, 0) and (3, 3)) and rotated to
  a lean of 2.55 degrees, 45 tilted squares at band parameter 0.899; annealed at that
  side (2 × 10⁷ moves, energy 0.0719) and quenched once to 16.899469084224, then kicked
  (sigma 0.0031) and quenched to 16.899469075879 18 seconds later in the same job, then
  kicked again (sigma 0.0296) and quenched, 3 seconds after that, to the filed side.
  The issue counts 46 tilted squares against the record’s 100, 16 of them at −42.88
  degrees, and says it is not one clean band.
  Against the registry packing, matched by assignment up to the square’s symmetries, it
  reports 262 of 269 centres beyond 1e-3, 124 beyond 0.05 (largest 1.456), 116 squares
  re-tilted beyond 1 degree (largest 44.77), and 46 squares tilted beyond 0.5 degree
  against the record’s 100.
- The issue describes the record, T-290, in two ways: in its claim paragraph as “built
  from Nate Chaoweeraprasit’s packing (itsnaka) improved by Evan Daniel and PingYou
  Ltd”, and in its lineage paragraph as found by transplanting Evan Daniel’s n = 304
  packing. The register records T-290 as the second: a strip cut of Evan Daniel’s 304,
  below T-174, Nate Chaoweeraprasit’s packing as Evan Daniel and PingYou Ltd improved
  it, which was the house before it.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the whole tree, 11 files: 7 retained under [source/](source/) and 4 pinned
by digest.

| File | Bytes |
| --- | --- |
| `LICENSE.md` | 1,484 |
| `README.md` | 7,213 |
| `n-269-candidate.yaml` | 611,228 |
| `n-269-decimal-pose.yaml` | 27,608, the decimal pose the witness was promoted from |
| `n269-witness.json` | 602,860, the same packing as JSON, which the reader holds equal to the YAML |
| `packing-witness-verify.txt` | 617 |
| `sqcheck-output.txt` | 101 |
| `LICENSE-evand-square-packing.txt` | 1,068, pinned against the identical copy of Evan Daniel’s MIT notice the [evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains |
| `records/n-269-candidate-diff.png` | 304,992, pinned by digest: a raster comparison that decides nothing |
| `verifier/README.md` | 3,441, pinned against the identical copy the [3 November s299 packet](../ozden-s299-upper-bound-2026-11-03/README.md) retains |
| `verifier/sqcheck.py` | 17,654, pinned against the identical copy the [9 November s232 packet](../ozden-s232-upper-bound-2026-11-09/README.md) retains, never executed here |

The SHA-256s the issue states for `n-269-candidate.yaml` and the README states for it
and for `n269-witness.json` are the files’.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is about 1.4 megabytes in a checkout and far less as Git stores it, so it is
kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `75cce00b6` on 12
November 2026):

- **269:** exact side 16.8994690758550466 rounded up at 16 places, below the case’s
  house (T-290, Doğa Özden’s own certificate of #947) by 1.526e-03, as the issue states,
  and below T-174, the house before it, by 2.045e-03. No register bound is pending
  adoption at 269.

## Report Order

The
[ledger of 12 November for this lane](../../../campaign/issue-intake/upper-bounds-962-20261112/README.md)
walks every report at 269 in the order it reached this repository, from a start frozen
at `main` `75cce00b6`, and records this packet’s claim at 269. The best public Kaggle
per-puzzle packing the issue quotes at 269, 16.901513582205 (kirilltym), is above this.
The issue also quotes, and states first, a side-only Kaggle leaderboard entry at 269,
16.889730079125 (team elegans, 5 November), 9.74e-3 below this side.
It is unpublished and states no packing, so it is no report and is recorded as context
only.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-290’s packing, T-174’s,
the house witness and the regularized view, and wrote
[measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **269:** no symmetry of the box pairs it one to one with T-290’s packing by nearest
  centres. The optimal assignment, under the best of the box’s eight symmetries, moves
  every square beyond 10⁻⁶, 230 beyond 10⁻³, 134 beyond 0.01 and 115 beyond 0.1 (largest
  1.12355), and turns 149 squares by more than 10⁻⁶ radians, by up to 44.77 degrees;
  aligned by box centres, 116 squares turn by more than a degree, as the issue says.
  Tilted beyond a degree: 45 here, 39.53 to 44.77 degrees from upright, 22 turned one
  way and 23 the other, with one more at 0.55 degrees, so 46 beyond half a degree, as
  the issue says, 16 of them within 0.01 degrees of −42.88; T-290’s 100, 18.70 to 36.11
  degrees, all turned one way.
  The house witness, as it stood before this adoption, measures the same, and its
  regularized view, a drawing of T-290’s packing at its side, the same but for 112
  squares beyond a tenth.
  So it is a new arrangement relative to T-290’s packing, not a further arrangement of
  it.
- **Against T-174**, the house before T-290, it is new as well: no symmetry pairs
  nearest centres one to one, and the optimal assignment moves 65 squares beyond a tenth
  (largest 0.928203); aligned by box centres, 70 squares turn by more than a degree.
  T-174 has 49 squares tilted beyond a degree, 33.99 to 44.87 degrees, 25 one way and 24
  the other.
- The issue’s own counts (262 of 269 beyond 10⁻³, 124 beyond 0.05, largest 1.456) are
  not those of the optimal assignment or of box-centred alignment, which give 230 and
  249 beyond 10⁻³ and a largest move of 1.12355 and 1.12358; the issue does not name its
  convention.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 216,276 pair decisions, 59.25 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 2.034e-13. `check --replay` decided the three jobs again.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
10⁻³⁰ past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)), with the
expected verdicts stated before it ran.
It lowered the side by the least far-wall clearance, closed the least-gap pair (squares
10 and 13) by its gap, and moved every square toward the nearer near wall by its least
clearance: both routes accepted each at contact with margin 0 and refused each past it.
It enlarged one square to its pair and one to its wall: both routes refused the first at
contact for its shape alone and accepted the second, square 103, which already touches
its wall and so grew by 0, at contact; both refused each 10⁻³⁰ past it for the overlap
or the wall as well.
Both refused a duplicated square.
All 11 were as stated in advance.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read the witness through the `witness-corners`
reader. The first route is the `packing-witness verify` the author ran on the same file,
so on that route the replay is reproduced with the producer’s code; the second shares no
verification code with it.
Neither is independent of this repository’s `packing-witness
promote`, which made the coordinates.
The source’s own `sqcheck.py` was not run.

## The Gain Against Padding

T-290’s certificate at 269, contracted uniformly about the origin to first contact and
boxed, loses 3.238 × 10⁻¹² of its side (1 − λ\* = 2.036 × 10⁻¹³, the binding pair
squares 119 and 202). The gain this certificate states, 1.526e-03, is 4.71 × 10⁸ times
that margin, so none of it is T-290’s padding; the owner’s open question about gains
inside a padding margin (RV-3, think-ruu2) does not reach it, and the entry is not held
at V0/C1 as T-285 and T-286 were.
T-174’s certificate has no padding to measure (1 − λ\* = 0, a pair already touching), as
T-290’s packet found.
This certificate’s own margin, measured the same way, is 3.234 × 10⁻¹² (1 − λ\* = 2.034
× 10⁻¹³, the binding pair squares 10 and 13, the least-gap pair); contracted, it would
be a square of side 16.89946907585181, which nobody reported and which is not registered
(RV-3). `devtools.contraction_margin` wrote the two receipts,
[measure/contraction-n269.json](measure/contraction-n269.json) and
[measure/contraction-n269-own.json](measure/contraction-n269-own.json), each contracted
packing decided on both maintained routes.

## The L Step

`devtools.l_step_scan`, with this side stood in for 269’s ceiling, finds the same L-step
and monotonicity consequences as on `main`: this bound carries to no other count
([measure/l-step-scan.json](measure/l-step-scan.json)).

## What Is Not Established

- **Human oversight.** No human oversight record.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **The lineage** the source states, beyond what the measurement above shows.

## Credit and Licence

The packing is Doğa Özden’s, found by his lab’s band-design search from tilted squares
of three packings: the registry’s n = 207 packing, PingYou Ltd’s; the registry’s n = 70
packing, Ryan Xu’s, as Evan Daniel and PingYou Ltd improved it; and his own n = 179
packing of #954. The issue asks that the improvement be credited to Özden, the band’s
source packings and the current record to their holders as the registry lists them, and
the local optimizer to Evan Daniel.
The record at 269 is T-290, Doğa Özden’s own packing from a strip cut of Evan Daniel’s n
= 304 packing. The issue says the search and its code were written and run by AI agents
throughout and that the checks were run by code that did not produce the packing; it
says the issue and repository were prepared and posted by his AI agent, and that Özden
directed the work. The source starts from this repository’s registry packings and makes
its exact coordinates with this repository’s promotion tool, so its lineage builds on
this project. The bibliography key is **[Özden s269 issue 962 2026-11-11]**.

The witness, the JSON, the decimal pose, the checker outputs, the README and the diff
image are published under CC BY 4.0, and `verifier/sqcheck.py` under the MIT licence,
copyright (c) 2026 Doğa Özden, as [source/LICENSE.md](source/LICENSE.md) states; it is
byte-identical to the `LICENSE.md` the lab added to its s299, s204 and s94 repositories
on 4 November 2026 and announced on #890
([comment](https://github.com/jlevy/squares/issues/890#issuecomment-6637821113)). The
diff image is pinned by digest only.
The source carries Evan Daniel’s MIT notice as `LICENSE-evand-square-packing.txt`, for
his quench code, byte-identical to the `LICENSE` the
[evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains, and
pinned against it.

## Commands

From `packing/`, with the project interpreter.
The identity measurement reads the house witness and its regularized view as they stood
at main 75cce00b6, before this adoption replaced them, so it reproduces there; the
contraction margins read the packets and reproduce anywhere
`devtools.contraction_margin` is:

```bash
python -m devtools.acquire_source ozden-s269-issue962-2026-11-11 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s269-issue962-2026-11-11 --check
python -m devtools.upper_bound_reports ozden-s269-issue962-2026-11-11 check-claims --write
python -m devtools.upper_bound_reports ozden-s269-issue962-2026-11-11 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ozden-s269-issue962-2026-11-11 check --replay
python -m devtools.upper_bound_reports ozden-s269-issue962-2026-11-11 sharp-controls
python -m devtools.measure_identity --n 269 'OZDEN=packet:ozden-s269-issue962-2026-11-11' \
  'T-290=packet:ozden-s269-upper-bound-2026-11-11' 'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-269-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-269.yaml' \
  --out resources/web/ozden-s269-issue962-2026-11-11/measure/identity.json
python -m devtools.contraction_margin --n 269 'T-290=packet:ozden-s269-upper-bound-2026-11-11' \
  --against 'ozden-962=packet:ozden-s269-issue962-2026-11-11' \
  --out resources/web/ozden-s269-issue962-2026-11-11/measure/contraction-n269.json
python -m devtools.contraction_margin --n 269 'ozden-962=packet:ozden-s269-issue962-2026-11-11' \
  --out resources/web/ozden-s269-issue962-2026-11-11/measure/contraction-n269-own.json
python -m devtools.l_step_scan --with 269=S269 \
  --out resources/web/ozden-s269-issue962-2026-11-11/measure/l-step-scan.json
```

In the last command `S269` is the `exact_side` in the packet’s claim record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
