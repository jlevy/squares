# n=12 3969/1000 T-017-Seeded Four-Grid Window-7 Covering Receipt

Status: **site set still open, unconverged**. The side stays open. No freeze.

Session-140 leftover rank 4: four-grid `(26, 35, 43, 48)` unioned with T-017's
atom sites from `certificate.json` scaled from `99/25` to `3969/1000`, plus
`--seed-windows 7`, `(n, L, B, net) = (12, 3969/1000, 9977/10000, 181 directions)`.
Seed sites 2533. The 1200 s deadline stopped the row loop after 36 LP rounds at
`12.091168` (54 still violated). It crossed 12 at round 11 (`12.000732`) and
sat near `12.091` from round 32. This is lower than the Session-139 four-grid
without windows at the same side (`12.116115`).

Remaining rows can only raise this value, so `12.091168` is not a covering
below 12.
Adding sites, or more wall, can still lower it. T-017 is unchanged. T-029 was
not offered. H-218 stays unconfirmed. Side `3.969` already exists.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 12 --side 3969/1000 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 26,35,43,48 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-certificate cases/n12_fractional_certificate/certificate.json --seed-map scale \
  --seed-windows 7 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-3969-1000-t017-grid4-windows7-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-3969-1000-t017-grid4-windows7-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-3969-1000-t017-grid4-windows7-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-3969-1000-t017-grid4-windows7-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-038/n12-3969-1000-t017-grid4-windows7.log
```

No freeze file: the 1200 s deadline stopped the row loop after 36 rounds.
Wall 1251.7 s. The leftover walker then printed `STOP before
n18-1871-400-t028-auto-windows5: remain=-4s`.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `12.091168` |
| Sites / orbits / rows | 8569 / 1184 / 10040 |
| Seed sites | 2533 |
| LP rounds | 36 |
| Crossing | round 11 (`12.000732`) |
| Wall | 1251.7 s |
| `least_covered` | 0.997200 |
| Converged | no (`violated == 54` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 12.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
