# n=11 191/50 Four-Grid Covering Receipt

Status: **site set refuted**. The side stays open. This is not a superset of the
historical 6637-site grid that sat at exactly eleven.

Session-139 probe on `--grid-counts 26,35,43,48` at
`(n, L, B, net) = (11, 191/50, 9977/10000, 181 directions)`.
BC-191 auto at this side is `(25, 34, 41)` (3365 sites). These counts are a
different named set (6037 sites), not a densification of the historical
`grid` row (6637 sites). Restricted optimum `11.142857` on a converged loop
refutes this site set only. T-025 at this side is unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 11 --side 191/50 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 26,35,43,48 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 600 \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-191-50-grid4-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-191-50-grid4-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-191-50-grid4.log
```

`--freeze-family` was not requested. Column generation added one orbit after the
row loop and stopped; wall 125.8 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `11.142857` |
| Rationalised total | `5571447/500000` = `11.142894` |
| Sites / orbits / rows | 6037 / 810 / 7677 |
| LP rounds | 31 |
| Crossing | round 8 (`11.010582`); rounds 4–7 sat at `11.000000` |
| Wall | 125.8 s |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |

`devtools.decide_certificate` was not run: the mass is not below 11.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
