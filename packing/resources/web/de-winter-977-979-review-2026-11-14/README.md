# Stage 4 Review of #977 and #979: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane L153’s blind stage 4 review of
issues [#977](https://github.com/jlevy/squares/issues/977) and
[#979](https://github.com/jlevy/squares/issues/979), Joost de Winter’s
$s(297) \le 17.739455558289$, $s(332) \le 18.739455558289$ and
$s(409) \le 20.739455558289$:
[`docs/project/reviews/review-2026-11-14-de-winter-977-979.md`](../../../../docs/project/reviews/review-2026-11-14-de-winter-977-979.md).

The sources are files of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing), not
retained here; an import lane would retain them in its own packet.
This directory is review-only.

| File | Pin | SHA-256 |
| --- | --- | --- |
| `n297/n297_exact.json` | `7b4701f35e815301e4f467d214fab4205ded5eb1` | `7ff1712fc2efe66661377481e1d37b8577b30a9979f10c83d2539cd2e31d6632` |
| `n297/n297_witness.yaml` | `7b4701f35e815301e4f467d214fab4205ded5eb1` | `96941f37d9c937b041f5e76efee7859485639f23c41a9bebcea01acef1be1bc5` |
| `above324_from_n297/n332_exact.json` | `c70defaf39af47db220d1e7c2922590637ffb664` | `d6fb8424688c6272acd452c7a0e46104e69f1bcd20def89741e1ac55062d0873` |
| `above324_from_n297/n409_exact.json` | `c70defaf39af47db220d1e7c2922590637ffb664` | `513a40e3cbb182f344ed0194e4fe8974d7f518a27d1ad7bff4d2f267eac4a443` |

The two `n297` files are the same blobs at both pins.

## Layout

- `programs/`: the review’s programs, the controls plan, the issues as fetched.
- `frozen/`: the checker’s digests at its freeze, the plan’s digest when it was stated,
  the findings’ digest at their freeze, and the frozen review text.
- `out/`: the receipts.

## Programs

Every program is lane L153’s own, written for this review as a clean-room
implementation: it imports nothing from this repository or the source, and reuses no
code of any earlier review.
The review of #967 (lane L127) was the model; its text, README and frozen digest lists
were read, and its programs were not opened.
Each was run with CPython 3.14.7 as `python -I -B` from `packing/` of a worktree of
`main` at `da5091505`, through `uv run --frozen --all-extras --group dev`, under
`nice -n 19`.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `l153_reader.py` | the reading: the JSON layout, count, canonical scalars; for 297 the Witness/v2 twin and its equality with the JSON file | a certificate and, for 297, its twin | nothing (a module) |
| `l153_sat.py` | method A: unit squares, wall clearances and pair margins by separating axes in Python integers over per-square denominators | integers from the reader | nothing (a module) |
| `l153_clip.py` | method B: unit squares (sides and diagonals of the corners), pairs and walls by exact convex clipping, containment by area, in `gmpy2.mpq` | integers from the reader | nothing (a module) |
| `l153_check.py` | a certificate, by both methods, every square, wall and pair | a certificate and, for 297, its twin | `out/check-nNNN.json` |
| `l153_geom.py` | nothing: builds squares with known margins and areas, the closed-form margin from centres and half-extents, and closing moves, for the self-test and the controls | fractions | nothing (a module) |
| `l153_selftest.py` | both methods and the reader against 7,720 cases with hand-derived answers, and two broken copies | nothing | `out/selftest.json` |
| `l153_plan_facts.py` | nothing: the exact facts the controls plan states its outcomes from | a certificate, its check receipt | `out/plan-facts-nNNN.json` |
| `l153_make_plan.py` | nothing: states the controls and their outcomes | the check receipts, the plan facts | `programs/controls-plan.json` |
| `l153_controls.py` | the controls, by both methods or the reader | a certificate, the plan, its facts, its check receipt | `out/controls-nNNN.json` |
| `l153_describe.py` | nothing: the side’s decimals, the tilts, the near-pair margins | a certificate, its check receipt | `out/describe-nNNN.json` |

`programs/issue-977-979.json` is the two issues as fetched at 11:03Z, trimmed to their
text and dates.

From `packing/`, with `A` the clone checked out at `7b4701f`, `C` the clone checked out
at `c70defa`, and `R` this directory:

```bash
PY="nice -n 19 uv run --frozen --all-extras --group dev python -I -B"
J297="$A/n297/n297_exact.json $A/n297/n297_witness.yaml"
J332=$C/above324_from_n297/n332_exact.json
J409=$C/above324_from_n297/n409_exact.json
$PY $R/programs/l153_selftest.py $R/out/selftest.json
$PY $R/programs/l153_check.py n297 $J297 $R/out/check-n297.json
$PY $R/programs/l153_check.py n332 $J332 $R/out/check-n332.json
$PY $R/programs/l153_check.py n409 $J409 $R/out/check-n409.json
$PY $R/programs/l153_plan_facts.py n297 $J297 $R/out/check-n297.json $R/out/plan-facts-n297.json
$PY $R/programs/l153_plan_facts.py n332 $J332 $R/out/check-n332.json $R/out/plan-facts-n332.json
$PY $R/programs/l153_plan_facts.py n409 $J409 $R/out/check-n409.json $R/out/plan-facts-n409.json
$PY $R/programs/l153_make_plan.py $R/programs/controls-plan.json \
  n297 $R/out/check-n297.json $R/out/plan-facts-n297.json twin \
  n332 $R/out/check-n332.json $R/out/plan-facts-n332.json none \
  n409 $R/out/check-n409.json $R/out/plan-facts-n409.json none
for n in 297 332 409; do
  eval J=\$J$n
  $PY $R/programs/l153_controls.py n$n $J $R/programs/controls-plan.json \
    $R/out/plan-facts-n$n.json $R/out/check-n$n.json $R/out/controls-n$n.json
  $PY $R/programs/l153_describe.py n$n $J $R/out/check-n$n.json $R/out/describe-n$n.json
done
```

## What They Printed

- `l153_selftest.py`: `PASSED 7720 cases 0 failed`; broken method A fails 2,512, broken
  method B 2,512.
- `l153_check.py`: `ACCEPT` for each file.
  297: 43,956 pairs apart by both methods, none touching, 33 wall contacts (16 top, 17
  right). 332: 54,946 pairs, 35 touching.
  409: 83,436 pairs, 302 touching.
  Least gap $9.99999999999999 \times 10^{-61}$ at (232, 237) in each.
- `l153_plan_facts.py`: S4 pair (188, 194), moving 188; 794, 865 and 882 near pairs.
- `l153_controls.py`: `EVERY_CONTROL_AS_STATED`, 19 of 19, 18 of 18 and 18 of 18.
- `l153_describe.py`: 110 squares of the 297 file turned beyond 44°, 187 upright; 794
  pairs from $9.99999999999999 \times 10^{-61}$ to $1.2071 \times 10^{-60}$, then
  $2.103 \times 10^{-7}$.

## Frozen Files

| File | What it fixes | When |
| --- | --- | --- |
| `frozen/checker-frozen-digests.txt` | the four source certificates, the six checker files and the receipts they had written | 2026-11-14T11:11:08Z |
| `frozen/controls-plan-digest.txt` | the controls plan, its facts and their programs, before `l153_controls.py` existed | 2026-11-14T11:16:43Z |
| `frozen/findings-frozen-digest.txt` | the frozen review text and the receipts at the freeze | 2026-11-14T11:28:52Z |
| `frozen/review-2026-11-14-de-winter-977-979.frozen.md` | the review as frozen, before the author’s checkers, outputs or READMEs, or this repository’s verifier, were read | 2026-11-14T11:28:52Z |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
