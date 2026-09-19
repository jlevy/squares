# n=12 397/100 T-017-Seeded Four-Grid Covering Receipt

Status: **site set refuted, unconverged**. The side stays open.

Session-139 probe: four-grid `(26, 35, 43, 48)` unioned with T-017's 2097 atom
sites scaled from `99/25` to `397/100`,
`(n, L, B, net) = (12, 397/100, 9977/10000, 181 directions)`.
The 900 s deadline stopped the row loop after 33 LP rounds at `12.122748`
(108 still violated). Crossed twelve at round 8 (`12.001574`). BC-206's
seeded auto at this side crossed at `12.016263`; this four-grid continued
and finished higher. Remaining rows can only raise this value. Adding sites
can still lower it, so `397/100` is not barred. T-017 is unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 12 --side 397/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 26,35,43,48 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 900 \
  --seed-certificate cases/n12_fractional_certificate/certificate.json --seed-map scale \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-037/n12-397-100-t017-grid4-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-037/n12-397-100-t017-grid4-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n12-397-100-t017-grid4-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n12-397-100-t017-grid4-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n12-397-100-t017-grid4.log
```

No freeze file: the row loop did not converge.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `12.122748` |
| Sites / orbits / rows | 8133 / 1120 / 9290 |
| Seed sites | 2097 |
| LP rounds | 33 |
| Crossing | round 8 (`12.001574`) |
| Wall | 939.9 s |
| `least_covered` | 0.987523 |
| Converged | no (`violated == 108` at stop) |

`devtools.decide_certificate` was not run: there is no freeze below 12.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
