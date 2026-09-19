# n=11 77/20 T-025-Seeded Auto-Plus-60 Covering Receipt

Status: **site set refuted**. The side stays open.

Session-139 probe: BC-191 auto `(25, 34, 42)` plus count 60, unioned with T-025's
584 atom sites scaled to `77/20`,
`(n, L, B, net) = (11, 77/20, 9977/10000, 181 directions)`.
`77/20 = 3.85` already has a BC-200 vertex-seeded row (unconverged `11.227631` on
22,625 sites). This is a different site set. The row loop crossed eleven at LP
round 2 (`11.000000`) and converged at `11.456576`. T-025 at `191/50` is unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 11 --side 77/20 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 25,34,42,60 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 600 \
  --seed-certificate cases/n11_threshold_certificate/certificate.json --seed-map scale \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-77-20-t025-auto60-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-77-20-t025-auto60-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-77-20-t025-auto60.log
```

`--freeze-family` was not requested. Column generation added one orbit after the
row loop and stopped; wall 196.0 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `11.456576` |
| Rationalised total | `2864157/250000` = `11.456628` |
| Sites / orbits / rows | 7705 / 1014 / 7194 |
| Seed sites | 584 |
| LP rounds | 26 |
| Crossing | round 2 (`11.000000`) |
| Wall | 196.0 s |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |

`devtools.decide_certificate` was not run: the mass is not below 11.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
