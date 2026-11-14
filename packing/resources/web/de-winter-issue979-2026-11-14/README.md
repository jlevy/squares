# Joost de Winter’s s(332) and s(409) Certificates at c70defa

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/c70defaf39af47db220d1e7c2922590637ffb664)
at `c70defaf39af47db220d1e7c2922590637ffb664` (committed 2026-11-14T10:39:38Z), the head
of `main` when it was read at 10:59Z, which
[issue #979](https://github.com/jlevy/squares/issues/979) names. The issue was opened at
10:41:23Z, 1 minute 45 seconds after the commit, which first published the folder
`above324_from_n297/`. GitHub’s activity log was not readable from this session, so the
push time is not read; no other report reached 332 or 409 between the commit and the
issue, so the ledger dates both claims by the issue, with the first commit kept.

Both counts lie beyond the case corpus of n ≤ 324. Beyond it the record keeps dated rows
in [source-coverage.yaml](../../../frontier/source-coverage.yaml), with no ceiling, each
recorded as its source reported it (the owner, 23 October 2026, D1), and no register
entry. Intake lane L154 (think-g2ax) retained this packet, replayed both certificates and
recorded both as rows on 14 November 2026, with
[issue #977](https://github.com/jlevy/squares/issues/977)’s packing of 297 squares, which
both are built from and the
[s297 packet](../de-winter-s297-upper-bound-2026-11-14/README.md) retains.

## What the Source Claims

- `above324_from_n297/n332_exact.json` and `n409_exact.json` state 332 and 409 unit
  squares as `[center_x, center_y, cos, sin]` rows of exact rationals with the side. The
  issue and the folder’s README round the sides up at 12 places, 18.739455558289 and
  20.739455558289, against the record’s 18.740417287544 and 20.740417290708 at `7629f5a`,
  an improvement of 0.00096 each.
- **The construction.** Both are the source’s packing of 297 squares plus axis-aligned
  squares, as `build.py` writes them from `n297/n297_exact.json`. At 332, the side is the
  297 side plus 1: the 297 packing moved by (1, 1), 18 squares along the bottom wall and
  17 along the left. At 409, the side plus 3: the 297 packing moved by (3, 3), two arms of
  3 × 17 squares against the far walls, and 10 squares in the corner, five of them in a
  square of side 2.72 (68/25), four at its corners and one at its centre turned by the
  rotation whose half-angle tangent is 408/985, 44.99996 degrees.
- **Lineage.** The README says the recorded values at 332 and 409 are built the same way
  from T-174 at 297, and that the credit stated for the 297 applies: the layout is T-174’s
  (Francisco Couzo’s packing, Evan Daniel’s exact optimum, PingYou Ltd’s refinement). The
  issue asks that both be credited to Joost de Winter as packings that build on T-174.
- **The checkers.** `verify_exact.py` and `check_area.py`, byte for byte the `n297/`
  copies, report 332 squares with 729 close pairs and 409 with 875; they share one author,
  `Fraction` and the input files. Neither ran here, nor did `build.py`.
- The README says the construction and the checks were produced with Claude Fable 5.2
  (Anthropic) under Joost de Winter’s direction.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the licence, the root README and the whole of
`above324_from_n297/`, 9 files: 6 retained under [source/](source/) and 3 pinned by
digest: `LICENSE`, against the
[227, 229 and 260 packet](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md)’s
copy; `verify_exact.py`, against the
[s132 packet](../de-winter-s132-upper-bound-2026-11-11/README.md)’s copy; and
`check_area.py`, against the s297 packet’s copy. `above324_from_n297/SHA256SUMS` states the
digests of the six other files of the folder, and they match. Both certificates are stored
compressed (below).

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `da5091505`, and
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) the
record the source register reads the rows from:

- **332:** exactly the s297 certificate’s side plus 1, 9.6173 × 10⁻⁴ below the row of
  `couzo-02f9690-2026-10-09`, Francisco Couzo’s certificate of 9 October 2026, 18.740417287544,
  and 0.231 below Göbel’s construction there, the corner-touching strip 2 + 12√2.
- **409:** exactly the s297 side plus 3, 9.6173 × 10⁻⁴ below the row of
  `tymchishin-reclosure-v3-2026-10-23`, Kirill Tymchishin’s Kaggle notebook packing,
  20.740417290708, and 0.160 below Göbel’s construction there, the Göbel square
  11 + 7√2 of 416 less 7 of its squares.

Neither row is above the classical construction, so each holds its count. The
[ledger of 14 November](../../../campaign/issue-intake/upper-bounds-977-979-20261114/README.md)
records both as new packings, each superseding the row it is below.

## Exact Replay

The checks below were planned before any of them ran (the s297 packet’s
[Exact Replay](../de-winter-s297-upper-bound-2026-11-14/README.md#exact-replay)).

`devtools.upper_bound_reports certify` decided both certificates and their
duplicate-square and outside-container controls on both maintained routes: 6 jobs, every
wall and pair, 54,946 pairs a job and route at 332 and 83,436 at 409, 830,292 pair
decisions and 468.4 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). Both positives passed and every control was refused on both
routes. Squares touch the walls exactly, and the added axis-aligned squares touch each
other, a least pair gap of exactly 0, as the borders of #941 do. `check --replay` decided
the six jobs again.

`sharp-controls` took each certificate to exact contact and 10⁻³⁰ past it on both
routes, 11 controls a count and 1,753 route CPU seconds
([receipts/sharp-controls-n332.json](receipts/sharp-controls-n332.json),
[receipts/sharp-controls-n409.json](receipts/sharp-controls-n409.json)), every control as
the module predicts:

- **Wall, pair and near-wall.** Squares touch every wall and the border squares touch
  each other, so the box lowered to the extent, the tightest pair (square 299 against 298,
  two border squares) closed and every square moved to its near wall are each the
  certificate itself, by 0: accepted at contact and refused 10⁻³⁰ past it.
- **Enlarged to a pair and to a wall.** Square 299, against 298, and square 1, at its
  wall, are enlarged by 0, accepted at contact, and refused 10⁻³⁰ past for their shape,
  the overlap and the wall.
- **Duplicate.** A duplicated square is refused.

The plan stated each of these in advance, though for the pair enlarged past contact it
named the shape and the overlap and not the wall that square 299 also touches.

The two routes share this repository’s centre-direction reader, `Fraction` arithmetic and
the separating-axis method; neither shares code with the source’s checkers.

## Pose by Pose and Padding

`devtools.measure_identity` and `devtools.contraction_margin` wrote the receipts under
[measure/](measure/), each against the certificate of the row it supersedes:

- **332.** No symmetry pairs it square for square with Couzo’s 332 by nearest centres; the
  optimal assignment moves 94 squares beyond a tenth (largest 0.740). Couzo’s certificate
  is his own earlier packing of 297 with the same border, 107 squares tilted by 43.04 to
  45.00 degrees, before Evan Daniel and PingYou Ltd improved it. Its contraction margin is
  1.874 × 10⁻¹⁹, and the gain is 5.1 × 10¹⁵ times it.
- **409.** No symmetry pairs it with Tymchishin’s 409; the optimal assignment moves 262
  squares beyond a tenth (largest 1.092). Its contraction margin is 1.546 × 10⁻⁹, and the
  gain is 6.2 × 10⁵ times it.

So neither gain is a re-certification of a row’s padding, and neither is RV-3 material.

## Stage 4 Review

The stage 4 review of 14 November 2026
([review-2026-11-14-de-winter-977-979.md](../../../../docs/project/reviews/review-2026-11-14-de-winter-977-979.md),
lane L153), written in a separate lane blind to this one throughout, accepts both
certificates, nothing blocking or major; the
[s297 packet](../de-winter-s297-upper-bound-2026-11-14/README.md#stage-4-review) gives its
method and its questions for the author.

- **Feasibility.** Its clean-room checker decides both files, every square, wall and all
  54,946 and 83,436 pairs, by two exact methods: 35 and 302 pairs touch, all among the
  added squares, none overlaps, and the least positive pair margin is the 297’s, at
  squares 232 and 237. Its 18 controls a count, stated beforehand, came out as stated,
  among them the squares accepted in the box of each claim’s own side.
- **The constructions (F12).** Squares 1 to 297 are the 297 certificate translated by
  (1, 1) and (3, 3) exactly, the sides exactly the 297 side plus 1 and plus 3, and the
  added squares as the README describes.
- **The corner square (F13)** is at 44.999964 degrees, edge direction
  (803761, 803760)/1136689, not 45.
- **The 409 row (F14)** lies 3.164 × 10⁻⁹ above T-174 + 3 and its squares are placed
  otherwise (262 beyond a tenth under the best assignment), so the README’s “built in the
  same way from the record T-174” holds for 332’s side only; the 409 gain is
  9.6173242 × 10⁻⁴, 3.16 × 10⁻⁹ more than the 297 gain.
- **Padding (F10).** The rows’ margins are 1.874 × 10⁻¹⁹ and 1.546 × 10⁻⁹, as measured
  here; RV-3 does not apply.
- **Significance.** S3 carried from the 297 by the register’s rule for derived bounds,
  S2 on their own content; rows beyond the horizon are no register entries, so the score
  bears on the import’s label only.

Both rows are verified from the replay, E-de-winter-979-exact-feasibility, and the
review’s clean-room run, E-de-winter-979-review-exact-feasibility.

## What Is Not Established

- **Optimality** of any kind at either count.
- **Consequences at other counts.** Two L steps from the 297 give 369 a side of 19.7395,
  above Göbel’s construction there, 19 + √2/2 = 19.7071, so no bound. Deleting squares
  bounds counts below each certificate; no report claims them, so they have no rows
  (think-kzme).
- **Human oversight**: no record is retained.

## Credit and Licence

Both packings are Joost de Winter’s: his packing of 297 (#977), in the layout of T-174
(Francisco Couzo’s packing, as Evan Daniel and PingYou Ltd improved it), with borders that
follow the construction of the rows they supersede. The source says the construction and
the checks were produced with Claude Fable 5.2 (Anthropic) under his direction. The
bibliography key is **[de Winter issue 979 2026-11-14]**.

Everything here is published under the MIT licence, copyright (c) 2026 Joost de Winter, by
`LICENSE` at the pin, which the root README says covers all files.

## Commands

From `packing/`, with the project interpreter:

```bash
P=de-winter-issue979-2026-11-14
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 332 "DE-WINTER=packet:$P" \
  'couzo-02f9690=evand-cert:resources/web/couzo-exact-certificates-2026-10-09/source/certificates/n332.cert' \
  --out resources/web/$P/measure/identity-n332.json
python -m devtools.measure_identity --n 409 "DE-WINTER=packet:$P" \
  'tymchishin-reclosure-v3=evand-cert:resources/web/couzo-issue763-2026-10-23/source/certificates/best/n409.cert' \
  --out resources/web/$P/measure/identity-n409.json
python -m devtools.contraction_margin --n 332 \
  'couzo-02f9690=evand-cert:resources/web/couzo-exact-certificates-2026-10-09/source/certificates/n332.cert' \
  --against "DE-WINTER=packet:$P" --no-routes --out resources/web/$P/measure/contraction-n332.json
python -m devtools.contraction_margin --n 409 \
  'tymchishin-reclosure-v3=evand-cert:resources/web/couzo-issue763-2026-10-23/source/certificates/best/n409.cert' \
  --against "DE-WINTER=packet:$P" --no-routes --out resources/web/$P/measure/contraction-n409.json
```

## Compressed Files

| Stored file | Origin | Git blob of stored file | SHA-256 of decompressed source |
| --- | --- | --- | --- |
| `source/above324_from_n297/n332_exact.json.gz` | upstream | `5e9e34725840cf831b21641bbdb4ccc0bb0d678a` | `d6fb8424688c6272acd452c7a0e46104e69f1bcd20def89741e1ac55062d0873` |
| `source/above324_from_n297/n409_exact.json.gz` | upstream | `e2b188f961d7ee31489304aa18ca06658f9cd6fb` | `513a40e3cbb182f344ed0194e4fe8974d7f518a27d1ad7bff4d2f267eac4a443` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
