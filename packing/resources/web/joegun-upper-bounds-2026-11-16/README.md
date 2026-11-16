# JoeGun’s Five Upper Bounds at bc10ce4

This packet retains
[JonathanGun/square-packing-upper-bounds](https://github.com/JonathanGun/square-packing-upper-bounds/tree/bc10ce471c9d7841b9a53b383dae87d23dbe5a99)
at `bc10ce471c9d7841b9a53b383dae87d23dbe5a99` (committed 2026-11-16T05:31:52Z), then
the repository’s only commit, which
[issue #1001](https://github.com/jlevy/squares/issues/1001) named when it was opened at
05:33:07Z, 75 seconds later.
The lane fetched the repository at 06:01Z on 16 November, when `git ls-remote` read the
same head. GitHub’s activity log was not readable from this session, so the push time is
not read; no other report reached these counts in those 75 seconds, so the ledger dates
the claims by the issue, with the first commit kept.

The history was rewritten after that fetch.
Read again at 09:16Z that day, the repository’s only branch head was
`0aac839e551fd8cb7d7717c20494b095429131a1`, a root commit of 06:37:41Z with `bc10ce4`’s
message and tree (`2faf49af`), only its author and committer address and time
differing. The issue was edited at 06:38:44Z, and its only change names `0aac839e` in
place of `bc10ce4`.
So the files retained here are the tree both commits hold, and the pin stays `bc10ce4`,
the commit the lane read, which is on no branch now.
A later commit, `5971b95` (09:28:39Z), adds the author’s numerical local-minimum check
and leaves every file retained here unchanged; the
[joegun-local-minimum-2026-11-16 packet](../joegun-local-minimum-2026-11-16/README.md)
retains it (lane L188, think-664l).

Intake lane L187 (think-0y9m) retained it, replayed it and measured it on 16 November
2026 and registers it as **T-305** to **T-309**, one result a count.
The blind stage 4 review of lane L186 (think-skt8) accepted all five the same day, so
they are at V3/C3, and each case adopted its certificate as its house in the pass of 16
November 2026 under the house rule.

## What the Source Claims

- **Five certificates.** `n-127-candidate.yaml`, `n-204-candidate.yaml`,
  `n-232-candidate.yaml`, `n-264-candidate.yaml` and `n-305-candidate.yaml` each state a
  packing as a `packing.squares:Witness/v2` document of rational corners, with the
  softschema envelope and a claim block of `coordinate_provenance: verified`. #1001 and
  the README print the sides rounded up at 12 places: 11.801753890487, 14.802646843107,
  15.759531627557, 16.773807598002 and 17.945762359659. Each is the issue’s print of an
  exact rational side: at 232 the side terminates at 15 places, 15.759531627556573, and
  the others are fractions of 300 to 430 digits.
- **The exact coordinates.** Each certificate was made by this repository’s
  `packing-witness promote --strategy robust-rational --max-side-increase 1e-11` at
  `31ddae6` from the binary64 pose kept beside it, `n-NNN-decimal-pose.yaml`, after the
  author’s export pushed every centre away from the centroid by a factor of at least 1 +
  10⁻¹². Each certificate block reports `center_dilation: '1'` and 36 rational digits.
- **Lineage.** The README says each packing is a public Kaggle packing by Tomáš Kodaj,
  from his notebook “Squares in Squares | [22.1636]” (last run 13 November 09:48 UTC,
  downloaded at 10:17 UTC that day), at 11.801765635430, 14.802646907234,
  15.759531732104, 16.773891500852 and 17.946298110350, improved further by JoeGun: a
  fault-line DP of his own at 127, 204 and 232 (13 November, 10:42 UTC), a 600-second
  quench with Evan Daniel’s code (evand/square-packing at `6067db5`, MIT) at 264, and
  two quench runs and then the fault-line DP at 305. JoeGun’s part of each gain is
  1.174 × 10⁻⁵, 6.41 × 10⁻⁸, 1.045 × 10⁻⁷, 8.390 × 10⁻⁵ and 5.358 × 10⁻⁴; the rest is
  Kodaj’s. The fault-line DP cuts pieces out of other packings along lines no square
  crosses and joins them by a dynamic programme; the donors were the author’s own and
  public Kaggle packings, and which donors the winning pieces came from was not recorded.
  The author did not trace what Kodaj’s packings build on.
- **The checkers.** `packing-witness verify` (`packing-witness-verify.txt`) reports
  VERIFIED, exact-algebraic, for all five, testing 8,001, 20,706, 26,796, 34,716 and
  46,360 pairs. `check.py` (`check-output.txt`), written apart from this repository’s code
  in `Fraction` arithmetic with no tolerance and no distance filter, reports VALID for all
  five, and refused three broken copies of the n = 127 witness. The README says the
  promotion used this repository’s tool, so `packing-witness verify` does not check the
  rounding independently and `check.py` does. Neither ran here.
- **Not claimed at the pin.** No local-optimality, rigidity or KKT analysis, no
  proof-assistant check, no human review outside this project, and no measurement of the
  least pair or contraction margin. Later on 16 November the author added a numerical
  check with Evan Daniel’s `exactsolve.py`, which the
  [local-minimum packet](../joegun-local-minimum-2026-11-16/README.md) retains: it
  reports the exact touching point near the certificate at 127, 232, 264 and 305 a KKT
  point and a local minimum, strict up to flat motions, so not rigid, and no result at
  204. The author says the check is numerical, at 80 digits, and not a proof, and claims
  no lower side.
- **Other public values.** The Kaggle per-puzzle leaderboard (read 16 November 04:38 UTC)
  lists side-only entries below the claims at all five counts, which state no packing.
  Kodaj’s notebook also holds n = 270 at 16.927469594094, below the record’s
  16.928148603343 (T-283), which the issue does not claim.
- **Credit.** Tomáš Kodaj as finder at all five counts, improved by JoeGun, and the quench
  to Evan Daniel; at 204 and 232, where JoeGun’s part is below 2 × 10⁻⁷, the issue says
  credit to Kodaj alone is fair. AI agents wrote and ran the search code, the checker and
  the filing, and JoeGun directed the work.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the whole tree, 17 files: 16 retained under [source/](source/), the five
certificates with the SHA-256 digests the issue lists, and Evan Daniel’s MIT notice,
`LICENSE-evand-square-packing.txt`, pinned by digest against the byte-identical `LICENSE`
the [issue 845 packet](../evand-issue845-2026-10-29/README.md) retains.
`check.py` and `make-pose.py` are retained as data and were never run here.

Kodaj’s notebook was not retained: `www.kaggle.com` was refused by this session’s proxy
(CONNECT 403 at 06:01:47Z), so neither his packings nor the notebook’s licence could be
read.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `31ddae6fe`.
Each certificate is below its count’s house in both lanes, and no register bound is
pending adoption at any of the five counts:

| n | Side, 12 places | House | Below it by |
| ---: | --- | --- | --- |
| 127 | 11.801753890487 | T-174, Ryan Xu’s packing refined by Francisco Couzo and PingYou Ltd | 9.1249 × 10⁻³ |
| 204 | 14.802646843107 | T-268, Evan Daniel’s packing | 1.7145 × 10⁻³ |
| 232 | 15.759531627557 | T-275, Alex Chilton’s packing refined by Francisco Couzo and Doğa Özden | 1.8780 × 10⁻³ |
| 264 | 16.773807598002 | T-186, Daniil Ostashev’s composition tightened by PingYou Ltd and Mishapolk | 9.2753 × 10⁻⁴ |
| 305 | 17.945762359659 | T-174, Nate Chaoweeraprasit’s SQUISH packing refined by Francisco Couzo and PingYou Ltd | 4.7041 × 10⁻³ |

The
[ledger of 16 November for this lane](../../../campaign/issue-intake/upper-bounds-1001-20261116/README.md)
records #1001 at all five counts, each continuing Kodaj’s packing, and lists the quoted
side at 270 as not claimed, with no packing in hand. The lower bounds at the five counts
lie below the sides.

## Exact Replay

The checks below were planned before any of them ran: the expected verdict of every
gross and sharp control was written down at 06:03:24Z on 16 November (SHA-256
`6c25dc71…cad35`, recorded on the bead), with two branches stated in advance, a square
that touches its wall exactly and a pair that touches exactly.
Before the plan was hashed the lane had digested the five certificates and read the
header and last squares of the 232 file; no route or program had read them.

`devtools.upper_bound_reports certify` decided each certificate and its duplicate-square
and outside-container controls on both maintained routes: 15 jobs, 819,474 pair
decisions, 252.05 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). Each
positive passed and every control was refused on both routes.
At every count squares touch the box at a near wall and at a far wall, the least wall
clearance exactly 0. The least pair gaps are about 1.1203 × 10⁻¹¹ at 127 (squares 50 and
54) and at 204 (8 and 109), 9.97 × 10⁻¹³ at 232 (188 and 197, exactly 997/10¹⁵), 1.2 ×
10⁻¹² at 264 (255 and 256) and 1.1251 × 10⁻¹¹ at 305 (130 and 137). `check --replay` decided the 15
jobs again.

`sharp-controls` took each certificate to exact contact and 10⁻³⁰ past it on both routes,
11 controls a count and 919 route CPU seconds in all
([receipts/sharp-controls-n127.json](receipts/sharp-controls-n127.json) and the four
beside it), and every control came out as stated in advance, the branch for a touching
square taken at each count:

- **Wall, pair and near-wall.** The box lowered to the extent (by 0, a square touching
  the far wall), the tightest pair closed by its gap, and every square moved toward its
  near wall by the least near-wall clearance, 0: each is accepted at exact contact and
  refused 10⁻³⁰ past it.
- **Enlarged to a pair.** The tightest pair’s square, enlarged against its partner, is
  refused at contact for its shape alone, and past it for the overlap as well.
- **Enlarged to a wall.** A square already at its wall, grown by 0, is accepted, and
  refused 10⁻³⁰ past it for the wall and its shape.
- **Duplicate.** A duplicated square is refused.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share this repository’s corner-witness reader (certificate parsing and
half-angle conversion), `Fraction` arithmetic and the separating-axis method.
The first is the `packing-witness verify` the author ran, from the package whose
promotion made the coordinates and ran that verifier on them, so on that route the
replay is reproduced with the producer’s code; the independent rational corner checker
shares no geometry or verification code with `sqpack.witness` or `sqpack.verify`, and the
replay’s independent re-implementation rests on it. Neither route is the author’s
`check.py`, which was not run.

## Pose by Pose and Padding

`devtools.measure_identity` wrote the `identity-nNNN.json` receipts under
[measure/](measure/), and `devtools.contraction_margin` the `contraction-*.json`
receipts:

- **Against each house.** At every count no symmetry of the box pairs the certificate one
  to one with the house’s packing by nearest centres, and the optimal assignment moves 70
  (127), 73 (204), 35 (232), 44 (264) and 113 (305) squares beyond a tenth, at most 0.955,
  1.098, 1.159, 0.775 and 1.092. Each is a new arrangement relative to the record’s
  packing, as Kodaj’s would be; the house witness and its regularized view measure as the
  house’s packet. At 204 and 232 the house before the current one measures the same way
  (44 and 39 squares beyond a tenth against T-264 and T-256).
- **Their tilts.** 56 squares turn beyond a degree at 127, 99 at 204, 65 at 232, 71 at
  264 and 92 at 305. At 232 and 264 they turn both ways where the house’s all turn one
  way, and at 305 all turn one way where T-174’s turn both ways.
- **Kodaj’s packings** are not in hand, so JoeGun’s step from them is not measured here.
- **Each house’s margin** is 0 at 127 and 305 (T-174’s squares touch), 1.4804 × 10⁻¹⁹
  at 204, 2.9978 × 10⁻¹² at 232 and 1.677 × 10⁻⁹⁹ at 264, wall slack included, so every
  gain, 9.3 × 10⁻⁴ or more, lies wholly outside the house’s padding. RV-3 (think-ruu2)
  does not reach any of them.
- **Each certificate’s own margin** is 1.2099 × 10⁻¹⁰ at 127, 1.5463 × 10⁻¹⁰ at 204,
  1.4715 × 10⁻¹¹ at 232, 1.8929 × 10⁻¹¹ at 264 and 1.9066 × 10⁻¹⁰ at 305. Contracted,
  each would be a square that much smaller, which nobody reported and which is not
  registered. JoeGun’s stated part of each gain is 415 times its own margin or more, at
  204, and 7,100 times at 232.

## The L Step

[measure/l-step-scan.json](measure/l-step-scan.json) is `devtools.l_step_scan` with the
five sides stood in for their ceilings: it finds the same L-step and monotonicity
consequences as on `main`, so no bound carries to another count.

## Stage 4 Review

The stage 4 review of 16 November 2026
([review-2026-11-16-joegun-1001.md](../../../../docs/project/reviews/review-2026-11-16-joegun-1001.md),
lane L186, under think-skt8), written blind to this lane until its findings were frozen,
accepts all five certificates with fifteen findings, all notes. Its clean-room checker,
kept in the review-only directory
[joegun-1001-review-2026-11-16](../joegun-1001-review-2026-11-16/README.md), decided
every square, wall and all 136,579 pairs twice, by separating axes in Python integers and
by exact clipping in GMP rationals, with no distance filter, and 160 of 160 controls,
stated beforehand as rules, came out as stated.
It was written by the strong tier, not the strong-max tier the runbook names.

This lane read the review at 06:56Z on 16 November, after its own replay, controls and
measurements (06:34Z) and its records for them (06:45Z) were committed.
Read against this packet’s receipts, the review’s least pair margins (squares 50 and 54
at 127, 8 and 109 at 204, nine pairs at 997/10¹⁵ at 232, 255 and 256 at 264, 130 and 137
at 305) are the replay’s exactly; its wall contacts include each square the sharp controls
grew by 0 (44, 47, 108, 124 and 27); and its contraction margins of each house and
certificate and its identity against each house are this packet’s
[measure/](measure/) receipts, from the same tools. No disagreement.

What the review adds:

- **F3**: each claim is its side’s 12-place ceiling; the squares are accepted in the box
  of the claim and refused in that of its floor.
- **F4**: each side is the packing’s extent in one direction; the other is short by 3.9 ×
  10⁻¹⁶ to 5.3 × 10⁻¹⁵, slack the record registers nothing for.
- **F5**: no pair touches; each packing is a contact arrangement opened by about 10⁻¹¹
  (127, 204, 305) or 10⁻¹² (232, 264).
- **F7**: the files call their coordinates `verified`; those are the promotion tool’s
  words, and the record states its own provenance.
- **F8 to F11, F13 and F15**: custody, the issue’s arithmetic, the padding (RV-3 does not
  apply), new arrangements credited to Kodaj and JoeGun, no closed form, and the
  maintained routes’ agreement.
- **F12**: `check.py` is sound; its format check is an `assert`, which `python -O`
  strips.
- **F14**: Kodaj’s notebook and its licence were not read (think-71uq).

Its seven questions for the author hold nothing open: Kodaj’s parent packings, his
notebook’s licence, what the fault-line programme moved at 204 and 232, the export’s push
factor, the side’s slack, `check.py`’s `assert`, and the programme itself.

## Adoption

Each case adopted its certificate as its house best packing in the pass of 16 November
2026 under the house rule: T-305 at 127 and T-309 at 305 in place of T-174, T-306 at
204 in place of T-268, T-307 at 232 in place of T-275, and T-308 at 264 in place of
T-186, each earlier house keeping its certificate as history. The same day’s pass had
moved only 90, so a day’s archive holds one prior state for each of the five counts.
Tomáš Kodaj is each packing’s finder and JoeGun its improver.

Both strong generators ran on the five new witnesses
([the runs](../../../cases/regularized_drawings/think-0y9m-2026-11-16/README.md)), and the
selection draws grid-slack’s same-side view at every count, admitted at row 10. Evan
Daniel’s driver certified a KKT local minimum below the side at 127, 232, 264 and 305,
1.2175 × 10⁻¹⁰, 4.0164 × 10⁻⁹, 1.9066 × 10⁻¹¹ and 1.9146 × 10⁻¹⁰ below it, about 1.006,
273, 1.007 and 1.004 times the certificate’s own contraction margin and beyond it at
each; each is held at row 3 as a register candidate and not admitted (RV-3). At 204 its
exact solve failed, so it drew no view there.
The author’s own run of the same solver, added after the filing, reaches the same four
points, equal in every digit both print, and fails at 204 too
([the comparison](../joegun-local-minimum-2026-11-16/README.md#against-the-record)).

## What Is Not Established

- **Kodaj’s packings and JoeGun’s steps**: the issue’s account; the notebook was not
  reachable here, and the fault-line DP’s donors were not recorded by the source.
- **Local optimality, rigidity or KKT**: not claimed by the source at the pin. Its later
  revision reports a numerical KKT point and local minimum at four of the five counts,
  which it says is not a proof, and the record’s driver reached the same points; the
  record registers none of it, and RV-3 holds the four points.
- **Human oversight**: no record is retained.

## Credit and Licence

The packings are Tomáš Kodaj’s, as JoeGun improved them; the quench at 264 and 305 is
Evan Daniel’s code. The issue says AI agents wrote and ran the search code, the checker
and the filing, under JoeGun’s direction. The record credits people, not AI agents
([attribution.md](../../../../attribution.md)), and states the assistance in the source’s
words. The bibliography key is **[JoeGun upper bounds 2026-11-16]**.

`LICENSE.md` at the pin licenses the witnesses, decimal poses, checker outputs and README
under CC BY 4.0 and `check.py` under MIT, copyright 2026 JoeGun; it says it covers the
author’s own contribution and does not change the terms of Kodaj’s work.
`make-pose.py` is named by no licence line and is retained under the presumption of
permission for a source its author submitted (think-cnn7); `LICENSE.md` at the later
revision licenses it under MIT.
The licence of Kodaj’s notebook was not checked by the source and could not be read here;
whether a seeded packing needs a notice of its own is the owner’s question think-71uq,
which holds no import.

## Commands

From `packing/`, with the project interpreter:

```bash
P=joegun-upper-bounds-2026-11-16
M=resources/web/$P/measure
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 204 "JOEGUN=packet:$P" \
  'T-268=packet:evand-issue914-2026-11-05' 'T-264=packet:ozden-s204-upper-bound-2026-11-03' \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-204-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-204.yaml' --out $M/identity-n204.json
python -m devtools.contraction_margin --n 204 'T-268=packet:evand-issue914-2026-11-05' \
  --against "joegun-1001=packet:$P" --out $M/contraction-n204.json
python -m devtools.contraction_margin --n 204 "joegun-1001=packet:$P" --out $M/contraction-n204-own.json
python -m devtools.l_step_scan --with 127=... --with 204=... --with 232=... --with 264=... \
  --with 305=... --out $M/l-step-scan.json
```

The other counts’ identity and contraction commands differ only in the count and the
house: `T-174=packet:pingyou-pr574-certificates-2026-10-13` at 127 and 305 (127’s
regularized view read by `witness-corners`), `T-275=packet:ozden-s232-upper-bound-2026-11-09`
and `T-256=packet:couzo-issue844-2026-10-28` at 232, and
`T-186=packet:mishapolk-kkt-refinements-2026-10-14` at 264. The identity measurements read
the house witnesses and regularized views as they stand at `main` `31ddae6fe`; each
`--with` names the exact side `acquisition/claims.json` records.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
