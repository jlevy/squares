# n=11 191/50 T-025-Seeded Auto-Plus-60 Window-Lattice Covering Receipt

Status: **site set refuted**. The side stays open.

Session-139 probe: the T-025-seeded auto-plus-60 construction at native
`191/50`, plus `--seed-windows 5` (225 ceiling-window lattice sites).
`(n, L, B, net) = (11, 191/50, 9977/10000, 181 directions)`.
Seed sites 809 = 584 T-025 + 225 windows. The same grids without windows
converged at `11.020212` on 7249 sites. Windows dropped that by 0.0016 to
`11.018646` on 7473 sites. Closest session-139 point-atom construction, still
above eleven. T-025 is unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 11 --side 191/50 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 25,34,41,60 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 600 \
  --seed-certificate cases/n11_threshold_certificate/certificate.json --seed-map scale \
  --seed-windows 5 \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-191-50-t025-windows5-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-191-50-t025-windows5-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n11-191-50-t025-windows5.log
```

`--freeze-family` was not requested. Column generation added one orbit after the
row loop and stopped; wall 176.2 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `11.018646` |
| Rationalised total | `5509353/500000` = `11.018706` |
| Sites / orbits / rows | 7473 / 993 / 7832 |
| Seed sites | 809 |
| LP rounds | 35 |
| Crossing | round 17 (`11.008586`); rounds 6–16 sat at `11.000000` |
| Wall | 176.2 s |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |

`devtools.decide_certificate` was not run: the mass is not below 11.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
