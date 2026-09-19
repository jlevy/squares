# n=18 4679/1000 T-029-Seeded Auto Window-5 Covering Receipt

Status: **retained**. `s(18) >= 4679/1000` is T-030. Canonical bytes:
`packing/cases/n18_fractional_certificate/certificate.json`. The previous
T-029 bytes sit at `certificate-1871-400.json`. T-028 remains at
`certificate-187-40.json`. T-027 remains at `certificate-467-100.json`.

Session-141 H-221 / exp-179: BC-191 auto grids `(32, 43, 54)` unioned
with T-029's 804 atom sites scaled from `1871/400` to `4679/1000`, plus
`--seed-windows 5`, `(n, L, B, net) = (18, 4679/1000, 9977/10000, 181
directions)`. Seed sites 1204. Auto at this side resolved to `(32, 43, 54)`,
the same triple T-029 used. The row loop never crossed 18 and converged at
`17.893285` with `least_covered = 1` (39 LP rounds, 6985 sites / 929 orbits).
`declare_least_cell_mass` then `decide_certificate` accepted both routes at
least cell mass `200001/200000`. sha256
`b62ead6f5b6aed68704487ad6a1b78beb7a3e585676e55825c6f84942c39cd63`.
T-029 at `1871/400` remains the previous n=18 rung. This retain confirms H-221
and does not confirm H-218: n=18 is off that sweep.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 18 --side 4679/1000 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-certificate cases/n18_fractional_certificate/certificate.json --seed-map scale \
  --seed-windows 5 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-039/n18-4679-1000-t029-auto-windows5-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-039/n18-4679-1000-t029-auto-windows5-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-039/n18-4679-1000-t029-auto-windows5-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n18-4679-1000-t029-auto-windows5-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n18-4679-1000-t029-auto-windows5.log
```

The seed path was T-029's live pointer at run time (`1871/400`, 804 atoms).
The live pointer now holds T-030.

Declare then decide:

```bash
uv run --frozen --all-extras --group dev python -m devtools.declare_least_cell_mass \
  campaign/series/series-000-smoke-and-calibration/results/agenda-039/n18-4679-1000-t029-auto-windows5-certificate.json
uv run --frozen --all-extras --group dev python -m devtools.decide_certificate \
  campaign/series/series-000-smoke-and-calibration/results/agenda-039/n18-4679-1000-t029-auto-windows5-certificate.json
```

The case copy is the canonical artifact.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `17.893285` |
| Artifact mass | `71573611/4000000 = 17.89340275` |
| Least cell mass | `200001/200000` |
| Atoms | 957 |
| Sites / orbits / rows | 6985 / 929 / 10098 |
| Seed sites | 1204 |
| LP rounds | 39 |
| Crossing | stayed below 18 |
| Wall | 432.9 s |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |
| Decide | RETAINABLE; interval 36 s, exact 7 s; 3,449,053 boxes, stalled 0 |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
