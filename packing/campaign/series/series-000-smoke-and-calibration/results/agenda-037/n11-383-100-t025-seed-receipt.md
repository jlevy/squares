# n=11 383/100 T-025-Seeded Covering Receipt

Status: **site set refuted**. The side stays open.

Session-139 probe: four-grid `(25, 34, 41, 48)` unioned with T-025's 584 atom
sites, scaled from `191/50` to `383/100`, at
`(n, L, B, net) = (11, 383/100, 9977/10000, 181 directions)`.
The extra seed dropped the restricted optimum by 0.0025 from the four-grid row
`11.142857`. A restricted optimum at or above 11 on a converged row loop
refutes this site set only. T-025 and T-026 are unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 11 --side 383/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 25,34,41,48 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 600 \
  --seed-certificate cases/n11_threshold_certificate/certificate.json --seed-map scale \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-383-100-t025-seed-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-383-100-t025-seed-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-383-100-t025-seed.log
```

`--freeze-family` was not requested. Column generation added one orbit after the
row loop and stopped; wall 107.9 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `11.140351` |
| Rationalised total | `1114039/100000` = `11.14039` |
| Sites / orbits / rows | 6249 / 835 / 6753 |
| Seed sites | 584 |
| LP rounds | 28 |
| Crossing | round 6 (`11.020202`); rounds 3–5 sat at `11.000000` |
| Wall | 107.9 s |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |

Point-atom covering at `383/100` did not fall below eleven on auto grids, the
four-grid, or this T-025-seeded union. `devtools.decide_certificate` was not run.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
