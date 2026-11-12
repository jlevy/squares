# Doğa Özden’s s(269) Certificate at f496016

This packet retains
[kenaznia-doga/s269-upper-bound-1688973007](https://github.com/kenaznia-doga/s269-upper-bound-1688973007/tree/f496016d3ebccb00c00cbf146efe85e0cc952dda)
at `f496016d3ebccb00c00cbf146efe85e0cc952dda` (committed 2026-11-12T03:00:02Z), the
repository’s one commit, which [issue #967](https://github.com/jlevy/squares/issues/967)
names 12 seconds later.
Doğa Özden’s AI agent, which uses the account kenaznia-doga, prepared and posted both on
his behalf. Seven seconds after the issue it pointed to it from his issue #947
([comment](https://github.com/jlevy/squares/issues/947#issuecomment-6813076182)), and a
second later from pull request #966, which adopted his #962 at this count
([comment](https://github.com/jlevy/squares/pull/966#issuecomment-6813076476)).

## What the Source Claims

- `n-269-candidate.yaml`, a `packing.squares:Witness/v2` file (corners, rational
  scalars, 269 squares), bounds s(269) by its exact side, a fraction whose 16-place
  ceiling is 16.8897300735956367. #967 prints its 12-place ceiling, 16.889730073596, and
  says it is 1.126e-02 below the record, T-290, the author’s own #947 certificate, and
  9.74e-3 below his #962, which PR #966 was adopting; it says it supersedes both.
  #966 merged at 07:08:09Z, so the house on `main` is now T-296, #962’s certificate.
  The issue and README also print the exact side as 16.889730073595636, the side
  truncated at 15 places, 6.9 × 10⁻¹⁶ below it.
  It claims an upper bound only: no KKT, local-optimality, rigidity or global-optimality
  claim.
- The exact coordinates were made by this repository’s own `packing-witness promote
  --strategy robust-rational` at `0352d755` from the lab’s decimal pose,
  `n-269-decimal-pose.yaml`, which the witness’s `source.path` names, with
  `center_dilation: '1'` and no dilation.
  The issue says the pair margins of about 2 × 10⁻¹³ are the decimal pose’s own, left by
  the final binary64 repair scaling of Evan Daniel’s quench (about 10⁻¹³ relative), that
  only the squares that set the left wall, the bottom wall and the side touch them
  exactly, and that other squares near a wall clear it by up to about 10⁻¹². Measured
  here, three squares touch a wall exactly: square 48 at the left, square 102 at the
  bottom and square 199 at the top, which sets the side.
  No square touches the right wall.
  Of the other square–wall clearances, 47 are below 10⁻¹² and at most 7.84 × 10⁻¹⁵, and
  10 lie between 9.16 × 10⁻⁶ and 9.32 × 10⁻⁴, beyond “up to about 1e-12”.
- `n269-witness.json` is the same file as JSON. `packing-witness-verify.txt` is the
  author’s run of this repository’s `packing-witness verify` at `0352d755` (VERIFIED,
  36,046 pairs); `sqcheck-output.txt` is the author’s run of `verifier/sqcheck.py`, an
  exact checker the source says was written separately from this repository’s code
  (VALID, exact rational, the exact side rounded up at 15 places).
  The issue says the two share only the unit-square, wall and non-overlap definitions,
  that `packing-witness verify` is not independent of how the coordinates were rounded,
  and that `sqcheck.py` certified the decimal pose in interval arithmetic at its own
  side before promotion.
  Those statements are the author’s; no source program ran here.
- The issue says the packing was found by an AI-run column-band designer, new for this
  filing, with no donor packing: tilted squares stand in columns across a band along the
  diagonal at unit pitch, each column a stack of one to three squares sliding on its
  own; the axis-parallel squares sit on the two wall-anchored staircase lattices; for a
  side fraction f and a band angle of 45 degrees minus delta an exact dynamic programme
  over the columns maximises the number of squares.
  The best design is quenched once with Evan Daniel’s ALM+SLP code from
  [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT,
  at `bb4cc78e`), then kicked and quenched again.
  This packing came from the design f = 0.913469, band angle 42.8 degrees (delta 2.2),
  tolerance 0, 45 tilted squares, column offset 0.96875 and diagonal variant 14,
  quenched once to 16.890507465412; a kick of sigma 0.0222 and a quench gave
  16.889734433328, and a kick of sigma 0.001007 and a quench gave the filed side.
  The cloud job b2h269 reached 16.88973007359575, but its pack file was lost, and the
  filed packing is a local re-find the issue says has the same structure and a side 9 ×
  10⁻¹⁴ higher. The issue counts 45 tilted squares against the record’s 100: one band at
  about 42.1 degrees and a small cluster at about −44.9 degrees at the upper-right end.
  Against the registry packing, matched by assignment up to the square’s symmetries, it
  reports 261 of 269 centres beyond 1e-3, 137 beyond 0.05 (largest 1.879), 121 squares
  re-tilted beyond 1 degree (largest 44.4), and 45 squares tilted beyond 0.5 degree
  against the record’s 100.
- The issue describes the record, T-290, in two ways, as #962 did: in its claim
  paragraph as “built from Nate Chaoweeraprasit’s packing (itsnaka) improved by Evan
  Daniel and PingYou Ltd”, and in its lineage paragraph as found by transplanting Evan
  Daniel’s n = 304 packing.
  The register records T-290 as the second: a strip cut of Evan Daniel’s 304, below
  T-174, Nate Chaoweeraprasit’s packing as Evan Daniel and PingYou Ltd improved it,
  which was the house before it.
- The issue’s credit paragraph asks that “the band’s source packing” be credited to the
  registry’s n = 207 packing, to n = 70 (Ryan Xu; improved by Evan Daniel and PingYou
  Ltd) and to the lab’s own n = 179 of #954, while its lineage paragraph and the README
  say the designer used no donor packing and no registry packing as a seed.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the whole tree, 11 files: 7 retained under [source/](source/) and 4 pinned
by digest.

| File | Bytes |
| --- | --- |
| `LICENSE.md` | 1,484 |
| `README.md` | 7,314 |
| `n-269-candidate.yaml` | 820,780 |
| `n-269-decimal-pose.yaml` | 28,459, the decimal pose the witness was promoted from |
| `n269-witness.json` | 812,482, the same packing as JSON, which the reader holds equal to the YAML |
| `packing-witness-verify.txt` | 559 |
| `sqcheck-output.txt` | 101 |
| `LICENSE-evand-square-packing.txt` | 1,068, pinned against the identical copy of Evan Daniel’s MIT notice the [evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains |
| `records/n-269-candidate-diff.png` | 308,205, pinned by digest: a raster comparison that decides nothing |
| `verifier/README.md` | 3,441, pinned against the identical copy the [3 November s299 packet](../ozden-s299-upper-bound-2026-11-03/README.md) retains |
| `verifier/sqcheck.py` | 17,654, pinned against the identical copy the [9 November s232 packet](../ozden-s232-upper-bound-2026-11-09/README.md) retains, never executed here |

The SHA-256s the issue states for `n-269-candidate.yaml` and the README states for it
and for `n269-witness.json` are the files’.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is about 1.8 megabytes in a checkout and far less as Git stores it, so it is
kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `45e2ecca2` on 12
November 2026):

- **269:** exact side 16.8897300735956367 rounded up at 16 places, below the case’s
  house (T-296, Doğa Özden’s own certificate of #962) by 9.739e-03, as the issue states,
  below T-290, the house before it, by 1.126e-02, as the issue states, and below T-174,
  the house before that, by 1.178e-02. No register bound is pending adoption at 269.

## Report Order

The
[ledger of 12 November for this lane](../../../campaign/issue-intake/upper-bounds-967-20261112/README.md)
walks every report at 269 in the order it reached this repository, from a start frozen
at `main` `45e2ecca2`, and records this packet’s claim at 269. The best public Kaggle
per-puzzle packing the issue quotes at 269, 16.901513582205 (kirilltym), is above this,
by 1.18e-2. The issue also quotes, and states first, a side-only Kaggle leaderboard
entry at 269, 16.889730079125 (team elegans, 5 November, from a cache of 9 November),
5.53 × 10⁻⁹ above this side, as the issue says.
It is unpublished and states no packing, so it is no report and is recorded as context
only.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-296’s packing, T-290’s,
T-174’s, the house witness and the regularized view, and wrote
[measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **Against T-296**, the house: no symmetry of the box pairs it one to one with T-296’s
  packing by nearest centres.
  The optimal assignment, under the identity of the box, moves every square beyond 10⁻⁶,
  266 beyond 10⁻³, 107 beyond 0.01 and 53 beyond 0.1 (largest 0.950002), and turns 102
  squares by more than 10⁻⁶ radians, by up to 44.77 degrees; aligned by box centres, 57
  squares turn by more than a degree.
  Tilted beyond a degree: 45 here, as in T-296, but a band of 41 at 41.60 to 42.06
  degrees and a cluster of four, squares 42 to 45, at −44.33 to −44.38 degrees at the
  upper-right end, against T-296’s 22 one way and 23 the other, 39.53 to 44.77 degrees.
  No square here is tilted between half a degree and one, so 45 are tilted beyond half a
  degree, as the issue says.
  The house witness measures as T-296, and its regularized view the same but for 125
  squares beyond 10⁻² under the assignment.
  So it is a new arrangement relative to T-296’s packing, not a further arrangement of
  it.
- **Against T-290**, the house before T-296: no symmetry pairs nearest centres one to
  one, and the optimal assignment moves 127 squares beyond a tenth (largest 1.25522);
  aligned by box centres, 122 squares turn by more than a degree.
  T-290 has 100 squares tilted beyond a degree, 18.70 to 36.11 degrees, all turned one
  way. It is new against T-290 as well.
- **Against T-174**, it is new: the optimal assignment moves 75 squares beyond a tenth
  (largest 0.91336); T-174 has 49 tilted squares.
- The issue’s band angles, “about 42.1°” and “about −44.9°”, are a little off: the band
  lies at 41.60 to 42.06 degrees and the cluster at −44.33 to −44.38. The issue’s own
  counts against T-290 (261 beyond 10⁻³, 137 beyond 0.05, largest 1.879, 121 re-tilted
  beyond a degree) are not those of the optimal assignment or of box-centred alignment,
  which give 268 and 269 beyond 10⁻³, a largest move of 1.25522 and 1.25512, and 122
  squares turned beyond a degree.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 216,276 pair decisions, 98.63 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 2.036e-13. `check --replay` decided the three jobs again.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
10⁻³⁰ past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)), with the
expected verdicts stated before it ran (the plan’s SHA-256 `98f0635c…c4b294`, 07:18:10Z
on 12 November). It lowered the side by the least far-wall clearance, closed the
least-gap pair (squares 40 and 38) by its gap, and moved every square toward the nearer
near wall by its least clearance: both routes accepted each at contact with margin 0 and
refused each past it.
It enlarged one square to its pair and one to its wall: both routes refused the first,
square 38, at contact for its shape alone and accepted the second, square 48, which
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
Neither is independent of this repository’s `packing-witness
promote`, which made the coordinates.
The source’s own `sqcheck.py` was not run.

## The Gain Against Padding

T-296’s certificate at 269, contracted uniformly about the origin to first contact and
boxed, loses 3.234 × 10⁻¹² of its side (1 − λ\* = 2.034 × 10⁻¹³, the binding pair
squares 10 and 13). The gain this certificate states, 9.739e-03, is 3.01 × 10⁹ times
that margin, so none of it is T-296’s padding; the owner’s open question about gains
inside a padding margin (RV-3, think-ruu2) does not reach it, and the entry is not held
at V0/C1 as T-285 and T-286 were.
T-290’s certificate, measured the same way in #962’s
[packet](../ozden-s269-issue962-2026-11-11/measure/contraction-n269.json), has 3.238 ×
10⁻¹² of padding, and the gain on it, 1.126e-02, is 3.48 × 10⁹ times that.
This certificate’s own margin, measured the same way, is 3.236 × 10⁻¹² (1 − λ\* = 2.036
× 10⁻¹³, the binding pair squares 38 and 40, the least-gap pair); contracted, it would
be a square of side 16.8897300735924008, which nobody reported and which is not
registered (RV-3). `devtools.contraction_margin` wrote the two receipts,
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

The packing is Doğa Özden’s, found by his lab’s column-band designer, which the issue
says took no donor packing, and quenched with Evan Daniel’s optimizer.
The issue asks that the improvement be credited to Özden, the band’s source packing and
the current record to their holders as the registry lists them, and the local optimizer
to Evan Daniel; it names the registry’s n = 207 packing, n = 70 (Ryan Xu; improved by
Evan Daniel and PingYou Ltd) and the lab’s own n = 179 of #954 as the band’s source
packing.
The record at 269 before this import was T-296, Doğa Özden’s own band packing of
#962, and before it T-290, his own packing from a strip cut of Evan Daniel’s n = 304
packing. The issue says the search and its code were written and run by AI agents
throughout and that the checks were run by code that did not produce the packing; it
says the issue and repository were prepared and posted by his AI agent, and that Özden
directed the work. The source makes its exact coordinates with this repository’s
promotion tool, so its lineage builds on this project.
The bibliography key is **[Özden s269 upper bound 2026-11-12]**.

The witness, the JSON, the decimal pose, the checker outputs, the README and the diff
image are published under CC BY 4.0, and `verifier/sqcheck.py` under the MIT licence,
copyright (c) 2026 Doğa Özden, as [source/LICENSE.md](source/LICENSE.md) states; it is
byte-identical to the `LICENSE.md` the lab added to its s299, s204 and s94 repositories
on 4 November 2026 and announced on #890
([comment](https://github.com/jlevy/squares/issues/890#issuecomment-6637821113)), and to
the one #962’s repository carries.
The diff image is pinned by digest only.
The source carries Evan Daniel’s MIT notice as `LICENSE-evand-square-packing.txt`, for
his quench code, byte-identical to the `LICENSE` the
[evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains, and
pinned against it.

## Commands

From `packing/`, with the project interpreter.
The identity measurement reads the house witness and its regularized view as they stood
at main 45e2ecca2, before this adoption replaced them, so it reproduces there; the
contraction margins read the packets and reproduce anywhere
`devtools.contraction_margin` is:

```bash
python -m devtools.acquire_source ozden-s269-upper-bound-2026-11-12 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s269-upper-bound-2026-11-12 --check
python -m devtools.upper_bound_reports ozden-s269-upper-bound-2026-11-12 check-claims --write
python -m devtools.upper_bound_reports ozden-s269-upper-bound-2026-11-12 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ozden-s269-upper-bound-2026-11-12 check --replay
python -m devtools.upper_bound_reports ozden-s269-upper-bound-2026-11-12 sharp-controls
python -m devtools.measure_identity --n 269 'OZDEN=packet:ozden-s269-upper-bound-2026-11-12' \
  'T-296=packet:ozden-s269-issue962-2026-11-11' 'T-290=packet:ozden-s269-upper-bound-2026-11-11' \
  'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-269-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-269.yaml' \
  --out resources/web/ozden-s269-upper-bound-2026-11-12/measure/identity.json
python -m devtools.contraction_margin --n 269 'T-296=packet:ozden-s269-issue962-2026-11-11' \
  --against 'ozden-967=packet:ozden-s269-upper-bound-2026-11-12' \
  --out resources/web/ozden-s269-upper-bound-2026-11-12/measure/contraction-n269.json
python -m devtools.contraction_margin --n 269 'ozden-967=packet:ozden-s269-upper-bound-2026-11-12' \
  --out resources/web/ozden-s269-upper-bound-2026-11-12/measure/contraction-n269-own.json
python -m devtools.l_step_scan --with 269=S269 \
  --out resources/web/ozden-s269-upper-bound-2026-11-12/measure/l-step-scan.json
```

In the last command `S269` is the `exact_side` in the packet’s claim record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
