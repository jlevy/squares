# Joost de Winter’s s(90) Certificate at fa53fb0

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/fa53fb0d734fbf438bcfb73c1434a15894bb2bc5)
at `fa53fb0d734fbf438bcfb73c1434a15894bb2bc5` (committed 2026-11-15T12:07:15Z), which
[issue #997](https://github.com/jlevy/squares/issues/997) names.
The issue was opened at 12:08:33Z. It replaces the certificate
[issue #996](https://github.com/jlevy/squares/issues/996) named at `64d5ee7` (opened at
11:30:13Z) by one 9e-8 smaller, and asks that this commit be pinned and the earlier one
disregarded. The superseded certificate is retained in the
[64d5ee7 packet](../de-winter-s90-64d5ee7-2026-11-15/README.md).

The repository is watched.
The lane fetched it at 12:01Z for #996, when its head was `9cafa33`, and again at 12:55Z
for #997, when its head was `6c0ad56`. `fa53fb0` replaces `n90/n90_exact.json`,
`n90/n90_witness.yaml` and the two figures, and updates `n90/README.md`,
`n90/REGISTRATION.md` and the root README’s row; its `n90/SHA256SUMS` still states the
digests of `9cafa33`’s files.
The head, `6c0ad56` (12:07:15Z), changes only `n90/REGISTRATION.md`, which now names
`fa53fb0` for the certificate, and `n90/SHA256SUMS`, whose digests of the certificate,
the witness, the figures, the checkers and `n90/README.md` match this pin’s files.
Every other file has the same Git blob at the pin and the head.
GitHub’s activity log was not readable from this session, so the push time of `fa53fb0`
is not read; no other report reached 90 in the 78 seconds before #997, so the ledger
dates the claim by the issue, with the first commit kept.

Intake lane L181 (think-32cl) retained it, replayed it and measured it on 15 November
2026 and registers it as **T-304**, the only result of the two issues.
The blind stage 4 review of lane L180 and its addendum (lane L182) accepted it the same
day, so it is at V3/C3, and the case adopted it as its house at 90 in the pass of 16
November 2026 under the house rule, in place of T-303.

## What the Source Claims

- `n90/n90_exact.json` states 90 unit squares as `[center_x, center_y, cos, sin]` rows
  of exact rationals, `(cos, sin)` the unit direction of one edge, with the side
  99940387666098521323/10000000000000000000 = 9.9940387666098521323, which terminates at
  19 places. #997 and the root README round it up at 12 places, 9.994038766610, and
  `n90/README.md` prints it in full.
  `n90/n90_witness.yaml` states the same packing as a `packing.squares:Witness/v2`
  document of rational corners, with the softschema envelope and a claim of
  `coordinate_provenance: reported`.
- **The construction.** The packing starts from T-303, jazivxt’s packing of
  [issue #989](https://github.com/jlevy/squares/issues/989), the record at 90, which
  jazivxt built from a crop of the source’s own packing of 157 squares (T-293). The
  README says T-303 has a cluster of 44 squares that lean away from the axes inside a
  frame of axis-aligned squares, and that a local search changed small groups of squares
  in position and angle, optimized the packing again after each change, and kept the
  changes that gave a smaller side.
  In the new packing, it says, the cluster has 40 leaning squares, four squares in the
  upper left are axis-aligned, four at the top lean by 25.1 and 27.8 degrees where T-303
  has 22.9, and one axis-aligned square at the top wall lies 0.32 lower.
  At `64d5ee7` the README counted 49 and 37.
- **The local optimum.** A linear program over all 90 squares, every contact linearized
  at the solution, found no first-order improvement larger than 4 × 10⁻¹⁰. The README
  adds that the certificate of #996 passed the same test at a side 9e-8 larger, so the
  test covers one set of contacts.
  The certificate keeps a smallest gap of 2 × 10⁻¹² between squares.
  Local optimality has no formal proof.
- **The Kaggle note.** A public merged submission to the Kaggle competition “Squares in
  Squares” (bestbryant/claude_code_squaresinsquares, 15 November 2026) lists
  9.998277166917 for n = 90; the leaderboard’s best sides were not available to the
  author.
- **The checkers.** `verify_exact.py` (separating axes, for every pair whose centres are
  closer than √2) and `check_area.py` (the area of each close pair’s clipped
  intersection), both Python’s `Fraction` and its standard library only, the same files
  as at `64d5ee7`. #997 says each reports 90 squares and 199 close pairs on the new
  files, that this repository’s `check_rational_witness_independent.py` reports
  “VERIFIED: 90 squares, 4005 pairs” on the witness, and that the witness validates
  against `witness.schema.yaml`. Neither of the author’s checkers ran here.
- **Credit.** #997 says the arrangement, lineage, credit and AI assistance are as #996
  states: credit to Joost de Winter as an improvement of jazivxt’s packing.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the licence, the root README and the whole of `n90/`, 11 files: 6 retained
under [source/](source/) and 5 pinned by digest: `LICENSE`, against the byte-identical
copy the
[227, 229 and 260 packet](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md)
retains; `verify_exact.py` and `check_area.py`, against the byte-identical copies the
64d5ee7 packet retains, never opened or run here; and the two figures.
The retained `SHA256SUMS` is the pin’s, whose lines for the certificate, the witness,
the figures, `REGISTRATION.md` and `README.md` are `9cafa33`’s digests; the head’s copy
states this pin’s.

**The twin.** `n90_witness.yaml` lists each square’s corners counterclockwise from the
corner at C + (u + v)/2 of its JSON pose, the vertex opposite the one this repository’s
corner reader starts from, so `witness-corners` reads each square a half turn on and
refuses an exactly upright one.
The reader `witness-corners-opposite`, written for these twins, reads the list from that
vertex, and the corner readers now accept the witness’s schema address and its
`square-1` to `square-90` ids (think-32cl). The declaration holds the twin to the JSON
as the same packing, pose for pose, every time the certificate is read.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `91acf2022`. The certificate is 42384003161478677/10000000000000000000 = 4.2384 ×
10⁻³ below T-303, the house at 90 in both lanes, jazivxt’s packing adopted in the pass
of 15 November. No register bound is pending adoption at 90. It is 9.0936 × 10⁻⁸ below
the certificate of #996. The
[ledger of 15 November for this lane](../../../campaign/issue-intake/upper-bounds-996-997-20261115/README.md)
records #997 as the only report at 90 since T-303, continuing T-303’s packing, and lists
#996 as replaced by its author.
The Kaggle submission’s side the README quotes lies above this side and states no
packing here.

## Exact Replay

The checks below were planned before any of them ran: the expected verdict of every
gross and sharp control on this certificate was written down at 12:56:59Z on 15 November
(SHA-256 `88b26ff1…8cf2`, recorded on the bead), with one branch stated in advance, for
a square that touches its wall exactly.
Before the plan was hashed the lane had read #997 and the diffs of the source’s two new
commits; no route or program had read this certificate.

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes: 3 jobs, 24,030 pair decisions,
2.36 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the left or bottom wall exactly, the least wall clearance 0, and the least
clearance from the top or right wall is about 2.51 × 10⁻²². Every pair clears by at
least about 2.0264 × 10⁻¹², squares 2 and 40, the gap of 2 × 10⁻¹² the README states.
`check --replay` decided the three jobs again.

`sharp-controls` took it to exact contact and 10⁻³⁰ past it on both routes, 11 controls
and 8.9 route CPU seconds
([receipts/sharp-controls.json](receipts/sharp-controls.json)), and every control came
out as stated in advance, the branch for a touching square taken:

- **Wall, pair and near-wall.** The box lowered to the extent (by about 2.51 × 10⁻²²),
  the tightest pair (square 40 against 2) closed by its gap, and every square moved
  toward its near wall by the least near-wall clearance, 0: each is accepted at exact
  contact and refused 10⁻³⁰ past it.
- **Enlarged to a pair.** Square 40, enlarged against 2, is refused at contact for its
  shape alone, and past it for the overlap as well.
- **Enlarged to a wall.** Square 10 already touches its wall; grown by 0 it is accepted,
  and refused 10⁻³⁰ past it for the wall and its shape.
- **Duplicate.** A duplicated square is refused.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share this repository’s centre-direction reader (certificate parsing and
half-angle conversion), `Fraction` arithmetic and the separating-axis method.
Neither shares code with the source’s two checkers, which were not run.

## Pose by Pose and Padding

`devtools.measure_identity` wrote [measure/identity.json](measure/identity.json), and
`devtools.contraction_margin` the `contraction-*.json` receipts under
[measure/](measure/):

- **Against T-303.** No symmetry of the box pairs it one to one with T-303’s packing by
  nearest centres. The optimal assignment, under the identity of the box, moves 87
  squares beyond a thousandth, 32 beyond a hundredth and 6 beyond a tenth (largest
  0.645), and turns 48 squares by more than 10⁻⁶ radians, by up to 22.91 degrees;
  aligned by box centres, 16 squares turn by more than a degree and none reverses its
  tilt. The house witness measures as T-303’s packet, and its regularized view nearly so.
  It is T-303’s arrangement moved by a local search, as the source says, not a new one:
  every square tilted here pairs with one T-303 tilts the same way.
- **Against #996’s certificate.** One to one by nearest centres under the identity, no
  square moved beyond 0.0142 and 8 beyond a hundredth, 19 turned by more than 10⁻⁶
  radians, by up to 1.17 degrees: a refinement of that packing.
  Its twin measures the same.
- **Its tilts.** 40 squares turn, by 22.90 to 30.99 degrees, all clockwise, and the
  other 50 are exactly upright, the README’s 40. T-303 has 44 turned beyond a degree,
  22.61 to 31.56 degrees, all clockwise, and five more within 0.07 degrees of upright.
- **The twin** is the JSON’s packing square for square, no square moved or turned.
- **T-303’s margin** is 1.0988 × 10⁻¹¹, wall slack included (1 − λ\* about 1.1945 ×
  10⁻¹², squares 79 and 81; [contraction-n090.json](measure/contraction-n090.json)), so
  the gain of 4.2384 × 10⁻³, about 3.9 × 10⁸ times the margin, lies wholly outside
  T-303’s padding. RV-3 (think-ruu2) does not reach it.
- **#996’s certificate’s margin** is 9.533 × 10⁻¹² (squares 2 and 40;
  [contraction-n090-996.json](measure/contraction-n090-996.json)), and the step from it,
  9.09 × 10⁻⁸, is about 9.5 × 10³ times that.
- **Its own margin** is 1.8187 × 10⁻¹¹ (1 − λ\* about 2.0222 × 10⁻¹², squares 2 and 40;
  [contraction-n090-own.json](measure/contraction-n090-own.json)). Contracted, it would
  be a square about 1.8 × 10⁻¹¹ smaller, which nobody reported and which is not
  registered.

## The L Step

[measure/l-step-scan.json](measure/l-step-scan.json) is `devtools.l_step_scan` with this
side stood in for 90’s ceiling: it finds the same L-step and monotonicity consequences
as on `main`. From 90 the L step lands at 109 at this side plus one, 10.994038766610,
above 109’s ceiling (10.9497…), and s(89) ≤ 9.9497… is already below this side, so the
bound carries to no other count.

## Stage 4 Review

The stage 4 review of 15 November 2026
([review-2026-11-15-de-winter-996.md](../../../../docs/project/reviews/review-2026-11-15-de-winter-996.md),
lane L180, under think-uhav), written blind to this lane, accepted the certificate #996
named before the author replaced it; the
[64d5ee7 packet](../de-winter-s90-64d5ee7-2026-11-15/README.md) reconciles it with this
lane’s replay of that certificate.
Its addendum of the same day (lane L182, the review’s last section, with its programs
and receipts under `addendum-997/` of the review-only directory
`de-winter-996-review-2026-11-15`) ran the review’s frozen checker unchanged on this
certificate and its twin, and accepts it: every square, wall and all 4,005 pairs decided
twice, by separating axes in Python integers and by exact clipping in GMP rationals, and
26 of 26 controls as stated in a plan hashed before they ran.

This lane read the addendum at 13:21Z on 15 November, after its own replay, controls and
measurements of this certificate (13:08Z) and its records for it (13:21Z) were
committed. Read against this packet’s receipts, the addendum’s least pair margin
(2.02641179076 × 10⁻¹², squares 2 and 40) is the replay’s exactly; its right and top
clearance, 2.51389952 × 10⁻²², is the amount the sharp controls lowered the side by; its
17 wall contacts, each along an edge, include square 10, the one the sharp controls grew
by 0. Its tilts (50 squares exactly upright, 40 turned 22.90 to 30.99 degrees), its
contraction margins (T-303 1.098813 × 10⁻¹¹, #996’s certificate 9.532970 × 10⁻¹², its
own 1.818734 × 10⁻¹¹) and its identity against T-303 (87, 32 and 6 squares beyond a
thousandth, a hundredth and a tenth, largest 0.645) and against #996’s certificate
(square k with square k, largest move 0.0142) are [measure/](measure/)’s. No
disagreement.

What the addendum adds:

- **F14**: the replacement is #996’s arrangement re-optimized, squares moving relative
  to one another; the step is 9,539 times #996’s contraction margin, so it is not
  padding taken off #996.
- **F15**: #997 says the arrangement is as #996 states, but the registration request at
  the head gives the corrected counts (44 and 40 leaning squares, four upright in the
  upper left, four at the top turned further, one 0.32 lower), which reproduce and which
  the record takes.
- **F11 on the twin**: the corner adapter refused the twin as published; this lane’s
  `witness-corners-opposite` reads it back to the JSON’s poses, as the addendum’s
  modified copy did.
- F1 to F13 otherwise hold with this certificate’s values, F10 and F12 answered by the
  author’s text at the pin, and the significance stays S3.

Its questions for the author hold nothing open: which text to record; whether #996’s
near-upright turn was the rational rounding; what produced the step; and L180’s
questions on the twin’s form and on publishing the search and the linear program.

## Adoption

The case adopted the certificate as its house at 90 in the pass of 16 November 2026
under the house rule, as T-304, in place of T-303, jazivxt’s packing, which keeps its
certificate as history.
The pass of 15 November had already moved 90, and a day’s archive holds one prior state
a count, so this lane wrote the adoption at 00:01Z on 16 November.
jazivxt is the packing’s finder and Joost de Winter its improver.
Both strong generators ran on the new witness
([the runs](../../../cases/regularized_drawings/think-32cl-2026-11-16/README.md)), and
the selection draws Evan Daniel’s same-side view, admitted at row 10. His driver also
solved the witness to a certified KKT local minimum 2.698 × 10⁻¹¹ below the side, about
1.48 times the certificate’s own contraction margin (1.8187 × 10⁻¹¹) and beyond it, held
at row 3 as a register candidate and not admitted (RV-3). The translation-escape screen,
derived again on the new witness, finds 12 of its 90 squares translating and none
separating, against T-303’s 31 and 15.

## What Is Not Established

- **The linear program’s first-order statement** and any optimality: not replayed here.
- **The local search’s history**: which groups were moved, in what order, is the
  source’s statement.
- **Human oversight**: no record is retained.

## Credit and Licence

The packing is T-303’s, jazivxt’s packing from shifted copies of a crop of Joost de
Winter’s 157, as Joost de Winter improved it by a local search, whose certificate this
repository holds. #996 says the local search was run with GPT-6.1 Sol Max (OpenAI) and
the local optimization, rational certificate, checks and figures were produced with
Claude Fable 5.2 (Anthropic), both under his direction, and #997 says so again; at
`64d5ee7`, `n90/README.md` named the search’s model “OpenAI Codex (GPT-6 Astra)”. The
record credits people, not AI agents ([attribution.md](../../../../attribution.md)), and
states the assistance in the source’s words.
The bibliography key is **[de Winter s90 upper bound 2026-11-15]**.

Everything here is published under the MIT licence, copyright (c) 2026 Joost de Winter,
by `LICENSE` at the pin, which the root README says covers all files.

## Commands

From `packing/`, with the project interpreter.
The identity measurement reads the house witness and its regularized view as they stand
at main `91acf2022`; the contraction margins read the packets:

```bash
P=de-winter-s90-upper-bound-2026-11-15
O=resources/web/de-winter-s90-64d5ee7-2026-11-15/source/n90
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 90 "DEWINTER=packet:$P" \
  'T-303=packet:jazivxt-s90-upper-bound-2026-11-15' \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-090-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-090.yaml' \
  "twin=witness-corners-opposite:resources/web/$P/source/n90/n90_witness.yaml" \
  "#996=center-direction-json:$O/n90_exact.json" \
  "#996-twin=witness-corners-opposite:$O/n90_witness.yaml" \
  --out resources/web/$P/measure/identity.json
python -m devtools.contraction_margin --n 90 'T-303=packet:jazivxt-s90-upper-bound-2026-11-15' \
  --against "dewinter-997=packet:$P" --out resources/web/$P/measure/contraction-n090.json
python -m devtools.contraction_margin --n 90 "dewinter-996=center-direction-json:$O/n90_exact.json" \
  --against "dewinter-997=packet:$P" --out resources/web/$P/measure/contraction-n090-996.json
python -m devtools.contraction_margin --n 90 "dewinter-997=packet:$P" \
  --out resources/web/$P/measure/contraction-n090-own.json
python -m devtools.l_step_scan --with 90=99940387666098521323/10000000000000000000 \
  --out resources/web/$P/measure/l-step-scan.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
