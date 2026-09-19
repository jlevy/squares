# n=17 23/5 Grid Covering Receipt

Status: **site set refuted, unconverged**. The side stays open.

Session-139 probe on BC-191 auto grids `(32, 42, 52)` at
`(n, L, B, net) = (17, 23/5, 9977/10000, 181 directions)`. `23/5 = 4.6` has no retained
covering row; the nearest recorded sides are the T-019 certificates at `229/50` and
`459/100`. A restricted optimum already at or above 17 on an unconverged row loop
refutes this site set only: remaining rows can only raise it.
Adding sites can still lower the covering value, so `23/5` is not barred.
T-019 at `459/100` is unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 17 --side 23/5 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 300 \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-grid-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-grid-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-grid.log
```

`--freeze-family` was not requested.
The 300 s deadline stopped the row loop after 39 rounds with 72 placements still
violated; no column-generation round ran.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `17.331710` |
| Sites / orbits / rows | 5484 / 716 / 10302 |
| LP rounds | 39 |
| Crossing | round 7 (`17.000094`) |
| Wall | 315.0 s |
| `least_covered` | 0.994279 |
| Converged | no (`violated == 72` at stop) |

`devtools.decide_certificate` was not run: the mass is not below 17.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
