# n=11 191/50 Auto-Plus-60 Covering Receipt

Status: **site set refuted**. The side stays open.

Session-139 probe on `--grid-counts 25,34,41,60` at
`(n, L, B, net) = (11, 191/50, 9977/10000, 181 directions)`.
This is BC-191 auto `(25, 34, 41)` plus one denser count, 6961 sites, a
superset of auto's 3365. It is not known to contain the historical 6637-site
grid that sat at exactly eleven. Restricted optimum `11.106195` on a converged
loop refutes this site set only. T-025 at this side is unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 11 --side 191/50 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 25,34,41,60 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 600 \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-191-50-auto60-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-191-50-auto60-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-191-50-auto60.log
```

`--freeze-family` was not requested. Column generation added one orbit after the
row loop and stopped; wall 84.7 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `11.106195` |
| Rationalised total | `2776561/250000` = `11.106244` |
| Sites / orbits / rows | 6961 / 921 / 6041 |
| LP rounds | 21 |
| Crossing | round 8 (`11.035354`); rounds 3–7 sat at `11.000000` |
| Wall | 84.7 s |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |

More sites than the historical exact-eleven grid, worse restricted optimum.
Site geometry matters more than count here. `devtools.decide_certificate` was
not run.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
