# n=31 57/10 Seedless Auto Window-5 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-141 exp-167: seedless auto grids plus `--seed-windows 5`,
`(n, L, B, net) = (31, 57/10, 9977/10000, 181 directions)`. Auto resolved to
`(41, 55, 68)`. Seed sites 625 (windows only). The 1200 s deadline stopped the
row loop after 38 LP rounds at `28.331329` (462 still violated). It did not
cross 31.

Remaining rows can only raise this value, so `28.331329` is not a covering
below 31.
Do not more-wall this set. Nagamochi `1 + sqrt(22)` stands. T-030 was not
offered. H-220 stays unconfirmed.

This is the first first-party covering row at n=31.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 31 --side 57/10 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-windows 5 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-039/n31-57-10-auto-windows5-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-039/n31-57-10-auto-windows5-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-039/n31-57-10-auto-windows5-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n31-57-10-auto-windows5-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n31-57-10-auto-windows5.log
```

No freeze file: the 1200 s deadline stopped the row loop after 38 rounds.
Wall 1284.5 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `28.331329` |
| Sites / orbits / rows | 9941 / 1318 / 12536 |
| Seed sites | 625 |
| Auto grids | `(41, 55, 68)` |
| LP rounds | 38 |
| Crossing | none |
| Wall | 1284.5 s |
| `least_covered` | 0.962225 |
| Converged | no (`violated == 462` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 31.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
