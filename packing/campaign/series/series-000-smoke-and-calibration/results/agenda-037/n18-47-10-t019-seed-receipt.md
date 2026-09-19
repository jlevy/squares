# n=18 47/10 T-019-Seeded Covering Receipt

Status: **converged above 18**. No certificate. The side stays open.

Session-139 probe: BC-191 auto `(33, 44, 54)` unioned with T-019's 1184 atom
sites scaled from `459/100` to `47/10`,
`(n, L, B, net) = (18, 47/10, 9977/10000, 181 directions)`.
The row loop converged at `18.165413` with `least_covered` 1
(44 LP rounds, 7117 sites / 939 orbits). Exact total mass
`18165509/1000000 = 18.165509`. Crossed eighteen at round 7. Remaining
rows can only raise this value. Adding sites can still lower it, so
`47/10` is not barred. T-027 at `467/100` is unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 18 --side 47/10 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 33,44,54 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 900 \
  --seed-certificate cases/n17_fractional_certificate/certificate.json --seed-map scale \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-47-10-t019-seed-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-47-10-t019-seed-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-47-10-t019-seed.log
```

`--freeze` was not requested. Wall 390.4 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `18.165413` |
| Artifact mass | `18165509/1000000 = 18.165509` |
| Atoms | 636 |
| Sites / orbits / rows | 7117 / 939 / 11265 |
| Seed sites | 1184 |
| LP rounds | 44 |
| Crossing | round 7 (`18.000000`) |
| Wall | 390.4 s |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |

`devtools.decide_certificate` was not run: the mass is not below 18.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
