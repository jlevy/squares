# n=45 684/100 Seedless Auto Window-5 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-141 exp-172: seedless auto grids plus `--seed-windows 5`,
`(n, L, B, net) = (45, 684/100, 9977/10000, 181 directions)`. Auto resolved to
`(51, 68, 84)`. Seed sites 900 (windows only). The 1200 s deadline stopped the
row loop after 26 LP rounds at `42.137360` (546 still violated). It did not
cross 45.

Remaining rows can only raise this value, so `42.137360` is not a covering
below 45.
Do not more-wall this set. Nagamochi `1 + sqrt(34)` stands. T-030 was not
offered. H-220 stays unconfirmed.

This is the first first-party covering row at n=45.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 45 --side 684/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-windows 5 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-039/n45-684-100-auto-windows5-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-039/n45-684-100-auto-windows5-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-039/n45-684-100-auto-windows5-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n45-684-100-auto-windows5-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n45-684-100-auto-windows5.log
```

No freeze file: the 1200 s deadline stopped the row loop after 26 rounds.
Wall 1253.8 s. The walker then started n=44 `675/100` as exp-173.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `42.137360` |
| Sites / orbits / rows | 15173 / 1967 / 9572 |
| Seed sites | 900 |
| Auto grids | `(51, 68, 84)` |
| LP rounds | 26 |
| Crossing | none |
| Wall | 1253.8 s |
| `least_covered` | 0.879972 |
| Converged | no (`violated == 546` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 45.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
