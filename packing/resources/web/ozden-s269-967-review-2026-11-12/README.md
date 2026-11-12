# Stage 4 Review of #967: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane L127’s blind stage 4 review of
issue [#967](https://github.com/jlevy/squares/issues/967), Doğa Özden’s
$s(269) \le 16.889730073596$:
[`docs/project/reviews/review-2026-11-12-ozden-967.md`](../../../../docs/project/reviews/review-2026-11-12-ozden-967.md).

The source is `n-269-candidate.yaml` of
[kenaznia-doga/s269-upper-bound-1688973007@f496016](https://github.com/kenaznia-doga/s269-upper-bound-1688973007/tree/f496016d3ebccb00c00cbf146efe85e0cc952dda),
SHA-256 `35b1307a3a0dc2eb806ef064933c809a2f2b7eda73551bcc4ba6c411a307b5e6`. It is not
retained here; an import lane would retain it in its own packet. This directory is
review-only.

## Layout

- `programs/`: the review’s programs, the controls plan, the issue as fetched.
- `frozen/`: the checker’s digests at its freeze, the plan’s digest when it was stated,
  the findings’ digest at their freeze, and the frozen review text.
- `out/`: the receipts.

## Programs

Every program is lane L127’s own, written for this review as a clean-room
implementation: it imports nothing from this repository or the source, and reuses no
code of any earlier review. The review of #962 (lane L117) was the model; its text,
README and frozen digest lists were read, and its programs were not opened. Each was run
with CPython 3.14.7 as `python -I -B` from `packing/` of a checkout of `main` at
`0352d7554`, through `uv run --frozen --all-extras --group dev`, under `nice -n 19`.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `l127_reader.py` | the reading: layout, count, ids, canonical scalars, the JSON twin | the certificate and its twin | nothing (a module) |
| `l127_sat.py` | method A: unit squares, wall clearances and pair margins by separating axes in Python integers over per-square denominators | integers from the reader | nothing (a module) |
| `l127_clip.py` | method B: unit squares (sides and diagonals), pairs and walls by exact convex clipping, containment by area, in `gmpy2.mpq` | integers from the reader | nothing (a module) |
| `l127_check.py` | the certificate, by both methods, every square, wall and pair | the certificate and its twin | `out/check-n269.json` |
| `l127_geom.py` | nothing: builds squares, the closed-form margin from centres and half-widths, and closing times, for the self-test and the controls | fractions | nothing (a module) |
| `l127_selftest.py` | both methods and the reader against 26,381 cases, and two broken copies | nothing | `out/selftest.json` |
| `l127_plan_facts.py` | nothing: the exact facts the controls plan states its outcomes from | the certificate, the check receipt, the issue | `out/plan-facts-n269.json` |
| `l127_make_plan.py` | nothing: states the 20 controls and their outcomes | the check receipt, the plan facts | `programs/controls-plan.json` |
| `l127_controls.py` | the 20 controls, by both methods or the reader | the certificate, the plan, the plan facts, the check receipt | `out/controls-n269.json` |
| `l127_describe.py` | nothing: the side’s decimals, the margin and clearance distributions, the tilts | the certificate | `out/describe-n269.json` |

`programs/issue-967.json` is the issue and the author’s announcing comment on #947 as
fetched, trimmed to their text and dates.

From `packing/`, with `SRC` the clone at the pin and `R` this directory:

```bash
PY="nice -n 19 uv run --frozen --all-extras --group dev python -I -B"
$PY $R/programs/l127_selftest.py $R/out/selftest.json
$PY $R/programs/l127_check.py $SRC/n-269-candidate.yaml $SRC/n269-witness.json $R/out/check-n269.json
$PY $R/programs/l127_plan_facts.py $SRC/n-269-candidate.yaml $SRC/n269-witness.json \
  $R/out/check-n269.json $R/programs/issue-967.json $R/out/plan-facts-n269.json
$PY $R/programs/l127_make_plan.py $R/out/check-n269.json $R/out/plan-facts-n269.json \
  $R/programs/controls-plan.json
$PY $R/programs/l127_controls.py $SRC/n-269-candidate.yaml $SRC/n269-witness.json \
  $R/programs/controls-plan.json $R/out/plan-facts-n269.json $R/out/check-n269.json \
  $R/out/controls-n269.json
$PY $R/programs/l127_describe.py $SRC/n-269-candidate.yaml $SRC/n269-witness.json \
  $R/out/describe-n269.json
```

## What They Printed

- `l127_selftest.py`: `PASSED 26381 cases 0 failed`; broken method A fails 1,312,
  broken method B 1,952.
- `l127_check.py`: `ACCEPT`, 36,046 pairs apart by both methods, three wall contacts
  (square 48 left, 102 bottom, 199 top), least gap $2.03645031468039 \times 10^{-13}$
  at (38, 40).
- `l127_controls.py`: `EVERY_CONTROL_AS_STATED`, 20 of 20.

## Frozen Files

| File | What it fixes | When |
| --- | --- | --- |
| `frozen/checker-frozen-digests.txt` | the six checker files and the receipts they had written | 2026-11-12T04:06:28Z |
| `frozen/controls-plan-digest.txt` | the controls plan, its facts and their programs, before `l127_controls.py` existed | 2026-11-12T04:09:52Z |
| `frozen/findings-frozen-digest.txt` | the frozen review text and the receipts at the freeze | see the file |
| `frozen/review-2026-11-12-ozden-967.frozen.md` | the review as frozen, before the author’s checkers, outputs or README, or this repository’s verifier, were read | see the digest list |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
