# n=27 525/100 Seedless Auto Window-5 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-141 exp-170: seedless auto grids plus `--seed-windows 5`,
`(n, L, B, net) = (27, 525/100, 9977/10000, 181 directions)`. Auto resolved to
`(37, 50, 62)`. Seed sites 625 (windows only). The 1200 s deadline stopped the
row loop after 38 LP rounds at `25.000000` (546 still violated). It sat on
`25.000000` from the early rounds. It did not cross 27.

Remaining rows can only raise this value, so `25.000000` is not a covering
below 27.
Do not more-wall this set. Nagamochi `1 + sqrt(18)` stands. T-030 was not
offered. H-220 stays unconfirmed.

This is the first first-party covering row at n=27.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 27 --side 525/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-windows 5 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-039/n27-525-100-auto-windows5-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-039/n27-525-100-auto-windows5-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-039/n27-525-100-auto-windows5-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n27-525-100-auto-windows5-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n27-525-100-auto-windows5.log
```

No freeze file: the 1200 s deadline stopped the row loop after 38 rounds.
Wall 1201.0 s. The walker then stopped before n=29 (`remain=-1094s` past the
10:26Z cut). Resume after 11:26Z.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `25.000000` |
| Sites / orbits / rows | 8329 / 1099 / 14004 |
| Seed sites | 625 |
| Auto grids | `(37, 50, 62)` |
| LP rounds | 38 |
| Crossing | none |
| Wall | 1201.0 s |
| `least_covered` | 0.888193 |
| Converged | no (`violated == 546` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 27.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
