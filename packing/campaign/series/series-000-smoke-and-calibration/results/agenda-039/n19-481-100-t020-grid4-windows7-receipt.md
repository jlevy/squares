# n=19 481/100 T-020 Four-Grid Window-7 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-141 exp-174: T-020 seed from `certificate-24-5.json` plus four-grid
`(34, 45, 56, 64)` plus `--seed-windows 7`,
`(n, L, B, net) = (19, 481/100, 9977/10000, 181 directions)`. Seed sites 3044.
The 1200 s deadline stopped the row loop after 34 LP rounds at `19.111435`
(369 still violated). It crossed 19 at round 15 (`19.017579`). Closer than
leftover auto plus windows 6 at this side (`19.132115`).

Remaining rows can only raise this value, so `19.111435` is not a covering
below 19.
Do not more-wall this set. T-020 stands. T-030 was not offered. H-218 stays
unconfirmed.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 19 --side 481/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 34,45,56,64 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-windows 7 --seed-certificate cases/n20_fractional_certificate/certificate-24-5.json \
  --seed-map scale \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-039/n19-481-100-t020-grid4-windows7-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-039/n19-481-100-t020-grid4-windows7-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-039/n19-481-100-t020-grid4-windows7-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n19-481-100-t020-grid4-windows7-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n19-481-100-t020-grid4-windows7.log
```

No freeze file: the 1200 s deadline stopped the row loop after 34 rounds.
Wall 1285.3 s. The walker then started n=12 `793/200` T-017 auto plus windows 7
as exp-175.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `19.111435` |
| Sites / orbits / rows | 13153 / 1724 / 11449 |
| Seed sites | 3044 |
| Grids | `(34, 45, 56, 64)` |
| LP rounds | 34 |
| Crossing | round 15 (`19.017579`) |
| Wall | 1285.3 s |
| `least_covered` | 0.966385 |
| Converged | no (`violated == 369` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 19.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
