# n=11 191/50 T-025-Seeded Auto-Plus-60 Covering Receipt

Status: **site set refuted**. The side stays open.

Session-139 probe: BC-191 auto `(25, 34, 41)` plus count 60, unioned with T-025's
584 atom sites at native side `191/50`,
`(n, L, B, net) = (11, 191/50, 9977/10000, 181 directions)`.
The row loop sat at exactly `11.000000` through LP round 16, then climbed to
`11.020212`. That is the closest session-139 point-atom construction at this
side, still above eleven, and still above the historical 6637-site grid that
sat at exactly eleven. T-025 is unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 11 --side 191/50 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 25,34,41,60 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 600 \
  --seed-certificate cases/n11_threshold_certificate/certificate.json --seed-map scale \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-191-50-t025-auto60-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-191-50-t025-auto60-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-191-50-t025-auto60.log
```

`--freeze-family` was not requested. Column generation added one orbit after the
row loop and stopped; wall 132.3 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `11.020212` |
| Rationalised total | `440811/40000` = `11.020275` |
| Sites / orbits / rows | 7249 / 958 / 7956 |
| Seed sites | 584 |
| LP rounds | 29 |
| Crossing | round 17 (`11.004716`); rounds 3–16 sat at `11.000000` |
| Wall | 132.3 s |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |

`devtools.decide_certificate` was not run: the mass is not below 11.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
