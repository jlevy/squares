# Mathematical Review of Issue 806, 25 October 2026: Code and Outputs

This directory keeps the code of the stage 4 mathematical review of Evan Daniel’s report
of $s(182) \le 13.970916436215$ (jlevy/squares#806), with everything it printed.
The review itself is
[review-2026-10-25-evand-n182.md](../../../../../../docs/project/reviews/review-2026-10-25-evand-n182.md).
It was written by the review lane c-review-806-math (bead think-meci): Claude, strongest
tier, maximum reasoning, working for the intake coordinator coord-intake-1024.
`record-changes.md` holds the draft registry records for the records lane.

## What Its Authors Read

The lane wrote the four Python programs here from the mathematics and the certificate
format, before reading any earlier work on this result. It added `custody.sh` after reading
the review of 24 October 2026, which keeps a custody listing of the same kind.

- **The certificate format.** It is the certificate’s own first line: a centre, and the
  frame $(c, s) = ((1-t^2)/(1+t^2), 2t/(1+t^2))$ from $t = \tan(\theta/2)$.
- **The source’s outputs, to compare.** These were the solver report `s182-1024.json`,
  the comparison files `s182-1024_prior.json` and `s182-1024_vs_prior.json`, the
  regularized report `s182-1024_regularized.json`, issue 806’s text and the commit
  message.
- **Not read.** The lane opened none of the source’s programs: `verify_cert.py`,
  `verify_cert2.py`, `exactsolve.py` and the search code. Nor did it open this
  repository’s maintained exact routes or the code of `devtools.measure_identity`.
  The stage 1 triage’s files and the review of 24 October 2026 that the review document
  follows for layout were read only after the findings were written.

The source’s commit carries a Claude co-author trailer, so the authorship overlaps the
producer’s in system family. The prompts and the code are separate.

## Inputs

The source’s files are those of evand/square-packing at
d99925d1298262c4ddb81c95abbb6f45adca8d3d, under `search/packer/candidates/`. They were
copied out of a clone with `git show` and read as data, never run.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `s182-1024.cert` | 30,648 | `9e12e0a42b05c4fcd2181c5255a4a19ab1aeb9a9f8c95f9943a20998a415fe97` |
| `s182-1024_regularized.cert` | 30,526 | `f1ec415a194b9c0d01d86d23d917a90375779dbd0739966287f189109fd2fabf` |
| `s182-1024.exact.txt` | 35,915 | `3ed2a8a82d30612b378ec23cc205d2194222580ddade133d4c59f79d2dc76893` |
| `s182-1024.input.txt` | 8,838 | `e79897cb13a1fd29c472acec01b07a56e85f5f3c708212e889f71a362d52f45c` |
| `s182-1024.json` | 4,376 | `e5491852a87029b8e3b871a481925ae345470a87878ac570724db8cca8f18461` |

The comparison packings come from this repository at bb756e193, and each receipt lists
the paths and digests it read.
They are T-174’s certificate as retained (`pingyou-pr574-certificates-2026-10-13`), the
house witness `witnesses/known-best/n-182.yaml`, T-098’s and T-056’s packings at 182,
and the 211 packings of T-188, T-175, T-182 and T-181.

## Programs

Every Python program runs under the project interpreter (Python 3.14.7) in isolated mode
and only reads its arguments. `programs/run_review.sh SRC REPO` reproduces every output in
`out/` except the custody listing. SRC is a directory holding the four source files
above: the packet’s `source/search/packer/candidates/` once the records lane retains
them, or, as on 25 October, the lane’s scratch copies of the same blobs. REPO is a
checkout of this repository, here the worktree at `main` `bb756e193`.
The full run took 129 CPU seconds, niced, one program at a time, on a shared four-core
host.

### `programs/custody.sh` (Decides Nothing)

`programs/custody.sh CLONE` prints the commit’s metadata and message and, from Git’s
object store, the blob id, size and SHA-256 of each source file read
(`out/custody.txt`). Nothing in the clone is executed.
Every file is the blob at `d99925d`, and the certificate is blob `a1c01bdf`.
The push time, 04:16:05Z in `3c335fe..d99925d`, is the stage 1 triage’s reading of
GitHub’s activity log. This session had no API access to the repository.

### `programs/exact_check.py` (Decides)

This is the clean-room exact checker.
It reads a certificate strictly: every token must be an integer or an integer fraction.
It builds each square’s corners as $(x, y) + u(c, s) + v(-s, c)$ with
$u, v \in \{-\tfrac12, \tfrac12\}$, and decides the packing in `fractions.Fraction`
arithmetic by two methods that share only that reader and corner construction:

- **Separating axes (SAT).** Every corner lies in $[0, S]^2$. For every pair, some edge
  normal of the two squares, an exact unit vector, has projection intervals that overlap
  in at most a point.
- **Exact clipped areas (AREA).** Every square clipped to the box keeps area 1. For every
  pair, the area of one square clipped to the other (Sutherland–Hodgman over Q) is 0.

`check` decides all 182 walls and 16,471 pairs by both methods. It prints the side and its
upward 12-place print, the least slack at the low walls, at the high walls and between
pairs, and the counts of pairs and walls within 1e-15. It also prints the SAT decision
with the rotation sense reversed: the same centres, each frame read as $(c, -s)$.

`controls` decides fourteen mutations, each by both methods over every wall and pair:

- the box at the packing’s extent, and 1e-30 below it;
- the packing translated onto the low walls, and 1e-30 past them;
- the closest pair closed by exactly its gap along its separating axis, and 1e-30 past;
- the square with the least room enlarged about its centre to its exact critical size,
  and 1e-30 past;
- the same for the square with the least room that a neighbour, not a wall, limits;
- the square with the least wall slack moved 1e-30 past its wall;
- a duplicated square;
- the rotation sense reversed;
- the mirror image $x \mapsto S - x$, $t \mapsto -t$.

| Output | What it shows |
| --- | --- |
| `out/check-s182-1024.{txt,json}` | Valid by both methods (SAT 3.3 s, AREA 3.4 s). $S$ = 13970916436214678735385725854133/10^30; 12-place upward print 13.970916436215. 68 tilted squares. Least low-wall slack exactly 1/(2·10^20) (square 0); least high-wall slack 5.00000000063645e-21 (square 15); least pair gap 9.999999999999992e-21 (squares 99, 100). 390 pairs and 45 square–wall incidences within 1e-15. Reversed rotation sense: 80 overlapping pairs. |
| `out/controls-s182-1024.{txt,json}` | All fourteen as expected under both methods (105.8 CPU s). A wall mutation is refused at walls only: 22 squares for the box 1e-30 below its extent, 16 for the translation 1e-30 past the low walls, one square for each single-square control. A pair mutation is refused at the targeted pair only, and the reversed rotation sense at 80 pairs. The closest pair 1e-30 past contact has SAT gap −1e-30 and intersection area 9.5e-31. The pair-limited enlargement (square 138, limited by square 85, room 1.73e-20) 1e-30 past its size has area 5.3e-61. |
| `out/check-s182-1024_regularized.{txt,json}` | The source’s regularized certificate, also valid by both methods at the same side; 478 pairs and 51 square–wall incidences within 1e-15. |

### `programs/sides.py` (Decides Nothing)

This program prints, in exact arithmetic, the certificate’s side and its upward prints,
and the gap to each side around it: the case record’s exact house side (T-174, read from
`frontier/n-182.md`), T-098’s exact side, T-056’s printed side, the source’s KKT side
$S^*$ and the two leaderboard values the issue quotes. In `out/sides.{txt,json}`:

- the house lies 3.174277e-3 above the certificate’s side;
- Subramanya N’s side-only 13.9709164362306 lies 1.592126e-11 above it, and Prathamesh
  Chavan’s 13.9727613470647 lies 1.844911e-3 above it;
- $S^*$ lies 1.397092e-19 below it;
- the commit title’s 13.97091643621468 is the 14-place upward print.

### `programs/kkt_consistency.py` (Decides Nothing)

This program checks the source’s 80-digit point (`s182-1024.exact.txt`) at 100 digits
(mpmath), only as far as it bears on the record. In `out/kkt-consistency.{txt,json}`:

- **The certificate is that point.** Its centres are dilated about the origin by
  1 + 1e-20 and its half-angle tangents rounded: centres agree within 4.97e-36, angles
  within 4.85e-34 degrees.
- **The sides.** The certificate’s side is $S^*(1 + 10^{-20})$ rounded up by 6.36e-31,
  and lies 1.397e-19 above $S^*$.
- **The point as a packing.** It is a packing at $S^*$ to its precision (least gap
  −3.5e-69), with 45 walls and 390 pairs active below 1e-60, as in the certificate. The
  least inactive gaps are 3.45e-6 at a wall and 1.13e-5 for a pair.
- **The free squares.** The six squares 121, 135, 142, 155, 163 and 180 (0-based, in the
  certificate’s order) touch nothing and keep the binary64 input’s values.

It does not check stationarity, multipliers, the second-order test or the flat motions.

### `programs/identity_lineage.py` (Decides Nothing)

This program runs in binary64 with scipy’s `linear_sum_assignment`.
It performs two measurements.

The first is identity. It compares the certificate with each packing at 182 under the
box’s eight symmetries, corner-anchored and box-centred.

The second is the L-cut lineage. It assigns the 182 squares optimally to 182 of a 211
packing’s squares. Every symmetry of the 211 box is tried, with the packing anchored at
each corner of the 182 box, and the placement is chosen by least summed distance.
It also lists the squares by which T-188 differs from T-175, T-181 and T-182, and
whether the certificate follows T-188 or the other packing at each.
In `out/identity-lineage.{txt,json}`:

- **Against the binary64 input.** Identity symmetry; 49 squares move beyond 1e-9, none
  beyond 2.55e-7.
- **Against T-174, the house witness, T-098 and T-056.** Identity symmetry; 44 squares
  beyond 0.1, 166 beyond 1e-3 corner-anchored; largest move 0.8127 (0.8144
  box-centred). Nearest centres do not pair the squares one to one.
- **Against the source’s regularized certificate.** Identity symmetry; 49 squares move
  beyond 1e-9, 5 beyond 0.1, the largest by 0.381.
- **The L-cut.** T-188’s packing fits in its own frame, symmetry 0, anchored at the
  lower-left corner, with summed distance 8.43 against 22.88 for the next placement. The
  29 squares left out are exactly the 29 within 1.5 of its right and top walls. Of the
  182: 17 move beyond 0.1 (largest 0.464), 156 beyond 1e-2, 173 beyond 1e-3; 59 of the 68
  tilted squares lie within 0.1. At the squares that tell T-188 from T-175, the
  certificate follows T-188 at squares 9 and 141 (0.024 and 0.015, against 0.175 and
  0.442).

`run_review.sh` keeps only the final version’s output.
Earlier versions of this program placed the 211 packing at the cut corner and the far
corner only and chose by squares within 1e-3. That choice matched axis-aligned blocks at
grid positions, which a unit grid matches under any whole shift, and missed the
placement above. The review records why the selection rule changed.

## Registration

`record-changes.md` drafts the `verifiers.yaml` record of `exact_check.py`, the one
program that decides, and the evidence entry that cites it.
`identity_lineage.py`, `kkt_consistency.py`, `sides.py` and `custody.sh` decide nothing
about the bound. They are kept here unregistered, and no evidence entry cites them.
