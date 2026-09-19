# n=11 31/8 T-025-Seeded Auto-Plus-60 Covering Receipt

Status: **site set refuted**. The side stays open.

Session-139 probe: BC-191 auto `(25, 34, 42)` plus count 60, unioned with T-025's
584 atom sites scaled to `31/8`,
`(n, L, B, net) = (11, 31/8, 9977/10000, 181 directions)`.
`31/8 = 3.875` sits 0.002 below the known-best packing at about 3.877.
The row loop crossed eleven at LP round 2 (`11.000000`) and converged at
`11.561186`. Same grid counts and seed as the `77/20` probe, which converged at
`11.456576`. T-025 at `191/50` is unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 11 --side 31/8 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 25,34,42,60 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 600 \
  --seed-certificate cases/n11_threshold_certificate/certificate.json --seed-map scale \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-31-8-t025-auto60-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-31-8-t025-auto60-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-31-8-t025-auto60.log
```

`--freeze-family` was not requested. Column generation added one orbit after the
row loop and stopped; wall 234.3 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `11.561186` |
| Rationalised total | `5780637/500000` = `11.561274` |
| Sites / orbits / rows | 7705 / 1014 / 8892 |
| Seed sites | 584 |
| LP rounds | 38 |
| Crossing | round 2 (`11.000000`) |
| Wall | 234.3 s |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |

`devtools.decide_certificate` was not run: the mass is not below 11.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
