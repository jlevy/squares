# Review Programs for `T-184` and `T-191`

These are the programs written for the stage 4 review
[review-2026-10-16-greff-k2m5-mixed-covers-76-95.md](../../../../../docs/project/reviews/review-2026-10-16-greff-k2m5-mixed-covers-76-95.md)
of Benjamin Greff’s mixed covers for $s(76) = 9$ (`T-184`) and $s(95) = 10$ (`T-191`),
with everything they printed.
They are kept in this packet for both results. The
[$s(95)$ packet’s `review/`](../../bengreff-s95-certificate-2026-10-15/review/README.md)
points here.
The reviewer is Claude, strong sub-agent tier, max reasoning. The programs were written
for the review by the reviewer and decide nothing on their own: every number is exact
(Python integers and `fractions.Fraction`), floats only choose where to look, and no
output is a certificate.

## What Each Program Does

| Program | Reads | Does |
| --- | --- | --- |
| `programs/k2m5_review.py cover COVER N` | the unpacked cover | its own parser of Daniel’s `mixed 1` format. It checks well-formedness, the exact total and its slack below $N$, $D_4$ invariance as a measure under all eight elements (atoms by position, line densities in canonical form) and as raw multisets under the two generators, the point and segment census (lines, lengths, overlaps, points on lines), the wall segments and the total without them, the input bounds of `zmx2`’s parser, and the SHA-256 and FNV-1a 64 of the bytes (the hash `zmx2` writes into its log header) |
| `programs/k2m5_review.py records PACKET N` | the packet: the source’s `records/zmx2/` and `records/zm_mixed/`, and the retention’s `receipts/` (replay and wall control) | the composite over the $D_4$ region, cell by cell. For each `zmx2` root log it checks the header (cover hash, settings, region), every `ROOT` line, the full root grid, the full-binary-tree identity of each census, the failing set against `failing_roots.txt` and the summary line. For each `zm_mixed.py` record it checks the header (pinned digests, cover digest, total, certificate-mode settings), one record, root equal to region, `UNCERT 0`, census identity, and alignment to the $1/20 \times 1/20 \times 1/32$ grid. Then it checks that the cells are exactly the sub-cells of the failing roots, that `jobs.txt` matches, and that source and replay agree. It also locates the failing roots and the second route’s root $R$ |
| `programs/k2m5_review.py poses COVER N PACKET` | the cover and the source’s `zmx2` log | exact $\mu(Q)$ at sampled admissible poses. The poses are uniform in the region, in every failing root, inside and at the corners of every listed uncertified box, at $u = 1/3$ and near $u = \sqrt{26} - 5$, at tile and one-cut germs, and 1,500 whole-container poses folded into the region by the $D_4$ reflections, with $\mu$ compared before and after. A local descent follows, and the retention’s two control poses are compared with `zm_mixed.py pose`’s exact values |
| `programs/k2m5_review.py mutants COVER N` | the cover | three mutations: the heaviest point orbit removed, the heaviest segment orbit removed, every mass scaled. For each it finds a pose where the mutant captures less than 1, exactly, and names the `zmx2` root that holds it. It samples flush axis-parallel squares with and without the wall segments, and writes the mutated covers (`--write-mutants`) |
| `programs/k2m5_review.py cellmin COVER N --box B` | the cover | the lowest exact $\mu$ found in one pose box (random poses, corners, descent) |
| `programs/k2m5_review.py localmut COVER N --pose P` | the cover | a mutant without the $D_4$ orbit of the heaviest piece the square at pose $P$ captures, so that the hole sits near that pose’s orbit (`--write` writes it) |
| `programs/k2m5_review.py tiling PACKET N CHECK_COVERAGE` | the source’s records and its `tools/check_coverage.py` | eight mutated record sets, each run through the author’s script (`python3 -I`, from the retained copy, after reading it) and through this program’s composite check |
| `programs/corner_scan.py COVER ZMX2_LOG ROOT_ID` | the cover and a `zmx2` log | exact $\mu$ at every corner of the uncertified boxes listed for one root (imports `k2m5_review.py` from its own directory) |
| `programs/run_zmx2_controls.sh` | the covers, the mutants, the `zmx2` binary | `zmx2 cert --d4` on one root per control, published and mutated |
| `programs/run_zm_control.sh` | the 199/200 mutant, the retained `zm_mixed.py` files | `zm_mixed.py cert` with `verify.sh`’s flags on the one cell that holds the mutant’s hole, under a 15-minute limit |
| `programs/run_zm_control_d12.sh` | the published cover and the 199/200 mutant | the same cell at a depth limit of 12, for both covers |
| `programs/run_zm_local.sh` | the published cover | `localmut` at the 199/200 mutant’s pose, then `zm_mixed.py` with `verify.sh`’s flags at depth 24 on the same cell, under a 10-minute limit |
| `programs/run_all_final.sh` | the covers and packets | every `k2m5_review.py` output but `localmut`’s, and `corner_scan.py`’s, in order |

`k2m5_review.py` imports nothing from the source, from Daniel’s checkers or from this
repository; it was written from the format, the statement and the record formats as read
in the source files. Its exact evaluator agrees with `zm_mixed.py pose` fraction for
fraction at every pose where both were run.

## How They Were Run

On 2026-10-16, on a shared four-core x86-64 container, with Python 3.14.7 (`python3 -I`),
one process at a time under `nice -n 10`.
The covers were unpacked from the packets’ `cover/*.txt.gz` into a scratch directory
(`data/`), and the scripts name the scratch paths they ran in.
The exact commands are in `programs/`:

- `run_all_final.sh` writes every `k2m5_review.py` output and `corner_scan.py`’s, from
  the final program. Its digest is in each output’s `program` field. An earlier run of
  the same commands, while the program was still being written, printed the same values.
- `run_zmx2_controls.sh` runs the `zmx2` controls.
- `run_zm_control.sh`, `run_zm_control_d12.sh` and `run_zm_local.sh` run the
  `zm_mixed.py` controls.

`LOWEST_POSE`, in `run_all_final.sh`, is the `descent_min` pose of the `poses` output.
The 199/200 mutant’s pose is the lowest corner `corner_scan.py` finds among the uncertified
boxes of root 8010.

`zmx2` was built from retained bytes by the project’s
`python -m devtools.replay_evand_zmx2 build --checker 6b7f0f79`. That gave binary
`cba78a9eb5a30e7baf7901b2745fc7cf65b027e54bfc945cfddf53b53abf8525`, rustc 1.97.0,
bit-identical to the retention’s.
`zm_mixed.py` ran from a scratch copy of the retained `zm_mixed.py` (`ee3e2915`),
`mixed_cover.py` (`bb89de15`) and `zeromargin.py` (`640fe453`), digests checked, under the
project interpreter. Nothing was fetched.

## What They Printed

Every output is in `outputs/`, as written. In short:

| Output | Result |
| --- | --- |
| `cover-n76.json`, `cover-n95.json` | well formed, totals $3788361049/50000000$ and $3791753447/40000000$, $D_4$-invariant under all eight elements; no point on any line; 16 and 404 wall segments of one unit each; FNV-1a `96e61ce6a0aa2545` and `e6e0d4182d7f6e43`, the hashes in the `zmx2` logs |
| `records-n76.json`, `records-n95.json` | every cell of each region decided by exactly one checker, from the source’s records and from the replay’s own; 8,096 + 64 and 9,981 + 304; source = replay root for root and record for record; the wall control’s census equal root for root |
| `poses-n76.json`, `poses-n95.json` | 9,326 and 17,319 exact evaluations, none below 1; lowest found $1.000417532651$ and $1.003389489532$; 1,500/1,500 folded poses with equal $\mu$ and image in the region |
| `mutants-n76.json`, `mutants-n95.json`, `mutants-n76-scaled-199-200.json` | every mutant below 1 at an exhibited pose, exactly; the published covers above 1 there |
| `zmx2/*.log` | `zmx2` NOT VERIFIED on each mutant at the root holding its pose; REGION CLEAN on the published cover at the same roots |
| `zm_control/n76_scaled-199-200_j054.*` | depth limit 24: stopped at the 15-minute limit (exit 124), no verdict |
| `zm_control/*_j054_depth12.*` | depth limit 12: the published cover’s cell `VERIFIED-D4 (PARTIAL)`, 121 boxes, the census of the source’s record `j054`; the mutant’s `NOT VERIFIED (PARTIAL)`, 879 boxes, 44 uncertified, one of them holding the hole’s pose |
| `cellmin-n76-j054.json` | lowest $\mu$ found by sampling and descent in that cell, $1.005196$; the hole’s pose ($1.004806$) is a corner of a `zmx2` uncertified box, found by `corner_scan.py` |
| `corner_scan-n76-root8010.txt` | the lowest corner of root 8010’s six listed uncertified boxes, $1.004805655988$ |
| `localmut-n76-j054.json` | the local mutant: the orbit of the segment $[73/16, 37/8] \times \{2\}$ removed (8 segments, $0.198$), $\mu = 0.955233$ at the hole’s pose |
| `zm_control/n76_local-j054.*` | that mutant at depth limit 24: stopped at the 10-minute limit (exit 124), no verdict |
| `tiling-n76.json`, `tiling-n95.json` | the author’s script accepts the published records and five of the eight malformed sets; this program accepts only the published ones |

The mutated covers themselves are not kept: `mutants` rewrites them byte for byte, and
their SHA-256 is in its output.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
