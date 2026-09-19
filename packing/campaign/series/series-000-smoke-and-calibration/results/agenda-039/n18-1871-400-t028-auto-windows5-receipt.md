# n=18 1871/400 T-028-Seeded Auto Window-5 Covering Receipt

Status: **retained**. `s(18) >= 1871/400` is T-029. Canonical bytes:
`packing/cases/n18_fractional_certificate/certificate.json`. The previous
T-028 bytes sit at `certificate-187-40.json`. T-027 remains at
`certificate-467-100.json`.

Session-141 leftover rank 1 / H-219: BC-191 auto grids `(32, 43, 54)` unioned
with T-028's 725 atom sites scaled from `187/40` to `1871/400`, plus
`--seed-windows 5`, `(n, L, B, net) = (18, 1871/400, 9977/10000, 181
directions)`. Seed sites 1125. Auto at this side resolved to `(32, 43, 54)`,
not T-028's `(32, 43, 53)`. The row loop never crossed 18 and converged at
`17.889237` with `least_covered = 1` (56 LP rounds, 6905 sites / 921 orbits).
`declare_least_cell_mass` then `decide_certificate` accepted both routes at
least cell mass `250001/250000`. sha256
`dd06c0e39639f06af475459a2a63f9fc8d5836b0b83ea3b6c3a4de8f212892d4`.
T-028 at `187/40` remains the previous n=18 rung. This retain confirms H-219
and does not confirm H-218: n=18 is off that sweep.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 18 --side 1871/400 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 1200 \
  --seed-certificate cases/n18_fractional_certificate/certificate.json --seed-map scale \
  --seed-windows 5 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-039/n18-1871-400-t028-auto-windows5-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-039/n18-1871-400-t028-auto-windows5-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-039/n18-1871-400-t028-auto-windows5-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n18-1871-400-t028-auto-windows5-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-039/n18-1871-400-t028-auto-windows5.log
```

The seed path was T-028's live pointer at run time (`187/40`, 725 atoms).
The live pointer now holds T-029.

Declare then decide:

```bash
uv run --frozen --all-extras --group dev python -m devtools.declare_least_cell_mass \
  campaign/series/series-000-smoke-and-calibration/results/agenda-039/n18-1871-400-t028-auto-windows5-certificate.json
uv run --frozen --all-extras --group dev python -m devtools.decide_certificate \
  campaign/series/series-000-smoke-and-calibration/results/agenda-039/n18-1871-400-t028-auto-windows5-certificate.json
```

The case copy is the canonical artifact.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `17.889237` |
| Artifact mass | `17889361/1000000 = 17.889361` |
| Least cell mass | `250001/250000` |
| Atoms | 804 |
| Sites / orbits / rows | 6905 / 921 / 12165 |
| Seed sites | 1125 |
| LP rounds | 56 |
| Crossing | stayed below 18 |
| Wall | 650.3 s |
| `least_covered` | 1 |
| Converged | yes (`violated == 0`) |
| Decide | RETAINABLE; interval 28 s, exact 5 s; 2,997,789 boxes, stalled 0 |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
