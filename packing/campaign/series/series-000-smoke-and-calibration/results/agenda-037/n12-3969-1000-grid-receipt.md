# n=12 3969/1000 Grid Covering Receipt

Status: **site set refuted**. The side stays open.

Session-139 probe on BC-191 auto grids `(26, 35, 43)` at
`(n, L, B, net) = (12, 3969/1000, 9977/10000, 181 directions)`.
A restricted optimum at or above 12 on a converged row loop refutes this site set
only. Adding sites can still lower the covering value, so `3969/1000` is not barred.
T-017 at `99/25` is unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 12 --side 3969/1000 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 0 \
  --column-rounds 1 --max-rounds 400 --deadline-seconds 600 \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n12-3969-1000-grid-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n12-3969-1000-grid-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n12-3969-1000-grid.log
```

The freeze paths were requested and not written: after the row loop converged, column
generation priced one extra orbit for 552 s at 99% CPU and was killed past the 600 s
deadline. That pricing round did not change the reported optimum.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `12.363498` |
| Sites / orbits / rows | 3737 / 511 / 5226 |
| LP rounds | 25 |
| Crossing | round 4 (`12.043810`) |
| Row-loop wall | 86.8 s |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |

`devtools.decide_certificate` was not run: the mass is not below 12.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
