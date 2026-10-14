# The Mathematical Review’s Programs, 14 October 2026

These are the programs the
[mathematical review](../../../../../docs/project/reviews/review-2026-10-14-fang-excess-theorem-and-direct-certificates.md)
of Kevin Fang’s Theorems 1 and 2 wrote and ran on 14 October 2026, kept as they ran,
with the output each printed in [`outputs/`](outputs/). The review was the stage 4
mathematical lane of the `think-0esw` import, by an AI agent, Fable, strong tier, max
reasoning, in a worktree and a session of its own.
It ran each program with the project interpreter (Python 3.14, `python3 -I -B`), reading
the retained packets as data: this packet’s `source/`, the pieces that the
[Daniel packet](../../evand-square-packing-2026-10-05/README.md), the
[two-wedge packet](../../fang-two-wedge-certificates-2026-10-10/README.md) and the
[direct-certificates packet](../../fang-direct-certificates-2026-10-13/README.md)
retain, and the two packets’ receipts and claims records.
No program imports or executes anything of the source’s or of this repository’s. The
whole set of runs took about three and a half CPU-minutes.

## What Its Authors Read

The lane read the source’s `README.md`, `tools/glue.py`, the `theorem/` tables and
notes, the rectangles’ `NOTES.md` and checker outputs, `CHANGELOG.md`, `ATTRIBUTION.md`,
`VERIFICATION.md` and `third_party/SOURCES.md`, and the archived paper of Arslanov,
Mustafin and Shangitbayev, before writing any program.
It did not read the source’s checkers, `verify.py`, `tools/rectcheck.py` or Evan
Daniel’s `verify_cert.py`, so the checker here is clean-room with respect to the code
that decided the certificates at the source: it was written from the README’s statement
of the certificate convention (lines 94–102) and the separating-axis theorem.
`tools/glue.py` is the producer’s construction, not a checker; the rebuild shares no
line with it but implements the layout its docstring and the README describe, so it is
independent after reading the producer’s code and not clean-room.
The source states that its search, verifier and bundle were written with Claude
(Anthropic); the programs here were written by a Claude agent too, prompted separately
and in files of its own.

## The Programs

| Program | What it does | Reads | Output |
| --- | --- | --- | --- |
| [`squares_exact.py`](programs/squares_exact.py) | The module the others import: parses a certificate (`n S` or `n W H`, then `x y t`), builds each square’s edge vectors and corners from `t = tan(θ/2)`, decides open-box containment and strict pairwise separation by the separating-axis test, all in `Fraction` arithmetic; pairs with centres farther than √2 apart are decided by the exact test `dx² + dy² > 2` and the rest by the axis test, within a grid of cells of side 2, or every pair by the axis test with `all_pairs`; the two mutation controls | (a module) | — |
| [`rectangle_check.py`](programs/rectangle_check.py) | Decides certificates, square or rectangular, in both dimensions: count, exact width and height, integer box, waste, exact squeeze, least wall clearance, least pair gap and the verdict; `--all-pairs` and `--control duplicate` or `outside` | the certificate files named | [`rectangles.out`](outputs/rectangles.out), [`rectangles_all_pairs.out`](outputs/rectangles_all_pairs.out), [`controls_duplicate.out`](outputs/controls_duplicate.out), [`controls_outside.out`](outputs/controls_outside.out), [`pieces.out`](outputs/pieces.out), [`inventory_retained.out`](outputs/inventory_retained.out), [`inventory_rebuilt.out`](outputs/inventory_rebuilt.out), [`all_pairs_932_380.out`](outputs/all_pairs_932_380.out) |
| [`glue_rebuild.py`](programs/glue_rebuild.py) | Rebuilds every one of the 76 inventory certificates from the retained pieces by its chain: Lemma 3’s layout at the common squeeze 1/10000, closed, then one scaling by 1 + d₀/(2(n − d₀)); writes the text with the comment line the retained files carry and compares its SHA-256 with the frozen header list, the table’s `sha256` column and, for the six retained files, the bytes | `theorem/inventory.tsv`, `theorem/best.tsv`, the six rectangles, Daniel’s eight pieces, `n0308`, `n0343`, `n0344`, the fourteen direct packings, `acquisition/inventory-headers.json` | [`glue_rebuild.out`](outputs/glue_rebuild.out) |
| [`excess_arithmetic.py`](programs/excess_arithmetic.py) | F(n) and its maximiser from the definition for n = 15..2000, the base r in 15..30, Theorem 1’s step of 16; every row of the two tables held to (F, p, q, r), count, side and a recount of its chain from the pieces’ counts and boxes; the deficiency table for k = 15..72 and the crossover with Ryu’s bound | `theorem/inventory.tsv`, `theorem/best.tsv`, `theorem/PIECES.md` | [`excess_arithmetic.out`](outputs/excess_arithmetic.out) |
| [`receipt_summary.py`](programs/receipt_summary.py) | Reads a packet’s exact replay receipt and claims record: the jobs and their sums, each positive’s deciding input against the retained certificate, both routes’ verdicts and least margins, each control’s refusal; each claim’s round-ups, grid gap and every comparison with another report, recomputed | `acquisition/report.json`, `acquisition/claims.json`, `receipts/exact-certification.json.xz`, the retained certificates, of this packet and of the direct-certificates packet | [`receipt_theorem.out`](outputs/receipt_theorem.out), [`receipt_direct.out`](outputs/receipt_direct.out) |
| [`pieces_digests.py`](programs/pieces_digests.py) | Which file each digest of `theorem/PIECES.md` identifies: the retained file, its bytes without comment lines, or neither | `theorem/PIECES.md` and the 31 piece files | [`pieces_digests.out`](outputs/pieces_digests.out) |

## What They Decide

Nothing here is registered yet; the review proposes the `verifiers.yaml` entries and the
records lane registers them with the evidence entries it writes.

| Program | Role | Decided in this run | Coverage |
| --- | --- | --- | --- |
| `rectangle_check.py` with `squares_exact.py` | decides | The six rectangles are strict-valid in both dimensions, with the squeezes the README and the NOTES state; the 25 square pieces the inventory uses are strict-valid; the six retained inventory certificates and the 70 rebuilt ones, byte-identical to the pinned files, are strict-valid at side n − 1/20000; the direct certificates at 380, 381 and 382 are strict-valid at their exact sides, with the margins the record’s receipt holds | full: 6 of 6 rectangles, 76 of 76 inventory certificates, 25 of 25 pieces, 3 of 14 direct certificates; the all-pairs control on R, R′, 932 and 380 agrees with the bucketed route exactly; the duplicate and outside controls are refused |
| `glue_rebuild.py` | decides | Each of the 76 inventory certificates is the Lemma 3 composite of the retained pieces its chain names, at the common squeeze 1/10000 and one final scaling, to the byte: 76 of 76 digests equal the frozen list’s and the tables’ | full |
| `excess_arithmetic.py` | decides | F(n), the maximiser’s base, the tables’ rows, the chains’ counts and the deficiency comparison | full, n = 15..2000 for the arithmetic and the 76 rows |
| `receipt_summary.py` | premises | The two receipts’ inputs are the retained certificates, every job passed or was refused as required, the summed statistics the packet READMEs print, and every claim comparison | full: 18 and 9 jobs, 6 and 14 claims |
| `pieces_digests.py` | premises | The `PIECES.md` digests identify Daniel’s eight files and none of the author’s own 22 as shipped | full |

## Commands

From `packing/`:

```sh
P=resources/web/fang-excess-theorem-2026-10-13/review/programs
SRC=resources/web/fang-excess-theorem-2026-10-13/source
EV=resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch/certs
TW=resources/web/fang-two-wedge-certificates-2026-10-10/source
DC=resources/web/fang-direct-certificates-2026-10-13/source
.venv/bin/python3 -I -B $P/excess_arithmetic.py $SRC/theorem
.venv/bin/python3 -I -B $P/glue_rebuild.py --source $SRC --daniel $EV --two-wedge $TW \
  --direct $DC --headers resources/web/fang-excess-theorem-2026-10-13/acquisition/inventory-headers.json \
  --out SCRATCH/rebuilt
.venv/bin/python3 -I -B $P/rectangle_check.py $SRC/rectangles/*/*.cert
.venv/bin/python3 -I -B $P/rectangle_check.py --all-pairs \
  $SRC/rectangles/r17x16_n0257/r17x16_n0257.cert $SRC/rectangles/r22x21_n0443/r22x21_n0443.cert
.venv/bin/python3 -I -B $P/rectangle_check.py --control duplicate \
  $SRC/rectangles/r17x16_n0257/r17x16_n0257.cert $SRC/rectangles/r22x21_n0443/r22x21_n0443.cert
.venv/bin/python3 -I -B $P/rectangle_check.py --control outside \
  $SRC/rectangles/r17x16_n0257/r17x16_n0257.cert $SRC/rectangles/r22x21_n0443/r22x21_n0443.cert
.venv/bin/python3 -I -B $P/rectangle_check.py $EV/n-110.cert $EV/n-132.cert $EV/n-156.cert \
  $EV/n-182.cert $EV/n-210.cert $EV/n-211.cert $EV/n-241.cert $EV/n-273.cert \
  $TW/n0308/n0308.cert $TW/n0343/n0343.cert $TW/n0344/n0344.cert $DC/n0*/n0*.cert
.venv/bin/python3 -I -B $P/rectangle_check.py $SRC/theorem/n015_F1.cert $SRC/theorem/n016_F1.cert \
  $SRC/theorem/n017_F1.cert $SRC/theorem/n018_F1.cert $SRC/theorem/best/n018_j2.cert $SRC/theorem/n031_F2.cert
.venv/bin/python3 -I -B $P/rectangle_check.py SCRATCH/rebuilt/theorem/*.cert SCRATCH/rebuilt/theorem/best/*.cert
.venv/bin/python3 -I -B $P/rectangle_check.py --all-pairs SCRATCH/rebuilt/theorem/n031_F2.cert $DC/n0380/n0380.cert
.venv/bin/python3 -I -B $P/receipt_summary.py resources/web/fang-excess-theorem-2026-10-13
.venv/bin/python3 -I -B $P/receipt_summary.py resources/web/fang-direct-certificates-2026-10-13
.venv/bin/python3 -I -B $P/pieces_digests.py $SRC/theorem/PIECES.md R=$SRC/rectangles/r17x16_n0257/r17x16_n0257.cert ...
```

The rebuilt certificates are 16 MB and are not kept (`OR-18`); the pinned files they
equal are identified by the digests in `acquisition/inventory-headers.json`, and
`glue_rebuild.py` writes them again in two seconds.
`pieces.out` names the direct packings in the order the command above lists them, and
`pieces_digests.py` was run with one `NAME=PATH` pair for each of the 31 rows of the
table, the paths being those `glue_rebuild.py` maps each name to.
The bucketed route decided all 76 inventory certificates in 60 CPU seconds; the
all-pairs control at 932 took 42 seconds.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
