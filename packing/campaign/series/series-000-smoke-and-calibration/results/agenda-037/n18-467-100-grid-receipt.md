# n=18 467/100 Auto-Grid Covering Receipt

Status: **unconverged at 18**. The side stays open.

Session-139 probe on BC-191 auto grids `(32, 43, 53)` at
`(n, L, B, net) = (18, 467/100, 9977/10000, 181 directions)`.
`467/100 = 4.67` sits just below the historical n=18 probes at `117/25 = 4.68`.
The row loop crossed eighteen at LP round 15 (`18.000000`) and held that value
through round 57, when the 600 s deadline stopped it with 336 placements still
violated. Remaining rows can only raise the restricted optimum. This site set
cannot confirm. Adding sites can still lower the covering value, so `467/100`
is not barred.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 18 --side 467/100 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 0 \
  --column-rounds 1 --max-rounds 400 --deadline-seconds 600 \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-467-100-grid-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-467-100-grid-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-467-100-grid.log
```

`--freeze-family` was not requested.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `18.000000` |
| Sites / orbits / rows | 5669 / 763 / 16426 |
| LP rounds | 57 |
| Crossing | round 15 (`18.000000`) |
| Wall | 621.7 s |
| `least_covered` | 0.973636 |
| Converged | no (deadline) |

`devtools.decide_certificate` was not run: the mass is not below 18.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
