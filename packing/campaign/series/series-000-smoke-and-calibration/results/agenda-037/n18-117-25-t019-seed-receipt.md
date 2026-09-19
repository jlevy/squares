# n=18 117/25 T-019-Seeded Covering Receipt

Status: **converged at mass 18.000043**. No certificate. The side stays open.

Session-139 probe: BC-191 auto `(32, 43, 54)` unioned with T-019's 1184 atom
sites scaled from `459/100` to `117/25`,
`(n, L, B, net) = (18, 117/25, 9977/10000, 181 directions)`.
The row loop converged at `17.999999999552305` with `least_covered` 1
(35 LP rounds, 6965 sites / 922 orbits). Exact total mass
`18000043/1000000 = 18.000043`. Crossed eighteen at round 8. The same
construction certified `467/100` as T-027; here the exact mass is not
strictly below 18. Three earlier site sets at this side also returned
`18.000000`. Adding sites can still lower a restricted optimum, so
`117/25` is not barred. T-027 at `467/100` is unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 18 --side 117/25 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 32,43,54 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 900 \
  --seed-certificate cases/n17_fractional_certificate/certificate.json --seed-map scale \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-117-25-t019-seed-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-117-25-t019-seed-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-117-25-t019-seed.log
```

`--freeze` was not requested. Wall 180.0 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `18.000000` (float `17.999999999552305`) |
| Artifact mass | `18000043/1000000 = 18.000043` |
| Atoms | 172 |
| Sites / orbits / rows | 6965 / 922 / 10990 |
| Seed sites | 1184 |
| LP rounds | 35 |
| Crossing | round 8 (`18.000000`) |
| Wall | 180.0 s |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |

`devtools.decide_certificate` was not run: the mass is not below 18.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
