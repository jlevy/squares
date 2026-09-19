# n=11 383/100 Grid Covering Receipt

Status: **site set refuted**. The side stays open.

Session-139 probe on BC-191 auto grids `(25, 34, 41)` at
`(n, L, B, net) = (11, 383/100, 9977/10000, 181 directions)`.
A restricted optimum at or above 11 on a converged row loop refutes this site set
only. Adding sites can still lower the covering value, so `383/100` is not barred.
T-025 at `191/50` and T-026 at
`955000*sqrt(518400042893309449)/179696714646249` are unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 11 --side 383/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 600 \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-383-100-grid-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-383-100-grid-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-383-100-grid.log
```

`--freeze-family` was not requested. Column generation added one orbit after the
row loop and stopped; wall 82.2 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `11.192598` |
| Rationalised total | `44770567/4000000` = `11.19264175` |
| Sites / orbits / rows | 3365 / 457 / 5233 |
| LP rounds | 24 |
| Crossing | round 6 (`11.096552`); round 4 sat at `11.000000` |
| Wall | 82.2 s |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |

`devtools.decide_certificate` was not run: the mass is not below 11.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
