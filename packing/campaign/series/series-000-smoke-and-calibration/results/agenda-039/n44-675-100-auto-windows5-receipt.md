# n=44 675/100 Seedless Auto Window-5 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-141 exp-173: seedless auto grids plus `--seed-windows 5`,
`(n, L, B, net) = (44, 675/100, 9977/10000, 181 directions)`. Auto resolved to
`(50, 67, 83)`. Seed sites 900 (windows only). The 1200 s deadline stopped the
row loop after 28 LP rounds at `41.236782` (546 still violated). It did not
cross 44.

Remaining rows can only raise this value, so `41.236782` is not a covering
below 44.
Do not more-wall this set. Nagamochi `1 + sqrt(33)` stands. T-030 was not
offered. H-220 stays unconfirmed. The eight queued Nagamochi sides are
measured.

This is the first first-party covering row at n=44.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 44 --side 675/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-windows 5 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-039/n44-675-100-auto-windows5-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-039/n44-675-100-auto-windows5-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-039/n44-675-100-auto-windows5-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n44-675-100-auto-windows5-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n44-675-100-auto-windows5.log
```

No freeze file: the 1200 s deadline stopped the row loop after 28 rounds.
Wall 1300.3 s. The walker then started n=19 `481/100` four-grid plus windows 7
as exp-174.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `41.236782` |
| Sites / orbits / rows | 14765 / 1939 / 10055 |
| Seed sites | 900 |
| Auto grids | `(50, 67, 83)` |
| LP rounds | 28 |
| Crossing | none |
| Wall | 1300.3 s |
| `least_covered` | 0.916075 |
| Converged | no (`violated == 546` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 44.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
