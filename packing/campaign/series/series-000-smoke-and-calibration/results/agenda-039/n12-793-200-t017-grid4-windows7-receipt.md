# n=12 793/200 T-017 Four-Grid Window-7 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-141 exp-178: T-017 seed plus four-grid `(26, 35, 43, 48)` plus
`--seed-windows 7`,
`(n, L, B, net) = (12, 793/200, 9977/10000, 181 directions)`. Seed sites 2533.
The 1200 s deadline stopped the row loop after 35 LP rounds at `12.066995`
(192 still violated). It crossed 12 at round 13 (`12.016486`). The objective
sat at `12.06699` from round 32. Closer than auto plus windows 7 at this side
(`12.067502`).

Remaining rows can only raise this value, so `12.066995` is not a covering
below 12.
Do not more-wall this set. T-017 stands. T-030 was not offered. H-218 stays
unconfirmed.

Side `3.965` already exists. This is a new named site set at that side.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 12 --side 793/200 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 26,35,43,48 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-windows 7 --seed-certificate cases/n12_fractional_certificate/certificate.json \
  --seed-map scale \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-039/n12-793-200-t017-grid4-windows7-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-039/n12-793-200-t017-grid4-windows7-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-039/n12-793-200-t017-grid4-windows7-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n12-793-200-t017-grid4-windows7-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n12-793-200-t017-grid4-windows7.log
```

No freeze file: the 1200 s deadline stopped the row loop after 35 rounds.
Wall 1216.8 s. The walker then started n=18 `4679/1000` T-029 auto plus
windows 5 as exp-179.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `12.066995` |
| Sites / orbits / rows | 8569 / 1184 / 9701 |
| Seed sites | 2533 |
| Grids | `(26, 35, 43, 48)` |
| LP rounds | 35 |
| Crossing | round 13 (`12.016486`) |
| Wall | 1216.8 s |
| `least_covered` | 0.988078 |
| Converged | no (`violated == 192` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 12.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
