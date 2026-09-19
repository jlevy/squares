# n=32 29/5 Seedless Auto Window-5 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-141 exp-166: seedless auto grids plus `--seed-windows 5`,
`(n, L, B, net) = (32, 29/5, 9977/10000, 181 directions)`. Auto resolved to
`(42, 56, 70)`. Seed sites 625 (windows only). The 1200 s deadline stopped the
row loop after 35 LP rounds at `29.803318` (546 still violated). It did not
cross 32.

Remaining rows can only raise this value, so `29.803318` is not a covering
below 32.
Do not more-wall this set. Nagamochi `1 + sqrt(23)` stands. T-030 was not
offered. H-220 stays unconfirmed.

This is the first first-party covering row at n=32.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 32 --side 29/5 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-windows 5 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-039/n32-29-5-auto-windows5-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-039/n32-29-5-auto-windows5-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-039/n32-29-5-auto-windows5-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n32-29-5-auto-windows5-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n32-29-5-auto-windows5.log
```

No freeze file: the 1200 s deadline stopped the row loop after 35 rounds.
Wall 1206.0 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `29.803318` |
| Sites / orbits / rows | 10417 / 1356 / 11974 |
| Seed sites | 625 |
| Auto grids | `(42, 56, 70)` |
| LP rounds | 35 |
| Crossing | none |
| Wall | 1206.0 s |
| `least_covered` | 0.929890 |
| Converged | no (`violated == 546` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 32.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
