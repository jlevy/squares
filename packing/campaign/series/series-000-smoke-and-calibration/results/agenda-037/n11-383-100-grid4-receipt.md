# n=11 383/100 Four-Grid Covering Receipt

Status: **site set refuted**. The side stays open.

Session-139 probe on `--grid-counts 25,34,41,48` at
`(n, L, B, net) = (11, 383/100, 9977/10000, 181 directions)`.
This is the denser named site set after auto grids `(25, 34, 41)` returned
`11.192598`. A restricted optimum at or above 11 on a converged row loop refutes
this site set only. Adding sites can still lower the covering value, so
`383/100` is not barred. T-025 and T-026 are unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 11 --side 383/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 25,34,41,48 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 600 \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-383-100-grid4-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-383-100-grid4-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-383-100-grid4.log
```

`--freeze-family` was not requested. Column generation added one orbit after the
row loop and stopped; wall 81.7 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `11.142857` |
| Rationalised total | `2228577/200000` = `11.142885` |
| Sites / orbits / rows | 5665 / 756 / 6317 |
| LP rounds | 23 |
| Crossing | round 6 (`11.020986`); rounds 3–5 sat at `11.000000` |
| Wall | 81.7 s |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |

About 2,300 extra sites dropped the restricted optimum by 0.050 from the auto-grid
row. `devtools.decide_certificate` was not run: the mass is not below 11.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
