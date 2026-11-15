# Joost de Winter’s s(90) Certificate at 64d5ee7

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/64d5ee762a1159248d375973fb33825d51da637d)
at `64d5ee762a1159248d375973fb33825d51da637d` (committed 2026-11-15T11:27:26Z), which
[issue #996](https://github.com/jlevy/squares/issues/996) names.
The issue was opened at 11:30:13Z. The repository is watched, and the lane fetched it at
12:01Z, when its head was `9cafa33`.

The folder `n90/` first appeared at `64d5ee7` with the certificate, the Witness/v2 file,
two checkers, two figures and the README, with a row and a paragraph of the root README.
The next commit, `0c9bcd2` (11:27:49Z), adds `n90/REGISTRATION.md`, the issue’s text in
the form of this repository’s registration template, and `n90/SHA256SUMS`. The head,
`9cafa33` (11:29:27Z), changes the model named for the local search from “OpenAI Codex
(GPT-6 Astra)” in `n90/README.md` and “OpenAI Codex” in the root README to “GPT-6.1 Sol
Max (OpenAI)”, the name the issue gives, in both and in `REGISTRATION.md`, and updates
the checksums.
Neither changes the certificate, the witness, the checkers or the figures:
each has the same Git blob at the pin and the head, and `SHA256SUMS` at the head states
their digests, which match.
Both are read in [campaign/intake-watch.yaml](../../../campaign/intake-watch.yaml).
GitHub’s activity log was not readable from this session, so the push time of `64d5ee7`
is not read; no other report reached 90 in the 2 minutes 47 seconds before the issue, so
the ledger dates the claim by the issue, with the first commit kept.

Intake lane L181 (think-32cl) retained it, replayed it, measured it and registered it on
15 November 2026 as **T-304**. The blind stage 4 review of lane L180 accepted it the
same day, so it is at V3/C3; the adoption at 90 waits for a pass of 16 November, since
the pass of 15 November already moved 90.

## What the Source Claims

- `n90/n90_exact.json` states 90 unit squares as `[center_x, center_y, cos, sin]` rows
  of exact rationals, `(cos, sin)` the unit direction of one edge, with the side
  199880777150913904183/20000000000000000000 = 9.99403885754569520915, which terminates
  at 20 places. The issue and the root README round it up at 12 places, 9.994038857546,
  and `n90/README.md` prints it in full.
  `n90/n90_witness.yaml` states the same packing as a `packing.squares:Witness/v2`
  document of rational corners, with the softschema envelope and a claim of
  `coordinate_provenance: reported`.
- **The construction.** The packing starts from T-303, jazivxt’s packing of
  [issue #989](https://github.com/jlevy/squares/issues/989), the record at 90, which
  jazivxt built from a crop of the source’s own packing of 157 squares (T-293). The
  README says T-303 has a cluster of 49 squares that lean away from the axes inside a
  frame of axis-aligned squares, and that a local search changed small groups of squares
  in position and angle, optimized the packing again after each change, and kept the
  changes that gave a smaller side.
  In the new packing, it says, the cluster has 37 leaning squares, seven squares in the
  upper left of the cluster have a new angle, and five squares along the left wall are
  axis-aligned.
- **The local optimum.** A linear program over all 90 squares, every contact linearized
  at the solution, found no first-order improvement larger than 4 × 10⁻¹⁰. The
  certificate keeps a smallest gap of 10⁻¹² between squares, so an exact solution of the
  contact equations would be smaller by about that much.
  Local optimality has no formal proof.
- **The Kaggle note.** A public merged submission to the Kaggle competition “Squares in
  Squares” (bestbryant/claude_code_squaresinsquares, 15 November 2026) lists
  9.998277166917 for n = 90; the leaderboard’s best sides were not available to the
  author.
- **The checkers.** `verify_exact.py` (separating axes, for every pair whose centres are
  closer than √2) and `check_area.py` (the area of each close pair’s clipped
  intersection), both Python’s `Fraction` and its standard library only.
  The issue says they have one author and read the same input file but share no code,
  and that each reports 90 squares and 202 close pairs.
  It says this repository’s `check_rational_witness_independent.py` at `ed7aff6` reports
  “VERIFIED: 90 squares, 4005 pairs” on the witness, and that the witness validates
  against `witness.schema.yaml`. Neither of the author’s checkers ran here.
- **Credit.** The issue asks that the bound be credited to Joost de Winter as an
  improvement of jazivxt’s packing.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the licence, the root README and the whole of `n90/`, 9 files: 6 retained
under [source/](source/) and 3 pinned by digest: `LICENSE`, against the byte-identical
copy the
[227, 229 and 260 packet](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md)
retains, and the two figures.
`verify_exact.py` and `check_area.py` are new files, retained as data and never opened
or run here.

**The twin.** `n90_witness.yaml` lists each square’s corners from the vertex opposite
the one this repository’s corner reader starts from, so `witness-corners` reads every
square a half turn from the JSON’s pose, which a square’s symmetry leaves unchanged.
The reader now also accepts the witness’s schema address and its `square-1` to
`square-90` ids (think-32cl). Measured by `devtools.measure_identity`, the witness is
the JSON’s packing square for square, no square moved and none turned modulo a quarter
turn ([measure/identity.json](measure/identity.json), the `twin` row).

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `91acf2022`. The certificate is 84766187606095817/20000000000000000000 = 4.2383 ×
10⁻³ below T-303, the house at 90 in both lanes, jazivxt’s packing adopted in the pass
of 15 November. No register bound is pending adoption at 90. The
[ledger of 15 November for this lane](../../../campaign/issue-intake/upper-bounds-996-20261115/README.md)
records it as the only report at 90 since T-303, continuing T-303’s packing.
The Kaggle submission’s side the README quotes, 9.998277166917, lies above this side and
states no packing here.

## Exact Replay

The checks below were planned before any of them ran: the expected verdict of every
gross and sharp control was written down at 12:03:58Z on 15 November (SHA-256
`b441e936…c7ea3`, recorded on the bead), with one branch stated in advance, for a square
that touches its wall exactly.
Before the plan was hashed the lane had read the source’s README and the issue, compared
the witness’s corner lists with the JSON’s poses in a scratch look, and summarized the
witness with `packing-witness inspect`; no route or control had read the certificate.

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes: 3 jobs, 24,030 pair decisions,
3.89 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the left or bottom wall exactly, the least wall clearance 0, and the least
clearance from the top or right wall is about 5.07 × 10⁻²¹. Every pair clears by at
least about 1.0641 × 10⁻¹², squares 2 and 40, the gap of 10⁻¹² the README states.
`check --replay` decided the three jobs again.

`sharp-controls` took it to exact contact and 10⁻³⁰ past it on both routes, 11 controls
and 15.6 route CPU seconds
([receipts/sharp-controls.json](receipts/sharp-controls.json)), and every control came
out as stated in advance, the branch for a touching square taken:

- **Wall, pair and near-wall.** The box lowered to the extent (by about 5.07 × 10⁻²¹),
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
  nearest centres. The optimal assignment, under the identity of the box, moves 89
  squares beyond a thousandth, 34 beyond a hundredth and 6 beyond a tenth (largest
  0.646), and turns 48 squares by more than 10⁻⁶ radians, by up to 22.91 degrees;
  aligned by box centres, 16 squares turn by more than a degree and none reverses its
  tilt. The house witness measures as T-303’s packet, and its regularized view nearly so
  (6 beyond a tenth, largest 0.645). It is T-303’s arrangement moved by a local search,
  as the source says, not a new one: every square tilted here pairs with one T-303 tilts
  the same way.
- **Its tilts.** 40 squares turn, by 22.90 to 30.99 degrees, all clockwise; the other 50
  lie within 10⁻³ degrees of upright.
  T-303 has 44 turned beyond a degree, 22.61 to 31.56 degrees, all clockwise, and five
  more within 0.07 degrees of upright.
  The README counts 49 leaning squares in T-303 and 37 here; the counts here are 49 (44
  and 5) and 40.
- **T-303’s margin** is 1.0988 × 10⁻¹¹, wall slack included (1 − λ\* about 1.1945 ×
  10⁻¹², squares 79 and 81; [contraction-n090.json](measure/contraction-n090.json)), so
  the gain of 4.2383 × 10⁻³, about 3.9 × 10⁸ times the margin, lies wholly outside
  T-303’s padding. RV-3 (think-ruu2) does not reach it.
- **Its own margin** is 9.533 × 10⁻¹² (1 − λ\* about 1.0599 × 10⁻¹², squares 2 and 40;
  [contraction-n090-own.json](measure/contraction-n090-own.json)). Contracted, it would
  be a square of side about 9.99403885753616, which nobody reported and which is not
  registered.

## The L Step

[measure/l-step-scan.json](measure/l-step-scan.json) is `devtools.l_step_scan` with this
side stood in for 90’s ceiling: it finds the same L-step and monotonicity consequences
as on `main`. From 90 the L step lands at 109 at this side plus one, 10.994038857546,
still above 109’s ceiling (10.9497…), and s(89) ≤ 9.9497… is already below this side, so
the bound carries to no other count.

## Stage 4 Review

The stage 4 review of 15 November 2026
([review-2026-11-15-de-winter-996.md](../../../../docs/project/reviews/review-2026-11-15-de-winter-996.md),
lane L180, under think-uhav), written blind to this lane, accepts the certificate with
seven findings, all notes, none blocking.
Its clean-room checker decides every square, wall and all 4,005 pairs twice, by
separating axes in Python integers from the JSON’s poses and by exact clipping of the
twin’s own corners in GMP rationals, and all 26 of its controls were decided as stated.
Its programs and receipts are in the review-only directory
`de-winter-996-review-2026-11-15`.

This lane read its frozen findings at 12:39Z on 15 November, after its own replay,
controls and measurements (12:17Z) and registration (12:38Z) were committed.
Read against this packet’s receipts, the review’s least pair margin (1.06410355706 ×
10⁻¹², squares 2 and 40) is the replay’s exactly.
Its 18 wall contacts, nine at the left and nine at the bottom, square 10 among them, are
the replay’s contacts, square 10 the one the sharp controls grew by 0. Its right and top
clearance,
9909955765625015940074994030630443123/1953125000000000000000004987507812500000000000000000000000,
is the amount the sharp controls lowered the side by.

Its twin, listed counterclockwise from the corner at C + (u + v)/2 of each JSON pose, is
the half turn [measure/identity.json](measure/identity.json)’s `twin` row reads, no
square moved.
Its tilts (50 squares sharing one direction 1.831 × 10⁻¹⁰ degrees clockwise
of upright, 40 turned clockwise by 22.90 to 30.99 degrees) are the identity
measurement’s, which counts the 50 within 10⁻³ degrees of upright.
No disagreement.

What the review adds:

- **The claim’s box** (F3): the squares are accepted in the box of the printed side,
  9.994038857546, and refused in the box of its 12-place floor.
- **The side and the extent** (F4): the left and bottom are touched and the right and
  top cleared by 5.07389735200 × 10⁻²¹, so the side is the packing’s extent rounded up
  at 20 places. The smaller box is the owner’s RV-3 question and is not registered.
- **A contact arrangement opened by about 10⁻¹²** (F5): 195 pairs from 1.0641 × 10⁻¹² to
  9.1968 × 10⁻¹², then none below 5.85 × 10⁻⁶.
- **For the author** (F6, F7): no threshold counts the issue’s 37 leaning squares, since
  no square is exactly upright; and the JSON names neither the box nor the rotation
  sense, which read the other way overlaps 52 pairs and which the twin fixes.

## What Is Not Established

- **The linear program’s first-order statement** and any optimality: not replayed here.
- **The local search’s history**: which groups were moved, in what order, is the
  source’s statement.
- **Human oversight**: no record is retained.

## Credit and Licence

The packing is T-303’s, jazivxt’s packing from shifted copies of a crop of Joost de
Winter’s 157, as Joost de Winter improved it by a local search, whose certificate this
repository holds. The issue says the local search was run with GPT-6.1 Sol Max (OpenAI)
and the local optimization, rational certificate, checks and figures were produced with
Claude Fable 5.2 (Anthropic), both under his direction; at the pin, `n90/README.md`
named the search’s model “OpenAI Codex (GPT-6 Astra)”. The record credits people, not AI
agents ([attribution.md](../../../../attribution.md)), and states the assistance in the
source’s words. The bibliography key is **[de Winter s90 upper bound 2026-11-15]**.

Everything here is published under the MIT licence, copyright (c) 2026 Joost de Winter,
by `LICENSE` at the pin, which the root README says covers all files.

## Commands

From `packing/`, with the project interpreter.
The identity measurement reads the house witness and its regularized view as they stand
at main `91acf2022`; the contraction margins read the packets:

```bash
P=de-winter-s90-upper-bound-2026-11-15
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
  "twin=witness-corners:resources/web/$P/source/n90/n90_witness.yaml" \
  --out resources/web/$P/measure/identity.json
python -m devtools.contraction_margin --n 90 'T-303=packet:jazivxt-s90-upper-bound-2026-11-15' \
  --against "dewinter-996=packet:$P" --out resources/web/$P/measure/contraction-n090.json
python -m devtools.contraction_margin --n 90 "dewinter-996=packet:$P" \
  --out resources/web/$P/measure/contraction-n090-own.json
python -m devtools.l_step_scan --with 90=199880777150913904183/20000000000000000000 \
  --out resources/web/$P/measure/l-step-scan.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
