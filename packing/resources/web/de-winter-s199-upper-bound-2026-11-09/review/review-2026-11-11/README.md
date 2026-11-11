# Stage 4 Review of #939 and #946: Programs and Receipts

The programs and receipts of
[review-2026-11-11-de-winter-939-946.md](../../../../../../docs/project/reviews/review-2026-11-11-de-winter-939-946.md)
(lane L82, bead `think-o53d`). This directory holds every program and the receipts for
#939 at 199 and for both issues together.
The receipts for #946 alone are in
[the 172 packet’s review directory](../../../de-winter-s172-upper-bound-2026-11-10/review/review-2026-11-11/README.md).

The programs import nothing from this repository or the source.
They read the source files as data, cloned from the author’s repository
`JoostdeWinter/square-packing` at `702c7af2` (`n199/`) and `c4e65d0b` (`n172/`); this
review did not compare them with the packets’ `source/` copies.

## Frozen Before Use

| Receipt | What it fixes | When |
| --- | --- | --- |
| `checker-freeze.json` | SHA-256 of `l82_check.py` and `l82_selftest.py` | 2026-11-11T06:22:08Z |
| `controls-plan.json`, `controls-freeze.json` | the 21 controls and their stated outcomes | 06:22:38Z |
| `findings-freeze.json` | the review’s text before the import lane was read | 06:38:01Z |

## Programs and Receipts

| Program | Receipt |
| --- | --- |
| `l82_check.py` | the checker module: separating axes in `Fraction`, clipped areas in `gmpy2.mpq` |
| `l82_selftest.py` (and with a mutant name as its argument) | `selftest.txt` |
| `l82_decide.py` | `decide-939.json` (with controls), `decide-t282.json`, `decide-t284.json`; `decide-946.json` in the 172 packet |
| `l82_algebra.py` | `algebra.json` |
| `l82_measure.py` | `measure.json` |
| `l82_moves.py`, `l82_supplement.py`, `l82_print300.py` | in the 172 packet |
| `l82_freeze.py` | the three freeze receipts |
| `l82_compare_lane.py`, after the freeze | `compare-lane.json` |

## Commands

From `packing/`, with the source files unpacked to `SRC` and the import lane’s
contraction receipts in `L78` (names as `l82_compare_lane.py` reads them):

```sh
PY=".venv/bin/python3 -I"; D=resources/web/de-winter-s199-upper-bound-2026-11-09/review/review-2026-11-11
$PY $D/l82_selftest.py
$PY $D/l82_decide.py 939 $SRC/n199/n199_exact.json $SRC/n199/n199_witness.yaml decide-939.json --controls
$PY $D/l82_decide.py 946 $SRC/n172/n172_exact.json $SRC/n172/n172_witness.yaml decide-946.json --controls
$PY $D/l82_decide.py t282 - witnesses/known-best/n-172.yaml decide-t282.json
$PY $D/l82_decide.py t284 - witnesses/known-best/n-199.yaml decide-t284.json
$PY $D/l82_algebra.py $SRC/n199/n199_exact.json $SRC/n172/n172_exact.json algebra.json
$PY $D/l82_measure.py witnesses/known-best/n-172.yaml witnesses/known-best/n-199.yaml \
  $SRC/n172/n172_exact.json $SRC/n199/n199_exact.json \
  cases/regularized_drawings/think-he66-2026-11-09/adopt-2026-11-09-n172-270-evand/n-172/report.json.gz \
  algebra.json measure.json
$PY $D/l82_moves.py witnesses/known-best/n-172.yaml $SRC/n172/n172_exact.json algebra.json measure.json moves.json
$PY $D/l82_supplement.py $SRC/n172/n172_exact.json witnesses/known-best/n-172.yaml moves.json supplement.json
$PY $D/l82_print300.py algebra.json $SRC/n172/n172_optimum_300_digits.txt print300.json
$PY $D/l82_compare_lane.py $L78 $SRC/n172/n172_exact.json witnesses/known-best/n-172.yaml measure.json moves.json compare-lane.json
```

The receipts were written with CPython 3.14.7, gmpy2 2.3.1 and sympy 1.14.0, under
`nice -n 19`, at most two processes, about 20 CPU-minutes in all.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
