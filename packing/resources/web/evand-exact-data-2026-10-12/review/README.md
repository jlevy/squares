# Grade-C Review Programs (23 October 2026)

The stage 4 mathematical review of the #545 import,
[review-2026-10-23-evand-grade-c-theorem-c.md](../../../../../docs/project/reviews/review-2026-10-23-evand-grade-c-theorem-c.md)
(bead `think-7scz`), wrote these programs and ran them here.
They import nothing from the source and run none of its code.
Their authors read Theorem C (`tasks/exact-minpoly/grade-C.md`), `gradec.py` and the
three modules it imports, and the published n = 10 certificate and run logs before
writing them; the review records that as independence after reading the producer’s code,
not a clean room.

## The Programs

| Program | Registered | Decides | Reads |
| --- | --- | --- | --- |
| `check_theorem_c.py` | `V-evand-gradec-review-check` | the hypotheses of Theorem C, as the review repairs it, and the record’s packing property, exactly | an exact form `n-N.minpoly.json.gz`; the archive’s `n-N.contacts.json`, in memory |
| `compare_certificates.py` | `V-evand-gradec-review-compare` | nothing: it compares the receipts with the published certificates | the receipts; the archive’s `n-N.gradec.json`, in memory |
| `test_derivatives.py` | `V-evand-gradec-review-derivatives` | nothing: it tests the row derivatives `check_theorem_c.py` uses | the same inputs as `check_theorem_c.py` |
| `summarize_run.py` | not registered; no evidence entry cites it | nothing: it merges the receipt files, sorted by count, and totals them | the receipts |

**`check_theorem_c.py`** decides, for each count:

- **P.** The record is a packing in $[0, S]^2$: every corner inside, and every pair
  weakly separated along an edge normal of one of the two squares, by outward-rounded
  float intervals where they decide and exact arithmetic in $K$ where they do not.
- **R.** Every row the contacts file lists is tight at the record and is a wall row, an
  interior incidence ($|\tau| < \frac12$) or one of a complete side-end pair; a lone
  side-end incidence or a corner beyond a side end is dropped, which only relaxes.
- **M.** Exact multipliers $\lambda^\ast > 0$ with $\sum_r \lambda^\ast_r L_r = e_S$: a
  linear program (scipy, HiGHS) proposes a max-min point, the rows outside an exact basis
  are rounded to dyadic rationals and the basis is solved exactly; the identity and every
  sign are then verified.
- **N.** The flat family $F$ (null space of the position columns), $\operatorname{null}
  L_0$ and a complement $W'$ of $F$ in it, by exact sparse elimination; every vector is
  verified by products, and a numerical SVD gives the same nullity at every count.
- **A.** Hypothesis 2: for each $w \in W'$ and each flat direction $k$, a lift $v$ with
  $L_0 v = -A_k w$, zero at $S$ and at the angle of every square owning a side that the
  family slides along (the review’s slip form); then the identities $L(\varphi)(w +
  \sum_k \varphi_k v_k) \equiv 0$ are verified, with $A_k$ computed both from the slip
  formula and, for the first three directions, as $L$ at shifted centres minus $L_0$.
- **H.** The Lagrangian Hessian’s $F \times W'$ block vanishes and its restriction to
  $W'$ is positive definite by an exact $LDL^\mathsf{T}$.

Arithmetic is CPython’s `int` and `fractions.Fraction`: in $\mathbb{Q}$ for the 175
configurations of field degree 1, and in $\mathbb{Q}[t]/(f)$ for degrees 2 and 4, with
signs by exact interval evaluation at $t^\ast$ and bisection of the stated interval, after
checking that $f$ changes sign on it. For 230 and 261, `--dropzero` drops the rows a
linear program finds forced to zero in every multiplier vector, a side-end pair as a whole.

## How to Run

From `packing/`, with `P = resources/web/evand-exact-data-2026-10-12`:

```sh
OPENBLAS_NUM_THREADS=1 .venv/bin/python3 -I $P/review/check_theorem_c.py \
  --minpoly-dir $P/source/search/exact/minpoly/data \
  --archive $P/acquisition/release/gradec-233.tar.zst \
  --dropzero 230,261 --out /tmp/theorem-c.jsonl $(cat $P/review/counts.txt)
.venv/bin/python3 -I $P/review/compare_certificates.py \
  --archive $P/acquisition/release/gradec-233.tar.zst /tmp/theorem-c.jsonl
.venv/bin/python3 -I $P/review/test_derivatives.py \
  --minpoly-dir $P/source/search/exact/minpoly/data \
  --archive $P/acquisition/release/gradec-233.tar.zst \
  5 10 19 53 54 66 70 107 127 150 153 175 178 230 267
```

`counts.txt` lists the 233 counts. The review ran the 233 as two processes of alternate
counts under `nice`, with the second's last seven counts split into two more (What They
Printed), which is how the receipts were written; one process gives the same lines.

## What They Printed

**`check_theorem_c.py`**, run on 23 October 2026 from 07:29:39Z to 08:26:13Z on the
233 counts of `counts.txt`, wrote one receipt per count, and every one says valid true:
175 configurations of field degree 1, 51 of degree 2 and 7 of degree 4. The checks took
1,463 CPU-seconds in all, a median of 0.94 and at most 369 (n = 294, with
$\dim W = 11$ and $\dim F = 88$), on four shared cores at load averages of 17 to 38.
It ran as two processes of alternate counts; the second was stopped after n = 291 so that
its last seven counts could run in two processes, n = 294 alone and 313 to 323 together,
so three ran at once near the end, and every count was run once.

| Quantity | Value |
| --- | --- |
| Rows classified | 202,010, of which 184,412 side-end rows, at 231 counts (all but 1 and 5) |
| Side-end rows that slip along the flat family | 58,988, at 206 counts |
| Counts with a flat family; with $\dim W > 0$ | 214; 47, at most $\dim W = 11$ |
| Lifts solved for hypothesis 2 | 1,066 |
| Rows dropped as forced to zero | 24 at 230, 24 at 261 (the source’s 24 at each) |
| Lone side-end incidences dropped | 36 at 230, 40 at 261 |
| Corners beyond a side end dropped | 12 at 66, 6 at 127, 16 at 150, 8 at 175 |
| SVD nullity of $L_0$ | equal to the exact one at all 233; smallest ratio of the last nonzero to the first zero singular value $2.1 \times 10^{13}$ |
| Least interior margin | $7.2 \times 10^{-17}$, at n = 175, decided exactly |
| Least multiplier | 0.0015 |

**`compare_certificates.py`** printed `agree: true` with no disagreement: at all 233
counts the row set, the rank of $L_0$, $\dim F$, $\dim W$, the moving squares and the
number of load-bearing squares are the published certificate’s; the interior margins
agree to the last digit printed, and the least multipliers within $2.1 \times 10^{-9}$
relative.

**`test_derivatives.py`** printed PASS: 5,646 rows of 15 configurations, largest
gradient error $1.3 \times 10^{-10}$ and largest Hessian error $2.7 \times 10^{-5}$ at a
step of $10^{-5}$, the rounding level of a second difference.

**Controls**, held by `packing/tests/test_evand_gradec_review.py`: with a load-bearing
square of n = 10 moved by $10^{-30}$ the checker refuses, as it does with the right-wall
rows removed; and its $LDL^\mathsf{T}$ refuses an indefinite matrix.

## Receipts

- [`../receipts/review-theorem-c-233.jsonl`](../receipts/review-theorem-c-233.jsonl): one
  line per count, sorted by count, with the inputs’ SHA-256, the program’s SHA-256, the
  environment, and every quantity the checker computed.
- [`../receipts/review-compare-233.json`](../receipts/review-compare-233.json): the
  comparison with the published certificates.
- [`../receipts/review-derivatives.json`](../receipts/review-derivatives.json): the
  derivative test.
- [`../receipts/review-run-2026-10-23.json`](../receipts/review-run-2026-10-23.json): the
  run itself, its commands, times and totals.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
