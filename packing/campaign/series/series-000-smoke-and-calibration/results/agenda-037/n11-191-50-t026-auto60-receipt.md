# n=11 191/50 T-026-Seeded Auto-Plus-60 Covering Receipt

Status: **site set refuted**. The side stays open.

Session-139 probe: BC-191 auto `(25, 34, 41)` plus count 60, unioned with
T-026's 1121 fractional-certificate atoms scaled from `381/100` to `191/50`,
`(n, L, B, net) = (11, 191/50, 9977/10000, 181 directions)`.
The T-025-seeded auto-plus-60 construction at this side converged at
`11.020212`; windows dropped that to `11.018646`. Fractional seed converged
at `11.033743` on 8081 sites. Worse than the threshold seed. T-025 and T-026
are unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 11 --side 191/50 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 25,34,41,60 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 600 \
  --seed-certificate cases/n11_fractional_certificate/certificate.json --seed-map scale \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-191-50-t026-auto60-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-191-50-t026-auto60-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-191-50-t026-auto60.log
```

`--freeze-family` was not requested. Column generation added one orbit after the
row loop and stopped; wall 265.4 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `11.033743` |
| Rationalised total | `5516909/500000` = `11.033818` |
| Sites / orbits / rows | 8081 / 1069 / 8324 |
| Seed sites | 1121 |
| LP rounds | 35 |
| Crossing | round 14 (`11.002509`); rounds 5–13 sat at `11.000000` |
| Wall | 265.4 s |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |

`devtools.decide_certificate` was not run: the mass is not below 11.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
