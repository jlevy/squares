# n=26 513/100 Seedless Auto Window-5 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-141 exp-169: seedless auto grids plus `--seed-windows 5`,
`(n, L, B, net) = (26, 513/100, 9977/10000, 181 directions)`. Auto resolved to
`(36, 49, 60)`. Seed sites 625 (windows only). The 1200 s deadline stopped the
row loop after 42 LP rounds at `25.000000` (546 still violated). It sat on
`25.000000` from round 11. It did not cross 26.

Remaining rows can only raise this value, so `25.000000` is not a covering
below 26.
Do not more-wall this set. Nagamochi `1 + sqrt(17)` stands. T-030 was not
offered. H-220 stays unconfirmed.

This is the first first-party covering row at n=26.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 26 --side 513/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-windows 5 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-039/n26-513-100-auto-windows5-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-039/n26-513-100-auto-windows5-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-039/n26-513-100-auto-windows5-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n26-513-100-auto-windows5-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n26-513-100-auto-windows5.log
```

No freeze file: the 1200 s deadline stopped the row loop after 42 rounds.
Wall 1208.6 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `25.000000` |
| Sites / orbits / rows | 7913 / 1049 / 15312 |
| Seed sites | 625 |
| Auto grids | `(36, 49, 60)` |
| LP rounds | 42 |
| Crossing | none |
| Wall | 1208.6 s |
| `least_covered` | 0.879358 |
| Converged | no (`violated == 546` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 26.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
