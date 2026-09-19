# n=17 23/5 T-019-Seeded Window-7 Lattice Covering Receipt

Status: **site set refuted, unconverged**. The side stays open.

Session-139 probe: BC-191 auto `(32, 42, 52)` unioned with T-019's 1184 atom
sites scaled from `459/100` to `23/5`, plus `--seed-windows 7`,
`(n, L, B, net) = (17, 23/5, 9977/10000, 181 directions)`.
Seed sites 1968 = 1184 T-019 plus 784 ceiling-window lattice sites.
The same grids with `--seed-windows 5` stopped at `17.042346`; windows 6
stopped at `17.048472`. Windows 7 finished between them: `17.046923` at
the 900 s deadline (42 LP rounds, 186 still violated). Crossed seventeen
at round 19 (`17.001965`). Remaining rows can only raise this value.
Adding sites can still lower it, so `23/5` is not barred. T-019 at
`459/100` is unchanged.

## Command

From `packing/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 17 --side 23/5 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts 32,42,52 --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 60 --deadline-seconds 900 \
  --seed-certificate cases/n17_fractional_certificate/certificate.json --seed-map scale \
  --seed-windows 7 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows7-certificate.json \
  --freeze-family campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows7-family.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows7-run.json \
  --row-log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows7-rows.jsonl \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-037/n17-23-5-t019-windows7.log
```

No freeze file: the 900 s deadline stopped the row loop after 42 rounds.
Wall 904.2 s.

## Covering

| Quantity | Value |
| --- | --- |
| Restricted optimum | `17.046923` |
| Sites / orbits / rows | 7452 / 978 / 12379 |
| Seed sites | 1968 |
| LP rounds | 42 |
| Crossing | round 19 (`17.001965`) |
| Wall | 904.2 s |
| `least_covered` | 0.995294 |
| Converged | no (`violated == 186` at stop) |

`devtools.decide_certificate` was not run: the mass is not below 17.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
