# n=12 397/100 T-017 Auto Window-7 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-141 exp-176: T-017 seed plus auto grids plus `--seed-windows 7`,
`(n, L, B, net) = (12, 397/100, 9977/10000, 181 directions)`. Auto resolved to
`(26, 35, 43)`. Seed sites 2533. The 1200 s deadline stopped the row loop after
34 LP rounds at `12.097146` (33 still violated). It crossed 12 at round 8
(`12.021858`). The objective sat at `12.097146` from round 32.

Remaining rows can only raise this value, so `12.097146` is not a covering
below 12.
Do not more-wall this set. T-017 stands. T-030 was not offered. H-218 stays
unconfirmed.

Side `3.97` already exists. This is a new named site set at that side.
Closer than four-grid plus windows 7 at this side (`12.133391`).

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 12 --side 397/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-windows 7 --seed-certificate cases/n12_fractional_certificate/certificate.json \
  --seed-map scale \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-039/n12-397-100-t017-auto-windows7-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-039/n12-397-100-t017-auto-windows7-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-039/n12-397-100-t017-auto-windows7-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n12-397-100-t017-auto-windows7-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n12-397-100-t017-auto-windows7.log
```

No freeze file: the 1200 s deadline stopped the row loop after 34 rounds.
Wall 1212.9 s. The walker then started n=19 `241/50` T-020 four-grid plus
windows 7 as exp-177.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `12.097146` |
| Sites / orbits / rows | 6269 / 885 / 8086 |
| Seed sites | 2533 |
| Auto grids | `(26, 35, 43)` |
| LP rounds | 34 |
| Crossing | round 8 (`12.021858`) |
| Wall | 1212.9 s |
| `least_covered` | 0.998924 |
| Converged | no (`violated == 33` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 12.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
