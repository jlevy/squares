# n=18 117/25 T-019-Seeded Window-Lattice Covering Receipt

Status: **site set refuted, unconverged**. Locked at 18. The side stays open.

Session-139 probe: BC-191 auto `(32, 43, 53)` unioned with T-019's 1184 atom
sites scaled from `459/100` to `117/25`, plus `--seed-windows 5`,
`(n, L, B, net) = (18, 117/25, 9977/10000, 181 directions)`.
Seed sites 1584 = 1184 T-019 plus 400 ceiling-window lattice sites.
The T-019-seeded auto `(32, 43, 54)` without windows converged at exact
mass `18.000043`. Windows on `(32, 43, 53)` sat at `18.000000` from round
10 through the 900 s deadline (57 LP rounds, 495 still violated).
Remaining rows can only raise this value. Adding sites can still lower
it, so `117/25` is not barred. T-027 at `467/100` is unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 18 --side 117/25 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 32,43,53 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 900 \
  --seed-certificate cases/n17_fractional_certificate/certificate.json --seed-map scale \
  --seed-windows 5 \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-117-25-t019-windows5-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-117-25-t019-windows5-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n18-117-25-t019-windows5.log
```

`--freeze` was not requested. The 900 s deadline stopped the row loop
after 57 rounds; no column-generation round ran. Wall 912.6 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `18.000000` |
| Sites / orbits / rows | 7253 / 975 / 18858 |
| Seed sites | 1584 |
| LP rounds | 57 |
| Crossing | round 10 (`18.000000`) |
| Wall | 912.6 s |
| `least_covered` | 0.960216 |
| Converged | no (`violated == 495` at stop) |

`devtools.decide_certificate` was not run: the mass is not below 18.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
