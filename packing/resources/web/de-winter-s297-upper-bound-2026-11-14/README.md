# Joost de Winter’s s(297) Certificate at 7b4701f

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/7b4701f35e815301e4f467d214fab4205ded5eb1)
at `7b4701f35e815301e4f467d214fab4205ded5eb1` (committed 2026-11-14T10:05:30Z), which
[issue #977](https://github.com/jlevy/squares/issues/977) names.
The issue was opened at 10:13:18Z. The repository is watched, and the lane read it at
10:59Z, when its head was `c70defa`.

The folder `n297/` first appeared at `e008214` (10:02:54Z) with the certificate, the
Witness/v2 file, the 250-digit solution, two figures, `verify_exact.py`, the README and the
checksums. `7b4701f` adds `check_area.py` and lists it in the README and checksums, so the
certificate’s bytes are `e008214`’s. GitHub’s activity log was not readable from this
session, so the push time of `e008214` is not read. By the owner’s rule of 14 October 2026
the folder would be a report from that commit if its push came first, but no other report
reached 297 in the 10 minutes 24 seconds before the issue, so the ledger dates the claim
by the issue, with the first commit kept, and the verdict is the same either way.
The next commit, `5fcb350` (10:10:06Z), adds `n297/REGISTRATION.md`, the issue’s text in
the form of this repository’s registration template, and lists it; it changes no packing
and is read in [campaign/intake-watch.yaml](../../../campaign/intake-watch.yaml).
The head, `c70defa` (10:39:38Z), adds `above324_from_n297/`, which
[issue #979](https://github.com/jlevy/squares/issues/979) reports and the
[de-winter-issue979-2026-11-14](../de-winter-issue979-2026-11-14/README.md) packet retains.

Intake lane L154 (think-g2ax) retained it, replayed it and registered it on 14 November
2026 as **T-299**. The blind stage 4 review of lane L153 accepted it the same day, so it
is at V3/C3, and the case adopted it as its house in place of T-174 under the house rule.

## What the Source Claims

- `n297/n297_witness.yaml` states 297 unit squares by centre and the unit direction of one
  edge, every number an exact rational, as a `packing.squares:Witness/v2` document with
  the softschema header and a claim block. `n297/n297_exact.json` states the same packing
  as `[center_x, center_y, cos, sin]` rows with the side.
- **The side.** The issue and the root README round it up at 12 places, 17.739455558289,
  which the packet admits; `n297/README.md` cuts it at 50 places,
  17.73945555828895172457454811760973557490907042860652…, and compares it with the
  record’s 17.7404172875438019, an improvement of 0.00096.
- **The construction.** The packing keeps the layout of T-174, the record at 297
  (Francisco Couzo’s packing, Evan Daniel’s exact optimum, PingYou Ltd’s refinement): an
  upper left and a lower right block of axis-aligned squares with staircase edges, a block
  of 10 squares in the lower left and upper right corners, and a diagonal band of 18
  columns of tilted squares between the staircases. Two things are new. Each staircase
  has two steps of double size, at the 6th and 13th columns of the band, between which the
  band lies one staircase step closer to the upper left block; the upper left block holds
  6 squares fewer and the lower right block 4 more, the column at each double step holds 7
  squares and the other 16 hold 6, so the band holds 110 squares and the blocks 187. And
  the band’s columns lean in two groups, by 0.375 degrees one way on the lower left and
  the other way on the upper right (89 of the 110), so the lean changes direction once,
  where T-174’s columns lean in four groups by 0.260 degrees and change direction three
  times. The double step was taken from the staircases of the source’s own pinwheels at
  132 and 157 (T-292 and T-293).
- **The local optimum.** The band was optimized by a sequence of linear programs,
  restarted many times from random changes to groups of band squares; two series of
  restarts with different seeds ended at 17.7394555582889, and a linear program over all
  297 squares found no first-order improvement. The 4,289 contact equations were then
  solved in 330-digit arithmetic, holding to 10⁻³⁰⁶, and the 33 other near contacts stay
  open by at least 2.1 × 10⁻⁷. The certificate’s side is 1.8 × 10⁻⁵⁹ above that solution.
  The place where the lean changes was also tried one and two columns either side of the
  middle before the restarts: 17.7394733018 in the middle and 17.7394781380 at the other
  four. Local optimality has no formal proof.
- **The Kaggle note.** The per-puzzle leaderboard of the Kaggle competition “Squares in
  Squares” listed 17.7404101723 as the best side for n = 297 on 13 November 2026. It shows
  no packings.
- **The checkers.** `verify_exact.py` (separating axes) and `check_area.py` (the area of
  each close pair’s clipped intersection), both Python’s `Fraction` and its standard
  library only. The issue says they share one author and the input file but no code, and
  that each reports 297 squares and 632 close pairs; it says the witness validates against
  this repository’s `witness.schema.yaml` at `7629f5a`. Neither checker ran here.
- **Credit.** The issue asks that the result be credited to Joost de Winter as a packing
  that builds on T-174.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the licence, the root README and the whole of `n297/`,
11 files: 7 retained under [source/](source/) and 4 pinned by digest: `LICENSE`, against
the byte-identical copy the
[227, 229 and 260 packet](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md)
retains; `verify_exact.py`, against the byte-identical copy the
[s132 packet](../de-winter-s132-upper-bound-2026-11-11/README.md) retains; and the two
figures. `n297/SHA256SUMS` states the digests of the eight other files of `n297/`, and they
match. The JSON is stored compressed (below).

**The witness and the loader.** `n297_witness.yaml` passes this repository’s witness
schema, as the issue says, and the loader refuses it on one rule the schema does not
state: its claim is `coordinate_provenance: verified` with no `certificate` record, as were
the source’s own witnesses of 132 and 157 from `57de046`
([the method packet](../de-winter-method-132-157-2026-11-12/README.md)).
The import reads it with `witness-center-basis-unreplayed`, written for it: the reading
`witness-center-basis` makes, held to the schema and to every other semantic rule, the
claim read and not believed. `read_facts` holds the JSON to it as the same packing, scalar
for scalar.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `da5091505`. The certificate is 9.6173 × 10⁻⁴ below T-174, the house (Francisco
Couzo’s packing, improved by Evan Daniel and PingYou Ltd). It is also below T-247, Hyukdong
Kim’s exact degree-21 side of T-174’s packing, registered and not the house, 3.4 × 10⁻⁹⁰
below T-174. The
[ledger of 14 November](../../../campaign/issue-intake/upper-bounds-977-979-20261114/README.md)
records it as a new packing, the only report at 297. The Kaggle leaderboard side the README
quotes, 17.7404101723, states no packing, so it is no report; it lies above this side.

## Exact Replay

The checks below were planned before any of them ran: the expected verdict of every gross
and sharp control was written down at 11:06:15Z on 14 November (SHA-256 `18ad29d0…6054`,
recorded on the bead).

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes: 3 jobs, all 43,956 pairs a job
and route, 263,736 pair decisions, 184.1 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes. Squares touch the walls
exactly, and every pair clears by at least 10⁻⁶⁰ less about 1.1 × 10⁻²⁵⁰. `check
--replay` decided the three jobs again.

`sharp-controls` took it to exact contact and 10⁻³⁰ past it on both routes, 11 controls
and 686 route CPU seconds ([receipts/sharp-controls.json](receipts/sharp-controls.json)),
and every control came out as stated in advance:

- **Wall, pair and near-wall.** The box lowered to the extent (by 0, squares touching the
  top and right walls), the tightest pair (square 237 against 232) closed by its gap of
  10⁻⁶⁰ less about 10⁻²⁵⁰, and every square moved toward its near wall by the least
  near-wall clearance, 1.5 × 10⁻⁶⁰: each is accepted at exact contact and refused 10⁻³⁰
  past it.
- **Enlarged to a pair.** Square 237, enlarged against 232, is refused at contact for its
  shape alone, and past it for the overlap as well.
- **Enlarged to a wall.** Square 1 already touches its wall; grown by 0 it is accepted,
  and refused 10⁻³⁰ past for the wall, its shape and an overlap with a neighbour that
  clears it by about 10⁻⁶⁰.
- **Duplicate.** A duplicated square is refused.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share this repository’s witness reader (certificate parsing and half-angle
conversion), `Fraction` arithmetic and the separating-axis method. Neither shares code
with the source’s two checkers, which were not run.

## Pose by Pose and Padding

`devtools.measure_identity` wrote [measure/identity.json](measure/identity.json), and
`devtools.contraction_margin` the `contraction-*.json` receipts under [measure/](measure/):

- **Against T-174.** No symmetry of the box pairs it one to one with T-174’s packing by
  nearest centres, and the house witness and its regularized view measure the same. The
  optimal assignment of least summed squared move, best under the box’s symmetry 5, moves
  55 squares beyond a tenth, 69 beyond a hundredth and 117 beyond a thousandth (largest
  0.700), and turns 114 by up to 44.74 degrees; aligned by box centres, 11 squares turn
  by more than a degree and 34 reverse their tilt. It is a new arrangement relative to
  T-174’s packing, in T-174’s layout.
- **Its tilts.** 110 squares turn, by 44.11 to 44.95 degrees, 61 one way and 49 the other,
  the band of 110 the README counts; the other 187 are exactly upright. T-174 has 107
  tilted squares, by 44.74 to 44.98 degrees, 63 one way and 44 the other, and 190 upright
  within 10⁻³ degrees, where the README’s counts (a band 2 squares larger than T-174’s, the
  blocks 2 smaller) imply a band of 108.
- **T-174’s margin** is 0, its pair 274 and 292 already touching, so the whole gain of
  9.617 × 10⁻⁴ lies outside the predecessor’s padding
  ([contraction-n297.json](measure/contraction-n297.json)). RV-3 (think-ruu2) does not
  reach it.
- **Its own margin** is 1.824 × 10⁻⁵⁹ (1 − λ\* = 10⁻⁶⁰, the binding pair squares 232 and
  237; [contraction-n297-own.json](measure/contraction-n297-own.json)), the 1.8 × 10⁻⁵⁹
  the README states. Contracted, it would be a square of side 17.7394555582889517245…,
  which nobody reported and which is not registered.

## The L Step

[measure/l-step-scan.json](measure/l-step-scan.json) is `devtools.l_step_scan` with this
side stood in for 297’s ceiling: it finds the same L-step and monotonicity consequences as
on `main`, so the bound carries to no other count of the corpus. From 297 the L step lands
at 332, beyond the horizon, at this side plus one: that is #979’s 332, a certificate the
[issue 979 packet](../de-winter-issue979-2026-11-14/README.md) retains and the record
holds as a beyond-horizon row.

## Stage 4 Review

The stage 4 review of 14 November 2026
([review-2026-11-14-de-winter-977-979.md](../../../../docs/project/reviews/review-2026-11-14-de-winter-977-979.md),
lane L153, under think-gabn), written in a separate lane blind to this one throughout,
accepts this certificate and #979’s two, nothing blocking or major. Its programs and
receipts are in the review-only directory
[de-winter-977-979-review-2026-11-14](../de-winter-977-979-review-2026-11-14/README.md).

- **Feasibility.** Its clean-room checker decides the JSON and the Witness/v2 twin,
  every square, wall and all 43,956 pairs, by separating axes in Python integers and by
  exact clipped areas in `gmpy2.mpq`, with no distance filter: 33 wall contacts (16 top,
  17 right), the left and bottom cleared by exactly 1.5 × 10⁻⁶⁰, no pair touching, and
  the least pair margin 10⁻⁶⁰ less about 10⁻²⁵⁰, at squares 232 and 237. Its 19 controls
  at 297, stated beforehand, came out as stated, among them the squares accepted in the
  box of side 17.739455558289 itself and refused in the box of its 12-place floor (F5),
  and the rotation read the other way refused for 112 overlapping pairs.
- **Against this lane.** Read against this packet’s receipts once both were done, its
  least pair margin, wall contacts and near-wall clearance are the replay’s exactly, and
  its contraction receipts (T-174’s margin 0 at squares 274 and 292; this certificate’s
  1.824 × 10⁻⁵⁹ at squares 232 and 237) and identity against T-174 (55 squares beyond a
  tenth, largest 0.700; 11 turned and 34 reversed by box centres) equal
  [measure/](measure/)’s. The 409 sharp controls of the issue 979 packet were still running
  when the review was read; nothing else here ran after it.
- **The lineage (F11).** The README’s counts hold: the upper-left block has 72 squares
  against T-174’s 78, the lower-right 95 against 91, and the band 110 against 108,
  counting T-174’s upright square 207 at the top wall, which closes its band and belongs
  to neither block; 89 band squares lean by 0.375 degrees against T-174’s 98 at 0.260,
  and the lean changes direction once against three times. That is the band of 108 this
  packet’s own tilt count left open.
- **The arithmetic (F9, F10).** The claim is the side’s 12-place ceiling, the gain
  9.6173 × 10⁻⁴; no padding is reached, and RV-3 does not apply. The README’s 250-digit
  solution lies 1.824 × 10⁻⁵⁹ below the side, and its next near contact, 2.103 × 10⁻⁷
  (squares 246 and 253), is the review’s next pair after the 794 below 10⁻³⁰. No
  s(m) + k closed form lies within 10⁻⁹.
- **The twin (F8, minor).** The review’s one finding above a note is the twin’s verified
  claim with no certificate record, which this repository’s loader refuses; this packet
  reads the twin with `witness-center-basis-unreplayed`, and the review read the JSON.
- **Notes for the author.** F6 (the JSON names no box), F13 and F14 (at 409, below), and
  F15: both checkers decide by `assert`, which `python -O` removes.

### Questions for the Author

The review’s questions, informational and holding nothing open:

1. Would you add a `certificate` record to `n297_witness.yaml`, or set its
   `coordinate_provenance` to `reported`, so that this repository’s witness reader
   accepts it (F8)?
2. Would you add Witness/v2 twins for 332 and 409, or name the box and its origin in the
   JSON `format` line (F6)?
3. The left and bottom walls of the 297 box are cleared by 1.5 × 10⁻⁶⁰ rather than
   touched, while the top and right are touched. Was that deliberate?
4. In what sense is the recorded value at 409 “built in the same way from the record
   T-174”, when its side lies 3.16 × 10⁻⁹ above T-174 + 3 and its squares are placed
   otherwise (F14)?
5. Would you say “about 45°” for the corner square at 409, or give its exact direction
   (F13)?
6. Would you make both checkers raise rather than `assert` (F15)?

## The Register

T-299 records the claim at V3/C3, S3, as the stage 4 review confirmed. The case adopted
it as its house in the pass of 14 November 2026 under the house rule, in place of T-174,
which keeps its certificate as history and still houses other counts, with Joost de
Winter the packing’s finder in the layout of Francisco Couzo’s packing as Evan Daniel and
PingYou Ltd improved it. Both strong generators ran on the new
witness ([the runs](../../../cases/regularized_drawings/think-g2ax-2026-11-14/README.md)):
the picture is grid-slack’s 0.5-degree view, admitted at row 10, with no light, uneven or
near-axis square and 17 angle classes, as the axis tool’s view has, and more full shared
sides (774 and 904 against 728 and 886), mirrored across the falling diagonal by the flip
record. Evan Daniel’s driver refused its same-side view; its certified KKT solve lies
1.824 × 10⁻⁵⁹ below the side, the certificate’s own margin, and its solved view,
1.77 × 10⁻¹⁹ above it, is held at row 4, so there is no register candidate (RV-3). The
settlement of 297 on T-174’s witness lapsed with the adoption. The rigidity block,
derived again on the new witness, stays not rigid: 62 of its 297 squares translate,
against 41 of T-174’s.

## What Is Not Established

- **The 330-digit solution as a local optimum**, and any optimality: not replayed here.
- **The construction’s history**: the double step’s source in the 132 and 157 pinwheels,
  and the restarts, are the source’s statements.
- **Human oversight**: no record is retained.

## Credit and Licence

The packing is Joost de Winter’s, in the layout of T-174 (Francisco Couzo’s packing, as
Evan Daniel and PingYou Ltd improved it), whose certificate the record holds, so its
lineage builds on this project. The source says the construction, optimization,
high-precision solution, rational certificate, checks and figures were produced with Claude
Fable 5.2 (Anthropic) under his direction. The bibliography key is
**[de Winter s297 upper bound 2026-11-14]**.

Everything here is published under the MIT licence, copyright (c) 2026 Joost de Winter, by
`LICENSE` at the pin, which the root README says covers all files.

## Commands

From `packing/`, with the project interpreter. The identity measurement reads the house
witness and its regularized view as they stand at main `da5091505`; the contraction margins
read the packets:

```bash
P=de-winter-s297-upper-bound-2026-11-14
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 297 "DEWINTER=packet:$P" \
  'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  'regularized=witness-corners:atlas/known-best/regularized/n-297-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-297.yaml' \
  --out resources/web/$P/measure/identity.json
python -m devtools.contraction_margin --n 297 'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  --against "dewinter-297=packet:$P" --out resources/web/$P/measure/contraction-n297.json
python -m devtools.contraction_margin --n 297 "dewinter-297=packet:$P" \
  --out resources/web/$P/measure/contraction-n297-own.json
python -m devtools.l_step_scan --with 297=S297 --out resources/web/$P/measure/l-step-scan.json
```

In the last command `S297` is the `exact_side` in the packet’s claim record.

## Compressed Files

| Stored file | Origin | Git blob of stored file | SHA-256 of decompressed source |
| --- | --- | --- | --- |
| `source/n297/n297_exact.json.gz` | upstream | `b200b925626838325641b2da5fd548c74d36ac6c` | `7ff1712fc2efe66661377481e1d37b8577b30a9979f10c83d2539cd2e31d6632` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
