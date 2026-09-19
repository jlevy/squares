# n=12 793/200 T-017 Auto Window-7 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-141 exp-175: T-017 seed plus auto grids plus `--seed-windows 7`,
`(n, L, B, net) = (12, 793/200, 9977/10000, 181 directions)`. Auto resolved to
`(26, 35, 43)`. Seed sites 2533. The 1200 s deadline stopped the row loop after
38 LP rounds at `12.067502` (102 still violated). It crossed 12 at round 11
(`12.005485`). The objective sat at `12.067502` from round 32.

Remaining rows can only raise this value, so `12.067502` is not a covering
below 12.
Do not more-wall this set. T-017 stands. T-030 was not offered. H-218 stays
unconfirmed.

This is the first first-party covering row at `793/200`.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 12 --side 793/200 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-windows 7 --seed-certificate cases/n12_fractional_certificate/certificate.json \
  --seed-map scale \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-039/n12-793-200-t017-auto-windows7-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-039/n12-793-200-t017-auto-windows7-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-039/n12-793-200-t017-auto-windows7-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n12-793-200-t017-auto-windows7-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n12-793-200-t017-auto-windows7.log
```

No freeze file: the 1200 s deadline stopped the row loop after 38 rounds.
Wall 1221.6 s. The walker then started n=12 `397/100` T-017 auto plus windows 7
as exp-176.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `12.067502` |
| Sites / orbits / rows | 6269 / 885 / 9171 |
| Seed sites | 2533 |
| Auto grids | `(26, 35, 43)` |
| LP rounds | 38 |
| Crossing | round 11 (`12.005485`) |
| Wall | 1221.6 s |
| `least_covered` | 0.989127 |
| Converged | no (`violated == 102` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 12.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
