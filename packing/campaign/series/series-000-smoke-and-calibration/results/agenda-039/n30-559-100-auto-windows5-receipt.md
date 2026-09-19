# n=30 559/100 Seedless Auto Window-5 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-141 exp-168: seedless auto grids plus `--seed-windows 5`,
`(n, L, B, net) = (30, 559/100, 9977/10000, 181 directions)`. Auto resolved to
`(40, 54, 67)`. Seed sites 625 (windows only). The 1200 s deadline stopped the
row loop after 50 LP rounds at `27.178193` (93 still violated). It did not
cross 30.

Remaining rows can only raise this value, so `27.178193` is not a covering
below 30.
Do not more-wall this set. Nagamochi `1 + sqrt(21)` stands. T-030 was not
offered. H-220 stays unconfirmed.

This is the first first-party covering row at n=30.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 30 --side 559/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-windows 5 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-039/n30-559-100-auto-windows5-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-039/n30-559-100-auto-windows5-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-039/n30-559-100-auto-windows5-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n30-559-100-auto-windows5-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n30-559-100-auto-windows5.log
```

No freeze file: the 1200 s deadline stopped the row loop after 50 rounds.
Wall 1213.0 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `27.178193` |
| Sites / orbits / rows | 9609 / 1269 / 15704 |
| Seed sites | 625 |
| Auto grids | `(40, 54, 67)` |
| LP rounds | 50 |
| Crossing | none |
| Wall | 1213.0 s |
| `least_covered` | 0.971793 |
| Converged | no (`violated == 93` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 30.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
